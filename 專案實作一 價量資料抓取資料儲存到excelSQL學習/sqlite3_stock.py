import yfinance as yf
import pandas as pd
import openpyxl as xl
import sqlite3



ticker = "2330.TW"  # 台積電的股票代碼
stock_data = yf.download(ticker, start="2023-01-01", end="2024-07-10")
         
# 查看資料
print(stock_data.head())
stock_data.to_excel("taiwan_stock_data.xlsx")

conn = sqlite3.connect('taiwan_stock_data.db')
c = conn.cursor()

# 創建股票資料表
c.execute('''CREATE TABLE IF NOT EXISTS stock_data
            (Date text, Open real, High real, Low real, Close real, Adj_Close real, Volume integer)''')
         
# 將Pandas DataFrame資料插入到資料表中
stock_data.to_sql('stock_data', conn, if_exists='replace', index=True)
         
# 執行基本查詢操作
c.execute('SELECT * FROM stock_data LIMIT 5')
print(c.fetchall())
         
# 關閉連接
conn.close()