import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.preprocessing import LabelEncoder
lb = LabelEncoder()

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
df['Year'] = df['Year'].fillna(0).astype(int)
df.dropna(inplace=True)

# df.info()   還有16389 比樣本 比原始資料少2% ，故將以此整理後資料進行數據分析

brand_count= df['Brand'].value_counts() #各品牌的銷售數量
total_brand= df['Brand'].nunique() #共有多少品牌
year_count= df['Year'].value_counts() #各年份銷售量

df_year_count = year_count.reset_index()
df_year_count.columns = ['Year','Count']

top_ten = brand_count.head(10).reset_index() #前10大銷售量品牌與銷售數,存成新的dataframe
top_ten.columns= ['Brand','Count'] #轉換成新的dataframe['Brand' & 'Count']

filter_year_20 = df[df['Year'] >2009]#把年份縮短到近20年
fueltype_year_20 = filter_year_20['FuelType'].value_counts() # 發現一個Fueltype為'-'
df_fueltype_year_20 = filter_year_20[filter_year_20['FuelType'] != '-']  # 先將'-'移除

#近10年總銷售額最高的前5大車廠的FuelType分類
df_filter_year_ten = df[df['Year'] >2002] #近10年
df_filter_year_ten['FuelType'] = np.where(df_filter_year_ten['FuelType'].isin(['Hybrid', 'Unleaded','Electric']), df_filter_year_ten['FuelType'], 'Other')#fueltype分類
df_fueltype_filter = df_filter_year_ten.query("FuelType != 'Other'") #other太多了，只看油電，無鉛，純電
top_10_sales = df_filter_year_ten.groupby('Brand')['Price'].sum().nlargest(5).index #看前10大銷售品牌的
df_top_10_year_sales = df_fueltype_filter[df_fueltype_filter['Brand'].isin(top_10_sales)]

#保留近10年的Brand,Year,Car/Suv,Transmission,FuelType,BodyType,Price 做heatmap
df_for_heatmap = df.loc[:, ['Brand', 'Year', 'Car/Suv', 'Transmission', 'FuelType', 'BodyType', 'Price']]


df_for_heatmap['Brand'] = lb.fit_transform(df_for_heatmap['Brand'])   #用labelEncoder 將字串轉換成數字
df_for_heatmap['Car/Suv'] = lb.fit_transform(df_for_heatmap['Car/Suv']) #用labelEncoder 將字串轉換成數字
df_for_heatmap['Transmission'] = lb.fit_transform(df_for_heatmap['Transmission']) #用labelEncoder 將字串轉換成數字
df_for_heatmap['FuelType'] = lb.fit_transform(df_for_heatmap['FuelType']) #用labelEncoder 將字串轉換成數字
df_for_heatmap['BodyType'] = lb.fit_transform(df_for_heatmap['BodyType']) #用labelEncoder 將字串轉換成數字


corr_matrix=df_for_heatmap.corr()  #相關係數
plt.figure(1, figsize=(14,8))
sns.heatmap(corr_matrix,center=0, annot=True)
plt.show()



sns.scatterplot(x='Year', y='Price', hue='FuelType', style='Brand', data=df_top_10_year_sales) #散點圖
plt.title('Relation with FuelType Price & Year')
plt.xlabel('Year')
plt.ylabel('Price')
plt.xticks(np.arange(min(df_top_10_year_sales['Year']), max(df_top_10_year_sales['Year'])+1, 1.0),rotation=45, ha='right')
plt.legend(title='FuelType')
plt.tight_layout()
plt.show()

sns.boxplot(x='Brand', y='Price', hue='FuelType', data=df_top_10_year_sales) #合鬚圖
plt.title('Brand & Fueltype price')
plt.xlabel('Brand')
plt.ylabel('Price')
plt.legend(title='FuelType', loc='upper right')
plt.tight_layout()
plt.show()


sns.barplot(x='Brand', y='Count', data=top_ten, palette='viridis') #長條圖
plt.xlabel('Brand')
plt.ylabel('Count')
plt.title('Brand Counts')
plt.xticks(rotation=45, ha='right')  
plt.tight_layout()
plt.show()


sns.countplot(x='Year', hue='FuelType', data=df_fueltype_year_20, palette='Set2', width=1) #計數長條圖
plt.tight_layout()
plt.title('Fuel Type Distribution Over Years')
plt.xlabel('Year')
plt.ylabel('Count')
plt.xticks(rotation=45, ha='right')
plt.show()




