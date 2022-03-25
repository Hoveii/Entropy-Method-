# Entropy Method with Panel data
# 面板数据熵值法

## 一、原始数据设定

- 假设数据为`d`个年度`m`个省份的`n`个指标
- 显然数据是`(d, m, n)`三维数组，但`.csv`存储数据一般是二维表，因此实际取得的数据是`(d*m, n)`的二维数组
- $X_{\theta i j}$ 表示第 $\theta$ 年省份 $i$ 的第 $j$ 个指标值。

## 二、数据标准化

- 这里采用的是极差标准化

- 正向指标和负向指标采用的方法有所不同：
  $$
  X'_{\theta i j} = 
  \left\{\begin{matrix}
  \frac{X_{\theta i j} - \min(X_{\theta i j})}
  {\max(X_{\theta i j}) - \min(X_{\theta i j})} &  第j个指标为正向指标 \\
  \frac{\max(X_{\theta i j}) - X_{\theta i j}}
  {\max(X_{\theta i j}) - \min(X_{\theta i j})}   & 第j个指标为负向指标
  \end{matrix}\right.
  $$
  
- 注意：极差标准化后会生成0的数据，需要对此作数据平移。

- 这里计算得到的$X' = [X_{\theta i j}]_{(d \times m) \times n}$ 是一个二维数组。

## 三、几率（比重）计算

- 这里计算的是第 $\theta$ 年省份 $i$ 的第 $j$ 个指标值在第 $j$ 个指标下的占比。
  $$
  P_{\theta i j} = 
  \frac{X'_{\theta i j}}
  {\sum\limits_{\theta=1}^{d}\sum\limits_{i=1}^{m}X'_{\theta i j}}
  $$

- 这里计算得到的$P = [P_{\theta i j}]_{(d \times m) \times n}$ 是一个二维数组。

## 四、信息熵计算

- 计算第 $j$ 个指标对应的信息熵
  $$
  E_j = - \frac{1}{\ln(dm)}
  \sum\limits_{\theta = 1}^{d}\sum\limits_{i = 1}^{m}
  [P_{\theta i j}\cdot \ln(P_{\theta i j})]
  $$

- 这里计算得到的$E = [E_j]_{n \times 1}$  是一个二维数组。

## 五、权重计算

- 计算第 $j$ 项指标的差异系数
  $$
  G_j = 1 - E_j
  $$

- 计算第 $j$ 项指标的权重
  $$
  W_j = \frac{G_j}{\sum\limits_{j=1}^{n}G_j}
  $$

- 这里计算得到的$W = [W_j]_{n \times 1}$  是一个二维数组。

## 六、综合得分计算

- 计算第 $\theta$ 年第 $i$ 个省的综合得分
  $$
  \begin{aligned}
  Z_{\theta i} 
  &= \sum\limits_{j = 1}^{n} (W_j \cdot X'_{\theta i j}) \\
  Z &=  X' \cdot W
  \end{aligned}
  $$

- 这里最终计算得到的$Z = [Z_{\theta i}]_{(d \times m) \times 1}$ 是同样是一个二维数组。
