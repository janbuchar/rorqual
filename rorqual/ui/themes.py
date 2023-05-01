from textual.design import ColorSystem

nord_colors = {
    "polar_night_0": "#2E3440",
    "polar_night_1": "#3B4252",
    "polar_night_2": "#434C5E",
    "polar_night_3": "#4C566A",
    "snow_storm_4": "#D8DEE9",
    "snow_storm_5": "#E5E9F0",
    "snow_storm_6": "#ECEFF4",
    "frost_7": "#8FBCBB",
    "frost_8": "#88C0D0",
    "frost_9": "#81A1C1",
    "frost_10": "#5E81AC",
    "aurora_red_11": "#BF616A",
    "aurora_orange_12": "#D08770",
    "aurora_yellow_13": "#EBCB8B",
    "aurora_green_14": "#A3BE8C",
    "aurora_magenta_15": "#B48EAD",
}

THEMES = {
    "nord": {
        "dark": ColorSystem(
            primary=nord_colors["frost_9"],
            secondary=nord_colors["frost_8"],
            background=nord_colors["polar_night_0"],
            surface=nord_colors["polar_night_1"],
            panel=nord_colors["polar_night_3"],
            success=nord_colors["aurora_green_14"],
            warning=nord_colors["aurora_yellow_13"],
            error=nord_colors["aurora_red_11"],
            dark=True,
        ),
        "light": ColorSystem(
            primary=nord_colors["frost_9"],
            secondary=nord_colors["frost_8"],
            background=nord_colors["polar_night_0"],
            surface=nord_colors["polar_night_1"],
            panel=nord_colors["polar_night_3"],
            success=nord_colors["aurora_green_14"],
            warning=nord_colors["aurora_yellow_13"],
            error=nord_colors["aurora_red_11"],
            dark=False,
        ),
    }
}
