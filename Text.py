import json
# import requests
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

    def __init__(this, path_to_text='metsudah_siddur.json'):
        this.path_to_text = path_to_text
        with open(path_to_text, 'r', encoding='utf-8') as file:
            this.text = file.read()

        this.content = this.parse()
        this.title = this.content['title']
        this.schema = this.content['schema'][this.schema_root]

    
    def parse(this):
        return json.loads(this.text)
    
    #Get the service basic path from the schema based on the current path
    #Returns a list of dictionaries
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
    
    #Get the service basic path from the schema based on the current path and convert it to nice text
    #returns a string
    def getServiceDataToText(this):
        pointer = this.getServiceData()
        return this.dictionaryListToText(pointer,0)

    #Get the service basic path from the schema based on the current path and convert it to an ordered list. This is a helper fxn
    #for orderedListToOrderedPaths
    #returns a list of lists as a tree
    def getServiceDataToOrderedList(this):
        pointer = this.getServiceData()
        return this.dictionaryListToOrderedList(pointer)
    
    #Converts a list of dictionaries to a string that displays nicley
    #helper fxn for getServiceDataToText
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
    
    #Converts a list of dictionaries to an ordered list
    #helper fxn for getServiceDataToOrderedList
    #returns a list of lists as a tree
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
    
    #Converts an ordered list to a list of paths
    #helper for orderedListToOrderedPaths
    #returns a list of lists (paths)
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
   
   #Converts an ordered list to a list of paths
    #returns a list of lists (paths)
    
    def orderedListToOrderedPaths(this,orderedList):
        paths = []
        this.orderedListToOrderedPathsLong(orderedList, [], paths, True)
        for path in paths:
            path.pop(0)
        
        while [] in paths:
            paths.remove([])

        return paths
    
    #Get the current path content
    def getCurrent(this):
        cur = this.content
        for i in [this.text_root] + this.cur_path:
            cur = cur[i]
        return cur
    
    def getPaths(this):
        serviceData = this.getServiceDataToOrderedList() #Get the service data as an ordered list
        if isinstance(serviceData, str):
            return serviceData
        else:
            serviceData = ['TOP']+serviceData
        # serviceData = ['TOP']+this.getServiceDataToOrderedList() #Get the service data as an ordered list

        paths = this.orderedListToOrderedPaths(serviceData) #Convert the ordered list to a list of paths
        return paths
    def getFullService(this):
        paths = this.getPaths() #Get the paths
        fullText = ""
        for path in paths: #Get the text at each path
            text = this.getTextAtPath(this.cur_path  + path)
            fullText+="</br></br>"+":".join(path)+"<br/>"+" ".join(text)
        return fullText
            
    def getFullServiceAsList(this):
        paths = this.getPaths() #Get the paths
        fullText = []
        for path in paths: #Get the text at each path
            text = this.getTextAtPath(this.cur_path  + path)
            fullText.append(text)
        return fullText
    



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
# myText.addCurrent('Weekday')
# myText.addCurrent('Shacharit')

def add_bidi_controls(text):
    return u'\u202B' + text + u'\u202C'

text = myText.getFullService()
with open('output.html', 'w', encoding='utf-8') as file:
    file.write(text)


# print(text)
# testData = {"games:" : [{'a':"Test1", 'b':"Test2"}, {'c':"Test3", 'd':"Test4"}], "test":"test","cars:": [{'e':"Test5", 'f':"Test6"}, {'g':"Test7", 'h':"Test8"}]}
# print(myText.getServiceDataToText())
# print("\n\n\n")
# print(myText.getServiceDataToOrderedList())
# paths = []
# mylist = ['TOP'] + myText.getServiceDataToOrderedList()
# paths = myText.orderedListToOrderedPaths(mylist)

# print("PATHS: " + str(paths))
