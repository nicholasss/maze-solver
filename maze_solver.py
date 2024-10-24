#!/usr/bin/python3

from tkinter import Tk, BOTH, Canvas
from typing import Self


class Point():
    def __init__(self, x: int, y: int):
        self.x: int = x  # horizontal, 0 is left side
        self.y: int = y  # vertical, 0 is the top side

    def __str__(self):
        return f"x {self.x}, y {self.y}"


class Line():
    def __init__(self, point_a: Point, point_b: Point):
        self._p_a: Point = point_a
        self._p_b: Point = point_b

    def __str__(self):
        return f"Start: {self._p_a}, End: {self._p_b}"

    def draw(self, canvas: Canvas, fill_color: str, width: int = 2):
        x1 = self._p_a.x
        y1 = self._p_a.y
        x2 = self._p_b.x
        y2 = self._p_b.y

        canvas.create_line(x1, y1, x2, y2, fill=fill_color, width=width)


class Window():
    def __init__(self, width: int, height: int):
        self._width: int = width
        self._height: int = height
        self._root: Tk = Tk()
        self._canvas: Canvas = Canvas(height=self._height, width=self._width)
        self._window_running: bool = False

        self._root.protocol("WM_DELETE_WINDOW", self.close)
        self._root.title("Maze Solver")
        self._canvas.pack(fill=BOTH, expand=True)

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

    def draw(self, line: Line, fill_color: str, width: int = 2):
        line.draw(canvas=self._canvas, fill_color=fill_color, width=width)


class Cell():
    def __init__(self, window: Window):
        self.has_left_wall: bool = True
        self.has_right_wall: bool = True
        self.has_top_wall: bool = True
        self.has_bottom_wall: bool = True
        self._x1: int  # x1, y1 is the top left corner
        self._y1: int
        self._x2: int  # x2, y2 is the bottom right corner
        self._y2: int
        self._win: Window = window
        self._fill_color: str = "black"

    def draw(self, top_left_p: Point, bottom_right_p: Point):
        self._x1 = top_left_p.x
        self._y1 = top_left_p.y
        self._x2 = bottom_right_p.x
        self._y2 = bottom_right_p.y

        if self.has_top_wall:
            top_left_p: Point = Point(self._x1, self._y1)
            top_right_p: Point = Point(self._x2, self._y1)
            self._win.draw(Line(top_left_p, top_right_p),
                           self._fill_color)

        if self.has_left_wall:
            top_left_p: Point = Point(self._x1, self._y1)
            bottom_left_p: Point = Point(self._x1, self._y2)
            self._win.draw(Line(top_left_p, bottom_left_p),
                           self._fill_color)

        if self.has_bottom_wall:
            bottom_left_p: Point = Point(self._x1, self._y2)
            bottom_right_p: Point = Point(self._x2, self._y2)
            self._win.draw(Line(bottom_left_p, bottom_right_p),
                           self._fill_color)

        if self.has_right_wall:
            bottom_right_p: Point = Point(self._x2, self._y2)
            top_right_p: Point = Point(self._x2, self._y1)
            self._win.draw(Line(bottom_right_p, top_right_p),
                           self._fill_color)

    def draw_move(self, to_cell: Self, undo=False):
        path_fill_color: str = "gray"
        if undo:
            path_fill_color = "red"

        center_self: Point = Point(
            x=((self._x1 + self._x2) / 2),
            y=((self._y1 + self._y2) / 2))
        center_next: Point = Point(
            x=((to_cell._x1 + to_cell._x2) / 2),
            y=((to_cell._y1 + to_cell._y2) / 2))
        path: Line = Line(center_self, center_next)

        print("drawing path")
        self._win.draw(path, path_fill_color, 5)


def main():
    win = Window(800, 600)

    p1_1 = Point(x=50, y=50)
    p1_2 = Point(x=100, y=100)
    cell1 = Cell(win)
    cell1.has_right_wall = False
    cell1.draw(p1_1, p1_2)

    p2_1 = Point(x=100, y=50)
    p2_2 = Point(x=150, y=100)
    cell2 = Cell(win)
    cell2.has_left_wall = False
    cell2.draw(p2_1, p2_2)

    cell1.draw_move(to_cell=cell2)

    win.wait_for_close()


if __name__ == "__main__":
    main()
