"""
Image processing functions.
"""
import numpy as np
from PIL import Image,ImageDraw,ImageFont
from .config import *
from pygments import lex
from pygments.lexers import *
def gettext(s, font):
    """
    Get size of text.
    :param s: text
    :param font: font
    :return: size (tuple)
    """
    img = Image.new('RGBA', (1, 1), (0, 0, 0, 0))
    idd = ImageDraw.ImageDraw(img)
    return idd.textsize(s, font)
def create_alpha(token_list,font):
    """
    Create a transparent background image by the token list.
    :param token_list: Token list.
    :param font: font
    :return: a transparent image (as numpy array).
    """
    final_w,final_h=0,0
    for i,j in token_list:
        final_w+=gettext(j,font)[0]
        final_h=max([final_h,gettext(j,font)[1]])
    size=(final_w,final_h)
    return np.array(Image.new('RGBA',size,(0,0,0,0)))
def add_text(alpha,token_list,font,config,token_checker):
    """
    Add tokens to background.
    :param alpha: background image.
    :param token_list: Token List.
    :param font: font.
    :param config: Highlighter config instance.
    :param token_checker: A TokenChecker instance.
    :return: Background with text added.
    """
    alpha=Image.fromarray(alpha)
    pos=0
    idd=ImageDraw.ImageDraw(alpha)
    for i,j in token_list:
        idd.text((pos,0),j,fill=config(token_checker(i)),font=font)
        sw,sh=gettext(j,font)
        pos+=sw
    return np.array(alpha)
def create_lineno(lineno,alpha,font,fgcolor,width,offset):
    """
    Create a image for line number.
    :param lineno: Line number.
    :param alpha: Transparent image
    :param font: font
    :param fgcolor: foreground color
    :param width: image width
    :param offset: Offset
    :return: Line number image.
    """
    a=alpha
    alpha=Image.fromarray(alpha)
    height=a.shape[0]
    bg=Image.new('RGBA',(width,height),(0,0,0,0))
    w,h=gettext(str(lineno),font)
    x=width-w-offset
    y=int(height-h)/2
    idd=ImageDraw.ImageDraw(bg)
    idd.text((x,y),str(lineno),font=font,fill=fgcolor)
    return np.array(bg)
def image_merge_row(img1,img2):
    img3=np.zeros((img1.shape[0],img2.shape[1]+img1.shape[1],4),dtype=np.uint8)
    img3[:,:img1.shape[1],:]=img1
    img3[:,img1.shape[1]:,:]=img2
    return img3
def image_merge_col(img1,img2):
    img3 = np.zeros((img1.shape[0]+img2.shape[0], img1.shape[1], 4), dtype=np.uint8)
    img3[:img1.shape[0],:,  :] = img1
    img3[img1.shape[0]:,:,  :] = img2
    return img3
def image_fit(img,w):
    img2=np.array(Image.new('RGBA',(w,img.shape[0]),(0,0,0,0)))
    img2[:,:img.shape[1],:]=img
    return img2
