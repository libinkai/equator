# 数据绑定与VUE应用

## VUE实例与数据绑定

### 实例与数据

```
var vm = new Vue({
    el: "#app",
    data: {
        name: "Equator"
    }
})
```

- el用于指定一个页面中已经存在的DOM元素来挂载Vue实例，可以是HTMLElement也可以是CSS选择器
- Vue实例本身代理了data对象里面的所有属性，故可以直接通过vm.name访问data.name
- 除了显式地声明数据，也可以指向一个已经存在的变量，并且它们之间默认建立了双向数据绑定关系

### 生命周期

> 下面的这些生命周期钩子与data等类似，也是作为选项写入Vue实例之中，并且钩子this指向调用它的Vue实例

- created
- mounted
- beforeDestroy

### 插值与表达式

- {{}}插值语法，除了简单的属性绑定之外，还可以使用JavaScript表达式进行简单运算，三元运算等
- 只支持单个表达式，不支持语句与流程控制

### 过滤器

- filters作为Vue选项，在其中写入过滤方法
- {{name | filter_function}} 通过管道符使用过滤方法
- 过滤器可以串联，也可以传入参数

## 指令与事件

- v-on用于绑定事件、v-bind用于绑定属性


- 自定义响应方法在methods选项中写入，也可以是内联方法，但是不推荐使用后者
- Vue代理了methods里面的方法，可以直接调用

## 语法糖

- v-bind :
- v-on @

# 计算属性

## 用法

- 计算属性写在computed选项之中，直接使用在插值表达式中即可
- 每一个计算属性都有setter、getter
- 计算属性可以依赖其它计算属性
- 计算属性不仅可以依赖当前实例的数据，还可以依赖其它实例的数据

## 缓存

- methods可以达到computed的视觉效果，但是计算属性是基于缓存的

# v-bind指令以及class、style绑定

## 绑定class的方式

1. 通过v-bind:class设置一个对象，可以通过data、methods、computed设置
2. 需要应用多个class，可以通过数组设置

## 绑定内联样式

- 与:class类似，也有对象语法以及数组语法
- CSS属性名称使用驼峰原则（camelCase）或者短横分隔（kebab-case）

# 内置指令

## 基本指令

### v-cloak

- 与CSS搭配使用，防止插值表达式引起的屏幕闪动

```
[v-cloak] {
    display: none
}
```

### v-once

指定元素或者组件只渲染一次，包括其所有节点

## 条件渲染指令

> v-show适合频繁切换的场景

### v-if

### v-else-if

### v-else

- v-else-if要紧跟v-if，v-else紧跟v-else-if
- VUE在渲染元素时，会尽可能复用已经渲染的元素。可以在元素上面使用key属性取消元素的复用

### v-show

- 用法与v-if一致，只改变元素的CSS样式

## 列表渲染

### 用法

```
<ul>
	<li v-for="item in items">{{item.name}}</li>
</ul>
```

- v-for支持一个可选参数作为当前项的索引

```
v-for="(item,index) in items"
```

- v-for可以使用在内置标签template上，将多个元素进行渲染
- 除了数组之外，对象的属性也可以遍历

```
v-for="(value,key,index) in obj"
```

- v-for也可以迭代整数

### 数组更新

- 观察数组变异的方法，会改变原数组：push、pop、shift、unshift、splice、sort、reverse
- 不改变原数组：filter、concat、slice
- VUE在检测到数组变化时，会尽最大可能地复用DOM元素，含有相同元素的项不会被重新渲染
- 通过索引直接设置项，直接修改数组长度，VUE无法检测到变化，并不会触发视图更新

### 过滤与排序

- 可以通过计算属性进行过滤或者排序而不影响原数据

## 方法与事件

### 基本语法

- v-on
- VUE提供$event，用于访问原生DOM事件

### 修饰符

1. stop 阻止事件冒泡
2. prevent 提交事件不重载页面
3. capture 使用事件捕获模式
4. self 只当事件在该元素本身（而不是子元素）触发时回调
5. once 只触发一次

### 键鼠监听

# 表单与v-model

## 基本用法

- VUE提供v-model指令，用于表单类元素上双向绑定
- 使用v-model指令时，在输入阶段，VUE是不会更新数据的，可以使用@input自定义事件实现

### 输入框

- input元素、textarea元素 使用v-model，输入的内容会实时映射到绑定的数据上面

### 单选

- 单独使用时不需要v-model，直接绑定（:checked）一个布尔值即可
- 组合使用实现互斥效果时，需要使用v-model搭配value使用，当v-model绑定值与单选按钮value值一致时，该项被选中

### 复选

- 单独使用时，使用v-model绑定一个布尔值
- 组合使用时，多个选择框绑定到一个数组类型数据上，勾选时value的值会自动push到这个数组里面

### 下拉选择

- 单选，如果option有value，v-model优先匹配value的值，否则直接匹配text的值
- 多选，给<selected>添加multiple属性，此时v-model绑定一个数组

## 绑定值

## v-model的修饰符

1. lazy VUE默认在input事件中同步输入框数据，lazy修饰之后在change事件中同步
2. number 将输入类型转化为整数
3. trim 去掉输入的首尾空格

# 组件

## 组件与复用

- 组件中template中的DOM结构必须被一个元素包含（必须有且只有一个根元素）


- 要在父实例中使用组件，必须在实例创建之前注册

### 全局注册

```
Vue.component('component_name',{})
```

### 局部注册

```
// 实例内部选项
components: {
    
}
```

- 除了template选项之外，组件还可以像VUE实例那样使用其它的选项，如data、computed、methods等。但是data必须是函数，将数据return回去

## 使用props传递参数

### 基本用法

- props的值可以是字符串数组，也可以是对象
- HTML不区分大小写，所以HTML模板中，驼峰原则的props名称要转为短横分隔命名（VUE会自动转换）
- 通过v-bind动态绑定props
- 如果直接传递数字、布尔值、数组、对象而且不使用v-bind，传递的仅仅是字符串

### 单向数据流

> VUE2.x通过props传递的数据是单向的，父组件的数据变化时会传递给子组件，反之不行

- 当props是对象与数组时，在子组件内改变会影响到父组件
- 改变prop的方法
  - 父组件传递初始值进来，子组件将它作为初始值保存起来，在自己的作用域下可以随意使用和修改（使用data）
  - prop作为需要被转换的原始值，使用计算属性

## 组件通信

父子组件间通信、兄弟间通信、跨级组件通信

### 自定义事件

- 观察者模式：\$emit()、\$on()
- v-on在组件上面监听自定义事件外，也可以监听DOM事件，加上native修饰符表示监听原生事件

### 使用v-model

- \$emit()事件名为input，使用v-model绑定的数据

### 中央事件总线

> 可以实现任何组件间的通信

- 创建一个空VUE实例作为事件总线
- 其它实例在mount阶段完成在总线上面的注册

### 父链（不推荐）

- 使用this.$parent可以直接访问父实例或者组件
- 使用this.$children可以直接访问它所有的子组件而且可以递归向上或者向下无线访问

### 子组件索引

- 子组件使用ref属性指定一个索引名称
- 在VUE实例中使用this.$refs.xxx访问子组件

## 使用slot分发内容

> 当需要让组件组合使用，混合父组件的内容与子组件的模板时，就会用到slot，该过程是内容分发（transclusion）

- app组件不知道它的挂载点会有什么内容，挂载内容由app组件的父组件决定
- app组件很可能有它自己的模板

### 作用域

- 父组件与子组件的内容是在各自的作用域内编译的
- slot分发的内容，作用域在父组件上

### slot用法

- 单个slot：在父组件模板中，插入子组件标签内所有内容将替代子组件的slot标签以及它的内容
- 具名slot：给slot元素指定一个name属性之后，可以分发多个内容，具名slot可以与单个匿名slot共存。匿名的slot将作为默认slot出现，如果没有指定默认的匿名slot，父组件多余的内容片段都将被抛弃

### 作用域插槽

- 使用一个可以复用的模板替换已经渲染的元素

### 访问slot

- 通过$slots可以访问某个具名slot

## 高级组件

### 递归组件

- 组件在模板内递归地调用自己，只要给组件设置name属性即可

### 内联模板

- 组件标签使用inline-template属性，组件就会把它的内容作为模板而不是把它当做内容分发
- 在父组件与子组件中声明的数据，都可以被内联模板渲染（子组件优先级高），但是作用域比较难理解，故不推荐使用

### 动态组件

- 使用<component>元素来挂载不同的组件，使用is属性选择要挂载的组件

### 异步组件

- VUE允许将组件定义为一个工厂函数，动态地解析组件

### $nextTick

- 异步更新队列

### X-Templates

- 在<script>元素中书写模板内容，给<script>元素标记id属性，在注册时通过id注册该Script标签即可
- 不推荐使用，因为其将模板与组件的其它定义隔离了

## 监听

- watch选项用来监听某个prop或者data的变化，当它们发生变化，就会触发watch配置的函数

# 自定义指令

## 基本用法

### 全局注册

```
Vue.directive('focus',{
    // options
})
```

### 局部注册

```
new Vue({
    el: '#app',
    directives:{
        foucus:{
            // options
        }
    }
})
```

### 选项

1. bind，指令第一次绑定到元素时调用
2. inserted，被绑定元素插入父节点时调用
3. update，被绑定元素所在的模板更新时调用
4. componentUpdated，元素所在模板完成一次更新周期时调用
5. unbind，指令与元素解绑时调用

# Render函数

# 使用webpack

# 插件

# iView组件

