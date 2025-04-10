import dearpygui.dearpygui as dpg
import threading
import random
import string
import time
from fonts import font_big


from dearpygui.dearpygui import mvKey_A, mvKey_RAlt

from settings import ROWS, WIDTH, KB_LAYOUT, ERROR_LABEL_HEIGHT


class WordleGame:

    def __init__(self):
        self.row_index = 0
        self.button_index = 0
        self.popular_words = []
        self.valid_words = []
        self.user_answer = []
        self.buttons_dict = {}
        self.random_word = ""
        self.game_state = "playing"
        self.in_word_letters = set()
        self.size = 12
        self.tile_area = None

    def show_error_popup(self, message, pos):
        dpg.set_item_label("error_popup", message)
        dpg.set_item_pos("error_popup", pos)
        dpg.configure_item("error_popup", show=True)

        threading.Thread(target=self.hide_error_popup, args=(2.0,)).start()

    def hide_error_popup(self, delay):
        time.sleep(delay)
        dpg.configure_item("error_popup", show=False)

    def pick_word(self):
        with open("valid_words.txt", "r+b") as file:
            words_list = file.read().splitlines()
            self.valid_words = [str(words, "UTF-8") for words in words_list if len(str(words, "UTF-8")) == self.size]

        with open("popular_words.txt", "r+b") as file:
            words_list = file.read().splitlines()
            self.popular_words = [str(words, "UTF-8") for words in words_list if len(str(words, "UTF-8")) == self.size]
            self.random_word = random.choice(self.popular_words)

            print(f"Word selected: {self.random_word}")

    # Fix from https://github.com/pixegami/python-wordle
    def verify_answer(self):
        user_answer = ''.join(self.user_answer)
        secret_word_letters = list(self.random_word)
        correct_positions = set()

        result = ["ABSENT"] * len(secret_word_letters)

        # Check for correct letters in correct positions and mark their positions.
        for i, letter in enumerate(user_answer):
            if letter == secret_word_letters[i]:
                correct_positions.add(i)
                result[i] = "CORRECT"
                # Void out the correctly guessed letter.
                secret_word_letters[i] = "*"

        # Check for correct letters in incorrect positions and mark them.
        for i, letter in enumerate(user_answer):
            if result[i] == "CORRECT":  # Skip letters already marked green.
                continue
            elif letter in secret_word_letters:
                result[i] = "INWORD"
                # Void out the guessed letter.
                secret_word_letters[secret_word_letters.index(letter)] = "*"

        # Mark remaining correct letters.
        for i, letter in enumerate(user_answer):
            if result[i] == "ABSENT" and letter in secret_word_letters:
                result[i] = "CORRECT"
                # Void out the correctly guessed letter.
                secret_word_letters[secret_word_letters.index(letter)] = "*"

        # Mark the buttons according to the result array.
        for i, color in enumerate(result):
            button_to_update = self.buttons_dict.get(i)
            if color == "CORRECT":
                self.mark_correct_guess(
                    button_to_update, user_answer[i])
            elif color == "INWORD":
                self.mark_in_word_guess(
                    button_to_update, user_answer[i])
            else:
                self.mark_incorrect_position(
                    button_to_update, user_answer[i])

        if len(correct_positions) == len(self.random_word):
            self.handle_game_won(correct_positions)

    def mark_incorrect_position(self, button, letter):
        dpg.bind_item_theme(button, "absent_theme")
        if letter in self.in_word_letters: return
        dpg.bind_item_theme(f"{letter}", "key_absent_theme")
    
    def mark_correct_guess(self, button, letter):
        print("mark_correct_guess")
        dpg.bind_item_theme(button, "correct_theme")
        dpg.bind_item_theme(f"{letter}", "key_correct_theme")

    def mark_in_word_guess(self, button, letter):
        self.in_word_letters.add(letter)
        dpg.bind_item_theme(button, "in_word_theme")
        dpg.bind_item_theme(f"{letter}", "key_in_word_theme")

    def handle_game_won(self, correct_positions):
        # dpg.set_item_label("logo", "Click to restart")
        self.show_error_popup("Splendid", [20, ERROR_LABEL_HEIGHT])
        self.game_state = "won"

    def keyboard_btn_pressed(self, sender):
        if self.game_state != "playing":
            return

        if len(self.user_answer) < self.size:
            key_pressed = dpg.get_item_label(sender)
            self.user_answer.append(key_pressed)

            self.update_game_ui(key_pressed)
            print(f"Pressed: {key_pressed}, added to list: {self.user_answer}")
        else:
            self.user_answer = self.user_answer[:self.size]
            print(f"Reached the limit of available space. {self.user_answer}")

    def key_press_handler(self, sender, app_data):
        app_data -= 449
        print("key:", app_data)

        if self.game_state != "playing":
            return
        elif app_data == 76:  # Enter key
            print("etnter")
            wordle_game.enter_key_button(sender)
        elif app_data == 74:  # Backspace key
            wordle_game.del_key_button(sender)


        if len(self.user_answer) < self.size:
            if 97 <= app_data <= 122:
                if dpg.is_key_down(mvKey_RAlt):
                    letter = chr(app_data)

                    if letter == 'a':
                        app_data = 261
                    elif letter == 'c':
                        app_data = 263
                    elif letter == 'e':
                        app_data = 281
                    elif letter == 'l':
                        app_data = 322
                    elif letter == 'n':
                        app_data = 324
                    elif letter == 'o':
                        app_data = 243
                    elif letter == 's':
                        app_data = 347
                    elif letter == 'x':
                        app_data = 378
                    elif letter == 'z':
                        app_data = 380

                key_pressed = chr(app_data)
                print("kp", key_pressed)
                self.user_answer.append(key_pressed)
                wordle_game.update_game_ui(key_pressed)
        else:
            self.user_answer = self.user_answer[:self.size]

    def enter_key_button(self, sender):
        answer = ''.join(self.user_answer)

        if self.game_state != "playing":
            return

        elif self.button_index == self.size:
            print(f"Row {self.row_index} completed!")

            if self.row_index == ROWS:
                print("All rows completed!")

            if answer in self.valid_words:
                self.verify_answer()
                self.row_index += 1
                self.button_index = 0
                self.user_answer.clear()

            else:
                self.show_error_popup("Not in word list", [20, ERROR_LABEL_HEIGHT])
                print(f"Invalid word, user answer: {self.user_answer} {answer}")

        else:
            self.show_error_popup("Not enough letters", [20, ERROR_LABEL_HEIGHT])
            print(f"Enter {self.size} letters in the current row. {self.user_answer}")

        if self.row_index >= ROWS:
            if self.game_state == "won":
                pass
            else:
                self.show_error_popup(
                    f"The words was: {self.random_word}", [20, ERROR_LABEL_HEIGHT])
                # dpg.set_item_label("logo", "Click to restart")
                self.game_state = "lost"

        else:
            print(f"Reached the limit of available space. {self.user_answer}")

    def del_key_button(self, sender):
        if self.game_state != "playing":
            return
        elif self.button_index > 0:
            self.button_index -= 1
            self.user_answer.pop()
            button_to_update = self.buttons_dict.get(self.button_index)
            print(f"Deleted last letter, new user answer: {self.user_answer}")

            if button_to_update:
                dpg.set_item_label(button_to_update, "")
                dpg.bind_item_theme(button_to_update, "tile_theme")

        else:
            self.user_answer = []
            print("No letters to delete.")

    def update_game_ui(self, key_pressed):
        if len(self.user_answer) <= self.size:
            if self.button_index < self.size:
                button_to_update = dpg.get_item_alias(
                    f"#{self.button_index + self.row_index * self.size}_key")
                if not dpg.get_item_label(button_to_update):
                    dpg.set_item_label(button_to_update, key_pressed)
                    self.button_index += 1
                    self.buttons_dict[self.button_index - 1] = button_to_update
                    print(f"""Letter: {key_pressed}, added to button #{
                          self.button_index} in row {self.row_index}""")
                    if self.button_index == self.size:
                        print("Row completed!")
        else:
            print(f"Reached the limit of available space. {self.user_answer}")

    def restart(self, sender, app_data, user_data:int):
        size = user_data
        # remove old rows
        for key, value in dpg.get_item_children("tile_area").items():
            if len(value) > 0:
                for v in value:
                    dpg.delete_item(v)

        dpg.bind_item_theme(f"size_chooser_{wordle_game.size}", "keyboard_theme")
        self.__init__()
        self.size = size
        dpg.bind_item_theme(f"size_chooser_{wordle_game.size}", "size_chooser_selected_theme")
        self.add_tiles()
        print("size:", size)
        self.pick_word()

        print("Game restarted!")

        # Restart keyboard state
        for i in KB_LAYOUT:
            for letter in i:
                if letter == "ENTER" or letter == "DEL": continue
                dpg.bind_item_theme(f"{letter}", "keyboard_theme")


    def add_tiles(self):
        for row in range(ROWS):
            group = dpg.add_group(horizontal=True, width=0, tag=f"tile_row_{row}", parent="tile_area")
            dpg.add_spacer(width=(WIDTH - wordle_game.size * 72) // 2, parent=group)
            for col in range(wordle_game.size):
                tile = dpg.add_button(label="", width=61, height=61, tag=f"#{row * wordle_game.size + col}_key",
                                      parent=group)
                dpg.bind_item_theme(tile, "tile_theme")
                dpg.bind_item_font(tile, font_big)

wordle_game = WordleGame()
