from finbourne_lab.luminesce.base import BaseLumiLab


class LusidLumiLabBase(BaseLumiLab):
    """The lusid lumi lab encapsulates standard measurements for lusid luminesce providers.

    """

    def __init__(self, atlas, verbose=False, skip_checks=False):
        """Creator for the LusidLumiLab class.

        Args:
            atlas (Atlas): the lumipy atlas to run luminesce queries with.
            verbose (bool): whether to run in verbose mode. This will give feedback on ensure (entity) steps
            during running. Defaults to false.
            skip_checks (bool): whether to skip ensure (instruments/portfolios/holdings/txns). Defaults to false.

        """

        self.skip_checks = skip_checks
        super().__init__(atlas, verbose)

    def _luids_query(self, row_lim: int):
        inst = self.atlas.lusid_instrument()
        return inst.select(
            inst.lusid_instrument_id, inst.client_internal
        ).limit(row_lim)

    def _ensure_instruments(self, row_lim: int):
        if self.skip_checks:
            return

        self.log('Checking instruments', 2)
        inst_df = self._luids_query(row_lim).go(quiet=True)

        if inst_df.shape[0] >= row_lim:
            self.log('All present', 4)
            return

        self.log('Creating instruments', 2)
        tv = self.atlas.lab_testdata_lusid_instrument().select('*').limit(row_lim).to_table_var()
        self.atlas.lusid_instrument_writer(to_write=tv).select('^').limit(1).go(quiet=True)
        self.log('Done', 4)

    def _ensure_portfolios(self, n_portfolios: int, scope: str, force: bool):
        if self.skip_checks:
            return

        self.log(f'Checking portfolios in {scope}', 2)
        pf = self.atlas.lusid_portfolio()
        p_df = pf.select(pf.portfolio_scope).where(pf.portfolio_scope == scope).go(quiet=True)

        if p_df.shape[0] >= n_portfolios and not force:
            self.log('All present', 4)
            return

        self.log('Creating portfolios', 2)
        tv = self.atlas.lab_testdata_lusid_portfolio(
            scope=scope
        ).select('*').limit(n_portfolios).to_table_var()

        write = self.atlas.lusid_portfolio_writer(to_write=tv)
        write.select('^').limit(1).go(quiet=True)
        self.log('Done', 4)

    def _ensure_txns(self, n_portfolios: int, txns_per_pf: int, scope: str, force: bool):
        if self.skip_checks:
            return

        self.log(f'Checking txns in {scope}', 2)
        tx = self.atlas.lusid_portfolio_txn()
        t_df = tx.select(
            tx.portfolio_code
        ).where(
            tx.portfolio_scope == scope
        ).group_by(
            tx.portfolio_code
        ).agg(
            N=tx.portfolio_code.count()
        ).go(quiet=True)

        if t_df.shape[0] == n_portfolios and all(c == txns_per_pf for c in t_df['N']) and not force:
            self.log('All present', 4)
            return

        tv = self.atlas.lab_testdata_lusid_transaction(
            scope=scope,
            num_portfolios=n_portfolios,
            instruments_per_portfolio=txns_per_pf,
            txns_per_instrument=1,
            luids=self._luids_query(txns_per_pf).to_table_var()
        ).select('*').to_table_var()

        w = self.atlas.lusid_portfolio_txn_writer(to_write=tv)
        q = w.select(w.write_error_code, w.write_error_detail).where(w.write_error_code != 0)

        self.log(f'Creating txns', 2)
        df = q.go(quiet=True)
        if df.shape[0] > 0:
            err_msgs = '\n'.join(df.WriteErrorDetail.iloc[:5])
            raise ValueError(
                f'The txns write contained {df.shape[0]} errors:\n{err_msgs}'
            )
        self.log('Done', 4)

    def _ensure_holdings(self, n_portfolios: int, n_holdings: int, scope: str, force: bool):
        if self.skip_checks:
            return

        self.log(f'Checking holdings in {scope}', 2)
        hld = self.atlas.lusid_portfolio_holding()
        h_df = hld.select(
            hld.portfolio_code
        ).where(
            hld.portfolio_scope == scope
        ).group_by(
            hld.portfolio_code
        ).agg(
            N=hld.portfolio_code.count()
        ).go(quiet=True)

        if h_df.shape[0] == n_portfolios and all(c == n_holdings for c in h_df['N']) and not force:
            self.log('All present', 4)
            return

        tv = self.atlas.lab_testdata_lusid_holding(
            scope=scope,
            num_portfolios=n_portfolios,
            instruments_per_portfolio=n_holdings,
            effective_ats_per_instrument=1,
            luids=self._luids_query(n_holdings).to_table_var(),
        ).select('*').to_table_var()

        w = self.atlas.lusid_portfolio_holding_writer(to_write=tv)
        q = w.select(w.write_error_code, w.write_error_detail).where(w.write_error_code != 0)

        self.log('Creating holdings', 2)
        df = q.go(quiet=True)
        if df.shape[0] > 0:
            err_msgs = '\n'.join(df.WriteErrorDetail.iloc[:5])
            raise ValueError(
                f'The holdings write contained {df.shape[0]} errors:\n{err_msgs}'
            )
        self.log('Done', 4)
