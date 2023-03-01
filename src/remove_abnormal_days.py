"""
通过K-means算法去除记录有很大误差的天数
测试代码可得聚类的轮廓系数，反映聚类效果
打开注释代码，注释掉训练部分代码，从主函数入口运行可只获取轮廓系数
"""
import os
import pandas as pd
import handle
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_samples
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler
import shutil
from itertools import chain


# 数据标准化
def normalize_data(df, method):
    # 最大最小值标准化
    if method == 'minmax':
        scaler = MinMaxScaler()
    elif method == 'standard':
        scaler = StandardScaler()
    else:
        return None
    scaler.fit(df)
    scaler_features = scaler.fit_transform(df)
    return pd.DataFrame(data=scaler_features, columns=df.columns, index=df.index)


def get_data(info, according='all'):
    data_path = info.get('path')
    data_list = []
    df = handle.get_all_flow_data(data_path)

    # 将df转换成日期为行，时间为列
    df = df.T
    # 去除一整天都缺失的数据
    df = df.dropna(how='all')
    date_index = df.index

    # 全部的数据在一起聚类
    if according == 'all':
        # 填充nan数据
        # 缺失数据用前一个不缺失数据填充
        if df.isnull().values.any():
            df.fillna(method='pad', axis=1, inplace=True)
        # 还有缺失的数据用后一个不缺失的数据填充
        if df.isnull().values.any():
            df.fillna(method='backfill', axis=1, inplace=True)

        # 数据标准化后加入数据列表
        data_list.append(normalize_data(df, 'minmax'))

    # 每个季节中的数据聚类(效果不佳)
    elif according == 'season':
        season_info = handle.get_season_info()
        for season in season_info:
            season_start = season_info.get(season).get('start')
            season_end = season_info.get(season).get('end')
            season_df = df[
                (df.index.map(lambda x: x[5:]) >= season_start) & (df.index.map(lambda x: x[5:]) <= season_end)]

            # 用均值填充nan 对每列进行遍历填充
            # 用每个时刻的均值填充
            for i in range(season_df.columns.size):
                season_df[season_df.columns[i]].fillna(season_df[season_df.columns[i]].mean(), inplace=True)

            # 还有缺失用前一个数据或后一个不缺失数据填充
            if season_df.isnull().values.any():
                season_df.fillna(method='pad', axis=1, inplace=True)
            if season_df.isnull().values.any():
                season_df.fillna(method='backfill', axis=1, inplace=True)

            # 数据标准化后加入数据列表
            data_list.append(normalize_data(season_df, 'standard'))

    # 按照每日的总流量聚类（效果不佳）
    elif according == 'flow':
        season_info = handle.get_season_info()
        for season in season_info:
            season_start = season_info.get(season).get('start')
            season_end = season_info.get(season).get('end')
            season_df = df[
                (df.index.map(lambda x: x[5:]) >= season_start) & (df.index.map(lambda x: x[5:]) <= season_end)]

            season_df = season_df.T
            means = season_df.mean().fillna(0)
            data_list.append(np.reshape(means.to_numpy(), (means.size, 1)))

    return data_list, date_index


# 返回df格式的日期和标签
def get_labels(info, according='all'):
    data_list, date_index = get_data(info, according)
    label_list = []

    for data in data_list:
        # 将df转换为 n×m 的矩阵
        train_data = np.array(data)

        # 进行训练
        kmeans = KMeans(n_clusters=2)
        kmeans.fit(train_data)
        means = np.mean(silhouette_samples(train_data, kmeans.labels_, metric='euclidean'))
        # 根据评估指标判断是否要保留训练标签
        if means > 0.5 or (according == 'all' and means > 0.4):
            temp_label = pd.DataFrame(kmeans.labels_, columns=['label'])
            if temp_label['label'].mean() > 0.5:
                label_list.append(temp_label['label'].map({0: 'False', 1: 'True'}))
            else:
                label_list.append(temp_label['label'].map({0: 'True', 1: 'False'}))
            center = kmeans.cluster_centers_
        else:
            temp_label = pd.Series(['True'] * data.index.size)
            label_list.append(temp_label)

        # # 测试
        # means = []
        # for i in range(2, 10):
        #     kmeans = KMeans(n_clusters=i)
        #     kmeans.fit(train_data)
        #     label = kmeans.labels_
        #     center = kmeans.cluster_centers_
        #     means.append(np.mean(silhouette_samples(train_data, label, metric='euclidean')))
        # print(means)

    # 将标签合为一个整体
    # 保存日期和标签，便于后面去除异常日期
    label = list(chain.from_iterable(label_list))
    df = pd.DataFrame(index=date_index, data=label, columns=['label'])
    df.index.name = '日期'
    return df


def remove_abnormal_days(source_folder_path, save_folder_path, according='all'):
    data_info = handle.getinfo(source_folder_path)
    for info in data_info:
        label = get_labels(info, according)

        # 找出对的日期 并保存
        date_list = label[label['label'] == 'True'].index.tolist()
        for date in date_list:
            file_name = os.path.join(info.get('path'), info.get('community') + '流量' + date + '.xlsx')
            child_path = info.get('group') + '\\' + info.get('community')
            save_path = os.path.join(save_folder_path, child_path)
            if not os.path.exists(save_path):
                os.makedirs(save_path)
            shutil.copy(file_name, save_path)
            print(info.get('community') + ' ' + date + '完成！')

        print(info.get('community') + '完成！')
    print('全部完成！')


remove_abnormal_days(r'D:\日常\学习\大四\大四下\毕业设计\超声水表流量数据\未筛选数据\按日拆分', r'D:\日常\学习\大四\大四下\毕业设计\超声水表流量数据\筛选数据\按日拆分')

# if __name__ == '__main__':
#     data_info = handle.getinfo(r'D:\日常\学习\大四\大四下\src\超声水表流量数据\未筛选数据\按日拆分')
#     for info in data_info:
#         get_labels(info)
