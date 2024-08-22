import yfinance as yf
import openpyxl as xl
import mysql.connector
import pandas as pd
import pymysql
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


# 台積電的股票代碼
ticker2330 = "2330.TW"  
stock2330_data = yf.download(ticker2330, start="2023-01-01", end="2024-07-10")


stock2330_data['Ret_daily'] = stock2330_data['Adj Close'].pct_change()
stock2330_data['Ret_daily%'] = stock2330_data['Ret_daily'] *100
stock2330_data['Ret_daily加1'] = stock2330_data['Ret_daily'] +1
stock2330_data['Avg_5D'] = stock2330_data['Adj Close'].rolling(window=5).mean()
stock2330_data['Avg_20D'] = stock2330_data['Adj Close'].rolling(window=20).mean()
stock2330_data['Avg_60D'] = stock2330_data['Adj Close'].rolling(window=60).mean()
stock_data = stock2330_data.drop(['Ret_daily%','Ret_daily加1'], axis=1)

# 0050的股票代碼
ticker0050 = "0050.TW"  
stock0050_data = yf.download(ticker0050, start="2023-01-01", end="2024-07-10")


stock0050_data['Ret_daily'] = stock0050_data['Adj Close'].pct_change()
stock0050_data['Ret_daily%'] = stock0050_data['Ret_daily'] *100
stock0050_data['Ret_daily加1'] = stock0050_data['Ret_daily'] +1
stock0050_data['Avg_5D'] = stock0050_data['Adj Close'].rolling(window=5).mean()
stock0050_data['Avg_20D'] = stock0050_data['Adj Close'].rolling(window=20).mean()
stock0050_data['Avg_60D'] = stock0050_data['Adj Close'].rolling(window=60).mean()
stock0050_data = stock0050_data.drop(['Ret_daily%','Ret_daily加1'], axis=1)
         
# 查看資料
print(stock2330_data.head())
print(stock0050_data.head())

# -----------------分隔線----------------------------------
stock2330_data.to_excel("taiwan_stock2330_data.xlsx")
stock0050_data.to_excel("taiwan_stock0050_data.xlsx")

stock2330 = "./taiwan_stock2330_data.xlsx"
stock0050 = "./taiwan_stock0050_data.xlsx"

df2330 = pd.read_excel(stock2330)
df0050 = pd.read_excel(stock0050)
df2330.dropna(inplace=True) #移除缺失值
df0050.dropna(inplace=True) #移除缺失值

# 用pymysql 連結MYSQL
conn = pymysql.connect(host="localhost",
                     user="root",
                     password="lin790502",
                     database="stock"
                     )
cursor = conn.cursor()

# 確認是否有連結到MYSQL
cursor.execute("SELECT VERSION()")
data = cursor.fetchone()

print ("Database version : " + str(data))
##關閉db
# db.close()

## 顯示DATABASE內容，並創建

# cursor.execute("CREATE DATABASE stock")
cursor.execute("SHOW DATABASES")
for x in cursor:
    print(x)

df_sql_0050 = pd.read_sql_query("select * from `0050`",conn)
df_sql_2330 = pd.read_sql_query("select * from `tsmc`",conn)
print(df_sql_0050)
print(df_sql_2330)

df_sql_2330.dropna(inplace=True) #移除缺失值
df_sql_0050.dropna(inplace=True) #移除缺失值

df_sql_0050 = df_sql_0050.rename(columns={'Ret_daily': 'Ret_daily_0050'})

## 創造一個只包含 Date 和 Return 的 dataframe，以便後續合併 Dataframe
df_0050_ret = df_sql_0050[['Date', 'Ret_daily_0050']]
print(df_0050_ret.tail(5))

# 將0050的Return 合併至new dataframe 
## 合併後，存入新的dataframe，命名為stock_df
stock_df = pd.merge(df_sql_2330 , df_0050_ret, on='Date')
print(stock_df.head())

# ## 累積複利計算
stock_df['Ret加1'] = stock_df['Ret_daily'] +1 #計算複利
stock_df['Ret_5D_backward'] = stock_df['Ret加1'].rolling(window=5).apply(np.prod)

#往後算五日的複利報酬
stock_df['Ret_5D_forward'] = stock_df['Ret加1'].shift(-5).rolling(window=5).apply(np.prod) 

## 計算2330 的未來20日累積複利報酬
stock_df['Ret_20D_forward'] = stock_df['Ret加1'].shift(-20).rolling(window=20).apply(np.prod)
#計算0050 的未來20日累積複利報酬
stock_df['Ret_0050加1'] = stock_df['Ret_daily_0050'] +1 #計算複
stock_df['Ret_20D_forward_0050'] = stock_df['Ret_0050加1'].shift(-20).rolling(window=20).apply(np.prod)

# 設定黃金交叉日
#計算移動平均
stock_df['Avg_5D'] = stock_df['Adj Close'].rolling(window=5).mean()
stock_df['Avg_10D'] = stock_df['Adj Close'].rolling(window=10).mean()

# 定義 5日移動平均 (MA5) > 10日移動平均 (MA10)
stock_df['MA5_above_MA10'] = np.where(stock_df['Avg_5D']>stock_df['Avg_10D'], 1, 0)

# 定義黃金交叉: 5日平均 從小於(等於)變為大於 10日移動平均 
# shift(1) 取得Row的前一筆資料
stock_df['Golden_MA5_MA10'] = np.where( stock_df['MA5_above_MA10'] > stock_df['MA5_above_MA10'].shift(1) , 1, 0)

#只保留 黃金交叉日的資料，以便比較
#創立一個新的df，只保留想要用的資料
df_Gold_MA5_MA10 = stock_df[['Date', 'Golden_MA5_MA10', 'Ret_20D_forward', 'Ret_20D_forward_0050']]

#只保留 黃金交叉日的資料，以便比較
df_Gold_MA5_MA10 = df_Gold_MA5_MA10.loc[df_Gold_MA5_MA10['Golden_MA5_MA10'] == 1]



# 去除包含遺失值(NaN)的row
df_no_NaN = df_Gold_MA5_MA10.dropna(subset=['Ret_20D_forward', 'Ret_20D_forward_0050'])
print('------最終結果-------')
print(df_no_NaN.describe())




# # table 中增加tsmc
# # cursor.execute("CREATE TABLE TSMC (\
# #                `Date` DATE, \
# #                `Open` FLOAT,\
# #                `High` FLOAT,\
# #                `Low` FLOAT,\
# #                `Close` FLOAT,\
# #                `Adj Close` FLOAT,\
# #                `Volume` INT,\
# #                `Ret_daily` FLOAT,\
# #                 `Avg_5D` FLOAT,\
# #                 `Avg_20D` FLOAT,\
# #                 `Avg_60D` FLOAT)")

# # table 中增加0050
# cursor.execute("CREATE TABLE `0050` (\
#                `Date` DATE, \
#                `Open` FLOAT,\
#                `High` FLOAT,\
#                `Low` FLOAT,\
#                `Close` FLOAT,\
#                `Adj Close` FLOAT,\
#                `Volume` INT,\
#                `Ret_daily` FLOAT,\
#                 `Avg_5D` FLOAT,\
#                 `Avg_20D` FLOAT,\
#                 `Avg_60D` FLOAT)")




# #插入SQL語法

# sql2330 = """
#     INSERT INTO TSMC (
#         `Date`, `Open`, `High`, `Low`, `Close`, `Adj Close`, `Volume`,
#         `Ret_daily`, `Avg_5D`, `Avg_20D`, `Avg_60D`
#     ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
# """



# sql0050 = """
#     INSERT INTO `0050` (
#         `Date`, `Open`, `High`, `Low`, `Close`, `Adj Close`, `Volume`,
#         `Ret_daily`, `Avg_5D`, `Avg_20D`, `Avg_60D`
#     ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
# """


# # #匯入Excel 檔案
# for index, row in df2330.iterrows():
#     val2330 = (row['Date'], row['Open'], row['High'], row['Low'], row['Close'], row['Adj Close'], row['Volume'],row['Ret_daily'], row['Avg_5D'], row['Avg_20D'], row['Avg_60D'])
#     try:
#         cursor.execute(sql2330, val2330)
#     except pymysql.MySQLError as e2330:
#         print(f"Error: {e2330}")

# for index, row in df0050.iterrows():
#     val0050 = (row['Date'], row['Open'], row['High'], row['Low'], row['Close'], row['Adj Close'], row['Volume'],row['Ret_daily'], row['Avg_5D'], row['Avg_20D'], row['Avg_60D'])
#     try:
#         cursor.execute(sql0050, val0050)
#     except pymysql.MySQLError as e0050:
#         print(f"Error: {e0050}")

# db.commit()




# #確認資料
# print(f"Executing SQL: {sql2330}")
# print(f"Executing SQL: {sql0050}")
# print(f"Values: {val2330}")
# print(f"Values: {val0050}")


# #畫圖

# df2330["Date"] = pd.to_datetime(df2330["Date"])
# df0050["Date"] = pd.to_datetime(df0050["Date"])
# df2330.set_index("Date", inplace=True)
# df0050.set_index("Date", inplace=True)

# fig, axs = plt.subplots(2, 1, figsize=(8, 8))

# axs[0].plot(df2330['Adj Close'], label='Adj Close')
# axs[0].plot(df2330['Avg_5D'], label='5_Day_Mean')
# axs[0].plot(df2330['Avg_20D'], label='20_Day_Mean')
# axs[0].plot(df2330['Avg_60D'], label='60_Day_Mean')
# axs[0].legend(loc='best', shadow=True, fontsize='x-large')
# axs[0].set_title(ticker2330 + '_yahoo_finance')
# axs[0].set_xlabel('Date')
# axs[0].set_ylabel('Price')




# axs[1].plot(df0050['Adj Close'], label='Adj Close')
# axs[1].plot(df0050['Avg_5D'], label='5_Day_Mean')
# axs[1].plot(df0050['Avg_20D'], label='20_Day_Mean')
# axs[1].plot(df0050['Avg_60D'], label='60_Day_Mean')
# axs[1].legend(loc='best', shadow=True, fontsize='x-large')
# axs[1].set_title(ticker0050 + '_yahoo_finance')
# axs[1].set_xlabel('Date')
# axs[1].set_ylabel('Price')  






