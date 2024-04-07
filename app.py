
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


text = myText.getFullService()
# import re

# def strip_chars(s):
    # return re.sub(r'[a-zA-Z<>\/]', '', s)
# text = strip_chars(text)
# text = api.formatAsHtml(text)
with open('output.html', 'w', encoding='utf-8') as file:
    file.write(text)

print(api.pipe_to_siddur(text))
text = api.grab_siddur()
GUI.addHtml(gui, text)
GUI.display(gui)




