import sys

from components.game import Game


def main():
    print("Rush Hour game!")
    try:
        game_start_file: str = sys.argv[1]
        game = Game(f"./data/{game_start_file}")
        path = game.solve()
        print(f"Steps: {path}")
    except Exception as err:
        print(f"Something went wrong. {err}")
        sys.exit(-1)


if __name__ == "__main__":
    main()
