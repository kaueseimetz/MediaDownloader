#**********#
# By Kaues #
#**********#
from functions import getURLByUser, GetYoutubeVideo, getVideoPath, WebsiteStatus, logo
from tkinter import messagebox
from pathlib import Path
import os, urllib, sys


print(logo)

mediaPath = Path(f"{getVideoPath()}\\YT Video Downloader")
videoPath = Path(f"{mediaPath}\\Videos")
audioPath = Path(f"{mediaPath}\\Audio")

pathList = [mediaPath, videoPath, audioPath]

for path in pathList:
    if not path.is_dir():
        os.mkdir(path)

def newDownload():
    newDownloadBool = input("Deseja fazer um novo download? \n(S/N): ")
    if newDownloadBool == "S" or newDownloadBool == "s":
        return main()
    elif newDownloadBool == "N" or newDownloadBool == "n":
        print("Saíndo do app...")
        sys.exit()
    else:
        print("Opção inválida")
        return newDownload()
    
def main():
    try:
        GetYoutubeVideo(getURLByUser(), videoPath)
    except urllib.error.URLError:
        messagebox.showerror(title="Falha na conexão", message="Ocorreu uma falha de conexão durante o download, \nverifique a sua conexão com a internet e tente novamente.")
    newDownload()
    
try:
    if WebsiteStatus("https://www.youtube.com"):
        main()
    else:
        messagebox.showerror(title="Falha na conexão", message="Ocorreu uma falha durante a conexão com a internet, \nverifique a sua conexão com a internet e tente novamente.")
        
except KeyboardInterrupt:
    print("\nApp finalizado pelo usuário")