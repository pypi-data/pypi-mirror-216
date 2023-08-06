from typing import List, IO, Optional
import subprocess as sp
import sys
from datetime import datetime
from pathlib import Path
import time
import threading
import csv

import typer
import psutil
import rich.live
import rich.text
import rich.console
import rich.panel
import rich.rule
import plotext

app = typer.Typer(rich_markup_mode="rich")


class Monitor:
    interval: float

    max_rss: float = 0
    max_vms: float = 0

    terminate: bool = False

    def __init__(
        self,
        command: List[str],
        output: IO[str],
        interval: float = 0.5,
        live: Optional[rich.live.Live] = None,
    ):
        self.interval = interval
        self.live = live
        self.command = command
        self.writer = csv.writer(output)
        self.writer.writerow(("time", "rss", "vms"))

        self.time: List[float] = [0]
        self.rss: List[float] = [0]
        self.vms: List[float] = [0]

    def run(self, p: psutil.Process):
        try:
            start = datetime.now()
            while p.status() in (psutil.STATUS_RUNNING, psutil.STATUS_SLEEPING):
                if self.terminate:
                    return
                delta = (datetime.now() - start).total_seconds()
                rss = p.memory_info().rss
                vms = p.memory_info().vms
                for subp in p.children(recursive=True):
                    try:
                        rss += subp.memory_info().rss
                        vms += subp.memory_info().vms
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        pass

                self.rss.append(rss / 1e6)
                self.vms.append(vms / 1e6)
                self.time.append(delta)
                self.max_rss = max(rss, self.max_rss)
                self.max_vms = max(vms, self.max_vms)

                self.writer.writerow((delta, rss, vms))

                if self.live is not None:
                    self.live.update(
                        rich.console.Group(
                            rich.rule.Rule("Memory monitoring"),
                            rich.text.Text("Running: " + " ".join(self.command)),
                            rich.text.Text(
                                f"[{delta:8.2f}s] [rss: {rss/1e6:8.2f}M, max: {self.max_rss/1e6:8.2f}M] [vms: {vms/1e6:8.2f}M, max: {self.max_vms/1e6:8.2f}M]"
                            ),
                        )
                    )

                time.sleep(self.interval)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            return


@app.command()
def main(
    cmd: List[str],
    interval: float = typer.Option(0.5, "--interval", "-i"),
    output: Path = typer.Option("spyral.csv", "--output", "-o"),
):
    p = psutil.Popen(cmd, stdout=sp.PIPE, stderr=sp.STDOUT)
    console = rich.console.Console()

    with rich.live.Live(
        console=console, transient=not sys.stdout.isatty()
    ) as live, output.open("w") as ofh:
        ofh.write("# " + " ".join(cmd) + "\n")
        mon = Monitor(interval=interval, live=live, output=ofh, command=cmd)
        t = threading.Thread(target=mon.run, args=(p,))
        t.start()

        try:
            while p.status() in (psutil.STATUS_RUNNING, psutil.STATUS_SLEEPING):
                for line in iter(p.stdout.readline, b""):
                    live.console.out(line.decode("utf-8"), highlight=False, end="")
        except KeyboardInterrupt:
            mon.terminate = True
            t.join()
            p.kill()
            raise

        p.wait()
        t.join()

    if sys.stdout.isatty():
        console.rule("Memory usage")
        plotext.clf()

        plotext.plot_size(
            plotext.terminal_width(), max(20, (plotext.terminal_height() or 70) / 3)
        )

        plotext.subplots(2, 1)

        p1 = plotext.subplot(1, 1)
        p2 = plotext.subplot(2, 1)

        p1.plot(mon.time, mon.rss)
        p1.title("RSS")
        p1.xlabel("time [s]")
        p1.ylabel("rss [M]")

        p2.title("VMS")
        p2.plot(mon.time, mon.vms)
        p2.xlabel("time [s]")
        p2.ylabel("vms [M]")

        plotext.show()  # to finally plot
