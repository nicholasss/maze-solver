#!/usr/bin/python3

from tkinter import Tk, BOTH, Canvas
from typing import Self
from enum import Enum
import time
import random


class Direction(Enum):
    Left = 1
    Right = 2
    Up = 3
    Down = 4


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
        self._window: Window = window
        self._fill_color: str = "black"
        self._bg_color: str = "#d9d9d9"
        self.visited: bool = False

    def draw(self, top_left_p: Point, bottom_right_p: Point):
        self._x1 = top_left_p.x
        self._y1 = top_left_p.y
        self._x2 = bottom_right_p.x
        self._y2 = bottom_right_p.y

        top_wall_color: str = self._bg_color
        if self.has_top_wall:
            top_wall_color = self._fill_color
        top_left_p: Point = Point(self._x1, self._y1)
        top_right_p: Point = Point(self._x2, self._y1)
        self._window.draw(
            Line(top_left_p, top_right_p), top_wall_color)

        left_wall_color: str = self._bg_color
        if self.has_left_wall:
            left_wall_color = self._fill_color
        top_left_p: Point = Point(self._x1, self._y1)
        bottom_left_p: Point = Point(self._x1, self._y2)
        self._window.draw(
            Line(top_left_p, bottom_left_p), left_wall_color)

        bottom_wall_color: str = self._bg_color
        if self.has_bottom_wall:
            bottom_wall_color = self._fill_color
        bottom_left_p: Point = Point(self._x1, self._y2)
        bottom_right_p: Point = Point(self._x2, self._y2)
        self._window.draw(
            Line(bottom_left_p, bottom_right_p), bottom_wall_color)

        right_wall_color: str = self._bg_color
        if self.has_right_wall:
            right_wall_color = self._fill_color
        bottom_right_p: Point = Point(self._x2, self._y2)
        top_right_p: Point = Point(self._x2, self._y1)
        self._window.draw(
            Line(bottom_right_p, top_right_p), right_wall_color)

    def draw_move(self, to_cell: Self, undo=False):
        path_fill_color: str = "green"
        if undo:
            path_fill_color = "grey"

        center_self: Point = Point(
            x=((self._x1 + self._x2) / 2),
            y=((self._y1 + self._y2) / 2))
        center_next: Point = Point(
            x=((to_cell._x1 + to_cell._x2) / 2),
            y=((to_cell._y1 + to_cell._y2) / 2))
        path: Line = Line(center_self, center_next)

        self._window.draw(path, path_fill_color, 5)


class Maze():
    def __init__(self, x1: int, y1: int, num_rows: int, num_columns: int,
                 cell_width: int, cell_height: int, window: Window,
                 seed: int = None):
        self._cells: list = []
        self._x1: int = x1
        self._y1: int = y1
        self._num_rows: int = num_rows
        self._num_columns: int = num_columns
        self._cell_width: int = cell_width
        self._cell_height: int = cell_height
        self._window: Window = window

        if seed is not None:
            self.seed = random.seed(seed)

        self._create_cells()

    def _create_cells(self):
        # filling cells into the matrix
        for i in range(self._num_columns):
            self._cells.append([])
            for j in range(self._num_rows):
                self._cells[i].append(Cell(self._window))

        # drawing each cell in the matrix
        for i in range(self._num_columns):
            for j in range(self._num_rows):
                self._draw_cell(i, j)

    def _draw_cell(self, i: int, j: int):
        # calculate x, y position of cells and draw cell, then call _animate
        top_left_p: Point = Point(x=self._x1 + (i * self._cell_width),
                                  y=self._y1 + (j * self._cell_height))
        bottom_right_p: Point = Point(x=top_left_p.x + self._cell_width,
                                      y=top_left_p.y + self._cell_height)

        cell: Cell = self._cells[i][j]
        cell.draw(top_left_p, bottom_right_p)

        self._animate()

    def _animate(self):
        self._window.redraw()
        time.sleep(0.05)

    def _break_cell_wall(self, i: int, j: int, side: str):
        current_cell: Cell = self._cells[i][j]
        if side == "top":
            current_cell.has_top_wall = False
        elif side == "left":
            current_cell.has_left_wall = False
        elif side == "right":
            current_cell.has_right_wall = False
        else:  # side == "bottom"
            current_cell.has_bottom_wall = False

    def _break_entrance_and_exit(self):
        if self._cells == []:
            # print("cells not created yet")
            return None

        first_cell: Cell = self._cells[0][0]
        i_index = self._num_columns - 1
        j_index = self._num_rows - 1
        last_cell: Cell = self._cells[i_index][j_index]

        first_cell.has_top_wall = False
        self._draw_cell(0, 0)
        last_cell.has_right_wall = False
        self._draw_cell(i_index, j_index)

    def _direction_from_cell(self, origin: list[int],
                             destination: list[int]) -> Direction:
        origin_i: int = origin[0]
        origin_j: int = origin[1]
        destination_i: int = destination[0]
        destination_j: int = destination[1]

        if destination_j == origin_j - 1 and destination_i == origin_i:
            return Direction.Up

        elif destination_j == origin_j + 1 and destination_i == origin_i:
            return Direction.Down

        elif destination_i == origin_i - 1 and destination_j == origin_j:
            return Direction.Left

        else:  # destination_i == origin_i + 1 and destination_j == origin_j:
            return Direction.Right

        # NOTE: no direction found past this point
        return None

    def _find_valid_neighbors(self, i: int, j: int) -> list:
        columns_max_index: int = self._num_columns - 1
        rows_max_index: int = self._num_rows - 1

        current_column: int = i
        current_row: int = j

        neighbors: list = []

        if current_row <= 0:
            # top-most row, no top neighbor
            top_neighbor = None
        else:
            top_neighbor = [i, j - 1]

        if current_column <= 0:
            # left-most column, no left neighbor
            left_neighbor = None
        else:
            left_neighbor = [i - 1, j]

        if current_row >= rows_max_index:
            # bottom-most row, no bottom neighbor
            bottom_neighbor = None
        else:
            bottom_neighbor = [i, j + 1]

        if current_column >= columns_max_index:
            # right-most column, no right neighbor
            right_neighbor = None
        else:
            right_neighbor = [i + 1, j]

        neighbors = [top_neighbor, left_neighbor,
                     bottom_neighbor, right_neighbor]

        neighbors = list(filter(lambda x: x is not None, neighbors))
        neighbors = list(filter(lambda x:
                                self._cells[x[0]][x[1]].visited is not True,
                                neighbors)
                         )
        return neighbors

    def _break_walls_r(self, i: int, j: int):
        self._cells[i][j].visited = True

        columns_max_index: int = self._num_columns - 1
        rows_max_index: int = self._num_rows - 1

        current_column: int = i
        current_row: int = j

        while True:
            # calculating neighbors
            neighbors: list = []
            if current_row <= 0:
                # top-most row, no top neighbor
                top_neighbor = None
            else:
                top_neighbor = [i, j - 1]

            if current_column <= 0:
                # left-most column, no left neighbor
                left_neighbor = None
            else:
                left_neighbor = [i - 1, j]

            if current_row >= rows_max_index:
                # bottom-most row, no bottom neighbor
                bottom_neighbor = None
            else:
                bottom_neighbor = [i, j + 1]

            if current_column >= columns_max_index:
                # right-most column, no right neighbor
                right_neighbor = None
            else:
                right_neighbor = [i + 1, j]

            neighbors = [top_neighbor, left_neighbor,
                         bottom_neighbor, right_neighbor]

            neighbors = list(filter(lambda x: x is not None, neighbors))
            neighbors = list(filter(lambda x:
                                    self._cells[x[0]][x[1]
                                                      ].visited is not True,
                                    neighbors)
                             )

            if neighbors == []:
                self._draw_cell(current_column, current_row)
                return

            # pickng a random direction
            random_neighbor = random.choice(neighbors)
            neighbors.remove(random_neighbor)

            if random_neighbor == top_neighbor:
                self._break_cell_wall(i, j, "top")
                self._break_cell_wall(
                    random_neighbor[0], random_neighbor[1], "bottom")
                self._break_walls_r(random_neighbor[0], random_neighbor[1])
            elif random_neighbor == left_neighbor:
                self._break_cell_wall(i, j, "left")
                self._break_cell_wall(
                    random_neighbor[0], random_neighbor[1], "right")
                self._break_walls_r(random_neighbor[0], random_neighbor[1])
            elif random_neighbor == bottom_neighbor:
                self._break_cell_wall(i, j, "bottom")
                self._break_cell_wall(
                    random_neighbor[0], random_neighbor[1], "top")
                self._break_walls_r(random_neighbor[0], random_neighbor[1])
            else:  # choice == right_neighbor
                self._break_cell_wall(i, j, "right")
                self._break_cell_wall(
                    random_neighbor[0], random_neighbor[1], "left")
                self._break_walls_r(random_neighbor[0], random_neighbor[1])

    def _reset_cells_visited(self):
        for i in range(self._num_columns):
            for j in range(self._num_rows):
                self._cells[i][j].visited = False

    def solve(self):
        print("solving maze")
        i: int = 0
        j: int = 0
        solved: bool = self._solve_r(i, j)
        if solved:
            return True
        else:
            return False

    def _solve_r(self, i: int, j: int):
        self._animate()
        current_cell: Cell = self._cells[i][j]
        current_cell_coord: list[int] = [i, j]
        current_cell.visited = True
        goal_i: int = self._num_columns - 1
        goal_j: int = self._num_rows - 1

        if i == goal_i and j == goal_j:
            return True

        valid_neighbors: list = self._find_valid_neighbors(i, j)

        for neighbor in valid_neighbors:

            neighbor_direction: Direction = self._direction_from_cell(
                origin=current_cell_coord, destination=neighbor)

            dir_blocked: bool = True
            if neighbor_direction is Direction.Up:
                dir_blocked = current_cell.has_top_wall
            elif neighbor_direction is Direction.Left:
                dir_blocked = current_cell.has_left_wall
            elif neighbor_direction is Direction.Down:
                dir_blocked = current_cell.has_bottom_wall
            else:  # right wall
                dir_blocked = current_cell.has_right_wall

            neighbor_cell = self._cells[neighbor[0]][neighbor[1]]
            if dir_blocked:
                continue

            current_cell.draw_move(neighbor_cell, undo=False)

            is_solved: bool = self._solve_r(neighbor[0], neighbor[1])
            if is_solved:
                return True
            else:
                current_cell.draw_move(neighbor_cell, undo=True)


def main():
    window = Window(800, 600)

    # TODO: After debugging, remove the seed argument to ensure randomness

    maze = Maze(50, 50, num_rows=10, num_columns=14,
                cell_width=50, cell_height=50, window=window)

    maze._break_entrance_and_exit()

    maze._break_walls_r(0, 0)
    maze._reset_cells_visited()

    is_solved: bool = maze.solve()
    if is_solved:
        print("maze was solved")

    window.wait_for_close()


if __name__ == "__main__":
    main()
