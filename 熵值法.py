import pandas as pd
import numpy as np


def entropy_method(data, features, m, d, ne_features=None, zero_offset=1e-6):
    """
    data：DataFrame类型，数据集（需要包含年份year）
    features：List类型，变量名列表
    ne_features：List类型，负向指标变量名列表
    m：int类型，省份数量
    d: int类型，年份数量
    zero_offset: float类型, 最小值平移数

    return :dict类型，normal_data, weight, score
    """
    # 极差标准化
    normal_data = data.copy()
    for feature in features:
        # 该部分是固定某指标下的最值，用于标准化处理（2021.12.19）
        normal_data_min = min(normal_data.loc[:, feature])
        normal_data_max = max(normal_data.loc[:, feature])
        for year in normal_data['year'].unique():
            if ne_features and feature in ne_features:
                temp = normal_data_max - normal_data.loc[normal_data['year'] == year, feature]
            else:
                temp = normal_data.loc[normal_data['year'] == year, feature] - normal_data_min
            temp = temp / (normal_data_max - normal_data_min)
            normal_data.loc[normal_data['year'] == year, feature] = temp

    # 最小值平移处理
    for feature in features:
        normal_data.loc[normal_data[feature] == 0, feature] = zero_offset

    # 计算指标比重
    pro_data = normal_data.copy()
    for feature in features:
        index = pro_data.loc[:, feature] / sum(pro_data.loc[:, feature])
        pro_data.loc[:, feature] = index

    # 计算信息熵
    entropy = np.arange(len(features)).astype(float)  # 注意初始化需要设定为浮点型
    for ind, feature in enumerate(features):
        entropy[ind] = (- 1 / np.log(m * d)) * sum(pro_data[feature] * np.log(pro_data[feature]))

    # 权重计算
    g = 1 - entropy  # 计算变异系数
    w = g / sum(g)  # 计算权重

    # 综合得分计算
    score = np.dot(normal_data.loc[:, features], w)

    # 汇总信息输出
    res = dict()
    res['normal_data'] = normal_data
    res['weight'] = pd.DataFrame(data=w, index=features, columns=['weight'])
    res['score'] = pd.DataFrame(data=score, columns=['score'])

    return res
