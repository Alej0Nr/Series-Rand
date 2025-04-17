import requests
import random

# get API_KEY from https://developer.themoviedb.org/docs/getting-started
API_KEY= ''

y= input("Ingrese la serie que desea ver: ")
y= y.replace(' ','%20')

url = f"https://api.themoviedb.org/3/search/tv?query={y}&include_adult=true&page=1"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer "+API_KEY
}

response = requests.get(url, headers=headers)
DATA = response.json().get("results",[])[:5]
n = 0
for i in DATA:
    print(f"{n = }\n{"Nombre:":<16}{i.get("name")}\n{"Descripción:":16}{i.get("overview")}\n")
    n+=1
x= int(input("Ingresa n de serie: "))
SERIE_id = str(DATA[x].get("id"))
# print(SERIE_id)
url_serie = "https://api.themoviedb.org/3/tv/"+SERIE_id
respuesta = requests.get(url_serie, headers=headers)
SERIE_DATA = respuesta.json().get("seasons")

EPS=[]
for i in SERIE_DATA:
    EPS.append([i.get("season_number"), i.get("episode_count")])

print("TxE = ",EPS)
def elegir(x='N'):
    temp= random.choice(EPS)
    ep= random.choice([i+1 for i in range(temp[1])])
    print(f"Temporada {temp[0]} episodio {ep}")
    x= input(f"Quieres ver este capitulo? Y/N: ")
    if x != 'Y':
        elegir(x)
    else:
        return
elegir()

