import requests
from pytube import YouTube
import os
from urllib.parse import urlparse
from colorama import init, Fore, Style

init()

logo = f"""
{Fore.RED}     _____          {Style.RESET_ALL}{Fore.BLUE}  _     _                   ___                    _                 _           {Style.RESET_ALL}
{Fore.RED}/\\_/\\__   \\   {Style.RESET_ALL}{Fore.BLUE} /\\   /(_) __| | ___  ___        /   \\_____      ___ __ | | ___   __ _  __| | ___ _ __ {Style.RESET_ALL}
{Fore.RED}\\_ _/ / /\\/    {Style.RESET_ALL}{Fore.BLUE}\\ \\ / / |/ _` |/ _ \\/ _ \\      / /\\ / _ \\ \\ /\\ / / '_ \\| |/ _ \\ / _` |/ _` |/ _ \\ '__|{Style.RESET_ALL}
{Fore.RED} / \\ / /        {Style.RESET_ALL}{Fore.BLUE}\\ V /| | (_| |  __/ (_) |    / /_// (_) \\ V  V /| | | | | (_) | (_| | (_| |  __/ |   {Style.RESET_ALL}
{Fore.RED} \\_/ \\/        {Style.RESET_ALL}{Fore.BLUE}  \\_/ |_|\\__,_|\\___|\\___/    /___,' \\___/ \\_/\\_/ |_| |_|_|\\___/ \\__,_|\\__,_|\\___|_|   {Style.RESET_ALL}
"""

def GetVideo(URL, OpPath):
    video = requests.get(URL)
    if video.status_code == 200:
        with open(f"{OpPath}\\{video.text}", 'wb') as file:
            file.write(video.content)
        return 200
    else:
        return video.status_code
    
def GetYoutubeVideo(URL, OpPath):
    yt = YouTube(URL)
    video = yt.streams.get_highest_resolution()
    video.download(output_path=OpPath)
    print(f"vídeo salvo em: \033]8;;file://{OpPath}\033\\{Fore.CYAN}{OpPath}{Style.RESET_ALL}\033]8;;\033\\")
    
def getVideoPath():
    # Obtém o caminho da pasta "Vídeos" do usuário
    caminho_videos = os.path.join(os.path.expanduser('~'), 'Videos')
    return caminho_videos

def validar_url(url):
    # Analisa a URL
    parsed_url = urlparse(url)

    # Verifica se o esquema é 'https' e o netloc é 'www.youtube.com'
    if parsed_url.scheme == 'https' and parsed_url.netloc == 'www.youtube.com':
        # Verifica se o caminho começa com '/watch' e tem um parâmetro 'v'
        path_parts = parsed_url.path.split('/')
        if len(path_parts) >= 2 and path_parts[1] == 'watch':
            query_params = parsed_url.query.split('&')
            for param in query_params:
                key, value = param.split('=')
                if key == 'v':
                    return True

    return False

def getURLByUser():
    URL = input("insira o link do vídeo: ").strip()
    if validar_url(URL):
        url = URL
        return url
    else:
        print(f"{Fore.RED}Link inválido.{Style.RESET_ALL} (ex: https://youtube.com/watch?v=AbCdEFgHijk)")
        return getURLByUser()
def WebsiteStatus(website):
    try:
        requests.get(website, timeout=5)
        return True
    except:
        return False

