from src.node import BPlusTreeNode

class BPlusTree:
    def __init__(self, order=4):
        self.root = BPlusTreeNode(is_leaf=True)
        self.order = order

    def _find_leaf(self, key):
        node = self.root
        while not node.is_leaf:
            i = 0
            while i < len(node.keys) and key >= node.keys[i]:
                i += 1
            node = node.children[i]
        return node

    def insert(self, key, value):
        leaf = self._find_leaf(key)

        insert_idx = 0
        while insert_idx < len(leaf.keys) and key > leaf.keys[insert_idx]:
            insert_idx += 1

        leaf.keys.insert(insert_idx, key)
        leaf.children.insert(insert_idx, value)

        if len(leaf.keys) > self.order - 1:
            self._split_leaf(leaf)

    def _split_leaf(self, leaf):
        new_leaf = BPlusTreeNode(is_leaf=True)
        mid = len(leaf.keys) // 2

        new_leaf.keys = leaf.keys[mid:]
        new_leaf.children = leaf.children[mid:]
        leaf.keys = leaf.keys[:mid]
        leaf.children = leaf.children[:mid]

        new_leaf.next_leaf = leaf.next_leaf
        leaf.next_leaf = new_leaf

        if leaf == self.root:
            new_root = BPlusTreeNode()
            new_root.keys = [new_leaf.keys[0]]
            new_root.children = [leaf, new_leaf]
            self.root = new_root
            leaf.parent = new_root
            new_leaf.parent = new_root
        else:
            parent = leaf.parent
            insert_idx = 0
            while insert_idx < len(parent.keys) and new_leaf.keys[0] > parent.keys[insert_idx]:
                insert_idx += 1

            parent.keys.insert(insert_idx, new_leaf.keys[0])
            parent.children.insert(insert_idx + 1, new_leaf)
            new_leaf.parent = parent

            if len(parent.keys) > self.order - 1:
                self._split_internal(parent)

    def _split_internal(self, node):
        new_internal = BPlusTreeNode()
        mid = len(node.keys) // 2

        push_key = node.keys[mid]

        new_internal.keys = node.keys[mid + 1:]
        new_internal.children = node.children[mid + 1:]
        for child in new_internal.children:
            child.parent = new_internal

        node.keys = node.keys[:mid]
        node.children = node.children[:mid + 1]

        if node == self.root:
            new_root = BPlusTreeNode()
            new_root.keys = [push_key]
            new_root.children = [node, new_internal]
            self.root = new_root
            node.parent = new_root
            new_internal.parent = new_root
        else:
            parent = node.parent
            insert_idx = 0
            while insert_idx < len(parent.keys) and push_key > parent.keys[insert_idx]:
                insert_idx += 1

            parent.keys.insert(insert_idx, push_key)
            parent.children.insert(insert_idx + 1, new_internal)
            new_internal.parent = parent

            if len(parent.keys) > self.order - 1:
                self._split_internal(parent)

    def search(self, key):
        leaf = self._find_leaf(key)
        for i, k in enumerate(leaf.keys):
            if k == key:
                return leaf.children[i]
        return None

    def search_greater_than(self, key):
        result = []
        leaf = self._find_leaf(key)
        while leaf:
            for i, k in enumerate(leaf.keys):
                if k > key:
                    result.append((k, leaf.children[i]))
            leaf = leaf.next_leaf
        return result

    def search_less_than(self, key):
        result = []
        node = self.root
        while not node.is_leaf:
            node = node.children[0]

        while node:
            for i, k in enumerate(node.keys):
                if k < key:
                    result.append((k, node.children[i]))
                else:
                    return result
            node = node.next_leaf
        return result

    def delete(self, key):
        leaf = self._find_leaf(key)
        if key in leaf.keys:
            index = leaf.keys.index(key)
            leaf.keys.pop(index)
            leaf.children.pop(index)

    def print_tree(self, node=None, level=0):
        if node is None:
            node = self.root

        indent = "  " * level
        if node.is_leaf:
            print(f"{indent}Leaf: {node.keys}")
        else:
            print(f"{indent}Internal: {node.keys}")
            for child in node.children:
                self.print_tree(child, level + 1)