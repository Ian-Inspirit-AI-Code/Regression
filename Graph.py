import tkinter as tk

from numpy import sin, cos, arctan
from copy import deepcopy


class Point:

    COUNTER = 0

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

        self.number = self.COUNTER

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

    def close(self, other, maximumOffset: float):
        difference = abs(self - other)
        return difference <= maximumOffset


class Line:
    COUNTER = 0

    def __init__(self, point1: Point, point2: Point):
        self.point1 = point1
        self.point2 = point2

        self.number = self.COUNTER

    @property
    def slope(self):
        return (self.point2.y - self.point1.y) / (self.point2.x - self.point1.x)

    @property
    def intercept(self):
        return self(0)

    def residual(self, point: Point):
        return point.y - self(point.x)

    def __call__(self, x) -> float:
        return self.slope * (x - self.point1.x) + self.point1.y

    def __contains__(self, item: Point):
        return item == self.point1 or item == self.point2

    def __str__(self):
        return f"{self.point1}--{self.point2}"

    def __deepcopy__(self, memo):
        return Line(deepcopy(self.point1), deepcopy(self.point2))

    def calculateDistance(self, point: Point, residual: float) -> float:
        y = point.y + residual
        theta = arctan((y - self.intercept) / point.x)

        return cos(theta) * residual

    def calculateRSquared(self, points: list[Point]):
        if not points:
            return 0

        average = sum([point.y for point in points]) / len(points)

        baselineDifferencesSquared = [(point.y - average) ** 2 for point in points]

        # print(average, residualsArraySquared, baselineDifferencesSquared)
        # print("aaa", sum(residualsArraySquared))

        return 1 - self.sumResidualSquared(points) / sum(baselineDifferencesSquared)

    def sumResidualSquared(self, points: list[Point]):
        if not points:
            return 0

        return sum([self.residual(point) ** 2 for point in points])


class Graph(tk.Tk):
    BACKGROUND_COLOR = "#F8DAD4"

    LINE_COLOR = "#0C51FA"
    LINE_THICKNESS = 3

    HEIGHT = 450
    WIDTH = 800

    MARGIN = 75

    X_INTERVALS = 1
    Y_INTERVALS = 20

    LABEL_LENGTH = 5

    FONT_SIZE = 10
    FONT = "Arial"

    DOT_SIZE = 12
    DOT_COLOR = "#FD0B0B"
    LINE_POINT_COLOR = "#5FEEF8"

    RESIDUAL_COLOR = "#DD5FF8"

    POINT_MAXIMUM_OFFSET = 1

    def __init__(self):
        super().__init__()

        self.canvas = tk.Canvas(self, bg=self.BACKGROUND_COLOR, height=self.HEIGHT, width=self.WIDTH)
        self.canvas.pack()

        self.minX, self.minY = 6, -20
        self.maxX = 10
        self.maxY = 80

        self.initDisplay()

        self.line = None
        self.linePoints = []
        self.points = []

        self.draggingPoint = None

        self.button = tk.Button(self, text="Line of best fit", width=20, height=2, command=self.createBestFitLine)
        self.button.pack()

        self.bind('<Button-1>', self.mouseClick)  # left click
        self.bind('<ButtonRelease-1>', lambda event: self.mouseRelease())  # left click release
        self.bind('<Motion>', self.motion)  # mouse moving

    @property
    def lineBottom(self) -> int:
        return self.HEIGHT - self.MARGIN

    @property
    def lineTop(self) -> int:
        return self.MARGIN

    @property
    def lineLeft(self) -> int:
        return self.MARGIN

    @property
    def lineRight(self) -> int:
        return self.WIDTH - self.MARGIN

    @property
    def xPixelSpan(self) -> float:
        return self.WIDTH - self.MARGIN - self.MARGIN

    @property
    def yPixelSpan(self) -> float:
        return self.HEIGHT - self.MARGIN - self.MARGIN

    @property
    def xRange(self) -> float:
        return self.maxX - self.minX

    @property
    def yRange(self) -> float:
        return self.maxY - self.minY

    @property
    def _xToPixelScale(self) -> int:
        return int(self.xPixelSpan / self.xRange)

    @property
    def _yToPixelScale(self) -> int:
        return int(self.yPixelSpan / self.yRange)

    def xToPixel(self, x: float) -> int:
        return round((x - self.minX) * self._xToPixelScale) + self.lineLeft

    def yToPixel(self, y: float) -> int:
        return self.lineBottom - round((y - self.minY) * self._yToPixelScale)

    def pixelToX(self, x: int) -> float:
        return (x - self.lineLeft) / self._xToPixelScale + self.minX

    def pixelToY(self, y: int) -> float:
        return (self.lineBottom - y) / self._yToPixelScale + self.minY

    def initDisplay(self):
        self.createAxis()
        self.createLabels()

    def createAxis(self):

        color = self.LINE_COLOR
        width = self.LINE_THICKNESS

        self.canvas.create_line(self.lineLeft, self.lineBottom, self.lineRight, self.lineBottom,
                                tags="xAxis", width=width, fill=color)

        self.canvas.create_line(self.lineLeft, self.lineBottom, self.lineLeft, self.lineTop,
                                tags="yAxis", width=width, fill=color)

    def createLabels(self):

        x = self.minX
        while x <= self.maxX:
            xPixel = self.xToPixel(x)
            self.canvas.create_line(xPixel, self.lineBottom, xPixel, self.lineBottom + self.LABEL_LENGTH,
                                    tags="xAxis")

            self.canvas.create_text(xPixel, self.lineBottom + self.LABEL_LENGTH + self.FONT_SIZE,
                                    text=str(x), justify=tk.CENTER, font=(self.FONT, self.FONT_SIZE),
                                    tags="xLabel")

            x += self.X_INTERVALS

        y = self.minY
        while y <= self.maxY:
            yPixel = self.yToPixel(y)
            self.canvas.create_line(self.lineLeft, yPixel, self.lineLeft - self.LABEL_LENGTH, yPixel,
                                    tags="yAxis")

            self.canvas.create_text(self.lineLeft - self.LABEL_LENGTH - self.FONT_SIZE, yPixel,
                                    text=str(y), justify=tk.CENTER, font=(self.FONT, self.FONT_SIZE),
                                    tags="yLabel")

            y += self.Y_INTERVALS

    def plot(self, point: Point, linePoint=False, showResidual=True):
        fill = self.LINE_POINT_COLOR if linePoint else self.DOT_COLOR

        x, y = point.x, point.y
        xPixel, yPixel = self.xToPixel(x), self.yToPixel(y)
        radius = self.DOT_SIZE // 2

        self.canvas.create_oval(xPixel - radius, yPixel - radius, xPixel + radius, yPixel + radius,
                                fill=fill, tags=f"Point:{point.number}")
        Point.COUNTER += 1

        if linePoint:
            self.linePoints.append(point)
        else:
            self.points.append(point)

        if showResidual and self.line and point not in self.line:
            self.showResidual(point, self.line)

    def createLine(self, line: Line, showPoints=False, showResidual=True):

        interceptX, interceptY = self.lineLeft, self.yToPixel(line.intercept)
        endX, endY = self.lineRight, self.yToPixel(line(self.maxX))

        self.canvas.create_line(interceptX, interceptY, endX, endY,
                                tags=f"Line:{line.number}")
        Line.COUNTER += 1

        self.line = line

        self.canvas.delete("residual")
        if showPoints:
            self.plot(line.point1, linePoint=True, showResidual=showResidual)
            self.plot(line.point2, linePoint=True, showResidual=showResidual)

        if showResidual:
            for point in self.points:
                self.showResidual(point, line)

        # print(line.calculateRSquared(self.points))

    def showResidual(self, point: Point, line: Line) -> float:
        residual = line.residual(point)

        linePixelX, linePixelY = self.xToPixel(point.x), self.yToPixel(point.y)

        if line.slope < 0:
            cornerPixelX = linePixelX + self._xToPixelScale * residual
            cornerPixelY = linePixelY + self._yToPixelScale * residual
        else:
            cornerPixelX = linePixelX - self._xToPixelScale * residual
            cornerPixelY = linePixelY + self._yToPixelScale * residual

        self.canvas.create_rectangle(cornerPixelX, cornerPixelY, linePixelX, linePixelY,
                                     fill=self.RESIDUAL_COLOR, stipple="gray25",
                                     tags="residual")

        return residual

    def createBestFitLine(self, showResidual=False):
        if not self.points:
            return

        if self.line:
            self.canvas.delete(f"Line:{self.line.number}")

        middle = (self.minX + self.maxX) / 2
        intercept = Point(middle, self.minY)
        endPoint = Point(middle + self.xRange / 10, self.minY)

        line = Line(intercept, endPoint)
        bestLine = deepcopy(line)

        bestResidual = line.sumResidualSquared(self.points)

        while intercept.y < self.maxY:

            while endPoint.y < self.maxY:

                residual = line.sumResidualSquared(self.points)
                if residual < bestResidual:
                    bestResidual = residual
                    bestLine = deepcopy(line)

                    # print(residual, intercept, endPoint)

                endPoint.y += self.yRange // 35

            intercept.y += self.yRange // 35

            endPoint.y = self.minY

        self.createLine(bestLine, showResidual=showResidual)

    def display(self):
        try:
            while self.state():
                self.update()
                self.update_idletasks()
        except tk.TclError:
            # print("Exiting")
            pass

    def mouseClick(self, event):
        pixelX, pixelY = event.x, event.y
        x, y = self.pixelToX(pixelX), self.pixelToY(pixelY)
        point = Point(x, y)

        # if the mouse clicked on a point
        # alternatively can use canvas.find_closest

        for p in self.points + self.linePoints:
            if point.close(p, self.POINT_MAXIMUM_OFFSET):
                self.draggingPoint = p
                break
        else:
            return

    def mouseRelease(self):
        self.draggingPoint = None

    def motion(self, event):
        if self.draggingPoint is None:
            return

        changeLine = None

        if self.line and self.draggingPoint in self.line:
            changeLine = self.line

            self.linePoints.remove(self.draggingPoint)
            linePoint = True
        else:
            self.points.remove(self.draggingPoint)
            linePoint = False

        x = self.pixelToX(event.x)
        y = self.pixelToY(event.y)

        self.canvas.delete(f"Point:{self.draggingPoint.number}")

        self.draggingPoint.x = x
        self.draggingPoint.y = y

        self.plot(self.draggingPoint, linePoint=linePoint)

        if changeLine is not None:
            self.canvas.delete(f"Line:{changeLine.number}")
            for point in self.linePoints:
                self.canvas.delete(f"Point:{point.number}")
            self.linePoints = []

            self.createLine(changeLine)

        showResidual = False
        if not showResidual:
            return

        self.canvas.delete("residual")
        for point in self.points:

            if self.line and point not in self.line:
                self.showResidual(point, self.line)
