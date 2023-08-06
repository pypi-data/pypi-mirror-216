"""BfG Cardplay utilities."""

from typing import List, Dict

from bridgeobjects import Suit, SUITS, Card


def get_list_of_best_scores(candidates: Dict[object, int], reverse: bool = False) -> List[object]:
    """Return a list of the best scoring candidates from a dict of candidates."""
    best_candidates = []
    max_score = 0
    min_score = 0
    for key, score in candidates.items():
        if score > max_score:
            max_score = score

    if reverse:
        min_score = max_score
        for key, score in candidates.items():
            if score < min_score:
                min_score = score

    for key, score in candidates.items():
        if reverse:
            if score == min_score:
                best_candidates.append(key)
        else:
            if score == max_score:
                best_candidates.append(key)
    return best_candidates


def other_suit_for_signals(suit: Suit) -> str:
    """Return the other suit for signalling."""
    if suit.name == 'S':
        other_suit = 'C'
    elif suit.name == 'C':
        other_suit = 'S'
    elif suit.name == 'H':
        other_suit = 'D'
    elif suit.name == 'D':
        other_suit = 'H'
    return other_suit


def get_suit_strength(cards: List[Card]) -> Dict[str, int]:
    """Return a dict of suit high card points keyed on suit name."""
    suit_points = {suit: 0 for suit in SUITS}
    for card in cards:
        suit_points[card.suit.name] += card.high_card_points
    return suit_points