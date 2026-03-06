//  Definition for singly-linked list.
export class ListNode {
  val: number
  next: ListNode | null

  /**
   * 构造函数，用于创建链表节点
   * @param val 节点存储的数值
   * @param next 指向下一个节点的指针
   */
  constructor(val?: number, next?: ListNode | null) {
    this.val = val === undefined ? 0 : val
    this.next = next === undefined ? null : next
  }
}

/**
 * 方法一：使用两个虚拟头结点分别收集小于 x 与大于等于 x 的节点
 *
 * 思路说明：
 * - 遍历原链表，遇到节点值 < x，就挂在 small 链表尾部；否则挂在 big 链表尾部
 * - 遍历结束后，把 small 链表的尾部指向 big 链表的头部
 * - 注意将 big 链表的尾指针 next 置为 null，防止形成环
 * - 由于我们始终按出现顺序追加节点，两个分区内部的相对顺序会被保留
 *
 * 时间复杂度：O(n)，只需遍历一遍链表
 * 空间复杂度：O(1)，只使用常数级额外指针
 *
 * @param head 原链表的头结点
 * @param x 分隔值，小于 x 的节点需要出现在前面
 * @returns 新链表的头结点
 */
export function partition(head: ListNode | null, x: number): ListNode | null {
  const smallDummy = new ListNode(0)
  const bigDummy = new ListNode(0)

  let smallTail = smallDummy
  let bigTail = bigDummy

  let cur = head

  while (cur !== null) {
    if (cur.val < x) {
      // 当前节点值小于 x，追加到 small 链表尾部
      smallTail.next = cur
      smallTail = smallTail.next
    } else {
      // 当前节点值大于等于 x，追加到 big 链表尾部
      bigTail.next = cur
      bigTail = bigTail.next
    }
    // 提前保存的 next 已经被使用，将 cur 前进
    cur = cur.next
  }

  // big 链表尾结点的 next 必须断开，避免可能的旧指针形成环
  bigTail.next = null
  // small 链表尾部连接到 big 链表的头部
  smallTail.next = bigDummy.next

  return smallDummy.next
}

/**
 * 方法二：在原链表上“就地重排”，只用一个虚拟头结点
 *
 * 思路说明：
 * - 第一步：找到第一个值大于等于 x 的节点位置，之前的节点本身就属于 “小于 x” 部分
 *   - 用 lessTail 指向当前已经确定的 “小于 x” 部分的尾结点
 * - 第二步：从第一个 >= x 的节点开始往后扫：
 *   - 如果遇到节点值 < x：
 *     1. 从当前位置删除该节点
 *     2. 将该节点插入到 lessTail 的后面
 *     3. 更新 lessTail，使其始终指向 “小于 x” 部分的最后一个节点
 *   - 如果节点值 >= x，则直接后移指针继续扫描
 * - 整个过程中只移动 “小于 x” 的节点，而且移动顺序与它们在原链表中被发现的顺序一致
 *   因此可以保证两个分区内部的相对顺序不变
 *
 * 时间复杂度：O(n)，每个节点只会被访问与移动常数次
 * 空间复杂度：O(1)，使用有限个指针进行就地操作
 *
 * @param head 原链表的头结点
 * @param x 分隔值，小于 x 的节点需要出现在前面
 * @returns 新链表的头结点
 */
export function partitionInPlace(head: ListNode | null, x: number): ListNode | null {
  const dummy = new ListNode(0, head)

  let lessTail: ListNode = dummy
  let prev: ListNode = dummy
  let cur = head

  // 先找到第一个值大于等于 x 的节点，其前面的部分天然满足 “小于 x 在前”
  while (cur !== null && cur.val < x) {
    lessTail = cur
    prev = cur
    cur = cur.next
  }

  // 从第一个 >= x 的节点开始扫描后续节点
  while (cur !== null) {
    if (cur.val < x) {
      // 1. 从当前位置删除 cur 节点
      prev.next = cur.next

      // 2. 将 cur 插入到 lessTail 之后
      cur.next = lessTail.next
      lessTail.next = cur

      // 3. 更新 lessTail 指针
      lessTail = cur

      // 4. 继续从 prev 的下一个节点开始扫描
      cur = prev.next
    } else {
      // 当前节点已经属于 “大于等于 x” 部分，仅向后移动
      prev = cur
      cur = cur.next
    }
  }

  return dummy.next
}
