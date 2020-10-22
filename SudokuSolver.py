"""
Purpose:        Solve a Sudoku puzzle

Input:          A text file containing an unfinished Sudoku called 'Sudoku.txt'. The text file
                should only contain numbers and should be formatted in a 9x9 grid. The number 0
                should be used to indicate an empty cell.

                Example:
                000407000
                901683000
                020005070
                000801050
                010009762
                734056000
                190704083
                040598026
                056100000

Output:         A text file called 'SudokuSolution.txt' with a possible solution to
                the given puzzle. If no solution is found, the text file will read
                "No solution found".

Description:    The program will open a text file that represents an unfinished Sudoku puzzle,
                parse the file, and attempt to solve the puzzle using a backtracking algorithm.
                The finished solution will be outputted in a new text file.

Author:         Bram Delver

Version: 1.0
"""

import sys


def main():
    # Look for Sudoku file provided by user through commandline argument
    try:
        sudoku_file = sys.argv[1]
    except IndexError:
        raise SystemExit("You have not provided a sudoku file to solve.\n"
                         "Please run this program with the name of the file as argument from the command line\n"
                         f"Example: {sys.argv[0]} my_sudoku_file.txt")

    sudoku = read_sudoku(sudoku_file)  # Parse the file
    solved_sudoku = solve_sudoku(sudoku)  # Solve the puzzle

    with open("SudokuSolution.txt", "w") as solution:
        if solved_sudoku is not None:  # Found a solution
            solved_sudoku = format_for_output(solved_sudoku)
            solution.write(solved_sudoku)

        else:  # Didn't find a solution
            solution.write("No solution found.")


def format_for_output(solution):
    """
    Formats the solution for readable output.

    :param solution: List of integers
    :return: String formatted in 9 rows of 9
    """
    formatted_solution = [str(num) for num in solution]
    formatted_solution = ''.join(formatted_solution)
    formatted_solution = formatted_solution[:9] + '\n' + formatted_solution[9:18] + '\n' + \
                         formatted_solution[18:27] + '\n' + formatted_solution[27:36] + '\n' + \
                         formatted_solution[36:45] + '\n' + formatted_solution[45:54] + '\n' + \
                         formatted_solution[54:63] + '\n' + formatted_solution[63:72] + '\n' + \
                         formatted_solution[72:]

    return formatted_solution


def read_sudoku(file):
    """
    Parses a given .txt file that has 9 rows of 9 numbers.

    :param file: Path to a .txt file
    :return: All numbers in the given file as a list of integers
    """

    with open(file) as sudoku_file:
        numbers_in_given_sudoku = sudoku_file.read().replace('\n', '')  # Parse file without newline characters

    return [int(number) for number in numbers_in_given_sudoku]  # Return a list of the numbers in the file


def solve_sudoku(sudoku, start=0):
    """
    Solves the Sudoku using a backtracking algorithm. Returns None if no solution could be found.

    :param start: Index of the position from where we want to solve the puzzle
    :param sudoku: List of integers
    :return: List of integers or None
    """
    # Base case: the whole puzzle is solved
    if solved(sudoku):
        return sudoku

    # Copy our input list
    candidate = sudoku.copy()

    # Find an empty cell
    for index in range(start, len(candidate)):  # Only iterate over the part of the puzzle we haven't solved yet
        if candidate[index] == 0:

            # Increment the number in the cell
            while candidate[index] < 9:
                candidate[index] += 1

                # If the number is (for now) correct, explore this solution
                if correct(candidate, index):
                    candidate_solution = solve_sudoku(candidate, index+1)

                    # We've found a solution
                    if candidate_solution is not None:
                        return candidate_solution

            # We've incremented up to 9 without correct solution, so backtrack
            return


def solved(candidate):
    """
    Returns true if there are no more empty cells in the Sudoku, false otherwise

    :param candidate: A list of integers
    :return: True or False
    """

    return candidate.count(0) == 0


def check_row_or_column(start, stop, step, candidate, value, index):
    """
    Helper function to iterate over a row or a column. Returns false if it finds duplicate values

    :param start: Index of the start of the row or column
    :param stop: Index of the start of the next row or column
    :param step: Step to the next index (1 for rows or 9 for columns)
    :param candidate: List of integers
    :param value: Value of the integer we want to check is correct
    :param index: Index of the value we want to check is correct
    :return: True or False
    """
    for i in range(start, stop, step):
        if i == index:  # Don't compare the value to itself
            continue
        if candidate[i] == value:  # Found a duplicate; not a valid solution
            return False

    return True


def correct(candidate, index):
    """
    Returns true if the number at the index position does not violate the rules of Sudoku
    (i.e. number does not repeat in horizontal row, vertical row, or the 3x3 quadrant it is in).

    :param candidate: List of integers
    :param index: Index of the value we want to check
    :return: True or False
    """

    # Store the value at the index we're checking
    check_val = candidate[index]

    # Check row
    start_row = (index // 9) * 9  # Find the index of the start of the row
    end_row = start_row + 9  # Find the index of the end of the row + 1 (start of next row)
    step = 1  # To find the next cell in the row, we increment the index by 1
    if not check_row_or_column(start_row, end_row, step, candidate, check_val, index):
        return False

    # Check column
    start_column = index % 9  # Find the index of the start of the column
    end_column = 8 * 9 + start_column  # Find the end of the column + 1 (start of next column)
    step = 9  # To find the next cell in the column, we increment by 9
    if not check_row_or_column(start_column, end_column, step, candidate, check_val, index):
        return False

    # Check 3x3 quadrant
    row_number = start_row / 9  # Calculate row number

    start_quadrant = int(((row_number // 3 * 3) * 9) + ((start_column // 3) * 3))

    return check_quadrant(start_quadrant, candidate, index, check_val)


def check_quadrant(start_index, candidate, index, check_val):
    """
    Checks for duplicate values in a 3x3 quadrant. Returns False if a duplicate value is found.

    :param start_index: Index of the top left cell of the quadrant
    :param candidate: List of integers
    :param index: Index of the value we're checking
    :param check_val: Value that we are checking
    :return: True or False
    """
    start = start_index  # Index of the start of the first row of the quadrant
    end = start_index + 3  # Index of the end of the first row of the quadrant + 1 (start of next row)

    for i in range(3):  # Iterate over the quadrant
        for j in range(start, end):  # Check the row
            if j == index:  # Don't compare value to itself
                continue
            if candidate[j] == check_val:  # Found a duplicate
                return False

        # Increment start and end values to the next row of the quadrant
        start += 9
        end += 9

    return True


if __name__ == '__main__':
    main()
