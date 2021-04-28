# Vue

## Vue的特点

- 遵循MVVM模式（Model-View-ViewModel），View层代表的是视图、模版，负责将数据模型转化为UI展现出来。Model层代表的是模型、数据，可以在Model层中定义数据修改和操作的业务逻辑。ViewModel层连接Model和View
- 只关注UI，可以引入VUE插件（依赖VUE）以及第三方库（不依赖VUE）
- 借鉴angular的模板和数据绑定技术，借鉴react组件化和虚拟DOM技术

## Vue插件

- vue-cli：脚手架
- vue-resource（axios）：ajax请求
- vue-router：路由
- vuex：状态管理
- vue-lazyload：图片懒加载
- vue-scroller：页面滑动相关
- mint-ui：移动端UI组件库
- element-ui：PC端UI组件库

# Vue实例

## 创建Vue实例

```javascript
var vm = new Vue({
  // 选项
})
```

## 数据与方法

- 当一个 Vue 实例被创建时，它将 `data` 对象中的所有的属性加入到 Vue 的**响应式系统**中
- 当这些数据改变时，视图会进行重渲染。值得注意的是只有当实例被创建时 `data` 中存在的属性才是**响应式**的，后面添加的数据不会被追踪。如果你知道你会在晚些时候需要一个属性，但是一开始它为空或不存在，那么你仅需要设置一些初始值。
- 唯一的例外是使用 `Object.freeze()`，这会阻止修改现有的属性，也意味着响应系统无法再*追踪*变化

## 生命周期

![](.\lifecycle.png)

# 模板语法

## 插值

- 数据绑定最常见的形式就是使用“Mustache”语法 (双大括号) 的文本插值
- 通过使用 v-once 指令，能执行一次性地插值，当数据改变时，插值处的内容不会更新
- 双大括号会将数据解释为普通文本，而非 HTML 代码。为了输出真正的 HTML，你需要使用 `v-html` 指令
- 动态渲染的任意 HTML 可能会非常危险，因为它很容易导致 XSS 攻击。请只对可信内容使用 HTML 插值，**绝不要**对用户提供的内容使用插值
- Mustache 语法不能作用在 HTML 特性上，遇到这种情况应该使用 v-bind 指令
- 对于所有的数据绑定，Vue.js 都提供了完全的 JavaScript 表达式支持。每个绑定都只能包含**单个表达式**。语句，不是表达式。流控制也不会生效，请使用三元表达式

### 插值表达式、v-text、v-html

- v-text、v-html都会覆盖标签里面的内容

### 防止闪烁

- 使用v-cloak指令可以解决插值表达式闪烁问题
- v-text、v-html 自动防止闪烁

## 指令

- 指令 (Directives) 是带有 `v-` 前缀的特殊符号。指令的职责是，当表达式的值改变时，将其产生的连带影响，响应式地作用于 DOM
- 修饰符 (modifier) 是以半角句号 `.` 指明的特殊后缀，用于指出一个指令应该以特殊方式绑定。例如，`.prevent` 修饰符告诉 `v-on` 指令对于触发的事件调用 `event.preventDefault()`

# 计算属性与监听器

## 计算属性

> 对于任何复杂逻辑，你都应当使用**计算属性**

```html
<div id="example">
  <p>Original message: "{{ message }}"</p>
  <p>Computed reversed message: "{{ reversedMessage }}"</p>
</div>
```

```javascript
var vm = new Vue({
  el: '#example',
  data: {
    message: 'Hello'
  },
  computed: {
    // 计算属性的 getter
    reversedMessage: function () {
      // `this` 指向 vm 实例
      return this.message.split('').reverse().join('')
    }
  }
})
```

- 我们可以将同一函数定义为一个方法而不是一个计算属性。两种方式的最终结果确实是完全相同的。然而，不同的是**计算属性是基于它们的响应式依赖进行缓存的**。只在相关响应式依赖发生改变时它们才会重新求值。这就意味着只要 `message` 还没有发生改变，多次访问 `reversedMessage` 计算属性会立即返回之前的计算结果，而不必再次执行函数。如果你不希望有缓存，请用方法来替代。

## 监听器

>虽然计算属性在大多数情况下更合适，但有时也需要一个自定义的侦听器。这就是为什么 Vue 通过 `watch` 选项提供了一个更通用的方法，来响应数据的变化。当需要在数据变化时执行异步或开销较大的操作时，这个方式是最有用的

# Class与Style绑定

> 操作元素的 class 列表和内联样式是数据绑定的一个常见需求。因为它们都是属性，所以我们可以用 `v-bind` 处理它们：只需要通过表达式计算出字符串结果即可。不过，字符串拼接麻烦且易错。因此，在将 `v-bind` 用于 `class` 和 `style` 时，Vue.js 做了专门的增强。表达式结果的类型除了字符串之外，还可以是对象或数组



## 绑定HTML Class

### 对象语法

```vue
<div v-bind:class="{ active: isActive }"></div>

data: {
  isActive: true,
  hasError: false
}
```

```vue
<div v-bind:class="classObject"></div>

data: {
  classObject: {
    active: true,
    'text-danger': false
  }
}
```

```vue
<div v-bind:class="classObject"></div>

data: {
  isActive: true,
  error: null
},
computed: {
  classObject: function () {
    return {
      active: this.isActive && !this.error,
      'text-danger': this.error && this.error.type === 'fatal'
    }
  }
}
```

### 数组语法

- 我们可以把一个数组传给 `v-bind:class`，以应用一个 class 列表

```html
<div v-bind:class="[activeClass, errorClass]"></div>
```

```javascript
data: {
  activeClass: 'active',
  errorClass: 'text-danger'
}
```

### 组件

## 绑定内联样式

> `v-bind:style` 的对象语法十分直观——看着非常像 CSS，但其实是一个 JavaScript 对象。CSS 属性名可以用驼峰式 (camelCase) 或短横线分隔 (kebab-case，记得用引号括起来) 来命名

### 对象语法

```
<div v-bind:style="{ color: activeColor, fontSize: fontSize + 'px' }"></div>

data: {
  activeColor: 'red',
  fontSize: 30
}
```

```
<div v-bind:style="styleObject"></div>

data: {
  styleObject: {
    color: 'red',
    fontSize: '13px'
  }
}
```

### 数组语法

# 条件渲染

## v-if

- 因为 `v-if` 是一个指令，所以必须将它添加到一个元素上。但是如果想切换多个元素呢？此时可以把一个 `<template>` 元素当做不可见的包裹元素，并在上面使用 `v-if`
- 使用 `v-else` 指令来表示 `v-if` 的“else 块”
- `v-else-if`，顾名思义，充当 `v-if` 的“else-if 块”，可以连续使用
- Vue 会尽可能高效地渲染元素，通常会复用已有元素而不是从头开始渲染。Vue 为你提供了一种方式来表达“这两个元素是完全独立的，不要复用它们”。只需添加一个具有唯一值的 key 属性即可。

## v-show

- 用于根据条件展示元素的选项是 `v-show` 指令
- 不同的是带有 `v-show` 的元素始终会被渲染并保留在 DOM 中。`v-show` 只是简单地切换元素的 CSS 属性 `display`
- `v-show` 不支持 `<template>` 元素，也不支持 `v-else`

# 列表渲染

## 数组

- 用 `v-for` 指令基于一个数组来渲染一个列表。
- `v-for` 指令需要使用 `item in items` 形式的特殊语法，其中 `items` 是源数据数组，而 `item` 则是被迭代的数组元素的**别名**。
- `v-for` 还支持一个可选的第二个参数，即当前项的索引
- 可以用 `of` 替代 `in` 作为分隔符，因为它更接近 JavaScript 迭代器的语法

## 对象

```vue
<div v-for="(value, name, index) in object">
  {{ index }}. {{ name }}: {{ value }}
</div>
```

## 维护状态

> 当 Vue 正在更新使用 `v-for` 渲染的元素列表时，它默认使用“就地更新”的策略。如果数据项的顺序被改变，Vue 将不会移动 DOM 元素来匹配数据项的顺序，而是就地更新每个元素，并且确保它们在每个索引位置正确渲染。为了给 Vue 一个提示，以便它能跟踪每个节点的身份，从而重用和重新排序现有元素，你需要为每项提供一个唯一 key 属性

```vue
<div v-for="item in items" v-bind:key="item.id">
  <!-- 内容 -->
</div>
```

- 建议尽可能在使用 `v-for` 时提供 `key` attribute，除非遍历输出的 DOM 内容非常简单，或者是刻意依赖默认行为以获取性能上的提升。

## 数组更新检测（深度监听）

### 变异方法

Vue 将被侦听的数组的变异方法进行了包裹，所以它们也将会触发视图更新。这些被包裹过的方法包括：

- `push()`
- `pop()`
- `shift()`
- `unshift()`
- `splice()`
- `sort()`
- `reverse()`

### 替换数组

> 变异方法，顾名思义，会改变调用了这些方法的原始数组。相比之下，也有非变异 (non-mutating method) 方法，例如 `filter()`、`concat()` 和 `slice()` 。它们不会改变原始数组，而**总是返回一个新数组**。当使用非变异方法时，可以用新数组替换旧数组

## 注意

- 利用索引直接设置一个数组项时，修改数组的长度时，Vue不能检测数组的变化
- 由于 JavaScript 的限制，**Vue 不能检测对象属性的添加或删除**

# 事件处理

> 当一个 ViewModel 被销毁时，所有的事件处理器都会自动被删除

## 监听事件

- 可以用 `v-on` 指令监听 DOM 事件，并在触发时运行一些 JavaScript 代码。其中v-on可以简化为@

```vue
<div id="example-1">
  <button v-on:click="counter += 1">Add 1</button>
  <p>The button above has been clicked {{ counter }} times.</p>
</div>
```

## 事件处理方法

- 然而许多事件处理逻辑会更为复杂，所以直接把 JavaScript 代码写在 `v-on` 指令中是不可行的。因此 `v-on` 还可以接收一个需要调用的方法名称


- 有时也需要在内联语句处理器中访问原始的 DOM 事件。可以用特殊变量 `$event` 把它传入方法

## 事件修饰符

> 使用修饰符时，顺序很重要

- `.stop` 阻止单击事件继续传播
- `.prevent` 提交事件不再重载页面
- `.capture` 即元素自身触发的事件先在此处理，然后才交由内部元素进行处理
- `.self`
- `.once`
- `.passive`

## 按键修饰符

- keyup.xxxKey

# 表单输入绑定

- 你可以用 `v-model` 指令在表单 `<input>`、`<textarea>` 及 `<select>` 元素上创建双向数据绑定。它会根据控件类型自动选取正确的方法来更新元素。
- `v-model` 会忽略所有表单元素的 `value`、`checked`、`selected` 特性的初始值而总是将 Vue 实例的数据作为数据来源。你应该通过 JavaScript 在组件的 `data` 选项中声明初始值。
- `v-model` 在内部为不同的输入元素使用不同的属性并抛出不同的事件：
  - text 和 textarea 元素使用 `value` 属性和 `input` 事件；
  - checkbox 和 radio 使用 `checked` 属性和 `change` 事件；
  - select 字段将 `value` 作为 prop 并将 `change` 作为事件。

# 组件基础

- 组件是可复用的 Vue 实例，且带有一个名字
- 因为组件是可复用的 Vue 实例，所以它们与 `new Vue` 接收相同的选项，例如 `data`、`computed`、`watch`、`methods` 以及生命周期钩子等。仅有的例外是像 `el` 这样根实例特有的选项
- 组件的`data` 必须是一个函数

## 组件注册

全局注册，全局注册的组件可以用在其被注册之后的任何 (通过 `new Vue`) 新创建的 Vue 根实例，也包括其组件树中的所有子组件的模板中

```javascript
Vue.component('my-component-name', {
  // ... options ...
})
```

## 组件数据传递

- Prop 是你可以在组件上注册的一些自定义特性。当一个值传递给一个 prop 特性的时候，它就变成了那个组件实例的一个属性。









