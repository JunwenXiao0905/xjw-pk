React 18 发布也有很长一段时间了，现在新项目基本都是 React 18 起步。

React 18 最重要的更新就是并发模式（Concurrent Mode）。

这节我们就来过一遍 React 18 的新特性。

## Automatic Batching（自动批处理）

在 React 18 之前，我们知道 setState 是“异步”的（在合成事件和生命周期中），但这其实是因为 React 的批处理机制。

但是，在 Promise、setTimeout 或者原生事件回调里，setState 却是同步的，因为那时候 React 的批处理“失灵”了。

比如这样：

```javascript
setTimeout(() => {
  setCount((c) => c + 1)
  setFlag((f) => !f)
}, 1000)
```

在 React 17 里，这会触发两次渲染。

但在 React 18 里，这就只触发一次渲染了。

这就是 **Automatic Batching**。

不管你在哪里 setState，React 都会尽量帮你合并更新，减少渲染次数，提升性能。

如果你非得想同步渲染，不想要批处理呢？

可以用 `flushSync`：

```javascript
import { flushSync } from 'react-dom'

function handleClick() {
  flushSync(() => {
    setCounter((c) => c + 1)
  })
  // 这里 DOM 已经更新了
  flushSync(() => {
    setFlag((f) => !f)
  })
  // 这里 DOM 又更新了
}
```

不过绝大多数情况我们都不需要它。

## 并发（Concurrency）

什么是并发呢？

简单说，就是“同时”处理多个任务。

但 JS 是单线程的啊，怎么同时处理？

其实就是**可中断渲染**。

以前 React 渲染是同步的，一旦开始，就必须一口气干完。如果组件树很大，计算量很重，主线程就被卡住了，用户的点击、输入就没反应了。

![](https://p1-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/xxx.image)

这就是卡顿的来源。

而 React 18 的并发模式，允许把渲染任务切片，先干一点，看看有没有紧急任务（比如用户输入），如果有就先去处理紧急任务，处理完了回来接着干剩下的。

![](https://p6-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/yyy.image)

这种机制体现在 API 上，就是 `useTransition` 和 `useDeferredValue`。

## useTransition

假设我们有个搜索框，下面是一个列表，列表有 10000 项。

输入框输入的时候，需要过滤列表。

如果直接写，输入会非常卡，因为每次输入都要重新渲染那个巨大的列表。

我们来模拟一下这个场景。

创建个项目：

```bash
npx create-react-app --template typescript react18-test
```

改下 `App.tsx`：

```javascript
import React, { useState } from 'react'

// 模拟一个耗时的列表组件
const List = ({ query }: { query: string }) => {
  const items = []
  for (let i = 0; i < 10000; i++) {
    items.push(
      <div key={i}>
        {query} - {i}
      </div>
    )
  }
  return <div>{items}</div>
}

function App() {
  const [text, setText] = useState('')

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setText(e.target.value)
  }

  return (
    <div>
      <input value={text} onChange={handleChange} />
      <List query={text} />
    </div>
  )
}

export default App
```

跑起来试试：

![](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/zzz.gif)

你会发现打字非常卡，输入一个字符，半天才能显示出来。

为什么？因为 `setText` 触发了重渲染，React 忙着生成那一万个 `div`，没空响应你的打字。

这时候 `useTransition` 就派上用场了。

它可以把更新分为两类：

1.  **紧急更新**：比如打字、点击、拖拽，需要立刻响应。
2.  **过渡更新（Transition）**：比如列表过滤、页面跳转，慢一点也没事。

我们改一下代码：

```javascript
import React, { useState, useTransition } from 'react'

const List = ({ query }: { query: string }) => {
  const items = []
  // 稍微加点料，让它更慢
  const start = performance.now()
  while (performance.now() - start < 10) {} // 强制阻塞 10ms

  for (let i = 0; i < 10000; i++) {
    items.push(
      <div key={i}>
        {query} - {i}
      </div>
    )
  }
  return <div>{items}</div>
}

function App() {
  const [text, setText] = useState('')
  const [query, setQuery] = useState('')
  const [isPending, startTransition] = useTransition()

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    // 紧急更新：输入框的值
    setText(e.target.value)

    // 过渡更新：列表的查询条件
    startTransition(() => {
      setQuery(e.target.value)
    })
  }

  return (
    <div>
      <input value={text} onChange={handleChange} />
      {isPending && <div>Loading...</div>}
      <List query={query} />
    </div>
  )
}

export default App
```

我们把状态拆成了两个：`text` 和 `query`。

`text` 是直接设置的，所以输入框会立马更新。

`query` 是被 `startTransition` 包裹设置的，React 会把它标记为“低优先级”。

如果这时候用户一直在打字，React 就会先处理 `setText`，保证输入框流畅，等空闲了再处理 `setQuery` 渲染列表。

`useTransition` 还会返回一个 `isPending`，告诉你现在是不是正在等待低优先级的更新。

再跑一下：

![](https://p6-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/aaa.gif)

输入如丝般顺滑！虽然列表更新会有延迟，但用户体验好了太多。

## useDeferredValue

`useDeferredValue` 和 `useTransition` 解决的是同一个问题，只是用法不同。

`useTransition` 是用来包装 `setState` 的更新函数的。

但有时候，这个 state 是通过 props 传进来的，你没法控制它的 setter。

这时候就可以用 `useDeferredValue`。

比如上面的例子，如果我们只用一个 state：

```javascript
import React, { useState, useDeferredValue } from 'react'

const List = ({ query }: { query: string }) => {
  // ... 同上
}

function App() {
  const [text, setText] = useState('')
  // 生成一个“延迟”版本的 text
  const deferredText = useDeferredValue(text)

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setText(e.target.value)
  }

  return (
    <div>
      <input value={text} onChange={handleChange} />
      {/* 列表使用延迟后的值 */}
      <List query={deferredText} />
    </div>
  )
}
```

当 `text` 变化时，`deferredText` 不会立马变，React 会尝试用旧值渲染，等紧急任务处理完了，再用新值渲染 `deferredText` 对应的 UI。

效果和 `useTransition` 是一样的。

**总结一下：如果你能控制 setState，就用 useTransition；如果这是个传进来的值，就用 useDeferredValue。**

## useId

这个 Hook 主要是为了解决 SSR（服务端渲染）的时候，ID 不一致的问题。

在 React 18 之前，我们生成唯一 ID 可能会用 `Math.random()` 或者全局计数器。

但是 SSR 会在服务端渲染一次 HTML，然后在客户端再 hydrate（注水）一次。

如果两边生成的 ID 不一样，React 就会报错：`Text content does not match server-rendered HTML`。

`useId` 就是为了生成两端一致的唯一 ID。

```javascript
import { useId } from 'react'

function App() {
  const id = useId()

  return (
    <div>
      <label htmlFor={id}>Name:</label>
      <input id={id} type="text" />
    </div>
  )
}
```

这样生成的 ID 结构是 `:r1:`、`:r2:` 这种，能够保证在组件树中的稳定性。

## 总结

React 18 的核心就是并发。

虽然我们日常开发可能不怎么直接用底层的并发 API，但像 `useTransition` 和 `useDeferredValue` 在处理性能优化的时候非常有用。

它们本质上就是一种**基于优先级的防抖/节流**。

以前我们用 `setTimeout` 或者 `lodash.debounce` 来做防抖，那是由时间控制的，不管电脑卡不卡，时间到了就执行。

而并发特性是由**主线程空闲程度**控制的，电脑快就响应快，电脑卡就让出主线程，这才是最极致的性能优化。
