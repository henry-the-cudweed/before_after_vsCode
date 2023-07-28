from bs4 import BeautifulSoup
from regex import regex as re
import PySimpleGUI as sg
import os
import os.path
from PIL import Image
import shutil 
import pathlib as p 

###GUI Layout
sg.theme("DarkTeal2")
layout = [[sg.T("")], 
          [sg.Text("Choose a before pic: "), sg.Input(), sg.FileBrowse(key="-IN1-")],
          [sg.Text("Choose an after pic: "), sg.Input(), sg.FileBrowse(key="-IN2-")],
          [sg.Text("Choose a folder : "), sg.Input(), sg.FolderBrowse(key="-IN3-")],
          [sg.Button("Submit")]]

###Building Window
window = sg.Window('My File Browser', layout, size=(600,150))
    
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event=="Exit":
        break
    if event == 'FolderBrowse':
        foldername = sg.PopupGetFolder('Select folder', no_window=True)
        if foldername: # `None` when clicked `Cancel` - so I skip it
            filenames = sorted(os.listdir(foldername))
            # it use `key='files'` to `Multiline` widget
            window['files'].update("\n".join(filenames))
    elif event == "Submit":
        before_url = values["-IN1-"]
        after_url = values["-IN2-"]
        user_path = values["-IN3-"]
        window.close()


### Load Template Document
with open('slider_template.html', 'r') as f:
    html_doc = f.read()

### Convert Template Document to String
soup = BeautifulSoup(html_doc, 'html.parser')
soup_string = str(soup)

### Define Variables for RegEx Replacement
beforePattern = "beforePictureSoup"
afterPattern = "afterPictureSoup"
#before_url = "https://www.pythontutorial.net/wp-content/uploads/2020/10/python-tutorial.png"
#after_url = "https://www.pythontutorial.net/wp-content/uploads/2020/10/python-tutorial.png"


#print(soup_string2)

###Create New Directory
directory = "aslider"
parent_dir = user_path
path = os.path.join(parent_dir, directory)

os.mkdir(path)


print(path)

##stripped the photos from the path
just_photo_before = os.path.basename(before_url)
just_photo_after = os.path.basename(after_url)


##combine photos to new path 
before_url_new_folder = os.path.join(path, just_photo_before )
after_url_new_folder = os.path.join(path, just_photo_after)

##move photos using new path name
shutil.copy(before_url, before_url_new_folder)
shutil.copy(after_url, after_url_new_folder)



### RegEx Replacement
soup_string1 = re.sub(beforePattern, just_photo_after, soup_string)
soup_string2 = re.sub(afterPattern, just_photo_before, soup_string1)

with open("aslider\slider.html", "w") as file:
    file.write(soup_string2)



    


        
