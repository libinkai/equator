# CSRF

## 防御

- 加入验证码
- 验证 Refere
- 使用 Anti CSRF Token
- 加入自定义Header（同上理）

# XSS

## 分类

- 反射型（如将非法脚本注入URL中让受害者点击）
- 储存型
- DOM型（劫持）

## 防御

- 对输入（和URL参数进行过滤），对输入进行编码，Cookie设置http-only