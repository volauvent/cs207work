import uuid
class BinaryTree:
    def __init__(self, data, parent=None):
        self.data = data
        self.parent = parent
        self.uuid= uuid.uuid4()
        self.left = None
        self.right = None    
            
    def addLeftChild(self, data): 
        n = self.__class__(data, self)
        self.left = n
        return n
        
    def addRightChild(self, data):
        n = self.__class__(data, self)
        self.right = n
        return n
        
    def hasLeftChild(self):
        return self.left is not None

    def hasRightChild(self):
        return self.right is not None

    def hasAnyChild(self):
        return self.hasRightChild() or self.hasLeftChild()

    def hasBothChildren(self):
        return self.hasRightChild() and self.hasLeftChild()
    
    def hasNoChildren(self):
        return not self.hasRightChild() and not self.hasLeftChild()
    
    def isLeftChild(self):
        return self.parent and self.parent.left == self

    def isRightChild(self):
        return self.parent and self.parent.right == self

    def isRoot(self):
        return not self.parent

    def isLeaf(self):
        return not (self.right or self.left)
    
            
    def preorder(self):
        if self.isLeftChild():
            yield (self.parent, self, "left")
        elif self.isRightChild():
            yield (self.parent, self, "right")
        if self.hasLeftChild():
            for v in self.left.preorder():
                yield v
        if self.hasRightChild():
            for v in self.right.preorder():
                yield v

class BinarySearchTree(BinaryTree):
        
    def __init__(self, data, parent=None):
        super().__init__(data, parent)
        self.count = 1

    def _insert_hook(self):
        pass
            
    def insert(self, data):
        if data < self.data:
            if self.hasLeftChild():
                self.left.insert(data)
            else:
                self.addLeftChild(data)
                self._insert_hook()
        elif data > self.data:
            if self.hasRightChild():
                self.right.insert(data)
            else:
                self.addRightChild(data)
                self._insert_hook()
        else: #duplicate value
            self.count += 1
            self._insert_hook()
            
    def search(self, data):
        if self.data == data:
            return self
        elif data < self.data and self.left:
            return self.left.search(data)
        elif data > self.data and self.right:
            return self.right.search(data)
        else:
            return None
        
    def delete(self, data):        
        if self.isRoot() and self.hasNoChildren() and self.data==data:#deleting the whole tree
            self.root=None#todo call a destructor that signals GC it can reap
            #self._update_sizes(up=False) #really tree is gone
            self._remove_hook()
        elif self.hasAnyChild():
            noder = self.search(data)
            if noder:
                self._remove(noder)
            else:
                raise ValueError("No such data {} in tree".format(data))
        else:
            raise ValueError("No such data {} in tree".format(data))

    def _remove_hook(self, up=False, by=1):
        pass
    
    def _remove(self, node):
        if node.isLeaf():
            if node.isLeftChild():
                node.parent.left = None
            else:
                node.parent.right = None
            #node._update_sizes(up=False, by=node.count)
            node._remove_hook(by=node.count)
            del node
        elif node.hasBothChildren():
            s = node.successor()
            #successor is guaranteed to have right child only
            s.spliceOut()
            #s._update_sizes(up=False, by=s.count)
            s._remove_hook(by=s.count)
            #handled more generally above
            #s.right.parent = s.parent
            #s.parent.left = s.right
            node.data = s.data
            #diff = s.count - node.count            
            #node._update_sizes(by=diff)
            node._remove_hook(up=True, by = s.count - node.count)
            node.count = s.count
            del s #the node became the successor
        else: # one child case
            if node.hasLeftChild():
                if node.isLeftChild():
                    node.left.parent = node.parent
                    node.parent.left = node.left
                elif node.isRightChild():
                    node.left.parent = node.parent
                    node.parent.right = node.left
                else: #root
                    self.root = node.left
                #node._update_sizes(up=False, by=node.count)
                node._remove_hook(by=node.count)
                del node
            else:
                if node.isLeftChild():
                    node.right.parent = node.parent
                    node.parent.left = node.right
                elif node.isRightChild():
                    node.right.parent = node.parent
                    node.parent.right = node.right
                else: #root
                    self.root = node.right
                #node._update_sizes(up=False, by=node.count)
                node._remove_hook(by=node.count)
                del node
                    
    def findMin(self):
        minnode = self
        while minnode.hasLeftChild():
            minnode = minnode.left
        return minnode
    
    def findMax(self):
        maxnode = self
        while maxnode.hasRightChild():
            maxnode = maxnode.right
        return maxnode
    
    def successor(self):
        s = None
        if self.hasRightChild():
            s = self.right.findMin()
        else:
            if self.parent:
                if self.isLeftChild():
                    s = self.parent
                else:
                    self.parent.right=None
                    s = self.parent.successor()
                    self.parent.right=self
        return s
    
    def predecessor(self):
        p=None
        if self.hasLeftChild():
            p = self.left.findMax()
        else:
            if self.parent:
                if self.isRightChild():
                    p = self.parent
                else:
                    self.parent.left = None
                    p = self.parent.predecessor()
                    self.parent.left = self
        return p
            
    def spliceOut(self):
        if self.isLeaf():
            if self.isLeftChild():
                self.parent.left = None
            else:
                self.parent.right = None
        elif self.hasAnyChild():
            if self.hasLeftChild():
                if self.isLeftChild():
                    self.parent.left = self.left
                else:
                    self.parent.right = self.left
                self.left.parent = self.parent
            else:
                if self.isLeftChild():
                    self.parent.left = self.right
                else:
                    self.parent.right = self.right
                self.right.parent = self.parent
       

    #now implement various pythonic things
    
    def __iter__(self):
        if self is not None:
            if self.hasLeftChild():
                for node in self.left:
                    yield node
            for _ in range(self.count):
                yield self
            if self.hasRightChild():
                for node in self.right:
                    yield node
                    
    def __len__(self):#expensive O(n) version
        start=0
        for node in self:
            start += 1
        return start
    
    def __getitem__(self, i):
        return self.ithorder(i+1)
    
    def __contains__(self, data):
        return self.search(data) is not None



class AugmentedBinarySearchTree(BinarySearchTree):
        
    def __init__(self, data, parent=None):
        super().__init__(data, parent)
        self.size = 1
        
    def _update_sizes(self, up=True, by=1):
        if up:
            inc = by
        else:
            inc = -by
        self.size += inc
        curr = self
        while curr.parent is not None:
            curr.parent.size += inc
            curr = curr.parent
       
    def _insert_hook(self):#insert up, by 1
        self._update_sizes()
            
    def _remove_hook(self, up=False, by=1):
        self._update_sizes(up, by)
        
    
    def ithorder(self, i): #starts from 1
        if self.hasLeftChild():
            a = self.left.size
        else:
            a = 0
        dupes = self.count - 1
        if  a+1 <= i  < a+1 + dupes:
            return self
        if i < a + 1 : #wont go here for size 0 on left
            return self.left.ithorder(i)
        elif  a+1 <= i  <= a+1 + dupes:
            return self
        else:#ok to have self.right here and not check right child
            return self.right.ithorder(i - a -1 -dupes)
       
    def _rankof(self, data):
        if self.data == data:#found at top
            if self.hasLeftChild():
                return self.left.size + self.count, self.count
            else:
                return self.count, self.count
        elif data < self.data and self.left:
            return self.left._rankof(data)
        elif data > self.data and self.right:
            rtup = self.right._rankof(data)
            if self.hasLeftChild():
                return self.count + self.left.size+rtup[0], rtup[1]
            else:
                return self.count + rtup[0], rtup[1]
        else:
            raise ValueError("{} not found".format(x))
            
    def rankof(self, data):
        ranktup = self._rankof(data)
        return [ranktup[0] - e for e in range(ranktup[1])]
    
    
    #now implement various pythonic things
    
    def __len__(self):
        return self.size

    
    def __getitem__(self, i):
        return self.ithorder(i+1)