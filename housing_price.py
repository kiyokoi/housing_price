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


# Impute missing values with most frequent
for column in x_all.columns:
    if x_all[column].isnull().sum() > 0:
        freq = dict(x_all[column].value_counts())
        most_freq = freq.keys()[0]

        print column, '\t', x_all[column].isnull().sum(), '\t', x_all[column].dtypes, '\t', most_freq

        x_all.loc[x_all[column].isnull(), column] = most_freq

"""
MSZoning        4       object          RL
LotFrontage     486     float64         21.0
Utilities       2       object          AllPub
Exterior1st     1       object          Stone
Exterior2nd     1       object          Stone
MasVnrType      24      object          None
MasVnrArea      23      float64         0.0
BsmtQual        81      object          Fa
BsmtCond        82      object          Fa
BsmtExposure    82      object          Gd
BsmtFinType1    79      object          LwQ
BsmtFinSF1      1       float64         0.0
BsmtFinType2    80      object          LwQ
BsmtFinSF2      1       float64         0.0
BsmtUnfSF       1       float64         0.0
TotalBsmtSF     1       float64         0.0
Electrical      1       object          FuseP
BsmtFullBath    2       float64         0.0
BsmtHalfBath    2       float64         0.0
KitchenQual     1       object          Fa
Functional      2       object          Sev
GarageType      157     object          Basment
GarageYrBlt     159     float64         2207.0
GarageFinish    159     object          Fin
GarageCars      1       float64         0.0
GarageArea      1       float64         0.0
GarageQual      159     object          Fa
GarageCond      159     object          Fa
SaleType        1       object          Oth
"""

# Visualize numerical data
import matplotlib.pyplot as plt

fig = plt.figure(figsize=(12, 48))
for i, column in enumerate(numerical):
    charts = fig.add_subplot(24, 6, i + 1)
    charts.set_xlabel(column)
    charts.set_ylabel('Sale Price')
    charts.set_xticklabels(column, rotation=70)
    charts.hist(x_all[column])
    locs, labels = plt.xticks()
fig.tight_layout()
fig.show()

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
