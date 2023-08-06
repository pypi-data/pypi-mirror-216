from colorama import Fore
import sys
ERROR=0
WARNING=1
INFO=2
def debug_output(text,level):
    val=['[ERROR]','[WARNING]','[INFO]']
    color=[Fore.RED,Fore.YELLOW,Fore.LIGHTBLUE_EX]
    print(color[level]+val[level]+Fore.RESET,' '+text,file=sys.stderr,flush=True)
