import pandas as pd 
import matplotlib.pyplot as plt

df = pd.read_csv('vechicle.csv')

df.dropna(inplace= True)



filter_df =df[(df['Year']>=2019) & (df['Year']<=2023)]

sales_by_year = filter_df.groupby(['Year', 'Brand']).size().reset_index(name='Sales')
sales_by_sorter =sales_by_year.sort_values(by=['Year','Sales'], ascending=[False, False])

def brand_car(sales_by_year, brand):
    brand_cars = sales_by_year[sales_by_year['Brand'].isin([brand])]
    return brand_cars



brand_mazda =brand_car(sales_by_year, 'Mazda')
brand_toyota =brand_car(sales_by_year, 'Toyota')
brand_honda =brand_car(sales_by_year, 'Honda')
brand_mg =brand_car(sales_by_year, 'MG')
brand_volkswagen =brand_car(sales_by_year, 'Volkswagen')
merge_data = pd.concat([brand_mazda, brand_toyota, brand_honda, brand_mg, brand_volkswagen], ignore_index=True)
print(merge_data.info())
merge_data['Year'] = merge_data['Year'].astype(str)
print(merge_data.info())


for year, data in merge_data.groupby('Brand'):
    plt.plot(data['Year'], data['Sales'], label=str(year))

plt.xlabel('Year')
plt.ylabel('Sales')
plt.title('Sales by Brand and Year')
plt.legend()
plt.show()

