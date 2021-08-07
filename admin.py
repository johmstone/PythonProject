import requests
from requests import models
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
from datetime import datetime
from tabulate import tabulate

monedero = []
transacciones = []
UserCode = ''

class Transaccion(object):
    def __init__(self, fecha, fromUser, toUser, tipo, monedaid, moneda, monto, montoUSD):
        self.fecha = fecha
        self.fromUser = fromUser
        self.toUser = toUser
        self.tipo = tipo
        self.monedaid = monedaid
        self.moneda = moneda
        self.monto = monto
        self.montoUSD = montoUSD

    def serialize(self):
        return {
            "Fecha": self.fecha.strftime("%m/%d/%Y, %H:%M:%S"),
            "De": self.fromUser,
            "Para": self.toUser,
            "Tipo de Transaccion": self.tipo,
            "Moneda": self.moneda,
            "Monto": self.monto,
            "Monto en USD": self.montoUSD
        }

class Criptomoneda(object):
    def __init__(self, id, internalid, nombre, saldo, cotizacion):
        self.id = id
        self.internalid = internalid
        self.nombre = nombre
        self.saldo = saldo
        self.cotizacion = cotizacion

    def indicarRate(self, cotizacion):
        self.cotizacion = cotizacion

    def DepositoDirecto(self, monto):
        self.saldo = self.saldo + monto
    
    def Transferencia(self, monto):
        self.saldo = self.saldo - monto

    def DepositoenUSD(self, monto):
        self.saldo = self.saldo + (monto/self.cotizacion)

    def calcularSaldo(self):  
        return self.saldo*self.cotizacion        
            
    def serialize(self):
        return {
            "id": self.id,
            "internalid": self.internalid,
            "nombre": self.nombre,
            "saldo": self.saldo
        }

def getMoneyDetail(id):
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?id=' + str(id)
    # print(url)
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': 'd23ea42b-4f22-47b3-8e28-4650f23c4096',
    }

    # session = Session()
    # session.headers.update(headers)
    try:
        response =  requests.get(url, headers=headers)
        data = json.loads(response.text)
        return(data)
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)

def initialdata():    
    monedero.append(Criptomoneda(1,1,'Bitcoins',0,0))
    monedero.append(Criptomoneda(1027,2,'Ethereum',0,0))
    monedero.append(Criptomoneda(1839,3,'Binance Coin',0,0))
    monedero.append(Criptomoneda(52,4,'XRP',0,0))

    for item in monedero:
        detail = getMoneyDetail(item.id)
        item.indicarRate(detail['data']["%s" % (item.id)]['quote']['USD']['price']) 
        # print(detail['data']["%s" % (item.id)]['quote']['USD']['price']) 

    print("===================================================================")
    print("======================= BUENOS DIAS ===============================")
    global UserCode
    UserCode = input("Por favor ingrese su codigo de Usuario: ")
    print("=== Gracias ===")

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

def CheckMoneyType(MoneyID):
    moneylist = []
    for item in monedero:
        moneylist.append(item.internalid)
    return MoneyID in moneylist

def SelectMoneyType():    
    ValidMoneyType = 0
    while ValidMoneyType == 0:
        getmonedas()
        moneyType = int(input("Seleccione la moneda?"))
        if(CheckMoneyType(moneyType)):
            ValidMoneyType = moneyType
            break
        else:
            print('El tipo de moneda seleccionado no existe')
            print("===================================================================")
    
    return ValidMoneyType

def SelectRemitente(msg):
    remitente = ''
    i = 0
    while i == 0:
        user = input(msg)
        if(user == UserCode):
            print('El código del remitente no es valido!!!')
        else:
            remitente = user
            break
    
    return remitente

def ValidAmount(msg,type,moneyID):
    amount = 0
    availableAmount = 0
    money = ''
    for item in monedero:
        if(item.internalid == moneyID):
            availableAmount = item.saldo
            money = item.nombre

    i = 0
    while i == 0:
        moneyQty = int(input(msg))
        if(moneyQty <= 0):
            print('Este monto es invalido!!!')
            continueNav()
        elif ((moneyQty > availableAmount) and (type == 'Debito')):
            print('Este monto excede al monto disponible (',availableAmount,money,").")
        else:
            amount = moneyQty
            break

    return amount

def continueNav():
    menu()
    option = int(input("Seleccione una opcion:"))
    actionMenu(option)

def Deposit(User, MoneyType, MoneyQty):
    MoneyName = ''
    USDAmount = 0
    for item in monedero:
            if item.internalid == MoneyType:
                item.DepositoDirecto(MoneyQty)
                MoneyName = item.nombre
                USDAmount = MoneyQty*item.cotizacion

    transacciones.append(Transaccion(datetime.now(),User, UserCode,'Credito',MoneyType,MoneyName,MoneyQty, USDAmount))

def Transfer(User, MoneyType, MoneyQty):
    MoneyName = ''
    USDAmount = 0
    for item in monedero:
            if item.internalid == MoneyType:
                item.Transferencia(MoneyQty)
                MoneyName = item.nombre
                USDAmount = MoneyQty*item.cotizacion

    transacciones.append(Transaccion(datetime.now(),UserCode, User,'Debito',MoneyType,MoneyName,MoneyQty, USDAmount))

def PrintBalanceByMoney(MoneyType):
    print("===================== BALANCE POR MONEDA ==========================")
    for item in monedero:
        if(item.internalid == MoneyType):
            print("=== Nuevo balance:",item.saldo, item.nombre, "==> Saldo en USD:", item.calcularSaldo(),"=====================")
    print("===================================================================")

def PrintMainBalance():
    TotalMoney = 0
    print("===================== BALANCE POR MONEDA ==========================")
    for item in monedero:
        TotalMoney = TotalMoney + item.calcularSaldo()
        print("=== Nuevo balance:",item.saldo, item.nombre, "==> Saldo en USD:", item.calcularSaldo(),"=====================")
    print("====================== BALANCE GENERAL ============================")
    print("=== Balance Total en USD:",TotalMoney)
    print("===================================================================")

def actionMenu(option):
    if option == 1:
        print("===================================================================")
        print("====================== RECIBIR DINERO =============================")
        UserCode = SelectRemitente('Por favor ingrese el codigo de Usuario que envió el dinero: ')
        ValidMoneyType = SelectMoneyType()
        moneyQty = ValidAmount('Por favor ingrese la cantidad a recibir?','Credito',ValidMoneyType)
        
        Deposit(UserCode,ValidMoneyType,moneyQty)

        # do stuff
        print("===================================================================")
        print("============================= HECHO ===============================")
        PrintBalanceByMoney(ValidMoneyType)
        continueNav()

    elif option == 2:
        print("===================================================================")
        print("==================== TRANSFERIR DINERO ============================")
        UserCode = SelectRemitente('Por favor ingrese el codigo de Usuario que recibe el dinero: ')
        ValidMoneyType = SelectMoneyType()
        moneyQty = ValidAmount('Por favor ingrese la cantidad a transferir?','Debito', ValidMoneyType)
        Transfer(UserCode,ValidMoneyType,moneyQty)
        # do stuff
        print("===================================================================")
        print("============================= HECHO ===============================")
        PrintBalanceByMoney(ValidMoneyType)
        continueNav()

    elif option == 3:
        # do stuff
        print("===================================================================")
        ValidMoneyType = SelectMoneyType()
        PrintBalanceByMoney(ValidMoneyType)
        continueNav()

    elif option == 4:
        print("===================================================================")
        PrintMainBalance()
        continueNav()

    elif option == 5:
        print("===================================================================")
        print("================ HISTORIAL DE TRANSACCIONES =======================")
        for item in transacciones:
            # print("=== Fecha:",item.fecha,"==> Tipo:", item.tipo, "==> Destino:", item.codigodestino, "==> Moneda:", item.moneda, "==> Monto:",item.monto ,"=====================")
            print(item.serialize())
        continueNav()
    else:
        print("=========== Salio del sistema =====================")

# Start all Logic Business
initialdata()    
menu()
option = int(input("Seleccione una opcion:"))
actionMenu(option)


# menu()
# option = int(input("Seleccione una opcion:"))
# actionMenu(option)