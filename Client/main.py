# author: Mark

from data.scripts.root import Root
from data.scripts.menu import Menu
from data.scripts.game import Game
from data.scripts.game_online import Online_game
from data.scripts.scene_transition import scene_animation
import pygame

# primary colors used in the game https://www.color-hex.com/color-palette/97154

def main():
    pygame.init()
    pygame.font.init()
    pygame.mixer.init()
    
    window_size = (1200, 700)
    root = Root(window_size, "Snake")

    Menu.introducing_image(root)

    menu_running = True
    offline_game_running = False
    online_game_running = False
    while True:
        if menu_running:
            # menu started
            menu = Menu()
            mode = menu.run(root)

            # menu finished
            menu_running = False

            if mode in ["classic", "advanced"]:
                offline_game_running = True
                online_game_running = False

            elif mode in ["onclassic", "onversus"]:
                online_game_running = True
                offline_game_running = False

        if offline_game_running:
            # game started
            game = Game(root, mode)

            scene_animation(root, 50, (24, 14), game.render)
            
            game.run()
            
            # game finished
            menu_running = True
            offline_game_running = False

            scene_animation(root, 50, (24, 14), game.render_final_screen)
            
            game.final_screen()

            scene_animation(root, 50, (24, 14), menu.render_first_stage)
            
        if online_game_running:
            # game started
            online_game = Online_game(root, mode, menu.server)

            scene_animation(root, 50, (24, 14), online_game.render)
            
            online_game.run()

            # game finished
            scene_animation(root, 50, (24, 14), online_game.render_final_screen)
            
            online_game.final_screen()

            scene_animation(root, 50, (24, 14), menu.render_first_stage)
            
            online_game_running = False
            menu_running = True
        
if __name__ == "__main__":
    main()
    