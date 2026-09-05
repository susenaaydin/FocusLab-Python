# FocusLab-Python

A desktop productivity and focus application developed with Python and CustomTkinter. FocusLab helps users track their working time, manage daily tasks, and review their productivity history.

## Features

* Work time tracking with a stopwatch
* Countdown timer for focused work sessions
* Preset timers of 10, 25, and 45 minutes
* Custom timer duration
* Adding and deleting daily tasks
* Creating and managing task categories
* Recording work sessions by category
* Viewing daily work history
* Viewing daily productivity statistics
* Reviewing previous work sessions through the calendar
* 9 different color themes
* Persistent data storage using a `JSON` file
* Windows `.exe` version available

## Technologies

* Python
* CustomTkinter
* Tkinter
* JSON
* Threading
* PyInstaller

## Application Sections

### Stopwatch

Tracks working time in seconds. While the stopwatch is running, the working time is recorded in the daily history.

### Timer

FocusLab provides three preset timer options:

* 10 minutes
* 25 minutes
* 45 minutes

Users can also enter a custom duration in minutes.

### Daily Planner

Users can create and delete tasks and organize them using custom categories.

Tasks are stored together with their completion status and recorded working duration.

### Calendar

Displays the total amount of recorded working time for previous days.

### Statistics

Displays the total working time for the current day in hours and minutes.

### Theme Selection

The application includes 9 different themes:

* Pink
* Dark Pink
* Metal
* Purple
* Blue
* Midnight
* Lilac
* Mint
* Sunset Orange

## Data Storage

FocusLab stores tasks, categories, the selected theme, and working history in the `data.json` file.

Example data structure:

```json
{
    "theme": "Pink",
    "categories": [],
    "tasks": [],
    "history": {}
}
```

## Installation

Install the required Python library:

```bash
pip install customtkinter
```

Then run the application with:

```bash
python FocusLab.py
```

## Windows EXE Version

A standalone Windows `.exe` version of FocusLab is also available.

The executable can be downloaded from the **GitHub Releases** section and run without requiring a Python installation.

## Project Structure

```text
FocusLab/
│
├── FocusLab.py
├── data.json
├── README.md
└── .gitignore
```

## Project Purpose

FocusLab was developed as a desktop productivity application for tracking working time, organizing tasks, and storing daily productivity data.

The project demonstrates desktop GUI development with Python, JSON-based data storage, time management, threading, theme management, and packaging a Python application as a Windows executable.

## Project Status

Completed.

## Future Improvements

* Graph-based productivity statistics
* Task editing
* Notification system
* Pomodoro mode
* Weekly and monthly reports
* Daily and weekly work goals
* More advanced calendar interface
* Improved data management

## Author

Sude Sena Aydın
