# -*- coding: utf-8 -*-
"""
Created on Sat Apr 20 14:07:23 2019

@author: Owner
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import seaborn as sns

os.chdir("C:\FADOUA\BA\instacart_2017_05_01")
os.getcwd()

# import data

df_ais=pd.read_csv('aisles.csv')
df_dep=pd.read_csv('departments.csv') 
df_prod_pr=pd.read_csv('order_products__prior.csv')
df_prod_tr=pd.read_csv('order_products__train.csv')
df_ord=pd.read_csv('orders.csv')
df_prod=pd.read_csv('products.csv')

# start analyzing order dataset

n1=df_ais.isnull().sum()
n2=df_dep.isnull().sum()
n3=df_prod_pr.isnull().sum()
n4=df_prod_tr.isnull().sum()
n5=df_ord.isnull().sum()
n6=df_prod.isnull().sum()

#we will drop the null data from  df_ord dataset

#df_ord = df_ord.dropna() # drop any row with null value
#n5=df_ord.isnull().sum()




# -------------------------data visualisation

# ----------Data order

colnam=df_ord.columns.values.tolist() # liste for columns names
df_ord.dtypes



df_ord['eval_set'].nunique() # number of values prior, train and test 
df_ord['eval_set'].value_counts()


prior_ord=df_ord['days_since_prior_order'].value_counts()
nbrdays=df_ord['days_since_prior_order'].unique()
#df_ord['days_since_prior_order'].dtype
#df_ord['days_since_prior_order']= df_ord['days_since_prior_order'].astype('int64') 

ord_numbr=df_ord['order_number'].unique()

#--------When do people order?
# Let’s have a look when frequently people buy groceries online -- witch day

sns.set(style="darkgrid")
sns.countplot(data=df_ord, x = 'order_dow')
plt.xlabel('days of Week')
plt.title('Frenquency of orders by days of Week')
plt.ylabel('Count')

plt.show()

# Let’s have a look when frequently people buy groceries online -- witch hour


sns.set(style="darkgrid")
sns.countplot(data=df_ord, x = 'order_hour_of_day')
plt.xlabel(' hours of days',  fontsize=9)
plt.title('Frenquency of orders by hour of day',  fontsize=10)
plt.ylabel('Count',  fontsize=9)
plt.show()



# --------plot count days since prior order
sns.set(style="darkgrid")
sns.countplot(data=df_ord, x =  'days_since_prior_order')
plt.xlabel('Number of days', fontsize=9)
plt.title('Frequency of days before next purchase', fontsize=12)
plt.xticks(rotation='vertical',size=9)
plt.yticks(size=9)
plt.ylabel('Count', fontsize=9)
plt.show()

# group user by number of order


nbr_ord_by_user=df_ord.groupby("user_id")["order_number"].size().sort_values(ascending=False)
nbr_ord_by_user_sum=nbr_ord_by_user.value_counts()

print(nbr_ord_by_user.max())
# we can see that majority of customers did between 4 and 9 reorder as max
#nbr_ord_by_user_top= nbr_ord_by_user_sum[nbr_ord_by_user_sum>3000]
nbr_ord_by_user_top= nbr_ord_by_user_sum.head(20)


sns.set(style="darkgrid")
sns.countplot(nbr_ord_by_user)
plt.xlabel('number of reorder')
plt.title('Max number of reorder by user')
plt.ylabel('Count')
plt.show()

sns.set(style="darkgrid")
sns.barplot(nbr_ord_by_user_top.index, nbr_ord_by_user_top.values)
plt.xlabel('Number of reorder')
plt.title("Top Max number of reorder by user")
plt.ylabel('Count')
plt.show()

#----- Prior prod, products, aisles, and departements data

# merge tables Prior prod, products, aisles, and departements 
df_order_products_prior = pd.merge(df_prod_pr, df_prod, on='product_id', how='left')
df_order_products_prior = pd.merge(df_order_products_prior, df_ais, on='aisle_id', how='left')
df_order_products_prior = pd.merge(df_order_products_prior, df_dep, on='department_id', how='left')
head_pr=df_order_products_prior.head(5)

# number of product in each order= max value in "add_to_cart_order"
grouped_df = df_order_products_prior.groupby("order_id")["add_to_cart_order"].aggregate("max").reset_index()
count_nbr_item_by_order = grouped_df.add_to_cart_order.value_counts()

plt.figure(figsize=(12,8))
sns.barplot(count_nbr_item_by_order.index, count_nbr_item_by_order.values, alpha=0.8)
plt.ylabel('Number of Occurrences', fontsize=10)
plt.xlabel('Number of products in the each order', fontsize=7)
plt.xticks(rotation='vertical')
plt.show()

# top 50 nbr product by order

count_nbr_item_by_order_top50=count_nbr_item_by_order.head(50)
plt.figure(figsize=(12,8))
sns.barplot(count_nbr_item_by_order_top50.index, count_nbr_item_by_order_top50.values, alpha=0.8)
plt.ylabel('Number of Occurrences', fontsize=10)
plt.xlabel('Number of products in the each order', fontsize=10)
plt.yticks(size=9)
plt.xticks(rotation='vertical', size=9)
plt.show()






# top 20 product ordred
nbr_product_ordred = df_order_products_prior['product_name'].value_counts().sort_values(ascending=False).reset_index()
nbr_product_ordred.columns = ['product_name', 'frequency_count']


sns.set(style="darkgrid")
plt.figure(figsize=(6,4))
sns.barplot(nbr_product_ordred.frequency_count, nbr_product_ordred.product_name, color="darkmagenta")
plt.ylabel('product_ordred', fontsize=9)
plt.xlabel('Count', fontsize=9)
plt.xticks( fontsize='7')
plt.yticks( fontsize='7')
plt.title('the 20 most ordered products', fontsize=12)

plt.show()



# what is the ratio of reordred product vs ordred .

# percentage of re-orders in prior set #
df_order_products_prior.reordered.sum() / df_order_products_prior.shape[0]
#df_order_products_prior.reordered.sum() / len(df_order_products_prior)
# --> 59% product are reordred

# Top 20 product reordred

reordred_prod2 = df_order_products_prior[df_order_products_prior.reordered==1]
#.groupby("product_id")
R2=reordred_prod2.head(5)

nbr_product_reordred = reordred_prod2['product_name'].value_counts().sort_values(ascending=False).reset_index().head(20)
nbr_product_reordred.columns = ['product_name', 'frequency_count']



sns.set(style="darkgrid")
sns.barplot(nbr_product_reordred.frequency_count, nbr_product_reordred.product_name, color="magenta")
plt.ylabel('product_reordered', fontsize=9)
plt.xlabel('Count', fontsize=9)
plt.xticks( fontsize='7')
plt.yticks( fontsize='7')
plt.title("The 20 most reordered products",fontsize='12' )
plt.show()


# Department Distribution:

plt.figure(figsize=(8,8))
# display the top 10 ordred product's departement 
aisles_val = df_order_products_prior['department'].value_counts().head(10)
labels = (np.array(aisles_val.index))


partition = (np.array((aisles_val / aisles_val.sum())*100))
plt.pie(partition, labels=labels, autopct='%1.1f%%', startangle=200 )
plt.title("Top 10 departments distribution", fontsize=12)
plt.show()


# Organic VS No organic

organic= df_order_products_prior['product_name'].str.contains('Organic').sum()
No_organic= len(df_order_products_prior)-organic


labels = ['Organic', 'No organic']
size = [organic,No_organic]
explode = [0, 0.1]

plt.rcParams['figure.figsize'] = (5, 5)
plt.pie(size, explode = explode, labels = labels, shadow = True, autopct = '%.2f%%')
plt.title('A pie chart Organic vs No organic')
plt.axis('off')
plt.legend()
plt.show()



