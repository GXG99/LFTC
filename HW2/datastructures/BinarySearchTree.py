class BinarySearchTree:
    def __init__(self, data=None):
        self.left = None
        self.right = None
        self.data = data

    def insert(self, data):
        if self.data is None:
            self.data = data
            return
        if self.data == data:
            return
        if data < self.data:
            if self.left is not None:
                self.left.insert(data)
                return
            self.left = BinarySearchTree(data)
            return
        if self.right is not None:
            self.right.insert(data)
            return
        self.right = BinarySearchTree(data)

    def get_min(self):
        current = self
        while current.left is not None:
            current = current.left
        return current.data

    def get_max(self):
        current = self
        while current.right is not None:
            current = current.right
        return current.data

    def exists(self, data):
        if self.data == data:
            return True
        if data < self.data:
            if self.left is None:
                return False
            return self.left.exists(data)
        if self.right is None:
            return False
        return self.right.exists(data)

    def inorder(self, values):  # Left Root Right
        if self.left is not None:
            self.left.inorder(values)
        if self.data is not None:
            values.append(self.data)
        if self.right is not None:
            self.right.inorder(values)
        return values
