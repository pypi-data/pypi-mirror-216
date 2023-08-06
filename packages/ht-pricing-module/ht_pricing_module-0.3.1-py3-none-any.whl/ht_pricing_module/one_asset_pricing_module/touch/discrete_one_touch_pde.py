from ..one_asset_option_base import CrankNicolsonEuropean, tqdm, np, math, BarrierType, interpolate


class DiscreteOneTouchPde(CrankNicolsonEuropean):

    def __init__(self, barrier_type, S, t, T, r, q, sigma, H, rbt, year_base,
                 T_KO=None, Ns=None, Nt=None, Smin=None, Smax=None, theta=1):
        self.S = S
        self.H = H
        self.r = r
        self.q = q
        self.sigma = sigma
        self.t = t
        self.T = T
        self.year_base = year_base
        self.rbt = rbt
        self.T_KO = (np.array([]) if T_KO is None else T_KO) / self.year_base

        self.Smin = 0 if Smin is None else Smin
        self.Smax = 4 * max(S, self.H) if Smax is None else Smax
        self.Ns = 1000 if Ns is None else int(Ns)
        self.Nt = int((T - t) * 1) if Nt is None else int(Nt)

        self._PaE = False
        self._is_down = {BarrierType.DOWN: True, BarrierType.UP: False}[barrier_type]
        self._theta = theta

    def _set_terminal_condition_(self):
        pass

    def _set_boundary_condition_(self):
        tau = self.Tvec[-1] - self.Tvec
        DF = np.exp(-self.r * tau * int(self._PaE))

        if not np.isscalar(self.rbt):
            f = interpolate(x=self.T_KO, y=self.rbt, kind='next', bounds_error=False, fill_value=(self.rbt[0], self.rbt[-1]))
            if self._is_down:
                self.grid[0, :] = f(self.Tvec) * DF
            else:
                self.grid[-1, :] = f(self.Tvec) * DF
        else:
            if self._is_down:
                self.grid[0, :] = self.rbt * DF
            else:
                self.grid[-1, :] = self.rbt * DF

    def _solve_(self):
        invM = np.linalg.inv(self._M2)

        KO_idx = np.searchsorted(self.Tvec.round(8), self.T_KO.round(8))
        update_bool_idx = (self.Svec <= self.H) if self._is_down else (self.Svec >= self.H)
        tau = self.Tvec[-1] - self.T_KO
        rbt = self.rbt * np.exp(-self.r * tau * int(self._PaE))

        for j in tqdm(list(reversed(np.arange(self.Nt))), leave=False):

            if j + 1 in KO_idx:
                self.grid[update_bool_idx, j + 1] = rbt[np.where(KO_idx == j + 1)[0]]

            U = self._M1.dot(self.grid[1: -1, j + 1])

            U[0] += self._theta * self._l[0] * self.dt * self.grid[0, j] + (1 - self._theta) * self._l[0] * self.dt * self.grid[0, j + 1]
            U[-1] += self._theta * self._u[-1] * self.dt * self.grid[-1, j] + (1 - self._theta) * self._u[-1] * self.dt * self.grid[-1, j + 1]

            self.grid[1: -1, j] = np.dot(invM, U)


if __name__ == '__main__':

    (S, H, r, q, t, T, year_base, sigma, barrier_type) = (5000, 4000, 0.03, 0.0, 0, 360*2, 360, 0.2, BarrierType.DOWN)
    (rbt, T_KO) = (0.2, 30)

    T_KO = np.hstack([np.arange(math.floor(t) + T_KO, T, T_KO), T])
    (rbt, Rbt_KO) = (rbt * T / year_base, rbt * T_KO / year_base)

    pricer = DiscreteOneTouchPde(barrier_type, S, t, T, r, q, sigma, H, Rbt_KO, year_base, T_KO)
    pricer.price()
    pricer.greeks()

    print(pricer.present_value(), pricer.delta(), pricer.gamma(), pricer.theta(), pricer.vega())
