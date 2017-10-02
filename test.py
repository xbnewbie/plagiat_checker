import sys
import os,shutil
import itertools
import threading
import time
from difflib import SequenceMatcher
import difflib
from docx import Document
from docx.shared import Inches
import  docx2txt
import wx


done = False
ratio_config = 0.6

debug_mode = False


#here is the animation
def animate():
    for c in itertools.cycle(['|', '/', '-', '\\']):
        if done:
            break
        sys.stdout.write('\rMemproses file ' + c)
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write('\rDone!     \n')
    exit = raw_input("press any key to exit")

def create_schedule(list):
    """ Create a schedule for the teams in the list and return it"""
    s = []

    if len(list) % 2 == 1: list = list + [list[0]]

    for i in range(len(list)-1):

        mid = len(list) / 2
        l1 = list[:mid]
        l2 = list[mid:]
        l2.reverse()

        # Switch sides after each round
        if(i % 2 == 1):
            s = s + [ zip(l1, l2) ]
        else:
            s = s + [ zip(l2, l1) ]

        list.insert(1, list.pop())

    return s


app = wx.App()
print "Pilih directori tugas "
dialog = wx.DirDialog(None, "Pilih directori tugas:",style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)
if dialog.ShowModal() == wx.ID_OK:
    direktori= dialog.GetPath()
else:
    print ""
    exit()
dialog.Destroy()

##listing file in direktori
data_file ={}
list_content={}
tugas =[]
list_file = os.listdir(direktori);

for file in list_file:
    if(file.endswith(".docx") or file.endswith(".doc")):
        full_path =os.path.join(direktori,file)
        tugas.append(full_path)


list_tugas =create_schedule(tugas)
print len(list_tugas)
t = threading.Thread(target=animate)
if(debug_mode==False):
    t.start()


tugas_duplicate=[]
all_duplicate=[]
for round in list_tugas:
    for match in round:
        #if match[0] in tugas_duplicate or match[1] in tugas_duplicate:
        if  match[1] in tugas_duplicate:
            pass
            #print "duplicate",match[1]
        elif match[0] == match[1]:
            #print "same file"
            pass
        else:
            #print match[0] , match[1]
            text1 = docx2txt.process(match[0])
            text2 = docx2txt.process(match[1])
            ratio = SequenceMatcher(None,text1,text2).ratio();
            if(ratio > ratio_config):
                if(match[0] not in tugas_duplicate):
                    tugas_duplicate.append(match[1]);
                    #tugas_duplicate.append(match[1])
                    #print match[0] + " added to duplicate"
                    #print match[1] +" added to duplicate"

                    ##put all result
                    all_duplicate.append(match[0])
                    all_duplicate.append(match[1])

                    #print out information
                    if(debug_mode):
                        print "rasio kesamaan ",ratio," : ",os.path.basename(match[0])," with ",os.path.basename(match[1])



#remove multi duplicate
tugas_duplicate =list(set(all_duplicate));

folder_plagiat =os.path.join(direktori,"plagiat")

if(os.path.exists(folder_plagiat) ==False):
    os.makedirs(folder_plagiat)

for plagiat in tugas_duplicate:
    p = os.path.join(direktori,"plagiat");
    p = os.path.join(p,os.path.basename(plagiat))
    shutil.move(plagiat,p)


print
print "_______________"
print "total file ", len(list_tugas)
print "terdapat " ,len(tugas_duplicate) ," file yang diduga plagiat"
print "file terduga plagiat dipindahkan ke folder plagiat"


done =True

