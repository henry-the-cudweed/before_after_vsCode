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
          [sg.Text("insert a calflora link:"), sg.InputText(key="-IN4-")],
          [sg.Text("before month/year:"), sg.InputText(key="-IN5-")],
          [sg.Text("after month/year:"), sg.InputText(key="-IN6-")],
          [sg.Text("project description:"), sg.Multiline(key="-IN7-", size=(70,10))],
          [sg.Button("Submit")]]

###Building Window
window = sg.Window('My File Browser', layout, size=(600,600))
    
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
        calflora_link = values["-IN4-"]
        before_date_text = values["-IN5-"]
        after_date_text = values["-IN6-"]
        description_text = values["-IN7-"]

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
calfloraLinkPattern = "calfloraLinkSoup"
beforeDateTextPattern = "beforeDateTextSoup"
afterDateTextPattern = "afterDateTextSoup"
descriptionTextPattern = "descriptionTextPatternSoup"


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

##

##combine photos to new path 
before_url_new_folder = os.path.join(path, just_photo_before )
after_url_new_folder = os.path.join(path, just_photo_after)

##move photos using new path name
shutil.copy(before_url, before_url_new_folder)
shutil.copy(after_url, after_url_new_folder)

### resized photos to try to fix slider zoom issue
image = Image.open(just_photo_before)
image_resized = image.resize((3579, 2015))
image_resized.save('aslider\photo_resized_before.jpg')

image2 = Image.open(just_photo_after)
image_resized2 = image2.resize((3579,2015))
image_resized2.save('aslider\photo_resized_after.jpg')


### RegEx Replacement
soup_string1 = re.sub(beforePattern, "photo_resized_after.jpg", soup_string)
soup_string2 = re.sub(afterPattern, "photo_resized_before.jpg", soup_string1)
soup_string3 = re.sub(calfloraLinkPattern, calflora_link, soup_string2)
soup_string4 = re.sub(beforeDateTextPattern, before_date_text, soup_string3)
soup_string5 = re.sub(afterDateTextPattern, after_date_text, soup_string4)
soup_string6 = re.sub(descriptionTextPattern, description_text, soup_string5)


with open("aslider\slider.html", "w") as file:
    file.write(soup_string6)



    


        
