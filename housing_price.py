# -*- coding: utf-8 -*-
"""
Created on Fri Sep 09 08:02:50 2016

@author: Kiyoko
"""

import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import Imputer

data = pd.read_csv('train.csv', na_values=' ')
pd.set_option('display.max_columns', 50)
print data.shape
print data.dtypes

# Drop features with > 40% of data missing
for column in data.columns:
    if data[column].isnull().sum() > (data.shape[0] * 0.4):
        print column, '\t', data[column].isnull().sum()

drop_features = ['Alley', 'FireplaceQu', 'PoolQC', 'Fence', 'MiscFeature']
data = data.drop(drop_features, axis=1)

# Create frequency table for categorical features
# Drop features with unbalanced data (>75% of data in one category)
object_cols = []
for column in data.columns:
    count_frac = data[column].value_counts(
    ) / data[column].value_counts().sum()
    for cat, frac in count_frac.iteritems():
        if frac > 0.75:
            object_cols.append(column)

print object_cols
"""
['MSZoning', 'Street', 'LandContour', 'Utilities', 'LandSlope', 'Condition1', 
'Condition2', 'BldgType', 'RoofStyle', 'RoofMatl', 'ExterCond', 'BsmtCond', 
'BsmtFinType2', 'BsmtFinSF2', 'Heating', 'CentralAir', 'Electrical', 
'LowQualFinSF', 'BsmtHalfBath', 'KitchenAbvGr', 'Functional', 'GarageQual', 
'GarageCond', 'PavedDrive', 'EnclosedPorch', '3SsnPorch', 'ScreenPorch', 
'PoolArea', 'MiscVal', 'SaleType', 'SaleCondition']
Drop them for now
"""
data = data.drop(['MSZoning', 'Street', 'LandContour', 'Utilities', 'LandSlope',
                  'Condition1', 'Condition2', 'BldgType', 'RoofStyle', 'RoofMatl',
                  'ExterCond', 'BsmtCond', 'BsmtFinType2', 'BsmtFinSF2', 'Heating',
                  'CentralAir', 'Electrical', 'LowQualFinSF', 'BsmtHalfBath',
                  'KitchenAbvGr', 'Functional', 'GarageQual', 'GarageCond',
                  'PavedDrive', 'EnclosedPorch', '3SsnPorch', 'ScreenPorch',
                  'PoolArea', 'MiscVal', 'SaleType', 'SaleCondition'],
                 axis=1)

print data.shape    # (1460, 45)
