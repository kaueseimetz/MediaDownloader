from tkinter import messagebox
from pytubefix import YouTube, Playlist
import urllib, sys, requests, os
from urllib.parse import urlparse, ParseResult
from colorama import init, Fore, Style
from pathlib import Path

init()

logo = f"""
{Fore.RED}     _____          {Style.RESET_ALL}{Fore.BLUE}  _     _                   ___                    _                 _           {Style.RESET_ALL}
{Fore.RED}/\\_/\\__   \\   {Style.RESET_ALL}{Fore.BLUE} /\\   /(_) __| | ___  ___        /   \\_____      ___ __ | | ___   __ _  __| | ___ _ __ {Style.RESET_ALL}
{Fore.RED}\\_ _/ / /\\/    {Style.RESET_ALL}{Fore.BLUE}\\ \\ / / |/ _` |/ _ \\/ _ \\      / /\\ / _ \\ \\ /\\ / / '_ \\| |/ _ \\ / _` |/ _` |/ _ \\ '__|{Style.RESET_ALL}
{Fore.RED} / \\ / /        {Style.RESET_ALL}{Fore.BLUE}\\ V /| | (_| |  __/ (_) |    / /_// (_) \\ V  V /| | | | | (_) | (_| | (_| |  __/ |   {Style.RESET_ALL}
{Fore.RED} \\_/ \\/        {Style.RESET_ALL}{Fore.BLUE}  \\_/ |_|\\__,_|\\___|\\___/    /___,' \\___/ \\_/\\_/ |_| |_|_|\\___/ \\__,_|\\__,_|\\___|_|   {Style.RESET_ALL}
"""

menu = """
O que você deseja fazer?

1 - Baixar Vídeo Com Qualidade Máxima
2 - Baixar Apenas Áudio Do Vídeo
3 - Baixar Playlist (vídeo e áudio)
4 - Baixar Playlist (apenas áudio)

0 - Sair"""

def getVideoPath() -> os.path:
    # Obtém o caminho da pasta "Vídeos" do usuário
    caminho_videos: os.path = os.path.join(os.path.expanduser('~'), 'Videos')
    return caminho_videos

mediaPath: Path = Path(f"{getVideoPath()}/YT Video Downloader")
videoPath: Path = Path(f"{mediaPath}/Videos")
audioPath: Path = Path(f"{mediaPath}/Audio")

pathList: list[Path, Path, Path] = [mediaPath, videoPath, audioPath]

def GetVideo(URL: str, OpPath: Path) -> int:
    video = requests.get(URL)
    if video.status_code == 200:
        with open(f"{OpPath}\\{video.text}", 'wb') as file:
            file.write(video.content)
        return 200
    else:
        return video.status_code
    
def DownloadYoutubeVideo(URL: str, OpPath:Path) -> None:
    yt: YouTube = YouTube(URL)
    video: YouTube.streams = yt.streams.get_highest_resolution()
    video.download(output_path=OpPath)
    print(f"vídeo salvo em: \033]8;;file://{OpPath}\033\\{Fore.CYAN}{OpPath}{Style.RESET_ALL}\033]8;;\033\\")
    # \033]8;; create a hyperLink

def GetYoutubeAudio(URL: str, OpPath: Path) -> None:
    yt: YouTube = YouTube(URL)
    audio: YouTube.streams = yt.streams.get_audio_only()
    audio.download(output_path=OpPath)
    print(f"áudio salvo em: \033]8;;file://{OpPath}\033\\{Fore.CYAN}{OpPath}{Style.RESET_ALL}\033]8;;\033\\")    
    # \033]8;; create a hyperLink

def validar_video(url: str) -> bool:
    parsed_url: ParseResult = urlparse(url)

    if parsed_url.scheme == 'https' and parsed_url.netloc == 'www.youtube.com':
        path_parts: list[str] = parsed_url.path.split('/')
        if len(path_parts) >= 2 and path_parts[1] == 'watch':
            query_params: list[str] = parsed_url.query.split('&')
            for param in query_params:
                key, _ = param.split('=')
                if key == 'v':
                    return True

    return False

def validar_playlist(url) -> bool:
    parsed_url: ParseResult = urlparse(url)

    if parsed_url.scheme == 'https' and parsed_url.netloc == 'www.youtube.com':
        path_parts: list[str] = parsed_url.path.split('/')
        if len(path_parts) >= 2 and path_parts[1] == 'playlist':
            query_params: list[str] = parsed_url.query.split('&')
            for param in query_params:
                key, value = param.split('=')
                if key == 'list':
                    return True

    return False

def getURLByUser(formato: str) -> str:
    URL: str = input(f"insira o link d{formato}: ").strip()
    if validar_video(URL):
        return URL
    else:
        print(f"{Fore.RED}Link inválido.{Style.RESET_ALL} (ex: https://youtube.com/watch?v=AbCdEFgHijk)")
        return getURLByUser(formato)
    
def WebsiteStatus(website: str) -> bool:
    try:
        requests.get(website, timeout=5)
        return True
    except:
        return False

def DownloadVideoPlaylist(URL: str, OpPath: Path) -> None:
    if validar_playlist(URL):
        playlist:Playlist = Playlist(URL)
        for video in playlist:
            DownloadYoutubeVideo(video, OpPath)
    else:
        print("URL inválida.")

#maybe doesnt work        
def DownloadAudioPlaylist(URL: str, OpPath: Path) -> None:
    if validar_playlist(URL):
        playlist: Playlist = Playlist(URL)
        for audio in playlist:
            GetYoutubeAudio(URL, OpPath)
    else:
        print("URL inválida.")
    
def newDownload() -> callable:
    newDownloadBool: str = input("Deseja fazer um novo download? \n(S/N): ")
    if newDownloadBool == "S" or newDownloadBool == "s":
        return main()
    elif newDownloadBool == "N" or newDownloadBool == "n":
        print("Saíndo do app...")
        sys.exit()
    else:
        print("Opção inválida")
        return newDownload()     
        
def Menu(videoPath: Path, audioPath: Path) -> callable:
    print(menu)
    r: str = input("> ").strip()
    if r == "1":
            try:
                DownloadYoutubeVideo(getURLByUser("o vídeo"), videoPath)
            except urllib.error.URLError as e:
                #print(e)
                messagebox.showerror(title="Falha na conexão", message="Ocorreu uma falha de conexão durante o download, \nverifique a sua conexão com a internet e tente novamente.")
                return newDownload()
        
    elif r == "2":
        try:
            GetYoutubeAudio(getURLByUser("o áudio"), audioPath)
        except urllib.error.URLError:
                messagebox.showerror(title="Falha na conexão", message="Ocorreu uma falha de conexão durante o download, \nverifique a sua conexão com a internet e tente novamente.")
                return Menu()
    elif r == "3":
        try:
            DownloadVideoPlaylist(getURLByUser("a playlist (vídeos)"), videoPath)
        except urllib.error.URLError:
                messagebox.showerror(title="Falha na conexão", message="Ocorreu uma falha de conexão durante o download, \nverifique a sua conexão com a internet e tente novamente.")
                return Menu()
    elif r == "4":
        try:
            DownloadAudioPlaylist(getURLByUser("a playlist (áudios)"), audioPath)
        except urllib.error.URLError:
                messagebox.showerror(title="Falha na conexão", message="Ocorreu uma falha de conexão durante o download, \nverifique a sua conexão com a internet e tente novamente.")
                return Menu()
    elif r == "0":
        sys.exit()
    else:
        os.system('cls') or None
        return Menu()
    
def main() -> None:
    Menu(videoPath, audioPath)
