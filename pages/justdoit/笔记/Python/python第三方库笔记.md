> NumPy（Numerical Python） 通常与 SciPy（Scientific Python）和 Matplotlib（绘图库）一起使用， 这种组合广泛用于替代 MatLab，是一个强大的科学计算环境，有助于我们通过 Python 学习数据科学或者机器学习

# NumPy

## Ndarray

### 创建

#### 语法

```
numpy.array(object, dtype = None, copy = True, order = None, subok = False, ndmin = 0)

object	数组或嵌套的数列
dtype	数组元素的数据类型，可选
copy	对象是否需要复制，可选
order	创建数组的样式，C为行方向，F为列方向，A为任意方向（默认）
subok	默认返回一个与基类类型一致的数组
ndmin	指定生成数组的最小维度

# numpy.asarray 类似 numpy.array，但 numpy.asarray 参数只有三个，比 numpy.array 少两个
numpy.asarray(a, dtype = None, order = None)
```

- numpy.empty 创建一个指定形状（shape）、数据类型（dtype）且未初始化的数组
- numpy.zeros 创建指定大小的数组，数组元素以 0 来填充
- numpy.ones 创建指定形状的数组，数组元素以 1 来填充
- numpy.frombuffer 接受 buffer 输入参数，以流的形式读入转化成 ndarray 对象
- numpy.fromiter 方法从可迭代对象中建立 ndarray 对象，返回一维数组
- numpy 包中的使用 arange 函数创建数值范围并返回 ndarray 对象
- numpy.linspace 函数用于创建一个一维数组，数组是一个等差数列构成的
- numpy.logspace 函数用于创建一个于等比数列
- full 填充

#### 注意

- 矩阵都是二维的
- []一维，[[]]二维，n维向量有n对[]

### 属性

| ndarray.ndim     | 秩，即轴的数量或维度的数量                                   |
| ---------------- | ------------------------------------------------------------ |
| ndarray.shape    | 数组的维度，对于矩阵，n 行 m 列                              |
| ndarray.size     | 数组元素的总个数，相当于 .shape 中 n*m 的值                  |
| ndarray.dtype    | ndarray 对象的元素类型                                       |
| ndarray.itemsize | ndarray 对象中每个元素的大小，以字节为单位                   |
| ndarray.flags    | ndarray 对象的内存信息                                       |
| ndarray.real     | ndarray元素的实部                                            |
| ndarray.imag     | ndarray 元素的虚部                                           |
| ndarray.data     | 包含实际数组元素的缓冲区，由于一般通过数组的索引获取元素，所以通常不需要使用这个属性。 |

### 访问与切片

> Ndarray的访问与切片机制与python的列表机制一致，此外，其还可以由整数数组索引、布尔索引及花式索引

#### 整数数组索引

- a[[0,2],[4,5]] 访问(0,4)、(2,5)元素

#### 布尔索引

- a[bool_expression]

#### 花式索引

- 花式索引根据索引数组的值作为目标数组的某个轴的下标来取值。对于使用一维整型数组作为索引，如果目标是一维数组，那么索引的结果就是对应位置的元素；如果目标是二维数组，那么就是对应下标的行。

  花式索引跟切片不一样，它总是将数据复制到新数组中

### 广播

> 广播(Broadcast)是 numpy 对不同形状(shape)的数组进行数值计算的方式， 对数组的算术运算通常在相应的元素上进行



# SciPy

# Matplotlib