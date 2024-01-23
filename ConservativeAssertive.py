

from schnapsen.game import Bot, PlayerPerspective, Move, GameState, GamePhase

class ConservativeAssertive(Bot):
    def get_move(self, perspective: PlayerPerspective, leader_move: Move) -> Move:
        if perspective.get_phase() == GamePhase.ONE:
            if leader_move is None:
                # Leading in the first phase, play conservatively
                return self.play_conservatively_phase_one(perspective)
            else:
                # Following in the first phase, play assertively
                return self.play_assertively_phase_one(perspective, leader_move)
        else:
            # Second phase, play assertively
            return self.play_assertively_phase_two(perspective)

    def play_conservatively_phase_one(self, perspective: PlayerPerspective) -> Move:
        moves = perspective.valid_moves()

        if not moves:
            # No legal moves, return a pass move (in this case, returning None)
            return None

        if perspective.am_i_leader():
            # Leading, play the lowest ranking non-trump card
            moves.sort(key=lambda move: move.cards[0].rank)
            return moves[0]
        else:
            # Following, look for a higher-ranking card of the same suit
            leader_move = perspective.get_game_history()[0][1].leader_move
            same_suit_moves = [move for move in moves if move.cards[0].suit == leader_move.cards[0].suit]

            if same_suit_moves:
                # Play the highest ranking card of the same suit
                same_suit_moves.sort(key=lambda move: move.cards[0].rank, reverse=True)
                return same_suit_moves[0]
            else:
                # No same suit moves available, play the lowest ranking non-trump card
                moves.sort(key=lambda move: move.cards[0].rank)
                return moves[0]

    def play_assertively_phase_one(self, perspective: PlayerPerspective, leader_move: Move) -> Move:
        moves = perspective.valid_moves()

        if not moves:
            # No legal moves, return a pass move (in this case, returning None)
            return None

        # Play the highest value trump card
        trump_moves = [move for move in moves if move.cards[0].suit == perspective.get_trump_suit()]
        if trump_moves:
            trump_moves.sort(key=lambda move: move.cards[0].rank, reverse=True)
            return trump_moves[0]
        else:
            # No trump cards available, play the highest value card
            moves.sort(key=lambda move: move.cards[0].rank, reverse=True)
            return moves[0]

    def play_assertively_phase_two(self, perspective: PlayerPerspective) -> Move:
        moves = perspective.valid_moves()

        if not moves:
            # No legal moves, return a pass move (in this case, returning None)
            return None

        # Check for marriages and trump exchanges first
        for move in moves:
            if move.is_marriage() or move.is_trump_exchange():
                return move

        # Play the highest value trump card
        trump_moves = [move for move in moves if move.cards[0].suit == perspective.get_trump_suit()]
        if trump_moves:
            trump_moves.sort(key=lambda move: move.cards[0].rank, reverse=True)
            return trump_moves[0]
        else:
            # No trump cards available, play the highest value card
            moves.sort(key=lambda move: move.cards[0].rank, reverse=True)
            return moves[0]


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#from typing import Optional
#from schnapsen.game import Bot, PlayerPerspective, Move, GamePhase
#
#class ConservativeAssertive(Bot):
#    """
#    ConservativeAssertive plays differently when leading or following.
#    When leading in the first phase, it chooses the lowest ranking non-trump card.
#    When following in the first phase, it looks for a higher-ranking card of the same suit as the opponent's card.
#    If not found, it plays the lowest ranking non-trump card.
#    In the second phase, it plays the lowest ranking non-trump card when leading or following.
#    """
#    def get_move(self, perspective: PlayerPerspective, leader_move: Optional[Move]) -> Move:
#        moves = perspective.valid_moves()
#
#        if perspective.get_phase() == GamePhase.ONE:
#            # First phase
#            if leader_move is None:
#                # Leading
#                # Play the lowest ranking non-trump card
#                best_move = min(moves, key=lambda move: move.card.rank)
#            else:
#                # Following
#                opponent_card = leader_move.card
#                same_suit_moves = [move for move in moves if move.card.suit == opponent_card.suit]
#
#                if same_suit_moves:
#                    # Play a higher-ranking card of the same suit as the opponent's card
#                    best_move = max(same_suit_moves, key=lambda move: move.card.rank)
#                else:
#                    # No higher-ranking card of the same suit, play the lowest ranking non-trump card
#                    non_trump_moves = [move for move in moves if not perspective.is_trump(move.card)]
#                    best_move = min(non_trump_moves, key=lambda move: move.card.rank)
#        else:
#            # Second phase
#            # Play the lowest ranking non-trump card when leading or following
#            best_move = min(moves, key=lambda move: move.card.rank)
#
#        return best_move
#    