# Advent Calendar Web Application

An interactive advent calendar with a Sudoku puzzle behind door 1!

## Features

- 24 interactive doors arranged in a grid
- Door 1 opens an interactive, playable Sudoku puzzle
- Knight's Rule Sudoku variant
- Keyboard navigation support
- Solution checking
- Responsive design

## Deployment Options

This application supports two deployment platforms:

### 🌊 Digital Ocean (main branch)
For cloud deployment on Digital Ocean App Platform.
- Branch: `main`
- See deployment files: `.do/app.yaml`, `Procfile`, `requirements.txt`, `.python-version`

### 🥧 Raspberry Pi (raspberry-pi branch)
For local deployment on Raspberry Pi.
- Branch: `raspberry-pi`
- See: [Raspberry Pi Setup Guide](README_RASPBERRY_PI.md)

## Quick Start (Raspberry Pi)

```bash
git clone https://github.com/drichter-official/calendar.git advent_calendar
cd advent_calendar
git checkout raspberry-pi
./install.sh
./setup_service.sh
```

## Project Structure

```
advent_calendar/
├── custom_sudoku_generator/
│   └── sudoku_knights_rule/
│       ├── sudoku.txt      # The puzzle
│       ├── solution.txt    # The solution
│       └── rule.py         # Generation logic
├── website/
│   ├── app.py             # Flask application
│   ├── static/
│   │   ├── styles.css
│   │   ├── img.png
│   │   └── white_img.png
│   └── templates/
│       ├── calendar.html   # Main calendar view
│       ├── door1.html      # Interactive Sudoku
│       ├── door2.html
│       └── door3.html
├── requirements.txt        # Python dependencies
├── .python-version        # Python version specification
└── Procfile               # Process configuration
```

## Development

### Local Development
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cd website
python app.py
```

Visit `http://localhost:5000`

## Technologies

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript
- **Deployment**: Gunicorn (WSGI server)
- **Platforms**: Digital Ocean App Platform, Raspberry Pi

## License

MIT License - feel free to use and modify for your own advent calendar!

