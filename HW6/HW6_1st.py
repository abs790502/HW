import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns
df = pd.read_csv('vechicle.csv')


df['Price'] = pd.to_numeric(df['Price'], errors= 'coerce') #to_numeric 把price 欄位轉成數字，errors= 'coerce' 表示無法轉成數字顯示NaN
# filter_df['Price'] = filter_df['Price'].astype(int)     <----#轉換數字會直接失敗，因為Price欄位有POA字串，新增第7行把price 進行清洗        
df.dropna(inplace= True) #清洗



#篩5年資料
filter_df =df[(df['Year']>=2019) & (df['Year']<=2023)]    
sales_by_year = filter_df.groupby(['Year', 'Brand','Title', 'Price']).size().reset_index(name='Sales') #重新做一個表格，新增sales欄位

#看mazda, toyota, honda, mg, volkswagen()
def brand_car(sales_by_year, brand):
    brand_cars = sales_by_year[sales_by_year['Brand'].isin([brand])]
    return brand_cars

brand_mazda =brand_car(sales_by_year, 'Mazda')
brand_toyota =brand_car(sales_by_year, 'Toyota')
brand_honda =brand_car(sales_by_year, 'Honda')
brand_mg =brand_car(sales_by_year, 'MG')
brand_volkswagen =brand_car(sales_by_year, 'Volkswagen')
merge_data = pd.concat([brand_mazda, brand_toyota, brand_honda, brand_mg, brand_volkswagen], ignore_index=True)


# 作圖一 五年平均  (done)

mazda_five_year_avg = brand_mazda['Price'].mean()
toyota_five_year_avg = brand_toyota['Price'].mean()
honda_five_year_avg = brand_honda['Price'].mean()
mg_five_year_avg = brand_mg['Price'].mean()
volkswagen_five_year_avg = brand_volkswagen['Price'].mean()

#5家廠商5年平均銷售額
avg_df = pd.DataFrame()
avg_df['Brand'] = ['Mazda', 'Toyota', 'Honda', 'MG', 'Volkswagen']
avg_df['avg_price'] =[
                    mazda_five_year_avg ,
                    toyota_five_year_avg,
                    honda_five_year_avg,
                    mg_five_year_avg ,
                    volkswagen_five_year_avg
]

plt.subplot(1, 2, 1)
x = avg_df['Brand']
y = avg_df['avg_price']
plt.title("5 years sales by Brand")
plt.xlabel("Brand")
plt.ylabel("Price ($)")
plt.bar(x, y, color ='Green', width=0.3)



# 作圖二目標 : 把數據，5年5家廠商分開呈現，並畫圖


def brand_year(sales_by_year, brand, year):
    brand_cars = sales_by_year[sales_by_year['Brand'].isin([brand])]
    brand_years = brand_cars[brand_cars['Year'].isin([year])]

    total_year = sales_by_year[sales_by_year['Year'].isin([year])]
    brand_year_df = total_year.loc[total_year['Brand'] == brand, 'Price'].sum()
    return brand_years, brand_year_df

brand_mazda , mazda_2019= brand_year(sales_by_year, 'Mazda', 2019)
brand_toyota, toyota_2019= brand_year(sales_by_year, 'Toyota', 2019)
brand_honda, honda_2019= brand_year(sales_by_year, 'Honda',2019)
brand_mg, mg_2019=brand_year(sales_by_year, 'MG',2019)
brand_volkswagen, volkswagen_2019= brand_year(sales_by_year, 'Volkswagen',2019)

brand_mazda , mazda_2020= brand_year(sales_by_year, 'Mazda', 2020)
brand_toyota, toyota_2020= brand_year(sales_by_year, 'Toyota', 2020)
brand_honda, honda_2020= brand_year(sales_by_year, 'Honda',2020)
brand_mg, mg_2020=brand_year(sales_by_year, 'MG',2020)
brand_volkswagen, volkswagen_2020= brand_year(sales_by_year, 'Volkswagen',2020)

brand_mazda , mazda_2021= brand_year(sales_by_year, 'Mazda', 2021)
brand_toyota, toyota_2021= brand_year(sales_by_year, 'Toyota', 2021)
brand_honda, honda_2021= brand_year(sales_by_year, 'Honda',2021)
brand_mg, mg_2021=brand_year(sales_by_year, 'MG',2021)
brand_volkswagen, volkswagen_2021= brand_year(sales_by_year, 'Volkswagen',2021)

brand_mazda , mazda_2022= brand_year(sales_by_year, 'Mazda', 2022)
brand_toyota, toyota_2022= brand_year(sales_by_year, 'Toyota', 2022)
brand_honda, honda_2022= brand_year(sales_by_year, 'Honda',2022)
brand_mg, mg_2022=brand_year(sales_by_year, 'MG',2022)
brand_volkswagen, volkswagen_2022= brand_year(sales_by_year, 'Volkswagen',2022)

brand_mazda , mazda_2023= brand_year(sales_by_year, 'Mazda', 2023)
brand_toyota, toyota_2023= brand_year(sales_by_year, 'Toyota', 2023)
brand_honda, honda_2023= brand_year(sales_by_year, 'Honda',2023)
brand_mg, mg_2023=brand_year(sales_by_year, 'MG',2023)
brand_volkswagen, volkswagen_2019= brand_year(sales_by_year, 'Volkswagen',2023)


df_2019 = pd.DataFrame()
df_2019['Brand'] = ['Mazda', 'Toyota', 'Honda', 'MG', 'Volkswagen']
df_2019['Price'] = [mazda_2019,
                         toyota_2019,
                         honda_2019,
                         mg_2019,
                         volkswagen_2019]
df_2019['Year'] = ['2019','2019','2019','2019','2019']


df_2020 = pd.DataFrame()
df_2020['Brand'] = ['Mazda', 'Toyota', 'Honda', 'MG', 'Volkswagen']
df_2020['Price'] = [mazda_2020,
                         toyota_2020,
                         honda_2020,
                         mg_2020,
                         volkswagen_2020]
df_2020['Year'] = ['2020','2020','2020','2020','2020']

df_2021 = pd.DataFrame()
df_2021['Brand'] = ['Mazda', 'Toyota', 'Honda', 'MG', 'Volkswagen']
df_2021['Price'] = [mazda_2021,
                         toyota_2021,
                         honda_2021,
                         mg_2021,
                         volkswagen_2021]
df_2021['Year'] = ['2021','2021','2021','2021','2021']

df_2022 = pd.DataFrame()
df_2022['Brand'] = ['Mazda', 'Toyota', 'Honda', 'MG', 'Volkswagen']
df_2022['Price'] = [mazda_2022,
                         toyota_2022,
                         honda_2022,
                         mg_2022,
                         volkswagen_2022]
df_2022['Year'] = ['2022','2022','2022','2022','2022']

df_2023 = pd.DataFrame()
df_2023['Brand'] = ['Mazda', 'Toyota', 'Honda', 'MG', 'Volkswagen']
df_2023['Price'] = [mazda_2023,
                         toyota_2023,
                         honda_2023,
                         mg_2023,
                         volkswagen_2020]
df_2023['Year'] = ['2023','2023','2023','2023','2023']

merge_year =pd.concat([df_2019, df_2020, df_2021, df_2022, df_2023], ignore_index=True)
merge_year['Price'] = merge_year['Price']/1000000

plt.subplot(1, 2, 2)  
x= merge_data['Year']
y= merge_data['Price']
sns.lineplot(x='Year', y='Price', hue='Brand', data=merge_year)
plt.title('Car Prices Over Years')
plt.xlabel('Year')
plt.ylabel('Price(million))')

plt.show()



