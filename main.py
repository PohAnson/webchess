from chess import Board, King, Queen, Bishop, Knight, Rook, Pawn

if input('Do you want to auto test for checkmate? (y/n)? ').strip().lower() == 'y':
  import auto_test
  auto_test.main()
else:
    import web
    web.main()