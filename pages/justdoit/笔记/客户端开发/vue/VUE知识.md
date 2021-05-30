# 模式对比

## MVP

- M Model，模型层
- P Presenter，控制器，大部分在操作DOM
- V View，视图层

## MVVM

- M Model
- VM ViewModel
- V View

# 实例

- 手动创建Vue实例

```
var vm = new Vue({
	// options
})
```

- 组件也是Vue实例

```
Vue.component('my-component',{
    // options
})
```

# 生命周期

- 生命周期函数就是Vue实例在某一个时间点会自动调用的函数，其定义在options中
- 生命周期函数
  - beforeCreate
  - created
  - beforeMount
  - mounted
  - beforeDestroy
  - destroyed
  - beforeUpdate
  - updated

# 模板语法

- 插值表达式与v-text等效，会将HTML转义输出
- v-html对HTML不转义，注意预防XSS

# 计算属性

- 语法

  ```javascript
  computed: {
      fullName: function() {
          return this.firstName + ',' + this.lastName;
      }
  }
  ```


- 插值表达式可以进行简单的数据运算，但是复杂的处理应该放到计算属性之中
- 计算属性有缓存机制，当计算属性依赖的数据没有发生变化时，属性并不会重新计算

## 计算属性的setter与getter

```javascript
computed: {
    fullName: {
        get: function() {
            return this.firstName + ',' + this.lastName;
        },
        set: function(val) {
             var strs = val.split(' ');
             this.lastName = strs[0];
             this.firstName = strs[1];
        }
    }
}
```

# 方法

- 语法

  ```javascript
  methods: {
      fullName: function() {
          return this.firstName + ',' + this.lastName;
      }
  }

  ```

- 没有缓存机制

# 侦听器

- 语法

  ```javascript
  watch: {
      firstName: function() {},
      lastName: function() {}
  }
  ```

- 侦听器在侦听目标改变时，才会触发事件，相当于有和计算属性一样的缓存机制

# 样式绑定

## class对象绑定

```
// isActivated 决定 activated 样式是否应用
<div :class="{activated: isActivated}"></div>
```

## class数组绑定

```
<div :class="[flag]"></div>
{
    data: {
        flag: 'activated'
    }
}
```

## style对象绑定

```
<div :style="styleObject"></div>
{
    data: {
        styleObject: {
            color: 'red',
            fontSize: '16px' // js对象中，不能使用短横分割
        }
    }
}
```

## style数组绑定

```
<div :style="[styleObject]"></div>
```

# 条件渲染

## v-show

- 与display: none;

## v-if

- v-if、v-else-if、v-else

## 关于复用

- Vue会尽量复用元素而不是重复渲染，如果想取消复用，可以给元素赋予唯一的key属性

# 列表渲染

- template元素可以用来包裹一些元素，但是最终不会被渲染出来

## 渲染数组

- 改变数组
  - 改变数组的引用
  - `push()` 、`pop()` 、`shift()`、 `unshift()`、 `splice()`、 `sort()`  、`reverse()`
  - 使用`Vue.set(obj,"key","value")`
  - 使用`vm.$set(obj,"key","value")`

## 渲染对象

- 改变对象属性
  - 改变对象的引用
  - 使用`Vue.set(obj,"key","value")`
  - 使用`vm.$set(obj,"key","value")`

# 组件

## 语法兼容

```
<div id="app">
	<table>
		<ul>
			<tr is="row"></tr>
			<tr is="row"></tr>
			<tr is="row"></tr>
		</ul>
	</table>
</div>

<script>
	Vue.componet('row',{
        template: '<tr><td>it is a row</td></tr>'
	})
	var vm = new Vue({
        el: '#app'
	})
</script>
```

## 组件中data写法

- 为了让组件的data独立不相互影响（组件可能在其它地方多次使用），组件中的data必须定义为一个函数，其返回值是一个对象。

## ref属性

- 根据元素标签的ref属性获取到的是DOM节点
- 根据组件的ref属性，获取到的是对应组件的引用
- 通过`vm.$refs.refValue`访问

## 父子组件数据传递

## 单向数据流

- 父组件可以向子组件传递任何数据，但是子组件不能修改父组件的数据。子组件应该复制一份自己的数据后面使用

  ```html
  <item :count="233"></item>
  <script>
  	Vue.componet('item',{
          props: ['count'],
          template: '<div>{{count}}</div>',
  	    data: function(){
  			return {
  				count: this.count
  			}
  		}
  	})
  	var vm = new Vue({
          el: '#app'
  	})
  </script>
  ```

## 参数校验

```html
<script>
	Vue.componet('item',{
        props: {
            count: {
                type: Number, // [Number,String] 多个类型可以选择
                required: true,
                default: 123,
                validator: function(val) {} // 复杂的自定义校验使用校验器 
            }
        },
        template: '<div>{{count}}</div>',
	    data: function(){
			return {
				count: this.count
			}
		}
	})
	var vm = new Vue({
        el: '#app'
	})
</script>
```

## 非props特性

- props特性
  - DOM不显示
  - 子组件声明，可以在子组件中使用
- 非props特性
  - 会显示在DOM之中
  - 子组件不声明，则无法使用

## 组件绑定原生事件

- 子组件template中绑定的事件为原生事件，在子组件标签上面直接绑定的事件为自定义事件
- 事件传递

```html
<div id="app">
    <child @click="handelClick"></child>
</div>
<script>
	Vue.componet('child',{
        template: '<div @click="handelChildClick">Child</div>',
        methods: {
            handelChildClick: function(){
                this.$emit('click')
            }
        }
	})
	var vm = new Vue({
        el: '#app',
        methods: {
            handelClick: function(){}
        }
	})
</script>
```

- 绑定原生事件（在组件标签加上修饰符native）

```
<div id="app">
    <child @click.native="handelClick"></child>
</div>
<script>
	Vue.componet('child',{
        template: '<div @click="handelChildClick">Child</div>'
	})
	var vm = new Vue({
        el: '#app',
        methods: {
            handelClick: function(){}
        }
	})
</script>
```

## 组件间通信

### VUEX

### 事件总线

> BUS、总线、发布订阅模式、观察者模式

```html
<script>
	Vue.prototype.bus = new Vue();
	
	Vue.componet('child',{
        props: {
            content: String
        },
        data: function() {
            return {
                content: this.content
            }
        }
        template: '<div @click="handelChildClick">{{content}}</div>',
        methods: {
            handelChildClick: function(){
                this.bus.$emit('change',this.content);
            }
        },
        mounted: function(){
            let _this = this;
            this.bus.$on('change', function(val){
                _this.content = val;
            })
        }
	})
	var vm = new Vue({
        el: '#app',
        methods: {
            handelClick: function(){}
        }
	})
</script>

```

## 插槽slot

> 将父级内容为HTML的参数不转义原样输出

1. `v-html`
2. `<slot></slot>`

### 匿名插槽

### 具名插槽

### 作用域插槽

## 动态组件

- 一个元素标签渲染不同的组件，使用`component`占位

```
<component :is="componentType"></component>

Vue.componet('componentType1',{
    template: '<div>componentType1</div>'
})

Vue.componet('componentType2',{
	template: '<div>componentType2</div>'
})
```

## v-once指令

- 只渲染一次

# VUE与CSS动画

## 原理

> VUE通过在动画的不同阶段添加CSS样式实现动画效果

```html
<transition name="fade">
	<div v-if="flag">
        // 在transition中，元素会添加动画效果，CSS中样式为 name-enter
    </div>
</transition>
```

### 元素出现

1. 第一帧 v-enter、v-enter-active
2. 过渡帧 ~~v-enter~~、v-enter-to
3. 最后一帧 ~~v-enter-to~~、~~v-enter-active~~

### 元素隐藏

1. 第一帧 v-leave、v-leave-active
2. 过渡帧 ~~v-leave~~、v-leave-to
3. 最后一帧 ~~v-leave-to~~、~~v-leave-active~~

## animate.css库

### CSS3

```
@keyframes bounce-in {
    0% {}
    50% {}
    100% {}
}
```

### 自定义CSS

- 默认CSS命名`name-enter`，可以自定义`enter-active-class`、`leave-active-class`
  - `enter-active-class`
  - `leave-active-class`
  - `appear-active-class`，第一次出现时的动画效果

```HTML
<style>
    .active {}
</style>

<transition name="fade" enter-active-class="active">
	<div v-if="flag" name="fade"></div>
</transition>
```

### animate库

> 封装了keyframes等CSS

- 必须是自定义CSS的形式

```html
<transition name="fade" enter-active-class="animated swing"
            enter-active-class="animated shake">
	<div v-if="flag" name="fade"></div>
</transition>
```

- 设置动画时长（解决多个动画冲突问题）

```html
<transition :duration="5000"></transition>

// 分别定义入场动画与出场动画
<transition :duration="{enter:5000, leave:10000}"></transition>
```

## 多个元素间过渡

```html
<transition mode="out-in">
	<div v-if="show" key="hello">hello</div>
    <div v-else key="bye">bye</div>
</transition>
```

## 多个组件间过渡

1. v-if 条件渲染
2. 动态组件

## 列表过渡

```html
<transition-group>
	<div v-for="item of list" :key="item.id">
        {{item.title}}
    </div>
</transition-group>
```

# VUE与JS动画

## 动画钩子

> 在methods中声明

1. before-enter
2. enter
3. after-enter
4. before-leave
5. leave
6. after-leave

## velocity.js库

> 动画库

# 动画封装

- 组件

```
Vue。component('fade',{
    props: ['show'],
    template: '<transition><slot v-if="show"></slot></transition>'
})
```

- 封装动画与样式（推荐）

```
Vue。component('fade',{
    props: ['show'],
    template: '<transition @before-enter="handelBeforeEnter"
    	@enter="handelEnter">
    	<slot v-if="show"></slot>
    </transition>',
    methods: {
        handelBeforeEnter : function(el){
            el.style.color = 'red'
        },
        handelEnter: function(el,done){
            // do something
            done();
        }
    }
})
```

