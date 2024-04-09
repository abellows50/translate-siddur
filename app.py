
from Text import Text
from GUI import GUI
from SefariaApi import SefariaApi
import requests
def search(word):
    api = SefariaApi()
    jsonFile = api.lexicon(word)
    jsonFile = api.formatAsHtml(jsonFile)
    return jsonFile

api = SefariaApi()
gui = GUI()
gui.setSearchFxn(search)

path_to_text = 'metsudah_siddur.json'

myText = Text(path_to_text)
myText.addCurrent('Weekday')
myText.addCurrent('Minchah')
myText.addCurrent('Amida')


# text = myText.getFullServiceAsList()
# for section in text:
#     for line in range(len(section)):
#         if "<small>" in section[line]:
#             index = section[line].index("<small>")
#             end = section[line].index("</small>")
#             section[line] = section[line][:index] + section[line][end+7:]
#     section = " ".join(section)
    

text = myText.getFullService()
for char in text:
    if not char.isprintable():
        print("NONPRINTING CHAR")
        text = text.replace(char, 'NONPRINTING CHAR')
    
# print(text)

text = str(text)
with open('output.html', 'w', encoding='utf-8') as file:
    file.write(text)
# import re

# def strip_chars(s):
#     return re.sub(r'[a-zA-Z<>\/]', '', s)
# text = strip_chars(text)
# text = api.formatAsHtml(text)

# with open('output.html', 'w', encoding='utf-8') as file:
#     file.write(text)

# print(api.pipe_to_siddur(text))
# text = api.grab_siddur()
GUI.addHtml(gui, text)
# GUI.display(gui)




bidi_chars = {'\u202A', '\u202B', '\u202C', '\u202D', '\u202E'}
bidi_char_replacements = {'\u202A': '<LRE>', '\u202B': '<RLE>', '\u202C': '<PDF>', '\u202D': '<LRO>', '\u202E': '<RLO>'}
nonPrintable = []
with open('metsudah_siddur.json', 'r', encoding='UTF-8') as file:
    while True:
        # read by character
        char = file.read(1)
        if not char.isprintable():
            if f"Unicode: U+{ord(char):04X}" not in nonPrintable:
                nonPrintable.append(f"Unicode: U+{ord(char):04X}")
        if not char:
            break
print(nonPrintable)