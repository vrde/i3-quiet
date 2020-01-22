#!/usr/bin/env python3

from subprocess import run, check_output
from i3ipc.aio import Connection
from i3ipc import Event
import asyncio

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

asyncio.get_event_loop().run_until_complete(main())
