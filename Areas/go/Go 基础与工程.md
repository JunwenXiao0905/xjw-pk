> 基于 Go 1.26（2026-02 发布，当前稳定 1.26.5 / 2026-07-07）。官方资源：[Tour](https://go.dev/tour/) · [语言规范](https://go.dev/ref/spec) · [Effective Go](https://go.dev/doc/effective_go) · [标准库](https://pkg.go.dev/std) · [下载](https://go.dev/dl/) · [1.26 Release Notes](https://go.dev/doc/go1.26)。

Go 是**编译型、静态类型、带 GC** 的语言。和已有的 Python（解释、动态）、Node/TS（JIT、动态类型）不同：Go 编译成**单一静态二进制**，运行时无外部依赖——这对 GIS 数据中台部署（单容器、单二进制、跨平台交叉编译）是核心优势。它刻意做得小而简：关键字仅 25 个、强制统一格式（gofmt）、显式错误处理（无 try/except）、goroutine 轻量并发。学习时多类比 Python/TS 的对应物，但注意 Go 在类型、错误、并发上是**另一套心智模型**。

## 目录

- [[#第1章 运行与入口]]
  - [[#1.1 安装与环境变量]]
  - [[#1.2 Hello World 与 main 包]]
  - [[#1.3 go run / go build / go install]]
  - [[#1.4 go.mod 与 module 依赖]]
  - [[#1.5 工具链命令速查]]
- [[#第2章 基本语法]]
  - [[#2.1 变量声明与零值]]
  - [[#2.2 基本类型]]
  - [[#2.3 常量与 iota]]
  - [[#2.4 控制流（if / for / switch）]]
  - [[#2.5 函数（多返回值、命名返回、闭包）]]
  - [[#2.6 指针]]
  - [[#2.7 语句与分号（自动分号插入）]]
- [[#第3章 复合类型]]
  - [[#3.1 切片]]

> **后续章节规划**（随学习补充，写完即并入目录）：
> 第3章续: map / struct / 字符串与 rune(切片已落 3.1) · 第4章 方法与接口（接收者/隐式实现/类型断言/Stringer·error·io）· 第5章 错误处理（error/%w/Is·As/panic·recover·defer）· 第6章 包与工程结构（可见性/internal/标准布局/go.work）· 第7章 泛型（类型参数/约束）· 第8章 测试（testing/表驱动/benchmark）· 第9章 工具链与开发习惯（gofmt/vet/golangci-lint/命名约定）

# 第1章 运行与入口

## 1.1 安装与环境变量

- 下载：[go.dev/dl](https://go.dev/dl/)。Windows 用 `.msi`，Linux 解压 `tar.gz` 到 `/usr/local/go`，Mac `brew install go`。验证 `go version` → `go version go1.26.5 windows/amd64`。
- 三个路径变量（用 `go env` 查看，`go env -w KEY=val` 持久设置）：
  - `GOROOT`：Go **安装目录**（标准库源码、工具链）。现代版本会自动推断，一般不用手设。
  - `GOPATH`：旧工作区目录，默认 `$HOME/go`。**module 模式下**它的作用缩减为：存放 `go install` 的二进制（`$GOPATH/bin`）和模块缓存（`$GOPATH/pkg/mod`）。你的源代码**不必**再放这里。
  - `GOBIN`：可执行文件安装目录，默认 `$GOPATH/bin`，建议加入 `PATH`。
- **module 模式**（Go 1.11+ 默认）：项目代码可放任意目录，依赖由 `go.mod` 声明、拉到模块缓存。GOPATH/src 那套老的"工作区"组织已基本废弃。
- **国内网络要点**（和 Docker 构建一致）：默认 `proxy.golang.org` 在国内不可达，需设置

  ```bash
  go env -w GOPROXY=https://goproxy.cn,direct      # 七牛镜像，逗号 fallback
  go env -w GOSUMDB=sum.golang.google.cn            # 校验库镜像（可选）
  ```

## 1.2 Hello World 与 main 包

```go
package main

import "fmt"

func main() {
    fmt.Println("Hello, 世界")
}
```

- `package main` + `func main()` 是**可执行程序**的硬性入口，由编译器/链接器识别。`main` 函数**无参数、无返回值**。
- 类比：
  - Python 的 `if __name__ == "__main__":` 是**运行时约定**，Go 是**编译期要求**——没有 main 包的代码 `go build` 不会产出可执行文件。
  - Node/NestJS 的入口是 `package.json` 指向的 `main.ts → bootstrap()`，由运行时调用；Go 的 `main()` 直接是进程入口。
- 命令行参数：`os.Args`（`[]string`，`Args[0]` 是程序名本身），结构化参数用 `flag` 包（见后端服务篇）。
- **同一目录 = 同一 package**：一个目录下的所有 `.go` 文件必须声明同一个 `package` 名（`main` 也不例外），文件间共享顶层作用域，无需互相 import。

> **包(package) vs 类型(type)——别混淆**：`fmt`、`color` 是**包**，是命名空间，import 即用 `包名.函数`，**没有"实例化"概念**（类比 Python `import math; math.pi`、TS `import * as x`，都不 new）。需要"造实例"的是**类型(struct)**：`p := Person{Name: "x"}` 之后才能调 `p` 的方法。Go 的 `new(T)` 只用于给类型分配零值指针，跟"用包"无关。

## 1.3 go run / go build / go install

| 命令 | 作用 | 产物 | 类比 |
|---|---|---|---|
| `go run .` | 编译到临时目录并**立即执行** | 无（临时文件用完即删） | `ts-node` / `python x.py` |
| `go build .` | 编译，产物放**当前目录** | 可执行二进制 | `tsc` + 链接，或 `gcc` |
| `go install` | 编译并装到 `GOBIN` | 全局可执行命令 | `npm i -g` |

- **交叉编译**（GIS 中台一次构建多平台镜像的关键）：设 `GOOS` / `GOARCH` 即可，无需交叉工具链（CGO 关闭时）：

  ```bash
  GOOS=linux GOARCH=amd64 CGO_ENABLED=0 go build -o gis-api .
  ```

  `CGO_ENABLED=0` 产出**纯静态二进制**，可直接放进 `FROM scratch` 镜像（极小体积）。
- **机制**：Go 以**包**为编译单位，从 main 包出发递归编译所有被 import 的包，最后链接成**单一二进制**（依赖被打包进去，不像 Python/Node 运行时再解析 `node_modules`/`site-packages`）。这是"部署只需一个文件"的根源。

## 1.4 go.mod 与 module 依赖

```bash
go mod init github.com/xjw/gis-api     # 在项目根生成 go.mod
```

- `module github.com/xjw/gis-api` 是**模块路径**，作为本模块内所有包的 import 前缀（如 `github.com/xjw/gis-api/internal/tile`）。
- `go 1.25.0`：声明本模块要求的语言/工具链版本。**坑**：Go 1.26 起 `go mod init` 默认写**低一版**（1.26 工具链写 `go 1.25.0`），目的是兼容仍受支持的两个版本。需要精确控制用 `go get go@1.26`。
- `require` 块声明依赖及其最低版本；`replace`/`exclude` 做本地替换或排除。
- `go.sum`：每个依赖的**密码学哈希**，做完整性/供应链校验。相当于 lockfile + 校验二合一。
- 依赖操作：

  | 命令 | 作用 |
  |---|---|
  | `go get github.com/xxx/yyy@v1.2.3` | 添加/升级依赖到指定版本 |
  | `go mod tidy` | 清理未用依赖 + 补全缺失依赖（提交前必跑） |
  | `go mod download` | 只下载依赖到缓存，不修改 go.mod |
  | `go mod vendor` | 把依赖复制到项目内 `vendor/`（离线/可复现构建） |

- **机制**：Go module 是**版本化依赖单元**，通过 `GOPROXY`（默认 `proxy.golang.org`，国内用 `goproxy.cn`）按 tag/commit 拉取 `.zip` + `.info` + `.mod`，哈希写入 `go.sum`。对比 Python（requirements + poetry.lock + PyPI）、Node（package.json + lock + npm registry），Go 把"声明 + 锁 + 校验"压进 `go.mod`/`go.sum` 两个文件，无独立 lockfile。

## 1.5 工具链命令速查

| 命令 | 用途 |
|---|---|
| `go fmt` / `gofmt -w` | 强制格式化（缩进、对齐、空格），**无配置项** |
| `go vet` | 静态检查常见错误（printf 参数、锁拷贝、不可达代码等） |
| `go test` | 跑测试（`_test.go` 结尾文件里的 `TestXxx` 函数） |
| `go doc fmt.Println` | 终端看文档（替代已删除的 `go tool doc`） |
| `go mod` / `go get` / `go env` | 模块/依赖/环境管理 |
| `go fix` | **1.26 重写**：modernizer，自动把代码升级到新惯用 API（基于 `go vet` 同款分析框架，不改变行为） |

`gofmt` 是 Go 文化核心：格式不是风格问题而是工具产物，团队零争论。配合编辑器保存即格式化即可，不要手写格式。

---

# 第2章 基本语法

## 2.1 变量声明与零值

```go
var x int        // 声明，零值 0
var y = 10       // 推断为 int
var a, b int = 1, 2
s := "hi"        // 短变量声明（仅函数内），最常用
i, j := 1, 2     // 多变量短声明
i, j = j, i      // 多重赋值 = 交换，无需临时变量
```

- **短变量声明 `:=`**：函数内最常用，等价于 `var + 推断 + 省略类型`。**包级不能用** `:=`，只能 `var`。
- **零值**：声明即有值，不存在 Python 那种"未赋值"。零值表——数值 `0`、`bool` `false`、`string` `""`、指针/接口/slice/map/channel/func `nil`。
- **坑①**：`:=` 左侧**必须至少一个新变量**，否则 `no new variables on left side of :=`；纯重赋值要改用 `=`：

  ```go
  x := 1
  x := 2   // 编译错误
  x = 2    // 正确
  ```

- **坑②**：`:=` 与作用域——在 `if`/`for` 块内 `:=` 会**新建**同名局部变量，遮蔽外层，改的不是你以为的那个。新手高发 bug。

## 2.2 基本类型

| 类别 | 类型 |
|---|---|
| 整数 | `int` `int8/16/32/64` · `uint` `uint8/...` · `uintptr`（存指针的数值） |
| 浮点 | `float32` `float64`（字面量默认 `float64`） |
| 布尔 | `bool` |
| 字符串 | `string`（**不可变** UTF-8 字节序列） |
| 字节/码点 | `byte` = `uint8` · `rune` = `int32`（一个 Unicode 码点） |
| 复数 | `complex64` `complex128`（GIS 基本不用） |

- **`int` 的陷阱**：`int` 在 64 位机上大小同 `int64`，但**它是独立类型**，与 `int64` 不互通，需显式转换。跨平台代码涉及二进制协议/切片长度时，用定长 `int32`/`int64` 更安全。
- **类型转换是显式的**，Go **没有隐式数值转换**（连 `int` → `int64` 都不行）：

  ```go
  var i int = 1
  var f float64 = float64(i)   // 必须
  s := string(65)              // ⚠ 这是 "A"（按 rune 转），不是 "65"！
  n := strconv.Itoa(65)        // "65" 才是这个
  ```

  对比 Python/TS 都会隐式转换，这里要改习惯。`string(rune/int)` 的语义是"按码点转字符"，是经典坑。

## 2.3 常量与 iota

```go
const Pi = 3.14159265358979
const (
    StatusOK = 200
    NotFound = 404
)

// iota：常量计数器，每个 const 块内从 0 开始，每出现一行 +1
const (
    _  = iota             // 0，丢弃
    KB = 1 << (10 * iota) // 1 << 10  = 1024
    MB                    // 1 << 20  （重复上一行表达式，iota 自增）
    GB                    // 1 << 30
)

type TileZ uint8
const (
    TileZ0 TileZ = iota   // 0,1,2... 做枚举用
    TileZ1
    TileZ2
)
```

- **无类型常量**（如上面的 `Pi`、`KB`）：不绑定具体类型，用到时才按上下文定类型，精度更高，能赋给 `float32`/`float64` 等多种。这是常量比变量灵活的地方。
- Go **没有真正的 enum**，惯例用 `type X int` + `const` + `iota` 组合模拟枚举。

## 2.4 控制流（if / for / switch）

Go 只有三个控制流关键字：`if`、`for`、`switch`。**没有** `while`、`do-while`、三元运算符 `?:`。

```go
// if：可带初始化语句，n 的作用域限于整个 if-else
if n := len(s); n > 10 {
    fmt.Println(n)
} else {
    fmt.Println(n)   // 这里也能用 n
}

// for：唯一的循环
for i := 0; i < 3; i++ { }      // C 风格
for count < 100 { count++ }     // 当 while 用
for { break }                    // 无限循环
for i, v := range slice { }      // 遍历（index, value）
for k, v := range m { }          // map 遍历（key, value）

// switch：默认每个 case 自动 break（不穿透！）
switch os := runtime.GOOS; os {
case "linux", "darwin":          // 多值
    fmt.Println("unix-like")
case "windows":
    fmt.Println("win")
default:
    fmt.Println("?")
}
// 无表达式 switch = if-else 链
switch {
case x < 0: ...
case x == 0: ...
}
```

- **for range 坑**：`range` 拷贝的是**元素的副本**到 `v`，改 `v` 不影响原集合。要改原值用下标 `s[i] = ...`。遍历 string 时 `range` 按 **rune** 切分（不是字节）。
- **switch 不穿透**（对比 C/Java 默认穿透）：Go 默认每个 case 末尾隐含 `break`，需要穿透用 `fallthrough`（少见）。这是为减少 bug 的有意设计。
- **map 遍历顺序随机**：每次 `range map` 顺序不同，这是运行时刻意随机的，不要依赖顺序。

## 2.5 函数（多返回值、命名返回、闭包）

```go
func add(a, b int) int { return a + b }            // 参数同类型可合并

// 多返回值：惯用于 (结果, 错误)
func divmod(a, b int) (int, int) {
    return a / b, a % b
}
q, r := divmod(17, 5)

// 命名返回：return 可裸写，返回值在函数入口已零值初始化
func parse(s string) (n int, err error) {
    n, err = strconv.Atoi(s)
    return                       // 裸 return，返回当前 n, err
}

// 可变参数：nums 在函数内是 []int
func sum(nums ...int) int { total := 0; for _, n := range nums { total += n }; return total }

// 函数是一等值 + 闭包
adder := func(a, b int) int { return a + b }       // 匿名函数赋给变量
counter := func() func() int {                      // 返回闭包
    c := 0
    return func() int { c++; return c }
}()
```

- **多返回值**是 Go 的核心约定：需要"既返回结果又返回错误"时，不用异常、不用 out 参数，直接 `(T, error)`。这是整个错误处理模型的基础（第5章）。
- **命名返回值**的两个用途：① 文档（签名就说明返回什么）；② 配合裸 `return`（但函数长时裸 return 可读性差，慎用）。更常见的价值是**命名返回值可用作零值初始化的变量**，配合 defer 修改（见错误处理章 panic/recover）。
- **闭包按引用捕获**外层变量：闭包持有的是变量的引用，不是拷贝。循环里开 goroutine 捕获循环变量是经典并发坑（第3章/并发篇详述）。

## 2.6 指针

```go
x := 10
p := &x          // p 是 *int，指向 x
fmt.Println(*p)  // 解引用 → 10
*p = 20          // 通过指针改 x → x 变 20

var ptr *int     // ptr 的零值是 nil

func incr(n *int) { *n++ }   // 传指针才能改外部值
n := 1
incr(&n)                     // n → 2

// new(T)：分配零值并返回指针
p2 := new(int)               // *int，指向 0
```

- Go 有指针但**不能做指针算术**（不能 `p++`、`p+1`），比 C 安全得多。指针主要用于三件事：
  1. **函数内修改外部变量**（上面的 `incr`）；
  2. **避免大 struct 的值拷贝**（传 `*BigStruct` 而非 `BigStruct`）；
  3. **可选字段/可空引用**：`*T` 可为 `nil`，值类型 `T` 不能（数据库 NULL、JSON 可选字段常用指针）。
- **`new(T)` vs `&T{}`**：`new` 返回零值指针；结构体更常用 `&Foo{...}` 字面量。**Go 1.26 新增** `new(expr)`：可直接给指针初始化值（`new(yearsSince(born))`），方便给 `*int` 这类可选字段赋值。
- **关键机制——逃逸分析**：返回局部变量的指针**在 Go 里是合法且安全的**，编译器分析到指针"逃逸"出函数时，会自动把它分配到**堆**而非栈。对比 C 的悬垂指针，Go 不存在这个问题。代价是该变量需 GC 回收。`go build -gcflags="-m"` 可看逃逸分析结果。

## 2.7 语句与分号（自动分号插入）

Go **语法**上每条语句以分号结尾，但源码里几乎不写分号——靠**词法器的自动分号插入**（[规范](https://go.dev/ref/spec#Automatic_semicolon_insertion)）。

**规则**：换行时，若**行末最后一个 token** 属于以下名单，词法器在该行末**自动插入分号**：

- 标识符、字面量
- `break` `continue` `fallthrough` `return`
- `++` `--`
- `)` `}` `]`

这是**词法层**的机械规则——词法器不懂语法、不判断"语句是否完整"，只看行末 token 类别（分号插入发生在建语法树**之前**，只能拿行末 token 当代理信号）。

**推论**：一行一语句时无需写分号；一行塞多条才用 `;` 分隔（`a := 1; b := 2`、`import ("fmt"; "os")`）。

**这条规则逼出来的格式习惯**（不是审美，是编译要求）：

- `{` 必须跟在函数 / 控制结构签名**同一行**——否则行末 `)` 触发分号，`func foo(); {` 报错。
- 链式调用换行，`.` / `[` 必须留在**行末**（不在名单，不插分号，调用延续）：

  ```go
  result := foo().
      Bar().
      Baz()
  ```
  对比 JS：JS 的 ASI 更宽松，习惯把 `.` 放**行首**；Go 必须放行末，否则行末 `)` 截断链式调用。
- `return` 后不要直接换行写返回值，否则变成 `return;` 提前返回空。

gofmt 会强制每条语句、每个 import 单独成行，所以实际编码中手写分号极少。

---

# 第3章 复合类型

## 3.1 切片

切片是 Go 日常用的"动态列表"——后端开发最高频、坑也最多的类型。理解一切的关键是它的**底层结构**。

### 3.1.1 数组 vs 切片

- **数组(array)**：固定长度，**长度是类型的一部分**（`[3]int` 和 `[4]int` 是不同类型），赋值/传参**拷贝整个数组**。基本不直接用。
- **切片(slice)**：动态长度，底层**引用一段数组**。

```go
a := [5]int{10, 20, 30, 40, 50}   // 数组：固定 5
s := []int{10, 20, 30}            // 切片：动态
```

### 3.1.2 底层结构：3 字段 header（ptr / len / cap）

切片在底层是三个字段：

| 字段 | 含义 |
|---|---|
| `ptr` | 指向**底层数组**首元素的指针 |
| `len` | 当前长度（可见元素数） |
| `cap` | 容量（底层数组从 `ptr` 到末尾的元素数） |

切片 = 底层数组上的一段窗口：`[ptr, ptr+len)` 可见，`[ptr, ptr+cap)` 是预留容量。

```
底层数组:  [10][20][30][40][50]
索引:       0   1   2   3   4
s := a[1:4]
  ptr ──> a[1] (值 20)
  len = 3   → s = [20,30,40]
  cap = 4   → 从 a[1] 到末尾共 4 个
```

> 注：`a[1]` 的 1 是**原数组索引**（a[1]=20）。切片自己的索引从 0 重新开始——`s[0]` 对应底层 `a[1]`，`s[i]` 对应 `a[1+i]`，ptr 决定偏移起点。这也是"共享底层"的本质：改 `s[0]` 就是改 `a[1]`，同一块内存，各自的 0 号位不是同一个槽。

**赋值/传参切片，拷贝的是这 3 字段 header，底层数组不拷贝** → 多个切片可指向同一底层数组。这是 append 扩容、共享修改坑的根源。

### 3.1.3 为什么切片"动态"（数组固定却动态）

动态性来自 header 的**间接性**，不是数组变长。两条路都**不改原来的数组**：

1. **改 len**（不换数组）：len 是 header 里的数，只要新 `len ≤ cap`，重新切片即可变长/变短，底层数组不动。
2. **cap 装不下时换新数组**（真·长大）：`append` 时 cap 不够，Go 新分配更大的数组、拷贝旧元素、让 header 的 `ptr` 指向新数组、更新 len/cap。

cap 的跳变就是"换数组"的信号：

```go
s := []int{1, 2}
fmt.Println(cap(s))                       // 2
s = append(s, 3);  fmt.Println(cap(s))    // 4   换了更大的新数组
s = append(s, 4,5,6); fmt.Println(cap(s)) // 8   又换
```

### 3.1.4 创建切片（4 种）

```go
s := []int{1, 2, 3}          // ① 字面量
a := make([]int, 3)          // ② make: len=3 cap=3 → [0 0 0]
b := make([]int, 3, 5)       //    make: len=3 cap=5 → [0 0 0] + 预留 2 格
var n []int                  // ③ var: nil 切片(len=0 cap=0, n==nil)
arr := [5]int{1,2,3,4,5}
s2 := arr[1:4]               // ④ 切割: [2 3 4],共享 arr 底层
```

- **make 高频坑**：`make([]int, 3)` 不是"准备 3 个空位等填"，它**已有 3 个 0**，append 从第 4 个位置追加。想"预分配容量但从空开始"用 `make([]int, 0, 3)`。
- **nil vs 空切片**：`var n []int`（nil）和 `[]int{}`（空）len/cap 都 0，区别在 `n==nil`。append 两者都安全。函数返回"没数据"用 nil 更地道。

### 3.1.5 切片表达式 s[low:high]

左闭右开 `[low, high)`：

```go
s := []int{10, 20, 30, 40, 50}
s[1:4]    // [20 30 40]
s[:3]     // [10 20 30]   省略 low = s[0:3]
s[2:]     // [30 40 50]   省略 high = s[2:len(s)]
s[:]      // 全部
```

类比 Python 几乎一样，但 Go **不支持步长**（无 `s[::2]`）、**不支持负索引**（无 `s[-1]`）。结果仍是切片，且与原切片**共享底层数组**。

### 3.1.6 遍历（range）与查改

```go
s := []int{10, 20, 30}
fmt.Println(s[1])        // 查 → 20
s[1] = 99                // 改
// s[5]                  // ❌ 越界 panic(只到 len-1)
fmt.Println(len(s), cap(s))

for i, v := range s { }  // i=索引 v=元素(拷贝); 改 v 不影响原切片
for _, v := range s { }  // 只要值
for i := range s { }     // 只要索引
```

`range` 是 for 的遍历形式（完整见 2.4）。`_` 是空白标识符——丢弃不要的值（Go 不允许声明未用的变量）。

### 3.1.7 增：append

```go
s := []int{1, 2}
s = append(s, 3)                 // 单个
s = append(s, 4, 5)              // 多个
s = append(s, []int{6,7}...)     // 追加切片,用 ... 展开
```

**必须接回 `s`**：append 可能换底层数组，不接回 = 旧 header 指旧数组，丢数据。

### 3.1.8 删（Go 没有内置 delete，靠 append 拼）

```go
s := []int{1, 2, 3, 4, 5}; i := 2
s = append(s[:i], s[i+1:]...)    // 保序删除 → [1 2 4 5]

// 不保序 O(1) 删(顺序无所谓时更快):末尾换到 i 再缩
s = []int{1,2,3,4,5}
s[i] = s[len(s)-1]
s = s[:len(s)-1]                 // [1 2 5 4]
```

**删除的坑**：保序删除**就地改底层数组**（前移覆盖），末尾位置残留旧值；若别的切片引用同一底层数组，可能读到脏数据。彻底清理需把末尾置零。

### 3.1.9 复制 copy（断开共享）与清空

```go
a := []int{1, 2, 3}
b := make([]int, len(a))
copy(b, a)          // 真拷贝元素到 b,此后 a/b 互不影响;返回拷贝数
// b := a           // ⚠ 只拷贝 header,共享底层,不是拷贝
s = s[:0]           // 清空:len 归零,cap 不变,底层数组保留 → 后续 append 复用内存
```

### 3.1.10 append 的扩容策略

cap 不够时新 cap 怎么定？这是 **runtime 实现细节**（`src/runtime/slice.go` 的 `growslice`），不是语言规范——**版本间会变，别写依赖具体 cap 值的代码**。

经验法则（Go 1.18+）：

- 旧 cap **< 256**：**翻倍**（2x）
- 旧 cap **≥ 256**：约 **1.25 倍的平滑增长**（不再粗暴翻倍，省内存）
- 一次 append 的量**超过翻倍**：直接用需求量
- 最后按内存 class **向上取整**，实际 cap 常略多

> 1.18 前是"<1024 翻倍，≥1024 增 1.25 倍"；1.18 把阈值降到 256 并改平滑曲线。**记经验法则即可，别记精确公式**。

工程要点：

1. **别依赖具体 cap 值**（它是实现细节）。要确定行为用 `copy` 或预分配。
2. **已知大小就预分配** `make([]T, 0, n)`，避免循环里反复"分配 + 拷贝"——后端处理批量数据（如 GIS 读坐标点列表）的常用优化。

### 3.1.11 共享底层的坑（污染 / 断开）与三索引切片

共享底层的切片，append 有**两个相反的坑**：

**坑① cap 还够 → 不换数组 → 污染兄弟切片**：

```go
a := []int{1, 2, 3, 4, 5}
b := a[1:4]            // b.cap = 5-1 = 4
b = append(b, 99)      // cap 够,不换数组;99 就地写进 a[4]
fmt.Println(a)         // [1 2 3 4 99]  ← a 的 5 被覆盖!
```

**坑② cap 满了 → 换新数组 → 与兄弟断开**：

```go
b = append(b, 100)     // cap 满,换新数组,b 指向新数组
b[0] = 888
fmt.Println(a)         // [1 2 3 4 99]  ← 不变了,a/b 已断开
```

"以为共享同步、append 后悄悄断开"是切片最常见的 bug 来源。

**避坑**：

- 要彻底独立：用 `copy`。
- 要安全 append 子切片：**三索引切片** `a[low:high:max]` 截断 cap（`cap = max - low`），强制 append 必换新数组：

```go
b := a[1:4:4]        // len=3, cap=3 → 任何 append 必换数组,不污染 a
b = append(b, 99)
```
