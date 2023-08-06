from ..one_asset_option_base import CrankNicolsonAmerican, interpolate, np, OptionType, BarrierType, KnockType


class SingleBarrierKnockOutAmPde(CrankNicolsonAmerican):

    def __init__(self, option_type, barrier_type, S, K, H, r, q, t, T, rbt, sigma, year_base, Ns=None, Nt=None, theta=1, alpha=0.8, epsilon=1e-6):
        super().__init__(S=S, K=K, r=r, q=q, t=t, T=T, sigma=sigma, option_type=option_type, year_base=year_base, Ns=Ns, Nt=Nt)

        self.H = H
        self.rbt = rbt
        self._is_down = {BarrierType.DOWN: True, BarrierType.UP: False}[barrier_type]
        self._eta = 1 if self._is_down else -1
        self._PaE = False
        self._theta = theta
        self._alpha = alpha
        self._epsilon = epsilon

        if self._is_down:
            self.Smin = self.H
            self.Smax = 3 * np.maximum(S, K)
        else:
            self.Smin = 1 / 5 * np.minimum(S, K)
            self.Smax = self.H

    def _set_terminal_condition_(self):
        self.grid[:, -1] = np.where(self._eta * (self.Svec - self.H) <= 0, self.rbt, np.maximum(self._omega * (self.Svec - self.K), 0))

    def _set_boundary_condition_(self):
        tau = self.Tvec[-1] - self.Tvec
        DFq = np.exp(-self.q * tau)
        DFr = np.exp(-self.r * tau)

        if self._is_down:
            self.grid[0, :] = self.rbt * np.exp(-self.r * tau * self._PaE)
            self.grid[-1, :] = np.maximum(self._omega * (self.Svec[-1] * DFq - self.K * DFr), 0)
        else:
            self.grid[0, :] = np.maximum(self._omega * (self.Svec[0] * DFq - self.K * DFr), 0)
            self.grid[-1, :] = self.rbt * np.exp(-self.r * tau * self._PaE)

    def present_value(self, S=None):
        S = self.S if S is None else S
        return interpolate(x=self.Svec, y=self.grid[:, 0], fill_value=(self.rbt, self.rbt))(S).round(8)


if __name__ == '__main__':

    (S, K, r, q, t, T, year_base, sigma) = (4400, 4300, 0.03, 0.03, 0, 40, 365, 0.2)
    (option_type, barrier_type, knock_type) = (OptionType.CALL, BarrierType.DOWN, KnockType.OUT)
    (H, rbt) = (4300, 0)
    (Ns, Nt) = (1000, T * 10)

    pricer = SingleBarrierKnockOutAmPde(option_type, barrier_type, S, K, H, r, q, t, T, rbt, sigma, year_base, Ns, Nt)
    pricer.price()
    pricer.greeks()

    print(pricer.present_value(), pricer.delta(), pricer.gamma(), pricer.theta())
