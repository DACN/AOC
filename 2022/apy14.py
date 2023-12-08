#!/usr/bin/env python
import itertools
from aocd.models import Puzzle
import timeit


Point = tuple[int, int]


def parse_point(point_str: str) -> Point:
    x, y = point_str.split(",", maxsplit=1)
    return (int(x), int(y))


def draw_line(grid: dict, start: Point, end: Point) -> None:
    if start[0] == end[0]:
        # vertical line
        y_min, y_max = sorted([start[1], end[1]])
        points = {(start[0], y): "#" for y in range(y_min, y_max + 1)}
    else:
        # horizontal line
        x_min, x_max = sorted([start[0], end[0]])
        points = {(x, start[1]): "#" for x in range(x_min, x_max + 1)}
    grid |= points
    return None


def make_grid(lines: list[str]) -> dict:
    grid: dict = {}
    for line in lines:
        points = [parse_point(p) for p in line.split(" -> ")]
        for start, end in itertools.pairwise(points):
            draw_line(grid, start, end)

    return grid


def drop_grain(grid: dict) -> None | Point:
    max_y = max(y for (x, y) in grid if grid[(x, y)] == "#")
    pos = (500, 0)
    while True:
        for next_pos in [
            (pos[0], pos[1] + 1),
            (pos[0] - 1, pos[1] + 1),
            (pos[0] + 1, pos[1] + 1),
        ]:
            if next_pos not in grid:
                if next_pos[1] == max_y:
                    # it's going to flow out the bottom
                    return None
                else:
                    pos = next_pos
                    break
        else:
            # none of the possible moves are free, grain can't move
            return pos


def do_part_1(grid: dict) -> int:
    while (pos := drop_grain(grid)) is not None:
        grid[pos] = "o"

    return count_grains(grid)


def do_part_2(grid: dict) -> int:
    max_y = max(y for (x, y) in grid if grid[(x, y)] == "#")
    grid[(500, 0)] = "o"
    points = {(500, 0): "o"}
    for y in range(1, max_y + 2):
        new_points = {}
        for point in points:
            for offset in [-1, 0, 1]:
                new_points[(point[0] + offset, y)] = "o"

        for point in list(new_points):
            if grid.get(point) == "#":
                del new_points[point]
        grid |= new_points
        points = new_points

    return count_grains(grid)


def count_grains(grid: dict) -> int:
    return len([x for x, y in grid.items() if y == "o"])


def main():
    # lines = read_input()
    puzzle = Puzzle(year=2022, day=14)

    lines = puzzle.input_data.split('\n')

    grid = make_grid(lines)

    part_1 = do_part_1(grid)
    print(f"{part_1=}")

    start_time = timeit.default_timer()

    do_part_2(grid)
    part_2 = len([x for x, y in grid.items() if y == "o"])
    print(f"{part_2=}")
    print("took", timeit.default_timer() - start_time)


def read_input() -> list[str]:
    with open("day14.txt") as f:
        return f.read().rstrip().split("\n")


if __name__ == "__main__":
    main()
