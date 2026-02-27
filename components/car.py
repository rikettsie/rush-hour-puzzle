class CarError(Exception):
    pass


class Car:
    RED_CAR: str = "X"
    DIR_HORIZ: int = 0
    DIR_VERT: int = 1

    SIZE_LONG: int = 2
    SIZE_SHORT: int = 1

    def __init__(
        self, label: str, top_left: tuple[int, int], size: int, direction: int
    ) -> None:
        self.__label = label
        if self.__validate_coordinate(top_left):
            self.__top_left = top_left
        else:
            raise CarError(f"Coordinate {top_left} is out of bound.")

        if self.__validate_direction(direction):
            self.__direction = direction
        else:
            raise CarError(
                f'Direction {direction} is not permitted. Pass 0 (for "horizontal") or 1 (for "vertical").'
            )

        if self.__validate_size(size):
            self.__size = size
        else:
            raise CarError(f"Size {size} is not permitted. Pass 2 or 3.")

    @property
    def label(self) -> str:
        return self.__label

    @property
    def top_left(self) -> tuple[int, int]:
        return self.__top_left

    @top_left.setter
    def top_left(self, value: tuple[int, int]) -> None:
        self.__top_left = value

    @property
    def direction(self) -> int:
        return self.__direction

    @property
    def size(self) -> int:
        return self.__size

    def is_horizontal_direction(self) -> bool:
        return self.__direction == self.DIR_HORIZ

    # Validators
    def __validate_coordinate(self, coord: tuple[int, int]) -> bool:
        return coord[0] >= 0 and coord[1] >= 0

    def __validate_direction(self, direction: int) -> bool:
        return direction in [0, 1]

    def __validate_size(self, size: int) -> bool:
        return size in [2, 3]

    def __str__(self) -> str:
        return f"{self.__label}: [top-left {self.__top_left}], [size: {self.__size}], [direction: {'H' if self.is_horizontal_direction() else 'V'}]"
