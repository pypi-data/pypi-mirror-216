from ..one_asset_option_base import interpolate, np, tqdm, CrankNicolsonSnowball


class SnowballPde(CrankNicolsonSnowball):

    def _set_other_vector_(self):
        self._IntVec = self.param.margin_rate * (np.exp(self.param.riskfree_rate * self.Tvec / self.param.year_base) - 1)
        self._EnhVec = np.maximum(self._omega * self.param.participation_rate * ((self.Svec - self.param.knock_out_barrier_price) / self.param.entrance_price), 0)
        self._S_KO = self._omega * (self.Svec - self.param.knock_out_barrier_price) >= 0
        self._S_KI = self._omega * (self.Svec - self.param.knock_in_barrier_price) <= 0

    def _set_terminal_condition_(self):
        S_NKI_NKO = ~(self._S_KO | self._S_KI)

        self.KIgrid[self._S_KO, -1] = (self.param.bonus_rate - self._IntVec[-1] + self._EnhVec[self._S_KO]) * self.param.notional
        self.KIgrid[self._S_KI, -1] = (np.maximum((self.param.floor_rate - 1), np.minimum(self._omega * (self.Svec[self._S_KI] - self.param.knock_in_strike_price) / self.param.entrance_price, 0)) - self._IntVec[-1]) * self.param.notional
        self.KIgrid[S_NKI_NKO, -1] = (np.maximum((self.param.floor_rate - 1), np.minimum(self._omega * (self.Svec[S_NKI_NKO] - self.param.knock_in_strike_price) / self.param.entrance_price, 0)) - self._IntVec[-1]) * self.param.notional

        self.NKIgrid[self._S_KO, -1] = self.KIgrid[self._S_KO, -1]
        self.NKIgrid[self._S_KI, -1] = self.KIgrid[self._S_KI, -1]
        self.NKIgrid[S_NKI_NKO, -1] = (self.param.bonus_rate - self._IntVec[-1]) * self.param.notional

    def _set_boundary_condition_(self):
        DFr = np.exp(-self.param.riskfree_rate * (self.Tvec[-1] - self.Tvec) / self.param.year_base)

        if self._is_call:
            self.KIgrid[0, :] = (np.maximum((self.param.floor_rate - 1), np.minimum(self._omega * (self.Svec[0] - self.param.knock_in_strike_price) / self.param.entrance_price, 0)) - self._IntVec) * self.param.notional * DFr
            if not np.isscalar(self._Rbt_KO) and len(self._Rbt_KO) > 1:
                f1 = interpolate(x=self._T_KO, y=self._Rbt_KO, kind='next', bounds_error=False, fill_value=(self._Rbt_KO[0], self._Rbt_KO[-1]))
                f2 = interpolate(x=self._T_KO, y=self._T_KO, kind='next', bounds_error=False, fill_value=(self._T_KO[0], self._T_KO[-1]))
                self.KIgrid[-1, :] = (f1(self.Tvec) - self._IntVec + self._EnhVec[-1]) * self.param.notional * np.exp(-self.param.riskfree_rate * (f2(self.Tvec) - self.Tvec) / self.param.year_base)
            else:
                self.KIgrid[-1, :] = (self._Rbt_KO - self._IntVec + self._EnhVec[-1]) * self.param.notional * DFr
        else:
            self.KIgrid[-1, :] = (np.maximum((self.param.floor_rate - 1), np.minimum(self._omega * (self.Svec[-1] - self.param.knock_in_strike_price) / self.param.entrance_price, 0)) - self._IntVec) * self.param.notional * DFr
            if not np.isscalar(self._Rbt_KO) and len(self._Rbt_KO) > 1:
                f1 = interpolate(x=self._T_KO, y=self._Rbt_KO, kind='next', bounds_error=False, fill_value=(self._Rbt_KO[0], self._Rbt_KO[-1]))
                f2 = interpolate(x=self._T_KO, y=self._T_KO, kind='next', bounds_error=False, fill_value=(self._T_KO[0], self._T_KO[-1]))
                self.KIgrid[0, :] = (f1(self.Tvec) - self._IntVec + self._EnhVec[0]) * self.param.notional * np.exp(-self.param.riskfree_rate * (f2(self.Tvec) - self.Tvec) / self.param.year_base)
            else:
                self.KIgrid[0, :] = (self._Rbt_KO - self._IntVec + self._EnhVec[0]) * self.param.notional * DFr

        self.NKIgrid[0, :] = self.KIgrid[0, :]
        self.NKIgrid[-1, :] = self.KIgrid[-1, :]

    def _solve_(self):
        invM = np.linalg.inv(self._M2)

        KO_idx = np.searchsorted(self.Tvec, self._T_KO)
        KI_idx = np.searchsorted(self.Tvec, self._T_KI)

        for j in tqdm(list(reversed(np.arange(self._Nt))), leave=False):

            if j + 1 in KO_idx:
                self.KIgrid[self._S_KO, j + 1] = (self._Rbt_KO[np.where(KO_idx == j + 1)] - self._IntVec[j + 1] + self._EnhVec[self._S_KO]) * self.param.notional
                self.NKIgrid[self._S_KO, j + 1] = self.KIgrid[self._S_KO, j + 1]

            U = self._M1.dot(self.KIgrid[1: -1, j + 1])
            U[0] += self._theta * self._l[0] * self.dt / self.param.year_base * self.KIgrid[0, j] + (1 - self._theta) * self._l[0] * self.dt / self.param.year_base * self.KIgrid[0, j + 1]
            U[-1] += self._theta * self._u[-1] * self.dt / self.param.year_base * self.KIgrid[-1, j] + (1 - self._theta) * self._u[-1] * self.dt / self.param.year_base * self.KIgrid[-1, j + 1]
            self.KIgrid[1: -1, j] = np.dot(invM, U)

            if j + 1 in KI_idx:
                self.NKIgrid[self._S_KI, j + 1] = self.KIgrid[self._S_KI, j + 1]

            U = self._M1.dot(self.NKIgrid[1: -1, j + 1])
            U[0] += self._theta * self._l[0] * self.dt / self.param.year_base * self.NKIgrid[0, j] + (1 - self._theta) * self._l[0] * self.dt / self.param.year_base * self.NKIgrid[0, j + 1]
            U[-1] += self._theta * self._u[-1] * self.dt / self.param.year_base * self.NKIgrid[-1, j] + (1 - self._theta) * self._u[-1] * self.dt / self.param.year_base * self.NKIgrid[-1, j + 1]
            self.NKIgrid[1: -1, j] = np.dot(invM, U)

            # if j in KO_idx:
            #     self.KIgrid[self._S_KO, j] = (self._Rbt_KO[np.where(KO_idx == j)] - self._IntVec[j] + self._EnhVec[self._S_KO]) * self.param.notional
            #     self.NKIgrid[self._S_KO, j] = self.KIgrid[self._S_KO, j]
            #
            # if j in KI_idx:
            #     self.NKIgrid[self._S_KI, j] = self.KIgrid[self._S_KI, j]

        if self._Tau > 0 and self._Nt > 0:
            dt = 1 - self._Tau
            M1 = self._I + (1 - self._theta) * dt / self.param.year_base * self._A
            M2 = self._I - self._theta * dt / self.param.year_base * self._A
            invM = np.linalg.inv(M2)

            U = M1.dot(self.KIgrid[1: -1, 1])
            U[0] += self._theta * self._l[0] * dt / self.param.year_base * self.KIgrid[0, 0] + (1 - self._theta) * self._l[0] * dt / self.param.year_base * self.KIgrid[0, 1]
            U[-1] += self._theta * self._u[-1] * dt / self.param.year_base * self.KIgrid[-1, 0] + (1 - self._theta) * self._u[-1] * dt / self.param.year_base * self.KIgrid[-1, 1]
            self.KIgrid[1: -1, 0] = np.dot(invM, U)

            U = self._M1.dot(self.NKIgrid[1: -1, 1])
            U[0] += self._theta * self._l[0] * dt / self.param.year_base * self.NKIgrid[0, 0] + (1 - self._theta) * self._l[0] * dt / self.param.year_base * self.NKIgrid[0, 1]
            U[-1] += self._theta * self._u[-1] * dt / self.param.year_base * self.NKIgrid[-1, 0] + (1 - self._theta) * self._u[-1] * dt / self.param.year_base * self.NKIgrid[-1, 1]
            self.NKIgrid[1: -1, 0] = np.dot(invM, U)
