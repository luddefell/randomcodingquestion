"""Linked lists, trees, tries, heaps and class-design problems.
Linked lists and trees are written as lists in tests (trees in level order with
None for missing children) and converted by harness.py."""
import bisect, heapq
from collections import OrderedDict, deque
from common import lc, design, ex, t
from harness import ListNode, TreeNode, list_to_arr, build_list

# ============================ Linked List ============================

@lc("reverse-linked-list", "Reverse Linked List", "easy", "head: Optional[ListNode]", "Optional[ListNode]", topic="linked list", desc="""
Given the `head` of a singly linked list, reverse the list and return the new head.
""", tests=[ex([1, 2, 3, 4, 5], out=[5, 4, 3, 2, 1]), ex([1, 2], out=[2, 1]), ex([], out=[])])
def reverseList(head):
    prev = None
    while head:
        head.next, prev, head = prev, head, head.next
    return prev


@lc("merge-two-sorted-lists", "Merge Two Sorted Lists", "easy", "list1: Optional[ListNode], list2: Optional[ListNode]", "Optional[ListNode]", topic="linked list", desc="""
Merge two sorted linked lists into one sorted list by splicing their nodes together. Return the head of the merged list.
""", tests=[ex([1, 2, 4], [1, 3, 4], out=[1, 1, 2, 3, 4, 4]), ex([], [], out=[]), ex([], [0], out=[0]), t([5], [1, 2, 3])])
def mergeTwoLists(list1, list2):
    return build_list(sorted(list_to_arr(list1) + list_to_arr(list2)))


@lc("middle-of-the-linked-list", "Middle of the Linked List", "easy", "head: Optional[ListNode]", "Optional[ListNode]", topic="linked list", desc="""
Return the middle node of the linked list (the returned list runs from that node to the end). If there are two middle nodes, return the second one.
""", tests=[ex([1, 2, 3, 4, 5], out=[3, 4, 5]), ex([1, 2, 3, 4, 5, 6], out=[4, 5, 6]), t([1]), t([1, 2])])
def middleNode(head):
    slow = fast = head
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next
    return slow


@lc("palindrome-linked-list", "Palindrome Linked List", "easy", "head: Optional[ListNode]", "bool", topic="linked list", name="isPalindrome", desc="""
Return `True` if the linked list reads the same forward and backward. Can you do it in O(1) extra space?
""", tests=[ex([1, 2, 2, 1], out=True), ex([1, 2], out=False), t([1]), t([1, 2, 3, 2, 1]), t([1, 1, 2, 1])])
def isPalindromeList(head):
    a = list_to_arr(head)
    return a == a[::-1]


@lc("reorder-list", "Reorder List", "medium", "head: Optional[ListNode]", "None", inplace=0, topic="linked list", desc="""
Reorder the list `L0 → L1 → … → Ln` into `L0 → Ln → L1 → Ln-1 → L2 → …` by relinking nodes (don't just change values). Your function returns nothing; the checker reads the list from `head`.
""", tests=[ex([1, 2, 3, 4], out=[1, 4, 2, 3]), ex([1, 2, 3, 4, 5], out=[1, 5, 2, 4, 3]), t([1]), t([1, 2])])
def reorderList(head):
    nodes = []
    while head:
        nodes.append(head)
        head = head.next
    i, j = 0, len(nodes) - 1
    order = []
    while i <= j:
        order.append(nodes[i])
        if i != j:
            order.append(nodes[j])
        i += 1; j -= 1
    for a, b in zip(order, order[1:] + [None]):
        a.next = b


@lc("remove-nth-node-from-end-of-list", "Remove Nth Node From End of List", "medium", "head: Optional[ListNode], n: int", "Optional[ListNode]", topic="linked list", desc="""
Remove the `n`-th node from the end of the list and return its head. Try to do it in one pass.
""", tests=[ex([1, 2, 3, 4, 5], 2, out=[1, 2, 3, 5]), ex([1], 1, out=[]), ex([1, 2], 1, out=[1]), t([1, 2], 2)])
def removeNthFromEnd(head, n):
    a = list_to_arr(head)
    del a[len(a) - n]
    return build_list(a)


@lc("add-two-numbers", "Add Two Numbers", "medium", "l1: Optional[ListNode], l2: Optional[ListNode]", "Optional[ListNode]", topic="linked list", desc="""
Two non-negative integers are stored as linked lists with their digits in **reverse** order (one digit per node). Add them and return the sum as a linked list in the same format.
""", tests=[ex([2, 4, 3], [5, 6, 4], out=[7, 0, 8]), ex([0], [0], out=[0]), ex([9, 9, 9, 9, 9, 9, 9], [9, 9, 9, 9], out=[8, 9, 9, 9, 0, 0, 0, 1]), t([5], [5])])
def addTwoNumbers(l1, l2):
    num = lambda n: int("".join(map(str, reversed(list_to_arr(n)))))
    return build_list([int(c) for c in reversed(str(num(l1) + num(l2)))])


@lc("find-the-duplicate-number", "Find the Duplicate Number", "medium", "nums: List[int]", "int", topic="linked list", desc="""
`nums` has `n + 1` integers, each in `[1, n]`. Exactly one value repeats (possibly several times). Return it without modifying `nums` and using O(1) extra space. (Hint: think of `i → nums[i]` as a linked list.)
""", tests=[ex([1, 3, 4, 2, 2], out=2), ex([3, 1, 3, 4, 2], out=3), ex([3, 3, 3, 3, 3], out=3), t([1, 1]), t([2, 5, 9, 6, 9, 3, 8, 9, 7, 1])])
def findDuplicate(nums):
    seen = set()
    for x in nums:
        if x in seen:
            return x
        seen.add(x)


@lc("merge-k-sorted-lists", "Merge k Sorted Lists", "hard", "lists: List[Optional[ListNode]]", "Optional[ListNode]", topic="linked list", desc="""
Given an array of `k` sorted linked lists, merge them into one sorted linked list and return it.
""", tests=[ex([[1, 4, 5], [1, 3, 4], [2, 6]], out=[1, 1, 2, 3, 4, 4, 5, 6]), ex([], out=[]), ex([[]], out=[]), t([[5], [], [1, 2, 9], [3]])])
def mergeKLists(lists):
    return build_list(sorted(v for l in lists for v in list_to_arr(l)))


@lc("reverse-nodes-in-k-group", "Reverse Nodes in k-Group", "hard", "head: Optional[ListNode], k: int", "Optional[ListNode]", topic="linked list", desc="""
Reverse the nodes of the list `k` at a time and return the new head. If the number of remaining nodes at the end is less than `k`, leave them as they are. Only relink nodes; don't change their values.
""", tests=[ex([1, 2, 3, 4, 5], 2, out=[2, 1, 4, 3, 5]), ex([1, 2, 3, 4, 5], 3, out=[3, 2, 1, 4, 5]), t([1], 1), t([1, 2, 3, 4, 5, 6], 3), t([1, 2], 3)])
def reverseKGroup(head, k):
    a = list_to_arr(head)
    for i in range(0, len(a) - len(a) % k, k):
        a[i:i + k] = a[i:i + k][::-1]
    return build_list(a)


# ============================ Trees ============================

def _tree_arr(root):
    from harness import tree_to_arr
    return tree_to_arr(root)


@lc("invert-binary-tree", "Invert Binary Tree", "easy", "root: Optional[TreeNode]", "Optional[TreeNode]", topic="trees", desc="""
Invert a binary tree (mirror it left-to-right) and return its root. Trees are shown in level order, with `None` for missing children.
""", tests=[ex([4, 2, 7, 1, 3, 6, 9], out=[4, 7, 2, 9, 6, 3, 1]), ex([2, 1, 3], out=[2, 3, 1]), ex([], out=[]), t([1, 2])])
def invertTree(root):
    if root:
        root.left, root.right = invertTree(root.right), invertTree(root.left)
    return root


@lc("maximum-depth-of-binary-tree", "Maximum Depth of Binary Tree", "easy", "root: Optional[TreeNode]", "int", topic="trees", desc="""
Return the maximum depth of a binary tree: the number of nodes on the longest path from the root down to a leaf.
""", tests=[ex([3, 9, 20, None, None, 15, 7], out=3), ex([1, None, 2], out=2), t([]), t([1, 2, None, 3, None, 4])])
def maxDepth(root):
    return 1 + max(maxDepth(root.left), maxDepth(root.right)) if root else 0


@lc("diameter-of-binary-tree", "Diameter of Binary Tree", "easy", "root: Optional[TreeNode]", "int", topic="trees", desc="""
Return the length (in edges) of the longest path between any two nodes in the tree. The path may or may not pass through the root.
""", tests=[ex([1, 2, 3, 4, 5], out=3), ex([1, 2], out=1), t([1]), t([1, 2, None, 3, 4, 5, None, None, 6])])
def diameterOfBinaryTree(root):
    best = 0
    def h(n):
        nonlocal best
        if not n:
            return 0
        l, r = h(n.left), h(n.right)
        best = max(best, l + r)
        return 1 + max(l, r)
    h(root)
    return best


@lc("balanced-binary-tree", "Balanced Binary Tree", "easy", "root: Optional[TreeNode]", "bool", topic="trees", desc="""
Return `True` if the tree is height-balanced: for every node, the heights of its two subtrees differ by at most one.
""", tests=[ex([3, 9, 20, None, None, 15, 7], out=True), ex([1, 2, 2, 3, 3, None, None, 4, 4], out=False), ex([], out=True), t([1, None, 2, None, 3])])
def isBalanced(root):
    def h(n):
        if not n:
            return 0
        l, r = h(n.left), h(n.right)
        return -1 if l < 0 or r < 0 or abs(l - r) > 1 else 1 + max(l, r)
    return h(root) >= 0


@lc("same-tree", "Same Tree", "easy", "p: Optional[TreeNode], q: Optional[TreeNode]", "bool", topic="trees", desc="""
Return `True` if trees `p` and `q` have the same structure and the same node values.
""", tests=[ex([1, 2, 3], [1, 2, 3], out=True), ex([1, 2], [1, None, 2], out=False), ex([1, 2, 1], [1, 1, 2], out=False), t([], [])])
def isSameTree(p, q):
    return _tree_arr(p) == _tree_arr(q)


@lc("subtree-of-another-tree", "Subtree of Another Tree", "easy", "root: Optional[TreeNode], subRoot: Optional[TreeNode]", "bool", topic="trees", desc="""
Return `True` if `subRoot` appears in `root` as a subtree: some node of `root` together with **all** of its descendants matches `subRoot` exactly.
""", tests=[ex([3, 4, 5, 1, 2], [4, 1, 2], out=True), ex([3, 4, 5, 1, 2, None, None, None, None, 0], [4, 1, 2], out=False), t([1, 1], [1]), t([1, 2, 3], [1, 2])])
def isSubtree(root, subRoot):
    target = _tree_arr(subRoot)
    stack = [root]
    while stack:
        n = stack.pop()
        if n:
            if _tree_arr(n) == target:
                return True
            stack += [n.left, n.right]
    return False


@lc("binary-tree-level-order-traversal", "Binary Tree Level Order Traversal", "medium", "root: Optional[TreeNode]", "List[List[int]]", topic="trees", desc="""
Return the level order traversal of the tree's values: a list of levels, each read left to right.
""", tests=[ex([3, 9, 20, None, None, 15, 7], out=[[3], [9, 20], [15, 7]]), ex([1], out=[[1]]), ex([], out=[]), t([1, 2, 3, 4, None, None, 5])])
def levelOrder(root):
    res, level = [], [root] if root else []
    while level:
        res.append([n.val for n in level])
        level = [c for n in level for c in (n.left, n.right) if c]
    return res


@lc("binary-tree-right-side-view", "Binary Tree Right Side View", "medium", "root: Optional[TreeNode]", "List[int]", topic="trees", desc="""
Imagine standing on the right side of the tree. Return the values of the nodes you can see, ordered from top to bottom.
""", tests=[ex([1, 2, 3, None, 5, None, 4], out=[1, 3, 4]), ex([1, None, 3], out=[1, 3]), ex([], out=[]), t([1, 2, 3, 4])])
def rightSideView(root):
    return [lvl[-1] for lvl in levelOrder(root)]


@lc("count-good-nodes-in-binary-tree", "Count Good Nodes in Binary Tree", "medium", "root: TreeNode", "int", topic="trees", desc="""
A node is **good** if no node on the path from the root to it has a greater value. Return the number of good nodes.
""", tests=[ex([3, 1, 4, 3, None, 1, 5], out=4), ex([3, 3, None, 4, 2], out=3), ex([1], out=1), t([2, None, 4, 10, 8, None, None, 4])])
def goodNodes(root):
    def go(n, m):
        if not n:
            return 0
        return (n.val >= m) + go(n.left, max(m, n.val)) + go(n.right, max(m, n.val))
    return go(root, root.val)


@lc("validate-binary-search-tree", "Validate Binary Search Tree", "medium", "root: Optional[TreeNode]", "bool", topic="trees", desc="""
Return `True` if the tree is a valid binary search tree: every node's left subtree holds only smaller values, its right subtree only larger values, and both subtrees are BSTs.
""", tests=[ex([2, 1, 3], out=True), ex([5, 1, 4, None, None, 3, 6], out=False), t([5, 4, 6, None, None, 3, 7]), t([2, 2, 2]), t([1])])
def isValidBST(root):
    def go(n, lo, hi):
        return not n or (lo < n.val < hi and go(n.left, lo, n.val) and go(n.right, n.val, hi))
    return go(root, float("-inf"), float("inf"))


@lc("kth-smallest-element-in-a-bst", "Kth Smallest Element in a BST", "medium", "root: Optional[TreeNode], k: int", "int", topic="trees", desc="""
Given the root of a binary search tree and an integer `k`, return the `k`-th smallest value (1-indexed) in the tree.
""", tests=[ex([3, 1, 4, None, 2], 1, out=1), ex([5, 3, 6, 2, 4, None, None, 1], 3, out=3), t([1], 1), t([5, 3, 6, 2, 4, None, None, 1], 6)])
def kthSmallest(root, k):
    vals = []
    def go(n):
        if n:
            go(n.left); vals.append(n.val); go(n.right)
    go(root)
    return vals[k - 1]


@lc("construct-binary-tree-from-preorder-and-inorder-traversal", "Construct Binary Tree from Preorder and Inorder Traversal", "medium",
    "preorder: List[int], inorder: List[int]", "Optional[TreeNode]", topic="trees", desc="""
Given the `preorder` and `inorder` traversals of a binary tree with unique values, build and return the tree.
""", tests=[ex([3, 9, 20, 15, 7], [9, 3, 15, 20, 7], out=[3, 9, 20, None, None, 15, 7]), ex([-1], [-1], out=[-1]), t([1, 2], [2, 1]), t([1, 2, 4, 5, 3, 6], [4, 2, 5, 1, 6, 3])])
def buildTree(preorder, inorder):
    if not preorder:
        return None
    i = inorder.index(preorder[0])
    return TreeNode(preorder[0], buildTree(preorder[1:i + 1], inorder[:i]), buildTree(preorder[i + 1:], inorder[i + 1:]))


@lc("binary-tree-maximum-path-sum", "Binary Tree Maximum Path Sum", "hard", "root: Optional[TreeNode]", "int", topic="trees", desc="""
A path is a sequence of nodes where each adjacent pair is connected by an edge; it doesn't have to pass through the root. Return the maximum sum of node values over all non-empty paths.
""", tests=[ex([1, 2, 3], out=6), ex([-10, 9, 20, None, None, 15, 7], out=42), t([-3]), t([2, -1]), t([5, 4, 8, 11, None, 13, 4, 7, 2, None, None, None, 1])])
def maxPathSum(root):
    best = float("-inf")
    def go(n):
        nonlocal best
        if not n:
            return 0
        l, r = max(go(n.left), 0), max(go(n.right), 0)
        best = max(best, n.val + l + r)
        return n.val + max(l, r)
    go(root)
    return best


# ============================ Heap / Priority Queue ============================

@lc("last-stone-weight", "Last Stone Weight", "easy", "stones: List[int]", "int", topic="heap", desc="""
Each turn, smash the two heaviest stones `x <= y` together: if equal both are destroyed, otherwise a stone of weight `y - x` remains. Return the weight of the last remaining stone, or `0` if none remain.
""", tests=[ex([2, 7, 4, 1, 8, 1], out=1), ex([1], out=1), t([2, 2]), t([10, 4, 2, 10])])
def lastStoneWeight(stones):
    h = [-s for s in stones]
    heapq.heapify(h)
    while len(h) > 1:
        y, x = -heapq.heappop(h), -heapq.heappop(h)
        if y != x:
            heapq.heappush(h, x - y)
    return -h[0] if h else 0


@lc("k-closest-points-to-origin", "K Closest Points to Origin", "medium", "points: List[List[int]], k: int", "List[List[int]]", cmp="any", topic="heap", desc="""
Return the `k` points closest to the origin `(0, 0)` by Euclidean distance, in any order. The answer is unique.
""", tests=[ex([[1, 3], [-2, 2]], 1, out=[[-2, 2]]), ex([[3, 3], [5, -1], [-2, 4]], 2, out=[[3, 3], [-2, 4]]), t([[0, 1], [1, 0], [5, 5]], 2), t([[1, 1]], 1)])
def kClosest(points, k):
    return sorted(points, key=lambda p: p[0] ** 2 + p[1] ** 2)[:k]


@lc("kth-largest-element-in-an-array", "Kth Largest Element in an Array", "medium", "nums: List[int], k: int", "int", topic="heap", desc="""
Return the `k`-th largest element in `nums` (in sorted order, not the k-th distinct). Can you do it without sorting?
""", tests=[ex([3, 2, 1, 5, 6, 4], 2, out=5), ex([3, 2, 3, 1, 2, 4, 5, 5, 6], 4, out=4), t([1], 1), t([-1, -1], 2)])
def findKthLargest(nums, k):
    return heapq.nlargest(k, nums)[-1]


@lc("task-scheduler", "Task Scheduler", "medium", "tasks: List[str], n: int", "int", topic="heap", desc="""
A CPU runs one task per interval, or stays idle. Identical tasks (same letter) must be at least `n` intervals apart. Return the minimum number of intervals needed to finish all `tasks`.
""", tests=[ex(["A", "A", "A", "B", "B", "B"], 2, out=8), ex(["A", "C", "A", "B", "D", "B"], 1, out=6), ex(["A", "A", "A", "B", "B", "B"], 3, out=10), t(["A"], 5)])
def leastInterval(tasks, n):
    from collections import Counter
    c = Counter(tasks).values()
    m = max(c)
    return max(len(tasks), (m - 1) * (n + 1) + sum(1 for v in c if v == m))


# ============================ Design ============================

@design("min-stack", "Min Stack", "medium",
        ["__init__(self)", "push(self, val: int) -> None", "pop(self) -> None", "top(self) -> int", "getMin(self) -> int"], topic="stack", desc="""
Design a stack that supports `push`, `pop`, `top`, and retrieving the minimum element, all in O(1) time.

Tests are a list of method calls and their arguments, starting with the constructor; the expected output lists each call's return value (`None` for methods that return nothing).
""", tests=[ex(["MinStack", "push", "push", "push", "getMin", "pop", "top", "getMin"], [[], [-2], [0], [-3], [], [], [], []],
                out=[None, None, None, None, -3, None, 0, -2]),
            t(["MinStack", "push", "push", "getMin", "push", "getMin", "pop", "getMin", "top"], [[], [5], [5], [], [7], [], [], [], []])])
class MinStack:
    def __init__(self):
        self.s = []
    def push(self, val):
        self.s.append((val, min(val, self.s[-1][1]) if self.s else val))
    def pop(self):
        self.s.pop()
    def top(self):
        return self.s[-1][0]
    def getMin(self):
        return self.s[-1][1]


@design("time-based-key-value-store", "Time Based Key-Value Store", "medium",
        ["__init__(self)", "set(self, key: str, value: str, timestamp: int) -> None", "get(self, key: str, timestamp: int) -> str"], topic="binary search", desc="""
Design a key-value store where each key can hold several values at different timestamps.

- `set(key, value, timestamp)` stores `value` for `key` at `timestamp`. Timestamps for `set` are strictly increasing.
- `get(key, timestamp)` returns the value set for `key` at the largest timestamp `<= timestamp`, or `""` if there is none.
""", tests=[ex(["TimeMap", "set", "get", "get", "set", "get", "get"], [[], ["foo", "bar", 1], ["foo", 1], ["foo", 3], ["foo", "bar2", 4], ["foo", 4], ["foo", 5]],
                out=[None, None, "bar", "bar", None, "bar2", "bar2"]),
            t(["TimeMap", "get", "set", "get", "get", "set", "get"], [[], ["a", 1], ["a", "x", 5], ["a", 4], ["a", 5], ["b", "y", 6], ["b", 100]])])
class TimeMap:
    def __init__(self):
        self.d = {}
    def set(self, key, value, timestamp):
        self.d.setdefault(key, []).append((timestamp, value))
    def get(self, key, timestamp):
        arr = self.d.get(key, [])
        i = bisect.bisect_right(arr, (timestamp, chr(0x10FFFF)))
        return arr[i - 1][1] if i else ""


@design("lru-cache", "LRU Cache", "medium",
        ["__init__(self, capacity: int)", "get(self, key: int) -> int", "put(self, key: int, value: int) -> None"], topic="linked list", desc="""
Design a Least Recently Used cache with a positive `capacity`.

- `get(key)` returns the value if `key` exists, else `-1`.
- `put(key, value)` inserts or updates the key. If this exceeds the capacity, evict the least recently used key.

Both should run in O(1) average time. A `get` or `put` counts as using the key.
""", tests=[ex(["LRUCache", "put", "put", "get", "put", "get", "put", "get", "get", "get"], [[2], [1, 1], [2, 2], [1], [3, 3], [2], [4, 4], [1], [3], [4]],
                out=[None, None, None, 1, None, -1, None, -1, 3, 4]),
            t(["LRUCache", "put", "put", "put", "get", "put", "get", "get"], [[1], [1, 1], [1, 5], [2, 2], [1], [3, 3], [2], [3]])])
class LRUCache:
    def __init__(self, capacity):
        self.cap, self.d = capacity, OrderedDict()
    def get(self, key):
        if key not in self.d:
            return -1
        self.d.move_to_end(key)
        return self.d[key]
    def put(self, key, value):
        self.d[key] = value
        self.d.move_to_end(key)
        if len(self.d) > self.cap:
            self.d.popitem(last=False)


@design("implement-trie-prefix-tree", "Implement Trie (Prefix Tree)", "medium",
        ["__init__(self)", "insert(self, word: str) -> None", "search(self, word: str) -> bool", "startsWith(self, prefix: str) -> bool"], topic="tries", desc="""
Implement a trie with `insert(word)`, `search(word)` (was this exact word inserted?) and `startsWith(prefix)` (was any inserted word starting with `prefix`?).
""", tests=[ex(["Trie", "insert", "search", "search", "startsWith", "insert", "search"], [[], ["apple"], ["apple"], ["app"], ["app"], ["app"], ["app"]],
                out=[None, None, True, False, True, None, True]),
            t(["Trie", "insert", "insert", "search", "startsWith", "startsWith", "search"], [[], ["car"], ["card"], ["ca"], ["ca"], ["cart"], ["card"]])])
class Trie:
    def __init__(self):
        self.words = set()
    def insert(self, word):
        self.words.add(word)
    def search(self, word):
        return word in self.words
    def startsWith(self, prefix):
        return any(w.startswith(prefix) for w in self.words)


@design("design-add-and-search-words-data-structure", "Design Add and Search Words Data Structure", "medium",
        ["__init__(self)", "addWord(self, word: str) -> None", "search(self, word: str) -> bool"], topic="tries", desc="""
Design a structure that supports adding words and searching for them, where the search pattern may contain `.` to match any single letter.
""", tests=[ex(["WordDictionary", "addWord", "addWord", "addWord", "search", "search", "search", "search"],
                [[], ["bad"], ["dad"], ["mad"], ["pad"], ["bad"], [".ad"], ["b.."]], out=[None, None, None, None, False, True, True, True]),
            t(["WordDictionary", "addWord", "search", "search", "search", "addWord", "search"], [[], ["a"], ["."], [".."], ["a"], ["ab"], [".b"]])])
class WordDictionary:
    def __init__(self):
        self.words = []
    def addWord(self, word):
        self.words.append(word)
    def search(self, word):
        import re
        return any(re.fullmatch(word, w) for w in self.words)


@design("kth-largest-element-in-a-stream", "Kth Largest Element in a Stream", "easy",
        ["__init__(self, k: int, nums: List[int])", "add(self, val: int) -> int"], topic="heap", desc="""
Design a class that tracks the `k`-th largest score in a stream. The constructor receives `k` and the initial `nums`; `add(val)` adds a score and returns the current `k`-th largest.
""", tests=[ex(["KthLargest", "add", "add", "add", "add", "add"], [[3, [4, 5, 8, 2]], [3], [5], [10], [9], [4]], out=[None, 4, 5, 5, 8, 8]),
            t(["KthLargest", "add", "add", "add"], [[1, []], [-3], [-2], [-4]])])
class KthLargest:
    def __init__(self, k, nums):
        self.k, self.h = k, heapq.nlargest(k, nums)
        heapq.heapify(self.h)
    def add(self, val):
        heapq.heappush(self.h, val)
        if len(self.h) > self.k:
            heapq.heappop(self.h)
        return self.h[0]


@design("find-median-from-data-stream", "Find Median from Data Stream", "hard",
        ["__init__(self)", "addNum(self, num: int) -> None", "findMedian(self) -> float"], topic="heap", desc="""
Design a structure that receives numbers one at a time and can return the median of everything seen so far. For an even count, the median is the mean of the two middle values.
""", tests=[ex(["MedianFinder", "addNum", "addNum", "findMedian", "addNum", "findMedian"], [[], [1], [2], [], [3], []], out=[None, None, None, 1.5, None, 2.0]),
            t(["MedianFinder", "addNum", "findMedian", "addNum", "findMedian", "addNum", "findMedian", "addNum", "findMedian"], [[], [-1], [], [-2], [], [-3], [], [-4], []])])
class MedianFinder:
    def __init__(self):
        self.a = []
    def addNum(self, num):
        bisect.insort(self.a, num)
    def findMedian(self):
        n = len(self.a)
        return float(self.a[n // 2]) if n % 2 else (self.a[n // 2 - 1] + self.a[n // 2]) / 2
