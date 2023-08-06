from .fd_grid_generator import FiniteDifference
from ..api_and_utils import np, tqdm, sp


class FullyImplicitEuropean(FiniteDifference):

    def _set_matrix_(self):
        self._A = sp.diags([self._l[1:], self._c, self._u[:-1]], [-1, 0, 1], format='csc').toarray()
        self._I = sp.eye(self.Ns - 1).toarray()
        self._M = self._I - self.dt * self._A

    def _solve_(self):
        invM = np.linalg.inv(self._M)

        for j in tqdm(list(reversed(np.arange(self.Nt))), leave=False):
            U = self.grid[1: -1, j + 1].copy()
            U[0] += self._l[0] * self.dt * self.grid[0, j]
            U[-1] += self._u[-1] * self.dt * self.grid[-1, j]

            self.grid[1: -1, j] = np.dot(invM, U)
