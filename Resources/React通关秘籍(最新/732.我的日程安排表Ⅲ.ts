/**
 * 解法一：差分 + 扫描线（有序时间点）
 *
 * 核心思路：
 * - 每个区间 [start, end) 可以看成在 start 处「+1」，在 end 处「-1」；
 * - 对所有区间的端点做差分后，按时间升序累加，得到每个时间点的并发预订数；
 * - 当前所有区间的最大并发数，就是这些前缀和中的最大值。
 *
 * 在 book 调用过程中：
 * - 把 start 位置的差分值 +1，把 end 位置的差分值 -1；
 * - 然后对所有 key 按时间排序，从头扫一遍累加前缀和，更新最大并发数。
 *
 * 复杂度分析：
 * - 设当前已经预订了 m 个区间，则最多有 2m 个端点；
 * - 每次 book 需要对所有 key 排序并扫描，时间复杂度约为 O(m log m)；
 * - 空间复杂度 O(m)。
 *
 * 该做法实现简单、易于理解，适合初次接触本题时使用。
 */
export class MyCalendarThree {
  // 记录每个端点的差分值：start -> +1, end -> -1
  private delta: Map<number, number>

  // 当前所有历史预订中出现过的最大并发数
  private maxK: number

  /**
   * 构造函数，初始化差分容器和最大并发数
   */
  constructor() {
    this.delta = new Map()
    this.maxK = 0
  }

  /**
   * 添加一个新的日程区间 [startTime, endTime)
   * 返回当前所有日程产生的最大 k 次预订（最大并发数）
   *
   * @param startTime 区间开始时间（含）
   * @param endTime 区间结束时间（不含）
   * @returns 当前为止的最大并发预订次数
   */
  book(startTime: number, endTime: number): number {
    // 在 startTime 位置 +1
    this.delta.set(startTime, (this.delta.get(startTime) ?? 0) + 1)
    // 在 endTime 位置 -1
    this.delta.set(endTime, (this.delta.get(endTime) ?? 0) - 1)

    // 重新计算前缀和的最大值
    let ongoing = 0
    let curMax = 0

    // 所有端点按时间升序排序后线性扫描
    const points = Array.from(this.delta.keys()).sort((a, b) => a - b)

    for (const t of points) {
      ongoing += this.delta.get(t)!
      if (ongoing > curMax) {
        curMax = ongoing
      }
    }

    this.maxK = curMax
    return this.maxK
  }
}

/**
 * 解法二：动态开点线段树 + 懒标记
 *
 * 核心思路：
 * - 题目中的时间范围为 [0, 10^9)，区间非常大，不能直接用数组；
 * - 使用「动态开点」的线段树，只在需要的节点上开辟子节点；
 * - 对每次预订的区间 [start, end) 执行区间加 1 操作；
 * - 根节点保存整个时间轴上的最大值，即所有时间点的最大并发预订数。
 *
 * 关键技巧：
 * - 使用懒标记（lazy / add）表示该节点子区间还未下传的增量；
 * - update 时：若当前区间被待更新区间完全覆盖，则直接在该节点累加并更新 max；
 * - 否则向左右子树递归，并在回溯时通过子节点的 max 更新当前节点的 max。
 *
 * 复杂度分析（令 n 为预订次数）：
 * - 每次 book 的时间复杂度约为 O(log C)，C 为坐标范围（这里约为 10^9）；
 * - 动态开点后，实际节点数量与操作次数近似线性相关，空间复杂度 O(n log C)。
 *
 * 相比解法一：
 * - 更适合在预订次数较多、端点较分散时使用；
 * - 不需要每次 book 都重新排序所有端点。
 */
class SegmentTreeNode {
  // 左右子节点
  left: SegmentTreeNode | null = null
  right: SegmentTreeNode | null = null

  // 当前区间的最大值
  max: number = 0

  // 懒标记：需要下传给子区间的增量
  add: number = 0
}

export class MyCalendarThreeSegmentTree {
  // 根节点代表整个时间范围 [0, N]
  private root: SegmentTreeNode

  // 题目给出的时间上界
  private readonly N: number

  /**
   * 构造函数，初始化线段树根节点与时间上界
   */
  constructor() {
    this.root = new SegmentTreeNode()
    // 时间范围 [0, 10^9)，为了方便线段树用闭区间 [0, 10^9]
    this.N = 1_000_000_000
  }

  /**
   * 对区间 [l, r] 执行加法操作（内部实现使用闭区间）
   *
   * @param node 当前线段树节点
   * @param start 当前节点表示的区间左端点
   * @param end 当前节点表示的区间右端点
   * @param l 更新区间左端点
   * @param r 更新区间右端点
   * @param val 区间要增加的值
   */
  private update(
    node: SegmentTreeNode,
    start: number,
    end: number,
    l: number,
    r: number,
    val: number
  ): void {
    if (l > end || r < start) {
      // 无交集，直接返回
      return
    }

    if (l <= start && end <= r) {
      // 当前区间被完全覆盖，直接打标记并更新最大值
      node.max += val
      node.add += val
      return
    }

    const mid = start + ((end - start) >> 1)

    // 下推懒标记，并保证子节点存在
    this.pushDown(node)

    if (l <= mid) {
      this.update(node.left!, start, mid, l, r, val)
    }
    if (r > mid) {
      this.update(node.right!, mid + 1, end, l, r, val)
    }

    // 回溯时更新当前节点的最大值
    node.max = Math.max(node.left!.max, node.right!.max)
  }

  /**
   * 将当前节点的懒标记下推给左右子节点
   *
   * @param node 当前线段树节点
   */
  private pushDown(node: SegmentTreeNode): void {
    if (!node.left) {
      node.left = new SegmentTreeNode()
    }
    if (!node.right) {
      node.right = new SegmentTreeNode()
    }

    if (node.add !== 0) {
      const addVal = node.add

      node.left.max += addVal
      node.left.add += addVal

      node.right.max += addVal
      node.right.add += addVal

      node.add = 0
    }
  }

  /**
   * 添加一个新的日程区间 [startTime, endTime)
   * 返回当前所有日程产生的最大 k 次预订（最大并发数）
   *
   * 在内部实现中，我们使用闭区间 [startTime, endTime - 1] 进行更新。
   *
   * @param startTime 区间开始时间（含）
   * @param endTime 区间结束时间（不含）
   * @returns 当前为止的最大并发预订次数
   */
  book(startTime: number, endTime: number): number {
    // 半开区间 [startTime, endTime) 对应闭区间 [startTime, endTime - 1]
    const l = startTime
    const r = endTime - 1

    if (l <= r) {
      this.update(this.root, 0, this.N, l, r, 1)
    }

    // 根节点的 max 始终表示整段时间内的最大并发数
    return this.root.max
  }
}
