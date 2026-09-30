import random
cardapio = {
    "chocolate": 5.00,
    "baunilha":4.50,
    "morango": 3.00,
    "flocos":4.00,
}

brindes = ["Canudo", "Copo personalizado", "Gelo", "Badge"]

def mostrar_cardapio():
    print("-- CARDAPIO --")
    for sabor, preco in cardapio.items():
        print(f"{sabor}: R$ {preco}")

def fazer_pedido():
    total = 0        
    pedido = []
    while True:
        sabor = input("Escolha um sabor ou fechar para sair: ")
        if sabor == "fechar":
            print("pedido finalizado.")
            break
        elif sabor in cardapio:
            total += cardapio[sabor]
            pedido.append(sabor)
            print(f"{sabor} adicionado!")
        else:
            print("sabor nao esta no cardapio.")
    return pedido, total
mostrar_cardapio()
pedido, total = fazer_pedido()
print(f"\nSeu pedido: {pedido}")
print(f"Total: R$ {total:.2f}")

if total > 15:
    print(f"VOCE GANHOU UM BRINDE: {random.choice(brindes)}")