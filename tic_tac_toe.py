import random

class TTT_cs170_judge:
    def __init__(self):
        self.board = []
        
    def create_board(self, n):
        for i in range(n):
            row = []
            for j in range(n):
                row.append('-')
            self.board.append(row)
            
    def display_board(self):
        for row in self.board:
            print(" ".join(row))
        print()
            
    def is_winner(self, player):
        # Check rows
        for row in self.board:
            if all([cell == player for cell in row]):
                return True
        
        # Check columns
        for col in range(len(self.board)):
            if all([self.board[row][col] == player for row in range(len(self.board))]):
                return True
        
        # Check diagonals
        if all([self.board[i][i] == player for i in range(len(self.board))]):
            return True
        if all([self.board[i][len(self.board) - i - 1] == player for i in range(len(self.board))]):
            return True
        
        return False
    
    def is_board_full(self):
        return all([cell in ['X', 'O'] for row in self.board for cell in row])
    

class Player_1:
    def __init__(self, judge):
        self.board = judge.board
    
    def my_play(self):
        while True:
            row, col = map(int, input("Enter the row and column numbers separated by space: ").split())
            
            if 1 <= row <= len(self.board) and 1 <= col <= len(self.board[0]):
                self.board[row-1][col-1] = 'X'
                break
            else:
                print("Wrong coordination!")


class Player_2:
    def __init__(self, judge):
        self.judge = judge
        self.board = judge.board
        self.boarddict = {}
    
    def board_is_winner(self, player):
        # Check rows
        for row in self.board:
            if all([cell == player for cell in row]):
                return True
        
        # Check columns
        for col in range(len(self.board)):
            if all([self.board[row][col] == player for row in range(len(self.board))]):
                return True
        
        # Check diagonals
        if all([self.board[i][i] == player for i in range(len(self.board))]):
            return True
        if all([self.board[i][len(self.board) - i - 1] == player for i in range(len(self.board))]):
            return True
        
        return False
    
    def board_is_board_full(self):
        return all([cell in ['X', 'O'] for row in self.board for cell in row])

    
    def board_display_board(self):
        for row in self.board:
            print(" ".join(row))
        print()
    
    def board_to_string(self):
        boardstring = ''
        for i in range(3) :
            for j in range(3) :
                boardstring += str(self.board[i][j])
        return boardstring
    
    def print_hash(self):
        for x,y in self.boarddict.items():
             print(x, ":" , y)

    def minimax(self, board: list[list[str]], depth: int, maximizing: bool, alpha: int, beta: int):
        if self.board_is_winner("X"):
            return -1
        
        if self.board_is_winner("O"):
            return 1
        
        if self.board_is_board_full():
            return 0
    
        
        if maximizing:
            best = -1000
            for i in range(3) :
                for j in range(3) :
                    if board[i][j] == '-':
                        board[i][j] = 'O'
                        bstring = self.board_to_string()
                        if bstring in self.boarddict:
                            best = max(best, self.boarddict[bstring])
                            # print("found maximizing " + bstring + "in boarddict")
                        else :
                            score = self.minimax(board, depth+1, not maximizing, alpha, beta)
                            # self.boarddict[bstring] = score
                            best = max( best, score)
                        # best = max(best, self.minimax(board, depth+1, not maximizing, alpha, beta))
                        board[i][j] = '-'
                        alpha = max(alpha, best)
                        if beta <= alpha:
                            break
            return best
        else :
            best = 1000
            for i in range (3) :
                for j in range(3) :
                    if board[i][j] == '-':
                        board[i][j] = 'X'
                        bstring = self.board_to_string()
                        if bstring in self.boarddict:
                            best = min(best, self.boarddict[bstring])
                            # print("found minimizing " + bstring  + "in boarddict")
                        else :
                            score = self.minimax(board, depth+1, not maximizing, alpha, beta)
                            # self.boarddict[bstring] = score
                            best = min(best, score)
                        # best = min(best, self.minimax(board, depth+1, not maximizing, alpha, beta))
                        board[i][j] = '-'
                        beta = min(beta, best)
                        if beta <= alpha:
                            break
            return best
        
    def my_play(self):
        # implement your code here
        score = 0
        maxscore = 0
        bestmove = (-1, -1)
        for row in range(3):
            for col in range(3):
                if self.board[row][col] == '-': 
                    self.board[row][col] = 'O'
                    bstring = self.board_to_string()
                    if bstring in self.boarddict:
                        score = self.boarddict[bstring]
                    else :
                        score = self.minimax(self.board, 0, False, -1000, 1000)
                        self.boarddict[bstring] = score
                    self.board[row][col] = '-'
                    self.print_hash()
                    print("\n")
                    if score >= maxscore:
                        maxscore = score
                        bestmove = (row, col)

        self.board[bestmove[0]][bestmove[1]] = 'O'

# Main Game Loop
def game_loop():
    n = 3  # Board size
    game = TTT_cs170_judge()
    game.create_board(n)
    player1 = Player_1(game)
    player2 = Player_2(game)
    starter = random.randint(0, 1)
    win = False
    if starter == 0:
        print("Player 1 starts.")
        game.display_board()
        while not win:
            player1.my_play()
            win = game.is_winner('X')
            game.display_board()
            if win:
                print("Player 1 wins!")
                break
            if game.is_board_full():
                print("It's a tie!")
                break

            player2.my_play()
            win = game.is_winner('O')
            game.display_board()
            if win:
                print("Player 2 wins!")
                break
            if game.is_board_full():
                print("It's a tie!")
                break
    else:
        print("Player 2 starts.")
        game.display_board()
        while not win:
            player2.my_play()
            win = game.is_winner('O')
            game.display_board()
            if win:
                print("Player 2 wins!")
                break
            if game.is_board_full():
                print("It's a tie!")
                break
            
            player1.my_play()
            win = game.is_winner('X')
            game.display_board()
            if win:
                print("Player 1 wins!")
                break
            if game.is_board_full():
                print("It's a tie!")
                break

game_loop() # Uncomment this line to play the game, but it must be commented again when you are submitting the code
