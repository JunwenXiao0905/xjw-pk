# 字母异位词分组算法笔记

## 题目描述
给你一个字符串数组，请你将 **字母异位词** 组合在一起。可以按任意顺序返回结果列表。
**字母异位词** 是指由相同的字母重排列形成的字符串（包括相同的字符）。

**示例**：
```typescript
输入: strs = ["eat", "tea", "tan", "ate", "nat", "bat"]
输出: [["bat"],["nat","tan"],["ate","eat","tea"]]
```

## 核心思路
核心在于找到一个 **“唯一标识（Key）”**，使得所有属于同一组的异位词，生成的 Key 都是一样的。

---

## 解法一：排序法 (Sorting)

### 原理
将每个字符串按字母顺序排序。
例如：`"eat"`, `"tea"`, `"ate"` 排序后都变成 `"aet"`。
以此作为 Map 的 Key。

### 代码实现
```typescript
function groupAnagramsSort(strs: string[]): string[][] {
  const map = new Map<string, string[]>();
  
  for (const s of strs) {
    // 关键点：排序作为 Key
    // 注意：默认 sort() 按字符编码排序，大写字母会排在小写字母前
    const key = s.split('').sort().join('');
    
    if (map.has(key)) {
      map.get(key)!.push(s);
    } else {
      map.set(key, [s]);
    }
  }
  
  return Array.from(map.values());
}
```

### 复杂度分析
*   **时间复杂度**: $O(nk \log k)$
    *   $n$: 字符串数组长度
    *   $k$: 字符串的最大长度
    *   主要耗时在 `sort()` 操作，通常为 $O(k \log k)$，共执行 $n$ 次。
*   **空间复杂度**: $O(nk)$
    *   需要存储所有字符串分组。

---

## 解法二：计数法 (Counting)

### 原理
统计每个字符串中各字母出现的次数。
例如：`"abb"` 统计为 `a:1, b:2`，生成 Key 如 `"1#2#0#0..."`（对应 a-z 的计数）。

### 代码实现
```typescript
function groupAnagramsCount(strs: string[]): string[][] {
  const map = new Map<string, string[]>();

  for (const s of strs) {
    // 统计 26 个字母的出现频率
    const count = new Array(26).fill(0);
    for (const char of s) {
      count[char.charCodeAt(0) - 97]++; // 'a' 的 ASCII 是 97
    }
    
    // 将计数数组转为字符串 Key
    // 技巧：加分隔符避免混淆，或直接 join (如 '1,0,2...')
    const key = count.join('#');
    
    if (map.has(key)) {
      map.get(key)!.push(s);
    } else {
      map.set(key, [s]);
    }
  }
  
  return Array.from(map.values());
}
```

### 复杂度分析
*   **时间复杂度**: $O(nk)$
    *   不需要排序，只需要遍历每个字符串的每个字符。
    *   当 $k$（字符串长度）很大时，此方法优于排序法。
*   **空间复杂度**: $O(nk)$
    *   同上，加上 Key 的存储开销。

---

## 常见问题 Q&A

### 1. 数组的 `sort()` 默认怎么排？
*   如果不传比较函数，默认将元素转为字符串，按 **UTF-16 代码单元值**（类似 ASCII）排序。
*   **注意**：`"B"` (66) 会排在 `"a"` (97) 前面。如果题目不保证全小写，需先 `.toLowerCase()`。

### 2. `[""]` 是空数组吗？
*   不是。`[""]` 长度为 1，包含一个空字符串。
*   算法会将其作为一组处理，输出 `[[""]]`。
*   `[]` 才是空数组，长度为 0。

### 3. 为什么题目限制 `1 <= strs.length`？
*   这是对输入的保证（Constraint），意味着你不需要处理输入为 `[]` 的情况，也不需要写 `if (strs.length === 0)` 这样的防御性代码。
