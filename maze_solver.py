#!/usr/bin/python3

from tkinter import Tk, BOTH, Canvas


class Window():
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.root = Tk()
        self.canvas = Canvas(height=self.height, width=self.width)

        self.root.protocol("WM_DELETE_WINDOW", self.close)
        self.root.title("Maze Solver")
        self.canvas.pack()

        self.window_running = False

    def redraw(self):
        self.root.update_idletasks()
        self.root.update()

    def wait_for_close(self):
        self.window_running = True
        while self.window_running:
            self.redraw()

    def close(self):
        self.window_running = False
        print("DEBUG: closing program")


class Point():
    def __init__(self, x, y):
        self.x = x  # horizontal, 0 is left side
        self.y = y  # vertical, 0 is the top side


class Line():
    def __init__(self, point_a, point_b):
        self.p_a = point_a
        self.p_b = point_b

    def draw(self, canvas: Canvas, fill_color: str):
        x1 = self.p_a.x
        y1 = self.p_a.y
        x2 = self.p_b.x
        y2 = self.p_b.y

        canvas.create_line(x1, y1, x2, y2, fill=fill_color, width=2)


def main():
    win = Window(800, 600)
    win.wait_for_close()


if __name__ == "__main__":
    main()
