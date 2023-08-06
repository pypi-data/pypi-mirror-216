"""
    Comment and Strategy cross references.
"""

import sysconfig
from pathlib import Path
import json
from termcolor import cprint

VIRTUAL_ENV_DIR = sysconfig.get_path('purelib')
PACKAGE = 'bfgbidding'
COMMENT_DATA_DIRECTORY = 'comment_data'
DATA_PATH = Path(VIRTUAL_ENV_DIR, PACKAGE, COMMENT_DATA_DIRECTORY)

COMMENT_XREF_FILE = 'comment_xref.json'
STRATEGY_XREF_FILE = 'strategy_xref.json'
COMMENTS_FILE_NAME = 'comments.json'
STRATEGIES_FILE_NAME = 'strategies.json'

def _read_json(path):
    try:
        with open(path, 'r') as f_json:
            return json.load(f_json)
    except FileNotFoundError:
        cprint(f'Missing json file', 'red')
        cprint(f'{path}', 'red')

comment_xrefs = _read_json(Path(DATA_PATH, COMMENT_XREF_FILE))
strategy_xrefs = _read_json(Path(DATA_PATH, STRATEGY_XREF_FILE))
comments = _read_json(Path(DATA_PATH, COMMENTS_FILE_NAME))
strategies = _read_json(Path(DATA_PATH, STRATEGIES_FILE_NAME))

def comment_id(call_id):
    """Return the comment_id associated with the call_id."""
    return comment_xrefs[call_id]

def comment_html(call_id):
    """Return the comment associated with the call_id."""
    comment_id = comment_xrefs[call_id]
    comment = convert_text_to_html(comments[comment_id])
    return comment

def strategy_html(call_id):
    """Return the strategy associated with the call_id."""
    comment_id = comment_xrefs[call_id]
    if not comment_id in strategy_xrefs:
        cprint(f'---> no strategy_xref record for {comment_id}!', 'red')
    strategy_id = strategy_xrefs[comment_id]
    strategy = convert_text_to_html(strategies[strategy_id])
    return strategy

def _tag(colour, end_tag=False):
    """Return a html tag of the colour."""
    slash = ''
    if end_tag:
        slash = '/'
    return f'<{slash}{colour}>'

def convert_text_to_html(text):
    """Convert proprietary text to html."""
    html = text
    for colour in ['red', 'blue', 'green', 'yellow']:
        if _tag(colour) in text:
            new_text = '<span style="color:%s">' % colour
            html = html.replace(_tag(colour), new_text)
        if _tag(colour, True) in text:
            html = html.replace(_tag(colour, True), '</span>')
    return html
