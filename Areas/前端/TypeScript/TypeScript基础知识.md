# TypeScript基础知识

## TypeScript 是什么

- TypeScript 是 JavaScript 的超集
- 它在 JavaScript 的基础上增加了静态类型系统
- TypeScript 最终会编译成 JavaScript 运行

## 为什么使用 TypeScript

- 更早发现类型错误
- 提升代码可读性和可维护性
- 更适合多人协作和大型项目
- 编辑器提示更强，重构更安全

## 后续补充方向

- 基础类型
- 类型推断
- 联合类型与交叉类型
- interface 和 type
- 泛型
- 类型守卫
- any、unknown、never 的区别
- 类型断言
- 函数类型
- 类与继承
- 模块与声明文件

## 类型断言与双重断言

### `as` 是什么

- `as` 是 TypeScript 的类型断言语法
- 它的作用是告诉 TypeScript：先把这个值当成某种类型来看
- 这不会改变运行时的值，只影响编译阶段的类型检查

```ts
const el = document.getElementById("app") as HTMLDivElement;
```

### `as unknown as` 是什么

- `as unknown as Xxx` 叫双重断言
- 第一步先把原值断言为 `unknown`
- 第二步再从 `unknown` 断言为目标类型
- 常用于“原始类型和目标类型差得太远，直接断言会报错”的场景

```ts
const value = something as unknown as TargetType;
```

- `unknown` 可以看作一个中间站
- 这种写法本质上是在绕过更严格的类型检查，所以要谨慎使用

### 示例解释

```ts
(window as unknown as { runBenchmarkTest: typeof runBenchmarkTest }).runBenchmarkTest =
  runBenchmarkTest;
```

可以拆成下面理解：

```ts
type WindowWithBenchmark = {
  runBenchmarkTest: typeof runBenchmarkTest;
};

(window as unknown as WindowWithBenchmark).runBenchmarkTest = runBenchmarkTest;
```

含义是：

- 先把 `window` 视为 `unknown`
- 再把它视为带有 `runBenchmarkTest` 属性的对象
- 然后给这个属性赋值

### 小括号的作用

- 小括号是在给表达式分组
- 这里表示：先完成整个类型断言，再去访问 `.runBenchmarkTest`

也就是：

```ts
(某个表达式).属性
```

如果不加括号，可读性会明显变差，而且编译器也可能把后面的内容和前面的类型部分混在一起理解。

### 使用建议

- 能直接给类型声明补充定义时，优先补类型，不要滥用双重断言
- 给 `window` 挂自定义属性时，更推荐扩展 `Window` 接口
- 双重断言适合临时兼容、迁移代码或第三方类型不完整的场景

### 为什么不能直接写 `window as { ... }`

- TypeScript 不允许随意把一个完全不相干的类型直接断言成另一个类型
- 一般要求两个类型“有一定重叠”，直接断言才更合理
- `Window` 是一个很复杂的内置类型，而 `{ runBenchmarkTest: ... }` 只是一个很小的对象类型
- 因此直接断言时，编译器可能认为这个转换过于可疑

例如：

```ts
window as { runBenchmarkTest: typeof runBenchmarkTest };
```

这类写法的核心问题是：

- 你不是在说“这个值本来就大致长这样”
- 而是在说“我强行把它看成另一个差异很大的类型”

这时就常见两种做法：

```ts
window as any as { runBenchmarkTest: typeof runBenchmarkTest };
```

或者：

```ts
window as unknown as { runBenchmarkTest: typeof runBenchmarkTest };
```

更推荐的方式仍然是补充全局类型：

```ts
declare global {
  interface Window {
    runBenchmarkTest: typeof runBenchmarkTest;
  }
}
```

### `as unknown as` 和 `as any as` 的区别

两者都属于双重断言，但语义和安全性不同。

#### `any`

- `any` 会关闭类型检查
- 对 `any` 做属性访问、调用、赋值，TypeScript 基本都不拦
- 它相当于告诉编译器：这里别管了

```ts
const x = value as any;
x.foo.bar.baz();
```

这种写法即使很危险，也往往不会报错。

#### `unknown`

- `unknown` 表示“我不知道它是什么类型”
- 它比 `any` 更安全
- 你不能直接对 `unknown` 取属性、调用函数，必须先缩小类型或再次断言

```ts
const x = value as unknown;
```

此时下面这些通常不允许直接做：

```ts
x.foo;
x();
```

#### 为什么更推荐 `unknown`

- `unknown` 至少不会在中间阶段完全丢掉类型约束
- 它表达的是“先过渡一下，再明确断言成目标类型”
- `any` 表达的是“这一段我彻底放弃检查”

所以：

- `as any as` 更粗暴
- `as unknown as` 语义上更清楚，也更符合 TypeScript 的设计思路

### `typeof runBenchmarkTest` 为什么能当类型用

- 在 JavaScript 里，`typeof x` 是运行时运算符，返回 `"string"`、`"function"` 这样的字符串
- 在 TypeScript 的类型位置里，`typeof x` 不是取值结果，而是“提取变量 `x` 的类型”

也就是说，TypeScript 里有两种不同语境：

#### 值语境

```ts
console.log(typeof runBenchmarkTest);
```

这里得到的是运行时字符串，比如：

```ts
"function"
```

#### 类型语境

```ts
type Fn = typeof runBenchmarkTest;
```

这里不是字符串，而是：

- 取出 `runBenchmarkTest` 这个函数变量本身的类型
- 然后把它作为一个类型来使用

例如：

```ts
function runBenchmarkTest(name: string): number {
  return name.length;
}

type BenchmarkFn = typeof runBenchmarkTest;
```

这时 `BenchmarkFn` 等价于：

```ts
type BenchmarkFn = (name: string) => number;
```

所以这段代码里：

```ts
{
  runBenchmarkTest: typeof runBenchmarkTest;
}
```

表示的不是：

- `runBenchmarkTest` 这个属性的值是字符串 `"function"`

而是：

- `runBenchmarkTest` 这个属性，必须是和当前 `runBenchmarkTest` 变量同类型的函数

### 一个整体理解

```ts
(window as unknown as { runBenchmarkTest: typeof runBenchmarkTest }).runBenchmarkTest =
  runBenchmarkTest;
```

可以整体读成：

- 我知道 `window` 上将要挂一个 `runBenchmarkTest`
- 这个属性的类型要和当前的 `runBenchmarkTest` 函数保持一致
- 由于默认的 `Window` 类型里没有这个属性，所以临时用双重断言告诉编译器先这样看

## `declare global` 与扩展 `Window`

```ts
declare global {
  interface Window {
    runBenchmarkTest: typeof runBenchmarkTest;
  }
}
```

这段代码的作用是：

- 不是给 `window` 真的新增属性
- 而是告诉 TypeScript：全局的 `Window` 类型上，应该认为存在这个属性

### `declare` 是什么

- `declare` 表示“声明类型信息”
- 它主要影响编译期，不会生成对应的运行时代码
- 可以理解成：告诉 TypeScript 外部世界长什么样

例如：

```ts
declare const VERSION: string;
```

含义是：

- 我告诉 TypeScript 有一个 `VERSION`
- 它的类型是 `string`
- 但这个值可能由别的脚本、构建工具或运行环境提供

### `global` 是什么

- `global` 表示“全局作用域”
- `declare global { ... }` 的意思是：我要给全局已有的类型做补充声明

这里补充的不是某个局部变量，而是整个项目里都可见的全局 `Window` 类型。

### `interface Window { ... }` 是什么

- `Window` 是浏览器里内置的全局类型
- TypeScript 默认已经有一份很大的 `Window` 接口定义
- 这里再次写 `interface Window { ... }`，不是覆盖原来的接口
- 而是和原有定义做声明合并

这叫 declaration merging，也就是声明合并。

合并后的效果相当于：

- 原来 `Window` 上已有的属性还都在
- 现在额外多了一个 `runBenchmarkTest`

### `runBenchmarkTest: typeof runBenchmarkTest` 的含义

- 这表示 `Window` 上的 `runBenchmarkTest` 属性
- 它的类型必须和当前的 `runBenchmarkTest` 函数完全一致

所以后面就可以安全写：

```ts
window.runBenchmarkTest = runBenchmarkTest;
```

### 它和双重断言的区别

双重断言是：

- 在某一行代码里临时骗过编译器

扩展 `Window` 是：

- 从类型层面正式告诉整个项目，这个属性就是存在的

因此通常更推荐扩展 `Window`，因为它：

- 可读性更好
- 复用性更强
- 后续别的文件访问 `window.runBenchmarkTest` 也能拿到正确提示

### 一个完整例子

```ts
function runBenchmarkTest(name: string): number {
  return name.length;
}

declare global {
  interface Window {
    runBenchmarkTest: typeof runBenchmarkTest;
  }
}

window.runBenchmarkTest = runBenchmarkTest;
```

### 一个常见注意点

- `declare global` 常见于模块文件中使用
- 如果文件里没有 `import` 或 `export`，有时会先补一个：

```ts
export {};
```

这样可以明确把当前文件当作模块，再进行全局类型扩展。

### 为什么 `export {}` 能让 `declare global` 更稳定

关键背景是：TypeScript 会把文件分成两类。

#### 脚本文件 script

- 如果一个文件里没有 `import` 或 `export`
- TypeScript 可能把它当成脚本文件
- 脚本文件顶层声明更容易进入全局作用域

#### 模块文件 module

- 如果一个文件里有 `import` 或 `export`
- TypeScript 会把它当成模块文件
- 模块文件顶层声明默认只在当前文件内生效

`export {}` 是一个空导出，它通常不是为了导出内容，而是为了明确告诉 TypeScript：

- 这个文件是模块，不是普通脚本

### 它为什么和 `declare global` 有关系

`declare global` 的语义其实是：

- 当前文件本身是模块
- 但我现在要有意识地给“全局作用域”补充一部分类型

也就是说，它强调的是：

- 平时我是局部模块
- 这里只是显式地扩展全局

因此很多时候会写成：

```ts
export {};

declare global {
  interface Window {
    runBenchmarkTest: typeof runBenchmarkTest;
  }
}
```

这样做的好处是：

- 明确满足全局增强的使用条件
- 避免文件里其他顶层名字意外泄漏到全局
- 让“哪些是局部，哪些是全局增强”边界更清楚

### 如果没有 `export {}` 可能怎样

假设文件里既没有 `import`，也没有 `export`：

```ts
declare global {
  interface Window {
    runBenchmarkTest: typeof runBenchmarkTest;
  }
}
```

在某些配置或上下文下，TypeScript 可能报类似这样的错误：

- 全局作用域增强只能直接嵌套在外部模块或环境模块声明中

本质原因就是：

- 这个文件没有被明确认定为模块
- 于是 `declare global` 的使用环境不够稳定

### 为什么说它“更稳定”

因为 `export {}` 让文件身份变得明确：

- 不依赖“这个文件未来会不会刚好有个 import”
- 不依赖不同工具链对脚本/模块边界的隐式推断
- 不容易因为后续删掉某个 `import` 而让全局增强突然失效

也就是说，`export {}` 不是在“增强功能”。

它是在：

- 固定当前文件的模块身份
- 让 `declare global` 这件事更明确、更稳妥

### 一个推荐写法

```ts
export {};

function runBenchmarkTest(name: string): number {
  return name.length;
}

declare global {
  interface Window {
    runBenchmarkTest: typeof runBenchmarkTest;
  }
}

window.runBenchmarkTest = runBenchmarkTest;
```
