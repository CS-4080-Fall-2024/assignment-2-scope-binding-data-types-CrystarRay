# Time Complexity: O(9^N) N is the number of empty cells
# Space Complexity O(N)
class Solution:
    def solveSudoku(self, board: List[List[str]]) -> None:
        # Initialize data structures to keep track of used numbers
        used_in_row = [set() for _ in range(9)]
        used_in_col = [set() for _ in range(9)]
        used_in_box = [set() for _ in range(9)]
        empty_positions = []

        # Iterating Over the Board -> If the cell contains '.', it's empty,
        # and its position (r, c) is added to empty_cells. -> Updating Used Numbers
        # else Calculating box_index
        for r in range(9):
            for c in range(9):
                num = board[r][c]
                if num != '.':
                    used_in_row[r].add(num)
                    used_in_col[c].add(num)
                    box_index = (r // 3) * 3 + c // 3
                    used_in_box[box_index].add(num)
                else:
                    empty_positions.append((r, c))

        # The backtracking algorithm works by recursively filling each empty cell
        # with a valid number from '1' to '9', ensuring that the chosen number doesn't
        # conflict with existing numbers in the same row, column, or 3x3 box. It places
        # a valid number in the current cell, updates the board and tracking sets, and
        # then proceeds to the next empty cell. If it encounters a situation where no
        # valid number can be placed in a cell, it backtracks: it resets the current cell
        # to empty, removes the number from the tracking sets, and tries the next possible
        # number. This process continues recursively, exploring all possible valid
        # configurations, until the entire puzzle is successfully solved.
        def backtrack(position_index):
            # Base Case
            if position_index == len(empty_positions):
                return True  # Puzzle solved
            row, col = empty_positions[position_index]
            box_index = (row // 3) * 3 + col // 3
            for digit in '123456789':
                if (digit not in used_in_row[row] and
                    digit not in used_in_col[col] and
                    digit not in used_in_box[box_index]):
                    # Place the digit
                    board[row][col] = digit
                    used_in_row[row].add(digit)
                    used_in_col[col].add(digit)
                    used_in_box[box_index].add(digit)

                    # Move to the next empty position
                    if backtrack(position_index + 1):
                        return True

                    # Backtrack if needed
                    board[row][col] = '.'
                    used_in_row[row].remove(digit)
                    used_in_col[col].remove(digit)
                    used_in_box[box_index].remove(digit)
            return False  # Trigger backtracking

        # The initial call starts the process by attempting to fill the first empty cell
        backtrack(0)

