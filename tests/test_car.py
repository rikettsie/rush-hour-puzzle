import unittest

from components.car import Car, CarError


class TestCarConstruction(unittest.TestCase):
    def test_horizontal_car(self):
        car = Car("A", (0, 0), 2, Car.DIR_HORIZ)
        self.assertEqual(car.label, "A")
        self.assertEqual(car.top_left, (0, 0))
        self.assertEqual(car.size, 2)
        self.assertTrue(car.is_horizontal_direction())

    def test_vertical_car(self):
        car = Car("B", (1, 2), 3, Car.DIR_VERT)
        self.assertFalse(car.is_horizontal_direction())
        self.assertEqual(car.size, 3)

    def test_size_3_allowed(self):
        car = Car("C", (0, 0), 3, Car.DIR_HORIZ)
        self.assertEqual(car.size, 3)

    def test_red_car_label(self):
        car = Car(Car.RED_CAR, (2, 1), 2, Car.DIR_HORIZ)
        self.assertEqual(car.label, "X")

    def test_top_left_setter(self):
        car = Car("A", (0, 0), 2, Car.DIR_HORIZ)
        car.top_left = (3, 3)
        self.assertEqual(car.top_left, (3, 3))


class TestCarValidation(unittest.TestCase):
    def test_invalid_direction_raises(self):
        with self.assertRaises(CarError):
            Car("A", (0, 0), 2, 5)

    def test_invalid_direction_negative_raises(self):
        with self.assertRaises(CarError):
            Car("A", (0, 0), 2, -1)

    def test_invalid_size_1_raises(self):
        with self.assertRaises(CarError):
            Car("A", (0, 0), 1, Car.DIR_HORIZ)

    def test_invalid_size_4_raises(self):
        with self.assertRaises(CarError):
            Car("A", (0, 0), 4, Car.DIR_HORIZ)

    def test_negative_row_raises(self):
        with self.assertRaises(CarError):
            Car("A", (-1, 0), 2, Car.DIR_HORIZ)

    def test_negative_col_raises(self):
        with self.assertRaises(CarError):
            Car("A", (0, -1), 2, Car.DIR_HORIZ)


class TestCarStr(unittest.TestCase):
    def test_str_contains_label(self):
        car = Car("X", (2, 1), 2, Car.DIR_HORIZ)
        self.assertIn("X", str(car))

    def test_str_shows_H_for_horizontal(self):
        car = Car("A", (0, 0), 2, Car.DIR_HORIZ)
        self.assertIn("H", str(car))

    def test_str_shows_V_for_vertical(self):
        car = Car("B", (0, 0), 2, Car.DIR_VERT)
        self.assertIn("V", str(car))


if __name__ == "__main__":
    unittest.main()
