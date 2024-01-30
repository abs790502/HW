import pandas as pd

df = pd.read_csv('Australian Vehicle Prices.csv')
# df.info()   最多有16733 比樣本
#先查看缺少的值有多少
# df.isnull().sum() 可以看到每行都有缺失值，其中Doors 與 Seats 缺少最多

# df.dropna(inplace=True) #移除缺失值
# df.isnull().sum() 移除後缺失值為0,但樣本數剩下14586比  ***要注意比原始資料少了12.8% ，此次分析不需要考慮Doors,Seats,Location 故先把這幾行的空格填入虛擬(virtual)
df['Location'].fillna('virtual', inplace=True)
df['Doors'].fillna('virtual', inplace=True)
df['Seats'].fillna('virtual', inplace=True)
df['Price'] = pd.to_numeric(df['Price'], errors='coerce') #price 欄位中有'POA' 故先把無效資訊轉成空值
df.dropna(inplace=True)
# df.info()   還有16389 比樣本 比原始資料少2% ，故將以此整理後資料進行數據分析

