from Graph import Graph
from Point import Point, randomPoint
from Line import Line, randomLine


def main():
    graph = Graph()

    for _ in range(15):
        graph.plot(randomPoint(graph.xMin, graph.xMax, graph.yMin, graph.yMax))

    # line = randomLine(graph.xMin, graph.xMax, graph.yMin, graph.yMax)
    # graph.createLine(line)

    graph.display()


if __name__ == "__main__":
    main()
