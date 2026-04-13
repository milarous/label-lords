# Label Lords - Web Version

A record label management simulation game, migrated from tkinter to Flask web app.

## How to Run

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the app:
   ```bash
   python main.py
   ```

3. Open your browser and go to `http://127.0.0.1:5000/`

## Game Features

- Set up your record label with custom name, CEO, and location
- Comprehensive dashboard showing label overview and signed artists
- View and sign unsigned artists from a talent pool
- Manage signed artists: promote, release singles/albums
- Finish weeks to earn revenue from releases (with depreciation over time)
- Persistent status display showing current week and funds across all pages
- Standard dark mode UI with a modern responsive interface

## Migration Notes

This app was originally a tkinter GUI application. It has been migrated to a web-based Flask application with HTML templates for the user interface. The current version uses a shared base template and dark-themed CSS for a polished browser experience.