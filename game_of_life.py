import sys
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from simple_term_menu import TerminalMenu as tm
import pygame
    
BLACK = (0,0,0)
WHITE = (255, 255, 255)
GREY = (32, 32, 32)


class GameOfLife:
    def __init__(self):
        self.screen = pygame.display.set_mode(size)
        pygame.display.set_caption("Game Of Life")
        self.clock = pygame.time.Clock()

        # Grid parameters
        self.square_size = square_size
        self.alive_squares = set()

    def run(self):
        running = True
        play_game = False
        generation = 0
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        play_game = not play_game 
                        if not play_game:
                            generation = 0
                    if event.key == pygame.K_r and not play_game:
                        self.alive_squares = set()

            if not len(self.alive_squares):
                play_game = False
            if play_game:
                self.next_generation()
                generation += 1
            #  self.debug_info(play_game, generation)
            self.change_state()
            self.screen.fill(BLACK)
            self.draw_grid()
            pygame.display.update()
            self.clock.tick(10)
        os.system("clear")


    def delete_last_lines(self, n=1): 
        for _ in range(n): 
            sys.stdout.write("\x1b[1A")
            sys.stdout.write("\x1b[2K") 


    def debug_info(self, run, generation):
        if run:
            self.delete_last_lines(2)
            print("Cells alive: {}\nGeneration: {}".format(len(self.alive_squares), generation))
        else:
            self.delete_last_lines()
            print("Cells alive: {}".format(len(self.alive_squares)), end="\r")
    

    def draw_grid(self):
        for elem in self.alive_squares:
            pygame.draw.rect(self.screen, WHITE, (elem[0], elem[1], self.square_size, self.square_size))
        pos = 0
        while pos < size[1]: 
            pygame.draw.line(self.screen, GREY, (0, pos), (size[0], pos))
            pos += self.square_size
        pos = 0
        while pos < size[0]:
            pygame.draw.line(self.screen, GREY, (pos, 0), (pos, size[1]))
            pos += self.square_size

    def change_state(self):
        mouse_buttons = pygame.mouse.get_pressed()
        if mouse_buttons[0] or mouse_buttons[2]:
            pos = pygame.mouse.get_pos()
            x = (pos[0] // self.square_size) * self.square_size
            y = (pos[1] // self.square_size) * self.square_size
            
            if mouse_buttons[0]:
                self.alive_squares.add((x, y))
            if mouse_buttons[2]:
                try:
                    self.alive_squares.remove((x, y))
                except KeyError:
                    pass

    def next_generation(self):
        a = self.square_size
        dead_squares = set()
        new_dead_squares = set()
        new_alive_square = set()
        for square in self.alive_squares:
            neighbour = 0
            for pos in [(0, -a), (0, a), (-a, 0), (a, 0), (-a, -a), (-a, a), (a, -a), (a, a)]:
                if (square[0] + pos[0], square[1] + pos[1]) in self.alive_squares:
                    neighbour += 1
                else:
                    dead_squares.add((square[0] + pos[0], square[1] + pos[1]))
            if neighbour not in [2, 3]:
                new_dead_squares.add(square)
        for square in dead_squares:
            neighbour = 0
            for pos in [(0, -a), (0, a), (-a, 0), (a, 0), (-a, -a), (-a, a), (a, -a), (a, a)]:
                if (square[0] + pos[0], square[1] + pos[1]) in self.alive_squares:
                    neighbour += 1
            if neighbour == 3:
                new_alive_square.add(square)

        try: 
            self.alive_squares -= new_dead_squares
            self.alive_squares.update(new_alive_square)
        except KeyError:
            pass

if __name__ == "__main__":
    os.system("clear && cat instructions.txt")
    print("Select configuration")
    configuration = tm(["Default", "Custom"]).show()
    if configuration:
        print("Select resolution:")
        size_list = ["Large", "Medium", "Small"]
        size_option = tm(size_list).show()
        if size_option == 0:
            size = (1920, 1080)
        elif size_option == 1:
            size = (1080, 720)
        else:
            size = (600, 600)
        print("Resolution {}: {}".format(size_list[size_option], size))
        print("Select square size:")
        square_option = tm(["10", "15", "20", "25"]).show()
        if square_option or square_option == 0:
            square_size = 10 + square_option * 5
        else:
            square_size = 15
    else:
        size = (1080, 720)
        print("Resolution Medium: (1080, 720)")
        square_size = 15
    print("Square Size: {}".format(square_size))
    #  os.system("clear")
    game_of_life = GameOfLife() 
    game_of_life.run()
