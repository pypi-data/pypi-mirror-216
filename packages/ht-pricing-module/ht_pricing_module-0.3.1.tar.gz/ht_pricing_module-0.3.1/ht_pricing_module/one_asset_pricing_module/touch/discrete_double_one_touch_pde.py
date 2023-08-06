from ht_pricing_module.one_asset_pricing_module.one_asset_option_base import CrankNicolsonEuropean, tqdm, np, math, interpolate


class DiscreteDoubleOneTouchPde(CrankNicolsonEuropean):

    def __init__(self, S, t, T, r, q, sigma, LH, UH, Lrbt, Urbt, year_base,
                 T_LKO=None, T_UKO=None, Ns=None, Nt=None, Smin=None, Smax=None, theta=1):
        self.S = S
        self.LH = LH
        self.UH = UH
        self.r = r
        self.q = q
        self.sigma = sigma
        self.t = t
        self.T = T
        self.year_base = year_base
        self.Lrbt = Lrbt
        self.Urbt = Urbt
        self.T_LKO = (np.array([]) if T_LKO is None else T_LKO) / self.year_base
        self.T_UKO = (np.array([]) if T_UKO is None else T_UKO) / self.year_base

        self.Smin = 0 if Smin is None else Smin
        self.Smax = 4 * max(S, self.UH) if Smax is None else Smax
        self.Ns = 1000 if Ns is None else int(Ns)
        self.Nt = int((T - t) * 1) if Nt is None else int(Nt)

        self._LPaE = True
        self._UPaE = True
        self._theta = theta

    def _set_terminal_condition_(self):
        pass

    def _set_boundary_condition_(self):
        tau = self.Tvec[-1] - self.Tvec
        LDF = np.exp(-self.r * tau * int(self._LPaE))
        UDF = np.exp(-self.r * tau * int(self._UPaE))

        if not np.isscalar(self.Lrbt):
            f = interpolate(x=self.T_LKO, y=self.Lrbt, kind='next', bounds_error=False, fill_value=(self.Lrbt[0], self.Lrbt[-1]))
            self.grid[0, :] = f(self.Tvec) * LDF
        else:
            self.grid[0, :] = self.Lrbt * LDF

        if not np.isscalar(self.Urbt):
            f = interpolate(x=self.T_UKO, y=self.Urbt, kind='next', bounds_error=False, fill_value=(self.Urbt[0], self.Urbt[-1]))
            self.grid[-1, :] = f(self.Tvec) * UDF
        else:
            self.grid[-1, :] = self.Urbt * UDF

    def _solve_(self):
        invM = np.linalg.inv(self._M2)

        KO_idx_down = np.searchsorted(self.Tvec.round(8), self.T_LKO.round(8))
        KO_idx_up = np.searchsorted(self.Tvec.round(8), self.T_UKO.round(8))

        update_bool_idx1 = (self.Svec <= self.LH)
        update_bool_idx2 = (self.Svec >= self.UH)

        tau_l = self.Tvec[-1] - self.T_LKO
        tau_u = self.Tvec[-1] - self.T_UKO
        rbt_l = self.Lrbt * np.exp(-self.r * tau_l * int(self._LPaE))
        rbt_u = self.Urbt * np.exp(-self.r * tau_u * int(self._UPaE))

        for j in tqdm(list(reversed(np.arange(self.Nt))), leave=False):

            if j + 1 in KO_idx_down:
                self.grid[update_bool_idx1, j + 1] = rbt_l[np.where(KO_idx_down == j + 1)]

            if j + 1 in KO_idx_up:
                self.grid[update_bool_idx2, j + 1] = rbt_u[np.where(KO_idx_up == j + 1)]

            U = self._M1.dot(self.grid[1: -1, j + 1])

            U[0] += self._theta * self._l[0] * self.dt * self.grid[0, j] + (1 - self._theta) * self._l[0] * self.dt * self.grid[0, j + 1]
            U[-1] += self._theta * self._u[-1] * self.dt * self.grid[-1, j] + (1 - self._theta) * self._u[-1] * self.dt * self.grid[-1, j + 1]

            self.grid[1: -1, j] = np.dot(invM, U)


if __name__ == '__main__':

    (S, t, T, r, q, sigma, LH, UH, Lrbt, Urbt, year_base) = (5000, 0, 360*2, 0.03, 0.0, 0.2, 4000, 5150, 0.4, 0.4, 360)

    T_UKO = 30
    T_UKO = np.hstack([np.arange(math.floor(t) + T_UKO, T, T_UKO), T])

    T_LKO = 1
    T_LKO = np.hstack([np.arange(math.floor(t) + T_LKO, T, T_LKO), T])

    pricer = DiscreteDoubleOneTouchPde(S, t, T, r, q, sigma, LH, UH, Lrbt, Urbt, year_base, T_LKO, T_UKO)
    pricer.price()
    pricer.greeks()

    print(pricer.present_value(), pricer.delta(), pricer.gamma(), pricer.theta(), pricer.vega())
