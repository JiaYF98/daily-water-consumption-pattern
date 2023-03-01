"""
绘制不同小区不同季节的平均流量图
"""
import handle
import pandas as pd
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

color = {0: '#FF0000', 1: '#FFFF00', 2: '#0000FF'}


def save_picture(save_path, info, season, pic_name):
    # 保存
    pic_save_path = os.path.join(save_path,
                                 info.get('group') + '\\' + info.get('community') + '\\' + season)
    if not os.path.exists(pic_save_path):
        os.makedirs(pic_save_path)
    plt.savefig(r"{0}\{1}.png".format(pic_save_path, pic_name))


def draw_average_flow(folder_path, save_path=None):
    data_info = handle.getinfo(folder_path)
    for info in data_info:
        data_path = info.get('path')
        for season in os.listdir(data_path):
            file_path = os.path.join(data_path, season)
            df_combination_list = []

            # 绘制单个图
            for file in os.listdir(file_path):
                df = pd.read_excel(os.path.join(file_path, file), index_col='时间')
                df.index = pd.to_datetime(df.index, format='%H:%M')
                df_combination_list.append(df)

                # 绘图
                fig = plt.figure(figsize=(19.2, 10.8))
                ax = fig.add_subplot(111)
                ax.plot(df.index, df[df.columns[0]], label=file.split('.')[0])
                ax.set_title(file.split('.')[0], fontsize=24, pad=20)

                # 设置图像的文字显示
                handle.set_picture_display(ax, df, info)
                save_picture(save_path, info, season, file.split('.')[0])

                plt.close()
                print(file.split('.')[0] + '完成！')
            plt.close('all')

            # 绘制组合对比图
            df_combination = pd.concat(df_combination_list, axis=1, join='outer')
            color_list = []  # 图例文字使用不同的颜色
            fig = plt.figure(figsize=(19.2, 10.8))
            ax = fig.add_subplot(111)
            ax.set_title(info.get('community') + season + '用水量对比', fontsize=24, pad=20)
            for i in range(df_combination.columns.size):
                ax.plot(df_combination.index, df_combination[df_combination.columns[i]], color.get(i),
                        label=df_combination.columns[i])
                color_list.append(color.get(i))
            handle.set_picture_display(ax, df_combination, info, color_list)
            save_picture(save_path, info, season, info.get('community') + season + '用水量对比')

        plt.close('all')

        print(info.get('community') + '完成！')


draw_average_flow(r'D:\日常\学习\大四\大四下\毕业设计\超声水表流量数据\平均用水量\数据', r'D:\日常\学习\大四\大四下\毕业设计\超声水表流量数据\平均用水量\绘图')
