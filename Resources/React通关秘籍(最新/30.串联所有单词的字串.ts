// 30. 串联所有单词的子串

/**
 * 解法一：暴力哈希表 (Naive HashMap)
 *
 * 思路：
 * 1. 因为 words 中所有单词长度相同，记为 wordLen。
 * 2. 我们可以遍历 s 的每一个字符作为起始点 i。
 * 3. 检查从 i 开始的长度为 totalLen 的子串，是否恰好由 words 中的所有单词组成。
 * 4. 检查方法：将子串按 wordLen 切分，统计频率，与 words 的频率对比。
 *
 * 复杂度分析：
 * - 时间复杂度：O(n * m * k)，其中 n 是 s 的长度，m 是 words 的个数，k 是单个单词的长度。
 *   每次循环需要遍历 m 个单词，每个单词截取和哈希操作耗时 O(k)。
 * - 空间复杂度：O(m * k)，用于存储哈希表。
 */
function findSubstring(s: string, words: string[]): number[] {
  const result: number[] = []
  if (!s || words.length === 0) return result

  const wordLen = words[0].length
  const wordCount = words.length
  const totalLen = wordLen * wordCount

  if (s.length < totalLen) return result

  // 统计 words 中每个单词的出现次数
  const wordMap = new Map<string, number>()
  for (const w of words) {
    wordMap.set(w, (wordMap.get(w) || 0) + 1)
  }

  // 遍历 s，注意只需遍历到 s.length - totalLen 即可
  for (let i = 0; i <= s.length - totalLen; i++) {
    const seen = new Map<string, number>()
    let j = 0

    // 尝试匹配 m 个单词
    while (j < wordCount) {
      // 截取当前单词
      const wordIndex = i + j * wordLen
      const word = s.substring(wordIndex, wordIndex + wordLen)

      // 如果这个单词不在 words 里，直接跳过当前起始点 i
      if (!wordMap.has(word)) {
        break
      }

      // 统计当前子串中该单词出现的次数
      seen.set(word, (seen.get(word) || 0) + 1)

      // 如果出现次数超过了 words 中的次数，也不符合
      if (seen.get(word)! > wordMap.get(word)!) {
        break
      }

      j++
    }

    // 如果成功匹配了所有单词
    if (j === wordCount) {
      result.push(i)
    }
  }

  return result
}

/**
 * 解法二：滑动窗口优化 (Sliding Window Optimization)
 *
 * 思路：
 * 1. 上面的解法中，每次移动 1 个字符，都要重新构建 Map，包含大量重复计算。
 * 2. 由于单词长度固定为 k (wordLen)，我们可以将起始点分为 k 组：
 *    - 从 0 开始：0, k, 2k...
 *    - 从 1 开始：1, 1+k, 1+2k...
 *    - ...
 *    - 从 k-1 开始
 * 3. 在每一组中，我们维护一个真正的“滑动窗口”，每次右移一个单词长度 k，
 *    左边移出一个单词，右边移入一个单词，只需 O(1) 更新 Map。
 *
 * 复杂度分析：
 * - 时间复杂度：O(k * (n/k)) = O(n)。外层循环 k 次，内层指针总共扫描 s 一次。
 * - 空间复杂度：O(m * k)。
 */
function findSubstringOptimized(s: string, words: string[]): number[] {
  const result: number[] = []
  if (!s || words.length === 0) return result

  const wordLen = words[0].length
  const wordCount = words.length
  const totalLen = wordLen * wordCount
  const n = s.length

  if (n < totalLen) return result

  const wordMap = new Map<string, number>()
  for (const w of words) {
    wordMap.set(w, (wordMap.get(w) || 0) + 1)
  }

  // 分 k 组进行滑动窗口，i 是起始偏移量
  for (let i = 0; i < wordLen; i++) {
    let left = i
    let right = i
    const currentMap = new Map<string, number>()
    let count = 0 // 窗口内有效匹配的单词总数

    // 窗口右移，每次移动一个单词长度
    while (right + wordLen <= n) {
      // 1. 移入右边的单词
      const w = s.substring(right, right + wordLen)
      right += wordLen

      if (wordMap.has(w)) {
        currentMap.set(w, (currentMap.get(w) || 0) + 1)
        count++

        // 如果当前单词数量超标了，需要从左边收缩窗口，直到数量正常
        while (currentMap.get(w)! > wordMap.get(w)!) {
          const leftWord = s.substring(left, left + wordLen)
          currentMap.set(leftWord, currentMap.get(leftWord)! - 1)
          count--
          left += wordLen
        }

        // 如果匹配数量达标，记录结果
        if (count === wordCount) {
          result.push(left)
        }
      } else {
        // 如果遇到了不在 words 里的单词，当前窗口直接作废
        // 重置所有状态，从下一个位置开始
        currentMap.clear()
        count = 0
        left = right
      }
    }
  }

  return result
}

// --- 测试代码 ---
const s = 'barfoothefoobarman'
const words = ['foo', 'bar']
console.log('Input:', s, words)
console.log('Naive Solution:', findSubstring(s, words))
console.log('Optimized Solution:', findSubstringOptimized(s, words))

const s2 = 'wordgoodgoodgoodbestword'
const words2 = ['word', 'good', 'best', 'word']
console.log('\nInput:', s2, words2)
console.log('Naive Solution:', findSubstring(s2, words2))
console.log('Optimized Solution:', findSubstringOptimized(s2, words2))
