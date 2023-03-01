"""
绘制校核前后压力点的对比图，跟 waterdesk 软件中的图一样
"""
import os
import handle
import pandas as pd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

color_list = ['#FF0000', '#00FF00', '#0000FF']  # 图例文字使用不同的颜色


def draw_all(ax, df, info, pic_save_path):
    ax.cla()
    ax.scatter(df.index, df[df.columns[0]], label=df.columns[0], color=color_list[0])
    ax.plot(df.index, df[df.columns[1]], label=df.columns[1], color=color_list[1])
    ax.plot(df.index, df[df.columns[2]], label=df.columns[2], color=color_list[2])
    handle.set_picture_display(ax, df, info, color_list, 'pressure')
    # 保存
    plt.savefig(r'{0}\{1}.png'.format(pic_save_path, info.get('community') + '压力对比'))
    print(info.get('community') + '压力总对比图完成！')


def draw_single(ax, df, info, pic_save_path, no):
    ax.cla()
    ax.scatter(df.index, df[df.columns[0]], label=df.columns[0], color=color_list[0])
    ax.plot(df.index, df[df.columns[no]], label=df.columns[no], color=color_list[2])
    handle.set_picture_display(ax, df, info, [color_list[0], color_list[2]], 'pressure')
    # 保存
    plt.savefig(
        r'{0}\{1}.png'.format(pic_save_path, info.get('community') + df.columns[no].split('-')[1] + '压力对比'))
    print(info.get('community') + df.columns[no].split('-')[1] + '压力对比完成！')


def draw_pressure(folder_path, save_path=None):
    data_info = handle.getinfo(folder_path)
    for info in data_info:
        file_path = info.get('path')
        for file in os.listdir(file_path):
            # 创建保存路径
            pic_save_path = os.path.join(save_path, info.get('group') + '\\' + info.get('community'))
            if not os.path.exists(pic_save_path):
                os.makedirs(pic_save_path)

            df = pd.read_excel(os.path.join(file_path, file), index_col='时间')
            df.index = pd.to_datetime(df.index, format='%H:%M')
            fig = plt.figure(figsize=(19.2, 10.8))
            ax = fig.add_subplot(111)
            ax.set_title(file.split('.')[0] + '压力值', fontsize=24, pad=20)

            draw_all(ax, df, info, pic_save_path)

            for i in range(1, df.columns.size):
                draw_single(ax, df, info, pic_save_path, i)


draw_pressure(r'D:\日常\学习\大四\大四下\毕业设计\超声水表流量数据\压力对比\数据', r'D:\日常\学习\大四\大四下\毕业设计\超声水表流量数据\压力对比\绘图')
