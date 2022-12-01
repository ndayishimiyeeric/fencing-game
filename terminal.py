import curses
import time
import os
import threading
import datetime
import characters
import classes
from playsound import playsound


stdscr = curses.initscr()
stdscr.nodelay(True)
curses.curs_set(0)
fps = 60

curses.start_color()
curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
COLOR_GREEN = curses.color_pair(1)
COLOR_YELLOW = curses.color_pair(2)
COLOR_RED = curses.color_pair(3)


def obj_drawer(_screen, _map, _char_dic, _color):
    for row in range(len(_map)):
        for col in range(len(_map[row])):
            _screen.addstr(row, col, _char_dic[_map[row][col]], _color)


ph, pw = stdscr.getmaxyx()

# elements
pg_win = stdscr.derwin(2, (pw//2)-1, (ph-2), 1)
pg_h, pg_w = pg_win.getmaxyx()
pg_y, pg_x = pg_win.getbegyx()

box_y = ((ph-1)) - pg_h
box_x = ((pw//2)//2) - 3//2
box_win = stdscr.derwin(2, 3, box_y, box_x)
# box coordinates list
box_coord = []
for y in range(box_y, box_y+2):
    for x in range(box_x, box_x+3):
        box_coord.append((y, x))


# players
p_one_y = ((ph-2) - 2) - pg_h
p_one_x = (box_x - 20)
p_one_win = stdscr.derwin(4, 4, p_one_y, p_one_x)
p_one_h, p_one_w = p_one_win.getmaxyx()

p_two_y = ((ph-2) - 2) - pg_h
p_two_x = (box_x + 20)
p_two_win = stdscr.derwin(4, 4, p_two_y, p_two_x)


class Scene:
    SCENE = ("_ _ _ _ _ _ 1 _ _ _ x _ _ 2 _ _ _ _ _").split(" ")

    def get_stored_scene(self):
        with open("scene.ffscene", "r") as f:
            self.SCENE = f.readline().split(" ")

    def __init__(self):
        self.player_one = classes.PlayerOne("PlayerOne")
        self.player_two = classes.PlayerTwo("PlayerTwo")
        self.get_stored_scene()
        self.score_file = max([os.path.join("data", f) for f in os.listdir(
            "data")], key=os.path.getctime)
        self.score_file = self.score_file.replace("\\", "/")
        self.score_file = self.score_file.split("/")[-1]
        self.get_stored_score(self.score_file)

    def draw(self):
        for i in self.SCENE:
            if i == "1":
                obj_drawer(p_one_win, characters.p_one_map,
                           characters.player_char_dic, COLOR_GREEN)
                if characters.p_one_attack:
                    obj_drawer(p_one_win, characters.p_one_map_attack,
                               characters.player_char_dic, COLOR_GREEN)
                if characters.p_one_block:
                    obj_drawer(p_one_win, characters.p_one_map_block,
                               characters.player_char_dic, COLOR_GREEN)
            elif i == "2":
                obj_drawer(p_two_win, characters.p_two_map,
                           characters.player_char_dic, COLOR_YELLOW)
                if characters.p_two_attack:
                    obj_drawer(p_two_win, characters.p_two_map_attack,
                               characters.player_char_dic, COLOR_YELLOW)
                if characters.p_two_block:
                    obj_drawer(p_two_win, characters.p_two_map_block,
                               characters.player_char_dic, COLOR_YELLOW)
            elif i == "x":
                box_win.attron(COLOR_RED)
                box_win.border()
                box_win.addstr(0, 1, "¤")
                box_win.attroff(COLOR_RED)
            elif i == "_":
                for i in range((pw//2)-2):
                    pg_win.addstr(0, i, "-")

    def move_down(self, player_win, y_pos, x_pos, sec=0.5):
        time.sleep(sec)
        if player_win == p_one_win:
            player_win.mvderwin(p_one_y, x_pos)
            player_win.mvwin(p_one_y, x_pos)
        player_win.mvderwin(y_pos + 2, x_pos)
        player_win.mvwin(y_pos + 2, x_pos)

    def move_up(self, player_win, y_pos, x_pos, sec=0.5):
        time.sleep(sec)
        player_win.mvderwin(y_pos - 2, x_pos)
        player_win.mvwin(y_pos - 2, x_pos)

    def jump_right(self, player_win, y_pos, x_pos, sec=1/fps):
        time.sleep(sec)
        new_x = x_pos + 6
        player_win.mvderwin(y_pos, new_x)
        player_win.mvwin(y_pos, new_x)
        t = threading.Thread(target=self.move_down, args=(
            player_win, y_pos, new_x))
        t.start()

    def jump_left(self, player_win, y_pos, x_pos, sec=1/fps):
        time.sleep(sec)
        new_x = x_pos - 6
        player_win.mvderwin(y_pos, new_x)
        player_win.mvwin(y_pos, new_x)
        t = threading.Thread(target=self.move_down, args=(
            player_win, y_pos, new_x))
        t.start()

    def move_right(self, player_win, y_pos, x_pos, sec=1/fps):
        time.sleep(sec)
        if x_pos >= ((pw//2)-2) - 4:
            return
        player_win.mvderwin(y_pos, x_pos + 1)
        player_win.mvwin(y_pos, x_pos + 1)

    def move_left(self, player_win, y_pos, x_pos, sec=1/fps):
        time.sleep(sec)
        if x_pos <= 1:
            return
        player_win.mvderwin(y_pos, x_pos - 1)
        player_win.mvwin(y_pos, x_pos - 1)

    def move_to_default(self, player_win, y_pos, x_pos, sec=1/fps):
        time.sleep(sec)
        player_win.mvderwin(y_pos, x_pos)
        player_win.mvwin(y_pos, x_pos)

    def get_stored_score(self, score_file):
        with open(os.path.join("data", f"{score_file}"), "r") as f:
            data = f.read().split(",")
            if len(data) < 2:
                characters.p_one_score = 0
                characters.p_two_score = 0
            else:
                characters.p_one_score = int(data[0])
                characters.p_two_score = int(data[1])

    def store_score(self):
        if not os.path.exists("data"):
            os.mkdir("data")
        file_name = datetime.datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
        with open(os.path.join("data", f"{file_name}.ffscore"), "w") as f:
            f.write(f"{characters.p_one_score},{characters.p_two_score}")

    def store_to_existing_file(self, file_name):
        with open(os.path.join("data", f"{file_name}"), "w") as f:
            f.write(f"{characters.p_one_score},{characters.p_two_score}")

    def attack(self, player, y_pos, x_pos):
        if player == self.player_one:
            if characters.p_one_attack_time > characters.p_two_block_time and not characters.p_two_block and not characters.p_two_attack:
                characters.p_one_score += 1
                self.store_to_existing_file(self.score_file)
                self.get_stored_score(self.score_file)
                stdscr.addstr(1, (pw//2) + 10,
                              f"{characters.p_one_score}")
                stdscr.addstr(1, (pw//2) + 20,
                              f"{characters.p_two_score}")
                self.move_to_default(p_one_win, y_pos, x_pos-2)
                self.move_to_default(p_two_win, p_two_y, p_two_x)
                self.draw()
            if characters.p_one_attack_time == characters.p_two_block_time or characters.p_two_attack:
                self.move_to_default(p_one_win, p_one_y, p_one_x)
                self.move_to_default(p_two_win, p_two_y, p_two_x)
                self.draw()
        elif player == self.player_two:
            if characters.p_two_attack_time > characters.p_one_block_time and not characters.p_one_block and not characters.p_one_attack:
                characters.p_two_score += 1
                self.store_to_existing_file(self.score_file)
                self.get_stored_score(self.score_file)
                stdscr.addstr(1, (pw//2) + 10,
                              f"{characters.p_one_score}")
                stdscr.addstr(1, (pw//2) + 20,
                              f"{characters.p_two_score}")
                self.move_to_default(p_two_win, y_pos, x_pos+2,)
                self.move_to_default(p_one_win, p_one_y, p_one_x)
                self.draw()
            if characters.p_two_attack_time == characters.p_one_block_time or characters.p_one_attack:
                self.move_to_default(p_one_win, p_one_y, p_one_x)
                self.move_to_default(p_two_win, p_two_y, p_two_x)
                self.draw()

    def inc_score_p_one(self):
        characters.p_one_score += 1
        self.store_to_existing_file(self.score_file)
        self.get_stored_score(self.score_file)
        stdscr.addstr(1, (pw//2) + 10,
                      f"{characters.p_one_score}")
        stdscr.addstr(1, (pw//2) + 20,
                      f"{characters.p_two_score}")
        self.move_to_default(p_one_win, p_one_y, p_one_x)
        self.move_to_default(p_two_win, p_two_y, p_two_x)
        self.draw()

    def inc_score_p_two(self):
        characters.p_two_score += 1
        self.store_to_existing_file(self.score_file)
        self.get_stored_score(self.score_file)
        stdscr.addstr(1, (pw//2) + 10,
                      f"{characters.p_one_score}")
        stdscr.addstr(1, (pw//2) + 20,
                      f"{characters.p_two_score}")
        self.move_to_default(p_one_win, p_one_y, p_one_x)
        self.move_to_default(p_two_win, p_two_y, p_two_x)
        self.draw()

    def reset_score(self):
        characters.p_one_score = 0
        characters.p_two_score = 0
        self.store_to_existing_file(self.score_file)

    def reset_bool(self, player, element, sec=1/fps):
        time.sleep(sec)
        if player == self.player_one:
            if element is characters.p_one_attack:
                characters.p_one_attack = False
                characters.p_one_in_attack = False
            elif element is characters.p_one_block:
                characters.p_one_block = False
        elif player == self.player_two:
            if element is characters.p_two_attack:
                characters.p_two_attack = False
                characters.p_two_in_attack = False
            elif element is characters.p_two_block:
                characters.p_two_block = False

    def play_sound(self, sound):
        if sound == "attack":
            playsound(os.path.join("sounds", "swod2.wav"))
        elif sound == "block":
            playsound(os.path.join("sounds", "swod1.wav"))


menu_list = ["Resume", "Reload", "Save New", "Save Existing", "Reset",  "Exit"]

help_win = stdscr.derwin(10, 50, 0, 50)
sm_help_win = stdscr.derwin(10, 20, 0, 20)


def print_menu(menu_list, selected_option):
    stdscr.clear()
    help_win.addstr(
        1, 1, "Press 'q' to move left and 'a' to jump left\n Press 'd' to move right and 'e' to jump right\n Press 'z' to attack and 's' to block", COLOR_GREEN)
    help_win.addstr(
        4, 1, "Press 'k' to move left and 'i' to jump left\n Press 'm' to move right and 'p' to jump right\n Press 'o' to attack and 'l' to block", COLOR_YELLOW)
    sm_help_win.addstr(
        1, 1, "Press 't' and 'g'\nto navigate the menu", COLOR_RED)
    for index, option in enumerate(menu_list):
        if index == selected_option:
            stdscr.attron(COLOR_RED)
            stdscr.addstr(index + 1, 1, option)
            stdscr.attroff(COLOR_RED)
        else:
            stdscr.addstr(index + 1, 1, option)

    stdscr.refresh()


mute = False


def loopBg():
    while not mute:
        playsound(os.path.join("sounds", "bg.mp3"))


loopBgThread = threading.Thread(target=loopBg)
loopBgThread.daemon = True
loopBgThread.start()


def game_loop():
    run = True
    global mute

    scene = Scene()
    while run:
        stdscr.clear()
        box_win.clear()
        p_one_win.clear()
        p_two_win.clear()

        # scene = Scene()
        # scene.get_stored_score(scene.score_file)
        scene.draw()

        stdscr.addstr(0, 0, "Press w of pause menu and b to end game",
                      curses.A_REVERSE)
        stdscr.addstr(1, pw//2, "Score:", curses.A_REVERSE)
        stdscr.addstr(
            1, (pw//2) + 10, f"{characters.p_one_score}", COLOR_GREEN)

        stdscr.addstr(
            1, (pw//2) + 20, f"{characters.p_two_score}", COLOR_YELLOW)

        new_p_one_y, new_p_one_x = p_one_win.getbegyx()
        new_p_two_y, new_p_two_x = p_two_win.getbegyx()

        try:
            key = stdscr.getkey()
        except:
            key = None

        if key == "b":
            run = False

        if key == "n":
            mute = not mute

        if key == "w":  # pause

            selected_option = 0
            while True:
                print_menu(menu_list, selected_option)
                try:
                    key = stdscr.getkey()
                except:
                    key = None

                if key == "t" and selected_option > 0:
                    selected_option -= 1

                if key == "g" and selected_option < len(menu_list) - 1:
                    selected_option += 1

                if key == "KEY_ENTER" or key == "\n":
                    if selected_option == 0:
                        break
                    elif selected_option == 1:
                        game_list = os.listdir("data")
                        selected_game = 0
                        while True:
                            stdscr.clear()
                            stdscr.addstr(0, 0, "Saved Games",
                                          curses.A_REVERSE)
                            for index, game in enumerate(game_list):
                                if index == selected_game:
                                    stdscr.attron(COLOR_RED)
                                    stdscr.addstr(index + 1, 1, game)
                                    stdscr.attroff(COLOR_RED)
                                else:
                                    stdscr.addstr(index + 1, 1, game)

                            stdscr.refresh()
                            try:
                                key = stdscr.getkey()
                            except:
                                key = None

                            if key == "t" and selected_game > 0:
                                selected_game -= 1

                            if key == "g" and selected_game < len(game_list) - 1:
                                selected_game += 1

                            if key == "KEY_ENTER" or key == "\n":
                                scene.score_file = game_list[selected_game]
                                scene.get_stored_score(
                                    game_list[selected_game])

                                break
                    elif selected_option == 2:
                        scene.store_score()
                        time.sleep(1)
                        break
                    elif selected_option == 3:
                        game_list = os.listdir("data")
                        selected_game = 0
                        while True:
                            stdscr.clear()
                            stdscr.addstr(0, 0, "Saved Games",
                                          curses.A_REVERSE)
                            for index, game in enumerate(game_list):
                                if index == selected_game:
                                    stdscr.attron(COLOR_RED)
                                    stdscr.addstr(index + 1, 1, game)
                                    stdscr.attroff(COLOR_RED)
                                else:
                                    stdscr.addstr(index + 1, 1, game)

                            stdscr.refresh()
                            try:
                                key = stdscr.getkey()
                            except:
                                key = None

                            if key == "t" and selected_game > 0:
                                selected_game -= 1

                            if key == "g" and selected_game < len(game_list) - 1:
                                selected_game += 1

                            if key == "KEY_ENTER" or key == "\n":
                                # save game
                                scene.store_to_existing_file(
                                    game_list[selected_game])

                                break
                    elif selected_option == 4:
                        scene.reset_score()
                        scene.move_to_default(p_one_win, p_one_y, p_one_x)
                        scene.move_to_default(p_two_win, p_two_y, p_two_x)
                        time.sleep(1)
                        break
                    elif selected_option == 5:
                        time.sleep(1)
                        run = False
                        break

                print_menu(menu_list, selected_option)
                stdscr.refresh()

        if key == "e":
            if new_p_one_y - 2 >= (p_one_y - 2) and (new_p_one_x + 6) < new_p_two_x:
                new_y = new_p_one_y - 2
                scene.move_up(p_one_win, new_p_one_y, new_p_one_x)
                t1 = threading.Thread(target=scene.jump_right, args=(
                    p_one_win, new_y, new_p_one_x))
                t1.start()
            else:
                scene.move_to_default(p_one_win, p_one_y, new_p_one_x)

        if key == "a":
            if new_p_one_y - 2 >= (p_one_y - 2) and (new_p_one_x - 4) > 0:
                new_y = new_p_one_y - 2
                scene.move_up(p_one_win, new_p_one_y, new_p_one_x)
                t2 = threading.Thread(target=scene.jump_left, args=(
                    p_one_win, new_y, new_p_one_x))
                t2.start()

        if key == "d":
            if new_p_one_y - 2 >= (p_one_y - 2) and (new_p_one_x + 4) < new_p_two_x:
                scene.move_right(p_one_win, new_p_one_y, new_p_one_x)

        if key == "q":
            scene.move_left(p_one_win, new_p_one_y, new_p_one_x)

        if key == "p":
            if new_p_two_y - 2 >= (p_two_y - 2) and (new_p_two_x + 4) < pw//2:
                new_y = new_p_two_y - 2
                scene.move_up(p_two_win, new_p_two_y, new_p_two_x)
                t3 = threading.Thread(target=scene.jump_right,
                                      args=(p_two_win, new_y, new_p_two_x))
                t3.start()

        if key == "i":
            if new_p_two_y - 2 >= (p_two_y - 2) and (new_p_two_x) > new_p_one_x + 4:
                new_y = new_p_two_y - 2
                scene.move_up(p_two_win, new_p_two_y, new_p_two_x)
                t4 = threading.Thread(target=scene.jump_left,
                                      args=(p_two_win, new_y, new_p_two_x))
                t4.start()
            else:
                scene.move_to_default(p_two_win, p_two_y, p_two_x)

        if key == "m":
            scene.move_right(p_two_win, new_p_two_y, new_p_two_x)

        if key == "k":
            t7 = threading.Thread(target=scene.move_left,
                                  args=(p_two_win, new_p_two_y, new_p_two_x))
            t7.start()

        # collusions with the box element
        # list of p_one's coordinates
        p_one_coords = []
        for y in range(new_p_one_y, new_p_one_y + 4):
            for x in range(new_p_one_x, new_p_one_x + 4):
                p_one_coords.append((y, x))

        # list of p_two's coordinates
        p_two_coords = []
        for y in range(new_p_two_y, new_p_two_y + 4):
            for x in range(new_p_two_x, new_p_two_x + 4):
                p_two_coords.append((y, x))

        if (new_p_one_y + 3, new_p_one_x + 1) in box_coord:
            scene.inc_score_p_two()
            scene.move_to_default(p_one_win, p_one_y, p_one_x)

        if (new_p_two_y + 3, new_p_two_x) in box_coord:
            scene.inc_score_p_one()
            scene.move_to_default(p_two_win, p_two_y, p_two_x)

        # attacking and blocking
        if key == "z":
            if (new_p_one_x + 4) < new_p_two_x + 1:
                scene.play_sound("attack")
                characters.p_one_block = False
                characters.p_one_attack = True
                characters.p_one_attack_time = time.time()
                scene.move_to_default(p_one_win, p_one_y, new_p_one_x+2)
                if (p_one_y + 3, new_p_one_x + 4) in p_two_coords:
                    scene.attack(scene.player_one, p_one_y, new_p_one_x)
                    t9 = threading.Thread(target=scene.reset_bool, args=(
                        scene.player_one, characters.p_one_attack))
                    t9.start()
            else:
                scene.move_to_default(p_one_win, new_p_one_y, new_p_one_x-2)
                scene.reset_bool(scene.player_one, characters.p_one_attack)

        if key == "s":
            scene.play_sound("block")
            characters.p_one_block_time = time.time()
            characters.p_one_attack = False
            characters.p_one_block = not characters.p_one_block
            characters.p_one_in_attack = False
            if characters.p_one_block_time > characters.p_two_attack_time and (new_p_two_y + 3, new_p_two_x) in p_one_coords:
                scene.move_to_default(p_one_win, p_one_y, new_p_one_x - 2)

        if key == "o":
            scene.play_sound("attack")
            if (new_p_two_x) > new_p_one_x + 3:
                characters.p_two_block = False
                characters.p_two_attack = True
                characters.p_two_attack_time = time.time()
                scene.move_to_default(p_two_win, p_two_y, new_p_two_x-2)
                if (p_two_y + 3, new_p_two_x - 1) in p_one_coords:
                    scene.attack(scene.player_two, p_two_y, new_p_two_x)
                    ta = threading.Thread(target=scene.reset_bool, args=(
                        scene.player_two, characters.p_two_attack))
                    ta.start()
            else:
                scene.move_to_default(p_two_win, new_p_two_y, new_p_two_x+2)
                scene.reset_bool(scene.player_two, characters.p_two_attack)

        if key == "l":
            scene.play_sound("block")
            characters.p_two_block_time = time.time()
            characters.p_two_attack = False
            characters.p_two_block = not characters.p_two_block
            characters.p_two_in_attack = False
            if characters.p_two_block_time > characters.p_one_attack_time and (new_p_one_y + 3, new_p_one_x + 4) in p_two_coords:
                scene.move_to_default(p_two_win, p_two_y, new_p_two_x + 2)

        time.sleep(1/fps)
        pg_win.refresh()
        p_one_win.refresh()
        p_two_win.refresh()
        stdscr.refresh()


curses.endwin()

if __name__ == "__main__":
    game_loop()
