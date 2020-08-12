from chess import *

def mini_board():
    game = Board(debug=Flse)
    game.start()
    game.position = {}
    game.add((0,7), King('white'))
    game.add((0,5), King('black'))
    game.add((3,5), Pawn('white'))
    a = Queen
    game.add((6,2), a('black'))
    game.turn = 'black'
    while game.winner is None:
        game.display()
        start, end = game.prompt()
        # print('====Display====')
        # game.display()
        game.update(start, end)
        game.next_turn()
    print(f'Game over. {game.winner} player wins!')

#input to use for testing of mini-board
# mini_board()
#62 35
#07 17
# 35 37


# FULL BOARD

# check not checkmate
move_list1 = [((4, 1), (4, 2)),
((0, 6), (0, 5)),
((5, 0), (2, 3)),
((0, 5), (0, 4)),
((0, 1), (0 ,2)),
((0, 4), (0, 3)),
((2, 3), (5, 6))]

# checkmate
move_list2 = [((4, 1), (4, 2)),
((0, 6), (0, 5)),
((5, 0), (2, 3)),
((0, 5), (0, 4)),
((3, 0), (5, 2)),
((0, 4), (0, 3)),
((2, 3), (5, 6))]
"""
white pawn 41 -> 42
black pawn 06 -> 05
white bishop 50 -> 23
black pawn 05 -> 04
white queen 30 -> 52
black pawn 04 -> 03
white bishop 23 -> 56
"""


game = Board(debug=True)
def auto_mover(move_list, game):
    move_num = 0
    if game.debug:
        game.start()
        while game.winner is None and move_num < len(move_list):
            print('== DISPLAY ==')
            game.display()
            print('== PROMPT ==')
            # start, end = game.prompt()
            start, end = move_list[move_num]
            print('== UPDATE ==')
            game.update(start, end)
            print('== NEXT TURN ==')
            game.next_turn()
            move_num += 1
    else:
        game.start()
        while game.winner is None:
            game.display()
            # start, end = game.prompt()
            start, end = move_list[move_num]
            game.update(start, end)
            game.next_turn()
            move_num += 1
    game.display()
    print(f'Game over. {game.winner} player wins!')
auto_mover(move_list2, game)