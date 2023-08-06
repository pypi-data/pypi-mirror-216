"""Expose the classes in the API."""

from ._version import __version__
VERSION = __version__

from .src.board import Board, Trick, Contract, Auction
from .src.dealer import Dealer
from .src.dealer_solo import Dealer as DealerSolo
from .src.dealer_duo import Dealer as DealerDuo

SOLO_SET_HANDS = {index: item[0] for index, item in enumerate(DealerSolo().set_hands)}
DUO_SET_HANDS = {index: item[0] for index, item in enumerate(DealerDuo().set_hands)}