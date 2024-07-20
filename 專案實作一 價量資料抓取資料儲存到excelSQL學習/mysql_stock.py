import yfinance as yf
import openpyxl as xl
import mysql.connector
import pandas as pd
import pymysql

# 台積電的股票代碼
ticker = "2330.TW"  
stock_data = yf.download(ticker, start="2023-01-01", end="2024-07-10")
         
# 查看資料
print(stock_data.head())
stock_data.to_excel("taiwan_stock_data.xlsx")


stock = "./taiwan_stock_data.xlsx"
df = pd.read_excel(stock)

# 用pymysql 連結MYSQL
db = pymysql.connect(host="localhost",
                     user="root",
                     password="lin790502",
                     database='stock')

cursor = db.cursor()

# 確認是否有連結到MYSQL
cursor.execute("SELECT VERSION()")
data = cursor.fetchone()
print ("Database version : " + str(data))
db.close()

# 顯示DATABASE內容，並創建
cursor.execute("CREATE DATABASE stock")
cursor.execute("SHOW DATABASES")

# table 中增加tsmc
cursor.execute("CREATE TABLE TSMC (`Date` DATE, `Open` FLOAT,`High` FLOAT,`Low` FLOAT,`Close` FLOAT,`Adj Close` FLOAT,`Volume` INT  )")

#插入SQL語法
sql = "INSERT INTO TSMC (`Date`, `Open`, `High`, `Low`, `Close`, `Adj Close`, `Volume` ) VALUES (%s, %s, %s, %s, %s, %s, %s)"

#匯入Excel 檔案
for index, row in df.iterrows():
    val = (row['Date'], row['Open'], row['High'], row['Low'], row['Close'], row['Adj Close'], row['Volume'])
    try:
        cursor.execute(sql, val)
    except pymysql.MySQLError as e:
        print(f"Error: {e}")

db.commit()

#顯示插入的行數
print(cursor.rowcount, "OK !")

#確認資料
print(f"Executing SQL: {sql}")
print(f"Values: {val}")
cursor.close()
db.close()





