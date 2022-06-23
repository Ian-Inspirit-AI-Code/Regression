from Graph import Graph, Point, Line

from random import uniform


def main():
    graph = Graph()

    initPointNumber = 15

    # for _ in range(initPointNumber):
    #     p = Point(uniform(graph.minX, graph.maxX), uniform(graph.minY, graph.maxY))
    #     graph.plot(p)

    points = [(6.9, 1.4), (9.1, 55.88), (8.3, 4.4), (7.7, 32.0), (7.8, 14.93), (8.2, 6.0), (7.5, 3.1), (7.5, 5.8),
              (9.5, 8.1), (8.1, 6.5), (8.1, 6.6), (8.1, 10.0), (7.5, 3.0), (6.1, 0.9), (8.4, 29.0), (7.9, 13.0),
              (8.3, 38.2), (8.4, 28.0), (8.3, 21.0), (7.6, 5.0), (7.4, 85.4), (6.6, 2.0), (8.4, 25.7), (8.4, 11.0),
              (8.2, 11.7), (8.3, 10.0)]
    points = [Point(*point) for point in points]
    
    for point in points:
        graph.plot(point)

    graph.display()


if __name__ == "__main__":
    main()
