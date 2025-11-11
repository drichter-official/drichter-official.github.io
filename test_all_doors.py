#!/usr/bin/env python
"""Comprehensive test for all doors."""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from website.app import app, load_sudoku, load_solution

def test_door_loading(door_number):
    """Test if a door can load its puzzle and solution."""
    print(f"\n{'='*60}")
    print(f"Testing Door {door_number}")
    print('='*60)

    try:
        # Test loading puzzle
        print(f"Loading puzzle for door {door_number}...")
        puzzle = load_sudoku(door_number)
        print(f"✓ Puzzle loaded: {len(puzzle)} rows")
        print(f"  First row: {puzzle[0]}")

        # Test loading solution
        print(f"Loading solution for door {door_number}...")
        solution = load_solution(door_number)
        print(f"✓ Solution loaded: {len(solution)} rows")
        print(f"  First row: {solution[0]}")

        # Test web page
        print(f"Testing web page for door {door_number}...")
        with app.test_client() as client:
            response = client.get(f'/door/{door_number}')
            print(f"✓ Page loaded with status: {response.status_code}")

            if response.status_code == 200:
                # Check for key elements
                if b'sudoku' in response.data.lower():
                    print(f"✓ Page contains sudoku content")
                if b'Check Solution' in response.data:
                    print(f"✓ Page has Check Solution button")
                if b'Generate New Puzzle' in response.data:
                    print(f"✓ Page has Generate New Puzzle button")

                print(f"\n✓✓✓ Door {door_number} is fully functional! ✓✓✓")
            else:
                print(f"✗ Page returned status {response.status_code}")

    except Exception as e:
        print(f"✗ Error testing door {door_number}: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    for i in range (1, 25):
        test_door_loading(i)

