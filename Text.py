import json
import requests

path_to_text = 'metsudah_siddur.json'

class Text:
    text = None
    content = None
    path_to_text = None
    title = None
    schema = None
    body = None
    text_root = 'text'
    schema_root = 'nodes'
    cur_path = []

    def __init__(this, path_to_text):
        this.path_to_text = path_to_text
        with open(path_to_text, 'r', encoding='utf-8') as file:
            this.text = file.read()

        this.content = this.parse()
        this.title = this.content['title']
        this.schema = this.content['schema'][this.schema_root]

    def parse(this):
        return json.loads(this.text)
    
    def getServiceData(this):
        pointer = this.schema
        for pathPart in this.cur_path:
            found = False
            for node in pointer:
                if node["enTitle"] == pathPart:
                    pointer = node["nodes"]
                    found = True
                    break
            if not found:
                return "Path not found"     
        return pointer
    
    def getServiceDataToText(this):
        pointer = this.getServiceData()
        return this.dictionaryListToText(pointer,0)

    def getServiceDataToOrderedList(this):
        pointer = this.getServiceData()
        return this.dictionaryListToOrderedList(pointer)
    
    def dictionaryListToText(this, dictionaryList, tabs):
        text =  "\n" + tabs*"    "
        tabs+=1
        if isinstance(dictionaryList, list):
            for dictionary in dictionaryList:
                text+=this.dictionaryListToText(dictionary, tabs)
        elif isinstance(dictionaryList, dict):
            for key in dictionaryList.keys():
                if key != "nodes":
                    text+=key+": "
                else:
                    text += ":"
                text+=this.dictionaryListToText(dictionaryList[key], tabs) + " "
        elif isinstance(dictionaryList, str):
            return dictionaryList + " "
        return text
    
    def dictionaryListToOrderedList(this, dictionaryList):
        myList =  []
        if isinstance(dictionaryList, list):
            for dictionary in dictionaryList:
                myList.append(this.dictionaryListToOrderedList(dictionary))
        elif isinstance(dictionaryList, dict):
            for key in dictionaryList.keys():
                if key!= "heTitle":
                    myList.append(this.dictionaryListToOrderedList(dictionaryList[key]))
        elif isinstance(dictionaryList, str):
            return dictionaryList
        return myList
    
    def orderedListToOrderedPathsLong(this, orderedList, curPath, paths, leaf=True):
        curPath = curPath.copy()
        for mylist in orderedList:
            if isinstance(mylist, str):
                curPath.append(mylist)
                if leaf:
                    paths.append(curPath)
                
            else:
                # check if the next recursion is a leaf
                leaf = True
                for next in mylist:
                    if isinstance(next, list):
                        leaf = False
                        break
                this.orderedListToOrderedPathsLong(mylist, curPath, paths, leaf)
   
    def orderedListToOrderedPaths(this,orderedList):
        paths = []
        this.orderedListToOrderedPathsLong(orderedList, [], paths, True)
        return paths
    
        
    def getCurrent(this):
        cur = this.content
        for i in [this.text_root] + this.cur_path:
            cur = cur[i]
        return cur
    
    def getTextAtPath(this, path):
        cur = this.content
        for i in [this.text_root] + path:
            cur = cur[i]
        return cur
    
    def addCurrent(this, path):
        this.cur_path.append(path)

    def print(this):
        print(this.title)
        print(this.getCurrent())
        print(this.schema)

myText = Text(path_to_text)
myText.addCurrent('Weekday')
myText.addCurrent('Minchah')

# testData = {"games:" : [{'a':"Test1", 'b':"Test2"}, {'c':"Test3", 'd':"Test4"}], "test":"test","cars:": [{'e':"Test5", 'f':"Test6"}, {'g':"Test7", 'h':"Test8"}]}
# print(myText.getServiceDataToText())
# print("\n\n\n")
# print(myText.getServiceDataToOrderedList())
paths = []
mylist = ['TOP'] + myText.getServiceDataToOrderedList()
paths = myText.orderedListToOrderedPaths(mylist)

print("PATHS: " + str(paths))