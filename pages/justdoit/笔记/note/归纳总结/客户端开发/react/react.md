# React初探

> Facebook于2013年开源

- React Fiber 即React 16.x
- 声明式开发，减少DOM操作代码量，Jquery等为命令式开发
- React可以与其它框架并存，其只管理自己挂载的部分
- 组件化
- 单向数据流，props是只读的，方便问题的定位
- 视图层的框架，复杂组件之间的传值需要使用数据层框架，如Redux
- 函数式编程，方便自动化测试

## 引入React

1. 引入.js来使用React
2. 通过脚手架编码（官方推荐`Create-react-app`）

## 基础环境

1. node、npm

2. 脚手架

   ```
   npm install -g create-react-app
   ```

3. 创建项目

   ```
   create-react-app project_name
   cd project_name
   npm install
   ```

## 项目目录结构

- node_modules 第三方包
- public 静态资源
  - favicon.ico
  - index.html
  - robots.txt
  - manifest.json（PWA清单）
- src
  - App.css
  - App.js
  - App.test.js
  - index.css
  - index.js 程序入口
  - logo.svg
  - serviceWorker.js 缓存工具
  - setupTests.js
- .gitignore
- package-lock.json
- package.json
- readme.md

## 组件

- 组件化编程

- 定义组件

  ```react
  import React, {Component} from 'react';
  class App extends Component {
  	render(){
  		return (
  			<div>hello world</div>
  		)
  	}
  }
  // 等价于
  import React from 'react';
  class App extends React.Component {
  	render(){
  		return (
  			<div>hello world</div>
  		)
  	}
  }
  
  export default App;
  ```

- 挂载组件

  ```react
  import React from 'react'; // 貌似没有使用，但是必须引入，用于编译JSX
  import ReactDOM from 'react-dom';
  import App from './App';
  ReactDOM.render(<App/>,document.getElementById('root'));
  ```

## JSX基础语法

> 在JS中书写HTML标签

- JSX中，HTML标签不需要单引号或者双引号

- 自定义组件，组件名称首字母大写（原生标签小写）

- 一个组件必须有且仅有一个父DIV，使用`React.Fragment`可以作为父容器而最后不被渲染

- 变量，函数使用`{}`包裹

- 注释

  ```
  {/*注释*/}
  {
  	// 注释
  }
  ```

- CSS一般独立写成一个样式文件，然后在组件中引入
- 使用class的时候，需要使用`className`
- 渲染Html，使用dangerousSetInnerHTML属性，如`<li>{item}</li>`改为`<li dangerousSetInnerHTML={{__html:item}}></li>`
- 使用label时，`for`需要改为`htmlFor`

# React基础精讲

## 响应式设计

- React不同于Vue等的双向数据绑定，需要自己处理数据的变化

```react
constructor(props) {
    super(props);
    // 使用state来保存数据
    this.state = {
        inputValue: "input your todo here",
        todolist: []
    }
}

<input value={this.state.inputValue} />
```

## 事件绑定

### 语法

- 使用驼峰命名法，如`onChange={this.handleInputChange}`

```react
handleInputChange(e) {
    // React为每一个组件提供了修改state的方法
    // this.state.inputValue = e.target.value;
    this.setState({
        inputValue: e.target.value
    })
}
<input value={this.state.inputValue} onChange={this.handleInputChange.bind(this)} />
```

### this指向问题

1. 声明时绑定 `<input value={this.state.inputValue} onChange={this.handleInputChange.bind(this)} />`
2. 推荐在组件的构造方法中进行绑定，会节约性能`this.handleInputChange = this.handleInputChange.bind(this)`
3. 使用 class fields 正确的绑定回调函数`handleInputChange = () => {}`
4. 在回调中使用箭头函数`onChange={()=>this.handleInputChange}`

### 传递参数

- React 的事件对象 `e` 会被作为第二个参数传递。如果通过箭头函数的方式，事件对象必须显式的进行传递，而通过 `bind` 的方式，事件对象以及更多的参数将会被隐式的进行传递

```react
<button onChange={(e) => this.handleInputChange(id, e)}>XXX</button>
<button onChange={this.handleInputChange.bind(this, id)}>XXX</button>
```

## 组件以及组件间通信

- React是单向数据流，组件间构成了树状结构
- 变量，函数都可以通过属性的方式传递到子组件

# React高级内容

## PropsTypes

```
import PropTypes from 'prop-types';
XXX.propTypes = {
    item: PropTypes.string.isRequired,
    index: PropTypes.number,
    handleDeleteItem: PropTypes.func
}
export default XXX
```

## DefaultProps

```
TodoItem.defaultProps = {
    item: 'item name'
}
```

## State、Props、render的关系

- state或者props改变时，render函数会重新执行
- 父组件的render函数执行时，子组件的render函数也会重新执行（递归上）

## 虚拟DOM

- 每次页面变化时，如果重新生成DOM片段（DocumentFragment）再替换，会非常损耗性能。如果不直接替换原始的DOM，而是通过先比较找出变化的部分，做局部的替换，但是比对部分也会损耗性能

- 综上所述，利用虚拟DOM技术（使用JS对象来描述真实DOM），通过比对找到变化的点，然后直接去操作DOM改变其内容，可以有效地提示性能。（JS创建对象比创建DOM的性能高得多）

- JSX createElement->JS对象（虚拟DOM）->真实的DOM

  ```react
  render() {
      return <li>{this.props.item}</li>
  }
  // 等价于
  render() {
      return React.createElement('li',{},this.props.item);
  }
  ```

- 优势

1. 提升比较性能
2. 使得跨端应用得以实现（原生应用可以识别JS对象）

## 虚拟DOM的Diff算法

> Difference，比对新旧虚拟DOM的不同之处

- Diff的发生时机在state改变的时候
- React会将多个setState合并为一个动作
- Diff的核心是同层比对，如果某一层不同，其下面的子节点将被全部替换
- 如果虚拟DOM拥有key，可以避免嵌套循环查找，会提高比对的性能（前提是新的虚拟DOM的key与旧的虚拟DOM的key一致）
- 不推荐使用index作为key的原因：index不稳定，会造成新旧虚拟DOM的key不一致

## Ref

- 获取元素DOM的一个途径

- 响应事件

  ```
  <input ref={(input)=>{this.inputElement = input}}/>
  
  e.target.value等价于this.inputElement.value
  ```

- 不推荐使用ref的原因：setState方法是异步的，有可能导致通过ref获取的DOM数据不一致（实际上可以在setState的回调函数中获取即可，但是不推荐使用ref）

## 生命周期函数

> 生命周期指的是在某一个时刻，组件会自动调用执行的函数

### Initialization

- constructor本质上也是一个生命周期函数

### Mounting

1. componentWillMount 组件即将被挂载的时刻
2. render 挂载，渲染
3. componentDidMount 组件被挂载之后的时刻

### Updation

1. componentWillReceiveProps （props改变时才会调用，state改变时不会调用）当组件从父组件接收了参数，组件不是第一次出现在父组件的时候才会被调用
2. shouldComponentUpdate 组件被更新之前，返回布尔值，决定了后续的函数是否被执行
3. componentWillUpdate 组件被更新之前，shouldComponentUpdate返回true才会被执行
4. render
5. componentDidUpdate 组件更新之后

### UnMounting

1. componentWillUnMount 当组件即将被从页面中剔除的时刻

### 使用场景

- 除了render函数之外的生命周期函数都可以不实现

- shouldComponentUpdate函数可以用来避免父组件的render调用导致全部子组件的递归渲染

  ```
  shouldComponentUpdate(nextProps,nextState){
  	if(nextProps.xxx !== this.props.xxx){
  		return false;
  	}
  	return true;
  }
  ```

- 网络请求在componentDidMount，不推荐componentWillMount，这样会和以后的技术冲突

## 网络请求

- axios

## 接口模拟

- Charles

## 动画

- 过渡动画、以及动画：通过变量来控制class

## react-transition-group

### CSSTransition

- 该组件包裹想要实现动画的单个元素|组件

### TransitionGroup

- 该组件搭配CSSTransition以实现多个元素|组件的动画效果

# Redux

> 数据层框架，Redux=Reducer+Flux

- 将所有数据保存在Redux的Store里，统一管理

## 工作流

![avatar](W:\leaning\note\归纳总结\客户端开发\react\redux工作流.jpg)

- React Component
- Action Creator
- Store
- Reducer

## 核心思想

1. store必须是唯一的
2. 只有store能修改自己的内容
3. reducer必须是纯函数（给定固定的输入，就一定有固定的输出，而且不会有任何副作用），常见非纯函数的例子——Date、UUID、AJAX

## UI组件与容器组件

- 将组件中render的内容拆分出来独立成为UI组件，容器组件通过属性将数据与函数传递给UI组件（这样的话，绑定this的时候统一在constructor函数之中）
- UI组件也叫傻瓜组件，容器组件也叫聪明的组件

## 无状态组件

- 一个只有render函数的组件，可以进一步定义为一个函数

- 示例

  ```
  const XXXUI = (props)=>{
  	return (<div></div>)
  }
  
  export default XXXUI;
  ```

## 发送异步请求

1. 在componentDidMount中发起网络请求
2. 创建Action
3. 派发Action

## Redux-thunk

> 统一管理异步函数

- ![avatar](W:\leaning\note\归纳总结\客户端开发\react\redux与redux-thunk.jpg)

- 在创建store的时候，使用redux中间件
- Action返回一个函数
- 将Action作为参数传入dispatch即可进行异步调用

## Redux-saga

- 将异步函数独立管理

## React-redux

> 更加方便地在react中使用redux

- 通过connect连接状态与逻辑，返回一个容器组件

# 实战

## 样式

- CSS是全局共享的，需要引入第三方库`styled-components`进行隔离，样式组件化
- 保持样式统一，需要引入`reset.css`的样式

## 数据

- 使用immutable.js库，避免在reducer中修改了state
- 使用redux-immutable.js统一数据格式

## 路由

- react-router-dom

## 异步组件

> 懒加载

- react-loadable