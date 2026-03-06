# 第 89 章—Vue3 与 React 核心机制对比

之前我们一直在深入 React 的世界，探讨了 Hooks、闭包陷阱、并发模式等等。

很多同学可能同时也在用 Vue，或者从 Vue 转过来的。

在写 React 的时候，总会有一种感觉：**“为什么 React 这么麻烦？依赖要自己填，闭包陷阱要自己防，性能优化（memo）要自己做？”**

反观 Vue3，定义一个 `ref`，改了它，界面就变了，哪有那么多事？

这背后其实是两者核心设计理念和实现机制的巨大差异。

这节我们就来深度对比一下 Vue3 和 React 的核心机制。

## 核心差异一：数据驱动的实现原理

### Vue3：响应式系统（Reactivity）

Vue3 的核心是**响应式系统**，基于 ES6 的 `Proxy`。

它的逻辑是：**“如果你变了，请告诉我。”**

1.  **依赖收集**：当组件渲染时，访问了某个响应式数据（Proxy），Vue 会把这个组件（或者说渲染副作用）记录下来，作为该数据的依赖。
2.  **派发更新**：当你修改数据时（Setter），Vue 会通知所有订阅了该数据的组件进行更新。

这种机制被称为**细粒度更新**。Vue 甚至可以精确知道是哪个组件的哪个 DOM 节点依赖了这个数据。

### React：快照（Snapshot）与重渲染

React 的核心是**不可变性（Immutability）**和**全量重执行**。

它**不使用 Proxy**，也不进行数据劫持。

它的逻辑是：**“不管谁变了，我重新跑一遍，看看哪里变了。”**

1.  **显式触发**：当你调用 `setState`（或 `dispatch`）时，你告诉 React：“状态变了，安排一次更新。”React 并不监听数据变化，而是等待你的通知。
2.  **重执行**：React 会**重新执行整个组件函数**。
3.  **Diff**：React 拿到新的 Virtual DOM，和旧的进行对比（Diff），找出差异，然后更新 DOM。

这就是为什么 React 需要 `memo`、`useMemo`、`useCallback`。因为如果不加控制，父组件一更新，所有子组件函数都会重新执行一遍。

## 核心差异二：组件函数的执行

这是最容易让 Vue 开发者困惑的地方。

### Vue3：Setup 只运行一次

在 Vue3 的 Composition API 中，`setup` 函数（或者 `<script setup>`）**只在组件创建时执行一次**。

```javascript
// Vue3
<script setup>
  import {ref} from 'vue' // 这行代码只跑一次 const count = ref(0) const increment = () =>{' '}
  {
    // 修改的是同一个对象的值
    count.value++
  }
</script>
```

因为只跑一次，所以定义的函数、变量都只有一份。闭包陷阱？不存在的，因为引用一直没变（或者说一直在同一个闭包里）。

### React：每次渲染都重新运行

在 React 中，**组件函数在每次渲染时都会重新执行**。

```javascript
// React
function App() {
  // 每次渲染，这行代码都会执行
  // 每次都创建了一个新的 count 变量
  const [count, setCount] = useState(0)

  const increment = () => {
    setCount(count + 1)
  }
}
```

- **第一次渲染**：`count` 是 0。
- **第二次渲染**：App 函数再次执行，`useState` 返回新的 `count` 是 1。注意，这个 1 是一个新的变量，不是原来的那个 0 变过来的。

这就是我们之前说的**“快照”**概念。

这也解释了为什么 React 会有闭包陷阱。如果你在一个定时器里引用了 `count`，而这个定时器是在第一次渲染定义的，那它引用的永远是第一次那个值为 0 的 `count`。

## 核心差异三：依赖管理的哲学

### Vue3：自动挡

由于 Vue3 有细粒度的响应式系统，它**自动知道**组件依赖了哪些数据。

- `computed` 自动收集依赖。
- `watch` 自动收集依赖（也可以手动指定）。
- 组件渲染函数自动收集依赖。

开发者几乎不需要关心依赖数组。

### React：手动挡

React 因为每次都重新执行函数，它没办法自动判断这个副作用（Effect）是不是需要重新执行，除非你明确告诉它。

所以 React 引入了**依赖数组（Dependency Array）**。

```javascript
useEffect(() => {
  console.log(count)
}, [count]) // 你必须告诉 React：这个 Effect 依赖 count
```

- 如果你不写 `[count]`，React 就认为这个 Effect 不依赖任何东西（只在挂载时跑一次），然后就掉进闭包陷阱了。
- 如果你乱写依赖，可能会导致无限循环或者逻辑错误。

这给了开发者极大的控制权，但也带来了极大的心智负担。React 团队正在开发的 **React Compiler (React Forget)** 就是为了解决这个问题，试图实现“自动挡”。

## 核心差异四：Concurrent Mode（并发模式）

这是 React 架构中最复杂也是最强大的部分。

由于 React 每次更新都要重新执行组件函数并进行 Diff，如果组件树很大，计算量就会很大，导致主线程阻塞，页面卡顿。

Vue 因为是细粒度更新，组件级更新，一般不需要 Diff 整棵树，性能通常默认就很好。

为了解决这个问题，React 引入了 **Fiber** 架构和 **Concurrent Mode**。

React 把更新过程拆分成一个个小的**任务单元（Fiber）**。它可以：

1.  **暂停**渲染，先去处理高优先级的任务（比如用户点击）。
2.  **废弃**渲染，如果状态又变了，之前的计算作废，重新来。
3.  **恢复**渲染。

这让 React 在处理复杂应用时，能保持界面的响应性（Time Slicing）。

Vue3 虽然没有 Time Slicing，但由于其更新粒度细，静态编译优化做得好（Block Tree, Patch Flags），在大多数场景下性能依然非常强悍。

## 总结

打个比方：

**Vue3 就像是一个精密的 Excel 表格。**
你把公式设好（响应式连接），改了一个单元格（数据），Excel 自动知道哪些相关的单元格需要更新，其他的动都不动。

**React 就像是一个每秒刷新 60 次的游戏引擎。**
数据变了？好，我重新画一帧画面（Virtual DOM），然后跟上一帧对比，把不一样的地方贴到屏幕上。为了不卡顿，我有超级复杂的调度系统（Fiber）来决定先画哪里。

- **Vue3**：

  - **优势**：上手简单，符合直觉，自动优化，性能下限高。
  - **心智模型**：可变数据（Mutable），响应式。

- **React**：
  - **优势**：JS 原生能力强，灵活性极高，生态繁荣，适合超大型应用（得益于并发模式）。
  - **心智模型**：不可变数据（Immutable），快照，函数式编程。

用一句话总结两者的“魔法”：

- **Vue3 的魔法**在于 `Proxy` 代理的 `set` 方法中自动触发重新渲染。
- **React 的魔法**在于 `setState` 的内部逻辑中，通知整个 React 重新执行组件函数并对比 DOM 进行重新渲染。

理解了这些区别，你就明白了为什么 React 需要 `useRef`，为什么会有闭包陷阱，以及为什么 `useEffect` 的依赖数组那么重要。

## 核心差异五：生命周期 vs 副作用 (Lifecycle vs Effect)

这也是很多 Vue 转 React 的开发者容易混淆的点：`useEffect(() => {}, [])` 等价于 `onMounted` 吗？

### 1. 心智模型的差异

- **Vue (Lifecycle)**：Vue 的 `onMounted` 是明确的**生命周期钩子**。它的语义是：“**在组件挂载完成后，执行这个操作**”。它关注的是**“时间点”**。
- **React (Synchronization)**：React 没有生命周期的概念（Hooks 时代），只有**副作用同步**。`useEffect` 的语义是：“**将这个副作用与组件状态同步**”。当你传入空数组 `[]`，意思是“**这个副作用不依赖任何数据流，所以只需要同步一次**”。它关注的是**“依赖关系”**。

### 2. 开发模式下的执行次数 (Strict Mode)

这是一个非常明显的区别。

- **Vue**：`onMounted` 在组件初始化时**只执行一次**。
- **React**：在 React 18 的**严格模式（Strict Mode）**开发环境下，为了帮你检查副作用的清理逻辑是否正确，React 会强制执行：**Mount -> Unmount -> Mount** 的流程。
  - 这意味着你的 `useEffect` 会被**执行两次**！
  - 这就是为什么 React 强调副作用必须要是**可清理的（Cleanable）**。

### 3. 清理机制

- **Vue**：你需要单独使用 `onUnmounted` 来处理清理逻辑。
- **React**：`useEffect` 的**返回值**就是清理函数。

```javascript
// React: 聚合在一起
useEffect(() => {
  const timer = setInterval(...)
  return () => clearInterval(timer) // 清理逻辑
}, [])

// Vue: 分散在两个钩子
const timer = ref(null)
onMounted(() => {
  timer.value = setInterval(...)
})
onUnmounted(() => {
  clearInterval(timer.value)
})
```

## 核心差异六：Update 阶段与 Watch

你问到：“`useState` 触发重新渲染，会导致 `useEffect` 执行吗？这算 Vue3 的 Update 阶段吗？”

这是一个非常好的问题，触及了 React 和 Vue 在“更新响应”上的根本区别。

### 1. useState 一定会触发 useEffect 吗？

**不一定。** 这完全取决于 `useEffect` 的**依赖数组**。

React 的逻辑是：**“渲染完成了，我看看哪些 Effect 需要执行。”**

- **情况 A：依赖数组为空 `[]`**

  - `useEffect(() => {}, [])`
  - **行为**：只在组件挂载（Mount）后执行一次。
  - **结果**：`useState` 触发重渲染时，**它不会执行**。
  - **类比 Vue**：`onMounted`。

- **情况 B：没有依赖数组**

  - `useEffect(() => {})`
  - **行为**：每次组件渲染（Mount + Update）完都会执行。
  - **结果**：`useState` 触发重渲染时，**它一定会执行**。
  - **类比 Vue**：`onMounted` + `onUpdated`。

- **情况 C：有依赖数组 `[count]`**
  - `useEffect(() => {}, [count])`
  - **行为**：只有当 `count` 发生变化时才执行。
  - **结果**：如果是 `setCount` 改了 `count`，**它会执行**；如果是 `setName` 改了 `name`（且 `name` 不在数组里），**它不会执行**。
  - **类比 Vue**：`watch(count, ..., { immediate: true })`。

### 2. 这算 Vue3 的 Update 阶段吗？

**概念上相似，但用途不同。**

- **Vue 的 `onUpdated`**：

  - 是一个纯粹的生命周期钩子。
  - 它表示“DOM 已经根据最新的响应式数据更新完毕了”。
  - 通常用于“每次更新后都需要操作 DOM”的场景，**很少用于处理数据逻辑**。
  - 如果你想监听数据变化执行逻辑，Vue 推荐用 `watch`。

- **React 的 `useEffect`**：
  - 它**身兼数职**。它既是 `onMounted`，又是 `onUpdated`，还是 `watch`。
  - 当你写 `useEffect(() => {})`（无依赖）时，它确实对应 Vue 的 `onUpdated` 阶段。
  - 但大多数时候，我们给它加依赖数组，这时候它更像 Vue 的 `watch`。

### 总结对照表

| 场景               | React 写法                            | Vue3 写法                              | 备注                                         |
| :----------------- | :------------------------------------ | :------------------------------------- | :------------------------------------------- |
| **只在初始化执行** | `useEffect(fn, [])`                   | `onMounted(fn)`                        | 最常用                                       |
| **每次渲染都执行** | `useEffect(fn)`                       | `onUpdated(fn)`                        | 需注意性能，React 中需配合 useRef 避免死循环 |
| **数据变了才执行** | `useEffect(fn, [data])`               | `watch(data, fn, { immediate: true })` | React 默认含 immediate 效果                  |
| **组件销毁时执行** | `useEffect(() => return cleanup, [])` | `onUnmounted(cleanup)`                 | React 将 setup 和 cleanup 聚合               |

## 核心差异七：Hooks 的“穿透”与“缓存”机制

你可能会疑惑：**“既然 React 组件函数每次都重新执行，那 `useState`、`useCallback` 这些 Hook 不也重新执行了吗？为什么它们能保持状态或者缓存？”**

没错，**Hook 函数本身确实每次都执行了**。

但是，React 在内部维持了一张链表（Fiber Node 上的 `memoizedState`），用来存储这些 Hook 的状态。

### 1. 真正的“有选择执行”

当我们说“有选择的重新执行”时，其实是指 Hook **内部逻辑**的有选择执行。

```javascript
function App() {
  // 1. useState
  // 每次 App 执行，这行代码都跑。
  // 但 React 内部会判断：这是 Update 阶段，我要忽略初始值 0，
  // 去链表里把当前的 state 拿出来给你。
  const [count, setCount] = useState(0)

  // 2. useCallback
  // 每次 App 执行，这行代码都跑。
  // React 内部会对比依赖数组 []。
  // 发现没变 -> 返回链表里存的那个旧函数引用。
  // 发现变了 -> 存下新函数，返回新函数引用。
  const handleClick = useCallback(() => {
    console.log('click')
  }, [])

  // 3. 普通函数
  // 每次 App 执行，这行代码都跑。
  // JS 引擎每次都会创建一个全新的函数对象。
  const handleHover = () => {}

  // 4. useEffect
  // 每次 App 执行，这行代码都跑。
  // React 内部对比依赖数组。
  // 没变 -> 不做任何标记。
  // 变了 -> 打个 tag，等 DOM 更新完（Commit 阶段）后，去执行回调。
  useEffect(() => {
    console.log('effect')
  }, [count])

  return <div onClick={handleClick}>...</div>
}
```

### 2. 为什么需要 useCallback/useMemo？

在 Vue3 中，`setup` 只跑一次，所以函数定义的开销只有一次。

```javascript
// Vue3
const handleClick = () => {} // 永远是同一个引用
```

在 React 中，因为组件函数多次执行，导致内部定义的函数每次都是**新的引用**。

```javascript
// React
const handleClick = () => {} // 每次渲染都是新的内存地址
```

如果把这个 `handleClick` 传给子组件：

1.  **没有 memo 的子组件**：不管 `handleClick` 变没变，子组件都会跟着父组件重渲染（默认行为）。
2.  **有 memo 的子组件** (`React.memo(Child)`)：子组件会对比 props。因为 `handleClick` 引用变了，子组件认为 props 变了，于是**被迫**重渲染。

这时候就需要 `useCallback` 了：它能保证只要依赖没变，返回的函数引用就不变，从而让子组件的 `React.memo` 生效，避免不必要的渲染。

### 总结

- **React 的组件函数**：是**全量执行**的（每一行代码都会跑）。
- - **React 的 Hooks**：是**有记忆**的（通过链表和依赖对比，决定是返回旧值还是新值，是忽略 Effect 还是调度 Effect）。

## 核心差异八：计算属性 (Computed) vs useMemo

你问：“那 React 中是不是就不需要计算属性？反正都会重新计算？”

**你答对了一半。**

### 1. 简单计算：直接写

在 Vue 中，我们习惯把所有派生数据都写成 `computed`：

```javascript
// Vue
const double = computed(() => count.value * 2)
```

在 React 中，对于简单的计算，我们**直接写在函数体里**：

```javascript
// React
const double = count * 2 // 每次渲染都算一遍，但在 JS 里这快得可以忽略不计
```

因为 React 组件函数每次都执行，所以 `double` 自然会得到最新的值。对于这种 O(1) 或者轻量的计算，React 的哲学是：**不要过度优化**。直接算比创建 `useMemo` 的开销（创建对象、对比依赖数组）还要小。

### 2. 昂贵计算：useMemo

但是，如果你的计算非常耗时（比如遍历一个 10000 条数据的数组进行过滤），或者你需要保证引用稳定性（为了传给子组件），那就必须用 `useMemo` 了。

**`useMemo` 就是 React 版的 `computed`。**

```javascript
// React
const expensiveValue = useMemo(() => {
  return hugeArray.filter(item => item.active).map(...)
}, [hugeArray]) // 只有当 hugeArray 变了，才重新算
```

### 3. 对比总结

| 特性         | Vue Computed     | React useMemo                    |
| :----------- | :--------------- | :------------------------------- |
| **依赖追踪** | **自动** (Auto)  | **手动** (Manual Deps Array)     |
| **语义**     | **响应式数据源** | **性能优化 (Memoization)**       |
| **是否必须** | 推荐作为默认实践 | 仅在计算昂贵或需要引用稳定时使用 |

- **Vue**：`computed` 是响应式链路的重要一环。因为 Vue 组件只初始化一次，如果不把派生数据定义为 `computed`，普通变量是不会随着依赖变化而自动更新的（除非你在 render 函数里直接用）。
- **React**：`useMemo` 只是性能优化手段。因为组件本身就会重跑，变量本身就会重算，所以不加 `useMemo` 逻辑也是对的，只是慢一点而已。

**一句话总结：Vue 的 `computed` 是为了“能动起来”，React 的 `useMemo` 是为了“别太累”。**
