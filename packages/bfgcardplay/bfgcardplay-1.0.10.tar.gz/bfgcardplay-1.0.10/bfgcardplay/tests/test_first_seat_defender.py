from pathlib import Path
from bridgeobjects import load_pbn

from .. import next_card
from ..tests.utilities import get_board

BOARD_PATH = Path('tests', 'test_data', 'first_seat_defender.pbn')

boards = load_pbn(BOARD_PATH)[0].boards


def test_play_partners_suit():
    """Return partner's suit in _select_suit_for_nt_contract."""
    board = get_board(boards, 0)
    assert next_card(board).name == '8H'


def test_play_winners():
    """Play winners in _select_card_from_suit."""
    board = get_board(boards, 1)
    assert next_card(board).name == '9H'
