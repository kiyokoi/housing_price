# -*- coding: utf-8 -*-
"""
Created on Fri Sep 09 08:02:50 2016

@author: Kiyoko
"""

import pandas as pd

data = pd.read_csv('train.csv', na_values=' ')
pd.set_option('display.max_columns', 50)
print data.shape
print data.dtypes

# Drop features with > 15% of data missing
for column in data.columns:
    if data[column].isnull().sum() > (data.shape[0] * 0.15):
        print column, '\t', data[column].isnull().sum()

drop_features = ['LotFrontage', 'Alley',
                 'FireplaceQu', 'PoolQC', 'Fence', 'MiscFeature']
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

print data.shape    # (1460, 44)

# Missing value treatment
# Explore missing values
for column in data.columns:
    if data[column].isnull().sum() > 0:
        print column, '\t', data[column].isnull().sum(), '\t', data[column].dtypes

"""
MasVnrType      8       object
MasVnrArea      8       float64
BsmtQual        37      object
BsmtExposure    38      object
BsmtFinType1    37      object
GarageType      81      object
GarageYrBlt     81      float64
GarageFinish    81      object
"""

# Impute missing values with most frequent
impute = ['MasVnrType', 'MasVnrArea', 'BsmtQual', 'BsmtExposure', 'BsmtFinType1',
          'GarageType', 'GarageYrBlt', 'GarageFinish']

for column in impute:
    freq = dict(data[column].value_counts())
    most_freq = freq.keys()[0]
    print column, '\t', most_freq

    data.loc[data[column].isnull(), column] = most_freq

"""
MasVnrType      None
MasVnrArea      0.0
BsmtQual        Fa
BsmtExposure    Gd
BsmtFinType1    LwQ
GarageType      Basment
GarageYrBlt     1900.0
GarageFinish    Fin
"""

# Assign dummies to categorical data
categorical = []
numerical = []
for column in data.columns:
    if data[column].dtypes == 'object':
        categorical.append(column)
    else:
        numerical.append(column)

cat_data = data[categorical]
cat_data = pd.get_dummies(cat_data)
num_data = data[numerical]
data = pd.concat([cat_data, num_data], axis=1)

print len(data.columns)  # 147 features
