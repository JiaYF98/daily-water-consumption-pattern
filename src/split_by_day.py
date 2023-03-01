"""
按日拆分原始数据，保存每日的流量数据
"""
import os
import pandas as pd

community_name = [["螺洲镇三期DN200"], ["融信湾花园", "金建小区二期42号楼DN200", "福湾新城春风苑DN200"]]


def split_by_day(data_path, save_path):
    # 获取excel路径
    path_list = os.listdir(data_path)
    file_path = []
    for i in range(len(path_list)):
        file_path.append(os.path.join(data_path, path_list[i]))

    # 创建存储路径
    new_save_path = []
    for child_path_list in path_list:
        new_save_path.append(os.path.join(save_path, child_path_list))
    for path in new_save_path:
        if not os.path.exists(path):
            os.makedirs(path)

    # 读取excel
    for i in range(len(file_path)):
        for file_name in os.listdir(file_path[i]):
            excel_path = os.path.join(file_path[i], file_name)
            df = pd.read_excel(excel_path, index_col='时间')
            df.index = pd.to_datetime(df.index)
            date_list = sorted(list(set(df.index.date)))
            for date in date_list:
                # 按日期拆分
                frame = df[df.index.date == date]
                excel_name = str(date)
                frame.to_excel(r'{0}\{1}.xlsx'.format(new_save_path[i], excel_name), index=True)
                print("完成{0}{1}拆分".format(path_list[i], excel_name))

                # 按小区拆分
                for community in community_name[i]:
                    small_frame = frame[community + "流量"]
                    excel_split_save_path = os.path.join(new_save_path[i], community)
                    if not os.path.exists(excel_split_save_path):
                        os.makedirs(excel_split_save_path)
                    excel_split_name = community + "流量" + str(date)
                    small_frame.to_excel(r'{0}\{1}.xlsx'.format(excel_split_save_path, excel_split_name))
                    print("完成{}拆分".format(excel_split_name))


split_by_day(r'D:\日常\学习\大四\大四下\毕业设计\超声水表流量数据\原始数据', r'D:\日常\学习\大四\大四下\毕业设计\超声水表流量数据\未筛选数据\按日拆分')
