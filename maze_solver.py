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


def main():
    win = Window(800, 600)
    win.wait_for_close()


if __name__ == "__main__":
    main()
