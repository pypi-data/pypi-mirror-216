from .fd_grid_generator import FiniteDifference, trigger
from ..api_and_utils import np, tqdm, sp


class CrankNicolsonAmerican(FiniteDifference):

    _theta = 0.5
    _alpha = 0.8
    _epsilon = 1e-6
    _max_iter = 1e4

    def _set_matrix_(self):
        self._A = sp.diags([self._l[1:], self._c, self._u[:-1]], [-1, 0, 1], format='csc').toarray()
        self._I = sp.eye(self.Ns - 1).toarray()
        self._M1 = self._I + (1 - self._theta) * self.dt * self._A

    def _solve_(self):
        thdt = self._theta * self.dt
        payoff = self.grid[1:-1, -1]
        m = len(payoff)
        pastval = payoff.copy()

        for j in tqdm(list(reversed(np.arange(self.Nt))), leave=False):
            counter = 0
            noBreak = 1
            newval = pastval.copy()

            z = self._M1.dot(pastval)
            z[0] += self._theta * self._l[0] * self.dt * self.grid[0, j] + (1 - self._theta) * self._l[0] * self.dt * self.grid[0, j + 1]
            z[-1] += self._theta * self._u[-1] * self.dt * self.grid[-1, j] + (1 - self._theta) * self._u[-1] * self.dt * self.grid[-1, j + 1]

            while noBreak:
                counter += 1
                oldval = newval.copy()
                newval[0] = np.maximum(payoff[0], oldval[0] + self._alpha / (1 - thdt * self._c[0]) * (z[0] - (1 - thdt * self._c[0]) * oldval[0] + thdt * self._u[0] * oldval[1]))
                for k in np.arange(1, m - 1):
                    newval[k] = np.maximum(payoff[k], oldval[k] + self._alpha / (1 - thdt * self._c[k]) * (z[k] + thdt * self._l[k] * newval[k - 1] - (1 - thdt * self._c[k]) * oldval[k] + thdt * self._u[k] * oldval[k + 1]))
                newval[m - 1] = np.maximum(payoff[m - 1], oldval[m - 1] + self._alpha / (1 - thdt * self._c[m - 1]) * (z[m - 1] + thdt * self._l[m - 1] * newval[m - 2] - (1 - thdt * self._c[m - 1]) * oldval[m - 1]))
                noBreak = trigger(oldval, newval, self._epsilon, counter, self._max_iter)

            pastval = newval.copy()
            self.grid[1:-1, j] = pastval
