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

    @app.route('/newgame', methods=['POST'])
    def newgame():
        ui.wname, ui.bname = request.form['wname'], request.form['bname']
        ui.next_link = "/play"
        ui.board = board.display()
        return render_template('game.html', ui=ui)

    @app.route('/play', methods=['POST'])
    def play():
        pass
        return render_template('game.html', ui=ui)

    @app.route('/error', methods=['POST'])
    def error():
        ui.errmsg = 'ERROR VARIABLE'
        return render_template('game.html', ui=ui)

    @app.route('/promote', methods=['POST'])
    def promote():
        ui.inputlabel = "Which piece do you want to promote?"
        ui.btnlabel = 'promote'
        return render_template('game.html', ui=ui)
    # app.run('0.0.0.0', debug=False)
    app.run(debug=True)

    @app.route('/validation')
    def validation():
        # May need to return redirect to the correct page. and edit the ui object
        pass


main()
