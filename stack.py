import unittest

class Stack:
    """ a custom stack implementation using a Python list """

    def __init__(self):
        """ instantiate the single field (a list) in our stack object """
        self.items = []

    def __str__(self):
        if len(self.items) <= 10:
            return "Field 'items' = " + str(self.items)
        else:
            return "Field 'items' = " + str(self.items[0:5]) + \
        '[,...]' + str(self.items[-5:])

    def isEmpty(self):
        """ return True if stack has zero items, False otherwise """
        return len(self.items) == 0

    def push(self, new_item):
        """ add a new item to the 'top' (or right) of the list """
        self.items.append(new_item)

    def pop(self):
        """ return and remove top-most item from the list """
        return self.items.pop()

    def peek(self):
        """ return top-most item but don't remove it """
        return self.items[-1]

    def size(self):
        """ return the size/length of the stack """
        return len(self.items)

class TestStack(unittest.TestCase):

    def testPush(self):
        s = Stack()
        s.push(5)
        s.push(8)
        self.assertIn("[5, 8]", str(s))

    def testPop(self):
        s = Stack()
        s.push(3)
        s.push(7)
        popped_item = s.pop()
        self.assertEqual(popped_item, 7)

if __name__ == '__main__':
    unittest.main()
