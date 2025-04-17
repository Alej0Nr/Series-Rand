import requests
import random
import re

debug = False
# get API_KEY from https://developer.themoviedb.org/docs/getting-started
API_KEY= ''


headers = {
    "accept": "application/json",
    "Authorization": "Bearer "+API_KEY
}


def series_input(serie=None):
    def series(x):
        if x==None:
            x = input("Ingrese la serie que desea ver: ")
            x = x.replace(' ','%20')
            return f"https://api.themoviedb.org/3/search/tv?query={x}&include_adult=true&page=1"
        x = x.replace(' ','%20')
        return f"https://api.themoviedb.org/3/search/tv?query={x}&include_adult=true&page=1"
    url = series(serie)
    response = requests.get(url, headers= headers)
    data = response.json().get("results",[])
    n = 0
    for i in data[:5]:
        print(f"\033[92m{n = }\033[0m\n{'Nombre:':<16}{i.get('name')}\n{'Descripción:':<16}{i.get('overview')}\n")
        n+=1
    question = input(f"Si la serie esta en la lista ingrese\033[92m n\033[0m, en otro caso ingrese el nombre de otra: ")
    if question in [f'{i}' for i in range(len(data))]:
        global watch_serie
        watch_serie = str(data[int(question)].get("original_name"))
        return str(data[int(question)].get("id"))
    else:
        return series_input(question)

def serie_rand(id):
    url = "https://api.themoviedb.org/3/tv/"+id
    response = requests.get(url, headers=headers)
    data = response.json().get("seasons")
    EPS=[]
    for i in data:
        EPS.append([i.get("season_number"), i.get("episode_count")])
    if EPS[0][0]==0: # elimina si hay temporada de especiales
        EPS = EPS[1:]
    if debug:
        print("TxE = ",EPS)
    def choose(x='N'):

        temp= random.choice(EPS)
        t = temp[0]
        e = random.choice([i+1 for i in range(temp[1])])
        print(f"\nTemporada {t} episodio {e}")
        x= input(f"Quieres ver este capitulo? Y/N: ")
        if x != 'Y':
            t,e = choose(x)
        return [t,e]
    watch = choose()
    return watch

def format_name(name):
    name = name.strip().lower()
    name = name.replace('&', '')
    name = name.replace(',', '')
    name = re.sub(r"[ :'\.\+]+", "-", name)
    name = re.sub(r"-+", "-", name)
    return name.strip("-")

def close():
    x = input(f"\n'C' para cerrar: ")
    if x!='C':
        close()
    return
    
###
"""

Future work
- return name of episode https://api.themoviedb.org/3/tv/{series_id}/season/{season_number}/episode/{episode_number}
- return to series browser
- explanation at the beginning
- add colors to text (n = )?

"""
###
# https://www.themoviedb.org/tv/66573-the-good-place/season/4/episode/1?language=es
###
if __name__ == '__main__':
    watch_serie = None
    n = series_input()
    T, E = serie_rand(n)
    watch_serie = format_name(watch_serie)
    url = f"\n\033[36mhttps://www.themoviedb.org/tv/{n}-{watch_serie}/season/{T}/episode/{E}?language=es\033[0m"
    print(url)
    close()
