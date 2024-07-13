import math

# Initialize the board
board = [' ' for _ in range(9)]

def print_board(board):
    for row in [board[i*3:(i+1)*3] for i in range(3)]:
        print('| ' + ' | '.join(row) + ' |')

def winner(board, player):
    win_conditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # columns
        [0, 4, 8], [2, 4, 6]              # diagonals
    ]
    return any(all(board[i] == player for i in combo) for combo in win_conditions)

def is_full(board):
    return ' ' not in board

def available_moves(board):
    return [i for i, spot in enumerate(board) if spot == ' ']

def minimax(board, depth, alpha, beta, is_maximizing):
    if winner(board, 'O'):
        return 1
    elif winner(board, 'X'):
        return -1
    elif is_full(board):
        return 0

    if is_maximizing:
        max_eval = -math.inf
        for move in available_moves(board):
            board[move] = 'O'
            eval = minimax(board, depth + 1, alpha, beta, False)
            board[move] = ' '
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = math.inf
        for move in available_moves(board):
            board[move] = 'X'
            eval = minimax(board, depth + 1, alpha, beta, True)
            board[move] = ' '
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

def best_move(board):
    best_val = -math.inf
    move = None
    for i in available_moves(board):
        board[i] = 'O'
        move_val = minimax(board, 0, -math.inf, math.inf, False)
        board[i] = ' '
        if move_val > best_val:
            best_val = move_val
            move = i
    return move

def play_game():
    print_board(board)
    while True:
        # Player Move
        player_move = int(input("Enter your move (1-9): ")) - 1
        if board[player_move] != ' ':
            print("Invalid move, try again.")
            continue
        board[player_move] = 'X'
        if winner(board, 'X'):
            print_board(board)
            print("You win!")
            break
        if is_full(board):
            print_board(board)
            print("It's a tie!")
            break
        
        # AI Move
        ai_move = best_move(board)
        board[ai_move] = 'O'
        print_board(board)
        if winner(board, 'O'):
            print("AI wins!")
            break
        if is_full(board):
            print("It's a tie!")
            break

play_game()
