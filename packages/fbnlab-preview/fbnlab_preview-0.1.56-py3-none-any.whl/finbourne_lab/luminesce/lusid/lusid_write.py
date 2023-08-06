import string
from math import ceil
import numpy as np

from finbourne_lab.luminesce.experiment import LumiExperiment
from finbourne_lab.luminesce.lusid.base import LusidLumiLabBase


class LusidLumiLabWrite(LusidLumiLabBase):

    def __init__(self, atlas, verbose=False, skip_checks=False):

        required = [
            "lusid_portfolio",
            "lusid_instrument",
            "lusid_portfolio_holding",
            "lusid_portfolio_txn",
            "lab_testdata_lusid_holding",
            "lab_testdata_lusid_instrument",
            "lab_testdata_lusid_portfolio",
            "lab_testdata_lusid_transaction",
        ]

        missing = [r for r in required if not hasattr(atlas, r)]
        if len(missing) > 0:
            missing_str = '\n  '.join(missing)
            raise ValueError(f'Atlas is missing required providers:\n  {missing_str}')

        super().__init__(atlas, verbose, skip_checks)

    def lusid_instrument_writer_measurement(self, **kwargs):
        """Make a pair of experiments (one main, one baseline) for the instrument writer measurement.

        Notes:
            The baseline experiment measures the time to read out test data into a table var before going to the writer.
            The main step is the test data read + writer call. To measure the writer the baseline result should be
            subtracted from the main

        Keyword Args:
            rows_rng (Union[int, List[int]]): the range to sample when getting x-many rows. Given as a list containing
            two integers or a const int value. Defaults to [1, 1000].

        Returns:
            List[LumiExperiment]: a pair of experiments for the measurement (main, base).

        """
        rows_rng = kwargs.get('rows_rng', [1, 1000])
        ins = self.atlas.lab_testdata_lusid_instrument()

        def baseline(x):
            tv = ins.select('*', Scope=self._make_write_scope('instrument')).limit(x).to_table_var()
            return tv.select('*').limit(1)

        def build(x):
            tv = ins.select('*', Scope=self._make_write_scope('instrument')).limit(x).to_table_var()
            writer = self.atlas.lusid_instrument_writer(to_write=tv)
            return writer.select('*')

        name = 'lusid_write_instrument'
        ex = LumiExperiment(name, build, rows_rng)
        base = LumiExperiment(name + '_base', baseline, rows_rng)
        return ex, base

    def lusid_portfolio_writer_measurement(self, **kwargs):
        """Make a pair of experiments (one main, one baseline) for the portfolio writer measurement.

        Notes:
            The baseline experiment measures the time to read out test data into a table var before going to the writer.
            The main step is the test data read + writer call. To measure the writer the baseline result should be
            subtracted from the main

        Keyword Args:
            rows_rng (Union[int, List[int]]): the range to sample when getting x-many rows. Given as a list containing
            two integers or a const int value. Defaults to [1, 25].

        Returns:
            List[LumiExperiment]: a pair of experiments for the measurement (main, base).

        """
        rows_rng = kwargs.get('rows_rng', [1, 25])

        def baseline(x):
            pf_data = self.atlas.lab_testdata_lusid_portfolio(scope=self._make_write_scope('portfolio'))
            tv = pf_data.select('*').limit(x).to_table_var()
            return tv.select('*').limit(1)

        def build(x):
            pf_data = self.atlas.lab_testdata_lusid_portfolio(scope=self._make_write_scope('portfolio'))
            tv = pf_data.select('*').limit(x).to_table_var()
            writer = self.atlas.lusid_portfolio_writer(to_write=tv)
            return writer.select('*')

        name = 'lusid_write_portfolio'
        ex = LumiExperiment(name, build, rows_rng)
        base = LumiExperiment(name + '_base', baseline, rows_rng)
        return ex, base

    def lusid_portfolio_holding_writer_measurement(self, **kwargs):
        """Make a list of experiments for the portfolio holdings writer measurement over different data shapes.

        Notes:
            The baseline experiment measures the time to read out test data into a table var before going to the writer.
            The main step is the test data read + writer call. To measure the writer the baseline result should be
            subtracted from the main

            Data shape is the number of portfolios the holdings are spread over. This is parameterised as the number of
            holdings per portfolio in a scope. A clean test scope will be created for a given shape for each write.

        Keyword Args:
            rows_rng (Union[int, List[int]]): the range to sample when getting x-many rows. Given as a list containing
            two integers or a const int value. Defaults to [1, 10000].
            force_ensure (bool): whether to force the ensure step. Defaults to False.
            hldg_per_pf_set (Set[int]): a set of integers that define the different data shapes to test for. Each value
            is the number of holdings per portfolio. Defaults to 100, 1000, 10000.

        Returns:
            List[LumiExperiment]: a list of experiments containing the main and base for each data shape.

        """

        force_ensure = kwargs.get('force_ensure', False)
        rows_rng = kwargs.get('rows_rng', [1, 10000])
        hldg_per_pf_set = kwargs.get('hldg_per_pf_set', {100, 1000, 10000})

        experiments = []
        for hldg_per_pf in hldg_per_pf_set:
            def build(x, y):
                scope = self._make_write_scope('holding')
                n_portfolios = ceil(x / y)

                self._ensure_portfolios(n_portfolios, scope, force_ensure)
                self._ensure_instruments(y)

                tv = self.atlas.lab_testdata_lusid_holding(
                    scope=scope,
                    num_portfolios=n_portfolios,
                    instruments_per_portfolio=int(y),
                    effective_ats_per_instrument=1,
                    luids=self._luids_query(y).to_table_var()
                ).select('*').limit(x).to_table_var()

                writer = self.atlas.lusid_portfolio_holding_writer(to_write=tv)
                return writer.select('*')

            def baseline(x, y):
                tv = self.atlas.lab_testdata_lusid_holding(
                    scope=self._make_write_scope('holding'),
                    num_portfolios=ceil(x / y),
                    instruments_per_portfolio=int(y),
                    effective_ats_per_instrument=1,
                    luids=self._luids_query(y).to_table_var()
                ).select('*').limit(x).to_table_var()
                return tv.select('*').limit(1)

            name = f'lusid_write_holding_{hldg_per_pf}'
            ex = LumiExperiment(name, build, rows_rng, hldg_per_pf)
            experiments.append(ex)
            base = LumiExperiment(name + '_base', baseline, rows_rng, hldg_per_pf)
            experiments.append(base)

        return experiments

    def lusid_portfolio_txn_writer_measurement(self, **kwargs):
        """Make a list of experiments for the portfolio txns writer measurement over different data shapes.

        Notes:
            The baseline experiment measures the time to read out test data into a table var before going to the writer.
            The main step is the test data read + writer call. To measure the writer the baseline result should be
            subtracted from the main

            Data shape is the number of portfolios the txns are spread over. This is parameterised as the number of
            txns per portfolio in a scope. A clean test scope will be created for a given shape for each write.

        Keyword Args:
            rows_rng (Union[int, List[int]]): the range to sample when getting x-many rows. Given as a list containing
            two integers or a const int value. Defaults to [1, 10000].
            force_ensure (bool): whether to force the ensure step. Defaults to False.
            txns_per_pf_set (Set[int]): a set of integers that define the different data shapes to test for. Each value
            is the number of txns per portfolio. Defaults to 100, 1000, 10000.

        Returns:
            List[LumiExperiment]: a list of experiments containing the main and base for each data shape.

        """

        force_ensure = kwargs.get('force_ensure', False)
        rows_rng = kwargs.get('rows_rng', [1, 10000])
        txns_per_pf_set = kwargs.get('txns_per_pf_set', {100, 1000, 10000})

        experiments = []
        for txns_per_pf in txns_per_pf_set:
            def build(x, y):
                scope = self._make_write_scope('txn')
                n_portfolios = ceil(x / y)

                self._ensure_portfolios(n_portfolios, scope, force_ensure)
                self._ensure_instruments(y)

                tv = self.atlas.lab_testdata_lusid_transaction(
                    scope=scope,
                    num_portfolios=n_portfolios,
                    instruments_per_portfolio=int(y),
                    txns_per_instrument=1,
                    luids=self._luids_query(y).to_table_var()
                ).select('*').limit(x).to_table_var()

                writer = self.atlas.lusid_portfolio_txn_writer(to_write=tv)
                return writer.select('*')

            def baseline(x, y):
                tv = self.atlas.lab_testdata_lusid_transaction(
                    scope=self._make_write_scope('txn'),
                    num_portfolios=ceil(x / y),
                    instruments_per_portfolio=int(y),
                    txns_per_instrument=1,
                    luids=self._luids_query(y).to_table_var()
                ).select('*').limit(x).to_table_var()
                return tv.select('*').limit(1)

            name = f'lusid_write_txn_{txns_per_pf}'
            ex = LumiExperiment(name, build, rows_rng, txns_per_pf)
            experiments.append(ex)
            base = LumiExperiment(name + '_base', baseline, rows_rng, txns_per_pf)
            experiments.append(base)

        return experiments

    def _make_write_scope(self, label: str) -> str:
        letters = list(string.ascii_lowercase + string.digits)
        rand_id = ''.join(np.random.choice(letters, size=8))
        return f'fbnlab-{label}-writer-{rand_id}'
