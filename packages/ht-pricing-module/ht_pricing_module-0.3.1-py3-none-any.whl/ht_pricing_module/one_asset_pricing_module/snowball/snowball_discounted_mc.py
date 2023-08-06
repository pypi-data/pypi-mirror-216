from ..one_asset_option_base import *


def __mc_snowball_discounted__(notional, spot_price, entrance_price, knock_in_barrier_price, knock_out_barrier_price, knock_in_strike_price,
                               margin_rate, bonus_rate, option_type, is_knock_in, riskfree_rate, dividend, volatility, residual_intraday,
                               expiry_date, year_base, knock_in_obs, knock_out_obs):
    """
    折价建仓雪球期权
    :param knock_in_obs 敲入观测日, 包括obs_index观测日期
    :param knock_out_obs 敲出观测日，包括obs_index观测日期，coupon_rate票息(已经过敲出日期调整)
    :param margin_rate 保证金率
    :param bonus_rate 到期收益(非年化)
    :param knock_in_strike_price 敲入行权价
    """

    phi = {OptionType.STANDARD: 1, OptionType.REVERSE: -1}[option_type]
    if expiry_date <= 0:
        # 判断最后一天敲入敲出
        ki_flag = np.logical_or(phi * (spot_price - knock_in_barrier_price) <= 0, is_knock_in)
        ko_flag = np.logical_and(phi * (spot_price - knock_out_barrier_price) >= 0, not ki_flag)

        if ki_flag:
            rst = phi * (spot_price - knock_in_strike_price) / entrance_price
        elif ko_flag:
            rst = knock_out_obs['coupon_rate'][np.where(knock_out_obs['obs_index'] == expiry_date)][0]
        else:
            rst = bonus_rate
        return notional * rst

    intraday = round(math.ceil(residual_intraday) - residual_intraday, 4)
    price = spot_price * McPathGenerator.generate(riskfree_rate=riskfree_rate, dividend=dividend, volatility=volatility,
                                                  intraday=intraday, expiry_date=expiry_date, year_base=year_base, random_seed=0)
    M = len(price)

    ki_obs_idx = np.where(knock_in_obs['obs_index'] >= 0)
    ki_obs_idx = knock_in_obs['obs_index'][ki_obs_idx].astype(int)

    ko_obs_idx = np.where(knock_out_obs['obs_index'] >= 0)
    ko_coupon = knock_out_obs['coupon_rate'][ko_obs_idx]
    ko_obs_idx = knock_out_obs['obs_index'][ko_obs_idx].astype(int)

    t_arr = np.hstack([0, np.arange(1, expiry_date + 1, 1) - intraday])
    assert round(expiry_date - intraday, 4) == round(t_arr[-1], 4)

    ki_mat_flag = np.zeros((M, 1), dtype=bool) if len(ki_obs_idx) == 0 else phi * (price[:, ki_obs_idx] - knock_in_barrier_price) <= 0
    ko_mat_flag = np.zeros((M, 1), dtype=bool) if len(ko_obs_idx) == 0 else phi * (price[:, ko_obs_idx] - knock_out_barrier_price) >= 0
    ki_idx = ki_mat_flag.argmax(axis=1)
    ko_idx = ko_mat_flag.argmax(axis=1)

    first_ki_idx = np.where(np.max(ki_mat_flag, axis=1), ki_obs_idx[ki_idx], np.nan)
    first_ko_idx = np.where(np.max(ko_mat_flag, axis=1), ko_obs_idx[ko_idx], np.nan)

    # 先敲入再敲出或仅敲入
    discount_factor = 1 if is_knock_in else 1 / np.exp(riskfree_rate * (expiry_date - intraday) / year_base)
    ki_arr_flag = np.logical_or(np.logical_or(is_knock_in, np.logical_and(~np.isnan(first_ki_idx), np.isnan(first_ko_idx))), first_ki_idx < first_ko_idx)
    ki_payoff = ki_arr_flag * discount_factor * notional * (phi * (price[:, -1] - knock_in_strike_price) / entrance_price - margin_rate * (np.exp(riskfree_rate * (expiry_date - intraday) / year_base) - 1))

    # 先敲出再敲入或仅敲出
    discount_factor = 1 / np.exp(riskfree_rate * t_arr[ko_obs_idx][ko_idx] / year_base)
    ko_arr_flag = np.logical_and(1 - is_knock_in, np.logical_or(first_ko_idx < first_ki_idx, np.logical_and(~np.isnan(first_ko_idx), np.isnan(first_ki_idx))))
    ko_payoff = ko_arr_flag * discount_factor * notional * (ko_coupon[ko_idx] - margin_rate * (np.exp(riskfree_rate * t_arr[ko_obs_idx][ko_idx] / year_base) - 1))

    # 未敲入未敲出
    discount_factor = 1 / np.exp(riskfree_rate * (expiry_date - intraday) / year_base)
    no_ki_no_ko_arr_flag = np.logical_and(np.logical_not(ki_arr_flag), np.logical_not(np.max(ko_mat_flag, axis=1)))
    no_ki_no_ko_payoff = no_ki_no_ko_arr_flag * discount_factor * notional * (bonus_rate - margin_rate * (1 / discount_factor - 1))

    rst = np.round(np.mean(ki_payoff + ko_payoff + no_ki_no_ko_payoff), 8)
    return rst


class SnowballDiscountedMc(OneAssetOptionBase):

    def __calculate_present_value__(self) -> float:
        residual_intraday = round(math.ceil(self.param.current_date) - self.param.current_date, 4)
        current_date_index = math.floor(self.param.current_date)
        return __mc_snowball_discounted__(
            notional=self.param.notional,
            spot_price=self.param.spot_price,
            entrance_price=self.param.entrance_price,
            knock_in_barrier_price=self.param.knock_in_barrier_price,
            knock_out_barrier_price=self.param.knock_out_barrier_price,
            knock_in_strike_price=self.param.knock_in_strike_price,
            margin_rate=self.param.margin_rate,
            bonus_rate=self.param.bonus_rate,
            option_type=self.param.option_type,
            is_knock_in=self.param.is_knock_in,
            riskfree_rate=self.param.riskfree_rate,
            dividend=self.param.dividend,
            volatility=self.param.volatility,
            residual_intraday=residual_intraday,
            expiry_date=self.param.expiry_date - current_date_index,
            year_base=self.param.year_base,
            knock_in_obs={'obs_index': np.array([obs.obs_index - current_date_index for obs in self.param.knock_in_obs_date])},
            knock_out_obs={'obs_index': np.array([obs.obs_index - current_date_index for obs in self.param.knock_out_obs_date]),
                           'coupon_rate': np.array([obs.coupon_rate for obs in self.param.knock_out_obs_date])}
        )
