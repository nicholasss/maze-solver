#!/usr/bin/python3

import unittest
from maze_solver import Maze, Window


class Tests(unittest.TestCase):
    def test_maze_create_calls(self):
        win1 = Window(800, 600)

        num_cols = 12
        num_rows = 10
        m1 = Maze(x1=0, y1=0,
                  num_rows=num_rows, num_columns=num_cols,
                  cell_width=10, cell_height=10, window=win1)

        self.assertEqual(
            len(m1._cells),
            num_cols
        )
        self.assertEqual(
            len(m1._cells[0]),
            num_rows
        )

        win1.close()

    def test_maze_cell_location(self):
        win2 = Window(800, 600)

        top_left_x = 20
        top_left_y = 20

        num_cols = 2
        num_rows = 5

        cell_height = 10
        cell_width = 40

        m2 = Maze(x1=top_left_x, y1=top_left_y,
                  num_rows=num_rows, num_columns=num_cols,
                  cell_width=cell_width, cell_height=cell_height,
                  window=win2)

        self.assertEqual(m2._cells[0][0]._x1,
                         top_left_x)
        self.assertEqual(m2._cells[0][0]._y1,
                         top_left_y)

        win2.close()

    def test_maze_break_entexit(self):
        win3 = Window(800, 600)

        m3 = Maze(0, 0, 10, 10, 5, 5, win3)
        m3._break_entrance_and_exit()

        self.assertEqual(False,
                         m3._cells[0][0].has_top_wall)
        self.assertEqual(False,
                         m3._cells[9][9].has_right_wall)

        win3.close()


if __name__ == "__main__":
    unittest.main()
