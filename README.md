# Rush Hour Solver

A Python implementation of a [Rush Hour](https://en.wikipedia.org/wiki/Rush_Hour_(puzzle)) puzzle solver using breadth-first search (BFS).

## Overview

Rush Hour is a sliding puzzle game played on a 6×6 grid. The goal is to move the red car (`X`) to the exit at position (row 2, column 4) by sliding other cars out of the way. Each car can only move along its own axis (horizontal or vertical).

This solver finds the **shortest sequence of moves** to solve any valid Rush Hour puzzle.

## Project Structure

```
rush_hour/
├── main.py                 # Entry point
├── components/
│   ├── car.py              # Car data model and validation
│   ├── board.py            # Board state and move generation
│   └── game.py             # BFS solver
└── data/
    ├── example_1.txt       # Simple puzzle example (4 cars)
    └── example_18.txt      # Complex puzzle example (12 cars)
```

## Usage

```bash
python3 main.py
```

The program loads the puzzle from `./data/` directory (e.g. `exemple_18.txt`), displays the initial board, and prints the solution.

To solve a different puzzle, place your own board initial file in the `./data/` directory and provide the file name as a parameter in the command line, e.g.:

```shell
python main.py exemple_1.txt
```

## Puzzle File Format

Each puzzle is a plain-text CSV file with one car per line:

```
Label,Row,Column,Size,Direction
```

| Field       | Description                            |
|-------------|----------------------------------------|
| `Label`     | Single character identifier (`X` = red car) |
| `Row`       | Top-left row (0-indexed)               |
| `Column`    | Top-left column (0-indexed)            |
| `Size`      | Car length: `2` or `3`                 |
| `Direction` | `0` = horizontal, `1` = vertical       |

**Example (`exemple_1.txt`):**

```
A,1,1,2,0
X,2,1,2,0
B,0,4,3,1
C,5,4,2,0
```

Which produces this board:

```
     0   1   2   3   4   5
0: |   | A |   |   | B |   |
1: |   | A |   |   | B |   |
2: |   | X | X |   | B |   |
3: |   |   |   |   |   |   |
4: |   |   |   |   |   |   |
5: |   |   |   |   | C | C |
```

## Algorithm

The solver uses **breadth-first search (BFS)** to guarantee the shortest solution:

1. Start from the initial board state.
2. Generate all reachable next states by sliding each car as far as possible in both directions.
3. Use SHA-256 hashing to detect and skip already-visited states.
4. Stop when the red car (`X`) reaches column 4 on row 2.
5. Reconstruct the solution path from the BFS parent-tracking dictionary.

## Running Tests

The test suite uses Python's built-in `unittest` module — no extra dependencies required.

```bash
python -m unittest discover -s tests -v
```

The 39 tests cover `Car`, `Board`, and `Game`, including end-to-end solver verification for two example puzzles.

## Requirements

- Python 3.8+
- No external dependencies (standard library only)
