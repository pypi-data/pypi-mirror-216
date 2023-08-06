from ..api_and_utils import np, deepcopy, interp1d, OptionType


def interpolate(x, y, kind='linear', fill_value=(0, 0), bounds_error=False):
    interp = interp1d(x=x, y=y, kind=kind, fill_value=fill_value, bounds_error=bounds_error)
    return interp


def trigger(oldval, newval, tol, counter, maxIteration):
    noBreak = 1
    if np.linalg.norm(newval - oldval) <= tol:
        noBreak = 0
    elif counter > maxIteration:
        print('结果可能不收敛')
        noBreak = 0
    return noBreak


class OptionPricingMethod:

    def __init__(self, S, K, r, q, t, T, sigma, year_base, option_type):
        self.S = S
        self.K = K
        self.r = r
        self.q = q
        self.t = t
        self.T = T
        self.year_base = year_base
        self.sigma = sigma
        self._is_call = {OptionType.CALL: True, OptionType.PUT: False}[option_type]
        self._omega = 1 if self._is_call else -1


class FiniteDifference(OptionPricingMethod):

    def __init__(self, S, K, r, q, t, T, sigma, year_base, option_type, Ns=None, Nt=None, Smin=None, Smax=None):
        super().__init__(S=S, K=K, r=r, q=q, t=t, T=T, sigma=sigma, year_base=year_base, option_type=option_type)

        self.Smin = 0 if Smin is None else Smin
        self.Smax = 4 * max(S, K) if Smax is None else Smax
        self.Ns = 1000 if Ns is None else int(Ns)
        self.Nt = int((T - t) * 1) if Nt is None else int(Nt)

    def _set_initial_grid_(self):
        self.dS = (self.Smax - self.Smin) / self.Ns * 1.0
        self.dt = self.T / self.year_base / self.Nt * 1.0
        self.Svec = np.linspace(self.Smin, self.Smax, self.Ns + 1)
        self.Tvec = np.linspace(0, (self.T - self.t) / self.year_base, self.Nt + 1)
        self.grid = np.zeros(shape=(self.Ns + 1, self.Nt + 1))

    def _set_terminal_condition_(self):
        self.grid[:, -1] = np.maximum(self._omega * (self.Svec - self.K), 0)

    def _set_boundary_condition_(self):
        tau = self.Tvec[-1] - self.Tvec
        DFq = np.exp(-self.q * tau)
        DFr = np.exp(-self.r * tau)

        self.grid[0, :] = np.maximum(self._omega * (self.Svec[0] * DFq - self.K * DFr), 0)
        self.grid[-1, :] = np.maximum(self._omega * (self.Svec[-1] * DFq - self.K * DFr), 0)

    def _set_coefficient_(self):
        drift = (self.r - self.q) * self.Svec[1: -1] / self.dS
        diffusion_square = (self.sigma * self.Svec[1: -1] / self.dS) ** 2

        self._l = 0.5 * (diffusion_square - drift)
        self._c = -diffusion_square - self.r
        self._u = 0.5 * (diffusion_square + drift)

    def _set_matrix_(self):
        pass

    def _solve_(self):
        pass

    def _set_grid_delta_(self):
        self.grid_delta = np.zeros(shape=(self.grid.shape[0], self.grid.shape[1]))
        self.grid_delta[1: -1] = (self.grid[2:] - self.grid[:-2]) / (2 * self.dS)
        self.grid_delta[0] = (self.grid[1] - self.grid[0]) / self.dS
        self.grid_delta[-1] = (self.grid[-1] - self.grid[-2]) / self.dS
        self.grid_delta = self.grid_delta.round(8)

    def _set_grid_gamma_(self):
        self.grid_gamma = np.zeros(shape=(self.grid.shape[0], self.grid.shape[1]))
        self.grid_gamma[1: -1] = (self.grid[2:] + self.grid[:-2] - 2 * self.grid[1: -1]) / (self.dS * self.dS)
        self.grid_gamma[0] = (self.grid[0] + self.grid[2] - 2 * self.grid[1]) / (self.dS * self.dS)
        self.grid_gamma[-1] = (self.grid[-1] + self.grid[-3] - 2 * self.grid[-2]) / (self.dS * self.dS)
        self.grid_gamma = self.grid_gamma.round(8)

    def _set_grid_theta_(self, dt: float = 1):
        idx_1day = np.abs(self.Tvec - dt / self.year_base).argmin()
        self.grid_theta = (self.grid[:, idx_1day:] - self.grid[:, :-idx_1day]) / (self.Tvec[idx_1day] * self.year_base)
        self.grid_theta = self.grid_theta.round(8)

    def _set_grid_vega_(self, dv: float = 0.01):
        pricer_up = deepcopy(self)
        pricer_up.sigma = self.sigma + dv
        pricer_up.price()
        self.grid_vega = pricer_up.grid - self.grid
        self.grid_vega = self.grid_vega.round(8)

    def price(self):
        self._set_initial_grid_()
        self._set_terminal_condition_()
        self._set_boundary_condition_()
        self._set_coefficient_()
        self._set_matrix_()
        self._solve_()

    def greeks(self, include_vega=True):
        self._set_grid_delta_()
        self._set_grid_gamma_()
        self._set_grid_theta_()
        if include_vega:
            self._set_grid_vega_()

    def present_value(self, S=None):
        S = self.S if S is None else S
        return interpolate(x=self.Svec, y=self.grid[:, 0])(S).round(8)

    def delta(self, S=None):
        S = self.S if S is None else S
        return interpolate(x=self.Svec, y=self.grid_delta[:, 0])(S).round(8)

    def gamma(self, S=None):
        S = self.S if S is None else S
        return interpolate(x=self.Svec, y=self.grid_gamma[:, 0])(S).round(8)

    def theta(self, S=None):
        S = self.S if S is None else S
        return interpolate(x=self.Svec, y=self.grid_theta[:, 0])(S).round(8)

    def vega(self, S=None):
        S = self.S if S is None else S
        return interpolate(x=self.Svec, y=self.grid_vega[:, 0])(S).round(8)
