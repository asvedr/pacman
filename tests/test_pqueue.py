from logic.p_queue import PQueue
import unittest

class TestPQueue(unittest.TestCase):

    def test_order(self):

        target = 5
        
        def volume(num):
            return abs(target - num)

        queue = PQueue()
        source = [1,3,5,6,8]
        for val in source:
            queue.push(val, volume(val))

        self.assertEqual(len(queue), len(source))
        self.assertEqual(queue.pop(), 5)
        self.assertEqual(len(queue), len(source)-1)
        self.assertEqual(queue.pop(), 6)
        self.assertEqual(queue.pop(), 3)
        self.assertEqual(queue.pop(), 8)
        self.assertEqual(queue.pop(), 1)
        self.assertEqual(len(queue), 0)
