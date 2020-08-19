from flask import Flask, render_template, request, redirect
from chess import Board, WebInterface


def main():
    app = Flask(__name__)
    ui = WebInterface()
    board = Board()
    board.start()

    @app.route('/')
    def root():
        ui.next_link = "/newgame"
        return render_template('homepage.html')

    @app.route('/newgame', methods=['GET', 'POST'])
    def newgame():
        ui.wname, ui.bname = request.form['wname'], request.form['bname']
        board.turn = 'black'
        return redirect('/play')

    @app.route('/play', methods=['GET', 'POST'])
    def play():
        ui.board = board.display()
        ui.errmsg = ''
        board.next_turn()
        ui.inputlabel = f'{board.turn} player:'
        ui.next_link = '/validation'
        return render_template('game.html', ui=ui)

    @app.route('/error', methods=['GET', 'POST'])
    def error():
        ui.errmsg = f'Invalid move for {board.turn} player:'
        ui.next_link = '/validation'
        return render_template('game.html', ui=ui)

    @app.route('/promote', methods=['GET', 'POST'])
    def promote():
        ui.inputlabel = "Which piece do you want to promote?"
        ui.btnlabel = 'promote'
        ui.next_link = '/validation'
        return render_template('game.html', ui=ui)

    @app.route('/validation', methods=['GET', 'POST'])
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
            return redirect('/play')

    # app.run('0.0.0.0', debug=False)
    app.run(debug=True)


main()
