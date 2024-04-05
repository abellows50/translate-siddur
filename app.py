from Text import Text
from GUI import GUI
from SefariaApi import SefariaApi

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
myText.addCurrent('Amidah')



text = myText.getFullService()
text = api.formatAsHtml(text)
GUI.addHtml(gui, text)
GUI.display(gui)

