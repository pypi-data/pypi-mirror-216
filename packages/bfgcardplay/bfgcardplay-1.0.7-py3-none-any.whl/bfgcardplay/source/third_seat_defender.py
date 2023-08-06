"""Third seat card play for defender."""

from typing import Union
from termcolor import cprint

import inspect
from ..logger import log

from bridgeobjects import SUITS, Card, CARD_VALUES, Suit
from bfgdealer import Trick
from .player import Player
from .utilities import other_suit_for_signals, get_suit_strength
from .third_seat import ThirdSeat
from .defender_play import deduce_partner_void_in_trumps, get_hilo_signal_card
import bfgcardplay.source.global_variables as global_vars

MODULE_COLOUR = 'blue'

MAXIMUM_TRICKS = 13
TRUMP_VALUE_UPLIFT = 13


class ThirdSeatDefender(ThirdSeat):
    def __init__(self, player: Player):
        super().__init__(player)

    def selected_card(self) -> Card:
        """Return the card if the third seat."""
        player = self.player
        manager = global_vars.manager
        trick = player.board.tricks[-1]


        cards = player.cards_for_trick_suit(trick)

        # Void
        if not cards:
            return self._select_card_if_void(player, trick)

        # Singleton
        if len(cards) == 1:
            return log(inspect.stack(), cards[0])

        self._update_manager()

        # win trick if possible
        card = self._winning_card()
        if card:
            return card

        # Play high
        card = self._play_high_card(cards, trick)
        if card:
            return card

        # Unblock suit
        card = self._unblock_suit(cards, trick)
        if card:
            return card

        # Play highest honour if winner
        card = self._play_winning_honour(trick)
        if card:
            return card

        # Play winner if possible
        if (not player.is_winner_defender(trick.cards[0], trick) and
                not trick.cards[0].is_honour and
                cards[0].value > trick.cards[1].value):
            return log(inspect.stack(), cards[0])

        # Doubleton - play the higher
        card = self._top_of_doubleton(cards, trick)
        if card:
            return card

        # signal attitude
        return self._signal_attitude(cards, trick)

    def _update_manager(self):
        player = self.player
        trick = player.board.tricks[-1]
        manager = global_vars.manager

        if len(player.board.tricks) == 1:
            manager.signal_card[player.partner_seat] = trick.cards[0]

        if player.trump_suit and trick.suit == player.trump_suit:
            if deduce_partner_void_in_trumps(player):
                manager.voids[player.partner_seat][player.trump_suit.name] = True

        suit_name = trick.suit.name
        if player.trick_number == 1:
            if trick.cards[0].is_honour:
                manager.set_like_dislike(player.partner_seat, suit_name, True)

    def _play_high_card(self, cards, trick) -> Card:
        player = self.player
        (value_0, value_1) = self._trick_card_values(trick, player.trump_suit)
        if value_1 > value_0:
            for card in cards[::-1]:
                if card.value > value_1:
                    return log(inspect.stack(), card)
        return None

    def _unblock_suit(self, cards, trick) -> Card:
        player = self.player
        if player.trick_number == 1:
            if trick.cards[0].is_honour and len(cards) <= 2:
                return log(inspect.stack(), cards[0])
        if player.trick_number == 2:
            if player.board.tricks[0] == trick.suit:
                if player.board.tricks[0].cards[0].is_honour and len(cards) <= 2:
                    return log(inspect.stack(), cards[0])
        if len(cards) == 2:
            leading_card = trick.cards[0]
            if leading_card.value < cards[0].value:
                return log(inspect.stack(), cards[0])
        return None

    def _play_winning_honour(self, trick) -> Card:
        player = self.player
        # TODO is this too specific?
        suit = trick.suit
        jack = Card('J', suit.name)
        queen = Card('Q', suit.name)
        king = Card('K', suit.name)
        ace = Card('A', suit.name)
        if (trick.cards[0] == jack and
                ace in player.dummys_unplayed_cards[suit.name] and
                player.dummy_on_right and
                king in player.unplayed_cards[suit.name] and
                queen not in player.unplayed_cards[suit.name]):
            return log(inspect.stack(), king)
        return None

    def _top_of_doubleton(self, cards, trick) -> Card:
        player = self.player
        manager = global_vars.manager
        suit_name = trick.suit.name
        if len(cards) == 2 and cards[0].value < CARD_VALUES['K']:
            manager.set_like_dislike(player.seat, suit_name, 1)
            return log(inspect.stack(), cards[0])
        return None

    def _signal_attitude(self, cards, trick) -> Card:
        player = self.player
        manager = global_vars.manager
        suit_name = trick.suit.name
        if not manager.like_dislike(player.seat, suit_name) or not player.suit_rounds[suit_name]:
            if cards[0].is_honour:
                for card in cards[1:]:
                    if not card.is_honour:
                        if card.value >= CARD_VALUES['7']:
                            manager.set_like_dislike(player.seat, card.suit.name, 1)
                        return log(inspect.stack(), card)
                manager.set_like_dislike(player.seat, cards[-1].suit.name, 0)
        return get_hilo_signal_card(player, cards)

    def _winning_card(self) -> Union[Card, None]:
        """Return the card if can win trick."""
        player = self.player
        trick = player.board.tricks[-1]
        cards = player.cards_for_trick_suit(trick)

        # No cards in trick suit, look for trump winner
        card = self._trump_if_void(cards, trick)
        if card:
            return card

        # Defeat contract if possible
        card = self._defeat_contract(cards, trick)
        if card:
            return card

        # Play winner if long suit
        card = self._winner_in_long_suit(cards, trick)
        if card:
            return card

        # Look for winner
        card = self._look_for_winner(trick)
        if card:
            return card

        card = self._select_card_based_on_position(cards, trick)
        if card:
            return card

        return None

    def _trump_if_void(self, cards, trick) -> Card:
        if cards:
            return None
        player = self.player
        (value_0, value_1) = self._trick_card_values(trick, player.trump_suit)
        if player.trump and player.trump_cards:
            for card in player.trump_cards[::-1]:
                if card.value + TRUMP_VALUE_UPLIFT > value_0 + 1 and card.value + TRUMP_VALUE_UPLIFT > value_1:
                    return log(inspect.stack(), card)
        return None

    def _defeat_contract(self, cards, trick) -> Card:
        player = self.player
        if (player.is_winner_defender(cards[0], trick) and
                not player.is_winner_defender(trick.cards[0], trick) and
                player.defenders_tricks >= MAXIMUM_TRICKS - player.declarers_target):
            return log(inspect.stack(), cards[0])
        return None

    def _winner_in_long_suit(self, cards, trick) -> Card:
        player = self.player
        if len(cards) >= 5:
            for card in cards[::-1]:
                if player.is_winner_defender(card, trick):
                    return log(inspect.stack(), card)
        return None

    def _look_for_winner(self, trick) -> Card:
        player = self.player
        if not player.is_winner_defender(trick.cards[0], trick):
            top_touching_honour = player.touching_honours_in_hand(player.hand, trick.suit.name)
            if top_touching_honour and top_touching_honour.value > trick.cards[1].value:
                return log(inspect.stack(), top_touching_honour)
        return None

    def _select_card_based_on_position(self, cards, trick) -> Card:
        short_cards = [card for card in cards[:-1]]
        for index, test_card in enumerate(short_cards[::-1]):
            # If dummy on left and can win, do so
            card = self._dummy_on_left(test_card, trick)
            if card:
                return card

            card = self._dummy_tenace_not_dominated(cards, trick, test_card, index)
            if card:
                return card
        return None

    def _get_card_value(self, card) -> int:
        card_value = card.value
        # trick card values already adjusted for trumps
        if card.suit == self.player.trump_suit:
            card_value += TRUMP_VALUE_UPLIFT
        return card_value

    def _dummy_on_left(self, card, trick) -> Card:
        player = self.player
        if not player.dummy_on_left:
            return None

        (value_0, value_1) = self._trick_card_values(trick, player.trump_suit)
        if player.dummys_unplayed_cards[trick.suit.name]:
            if value_1 > value_0:
                card_value = self._get_card_value(card)
                if card_value > player.dummys_unplayed_cards[trick.suit.name][0].value:
                    return log(inspect.stack(), card)
        return None

    def _dummy_tenace_not_dominated(self, cards, trick, card, index) -> Card:
        player = self.player
        card_value = self._get_card_value(card)
        (value_0, value_1) = self._trick_card_values(trick, player.trump_suit)
        if (card_value > value_0 + 3 and
                card_value > value_1 and
                card.value != cards[index+1].value + 1):
            if (not self._seat_dominates_left_hand_dummy_tenace(card) and
                    not self._ace_is_deprecated(trick, card)):
                return log(inspect.stack(), card)
        return None

    def _seat_dominates_left_hand_dummy_tenace(self, card: Card) -> bool:
        """Return True if hand dominated dummies tenace in that suit."""
        if self.player.dummy_on_left:
            return False
        tenace = self.player.dummy_suit_tenaces[card.suit.name]
        if tenace:
            if card.value > tenace.value:
                return True
        return False

    def _select_card_if_void(self, player: Player, trick: Trick) -> Card:
        """Return card if cannot follow suit."""
        player.record_void(trick.suit)
        # Trump if appropriate
        if player.trump_suit:
            (value_0, value_1) = self._trick_card_values(trick, player.trump_suit)
            if player.trump_cards:
                unplayed_cards = player.total_unplayed_cards[trick.suit.name]
                if unplayed_cards:
                    if (value_1 > value_0 or
                            trick.cards[0].value < unplayed_cards[0].value):
                        return log(inspect.stack(), player.trump_cards[-1])

        # Signal suit preference first time it is led."""
        signal_card = self._signal_on_first_lead(player, trick)
        if signal_card:
            return signal_card

        best_suit = self._best_suit(player)
        other_suit = other_suit_for_signals(best_suit)
        if other_suit != player.trump_suit:
            other_suit_cards = player.suit_cards[other_suit]
            if other_suit_cards and not other_suit_cards[-1].is_honour:
                return log(inspect.stack(), other_suit_cards[-1])

        long_suit_cards = {}
        selected_card = None
        for suit in SUITS:
            cards = player.suit_cards[suit]
            long_suit_cards[suit] = len(cards)
            if player.trump_suit and suit != player.trump_suit.name:
                if cards and not cards[-1].is_honour:
                    selected_card = cards[-1]
        if selected_card:
            return log(inspect.stack(), selected_card)

        for suit_name in SUITS:
            cards = player.unplayed_cards[suit]
            dummys_cards = player.dummys_unplayed_cards[suit]
            if len(cards) > len(dummys_cards):
                return log(inspect.stack(), cards[-1])

            # if suit_name != best_suit.name and suit_name != other_suit:
            #     final_suit_cards = player.suit_cards[suit_name]
            #     if final_suit_cards:
            #         return log(inspect.stack(), final_suit_cards[-1])

        # print(f'{player.suit_cards[suit][0]=}')
        max_length = 0
        for suit in SUITS:
            if long_suit_cards[suit] > max_length:
                max_length = long_suit_cards[suit]
                long_suit = suit
        return log(inspect.stack(), player.suit_cards[long_suit][-1])

    def _signal_on_first_lead(self, player: Player, trick: Trick) -> Union[Card, None]:
        """Return a card if it is first time that partner led it."""
        suits_already_signed = []
        if player.trump_suit:
            suits_already_signed.append(player.trump_suit)
        for board_trick in player.board.tricks:
            if board_trick.leader == player.partner_seat and board_trick != trick:
                suits_already_signed.append(board_trick.start_suit)

        if trick.start_suit not in suits_already_signed:
            suit = self._best_suit(player)
            suit_cards = player.suit_cards[suit.name]
            for card in suit_cards:
                if not card.is_honour:
                    return log(inspect.stack(), card)
        return None

    def _best_suit(self, player: Player) -> Suit:
        """Select suit for signal."""
        # TODO handle no points and equal suits
        cards = player.hand_cards.list
        suit_points = get_suit_strength(cards)
        max_points = 0
        best_suit = None
        for suit in SUITS:
            if player.trump_suit and suit == player.trump_suit.name:
                continue
            hcp = suit_points[suit]
            if hcp > max_points:
                max_points = hcp
                best_suit = suit
        if not best_suit:
            return player.longest_suit
        return Suit(best_suit)
