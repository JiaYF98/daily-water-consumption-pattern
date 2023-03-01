"""
常用函数，降低代码重复耦合
返回假日部分代码需更改
"""
import os
import pandas as pd
import datetime
import matplotlib.dates as dates
import matplotlib.ticker as mticker


# 返回读取文件的目录及其分组
def getinfo(path):
    os.chdir(path)
    group_name = [name for name in os.listdir() if os.path.isdir(name)]
    dir_path = [os.path.join(path, x) for x in group_name]
    data_info = []
    for child_dir_path in dir_path:
        os.chdir(child_dir_path)
        for pth in os.listdir():
            if os.path.isdir(pth):
                data_info.append({'path': os.path.join(child_dir_path, pth), 'group': os.path.basename(child_dir_path),
                                  'community': pth})
    return data_info


# 将该文件夹中所有日期的数据读到一个df中
def get_all_flow_data(data_path):
    df_list = []
    for file in os.listdir(data_path):
        excel_path = os.path.join(data_path, file)
        temp_df = pd.read_excel(excel_path, index_col='时间')

        date = temp_df.index[0].strftime('%Y-%m-%d')
        temp_df.rename(columns={temp_df.columns[0]: date}, index=lambda x: x.strftime('%H:%M'), inplace=True)
        df_list.append(temp_df)

    # 将list格式转换为df格式
    df = pd.concat(df_list, axis=1, join='outer')
    return df


# 设置绘图显示的坐标和图例
def set_picture_display(ax, df, info, color_list=None, draw_type='flow'):
    # 显示图例
    ax.legend(loc=2, fontsize=16, labelcolor=color_list, borderpad=0.4, labelspacing=0.6)

    # 设置坐标轴名称及位置
    ax.set_xlabel(u'时间($h$)', fontsize=18, labelpad=20)
    if draw_type == 'flow':
        ax.set_ylabel(u'流量($m^3/h$)', fontsize=18, labelpad=20)
    elif draw_type == 'pressure':
        ax.set_ylabel(u'压力(m)', fontsize=18, labelpad=20)
    elif draw_type == 'variation curve':
        ax.set_ylabel(u'时用水量占全日的百分数(%)', fontsize=18, labelpad=20)

    # 设置x轴刻度
    # 主刻度
    formatter = dates.DateFormatter('%H:%M')
    ax.xaxis.set_major_locator(dates.HourLocator(range(0, 24, 1)))
    ax.xaxis.set_major_formatter(formatter)
    # 次刻度
    ax.xaxis.set_minor_locator(dates.MinuteLocator(range(0, 60, 30)))

    # 设置y轴刻度
    y_major_tick_spacing = None  # 主刻度间距
    y_minor_tick_spacing = None  # 次刻度间距

    if draw_type == 'flow':
        y_major_tick_spacing = 10  # 主刻度间距
        y_minor_tick_spacing = 5  # 次刻度间距
    elif draw_type == 'pressure':
        y_major_tick_spacing = 1  # 主刻度间距
        y_minor_tick_spacing = 0.1  # 次刻度间距
    elif draw_type == 'variation curve':
        y_major_tick_spacing = 1  # 主刻度间距
        y_minor_tick_spacing = 0.5  # 次刻度间距

    ax.yaxis.set_major_locator(mticker.MultipleLocator(y_major_tick_spacing))
    ax.yaxis.set_minor_locator(mticker.MultipleLocator(y_minor_tick_spacing))

    # 设置x轴显示范围
    ax.set_xlim(left=df.index[0], right=df.index[-1])

    # 设置y轴显示范围
    current_community = info.get('community')
    if draw_type == 'flow':
        community_flow = get_community_flow(current_community)
        ax.set_ylim(community_flow.get('min'), community_flow.get('max'))
    elif draw_type == 'pressure':
        community_pressure = get_community_pressure(current_community)
        ax.set_ylim(community_pressure.get('min'), community_pressure.get('max'))
    elif draw_type == 'variation curve':
        ax.set_ylim(0, 10)

    # 显示刻度线
    ax.xaxis.grid(True, which='major')
    ax.yaxis.grid(True, which='major')

    # datetime类型没有24:00
    # 制作x轴标签
    time, time_label = get_time_label(df.index[0], df.index[0] + datetime.timedelta(days=1))

    # 设置x轴标签（画出的图不能显示每个时刻，只能显示标签的时刻）
    ax.set_xticks(time)
    ax.set_xticklabels(time_label)

    # 设置坐标轴刻度的显示效果
    ax.tick_params(labelsize=13, pad=10)


# 返回时间刻度和刻度标签
def get_time_label(time_start, time_end):
    time = pd.date_range(start=time_start, end=time_end, freq='h')
    time_label = sorted(list(set([label.strftime('%H:%M') for label in time])), reverse=False)
    time_label.append('24:00')
    return time, time_label


# 返回各组的流量范围
def get_community_flow(community):
    return {'螺洲镇三期DN200': {'min': 20, 'max': 120}, '福湾新城春风苑DN200': {'min': 0, 'max': 100},
            '金建小区二期42号楼DN200': {'min': 0, 'max': 80}, '融信湾花园': {'min': 0, 'max': 70}}.get(community)


# 返回各组的压力范围
def get_community_pressure(community):
    return {'螺洲镇三期DN200': {'min': 20, 'max': 28}, '福湾新城春风苑DN200': {'min': 15, 'max': 24},
            '金建小区二期42号楼DN200': {'min': 19, 'max': 24}, '融信湾花园': {'min': 25, 'max': 30}}.get(community)


# 返回福州季节范围
def get_season_info():
    # 5月6号入夏，最早数据从5月1号开始
    # 10月20号入秋，大致从11月1号开始用水量明显变化
    # 综上所述，夏季和秋季的开始结束时间略作调整
    return {'夏季': {'start': '05-01', 'end': '10-31'}, '秋季': {'start': '11-01', 'end': '12-31'}}


# 返回假日
# 此处可按照节日分类修改代码，设置节日的起止日期自动生成中间的日期以避免手工大量输入
def get_holiday():
    return ['05-01', '05-02', '05-03', '05-04', '05-05', '06-12', '06-13', '06-14', '09-19', '09-20', '09-21', '10-01',
            '10-02', '10-03', '10-04', '10-05', '10-06', '10-07']
