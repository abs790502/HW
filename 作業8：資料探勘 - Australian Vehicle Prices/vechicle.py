import pandas as pd

df = pd.read_csv('Australian Vehicle Prices.csv')

#print(df.info()) #由info 可看出缺少的項目 Car/Suv,Location,BodyType,Doors,Seats,Price
#先處理Car/Suv,由model 中找出眾數填入

#null_in_car_suv = ['02 **** ****\n','03 **** ****\n','07 **** ****\n','08 **** ****\n']    一開始因為沒有注意到這些字串後面有空格，導致卡關

df.replace(r'\s+', '', regex=True, inplace=True)  # 去除所有空格
null_in_car_suv = ['02********','03********','07********','08********']                                                                                                                                       
df['Car/Suv'] = df['Car/Suv'].replace(null_in_car_suv, '')

