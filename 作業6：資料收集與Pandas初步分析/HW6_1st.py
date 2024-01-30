import pandas as pd 
import matplotlib.pyplot as plt

df = pd.read_csv('vechicle.csv')

#print(df.loc[[0,20]])  #loc 找出列

df.dropna(inplace= True)


# brand_MG = df[df['Brand'].isin(['MG'])]
# brand_Honda = df[df['Brand'].isin(['Honda'])]
# brand_Toyota = df[df['Brand'].isin(['Toyota'])]
# mg_2023 = brand_MG[brand_MG['Year'].isin([2023])]
# honda_2023 = brand_Honda[brand_Honda['Year'].isin([2023])]
# toyota_2023 = brand_Toyota[brand_Toyota['Year'].isin([2023])]  
#用function 包起來

# def brand_car(df, brand, year):
#     brand_df = df[df['Brand'].isin([brand])]
#     brand_year_df = brand_df[brand_df['Year'].isin([year])]
#     return brand_year_df

# brand_MG_2023 = brand_car(df, 'MG', 2023)
# brand_Honda_2023 = brand_car(df, 'Honda', 2023)
# brand_Toyota_2023 = brand_car(df, 'Toyota', 2023)

filter_df =df[(df['Year']>=2019) & (df['Year']<=2023)]

sales_by_year = filter_df.groupby(['Year', 'Brand']).size().reset_index(name='Sales')
sales_by_sorter =sales_by_year.sort_values(by=['Year','Sales'], ascending=[False, False])
print(sales_by_year)
# #Mazda  ,Toyota, Honda, MG, Volkswagen 每年賣多少
# def brand_car(sales_by_year, brand):
#     brand_cars = sales_by_year[sales_by_year['Brand'].isin([brand])]
#     return brand_cars



# brand_mazda =brand_car(sales_by_year, 'Mazda')
# brand_toyota =brand_car(sales_by_year, 'Toyota')
# brand_honda =brand_car(sales_by_year, 'Honda')
# brand_mg =brand_car(sales_by_year, 'MG')
# brand_volkswagen =brand_car(sales_by_year, 'Volkswagen')
# merge_data = pd.concat([brand_mazda, brand_toyota, brand_honda, brand_mg, brand_volkswagen], ignore_index=True)
# print(merge_data.info())
# merge_data['Year'] = merge_data['Year'].astype(str)
# print(merge_data.info())


# for year, data in merge_data.groupby('Brand'):
#     plt.plot(data['Year'], data['Sales'], label=str(year))

# plt.xlabel('Year')
# plt.ylabel('Sales')
# plt.title('Sales by Brand and Year')
# plt.legend()
# plt.show()

# # sales_by_sorter = sales_by_year.sort_values(by=['Year', 'Sales'], ascending=[False, False]) #依照年份降冪排序






# brand = brand_count['Brand']
# count = brand_count['count']
# plt.pie(count)
# plt.show




# plt.pie(x)
# plt.show()
