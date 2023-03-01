"""
根据拆分的每日流量绘制每日流量图，以大致观察流量变化范围，便于确定图例的显示范围
"""
import os
import pandas as pd
import handle
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False


def draw(path, save_path):
    data_info = handle.getinfo(path)
    # data_info 由 path, group, community 三部分组成
    for info in data_info:
        data_path = info.get('path')
        file_dir = os.listdir(data_path)
        for file in file_dir:
            excel_path = os.path.join(data_path, file)
            df = pd.read_excel(excel_path, index_col='时间')
            pic_save_path = os.path.join(save_path, info.get('group') + '\\' + info.get('community'))
            if not os.path.exists(pic_save_path):
                os.makedirs(pic_save_path)

            # 创建绘图框
            fig = plt.figure(figsize=(19.2, 10.8))
            ax = fig.add_subplot(111)
            ax.plot(df.index, df[df.columns[0]], label=df.index[0].strftime('%Y-%m-%d'))

            # 设置图像的标题
            title_name = df.columns[0] + ' ' + df.index[0].strftime('%Y-%m-%d')
            ax.set_title(title_name, fontsize=24, pad=20)  # 设置坐标轴名称及位置

            # 设置绘图显示的坐标和图例
            handle.set_picture_display(ax, df, info)

            # 保存图片
            plt.savefig(r"{0}\{1}.png".format(pic_save_path, file))
            # plt.show()
            plt.close()
            print(title_name + "完成！")
        plt.close('all')
    print("全部完成！")


draw(r"D:\日常\学习\大四\大四下\毕业设计\超声水表流量数据\未筛选数据\按日拆分", r"D:\日常\学习\大四\大四下\毕业设计\超声水表流量数据\未筛选数据\按日绘图")
