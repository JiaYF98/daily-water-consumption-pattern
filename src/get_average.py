"""
得到每个小区不同季节平均流量作为最终分析所用流量
计算方法分为 all （计算某季节所有日期的平均流量）和 holiday（分别计算某季节工作日和休息日的平均流量）
用小区每个时刻在相应季节流量最大值作为该季节最终流量规律分析效果不佳（好像是）
"""
import handle
import os
import pandas as pd
import numpy as np


def get_average(source_folder_path, save_folder_path=None, method='all'):
    data_info = handle.getinfo(source_folder_path)
    for info in data_info:
        data_path = info.get('path')
        group = info.get('group')
        community = info.get('community')

        df = handle.get_all_flow_data(data_path)

        # 时间为列，日期为行
        df = df.T

        season_info = handle.get_season_info()
        for season in season_info:
            season_start = season_info.get(season).get('start')
            season_end = season_info.get(season).get('end')
            is_current_season = (df.index.map(lambda x: x[5:]) >= season_start) & (
                    df.index.map(lambda x: x[5:]) <= season_end)
            if np.sum(is_current_season) > 0:
                season_df_all = df[is_current_season]

                # 计算平均流量
                average_flow_all = round(season_df_all.mean(), 2)
                average_flow_all.name = season + '平均用水量'

                # # 计算最大流量
                # max_flow_all = round(season_df_all.max(), 2)
                # max_flow_all.name = '流量'

                # 创建保存路径
                save_path = os.path.join(save_folder_path, group + '\\' + community + '\\' + season)
                if not os.path.exists(save_path):
                    os.makedirs(save_path)

                if method == 'all':
                    average_flow_all.to_excel(r'{0}\{1}.xlsx'.format(save_path, community + season + '平均用水量'),
                                              index=True)

                    # max_flow_all.to_excel(r'{0}\{1}.xlsx'.format(save_path, community + season + '最大流量'), index=True)

                if method == 'holiday':
                    season_df_all.index = pd.to_datetime(season_df_all.index, format='%Y-%m-%d')
                    is_holiday = (season_df_all.index.dayofweek >= 5) | (
                        season_df_all.index.strftime('%m-%d').isin(handle.get_holiday()))

                    # 选出工作日和休息日的流量
                    if np.sum(is_holiday) > 0:
                        season_df_holiday = season_df_all[is_holiday]
                        average_flow_holiday = round(season_df_holiday.mean(), 2)
                        average_flow_holiday.name = season + '休息日用水量'
                        average_flow_holiday.to_excel(r'{0}\{1}.xlsx'.format(save_path, community + season + '休息日用水量'),
                                                      index=True)
                        print(community + season + '休息日用水量完成！')

                    if np.sum(~is_holiday) > 0:
                        season_df_workday = season_df_all[~is_holiday]
                        average_flow_workday = round(season_df_workday.mean(), 2)
                        average_flow_workday.name = season + '工作日用水量'
                        average_flow_workday.to_excel(r'{0}\{1}.xlsx'.format(save_path, community + season + '工作日用水量'),
                                                      index=True)
                        print(community + season + '工作日用水量完成！')

                print(community + season + '完成！')

        print(community + '完成！')


get_average(r'D:\日常\学习\大四\大四下\毕业设计\超声水表流量数据\去除异常数据\按日拆分', r'D:\日常\学习\大四\大四下\毕业设计\超声水表流量数据\平均用水量\数据')
get_average(r'D:\日常\学习\大四\大四下\毕业设计\超声水表流量数据\去除异常数据\按日拆分', r'D:\日常\学习\大四\大四下\毕业设计\超声水表流量数据\平均用水量\数据', 'holiday')
