from collections import deque
from collatz import Node, collatz_iter


class TestNode:
    def test_is_root(self):
        node = Node(1)

        assert(node.is_root)

    def test_is_leaf(self):
        node = Node(1)

        assert(node.is_leaf)

    def test_is_odd_odd(self):
        node = Node(17)

        assert (node.is_odd == True)

    def test_is_odd_even(self):
        node = Node(24)

        assert (node.is_odd == False)

    def test_depth(self):
        node = Node.collatz_tree(7).children[0].children[0]

        assert(node.depth == 2)

    def test_num_ancestors(self):
        node = Node.collatz_tree(7)

        assert(node.num_ancestors == 18)

    def test_root_of_self(self):
        node = Node(1)

        assert (node is node.root)

    def test_root(self):
        node = Node.collatz_tree(7).children[0].children[0]

        assert (node.root.number == 1)
        assert (node.root.depth == 0)
        assert (node.root.num_ancestors == 18)
        assert (node.root.parent is None)

    def test_collatz_tree(self):
        root = Node.collatz_tree(7)

        one = Node(1)
        two = Node(2, one)
        four = Node(4, two)
        eight = Node(8, four)
        sixteen = Node(16, eight)
        five = Node(5, sixteen)
        ten = Node(10, five)
        three = Node(3, ten)
        six = Node(6, three)
        twenty = Node(20, ten)
        forty = Node(40, twenty)
        thirteen = Node(13, forty)
        twenty_six = Node(26, thirteen)
        fifty_two = Node(52, twenty_six)
        seventeen = Node(17, fifty_two)
        thirty_four = Node(34, seventeen)
        eleven = Node(11, thirty_four)
        twenty_two = Node(22, eleven)
        seven = Node(7, twenty_two)

        one.children.append(two)
        two.children.append(four)
        four.children.append(eight)
        eight.children.append(sixteen)
        sixteen.children.append(five)
        five.children.append(ten)
        ten.children.extend((twenty, three))
        three.children.append(six)
        twenty.children.append(forty)
        forty.children.append(thirteen)
        thirteen.children.append(twenty_six)
        twenty_six.children.append(fifty_two)
        fifty_two.children.append(seventeen)
        seventeen.children.append(thirty_four)
        thirty_four.children.append(eleven)
        eleven.children.append(twenty_two)
        twenty_two.children.append(seven)

        stack1 = deque([root])
        stack2 = deque([one])

        while stack1 and stack2:
            node1 = stack1.pop()
            node2 = stack2.pop()

            assert (node1.number == node2.number)
            assert (node1.depth == node2.depth)
            assert (node1.num_ancestors == node2.num_ancestors)
            assert (node1.parent.number == node2.parent.number
                    if node1.parent and node2.parent
                    else node1.parent is None and node2.parent is None)

            for child1 in node1.children:
                stack1.append(child1)

            for child2 in node2.children:
                stack2.append(child2)


def test_collatz_iter():
    n = 9
    expected = [28, 14, 7, 22, 11, 34, 17, 52,
                26, 13, 40, 20, 10, 5, 16, 8, 4, 2, 1]
    actual = list(collatz_iter(n))

    assert (expected == actual)
