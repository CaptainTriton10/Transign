from mediapipe import tasks
import customtkinter as ctk
from customtkinter import ThemeManager
from configparser import ConfigParser, NoOptionError, NoSectionError

GLOBALS = {
    "IMG_WIDTH": 480,
    "IMG_HEIGHT": 360,
    "WINDOW_WIDTH": 1080,
    "WINDOW_HEIGHT": 720,
    "PADX": 15,
    "PADY": 15,
    "MAX_REPS": 50,
    "CURSOR_CHAR": "▌",
    "CAM_NUMBERS": [
        "0",
        "1",
    ]
}

THEMES = {
    "Default": "default",
    "Autumn": r"Themes/autumn.json",
    "Breeze": r"Themes/breeze.json",
    "Carrot": r"Themes/carrot.json",
    "Cherry": r"Themes/cherry.json",
    "Coffee": r"Themes/coffee.json",
    "Lavender": r"Themes/lavender.json",
    "Marsh": r"Themes/marsh.json",
    "Metal": r"Themes/metal.json",
    "Midnight": r"Themes/midnight.json",
    "Orange": r"Themes/orange.json",
    "Patina": r"Themes/patina.json",
    "Pink": r"Themes/pink.json",
    "Red": r"Themes/red.json",
    "Rime": r"Themes/rime.json",
    "Rose": r"Themes/rose.json",
    "Sky": r"Themes/sky.json",
    "Violet": r"Themes/violet.json",
    "Yellow": r"Themes/yellow.json"
}

COLOURS = {
    'AliceBlue': '#F0F8FF',
    'AntiqueWhite': '#FAEBD7',
    'AntiqueWhite1': '#FFEFDB',
    'AntiqueWhite2': '#EEDFCC',
    'AntiqueWhite3': '#CDC0B0',
    'AntiqueWhite4': '#8B8378',
    'BlanchedAlmond': '#FFEBCD',
    'BlueViolet': '#8A2BE2',
    'CadetBlue': '#5F9EA0',
    'CadetBlue1': '#98F5FF',
    'CadetBlue2': '#8EE5EE',
    'CadetBlue3': '#7AC5CD',
    'CadetBlue4': '#53868B',
    'CornflowerBlue': '#6495ED',
    'DarkGoldenrod': '#B8860B',
    'DarkGoldenrod1': '#FFB90F',
    'DarkGoldenrod2': '#EEAD0E',
    'DarkGoldenrod3': '#CD950C',
    'DarkGoldenrod4': '#8B6508',
    'DarkGreen': '#006400',
    'DarkKhaki': '#BDB76B',
    'DarkOliveGreen': '#556B2F',
    'DarkOliveGreen1': '#CAFF70',
    'DarkOliveGreen2': '#BCEE68',
    'DarkOliveGreen3': '#A2CD5A',
    'DarkOliveGreen4': '#6E8B3D',
    'DarkOrange': '#FF8C00',
    'DarkOrange1': '#FF7F00',
    'DarkOrange2': '#EE7600',
    'DarkOrange3': '#CD6600',
    'DarkOrange4': '#8B4500',
    'DarkOrchid': '#9932CC',
    'DarkOrchid1': '#BF3EFF',
    'DarkOrchid2': '#B23AEE',
    'DarkOrchid3': '#9A32CD',
    'DarkOrchid4': '#68228B',
    'DarkSalmon': '#E9967A',
    'DarkSeaGreen': '#8FBC8F',
    'DarkSeaGreen1': '#C1FFC1',
    'DarkSeaGreen2': '#B4EEB4',
    'DarkSeaGreen3': '#9BCD9B',
    'DarkSeaGreen4': '#698B69',
    'DarkSlateBlue': '#483D8B',
    'DarkSlateGray1': '#97FFFF',
    'DarkSlateGray2': '#8DEEEE',
    'DarkSlateGray3': '#79CDCD',
    'DarkSlateGray4': '#528B8B',
    'DarkTurquoise': '#00CED1',
    'DarkViolet': '#9400D3',
    'DeepPink2': '#EE1289',
    'DeepPink3': '#CD1076',
    'DeepPink4': '#8B0A50',
    'DeepSkyBlue2': '#00B2EE',
    'DeepSkyBlue3': '#009ACD',
    'DeepSkyBlue4': '#00688B',
    'DodgerBlue2': '#1C86EE',
    'DodgerBlue3': '#1874CD',
    'DodgerBlue4': '#104E8B',
    'FloralWhite': '#FFFAF0',
    'GhostWhite': '#F8F8FF',
    'GreenYellow': '#ADFF2F',
    'HotPink': '#FF69B4',
    'HotPink1': '#FF6EB4',
    'HotPink2': '#EE6AA7',
    'HotPink3': '#CD6090',
    'HotPink4': '#8B3A62',
    'IndianRed': '#CD5C5C',
    'IndianRed1': '#FF6A6A',
    'IndianRed2': '#EE6363',
    'IndianRed3': '#CD5555',
    'IndianRed4': '#8B3A3A',
    'LavenderBlush2': '#EEE0E5',
    'LavenderBlush3': '#CDC1C5',
    'LavenderBlush4': '#8B8386',
    'LawnGreen': '#7CFC00',
    'LemonChiffon2': '#EEE9BF',
    'LemonChiffon3': '#CDC9A5',
    'LemonChiffon4': '#8B8970',
    'LightBlue': '#ADD8E6',
    'LightBlue1': '#BFEFFF',
    'LightBlue2': '#B2DFEE',
    'LightBlue3': '#9AC0CD',
    'LightBlue4': '#68838B',
    'LightCoral': '#F08080',
    'LightCyan2': '#D1EEEE',
    'LightCyan3': '#B4CDCD',
    'LightCyan4': '#7A8B8B',
    'LightGoldenrod': '#EEDD82',
    'LightGoldenrod1': '#FFEC8B',
    'LightGoldenrod2': '#EEDC82',
    'LightGoldenrod3': '#CDBE70',
    'LightGoldenrod4': '#8B814C',
    'LightGoldenrodYellow': '#FAFAD2',
    'LightPink': '#FFB6C1',
    'LightPink1': '#FFAEB9',
    'LightPink2': '#EEA2AD',
    'LightPink3': '#CD8C95',
    'LightPink4': '#8B5F65',
    'LightSalmon2': '#EE9572',
    'LightSalmon3': '#CD8162',
    'LightSalmon4': '#8B5742',
    'LightSeaGreen': '#20B2AA',
    'LightSkyBlue': '#87CEFA',
    'LightSkyBlue1': '#B0E2FF',
    'LightSkyBlue2': '#A4D3EE',
    'LightSkyBlue3': '#8DB6CD',
    'LightSkyBlue4': '#607B8B',
    'LightSlateBlue': '#8470FF',
    'LightSteelBlue': '#B0C4DE',
    'LightSteelBlue1': '#CAE1FF',
    'LightSteelBlue2': '#BCD2EE',
    'LightSteelBlue3': '#A2B5CD',
    'LightSteelBlue4': '#6E7B8B',
    'LightYellow2': '#EEEED1',
    'LightYellow3': '#CDCDB4',
    'LightYellow4': '#8B8B7A',
    'LimeGreen': '#32CD32',
    'MediumOrchid': '#BA55D3',
    'MediumOrchid1': '#E066FF',
    'MediumOrchid2': '#D15FEE',
    'MediumOrchid3': '#B452CD',
    'MediumOrchid4': '#7A378B',
    'MediumPurple': '#9370DB',
    'MediumPurple1': '#AB82FF',
    'MediumPurple2': '#9F79EE',
    'MediumPurple3': '#8968CD',
    'MediumPurple4': '#5D478B',
    'MediumSeaGreen': '#3CB371',
    'MediumSlateBlue': '#7B68EE',
    'MediumSpringGreen': '#00FA9A',
    'MediumTurquoise': '#48D1CC',
    'MediumVioletRed': '#C71585',
    'MintCream': '#F5FFFA',
    'MistyRose2': '#EED5D2',
    'MistyRose3': '#CDB7B5',
    'MistyRose4': '#8B7D7B',
    'NavajoWhite2': '#EECFA1',
    'NavajoWhite3': '#CDB38B',
    'NavajoWhite4': '#8B795E',
    'OldLace': '#FDF5E6',
    'OliveDrab': '#6B8E23',
    'OliveDrab1': '#C0FF3E',
    'OliveDrab2': '#B3EE3A',
    'OliveDrab4': '#698B22',
    'OrangeRed2': '#EE4000',
    'OrangeRed3': '#CD3700',
    'OrangeRed4': '#8B2500',
    'PaleGoldenrod': '#EEE8AA',
    'PaleGreen': '#98FB98',
    'PaleGreen1': '#9AFF9A',
    'PaleGreen3': '#7CCD7C',
    'PaleGreen4': '#548B54',
    'PaleTurquoise': '#AFEEEE',
    'PaleTurquoise1': '#BBFFFF',
    'PaleTurquoise2': '#AEEEEE',
    'PaleTurquoise3': '#96CDCD',
    'PaleTurquoise4': '#668B8B',
    'PaleVioletRed': '#DB7093',
    'PaleVioletRed1': '#FF82AB',
    'PaleVioletRed2': '#EE799F',
    'PaleVioletRed3': '#CD687F',
    'PaleVioletRed4': '#8B475D',
    'PeachPuff2': '#EECBAD',
    'PeachPuff3': '#CDAF95',
    'PeachPuff4': '#8B7765',
    'PowderBlue': '#B0E0E6',
    'RosyBrown': '#BC8F8F',
    'RosyBrown1': '#FFC1C1',
    'RosyBrown2': '#EEB4B4',
    'RosyBrown3': '#CD9B9B',
    'RosyBrown4': '#8B6969',
    'RoyalBlue': '#4169E1',
    'RoyalBlue1': '#4876FF',
    'RoyalBlue2': '#436EEE',
    'RoyalBlue3': '#3A5FCD',
    'RoyalBlue4': '#27408B',
    'SandyBrown': '#F4A460',
    'SeaGreen1': '#54FF9F',
    'SeaGreen2': '#4EEE94',
    'SeaGreen3': '#43CD80',
    'SkyBlue': '#87CEEB',
    'SkyBlue1': '#87CEFF',
    'SkyBlue2': '#7EC0EE',
    'SkyBlue3': '#6CA6CD',
    'SkyBlue4': '#4A708B',
    'SlateBlue': '#6A5ACD',
    'SlateBlue1': '#836FFF',
    'SlateBlue2': '#7A67EE',
    'SlateBlue3': '#6959CD',
    'SlateBlue4': '#473C8B',
    'SlateGray1': '#C6E2FF',
    'SlateGray2': '#B9D3EE',
    'SlateGray3': '#9FB6CD',
    'SlateGray4': '#6C7B8B',
    'SpringGreen2': '#00EE76',
    'SpringGreen3': '#00CD66',
    'SpringGreen4': '#008B45',
    'SteelBlue': '#4682B4',
    'SteelBlue1': '#63B8FF',
    'SteelBlue2': '#5CACEE',
    'SteelBlue3': '#4F94CD',
    'SteelBlue4': '#36648B',
    'VioletRed': '#D02090',
    'VioletRed1': '#FF3E96',
    'VioletRed2': '#EE3A8C',
    'VioletRed3': '#CD3278',
    'VioletRed4': '#8B2252',
    'aquamarine2': '#76EEC6',
    'aquamarine4': '#458B74',
    'azure2': '#E0EEEE',
    'azure3': '#C1CDCD',
    'azure4': '#838B8B',
    'beige': '#F5F5DC',
    'bisque2': '#EED5B7',
    'bisque3': '#CDB79E',
    'bisque4': '#8B7D6B',
    'blue2': '#0000EE',
    'brown': '#A52A2A',
    'brown1': '#FF4040',
    'brown2': '#EE3B3B',
    'brown3': '#CD3333',
    'brown4': '#8B2323',
    'burlywood': '#DEB887',
    'burlywood1': '#FFD39B',
    'burlywood2': '#EEC591',
    'burlywood3': '#CDAA7D',
    'burlywood4': '#8B7355',
    'chartreuse2': '#76EE00',
    'chartreuse3': '#66CD00',
    'chartreuse4': '#458B00',
    'chocolate': '#D2691E',
    'chocolate1': '#FF7F24',
    'chocolate2': '#EE7621',
    'chocolate3': '#CD661D',
    'coral': '#FF7F50',
    'coral1': '#FF7256',
    'coral2': '#EE6A50',
    'coral3': '#CD5B45',
    'coral4': '#8B3E2F',
    'cornsilk2': '#EEE8CD',
    'cornsilk3': '#CDC8B1',
    'cornsilk4': '#8B8878',
    'crymson': '#DC143C',
    'cyan2': '#00EEEE',
    'cyan3': '#00CDCD',
    'firebrick': '#B22222',
    'firebrick1': '#FF3030',
    'firebrick2': '#EE2C2C',
    'firebrick3': '#CD2626',
    'firebrick4': '#8B1A1A',
    'gainsboro': '#DCDCDC',
    'gold2': '#EEC900',
    'gold3': '#CDAD00',
    'gold4': '#8B7500',
    'goldenrod': '#DAA520',
    'goldenrod1': '#FFC125',
    'goldenrod2': '#EEB422',
    'goldenrod3': '#CD9B1D',
    'goldenrod4': '#8B6914',
    'green2': '#00EE00',
    'green3': '#00CD00',
    'green4': '#008B00',
    'gray': '#BEBEBE',
    'gray1': '#030303',
    'gray10': '#1A1A1A',
    'gray11': '#1C1C1C',
    'gray12': '#1F1F1F',
    'gray13': '#212121',
    'gray14': '#242424',
    'gray15': '#262626',
    'gray16': '#292929',
    'gray17': '#2B2B2B',
    'gray18': '#2E2E2E',
    'gray19': '#303030',
    'gray2': '#050505',
    'gray20': '#333333',
    'gray21': '#363636',
    'gray22': '#383838',
    'gray23': '#3B3B3B',
    'gray24': '#3D3D3D',
    'gray25': '#404040',
    'gray26': '#424242',
    'gray27': '#454545',
    'gray28': '#474747',
    'gray29': '#4A4A4A',
    'gray3': '#080808',
    'gray30': '#4D4D4D',
    'gray31': '#4F4F4F',
    'gray32': '#525252',
    'gray33': '#545454',
    'gray34': '#575757',
    'gray35': '#595959',
    'gray36': '#5C5C5C',
    'gray37': '#5E5E5E',
    'gray38': '#616161',
    'gray39': '#636363',
    'gray4': '#0A0A0A',
    'gray40': '#666666',
    'gray42': '#6B6B6B',
    'gray43': '#6E6E6E',
    'gray44': '#707070',
    'gray45': '#737373',
    'gray46': '#757575',
    'gray47': '#787878',
    'gray48': '#7A7A7A',
    'gray49': '#7D7D7D',
    'gray5': '#0D0D0D',
    'gray50': '#7F7F7F',
    'gray51': '#828282',
    'gray52': '#858585',
    'gray53': '#878787',
    'gray54': '#8A8A8A',
    'gray55': '#8C8C8C',
    'gray56': '#8F8F8F',
    'gray57': '#919191',
    'gray58': '#949494',
    'gray59': '#969696',
    'gray6': '#0F0F0F',
    'gray60': '#999999',
    'gray61': '#9C9C9C',
    'gray62': '#9E9E9E',
    'gray63': '#A1A1A1',
    'gray64': '#A3A3A3',
    'gray65': '#A6A6A6',
    'gray66': '#A8A8A8',
    'gray67': '#ABABAB',
    'gray68': '#ADADAD',
    'gray69': '#B0B0B0',
    'gray7': '#121212',
    'gray70': '#B3B3B3',
    'gray71': '#B5B5B5',
    'gray72': '#B8B8B8',
    'gray73': '#BABABA',
    'gray74': '#BDBDBD',
    'gray75': '#BFBFBF',
    'gray76': '#C2C2C2',
    'gray77': '#C4C4C4',
    'gray78': '#C7C7C7',
    'gray79': '#C9C9C9',
    'gray8': '#141414',
    'gray80': '#CCCCCC',
    'gray81': '#CFCFCF',
    'gray82': '#D1D1D1',
    'gray83': '#D4D4D4',
    'gray84': '#D6D6D6',
    'gray85': '#D9D9D9',
    'gray86': '#DBDBDB',
    'gray87': '#DEDEDE',
    'gray88': '#E0E0E0',
    'gray89': '#E3E3E3',
    'gray9': '#171717',
    'gray90': '#E5E5E5',
    'gray91': '#E8E8E8',
    'gray92': '#EBEBEB',
    'gray93': '#EDEDED',
    'gray94': '#F0F0F0',
    'gray95': '#F2F2F2',
    'gray97': '#F7F7F7',
    'gray98': '#FAFAFA',
    'gray99': '#FCFCFC',
    'honeydew2': '#E0EEE0',
    'honeydew3': '#C1CDC1',
    'honeydew4': '#838B83',
    'indigo': '#4B0082',
    'ivory2': '#EEEEE0',
    'ivory3': '#CDCDC1',
    'ivory4': '#8B8B83',
    'khaki': '#F0E68C',
    'khaki1': '#FFF68F',
    'khaki2': '#EEE685',
    'khaki3': '#CDC673',
    'khaki4': '#8B864E',
    'lavender': '#E6E6FA',
    'linen': '#FAF0E6',
    'magenta2': '#EE00EE',
    'magenta3': '#CD00CD',
    'maroon': '#B03060',
    'maroon1': '#FF34B3',
    'maroon2': '#EE30A7',
    'maroon3': '#CD2990',
    'maroon4': '#8B1C62',
    'moccasin': '#FFE4B5',
    'olive': '#808000',
    'orange2': '#EE9A00',
    'orange3': '#CD8500',
    'orange4': '#8B5A00',
    'orchid': '#DA70D6',
    'orchid1': '#FF83FA',
    'orchid2': '#EE7AE9',
    'orchid3': '#CD69C9',
    'orchid4': '#8B4789',
    'pink': '#FFC0CB',
    'pink1': '#FFB5C5',
    'pink2': '#EEA9B8',
    'pink3': '#CD919E',
    'pink4': '#8B636C',
    'plum': '#DDA0DD',
    'plum1': '#FFBBFF',
    'plum2': '#EEAEEE',
    'plum3': '#CD96CD',
    'plum4': '#8B668B',
    'purple': '#A020F0',
    'purple1': '#9B30FF',
    'purple2': '#912CEE',
    'purple3': '#7D26CD',
    'purple4': '#551A8B',
    'red2': '#EE0000',
    'red3': '#CD0000',
    'salmon': '#FA8072',
    'salmon1': '#FF8C69',
    'salmon2': '#EE8262',
    'salmon3': '#CD7054',
    'salmon4': '#8B4C39',
    'seashell2': '#EEE5DE',
    'seashell3': '#CDC5BF',
    'seashell4': '#8B8682',
    'sienna': '#A0522D',
    'sienna1': '#FF8247',
    'sienna2': '#EE7942',
    'sienna3': '#CD6839',
    'sienna4': '#8B4726',
    'silver': '#C0C0C0',
    'snow2': '#EEE9E9',
    'snow3': '#CDC9C9',
    'snow4': '#8B8989',
    'tan': '#D2B48C',
    'tan1': '#FFA54F',
    'tan2': '#EE9A49',
    'tan4': '#8B5A2B',
    'teal': '#008080',
    'thistle': '#D8BFD8',
    'thistle1': '#FFE1FF',
    'thistle2': '#EED2EE',
    'thistle3': '#CDB5CD',
    'thistle4': '#8B7B8B',
    'tomato2': '#EE5C42',
    'tomato3': '#CD4F39',
    'tomato4': '#8B3626',
    'turquoise': '#40E0D0',
    'turquoise1': '#00F5FF',
    'turquoise2': '#00E5EE',
    'turquoise3': '#00C5CD',
    'turquoise4': '#00868B',
    'violet': '#EE82EE',
    'wheat': '#F5DEB3',
    'wheat1': '#FFE7BA',
    'wheat2': '#EED8AE',
    'wheat3': '#CDBA96',
    'wheat4': '#8B7E66',
    'yellow2': '#EEEE00',
    'yellow3': '#CDCD00',
    'yellow4': '#8B8B00'}


# region Functions

# Unused, but crops image to hand with an offset
def CropToBounds(image, x_landmarks, y_landmarks):
    offset = 40

    # Gets pixel values of edge crops with added offset
    left = int(min(x_landmarks) * 640) - offset
    right = int(max(x_landmarks) * 640) + offset
    bottom = int(max(y_landmarks) * 480) + offset
    upper = int(min(y_landmarks) * 480) - offset

    cropped_image = image.crop((left, upper, right, bottom))
    return cropped_image


# Converts hex code string to rgb tuple
def HexToRgb(hex_code: str) -> (int, int, int):
    hex_code = hex_code.lstrip("#")

    # Found from https://stackoverflow.com/questions/29643352/converting-hex-to-rgb-value-in-python
    rgb = tuple(int(hex_code[i:i + 2], 16) for i in (0, 2, 4))

    return rgb


# Gets value from config.ini file
def GetConfig(section, name, config_file="config.ini"):
    config = ConfigParser()
    value = None
    try:
        config.read(config_file)

        value = config.get(section, name)
        return value

    # Error if value not found
    except NoSectionError or NoOptionError as e:
        print(f"Option or file not found: {e}")


# Updates config.ini file
def SetConfig(section, name, value, config_file="config.ini"):
    config = ConfigParser()
    try:
        config.read(config_file)
        config.set(section, name, value)

        with open(config_file, "w") as updated_file:
            config.write(updated_file)


    except NoSectionError or NoOptionError as e:
        print(f"Option or file not found: {e}")


# Gets dark colour from frame
def GetFrameColour() -> str:
    # Widget to be used for colour sampling
    widget = "CTkFrame"
    option = "fg_color"
    dark_factor = 0.9
    mode = 0 if ctk.get_appearance_mode() == "light" else 1  # Gets light/dark as 0 or 1
    theme = ThemeManager.theme

    base_colour: str = None

    # Sets it as hex value
    try:
        if "#" in theme[widget][option][mode]:
            base_colour = theme[widget][option][mode]

        else:
            base_colour = COLOURS[theme[widget][option][mode]]

    # If key not found
    except KeyError:
        print(f"Colour key not found for: {widget} > {option} > {ctk.get_appearance_mode()}")

    # If there is no error
    else:
        hex_code = HexToRgb(base_colour)
        dark_color = tuple([int(i * dark_factor) for i in hex_code])

        # Found from https://www.codespeedy.com/convert-rgb-to-hex-color-code-in-python/
        hex_dark_color = "#" + ("%02x%02x%02x" % dark_color).upper()
        return hex_dark_color


# endregion

# region Mediapipe

# .task model path
MODEL_PATH = r"asl_model_v3.task"

with open(MODEL_PATH, "rb") as file:
    model = file.read()

# Prerequisites for mediapipe gesture recognition
BaseOptions = tasks.BaseOptions
GestureRecognizer = tasks.vision.GestureRecognizer
GestureRecognizerOptions = tasks.vision.GestureRecognizerOptions
GestureRecognizerResult = tasks.vision.GestureRecognizerResult
VisionRunningMode = tasks.vision.RunningMode


def GetOptions(callback):
    # Options for gesture recogniser
    options = GestureRecognizerOptions(
        base_options=BaseOptions(model_asset_buffer=model),
        running_mode=VisionRunningMode.LIVE_STREAM,
        result_callback=callback
    )

    return options

# endregion
