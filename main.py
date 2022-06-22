from Graph import Graph, Point, Line

from random import uniform


def main():
    graph = Graph()

    initPointNumber = 15

    for _ in range(initPointNumber):
        p = Point(uniform(graph.minX, graph.maxX), uniform(graph.minY, graph.maxY))
        graph.plot(p)

    graph.display()


if __name__ == "__main__":
    main()
