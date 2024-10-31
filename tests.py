#!/usr/bin/python3

import unittest
from maze_solver import Maze, Window, Direction


class Tests(unittest.TestCase):
    def test_direction_from_cell(self):
        origin_1 = [1, 1]
        dest_1 = [1, 0]
        self.assertEqual(Maze._direction_from_cell(
            origin_1, dest_1), Direction.Up)

        origin_2 = [1, 1]
        dest_2 = [1, 2]
        self.assertEqual(Maze._direction_from_cell(
            origin_2, dest_2), Direction.Down)

        origin_3 = [1, 1]
        dest_3 = [0, 1]
        self.assertEqual(Maze._direction_from_cell(
            origin_3, dest_3), Direction.Left)

        origin_4 = [1, 1]
        dest_4 = [2, 1]
        self.assertEqual(Maze._direction_from_cell(
            origin_4, dest_4), Direction.Right)

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

    def test_reset_visited(self):
        win4 = Window(800, 600)

        m4 = Maze(0, 0, 10, 10, 5, 5, win4)
        m4._break_entrance_and_exit()
        m4._break_walls_r(0, 0)
        m4._reset_cells_visited()

        self.assertEqual(m4._cells[0][0].visited, False)

        win4.close()


if __name__ == "__main__":
    unittest.main()
