from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

monedero = []

class Criptomoneda(object):
    def __init__(self, id, internalid, nombre, saldo, cotizacion):
        self.id = id
        self.internalid = internalid
        self.nombre = nombre
        self.saldo = saldo
        self.cotizacion = cotizacion
    
    def calcularSaldo(self, moneda):  
        if moneda == "USD":
            return self.saldo*self.cotizacion
        else:
            return self.saldo
            
    def serialize(self):
        return {
            "id": self.id,
            "internalid": self.internalid,
            "nobmre": self.nombre,
            "saldo": self.saldo
        }

def getMoneyDetail(id):
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest' + str(id)
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': 'd23ea42b-4f22-47b3-8e28-4650f23c4096',
    }

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url)
        data = json.loads(response.text)
        print(data)
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)

def initialdata():
    
    monedero.append(Criptomoneda(1,1,'Bitcoins',0,0))
    monedero.append(Criptomoneda(1027,2,'Ethereum',0,0))
    monedero.append(Criptomoneda(1839,3,'Binance Coin',0,0))
    monedero.append(Criptomoneda(52,4,'XRP',0,0))

    for item in monedero


def getmonedas():
    print("Tipo de Moneda")
    print('[1] Bitcoins')
    print('[2] Ethereum')
    print('[3] Binance Coin')
    print('[4] XRP')

def menu():
    print("Menu")
    print("[1] Recibir Dinero")
    print("[2] Transferir Dinero")
    print("[3] Balance por moneda")
    print("[4] Balance General")
    print("[5] Historial de Transaccciones")
    print("[0] Salir del programa")

def recibirDinero():
    print("[1] Recibir Dinerop")
    print("[2] Transferir Dinero")
    print("[1] Recibir Dinero")
    print("[2] Transferir Dinero")


# Start all Logic Business
initialdata()    
menu()

option = int(input("Seleccione una opcion:"))

if option == 1:
    getmonedas()
    
    moneyType = int(input("Seleccione la moneda?"))
    moneyQty = int(input("Cantidad?"))

    for item in monedero:
        if item.internalid == moneyType:
            item.saldo = item.saldo + moneyQty

    # do stuff
    for item in monedero:
        print(item.id, item.nombre,item.saldo)



elif option == 2:
    print("option 2")
elif option == 3:
    print("option 3")
elif option == 4:
    print("option 4")
else:
    print("option 5")
