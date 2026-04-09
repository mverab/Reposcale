# TaskCLI

A command-line task management tool with user accounts.

## Setup

```bash
pip install -r requirements.txt
python manage.py migrate
python src/main.py
```

## Features

- Create, list, and complete tasks
- User registration and login
- Persistent storage with SQLite
- Team collaboration (coming soon)

## Usage

```bash
python src/main.py add "Buy groceries"
python src/main.py list
python src/main.py done 1
```
