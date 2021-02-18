# img_viewer.py
import os
import PySimpleGUI as sg
import os.path
from matplotlib import pyplot as plt
import cv2
from Bearing import Bearings as b

br = b.bearings_classifier()

# First the window layout in 2 columns
file_list_column = [
    [
        sg.Text("Image Folder"),
        sg.In(size=(25, 1), enable_events=True, key="-FOLDER-"),
        sg.FolderBrowse(),
        sg.Button("Detected Pins")
    ],
    [
        sg.Listbox(
            values=[], enable_events=True, size=(40, 20), key="-FILE LIST-"
        )
    ],
]

# For now will only show the name of the file that was chosen
image_viewer_column = [
    [sg.Text("Choose an image from list on left and find detected result in Result folder")],
    [sg.Text(size=(40, 1), key="-TOUT-")],
    [sg.Image(key="-IMAGE-")],
]

# ----- Full layout -----
layout = [
    [
        sg.Column(file_list_column),
        sg.VSeperator(),
        sg.Column(image_viewer_column),
    ]
]

window = sg.Window("Roller Bearings Quality Check", layout)
loop = 0
# Run the Event Loop
while True:
    loop+=1
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    # Folder name was filled in, make a list of files in the folder
    if event == "-FOLDER-":
        folder = values["-FOLDER-"]
        try:
            # Get list of files in folder
            file_list = os.listdir(folder)
        except:
            file_list = []

        fnames = [
            f
            for f in file_list
            if os.path.isfile(os.path.join(folder, f))
            and f.lower().endswith((".png", ".gif",".bmp",".jpg"))
        ]
        window["-FILE LIST-"].update(fnames)
    elif event == "-FILE LIST-":  # A file was chosen from the listbox
        try:
            filename = os.path.join(
                values["-FOLDER-"], values["-FILE LIST-"][0]
            )
            window["-TOUT-"].update(filename)
            #cv2.imshow(filename)
            if not os.path.isdir('Result'):
                os.mkdir('Result')

        except:
            print('Exception occured')
            pass
    elif event == "Detected Pins":
        c, img = br.roller_pin_count(filename)
        if c is not None:
            dst = 'Result/'+str(loop)+'_Result.png'
            plt.imsave(dst, img)
            if c == 16:
                window["-TOUT-"].update(f'Needle count {c}, Good Bearing')
                window["-IMAGE-"].update(filename=dst)
            else:
                window["-TOUT-"].update(f'Needle count {c}, Bad Bearing')
                window["-IMAGE-"].update(filename=dst)
                
        else:
            window["-TOUT-"].update(f'Needle count is not possible here')
            
window.close()
