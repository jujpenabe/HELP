# import the pygame module, so you can use it
import pygame
import os

from sys import exit
from statemachine import StateMachine, State

class GameStateMachine(StateMachine):
    MENU = State('Menu')
    FADE_IN = State('FadeIn', initial = True)
    PLAY = State('Play')
    FADE_OUT = State('FadeOut')
    QUIT = State('Quit')

    fadein = FADE_OUT.to(FADE_IN)
    fadeout = MENU.to(FADE_OUT) | PLAY.to(FADE_OUT)
    quiting = FADE_OUT.to(QUIT)
    transitioning = FADE_OUT.to(FADE_OUT) | FADE_IN.to(FADE_IN)
    playing = FADE_IN.to(PLAY)
    menuing = FADE_IN.to(MENU)

    # def on_fadein(self):
    #     print ("This is Fading in")
    # def on_fadeout(self):
    #     print("This is now Fading out")
    def on_quiting(self):
        pygame.quit()
        exit()
    def on_playing(self, game):
        print ("Playing is need to load all HUD here? per scenes?")
    def on_menuing(self, game):
    # Load MENU HUD
        screen = game.screen
        enterlogo = pygame.image.load("Logos/EnterLogo.png").convert_alpha()
        enterlogo.set_alpha(192)
        spot1 =  Spot(enterlogo.get_rect(),"PLAY",1,0)

        game.add_spot_to_room(spot1)
        created_by = game.fonts[0].render("Created by Juan José Peña", True, (0,0,44))

        screen.blit(enterlogo, (((screen.get_width()/2)- (enterlogo.get_rect().width * 2.5)),(screen.get_height()*3/4)))
        screen.blit(created_by,(490,570))

    #On enter callbacks
    def on_enter_FADEIN(self):
        print ("The beginnig of the fadein")
    def on_enter_FADEOUT(self):
        print ("The beginning of the fadeout")
    def on_enter_QUIT(self):
        print("This should be the last print before quiting")

    #On exit callbacks
    def on_exit_FADEIN(self):
        print ("The end of the fadein")
    def on_exit_FADEOUT(self):
        print("The end of the fadeout")
    def on_exit_QUIT(self):
        print("This should never be displayed")

class Game:

    state           = None
    target_state    = None
    scene           = 0
    target_scene    = 0
    room            = 0
    target_room     = 0
    opacity         = 0
    fonts           = []

    def __init__(self, resolution = (800,600)):
        self.screen = pygame.display.set_mode((800, 600))

    def set_game_state_machine(self, state_machine):
        self.gsm = state_machine

    def addFont(self, font):
        self.fonts.append(font)

    def load_scenes_rooms_background(self, folder):
        scenes = []
        for scene in os.listdir(folder):
            rooms = []
            for i in os.listdir(os.path.join(folder,scene)):
                path =  os.path.join(folder,scene)+"/"+i
                background = pygame.image.load(path).convert()
                new_room = Room(background)
                rooms.append(new_room)
            new_scene = Scene((0,0,20),rooms)
            scenes.append(new_scene)
        self.scenes = scenes
    def fade_in_scene(self):
        self.screen.fill((0,0,20))
        bg = self.scenes[self.target_scene].rooms[self.target_room].background
        bg.set_alpha(self.opacity)
        self.screen.blit(bg, (0,0))
        if self.opacity<256:
            self.opacity += 24
        else:
            self.opacity = 256
            # all options to switch from FADE IN
            if (self.target_state == "MENU"):
                self.gsm.menuing(self)
            elif (self.target_state == "PLAY"):
                self.gsm.playing(self)
    def fade_out_scene(self):
        self.screen.fill((0,0,20))
        bg = self.scenes[self.scene].rooms[self.room].background
        bg.set_alpha(self.opacity)
        if self.opacity>0:
            self.opacity -= 32
        else:
            self.opacity = 0
            # all options to switch from FADE OUT
            if (self.target_state == "QUIT"):
                self.gsm.quiting()
            elif (self.target_state == "PLAY"):
                print("Estado: " + self.state)
                print("Estado GSM: " + str(self.gsm.current_state))
                self.gsm.fadein()
            else:
                print("Por lo menos fadea out: " + str(self.gsm.current_state))
        self.screen.blit(bg, (0,0))
    # Change state scene room
    def change_ssr(self,target_state, target_scene, target_room):
        self.target_state = target_state
        self.target_scene = target_scene
        self.target_room = target_room
    def switch_state(self):
        # Check if both states are diferent in order to switch states
        if (self.state != self.target_state):
            # All code if the state is FADE_IN
            if self.target_state == "FADE_IN":
                self.fade_in_scene()

            # All code if the state is FADE_OUT
            elif self.target_state == "FADE_OUT":
                self.fade_out_scene()

            # All code if the state is MENU
            elif self.target_state == "MENU":
                self.fade_in_scene()

            # All code if the state is PLAY
            elif self.target_state == "PLAY":
                if self.state == "FADE_OUT":
                    self.fade_out_scene()
                elif self.state == "FADE_IN":
                    self.fade_in_scene()
                else:
                    self.gsm.fadeout()
            # All code if the state is QUIT
            elif self.target_state == "QUIT":
                if self.state == "FADE_OUT":
                    self.fade_out_scene()
                else:
                    self.gsm.fadeout()
            else:
                print("No target state assigned")
        else:
            pass
    def add_spot_to_room(self, spot):
        self.scenes[self.scene].rooms[self.room].add_spot(spot)
    def check_spot(self, click_pos):
        for spot in self.scenes[self.scene].rooms[self.room]._spots:
            if (spot._rectangle.collidepoint(click_pos) and spot._active):
                self.change_ssr(spot._target_state, spot._target_scene, spot._target_room)
            else:
                pass
class Scene:
    def __init__(self, rgb=(0,0,20), rooms_list= None) :
        self.background_color = rgb
        self.rooms = rooms_list
class Room:
    def __init__(self, background):
        self.background = background
        self._spots = set()
    def add_spot(self, spot):
        self._spots.add(spot)
class Spot:
    def __init__(self, rectangle, target_state,target_scene, target_room, show = True, active = True):
        self._rectangle = rectangle
        self._target_state = target_state
        self._target_scene = target_scene
        self._target_room = target_room
        self._show = show
        self._active = active
        self._observers = []
    def register(self, spot):
        self._observers.append(spot)
    def unregister(self, spot):
        if spot in self._observers:
            self._observers.remove(spot)
    def notify_observers(self, event):
        for observer in self._observers:
            observer.notify(event)
    def notify(self, event):
        if event == "Show":
            self._show = True
        elif event == "Hide":
            self._show = False
        elif event == "Activate":
            self._active = True
        elif event == "Deactivate":
            self._active = False
        else:
            print ("Unknown event")

# define a main function
def main():
    # initialize the pygame module
    pygame.init()
    #Global variables for the game
    _new_game = Game((800,600))
    _new_game.load_scenes_rooms_background("Scenes/")
    # Add game state machine GSM
    _gsm = GameStateMachine(_new_game)
    _new_game.set_game_state_machine(_gsm)
    # Clock for ceil fps
    clock = pygame.time.Clock()
    # load and set the logo
    logo = pygame.image.load("Logos/HelpLogo.png").convert()
    pygame.display.set_icon(logo)
    pygame.display.set_caption("HELP")

    #Add some fonts
    mainfont = pygame.font.Font("Fonts/LCALLIG.TTF", 20)
    
    _new_game.addFont(mainfont)
    #Custom event every 100ms
    event_100ms = pygame.USEREVENT + 1

    pygame.time.set_timer(event_100ms,100)
    _new_game.change_ssr("MENU", 0,0)
    # main loop
    while True:
        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                _new_game.change_ssr("QUIT", 1, 0)
            if event.type == event_100ms:
                _new_game.switch_state()
            if event.type == pygame.MOUSEBUTTONDOWN:
                print ("Target scene: " + str(_new_game.target_scene))
                print (event.pos)
                _new_game.check_spot(event.pos)
        pygame.display.update()
        #Maximum 44 fps
        clock.tick(44)

# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    main()


