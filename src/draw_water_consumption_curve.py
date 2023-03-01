"""
绘制时用水量变化曲线对比图
"""
import os
import handle
import matplotlib.pyplot as plt
import pandas as pd

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

color_list = ['#000000', '#0000FF', '#FF0000']


def draw_water_consumption_curve(folder_path, save_path=None):
    data_info = handle.getinfo(folder_path)
    for info in data_info:
        file_path = info.get('path')
        for file in os.listdir(file_path):
            df = pd.read_excel(os.path.join(file_path, file), index_col='时间')
            df.index = pd.to_datetime(df.index, format='%H:%M')
            total_flow = df.sum()
            for i in range(0, 24):
                df[df.index.hour == i] = df[df.index.hour == i].sum() / total_flow * 100

            changed_kh = df[df.columns[0]].max() * 24 / 100
            original_kh = df[df.columns[1]].max() * 24 / 100
            average_percentage = 100 / 24

            pic_save_path = os.path.join(save_path, info.get('group') + '\\' + info.get('community'))
            if not os.path.exists(pic_save_path):
                os.makedirs(pic_save_path)

            fig = plt.figure(figsize=(19.2, 10.8))
            ax = fig.add_subplot(111)
            ax.set_title(info.get('community') + '时用水量变化曲线', fontsize=24, pad=20)

            # 比例平均值
            ax.axhline(average_percentage, color=color_list[0],
                       label='平均值({}%)'.format(round(average_percentage, 2)), linestyle='--')

            # 原用水规律
            ax.plot(df.index, df[df.columns[1]], label='原时用水量变化曲线({0} = {1})'.format('$k_{h}$', round(original_kh, 2)),
                    color=color_list[1])

            # 实测用水规律
            ax.plot(df.index, df[df.columns[0]],
                    label='基于实测流量的时用水量变化曲线({0} = {1})'.format('$k_{h}$', round(changed_kh, 2)),
                    color=color_list[2])

            # 设置绘图显示的坐标和图例
            handle.set_picture_display(ax, df, info, color_list, 'variation curve')

            # 保存
            plt.savefig(r'{0}\{1}.png'.format(pic_save_path, info.get('community') + '用水量变化曲线'))
            print(info.get('community') + '用水量变化曲线完成！')


draw_water_consumption_curve(r'D:\日常\学习\大四\大四下\毕业设计\超声水表流量数据\平均用水量\用水量变化', r'D:\日常\学习\大四\大四下\毕业设计\超声水表流量数据\平均用水量\用水量曲线')
