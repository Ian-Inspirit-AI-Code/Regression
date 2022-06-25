from Point import Point, randomPoint

from numpy import cos, arctan


class Line:
    COUNTER = 0

    def __init__(self, point1: Point, point2: Point):
        self.point1 = point1
        self.point2 = point2

        self.number = self.COUNTER
        self.incrementCounter()

    @property
    def slope(self):
        try:
            return (self.point2.y - self.point1.y) / (self.point2.x - self.point1.x)
        except ZeroDivisionError:
            return 1000

    @property
    def intercept(self):
        return self(0)

    @property
    def xIntercept(self):
        return - self.intercept / self.slope

    @property
    def displayedPoints(self):
        return [self.point1, self.point2]

    def residual(self, point: Point):
        return point.y - self(point.x)

    def pointAtY(self, y: float) -> Point:
        x = (y - self.intercept) / self.slope
        return Point(x, y)

    def __call__(self, x) -> float:
        return self.slope * (x - self.point1.x) + self.point1.y

    def __contains__(self, item: Point) -> bool:
        return item in self.displayedPoints

    def __str__(self):
        return f"{self.point1}--{self.point2}"

    def __deepcopy__(self, memo):
        return Line(deepcopy(self.point1), deepcopy(self.point2))

    def toTag(self) -> str:
        return f"Line:{self.number}"

    def onLine(self, point: Point) -> bool:
        return self(point.x) == point.y

    def calculateDistance(self, point: Point, residual: float = None) -> float:
        y = self(point.x)
        residual = point.y - y if residual is None else residual
        theta = arctan((y - self.intercept) / point.x)

        return cos(theta) * residual

    def calculateRSquared(self, points: list[Point]):
        # TODO: Not functional sometimes
        if not points:
            return 0

        average = sum([point.y for point in points]) / len(points)
        baselineDifferencesSquared = [(point.y - average) ** 2 for point in points]

        return 1 - self.sumResidualSquared(points) / sum(baselineDifferencesSquared)

    def sumResidualSquared(self, points: list[Point]):
        if not points:
            return 0

        return sum([self.residual(point) ** 2 for point in points])

    @classmethod
    def incrementCounter(cls):
        cls.COUNTER += 1


class PointSlopeLine(Line):
    def __init__(self, point: Point, slope: float):
        super().__init__(point, Point(point.x + 1, point.y + slope))

    def equation(self):
        return f"y = {slope}(x-{self.point1.x}) + {self.point1.y}"

    @property
    def displayedPoints(self):
        return [self.points1]


class SlopeIntercept(Line):
    def __init__(self, slope: float, intercept: float):
        super().__init__(Point(0, intercept), Point(1, intercept + slope))

    @property
    def displayedPoints(self):
        return [self.point1]

    def equation(self):
        return f"y = {slope}x + {self.intercept}"


def randomLine(xMin, xMax, yMin, yMax) -> Line:
    return Line(randomPoint(xMin, xMax, yMin, yMax), randomPoint(xMin, xMax, yMin, yMax))
