
print("======================================")
print("======================================")


def media(nota1, nota2, nota3):
    
    return (nota1 + nota2 + nota3) / 3


nota1 = float(input("Digite a primeira nota: "))


nota2 = float(input("Digite a segunda nota : ")
              )

nota3 = float(input("Digite a terceira nota: "))

resultado = media(nota1,nota2,nota3)


if resultado >= 7:
    print("aprovado com média: ", resultado)


elif resultado >= 5 and resultado < 7:
    print("recuperaçao com média:", resultado)
    

else:
    print("reprovado com média:" , resultado)
