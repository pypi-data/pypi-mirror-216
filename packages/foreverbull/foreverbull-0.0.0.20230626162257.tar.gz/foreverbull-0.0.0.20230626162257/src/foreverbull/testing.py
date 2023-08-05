import socket
import time

import pytest

from foreverbull import Foreverbull, broker, models
from foreverbull.broker.socket.client import SocketClient
from foreverbull.models.service import Request, SocketConfig, SocketType


class Execution:
    def __init__(self):
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

    def setup(self, **routes):
        self._fb.setup(**routes)

    def configure(self, backtest: models.backtest.Backtest):
        broker.finance.create_assets(backtest.config.symbols)
        broker.finance.create_ohlc(backtest.config.symbols, backtest.config.start_time, backtest.config.end_time)

        backtest = broker.backtest.create(backtest)
        self._backtest_id = backtest["id"]
        while backtest["stage"] != "RUNNING":
            if backtest["error"]:
                raise Exception("backtest failed to start: ", backtest["error"])
            time.sleep(0.2)
            backtest = broker.backtest.get(self._backtest_id)
        socket_config = SocketConfig(
            host="127.0.0.1",
            port=27015,
            socket_type=SocketType.REQUESTER,
            listen=False,
            recv_timeout=10000,
            send_timeout=10000,
        )
        socket = SocketClient(socket_config)
        self._ctx_socket = socket.new_context()
        self._ctx_socket.send(Request(task="get_configuration"))
        rsp = self._ctx_socket.recv()
        configuration = models.backtest.Execution(**rsp.data)
        self._fb.configure(configuration)

    def run(self):
        self._fb.run_backtest()
        self._ctx_socket.send(Request(task="start"))
        self._ctx_socket.recv()
        self._ctx_socket.send(Request(task="stop"))
        self._ctx_socket.recv()
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
