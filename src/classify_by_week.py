"""
将按日拆分的数据按小区和周次组合
"""
import os
import handle
import pandas as pd


def classify(folder_path, save_path):
    data_info = handle.getinfo(folder_path)
    for info in data_info:
        data_path = info.get('path')
        group_name = info.get('group')
        community_name = info.get('community')
        for file in os.listdir(data_path):
            excel_path = os.path.join(data_path, file)
            df = pd.read_excel(excel_path, index_col='时间')

            # 将索引去掉日期，并修改列名
            week = df.index[0].week
            date = df.index[0].strftime('%Y-%m-%d')
            df.rename(columns={df.columns[0]: date}, index=lambda x: x.strftime('%H:%M'), inplace=True)  # 将流量列的名称改为日期

            # 创建保存目录
            save_dir = os.path.join(save_path, group_name + '\\' + community_name + '\\week' + str(week))
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)

            # 保存excel
            df.to_excel(r"{0}\{1}.xlsx".format(save_dir, date), index=True)
            print(community_name + "流量" + date + "归类完成！")
    print("全部完成！")


classify(r'D:\日常\学习\大四\大四下\毕业设计\超声水表流量数据\未筛选数据\按日拆分', r'D:\日常\学习\大四\大四下\毕业设计\超声水表流量数据\未筛选数据\按周拆分')
