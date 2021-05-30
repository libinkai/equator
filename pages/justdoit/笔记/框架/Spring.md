# IOC

> IOC，Inversion of Control，控制反转

- DI，Dependence Injection，依赖注入，将底层类作为参数传递给上层类，实现上层对下层的控制

## IOC的实现

- DL（已过时）
- DI
  - 构造器注入
  - 接口注入
  - Set方法注入
  - 注解注入

## 流程

1. 读取Bean配置信息
2. 根据Bean注册表实例化Bean
3. 将Bean实例放入Spring容器
4. 使用Bean

## 相关类

### BeanDefinition

- 主要用来描述Bean的定义，将xml或者注解Bean解析为BeanDefinition

### BeanDefinitionRegistry

- 提供向IOC容器注册BeanDefinition对象的方法

### BeanFactory

- 提供IOC的配置机制
- 包含Bean的各种定义，便于实例化Bean
- 建立Bean之间的依赖关系
- Bean生命周期的控制

### ApplicationContext

> 实现多个接口

- BeanFactory：能够管理、装配Bean
- ResourcePatternResolver：能够加载资源文件
- MessageSource：国际化
- ApplicationEventPublisher：注册监听器，实现监听机制

## refresh方法

## getBean方法

1. 转换beanName
2. 从缓存中加载实例
3. 实例化Bean
4. 检测parentBeanFactory
5. 初始化依赖的Bean
6. 创建Bean

## Bean的作用域

- singleton，默认，容器里面拥有唯一的Bean实例
- prototype，**针对每个getBean请求，容器创建一个Bean实例**
- request
- session
- globalSession（仅对Portlet有效）

## 生命周期

## 解决循环依赖问题

- 发生循环依赖时，如果容器不处理的话，容器会无限执行初始化bean流程，直到内存溢出
- 在容器再次发现 beanB 依赖于 beanA 时，容器会获取 beanA 对象的一个早期的引用（early reference），并把这个早期引用注入到 beanB 中，让 beanB 先完成实例化。beanB 完成实例化，beanA 就可以获取到 beanB 的引用，beanA 随之完成实例化（构造器注入循环依赖Spring无力解决）

# AOP

> 面向切面编程

- 通用化代码的实现，对应的就是所谓的切面Aspect

## 织入方式

- 编译时织入：需要特殊的编译器，如AspectJ
- 类加载时织入：需要特殊的编译器，如AspectJ和AspectWerkz
- 运行时织入：Spring默认，动态代理方式实现

## 概念

- Aspect：通用功能的代码实现
- Target：被织入Aspect的对象
- Join Point：可以作为切入点的机会，**所有方法都可以作为切入点**
- Pointcut：切面实际被应用在的Join Point，支持正则表达式
- Advice：类里的方法以及这个方法如何织入到目标方法的方式
  - 前置通知 Before
  - 后置通知 AfterReturning
  - 异常通知 AfterThrowing
  - 最终通知 After
  - 环绕通知 Around
- Weaving：织入的过程

## 实现

> 由AopProxyFactory根据AdvisedSupport对象的配置来决定。默认策略如果目标类是接口，则使用JDK代理，否则使用后者

## 代理模式

> 接口+真实实现类+代理类

- Spring中的代理模式
  - 真实实现类的逻辑包含在`getBean`方法中
  - `getBean`方法实际上是proxy的实例
  - proxy实例是spring采用JDK Proxy或者CGLIB动态生成的

### JDK代理

- 核心：`InvocationHandler`接口和Proxy类
- 通过Java反射机制实现，在生成类的过程中比较高效

### CGLIB

- 以继承的方式动态生成目标类的代理对象，不能代理final类
- 借助ASM实现，在生成类之后的执行过程中比较高效

# 事务

