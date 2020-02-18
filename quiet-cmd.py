#!/usr/bin/env python3

import argparse
import sys
import json
from subprocess import run, check_output
import os

ZEN_NUMBER = 99
ZEN_NAME = 'zen'
ZEN_WORKSPACE = '{}: {}'.format(ZEN_NUMBER, ZEN_NAME)

WIDTH_PERC=50
MAX_WIDTH=800
HEIGHT_PERC=90
MAX_HEIGHT=1024
SIZES = {
    'small': [50, 70, 800, 800],
    'medium': [65, 80, 1024, 1024],
    'large': [90, 90, 1600, 1600],
}
DEFAULT_SIZE = 'medium'
ZEN_BORDER = 'none'
DEFAULT_BORDER = 'normal'
ZEN_FILE_PATH = os.path.join(os.environ['HOME'], '.config/i3/.i3-quiet.json')


def enable_zen_mode(workspace):
    wp, hp, wm, hm = SIZES[DEFAULT_SIZE]
    width = round(min(workspace['rect']['width'] * wp / 100, wm))
    height = round(min(workspace['rect']['height'] * hp / 100, hm))
    msg = ';'.join([
        'move container to workspace {}'.format(ZEN_WORKSPACE),
        'workspace {}'.format(ZEN_WORKSPACE),
        'floating enable',
        'resize set width {}'.format(width),
        'resize set height {}'.format(height),
        'move position center'
    ])
    run(['i3-msg', msg])
    layout = check_output(['i3-save-tree', '--workspace', ZEN_WORKSPACE])
    msg = ';'.join([
        'border {}'.format(ZEN_BORDER)
    ])
    run(['i3-msg', msg])
    layout = layout.decode()
    layout = layout.split('\n')
    layout = filter(lambda l: not l.strip().startswith('//'), layout)
    layout = json.loads(''.join(layout))

    with open(ZEN_FILE_PATH, 'w') as zen_file:
        json.dump({'workspace': workspace, 'layout': layout}, zen_file)

def disable_zen_mode(workspace):
    try:
        with open(ZEN_FILE_PATH, 'r') as zen_file:
            border = json.load(zen_file)['layout']['border']
    except (FileNotFoundError, KeyError):
        border = DEFAULT_BORDER

    msg = ';'.join([
        'move container to workspace number {}'.format(workspace['num']),
        'workspace number {}'.format(workspace['num']),
        'floating disable',
        'border {}'.format(border)
    ])
    run(['i3-msg', msg])

def resize(args):
    cw, _, _= get_workspaces()
    workspace_width = cw['rect']['width']
    workspace_height = cw['rect']['height']
    wp, hp, wm, hm = SIZES[args.size]
    width = round(min(workspace_width * wp / 100, wm))
    height = round(min(workspace_height * hp / 100, hm))
    msg = ';'.join([
        'resize set width {}'.format(width),
        'resize set height {}'.format(height),
        'move position center'
    ])
    run(['i3-msg', msg])

def goto_zen():
    msg = 'workspace {}'.format(ZEN_WORKSPACE)
    run(['i3-msg', msg])

def switch_workspace(args):
    goto_zen()

def toggle(args):
    cw, pw, zw = get_workspaces()
    if zw:
        disable_zen_mode(pw)
    else:
        enable_zen_mode(cw)

def get_workspaces():
    out = run(['i3-msg', '-t', 'get_workspaces'], capture_output=True)
    workspaces = json.loads(out.stdout)

    try:
        with open(ZEN_FILE_PATH, 'r') as zen_file:
            workspace_previous = json.load(zen_file)['workspace']
    except (FileNotFoundError, KeyError):
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
parser_resize = subparsers.add_parser('resize')
parser_resize.add_argument('size', type=str,
        help='Size of the window specified as "small", "medium", or "large"')
parser_resize.set_defaults(func=resize)
args = parser.parse_args()

args.func(args)
