React 19 终于来了！

如果说 React 18 关注的是底层的并发性能，那 React 19 关注的就是**开发体验**。

它的目标很简单：**让你少写代码，少掉坑。**

## React Compiler（React 编译器）

用 React 最烦的是什么？

肯定是 `useMemo`、`useCallback` 和 `memo`。

为了不让子组件无意义渲染，我们得手动给函数包 `useCallback`，给对象包 `useMemo`，给组件包 `memo`。

一旦漏了一个，依赖链断了，优化就全白瞎了。

React 团队也意识到这个问题了，于是推出了 **React Compiler**（之前叫 React Forget）。

它是一个编译器，在构建的时候自动分析你的代码，把该缓存的都缓存了。

也就是说，**以后你再也不用写 useMemo 和 useCallback 了！**

你的代码会变得非常干净：

```javascript
function App() {
  const [count, setCount] = useState(0)

  // 编译器会自动识别这个函数依赖 count，自动缓存它
  const handleClick = () => {
    console.log(count)
  }

  return <Button onClick={handleClick} />
}
```

这绝对是史诗级的减负。

## use Hook

注意，这个 Hook 就叫 `use`。

它的功能非常强大，可以用来读取资源的值，比如 Promise 和 Context。

### 读取 Context

以前我们用 `useContext`，必须在组件顶层调用。

现在可以用 `use`，而且**可以在条件语句和循环里调用**！

```javascript
import { use } from 'react'
import ThemeContext from './ThemeContext'

function App({ showTheme }) {
  if (showTheme) {
    // 以前这样写绝对报错，现在可以了
    const theme = use(ThemeContext)
    return <div style={{ color: theme.color }}>Hello</div>
  }
  return null
}
```

### 读取 Promise

`use` 还可以直接接收一个 Promise。

React 会在这个 Promise resolve 之前挂起（Suspense）组件，等数据好了再渲染。

```javascript
import { use, Suspense } from 'react'

// 一个获取数据的 Promise
const dataPromise = fetch('/api/data').then((res) => res.json())

function DataComponent() {
  // 直接读！像同步代码一样
  const data = use(dataPromise)

  return <div>{data.message}</div>
}

function App() {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <DataComponent />
    </Suspense>
  )
}
```

不需要 `useEffect`，不需要 `useState` 来存数据，直接 `use(promise)`，简直不要太爽。

## Actions（服务端 Action 与表单处理）

在做表单提交的时候，我们通常要写一堆状态：`isPending`、`error`、`data`。

React 19 引入了 Actions 的概念，配合新的 Hook `useActionState`（之前叫 `useFormState`），极大地简化了表单处理。

```javascript
import { useActionState } from 'react'

// 这里的 action 可以是异步函数，甚至可以是 Server Action
async function updateName(prevState, formData) {
  const name = formData.get('name')
  await new Promise((r) => setTimeout(r, 1000)) // 模拟请求
  if (!name) return { error: 'Name is required' }
  return { message: `Updated to ${name}` }
}

function App() {
  const [state, formAction, isPending] = useActionState(updateName, null)

  return (
    <form action={formAction}>
      <input name="name" />
      <button type="submit" disabled={isPending}>
        {isPending ? 'Updating...' : 'Update'}
      </button>
      {state?.error && <p style={{ color: 'red' }}>{state.error}</p>}
      {state?.message && <p style={{ color: 'green' }}>{state.message}</p>}
    </form>
  )
}
```

看到 `<form action={formAction}>` 了吗？

这是 React 对原生 form action 属性的扩展。

`useActionState` 帮你自动管理了 `isPending` 状态和返回值，你只需要关注业务逻辑。

### useFormStatus

还有一个痛点：如果你把 Submit 按钮封装成了子组件，怎么在子组件里知道表单是不是正在提交？

以前得把 `isPending` 通过 props 一层层传下去。

现在有了 `useFormStatus`：

```javascript
import { useFormStatus } from 'react-dom'

function SubmitButton() {
  // 自动感知最近的父 form 的状态
  const { pending } = useFormStatus()

  return <button disabled={pending}>{pending ? 'Submitting...' : 'Submit'}</button>
}
```

不需要传 props，直接用！

## ref 作为 prop

喜大普奔！`forwardRef` 终于要进历史垃圾堆了。

以前要给函数组件传 ref，必须套一层 `forwardRef`：

```javascript
const MyInput = React.forwardRef((props, ref) => {
  return <input ref={ref} {...props} />
})
```

在 React 19 里，`ref` 变成了普通的 prop：

```javascript
function MyInput({ ref, ...props }) {
  return <input ref={ref} {...props} />
}
```

就这么简单。

## Document Metadata（文档元数据）

以前我们要修改 `<title>` 或者 `<meta>` 标签，通常要用 `react-helmet` 这种库。

React 19 原生支持了：

```javascript
function BlogPost({ post }) {
  return (
    <article>
      <title>{post.title}</title>
      <meta name="description" content={post.summary} />
      <h1>{post.title}</h1>
      <p>{post.content}</p>
    </article>
  )
}
```

React 会自动把这些标签提升到 `<head>` 里，并且保证去重。

## useOptimistic

乐观更新（Optimistic UI）是指：用户操作后，不等待服务器响应，直接在界面上显示成功的结果。如果失败了再回滚。

比如点赞，点了立马变红，不用等请求返回。

React 19 给了个 Hook `useOptimistic` 专门干这事：

````javascript
import { useOptimistic } from 'react';

function LikeButton({ likeCount, onClick }) {
  // optimisticCount 是乐观值，每次 addOptimistic 被调用时更新
  const [optimisticCount, addOptimistic] = useOptimistic(
    likeCount,
    (state, amount) => state + amount
  );

  const handleClick = async () => {
    addOptimistic(1); // 立即更新 UI 为 +1
    await onClick();  // 发送真实请求
  };

  return (
    <button onClick={handleClick}>
      Likes: {optimisticCount}
    </button>
  );
}

### 为什么要用它？区别在哪里？

你可能会问：**“我直接用 useState 也可以做乐观更新啊，为什么要用 useOptimistic？”**

区别主要有两点：**自动回滚** 和 **数据源单一**。

如果用 `useState` 手写，你得这样搞：

````javascript
function LikeButton({ likeCount, onClick }) {
  const [count, setCount] = useState(likeCount);

  const handleClick = async () => {
    const prev = count;
    setCount(prev + 1); // 1. 手动设置乐观值
    try {
      await onClick(); // 2. 发送请求
    } catch (e) {
      setCount(prev); // 3. 失败了必须手动回滚！容易忘！
    }
  };

  // 4. 还有一个坑：如果父组件传下来的 likeCount 变了（比如别人点赞了），
  // 你还得写 useEffect 来同步 props 到 state，非常麻烦。
  useEffect(() => {
     setCount(likeCount);
  }, [likeCount]);

  return <button onClick={handleClick}>{count}</button>;
}
````

而 `useOptimistic` 的逻辑是：

1.  **临时性**：它产生的状态是“临时”的。一旦异步操作（Action）结束，这个乐观状态就自动销毁了，React 会自动回退到使用 `props.likeCount`。
2.  **自动回滚**：因为它是临时的，所以如果请求失败（Action 结束），UI 会自动“变回” `likeCount` 的值，你不需要写 `try...catch` 去手动回滚。
3.  **单一数据源**：它始终依赖 props 传进来的 `likeCount`。如果请求成功，父组件更新了 `likeCount`，`useOptimistic` 就直接用新的；如果请求还没结束，父组件更新了 `likeCount`，它会在新的 `likeCount` 基础上继续 +1。

简单说，它帮你省去了**同步 props** 和 **错误回滚** 的逻辑。

```

## 总结

React 19 是一次非常务实的更新。

它没有引入太多的新概念（像 Concurrent Mode 那么抽象），而是实打实地解决我们在开发中遇到的痛点：

*   **React Compiler**：消灭 `useMemo` / `useCallback`。
*   **use Hook**：简化 Context 和 Promise 的读取。
*   **Actions**：简化表单和数据提交。
*   **ref as prop**：消灭 `forwardRef`。
*   **useOptimistic**：简化乐观更新。

可以预见，React 19 普及后，我们的代码量会通过“减法”变得更少、更清晰。

这大概就是 React 团队给我们的最好的礼物吧。
```
