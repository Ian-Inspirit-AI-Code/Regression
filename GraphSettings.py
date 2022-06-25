class GraphSettings:

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
    DEFAULT_DRAG_LINE = True
    DEFAULT_SHOW_RESIDUAL = False

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
                 dragLine=DEFAULT_DRAG_LINE, showResidual=DEFAULT_SHOW_RESIDUAL,
                 ):

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
