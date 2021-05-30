# 命令行CLI

## VUE开发环境

1. `npm install --global vue-cli`
2. `vue init webpack project-name`
3. `cd project-name`
4. `pip install`
5. `npm run dev`

## 安装fastclick库

- `npm install fastclick --save`
- save表示生产环境与开发环境都使用

# 项目结构

- build webpack配置
- config
  - index.js 基础
  - dev.env.js 开发环境
  - prod.env.js 生产环境
- node_modules 依赖包
- src
  - assets 资源
  - components 组件
  - router 路由
  - App.vue 入口
  - main.js
- static 只有该文件夹下的资源可以被外部直接访问
- .babelrc 将单文件转换为浏览器可编译语法
- .editorconfig 编辑器配置
- .eslintignore 代码检测忽略文件
- eslintrc.js 代码语法规范
- .gitignore git忽略文件
- .postcssrc.js
- index.html 首页
- LICENSE
- package.json 
- package-lock.json 依赖说明
- readme.md 说明文件

# VUE路由

## 单文件组件

- `xxx.vue`

  ```html
  <template></template>

  <script></script>

  <style></style>
  ```

## 路由

- 路由映射在`/router/index.js`中配置


- 在`main.js`中options中配置router，与data同级
- `<router-view></router-view>` 显示的是当前路由对应的内容
- @代表`src`目录

# 多页面VS单页面

##多页面

> 页面跳转->返回HTML

### 优点

1. 首屏时间快
2. SEO效果好

### 缺点

1. 页面切换慢

## 单页面

> 页面跳转->JS渲染

### 优点

1. 页面切换快

### 缺点

2. 首屏时间慢
3. SEO效果差


# Git开发

- 一般不在主分支master上开发

- 开发一个新功能的步骤

  1. 在线上创建一个新分支`branch-name`

  2. `git pull`

  3. `git checkout branch-name`

  4. 开发完毕之后

     ```
     git add .
     git commit -m
     git push
     ```

  5. 线下合并分支`git merge branch-name`、`git push`

  6. 也可以对master设置分支保护，在线上review代码之后，再合并分支

# 部署

- `npm run build`打包编译

# 常用第三方包

