#!/usr/bin/env python3

import sys
import json
import subprocess

ZEN_NUMBER = 99
ZEN_NAME = 'zen'

WIDTH_PERC=50
MAX_WIDTH=800
HEIGHT_PERC=90
MAX_HEIGHT=1024

def enable_zen_mode(workspace_current, workspace_width, workspace_height):
    width = round(min(workspace_width * WIDTH_PERC / 100, MAX_WIDTH))
    height = round(min(workspace_height * HEIGHT_PERC / 100, MAX_HEIGHT))
    workspace_name = '{}: {}'.format(ZEN_NUMBER, workspace_current)
    return ';'.join([
        'move container to workspace {}'.format(workspace_name),
        'workspace {}'.format(workspace_name),
        'floating enable',
        'border none',
        'resize set width {}'.format(width),
        'resize set height {}'.format(height),
        'move position center'
    ])

def disable_zen_mode(workspace_previous):
    return ';'.join([
        'move container to workspace {}'.format(workspace_previous),
        'workspace {}'.format(workspace_previous),
        'floating disable',
        'border normal'
    ])

def goto_zen(workspace_name):
    return 'workspace {}'.format(workspace_name)

out = subprocess.run(['i3-msg', '-t', 'get_workspaces'], capture_output=True)
workspaces = json.loads(out.stdout)

workspace_current = list(filter(lambda w: w['focused'], workspaces))[0]
workspace_zen = list(filter(lambda w: w['num'] == ZEN_NUMBER, workspaces))

if __name__ == '__main__':
    if len(sys.argv) > 1:
        if len(workspace_zen):
            msg = disable_zen_mode(workspace_zen[0]['name'].split(':')[1].strip())
    else:
        if len(workspace_zen):
            msg = goto_zen(workspace_zen[0]['name'])
        else:
            msg = enable_zen_mode(workspace_current['num'],
                                  workspace_current['rect']['width'],
                                  workspace_current['rect']['height'])
    print(msg)
    subprocess.run(['i3-msg', msg])
