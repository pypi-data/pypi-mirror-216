from math import ceil

from finbourne_lab.luminesce.experiment import LumiExperiment
from finbourne_lab.luminesce.lusid.base import LusidLumiLabBase


class LusidLumiLabRead(LusidLumiLabBase):

    def __init__(self, atlas, verbose=False, skip_checks=False):
        super().__init__(atlas, verbose, skip_checks)

    def lusid_portfolio_read_measurement(self, **kwargs):
        """Make an experiment for measuring the performance of lusid.portfolio

        Keyword Args:
            rows_rng (Union[int, List[int]]): the range to sample when getting x-many rows. Given as a list containing
            two integers or a const int value. Defaults to [1, 400].

        Returns:
            LumiExperiment: experiment object for the lusid.portfolio measurement.

        """
        rows_rng = kwargs.get('rows_rng', [1, 400])
        return self._reader_experiment('lusid_read_portfolio', self.atlas.lusid_portfolio, rows_rng, None)

    def lusid_instrument_read_measurement(self, **kwargs):
        """Make an experiment for measuring the performance of lusid.instrument

        Keyword Args:
            rows_rng (Union[int, List[int]]): the range to sample when getting x-many rows. Given as a list containing
            two integers or a const int value. Defaults to [1, 10000].

        Returns:
            LumiExperiment: experiment object for the lusid.instrument measurement.

        """
        rows_rng = kwargs.get('rows_rng', [1, 10000])
        return self._reader_experiment('lusid_read_instrument', self.atlas.lusid_instrument, rows_rng, None)

    def lusid_portfolio_txn_read_measurement(self, **kwargs):
        """Make a list of experiments for measuring the performance of lusid.portfolio.txn over different shape of data.

        Keyword Args:
            rows_rng (Union[int, List[int]]): the range to sample when getting x-many rows. Given as a list containing
            two integers or a const int value. Defaults to [1, 10000].
            force_ensure (bool): whether to force the ensure step. Defaults to False.
            txns_per_pf_set (Set[int]): a set of integers that define the different data shapes to test for. Each value
            is the number of txns per portfolio. Defaults to 100, 1000, 10000.

        Notes:
            Data shape is the number of portfolios the txns are spread over. This is parameterised as the number of txns
            per portfolio in a scope. A test scope will be created for a given shape for each experiment.


        Returns:
            List[LumiExperiment]: experiment list for measuring txn read performance over different shaped data.

        """
        force_ensure = kwargs.get('force_ensure', False)
        rows_rng = kwargs.get('rows_rng', [1, 10000])
        rows_max = max(rows_rng)

        self._ensure_instruments(rows_max)

        txns_per_pf_set = kwargs.get('txns_per_pf', [10000, 1000, 100])

        experiments = []

        txn = self.atlas.lusid_portfolio_txn()

        for txns_per_pf in txns_per_pf_set:
            name = f'lusid_read_txn_{txns_per_pf}'
            scope = f'fbnlab_{name}'

            n_portfolios = ceil(rows_max / txns_per_pf)
            self._ensure_portfolios(n_portfolios, scope, force_ensure)
            self._ensure_txns(n_portfolios, txns_per_pf, scope, force_ensure)

            def build(x, s):
                return txn.select('*').where(txn.portfolio_scope == s).limit(x)

            ex = LumiExperiment(name, build, rows_rng, scope)
            experiments.append(ex)

        return experiments

    def lusid_portfolio_holding_read_measurement(self, **kwargs):
        """Make a list of experiments for measuring the performance of lusid.portfolio.holding over different shape of data.

        Keyword Args:
            rows_rng (Union[int, List[int]]): the range to sample when getting x-many rows. Given as a list containing
            two integers or a const int value. Defaults to [1, 10000].
            force_ensure (bool): whether to force the ensure step. Defaults to False.
            hlds_per_pf_set (Set[int]): a set of integers that define the different data shapes to test for. Each value
            is the number of holdings per portfolio. Defaults to 100, 1000, 10000.

        Notes:
            Data shape is the number of portfolios the holdings are spread over. This is parameterised as the number of
            holdings per portfolio in a scope. A test scope will be created for a given shape for each experiment.


        Returns:
            List[LumiExperiment]: experiment list for measuring holdings read performance over different shaped data.

        """
        force_ensure = kwargs.get('force_ensure', False)
        rows_rng = kwargs.get('rows_rng', [1, 10000])
        rows_max = max(rows_rng)

        self._ensure_instruments(rows_max)

        hlds_per_pf_set = kwargs.get('hlds_per_pf', [10000, 1000, 100])

        experiments = []

        hld = self.atlas.lusid_portfolio_holding()

        for hlds_per_pf in hlds_per_pf_set:
            name = f'lusid_read_hld_{hlds_per_pf}'
            scope = f'fbnlab_{name}'

            n_portfolios = ceil(rows_max / hlds_per_pf)
            self._ensure_portfolios(n_portfolios, scope, force_ensure)
            self._ensure_holdings(n_portfolios, hlds_per_pf, scope, force_ensure)

            def build(x, s):
                return hld.select('*').where(hld.portfolio_scope == s).limit(x)

            ex = LumiExperiment(name, build, rows_rng, scope)
            experiments.append(ex)

        return experiments
