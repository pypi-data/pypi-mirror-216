from ht_pricing_module.one_asset_pricing_module.one_asset_option_base import tqdm, math, CrankNicolsonEuropean, interpolate, np, OptionType, BarrierType


class DiscreteSingleBarrierKnockOutPde(CrankNicolsonEuropean):

    def __init__(self, option_type, barrier_type, S, K, t, T, r, q, sigma, H, rbt, year_base, T_KO=None, Ns=None, Nt=None, Smin=None, Smax=None, theta=1):
        super().__init__(option_type=option_type, S=S, K=K, t=t, T=T, r=r, q=q, sigma=sigma, year_base=year_base, Ns=Ns, Nt=Nt)

        self.H = H
        self.rbt = rbt
        self._PaE = False
        self.T_KO = (np.array([]) if T_KO is None else T_KO) / self.year_base

        self.Smin = 0 if Smin is None else Smin
        self.Smax = 4 * max(S, self.K) if Smax is None else Smax

        self._is_down = {BarrierType.DOWN: True, BarrierType.UP: False}[barrier_type]
        self._eta = 1 if self._is_down else -1
        self._theta = theta

    def _set_terminal_condition_(self):
        self.grid[:, -1] = np.where(self._eta * (self.Svec - self.H) <= 0, self.rbt, np.maximum(self._omega * (self.Svec - self.K), 0))

    def _set_boundary_condition_(self):
        tau = self.Tvec[-1] - self.Tvec
        DFq = np.exp(-self.q * tau)
        DFr = np.exp(-self.r * tau)

        self.grid[0, :] = np.maximum(self._omega * (self.Svec[0] * DFq - self.K * DFr), 0)
        self.grid[-1, :] = np.maximum(self._omega * (self.Svec[-1] * DFq - self.K * DFr), 0)

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

    (S, K, H, r, q, t, T, year_base, sigma, rbt) = (5000, 5000, 5150, 0.03, 0.0, 0, 2*360, 360, 0.2, 0)
    (option_type, barrier_type) = (OptionType.PUT, BarrierType.UP)

    T_KO = 30
    T_KO = np.hstack([np.arange(math.floor(t) + T_KO, T, T_KO), T])

    pricer = DiscreteSingleBarrierKnockOutPde(option_type, barrier_type, S, K, t, T, r, q, sigma, H, rbt, year_base, T_KO)
    pricer.price()
    pricer.greeks()

    print(pricer.present_value(), pricer.delta(), pricer.gamma(), pricer.theta(), pricer.vega())
