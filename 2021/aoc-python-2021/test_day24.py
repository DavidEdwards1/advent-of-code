import pytest
import day24

@pytest.mark.parametrize(
    "input_state,expected",
    [
        (
            {"w": 0, "x": 0, "y": 0, "z": 0, "input": {"buffer": [1], "read_pos": 0}},
            {"w": 0, "x": -1, "y": 0, "z": 0, "input": {"buffer": [1], "read_pos": 1}},
        )
    ]
)
def test_example_program(input_state, expected):
    program = day24.parse_input("data-day24-example.txt")
    assert day24.evaluate(program, input_state) == expected

@pytest.mark.parametrize(
    "input_state,expected",
    [
        (
            {"w": 0, "x": 0, "y": 0, "z": 0, "input": {"buffer": [1,3], "read_pos": 0}},
            {"w": 0, "x": 3, "y": 0, "z": 1, "input": {"buffer": [1,3], "read_pos": 2}},
        ),
        (
            {"w": 0, "x": 0, "y": 0, "z": 0, "input": {"buffer": [1,4], "read_pos": 0}},
            {"w": 0, "x": 4, "y": 0, "z": 0, "input": {"buffer": [1,4], "read_pos": 2}},
        )
    ]
)
def test_example_program_two(input_state, expected):
    program = day24.parse_input("data-day24-example2.txt")
    assert day24.evaluate(program, input_state) == expected

@pytest.mark.parametrize(
    "input_state,expected",
    [
        (
            {"w": 0, "x": 0, "y": 0, "z": 0, "input": {"buffer": [12], "read_pos": 0}},
            {"w": 1, "x": 1, "y": 0, "z": 0, "input": {"buffer": [12], "read_pos": 1}},
        ),
        (
            {"w": 0, "x": 0, "y": 0, "z": 0, "input": {"buffer": [5], "read_pos": 0}},
            {"w": 0, "x": 1, "y": 0, "z": 1, "input": {"buffer": [5], "read_pos": 1}},
        )
    ]
)
def test_example_program_three(input_state, expected):
    program = day24.parse_input("data-day24-example3.txt")
    assert day24.evaluate(program, input_state) == expected
