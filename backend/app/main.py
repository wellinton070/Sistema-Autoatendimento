import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from datetime import datetime

app = Flask(__name__)
CORS(app)

# ── Banco de dados ──────────────────────────────────────────────
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5433/autoatendimento"
)

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
Base = declarative_base()


# ── Modelos ─────────────────────────────────────────────────────
class Produto(Base):
    __tablename__ = "produtos"

    id       = Column(Integer, primary_key=True)
    nome     = Column(String(100), nullable=False)
    descricao= Column(Text, default="")
    preco    = Column(Float, nullable=False)
    categoria= Column(String(50), default="Geral")
    ativo    = Column(Boolean, default=True)


class Pedido(Base):
    __tablename__ = "pedidos"

    id          = Column(Integer, primary_key=True)
    mesa        = Column(Integer, nullable=False)
    cliente     = Column(String(100), nullable=False)
    status      = Column(String(30), default="recebido")   # recebido | preparando | pronto
    criado_em   = Column(DateTime, default=datetime.utcnow)
    itens       = relationship("ItemPedido", back_populates="pedido", cascade="all, delete-orphan")


class ItemPedido(Base):
    __tablename__ = "itens_pedido"

    id          = Column(Integer, primary_key=True)
    pedido_id   = Column(Integer, ForeignKey("pedidos.id"), nullable=False)
    produto_id  = Column(Integer, nullable=False)
    nome_produto= Column(String(100), nullable=False)
    quantidade  = Column(Integer, default=1)
    preco_unit  = Column(Float, nullable=False)
    pedido      = relationship("Pedido", back_populates="itens")


# Cria as tabelas automaticamente se não existirem
def init_db():
    Base.metadata.create_all(engine)
    # Insere produtos de exemplo se o banco estiver vazio
    with Session() as session:
        if session.query(Produto).count() == 0:
            produtos_iniciais = [
                Produto(nome="X-Burguer",        descricao="Pão, carne, queijo e alface",  preco=18.90, categoria="Lanches"),
                Produto(nome="X-Bacon",          descricao="Pão, carne, bacon e queijo",   preco=22.90, categoria="Lanches"),
                Produto(nome="Frango Grelhado",  descricao="Pão, frango grelhado e salada", preco=20.50, categoria="Lanches"),
                Produto(nome="Batata Frita",     descricao="Porção grande crocante",        preco=12.00, categoria="Acompanhamentos"),
                Produto(nome="Coca-Cola",        descricao="Lata 350ml",                   preco=7.00,  categoria="Bebidas"),
                Produto(nome="Suco de Laranja",  descricao="Natural 300ml",                preco=9.00,  categoria="Bebidas"),
                Produto(nome="Sorvete",          descricao="2 bolas, sabores variados",    preco=10.00, categoria="Sobremesas"),
                Produto(nome="Pudim",            descricao="Fatia individual",             preco=8.50,  categoria="Sobremesas",  ativo=False),
            ]
            session.add_all(produtos_iniciais)
            session.commit()


# ── Rotas ────────────────────────────────────────────────────────

@app.route("/")
def home():
    return jsonify({"mensagem": "API Flask rodando 🚀"})


@app.route("/api/cardapio")
def cardapio():
    """Retorna produtos ativos, opcionalmente filtrados por categoria."""
    categoria = request.args.get("categoria")
    with Session() as session:
        query = session.query(Produto).filter(Produto.ativo == True)
        if categoria:
            query = query.filter(Produto.categoria == categoria)
        produtos = query.all()
        return jsonify([{
            "id":        p.id,
            "nome":      p.nome,
            "descricao": p.descricao,
            "preco":     p.preco,
            "categoria": p.categoria,
            "ativo":     True,
        } for p in produtos])


@app.route("/api/pedido", methods=["POST"])
def criar_pedido():
    """Cria um novo pedido."""
    dados = request.get_json(silent=True) or {}
    itens    = dados.get("itens", [])
    mesa     = dados.get("mesa")
    cliente  = dados.get("cliente", "").strip()

    if not itens:
        return jsonify({"erro": "Carrinho vazio. Adicione itens antes de pedir."}), 400
    if not mesa:
        return jsonify({"erro": "Número da mesa não informado."}), 400
    if not cliente:
        return jsonify({"erro": "Nome do cliente não informado."}), 400

    with Session() as session:
        pedido = Pedido(mesa=mesa, cliente=cliente)
        for item in itens:
            pedido.itens.append(ItemPedido(
                produto_id   = item.get("id"),
                nome_produto = item.get("nome", ""),
                quantidade   = item.get("quantidade", 1),
                preco_unit   = item.get("preco", 0),
            ))
        session.add(pedido)
        session.commit()

        return jsonify({
            "mensagem":  "Pedido recebido com sucesso! 🎉",
            "pedido_id": pedido.id,
            "mesa":      pedido.mesa,
            "cliente":   pedido.cliente,
            "status":    pedido.status,
        }), 201


@app.route("/api/pedidos")
def listar_pedidos():
    """Lista todos os pedidos (painel da cozinha)."""
    with Session() as session:
        pedidos = session.query(Pedido).order_by(Pedido.criado_em.desc()).all()
        return jsonify([{
            "id":       p.id,
            "mesa":     p.mesa,
            "cliente":  p.cliente,
            "status":   p.status,
            "criado_em": p.criado_em.strftime("%H:%M"),
            "itens": [{
                "nome":       i.nome_produto,
                "quantidade": i.quantidade,
                "preco":      i.preco_unit,
            } for i in p.itens],
        } for p in pedidos])


@app.route("/api/pedido/<int:pedido_id>/status", methods=["PATCH"])
def atualizar_status(pedido_id):
    """Atualiza status do pedido (cozinha usa isso)."""
    dados  = request.get_json(silent=True) or {}
    status = dados.get("status")
    validos = ["recebido", "preparando", "pronto"]

    if status not in validos:
        return jsonify({"erro": f"Status inválido. Use: {validos}"}), 400

    with Session() as session:
        pedido = session.get(Pedido, pedido_id)
        if not pedido:
            return jsonify({"erro": "Pedido não encontrado."}), 404
        pedido.status = status
        session.commit()
        return jsonify({"mensagem": f"Status atualizado para '{status}'."})


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5001, debug=True)
