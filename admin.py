def menu():
    print("[1] Recibir Dinero")
    print("[2] Transferir Dinero")
    print("[3] Balance por moneda")
    print("[4] Balance General")
    print("[5] Historial de Transaccciones")
    print("[0] Salir del programa")

menu()

option = int(input("Seleccione una opcion:"))

if option == 1:
    print("option1")
elif option == 2:
    print("option 2")
elif option == 3:
    print("option 3")
elif option == 4:
    print("option 4")
else:
    print("option 5")
