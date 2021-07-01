from ply4ever.calcBase import *
import ply.yacc as yacc
yacc.yacc()

load_files(yacc)
cli(yacc)