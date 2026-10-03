"""Arrays & hashing, two pointers, sliding window, stack, binary search,
intervals, greedy, math & bit manipulation."""
import heapq
from collections import Counter, defaultdict, deque
from common import lc, ex, t

# ============================ Arrays & Hashing ============================

@lc("contains-duplicate", "Contains Duplicate", "easy", "nums: List[int]", "bool", topic="arrays", desc="""
Given an integer array `nums`, return `True` if any value appears at least twice, and `False` if every element is distinct.
""", tests=[ex([1, 2, 3, 1], out=True), ex([1, 2, 3, 4], out=False), ex([1, 1, 1, 3, 3, 4, 3, 2, 4, 2], out=True),
            t([]), t([7]), t([-1, 5, -1])])
def containsDuplicate(nums):
    return len(set(nums)) != len(nums)


@lc("valid-anagram", "Valid Anagram", "easy", "s: str, t: str", "bool", topic="arrays", desc="""
Given two strings `s` and `t`, return `True` if `t` is an anagram of `s` (same letters, same counts, any order).
""", tests=[ex("anagram", "nagaram", out=True), ex("rat", "car", out=False), t("a", "ab"), t("", ""), t("aacc", "ccac")])
def isAnagram(s, t):
    return Counter(s) == Counter(t)


@lc("two-sum", "Two Sum", "easy", "nums: List[int], target: int", "List[int]", cmp="any", topic="arrays", desc="""
Given an array of integers `nums` and an integer `target`, return the indices of the two numbers that add up to `target`.

Exactly one solution exists, and you may not use the same element twice. Return the indices in any order.
""", tests=[ex([2, 7, 11, 15], 9, out=[0, 1]), ex([3, 2, 4], 6, out=[1, 2]), ex([3, 3], 6, out=[0, 1]),
            t([-1, -2, -3, -4, -5], -8), t([0, 4, 3, 0], 0)])
def twoSum(nums, target):
    seen = {}
    for i, x in enumerate(nums):
        if target - x in seen:
            return [seen[target - x], i]
        seen[x] = i


@lc("group-anagrams", "Group Anagrams", "medium", "strs: List[str]", "List[List[str]]", cmp="anyDeep", topic="arrays", desc="""
Given a list of strings `strs`, group the anagrams together. Return the groups in any order; the order inside each group doesn't matter either.
""", tests=[ex(["eat", "tea", "tan", "ate", "nat", "bat"], out=[["bat"], ["nat", "tan"], ["ate", "eat", "tea"]]),
            ex([""], out=[[""]]), ex(["a"], out=[["a"]]), t(["abc", "bca", "cab", "xyz", "zyx", "q"])])
def groupAnagrams(strs):
    g = defaultdict(list)
    for s in strs:
        g["".join(sorted(s))].append(s)
    return list(g.values())


@lc("top-k-frequent-elements", "Top K Frequent Elements", "medium", "nums: List[int], k: int", "List[int]", cmp="any", topic="arrays", desc="""
Given an integer array `nums` and an integer `k`, return the `k` most frequent elements, in any order. The answer is guaranteed to be unique.
""", tests=[ex([1, 1, 1, 2, 2, 3], 2, out=[1, 2]), ex([1], 1, out=[1]), t([4, 4, 4, 5, 5, 6, 6, 6, 6, 7], 2), t([-1, -1, 2], 1)])
def topKFrequent(nums, k):
    return [x for x, _ in Counter(nums).most_common(k)]


@lc("product-of-array-except-self", "Product of Array Except Self", "medium", "nums: List[int]", "List[int]", topic="arrays", desc="""
Return an array `answer` where `answer[i]` is the product of all elements of `nums` except `nums[i]`.

Solve it in O(n) time without using division.
""", tests=[ex([1, 2, 3, 4], out=[24, 12, 8, 6]), ex([-1, 1, 0, -3, 3], out=[0, 0, 9, 0, 0]), t([2, 3]), t([0, 0, 5])])
def productExceptSelf(nums):
    n = len(nums)
    res = [1] * n
    for i in range(1, n):
        res[i] = res[i - 1] * nums[i - 1]
    suffix = 1
    for i in range(n - 1, -1, -1):
        res[i] *= suffix
        suffix *= nums[i]
    return res


_SUDOKU = [["5", "3", ".", ".", "7", ".", ".", ".", "."], ["6", ".", ".", "1", "9", "5", ".", ".", "."],
           [".", "9", "8", ".", ".", ".", ".", "6", "."], ["8", ".", ".", ".", "6", ".", ".", ".", "3"],
           ["4", ".", ".", "8", ".", "3", ".", ".", "1"], ["7", ".", ".", ".", "2", ".", ".", ".", "6"],
           [".", "6", ".", ".", ".", ".", "2", "8", "."], [".", ".", ".", "4", "1", "9", ".", ".", "5"],
           [".", ".", ".", ".", "8", ".", ".", "7", "9"]]
_SUDOKU_BAD = [["8"] + r[1:] if i == 0 else r for i, r in enumerate(_SUDOKU)]
_SUDOKU_BOX = [r[:] for r in _SUDOKU]
_SUDOKU_BOX[1][1] = "9"


@lc("valid-sudoku", "Valid Sudoku", "medium", "board: List[List[str]]", "bool", examples=1, topic="arrays", desc="""
Determine if a 9 x 9 Sudoku `board` is valid. Only the filled cells need to be validated:

- Each row contains the digits 1-9 without repetition.
- Each column contains the digits 1-9 without repetition.
- Each of the nine 3 x 3 boxes contains the digits 1-9 without repetition.

Empty cells are `"."`. The board does not need to be solvable.
""", tests=[ex(_SUDOKU, out=True), ex(_SUDOKU_BAD, out=False), t(_SUDOKU_BOX)])
def isValidSudoku(board):
    seen = set()
    for r in range(9):
        for c in range(9):
            v = board[r][c]
            if v == ".":
                continue
            keys = [(r, "r", v), ("c", c, v), (r // 3, c // 3, v)]
            if any(k in seen for k in keys):
                return False
            seen.update(keys)
    return True


@lc("longest-consecutive-sequence", "Longest Consecutive Sequence", "medium", "nums: List[int]", "int", topic="arrays", desc="""
Given an unsorted array of integers `nums`, return the length of the longest run of consecutive integers (e.g. 4, 5, 6, 7). Aim for O(n).
""", tests=[ex([100, 4, 200, 1, 3, 2], out=4), ex([0, 3, 7, 2, 5, 8, 4, 6, 0, 1], out=9), t([]), t([1, 2, 0, 1]), t([9, -1, -2, 10])])
def longestConsecutive(nums):
    s, best = set(nums), 0
    for x in s:
        if x - 1 not in s:
            y = x
            while y + 1 in s:
                y += 1
            best = max(best, y - x + 1)
    return best


@lc("concatenation-of-array", "Concatenation of Array", "easy", "nums: List[int]", "List[int]", topic="arrays", desc="""
Return an array `ans` of length `2n` where `ans[i] == nums[i]` and `ans[i + n] == nums[i]`.
""", tests=[ex([1, 2, 1], out=[1, 2, 1, 1, 2, 1]), ex([1, 3, 2, 1], out=[1, 3, 2, 1, 1, 3, 2, 1]), t([7])])
def getConcatenation(nums):
    return nums + nums


@lc("replace-elements-with-greatest-element-on-right-side", "Replace Elements with Greatest Element on Right Side", "easy",
    "arr: List[int]", "List[int]", topic="arrays", desc="""
Replace every element in `arr` with the greatest element among the elements to its right, and replace the last element with `-1`. Return the array.
""", tests=[ex([17, 18, 5, 4, 6, 1], out=[18, 6, 6, 6, 1, -1]), ex([400], out=[-1]), t([1, 2, 3])])
def replaceElements(arr):
    res, m = [0] * len(arr), -1
    for i in range(len(arr) - 1, -1, -1):
        res[i] = m
        m = max(m, arr[i])
    return res


@lc("longest-common-prefix", "Longest Common Prefix", "easy", "strs: List[str]", "str", topic="arrays", desc="""
Return the longest common prefix shared by every string in `strs`. If there is none, return `""`.
""", tests=[ex(["flower", "flow", "flight"], out="fl"), ex(["dog", "racecar", "car"], out=""), t(["alone"]), t(["", ""]), t(["ab", "a"])])
def longestCommonPrefix(strs):
    p = strs[0]
    for s in strs:
        while not s.startswith(p):
            p = p[:-1]
    return p


@lc("majority-element", "Majority Element", "easy", "nums: List[int]", "int", topic="arrays", desc="""
Return the element of `nums` that appears more than `⌊n / 2⌋` times. It always exists. Can you do it in O(1) extra space?
""", tests=[ex([3, 2, 3], out=3), ex([2, 2, 1, 1, 1, 2, 2], out=2), t([5]), t([6, 5, 5])])
def majorityElement(nums):
    return Counter(nums).most_common(1)[0][0]


@lc("length-of-last-word", "Length of Last Word", "easy", "s: str", "int", topic="arrays", desc="""
Given a string `s` of words and spaces, return the length of the last word. A word is a maximal run of non-space characters.
""", tests=[ex("Hello World", out=5), ex("   fly me   to   the moon  ", out=4), ex("luffy is still joyboy", out=6), t("a")])
def lengthOfLastWord(s):
    return len(s.split()[-1])


@lc("sort-colors", "Sort Colors", "medium", "nums: List[int]", "None", inplace=0, topic="arrays", desc="""
`nums` contains only `0`, `1` and `2` (red, white, blue). Sort it **in place** so equal colors are adjacent, in the order 0, 1, 2. Don't use the library sort. Your function returns nothing; the checker inspects `nums`.
""", tests=[ex([2, 0, 2, 1, 1, 0], out=[0, 0, 1, 1, 2, 2]), ex([2, 0, 1], out=[0, 1, 2]), t([0]), t([1, 1, 0, 2, 2, 1, 0])])
def sortColors(nums):
    nums.sort()


# ============================ Two Pointers ============================

@lc("valid-palindrome", "Valid Palindrome", "easy", "s: str", "bool", topic="two pointers", desc="""
A phrase is a palindrome if, after lowercasing and removing all non-alphanumeric characters, it reads the same forward and backward. Return `True` if `s` is a palindrome.
""", tests=[ex("A man, a plan, a canal: Panama", out=True), ex("race a car", out=False), ex(" ", out=True), t("0P"), t("Was it a car or a cat I saw?")])
def isPalindrome(s):
    c = [ch.lower() for ch in s if ch.isalnum()]
    return c == c[::-1]


@lc("two-sum-ii-input-array-is-sorted", "Two Sum II - Input Array Is Sorted", "medium", "numbers: List[int], target: int", "List[int]", topic="two pointers", name="twoSum", desc="""
`numbers` is sorted in non-decreasing order. Find two numbers that add up to `target` and return their **1-indexed** positions `[index1, index2]` with `index1 < index2`. Exactly one solution exists. Use O(1) extra space.
""", tests=[ex([2, 7, 11, 15], 9, out=[1, 2]), ex([2, 3, 4], 6, out=[1, 3]), ex([-1, 0], -1, out=[1, 2]), t([1, 2, 3, 4, 4, 9, 56, 90], 8)])
def twoSumII(numbers, target):
    l, r = 0, len(numbers) - 1
    while numbers[l] + numbers[r] != target:
        if numbers[l] + numbers[r] < target:
            l += 1
        else:
            r -= 1
    return [l + 1, r + 1]


@lc("3sum", "3Sum", "medium", "nums: List[int]", "List[List[int]]", cmp="anyDeep", topic="two pointers", desc="""
Return all unique triplets `[a, b, c]` from `nums` (using three different indices) such that `a + b + c == 0`. The output must not contain duplicate triplets; order doesn't matter.
""", tests=[ex([-1, 0, 1, 2, -1, -4], out=[[-1, -1, 2], [-1, 0, 1]]), ex([0, 1, 1], out=[]), ex([0, 0, 0], out=[[0, 0, 0]]),
            t([-2, 0, 1, 1, 2]), t([0, 0, 0, 0]), t([-4, -2, -2, -2, 0, 1, 2, 2, 2, 3, 3, 4, 4, 6, 6])])
def threeSum(nums):
    nums, res = sorted(nums), []
    for i in range(len(nums)):
        if i and nums[i] == nums[i - 1]:
            continue
        l, r = i + 1, len(nums) - 1
        while l < r:
            s = nums[i] + nums[l] + nums[r]
            if s < 0:
                l += 1
            elif s > 0:
                r -= 1
            else:
                res.append([nums[i], nums[l], nums[r]])
                l += 1
                while l < r and nums[l] == nums[l - 1]:
                    l += 1
    return res


@lc("container-with-most-water", "Container With Most Water", "medium", "height: List[int]", "int", topic="two pointers", desc="""
`height[i]` is the height of a vertical line at position `i`. Choose two lines that, together with the x-axis, hold the most water. Return that maximum area.
""", tests=[ex([1, 8, 6, 2, 5, 4, 8, 3, 7], out=49), ex([1, 1], out=1), t([4, 3, 2, 1, 4]), t([1, 2, 1])])
def maxArea(height):
    l, r, best = 0, len(height) - 1, 0
    while l < r:
        best = max(best, (r - l) * min(height[l], height[r]))
        if height[l] < height[r]:
            l += 1
        else:
            r -= 1
    return best


@lc("trapping-rain-water", "Trapping Rain Water", "hard", "height: List[int]", "int", topic="two pointers", desc="""
Given `n` non-negative integers representing an elevation map where each bar has width 1, compute how much rain water it can trap.
""", tests=[ex([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1], out=6), ex([4, 2, 0, 3, 2, 5], out=9), t([]), t([5, 4, 1, 2]), t([2, 0, 2])])
def trap(height):
    l, r, lm, rm, res = 0, len(height) - 1, 0, 0, 0
    while l < r:
        if height[l] < height[r]:
            lm = max(lm, height[l]); res += lm - height[l]; l += 1
        else:
            rm = max(rm, height[r]); res += rm - height[r]; r -= 1
    return res


@lc("is-subsequence", "Is Subsequence", "easy", "s: str, t: str", "bool", topic="two pointers", desc="""
Return `True` if `s` is a subsequence of `t`, i.e. it can be formed by deleting some (or no) characters of `t` without reordering the rest.
""", tests=[ex("abc", "ahbgdc", out=True), ex("axc", "ahbgdc", out=False), t("", "abc"), t("abc", ""), t("aaa", "aa")])
def isSubsequence(s, t):
    it = iter(t)
    return all(c in it for c in s)


@lc("move-zeroes", "Move Zeroes", "easy", "nums: List[int]", "None", inplace=0, topic="two pointers", desc="""
Move all `0`'s in `nums` to the end while keeping the relative order of the non-zero elements. Do it **in place**; your function returns nothing.
""", tests=[ex([0, 1, 0, 3, 12], out=[1, 3, 12, 0, 0]), ex([0], out=[0]), t([1, 2, 3]), t([0, 0, 1])])
def moveZeroes(nums):
    nz = [x for x in nums if x != 0]
    nums[:] = nz + [0] * (len(nums) - len(nz))


@lc("reverse-string", "Reverse String", "easy", "s: List[str]", "None", inplace=0, topic="two pointers", desc="""
Reverse the list of characters `s` **in place** using O(1) extra memory. Your function returns nothing.
""", tests=[ex(["h", "e", "l", "l", "o"], out=["o", "l", "l", "e", "h"]), ex(["H", "a", "n", "n", "a", "h"], out=["h", "a", "n", "n", "a", "H"]), t(["x"])])
def reverseString(s):
    s.reverse()


@lc("merge-sorted-array", "Merge Sorted Array", "easy", "nums1: List[int], m: int, nums2: List[int], n: int", "None", inplace=0, topic="two pointers", desc="""
`nums1` has length `m + n`: its first `m` elements are sorted, the rest are `0` placeholders. `nums2` has `n` sorted elements. Merge `nums2` into `nums1` **in place** so `nums1` is fully sorted. Your function returns nothing.
""", tests=[ex([1, 2, 3, 0, 0, 0], 3, [2, 5, 6], 3, out=[1, 2, 2, 3, 5, 6]), ex([1], 1, [], 0, out=[1]), ex([0], 0, [1], 1, out=[1]),
            t([4, 5, 6, 0, 0, 0], 3, [1, 2, 3], 3)])
def merge(nums1, m, nums2, n):
    nums1[:] = sorted(nums1[:m] + nums2)


# ============================ Sliding Window ============================

@lc("best-time-to-buy-and-sell-stock", "Best Time to Buy and Sell Stock", "easy", "prices: List[int]", "int", topic="sliding window", desc="""
`prices[i]` is a stock's price on day `i`. Choose one day to buy and a later day to sell. Return the maximum profit, or `0` if no profit is possible.
""", tests=[ex([7, 1, 5, 3, 6, 4], out=5), ex([7, 6, 4, 3, 1], out=0), t([1]), t([2, 4, 1]), t([3, 2, 6, 5, 0, 3])])
def maxProfit(prices):
    lo, best = float("inf"), 0
    for p in prices:
        lo = min(lo, p)
        best = max(best, p - lo)
    return best


@lc("longest-substring-without-repeating-characters", "Longest Substring Without Repeating Characters", "medium", "s: str", "int", topic="sliding window", desc="""
Return the length of the longest substring of `s` that contains no repeated characters.
""", tests=[ex("abcabcbb", out=3), ex("bbbbb", out=1), ex("pwwkew", out=3), t(""), t(" "), t("dvdf"), t("abba")])
def lengthOfLongestSubstring(s):
    last, start, best = {}, 0, 0
    for i, c in enumerate(s):
        if last.get(c, -1) >= start:
            start = last[c] + 1
        last[c] = i
        best = max(best, i - start + 1)
    return best


@lc("longest-repeating-character-replacement", "Longest Repeating Character Replacement", "medium", "s: str, k: int", "int", topic="sliding window", desc="""
`s` consists of uppercase English letters. You may change at most `k` characters to any other uppercase letter. Return the length of the longest substring containing a single repeated letter you can get.
""", tests=[ex("ABAB", 2, out=4), ex("AABABBA", 1, out=4), t("A", 0), t("ABCDE", 1), t("AAAB", 0)])
def characterReplacement(s, k):
    count, l, top, best = Counter(), 0, 0, 0
    for r, c in enumerate(s):
        count[c] += 1
        top = max(top, count[c])
        while r - l + 1 - top > k:
            count[s[l]] -= 1
            l += 1
        best = max(best, r - l + 1)
    return best


@lc("permutation-in-string", "Permutation in String", "medium", "s1: str, s2: str", "bool", topic="sliding window", desc="""
Return `True` if `s2` contains a permutation of `s1` as a contiguous substring.
""", tests=[ex("ab", "eidbaooo", out=True), ex("ab", "eidboaoo", out=False), t("adc", "dcda"), t("abc", "ab"), t("a", "a")])
def checkInclusion(s1, s2):
    n = len(s1)
    need = Counter(s1)
    return any(Counter(s2[i:i + n]) == need for i in range(len(s2) - n + 1))


@lc("minimum-window-substring", "Minimum Window Substring", "hard", "s: str, t: str", "str", topic="sliding window", desc="""
Return the shortest substring of `s` that contains every character of `t` (including duplicates). If there is none, return `""`. The answer is unique for all tests.
""", tests=[ex("ADOBECODEBANC", "ABC", out="BANC"), ex("a", "a", out="a"), ex("a", "aa", out=""), t("aaflslflsldkalskaaa", "aaa"), t("ab", "b")])
def minWindow(s, t):
    need, missing = Counter(t), len(t)
    l, best = 0, (0, float("inf"))
    for r, c in enumerate(s):
        if need[c] > 0:
            missing -= 1
        need[c] -= 1
        while missing == 0:
            if r - l < best[1] - best[0]:
                best = (l, r)
            need[s[l]] += 1
            if need[s[l]] > 0:
                missing += 1
            l += 1
    return "" if best[1] == float("inf") else s[best[0]:best[1] + 1]


@lc("sliding-window-maximum", "Sliding Window Maximum", "hard", "nums: List[int], k: int", "List[int]", topic="sliding window", desc="""
A window of size `k` slides over `nums` from left to right, one step at a time. Return the maximum of each window. Aim for O(n).
""", tests=[ex([1, 3, -1, -3, 5, 3, 6, 7], 3, out=[3, 3, 5, 5, 6, 7]), ex([1], 1, out=[1]), t([9, 8, 7, 6], 2), t([1, -1], 1), t([4, 2, 12, 3, 8, 1], 4)])
def maxSlidingWindow(nums, k):
    dq, res = deque(), []
    for i, x in enumerate(nums):
        while dq and nums[dq[-1]] <= x:
            dq.pop()
        dq.append(i)
        if dq[0] <= i - k:
            dq.popleft()
        if i >= k - 1:
            res.append(nums[dq[0]])
    return res


# ============================ Stack ============================

@lc("valid-parentheses", "Valid Parentheses", "easy", "s: str", "bool", topic="stack", desc="""
Given a string `s` containing only `()[]{}`, determine if it is valid: every open bracket is closed by the same type of bracket, in the correct order.
""", tests=[ex("()", out=True), ex("()[]{}", out=True), ex("(]", out=False), t("([)]"), t("{[]}"), t("["), t("]")])
def isValid(s):
    st, pairs = [], {")": "(", "]": "[", "}": "{"}
    for c in s:
        if c in pairs:
            if not st or st.pop() != pairs[c]:
                return False
        else:
            st.append(c)
    return not st


@lc("evaluate-reverse-polish-notation", "Evaluate Reverse Polish Notation", "medium", "tokens: List[str]", "int", topic="stack", desc="""
Evaluate an arithmetic expression in Reverse Polish Notation. Operators are `+`, `-`, `*`, `/`; division truncates toward zero. The expression is always valid.
""", tests=[ex(["2", "1", "+", "3", "*"], out=9), ex(["4", "13", "5", "/", "+"], out=6),
            ex(["10", "6", "9", "3", "+", "-11", "*", "/", "*", "17", "+", "5", "+"], out=22), t(["7", "-2", "/"])])
def evalRPN(tokens):
    st = []
    for tok in tokens:
        if tok in "+-*/":
            b, a = st.pop(), st.pop()
            st.append(a + b if tok == "+" else a - b if tok == "-" else a * b if tok == "*" else int(a / b))
        else:
            st.append(int(tok))
    return st[0]


@lc("generate-parentheses", "Generate Parentheses", "medium", "n: int", "List[str]", cmp="any", topic="stack", desc="""
Given `n` pairs of parentheses, return all combinations of well-formed parentheses, in any order.
""", tests=[ex(3, out=["((()))", "(()())", "(())()", "()(())", "()()()"]), ex(1, out=["()"]), t(2), t(4)])
def generateParenthesis(n):
    res = []
    def go(s, o, c):
        if len(s) == 2 * n:
            res.append(s); return
        if o < n: go(s + "(", o + 1, c)
        if c < o: go(s + ")", o, c + 1)
    go("", 0, 0)
    return res


@lc("daily-temperatures", "Daily Temperatures", "medium", "temperatures: List[int]", "List[int]", topic="stack", desc="""
For each day, return how many days you have to wait until a warmer temperature. Use `0` if there is no future warmer day.
""", tests=[ex([73, 74, 75, 71, 69, 72, 76, 73], out=[1, 1, 4, 2, 1, 1, 0, 0]), ex([30, 40, 50, 60], out=[1, 1, 1, 0]), ex([30, 60, 90], out=[1, 1, 0]), t([5, 5, 5])])
def dailyTemperatures(temperatures):
    res, st = [0] * len(temperatures), []
    for i, x in enumerate(temperatures):
        while st and temperatures[st[-1]] < x:
            j = st.pop()
            res[j] = i - j
        st.append(i)
    return res


@lc("car-fleet", "Car Fleet", "medium", "target: int, position: List[int], speed: List[int]", "int", topic="stack", desc="""
`n` cars drive toward mile `target` on a one-lane road. Car `i` starts at `position[i]` with speed `speed[i]`. A car can't pass a slower car ahead; it catches up and they drive together as a **fleet** at the slower speed. A car that catches up exactly at the target joins that fleet. How many fleets arrive?
""", tests=[ex(12, [10, 8, 0, 5, 3], [2, 4, 1, 1, 3], out=3), ex(10, [3], [3], out=1), ex(100, [0, 2, 4], [4, 2, 1], out=1), t(10, [6, 8], [3, 2])])
def carFleet(target, position, speed):
    fleets, slowest = 0, 0.0
    for p, s in sorted(zip(position, speed), reverse=True):
        time = (target - p) / s
        if time > slowest:
            fleets += 1
            slowest = time
    return fleets


@lc("largest-rectangle-in-histogram", "Largest Rectangle in Histogram", "hard", "heights: List[int]", "int", topic="stack", desc="""
`heights` are the bar heights of a histogram where every bar has width 1. Return the area of the largest rectangle that fits inside the histogram.
""", tests=[ex([2, 1, 5, 6, 2, 3], out=10), ex([2, 4], out=4), t([1]), t([2, 1, 2]), t([6, 2, 5, 4, 5, 1, 6])])
def largestRectangleArea(heights):
    st, best = [], 0
    for i, h in enumerate(heights + [0]):
        start = i
        while st and st[-1][1] >= h:
            j, hh = st.pop()
            best = max(best, hh * (i - j))
            start = j
        st.append((start, h))
    return best


# ============================ Binary Search ============================

@lc("binary-search", "Binary Search", "easy", "nums: List[int], target: int", "int", topic="binary search", desc="""
Given a sorted array of distinct integers `nums` and a `target`, return its index, or `-1` if it isn't present. Aim for O(log n).
""", tests=[ex([-1, 0, 3, 5, 9, 12], 9, out=4), ex([-1, 0, 3, 5, 9, 12], 2, out=-1), t([5], 5), t([5], -5), t([1, 3, 5, 7, 9, 11, 13], 1)])
def search(nums, target):
    return nums.index(target) if target in nums else -1


@lc("search-a-2d-matrix", "Search a 2D Matrix", "medium", "matrix: List[List[int]], target: int", "bool", topic="binary search", desc="""
Each row of `matrix` is sorted, and each row's first value is greater than the previous row's last value. Return `True` if `target` is in the matrix. Aim for O(log(m·n)).
""", tests=[ex([[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]], 3, out=True), ex([[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]], 13, out=False),
            t([[1]], 1), t([[1, 3]], 3), t([[1], [3]], 2)])
def searchMatrix(matrix, target):
    return any(target in row for row in matrix)


@lc("koko-eating-bananas", "Koko Eating Bananas", "medium", "piles: List[int], h: int", "int", topic="binary search", desc="""
Koko has `piles` of bananas and `h` hours. Each hour she picks one pile and eats `k` bananas from it (or the whole pile if it has fewer). Return the minimum integer speed `k` that lets her finish all piles within `h` hours.
""", tests=[ex([3, 6, 7, 11], 8, out=4), ex([30, 11, 23, 4, 20], 5, out=30), ex([30, 11, 23, 4, 20], 6, out=23), t([312884470], 312884469), t([1, 1, 1, 999999999], 10)])
def minEatingSpeed(piles, h):
    lo, hi = 1, max(piles)
    while lo < hi:
        k = (lo + hi) // 2
        if sum((p + k - 1) // k for p in piles) <= h:
            hi = k
        else:
            lo = k + 1
    return lo


@lc("find-minimum-in-rotated-sorted-array", "Find Minimum in Rotated Sorted Array", "medium", "nums: List[int]", "int", topic="binary search", desc="""
A sorted array of unique values was rotated some number of times (e.g. `[0,1,2,4,5,6,7]` → `[4,5,6,7,0,1,2]`). Return its minimum in O(log n).
""", tests=[ex([3, 4, 5, 1, 2], out=1), ex([4, 5, 6, 7, 0, 1, 2], out=0), ex([11, 13, 15, 17], out=11), t([2, 1]), t([1])])
def findMin(nums):
    return min(nums)


@lc("search-in-rotated-sorted-array", "Search in Rotated Sorted Array", "medium", "nums: List[int], target: int", "int", topic="binary search", name="search", desc="""
`nums` is a sorted array of distinct values that may have been rotated. Return the index of `target`, or `-1`. Aim for O(log n).
""", tests=[ex([4, 5, 6, 7, 0, 1, 2], 0, out=4), ex([4, 5, 6, 7, 0, 1, 2], 3, out=-1), ex([1], 0, out=-1), t([3, 1], 1), t([5, 1, 3], 5)])
def searchRotated(nums, target):
    return nums.index(target) if target in nums else -1


@lc("median-of-two-sorted-arrays", "Median of Two Sorted Arrays", "hard", "nums1: List[int], nums2: List[int]", "float", topic="binary search", desc="""
Return the median of the two sorted arrays `nums1` and `nums2` combined. Aim for O(log(m + n)).
""", tests=[ex([1, 3], [2], out=2.0), ex([1, 2], [3, 4], out=2.5), t([], [1]), t([0, 0], [0, 0]), t([1, 4, 9], [2, 3, 10, 11])])
def findMedianSortedArrays(nums1, nums2):
    a = sorted(nums1 + nums2)
    n = len(a)
    return float(a[n // 2]) if n % 2 else (a[n // 2 - 1] + a[n // 2]) / 2


# ============================ Intervals ============================

@lc("insert-interval", "Insert Interval", "medium", "intervals: List[List[int]], newInterval: List[int]", "List[List[int]]", topic="intervals", desc="""
`intervals` is sorted by start and non-overlapping. Insert `newInterval`, merging where necessary, and return the resulting sorted, non-overlapping list.
""", tests=[ex([[1, 3], [6, 9]], [2, 5], out=[[1, 5], [6, 9]]), ex([[1, 2], [3, 5], [6, 7], [8, 10], [12, 16]], [4, 8], out=[[1, 2], [3, 10], [12, 16]]),
            t([], [5, 7]), t([[1, 5]], [6, 8]), t([[3, 5]], [1, 2])])
def insert(intervals, newInterval):
    return mergeIntervals(intervals + [newInterval])


@lc("merge-intervals", "Merge Intervals", "medium", "intervals: List[List[int]]", "List[List[int]]", topic="intervals", name="merge", desc="""
Merge all overlapping intervals and return the non-overlapping intervals that cover the same ranges, sorted by start. Touching intervals like `[1,4]` and `[4,5]` overlap.
""", tests=[ex([[1, 3], [2, 6], [8, 10], [15, 18]], out=[[1, 6], [8, 10], [15, 18]]), ex([[1, 4], [4, 5]], out=[[1, 5]]), t([[1, 4], [0, 4]]), t([[1, 4], [2, 3]])])
def mergeIntervals(intervals):
    res = []
    for s, e in sorted(intervals):
        if res and s <= res[-1][1]:
            res[-1][1] = max(res[-1][1], e)
        else:
            res.append([s, e])
    return res


@lc("non-overlapping-intervals", "Non-overlapping Intervals", "medium", "intervals: List[List[int]]", "int", topic="intervals", desc="""
Return the minimum number of intervals to remove so the rest don't overlap. Intervals that only touch (like `[1,2]` and `[2,3]`) don't overlap.
""", tests=[ex([[1, 2], [2, 3], [3, 4], [1, 3]], out=1), ex([[1, 2], [1, 2], [1, 2]], out=2), ex([[1, 2], [2, 3]], out=0), t([[0, 10], [1, 2], [3, 4], [5, 6]])])
def eraseOverlapIntervals(intervals):
    end, kept = float("-inf"), 0
    for s, e in sorted(intervals, key=lambda x: x[1]):
        if s >= end:
            kept += 1
            end = e
    return len(intervals) - kept


@lc("meeting-rooms", "Meeting Rooms", "easy", "intervals: List[List[int]]", "bool", topic="intervals", desc="""
Given meeting time intervals `[start, end]`, return `True` if one person could attend all of them (no two overlap; a meeting may start exactly when another ends).
""", tests=[ex([[0, 30], [5, 10], [15, 20]], out=False), ex([[7, 10], [2, 4]], out=True), t([]), t([[1, 5], [5, 8]])])
def canAttendMeetings(intervals):
    iv = sorted(intervals)
    return all(iv[i][0] >= iv[i - 1][1] for i in range(1, len(iv)))


@lc("meeting-rooms-ii", "Meeting Rooms II", "medium", "intervals: List[List[int]]", "int", topic="intervals", desc="""
Given meeting time intervals `[start, end]`, return the minimum number of rooms needed so every meeting has a room. A room freed at time `t` can be reused by a meeting starting at `t`.
""", tests=[ex([[0, 30], [5, 10], [15, 20]], out=2), ex([[7, 10], [2, 4]], out=1), t([[1, 5], [5, 8]]), t([[1, 10], [2, 7], [3, 19], [8, 12], [10, 20], [11, 30]])])
def minMeetingRooms(intervals):
    ends = []
    for s, e in sorted(intervals):
        if ends and ends[0] <= s:
            heapq.heapreplace(ends, e)
        else:
            heapq.heappush(ends, e)
    return len(ends)


# ============================ Greedy ============================

@lc("maximum-subarray", "Maximum Subarray", "medium", "nums: List[int]", "int", topic="greedy", desc="""
Return the largest sum of any non-empty contiguous subarray of `nums`.
""", tests=[ex([-2, 1, -3, 4, -1, 2, 1, -5, 4], out=6), ex([1], out=1), ex([5, 4, -1, 7, 8], out=23), t([-3, -1, -2])])
def maxSubArray(nums):
    best = cur = nums[0]
    for x in nums[1:]:
        cur = max(x, cur + x)
        best = max(best, cur)
    return best


@lc("jump-game", "Jump Game", "medium", "nums: List[int]", "bool", topic="greedy", desc="""
You start at index 0. `nums[i]` is the maximum jump length from index `i`. Return `True` if you can reach the last index.
""", tests=[ex([2, 3, 1, 1, 4], out=True), ex([3, 2, 1, 0, 4], out=False), t([0]), t([2, 0, 0]), t([1, 0, 1])])
def canJump(nums):
    reach = 0
    for i, x in enumerate(nums):
        if i > reach:
            return False
        reach = max(reach, i + x)
    return True


@lc("jump-game-ii", "Jump Game II", "medium", "nums: List[int]", "int", topic="greedy", desc="""
You start at index 0, and `nums[i]` is the maximum jump length from index `i`. Return the minimum number of jumps to reach the last index. It is always reachable.
""", tests=[ex([2, 3, 1, 1, 4], out=2), ex([2, 3, 0, 1, 4], out=2), t([0]), t([1, 1, 1, 1]), t([5, 1, 1, 1, 1, 1, 1])])
def jump(nums):
    jumps, end, far = 0, 0, 0
    for i in range(len(nums) - 1):
        far = max(far, i + nums[i])
        if i == end:
            jumps += 1
            end = far
    return jumps


@lc("gas-station", "Gas Station", "medium", "gas: List[int], cost: List[int]", "int", topic="greedy", desc="""
Gas stations sit on a circular route. Station `i` gives `gas[i]` fuel, and driving from station `i` to `i + 1` costs `cost[i]`. Starting with an empty tank, return the index of the station from which you can complete the circuit once, or `-1` if impossible. The answer is unique if it exists.
""", tests=[ex([1, 2, 3, 4, 5], [3, 4, 5, 1, 2], out=3), ex([2, 3, 4], [3, 4, 3], out=-1), t([5], [4]), t([3, 1, 1], [1, 2, 2])])
def canCompleteCircuit(gas, cost):
    if sum(gas) < sum(cost):
        return -1
    tank, start = 0, 0
    for i in range(len(gas)):
        tank += gas[i] - cost[i]
        if tank < 0:
            tank, start = 0, i + 1
    return start


@lc("hand-of-straights", "Hand of Straights", "medium", "hand: List[int], groupSize: int", "bool", topic="greedy", desc="""
Can the cards in `hand` be rearranged into groups of `groupSize` consecutive values (e.g. 3, 4, 5)? Return `True` or `False`.
""", tests=[ex([1, 2, 3, 6, 2, 3, 4, 7, 8], 3, out=True), ex([1, 2, 3, 4, 5], 4, out=False), t([1], 1), t([1, 1, 2, 2, 3, 3], 3), t([1, 2, 4, 5], 2)])
def isNStraightHand(hand, groupSize):
    count = Counter(hand)
    for x in sorted(count):
        n = count[x]
        if n:
            for y in range(x, x + groupSize):
                if count[y] < n:
                    return False
                count[y] -= n
    return True


@lc("partition-labels", "Partition Labels", "medium", "s: str", "List[int]", topic="greedy", desc="""
Split `s` into as many parts as possible so each letter appears in at most one part. Return the sizes of the parts, in order.
""", tests=[ex("ababcbacadefegdehijhklij", out=[9, 7, 8]), ex("eccbbbbdec", out=[10]), t("abc"), t("a")])
def partitionLabels(s):
    last = {c: i for i, c in enumerate(s)}
    res, start, end = [], 0, 0
    for i, c in enumerate(s):
        end = max(end, last[c])
        if i == end:
            res.append(end - start + 1)
            start = i + 1
    return res


@lc("valid-parenthesis-string", "Valid Parenthesis String", "medium", "s: str", "bool", topic="greedy", desc="""
`s` contains `(`, `)` and `*`. Each `*` may act as `(`, `)` or an empty string. Return `True` if `s` can be valid.
""", tests=[ex("()", out=True), ex("(*)", out=True), ex("(*))", out=True), t("((*"), t(")("), t("(((((*)))**")])
def checkValidString(s):
    lo = hi = 0
    for c in s:
        lo += 1 if c == "(" else -1
        hi += -1 if c == ")" else 1
        if hi < 0:
            return False
        lo = max(lo, 0)
    return lo == 0


# ============================ Math & Geometry ============================

@lc("rotate-image", "Rotate Image", "medium", "matrix: List[List[int]]", "None", inplace=0, topic="math", desc="""
Rotate the `n x n` image `matrix` by 90 degrees clockwise, **in place**. Your function returns nothing.
""", tests=[ex([[1, 2, 3], [4, 5, 6], [7, 8, 9]], out=[[7, 4, 1], [8, 5, 2], [9, 6, 3]]),
            ex([[5, 1, 9, 11], [2, 4, 8, 10], [13, 3, 6, 7], [15, 14, 12, 16]], out=[[15, 13, 2, 5], [14, 3, 4, 1], [12, 6, 8, 9], [16, 7, 10, 11]]), t([[1]])])
def rotate(matrix):
    matrix[:] = [list(r) for r in zip(*matrix[::-1])]


@lc("spiral-matrix", "Spiral Matrix", "medium", "matrix: List[List[int]]", "List[int]", topic="math", desc="""
Return all elements of the `m x n` `matrix` in spiral order (clockwise, starting top-left).
""", tests=[ex([[1, 2, 3], [4, 5, 6], [7, 8, 9]], out=[1, 2, 3, 6, 9, 8, 7, 4, 5]), ex([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]], out=[1, 2, 3, 4, 8, 12, 11, 10, 9, 5, 6, 7]),
            t([[1]]), t([[1], [2], [3]]), t([[1, 2], [3, 4], [5, 6]])])
def spiralOrder(matrix):
    res, m = [], [r[:] for r in matrix]
    while m:
        res += m.pop(0)
        m = [list(r) for r in zip(*m)][::-1]
    return res


@lc("set-matrix-zeroes", "Set Matrix Zeroes", "medium", "matrix: List[List[int]]", "None", inplace=0, topic="math", desc="""
If an element of `matrix` is `0`, set its entire row and column to `0`. Do it **in place**; your function returns nothing.
""", tests=[ex([[1, 1, 1], [1, 0, 1], [1, 1, 1]], out=[[1, 0, 1], [0, 0, 0], [1, 0, 1]]),
            ex([[0, 1, 2, 0], [3, 4, 5, 2], [1, 3, 1, 5]], out=[[0, 0, 0, 0], [0, 4, 5, 0], [0, 3, 1, 0]]), t([[1]]), t([[1, 0]])])
def setZeroes(matrix):
    rows = {r for r, row in enumerate(matrix) for v in row if v == 0}
    cols = {c for row in matrix for c, v in enumerate(row) if v == 0}
    for r, row in enumerate(matrix):
        for c in range(len(row)):
            if r in rows or c in cols:
                row[c] = 0


@lc("happy-number", "Happy Number", "easy", "n: int", "bool", topic="math", desc="""
Repeatedly replace `n` by the sum of the squares of its digits. If this eventually reaches `1`, `n` is happy; otherwise it loops forever. Return `True` if `n` is happy.
""", tests=[ex(19, out=True), ex(2, out=False), t(1), t(7), t(116)])
def isHappy(n):
    seen = set()
    while n != 1 and n not in seen:
        seen.add(n)
        n = sum(int(d) ** 2 for d in str(n))
    return n == 1


@lc("plus-one", "Plus One", "easy", "digits: List[int]", "List[int]", topic="math", desc="""
A large integer is given as a list of `digits`, most significant first. Add one and return the resulting digits.
""", tests=[ex([1, 2, 3], out=[1, 2, 4]), ex([4, 3, 2, 1], out=[4, 3, 2, 2]), ex([9], out=[1, 0]), t([9, 9, 9]), t([1, 0, 9])])
def plusOne(digits):
    return [int(c) for c in str(int("".join(map(str, digits))) + 1)]


@lc("multiply-strings", "Multiply Strings", "medium", "num1: str, num2: str", "str", topic="math", desc="""
Multiply two non-negative integers given as strings and return the product as a string. Don't convert the inputs to integers directly.
""", tests=[ex("2", "3", out="6"), ex("123", "456", out="56088"), t("0", "9999"), t("999", "999"), t("123456789", "987654321")])
def multiply(num1, num2):
    return str(int(num1) * int(num2))


@lc("fizz-buzz", "Fizz Buzz", "easy", "n: int", "List[str]", examples=1, topic="math", desc="""
Return a list of strings for `1..n`: `"FizzBuzz"` if divisible by 3 and 5, `"Fizz"` if divisible by 3, `"Buzz"` if divisible by 5, otherwise the number as a string.
""", tests=[ex(5, out=["1", "2", "Fizz", "4", "Buzz"]), t(1), t(15)])
def fizzBuzz(n):
    return ["FizzBuzz" if i % 15 == 0 else "Fizz" if i % 3 == 0 else "Buzz" if i % 5 == 0 else str(i) for i in range(1, n + 1)]


@lc("roman-to-integer", "Roman to Integer", "easy", "s: str", "int", topic="math", desc="""
Convert a Roman numeral (`I`=1, `V`=5, `X`=10, `L`=50, `C`=100, `D`=500, `M`=1000) to an integer. A smaller value before a larger one is subtracted, as in `IV` = 4 or `CM` = 900.
""", tests=[ex("III", out=3), ex("LVIII", out=58), ex("MCMXCIV", out=1994), t("IX"), t("MMMCMXCIX")])
def romanToInt(s):
    v = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}
    return sum(-v[c] if i + 1 < len(s) and v[c] < v[s[i + 1]] else v[c] for i, c in enumerate(s))


# ============================ Bit Manipulation ============================

@lc("single-number", "Single Number", "easy", "nums: List[int]", "int", topic="bits", desc="""
Every element in `nums` appears twice except for one. Find that single one in O(n) time and O(1) extra space.
""", tests=[ex([2, 2, 1], out=1), ex([4, 1, 2, 1, 2], out=4), ex([1], out=1), t([-3, 7, 7])])
def singleNumber(nums):
    r = 0
    for x in nums:
        r ^= x
    return r


@lc("number-of-1-bits", "Number of 1 Bits", "easy", "n: int", "int", topic="bits", desc="""
Given a positive integer `n`, return the number of `1` bits in its binary representation.
""", tests=[ex(11, out=3), ex(128, out=1), ex(2147483645, out=30), t(1)])
def hammingWeight(n):
    return bin(n).count("1")


@lc("counting-bits", "Counting Bits", "easy", "n: int", "List[int]", topic="bits", desc="""
Return a list `ans` of length `n + 1` where `ans[i]` is the number of `1` bits in `i`.
""", tests=[ex(2, out=[0, 1, 1]), ex(5, out=[0, 1, 1, 2, 1, 2]), t(0), t(8)])
def countBits(n):
    return [bin(i).count("1") for i in range(n + 1)]


@lc("reverse-bits", "Reverse Bits", "easy", "n: int", "int", topic="bits", desc="""
Reverse the bits of the 32-bit unsigned integer `n` and return the result as an unsigned integer.
""", tests=[ex(43261596, out=964176192), ex(4294967293, out=3221225471), t(0), t(1)])
def reverseBits(n):
    return int(format(n, "032b")[::-1], 2)


@lc("missing-number", "Missing Number", "easy", "nums: List[int]", "int", topic="bits", desc="""
`nums` contains `n` distinct numbers in the range `[0, n]`. Return the only number in that range that is missing.
""", tests=[ex([3, 0, 1], out=2), ex([0, 1], out=2), ex([9, 6, 4, 2, 3, 5, 7, 0, 1], out=8), t([0]), t([1])])
def missingNumber(nums):
    n = len(nums)
    return n * (n + 1) // 2 - sum(nums)


@lc("sum-of-two-integers", "Sum of Two Integers", "medium", "a: int, b: int", "int", topic="bits", desc="""
Return the sum of `a` and `b` without using the `+` or `-` operators. Both are in `[-1000, 1000]`. (Hint: work with 32-bit masks in Python.)
""", tests=[ex(1, 2, out=3), ex(2, 3, out=5), t(-1, 1), t(-12, -8), t(1000, -1000), t(-7, 3)])
def getSum(a, b):
    return a + b


@lc("reverse-integer", "Reverse Integer", "medium", "x: int", "int", topic="bits", desc="""
Reverse the digits of the signed 32-bit integer `x`. If the result falls outside `[-2^31, 2^31 - 1]`, return `0`.
""", tests=[ex(123, out=321), ex(-123, out=-321), ex(120, out=21), t(0), t(1534236469), t(-2147483412)])
def reverse(x):
    r = int(str(abs(x))[::-1]) * (1 if x >= 0 else -1)
    return r if -2 ** 31 <= r < 2 ** 31 else 0
