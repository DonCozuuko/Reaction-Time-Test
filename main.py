import pygame as pg
import random as r
import time


WIN_SIZE = (600, 600)
TEXT_SIZE = 60
BLACK = (0, 0 ,0)
WHITE = (255, 255, 255)
GREY = (128, 128, 128)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

TIME_INV = 8
ELAPSED_TIME = 0

class Display_Screen1:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        pg.font.init()

    def run(self):
        font = pg.font.SysFont(None, TEXT_SIZE)
        img = font.render("Click to Play!", None, BLACK)

        text_rect = img.get_rect()
        text_rect.centerx = self.screen.get_rect().centerx  # Center horizontally
        text_rect.top = 200
        self.screen.blit(img, text_rect)


class Display_Screen2:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        pg.font.init()

    def run(self):
        font1 = pg.font.SysFont(None, TEXT_SIZE)
        font2 = pg.font.SysFont(None, TEXT_SIZE)
        font2.set_italic(True)

        img1 = font1.render("Click when the", None, GREY)
        img2 = font1.render("screen changes colour", None, GREY)
        img3 = font2.render("Click to start", None, GREY)

        text_rect1 = img1.get_rect()
        text_rect2 = img2.get_rect()
        text_rect3 = img3.get_rect()

        text_rect1.centerx = self.screen.get_rect().centerx  # Center horizontally
        text_rect2.centerx = self.screen.get_rect().centerx  # Center horizontally
        text_rect3.centerx = self.screen.get_rect().centerx

        text_rect1.top = 200
        text_rect2.top = 250
        text_rect3.top = 300

        self.screen.blit(img1, text_rect1)
        self.screen.blit(img2, text_rect2)
        self.screen.blit(img3, text_rect3)


class Display_Screen3:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.countdown_played = False
        pg.font.init()

    def countdown(self):
        if not self.countdown_played:
            font = pg.font.SysFont(None, TEXT_SIZE)

            cd1 = font.render("3", None, GREEN)
            cd2 = font.render("2", None, YELLOW)
            cd3 = font.render("1", None, RED)

            cd_rect1 = cd1.get_rect(center = (200, 200))
            cd_rect2 = cd2.get_rect(center = (300, 300))
            cd_rect3 = cd3.get_rect(center = (400, 400))
            
            cd_rect1.top = 300
            cd_rect2.top = 300
            cd_rect3.top = 300

            self.screen.fill(WHITE)
            self.screen.blit(cd1, cd_rect1)
            pg.display.update()
            time.sleep(0.5)

            self.screen.fill(WHITE)
            self.screen.blit(cd2, cd_rect2)
            pg.display.update()
            time.sleep(0.5)

            self.screen.fill(WHITE)
            self.screen.blit(cd3, cd_rect3)
            pg.display.update()
            time.sleep(0.5)
            self.screen.fill(WHITE)
            self.countdown_played = True


class Display_Screen4:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen

    def run(self):
        time.sleep(3)  # Wait before starting the green flash

        # Start the flash and capture the start time.
        self.game.flash_start_time = pg.time.get_ticks()

        green_flash_duration = 250  # 500 milliseconds flash duration
        elapsed_time = 0

        # Loop to display the green flash for a specific duration
        while elapsed_time < green_flash_duration:
            self.screen.fill(GREEN)
            pg.display.update()
            elapsed_time = pg.time.get_ticks() - self.game.flash_start_time  # Elapsed time since flash started
            pg.time.wait(50)  # Small wait before next screen update

        # Now wait for the mouse click and capture the time.
        waiting_for_click = True
        while waiting_for_click:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    exit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    # Calculate the reaction time: how long after the green flash
                    click_time = pg.time.get_ticks() - self.game.flash_start_time
                    self.game.ms = click_time  # Store the reaction time
                    waiting_for_click = False  # Exit the loop
                    self.game.current_screen = 5  # Move to the next screen
                    break


class Display_Screen5:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen

    def run(self):
        # Get the reaction time in milliseconds
        reaction_time = self.game.ms

        font = pg.font.SysFont(None, TEXT_SIZE)
        img = font.render(f"Reaction Time: {reaction_time} ms", True, BLACK)
        text_rect = img.get_rect()
        text_rect.centerx = self.screen.get_rect().centerx  # Center horizontally
        text_rect.top = 200
        self.screen.blit(img, text_rect)


class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode(WIN_SIZE)
        self.Display_Screen1 = Display_Screen1(self)
        self.Display_Screen2 = Display_Screen2(self)
        self.Display_Screen3 = Display_Screen3(self)
        self.Display_Screen4 = Display_Screen4(self)
        self.Display_Screen5 = Display_Screen5(self)
        self.current_screen = 1
        self.ms = 0  # This will store the reaction time in ms
        self.flash_start_time = 0  # To store the start time of the green flash

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()

            if event.type == pg.MOUSEBUTTONDOWN:
                if self.current_screen == 4:  # If we're on screen 4, track the click time
                    click_time = pg.time.get_ticks() - self.flash_start_time
                    self.ms = click_time  # Store the reaction time in ms
                    self.current_screen = 5  # Move to the next screen to display time
                else:
                    self.current_screen += 1  # Move to the next screen for other cases

    def run(self):
        while True:
            self.screen.fill(WHITE)
            self.check_events()

            if self.current_screen == 1:
                self.Display_Screen1.run()
            elif self.current_screen == 2:
                self.Display_Screen2.run()
            elif self.current_screen == 3:
                self.Display_Screen3.countdown()
                self.current_screen += 1
            elif self.current_screen == 4:
                self.Display_Screen4.run()  # Green flash screen
            elif self.current_screen == 5:
                self.Display_Screen5.run()  # Reaction time screen

            pg.display.update()


if __name__ == "__main__":
    game_run = Game()
    game_run.run()
