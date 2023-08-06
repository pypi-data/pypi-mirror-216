from ht_pricing_module.one_asset_pricing_module.one_asset_option_base import *
from ht_pricing_module.one_asset_pricing_module.binary.binary_as import Binary
from ht_pricing_module.one_asset_pricing_module.vanilla.vanilla_as import Vanilla


class SharkfinYield(OneAssetOptionBase):

    def __calculate_present_value__(self):
        time_to_expiry = (self.param.expiry_date - self.param.entrance_date) / self.param.year_base
        participation_rate = (self.param.max_yield_annual - self.param.min_yield_annual) * time_to_expiry / abs((self.param.strike_price - self.param.barrier_price) / self.param.entrance_price)

        param = Params()
        param['option_type'] = self.param.option_type
        param['exercise_type'] = self.param.exercise_type
        param['spot_price'] = self.param.spot_price / self.param.entrance_price
        param['strike_price'] = self.param.strike_price / self.param.entrance_price
        param['expiry_date'] = self.param.expiry_date
        param['current_date'] = self.param.current_date
        param['volatility'] = self.param.volatility
        param['riskfree_rate'] = self.param.riskfree_rate
        param['dividend'] = self.param.dividend
        param['year_base'] = self.param.year_base
        vanilla1 = Vanilla(param)

        param = Params()
        param['option_type'] = self.param.option_type
        param['exercise_type'] = self.param.exercise_type
        param['spot_price'] = self.param.spot_price / self.param.entrance_price
        param['strike_price'] = self.param.barrier_price / self.param.entrance_price
        param['expiry_date'] = self.param.expiry_date
        param['current_date'] = self.param.current_date
        param['volatility'] = self.param.volatility
        param['riskfree_rate'] = self.param.riskfree_rate
        param['dividend'] = self.param.dividend
        param['year_base'] = self.param.year_base
        vanilla2 = Vanilla(param)

        param = Params()
        param['option_type'] = self.param.option_type
        param['exercise_type'] = self.param.exercise_type
        param['spot_price'] = self.param.spot_price / self.param.entrance_price
        param['strike_price'] = self.param.barrier_price / self.param.entrance_price
        param['expiry_date'] = self.param.expiry_date
        param['current_date'] = self.param.current_date
        param['volatility'] = self.param.volatility
        param['riskfree_rate'] = self.param.riskfree_rate
        param['dividend'] = self.param.dividend
        param['payoff'] = self.param.rebate_annual * time_to_expiry
        param['year_base'] = self.param.year_base
        binary3 = Binary(param)

        return self.param.notional * (participation_rate * (vanilla1.present_value() - vanilla2.present_value()) - binary3.present_value() + self.param.min_yield_annual * time_to_expiry)


if __name__ == '__main__':
    param = Params()
    param['option_type'] = OptionType.PUT
    param['exercise_type'] = ExerciseType.EUROPEAN
    param['notional'] = 1
    param['spot_price'] = 100
    param['entrance_price'] = 100
    param['strike_price'] = 95
    param['barrier_price'] = 90
    param['expiry_date'] = 245
    param['current_date'] = 245
    param['entrance_date'] = 0
    param['volatility'] = 0.14
    param['riskfree_rate'] = 0.03
    param['dividend'] = 0.03
    param['year_base'] = 245
    param['rebate_annual'] = 0.07
    param['min_yield_annual'] = 0.02
    param['max_yield_annual'] = 0.14

    pricer = SharkfinYield(param=param)
    print(pricer.present_value())
    import matplotlib.pyplot as plt
    spot_ls = np.arange(85, 100, 0.1)
    pv_ls = []
    for spot in spot_ls:
        param['spot_price'] = spot
        pricer = SharkfinYield(param=param)
        pv_ls.append(pricer.present_value())
    plt.plot(spot_ls, pv_ls)
    plt.show()
