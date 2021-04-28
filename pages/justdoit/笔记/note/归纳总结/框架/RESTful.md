# 定义

> Resource Representational State Transfer

- Resource 资源
- Representational 表现形式
- State Transfer 状态转移

# 意义

- 前后端分离，统一调用

# 层次

- level0 面向前台
- level1 面向资源，利用分治法将大型服务端点分解为多个资源
- level2 打上标签，利用GET、POST等动词
- level3 完美服务，可发现性，使协议拥有自我描述的能力

# 那些动词

- GET 用来获取资源
- POST 用来新建资源（也可以用于更新资源）
- PUT 用来更新资源
- DELETE 用来删除资源

# 文件上传

- 一样的使用`MultipartFile`
- 大文件上传解决方法：分片上传、断点续传 

