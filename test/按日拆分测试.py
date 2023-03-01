import pandas as pd

community_name = [["螺洲镇三期DN200流量"], ["融信湾花园流量", "金建小区二期42号楼DN200流量", "福湾新城春风苑DN200流量"]]
data_name = [["水质47组5月", "水质47组6月", "水质47组7月", "水质47组9月", "水质47组10月", "水质47组11月", "水质47组12月"],
             ["水质48组6月", "水质48组7月", "水质48组8月", "水质48组9月", "水质48组10月", "水质48组11月", "水质48组12月"]]


def excel_split(file_name, cols_name):
    data = pd.read_excel('D:/日常/学习/大四/大四下/src/超声水表流量数据/{}.xlsx'.format(file_name), index_col='时间')
    new_list_date = sorted(list(set(data.index.map(lambda x: x[0: 10]))))
    for frame in new_list_date:
        excel_small = data[data.index.map(lambda x: x[0: 10]) == frame]
        excel_small.to_excel('D:/日常/学习/大四/大四下/src/超声水表流量数据/数据拆分/{0}/{1}.xlsx'
                             .format(file_name[0: 5], frame), index=True)
        print("完成{}{}拆分".format(file_name[0: 5], frame))
        for cols_len in range(len(cols_name)):
            excel_split_community = excel_small[cols_name]
            excel_split_community.to_excel('D:/日常/学习/大四/大四下/src/超声水表流量数据/数据拆分/{0}/{1}/{1}{2}.xlsx'
                                           .format(file_name[0: 5], cols_name[cols_len], frame, index=True))
            print("完成{}{}拆分".format(cols_name[cols_len], frame))


def get_file_name(i_, j_):
    return data_name[i_][j_]


def get_community_name(i_):
    return community_name[i_]


for i in range(len(data_name)):
    for j in range(len(data_name[i])):
        excel_split(get_file_name(i, j), get_community_name(i))
        print("{}完成！".format(get_file_name(i, j)))

print("\n全部完成！")
