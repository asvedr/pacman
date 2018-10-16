import heapq


class _Node(object):

    __slots__ = 'value', 'volume'

    def __init__(self, value, volume):
        self.value = value
        self.volume = volume

    def __lt__(self, other):
        return self.volume < other.volume

    def __eq__(self, other):
        return self.volume < other.volume


class PQueue(object):

    __slots__ = 'heap'

    def __init__(self):
        self.heap = []

    def push(self, val, volume):
        heapq.heappush(self.heap, _Node(val, volume))

    def pop(self):
        node = heapq.heappop(self.heap)
        return node.value

    def __len__(self):
        return len(self.heap)

