#!/usr/bin/env python3

from subprocess import run
from i3ipc.aio import Connection
from i3ipc import Event
import asyncio

async def main():
    def on_event(self, e):
        if e.current.num == 99:
            run(['polybar-msg', 'cmd', 'hide'])
        elif e.old and e.old.num == 99:
            run(['polybar-msg', 'cmd', 'show'])

    c = await Connection(auto_reconnect=True).connect()
    workspaces = await c.get_workspaces()
    c.on(Event.WORKSPACE_FOCUS, on_event)
    await c.main()

asyncio.get_event_loop().run_until_complete(main())
