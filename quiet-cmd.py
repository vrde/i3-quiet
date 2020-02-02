#!/usr/bin/env python3

import sys
import json
import subprocess
import os

ZEN_NUMBER = 99
ZEN_NAME = 'zen'

WIDTH_PERC=50
MAX_WIDTH=800
HEIGHT_PERC=90
MAX_HEIGHT=1024

ZEN_BORDER = 'none'
DEFAULT_BORDER = 'none'

ZEN_FILE_PATH = os.path.join(os.environ['HOME'], '.config/i3/.i3-quiet.json')

def enable_zen_mode(workspace):
    width = round(min(workspace['rect']['width'] * WIDTH_PERC / 100, MAX_WIDTH))
    height = round(min(workspace['rect']['height'] * HEIGHT_PERC / 100, MAX_HEIGHT))
    workspace_name = '{}: {}'.format(ZEN_NUMBER, workspace['name'])
    with open(ZEN_FILE_PATH, 'w') as zen_file:
        json.dump(workspace, zen_file)
    return ';'.join([
        'move container to workspace {}'.format(workspace_name),
        'workspace {}'.format(workspace_name),
        'floating enable',
        'border {}'.format(ZEN_BORDER),
        'resize set width {}'.format(width),
        'resize set height {}'.format(height),
        'move position center'
    ])

def disable_zen_mode(workspace):
    return ';'.join([
        'move container to workspace number {}'.format(workspace['num']),
        'workspace number {}'.format(workspace['num']),
        'floating disable',
        'border {}'.format(DEFAULT_BORDER)
    ])

def goto_zen(workspace_name):
    return 'workspace {}'.format(workspace_name)

out = subprocess.run(['i3-msg', '-t', 'get_workspaces'], capture_output=True)
workspaces = json.loads(out.stdout)

with open(ZEN_FILE_PATH, 'r') as zen_file:
    try:
        workspace_previous = json.load(zen_file)
    except:
        workspace_previous = None
workspace_current = list(filter(lambda w: w['focused'], workspaces))[0]
workspace_zen = list(filter(lambda w: w['num'] == ZEN_NUMBER, workspaces))

if __name__ == '__main__':
    if len(sys.argv) > 1:
        if len(workspace_zen):
            msg = disable_zen_mode(workspace_previous)
    else:
        if len(workspace_zen):
            msg = goto_zen(workspace_zen[0]['name'])
        else:
            msg = enable_zen_mode(workspace_current)
    print(msg)
    subprocess.run(['i3-msg', msg])

