from flask import Flask, render_template, jsonify
import random
import os
import ast
import sys

app = Flask(__name__)

# Add the custom_sudoku_generator to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'custom_sudoku_generator'))

# Mapping of door numbers to rule folders
DOOR_TO_RULE = {
    1: 'sudoku_knights_rule',
    # Add more mappings as needed
}

def get_rule_folder(door_number):
    """Get the rule folder path for a given door number."""
    rule_name = DOOR_TO_RULE.get(door_number, 'sudoku_knights_rule')
    return os.path.join(os.path.dirname(__file__), '..', 'custom_sudoku_generator', rule_name)

position_classes = [
    'pos1', 'pos2', 'pos3', 'pos4', 'pos5', 'pos6',
    'pos7', 'pos8', 'pos9', 'pos10', 'pos11', 'pos12',
    'pos13', 'pos14', 'pos15', 'pos16', 'pos17', 'pos18',
    'pos19', 'pos20', 'pos21', 'pos22', 'pos23', 'pos24',
]

def load_sudoku(door_number=1):
    """Load sudoku puzzle from text file."""
    rule_folder = get_rule_folder(door_number)
    path = os.path.join(rule_folder, 'sudoku.txt')
    grid = []
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            row = ast.literal_eval(line)
            grid.append(row)
    return grid

def load_solution(door_number=1):
    """Load sudoku solution from text file."""
    rule_folder = get_rule_folder(door_number)
    path = os.path.join(rule_folder, 'solution.txt')
    grid = []
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            row = ast.literal_eval(line)
            grid.append(row)
    return grid

@app.route('/')
def calendar():
    shuffled_doors = list(range(1, 25))
    random.shuffle(shuffled_doors)
    # Pass list of tuples (door_number, position_class)
    door_positions = list(zip(shuffled_doors, position_classes))
    return render_template("calendar.html", door_positions=door_positions)

@app.route('/door/<int:door_number>')
def door(door_number):
    # For door 1, load and display the interactive sudoku
    if door_number == 1:
        sudoku_grid = load_sudoku(door_number)
        solution_grid = load_solution(door_number)
        return render_template("door1.html", door=door_number, sudoku=sudoku_grid, solution=solution_grid)
    # For other doors, render their specific templates
    return render_template(f"door{door_number}.html", door=door_number)

@app.route('/generate/<int:door_number>')
def generate_puzzle(door_number):
    """Generate a new sudoku puzzle for the specified door."""
    try:
        from run import generate_sudoku_for_rule

        rule_folder = get_rule_folder(door_number)

        # Generate new puzzle
        print(f"Generating new puzzle for door {door_number}...")
        puzzle_grid, solution_grid = generate_sudoku_for_rule(rule_folder)

        return jsonify({
            'success': True,
            'message': 'New puzzle generated successfully!'
        })
    except Exception as e:
        print(f"Error generating puzzle: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'message': f'Error generating puzzle: {str(e)}'
        }), 500

if __name__ == "__main__":
    app.run(debug=True)
