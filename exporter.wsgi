import os
import sys

path = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, path)
os.chdir(path)

from app import create_app
application = create_app()
