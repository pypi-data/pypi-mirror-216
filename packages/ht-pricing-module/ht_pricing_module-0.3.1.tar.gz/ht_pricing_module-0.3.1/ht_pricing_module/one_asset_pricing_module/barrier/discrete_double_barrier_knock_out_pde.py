from ht_pricing_module.one_asset_pricing_module.one_asset_option_base import tqdm, math, CrankNicolsonEuropean, np, OptionType


class DiscreteDoubleBarrierKnockOutPde(CrankNicolsonEuropean):

    def __init__(self, option_type, S, K, t, T, r, q, sigma, LH, UH, Lrbt, Urbt, year_base,
                 T_LKO=None, T_UKO=None, Ns=None, Nt=None, Smin=None, Smax=None, theta=1):
        super().__init__(option_type=option_type, S=S, K=K, t=t, T=T, r=r, q=q, sigma=sigma, year_base=year_base, Ns=Ns, Nt=Nt)

        self.LH = LH
        self.UH = UH
        self.Lrbt = Lrbt
        self.Urbt = Urbt
        self._LPaE = False
        self._UPaE = False
        self.T_LKO = (np.array([]) if T_LKO is None else T_LKO) / self.year_base
        self.T_UKO = (np.array([]) if T_UKO is None else T_UKO) / self.year_base

        self.Smin = 0 if Smin is None else Smin
        self.Smax = 4 * max(S, self.K) if Smax is None else Smax

        self._theta = theta

    def _set_terminal_condition_(self):
        update_down_bool_idx = (self.Svec <= self.LH)
        update_up_bool_idx = (self.Svec >= self.UH)
        self.grid[:, -1] = np.maximum(self._omega * (self.Svec - self.K), 0)
        self.grid[update_down_bool_idx, -1] = self.Lrbt
        self.grid[update_up_bool_idx, -1] = self.Urbt

    def _set_boundary_condition_(self):
        tau = self.Tvec[-1] - self.Tvec
        self.grid[0, :] = self.Lrbt * np.exp(-self.r * tau * int(self._LPaE))
        self.grid[-1, :] = self.Urbt * np.exp(-self.r * tau * int(self._UPaE))

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

    (S, K, t, T, r, q, sigma, LH, UH, Lrbt, Urbt, year_base) = (5000, 5000, 0, 360*2, 0.03, 0.0, 0.2, 4000, 5150, 0., 0., 360)
    option_type = OptionType.PUT

    T_UKO = 30
    T_UKO = np.hstack([np.arange(math.floor(t) + T_UKO, T, T_UKO), T])

    T_LKO = 30
    T_LKO = np.hstack([np.arange(math.floor(t) + T_LKO, T, T_LKO), T])

    pricer = DiscreteDoubleBarrierKnockOutPde(option_type, S, K, t, T, r, q, sigma, LH, UH, Lrbt, Urbt, year_base, T_LKO, T_UKO)
    pricer.price()
    pricer.greeks()

    print(pricer.present_value(), pricer.delta(), pricer.gamma(), pricer.theta(), pricer.vega())
