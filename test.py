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

done = False
#here is the animation
def animate():
    for c in itertools.cycle(['|', '/', '-', '\\']):
        if done:
            break
        sys.stdout.write('\rMemproses file ' + c)
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write('\rDone!     ')

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



if(len(sys.argv) ==1):
    print "direktori tidak ada"
    exit(1)
else:
    direktori = sys.argv[1]
    print direktori
##listing file in direktori
data_file ={}
list_content={}
tugas =[]
list_file = os.listdir(direktori);

for file in list_file:
    if(file.endswith(".docx")):
        full_path =os.path.join(direktori,file)
        tugas.append(full_path)


list_tugas =create_schedule(tugas)
print len(list_tugas)
t = threading.Thread(target=animate)
t.start()


tugas_duplicate=[]

for round in list_tugas:
    for match in round:
        if match[0] in tugas_duplicate or match[1] in tugas_duplicate:
            pass
            #print "duplicate"
        elif match[0] == match[1]:
            pass
            #print "same file"
        else:
            text1 = docx2txt.process(match[0])
            text2 = docx2txt.process(match[1])
            ratio = SequenceMatcher(None,text1,text2).ratio();
            if(ratio > 0.5):
                tugas_duplicate.append(match[0]);
                tugas_duplicate.append(match[1])
                #print match[0] + " added to duplicate"
                #print match[1] +" added to duplicate"

done =True
print
print "_______________"
print "total file ", len(list_tugas)
print "terdapat " ,len(tugas_duplicate) ," file yang diduga plagiat"
print "file terduga plagiat dipindahkan ke folder plagiat"

folder_plagiat =os.path.join(direktori,"plagiat")

if(os.path.exists(folder_plagiat) ==False):
    os.makedirs(folder_plagiat)

for plagiat in tugas_duplicate:
    p = os.path.join(direktori,"plagiat");
    p = os.path.join(p,os.path.basename(plagiat))
    shutil.move(plagiat,p)



