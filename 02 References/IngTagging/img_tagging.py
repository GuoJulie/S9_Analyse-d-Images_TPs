# -*- coding:Utf8 -*-
# Software operation interface


# Importing packages
import os
from tkinter import *
from tkinter.filedialog import askdirectory
from New_Tags import new_tags
from PIL import ImageTk, Image


# Definition of my functions
def compareListes(string1,string2):
    str1 = string1.replace(" ", "")
    str2 = string2.replace(" ", "")
    if len(str1) > 0:
        Y = str1.split(",")
        s1 = set(Y)
    else:
        s1 = set()

    if len(str2) > 0:
        Z = str2.split(",")
        s2 = set(Z)
    else:
        s2 = set()

    set1 = s1 - s2   # missing keywords
    set2 = s2 - s1   # extra keywords

    rslt = []
    rslt.append(len(set1)) # missing keywords
    rslt.append(len(set2)) # extra keywords
    return rslt


def compareItem2GT(item):

    # Reading New_Tags file
    fNT = "NT/" + item
    if(os.path.exists(fNT)):
        ft = open(fNT, 'r')
        keywords = ft.readline()
        ft.close()
    else:
        keywords = ""

    # Reading GT file
    fGT = "GT/" + item
    if (os.path.exists(fGT)):
        f_gt = open(fGT, 'r')
        GT = f_gt.readline()
        f_gt.close()
    else:
        GT = ""

    score_lst = compareListes(GT, keywords)

    # write in log file
    flog = open("Log.TXT", 'a')
    flog.write(keywords + "   >>   " + GT + ' - Score:' + str(score_lst) + "\n")
    flog.close()

    boxkeywords.delete(0, END)
    boxkeywords.insert(0, keywords + "  >>  " + GT)
    txtstatut.configure(text = 'Score:'+ str(score_lst))
    return score_lst


def DisplayItem(item):

    global img,photo,can1,imgdefaut,boxkeywords, MalisteTxt, MalisteImg

    img = Image.open(MalisteImg[item])
    basewidth = 400
    wpercent = (basewidth / float(img.size[0]))
    hsize = int((float(img.size[1]) * float(wpercent)))
    img = img.resize((basewidth, hsize), Image.ANTIALIAS)

    if(hsize > 400) :
        baseh = 400
        wpercent = (baseh / float(img.size[1]))
        wsize = int((float(img.size[0]) * float(wpercent)))
        img = img.resize((wsize, baseh), Image.ANTIALIAS)

    photo = ImageTk.PhotoImage(img)
    imgdefaut = can1.create_image(200, 200, image=photo)

    # Reading text file
    strfgt = "GT/" + MalisteTxt[item]
    if(os.path.exists(strfgt)):
        ft = open(strfgt, 'r')
        keywords = ft.readline()
        ft.close()
    else:
        keywords = ""

    boxkeywords.delete(0, END)
    boxkeywords.insert(0, keywords)
    txtstatut.configure(text = 'Ok' )


def getNew_keywords(item):
    global boxkeywords_1
    global keywords_1

    keywords_1 = ''
    file_path = MalisteImg[item]
    new_keywords = new_tags.new_detect(file_path)
    keywords_1 = ', '.join(new_keywords)

    # Write new text file
    foldername = "NT"
    if not os.path.exists(foldername):
        os.makedirs(foldername)
    if len(MalisteTxt) > 0:
        ft = open("NT/" + MalisteTxt[item], 'w')
        ft.write(keywords_1)
        ft.close()

    boxkeywords_1.delete(0, END)
    boxkeywords_1.insert(0, keywords_1)

    txtstatut.configure(text='Ok')


def directoryBox(root, title=None, dirName=None):
    options = {}
    options['initialdir'] = dirName
    options['title'] = title
    options['mustexist'] = True
    root.update()
    repName = askdirectory(**options)
    return repName




# Menu callback ---------------------------------------------------

def call_GT():
    txtstatut.configure(text='Compare to GT')

    # Reset log file
    if os.path.exists("GT"):
        flog = open("Log.TXT", 'w')
        flog.write("Log file : \n")
        flog.close()
    else:
        txtstatut.configure(text='No GT dir')
        return 1

    rslt = [0,0]
    cpt = 0
    for element in MalisteTxt:
        score_set = compareItem2GT(element)
        rslt[0] = rslt[0] + score_set[0]
        rslt[1] = rslt[1] + score_set[1]
        cpt = cpt + 1

    flog = open("Log.TXT", 'a')
    flog.write("Final score : " + str(rslt) + " on " + str(cpt) + " images \n")
    flog.close()

    txtstatut.configure(text = 'Done (' + str(rslt) + ")" )
    return 0


def call_save():
    global boxkeywords

    # Write text file
    if len(MalisteTxt) > 0 :
        ft = open("GT/" + MalisteTxt[no_item], 'w')
        keywords = boxkeywords.get()
        ft.write(keywords)
        txtstatut.configure(text = "Saved (" + MalisteTxt[no_item] + ").")
        ft.close()


def call_next():
    global no_item
    if no_item < len(MalisteTxt)-1:
        no_item +=1
        DisplayItem(no_item)
        getNew_keywords(no_item)

    txtstatut.configure(text = MalisteImg[no_item] )


def call_previous():
    global no_item
    if no_item > 0:
        no_item -=1
        DisplayItem(no_item)
        getNew_keywords(no_item)

    txtstatut.configure(text= MalisteImg[no_item])


def call_del():
    global  boxkeywords
    boxkeywords.delete(0, END)
    boxkeywords.insert(0, " ")


####################################################################
#                         Prgm Principal
####################################################################


#Debut IHM ----------------------------------------------------------
mainw = Tk()
mainw.title('Image Tagging PolytechTours')

# creation of widgets 'Label' and 'Entry' :
txtseparator = Label(mainw, text =' Use the comma as a separator                 - Click on [Update] to save the modifications !!!')
txt_tag = Label(mainw, text =' Tags:')
txt_tag_1 = Label(mainw, text =' New_Tags:')
txt_color = Label(mainw, text =' Colors: black,white,red,green,blue,yellow,orange,gray,purple')
txt_scene = Label(mainw, text ='Scene: inside,outside,nature,city')
txt_inside = Label(mainw, text ='Main elements: human,face,animal,car,plane,van,bike,ski')
txt_outside = Label(mainw, text ='Main elements: sky,sun,house,tree,sea,mountain,snow')
txt_quality = Label(mainw, text ='Quality: fuzzy,dark,light')

boxkeywords = Entry(mainw, width=120)
boxkeywords_1 = Entry(mainw, width=120)
txtstatut = Label(mainw, text ='OK')

# Boutons
b_previous = Button(mainw, text='<<<<', command = call_previous)
b_next = Button(mainw, text='>>>>', command = call_next)
b_update = Button(mainw, text='Update', command = call_save)
b_del = Button(mainw, text='Clear', command = call_del)
b_gt = Button(mainw, text='GT', command = call_GT)
b_exit = Button(mainw, text='Exit', command = mainw.quit)

# creation of a 'Canvas' widget containing a bitmap image :
img = Image.open('Affiche.gif')
basewidth = 400
wpercent = (basewidth/float(img.size[0]))
hsize = int((float(img.size[1])*float(wpercent)))
img = img.resize((basewidth,hsize), Image.ANTIALIAS)
photo = ImageTk.PhotoImage(img)

can1 = Canvas(mainw, width =400, height =400, bg ='white')
imgdefaut = can1.create_image(200, 200, image = photo)

# Layout using the 'grid' method
can1.grid(row =1, column =1,columnspan =3, rowspan =5, padx =10, pady =5)
txt_color.grid(row =1, column =4,sticky = W)
txt_scene.grid(row =2, column =4,sticky = W)
txt_inside.grid(row =3, column =4,sticky = W)
txt_outside.grid(row =4, column =4,sticky = W)
txt_quality.grid(row =5, column =4,sticky = W)

b_previous.grid(row =6, column =1)
b_update.grid(row =6, column =2)
b_next.grid(row =6, column =3)

txt_tag.grid(row =8, column =1)
boxkeywords.grid(row =8, columnspan =4, column =2)

txt_tag_1.grid(row =10, column =1)
boxkeywords_1.grid(row =10, columnspan =4, column =2)

b_gt.grid(row =11, column =1)
b_del.grid(row =11, column =2)
b_exit.grid(row =11, column =3)

txtseparator.grid(row =13, column =1, columnspan =4)
txtstatut.grid(row =13, columnspan =5, column =1,sticky = E)



# Fin IHM ----------------------------------------------------------

# Scan the chosen directory to look for image files
rep = os.getcwd()
rep = directoryBox(mainw,title='Working directory', dirName=rep)

if len(rep) == 0:
    rep = os.getcwd()
os.chdir(rep)

MalisteImg = []
MalisteTxt = []

for element in os.listdir(rep):
    if (element.endswith('.jpg') or element.endswith('.JPG') or element.endswith('.png') or element.endswith('.PNG') ):
        namef = os.path.splitext(element)
        MalisteImg.append(element)
        MalisteTxt.append(namef[0] + ".txt")

# cloning of the Mediateque list for initial display
no_item = 0

if len(MalisteImg) > 0:
    DisplayItem(no_item)
    getNew_keywords(no_item)
else:
    boxkeywords.delete(0, END)
    boxkeywords.insert(0,'NO IMAGE FOUND IN THE SELECTED DIRECTORY')
    boxkeywords_1.delete(0, END)
    boxkeywords_1.insert(0, 'NO IMAGE FOUND IN THE SELECTED DIRECTORY')

# start-up :
mainw.mainloop()