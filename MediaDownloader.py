#**********#
# By Kaues #
#**********#
from functions import main, logo, pathList
from tkinter import messagebox
import os

print(logo)

for path in pathList:
    if not path.is_dir():
        os.mkdir(path)

try:
    main()
        
except KeyboardInterrupt:
    print("\nApp finalizado pelo usuário")