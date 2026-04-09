"""TaskCLI — main entry point."""

import click

from tasks import TaskManager


@click.group()
def cli():
    """TaskCLI — manage your tasks from the command line."""
    pass


@cli.command()
@click.argument("title")
def add(title):
    """Add a new task."""
    tm = TaskManager()
    task = tm.add_task(title)
    click.echo(f"Added task #{task['id']}: {title}")


@cli.command(name="list")
def list_tasks():
    """List all tasks."""
    tm = TaskManager()
    tasks = tm.get_tasks()
    if not tasks:
        click.echo("No tasks yet.")
        return
    for t in tasks:
        status = "✓" if t["done"] else " "
        click.echo(f"  [{status}] #{t['id']} {t['title']}")


@cli.command()
@click.argument("task_id", type=int)
def done(task_id):
    """Mark a task as done."""
    tm = TaskManager()
    tm.complete_task(task_id)
    click.echo(f"Task #{task_id} marked as done.")


if __name__ == "__main__":
    cli()
