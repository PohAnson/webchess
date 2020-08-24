from flask import Flask, render_template, request, redirect
from chess import Board, WebInterface
from movehistory import MoveHistory
import time
import re

def main():
    app = Flask(__name__)
    ui = WebInterface()
    board = Board()
    board.start()
    history = MoveHistory(10)

    @app.route('/')
    def root():
        ui.next_link = '/newgame'
        return render_template('homepage.html', ui=ui)

    @app.route('/newgame', methods=['GET', 'POST'])
    def newgame():
        ui.wname, ui.bname = request.form['wname'], request.form['bname']
        board.turn = 'black'
        ui.errmsg = ''
        return redirect('/play')

    @app.route('/play', methods=['POST', 'GET'])
    def play():
        ui.board = board.display()
        board.next_turn()
        if ui.errmsg == None:
            ui.errmsg = ''
        if board.turn == 'white':
            ui.inputlabel = f'{ui.wname}\'s turn:'
        else:
            ui.inputlabel = f'{ui.bname}\'s turn:'
        ui.next_link = '/validation'
        return render_template('game.html', ui=ui, variables=None)

    @app.route('/error', methods=['POST', 'GET'])
    def error():
        player = ui.wname if board.turn == "white" else ui.bname
        ui.board = board.display()
        ui.errmsg = f'Invalid move for {player}'
        ui.next_link = '/validation'
        return render_template('game.html', ui=ui, variables=None)

    @app.route('/promotion', methods=['POST', 'GET'])
    def promotion():
        print("promotion page")
            # /promote path must always have coord in GET parameter so that
        # board knows where the pawn to be promoted is
        # Process pawn promotion
        # Player will be prompted for another input if invalid
        if request.method == 'POST':
            print('USING POST')
            char = request.form['move'].lower()
            pattern = r"\(\d, \d\)"
            temp = request.form['variables']
            start, end = re.findall(pattern, temp)
            print(start, end)

            if char in 'rkbq':
                board.promote_pawn(coord,
                                char,
                                push_to=history.this_move(),
                                )
                return redirect('/play')
            else:
                print('WRONG LETTER')
                ui.errmsg = 'Invalid input (r, k, b, or q only). Please try again.'
                print(start,end)
                return redirect(f'/promotion?start={start}&end={end}')

        elif request.method == 'GET':
            start, end = request.args['start'], request.args['end']
            print('start', start, '\tend', end)
            print('USING', request.method)
            ui.board = board.display()
            ui.inputlabel = f'Promote pawn at {end} to (r, k, b, q): '
            ui.btnlabel = 'Promote'
            ui.next_link = '/promotion'
            return render_template('game.html', ui=ui, variables=(start, end))

    @app.route('/validation', methods=['POST', 'GET'])
    def validation():
        move = request.form['move']
        ui.errmsg = ''
        status = board.prompt(move, ui)
        if status == 'error':
            return redirect('/error')
        else:
            start, end = status
            if board.movetype(start, end) == 'promotion':
                board.update(start, end)
                return redirect(f'/promotion?start={start}&end={end}')
            else:
                board.update(start, end)
                opponent_colour = 'black' if board.turn == 'white' else 'white'
                if board.checkmate_checking(opponent_colour):
                    ui.winner=board.turn
                    return redirect('/winner')

            move = (start,end)
            history.push(move)
            print(history)
            return redirect('/play')

    @app.route('/winner')
    def winner():
        ui.winner = ui.wname if board.turn == "white" else ui.bname
        return render_template('winner.html',ui=ui, variables=None)

            
    @app.route('/undo',methods=['POST','GET'])
    def undo():
        move = history.pop()
        if move == None:
            ui.errmsg = 'No more undo move'
            board.next_turn()
            return redirect('/play')
        else:    
            board.undo(move)
        ui.errmsg = ''
        return redirect('/play')

    app.run('0.0.0.0', debug=True)
    # app.run(debug=True)


main()
