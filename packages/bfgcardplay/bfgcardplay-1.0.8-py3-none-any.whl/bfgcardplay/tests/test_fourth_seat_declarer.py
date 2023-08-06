from pathlib import Path
from bridgeobjects import load_pbn

from .. import next_card
from ..tests.utilities import get_board

BOARD_PATH = Path('tests', 'test_data', 'fourth_seat_declarer.pbn')

boards = load_pbn(BOARD_PATH)[0].boards


def test_play_partners_suit():
    """Ensure not a S in _select_card_if_void, entry to partner's hand
        for suit in SUITS:."""
    board = get_board(boards, 0)
    assert next_card(board).suit.name != 'S'
