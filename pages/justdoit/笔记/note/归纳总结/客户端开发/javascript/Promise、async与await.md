# Promise

- 在JavaScript的世界中，所有代码都是单线程执行的，这导致JavaScript的所有网络操作，浏览器事件，都必须是异步执行

- 异步执行可以用回调函数实现，一般是利用`setTimeout`函数

- 承诺将来会执行某函数的对象在JavaScript中称为Promise对象

  ```javascript
  new Promise(function (resolve, reject) {
      log('start new Promise...');
      var timeOut = Math.random() * 2;
      log('set timeout to: ' + timeOut + ' seconds.');
      setTimeout(function () {
          if (timeOut < 1) {
              log('call resolve()...');
              resolve('200 OK');
          }
          else {
              log('call reject()...');
              reject('timeout in ' + timeOut + ' seconds.');
          }
      }, timeOut * 1000);
  }).then(function (r) {
      log('Done: ' + r);
  }).catch(function (reason) {
      log('Failed: ' + reason);
  });
  
  // Promise接受一个函数参数（假设为A），函数A接受两个参数，一个是resolve函数，一个是reject函数。当在函数A中执行resolve时，Promise将会执行then函数。当在函数A中执行reject时，Promise会执行catch函数。then函数的参数为resolve函数的参数，catch函数的参数为reject函数的参数
  ```

- Promise对象可以链式调用

## Promise的“与运算”与“或运算”

```js
var p1 = new Promise(function (resolve, reject) {
    setTimeout(resolve, 500, 'P1');
});
var p2 = new Promise(function (resolve, reject) {
    setTimeout(resolve, 600, 'P2');
});
```

- all

```javascript
// 同时执行p1和p2，并在它们都完成后执行then:
Promise.all([p1, p2]).then(function (results) {
    console.log(results); // 获得一个Array: ['P1', 'P2']
});
```

- race

```javascript
Promise.race([p1, p2]).then(function (result) {
    console.log(result); // 'P1'
});
```

- 组合使用Promise，可以把很多异步任务以并行和串行的方式组合起来执行

# async与await

- JavaScript的async/await实现，离不开Promise
- async 是asynchronous的简写，而 await 可以认为是 async wait 的简写
- async 用于声明一个 function 是异步的，而 await 用于等待一个异步方法执行完成
- `await 只能出现在 async 函数中`
- async 函数（包含函数语句、函数表达式、Lambda表达式）会返回一个 Promise 对象，如果在函数中 `return` 一个直接量，async 会把这个直接量通过 `Promise.resolve()` 封装成 Promise 对象
- Promise 的特点是无等待，所以在没有 `await` 的情况下执行 async 函数，它会立即执行，返回一个 Promise 对象，并且，绝不会阻塞后面的语句。这和普通返回 Promise 对象的函数并无二致
- await 等待的是一个表达式，这个表达式的计算结果是 Promise 对象或者其它值（换句话说，就是没有特殊限定），所以await 后面实际上是可以接普通函数调用或者直接量的
- 如果await等到的不是一个Promise对象，那await表达式的运算结果就是它等到的东西。如果它等到的是一个 Promise 对象，它会阻塞后面的代码（async 函数调用不会造成阻塞，它内部所有的阻塞都被封装在一个 Promise 对象中异步执行），等着 Promise 对象 resolve，然后得到 resolve 的值，作为 await 表达式的运算结果
- 单一的 Promise 链并不能发现 async/await 的优势，但是，如果需要处理由多个 Promise 组成的 then 链的时候，优势就能体现出来了（Promise 通过 then 链来解决多层回调的问题，现在又用 async/await 来进一步优化它）