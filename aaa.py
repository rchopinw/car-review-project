def isMonotonic(L):
    # Write your code here.
    if not L:
        return False
    if all([i >= j for i, j in zip(L, L[1:])]) or all([i <= j for i, j in zip(L, L[1:])]):
        return True
    else:
        return False


def isAscending(L):
    # Write your code here.
    if not L:
        return False
    return True if all([i <= j for i, j in zip(L, L[1:])]) else False


def test_e1_1():
    # Test cases for new functions above
    cases = [[], [1, 2, 2, 5], [4, 2, 1, 1, -10], [1, 5, 4], [1, 1, 1, 1], [4, 3, 2, 1, -10]]
    mono_answers = [False, True, True, False, True, True]
    asc_answers = [False, True, False, False, True, False]
    for i, j, k in zip(cases, mono_answers, asc_answers):
        assert isMonotonic(i) == j
        assert isAscending(i) == k


import bisect


def ascContains(A, e):
    # Write your code here.
    if not A:
        return False
    idx = bisect.bisect(A, e)
    if A[idx-1] == e:
        return True
    return False


def ascInsert(A, e):
    # Write your code here.
    bisect.insort_left(A, e)


def ascDelete(A, e):
    # Write your code here.
    if ascContains(A, e):
        A.remove(e)


def test_e1_2():
    # Test cases for new functions above
    A1 = [3, 5, 6, 10, 21, 22, 80, 80, 80]
    e1 = 20
    e2 = 21
    e3 = 111
    assert ascContains(A1, e1) is False
    assert ascContains(A1, e2) is True
    ascInsert(A1, e1)
    assert A1 == [3, 5, 6, 10, 20, 21, 22, 80, 80, 80]
    ascDelete(A1, e2)
    assert A1 == [3, 5, 6, 10, 20, 22, 80, 80, 80]
    ascDelete(A1, e3)
    assert A1 == [3, 5, 6, 10, 20, 22, 80, 80, 80]

    A2 = []
    e1 = 10
    assert ascContains(A2, e1) is False


def ascMerge(A, B):
    # hint consider using bisect and a variant of merge. Return the result in ascending order.
    # Time Complexity O(N log(N)) | Space Complexity O(N)
    res = [x for x in A]
    [ascInsert(res, x) for x in B]
    return res


def ascUnion(A, B):
    # hint consider using bisect and a variant of merge. Return the result in ascending.
    # Time Complexity O(N log(N)) | Space Complexity O(N)
    res = []
    p1 = 0
    p2 = 0
    n, m = len(A), len(B)
    while p1 < n and p2 < m:
        if A[p1] <= B[p2]:
            tmp = A[p1]
            p1 += 1
        else:
            tmp = B[p2]
            p2 += 1
        if not ascContains(res, tmp):
            res.append(tmp)
    res += [x for x in A[p1:] if x not in res]
    res += [x for x in B[p2:] if x not in res]
    return res


def ascIntersection(A, B):
    # hint consider using bisect and a variant of merge. Return the result in ascending order.
    # Time Complexity O(N log(N)) | Space Complexity O(N)
    res = []
    for i in B:
        if ascContains(A, i):
            res.append(i)
    return res


def test_e1_3():
    # Test cases for new functions above
    A = []
    B = [1, 2, 3]
    assert [1, 2, 3] == ascMerge(A, B)
    assert [] == ascIntersection(A, B)

    A = [2, 5, 6, 10]
    B = [5, 10, 17, 18, 20]
    assert [2, 5, 5, 6, 10, 10, 17, 18, 20] == ascMerge(A, B)
    assert [2, 5, 6, 10, 17, 18, 20] == ascUnion(A, B)
    assert [5, 10] == ascIntersection(A, B)


from collections.abc import MutableSet


class OrderedSet(MutableSet):

    ### TODO e1.2.2
    ### Add an appropriate docstring to each method below
    ### Add a comment above each method with its and time and space complexity

    def __init__(self, iterable=None):
        self.end = end = []
        end += [None, end, end]  # sentinel node for doubly linked list
        self.map = {}  # key --> [key, prev, next]
        if iterable is not None:
            self |= iterable

    def __len__(self):
        return len(self.map)

    def __contains__(self, key):
        return key in self.map

    def add(self, key):
        if key not in self.map:
            end = self.end
            curr = end[1]
            curr[2] = end[1] = self.map[key] = [key, curr, end]

    def discard(self, key):
        if key in self.map:
            key, prev, next = self.map.pop(key)
            prev[2] = next
            next[1] = prev

    def pop(self, last=True):
        if not self:
            raise KeyError('set is empty')
        key = self.end[1][0] if last else self.end[2][0]
        self.discard(key)
        return key

    def __eq__(self, other):
        if isinstance(other, OrderedSet):
            return len(self) == len(other) and list(self) == list(other)
        return set(self) == set(other)

    def __iter__(self):
        end = self.end
        curr = end[2]
        while curr is not end:
            yield curr[0]
            curr = curr[2]

    def __reversed__(self):
        end = self.end
        curr = end[1]
        while curr is not end:
            yield curr[0]
            curr = curr[1]

    def __repr__(self):
        if not self:
            return f'{self.__class__.__name__}()'
        return f'{self.__class__.__name__}({list(self)})'


if __name__ == '__main__':
    s = OrderedSet('shazaam')
    t = OrderedSet('simsalabim')
    print(s)
    print(t)
    print('Union:', s | t)
    print('Intersection:', s & t)
    print('Difference:', s - t)

    g = OrderedSet('ssaakk')
    k = OrderedSet('wwwwwok')
    print("This is an example of three elements ordered set: {}".format(g))
    print('Union operation between g and k: {}'.format(g | k))
    print('Intersection operation between g and k: {}'.format(g & k))
    print('Difference operation between g and k: {}'.format(g - k))

from copy import deepcopy
def count_sort(L):
    """
    This function implements the counting sort of a list L
    :param L: a list of elements to be sorted
    :return: the sorted list
    Time Complexity O(N+k) | Space Complexity O(N+k)
    """
    lc = deepcopy(L)
    if not lc:  # If is an empty list
        return lc
    m = max(lc) + 1  # Calculate the range of the list
    arr = [0 for _ in range(m)]  # Creat a list of same range
    idx = 0
    l = len(lc)
    for i in range(l):
        if not arr[lc[i]]:
            arr[L[i]] = 0
        arr[lc[i]] += 1
    for j in range(m):
        while arr[j] > 0:
            lc[idx] = j
            idx += 1
            arr[j] -= 1
    return lc

def count_ort(L):
    m = max(L)
    arr_len = m + 1
    bucket = [0]*bucketLen
    sortedIndex =0
    arrLen = len(L)
    for i in range(arrLen):
        if not bucket[L[i]]:
            bucket[L[i]]=0
        bucket[L[i]]+=1
    for j in range(bucketLen):
        while bucket[j]>0:
            L[sortedIndex] = j
            sortedIndex+=1
            bucket[j]-=1
    return L