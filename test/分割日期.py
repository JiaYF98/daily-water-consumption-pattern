import pandas as pd

df = pd.read_excel('C:/Users/embrace/Desktop/螺洲镇三期DN200流量2021-05-01.xlsx')
date = str(df['时间'][0])[0: 10]
print(date)
df_temp = df['时间'].astype(str).str.split(expand=True)
df['时间'] = df_temp[1]
df.columns = ['时间', '{}'.format(date)]
df.set_index('时间', inplace=True)
print(df)
df.to_excel('C:/Users/embrace/Desktop/螺洲镇三期DN200流量2021-05-01分割.xlsx')
