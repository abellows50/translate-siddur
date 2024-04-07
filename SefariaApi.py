import requests
import json
import html
class SefariaApi:

    def __init__(this):
        this.LEXICON = "https://www.sefaria.org/api/words/"
        this.WORD_COMPLETION = "https://www.sefaria.org/api/words/completion/"
    
    def request(this, url):
        return requests.get(url).json()
    
    def lexicon(this, word):
        url = this.LEXICON + word
        return this.request(url)
    
    def word_completion(this, word):
        url = this.WORD_COMPLETION + word
        return this.request(url)

    def pipe_to_siddur(this, text):
        return requests.post('https://siddur.pythonanywhere.com/change', data = {'text': text}).text
    
    def grab_siddur(this):
        return requests.get('https://siddur.pythonanywhere.com/').text
    
    def formatAsHtml(this, json):
        string = ""
        if isinstance(json, list):
            for item in json:
                string += this.formatAsHtml(item)
        elif isinstance(json, dict):
            for key in json.keys():
                string += key + ": "
                string += this.formatAsHtml(json[key]) + "<br/></br><br/>"  
        elif isinstance(json, str):
            return html.unescape(json) + " "
        
        return string
        
def test():
    api = SefariaApi()
    jsonFile = api.lexicon('בראשית')
    jsonFile = "<p>" + api.formatAsHtml(jsonFile) +"</p>"

    with open('output.html', 'w', encoding='utf-8') as file:
        file.write(jsonFile)

    print(jsonFile)
    print(api.word_completion('בראש'))
