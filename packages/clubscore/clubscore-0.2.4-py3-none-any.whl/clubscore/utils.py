from PIL import Image, ImageDraw, ImageFont
import xml.etree.ElementTree as ET
import difflib
import os
import requests
import logging
import os
from bs4 import BeautifulSoup
import glob

# set the logging level (e.g. DEBUG, INFO, WARNING, ERROR)
logging.basicConfig(level=logging.INFO)

"""
Prende un file in formato PNG e lo colora completamente di
un colore specifico in rgb.
Colore di default è bianco
"""


def coloraPNG(img, new_r=255, new_g=255, new_b=255):
    img = img.convert("RGBA")
    pixels = img.load()
    for i in range(img.width):
        for j in range(img.height):
            r, g, b, a = pixels[i, j]
            # set the color of the pixel
            pixels[i, j] = (new_r, new_g, new_b, a)
    return img


"""
Restituisce le coordinate precise per centrare su asse x e y
"""

def align_center_x():
    pass

def align_center_y():
    pass


"""
Dato un font di partenza (main_font) e un testo, indica qual è la dimensione ideale
per rispettare i vincoli di larghezza max_width
"""


def getIdealFont(image, main_font, testo, size, max_width):
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(main_font, size)
    w = draw.textlength(testo, font)

    while w > max_width:
        font = ImageFont.truetype(main_font, font.size - 1)
        w = draw.textlength(testo, font)

    return font


"""

"""
#sostituisce il . locale di un template con quello assoluto
def fix_path(current_path, template_path):
    if 'ENV' in os.environ and os.environ['ENV'] == 'testing':
        current_path = os.path.dirname(template_path)[3:] + current_path[1:]
    else:
        current_path = os.path.dirname(template_path) + current_path[1:]

    return current_path


def print_file_tree(folder_path, indent=''):
    all_files = glob.glob(folder_path + "/**/*", recursive=True)

    # Create a dictionary to store files grouped by folder_name
    file_tree = {}

    for file_path in all_files:
        if os.path.isfile(file_path):
            folder_name = os.path.basename(os.path.dirname(file_path))
            file_name = os.path.basename(file_path)

            # Group files by folder_name in the file_tree dictionary
            if folder_name not in file_tree:
                file_tree[folder_name] = []
            file_tree[folder_name].append(file_name.replace(".png",""))

    s = ""
    # Recursively print the file tree structure
    for folder_name, files in file_tree.items():
        s += indent + folder_name + '/' +'\n'
        print(indent + folder_name + '/')
        for file_name in sorted(files):
            print(indent + '  ' + file_name)
            s += indent + '  ' + file_name + '\n'

        s += "\n"

    return s


def get_all_teams(folder_path):
    # Utilizza glob in modo ricorsivo per trovare tutti i file nella cartella e nelle sottocartelle
    all_files = glob.glob(folder_path + "/**/*.png", recursive=True)

    return(all_files)

def fix_transparency_issue(png):
    image = Image.open(png)
    print(png, image.mode)
    image = image.convert("RGBA")

    pixel_data = image.getdata()
    new_pixel_data = []

    for pixel in pixel_data:
        r, g, b, a = pixel

        if a == 0 and (r != 0 or g != 0 or b != 0):
            new_pixel_data.append((r, g, b, 255))
        else:
            new_pixel_data.append(pixel)

    new_image = Image.new("RGBA", image.size)
    new_image.putdata(new_pixel_data)

    new_image.save(png)

"""
presa una foto fa il resize rispettando il vincolo di larghezza
"""


def diagonal_resize(foto, new_width, new_height=0):
    wSquadra, hSquadra = foto.size

    if new_height == 0:
        new_height = int(new_width * hSquadra / wSquadra)
    else:
        new_width = int(new_height * wSquadra / hSquadra)

    return foto.resize((new_width, new_height)), new_width, new_height


"""
data una parola, viene restituita quella più vicina tra le disponibili in elenco
"""


def matchWord(s, arr):
    arr_lower = [x.lower().replace(" ", "") for x in arr]
    s_lower = s.lower().replace(" ", "")

    match = difflib.get_close_matches(s_lower, arr_lower, n=1, cutoff=0.3)
    if match:
        # Find the index of the lowercase match
        index = arr_lower.index(match[0])
        # Return the original string in its original case
        return arr[index]
    else:
        logging.info("Non ho trovato")
        raise Exception("Non ho trovato una squadra")


"""
Recupera la lista delle squadre di cui si hanno le grafiche
"""


def getTeams(path):
    return [os.path.basename(elem).replace('.png', '') for elem in glob.glob(path + '/*.png')]

def getTeamsFromTXT(path):
    if 'ENV' in os.environ and os.environ['ENV'] == 'testing':
        path = "../" + path

    #print(path)

    if ".txt" in path:
        f = open(path)
        f = f.readlines()
        f = [s.strip() for s in f]
        #print(f)
        return f


def getTemplateText(template,s):
    if 'ENV' in os.environ and os.environ['ENV'] == 'testing':
        template = "../" + template

    tree = ET.parse(template)
    example = tree.find(s)

    if example is None:
        return []

    example = example.text.split("\n")

    s = ""

    for el in example:
        s += el.strip() + "\n"

    return s

def getTemplateGuide(template):
    return getTemplateText(template,"GUIDA")


def getTemplateAttribute(template,attribute):
    if os.environ.get('ENV') == 'testing':
        template = "../" + template

    tree = ET.parse(template)
    root = tree.getroot()
    return root.attrib[attribute] if attribute in root.attrib else False



def getHockeyItalianoClassificaTable(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('td', string=' CLASSIFICA UFFICIALE').parent.parent
    return table


def createHockeyItalianoClassificaList(table):
    rows = table.find_all('tr')
    classifica = []

    for i in range(2, len(rows)):
        classifica.append(rows[i].find_all('td')[1].text + "," + rows[i].find_all('td')[2].text)

    return classifica


def getAbsolutePath(relative_path):
    absolute_path = os.path.abspath(os.path.join(os.getcwd(), relative_path))
    return absolute_path



def super_print(*args, **kwargs):
    for arg in args:
        print(f"{arg} = {eval(arg)}")

    for name, value in kwargs.items():
        print(f"{name} = {value}")


