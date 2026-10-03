"""Backtracking, graphs, 1-D and 2-D dynamic programming."""
from collections import Counter, deque
from functools import lru_cache
from itertools import combinations, permutations
from common import lc, ex, t

# ============================ Backtracking ============================

@lc("subsets", "Subsets", "medium", "nums: List[int]", "List[List[int]]", cmp="anyDeep", topic="backtracking", desc="""
Given an array of unique integers, return all possible subsets (the power set), in any order, without duplicates.
""", tests=[ex([1, 2, 3], out=[[], [1], [2], [1, 2], [3], [1, 3], [2, 3], [1, 2, 3]]), ex([0], out=[[], [0]]), t([5, -1, 2, 7])])
def subsets(nums):
    return [list(c) for r in range(len(nums) + 1) for c in combinations(nums, r)]


@lc("subsets-ii", "Subsets II", "medium", "nums: List[int]", "List[List[int]]", cmp="anyDeep", topic="backtracking", desc="""
`nums` may contain duplicates. Return all possible subsets without duplicate subsets, in any order.
""", tests=[ex([1, 2, 2], out=[[], [1], [1, 2], [1, 2, 2], [2], [2, 2]]), ex([0], out=[[], [0]]), t([4, 4, 4, 1, 4])])
def subsetsWithDup(nums):
    return [list(c) for c in {c for r in range(len(nums) + 1) for c in combinations(sorted(nums), r)}]


@lc("combination-sum", "Combination Sum", "medium", "candidates: List[int], target: int", "List[List[int]]", cmp="anyDeep", topic="backtracking", desc="""
Given distinct positive `candidates`, return all unique combinations that sum to `target`. Each number may be used any number of times. Two combinations are the same if they use the same numbers with the same counts.
""", tests=[ex([2, 3, 6, 7], 7, out=[[2, 2, 3], [7]]), ex([2, 3, 5], 8, out=[[2, 2, 2, 2], [2, 3, 3], [3, 5]]), ex([2], 1, out=[]), t([3, 4, 5], 12)])
def combinationSum(candidates, target):
    res = []
    def go(i, left, cur):
        if left == 0:
            res.append(cur[:]); return
        for j in range(i, len(candidates)):
            if candidates[j] <= left:
                cur.append(candidates[j]); go(j, left - candidates[j], cur); cur.pop()
    go(0, target, [])
    return res


@lc("combination-sum-ii", "Combination Sum II", "medium", "candidates: List[int], target: int", "List[List[int]]", cmp="anyDeep", topic="backtracking", desc="""
Return all unique combinations of `candidates` that sum to `target`. Each element may be used **at most once**, and the result must not contain duplicate combinations.
""", tests=[ex([10, 1, 2, 7, 6, 1, 5], 8, out=[[1, 1, 6], [1, 2, 5], [1, 7], [2, 6]]), ex([2, 5, 2, 1, 2], 5, out=[[1, 2, 2], [5]]), t([1, 1, 1, 1], 2)])
def combinationSum2(candidates, target):
    c = sorted(candidates)
    return [list(x) for x in {x for r in range(1, len(c) + 1) for x in combinations(c, r) if sum(x) == target}]


@lc("permutations", "Permutations", "medium", "nums: List[int]", "List[List[int]]", cmp="any", topic="backtracking", desc="""
Given an array of distinct integers, return all possible permutations, in any order.
""", tests=[ex([1, 2, 3], out=[[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]), ex([0, 1], out=[[0, 1], [1, 0]]), ex([1], out=[[1]]), t([4, 5, 6, 7])])
def permute(nums):
    return [list(p) for p in permutations(nums)]


@lc("word-search", "Word Search", "medium", "board: List[List[str]], word: str", "bool", topic="backtracking", desc="""
Return `True` if `word` can be spelled by a path of horizontally or vertically adjacent cells in `board`, using each cell at most once.
""", tests=[ex([["A", "B", "C", "E"], ["S", "F", "C", "S"], ["A", "D", "E", "E"]], "ABCCED", out=True),
            ex([["A", "B", "C", "E"], ["S", "F", "C", "S"], ["A", "D", "E", "E"]], "SEE", out=True),
            ex([["A", "B", "C", "E"], ["S", "F", "C", "S"], ["A", "D", "E", "E"]], "ABCB", out=False), t([["a"]], "a"), t([["a", "a"]], "aaa")])
def exist(board, word):
    R, C = len(board), len(board[0])
    def go(r, c, i):
        if i == len(word):
            return True
        if not (0 <= r < R and 0 <= c < C) or board[r][c] != word[i]:
            return False
        ch, board[r][c] = board[r][c], "#"
        ok = any(go(r + dr, c + dc, i + 1) for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)))
        board[r][c] = ch
        return ok
    return any(go(r, c, 0) for r in range(R) for c in range(C))


@lc("palindrome-partitioning", "Palindrome Partitioning", "medium", "s: str", "List[List[str]]", cmp="any", topic="backtracking", desc="""
Partition `s` so that every piece is a palindrome. Return all possible partitions, in any order (each partition lists its pieces left to right).
""", tests=[ex("aab", out=[["a", "a", "b"], ["aa", "b"]]), ex("a", out=[["a"]]), t("racecar"), t("abba")])
def partition(s):
    if not s:
        return [[]]
    return [[s[:i]] + rest for i in range(1, len(s) + 1) if s[:i] == s[:i][::-1] for rest in partition(s[i:])]


@lc("letter-combinations-of-a-phone-number", "Letter Combinations of a Phone Number", "medium", "digits: str", "List[str]", cmp="any", topic="backtracking", desc="""
Given a string of digits `2-9`, return all letter combinations they could represent on a phone keypad (2=abc, 3=def, 4=ghi, 5=jkl, 6=mno, 7=pqrs, 8=tuv, 9=wxyz), in any order. Empty input gives an empty list.
""", tests=[ex("23", out=["ad", "ae", "af", "bd", "be", "bf", "cd", "ce", "cf"]), ex("", out=[]), ex("2", out=["a", "b", "c"]), t("79")])
def letterCombinations(digits):
    if not digits:
        return []
    keys = {"2": "abc", "3": "def", "4": "ghi", "5": "jkl", "6": "mno", "7": "pqrs", "8": "tuv", "9": "wxyz"}
    res = [""]
    for d in digits:
        res = [p + c for p in res for c in keys[d]]
    return res


@lc("n-queens", "N-Queens", "hard", "n: int", "List[List[str]]", cmp="any", examples=1, topic="backtracking", desc="""
Place `n` queens on an `n x n` board so no two attack each other. Return all distinct solutions, in any order. Each solution is a list of rows, using `Q` for a queen and `.` for empty.
""", tests=[ex(4, out=[[".Q..", "...Q", "Q...", "..Q."], ["..Q.", "Q...", "...Q", ".Q.."]]), ex(1, out=[["Q"]]), t(5), t(6)])
def solveNQueens(n):
    return [["." * c + "Q" + "." * (n - c - 1) for c in p] for p in permutations(range(n))
            if len({r + c for r, c in enumerate(p)}) == n and len({r - c for r, c in enumerate(p)}) == n]


# ============================ Graphs ============================

_DIRS = ((1, 0), (-1, 0), (0, 1), (0, -1))


def _flood(grid, r, c, is_land, mark):
    stack, size = [(r, c)], 0
    while stack:
        r, c = stack.pop()
        if 0 <= r < len(grid) and 0 <= c < len(grid[0]) and is_land(grid[r][c]):
            grid[r][c] = mark
            size += 1
            stack += [(r + dr, c + dc) for dr, dc in _DIRS]
    return size


@lc("number-of-islands", "Number of Islands", "medium", "grid: List[List[str]]", "int", examples=1, topic="graphs", desc="""
`grid` is a map of `"1"` (land) and `"0"` (water). Return the number of islands: groups of land connected horizontally or vertically.
""", tests=[ex([["1", "1", "1", "1", "0"], ["1", "1", "0", "1", "0"], ["1", "1", "0", "0", "0"], ["0", "0", "0", "0", "0"]], out=1),
            ex([["1", "1", "0", "0", "0"], ["1", "1", "0", "0", "0"], ["0", "0", "1", "0", "0"], ["0", "0", "0", "1", "1"]], out=3),
            t([["0"]]), t([["1", "0", "1"], ["0", "1", "0"], ["1", "0", "1"]])])
def numIslands(grid):
    return sum(_flood(grid, r, c, lambda v: v == "1", "#") > 0 for r in range(len(grid)) for c in range(len(grid[0])))


@lc("max-area-of-island", "Max Area of Island", "medium", "grid: List[List[int]]", "int", examples=1, topic="graphs", desc="""
`grid` contains `1` (land) and `0` (water). An island is a group of `1`s connected horizontally or vertically. Return the area of the largest island, or `0` if there is none.
""", tests=[ex([[0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0], [0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0], [0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0]], out=6),
            ex([[0, 0, 0, 0, 0, 0, 0, 0]], out=0), t([[1, 1], [1, 0]])])
def maxAreaOfIsland(grid):
    return max([_flood(grid, r, c, lambda v: v == 1, 2) for r in range(len(grid)) for c in range(len(grid[0]))] + [0])


@lc("rotting-oranges", "Rotting Oranges", "medium", "grid: List[List[int]]", "int", topic="graphs", desc="""
Each cell is `0` (empty), `1` (fresh orange) or `2` (rotten orange). Every minute, fresh oranges next to a rotten one (up/down/left/right) become rotten. Return the minutes until no fresh orange remains, or `-1` if that's impossible.
""", tests=[ex([[2, 1, 1], [1, 1, 0], [0, 1, 1]], out=4), ex([[2, 1, 1], [0, 1, 1], [1, 0, 1]], out=-1), ex([[0, 2]], out=0), t([[1]]), t([[2, 2], [1, 1], [0, 0], [2, 0]])])
def orangesRotting(grid):
    R, C = len(grid), len(grid[0])
    q = deque((r, c) for r in range(R) for c in range(C) if grid[r][c] == 2)
    fresh = sum(v == 1 for row in grid for v in row)
    minutes = 0
    while q and fresh:
        for _ in range(len(q)):
            r, c = q.popleft()
            for dr, dc in _DIRS:
                nr, nc = r + dr, c + dc
                if 0 <= nr < R and 0 <= nc < C and grid[nr][nc] == 1:
                    grid[nr][nc] = 2
                    fresh -= 1
                    q.append((nr, nc))
        minutes += 1
    return -1 if fresh else minutes


@lc("pacific-atlantic-water-flow", "Pacific Atlantic Water Flow", "medium", "heights: List[List[int]]", "List[List[int]]", cmp="any", examples=1, topic="graphs", desc="""
An island's `heights` grid touches the Pacific on its top and left edges and the Atlantic on its bottom and right edges. Rain flows to a neighboring cell (up/down/left/right) with height less than or equal to the current one. Return all cells `[r, c]`, in any order, from which water can reach both oceans.
""", tests=[ex([[1, 2, 2, 3, 5], [3, 2, 3, 4, 4], [2, 4, 5, 3, 1], [6, 7, 1, 4, 5], [5, 1, 1, 2, 4]],
                out=[[0, 4], [1, 3], [1, 4], [2, 2], [3, 0], [3, 1], [4, 0]]), ex([[1]], out=[[0, 0]]), t([[3, 3, 3], [3, 1, 3], [0, 2, 4]])])
def pacificAtlantic(heights):
    R, C = len(heights), len(heights[0])
    def reach(starts):
        seen, stack = set(starts), list(starts)
        while stack:
            r, c = stack.pop()
            for dr, dc in _DIRS:
                nr, nc = r + dr, c + dc
                if 0 <= nr < R and 0 <= nc < C and (nr, nc) not in seen and heights[nr][nc] >= heights[r][c]:
                    seen.add((nr, nc)); stack.append((nr, nc))
        return seen
    pac = reach([(0, c) for c in range(C)] + [(r, 0) for r in range(R)])
    atl = reach([(R - 1, c) for c in range(C)] + [(r, C - 1) for r in range(R)])
    return [list(x) for x in pac & atl]


@lc("surrounded-regions", "Surrounded Regions", "medium", "board: List[List[str]]", "None", inplace=0, examples=1, topic="graphs", desc="""
Capture every region of `"O"` cells that is completely surrounded by `"X"` (i.e. not connected to the border) by flipping it to `"X"`. Modify `board` **in place**; your function returns nothing.
""", tests=[ex([["X", "X", "X", "X"], ["X", "O", "O", "X"], ["X", "X", "O", "X"], ["X", "O", "X", "X"]],
                out=[["X", "X", "X", "X"], ["X", "X", "X", "X"], ["X", "X", "X", "X"], ["X", "O", "X", "X"]]), ex([["X"]], out=[["X"]]),
            t([["O", "O", "O"], ["O", "X", "O"], ["O", "O", "O"]]), t([["X", "O", "X"], ["O", "X", "O"], ["X", "O", "X"]])])
def solve(board):
    R, C = len(board), len(board[0])
    for r in range(R):
        for c in range(C):
            if r in (0, R - 1) or c in (0, C - 1):
                _flood(board, r, c, lambda v: v == "O", "S")
    for row in board:
        for c, v in enumerate(row):
            row[c] = "O" if v == "S" else "X"


@lc("course-schedule", "Course Schedule", "medium", "numCourses: int, prerequisites: List[List[int]]", "bool", topic="graphs", desc="""
There are `numCourses` courses labeled `0` to `numCourses - 1`. `prerequisites[i] = [a, b]` means you must take `b` before `a`. Return `True` if you can finish all courses.
""", tests=[ex(2, [[1, 0]], out=True), ex(2, [[1, 0], [0, 1]], out=False), t(3, []), t(4, [[1, 0], [2, 1], [3, 2], [1, 3]]), t(5, [[1, 4], [2, 4], [3, 1], [3, 2]])])
def canFinish(numCourses, prerequisites):
    return len(findOrder(numCourses, prerequisites)) == numCourses


def findOrder(numCourses, prerequisites):
    indeg, adj = [0] * numCourses, [[] for _ in range(numCourses)]
    for a, b in prerequisites:
        adj[b].append(a); indeg[a] += 1
    q, order = deque(i for i in range(numCourses) if indeg[i] == 0), []
    while q:
        x = q.popleft(); order.append(x)
        for y in adj[x]:
            indeg[y] -= 1
            if indeg[y] == 0:
                q.append(y)
    return order


@lc("redundant-connection", "Redundant Connection", "medium", "edges: List[List[int]]", "List[int]", topic="graphs", desc="""
A tree with nodes `1..n` had one extra edge added. `edges` lists all `n` edges. Return an edge you can remove so the result is a tree again. If there are several, return the one that appears last in `edges`.
""", tests=[ex([[1, 2], [1, 3], [2, 3]], out=[2, 3]), ex([[1, 2], [2, 3], [3, 4], [1, 4], [1, 5]], out=[1, 4]), t([[3, 4], [1, 2], [2, 4], [3, 5], [2, 5]])])
def findRedundantConnection(edges):
    parent = list(range(len(edges) + 1))
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]; x = parent[x]
        return x
    for a, b in edges:
        ra, rb = find(a), find(b)
        if ra == rb:
            return [a, b]
        parent[ra] = rb


@lc("number-of-connected-components-in-an-undirected-graph", "Number of Connected Components in an Undirected Graph", "medium",
    "n: int, edges: List[List[int]]", "int", topic="graphs", desc="""
Given `n` nodes labeled `0..n-1` and a list of undirected `edges`, return the number of connected components.
""", tests=[ex(5, [[0, 1], [1, 2], [3, 4]], out=2), ex(5, [[0, 1], [1, 2], [2, 3], [3, 4]], out=1), t(3, []), t(6, [[0, 1], [2, 3], [1, 0]])])
def countComponents(n, edges):
    parent = list(range(n))
    def find(x):
        while parent[x] != x:
            x = parent[x]
        return x
    for a, b in edges:
        parent[find(a)] = find(b)
    return len({find(i) for i in range(n)})


@lc("graph-valid-tree", "Graph Valid Tree", "medium", "n: int, edges: List[List[int]]", "bool", topic="graphs", desc="""
Given `n` nodes labeled `0..n-1` and a list of undirected `edges`, return `True` if the edges form a valid tree (connected, with no cycles).
""", tests=[ex(5, [[0, 1], [0, 2], [0, 3], [1, 4]], out=True), ex(5, [[0, 1], [1, 2], [2, 3], [1, 3], [1, 4]], out=False), t(1, []), t(4, [[0, 1], [2, 3]])])
def validTree(n, edges):
    return len(edges) == n - 1 and countComponents(n, edges) == 1


@lc("word-ladder", "Word Ladder", "hard", "beginWord: str, endWord: str, wordList: List[str]", "int", topic="graphs", desc="""
Transform `beginWord` into `endWord` by changing one letter at a time, where every intermediate word must be in `wordList`. Return the number of words in the shortest such sequence (including both ends), or `0` if impossible.
""", tests=[ex("hit", "cog", ["hot", "dot", "dog", "lot", "log", "cog"], out=5), ex("hit", "cog", ["hot", "dot", "dog", "lot", "log"], out=0),
            t("a", "c", ["a", "b", "c"]), t("hot", "dog", ["hot", "dog"])])
def ladderLength(beginWord, endWord, wordList):
    words, q, seen = set(wordList), deque([(beginWord, 1)]), {beginWord}
    while q:
        w, d = q.popleft()
        if w == endWord:
            return d
        for i in range(len(w)):
            for ch in "abcdefghijklmnopqrstuvwxyz":
                nw = w[:i] + ch + w[i + 1:]
                if nw in words and nw not in seen:
                    seen.add(nw); q.append((nw, d + 1))
    return 0


# ============================ 1-D Dynamic Programming ============================

@lc("climbing-stairs", "Climbing Stairs", "easy", "n: int", "int", topic="dp", desc="""
You're climbing a staircase with `n` steps and can climb 1 or 2 steps at a time. In how many distinct ways can you reach the top?
""", tests=[ex(2, out=2), ex(3, out=3), t(1), t(5), t(10), t(45)])
def climbStairs(n):
    a, b = 1, 1
    for _ in range(n):
        a, b = b, a + b
    return a


@lc("min-cost-climbing-stairs", "Min Cost Climbing Stairs", "easy", "cost: List[int]", "int", topic="dp", desc="""
`cost[i]` is the cost of stepping on stair `i`. After paying, you can climb one or two stairs. You may start on stair 0 or 1. Return the minimum cost to reach the top (just past the last stair).
""", tests=[ex([10, 15, 20], out=15), ex([1, 100, 1, 1, 1, 100, 1, 1, 100, 1], out=6), t([0, 0]), t([5, 1, 5])])
def minCostClimbingStairs(cost):
    a = b = 0
    for c in cost:
        a, b = b, min(a, b) + c
    return min(a, b)


@lc("house-robber", "House Robber", "medium", "nums: List[int]", "int", topic="dp", desc="""
Houses along a street hold `nums[i]` money. You can't rob two adjacent houses. Return the maximum amount you can rob.
""", tests=[ex([1, 2, 3, 1], out=4), ex([2, 7, 9, 3, 1], out=12), t([5]), t([2, 1, 1, 2]), t([0, 0, 0])])
def rob(nums):
    a = b = 0
    for x in nums:
        a, b = b, max(b, a + x)
    return b


@lc("house-robber-ii", "House Robber II", "medium", "nums: List[int]", "int", topic="dp", name="rob", desc="""
Same as House Robber, but the houses are arranged in a **circle**: the first and last houses are adjacent. Return the maximum amount you can rob.
""", tests=[ex([2, 3, 2], out=3), ex([1, 2, 3, 1], out=4), ex([1, 2, 3], out=3), t([5]), t([200, 3, 140, 20, 10])])
def robCircle(nums):
    return max(nums[0], rob(nums[1:]), rob(nums[:-1]))


@lc("longest-palindromic-substring", "Longest Palindromic Substring", "medium", "s: str", "str", topic="dp", desc="""
Return the longest palindromic substring of `s`. (Tests are chosen so the answer is unique.)
""", tests=[ex("cbbd", out="bb"), ex("a", out="a"), t("forgeeksskeegfor"), t("abacdfgdcaba"), t("racecarxyz")])
def longestPalindrome(s):
    best = ""
    for i in range(len(s)):
        for l, r in ((i, i), (i, i + 1)):
            while l >= 0 and r < len(s) and s[l] == s[r]:
                l -= 1; r += 1
            if r - l - 1 > len(best):
                best = s[l + 1:r]
    return best


@lc("palindromic-substrings", "Palindromic Substrings", "medium", "s: str", "int", topic="dp", desc="""
Return the number of palindromic substrings in `s`. Substrings at different positions count separately, even if they're equal.
""", tests=[ex("abc", out=3), ex("aaa", out=6), t("a"), t("abba"), t("racecar")])
def countSubstrings(s):
    return sum(s[i:j] == s[i:j][::-1] for i in range(len(s)) for j in range(i + 1, len(s) + 1))


@lc("decode-ways", "Decode Ways", "medium", "s: str", "int", topic="dp", desc="""
Letters are encoded as `"A"` → `"1"`, …, `"Z"` → `"26"`. Given a string of digits `s`, return the number of ways to decode it. Codes like `"06"` are invalid.
""", tests=[ex("12", out=2), ex("226", out=3), ex("06", out=0), t("10"), t("11106"), t("2101")])
def numDecodings(s):
    a, b = 0, 1  # ways up to i-2, i-1
    prev = ""
    for ch in s:
        cur = (b if ch != "0" else 0) + (a if prev and 10 <= int(prev + ch) <= 26 else 0)
        a, b, prev = b, cur, ch
    return b


@lc("coin-change", "Coin Change", "medium", "coins: List[int], amount: int", "int", topic="dp", desc="""
Return the fewest number of coins needed to make up `amount`, using unlimited coins of each denomination in `coins`. Return `-1` if it can't be done.
""", tests=[ex([1, 2, 5], 11, out=3), ex([2], 3, out=-1), ex([1], 0, out=0), t([186, 419, 83, 408], 6249), t([2, 5, 10, 1], 27)])
def coinChange(coins, amount):
    dp = [0] + [float("inf")] * amount
    for a in range(1, amount + 1):
        dp[a] = min([dp[a - c] + 1 for c in coins if c <= a] + [float("inf")])
    return dp[amount] if dp[amount] != float("inf") else -1


@lc("maximum-product-subarray", "Maximum Product Subarray", "medium", "nums: List[int]", "int", topic="dp", desc="""
Return the largest product of any non-empty contiguous subarray of `nums`.
""", tests=[ex([2, 3, -2, 4], out=6), ex([-2, 0, -1], out=0), t([-2]), t([-2, 3, -4]), t([0, 2]), t([-1, -2, -3, 0, 4, -1])])
def maxProduct(nums):
    best = hi = lo = nums[0]
    for x in nums[1:]:
        hi, lo = max(x, hi * x, lo * x), min(x, hi * x, lo * x)
        best = max(best, hi)
    return best


@lc("word-break", "Word Break", "medium", "s: str, wordDict: List[str]", "bool", topic="dp", desc="""
Return `True` if `s` can be split into a sequence of one or more words from `wordDict`. Words may be reused.
""", tests=[ex("leetcode", ["leet", "code"], out=True), ex("applepenapple", ["apple", "pen"], out=True), ex("catsandog", ["cats", "dog", "sand", "and", "cat"], out=False),
            t("aaaaaaa", ["aaaa", "aaa"]), t("b", ["a"])])
def wordBreak(s, wordDict):
    dp = [True] + [False] * len(s)
    for i in range(1, len(s) + 1):
        dp[i] = any(dp[i - len(w)] and s[i - len(w):i] == w for w in wordDict if len(w) <= i)
    return dp[-1]


@lc("longest-increasing-subsequence", "Longest Increasing Subsequence", "medium", "nums: List[int]", "int", topic="dp", desc="""
Return the length of the longest strictly increasing subsequence of `nums`.
""", tests=[ex([10, 9, 2, 5, 3, 7, 101, 18], out=4), ex([0, 1, 0, 3, 2, 3], out=4), ex([7, 7, 7, 7, 7, 7, 7], out=1), t([1]), t([4, 10, 4, 3, 8, 9])])
def lengthOfLIS(nums):
    import bisect
    tails = []
    for x in nums:
        i = bisect.bisect_left(tails, x)
        tails[i:i + 1] = [x]
    return len(tails)


@lc("partition-equal-subset-sum", "Partition Equal Subset Sum", "medium", "nums: List[int]", "bool", topic="dp", desc="""
Return `True` if `nums` can be split into two subsets with equal sums.
""", tests=[ex([1, 5, 11, 5], out=True), ex([1, 2, 3, 5], out=False), t([1, 1]), t([2, 2, 3, 5]), t([3, 3, 3, 4, 5])])
def canPartition(nums):
    if sum(nums) % 2:
        return False
    sums = {0}
    for x in nums:
        sums |= {s + x for s in sums}
    return sum(nums) // 2 in sums


# ============================ 2-D Dynamic Programming ============================

@lc("unique-paths", "Unique Paths", "medium", "m: int, n: int", "int", topic="dp", desc="""
A robot starts at the top-left of an `m x n` grid and can only move right or down. How many distinct paths lead to the bottom-right corner?
""", tests=[ex(3, 7, out=28), ex(3, 2, out=3), t(1, 1), t(10, 10), t(23, 12)])
def uniquePaths(m, n):
    from math import comb
    return comb(m + n - 2, m - 1)


@lc("longest-common-subsequence", "Longest Common Subsequence", "medium", "text1: str, text2: str", "int", topic="dp", desc="""
Return the length of the longest subsequence common to `text1` and `text2`, or `0` if there is none.
""", tests=[ex("abcde", "ace", out=3), ex("abc", "abc", out=3), ex("abc", "def", out=0), t("bsbininm", "jmjkbkjkv"), t("oxcpqrsvwf", "shmtulqrypy")])
def longestCommonSubsequence(text1, text2):
    @lru_cache(None)
    def go(i, j):
        if i == len(text1) or j == len(text2):
            return 0
        return 1 + go(i + 1, j + 1) if text1[i] == text2[j] else max(go(i + 1, j), go(i, j + 1))
    return go(0, 0)


@lc("best-time-to-buy-and-sell-stock-with-cooldown", "Best Time to Buy and Sell Stock with Cooldown", "medium", "prices: List[int]", "int", topic="dp", name="maxProfit", desc="""
You may complete as many buy/sell transactions as you like, holding at most one share at a time. After selling, you must wait one day (cooldown) before buying again. Return the maximum profit.
""", tests=[ex([1, 2, 3, 0, 2], out=3), ex([1], out=0), t([2, 1]), t([6, 1, 6, 4, 3, 0, 2]), t([1, 2, 4])])
def maxProfitCooldown(prices):
    hold, sold, rest = float("-inf"), 0, 0
    for p in prices:
        hold, sold, rest = max(hold, rest - p), hold + p, max(rest, sold)
    return max(sold, rest)


@lc("coin-change-ii", "Coin Change II", "medium", "amount: int, coins: List[int]", "int", topic="dp", desc="""
Return the number of combinations of coins that sum to `amount`, with unlimited coins of each denomination. Order doesn't matter (1+2 and 2+1 are the same combination).
""", tests=[ex(5, [1, 2, 5], out=4), ex(3, [2], out=0), ex(10, [10], out=1), t(0, [7]), t(100, [1, 5, 10, 25])])
def change(amount, coins):
    dp = [1] + [0] * amount
    for c in coins:
        for a in range(c, amount + 1):
            dp[a] += dp[a - c]
    return dp[amount]


@lc("target-sum", "Target Sum", "medium", "nums: List[int], target: int", "int", topic="dp", desc="""
Put a `+` or `-` in front of every number in `nums`. Return how many of these expressions evaluate to `target`.
""", tests=[ex([1, 1, 1, 1, 1], 3, out=5), ex([1], 1, out=1), t([0, 0, 1], 1), t([2, 3, 5, 7], 3), t([1, 2], 4)])
def findTargetSumWays(nums, target):
    ways = Counter({0: 1})
    for x in nums:
        nxt = Counter()
        for s, c in ways.items():
            nxt[s + x] += c; nxt[s - x] += c
        ways = nxt
    return ways[target]


@lc("interleaving-string", "Interleaving String", "medium", "s1: str, s2: str, s3: str", "bool", topic="dp", desc="""
Return `True` if `s3` can be formed by interleaving `s1` and `s2`: merging them while keeping each string's characters in their original order.
""", tests=[ex("aabcc", "dbbca", "aadbbcbcac", out=True), ex("aabcc", "dbbca", "aadbbbaccc", out=False), ex("", "", "", out=True), t("a", "", "c"), t("ab", "cd", "acbd")])
def isInterleave(s1, s2, s3):
    if len(s1) + len(s2) != len(s3):
        return False
    @lru_cache(None)
    def go(i, j):
        if i == len(s1) and j == len(s2):
            return True
        k = i + j
        return (i < len(s1) and s1[i] == s3[k] and go(i + 1, j)) or (j < len(s2) and s2[j] == s3[k] and go(i, j + 1))
    return go(0, 0)


@lc("edit-distance", "Edit Distance", "medium", "word1: str, word2: str", "int", topic="dp", desc="""
Return the minimum number of single-character insertions, deletions or substitutions needed to turn `word1` into `word2`.
""", tests=[ex("horse", "ros", out=3), ex("intention", "execution", out=5), t("", "abc"), t("abc", "abc"), t("kitten", "sitting")])
def minDistance(word1, word2):
    prev = list(range(len(word2) + 1))
    for i, a in enumerate(word1, 1):
        cur = [i]
        for j, b in enumerate(word2, 1):
            cur.append(prev[j - 1] if a == b else 1 + min(prev[j - 1], prev[j], cur[-1]))
        prev = cur
    return prev[-1]


@lc("longest-increasing-path-in-a-matrix", "Longest Increasing Path in a Matrix", "hard", "matrix: List[List[int]]", "int", topic="dp", desc="""
Return the length of the longest strictly increasing path in `matrix`, moving up, down, left or right (no diagonals or wrap-around).
""", tests=[ex([[9, 9, 4], [6, 6, 8], [2, 1, 1]], out=4), ex([[3, 4, 5], [3, 2, 6], [2, 2, 1]], out=4), ex([[1]], out=1), t([[1, 2, 3], [6, 5, 4], [7, 8, 9]])])
def longestIncreasingPath(matrix):
    R, C = len(matrix), len(matrix[0])
    @lru_cache(None)
    def go(r, c):
        return 1 + max([go(r + dr, c + dc) for dr, dc in _DIRS
                        if 0 <= r + dr < R and 0 <= c + dc < C and matrix[r + dr][c + dc] > matrix[r][c]] + [0])
    return max(go(r, c) for r in range(R) for c in range(C))


@lc("distinct-subsequences", "Distinct Subsequences", "hard", "s: str, t: str", "int", topic="dp", desc="""
Return the number of distinct subsequences of `s` that equal `t`.
""", tests=[ex("rabbbit", "rabbit", out=3), ex("babgbag", "bag", out=5), t("a", "b"), t("aaaa", "aa"), t("", "a")])
def numDistinct(s, t):
    dp = [1] + [0] * len(t)
    for ch in s:
        for j in range(len(t), 0, -1):
            if t[j - 1] == ch:
                dp[j] += dp[j - 1]
    return dp[-1]


@lc("burst-balloons", "Burst Balloons", "hard", "nums: List[int]", "int", topic="dp", desc="""
Bursting balloon `i` earns `nums[i - 1] * nums[i] * nums[i + 1]` coins, using the current neighbors (out-of-range neighbors count as `1`); then its neighbors become adjacent. Return the maximum coins from bursting all balloons.
""", tests=[ex([3, 1, 5, 8], out=167), ex([1, 5], out=10), t([7]), t([9, 76, 64, 21])])
def maxCoins(nums):
    a = [1] + nums + [1]
    @lru_cache(None)
    def go(l, r):
        return max([a[l] * a[k] * a[r] + go(l, k) + go(k, r) for k in range(l + 1, r)] + [0])
    return go(0, len(a) - 1)


@lc("regular-expression-matching", "Regular Expression Matching", "hard", "s: str, p: str", "bool", topic="dp", desc="""
Implement regular expression matching with `.` (any single character) and `*` (zero or more of the preceding element). The pattern must match the **entire** string.
""", tests=[ex("aa", "a", out=False), ex("aa", "a*", out=True), ex("ab", ".*", out=True), t("aab", "c*a*b"), t("mississippi", "mis*is*p*."), t("", "a*b*")])
def isMatch(s, p):
    import re
    return re.fullmatch(p, s) is not None
