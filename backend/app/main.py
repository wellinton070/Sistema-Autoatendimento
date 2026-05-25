from flask import Flask, jsonify, request

app = Flask(__name__)

# ---------- Dados simulados (em produção viria do banco) ----------
PRODUTOS = [
    {"id": 1, "nome": "X-Burguer",   "preco": 18.90, "ativo": True},
    {"id": 2, "nome": "Coca-Cola",   "preco":  7.00, "ativo": True},
    {"id": 3, "nome": "Frango Grelhado", "preco": 22.50, "ativo": False},
]

# ---------- Rotas ----------

@app.route("/")
def home():
    return jsonify({"mensagem": "API Flask rodando 🚀"})


@app.route("/api/cardapio")
def cardapio():
    """Retorna apenas os produtos ativos."""
    ativos = [p for p in PRODUTOS if p["ativo"]]
    return jsonify(ativos)


@app.route("/api/pedido", methods=["POST"])
def criar_pedido():
    """Cria um pedido; rejeita carrinho vazio."""
    dados = request.get_json(silent=True) or {}
    itens = dados.get("itens", [])

    if not itens:
        return jsonify({"erro": "Carrinho vazio. Adicione itens antes de pedir."}), 400

    return jsonify({"mensagem": "Pedido recebido com sucesso!", "itens": itens}), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
