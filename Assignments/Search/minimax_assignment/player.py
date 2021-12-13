#!/usr/bin/env python3
import random
import math

from fishing_game_core.game_tree import Node
from fishing_game_core.player_utils import PlayerController
from fishing_game_core.shared import ACTION_TO_STR


class PlayerControllerHuman(PlayerController):
    def player_loop(self):
        """
        Function that generates the loop of the game. In each iteration
        the human plays through the keyboard and send
        this to the game through the sender. Then it receives an
        update of the game through receiver, with this it computes the
        next movement.
        :return:
        """

        while True:
            # send message to game that you are ready
            msg = self.receiver()
            if msg["game_over"]:
                return


class PlayerControllerMinimax(PlayerController):

    def __init__(self):
        super(PlayerControllerMinimax, self).__init__()

    def player_loop(self):
        """
        Main loop for the minimax next move search.
        :return:
        """

        # Generate first message (Do not remove this line!)
        first_msg = self.receiver()

        while True:
            msg = self.receiver()

            # Create the root node of the game tree
            node = Node(message=msg, player=0)

            # Possible next moves: "stay", "left", "right", "up", "down"
            best_move = self.search_best_next_move(initial_tree_node=node)

            # Execute next action
            self.sender({"action": best_move, "search_time": None})

    def search_best_next_move(self, initial_tree_node):
        """
        Use minimax (and extensions) to find best possible next move for player 0 (green boat)
        :param initial_tree_node: Initial game tree node
        :type initial_tree_node: game_tree.Node
            (see the Node class in game_tree.py for more information!)
        :return: either "stay", "left", "right", "up" or "down"
        :rtype: str
        """

        # EDIT THIS METHOD TO RETURN BEST NEXT POSSIBLE MODE USING MINIMAX ###

        # NOTE: Don't forget to initialize the children of the current node
        #       with its compute_and_get_children() method!

        # if initial_tree_node.depth == 2 or len(initial_tree_node.state.fish_positions) == 0:

        children = initial_tree_node.compute_and_get_children()
        best_score = -math.inf
        best_move = 0
        for child in children:
            new_score = self.minimax(child, math.inf, -math.inf)
            if(new_score > best_score):
                best_score = new_score
                best_move = child.move
        return ACTION_TO_STR[best_move]

    # TODO: Implement alpha-beta-pruning to enable deeper levels
    # minimax returns a heuristic approximation of best possible move
    def minimax(self, node, beta, alpha):
        state = node.state
        # terminal state
        if node.depth == 2 or len(state.fish_positions) == 0:
            return self.heuristic(state)
        # min plays
        if state.player:
            minEval = math.inf
            children = node.compute_and_get_children()
            for child in children:
                eval = self.minimax(child, beta, alpha)
                minEval = min(eval, minEval)
                beta = min(minEval, beta)
                if beta <= alpha:
                    break
            return minEval
        # max plays
        else:
            maxEval = -math.inf
            children = node.compute_and_get_children()
            for child in children:
                eval = self.minimax(child, beta, alpha)
                maxEval = max(eval, maxEval)
                alpha = max(maxEval, alpha)
                if beta <= alpha:
                    break
            return maxEval
    
    def heuristic(self, state):
        max_score = state.player_scores[0]
        min_score = state.player_scores[1]
        heuristic = max_score - min_score
        # min
        if state.player:
            heuristic = heuristic + self.closest_fish(state.player, state)
        # max
        else:
            heuristic = heuristic - self.closest_fish(state.player, state)
        return heuristic
    
    def closest_fish(self, player, state):
        hook_position = state.hook_positions[player]
        min_distance = math.inf
        for fish_position in state.fish_positions.values():
            min_distance = min(min_distance, self.get_distance(fish_position, hook_position))
        return min_distance


    
    def get_distance(self, fish_position, hook_position):
        distance = math.sqrt((fish_position[0]-hook_position[0])**2 + (fish_position[1]-hook_position[1])**2)
        return distance





