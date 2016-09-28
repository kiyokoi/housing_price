# -*- coding: utf-8 -*-
"""
Created on Fri Sep 09 08:02:50 2016

@author: Kiyoko
"""


feature_cols = list(train.columns[:-1])
label_col = train.columns[-1]

x = train[feature_cols]
y = train[label_col]

x_all = x.append(test)

pd.set_option('display.max_columns', 50)
print x_all.shape
print x_all.dtypes

# Drop features with > 40% of data missing
for column in data.columns:
    if data[column].isnull().sum() > (data.shape[0] * 0.4):
        print column, '\t', data[column].isnull().sum()

drop_features = ['Alley', 'FireplaceQu', 'PoolQC', 'Fence', 'MiscFeature']
data = data.drop(drop_features, axis=1)

# Define categorical and numerical columns
categorical = []
numerical = []
for column in x_all.columns:
    if x_all[column].dtypes == 'object':
        categorical.append(column)
    else:
        numerical.append(column)

# Take log of data with skew > 0.1
from scipy.stats import skew
for column in numerical:
    if skew(x_all[column]) > 0.1:
        x_all[column] = np.log1p(x_all[column])

y = np.log1p(y)

print x_all.shape    # (2919, 75)

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
