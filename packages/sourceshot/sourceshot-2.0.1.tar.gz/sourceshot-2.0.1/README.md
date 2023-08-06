<p><span><span style="font-family:Verdana, Arial, Helvetica, sans-serif;line-height:19px;text-indent:26px;"><span style="font-size:14px;"><span style="font-family:Arial;line-height:26px;"><br></span></span></span></span></p>

### This package takes pictures of source code
Example code: 
```python
from sshot import shot
from PIL import Image
code='''
print('Hello World!')
'''
image=shot(code,lang='python')
Image.fromarray(image).save('code.png')
```
The code above will create something like:
![](https://i.postimg.cc/sxLHWpJ7/code.png)

Use in command line:
```commandline
sshot -i test.py -l python -o code.png
sshot -i test.py -l python -o code.png -b bg.png # Add background image.
sshot -i test.py -l python -o code.png -b 00FF00FF0000 # Red code background color, green line number background color.
sshot -i test.py -l python # Show the image in a tkinter window.
```

It is also supported to set the background image of code, like:
```python
from sshot import shot
from PIL import Image
from sshot.background import Background
import numpy as np
code='''
print('Hello World!')
'''
bg=np.array(Image.open('bg.png'))
image=shot(code,lang='python',background=Background(bg))
Image.fromarray(image).save('code.png')
```
Bugs below are fixed in this version:
1. Error when reading GIF files. (IndexError: too many indices for array: array is 2-dimensional, but 3 were indexed.)
2. SVG files are read incorrectly.
3. Error when reading JSON files. 
This version's command line tool is better at guessing the language of the code.

### Syntax highlight config in JSON file.

A correct syntax highlight config should have a 'config' key.
It can also have an optional 'default' key.

The 'config' key is a dictionary, the key in that dictionary stands for the token name in the TokenChecker class (builtin, identifier, etc.)
The 'default' key stands for the default color.

For example:
```json
{
  "config": {
    "builtin": [127,0,0],
    "exception": [0,127,0],
    "string": [0,0,127]
  },
  "default": [127,127,127]
}
```
Using the JSON file above to create a picture of the code "print('Hello World!'), you will get:
![](https://i.postimg.cc/Mp48Jdxz/code2.png)