from enum import Enum
from math import inf, pi, acos, atan2, isclose
from typing import Iterable


class Vector:
    def __init__(self, *coords: Iterable[float]):
        self.coords = tuple(coords)
    
    @property
    def x(self):
        return self.coords[0]
    
    @property
    def y(self):
        return self.coords[1]
    
    @property
    def z(self):
        return self.coords[2]
    
    @classmethod
    def from_points(cls, point1, point2):
        return cls(*(point2 - point1).coords)
    
    @classmethod
    def dot_product(cls, vector1, vector2):
        if not isinstance(vector1, cls) or not isinstance(vector2, cls):
            raise TypeError(f"operands must be of type {vector1.__class__}")

        return sum(c1 * c2 for c1, c2 in zip(vector1.coords, vector2.coords))

    @classmethod
    def cross_product(cls, vector1, vector2):
        if not isinstance(vector1, cls) or not isinstance(vector2, cls):
            raise TypeError(f"operands must be of type {vector1.__class__}")

        return vector1.x * vector2.y - vector1.y * vector2.x

    def norm(self, metric="euclidean"):
        try:
            p = {
                "octahedral": 1,
                "euclidean": 2,
                "cubic": inf
            }[metric]
        except KeyError:
            raise ValueError(f'unknown metric "{metric}"')

        if p == inf:
            return max(abs(c) for c in self.coords)
        
        return sum(abs(c**p) for c in self.coords) ** (1 / p)
    
    def normalize(self, metric="euclidean"):
        self.coords = tuple(c / self.norm(metric) for c in self.coords)
    
    def __str__(self):
        return f"({', '.join(str(c) for c in self.coords)})"
    
    def __repr__(self):
        return str(self)


class Point:
    def __init__(self, *coords: Iterable[float]):
        self.coords = tuple(coords)
    
    @property
    def x(self):
        return self.coords[0]
    
    @property
    def y(self):
        return self.coords[1]
    
    @property
    def z(self):
        return self.coords[2]
    
    @classmethod
    def centroid(cls, *points):
        return cls(*(sum(coord) / len(coord) for coord in zip(*points)))
    
    @staticmethod
    def angle(point1, point2, point3):
        v1 = Vector.from_points(point2, point1)
        v2 = Vector.from_points(point2, point3)
        v1.normalize()
        v2.normalize()

        return acos(Vector.dot_product(v1, v2) / (v1.norm() * v2.norm()))

    @staticmethod
    def polar_angle(point, origin):
        return atan2(point.y-origin.y, point.x-origin.x)
    
    @classmethod
    def nonnegative_polar_angle(cls, point, origin):
        angle = cls.polar_angle(point, origin)
        return angle if angle >= 0 else 2 * pi + angle

    @classmethod
    def dist(cls, point, obj, metric="euclidean"):
        if isinstance(obj, cls):
            try:
                p = {
                    "manhattan": 1,
                    "euclidean": 2,
                    "chebyshev": inf
                }[metric]
            except KeyError:
                raise ValueError(f'unknown metric "{metric}"')
            
            if p == inf:
                return max(abs(c1-c2) for c1, c2 in zip(point.coords, obj.coords))
            
            return sum(abs((c1-c2)**p) for c1, c2 in zip(point.coords, obj.coords)) ** (1 / p)
        
        if isinstance(obj, Line2D):
            try:
                p = {
                    "euclidean": 2,
                    "manhattan": inf
                }[metric]
            except KeyError:
                raise ValueError(f'unknown metric "{metric}"')
            
            denominator = max(abs(obj.a, obj.b)) if p == inf else (obj.a**2 + obj.b**2) ** 0.5
            return abs(obj.a*point.x+obj.b*point.y+obj.c) / denominator

    @staticmethod
    def direction(point1, point2, point3):
        v1 = Vector.from_points(point1, point3)
        v2 = Vector.from_points(point1, point2)

        return Vector.cross_product(v1, v2)

    def __len__(self):
        return len(self.coords)
    
    def __getitem__(self, key):
        return self.coords[key]
    
    def __eq__(self, other):
        return (
            isinstance(other, self.__class__)
            and all(isclose(c1, c2, abs_tol=1e-3, rel_tol=0) for c1, c2 in zip(self.coords, other.coords))
        )
    
    def __lt__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError(f'right operand of "<" must be of {self.__class__} type')
        
        return self.coords < other.coords

    def __add__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError(f"right operand of addition must be of {self.__class__} type")
        
        return self.__class__(*(c1 + c2 for c1, c2 in zip(self.coords, other.coords)))
    
    def __sub__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError(f"right operand of addition must be of {self.__class__} type")
        
        return self.__class__(*(c1 - c2 for c1, c2 in zip(self.coords, other.coords)))
    
    def __hash__(self):
        return hash(self.coords)
    
    def __str__(self):
        return f"({', '.join(str(c) for c in self.coords)})"
    
    def __repr__(self):
        return str(self)


class Line2D:
    """A 2D line represented by the equation ax + by + c = 0 or y = slope * x + y_intercept."""
    def __init__(self, point1, point2):
        if not isinstance(point1, Point) or not isinstance(point2, Point):
            raise TypeError(f"2D line must be initialized with two distinct points of type {Point}")
        if point1 == point2:
            raise ValueError(f"2D line must be initialized with two distinct points")

        self.point1 = point1
        self.point2 = point2
    
    @property
    def a(self):
        return self.point1.y - self.point2.y
    
    @property
    def b(self):
        return self.point2.x - self.point1.x
    
    @property
    def c(self):
        return self.point1.x * self.point2.y - self.point2.x * self.point1.y
    
    @property
    def slope(self):
        return -inf if self.b == 0 else -self.a / self.b
    
    @property
    def y_intercept(self):
        return -inf if self.b == 0 else -self.c / self.b



class BinTreeNode:
    def __init__(self, data, left=None, right=None):
        self.data = data
        self.left = left
        self.right = right
    
    @property
    def is_leaf(self):
        return self.left is None and self.right is None
    
    def traverse_inorder(self, node=None, nodes=None):
        if node is None:
            node = self
        if nodes is None:
            nodes = []
        
        if node.left:
            self.traverse_inorder(node.left, nodes)
        
        nodes.append(node)

        if node.right:
            self.traverse_inorder(node.right, nodes)
        
        return nodes
    
    def __eq__(self, other):
        return (
            isinstance(other, self.__class__)
            and self.data == other.data
            and self.left == other.left
            and self.right == other.right
        )
    

class BinTree:
    node_class = BinTreeNode

    def __init__(self, root):
        self.root = root
    
    @classmethod
    def from_iterable(cls, iterable):
        return cls(cls._from_iterable(iterable))
    
    @classmethod
    def _from_iterable(cls, iterable, left=0, right=None):
        if right is None:
            right = len(iterable) - 1
        if left > right:
            return None
        
        mid = (left + right) // 2
        node = cls.node_class(iterable[mid])
        node.left = cls._from_iterable(iterable, left, mid-1)
        node.right = cls._from_iterable(iterable, mid+1, right)

        return node
    
    def traverse_inorder(self):
        return self.root.traverse_inorder()
    
    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.root == other.root


class ThreadedBinTreeNode(BinTreeNode):
    def __init__(self, data):
        super().__init__(data)
        self.prev = None
        self.next = None
    
    def __repr__(self):
        return f"{self.left.data if self.left else ''}<-{self.data}->{self.right.data if self.right else ''}"


class ThreadedBinTree(BinTree):
    node_class = ThreadedBinTreeNode

    @classmethod
    def from_iterable(cls, iterable, circular=True):
        tree = super().from_iterable(iterable)
        nodes = tree.traverse_inorder()
        
        for i, node in enumerate(nodes):            
            node.prev = node.left if node.left else nodes[i-1]
            node.next = node.right if node.right else nodes[(i+1)%len(nodes)]
        
        if not circular:
            nodes[0].prev = None
            nodes[-1].next = None
        
        return tree


class PointType(Enum):
    convex = 0
    reflex = 1
    left_supporting = 2
    right_supporting = 3

    @classmethod
    def by_nodes(cls, source, target):
        if target.prev is None:
            direction = Point.direction(source.data, target.data, target.next.data)
            if source.data.x < target.data.x:
                return cls.left_supporting if direction > 0 else cls.convex
            
            return cls.right_supporting if direction >= 0 else cls.reflex
        
        if target.next is None:
            direction = Point.direction(source.data, target.data, target.prev.data)
            if source.data.x < target.data.x:
                return cls.left_supporting if direction >= 0 else cls.reflex
            
            return cls.right_supporting if direction > 0 else cls.convex
        
        return cls.by_points(source.data, target.data, target.prev.data, target.next.data)

    @classmethod
    def by_points(cls, source, target, left, right):
        def polar_angle(point):
            """[0, 2*pi) polar angle in coordinate system with axis target -> source (rotated against x axis by rot)"""
            rot = Point.nonnegative_polar_angle(source, target)
            angle = Point.nonnegative_polar_angle(point, target)
            return angle - rot + (2 * pi if angle < rot else 0)
        
        angles = polar_angle(left), polar_angle(right)
        angle1 = min(angles)
        angle2 = max(angles)

        convex_or_reflex = 0 < angle1 <= pi <= angle2 < 2 * pi

        # Convex
        if convex_or_reflex and angle2 < angle1 + pi:
            return cls.convex
        
        # Reflex
        if convex_or_reflex and angle2 > angle1 + pi:
            return cls.reflex

        # Left supporting
        if 0 <= angle1 < angle2 < pi:
            return cls.left_supporting
        
        # Right supporting
        if angle1 == 0:
            angle1 = 2 * pi
            angle1, angle2 = angle2, angle1
        
        if pi < angle1 < angle2 <= 2 * pi:
            return cls.right_supporting
        
        raise ValueError