from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import requests

app = FastAPI()
#Nossa lista para guardar os sucos cadastrados e um contador de IDs
banco_sucos = []
contador_id = 1

# Modelo que valida os dados enviados no cadastro de suco 
class SucoInput(BaseModel):
     nome: str
     frutas: List[str]
     tem_gosto_de: str
#==================================================================] 
#PARTE 1 CONSULTAR FRUTA (GET / FRUTAS /frutas/{nome})
#==================================================================]
@app.get("/frutas/{nome}")
def consultar_fruta(nome: str):
     #1. Monta a URL da api externa com o nome da fruta
     url = f"https://www.fruityvice.com/api/fruit/{nome.lower()}"

     #2- requisiçao GET
     resposta = requests. get(url)

     #3- tratamos caso da fruta não existir(requisito 4)
     if resposta.status_code != 200:
          raise HTTPException(status_code=404, detail="Fruta não encontrada na base de dados.")

     #4 e 5.Converte para JSON e filtra os campos pedidos 
     dados = resposta.json()
     return{
          "nome": dados .get("name"),
          "calorias": dados.get("nutritions", {}).get("calories"),
          "acucar": dados.get("nutritions", {}).get("sugar")
     }

#===============================================================]
#PARTE 2: Cadastrar Suco (POST /sucos)
#===============================================================]
@app.post("/sucos" , status_code=201)
def cadastrar_suco(suco: SucoInput):
    global contador_id

    total_calorias = 0.0
    total_acucar = 0.0
     # Passa por cada fruta enviada na lista
    for nome_fruta in suco.frutas:
        url = f"https://www.fruityvice.com/api/fruit/{nome_fruta.lower()}"
        resposta = requests.get(url)
     #se alguma fruta nao existir, retorna erro 404 
        if resposta.status_code != 200:
            raise HTTPException(
                status_code=404,
                detail=f"A fruta '{nome_fruta}' não foi encontrada na base de dados"
            )

        dados = resposta.json()
        nutricoes = dados.get("nutritions", {})

          #soma de calorias e açúcar
        total_calorias +=  nutricoes.get("calories", 0.0)
        total_acucar += nutricoes.get("sugar", 0.0)
     #Monta o dicinário com o resultado funal do suco
    novo_suco = {
        "id": contador_id,
        "nome": suco.nome,
        "frutas": suco.frutas,
        "tem_gosto_de": suco.tem_gosto_de,
        "total_calorias": round(total_calorias, 2),
        "total_acucar": round(total_acucar, 2)
    }

     # Salva na lista temporária e incrementa o ID para o próximo 
    banco_sucos.append(novo_suco)
    contador_id += 1
 
    return novo_suco

#___________________________________]
#LISTAR SUCOS CADASTRADOS (GET)
#__________________________________[
@app.get("/sucos")
def listar_sucos():
    return banco_sucos

#======================================
#Buscar Suco por ID (GET)
#======================================
@app.get("/sucos/{id}")
def buscar_suco_por_id(id: int):
    for suco in banco_sucos:
        if suco["id"] == id:
            return suco

    raise HTTPException(
        status_code=404,
        detail=f"Suco com ID {id} não foi encontrado."
    )
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@]
#DELETE funçao que apagaga um suco da lista de fucos@]
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@]
@app.delete("/sucos/{suco_id}")
def deletar_suco(suco_id: int):
    for index, suco  in enumerate(banco_sucos):
        if suco["id"] == suco_id: 
            suco_removido = banco_sucos.pop(index)
            return {
             "mensagem": "suco  deletado com sucesso!",
             "suco_removido": suco_removido
         }
    raise HTTPException(status_code=404, detail="suco não encontrado para exclusão")
