from flask import Flask, render_template, request, redirect
from chess import Board, WebInterface
from movehistory import MoveHistory


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
        return render_template('game.html', ui=ui)

    @app.route('/error', methods=['POST', 'GET'])
    def error():
        ui.errmsg = f'Invalid move for {board.turn} player:'
        ui.next_link = '/validation'
        return render_template('game.html', ui=ui)

    @app.route('/promote', methods=['POST', 'GET'])
    def promote():
        ui.inputlabel = "Which piece do you want to promote?"
        ui.btnlabel = 'Promote'
        ui.next_link = '/validation'
        return render_template('game.html', ui=ui)

    @app.route('/validation', methods=['POST', 'GET'])
    def validation():
        move = request.form['move']
        ui.errmsg = None
        status = board.prompt(move, ui)
        if status == 'error':
            return redirect('/error')
        else:

            start, end = status
            if board.movetype(start, end) == 'promotion':
                return redirect('/promotion')
            board.update(start, end)
            opponent_colour = 'black' if board.turn == 'white' else 'white'
            if board.checkmate_checking(opponent_colour):
                ui.winner=board.turn
                return redirect('/winner')

            if board.movetype(start,end) == 'promotion':
                return redirect('/promotion')

            move = (start,end)
            board.update(start, end)
            print(f'move in validation:{move}')
            history.push(move)
            return redirect('/play')

    @app.route('/winner')
    def winner():
        return render_template('winner.html',ui=ui)

            
    @app.route('/undo',methods=['POST','GET'])
    def undo():
        move = history.pop()
        if move == None:
            ui.errmsg = 'No more undo move'
            board.next_turn()
            return redirect('/play')
        else:    
            board.undo(move)
        return redirect('/play')

    app.run('0.0.0.0', debug=False)
    # app.run(debug=True)


main()
