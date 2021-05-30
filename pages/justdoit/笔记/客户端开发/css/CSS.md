# 字体

## font-size 字体大小

- em，相对于当前对象内文本的字体尺寸
- px，像素
- 互联网常用字体大小为14px+，默认16px

## font-family 字体

- 默认为微软雅黑
- 可以同时指定多个，如果浏览器不支持第一个字体，会依次向下搜索直到匹配为止
- 如果字体有特殊字符或者空格，需要加上引号

## Unicode字体

- font-family编码中文乱码的解决方案

## font-weight 字体粗细

> 字体加粗除了使用b和strong标签之外，还可以使用css实现，但是css是没有语义的

- normal-400（默认）
- bold-700
- bolder
- lighter
- 100~900（100的整数倍）

## font-style 字体风格

> 常常使斜体变得不倾斜而不是使字体倾斜

- normal
- italic 斜体

## font 综合设置

```css
选择器 {font: font-style font-weight font-size font-family}
```

- font-size和font-family为必须的，不可以省略，其它的可以省略取默认值

# 选择器

## 元素选择器（标签选择器）

## 类选择器

- CSS，“.style_name{}”；HTML，


- 命名规范：尽量名字过长的话，使用-而不是_，避免兼容性问题

## 多类名选择器

- class="style1 style2"
- 多个类名先后顺序没有关系，受CSS样式书写的上下顺序有关
- 方向不同

## id选择器

## 通配符选择器

- \* 

## 伪类选择器

### 链接伪类选择器

- :link
- :visited
- :hover
- :active 选定的链接，点击后鼠标未松开的时候
- 尽量按照lvha顺序
- 实际上常用link以及hover，简写

### 结构伪类选择器

- :first-child
- :last-child
- nth-child(n)    n从0开始，但是第一个元素索引为1；even偶数，odd奇数；也可以是公式：如2n，2n+1，3n
- nth-last-child(n)

### 目标伪类选择器

- :target 选取当前活动的目标元素

## 复合选择器

### 交集选择器

- 标签选择器+class选择器

  ```css
  div.className {} //中间没有空格！
  ```

### 并集选择器

- 任何形式的选择器都可以作为并集选择器选择的部分

  ```
  div, p, span, h3, .className, #id {}
  ```

### 后代选择器

- 外层+内层，空格分隔，可选择多代

  ```
  div .className {}
  ```

### 子元素选择器

- 只选择亲儿子

  ```
  父元素 > 子元素 {}
  ```

## 属性选择器

- E[attr] 含有指定属性
- E[attr="val"] 指定属性值相等
- E[attr*="val"] 包含指定属性值
- E[attr^="val"] 以指定属性值开始
- E[attr$="val"] 以指定属性值结尾

## 伪元素选择器

### 语法

- ::first-letter 第一个字


- ::first-line 第一行
- ::selection 文字选中时颜色
- ::before  元素前面
- ::after 元素后面

### 原理

伪元素不是真正的页面元素，HTML没有对应的元素，但是其所有用法和行为与真正的页面元素一致，可以对其使用css样式，表面上看上去貌似是页面的某些元素来展现，实际上是css样式展现的行为，因此被称为伪元素。

- 类选择器、伪类选择器是选取对象，而伪元素选择器是插入了一个行内元素，可以转换为行内元素

- 语法

  ```
  div:hover::before {
      content:"内容";
      display:block;
  }
  ```

# CSS外观属性

## 颜色

- 预定义颜色
- 十六进制颜色（最常用） #红绿蓝；#AAAAAA，#AABBCC格式的可以简写，如#ff6600即#f60
- RGB代码

## line-height 行间距

- 单位：px（常用），em，%
- 一般比字号大7.8px即可
- line-height = 容器height，可以实现垂直居中

## text-align 水平对齐方式

- 属性值：left，right，center

## text-indent 首行缩进

- 单位：建议使用em，1em就是一个汉字的宽度

## letter-spacing 字间距

- 默认为normal

## word-spacing 单词间距

- letter-spacing与word-spacing均可以对英文进行设置，不同的是letter-spacing定义的是字母之间的间距，而word-spacing设置的是单词之间的间距、

## 颜色半透明

- rgba(r,g,b,a)，a为alpha的简写，值为[0,1]，表示透明程度

## 文字阴影 text-shadow

- text-shadow

```css
text-shadow:水平位置 垂直位置 模糊距离 阴影颜色
```

- h-shadow 水平位置，可以看做灯光在目标上方偏左距离
- v-shadow 垂直位置，可以看做灯光在目标上方偏上距离
- blur 模糊距离
- color 阴影颜色


# 样式表

1. 内部样式表
2. 外部样式表
3. 内联样式表

# 标签显示模式

## 块级元素 block

- h、p、div、ul、ol、li
- 特点
  - 总是从新行开始
  - 可以修改高度、宽度（默认为容器的100%）、行高、内外边距
  - 可以容纳内联元素以及其它块元素

## 行内元素 inline

- a、strong、b、em、i、del、s、ins、u、span
- 特点
  - 不占有独立的区域，仅仅靠自身的字体大小和图像尺寸来支撑结构，一般不可以设置宽度高度、对齐等特性，常用于控制页面文本中的样式
  - 和相邻行内元素在同一行
  - 宽（默认宽度为自身内容宽度）高不可以设置
  - 行内元素只能容纳行内元素，但是a标签为特殊情况

## 行内块元素 inline-block

- img、input、td
- 特点
  - 默认宽度为自身内容宽度
  - 和相邻行内块元素在同一行，但是中间有空白
  - 可以修改高度、宽度（默认为容器的100%）、行高、内外边距

## 显示模式转换

- display属性：inline、block

# 背景

## 背景照片

- back-image: url("") 背景图片


- background-color 颜色
- background-repeat 平铺
- background-position 位置；
  - left、right、top、bottom、center；默认left top 左上角；只写一个，另外一个默认为center
  - length，数值|百分比，x y
- background-attachment 固定 fixed /浮动 scroll（默认）
- background-size（img元素通过width、height修改）
  - 设置背景大小（尽量只修改一个，避免缩放导致失真），数值|百分比
  - cover，溢出部分自动隐藏（等比例缩放）
  - contain，自动缩放比例，保证图片完整显示在背景区域
- 组合：color url repeat attachment position

## 背景透明

```
background: rgba(0,0,0,0.5)
```

## 多背景图片

- 使用background组合属性，以逗号分隔

  ```
  background: url("") no-repeat fixed top center,
  url("") no-repeat fixed top center,
  url("") no-repeat fixed top center color;
  //color写在最后
  ```

# CSS特性

## 层叠性

- 样式冲突时，后来居上
- 只覆盖冲突的部分

## 继承性

- text-、font-、line-、color属性可以继承

## 优先级

> 选择器作用范围越小，权重越大

- 继承或者* (0,0,0,0)

- 元素（标签选择器） (0,0,0,1)

- 类、伪类 (0,0,1,0)

- ID (0,1,0,0)

- 行内样式 (1,0,0,0)

- !important ∞无穷大，! 表示 强调

  ```
  div {
      color: red!important;
  }
  ```

- 优先级可以叠加，无进制概念

# 盒子模型

> 边框 border、内边距 padding、内边距 margin

## 边框

- border-width
- border-style none、solid（实线）、dashed（虚线）、dotted（点线）、double（双实线）
- border-color


- border : border-width border-style border-color
- border-top|bottom|left|right-xxx 设置指定边
- border-collapse: collapse; 将表格边框合并在一起（表格中单元格边框重叠会导致边框变粗）

### 圆角

- border-radius: 数值|百分比
- 50%，圆
- 一个值：四个角
- 两个值：左上角&右下角  右上角&左下角
- 三个值：左上角 右下角&左下角 右下角
- 四个值：左上角 右上角 右下角 左下角（顺时针）

## 

## 内边距

> 内容距离边框的距离

- padding-left、right、top、bottom
- 一个值：上下左右
- 两个值：上&下 左&右
- 三个值：上 左&右 下
- 四个值：上 右 下 左（顺时针）

## 外边距

- margin-left、right、top、bottom
- 一个值：上下左右
- 两个值：上&下 左&右
- 三个值：上 左&右 下
- 四个值：上 右 下 左（顺时针）

### 外边距实现居中对齐

- 只对块级元素有效


- margin: 10px auto；

### 清除内外边距

```
padding:0;
margin:0;
```

### 行内元素

- 行内元素只有左右外边距，没有上下外边距
- 行内元素只有左右内边距，上下内边距有怪癖
- 总结：行内元素不要指定上下内外边距

### 外边距合并

- 垂直的相邻块级元素的外边距会发生外边距合并，以大的值为准（解决方法：通过平分外边距回避）
- 嵌套的块级元素外边距会发生外边距合并，导致高度塌陷
- 解决方案
  - 外部块级元素加 上边框，或者 上内边距
  - 外部元素指定：overflow:hidden

## CSS盒模型

- box-sizing
  -  content-box，默认值，传统盒模型
  - border-box，CSS新盒子模型，padding，border不撑开盒子

## 盒子阴影

- box-shadow
  1. h-shadow 水平阴影（必须）
  2. v-shadow 垂直阴影（必须）
  3. blur 模糊距离
  4. spread 阴影尺寸
  5. color 阴影颜色
  6. inset 将外部阴影转化为内部阴影

# 浮动

## 定位机制

### 普通流（标准流）

- 块级元素、行内元素

### 浮动

> 初始主要用于实现文字环绕效果，后面用于实现元素脱离标准流，移动到父元素的指定位置。display:inline-block;元素之间有间隙，不方便处理。

- float:left（默认）、right，只有左右浮动
- 浮动就是漂浮的意思
- 浮动的元素总是找离它最近的父级元素对齐，但是不会超出内边距的范围
- 有浮动属性的元素具有行内块的特性

### 清除浮动

> 实际上是清除浮动带来的影响，父级元素因为子级元素浮动而引起内部高度为0的问题（父级元素一般不设置高度，避免子级元素溢出）
>
> 本质是让父级元素闭合出口与入口

```
选择器{clear:left|right|both} //常用both
```

#### 额外标签法

> 在浮动的盒子后面加上一个空盒子（不常用）

```
<div class="father">
	<div class="son1"></div>
	<div class="son2"></div>
	<div class="clear"></div>
</div>

.clear{
    clear:both;
}
```

#### 父级元素添加overflow属性

```
<div class="father">
	<div class="son1"></div>
	<div class="son2"></div>
</div>

.father{
    overflow:hidden|auto|scroll;
}
```

#### 使用after伪元素清除浮动

```
<div class="father">
	<div class="son1"></div>
	<div class="son2"></div>
</div>

.father:after{
	content:"fix";
	display:block;
	height:0;
	visiability:hidden;
	clear:both;
}
.father{
	*zoom:1;
}
```

#### 使用before与after双伪元素清除浮动

```
<div class="father">
	<div class="son1"></div>
	<div class="son2"></div>
</div>

.father:before{
	content:".";
	display:table;
}
.father:after{
	clear:both;
}
.father{
	*zoom:1;
}
```

### 定位

# 定位

> 边偏移 + 定位模式 = 定位

## 边偏移

- top、bottom、left、right: 数值px;
- 偏移量，定义元素相当于其父元素X边线的距离

## 定位模式

- position:属性值;

  - static，默认，静态定位，边偏移无效
  - relative，相对定位，相当于其原文档流的位置进行定位，参照点为自身左上角。原位置仍然保留，相对定位不脱标
  - absolute，绝对定位，相当于其上一个已经定位的元素进行定位。不占有原来的位置，绝对定位完全脱标。
    - 如果父级元素没有定位，以浏览器为准对齐
    - 如果父级元素已经定位，以父级元素为准对齐
  - fixed，固定定位，相当于浏览器进行定位。IE6以及以下不支持固定点位。脱离标准文档流

- 子绝父相

  - 子级元素是绝对定位的话，父级元素要用相对位置

- 绝对定位居中对齐

  ```
  left:50%;//父级元素的一半
  margin-left:-50px；//宽外边距的一半
  top:50%;
  margin-top:-40px;//高外边距的一半
  ```

## 叠放次序

- z-index: 数值;调整定位元素的层叠等级属性，默认为0，数值越大越高级
- 只有相对定位，绝对定位，，固定定位有此属性
- z坐标轴方向的次序

## 定位模式转换

- 元素添加绝对定位与固定定位之后，元素模式会转换为行内块模式。因此，元素使用绝对定位与固定定位之后，可以不用转换模式，直接给定高度与宽度即可

# 元素的显示与隐藏

- display:none，隐藏之后，不再保留位置（下拉菜单常用）
- visibility:visible|hidden;隐藏之后，保留位置

# 元素溢出处理

- overflow
  - visible 默认，可能发现溢出
  - auto 必要时添加滚动条
  - scroll 一直显示滚动条
  - hidden 溢出隐藏


# CSS高级技巧

> 高级技巧即修改用户界面样式

## 鼠标样式

- cursor
  - default 箭头
  - point 手
  - text 文本（文本）
  - move 移动

## 轮廓线

> 在边框外部的轮廓线

- outline: width type color; 宽度、线类型、颜色
- 一般 outline:0 | none; 取消轮廓线

## 防止拖拽文本域

- resize: none;

## 垂直对齐

- vertical-align，不影响块级元素中的内容对齐，它只针对行内元素或者行内块元素，一般用于控制图片/表单与文字的对齐
  - baseline 默认，基线对齐
  - top
  - middle
  - bottom
- 图片与变淡等行内块元素，其底线与父级元素的基线对齐，导致行内块元素底侧存在一条空白缝隙
  - 解决方案1：转换为块级元素
  - 解决方案2：vertical:top;（常用，推荐）

## 溢出文字换行

- word-break 只对英文有效
  - normal
  - break-all 允许截断单词
  - keep-all 不允许截断单词，连字符除外
- white-space
  - normal
  - nowrap: 强制不换行
- text-overflow，必须使用nowrap+overflow属性一起使用才有效
  - clip 截断舍弃
  - ellipsis 省略号

## CSS精灵技术

> 将一个页面涉及到的零星图像放置到一个图像之内，减少服务器请求次数

- 代码实现

  ```
  spirit {
      width: 17px; //小图的宽度
      height: 18px; //小图的高度
      background: url() no-repeat;
      background-position: 0 -256px;//小图在大图中的位置x y，一般为负数
  }
  ```

## 字体图标

> 与图像效果一致，但是本质上是文字，移动端必备

### 使用步骤

1. UI人员设计字体图标效果图
2. 前端人员上传兼容性字体文件包
3. 前端人员下载兼容字体文件包到本地
4. 把字体文件包引入到HTML页面中

## 滑动门技术

> 利用精灵技术和盒子padding撑开高度以便能适应不同字数的导航栏

```
a {
    display:inline-block;
    height:33px;
    background:url no-repeat;
    padding-left:15px;
}
a span {
     display:inline-block;
    height:33px;
    background:url no-repeat right;
    padding-right:15px;
}

<a href="#">
	<span>首页</span>
</a>
```

# CSS3过渡

## 语法

```
transition: 要过渡的属性 花费时间 运动曲线 何时开始;//多组属性由逗号隔开

transition-property //规定应用过渡的CSS属性名称，一般搭配hover使用

transition-duration //花费时间，默认0，单位s

transition-timing-function //时间曲线，默认ease

transition-delay //过渡效果如何开始，默认0，单位s
```

- 所有属性都变化，可以transition: all transition-duration;

# CSS3 2D变形

## 平移

```
transform: translate(xpx,ypx);
transform: translate(xpx); // 即translateX(xpx);
transform: translate(0,ypx); // 即translateY(ypx);
```

- xpx、ypx不是以父级元素为准，是以自己的宽度为准

### 定位的盒子居中对齐!!!

```
div {
    position:absolute;
    //水平居中
    left:50%;
    transform: translateX(-50%);
    //垂直居中
    top: 50%;
    transform: translateY(-50%);
    //垂直水平居中
    transform: translate(-50%,-50%);
}
```

## 缩放

```
transform:scale(x,y);//scale（x&y）
transform:scaleX(x);
transform:scaleY(y);
小于等于0.99缩小，大于等于1.01放大
```

### 应用场景

1. 照片hover放大，搭配overflow:hidden;

## 旋转

```
transform: rotate(deg);//正值顺时针，负值逆时针
```

### 旋转中心点设置

```
transform-origin:top left;// xpx ypx（坐标精准控制）
```

## 倾斜

```
skew(xdeg,ydeg);
```

# CSS3 3D变形

## Z轴坐标

- 里面为负，屏幕外为正

## 透视

- perspective，视距，一般作为一个属性，设置在父元素，作用于所有3D转换的子元素
- 近大远小，视距越大，透视效果越不明显

## 旋转

```
transform: rotateZ(zdeg);
```

## 平移

```
transform: translateZ(zpx);
// zpx越大，物体越大

translate3d(x,y,z);// z只能是px而不能是%
```

- backface-visibility: hidden（不是正面面对屏幕，就隐藏）

# CSS3 动画

- animation: 动画名称 动画时间 运动曲线 何时开始 播放次数 是否反方向（简写属性）
  1. animation-name，动画名称
  2. animation-duration 花费时间，单位s
  3. animation-timing-function，运动曲线
  4. animation-delay，开始时间
  5. animation-iteration-count，播放次数；infinite无限循环
  6. animation-direction:normal|reserve|alternate往复|alternate-reserve，动画方向
  7. animation-play-state
  8. animation-fill-mode

```
定义动画
@keyframes animation-name {
    from {
        transform:translate(xpx);
    }
    to {
        transform:translate(xpx);
    }
}

定义多帧动画
@keyframes animation-name {
    0% {
        transform:translate(xpx);
    }
    25% {
        transform:translate(xpx);
    }
    50% {
        transform:translate(xpx);
    }
    75% {
        transform:translate(xpx);
    }
    100% {
        transform:translate(xpx);
    }
}
```

- animation-play-state:paused;搭配hover，鼠标经过暂停动画

# 伸缩布局（弹性布局）

## 语法

- 父级元素添加display:flex;
- 子元素flex:n；可以表示宽度（栅格系统）
- 一般搭配min-width使用保护盒子宽度
- 某一个子元素固定宽度，其余盒子瓜分其余的宽度
- flex-direction:column;垂直方向（默认row）
- 调整主轴对齐（水平对齐） justify-content
  - flex-start 默认值，项目位于容器的开头
  - flex-end 项目位于容器的结尾
  - center 项目位于容器中心
  - space-between 空白在容器中间
  - space-around 空白在容器周围（在每个项目的左右两侧）
- 侧轴对齐（垂直对齐）align-items
  - stretch，默认值，项目被拉伸以适应容器（元素需要不设置高度，相当于100%）
  - center，项目位于容器中心
  - flex-start，项目位于容器开头
  - flex-end，位于容器结尾
- flex-wrap 控制换行
  - nowrap 不换行，强制一行内显示
  - wrap 换行
  - wrap-reserve
- flex-content 堆栈对齐（由flex-wrap产生的独立行，多行垂直对齐）
  - 父级元素必须设置display:flex属性，且flex-direction:row;该属性才起作用
  - stretch，默认值，元素被拉伸
  - center
  - flex-start
  - flex-end
  - space-between
  - space-around
- flex-flow: direction wrap;简写属性
- order控制元素排列顺序，默认0；数值越小，越往前。