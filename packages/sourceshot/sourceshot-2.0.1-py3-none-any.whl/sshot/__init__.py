"""
Takes pictures of code!
"""
from pygments import *
from pygments.lexers import *
from .background import *
from PIL import ImageFont
from .config import *
from .imageproc import *
from .easy import *
from .tokenproc import split_line
from argparse import *
from .debug import *
from colorama import *
import sys
__version__='2.0.1'
default_config=ColorConfig(
    cfdct={
        'keyword':(127,127,0),
        'int':(127,0,127),
        'oct':(127,0,127),
        'bin':(127,0,127),
        'hex':(127,0,127),
        'float':(127,0,127),
        'comment':(127,127,127),
        'docstring':(127,127,127),
        'builtin':(0,0,127),
        'string':(127,0,0),
        'shebang':(127,127,127),
        'escape':(255,193,193),
        'char':(139,101,139),
        'affix':(127,0,0),
        'date':(127,0,127),
        'exception':(0,127,127),
        'preprocessor':(0,0,127),
        'preprocessor-file':(40,113,62)
    }
)
def shot(code,config=default_config,lang='auto',background=Background(((255,255,255),(255,255,255))),font=ImageFont.truetype('simsun.ttc',size=30),lineno_fgcolor=(0,0,0),tabsize=4,verbose=False):
    """
    Creates an image of the given code.
    :param code: Code as a string.
    :param config: Syntax highlight config.
    :param lang: Language of the code.
    :param background: Background.
    :param font: Font.
    :param lineno_fgcolor: Line number foreground color.
    :param tabsize: Tab size
    :param verbose: Verbose
    :return: Image as a numpy array.
    """
    if verbose:
        init(autoreset=True)
    if not code.strip():
        debug_output('Source code should NOT be empty',ERROR)
        return
    code=code.replace('\t',' '*tabsize)
    if lang=='auto':
        lang_lex=guess_lexer(code)
    else:
        lang_lex=get_lexer_by_name(lang)
    if verbose:
        debug_output('Tokenizing...',INFO)
    token_list=lex(code,lang_lex)
    token_list_line=split_line(token_list)
    linenos=[]
    lines=[]
    if verbose:
        debug_output('Processing {} lines of tokens'.format(len(token_list_line)),INFO)
    for i,tok in enumerate(token_list_line):
        if verbose:
            debug_output('Creating transparent background for line {}'.format(i+1),INFO)
        alpha=create_alpha(tok,font)
        if verbose:
            debug_output('Adding text to background for line {}'.format(i+1),INFO)
        text=add_text(alpha,tok,font,config,TokenChecker())
        if verbose:
            debug_output('Creating line number {}'.format(i+1),INFO)
        lineno=create_lineno(i+1,alpha,font,lineno_fgcolor,font.size*2,font.size//6)
        lines.append(text)
        linenos.append(lineno)
    line=None
    if verbose:
        debug_output('Start merging code lines',INFO)
    for i,j in enumerate(lines):
        if verbose:
            debug_output('Merging code line {}'.format(i+1),INFO)
        if i==0:
            line=j
        else:
            if line.shape[1]>j.shape[1]:
                j=image_fit(j,line.shape[1])
            else:
                line = image_fit(line, j.shape[1])
            line=image_merge_col(line,j)
    lineno = None
    if verbose:
        debug_output('Start merging line numbers',INFO)
    for i, j in enumerate(linenos):
        if verbose:
            debug_output('Merging line number {}'.format(i+1),INFO)
        if i == 0:
            lineno = j
        else:
            lineno = image_merge_col(lineno, j)
    if verbose:
        debug_output('Adding background',INFO)
    result=background.color(line,lineno)
    if verbose:
        debug_output('Done!',INFO)
    return result


def _cli():
    a=ArgumentParser()
    a.add_argument('-i','--code',help='Source code file name')
    a.add_argument('-V','--version',help='Print the version of sourceshot and exit',action='store_true')
    a.add_argument('-v','--verbose',help='Print out verbose logs',action='store_true')
    a.add_argument('-o','--output',help='Output image file name, the output image will be shown in a tkinter window if not given')
    a.add_argument('-f','--font',help='Font file name',default='simsun.ttc')
    a.add_argument('-s','--fontsize',help='Font size',default='30')
    a.add_argument('-l','--language',help='Source code language, if not given, the language will be automatically determined',default='auto')
    a.add_argument('-c','--config',help='Syntax highlight config JSON file')
    a.add_argument('-b','--background',help='Background color or image, could be:\n1. 6 hexadecimal bits representing the background color of the whole code.\n2. 12 hexadecimal bits, th first 6 represents the background color of the code, the lest 6 represents the background color of the line number.\n3. Path of an image.',default='FFFFFF')
    a.add_argument('-e','--encoding',help='Source code encoding',default='utf-8')
    a.add_argument('-t','--tabsize',help='Tab size',default='4')
    args=a.parse_args()
    if args.version:
        print(__version__)
        return
    if args.verbose:
        verbose=True
    else:
        verbose=False
    if not args.fontsize.isdigit():
        debug_output('Font size should be an integer',ERROR)
        return -1
    try:
        font=ImageFont.truetype(args.font,size=int(args.fontsize))
    except BaseException as e:
        debug_output('Error occurred when creating font instance: {}'.format(e),ERROR)
        return -1
    if args.config:
        config=color_config_from_json(open(args.config,'r').read())
    else:
        config=default_config
    expected_lang=args.language
    if args.code:
        if args.language=='auto':
            try:
                expected_lang=get_lexer_for_filename(args.code).name
            except:
                pass
        try:
            with open(args.code, 'r', encoding=args.encoding) as f:
                source = f.read()
        except UnicodeError:
            debug_output('Found chars which cannot be decoded in the current encoding \'{}\', these characters will be ignored'.format(args.encoding),WARNING)
            with open(args.code, 'r', encoding=args.encoding,errors='ignore') as f:
                source = f.read()
    else:
        debug_output('Read code from stdin',INFO)
        source=sys.stdin.read()
    try:
        tabsize=int(args.tabsize)
    except:
        debug_output('Tab size should be an integer', ERROR)
        return -1
    img=shot(source,config,verbose=verbose,lang=expected_lang,font=font,tabsize=tabsize,background=fromstr(args.background))
    if not args.output:
        try:
            image_show(img)
        except BaseException as e:
            debug_output('Error occurred when showing image: {}'.format(e), ERROR)
            return -1
    else:
        try:
            image_save(args.output, img)
        except BaseException as e:
            debug_output('Error occurred when saving file: {}'.format(e), ERROR)
            return -1
        debug_output('Successfully saved file as {}'.format(args.output),INFO)

__all__=['shot','default_config']
if __name__=="__main__":
    sys.exit(_cli())