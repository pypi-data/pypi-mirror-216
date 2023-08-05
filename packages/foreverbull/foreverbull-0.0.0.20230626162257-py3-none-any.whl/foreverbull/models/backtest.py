from datetime import datetime, timezone
from typing import List, Optional

import pandas as pd

from foreverbull.models.service import Database, SocketConfig

from .base import Base
from .service import Parameter


class Execution(Base):
    execution: str
    start_time: datetime
    end_time: datetime
    database: Optional[Database]
    parameters: Optional[List[Parameter]]
    socket: SocketConfig


class Backtest(Base):
    class Configuration(Base):
        start_time: datetime
        end_time: datetime
        symbols: List[str]

    backtest_service: str
    config: Configuration
    execution_type: str = "manual"


class IngestConfig(Base):
    calendar: Optional[str]
    start_time: Optional[datetime]
    end_time: Optional[datetime]
    symbols: List[str]


class EngineConfig(Base):
    calendar: str
    start_time: datetime
    end_time: datetime
    benchmark: Optional[str] = None
    symbols: List[str]


class Period(Base):
    period: datetime
    shorts_count: Optional[int]
    pnl: Optional[int]
    long_value: Optional[int]
    short_value: Optional[int]
    long_exposure: Optional[int]
    starting_exposure: Optional[int]
    short_exposure: Optional[int]
    capital_used: Optional[int]
    gross_leverage: Optional[int]
    net_leverage: Optional[int]
    ending_exposure: Optional[int]
    starting_value: Optional[int]
    ending_value: Optional[int]
    starting_cash: Optional[int]
    ending_cash: Optional[int]
    returns: Optional[int]
    portfolio_value: Optional[int]
    longs_count: Optional[int]
    algo_volatility: Optional[int]
    sharpe: Optional[int]
    alpha: Optional[int]
    beta: Optional[int]
    sortino: Optional[int]
    max_drawdown: Optional[int]
    max_leverage: Optional[int]
    excess_return: Optional[int]
    treasury_period_return: Optional[int]
    benchmark_period_return: Optional[int]
    benchmark_volatility: Optional[int]
    algorithm_period_return: Optional[int]

    @classmethod
    def from_backtest(cls, period):
        return Period(
            period=period["period_open"].to_pydatetime().replace(tzinfo=timezone.utc),
            shorts_count=int(period["shorts_count"] * 100),
            pnl=int(period["pnl"] * 100),
            long_value=int(period["long_value"] * 100),
            short_value=int(period["short_value"] * 100),
            long_exposure=int(period["long_exposure"] * 100),
            starting_exposure=int(period["starting_exposure"] * 100),
            short_exposure=int(period["short_exposure"] * 100),
            capital_used=int(period["capital_used"] * 100),
            gross_leverage=int(period["gross_leverage"] * 100),
            net_leverage=int(period["net_leverage"] * 100),
            ending_exposure=int(period["ending_exposure"] * 100),
            starting_value=int(period["starting_value"] * 100),
            ending_value=int(period["ending_value"] * 100),
            starting_cash=int(period["starting_cash"] * 100),
            ending_cash=int(period["ending_cash"] * 100),
            returns=int(period["returns"] * 100),
            portfolio_value=int(period["portfolio_value"] * 100),
            longs_count=int(period["longs_count"] * 100),
            algo_volatility=None if pd.isnull(period["algo_volatility"]) else int(period["algo_volatility"] * 100),
            sharpe=None if pd.isnull(period["sharpe"]) else int(period["sharpe"] * 100),
            alpha=None if period["alpha"] is None or pd.isnull(period["alpha"]) else int(period["alpha"] * 100),
            beta=None if period["beta"] is None or pd.isnull(period["beta"]) else int(period["beta"] * 100),
            sortino=None if pd.isnull(period["sortino"]) else int(period["sortino"] * 100),
            max_drawdown=None if pd.isnull(period["max_drawdown"]) else int(period["max_drawdown"] * 100),
            max_leverage=None if pd.isnull(period["max_leverage"]) else int(period["max_leverage"] * 100),
            excess_return=None if pd.isnull(period["excess_return"]) else int(period["excess_return"] * 100),
            treasury_period_return=None
            if pd.isnull(period["treasury_period_return"])
            else int(period["treasury_period_return"] * 100),
            benchmark_period_return=None
            if pd.isnull(period["benchmark_period_return"])
            else int(period["benchmark_period_return"] * 100),
            benchmark_volatility=None
            if pd.isnull(period["benchmark_volatility"])
            else int(period["benchmark_volatility"] * 100),
            algorithm_period_return=None
            if pd.isnull(period["algorithm_period_return"])
            else int(period["algorithm_period_return"] * 100),
        )


class Result(Base):
    periods: List[Period]
