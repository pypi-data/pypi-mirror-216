import numpy as np
import pandas as pd
from typing import Callable, Any
from finbourne_lab.common.experiment import Experiment
from lumipy.lumiflex._common.str_utils import to_snake_case


class LumiExperiment(Experiment):
    """Experiment class for running luminesce experiments.

    """

    def __init__(self, name: str, build_fn: Callable, *ranges: Any, **metadata: Any):
        """Constructor of the LumiExperiment class.

        Args:
            name (str): name of the luminesce experiment
            build_fn (Callable): build function of the luminesce experiment. Must return a query object given some values.
            *ranges (Any): parameter value ranges. Must be either constant values, pair of integers or a set of values.
            **metadata (Any): other values to be attached to observations.

        Keyword Args:
              keep_for (int): time to keep query results for. Defaults to 900s.
              check_period (float): wait period before checking a query status. Defaults to 0.025s
              skip_download (bool): whether to skip the download step. Defaults to true.

        """

        self.keep_for = metadata.get('keep_for', 900)
        self.check_period = metadata.get('check_period', 0.025)
        self.skip_download = metadata.get('skip_download', True)

        super().__init__(name, build_fn, *ranges, **metadata)

    def measurement(self, obs, runnable):
        qry = runnable

        obs.log_time('send')
        job = qry.go_async(keep_for=self.keep_for)
        obs['execution_id'] = job.ex_id
        obs.log_time('submitted')
        obs['start_query_time'] = (obs['submitted'] - obs['send']).total_seconds()

        job.interactive_monitor(True, self.check_period)

        obs.log_time('get')
        obs['query_time'] = (obs['get'] - obs['submitted']).total_seconds()

        def make_pair(x):
            lhs, rhs = x.split(':')
            name = ''.join(s for s in lhs.strip() if s.isalnum()).title() + 'Time'
            val = float(rhs.strip().strip(' ms')) * 0.001
            return to_snake_case(name), val

        server_side = {}
        arr = [line for line in job.get_progress().split('\n') if ' ms' in line]
        for time_name, time_val in map(make_pair, arr):
            server_side[time_name] = time_val

        ss_cols = ['prep_time', 'providers_time', 'mergesql_time', 'filltable_time', 'total_time']
        for col in ss_cols:
            if col not in server_side:
                obs[col] = np.NaN
            else:
                obs[col] = server_side[col]

        if self.skip_download:
            obs['download_finish'] = pd.NaT
            obs['obs_rows'] = None
            obs['obs_cols'] = None
            obs['download_time'] = None
            return

        df = job.get_result(False)
        obs.log_time('download_finish')
        obs['obs_rows'] = df.shape[0]
        obs['obs_cols'] = df.shape[1]
        obs['download_time'] = (obs['download_finish'] - obs['get']).total_seconds()
