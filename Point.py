from random import uniform


class Point:

    COUNTER = 0

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

        self.number = self.COUNTER
        self.incrementCounter()

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __le__(self, other: float):
        return self.x <= other and self.y <= other

    def __ge__(self, other: float):
        return self.x >= other and self.y >= other

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __abs__(self):
        self.x = abs(self.x)
        self.y = abs(self.y)

        return self

    def __str__(self):
        return f"({self.x},{self.y})"

    def __deepcopy__(self, memo):
        return Point(self.x, self.y)

    def toTag(self) -> str:
        return f"Point:{self.number}"

    def close(self, other, maximumOffsetX: float, maximumOffsetY: float) -> bool:
        difference = abs(self - other)
        return difference.x <= maximumOffsetX and difference.y <= maximumOffsetY

    @classmethod
    def incrementCounter(cls):
        cls.COUNTER += 1


def randomPoint(xMin, xMax, yMin, yMax) -> Point:
    return Point(uniform(xMin, xMax), uniform(yMin, yMax))
