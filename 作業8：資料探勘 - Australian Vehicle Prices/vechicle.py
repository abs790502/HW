import pandas as pd

df = pd.read_csv('Australian Vehicle Prices.csv')

#print(df.info()) #由info 可看出缺少的項目 Car/Suv,Location,BodyType,Doors,Seats,Price
#先處理Car/Suv,由model 中找出眾數填入

#null_in_car_suv = ['02 **** ****\n','03 **** ****\n','07 **** ****\n','08 **** ****\n']    一開始因為沒有注意到這些字串後面有空格，導致卡關

df.replace(r'\s+', '', regex=True, inplace=True)  # 去除所有空格
null_in_car_suv = ['02********','03********','07********','08********']                                                                                                                                       
df['Car/Suv'] = df['Car/Suv'].replace(null_in_car_suv, '')

df.to_csv('newdata.csv')
   

# def fillna_mode(series):
#     mode_value = series.mode().iloc[0]  # 众数
#     return series.fillna(mode_value)

# df['Car/Suv'] = df.groupby('Model')['Car/Suv'].transform(fillna_mode)

# import pandas as pd



# df = pd.read_csv('newdata.csv')

# # 将 "item" 列中值为1的项替换为空白

# null_a = (1,2)
# df['item'] = df['item'].replace(null_a, '')

# # 显示结果
# print(df)