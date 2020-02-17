#!/usr/bin/env python3

import argparse
import sys
import json
import subprocess
import os

ZEN_NUMBER = 99
ZEN_NAME = 'zen'
ZEN_WORKSPACE = '{}: {}'.format(ZEN_NUMBER, ZEN_NAME)

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
    with open(ZEN_FILE_PATH, 'w') as zen_file:
        json.dump(workspace, zen_file)
    return ';'.join([
        'move container to workspace {}'.format(ZEN_WORKSPACE),
        'workspace {}'.format(ZEN_WORKSPACE),
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

def goto_zen():
    return 'workspace {}'.format(ZEN_WORKSPACE)

def switch_workspace(args):
    msg = goto_zen()
    subprocess.run(['i3-msg', msg])

def toggle(args):
    cw, pw, zw = get_workspaces()
    if zw:
        msg = disable_zen_mode(pw)
    else:
        msg = enable_zen_mode(cw)
    subprocess.run(['i3-msg', msg])

def get_workspaces():
    out = subprocess.run(['i3-msg', '-t', 'get_workspaces'], capture_output=True)
    workspaces = json.loads(out.stdout)

    try:
        with open(ZEN_FILE_PATH, 'r') as zen_file:
            workspace_previous = json.load(zen_file)
    except FileNotFoundError:
        workspace_previous = {'num': 1}
    workspace_current = list(filter(lambda w: w['focused'], workspaces))[0]
    workspace_zen = list(filter(lambda w: w['num'] == ZEN_NUMBER, workspaces))
    return workspace_current, workspace_previous, workspace_zen


parser = argparse.ArgumentParser(description='Control i3-quiet.')
parser.set_defaults(func=lambda args: parser.print_help())
subparsers = parser.add_subparsers(title='subcommands',
                                   description='valid subcommands',
                                   help='additional help')
parser_toggle = subparsers.add_parser('toggle')
parser_toggle.set_defaults(func=toggle)
parser_switch = subparsers.add_parser('switch')
parser_switch.set_defaults(func=switch_workspace)
args = parser.parse_args()

args.func(args)
