/**
 * 解法一：用数组保存所有区间，逐个检查是否有重叠
 *
 * 思路说明：
 * - 用一个数组 intervals 存储已经成功预订的所有区间 [start, end)；
 * - 每次调用 book(start, end)：
 *   - 遍历所有已存在区间 [s, e)，判断是否存在交集：
 *     - 交集条件：max(s, start) < min(e, end) 即说明时间有重叠；
 *   - 一旦发现有重叠，返回 false，不插入新日程；
 *   - 如果与所有区间都不重叠，则把 [start, end) 加入数组并返回 true。
 *
 * 复杂度分析：
 * - 设已经存储了 n 个区间，每次 book 需要 O(n) 时间遍历检查；
 * - 空间复杂度 O(n)。实现简单，适合入门理解本题。
 */
export class MyCalendar {
  // 保存已经成功预订的所有区间
  private intervals: Array<[number, number]>

  /**
   * 构造函数：初始化日程数组
   */
  constructor() {
    this.intervals = []
  }

  /**
   * 尝试预订区间 [startTime, endTime)
   * 若不会造成重复预订，则插入并返回 true；否则返回 false。
   *
   * @param startTime 日程开始时间（含）
   * @param endTime 日程结束时间（不含）
   * @returns 是否预订成功
   */
  book(startTime: number, endTime: number): boolean {
    for (const [s, e] of this.intervals) {
      // 判断区间 [s, e) 与 [startTime, endTime) 是否有交集
      // 有交集的充要条件：max(s, startTime) < min(e, endTime)
      if (Math.max(s, startTime) < Math.min(e, endTime)) {
        // 说明时间上有重叠，不能预订
        return false
      }
    }

    // 与所有既有区间都不重叠，可以添加
    this.intervals.push([startTime, endTime])
    return true
  }
}

/**
 * 解法二：保持区间按开始时间有序 + 二分查找插入位置
 *
 * 思路说明：
 * - 同样保存所有成功预订的区间，但始终保持数组按 start 升序；
 * - 每次 book：
 *   1. 通过二分查找，找到新区间应插入的位置 idx；
 *   2. 只需要和前一个区间 intervals[idx - 1]、当前区间 intervals[idx]
 *      检查是否有交集即可（因为其它区间要么全部在左，要么全部在右，不可能重叠）；
 *   3. 若无重叠，则在 idx 位置插入新区间，返回 true，否则返回 false。
 *
 * 复杂度分析：
 * - 二分查找 O(log n)，插入数组需要移动元素 O(n)，整体仍为 O(n)；
 * - 与解法一相比，只是常数略有优化，但思路更接近「有序结构 + 查找」的实际写法。
 */
export class MyCalendarBinarySearch {
  // 依照 start 升序排列的区间数组
  private intervals: Array<[number, number]>

  /**
   * 构造函数：初始化有序区间数组
   */
  constructor() {
    this.intervals = []
  }

  /**
   * 二分查找新区间 [startTime, endTime) 应该插入的位置
   * 保证插入后 intervals 仍按 start 升序
   *
   * @param startTime 新区间的开始时间
   * @returns 插入位置下标
   */
  private findInsertPosition(startTime: number): number {
    let left = 0
    let right = this.intervals.length

    while (left < right) {
      const mid = left + ((right - left) >> 1)
      const [s] = this.intervals[mid]

      if (s < startTime) {
        left = mid + 1
      } else {
        right = mid
      }
    }

    return left
  }

  /**
   * 尝试预订区间 [startTime, endTime)
   * 若不会造成重复预订，则插入并返回 true；否则返回 false。
   *
   * @param startTime 日程开始时间（含）
   * @param endTime 日程结束时间（不含）
   * @returns 是否预订成功
   */
  book(startTime: number, endTime: number): boolean {
    const idx = this.findInsertPosition(startTime)

    // 检查与前一个区间是否有重叠
    if (idx > 0) {
      const [prevStart, prevEnd] = this.intervals[idx - 1]
      if (Math.max(prevStart, startTime) < Math.min(prevEnd, endTime)) {
        return false
      }
    }

    // 检查与当前位置区间是否有重叠
    if (idx < this.intervals.length) {
      const [nextStart, nextEnd] = this.intervals[idx]
      if (Math.max(nextStart, startTime) < Math.min(nextEnd, endTime)) {
        return false
      }
    }

    // 没有重叠，可以安全插入到有序数组中
    this.intervals.splice(idx, 0, [startTime, endTime])
    return true
  }
}
