import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('Australian Vehicle Prices.csv')
# df.info()   最多有16733 比樣本
#先查看缺少的值有多少
# df.isnull().sum() 可以看到每行都有缺失值，其中Doors,Seats,Location 缺少最多

# df.dropna(inplace=True) #移除缺失值
# df.isnull().sum() 移除後缺失值為0,但樣本數剩下14586比  ***要注意比原始資料少了12.8% ，此次分析不需要考慮Doors,Seats,Location 故先把這幾行的空格填入虛擬(virtual)
df['Location'].fillna('virtual', inplace=True)
df['Doors'].fillna('virtual', inplace=True)
df['Seats'].fillna('virtual', inplace=True)
df['Price'] = pd.to_numeric(df['Price'], errors='coerce') #price 欄位中有'POA' 故先把無效資訊轉成空值
df.dropna(inplace=True)
# df.info()   還有16389 比樣本 比原始資料少2% ，故將以此整理後資料進行數據分析

brand_count= df['Brand'].value_counts() #各品牌的銷售數量
total_brand= df['Brand'].nunique() #共有多少品牌
year_count= df['Year'].value_counts() #各年份銷售量

df_year_count = year_count.reset_index()
df_year_count.columns = ['Year','Count']



top_ten = brand_count.head(10).reset_index() #前10大銷售量品牌與銷售數,存成新的dataframe
top_ten.columns= ['Brand','Count'] #轉換成新的dataframe['Brand' & 'Count']

filter_year = df[df['Year'] >2009]#把年份縮短到近20年
fueltype_year = filter_year['FuelType'].value_counts() # 發現一個Fueltype為'-'
df_fueltype_year = filter_year[filter_year['FuelType'] != '-']  # 先將'-'移除


plt.subplot(1,3,1) # 用top_ten作圖

sns.barplot(x='Brand', y='Count', data=top_ten, palette='viridis')
plt.xlabel('Brand')
plt.ylabel('Count')
plt.title('Brand Counts')
plt.xticks(rotation=45, ha='right')  


plt.subplot(1,3,2) #用汽車總銷量作圖

plt.tight_layout()
sns.scatterplot(x='Year', y='Count', data=df_year_count, size='Year', hue='Year', sizes=(10, 50), palette='viridis')
plt.title('Car Sales by Year')
plt.xlabel('Year')
plt.ylabel('Count')
plt.tight_layout()



plt.subplot(1,3,3) #各年的燃油類型銷售

sns.countplot(x='Year', hue='FuelType', data=df_fueltype_year, palette='Set2', width=1)
plt.tight_layout()
plt.title('Fuel Type Distribution Over Years')
plt.xlabel('Year')
plt.ylabel('Count')
plt.xticks(rotation=45, ha='right')
plt.show()

