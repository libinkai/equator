# 初识Spring

# JDBC必知必会

## 配置单数据源

## 事务抽象

### 传播行为

### 隔离级别

### 编程式事务

### 声明式事务

- 开启事务注解`EnableTransactionManagement`
- 配置属性
  - proxyTargetClass 布尔
  - mode
  - order 事务拦截器顺序
- `Transactional`
  - transactionManager
  - propagation
  - isolation
  - timeout
  - readOnly
  - rollbackFor 回滚条件
- 注意service方法子调用导致无法使用事务

## 异常抽象

- Spring会将数据库操作异常转换为DataAccessException，无论使用何种数据访问方式，都能使用一样的异常
- Spring统一错误码，通过`SQLErrorCodeExceptionTranslator`

# OR Mapping 实践

# NoSql 实践

# 数据库访问进阶

# Spring MVC实践

# 访问Web资源

# Web开发进阶

# 重新认识SpringBoot

# 运行中的SpringBoot

# Spring Cloud及Cloud Native概述

# 服务注册与发现

# 服务熔断

# 服务配置

# Spring Cloud Stream

# 服务链路追踪