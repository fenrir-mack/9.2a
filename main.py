from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

itens = [
    {"id": 1, "nome": "Teclado Mecânico", "preco": 250.00},
    {"id": 2, "nome": "Mouse Gamer", "preco": 150.00}
]


@app.get("/")
def home():
    return "API FastAPI funcionando! Use os endpoints de /itens para interagir com a API."


@app.get("/itens")
def listar_itens():
    return itens


@app.get("/itens/{item_id}")
def obter_item(item_id: int):
    # Procura o item na lista
    item = next((i for i in itens if i["id"] == item_id), None)
    if item is None:
        return JSONResponse(content={"erro": "Item não encontrado"}, status_code=404)
    return item


# 3. POST - Criar um novo item (CREATE)
@app.post("/itens")
def criar_item(dados: dict):
    # Validação simples
    if not dados or "nome" not in dados or "preco" not in dados:
        return JSONResponse(content={"erro": "Dados inválidos. Envie 'nome' e 'preco'."}, status_code=400)

    # Cria o novo item gerando um ID incremental
    novo_id = max([item["id"] for item in itens], default=0) + 1
    novo_item = {
        "id": novo_id,
        "nome": dados["nome"],
        "preco": dados["preco"]
    }

    itens.append(novo_item)
    return JSONResponse(content=novo_item, status_code=201)


# 4. PUT - Atualizar um item existente por ID (UPDATE)
@app.put("/itens/{item_id}")
def atualizar_item(item_id: int, dados: dict):
    # Procura o item na lista
    item = next((i for i in itens if i["id"] == item_id), None)
    if item is None:
        return JSONResponse(content={"erro": "Item não encontrado"}, status_code=404)

    # Atualiza os dados se fornecidos no corpo da requisição
    item["nome"] = dados.get("nome", item["nome"])
    item["preco"] = dados.get("preco", item["preco"])

    return item


# 5. DELETE - Deletar um item por ID (DELETE)
@app.delete("/itens/{item_id}")
def deletar_item(item_id: int):
    global itens
    # Procura o item na lista
    item = next((i for i in itens if i["id"] == item_id), None)
    if item is None:
        return JSONResponse(content={"erro": "Item não encontrado"}, status_code=404)

    # Filtra a lista removendo o item com o ID especificado
    itens = [i for i in itens if i["id"] != item_id]
    return {"mensagem": f"Item {item_id} removido com sucesso!"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

