import tkinter as tk

from Line import Line, SlopeIntercept
from Point import Point

from functools import cached_property
from itertools import takewhile, count, product

from numpy import arange, polyfit


class Graph(tk.Tk):
    DEFAULT_BACKGROUND_COLOR = "#F8DAD4"

    DEFAULT_HEIGHT_PIXEL = 450
    DEFAULT_WIDTH_PIXEL = 800
    DEFAULT_MARGIN = 75

    DEFAULT_X_LABEL_INTERVAL = 1
    DEFAULT_Y_LABEL_INTERVAL = 1
    DEFAULT_LABEL_LENGTH = 5

    DEFAULT_FONT_SIZE = 10
    DEFAULT_FONT = "Arial"

    DEFAULT_POINT_RADIUS = 6
    DEFAULT_POINT_COLOR = "#FD0B0B"

    DEFAULT_LINE_THICKNESS = 3
    DEFAULT_LINE_COLOR = "#0C51FA"

    DEFAULT_RESIDUAL_COLOR = "#DD5FF8"
    DEFAULT_RESIDUAL_STIPPLE = "gray25"

    DEFAULT_X_MIN = 0
    DEFAULT_Y_MIN = 0
    DEFAULT_X_MAX = 20
    DEFAULT_Y_MAX = 10

    DEFAULT_DRAG_POINT_VARIABILITY_PIXEL = 25

    def __init__(self, *,
                 backgroundColor=DEFAULT_BACKGROUND_COLOR,
                 height=DEFAULT_HEIGHT_PIXEL, width=DEFAULT_WIDTH_PIXEL, margin=DEFAULT_MARGIN,
                 xLabelInterval=DEFAULT_X_LABEL_INTERVAL, yLabelInterval=DEFAULT_Y_LABEL_INTERVAL,
                 labelLength=DEFAULT_LABEL_LENGTH,
                 fontSize=DEFAULT_FONT_SIZE, font=DEFAULT_FONT,
                 pointRadius=DEFAULT_POINT_RADIUS, pointColor=DEFAULT_POINT_COLOR,
                 lineThickness=DEFAULT_LINE_THICKNESS, lineColor=DEFAULT_LINE_COLOR,
                 residualColor=DEFAULT_RESIDUAL_COLOR, residualStipple=DEFAULT_RESIDUAL_STIPPLE,
                 xMin=DEFAULT_X_MIN, xMax=DEFAULT_X_MAX, yMin=DEFAULT_Y_MIN, yMax=DEFAULT_Y_MAX,
                 dragVariability=DEFAULT_DRAG_POINT_VARIABILITY_PIXEL,
                 dragLine=True, showResidual=False):

        super().__init__()

        self.bg = backgroundColor
        self.height = height
        self.width = width
        self.margin = margin
        self.xLabelInterval = xLabelInterval
        self.yLabelInterval = yLabelInterval
        self.labelLength = labelLength
        self.fontSize = fontSize
        self.font = font
        self.pointRadius = pointRadius
        self.pointColor = pointColor
        self.lineThickness = lineThickness
        self.lineColor = lineColor
        self.residualColor = residualColor
        self.residualStipple = residualStipple
        self.xMin = xMin
        self.yMin = yMin
        self.xMax = xMax
        self.yMax = yMax
        self.dragVariability = dragVariability

        self.dragLine = dragLine
        self.showResidual = showResidual
        
        self.canvas = tk.Canvas(self, bg=self.bg, height=self.height, width=self.width)
        self.canvas.pack()
        
        w = 20
        h = 2
        tk.Button(self, text="Show line of best fit", width=w, height=h, command=self.createBestFitLine).pack()
        tk.Button(self, text="Hide line of best fit", width=w, height=h, command=self.removeBestFitLine).pack()
        tk.Button(self, text="Toggle residual", width=w, height=h, command=self.toggleResidual).pack()
        tk.Button(self, text="DeleteLine", width=w, height=h, command=self.deleteLine).pack()

        self.bind('<Button-1>', self.mouseClick)  # left click
        self.bind('<ButtonRelease-1>', lambda _: self.mouseRelease())  # left click release
        self.bind('<Motion>', self.motion)  # mouse moving

        self.points = []
        self.lines = []

        self.draggingPoint = None

        self.initDisplay()

    @cached_property
    def _lineBottom(self) -> int:
        return self.height - self.margin

    @cached_property
    def _lineTop(self) -> int:
        return self.margin

    @cached_property
    def _lineLeft(self) -> int:
        return self.margin

    @cached_property
    def _lineRight(self) -> int:
        return self.width - self.margin

    @cached_property
    def _xPixelSpan(self) -> float:
        return self.width - 2 * self.margin

    @cached_property
    def _yPixelSpan(self) -> float:
        return self.height - 2 * self.margin

    @cached_property
    def _xRange(self) -> float:
        return self.xMax - self.xMin

    @cached_property
    def _yRange(self) -> float:
        return self.yMax - self.yMin

    @cached_property
    def _xToPixelScale(self) -> int:
        return int(self._xPixelSpan / self._xRange)

    @cached_property
    def _yToPixelScale(self) -> int:
        return int(self._yPixelSpan / self._yRange)
    
    def _xToPixel(self, x: float) -> int:
        return round((x - self.xMin) * self._xToPixelScale) + self._lineLeft

    def _yToPixel(self, y: float) -> int:
        return self._lineBottom - round((y - self.yMin) * self._yToPixelScale)

    def _pixelToX(self, x: int) -> float:
        return (x - self._lineLeft) / self._xToPixelScale + self.xMin

    def _pixelToY(self, y: int) -> float:
        return (self._lineBottom - y) / self._yToPixelScale + self.yMin

    def initDisplay(self):
        self.createAxis()
        self.createLabels()

    def display(self):
        try:
            while self.state():
                self.update()
                self.update_idletasks()
        except tk.TclError:
            # print("Exiting")
            pass

    def createAxis(self):
        color = self.lineColor
        width = self.lineThickness

        self.canvas.create_line(self._lineLeft, self._lineBottom, self._lineRight, self._lineBottom,
                                tags="xAxis", width=width, fill=color)

        self.canvas.create_line(self._lineLeft, self._lineBottom, self._lineLeft, self._lineTop,
                                tags="yAxis", width=width, fill=color)

    def createLabels(self):

        for x in takewhile(lambda xValue: xValue <= self._lineRight,
                           count(self._lineLeft, self.xLabelInterval * self._xToPixelScale)):
            self.canvas.create_line(x, self._lineBottom, x, self._lineBottom + self.labelLength, tags="xAxis")
            self.canvas.create_text(x, self._lineBottom + self.labelLength + self.fontSize,
                                    text=str(self._pixelToX(x)), justify=tk.CENTER, font=(self.font, self.fontSize),
                                    tags="xLabel")

        for y in takewhile(lambda yValue: yValue >= self._lineTop,
                           count(self._lineBottom, - self.yLabelInterval * self._yToPixelScale)):
            self.canvas.create_line(self._lineLeft, y, self._lineLeft - self.labelLength, y, tags="yAxis")
            self.canvas.create_text(self._lineLeft - self.labelLength - self.fontSize, y,
                                    text=str(self._pixelToY(y)), justify=tk.CENTER, font=(self.font, self.fontSize),
                                    tags="yLabel")

    def plot(self, point: Point, partOfLine=False):
        x, y = self._xToPixel(point.x), self._yToPixel(point.y)
        r = self.pointRadius

        fill = self.lineColor if partOfLine else self.pointColor
        self.canvas.create_oval(x - r, y - r, x + r, y + r,
                                fill=fill, tags=point.toTag())

        self.points.append(point)

        # TODO: residuals

    def removePoint(self, point: Point):
        self.canvas.delete(point.toTag())

        try:
            self.points.remove(point)
        except ValueError:
            pass

    def updatePoint(self, p: Point, newPixelX: int, newPixelY: int):
        x, y = p.x, p.y
        newX, newY = self._pixelToX(newPixelX), self._pixelToY(newPixelY)

        pixelX, pixelY = self._xToPixel(x), self._yToPixel(y)

        dx, dy = newPixelX - pixelX, newPixelY - pixelY

        p.x, p.y = newX, newY

        self.canvas.move(p.toTag(), dx, dy)

    def leftRightOfLine(self, line: Line):
        valueAtMin = line(self.xMin)

        if self.yMin <= valueAtMin <= self.yMax:
            pLeft = Point(self.xMin, valueAtMin)
        elif valueAtMin < self.yMin and line.slope > 0:
            pLeft = line.pointAtY(self.xMin)
        elif valueAtMin > self.yMax and line.slope < 0:
            pLeft = line.pointAtY(self.yMax)
        else:
            return

        valueAtMax = line(self.xMax)
        if self.yMin <= valueAtMax <= self.yMax:
            pRight = Point(self.xMax, valueAtMax)
        elif valueAtMax < self.yMin and line.slope < 0:
            pRight = line.pointAtY(self.xMin)
        elif valueAtMax > self.yMax and line.slope > 0:
            pRight = line.pointAtY(self.yMax)
        else:
            return

        return pLeft, pRight

    def createLine(self, line: Line, plotPoints=True, updateLine=False, addToLines=True, tag=None):
        try:
            pLeft, pRight = self.leftRightOfLine(line)
        except ValueError:
            return

        if plotPoints:
            self.plot(pLeft, partOfLine=True)
            self.plot(pRight, partOfLine=True)

        if not updateLine:
            line.point1, line.point2 = pLeft, pRight

        if addToLines:
            self.lines.append(line)

        tag = line.toTag() if tag is None else tag

        self.canvas.create_line(self._xToPixel(pLeft.x), self._yToPixel(pLeft.y),
                                self._xToPixel(pRight.x), self._yToPixel(pRight.y),
                                tags=tag, fill=self.lineColor)

        self.updateResiduals()

    def deleteLine(self, line: Line = None):
        try:
            line = self.lines[0] if line is None else line
        except IndexError:
            print("Cannot delete a line without lines of screen. If you are trying to delete a best fit line, use the",
                  '"removeBestFitLine button"')

        self.canvas.delete(line.toTag())
        self.lines.remove(line)

        list(map(lambda p: self.removePoint(p), line.displayedPoints))

        self.updateResiduals()

    def updateLine(self, line):
        self.canvas.delete(line.toTag())
        self.createLine(line, False, True)

    def createBestFitLine(self):
        self.removeBestFitLine()

        pointListX, pointListY = [point.x for point in self.points], [point.y for point in self.points]
        polyCoefficients = polyfit(pointListX, pointListY, 1)

        slope, intercept = polyCoefficients[0], polyCoefficients[1]

        line = SlopeIntercept(slope, intercept)
        self.createLine(line, plotPoints=False, updateLine=False, addToLines=True, tag="bestFit")

        self.updateResiduals()

    def removeBestFitLine(self):
        self.canvas.delete("bestFit")
        self.lines = [line for line in self.lines if not isinstance(line, SlopeIntercept)]

        self.updateResiduals()

    def toggleResidual(self):
        if len(self.lines) != 1 and not self.showResidual:
            print("Cannot show residuals when there is not exactly 1 line on screen")
            return

        self.showResidual = not self.showResidual
        self.updateResiduals()

    def updateResiduals(self):
        self.showResidual = self.showResidual and len(self.lines) == 1

        if self.showResidual:
            list(map(lambda point: self.showResidualPoint(point, self.lines[0]), self.points))
        else:
            self.canvas.delete("residual")

    def showResidualPoint(self, point: Point, line: Line):
        residual = line.residual(point)

        linePixelX, linePixelY = self._xToPixel(point.x), self._yToPixel(point.y)

        if line.slope < 0:
            cornerPixelX = linePixelX + self._xToPixelScale * residual
            cornerPixelY = linePixelY + self._yToPixelScale * residual
        else:
            cornerPixelX = linePixelX - self._xToPixelScale * residual
            cornerPixelY = linePixelY + self._yToPixelScale * residual

        self.canvas.create_rectangle(cornerPixelX, cornerPixelY, linePixelX, linePixelY,
                                     fill=self.residualColor, stipple=self.residualStipple,
                                     tags="residual")

        return residual

    def mouseClick(self, event):
        point = Point(self._pixelToX(event.x), self._pixelToY(event.y))

        for p in self.points:
            if point.close(p, self.dragVariability / self._xToPixelScale, self.dragVariability / self._yToPixelScale):
                self.draggingPoint = p
                break
        else:
            return

    def mouseRelease(self):
        self.draggingPoint = None
    
    def motion(self, event):
        p = self.draggingPoint

        if p is None:
            return

        if not (self._lineRight >= event.x >= self._lineLeft and self._lineTop <= event.y <= self._lineBottom):
            return

        self.updatePoint(p, event.x, event.y)

        if self.dragLine and self.lines:
            try:
                line = next(line for line in self.lines if p in line)
                self.updateLine(line)
            except StopIteration:
                pass
