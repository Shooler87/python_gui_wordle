import dearpygui.dearpygui as dpg

dpg.create_context()
with dpg.font_registry():
    with dpg.font("./fonts/Arial.ttf", 30) as font_big:
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Default)
        dpg.add_font_chars([
            0x0105,
            0x0107,
            0x0119,
            0x0142,
            0x0144,
            0x00f3,
            0x015b,
            0x017a,
            0x017c
        ])

    with dpg.font("./fonts/Arial.ttf", 32) as font_small:
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Default)