"""
在聚类之后，各小区按照季节去除每个时刻的异常数据
异常数据的判定采用 Z-Score 方法
去除异常数据采用更细致的判定方法
"""
import os
import handle
import pandas as pd


def remove_outlier(source_folder_path, save_folder_path=None):
    outlier_boundary = 3
    data_info = handle.getinfo(source_folder_path)
    for info in data_info:
        data_path = info.get('path')
        group = info.get('group')
        community = info.get('community')

        df = handle.get_all_flow_data(data_path)
        # 将df转换成日期为行，时间为列
        df = df.T
        # 去除一整天都缺失的数据
        df = df.dropna(how='all')

        season_info = handle.get_season_info()
        for season in season_info:
            season_start = season_info.get(season).get('start')
            season_end = season_info.get(season).get('end')
            season_df = df[
                (df.index.map(lambda x: x[5:]) >= season_start) & (df.index.map(lambda x: x[5:]) <= season_end)]

            # 去除异常值
            for i in range(season_df.columns.size):
                # Z-score
                sta = (season_df[season_df.columns[i]] - season_df[season_df.columns[i]].mean()) / \
                      season_df[season_df.columns[i]].std()

                # 将异常数据和负值的数据设为空
                del_index = season_df[(sta.abs() > outlier_boundary) | (season_df[season_df.columns[i]] <= 0)].index
                if del_index.size > 0:
                    season_df.loc[del_index, season_df.columns[i]] = None

            # 当某天的空值数据超过该天总数据量的一半时，删除该天
            # 找到要删除的日期
            drop_index = []
            for i in range(season_df.index.size):
                if season_df.iloc[i].isnull().sum() >= (season_df.columns.size / 2):
                    drop_index.append(season_df.index[i])
            # 删除该日的数据
            season_df.drop(labels=drop_index, inplace=True)

            # 如果该时刻空值数小于四分之一，则用均值填充空值数据，否则记录下该时刻
            vacant_time = []
            for i in range(season_df.columns.size):
                if season_df[season_df.columns[i]].isnull().sum() < (season_df.index.size / 4):
                    season_df.loc[:, season_df.columns[i]].fillna(round(season_df[season_df.columns[i]].mean(), 2),
                                                                  inplace=True)
                else:
                    vacant_time.append(season_df.columns[i])

            # 填充记录下的空缺时刻
            # 先用每一天该时刻前一个时刻或后一个时刻的数据填充该时刻
            if season_df.isnull().values.any():
                season_df.fillna(method='pad', axis=1, inplace=True)
            if season_df.isnull().values.any():
                season_df.fillna(method='backfill', axis=1, inplace=True)

            # 去除新填充的时刻的异常值
            for time in vacant_time:
                sta = (season_df[time] - season_df[time].mean()) / season_df[time].std()

                # 将异常数据设为空
                del_index = season_df[sta.abs() > outlier_boundary].index
                if del_index.size > 0:
                    season_df.loc[del_index, time] = None

            # 如果有空值则用均值填充
            for time in vacant_time:
                if season_df[time].isnull().sum() > 0:
                    season_df.loc[:, time].fillna(round(season_df[time].mean(), 2), inplace=True)

            # 保存修改后的文件
            season_df = season_df.T  # 时间为纵坐标，日期为横坐标
            save_path = os.path.join(save_folder_path, group + '\\' + community)
            if not os.path.exists(save_path):
                os.makedirs(save_path)
            for i in range(season_df.columns.size):
                date = season_df.columns[i]
                excel_name = community + "流量" + str(date)
                index_list = pd.to_datetime(season_df.index.map(lambda x: date + ' ' + x))
                new_season_df = pd.DataFrame(index=index_list, data=season_df[season_df.columns[i]].tolist(),
                                             columns=[community])
                new_season_df.to_excel(r'{0}\{1}.xlsx'.format(save_path, excel_name))
                print(community + "流量" + date + "完成！")
        print(community + "完成！")


remove_outlier(r'D:\日常\学习\大四\大四下\毕业设计\超声水表流量数据\筛选数据\按日拆分', r'D:\日常\学习\大四\大四下\毕业设计\超声水表流量数据\去除异常数据\按日拆分')
