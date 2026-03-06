// 字母异位词分组

// 解法一：排序法
function groupAnagramsSort(strs: string[]): string[][] {
  // 边界情况：""、有大写字母、字符串长度检测
  if (strs.length === 0) return []

  // 情形1：strs = ["eat", "tea", "tan", "ate", "nat", "bat"]
  // 思路：提取每一个字符串的字母，进行排序，作为key。如果两个字符串排序后相同，说明是异位词。
  // 时间复杂度：O(nk log k)；计算复杂度：O(nk)；
  const map = new Map<string, string[]>()

  for (const s of strs) {
    // 将字符串转为数组 -> 排序 -> 转回字符串，作为唯一标识
    const key = s.split('').sort().join('')

    if (map.has(key)) {
      map.get(key)!.push(s)
    } else {
      map.set(key, [s])
    }
  }

  return Array.from(map.values())
}

// 解法二：计数法
function groupAnagramsCount(strs: string[]): string[][] {
  // 边界情况：""、有大写字母、字符串长度检测
  if (strs.length === 0) return []

  // 情形1：strs = ["eat", "tea", "tan", "ate", "nat", "bat"]
  // 思路：利用计数数组统计每个字符出现次数，将其转化为字符串作为key。
  // 时间复杂度：O(nk)；计算复杂度：O(nk)；
  const map = new Map<string, string[]>()

  for (const s of strs) {
    const count = new Array(26).fill(0)
    for (const char of s) {
      // 假设都是小写字母
      count[char.charCodeAt(0) - 'a'.charCodeAt(0)]++
    }
    // 使用特定分隔符或直接转字符串作为key，例如 1#0#2#...
    const key = count.join('#')

    if (map.has(key)) {
      map.get(key)!.push(s)
    } else {
      map.set(key, [s])
    }
  }

  return Array.from(map.values())
}

// --- 测试代码 ---
console.log('=== 排序测试 ===')
const s1 = 'aBc'
const s2 = 'abc'
console.log(`"${s1}" sorted: "${s1.split('').sort().join('')}"`)
console.log(`"${s2}" sorted: "${s2.split('').sort().join('')}"`)
console.log(`Is same? ${s1.split('').sort().join('') === s2.split('').sort().join('')}`)

console.log('\n=== 算法测试 ===')
const input = ['eat', 'tea', 'tan', 'ate', 'nat', 'bat']
console.log('Input:', input)
console.log('Sort Method Output:', groupAnagramsSort(input))
console.log('Count Method Output:', groupAnagramsCount(input))
