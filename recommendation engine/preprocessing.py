# -*- coding: utf-8 -*-
"""
Created on Tue Jul 23 19:12:28 2019

@author: vivek
"""
import pandas as pd
import numpy as np
customers=pd.read_csv('recommend_1.csv')
transactions=pd.read_csv('trx_data.csv')
#preprocessing
transactions['products'] = transactions['products'].apply(lambda x: [int(i) for i in x.split('|')])
transactions.head(2).set_index('customerId')['products'].apply(pd.Series).reset_index()
'''organize a given table into a dataframe with customerId, single productId, and purchase count
pd.melt(transactions.head(2).set_index('customerId')['products'].apply(pd.Series).reset_index(), 
             id_vars=['customerId'],
             value_name='products') \
    .dropna().drop(['variable'], axis=1) \
    .groupby(['customerId', 'products']) \
    .agg({'products': 'count'}) \
    .rename(columns={'products': 'purchase_count'}) \
    .reset_index() \
    .rename(columns={'products': 'productId'})'''
data = pd.melt(transactions.set_index('customerId')['products'].apply(pd.Series).reset_index(), 
             id_vars=['customerId'],
             value_name='products') \
    .dropna().drop(['variable'], axis=1) \
    .groupby(['customerId', 'products']) \
    .agg({'products': 'count'}) \
    .rename(columns={'products': 'purchase_count'}) \
    .reset_index() \
    .rename(columns={'products': 'productId'})
data['productId'] = data['productId'].astype(np.int64)
def create_data_dummy(data):
    data_dummy = data.copy()
    data_dummy['purchase_dummy'] = 1
    return data_dummy
data_dummy = create_data_dummy(data)
# Normalize item values across users
df_matrix = pd.pivot_table(data, values='purchase_count', index='customerId', columns='productId')
df_matrix_norm = ((df_matrix-df_matrix.min())/(df_matrix.max()-df_matrix.min()))
d = df_matrix_norm.reset_index()
d.index.names = ['scaled_purchase_freq']
data_norm = pd.melt(d, id_vars=['customerId'], value_name='scaled_purchase_freq').dropna()

from sklearn.model_selection import train_test_split
train,test=train_test_split(data,test_size=0.2,random_state=0)
















