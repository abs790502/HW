import pandas as pd 
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
data = pd.read_csv('vechicle.csv')


sns.set_style("whitegrid")
matplotlib.rcParams['font.size'] = 8
matplotlib.rcParams['figure.figsize'] = (12, 4)
matplotlib.rcParams['figure.dpi'] = 100


data.info()
