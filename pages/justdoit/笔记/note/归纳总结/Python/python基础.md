# 基本语法

## 注释

- 单行注释

  ```python
  # 注释注释
  ```

  ​

- 多行注释

  ```python
  '''
  注释
  '''

  """
  注释
  """
  ```

# 数据类型

## 标准数据类型

- Python 中的变量不需要声明。每个变量在使用前都必须赋值，变量赋值以后该变量才会被创建。
- 在 Python 中，变量就是变量，它没有类型，我们所说的"类型"是变量所指的内存中对象的类型。
- Python3 中有六个标准的数据类型：
  - Number（数字）
  - String（字符串）
  - List（列表）
  - Tuple（元组）
  - Set（集合）
  - Dictionary（字典）
- Python3 的六个标准数据类型中：
  - **不可变数据（3 个）：**Number（数字）、String（字符串）、Tuple（元组）
  - **可变数据（3 个）：**List（列表）、Dictionary（字典）、Set（集合）
- 使用del语句删除单个或多个对象，del var1[,var2[,var3[....,varN]]]
- 内置的 type(a) 函数可以用来查询变量所指的对象类型，也可以用 isinstance (a, int)来判断。isinstance 和 type 的区别在于：type()不会认为子类是一种父类类型，isinstance()会认为子类是一种父类类型。

## Number（数字）

> Python3 支持 int、float、bool、complex（复数）

- 在 Python2 中是没有布尔型的，它用数字 0 表示 False，用 1 表示 True。到 Python3 中，把 True 和 False 定义成关键字了，但它们的值还是 1 和 0，它们可以和数字相加。
- 在混合计算时，Python会把整型转换成为浮点数
- 数字常量：pi、e

## String（字符串）

- Python中的字符串用单引号 ' 或双引号 " 括起来，同时使用反斜杠 \ 转义特殊字符，如果你不想让反斜杠发生转义，可以在字符串前面添加一个 r，表示原始字符串

- 字符串的截取的语法格式如下：

  ```
  变量[头下标:尾下标]
  ```

  索引值以 0 为开始值，-1 为从末尾的开始位置

- 加号 + 是字符串的连接符， 星号 * 表示复制当前字符串，紧跟的数字为复制的次数

- Python 没有单独的字符类型，一个字符就是长度为1的字符串

- 与 C 字符串不同的是，Python 字符串不能被改变。向一个索引位置赋值，比如word[0] = 'm'会导致错误

## List（列表）

- 列表是写在方括号 [] 之间、用逗号分隔开的元素列表

- 和字符串一样，列表同样可以被索引和截取，列表被截取后返回一个包含所需元素的新列表。

  列表截取的语法格式如下：

  ```
  变量[头下标:尾下标]
  ```

  索引值以 0 为开始值，-1 为从末尾的开始位置，截取时“包头不包尾”。Python 列表截取可以接收第三个参数，参数作用是截取的步长。如果第三个参数为负数表示逆向读取。

- 列表可以完成大多数集合类的数据结构实现。列表中元素的类型可以不相同，它支持数字，字符串甚至可以包含列表（所谓嵌套）

- 加号 + 是列表连接运算符，星号 * 是重复操作

- print(r'\n')或者print(R'\n')，表示不转义

- 通过%格式化字符串

## Tuple（元组）

- 元组（tuple）与列表类似，不同之处在于元组的元素不能修改。元组写在小括号 () 里，元素之间用逗号隔开

- 虽然tuple的元素不可改变，但它可以包含可变的对象，比如list列表

- 元组中只包含一个元素时，需要在元素后面添加逗号，否则括号会被当作运算符使用：

  ```python
  >>>tup1 = (50)
  >>> type(tup1)     # 不加逗号，类型为整型
  <class 'int'>
   
  >>> tup1 = (50,)
  >>> type(tup1)     # 加上逗号，类型为元组
  <class 'tuple'>
  ```

## Set（集合）

> 集合（set）是由一个或数个形态各异的大小整体组成的，构成集合的事物或对象称作元素或是成员，基本功能是进行成员关系测试和删除重复元素

- 可以使用大括号 { } 或者 set() 函数创建集合，注意：创建一个空集合必须用 set() 而不是 { }，因为 { } 是用来创建一个空字典

  ```
  parame = {value01,value02,...}
  或者
  set(value)
  ```

- add()、remove() 不存在会报错、discard不存在不会报错、pop()随机删除

## Dictionary（字典）

- 列表是有序的对象集合，字典是无序的对象集合。两者之间的区别在于：字典当中的元素是通过键来存取的，而不是通过偏移存取

- 字典是一种映射类型，字典用 { } 标识，它是一个无序的 **键(key) : 值(value)** 的集合

- 键(key)必须使用不可变类型，所以可以用数字，字符串或元组充当，而用列表就不行

- 在同一个字典中，键(key)必须是唯一的

- 初始化

  ```
  d = {key1 : value1, key2 : value2 }
  ```

- 访问 dict[key]

## 类型转换

> 数据类型的转换，只需要将数据类型作为函数名即可

- int(x[,base])、float(x)、complex(real[,image])、str()、list()、tuple()、set()、dict()
- chr()整数转换为字符，ord()字符转换为它的整数值
- hex()十六进制，otc()八进制
- eval(str)，用来计算在字符串中的有效Python表达式,并返回一个对象，repr()将对象 x 转换为表达式字符串
- frozenset(s)转换为不可变集合

## 空容器的创建

- List    []
- Tuple    ()
- Set    set()
- Dictionary  {}

# 运算符

## 算数运算符

- +、-、*、/
- %     取模
- **    幂 - 返回x的y次幂
- //     取整除 - 向下取接近除数的整数

## 比较运算符

- ==、!=、<、>、<=、>=

## 赋值运算符

- =、+=、-=、*=、/=、%=、**=、//=

## 逻辑运算符

- and
- or
- not

## 位运算符

- &
- | 按位或
- ~ 按位取反
- <<
- \>\>

## 成员运算符

- in
- not in

## 身份运算符

- is，判断两个标识符饮用自同一个对象，等同于 id(x) == id(y)
- not is，等同于id(x) != id(y)
- id()表示获取对象的内存地址

# 流程控制

## 条件控制

### if语句

```python
if condition_1:
    statement_block_1
elif condition_2:
    statement_block_2
else:
    statement_block_3
```

- 在Python中没有switch – case语句

## 循环控制

### while循环

```python
while 判断条件：
    语句
```

### while-else 语句

```python
count = 0
while count < 5:
   print (count, " 小于 5")
   count = count + 1
else:
   print (count, " 大于或等于 5")
```

### for语句

```python
for <variable> in <sequence>:
    <statements>
else:
    <statements>
```

## break与continue

## pass

- 一般用于占位符，不做任何处理

# 迭代器与生成器

## 迭代器

- iter()创建迭代器，next(it)输出下一个元素

  ```python
  list=[1,2,3,4]
  it = iter(list)    # 创建迭代器对象
  print (next(it))   # 输出迭代器的下一个元素
  ```

- StopIteration 异常用于标识迭代的完成，防止出现无限循环的情况

## 生成器

> 跟普通函数不同的是，生成器是一个返回迭代器的函数，只能用于迭代操作，更简单点理解生成器就是一个迭代器

# 函数

## 函数定义

- 函数代码块以 **def** 关键词开头，后接函数标识符名称和圆括号 **()**
- 任何传入参数和自变量必须放在圆括号中间，圆括号之间可以用于定义参数
- 函数的第一行语句可以选择性地使用文档字符串—用于存放函数说明
- 函数内容以冒号起始，并且缩进
- **return [表达式]** 结束函数，选择性地返回一个值给调用方。不带表达式的return相当于返回 None

```python
def 函数名（参数列表）:
    函数体
```

## 函数调用

## 参数传递

- **不可变类型：**类似 c++ 的值传递，如 整数、字符串、元组。如fun（a），传递的只是a的值，没有影响a对象本身。比如在 fun（a）内部修改 a 的值，只是修改另一个复制的对象，不会影响 a 本身
- **可变类型：**类似 c++ 的引用传递，如 列表，字典。如 fun（la），则是将 la 真正的传过去，修改后fun外部的la也会受影响
- python 中一切都是对象，严格意义我们不能说值传递还是引用传递，我们应该说传不可变对象和传可变对象

### 必需参数

- 必需参数须以正确的顺序传入函数。调用时的数量必须和声明时的一样

### 关键字参数

- 关键字参数和函数调用关系紧密，函数调用使用关键字参数来确定传入的参数值

### 默认参数

- 调用函数时，如果没有传递参数，则会使用默认参数

  ```python
  def 函数名（参数1 = 默认值）:
      函数体
  ```

### 不定长参数

- 加了星号 * 的参数会以元组(tuple)的形式导入，存放所有未命名的变量参数

```python
def functionname([formal_args,] *var_args_tuple ):
   "函数_文档字符串"
   function_suite
   return [expression]
```

- 加了两个星号 ** 的参数会以字典的形式导入

  ```python
  def functionname([formal_args,] **var_args_dict ):
     "函数_文档字符串"
     function_suite
     return [expression]
  ```

## 匿名函数

- python 使用 lambda 来创建匿名函数。所谓匿名，意即不再使用 def 语句这样标准的形式定义一个函数。

- lambda 只是一个表达式，函数体比 def 简单很多。

- lambda的主体是一个表达式，而不是一个代码块。仅仅能在lambda表达式中封装有限的逻辑进去。

- lambda 函数拥有自己的命名空间，且不能访问自己参数列表之外或全局命名空间里的参数。

- 虽然lambda函数看起来只能写一行，却不等同于C或C++的内联函数，后者的目的是调用小函数时不占用栈内存从而增加运行效率。

  ```python
  lambda [arg1 [,arg2,.....argn]]:expression
  ```

  ```python
  # 可写函数说明
  sum = lambda arg1, arg2: arg1 + arg2
   
  # 调用sum函数
  print ("相加后的值为 : ", sum( 10, 20 ))
  print ("相加后的值为 : ", sum( 20, 20 ))
  ```

## 变量作用域

- 变量的作用域决定了在哪一部分程序可以访问哪个特定的变量名称。Python的作用域一共有4种，分别是：
  - L （Local） 局部作用域
  - E （Enclosing） 闭包函数外的函数中
  - G （Global） 全局作用域
  - B （Built-in） 内置作用域（内置函数所在模块的范围）
- 以 L –> E –> G –>B 的规则查找，即：在局部找不到，便会去局部外的局部找（例如闭包），再找不到就会去全局找，再者去内置中找
- **Python 中只有模块（module），类（class）以及函数（def、lambda）才会引入新的作用域，其它的代码块（如 if/elif/else/、try/except、for/while等）是不会引入新的作用域的，也就是说这些语句内定义的变量，外部也可以访问**！！！
- 当内部作用域想修改外部作用域的变量时，就要用到global（修改全局作用域）和nonlocal（enclosing 作用域，外层非全局作用域）关键字

# 模块

## import语句

使用 Python 源文件，只需在另一个源文件里执行 import 语句

```python
import module1[, module2[,... moduleN]
```

## from … import 语句

Python 的 from 语句让你从模块中导入一个指定的部分到当前命名空间中，语法如下：

```python
from modname import name1[, name2[, ... nameN]]
```

## from … import * 语句

把一个模块的所有内容全都导入到当前的命名空间也是可行的，只需使用如下声明：

```
from modname import *
```

## \__name\__属性

- 一个模块被另一个程序第一次引入时，其主程序将运行。如果我们想在模块被引入时，模块中的某一程序块不执行，我们可以用__name__属性来使该程序块仅在该模块自身运行时执行。 每个模块都有一个__name__属性，当其值是'__main__'时，表明该模块自身在运行，否则是被引入。

  ```python
  #!/usr/bin/python3
  # Filename: using_name.py

  if __name__ == '__main__':
     print('程序自身在运行')
  else:
     print('我来自另一模块')
  ```

## dir()函数

> 内置的函数 dir() 可以找到模块内定义的所有名称，以一个字符串列表的形式返回

# 输入输出

# 文件

## open()

```python
open(file, mode='r', buffering=-1, encoding=None, errors=None, newline=None, closefd=True, opener=None)
```

- file: 必需，文件路径（相对或者绝对路径）。
- mode: 可选，文件打开模式
- buffering: 设置缓冲
- encoding: 一般使用utf8
- errors: 报错级别
- newline: 区分换行符
- closefd: 传入的file参数类型
- opener:

## file对象

- read(size)
- readline(size)
- readlines(size)
- tell()    返回文件当前位置
- seek(offset,from_where)    设置文件位置
- write(str)
- writelines(sequence)    向文件写入一个序列字符串列表，如果需要换行则要自己加入每行的换行符
- flush()
- close()

# OS

> **os** 模块提供了非常丰富的方法用来处理文件和目录，可以实现shell类型的功能

- [菜鸟教程](https://www.runoob.com/python3/python3-os-file-methods.html)

# 异常

## 异常

> 即便Python程序的语法是正确的，在运行它的时候，也有可能发生错误。运行期检测到的错误被称为异常

## 异常处理

```python
try:
	 x=int(input("Please enter a number: "))
     break
except ValueError:
     print("Oops!  That was no valid number.  Try again   ")
```

```python
# 一个except子句可以同时处理多个异常，这些异常将被放在一个括号里成为一个元组
except (RuntimeError, TypeError, NameError):
        pass
```

- 最后一个except子句可以忽略异常的名称，它将被当作通配符使用

- try except 语句还有一个可选的else子句，如果使用这个子句，那么必须放在所有的except子句之后。这个子句将在try子句没有发生任何异常的时候执行

- try 语句还有另外一个可选的finally子句，它定义了无论在任何情况下都会执行的清理行为

  ​

## 抛出异常

- Python 使用 raise 语句抛出一个指定的异常

  ```python
  raise NameError('HiThere')
  ```

## 自定义异常

# 面向对象

## 面向对象技术简介

- **类(Class):** 用来描述具有相同的属性和方法的对象的集合。它定义了该集合中每个对象所共有的属性和方法。对象是类的实例。
- **方法：**类中定义的函数。
- **类变量：**类变量在整个实例化的对象中是公用的。类变量定义在类中且在函数体之外。类变量通常不作为实例变量使用。
- **数据成员：**类变量或者实例变量用于处理类及其实例对象的相关的数据。
- **方法重写：**如果从父类继承的方法不能满足子类的需求，可以对其进行改写，这个过程叫方法的覆盖（override），也称为方法的重写。
- **局部变量：**定义在方法中的变量，只作用于当前实例的类。
- **实例变量：**在类的声明中，属性是用变量来表示的。这种变量就称为实例变量，是在类声明的内部但是在类的其他成员方法之外声明的。
- **继承：**即一个派生类（derived class）继承基类（base class）的字段和方法。继承也允许把一个派生类的对象作为一个基类对象对待。例如，有这样一个设计：一个Dog类型的对象派生自Animal类，这是模拟"是一个（is-a）"关系（例图，Dog是一个Animal）。
- **实例化：**创建一个类的实例，类的具体对象。
- **对象：**通过类定义的数据结构实例。对象包括两个数据成员（类变量和实例变量）和方法。

## 类定义

- 类的定义

  ```python
  class ClassName:
      <statement-1>
      .
      .
      .
      <statement-N>
  ```

- 类有一个名为 __init__() 的特殊方法（**构造方法**），该方法在类实例化时会自动调用，像下面这样：

  ```python
  def __init__(self):
      self.data = []
  ```

- 类的方法与普通的函数只有一个特别的区别——它们必须有一个额外的**第一个参数名称**, 按照惯例它的名称是 self。self 代表的是类的实例，代表当前对象的地址，而 self.class 则指向类。self 不是 python 关键字，我们把他换成其它单词也是可以正常执行的

## 继承

- 需要注意圆括号中基类的顺序，若是基类中有相同的方法名，而在子类使用时未指定，python从左至右搜索 即方法在子类中未找到时，从左到右查找基类中是否包含方法。

  ```python
  class DerivedClassName(BaseClassName1):
      <statement-1>
      .
      .
      .
      <statement-N>
  ```

- BaseClassName（示例中的基类名）必须与派生类定义在一个作用域内。除了类，还可以用表达式，基类定义在另一个模块中时这一点非常有用:

  ```python
  class DerivedClassName(modname.BaseClassName):
  ```

## 多继承

- 语法

  ```python
  class DerivedClassName(Base1, Base2, Base3):
      <statement-1>
      .
      .
      .
      <statement-N>
  ```

## 方法重写

- 如果父类方法的功能不能满足需求，可以在子类重写父类的方法

- super()函数是用于调用父类(超类)的一个方法

  ```python
  super(type[, object-or-type])
  ```

  - type -- 类。
  - object-or-type -- 类，一般是 self

## 类属性与方法

### 类的私有属性

**__private_attrs**：**两个下划线开头**，声明该属性为私有，不能在类的外部被使用或直接访问。在类内部的方法中使用时 **self.__private_attrs**。

### 类的方法

在类的内部，使用 def 关键字来定义一个方法，与一般函数定义不同，类方法必须包含参数 self，且为第一个参数，self 代表的是类的实例。

self 的名字并不是规定死的，也可以使用 this，但是最好还是按照约定是用 self。

### 类的私有方法

**__private_method**：**两个下划线开头**，声明该方法为私有方法，只能在类的内部调用 ，不能在类的外部调用。**self.__private_methods**。

### 类的专有方法

- **__init__ :** 构造函数，在生成对象时调用
- **__del__ :** 析构函数，释放对象时使用
- **__repr__ :** 打印，转换
- **__setitem__ :** 按照索引赋值
- **__getitem__:** 按照索引获取值
- **__len__:** 获得长度
- **__cmp__:** 比较运算
- **__call__:** 函数调用
- **__add__:** 加运算
- **__sub__:** 减运算
- **__mul__:** 乘运算
- **__truediv__:** 除运算
- **__mod__:** 求余运算
- **__pow__:** 乘方

### 运算符重载

> 重写类的专有方法