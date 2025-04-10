from themes import setup_themes
from functions import *
from settings import ERROR_LABEL_HEIGHT
from fonts import font_big, font_small

wordle_game.pick_word()
dpg.create_context()
setup_themes()


def logo(text):
    logo = dpg.add_button(label=text, tag="logo", width=300, height=50)
    dpg.bind_item_theme(logo, "logo_theme")
    dpg.bind_item_font(logo, font_big)


def size_chooser(size, selected = False):
    size_btn = dpg.add_button(label=str(size), width=56, height=56, tag=f"size_chooser_{size}", callback=wordle_game.restart, user_data=size)
    if selected:
        dpg.bind_item_theme(size_btn, "size_chooser_selected_theme")
    else:
        dpg.bind_item_theme(size_btn, "keyboard_theme")
    dpg.bind_item_font(size_btn, font_small)


def keyboard(text):
    keyboard = dpg.add_button(
    label=text, width=58, height=58, tag=text, callback=wordle_game.keyboard_btn_pressed)
    dpg.bind_item_theme(keyboard, "keyboard_theme")
    dpg.bind_item_font(keyboard, font_big)


def keyboard_action(text, callback):
    if text == "ENTER":
        keyboard_action = dpg.add_button(label=text, width=120, height=58, callback=callback)
    else:
        keyboard_action = dpg.add_button(label=text, width=65, height=58, callback=callback)
    dpg.bind_item_theme(keyboard_action, "keyboard_theme")
    dpg.bind_item_font(keyboard_action, font_big)


def error_popup(text, pos, tag):
    error_popup = dpg.add_button(label=text, width=-1, height=ERROR_LABEL_HEIGHT, pos=pos, tag=tag)
    dpg.bind_item_theme(error_popup, "error_popup_theme")
    dpg.bind_item_font(error_popup, font_big)