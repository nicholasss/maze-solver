#!/usr/bin/python3

from tkinter import Tk, BOTH, Canvas


class Point():
    def __init__(self, x: int, y: int):
        self.x: int = x  # horizontal, 0 is left side
        self.y: int = y  # vertical, 0 is the top side


class Line():
    def __init__(self, point_a: Point, point_b: Point):
        self._p_a: Point = point_a
        self._p_b: Point = point_b

    def draw(self, canvas: Canvas, fill_color: str):
        x1 = self._p_a.x
        y1 = self._p_a.y
        x2 = self._p_b.x
        y2 = self._p_b.y

        canvas.create_line(x1, y1, x2, y2, fill=fill_color, width=2)


class Window():
    def __init__(self, width: int, height: int):
        self._width: int = width
        self._height: int = height
        self._root: Tk = Tk()
        self._canvas: Canvas = Canvas(height=self._height, width=self._width)
        self._window_running: bool = False

        self._root.protocol("WM_DELETE_WINDOW", self.close)
        self._root.title("Maze Solver")
        self._canvas.pack()

    def redraw(self):
        self._root.update_idletasks()
        self._root.update()

    def wait_for_close(self):
        self._window_running = True
        while self._window_running:
            self.redraw()

    def close(self):
        self._window_running = False
        print("Window was closed.")

    def draw(self, line: Line, fill_color: str):
        line.draw(canvas=self._canvas, fill_color=fill_color)


class Cell():
    def __init__(self):
        self.has_left_wall: bool
        self.has_right_wall: bool
        self.has_top_wall: bool
        self.has_bottom_wall: bool
        self._x1: int
        self._y1: int
        self._x2: int
        self._y2: int
        self._win: Window

    def draw(self):
        pass


def main():
    win = Window(800, 600)

    # line1 = Line(Point(100, 100), Point(300, 300))
    # win.draw(line=line1, fill_color="black")

    # line2 = Line(Point(100, 300), Point(300, 100))
    # win.draw(line=line2, fill_color="red")

    win.wait_for_close()


if __name__ == "__main__":
    main()
