"""
Easy functions for images
"""
from PIL import Image,ImageTk
import numpy as np
from platform import system
import os
from uuid import uuid4
def require_tk():
    return __import__('tkinter')
def save_svg(path,img):
    import matplotlib.pyplot as plt
    plt.imsave(path,img)
def read_svg(path):
    import aspose.words as a
    import cv2
    def _tmp():
        if system()=='Windows':
            return os.environ['TMP']
        else:
            return '/tmp'
    d=a.Document()
    db=a.DocumentBuilder(d)
    fn=str(uuid4())+'.png'
    file=os.path.join(_tmp(),fn)
    svg=db.insert_image(path)
    svg.image_data.save(file)
    cwd=os.getcwd()
    os.chdir(_tmp())
    img=cv2.imread(fn) # Only OpenCV can read this sort of PNG file.
    img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    os.chdir(cwd)
    return img
def image_open(path):
    if path.endswith('.svg'):
        return read_svg(path)
    return np.array(Image.open(path))
def image_save(path,img):
    if path.endswith('.svg'):
        save_svg(path,img)
    else:
        Image.fromarray(img).save(path)
def image_show(img,title=''):
    tk=require_tk()
    image_pil=Image.fromarray(img)
    wn=tk.Tk()
    wn.title(title)
    image_tk = ImageTk.PhotoImage(image_pil)
    wn.geometry('{}x{}'.format(img.shape[1],img.shape[0]))
    l=tk.Label(wn,text='',image=image_tk)
    l.place(x=0,y=0,width=img.shape[1],height=img.shape[0])
    wn.mainloop()
