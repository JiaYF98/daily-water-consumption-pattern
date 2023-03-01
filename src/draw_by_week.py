"""
根据按周组合的流量数据，绘制小区一个周的每日流量图，更直观的反映用水规律
"""
import handle
import os
import pandas as pd
import datetime as dt
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

color = {1: '#FF0000', 2: '#FF7F00', 3: '#FFFF00', 4: '#00FF00', 5: '#00FFFF', 6: '#0000FF', 7: '#8B00FF'}


def draw(folder_path, save_path):
    data_info = handle.getinfo(folder_path)
    for info in data_info:
        data_path = info.get('path')
        week_list = os.listdir(data_path)
        for week in week_list:
            excel_path = os.path.join(data_path, week)
            pic_save_path = os.path.join(save_path, info.get('group') + '\\' + info.get('community'))

            # 创建保存路径
            if not os.path.exists(pic_save_path):
                os.makedirs(pic_save_path)

            # 将数据按周合并
            temp_df = []
            for excel_file in os.listdir(excel_path):
                temp_df.append(pd.read_excel(os.path.join(excel_path, excel_file), index_col='时间'))
            df = pd.concat(temp_df, axis=1, join='outer')
            df.index = pd.to_datetime(df.index, format='%H:%M')

            # 绘图
            title_name = info.get('community') + "流量(" + str(week) + ")"
            fig = plt.figure(figsize=(19.2, 10.8))
            ax = fig.add_subplot(111)
            ax.set_title(title_name, fontsize=24, pad=20)

            # 绘制每一条流量曲线
            color_list = []  # 图例文字使用不同的颜色
            for i in range(df.columns.size):
                date = dt.datetime.strptime(df.columns[i], '%Y-%m-%d')
                weekday = date.isoweekday()
                ax.plot(df.index, df[df.columns[i]], color=color.get(weekday),
                        label=df.columns[i] + '(' + date.strftime("%a") + ')')
                color_list.append(color.get(weekday))

            # 设置绘图显示的坐标和图例
            handle.set_picture_display(ax, df, info, color_list)

            # 保存图片
            plt.savefig(r"{0}\{1}.png".format(pic_save_path, title_name))
            plt.close()
            print(title_name + "完成!")

        plt.close('all')

    print("全部完成！")


draw(r'D:\日常\学习\大四\大四下\毕业设计\超声水表流量数据\筛选数据\按周拆分', r'D:\日常\学习\大四\大四下\毕业设计\超声水表流量数据\筛选数据\按周绘图')
