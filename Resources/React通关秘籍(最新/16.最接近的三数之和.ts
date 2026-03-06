/**
 * 最接近的三数之和（LeetCode 16）
 *
 * 解题思路（排序 + 双指针）：
 * 1. 先对数组进行升序排序，便于使用双指针技巧；
 * 2. 固定第一个数 nums[i]，然后在区间 [i + 1, n - 1] 上，用左右指针 l、r 找另外两个数：
 *    - 当前三数之和为 sum = nums[i] + nums[l] + nums[r]；
 *    - 用 best 记录目前为止最接近 target 的三数之和；
 *    - 如果 |sum - target| 更小，则更新 best；
 *    - 如果 sum 恰好等于 target，可以直接返回，因为这已经是最优答案；
 *    - 如果 sum > target，说明和偏大，为了让和变小，右指针左移（r--）；
 *    - 如果 sum < target，说明和偏小，为了让和变大，左指针右移（l++）。
 * 3. 遍历所有可能的 i（0 <= i <= n - 3），最终 best 即为答案。
 *
 * 由于题目保证恰好存在一个解，所以初始 best 可以直接取前三个数之和。
 *
 * 时间复杂度：O(n^2)，外层枚举 i，内层是一次双指针扫描；
 * 空间复杂度：O(1)，排序通常视为原地排序，仅使用常数额外空间。
 *
 * @param nums 整数数组
 * @param target 目标值
 * @returns 与 target 最接近的三数之和
 */
export function threeSumClosest(nums: number[], target: number): number {
  const n = nums.length

  // 题目保证一定有解，且至少能取到三个数
  if (n < 3) {
    throw new Error('数组长度必须至少为 3')
  }

  // 先排序，方便使用双指针
  nums.sort((a, b) => a - b)

  // 初始最优值：先取前三个数之和
  let best = nums[0] + nums[1] + nums[2]

  for (let i = 0; i < n - 2; i++) {
    let l = i + 1
    let r = n - 1

    while (l < r) {
      const sum = nums[i] + nums[l] + nums[r]

      // 如果当前更接近 target，则更新 best
      if (Math.abs(sum - target) < Math.abs(best - target)) {
        best = sum
      }

      if (sum === target) {
        // 已经和 target 一样了，不可能再更优，直接返回
        return sum
      } else if (sum > target) {
        // 和偏大，右指针左移
        r--
      } else {
        // 和偏小，左指针右移
        l++
      }
    }
  }

  return best
}

/**
 * 方法二：朴素三重循环枚举（用于理解问题，不推荐在 n 很大时使用）
 *
 * 思路说明：
 * - 直接枚举所有下标 i、j、k（i < j < k）组成的三元组；
 * - 计算每个三元组的和 sum，与当前记录的 best 比较；
 * - 如果 |sum - target| 更小，就更新 best；
 * - 枚举结束后，best 即为最接近 target 的三数之和。
 *
 * 这个方法的优点是思路非常直接，有助于理解题意；
 * 缺点是时间复杂度较高，为 O(n^3)，当 n 较大时会比较慢。
 *
 * @param nums 整数数组
 * @param target 目标值
 * @returns 与 target 最接近的三数之和（朴素解法）
 */
export function threeSumClosestBruteForce(nums: number[], target: number): number {
  const n = nums.length

  if (n < 3) {
    throw new Error('数组长度必须至少为 3')
  }

  // 初始 best 取前三个元素之和
  let best = nums[0] + nums[1] + nums[2]

  for (let i = 0; i < n - 2; i++) {
    for (let j = i + 1; j < n - 1; j++) {
      for (let k = j + 1; k < n; k++) {
        const sum = nums[i] + nums[j] + nums[k]

        if (Math.abs(sum - target) < Math.abs(best - target)) {
          best = sum
        }
      }
    }
  }

  return best
}
