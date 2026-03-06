/**
 * 方法一：快慢指针（稳定保序）
 *
 * 思路说明：
 * - 使用两个指针：
 *   - 快指针 fast：从头到尾扫描整个数组；
 *   - 慢指针 slow：指向「下一个要放置的不等于 val 的元素」的位置；
 * - 当 nums[fast] !== val 时，将该元素复制到 nums[slow]，然后 slow++；
 * - 当 nums[fast] === val 时，则跳过，不做任何操作；
 * - 遍历结束后，[0, slow) 区间即为所有不等于 val 的元素，数量为 slow；
 * - 题目说明后面的元素和顺序不重要，所以 [slow, n) 区间的内容可以忽略。
 *
 * 该方法的特点：
 * - 保证不等于 val 的元素相对顺序不变（稳定）；
 * - 只遍历一遍数组，满足原地 O(1) 额外空间。
 *
 * 时间复杂度：O(n)
 * 空间复杂度：O(1)
 *
 * @param nums 原始数组，会被原地修改
 * @param val 需要移除的元素值
 * @returns 不等于 val 的元素个数 k
 */
export function removeElement(nums: number[], val: number): number {
  let slow = 0

  for (let fast = 0; fast < nums.length; fast++) {
    if (nums[fast] !== val) {
      // 将不等于 val 的元素搬运到前面
      nums[slow] = nums[fast]
      slow++
    }
  }

  // slow 即为不等于 val 的元素数量
  return slow
}

/**
 * 方法二：首尾双指针（允许改变顺序）
 *
 * 思路说明：
 * - 使用两个指针：
 *   - 左指针 left：从左向右扫描；
 *   - 右指针 right：指向当前数组的「有效末尾位置」（初始为 nums.length - 1）；
 * - 当 nums[left] === val 时：
 *   - 将 nums[left] 替换为 nums[right]，并将 right--；
 *   - 此时并不移动 left，因为替换过来的元素还需要再次检查；
 * - 当 nums[left] !== val 时：
 *   - left++，继续向右扫描；
 * - 当 left > right 时，扫描结束：
 *   - [0, right] 区间即为不等于 val 的元素，元素个数为 right + 1。
 *
 * 该方法的特点：
 * - 不保证原数组中不等于 val 的元素相对顺序；
 * - 但可以减少写操作次数，尤其当要删除的元素较少时更高效。
 *
 * 时间复杂度：O(n)
 * 空间复杂度：O(1)
 *
 * @param nums 原始数组，会被原地修改
 * @param val 需要移除的元素值
 * @returns 不等于 val 的元素个数 k
 */
export function removeElementSwap(nums: number[], val: number): number {
  let left = 0
  let right = nums.length - 1

  while (left <= right) {
    if (nums[left] === val) {
      // 将等于 val 的元素与当前有效末尾元素交换，然后缩短有效区间
      nums[left] = nums[right]
      right--
      // 此时不能 left++，因为换过来的元素还未检查
    } else {
      // 当前元素保留，继续向右扫描
      left++
    }
  }

  // 有效区间为 [0, right]，长度为 right + 1
  return right + 1
}
