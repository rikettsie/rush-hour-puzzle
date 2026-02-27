from collections import deque
from typing import Deque, Optional

from .board import Board


class Game:
    END_GAME_POS: tuple[int, int] = (2, 4)

    def __init__(self, game_filepath: str) -> None:
        with open(game_filepath, "r") as fp:
            self.__initial_state_descr = fp.read()

    def solve(self) -> Optional[list[str]]:
        board_conf: Board = Board(self.__initial_state_descr)
        print("Initial state:")
        board_conf.describe()

        init_uid = board_conf.to_sha256()
        # We track the path from beginning to the solution
        tracker: dict[str, Optional[dict["str", "str"]]] = {init_uid: None}

        # We set already visited game configurations
        visited: set[str] = set(init_uid)

        # We track the processed parent game configuration
        processed: set[str] = set()

        # We initialize the BFS traversal queue with the initial board state
        tq: Deque[Board] = deque([board_conf])

        while tq:
            # Pop the next configuration
            game_conf = tq.popleft()

            # If already processed, skip it
            uid: str = game_conf.to_sha256()
            if uid in processed:
                continue

            # Verify if this is a winning configuration
            if self.__is_end_game(game_conf):
                path: list[str] = self.__path(uid, tracker)
                print(f"Game solved in {len(path)} steps.")
                return path

            # Mark as "processed"
            processed.add(uid)

            for variant in game_conf.available_variants():
                variant_board = variant["board"]
                vuid = variant_board.to_sha256()
                if vuid not in visited and vuid not in processed:
                    # Append configuration to be processed next
                    tq.append(variant_board)
                    # Mark as "visited"
                    visited.add(vuid)
                    # Tack ancestor relationship
                    tracker[vuid] = {"ancestor": uid, "move": variant["move"]}

        print("Game is not solvable.")
        return None

    def __path(
        self, uid: str, tracker: dict[str, Optional[dict["str", "str"]]]
    ) -> list[str]:
        path: list[str] = []
        while parent_state := tracker.get(uid):
            path.append(parent_state["move"])
            uid = parent_state["ancestor"]
        path.reverse()
        return path

    def __is_end_game(self, board_state: Board) -> bool:
        return board_state.cars["X"].top_left == self.END_GAME_POS
