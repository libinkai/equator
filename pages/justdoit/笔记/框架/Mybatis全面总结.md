# 基础

> ORM Object Relational Mapping，对象-关系映射

## 常见的持久化框架

- Hibernate
- JPA Java Persistence API
- Spring JDBC
- Mybatis

## 架构

![mybatis架构](.\mybatis架构.png)

## 整体流程

1. 使用配置文件构建`SqlSessionFactory`
2. 使用`SqlSessionFactory`获得`SqlSession`，`SqlSession`相当于传统JDBC的connection
3. 使用`SqlSession`得到`Mapper`
4. 使用`Mapper`执行SQL
5. 将结果封装到JavaBean

# 基础支持层

## 解析器

> 解析XML

## 反射工具箱

> 对Java反射进行进一步封装

## 类型转换

> Java类型与JDBC类型互转

## 日志模块

## 资源加载

## 数据源模块

## 事务模块

## binding模块

> 定义Mapper接口，提前发现类型不对应错误

## 缓存模块

# 核心处理层

## 配置解析

## SQL解析

## 结果集映射

## 参数映射

## SQL执行

# 接口层 SqlSession

# 高级

## 插件

## Spring整合Mybatis

