import pygame
from network import Network
from game import Intersection, Player
from button import Button
import bz2
pygame.init()

## COLORS ##
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

## GAME CONSTANTS ##
WIDTH = 720
GRID_WIDTH = WIDTH // 144
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Gomoku")
FPS = 60

## FILE IMPORTS ##
WOOD_PICTURE = pygame.image.load('Assets/wooden_background.jpeg')
BACKGROUND = pygame.transform.scale(WOOD_PICTURE, (WIDTH, WIDTH))
HIGHLIGHT_PICTURE = pygame.image.load(
    'Assets/light-alpha-gradient-transparency-and-translucency-web-browser-luz-9c61015f077b3ac9d8000909ca2f0115.png')
HIGHLIGHT = pygame.transform.scale(
    HIGHLIGHT_PICTURE, (WIDTH // 30, WIDTH // 30))
ENDSCREEN_FONT = pygame.font.SysFont('timesnewroman', WIDTH // 15, True)
STARTUP_FONT = pygame.font.SysFont('helveticaneue', WIDTH // 15, True, True)


class IntersectionRender:
    """this is a class for an Intersection that knows how to draw itself and detect if it is clicked on or hovered on
    """

    def __init__(self, intersection: Intersection):
        """constructor for an IntersectionRender

        :param intersection: the abstract Intersection to turn into a Render
        """
        self.x = intersection.row * (WIDTH // 16)
        self.y = intersection.column * (WIDTH // 16)
        self.row = intersection.row
        self.column = intersection.column
        self.state = intersection.state

    def is_mouse_hov(self):
        """determines if the mouse is hovering near this intersection

        :return: returns True if the mouse is hovering within 10 pixel radius of the intersection
        """
        mouse_x, mouse_y = pygame.mouse.get_pos()
        return not self.state and abs(mouse_x - self.x) < WIDTH // 36 and abs(mouse_y - self.y) < WIDTH // 36

    def is_clicked_on(self):
        """whether the mouse is clicked when hovering on this intersection

        :return: returns True if the mouse is clicked when hovering on the intersection (if it's clicked on)
        """
        return self.is_mouse_hov() and pygame.mouse.get_pressed()[0]

    def draw(self, my_turn):
        """ draws the intersection with piece / highlights as necessary

        :param my_turn: boolean true if its the client's turn, false if not
        """
        if self.state == None and self.is_mouse_hov() and my_turn:
            WIN.blit(HIGHLIGHT, (self.x - HIGHLIGHT.get_width() //
                     2, self.y - HIGHLIGHT.get_height() // 2))
        elif self.state == Player.WHITE_PLAYER:
            pygame.draw.circle(WIN, WHITE, (self.x, self.y), WIDTH // 48)
        elif self.state == Player.BLACK_PLAYER:
            pygame.draw.circle(WIN, BLACK, (self.x, self.y), WIDTH // 48)


def generate_board_render(game_board):
    """generates a renderable game board based on the abstract game_board received from the server

    :param game_board: the game_board object to turn into a game_board_render
    :return: a renderable game board version of game_board
    """
    board_render = []
    for i in range(len(game_board)):
        board_render.append([])
        for j in range(len(game_board[0])):
            board_render[i].append(IntersectionRender(game_board[i][j]))
    return board_render


def draw_board():
    """function to render the "board" (wooden background with intersection pattern)
    """
    WIN.blit(BACKGROUND, (0, 0))

    # render columns
    for i in range(1, 16):
        pygame.draw.rect(WIN, BLACK, pygame.Rect(
            (WIDTH // 16) * i - (GRID_WIDTH // 2), WIDTH // 16, GRID_WIDTH, (WIDTH * 14) // 16))
    # render rows
    for i in range(1, 16):
        pygame.draw.rect(WIN, BLACK, pygame.Rect(
            WIDTH // 16, (WIDTH // 16) * i - (GRID_WIDTH // 2), (WIDTH * 14) // 16, GRID_WIDTH))


def draw_pieces(game_board_render, my_turn):
    """method to draw each piece

    :param game_board_render: the game_board_render object the contains IntersectionRenders
    :param my_turn: true if its the client's turn, false otherwise
    """
    for row in game_board_render:
        for piece in row:
            piece.draw(my_turn)


def draw_mouse(p):
    """method to render the mouse tracer piece given which players turn it is

    :param p: 0 if white's turn, 1 if black's turn
    """
    if p == 0:
        pygame.draw.circle(WIN, WHITE,  pygame.mouse.get_pos(), WIDTH // 72)
    else:
        pygame.draw.circle(WIN, BLACK,  pygame.mouse.get_pos(), WIDTH // 72)


def redraw_window(game, p, board_render, my_turn):
    """method to redraw the game window

    :param game: game object that represents the current game
    :param p: the player that this client is
    :param board_render: a renderable board object
    :param my_turn: true if its the client's turn, false if not
    """
    draw_board()

    if not game.connected:
        text = ENDSCREEN_FONT.render('Waiting for player...', 1, (0, 0, 0))
        WIN.blit(text, (WIDTH/2 - text.get_width() /
                        2, WIDTH/2 - text.get_height()/2))
    else:
        draw_pieces(board_render, my_turn)
        draw_mouse(p)
    pygame.display.update()


def draw_start_up():
    """draws the start screen
    """
    WIN.blit(BACKGROUND, (0, 0))
    START_TEXT = STARTUP_FONT.render("Gomoku", 1, WHITE)
    WIN.blit(START_TEXT, (WIDTH // 2 - START_TEXT.get_width() // 2, WIDTH // 4))


def main():
    """method to being the game loop
    """
    run = True
    clock = pygame.time.Clock()
    network = Network()
    try:
        # get player number
        p = int(network.get_p())
    except:
        print('Could not get player')
    print('You are player', p)

    while run:
        clock.tick(FPS)
        pygame.mouse.set_visible(False)
        try:
            # get game state
            game = network.send('get')
        except Exception as e:
            # close game if server is closed
            print(e)
            print("Couldn't get game")
            game.connected = False
            run = False
            break
        board_render = generate_board_render(game.game_board)
        my_turn = game.turn == p
        if game.winner() == None:
            pass
        elif game.winner() == -1:
            # if the game is a draw, display the draw and reset the game
            WIN.fill(YELLOW)
            END_TEXT = ENDSCREEN_FONT.render("Draw", 1, BLACK)
            WIN.blit(END_TEXT, (WIDTH // 2 - END_TEXT.get_width() //
                     2, WIDTH // 2 - END_TEXT.get_height() // 2))
            pygame.display.update()
            pygame.time.delay(2000)
            network.send('reset')
            main_menu()
        elif game.winner() == p:
            # if a player wins, display the winner and reset the game
            WIN.fill(WHITE)
            END_TEXT = ENDSCREEN_FONT.render("You Win!", 1, BLACK)
            WIN.blit(END_TEXT, (WIDTH // 2 - END_TEXT.get_width() //
                     2, WIDTH // 2 - END_TEXT.get_height() // 2))
            pygame.display.update()
            pygame.time.delay(2000)
            network.send('reset')
            main_menu()
        else:
            # if a player loses, display the loser and reset the game
            WIN.fill(BLACK)
            END_TEXT = ENDSCREEN_FONT.render("You Lose!", 1, WHITE)
            WIN.blit(END_TEXT, (WIDTH // 2 - END_TEXT.get_width() //
                     2, WIDTH // 2 - END_TEXT.get_height() // 2))
            pygame.display.update()
            pygame.time.delay(2000)
            network.send('reset')
            main_menu()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print('Game quit')
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN and game.connected:
                for row in board_render:
                    for intersection in row:
                        if intersection.is_clicked_on() and game.turn == p and intersection.state == None:
                            # if a move is made, send the move to the server
                            network.send(
                                (intersection.row, intersection.column))
        redraw_window(game, p, board_render, my_turn)


def main_menu():
    """method to manage the start screen
    """
    not_started = True
    clock = pygame.time.Clock()
    pygame.mouse.set_visible(True)
    start_button = Button(WIN, 'Assets/start_button_image.png', WIDTH // 2 - WIDTH // 3,
                          WIDTH // 2 - WIDTH // 8, 2 * WIDTH // 3, WIDTH // 4, 'Assets/start_button_on_hover.png')
    while not_started:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN and start_button.is_clicked_on():
                not_started = False
        draw_start_up()
        start_button.draw()
        pygame.display.update()

    main()


if __name__ == '__main__':
    main_menu()
