import unittest

from components.board import Board, BoardError

# Matches the layout of data/exemple_1.txt
EXEMPLE_1_DESCR = "A,1,1,2,0\nX,2,1,2,0\nB,0,4,3,1\nC,5,4,2,0"


class TestBoardParsing(unittest.TestCase):
    def test_cars_are_loaded(self):
        board = Board(EXEMPLE_1_DESCR)
        self.assertEqual(set(board.cars.keys()), {"A", "X", "B", "C"})

    def test_car_positions(self):
        board = Board(EXEMPLE_1_DESCR)
        self.assertEqual(board.cars["X"].top_left, (2, 1))
        self.assertEqual(board.cars["A"].top_left, (1, 1))
        self.assertEqual(board.cars["B"].top_left, (0, 4))
        self.assertEqual(board.cars["C"].top_left, (5, 4))

    def test_car_directions(self):
        board = Board(EXEMPLE_1_DESCR)
        self.assertTrue(board.cars["X"].is_horizontal_direction())
        self.assertFalse(board.cars["B"].is_horizontal_direction())  # vertical

    def test_missing_red_car_raises(self):
        with self.assertRaises(BoardError):
            Board("A,0,0,2,0")

    def test_overlapping_cars_raises(self):
        # A at (2,2) would overlap X which occupies (2,1) and (2,2)
        with self.assertRaises(BoardError):
            Board("X,2,1,2,0\nA,2,2,2,0")

    def test_none_descr_gives_empty_board(self):
        board = Board(None)
        self.assertEqual(board.cars, {})


class TestBoardHashing(unittest.TestCase):
    def test_sha256_is_64_char_hex(self):
        board = Board(EXEMPLE_1_DESCR)
        h = board.to_sha256()
        self.assertRegex(h, r"^[0-9a-f]{64}$")

    def test_identical_boards_same_hash(self):
        self.assertEqual(
            Board(EXEMPLE_1_DESCR).to_sha256(),
            Board(EXEMPLE_1_DESCR).to_sha256(),
        )

    def test_different_boards_different_hash(self):
        board1 = Board(EXEMPLE_1_DESCR)
        board2 = Board("X,2,0,2,0\nB,0,4,3,1")
        self.assertNotEqual(board1.to_sha256(), board2.to_sha256())

    def test_eq_operator(self):
        self.assertEqual(Board(EXEMPLE_1_DESCR), Board(EXEMPLE_1_DESCR))


class TestBoardVariants(unittest.TestCase):
    def test_variants_nonempty(self):
        board = Board(EXEMPLE_1_DESCR)
        self.assertGreater(len(board.available_variants()), 0)

    def test_variant_has_board_and_move_keys(self):
        variant = Board(EXEMPLE_1_DESCR).available_variants()[0]
        self.assertIn("board", variant)
        self.assertIn("move", variant)

    def test_variant_board_is_board_instance(self):
        variant = Board(EXEMPLE_1_DESCR).available_variants()[0]
        self.assertIsInstance(variant["board"], Board)

    def test_variant_move_format(self):
        for variant in Board(EXEMPLE_1_DESCR).available_variants():
            self.assertRegex(variant["move"], r"^\w -> \(\d+, \d+\)$")

    def test_empty_board_has_no_variants(self):
        self.assertEqual(Board(None).available_variants(), [])

    def test_variant_boards_differ_from_original(self):
        board = Board(EXEMPLE_1_DESCR)
        for variant in board.available_variants():
            self.assertNotEqual(variant["board"], board)


if __name__ == "__main__":
    unittest.main()
