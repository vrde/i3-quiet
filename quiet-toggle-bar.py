#!/usr/bin/env python3

import os
import sys
import argparse
import asyncio
from subprocess import run, check_output
from i3ipc.aio import Connection
from i3ipc import Event


def check_daemon(kill=False):
    name = os.path.basename(__file__)
    pid = os.getpid()
    pids = list(filter(lambda p: int(p) != pid, check_output(['pgrep', '-f', name]).split()))
    if pids:
        if kill:
            run(['kill'] + pids)
        else:
            sys.exit('Another instance is running, kill it or run this command with the --kill option')

async def main():
    def on_event(self, e):
        ws = 99
        if e.current.num == ws:
            run('i3-msg bar mode invisible'.split())
            run('polybar-msg cmd hide'.split())
        elif e.old and e.old.num == ws:
            run('i3-msg bar mode dock'.split())
            run('polybar-msg cmd show'.split())

    c = await Connection(auto_reconnect=True).connect()
    workspaces = await c.get_workspaces()
    c.on(Event.WORKSPACE_FOCUS, on_event)
    await c.main()

parser = argparse.ArgumentParser(description='Toggle the statusbar on i3wm.')
parser.add_argument('--kill', dest='kill', action='store_const',
                    const=True, default=False,
                    help='Kill any other running instance.')

args = parser.parse_args()
check_daemon(args.kill)
try:
    asyncio.get_event_loop().run_until_complete(main())
except KeyboardInterrupt:
    pass
