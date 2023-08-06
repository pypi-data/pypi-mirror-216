"""Expose the classes in the API."""
from ._version import __version__

from .src.hand import Hand
from .src.comments import comments, strategies, comment_xrefs, convert_text_to_html
from .src.strategy_xref import StrategyXref, strategy_descriptions
from .src.bidding import Bid, Pass, Double
from .src.player import Player

VERSION = __version__