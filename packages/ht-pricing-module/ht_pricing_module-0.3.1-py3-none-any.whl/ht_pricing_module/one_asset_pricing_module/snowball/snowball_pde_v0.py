from ht_pricing_module.one_asset_pricing_module.one_asset_option_base import FiniteDifference, tqdm, math, np, OptionType, BarrierType
from ht_pricing_module.one_asset_pricing_module.touch.discrete_double_one_touch_pde import DiscreteDoubleOneTouchPde
from ht_pricing_module.one_asset_pricing_module.touch.discrete_one_touch_pde import DiscreteOneTouchPde
from ht_pricing_module.one_asset_pricing_module.barrier.discrete_double_barrier_knock_out_pde import DiscreteDoubleBarrierKnockOutPde
from ht_pricing_module.one_asset_pricing_module.barrier.discrete_barrier_knock_out_pde import DiscreteSingleBarrierKnockOutPde


class SnowballPdeV0(FiniteDifference):

    def __init__(self, option_type, S, K, Not, t, T, r, q, sigma, LH, UH, bonus, Lrbt, Urbt, year_base,
                 T_LKO=None, T_UKO=None, Ns=None, Nt=None, Smin=None, Smax=None, theta=1):
        self.option_type = option_type
        self.S = S
        self.K = K
        self.Not = Not
        self.r = r
        self.q = q
        self.t = t
        self.T = T
        self.sigma = sigma
        self.LH = LH
        self.UH = UH
        self.Ns = Ns
        self.Nt = Nt
        self.bonus = bonus
        self.Lrbt = Lrbt
        self.Urbt = Urbt
        self.year_base = year_base
        self.T_LKO = (np.array([]) if T_LKO is None else T_LKO)
        self.T_UKO = (np.array([]) if T_UKO is None else T_UKO)

        self.Smin = 0 if Smin is None else Smin
        self.Smax = 2 * max(S, self.K) if Smax is None else Smax
        self.Ns = 1000 if Ns is None else int(Ns)
        self.Nt = int((T - t) * 1) if Nt is None else int(Nt)

        self.grid = None

        self._theta = theta

    def _set_initial_grid_(self):
        self.dS = (self.Smax - self.Smin) / self.Ns * 1.0
        self.dt = self.T / self.year_base / self.Nt * 1.0
        self.Svec = np.linspace(self.Smin, self.Smax, self.Ns + 1)
        self.Tvec = np.linspace(0, (self.T - self.t) / self.year_base, self.Nt + 1)
        self.grid = np.zeros(shape=(self.Ns + 1, self.Nt + 1))

    def price(self):
        self._set_initial_grid_()
        OTU = DiscreteOneTouchPde(barrier_type=BarrierType.UP, S=self.S, t=self.t, T=self.T, r=self.r, q=self.q, sigma=self.sigma, H=self.UH, rbt=self.Urbt,
                                  year_base=self.year_base, T_KO=self.T_UKO, Ns=self.Ns, Nt=self.Nt, Smin=self.Smin, Smax=self.Smax, theta=self._theta)
        OTU.price()

        DOT = DiscreteDoubleOneTouchPde(S=self.S, t=self.t, T=self.T, r=self.r, q=self.q, sigma=self.sigma, LH=self.LH, UH=self.UH, Lrbt=self.bonus, Urbt=self.bonus,
                                        year_base=self.year_base, T_LKO=self.T_LKO, T_UKO=self.T_UKO, Ns=self.Ns, Nt=self.Nt, Smin=self.Smin, Smax=self.Smax, theta=self._theta)
        DOT.price()

        DKOP = DiscreteDoubleBarrierKnockOutPde(option_type=OptionType.PUT, S=self.S, K=self.K, t=self.t, T=self.T, r=self.r, q=self.q, sigma=self.sigma, LH=self.LH,
                                                UH=self.UH, Lrbt=0, Urbt=0, year_base=self.year_base, T_LKO=self.T_LKO, T_UKO=self.T_UKO, Ns=self.Ns, Nt=self.Nt,
                                                Smin=self.Smin, Smax=self.Smax, theta=self._theta)
        DKOP.price()

        UOP = DiscreteSingleBarrierKnockOutPde(option_type=OptionType.PUT, barrier_type=BarrierType.UP, S=self.S, K=self.K, t=self.t, T=self.T, r=self.r,
                                               q=self.q, sigma=self.sigma, H=self.UH, rbt=0, year_base=self.year_base, T_KO=self.T_UKO, Ns=self.Ns,
                                               Nt=self.Nt, Smin=self.Smin, Smax=self.Smax, theta=self._theta)
        UOP.price()

        self.grid = self.Not * (OTU.grid + (self.bonus * np.exp(-self.r * (self.T - self.t) / self.year_base) - DOT.grid) + (DKOP.grid - UOP.grid) / self.K)


if __name__ == '__main__':

    (S, K, BI, BO, r, q, t, T, year_base, sigma, Not, option_type) = (100, 100, 95, 100, 0.03, 0.03, 0, 20, 360, 0.2, 100, OptionType.STANDARD)
    rbt = 0.5

    T_UKO = 5
    T_UKO = np.hstack([np.arange(math.floor(t) + T_UKO, T, T_UKO), T])
    (rbt, Rbt_KO) = (rbt * (T - t) / year_base, rbt * T_UKO / year_base)

    T_LKO = 1
    T_LKO = np.hstack([np.arange(math.floor(t) + T_LKO, T, T_LKO), T])

    import time
    tic = time.time()
    # option_type, S, K, t, T, r, q, sigma, LH, UH, Lrbt, Urbt, year_base, T_LKO, T_UKO
    pricer = SnowballPdeV0(option_type, S, K, Not, t, T, r, q, sigma, BI, BO, rbt, 0, Rbt_KO, year_base, T_LKO, T_UKO)
    pricer.price()
    pricer.greeks()

    print(pricer.present_value(), pricer.delta(), pricer.gamma(), pricer.theta(), pricer.vega())

    print(time.time() - tic)
    import matplotlib.pyplot as plt
    plt.plot(pricer.grid_delta[450:550, 0])
    plt.show()
