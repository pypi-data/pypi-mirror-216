from ..one_asset_option_base import CrankNicolsonEuropean, interpolate, np, OptionType, BarrierType, KnockType


class SingleBarrierKnockOutPde(CrankNicolsonEuropean):

    def __init__(self, option_type, barrier_type, S, K, t, T, r, q, sigma, H, rbt, year_base, Ns=None, Nt=None, theta=1):
        super().__init__(option_type=option_type, S=S, K=K, t=t, T=T, r=r, q=q, sigma=sigma, year_base=year_base, Ns=Ns, Nt=Nt)

        self.H = H
        self.rbt = rbt
        self._PaE = False
        self._is_down = {BarrierType.DOWN: True, BarrierType.UP: False}[barrier_type]
        self._eta = 1 if self._is_down else -1
        self._theta = theta

        if self._is_down:
            self.Smin = self.H
            self.Smax = 4 * np.maximum(S, K)
        else:
            self.Smin = 0
            self.Smax = self.H

    def _set_terminal_condition_(self):
        self.grid[:, -1] = np.where(self._eta * (self.Svec - self.H) <= 0, self.rbt, np.maximum(self._omega * (self.Svec - self.K), 0))

    def _set_boundary_condition_(self):
        tau = self.Tvec[-1] - self.Tvec
        DFq = np.exp(-self.q * tau)
        DFr = np.exp(-self.r * tau)

        if self._is_down:
            self.grid[0, :] = self.rbt * np.exp(-self.r * tau * int(self._PaE))
            self.grid[-1, :] = np.maximum(self._omega * (self.Svec[-1] * DFq - self.K * DFr), 0)
        else:
            self.grid[0, :] = np.maximum(self._omega * (self.Svec[0] * DFq - self.K * DFr), 0)
            self.grid[-1, :] = self.rbt * np.exp(-self.r * tau * int(self._PaE))

    def present_value(self, S=None):
        S = self.S if S is None else S
        return interpolate(x=self.Svec, y=self.grid[:, 0], fill_value=(self.rbt, self.rbt))(S).round(8)


if __name__ == '__main__':

    (S, K, H, r, q, t, T, year_base, sigma, rbt) = (3500, 3500, 3700, 0.03, 0.03, 0, 20, 245, 0.2, 0)
    (option_type, barrier_type) = (OptionType.CALL, BarrierType.UP)
    (Ns, Nt) = (1000, 100)

    pricer = SingleBarrierKnockOutPde(option_type, barrier_type, S, K, t, T, r, q, sigma, H, rbt, year_base, Ns, Nt)
    pricer.price()
    pricer.greeks()

    print(pricer.present_value(), pricer.delta(), pricer.gamma(), pricer.theta(), pricer.vega())
