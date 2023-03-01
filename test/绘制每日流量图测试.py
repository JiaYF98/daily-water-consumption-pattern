import datetime
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as dates
import matplotlib.ticker as mticker
import matplotlib as mpl

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

group_flow = {'水质47组': {'min': 20, 'max': 170}, '水质48组': {'min': 0, 'max': 100}}

df = pd.read_excel(r'C:\Users\embrace\Desktop\2021-05-01.xlsx', index_col='时间')

fig = plt.figure(figsize=(15, 7.5))
ax = fig.add_subplot(111)
ax.plot(df.index, df[df.columns[0]], color='dodgerblue', label=df.columns[0])

# 设置图像的标题
title_name = df.columns[0] + df.index[0].strftime('%Y-%m-%d')
ax.set_title(title_name, fontsize=12)

# 设置x轴名称
ax.set_xlabel('时间', fontsize=10)
ax.set_ylabel('流量', fontsize=10)

# 设置x轴显示范围
ax.set_xlim(left=df.index[0], right=df.index[0] + datetime.timedelta(days=1))
# 设置y轴显示范围
ax.set_ylim(bottom=flow.get(df.columns[0]).get('min'), top=flow.get(df.columns[0]).get('max'))

# 设置x轴刻度
# 主刻度
formatter = dates.DateFormatter('%H:%M')
ax.xaxis.set_major_locator(dates.HourLocator(range(0, 24, 1)))
ax.xaxis.set_major_formatter(formatter)
# 次刻度
ax.xaxis.set_minor_locator(dates.MinuteLocator(range(0, 60, 30)))
# ax.xaxis.set_minor_formatter(formatter)

# 设置y轴刻度
y_major_tick_spacing = 10  # 主刻度间距
y_minor_tick_spacing = 5  # 次刻度间距
ax.yaxis.set_major_locator(mticker.MultipleLocator(y_major_tick_spacing))
ax.yaxis.set_minor_locator(mticker.MultipleLocator(y_minor_tick_spacing))

# 显示刻度线
ax.xaxis.grid(True, which='major')
ax.yaxis.grid(True, which='major')

# datetime类型没有24:00
# 制作x轴标签
time_start = df.index[0]
time_end = df.index[0] + datetime.timedelta(days=1)
time = pd.date_range(start=time_start, end=time_end, freq='h')
time_label = sorted(list(set([label.strftime('%H:%M') for label in time])), reverse=False)
time_label.append('24:00')

# 设置x轴标签（画出的图不能显示每个时刻，只能显示标签的时刻）
# ax.set_xticks(time)
# ax.set_xticklabels(time_label)

# 添加图例
ax.legend(fontsize=8, labelcolor='black')

plt.show()
