import os, functions, urllib
from pathlib import Path
from tkinter import messagebox

menu = """
O que você deseja fazer?

1 - Baixar Vídeo Com Qualidade Máxima
2 - Baixar Apenas Áudio Do Vídeo
3 - Baixar Playlist (vídeo e áudio)
4 - Baixar Playlist (apenas áudio)

0 - Sair
"""
mediaPath = Path(f"{functions.getVideoPath()}\\YT Video Downloader")
videoPath = Path(f"{mediaPath}\\Videos")
audioPath = Path(f"{mediaPath}\\Audio")

def Menu():
    try:
        print(menu)
        r = input("> ")
        if r == "1":
                try:
                    functions.GetYoutubeVideo(functions.getURLByUser(), videoPath)
                except urllib.error.URLError:
                    messagebox.showerror(title="Falha na conexão", message="Ocorreu uma falha de conexão durante o download, \nverifique a sua conexão com a internet e tente novamente.")
                    functions.newDownload()
            
        elif r == "2":
            pass
        elif r == "3":
            pass
        elif r == "0":
            pass
        else:
            os.system('cls') or None
            return Menu()
    except KeyboardInterrupt:
            print("\nFechado Pelo Usuário")
        
Menu()