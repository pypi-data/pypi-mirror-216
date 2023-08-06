from ..monte_carlo_engine import *
from ..api_and_utils import *
from ..finite_difference_engine import *


class OneAssetOptionBase(ParamsBase):

    def __init__(self, param):
        super().__init__(param)

    def __calculate_present_value__(self) -> float:
        raise NotImplementedError()

    @lru_cache(maxsize=10)
    def present_value(self) -> float:
        return self.__calculate_present_value__()

    @lru_cache(maxsize=10)
    def delta(self, step: float = 0.001) -> float:
        if hasattr(self.param, 'expiry_date') and hasattr(self.param, 'current_date') and hasattr(self.param, 'spot_price'):
            if self.param.expiry_date - self.param.current_date <= 0:
                return 0.0
            else:
                spot_up = self.param.spot_price * (1 + step)
                spot_down = self.param.spot_price * (1 - step)
                pricer_up, pricer_down = deepcopy(self), deepcopy(self)
                pricer_up.param.spot_price = spot_up
                pricer_down.param.spot_price = spot_down
                return (pricer_up.present_value() - pricer_down.present_value()) / (spot_up - spot_down)
        return 0.0

    @lru_cache(maxsize=10)
    def moddelta(self, step: float = 0.001) -> float:
        if hasattr(self.param, 'expiry_date') and hasattr(self.param, 'current_date') and hasattr(self.param, 'spot_price'):
            if 0 < self.param.expiry_date - self.param.current_date <= 1:
                mod_step = 0.0001
                mod_current = self.param.expiry_date - mod_step
                spot_up = self.param.spot_price * (1 + step)
                spot_down = self.param.spot_price * (1 - step)
                mod_pricer_up, mod_pricer_down = deepcopy(self), deepcopy(self)
                mod_pricer_up.param.spot_price = spot_up
                mod_pricer_down.param.spot_price = spot_down
                mod_pricer_up.param.current_date = mod_current
                mod_pricer_down.param.current_date = mod_current
                return (mod_pricer_up.present_value() - mod_pricer_down.present_value()) / (spot_up - spot_down)
            else:
                return self.delta(step=step)
        return 0.0

    @lru_cache(maxsize=10)
    def gamma(self, step: float = 0.001) -> float:
        if hasattr(self.param, 'spot_price'):
            spot_up = self.param.spot_price * (1 + step)
            spot_down = self.param.spot_price * (1 - step)
            pricer_up, pricer_down = deepcopy(self), deepcopy(self)
            pricer_up.param.spot_price = spot_up
            pricer_down.param.spot_price = spot_down
            return (pricer_up.present_value() + pricer_down.present_value() - 2 * self.present_value()) / pow((spot_up - spot_down) / 2, 2) 
        return 0.0

    @lru_cache(maxsize=10)
    def vega(self, step: float = 0.01) -> float:
        if hasattr(self.param, 'volatility'):
            vol_up = self.param.volatility + step
            pricer_up = deepcopy(self)
            pricer_up.param.volatility = vol_up
            return pricer_up.present_value() - self.present_value()
        return 0.0

    @lru_cache(maxsize=10)
    def theta(self, step: float = 1) -> float:
        if hasattr(self.param, 'current_date'):
            current_up = self.param.current_date + step
            pricer_up = deepcopy(self)
            pricer_up.param.current_date = current_up
            return pricer_up.present_value() - self.present_value()
        return 0.0

    @lru_cache(maxsize=10)
    def rho(self, step: float = 0.0001) -> float:
        if hasattr(self.param, 'riskfree_rate'):
            current_up = self.param.riskfree_rate + step
            pricer_up = deepcopy(self)
            pricer_up.param.riskfree_rate = current_up
            return pricer_up.present_value() - self.present_value()
        return 0.0

    @lru_cache(maxsize=10)
    def ddeltadt(self, time_step: float = 1, price_step: float = 0.001):
        if hasattr(self.param, 'current_date') and hasattr(self.param, 'spot_price'):
            current_up = self.param.current_date + time_step
            pricer_up = deepcopy(self)
            pricer_up.param.current_date = current_up
            return pricer_up.delta(step=price_step) - self.delta(step=price_step)
        return 0.0

    @lru_cache(maxsize=10)
    def modddeltadt(self, time_step: float = 1, price_step: float = 0.001):
        if hasattr(self.param, 'expiry_date') and hasattr(self.param, 'current_date') and hasattr(self.param, 'spot_price'):
            if 0 < self.param.expiry_date - self.param.current_date <= 1:
                mod_step = 0.0001
                mod_current = self.param.expiry_date - mod_step
                mod_current_up = mod_current + time_step
                mod_pricer, mod_pricer_up = deepcopy(self), deepcopy(self)
                mod_pricer.param.current_date = mod_current
                mod_pricer_up.param.current_date = mod_current_up
                return mod_pricer_up.delta(step=price_step) - mod_pricer.delta(step=price_step)
            else:
                return self.ddeltadt(time_step=time_step, price_step=price_step)
        return 0.0

    @lru_cache(maxsize=10)
    def ddeltadv(self, vol_step: float = 0.01, price_step: float = 0.001):
        if hasattr(self.param, 'volatility') and hasattr(self.param, 'spot_price'):
            vol_up = self.param.volatility + vol_step
            pricer_up = deepcopy(self)
            pricer_up.param.volatility = vol_up
            return pricer_up.delta(step=price_step) - self.delta(step=price_step)
        return 0.0
