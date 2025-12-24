from weather import Weather
from task import Tasks
import sys


def main():
    """Interactive in-program input() prompts for adding tasks."""
    Tasks._ensure_table()
    print("Add tasks (leave title empty to quit)")
    while True:
        try:
            title = input("Title: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting.")
            break
        if not title:
            print("Exiting.")
            break
        due = input("Due date (YYYY-MM-DD, optional): ").strip() or None
        try:
            tid = Tasks.add_task(title, due)
            print(f"Task added with id: {tid}")
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)


if __name__ == '__main__':
    main()
