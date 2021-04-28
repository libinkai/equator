# 概念

- 一门跨平台、具有静态类型与面向对象编程的语言，是JS的超集

# 环境

```shell
// 全局安装
npm install typescript -g
// 查看版本
tsc --version
// 创建配置文件
tsc --init
// 解决模块的声明文件问题
npm install @types/node --dev-save
// Ts 转 Js
tsc
// node 运行 js
node xxx.js
```

# 类型

## umber

## string

```typescript
// 基本类型
let a:string = 'aaa'
// 引用类型
let b:String = new String('abc')
// 模版字符串，可以定义多行文本和内嵌表达式。 这种字符串是被反引号包围（ `），并且以${ expr }这种形式嵌入表达式
```

## boolean

## enum 枚举

## any 任意类型，不推荐使用

## void

## Undefined、Null

## Array

```typescript
// 基础类型：字面量赋值
let arr1:number[] = [1,2,3]
// 泛型数组
let arr2:Array<String>
```

## Tuple

- 元组类型允许表示一个已知元素数量和类型的数组，各元素的类型不必相同

## 高级类型

# 函数

## 参数

- 普通的函数

  ```
  function xxx(para1:type1):type0{}
  ```

- 带可选参数的函数

  ```
  function xxx(para1:type1,para2:?type2):type0{}
  ```

- 带默认参数的函数

  ```
  function xxx(para1:type1,para2:type2=defaultValue):type0{}
  ```

- 带可变长参数的函数（剩余参数）

  ```
  function xxx(...para1:type1[]):type0{}
  ```

## 定义

- 函数声明法

  ```typescript
  function add(n1:number,n2:number):number{
  	return n1+n2;
  }
  add(1,2)
  ```

- 函数表达式

  ```typescript
  var add = function(n1:number,n2:number):number{
  	return n1+n2;
  }
  add(1,2)
  ```

- 箭头函数

  ```
  var add = (n1:number,n2:number):number=>{
  	return n1+n2;
  }
  ```

## 函数中变量的作用域

- 变量的作用域按照函数中划分

- 全局变量：函数之外定义的变量；局部变量：函数中定义的变量

- 局部作用域中冲突的变量会将外部变量覆盖

- 变量提升

  ```
  function func(){
  	console.log(xxx); // undefined
  	var xxx = 'abc';
  	console.log(xxx); // abc
  }
  // 实际上
  function func(){
  	var xxx;
  	console.log(xxx); // undefined
  	xxx = 'abc';
  	console.log(xxx); // abc
  }
  ```

- let关键字，块级作用域：一个坑：Ts会自动将ES6的let转换为var

# 接口

## 规范变量

- 类型检查器会查看`printLabel`的调用。 `printLabel`有一个参数，并要求这个对象参数有一个名为`label`类型为`string`的属性

  ```
  function printLabel(labelledObj: { label: string }) {
    console.log(labelledObj.label);
  }
  
  let myObj = { size: 10, label: "Size 10 Object" };
  printLabel(myObj);
  ```

- 类型检查器不会去检查属性的顺序，只要相应的属性存在并且类型也是对的就可以
- 带有可选属性的接口与普通的接口定义差不多，只是在可选属性名字定义的后面加一个`?`符号

## 函数接口

## 接口的实现

# 类

## 定义

```typescript
class Greeter {
    greeting: string;
    constructor(message: string) {
        this.greeting = message;
    }
    greet() {
        return "Hello, " + this.greeting;
    }
}

let greeter = new Greeter("world");
greeter.greet();
```

## 继承

- `extends`关键字
- 单继承
- 派生类的构造函数，必须调用 `super()`，它会执行基类的构造函数。 而且，在构造函数里访问 `this`的属性之前，我们 *一定*要调用 `super()`。 这个是TypeScript强制执行的一条重要规则

## 属性封装

- 默认为`public`
- `private`私有，不能在声明它的类的外部访问
- `protected`保护，与 `private`修饰符的行为很相似，但有一点不同， `protected`成员在派生类中仍然可以访问
- 构造函数也可以被标记成 `protected`。 这意味着这个类不能在包含它的类外被实例化，但是能被继承
- `readonly`关键字将属性设置为只读的。 只读属性必须在声明时或构造函数里被初始化

## 存取器

```
class Employee {
    private _fullName: string;

    get fullName(): string {
        return this._fullName;
    }

    set fullName(newName: string) {
        if (passcode && passcode == "secret passcode") {
            this._fullName = newName;
        }
        else {
            console.log("Error: Unauthorized update of employee!");
        }
    }
}
```

- 存取器要求你将编译器设置为输出ECMAScript 5或更高。 不支持降级到ECMAScript 3
- 只带有 `get`不带有 `set`的存取器自动被推断为 `readonly`

## 静态属性

- `static`

## 抽象类

- 抽象方法与普通方法可以共存

  ```
  abstract class Animal {
      abstract makeSound(): void;
      move(): void {
          console.log('roaming the earch...');
      }
  }
  ```

- 

# 泛型

# 模板

# 命名空间

# 