from rich.live import Live
from rich.table import Table
from rich.console import Group
from rich.panel import Panel
from rich.progress import Progress, BarColumn, TextColumn
from rich.align import Align
from rich import box
import time
from threading import Thread
from metrics import get_metrics


def start_dashboard():
    Thread(target=run_dashboard, daemon=True).start()


def run_dashboard():
    with Live(render_dashboard(), refresh_per_second=1, screen=True) as live:
        while True:
            time.sleep(1)
            live.update(render_dashboard())


def render_dashboard():
    metrics = get_metrics()

    uptime = int(time.time() - metrics["start_time"])
    total_messages = metrics["total_messages"]
    messages_per_min = metrics["messages_per_minute"]
    strain = metrics["server_strain"]
    emotion_counts = metrics["emotion_counts"]

    main_table = Table.grid(padding=1)
    main_table.add_column()
    main_table.add_column()

    summary = Table(title="Summary", box=box.SIMPLE)
    summary.add_column("Metric", justify="left")
    summary.add_column("Value", justify="right")
    summary.add_row("Uptime (s)", str(uptime))
    summary.add_row("Total Msgs", str(total_messages))
    summary.add_row("Msgs/Min", f"{messages_per_min:.2f}")
    summary.add_row("Server Strain", f"{strain:.0f}%")

    progress = Progress(
        TextColumn("Server Load"),
        BarColumn(bar_width=30),
        TextColumn("{task.percentage:>3.0f}%")
    )
    task = progress.add_task("strain", total=100, completed=strain)

    emotion_table = Table(title="Emotion Counts", box=box.SIMPLE, expand=True)
    emotion_table.add_column("Emotion")
    emotion_table.add_column("Messages", justify="right")
    for emo, count in emotion_counts.items():
        emotion_table.add_row(emo.capitalize(), str(count))

    main_table.add_row(summary, Panel(progress, title="Server Strain", border_style="cyan"))
    layout = Group(
        Panel(main_table, title="Bot Metrics", border_style="green"),
        emotion_table
    )
    return Align.center(layout)
