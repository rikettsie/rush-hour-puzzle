import io
import os
import unittest
from unittest.mock import patch

from components.game import Game

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
EXEMPLE_1 = os.path.join(DATA_DIR, "example_1.txt")
EXEMPLE_18 = os.path.join(DATA_DIR, "example_18.txt")

MOVE_PATTERN = r"^\w -> \(\d+, \d+\)$"
EXIT_MOVE = "X -> (2, 4)"


def solve_silently(filepath: str):
    """Run Game.solve() with stdout suppressed."""
    game = Game(filepath)
    with patch("sys.stdout", new_callable=io.StringIO):
        return game.solve()


class TestExemple1(unittest.TestCase):
    """Simple 4-car puzzle — expected optimal solution: 3 moves."""

    @classmethod
    def setUpClass(cls):
        cls.solution = solve_silently(EXEMPLE_1)

    def test_is_solvable(self):
        self.assertIsNotNone(self.solution)

    def test_solution_is_list(self):
        self.assertIsInstance(self.solution, list)

    def test_optimal_length(self):
        # Minimum solution: move C left, move B down, slide X to exit
        self.assertEqual(len(self.solution), 3)

    def test_move_format(self):
        for move in self.solution:
            self.assertRegex(move, MOVE_PATTERN)

    def test_last_move_places_red_car_at_exit(self):
        self.assertEqual(self.solution[-1], EXIT_MOVE)


class TestExemple18(unittest.TestCase):
    """Complex 12-car puzzle — verifies solver correctness."""

    @classmethod
    def setUpClass(cls):
        # This may take a few seconds for BFS to explore the state space.
        cls.solution = solve_silently(EXEMPLE_18)

    def test_is_solvable(self):
        self.assertIsNotNone(self.solution)

    def test_solution_is_list(self):
        self.assertIsInstance(self.solution, list)

    def test_move_format(self):
        for move in self.solution:
            self.assertRegex(move, MOVE_PATTERN)

    def test_last_move_places_red_car_at_exit(self):
        self.assertEqual(self.solution[-1], EXIT_MOVE)


if __name__ == "__main__":
    unittest.main()
