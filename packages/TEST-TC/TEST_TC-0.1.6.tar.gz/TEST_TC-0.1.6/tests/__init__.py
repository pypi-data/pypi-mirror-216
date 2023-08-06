import sys
import os

proj_path = os.path.split(os.path.dirname(os.path.abspath(__file__)))[0]
lib_path  = os.path.join(proj_path, os.path.split(proj_path)[1].lower())

sys.path.append(lib_path)