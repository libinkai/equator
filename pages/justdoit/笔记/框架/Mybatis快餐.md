# 工作流程

- **通过Reader对象读取Mybatis配置文件**
- **通过SqlSessionFactoryBuilder对象创建SqlSessionFactory对象**
- **获取当前线程的SQLSession**
- **事务默认开启**
- **通过SQLSession读取映射文件中的操作编号，从而读取SQL语句**
- **提交事务**
- **关闭资源**

# `#{}`和`${}`的区别

- `#{}`是预编译处理，`${}`是字符串替换

- Mybatis在处理`#{}`时，会将sql中的`#{}`替换为?号，调用PreparedStatement的set方法来赋值；

- Mybatis在处理`${}`时，就是把`${}`替换成变量的值

- 使用`#{}`可以有效的防止SQL注入，提高系统安全性

# Mapper接口可以重载吗

- mapper接口里的方法是不能被重载的，因为是使用全限名+方法名的保存和寻找策略

# Mapper工作原理

- 接口的全限名，就是映射文件中的namespace的值；接口的方法名，就是映射文件中Mapper的Statement的id值；接口方法内的参数，就是传递给sql的参数。 mapper接口是没有实现类的，当调用接口方法时,接口全限名+方法名拼接字符串作为key值，可唯一定位一个MapperStatement。在Mybatis中，每一个<select>、<insert>、<update>、<delete>标签，都会被解析为一个MapperStatement对象
- Dao接口的工作原理是JDK动态代理，Mybatis运行时会使用JDK动态代理为Dao接口生成代理proxy对象，代理对象proxy会拦截接口方法，转而执行MappedStatement所代表的sql，然后将sql执行结果返回

# Mybatis的一级、二级缓存

- 一级缓存 事务范围：缓存只能被当前事务访问。缓存的生命周期 依赖于事务的生命周期当事务结束时，缓存也就结束生命周期。 在此范围下，缓存的介质是内存。 二级缓存 进程范围：缓存被进程内的所有事务共享。这些事务有 可能是并发访问缓存，因此必须对缓存采取必要的事务隔离机制。 缓存的生命周期依赖于进程的生命周期，进程结束时， 缓存也就结束了生命周期。进程范围的缓存可能会存放大量的数据， 所以存放的介质可以是内存或硬盘
- **mybatis一级缓存是一个SqlSession级别，sqlsession只能访问自己的一级缓存的数据**
- **二级缓存是跨sqlSession，是mapper级别的缓存，对于mapper级别的缓存不同的sqlsession是可以共享的**
- Mybatis默认就是支持一级缓存的，并不需要我们配置。mybatis和spring整合后进行mapper代理开发，不支持一级缓存，mybatis和spring整合，spring按照mapper的模板去生成mapper代理对象，模板中在最后统一关闭sqlsession

# 动态SQL

> Mybatis提供了9种动态sql标签

- Mybatis动态sql可以让我们在Xml映射文件内，以标签的形式编写动态sql，完成逻辑判断和动态拼接sql的功能。其执行原理为：使用OGNL（）从sql参数对象中计算表达式的值，根据表达式的值动态拼接sql，以此来完成动态sql的功能
- 对象导航图语言（Object Graph Navigation Language），简称OGNL，是应用于Java中的一个开源的表达式语言（Expression Language），作用是对数据进行访问，它拥有类型转换、访问对象方法、操作集合对象等功能

## if

- ```
  <if test="xxx"></if>
  ```

- where中使用，条件查询

- update中使用，只更新部分字段

- insert中使用，非空属性才插入

## trim、set、where

## foreach

- collection：必填， 集合/数组/Map的名称

  - 只有一个数组参数或集合参数

    默认情况： 集合collection=list， 数组是collection=array

    推荐： 使用 @Param 来指定参数的名称， 如我们在参数前@Param("ids")， 则就填写 collection=ids

    注：多参数请使用 @Param 来指定， 否则SQL中会很不方便

  - 参数是Map：指定为 Map 中的对应的 Key 即可。 其实上面的 @Param 最后也是转化为 Map 的
  - 参数是对象：使用`对象.属性`即可

- item：变量名。 即从迭代的对象中取出的每一个值

- index：索引的属性名。 当迭代的对象为 Map 时， 该值为 Map 中的 Key

- open：循环开头的字符串

- close：循环结束的字符串

- separator： 每次循环的分隔符

## choose、when、otherwise

> 实现if else逻辑，一个 choose 标签至少有一个 when，最多一个otherwise

## bind

> 通过 OGNL 表达式去定义一个上下文的变量

# 分页

- Mybatis使用RowBounds对象进行分页，它是针对ResultSet结果集执行的内存分页，而非物理分页，可以在sql内直接书写带有物理分页的参数来完成物理分页功能，也可以使用分页插件来完成物理分页
- 分页插件的基本原理是使用Mybatis提供的插件接口，实现自定义插件，在插件的拦截方法内拦截待执行的sql，然后重写sql，根据dialect方言，添加对应的物理分页语句和物理分页参数

# 查询原理

SqlSessionFactoryBean
	opensession
	getConfiguration(所有配置信息都在Configuration)
		MapperRegistr(mapper注册表,里面有 Map<type,MapperProxy>)
		TypeHandler
		Map<String,MappedStatement> (一个 insert|select|update|delete 就是一个MappedStatement)
		Map<String,Cache>
		Map<String,ResultMap>
		Map<String,ParameterMap>
		...
		

构建SqlSessionFactory
1. 先解析配置参数 mybatis-config.xml
2. 再解析mapper.xml 文件
	配置文件属性:
		property属性:
			typeAliases: 配置别名
			typeHandlers: 类型转换
			plugins: 插件
			...
		解析mapperLocations：mapper文件路径
			通过解析里面的select/insert/update/delete节点，每一个节点生成一个MappedStatement对象。
			最后注册到Configuration对象的mappedStatements。key为mapper的namespace+节点id。
				<select id="对象方法名"> </select>
					mapperKey = namespace+id
			缓存:
				<cache/>: 配置开启mybatis 二级缓存
					configuration 里面有一个CacheMap ,这些缓存就村到cacheMap 里面
				<cache-ref/>
			resultMap、parameterMap:
				查询结果集中的列与Java对象中属性的对应关系。其实，只有在数据库字段与JavaBean不匹
				配的情况下才用到，通常情况下推荐使用resultType/parameterType.
				解析完成之后也是保存到configuration里面，Map 里面。
			sql 标签： 
				对可复用的sql提取出来。
				内容放入sqlFragments容器。id为命名空间+节点id.
				其他节点通过 <include id="sqlId"/> 复用
			input|select|update|delete标签:
				动态sql是mybatis的核心，Choose,ForEach,If,Set,Where等
				每一种动态标签对应一种处理器,一层一层循环调用处理器形成完整sql语句,最后解析一定会变成静态sql.
				input等标签解析完成之后，生成一个mappedstatement 对象，注册到configuration里面，等待调用。
				创建mappedstatement是把一些基本参数也放进去，resultMap 等等.
			到此xml解析完成，最终生成了一个configuration对象，Dao接口调用时，根据namespace+id 
			找到对应的mappedstatement 来处理sql数据请求。
		-------------MapperProxy<T>------------------------------------------------------------------------------------
		-					mybatis xml 配置解析完成				-
		-												-	
		-------------------------------------------------------------------------------------------------
3. 基于注解实现:
	除了在mapper文件中配置SQL，Mybatis还支持注解方式的SQL。通过@Select，标注在Mapper接口的方法上。
		@Select("select * from user ")
	你想要的是动态SQL，那么就加上<script>
		@Select(`<script>
			select * from user 
				<if test='id!=null'>
					where id=#{id}
				</if>
			</script>`)

	还可以通过@SelectProvider来声明一个类的方法，此方法负责返回一个SQL的字符串:
		详细见：https://juejin.im/post/5c84b3eb6fb9a049eb3cbf79#heading-8
	注解扫描:
		1.根据配置的mapper接口类保名，扫描该包获取 Dao 类信息。
		2.获取到包之后再解析:
		3.MapperRegistry:(cofiguration 里面的)
			MapperAnnotationBuilder:(mapperRegistry 内部调用)
				该方法会通过传入的dao接口对象，进行方法扫描，拿到方法上的注解sql字段.
				拿到注解sql字段之后解析生成mappedstatement对象，注册到configuration 里面，解析过程和
				xml解析一样.

		-------------------------------------------------------------------------------------------------
		-					mybatis  注解 解析完成					-
		-												-	
		-------------------------------------------------------------------------------------------------

mybatis 如何生成Dao接口的代理类的：
	mybatis通过spring 配置xml bean 扫描mapper.dao 生成 beanDefine，待使用.
		通过调用 spring 的 assPathBeanDefinitionScanner 的scaner 方法来扫描指定包下的文件.
	
		<property name="annotationClass" value="org.springframework.stereotype.Repository" />
	在类上写@Repository 时会跳过这个类，不会生成beanDefine 对象。
	
	得到beanDefine对象之后，key 还是dao类名字，而value 则被替换为 mapperFactoryBean<?> ,之后spring 调用则是调用的
	mapperFactoryBean。（通过引用修改beanDefine 内部数据，则spring那边同步修改了,因此注入的才是代理对象）
	
		https://blog.csdn.net/xiaokang123456kao/article/details/76228684
	最后获取到的就是 mapperProxy对象。
		mapperProxy 最终会调用 mapperMethod 这个类结合sqlSession 进一步处理请求。
			mapperMethod包含: 
				SqlCommand:
					处理sql 根据类型等找到对应的mappedstatement
				MethodSignature:
					方法的签名信息。里面包含：返回值类型、是否void、是否为集合类型、是否为Cursor等，
					主要还获取到了方法参数上的@Param注解的名称，方便下一步获取参数值
				结合前面，sqlsession 里面是有configuration 这个对象的，通过namespce+id 获取到Mappedstatement 
				处理数据。
			* 代理方式：
				如果是toString() 等方法 直接调用原方法
					method.invoke(target.args);
				如果调用的是sql方法
					通过 sqlSession 这个对象结合传入的参数去请求数据库.
	
		sqlSourse:
			动态生成的各种sqlNode保存在SqlSource对象.
		BoundSql:
			根据参数等，生成sql语句
			表示动态生成的SQL语句和相应的参数信息.(保存在sqlSourse 里面)
		ParameterMapping:
			对象保存的就是参数的类型信息，如果没有配置则为null。
			最后返回的BoundSql对象就包含一个带有占位符的SQL和参数的具体信息。
		获取到boundSql 对象之后，生成PreparedStatement。
		Connection:
			从数据库连接池获取Connection对象，并为它创建代理，以便打印日志.
		PreparedStatement:
			调用PreparedStatement之前先判断cache,没有命中再通过PreparedStatement 查询。

结果映射:
	ResultSetWrapper:
		数据库返回ResultSet,使用ResultSetWrapper包装解析。
	获取到数据及类型:
	        //元数据 列名、列类型等信息
		final ResultSetMetaData metaData = rs.getMetaData();
		final int columnCount = metaData.getColumnCount();
		类型转换：
			通过typeHandler数据类转换映射。
	MetaObject ：
		通过resultSet+ResultMap(可能是)+typehandler 经过反射最终生成返回的对象.
	BeanWapper:
		通过配置文件，获取到返回值类型，包装成BeanWapper。
	最后返回这个bean对象到最开始的查询处，进一步判断返回的daoPorxy对象。

查询结束