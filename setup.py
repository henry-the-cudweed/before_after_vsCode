import PyInstaller.__main__
import os
    
PyInstaller.__main__.run([  
     'name-%s%' % 'slider_creator',
     '--onefile',
     '--windowed',
     os.path.join('/path/to/your/script/', 'slider_creator.py'), """your script and path to the script"""                                        
])