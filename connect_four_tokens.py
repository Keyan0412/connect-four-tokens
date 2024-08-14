import turtle


def click(*args):
    """
    place tokens when click
    """
    global placeholders, chessboard, chess, order

    # find position of mouse when click
    click_x = args[0]
    for num in range(8):
        temp = placeholders[num].xcor()
        if abs(click_x - temp) <= 30:
            pos = num
            break
    else:
        pos = -1

    temp = pos
    if 0 <= temp <= 7 and order[temp] <= 7:

        # release binding to make sure no interruption during processing
        screen.onclick(None)

        # record the step
        player = sum(order) % 2
        chessboard[temp][order[temp]] = player
        order[temp] = order[temp] + 1

        # place the tokens
        screen.tracer(0)
        t = turtle.Turtle('circle')
        if player == 0:
            t.color('red')
        else:
            t.color('blue')
        t.speed(8)
        t.shapesize(3, 3, 10)
        t.pu()
        t.goto(50+temp*100, 800)
        screen.update()
        screen.tracer(1)
        t.goto(50 + temp * 100, 100 * (order[temp])-40)
        chess[temp].append(t)

        end_game(player)


def end_game(player):
    """
    stop the game when a player wins
    """
    global end, canvas, screen
    flag, key_chess = check()
    if flag:

        # stop the mouse tracker
        canvas.unbind('<Motion>')
        end = True

        # highlight the tokens of winner
        for i in key_chess:
            i.color('green', i.color()[0])

        # print information of winner in the title
        if player == 0:
            text = "Winner! Player 1"
        else:
            text = "Winner! Player 2"
        turtle.title(text)

        return None

    if tie_test():
        # stop the mouse tracker
        canvas.unbind('<Motion>')
        end = True

        turtle.title('Game Tied!')
        return None

    # bind the function again
    if player == 1:
        screen.title("Connect Four-Player 1 Turn")
    else:
        screen.title("Connect Four-Player 2 Turn")
    screen.onclick(click)


def tie_test():
    """
    check whether the game is tied
    """
    global order
    if order == [8, 8, 8, 8, 8, 8, 8, 8]:
        return True
    return False


def check():
    """
    check whether one of the players have won the game
    """
    global chessboard, chess

    # check each row
    for row in range(8):
        key_chess = []
        re = None
        count = 1
        for col in range(8):
            if chessboard[col][row] == 0 or chessboard[col][row] == 1:
                if re == chessboard[col][row]:
                    count += 1
                    key_chess.append(chess[col][row])
                    if count == 4:
                        return True, key_chess
                else:
                    re = chessboard[col][row]
                    count = 1
                    key_chess = [chess[col][row]]
            else:
                re = None
                count = 1

    # check each column
    for col in range(8):
        key_chess = []
        re = None
        count = 1
        for row in range(8):
            if chessboard[col][row] == 0 or chessboard[col][row] == 1:
                if re == chessboard[col][row]:
                    count += 1
                    key_chess.append(chess[col][row])
                    if count == 4:
                        return True, key_chess
                else:
                    re = chessboard[col][row]
                    count = 1
                    key_chess = [chess[col][row]]
            else:
                re = None
                count = 1

    # check each diagonal
    for dia in range(9):
        key_chess = []
        re = None
        count = 1
        if dia <= 4:
            x = 0
            y = 4 - dia
        else:
            x = dia - 4
            y = 0
        for j in range(8-abs(dia-4)):
            x1, y1 = x+j, y+j
            if chessboard[x1][y1] == 0 or chessboard[x1][y1] == 1:
                if re == chessboard[x1][y1]:
                    count += 1
                    key_chess.append(chess[x1][y1])
                    if count == 4:
                        return True, key_chess
                else:
                    re = chessboard[x1][y1]
                    count = 1
                    key_chess = [chess[x1][y1]]
            else:
                re = None
                count = 1

    for dia in range(9):
        key_chess = []
        re = None
        count = 1
        if dia <= 4:
            x = 7
            y = 4 - dia
        else:
            x = 11 - dia
            y = 0
        for j in range(8-abs(dia-4)):
            x1, y1 = x-j, y+j
            if chessboard[x1][y1] == 0 or chessboard[x1][y1] == 1:
                if re == chessboard[x1][y1]:
                    count += 1
                    key_chess.append(chess[x1][y1])
                    if count == 4:
                        return True, key_chess
                else:
                    re = chessboard[x1][y1]
                    count = 1
                    key_chess = [chess[x1][y1]]
            else:
                re = None
                count = 1

    return False, None


def tracker():
    """
    track mouse and highlight particular holder
    """
    global highlight, pointer_x, placeholders, end
    for num in range(8):
        temp = placeholders[num].xcor()
        if abs(pointer_x - temp) <= 30:
            placeholders[num].color('purple', 'black')
            if highlight != num:
                placeholders[highlight].color('black')
                highlight = num
            break
    else:
        placeholders[highlight].color('black')

    if end:
        placeholders[highlight].color('black')
        return None
    screen.ontimer(tracker, 100)


def pointer(event):
    """
    delivery position of mouse
    """
    global pointer_x
    pointer_x, pointer_y = event.x, event.y
    # print('mouse_position:', pointer_x, pointer_y)


def draw_holders():
    """
    draw the holders firstly
    """
    global screen, placeholders
    for num in range(8):
        screen.tracer(0)
        placeholders.append(turtle.Turtle('square'))
        placeholders[num].shapesize(1, 3, 5)
        placeholders[num].speed(10)
        placeholders[num].pu()
        placeholders[num].goto(50+100*num, 10)
        screen.update()
        screen.tracer(1)


def main():

    # initialize settings of screen
    global screen, canvas
    screen.title('Connect Four-Player 1 Turn')
    screen.setup(820, 850)
    screen.setworldcoordinates(0, 0, 820, 850)

    draw_holders()

    # bind functions to events
    canvas = screen.getcanvas()
    canvas.bind('<Motion>', pointer)
    screen.ontimer(tracker, 500)
    screen.onclick(click)

    screen.mainloop()


if __name__ == "__main__":

    # initialize variables for recording steps
    chessboard = []
    for num_col in range(8):
        chessboard.append([3, 3, 3, 3, 3, 3, 3, 3])
    chess = [[], [], [], [], [], [], [], []]
    order = [0, 0, 0, 0, 0, 0, 0, 0]

    # initialize variables for tracing mouse
    pointer_x = 800
    highlight = 7
    placeholders = []

    # initialize variables for screen and holders
    screen = turtle.Screen()
    canvas = None
    end = False

    main()
