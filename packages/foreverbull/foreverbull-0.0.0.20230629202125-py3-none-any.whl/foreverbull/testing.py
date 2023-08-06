import socket
import time

import pytest

from foreverbull import Foreverbull, broker, models
from foreverbull.broker.socket.client import SocketClient
from foreverbull.models.service import Request, SocketConfig, SocketType


class Execution:
    def __init__(self):
        self._socket: SocketClient = None
        self._backtest_id = None
        self._strategy = None
        self._worker_pool = None
        self._local_host = socket.gethostbyname(socket.gethostname())
        self._fb = None

    def __enter__(self):
        self._fb = Foreverbull(local_host=self._local_host)
        self._fb.start()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._fb.stop()

    def setup(self, backtest: models.backtest.Backtest, **routes):
        self._fb.setup(**routes)
        manual = broker.backtest.create_manual(backtest.backtest_service)
        manual_id = manual["id"]
        while manual["stage"] != "RUNNING":
            if manual["error"]:
                raise Exception("manual failed to start: ", manual["error"])
            time.sleep(0.2)
            manual = broker.backtest.get_manual(manual_id)
        socket_config = SocketConfig(
            host="127.0.0.1",
            port=manual["socket"]["port"],
            socket_type=SocketType.REQUESTER,
            listen=False,
            recv_timeout=10000,
            send_timeout=10000,
        )
        self._socket = SocketClient(socket_config)
        ctx_socket = self._socket.new_context()

        ingest_config = models.backtest.IngestConfig(
            calendar="NYSE",
            start_time=backtest.config.start_time,
            end_time=backtest.config.end_time,
            symbols=backtest.config.symbols,
        )
        ctx_socket.send(Request(task="ingest", data=ingest_config))
        rsp = ctx_socket.recv()
        print("RSP: ", rsp)
        assert rsp.task == "ingest"

        ctx_socket.close()
        return

    def configure(self, backtest: models.backtest.Backtest):
        ctx_socket = self._socket.new_context()
        ctx_socket.send(Request(task="new_backtest", data=backtest))
        rsp = ctx_socket.recv()
        print("RSP: ", rsp)
        self._backtest_id = rsp.data["id"]

        ctx_socket.send(Request(task="get_configuration"))
        rsp = ctx_socket.recv()
        configuration = models.backtest.Execution(**rsp.data)
        self._fb.configure(configuration)

    def run(self):
        self._fb.run_backtest()
        ctx_socket = self._socket.new_context()
        ctx_socket.send(Request(task="run"))
        ctx_socket.recv()
        ctx_socket.send(Request(task="stop"))
        ctx_socket.recv()
        for _ in range(10):
            # Seems like we are a bit too fast sometimes
            try:
                return self._fb.get_backtest_result(self._backtest_id)
            except Exception:
                time.sleep(0.2)
        raise Exception("backtest finish, but could not find results")


@pytest.fixture(scope="function")
def execution():
    execution = Execution()
    with execution:
        yield execution
