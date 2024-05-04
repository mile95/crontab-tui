import sys
import croniter
import datetime
import re

from typing import List
from textual.app import App, ComposeResult
from textual.widgets import DataTable


def read_crontab_file() -> List[str]:
    file_name = sys.argv[1]
    lines = []
    with open(file_name, "r") as f:
        return f.read()


def parse_crontab():
    entries = []
    pattern = re.compile(r"^(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(.*)$")
    raw_file = read_crontab_file()
    for line in raw_file.splitlines():
        if line.strip() and not line.strip().startswith("#"):
            match = pattern.match(line.strip())
            if match:
                schedule = " ".join(match.group(1, 2, 3, 4, 5))
                script = match.group(6)
                entries.append((schedule, script))
    return entries


def generate_rows():
    crontab = parse_crontab()
    now = datetime.datetime.now()
    rows = []
    for schedule, job in crontab:
        cron = croniter.croniter(schedule, now)
        next_run = cron.get_next(datetime.datetime)
        time_to_next = next_run - now
        rows.append((schedule, job, next_run, time_to_next))

    return rows


class CronTabApp(App):

    def compose(self) -> ComposeResult:
        yield DataTable()

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.add_columns("Schedule", "Job", "Next", "Time until next")
        rows = generate_rows()
        table.add_rows(rows)


if __name__ == "__main__":
    app = CronTabApp()
    app.run()
