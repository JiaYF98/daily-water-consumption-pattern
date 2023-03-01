"""
可设置一个绘制整个文件夹里所有图的方法，避免每次画图都要在不同文件下更换地址
也可以设置一个能实现全套流程的方法
此处的方法设置的保存路径可能不好使
"""
import os
import draw_by_day
import classify_by_week
import draw_by_week


def draw(folder):
    # draw_by_day.draw(os.path.join(folder, '按日拆分'), os.path.join(folder, '按日绘图'))
    classify_by_week.classify(os.path.join(folder, '按日拆分'), os.path.join(folder, '按周拆分'))
    draw_by_week.draw(os.path.join(folder, '按周拆分'), os.path.join(folder, '按周绘图'))


if __name__ == '__main__':
    draw(r'D:\日常\学习\大四\大四下\毕业设计\超声水表流量数据\未筛选数据')
