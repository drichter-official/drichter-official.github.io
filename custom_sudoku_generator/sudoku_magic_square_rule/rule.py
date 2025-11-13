import sys
import os
import random

# Add parent directory to path to import base_rule
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from base_rule import BaseRule


class MagicSquareRule(BaseRule):
    """
    Magic Square Sudoku: The center 3x3 box must form a magic square where all rows,
    columns, and diagonals sum to 15 (using digits 1-9).

    Generation strategy (FORWARD GENERATION with pre-filling):
    1. Pre-fill the center 3x3 box with one of the 8 valid magic square configurations
    2. Then use backtracking to solve the rest of the grid with standard Sudoku rules
    3. The magic square cells act as "givens" that constrain the rest of the puzzle

    This is NOT reverse generation (which would generate a complete solution first,
    then derive constraints). Instead, we set up the magic square constraint upfront
    and generate the solution around it.
    """

    # All possible 3x3 magic squares using digits 1-9 (and their rotations/reflections)
    MAGIC_SQUARES = [
        [[2, 7, 6], [9, 5, 1], [4, 3, 8]],
        [[2, 9, 4], [7, 5, 3], [6, 1, 8]],
        [[4, 3, 8], [9, 5, 1], [2, 7, 6]],
        [[4, 9, 2], [3, 5, 7], [8, 1, 6]],
        [[6, 1, 8], [7, 5, 3], [2, 9, 4]],
        [[6, 7, 2], [1, 5, 9], [8, 3, 4]],
        [[8, 1, 6], [3, 5, 7], [4, 9, 2]],
        [[8, 3, 4], [1, 5, 9], [6, 7, 2]],
    ]

    def __init__(self, size=9, box_size=3):
        super().__init__(size, box_size)
        self.name = "Magic Square Sudoku"
        self.description = "Center 3x3 box forms a magic square (all rows, columns, diagonals sum to 15)"

        # The center box spans rows 3-5 and columns 3-5
        self.magic_box_rows = (3, 4, 5)
        self.magic_box_cols = (3, 4, 5)
        self.magic_sum = 15

        # Store the chosen magic square configuration
        self.chosen_magic_square = None

    def supports_reverse_generation(self):
        """Magic Square uses forward generation with pre-filling."""
        return False

    def pre_fill_grid(self, grid):
        """
        Pre-fill the grid with a valid magic square in the center box.
        This is called before the main generation process.

        Args:
            grid: The empty grid to pre-fill

        Returns:
            bool: True if pre-filling was successful
        """
        print("  Pre-filling center box with magic square...")

        # Try different magic square configurations until one works with Sudoku constraints
        magic_squares = self.MAGIC_SQUARES.copy()
        random.shuffle(magic_squares)

        for magic_square in magic_squares:
            # Try to place this magic square in the center
            valid = self._try_place_magic_square(grid, magic_square)
            if valid:
                self.chosen_magic_square = magic_square
                print(f"  Successfully placed magic square in center box")
                self._print_magic_square(magic_square)
                return True

        print("  Warning: Could not place any magic square configuration!")
        return False

    def _try_place_magic_square(self, grid, magic_square):
        """
        Try to place a magic square in the center box.
        Check if it violates any initial Sudoku constraints.
        """
        # Place the magic square temporarily
        for i, row_idx in enumerate(self.magic_box_rows):
            for j, col_idx in enumerate(self.magic_box_cols):
                grid[row_idx][col_idx] = magic_square[i][j]

        # Verify it doesn't violate basic Sudoku rules (rows/cols at this stage)
        # Since we're filling an empty grid, we just need to check the box has unique values
        values = []
        for i in self.magic_box_rows:
            for j in self.magic_box_cols:
                val = grid[i][j]
                if val in values:
                    # Duplicate found, this configuration doesn't work
                    self._clear_magic_square(grid)
                    return False
                values.append(val)

        return True

    def _clear_magic_square(self, grid):
        """Clear the magic square from the grid."""
        for row_idx in self.magic_box_rows:
            for col_idx in self.magic_box_cols:
                grid[row_idx][col_idx] = 0

    def _print_magic_square(self, magic_square):
        """Print the magic square for debugging."""
        print("  Magic square configuration:")
        for row in magic_square:
            print(f"    {row}")
        print(f"  All rows, columns, and diagonals sum to {self.magic_sum}")


    def validate(self, grid, row, col, num):
        """
        Check if placing 'num' at (row, col) violates the magic square rule.

        Since the magic square is pre-filled, we just need to ensure it stays intact.
        """
        # Only check if we're in the center box
        if row not in self.magic_box_rows or col not in self.magic_box_cols:
            return True

        # If this cell is part of the pre-filled magic square, it should already be set
        # During generation, the magic square cells are filled first, so this shouldn't be called
        # But if it is, we check against the chosen magic square
        if self.chosen_magic_square is not None:
            row_idx = list(self.magic_box_rows).index(row)
            col_idx = list(self.magic_box_cols).index(col)
            expected = self.chosen_magic_square[row_idx][col_idx]
            # The magic square cells should match what we pre-filled
            return num == expected

        # Fallback: check magic square constraints dynamically
        # Create a temporary view with the new number
        def get_val(r, c):
            if r == row and c == col:
                return num
            return grid[r][c]

        # Check all rows in the magic box
        for r in self.magic_box_rows:
            vals = [get_val(r, c) for c in self.magic_box_cols]
            if all(v != 0 for v in vals):
                if sum(vals) != self.magic_sum:
                    return False

        # Check all columns in the magic box
        for c in self.magic_box_cols:
            vals = [get_val(r, c) for r in self.magic_box_rows]
            if all(v != 0 for v in vals):
                if sum(vals) != self.magic_sum:
                    return False

        # Check main diagonal (top-left to bottom-right)
        diag1_vals = [get_val(self.magic_box_rows[i], self.magic_box_cols[i]) for i in range(3)]
        if all(v != 0 for v in diag1_vals):
            if sum(diag1_vals) != self.magic_sum:
                return False

        # Check anti-diagonal (top-right to bottom-left)
        diag2_vals = [get_val(self.magic_box_rows[i], self.magic_box_cols[2-i]) for i in range(3)]
        if all(v != 0 for v in diag2_vals):
            if sum(diag2_vals) != self.magic_sum:
                return False
        
        return True

    def get_metadata(self):
        """Return metadata including magic square box location."""
        metadata = super().get_metadata()
        metadata['magic_box_location'] = {
            'rows': list(self.magic_box_rows),
            'cols': list(self.magic_box_cols),
            'target_sum': self.magic_sum
        }
        if self.chosen_magic_square is not None:
            metadata['magic_square'] = self.chosen_magic_square
        metadata['generation_mode'] = 'forward_with_prefill'
        return metadata



# Factory function to create an instance of this rule
def create_rule(size=9, box_size=3):
    return MagicSquareRule(size, box_size)
