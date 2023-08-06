"""Expose the classes in the API."""

from ._version import __version__
VERSION = __version__

from .source.board import Board, Trick, Contract, Auction
from .source.dealer import Dealer
from .source.dealer_solo import Dealer as DealerSolo
from .source.dealer_duo import Dealer as DealerDuo
# from .source.dealer import Dealer
# from .source.dealer_engine import DealerEngine

SOLO_SET_HANDS = {index: item[0] for index, item in enumerate(DealerSolo().set_hands)}
DUO_SET_HANDS = {index: item[0] for index, item in enumerate(DealerDuo().set_hands)}