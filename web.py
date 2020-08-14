from flask import Flask,render_template, request
from chess import *

def main():
    app = Flask(__name__)
    ui = WebInterface()

    @app.route('/')
    def root():
        return render_template('homepage.html')

    @app.route('/newgame', methods=['POST'])
    def newgame():
        wname, bname = request.form['wname'], request.form['bname']
        # players = f"{wname} vs {bname}"
        board = Board()
        return render_template('game.html', ui=ui)

    @app.route('/error', methods=['POST'])
    def error():
        ui.errmsg='ERROR VARIABLE'
        return render_template('game.html', ui=ui)

    @app.route('/promote', methods=['POST'])
    def promote():
        ui.inputlabel="Which piece do you want to promote?"
        ui.btnlabel='promote'
        return render_template('game.html', ui=ui)
    app.run('0.0.0.0', debug=False)