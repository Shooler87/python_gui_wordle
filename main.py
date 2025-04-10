from functions import WordleGame
from gui import dpg, logo, keyboard, keyboard_action, wordle_game, error_popup, size_chooser
from settings import ROWS, WIDTH, HEIGHT, KB_LAYOUT, ERROR_LABEL_HEIGHT

# Main window
with dpg.window(tag="Root"):
    # Logo
    with dpg.group(horizontal=True, width=-1):
        logo("Wordle.py")

    dpg.add_separator(), dpg.add_spacer(height=10)

    with dpg.group(horizontal=True, width=0):
        spacer_width = (WIDTH - 9 * 70) // 2
        dpg.add_spacer(width=spacer_width)
        for size in range(4, 13):
            size_chooser(size, wordle_game.size == size)
    dpg.add_spacer(height=10)

    dpg.add_separator(), dpg.add_spacer(height=10)

    # Create Tiles module
    dpg.add_group(width=0, tag="tile_area")
    wordle_game.add_tiles()

    dpg.add_spacer(height=10)

    # Create keyboard module
    for row_index, row in enumerate(KB_LAYOUT):
        with dpg.group(horizontal=True):
            num_buttons = len(row)
            if row_index == 2:
                spacer_width = (WIDTH - num_buttons * 78) // 2
            else:
                spacer_width = (WIDTH - num_buttons * 70) // 2

            dpg.add_spacer(width=spacer_width)

            for key in row:
                if key == "ENTER":
                    keyboard_action(key, callback=wordle_game.enter_key_button)
                elif key == "DEL":
                    keyboard_action(key, callback=wordle_game.del_key_button)
                else:
                    keyboard(key)

    with dpg.group(tag="#error_popup_group"):
        error_popup(f"Error popup", pos=[230, -ERROR_LABEL_HEIGHT], tag="error_popup")

# Keyboard handle
with dpg.handler_registry():
    dpg.add_key_press_handler(callback=wordle_game.key_press_handler)

dpg.set_primary_window("Root", True)
dpg.create_viewport(title="Wordle.py", width=WIDTH, height=HEIGHT, resizable=False,
                    small_icon="./appicon.ico", large_icon="./appicon.ico")
dpg.show_viewport()
dpg.setup_dearpygui()
dpg.start_dearpygui()
dpg.destroy_context()
