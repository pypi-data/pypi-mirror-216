from PIL import Image,ImageFont
import numpy as np
import cv2
from .imageproc import *
from pygments.lexers import *
from pygments import *
from .config import *
from .easy import *
class Background():
    """
    Class for background of code screenshot.
    """
    def __init__(self,obj):
        if isinstance(obj,tuple): # Background is a color.
            if isinstance(obj[0],tuple):
                self.type=0
                self.lineno_bg=obj[0]
                self.code_bg=obj[1]
            else:
                self.lineno_bg=obj
                self.code_bg=obj
                self.type=0
        else: # Background is an image.
            self.type=1
            self.bg=obj
    def color(self,code,lineno): # Used more numpy functions now, so much faster.
        if self.type:
            whole=image_merge_row(lineno,code)
            bg=cv2.resize(self.bg,(whole.shape[1],whole.shape[0]),interpolation=cv2.INTER_LINEAR)
            mask=(whole[:,:,3]==0)
            whole[:,:,3]-=whole[:,:,3]*mask
            whole[:,:,3]+=255
            whole[:,:,0]-=whole[:,:,0]*mask
            whole[:,:,1]-=whole[:,:,1]*mask
            whole[:,:,2]-=whole[:,:,2]*mask
            whole[:, :, 0] += bg[:, :, 0] * mask
            whole[:, :, 1] += bg[:, :, 1] * mask
            whole[:, :, 2] += bg[:, :, 2] * mask
            return np.array(Image.fromarray(whole).convert('RGB'))
        else:
            mask_code=(code[:,:,3]==0)
            mask_lineno=(lineno[:,:,3]==0)
            code[:,:,3]-=code[:,:,3]*mask_code
            lineno[:,:,3]-=lineno[:,:,3]*mask_lineno
            code[:,:,3]+=255
            lineno[:, :, 3] += 255
            code[:,:,0]-=code[:,:,0]*mask_code
            code[:, :, 0] += np.uint8(self.code_bg[0]) * mask_code
            code[:, :, 1] -= code[:, :, 1] * mask_code
            code[:, :, 1] += np.uint8(self.code_bg[1]) * mask_code
            code[:, :, 2] -= code[:, :, 2] * mask_code
            code[:, :, 2] += np.uint8(self.code_bg[2]) * mask_code
            lineno[:, :, 0] -= lineno[:, :, 0] * mask_lineno
            lineno[:, :, 0] += np.uint8(self.lineno_bg[0]) * mask_lineno
            lineno[:, :, 1] -= lineno[:, :, 1] * mask_lineno
            lineno[:, :, 1] += np.uint8(self.lineno_bg[1]) * mask_lineno
            lineno[:, :, 2] -= lineno[:, :, 2] * mask_lineno
            lineno[:, :, 2] += np.uint8(self.lineno_bg[2]) * mask_lineno
            return np.array(Image.fromarray(image_merge_row(lineno,code)).convert('RGB'))
def fromstr(string):
    def hex2rgb(x):
        return (int(x[:2],16),int(x[2:4],16),int(x[4:6],16))
    if '.' in string:
        return Background(image_open(string))
    elif len(string)==6:
        return Background(hex2rgb(string))
    else:
        return Background((hex2rgb(string[:6]),hex2rgb(string[6:])))
