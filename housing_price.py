# -*- coding: utf-8 -*-
"""
Created on Fri Sep 09 08:02:50 2016

@author: Kiyoko
"""

import pandas as pd
from sklearn.preprocessing import LabelEncoder

data = pd.read_csv('train.csv', na_values = ' ')
pd.set_option('display.max_columns', 50)
print data.shape
print data.dtypes

# Drop features with > 40% of data missing
for column in data.columns:
    if data[column].isnull().sum() > (data.shape[0] * 0.4):
        print column, '\t', data[column].isnull().sum()

drop_features = ['Alley', 'FireplaceQu', 'PoolQC', 'Fence', 'MiscFeature']
data = data.drop(drop_features, axis=1)

# Correct object datatype features
data_temp = data.dropna(how='any')
data_temp.shape

object_cols = []
for column in data.columns:
    if data[column].dtypes == 'object':
        object_cols.append(column)

lbl = LabelEncoder()
for column in object_cols:
    lbl.fit(list(data_temp[column].values))
    data_temp[column] = lbl.transform(data_temp[column].values)

print data_temp[object_cols].describe()
"""
These features have unbalanced data:
'MSZoning', 'Street', 'LandContour', 'LotConfig', 'LandSlope', 'Condition1', 
'BldgType', 'RoofMatl', 'ExterCond', 'BsmtCond', 'Heating', 'BsmtFinType1', 
'CentralAir', 'Electrical', 'Functional', 'GarageQual', 'GarageCond', 'PavedDrive', 
'SaleType', 'SaleCondition'
Drop them for now
"""
data = data.drop(['MSZoning', 'Street', 'LandContour', 'LotConfig', 'LandSlope',\
           'Condition1', 'BldgType', 'RoofMatl', 'ExterCond', 'BsmtCond',\
           'Heating', 'BsmtFinType1', 'CentralAir', 'Electrical', 'Functional',\
           'GarageQual', 'GarageCond', 'PavedDrive', 'SaleType', 'SaleCondition'],\
           axis=1)
