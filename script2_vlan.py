vlan = int(input("Ingresa número de VLAN: "))

if 1 <= vlan <= 1005:
    print("La VLAN es de rango NORMAL.")
elif 1006 <= vlan <= 4094:
    print("La VLAN es de rango EXTENDIDO.")
else:
    print("Número de VLAN inválido.")
