from .fd_grid_generator import FiniteDifference
from ..api_and_utils import np, tqdm, sp


class CrankNicolsonEuropean(FiniteDifference):
    _theta = 0.5

    def _set_matrix_(self):
        self._A = sp.diags([self._l[1:], self._c, self._u[:-1]], [-1, 0, 1], format='csc').toarray()
        self._I = sp.eye(self.Ns - 1).toarray()
        self._M1 = self._I + (1 - self._theta) * self.dt * self._A
        self._M2 = self._I - self._theta * self.dt * self._A

    def _solve_(self):
        invM = np.linalg.inv(self._M2)

        for j in tqdm(list(reversed(np.arange(self.Nt))), leave=False):
            U = self._M1.dot(self.grid[1: -1, j + 1])

            U[0] += self._theta * self._l[0] * self.dt * self.grid[0, j] + (1 - self._theta) * self._l[0] * self.dt * self.grid[0, j + 1]
            U[-1] += self._theta * self._u[-1] * self.dt * self.grid[-1, j] + (1 - self._theta) * self._u[-1] * self.dt * self.grid[-1, j + 1]

            self.grid[1: -1, j] = np.dot(invM, U)
