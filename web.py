from flask import Flask, render_template, request, redirect
from chess import Board, WebInterface


def main():
    app = Flask(__name__)
    ui = WebInterface()
    board = Board()
    board.start()

    @app.route('/')
    def root():
        return render_template('homepage.html')

    @app.route('/play', methods=['POST', 'GET'])
    def play():
        ui.wname, ui.bname = request.form['wname'], request.form['bname']
        ui.board = board.display()
        ui.errmsg = ''
        board.next_turn()
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
            return redirect('/play')

    app.run('0.0.0.0', debug=False)
    # app.run(debug=True)


main()
