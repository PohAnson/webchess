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

    @app.route('/newgame',methods = ['POST'])
    def newgame():
        ui.wname , ui.bname = request.form['wname'], request.form['bname']
        ui.board = board.display()
        ui.inputlabel = f'{board.turn} player: '
        ui.btnlabel = 'Move'
        return render_template('game.html', ui=ui)


    @app.route('/play',methods = ['POST'])
    def play():
        inputstr = request.form['move']
        start,end = board.prompt(inputstr)
        board.update(start,end)
        ui.board = board.display()
        board.next_turn()
        ui.inputlabel = f'{board.turn} player:'
        ui.next_link = '/validation'
        return render_template('game.html', ui=ui)

    @app.route('/error',methods = ['POST'])
    def error():
        #ui.errmsg = 'ERROR VARIABLE'
        ui.errmsg = f'Invalid move for {board.turn} player:'
        ui.next_link = '/play'
        return render_template('game.html', ui=ui)

    @app.route('/promote',methods = ['POST'])
    def promote():
        ui.inputlabel = "Which piece do you want to promote?"
        ui.btnlabel = 'promote'
        ui.next_link = '/validation'
        return render_template('game.html', ui=ui)

    @app.route('/validation',methods = ['POST'])
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

    app.run('0.0.0.0', debug=False)
    #app.run(debug=True)

main()