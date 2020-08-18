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

    @app.route('/newgame')
    def newgame():
        ui.players = {'white': request.args['wname'], 'black': request.args['bname']}
        return redirect('/play')

    @app.route('/play')
    def play():
        # TODO: if there is no player move, render the page template
        ui.board = board.display()
        ui.next_link = '/validation'
        return render_template('game.html', ui=ui)

    @app.route('/error')
    def error():
        ui.errmsg = 'ERROR VARIABLE'
        return render_template('game.html', ui=ui)

    @app.route('/promote')
    def promote():
        ui.inputlabel = "Which piece do you want to promote?"
        ui.btnlabel = 'promote'
        ui.next_link = '/validation'
        return render_template('game.html', ui=ui)

    @app.route('/validation')
    def validation():
        move = request.args['move']
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