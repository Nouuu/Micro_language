from ply4ever.calcBase import *
import ply.yacc as yacc

from ply4ever.consoleColor import bcolors

yacc.yacc()

print(f"""
{bcolors.HEADER + bcolors.BOLD}Welcome to PYLang!{bcolors.ENDC}
{bcolors.BOLD}------------------------------------------------{bcolors.ENDC}
Enter {bcolors.OKGREEN}exit();{bcolors.ENDC} to leave
Enter {bcolors.OKGREEN}debugOn();{bcolors.ENDC} to show treeGraph {bcolors.WARNING}(must have graphviz installed){bcolors.ENDC}
Enter {bcolors.OKGREEN}debugOff();{bcolors.ENDC} to disable treeGraph showing (default)
Enter {bcolors.OKGREEN}load("<filename>");{bcolors.ENDC} to file with valid code
{bcolors.BOLD}------------------------------------------------{bcolors.ENDC}
""")

set_yacc(yacc)
load_files()
cli()
