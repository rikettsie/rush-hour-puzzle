import hashlib
from copy import deepcopy
from typing import Any, Optional

from .car import Car


class BoardError(Exception):
    pass


class Board:
    EMPTY_POS: str = " "
    MAX_WIDTH: int = 6
    MAX_HEIGTH: int = 6

    def __init__(self, state_descr: Optional[str]) -> None:
        self.__init_empty_state()
        if state_descr:
            self.__parse_state(state_descr)

    @property
    def cars(self) -> dict[str, Car]:
        return self.__cars

    def describe(self) -> None:
        print(self)

    def to_sha256(self) -> str:
        sha256_hash = hashlib.sha256()
        sha256_hash.update(f"{self}".encode("utf-8"))
        return sha256_hash.hexdigest()

    def available_variants(self) -> list[dict[str, Any]]:
        variants: list[dict[str, Any]] = []
        for car_label, tl_positions in self.__available_moves().items():
            for tl_pos in tl_positions:
                variant: dict[str, Any] = {}
                variant_board = deepcopy(self)
                car = variant_board.cars[car_label]
                variant_board._Board__move_car_to(car, tl_pos)

                variant["board"] = variant_board
                variant["move"] = f"{car.label} -> {tl_pos}"
                variants.append(variant)
        return variants

    def __move_car_to(self, car: Car, new_top_left: tuple[int, int]) -> None:
        if car.label not in self.__cars:
            raise BoardError(f"The car labeled {car.label} is not in the board.")

        self.__clear_from_board(car)
        self.__cars[car.label].top_left = new_top_left
        self.__mark_board_with(car)

    def __available_moves(self) -> dict[str, list[tuple[int, int]]]:
        return {
            car.label: self.__available_moves_of(car) for car in self.__cars.values()
        }

    def __init_empty_state(self) -> None:
        self.__state: list[list[str]] = [
            [self.EMPTY_POS for _ in range(self.MAX_WIDTH)]
            for _ in range(self.MAX_HEIGTH)
        ]
        self.__cars: dict[str, Car] = {}

    def __available_moves_of(self, car: Car) -> list[tuple[int, int]]:
        if car.label not in self.__cars:
            raise BoardError("The car labeled {car.label} is not in the board.")
        (r, c) = car.top_left
        avails: list[tuple[int, int]] = []
        if car.is_horizontal_direction():
            cl: int = c - 1
            while self.__is_in_bounds_position((r, cl)) and self.__is_empty_position(
                (r, cl)
            ):
                avails.append((r, cl))
                cl -= 1
            cr: int = c + 1
            while self.__is_in_bounds_position(
                (r, cr + car.size - 1)
            ) and self.__is_empty_position((r, cr + car.size - 1)):
                avails.append((r, cr))
                cr += 1
        else:
            ru: int = r - 1
            while self.__is_in_bounds_position((ru, c)) and self.__is_empty_position(
                (ru, c)
            ):
                avails.append((ru, c))
                ru -= 1
            rd: int = r + 1
            while self.__is_in_bounds_position(
                (rd + car.size - 1, c)
            ) and self.__is_empty_position((rd + car.size - 1, c)):
                avails.append((rd, c))
                rd += 1
        return avails

    # Label, Top-Left corner (row coordinate), Top-Left corner (column coordinate), Size, Direction
    # Exemple:
    # A,1,1,2,0
    def __parse_state(self, state_descr: str) -> None:
        try:
            for line in state_descr.split("\n"):
                if line == "" or line is None:
                    continue
                tks: list[str] = line.split(",")
                car = Car(tks[0], (int(tks[1]), int(tks[2])), int(tks[3]), int(tks[4]))
                if not self.__is_car_addable(car):
                    raise BoardError(f"Car not addable to the game: {car}")

                self.__cars[car.label] = car
                self.__mark_board_with(car)

            if not self.__check_for_red_car():
                raise BoardError("Red car not present in descriptor")

        except (IndexError, ValueError) as e:
            raise BoardError(f"Error parsing state description: {e}")

    def __is_car_addable(self, car: Car) -> bool:
        (r, c) = car.top_left
        checks: list[tuple[int, int]] = self.__cells_of(car)
        for coord in checks:
            if not self.__is_in_bounds_position(coord) or not self.__is_empty_position(
                coord
            ):
                return False
        return True

    def __is_in_bounds_position(self, coord: tuple[int, int]) -> bool:
        return not (
            coord[0] < 0
            or coord[0] >= self.MAX_HEIGTH
            or coord[1] < 0
            or coord[1] >= self.MAX_WIDTH
        )

    def __is_empty_position(self, coord: tuple[int, int]) -> bool:
        return self.__state[coord[0]][coord[1]] == self.EMPTY_POS

    def __check_for_red_car(self) -> bool:
        return Car.RED_CAR in self.__cars

    def __cells_of(self, car: Car) -> list[tuple[int, int]]:
        (r, c) = car.top_left
        return (
            [(r, c + i) for i in range(car.size)]
            if car.is_horizontal_direction()
            else [(r + i, c) for i in range(car.size)]
        )

    def __mark_board_with(self, car: Car) -> None:
        for r, c in self.__cells_of(car):
            self.__state[r][c] = car.label

    def __clear_from_board(self, car: Car) -> None:
        for r, c in self.__cells_of(car):
            self.__state[r][c] = self.EMPTY_POS

    def __eq__(self, other: Any) -> bool:
        return self.to_sha256() == other.to_sha256()

    def __str__(self) -> str:
        text: str = "     0   1   2   3   4   5"
        for r, row in enumerate(self.__state):
            text += f"\n{r}: | "
            for col in row:
                text += f"{col} | "
        text += "\n"
        return text
