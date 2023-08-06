from ..one_asset_option_base import *


def __mc_snowball__(notional, spot_price, entrance_price, knock_in_barrier_price, knock_out_barrier_price, knock_in_strike_price,
                    floor_rate, margin_rate, bonus_rate, option_type, is_knock_in, riskfree_rate, dividend, volatility,
                    residual_intraday, expiry_date, year_base, knock_in_obs, knock_out_obs, participation_rate=0):
    """
    雪球期权
    :param knock_in_obs 敲入观测日, 包括obs_index观测日期，adjust(对障碍价格进行比率调整，1为原始输入敲入价格)
    :param knock_out_obs 敲出观测日，包括obs_index观测日期，adjust(对障碍价格进行比率调整，1为原始输入敲出价格)，coupon_rate票息(已经过敲出日期调整)
    :param floor_rate 保护价
    :param margin_rate 保证金率
    :param bonus_rate 到期收益(非年化)
    """

    phi = {OptionType.STANDARD: 1, OptionType.REVERSE: -1}[option_type]
    if expiry_date <= 0:
        # 判断最后一天敲入敲出
        ki_adj = knock_in_obs['adjust_rate'][np.where(knock_in_obs['obs_index'] == expiry_date)]
        ki_flag = phi * (spot_price - knock_in_barrier_price * ki_adj) <= 0
        ki_flag = False if len(ki_flag) == 0 else ki_flag[0]

        ko_adj = knock_out_obs['adjust_rate'][np.where(knock_out_obs['obs_index'] == expiry_date)]
        ko_flag = phi * (spot_price - knock_out_barrier_price * ko_adj) >= 0
        ko_flag = False if len(ko_flag) == 0 else ko_flag[0]
        if ko_flag:
            # 敲出损益
            rst = notional * (knock_out_obs['coupon_rate'][np.where(knock_out_obs['obs_index'] == expiry_date)][0]
                              + phi * participation_rate * (spot_price - knock_out_barrier_price * ko_adj[0]) / entrance_price)
        elif is_knock_in or ki_flag:
            # 敲入损益
            rst = notional * max((floor_rate - 1), min(phi * (spot_price - knock_in_strike_price) / entrance_price, 0))
        else:
            # 未敲入未敲出
            rst = notional * bonus_rate
        return rst

    intraday = round(math.ceil(residual_intraday) - residual_intraday, 4)
    price = spot_price * McPathGenerator.generate(riskfree_rate=riskfree_rate, dividend=dividend, volatility=volatility,
                                                  intraday=intraday, expiry_date=expiry_date, year_base=year_base, random_seed=0)
    M = len(price)

    ki_obs_idx = np.where(knock_in_obs['obs_index'] >= 0)
    ki_adj = knock_in_obs['adjust_rate'][ki_obs_idx]
    ki_obs_idx = knock_in_obs['obs_index'][ki_obs_idx].astype(int)

    ko_obs_idx = np.where(knock_out_obs['obs_index'] >= 0)
    ko_adj = knock_out_obs['adjust_rate'][ko_obs_idx]
    ko_coupon = knock_out_obs['coupon_rate'][ko_obs_idx]
    ko_obs_idx = knock_out_obs['obs_index'][ko_obs_idx].astype(int)

    t_arr = np.hstack([0, np.arange(1, expiry_date + 1, 1) - intraday])
    assert round(expiry_date - intraday, 4) == round(t_arr[-1], 4)

    knock_in_barrier_price = knock_in_barrier_price * ki_adj
    knock_out_barrier_price = knock_out_barrier_price * ko_adj

    ki_mat_flag = np.zeros((M, 1), dtype=bool) if len(ki_obs_idx) == 0 else phi * (price[:, ki_obs_idx] - knock_in_barrier_price) <= 0
    ko_mat_flag = np.zeros((M, 1), dtype=bool) if len(ko_obs_idx) == 0 else phi * (price[:, ko_obs_idx] - knock_out_barrier_price) >= 0
    ko_idx = ko_mat_flag.argmax(axis=1)

    # 敲出
    discount_factor = 1 / np.exp(riskfree_rate * t_arr[ko_obs_idx][ko_idx] / year_base)
    ko_arr_flag = np.max(ko_mat_flag, axis=1)
    ko_payoff = ko_arr_flag * discount_factor * notional * (ko_coupon[ko_idx] + phi * participation_rate * (((price[:, ko_obs_idx] - knock_out_barrier_price) / entrance_price)[np.arange(M), ko_idx])
                                                            - margin_rate * (np.exp(riskfree_rate * t_arr[ko_obs_idx][ko_idx] / year_base) - 1))

    # 敲入未敲出
    discount_factor = 1 / np.exp(riskfree_rate * (expiry_date - intraday) / year_base)
    ki_arr_flag = np.logical_or(is_knock_in, np.max(ki_mat_flag, axis=1))
    ki_no_ko_arr_flag = np.logical_and(ki_arr_flag, np.logical_not(ko_arr_flag))
    ki_no_ko_payoff = ki_no_ko_arr_flag * discount_factor * notional * (np.maximum((floor_rate - 1), np.minimum(phi * (price[:, -1] - knock_in_strike_price) / entrance_price, 0))
                                                                        - margin_rate * (1 / discount_factor - 1))

    # 未敲入未敲出
    discount_factor = 1 / np.exp(riskfree_rate * (expiry_date - intraday) / year_base)
    no_ki_no_ko_arr_flag = np.logical_and(np.logical_not(ki_arr_flag), np.logical_not(ko_arr_flag))
    no_ki_no_ko_payoff = no_ki_no_ko_arr_flag * discount_factor * notional * (bonus_rate - margin_rate * (1 / discount_factor - 1))

    rst = np.round(np.mean(ko_payoff + ki_no_ko_payoff + no_ki_no_ko_payoff), 8)
    return rst


class SnowballMc(OneAssetOptionBase):

    def __calculate_present_value__(self) -> float:
        residual_intraday = round(math.ceil(self.param.current_date) - self.param.current_date, 4)
        current_date_index = math.floor(self.param.current_date)
        return __mc_snowball__(
            notional=self.param.notional,
            spot_price=self.param.spot_price,
            entrance_price=self.param.entrance_price,
            knock_in_barrier_price=self.param.knock_in_barrier_price,
            knock_out_barrier_price=self.param.knock_out_barrier_price,
            knock_in_strike_price=self.param.knock_in_strike_price,
            floor_rate=self.param.floor_rate,
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
            participation_rate=self.param.participation_rate,
            knock_in_obs={'obs_index': np.array([obs.obs_index - current_date_index for obs in self.param.knock_in_obs_date]),
                          'adjust_rate': np.array([obs.adjust_rate for obs in self.param.knock_in_obs_date])},
            knock_out_obs={'obs_index': np.array([obs.obs_index - current_date_index for obs in self.param.knock_out_obs_date]),
                           'adjust_rate': np.array([obs.adjust_rate for obs in self.param.knock_out_obs_date]),
                           'coupon_rate': np.array([obs.coupon_rate for obs in self.param.knock_out_obs_date])}
        )
