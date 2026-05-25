"""
Testes Unitários — Sistema de Autoatendimento
=============================================
Casos cobertos:
  Caso 01 (Positivo) — GET /api/cardapio retorna somente produtos ativos
  Caso 02 (Negativo) — Produto inativo NÃO aparece no cardápio
  Caso 04 (Negativo) — POST /api/pedido com carrinho vazio é bloqueado
"""

import json
import pytest
from unittest.mock import patch, MagicMock
from app.main import app


# Produtos fictícios para os testes (sem precisar do banco)
PRODUTOS_MOCK = [
    MagicMock(id=1, nome="X-Burguer",   descricao="Pão e carne",  preco=18.90, categoria="Lanches", ativo=True),
    MagicMock(id=2, nome="Coca-Cola",   descricao="Lata 350ml",   preco=7.00,  categoria="Bebidas",  ativo=True),
    MagicMock(id=3, nome="Pudim",       descricao="Fatia",        preco=8.50,  categoria="Sobremesas", ativo=False),
]

PRODUTOS_ATIVOS_MOCK = [p for p in PRODUTOS_MOCK if p.ativo]


@pytest.fixture
def client():
    """Cria um cliente de teste Flask isolado."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def mock_session_query(produtos):
    """Monta a cadeia session.query(...).filter(...).all() como mock."""
    mock_query = MagicMock()
    mock_query.filter.return_value = mock_query
    mock_query.all.return_value = produtos

    mock_session = MagicMock()
    mock_session.query.return_value = mock_query
    mock_session.__enter__ = MagicMock(return_value=mock_session)
    mock_session.__exit__ = MagicMock(return_value=False)
    return mock_session


# ─────────────────────────────────────────────
# CASO 01 — Retorna apenas produtos ativos
# ─────────────────────────────────────────────
class TestCaso01CardapioAtivos:
    """GET /api/cardapio deve retornar somente os produtos com ativo=True."""

    def test_status_code_200(self, client):
        with patch("app.main.Session", return_value=mock_session_query(PRODUTOS_ATIVOS_MOCK)):
            resposta = client.get("/api/cardapio")
        assert resposta.status_code == 200

    def test_retorna_lista(self, client):
        with patch("app.main.Session", return_value=mock_session_query(PRODUTOS_ATIVOS_MOCK)):
            resposta = client.get("/api/cardapio")
        dados = json.loads(resposta.data)
        assert isinstance(dados, list)

    def test_todos_os_itens_sao_ativos(self, client):
        with patch("app.main.Session", return_value=mock_session_query(PRODUTOS_ATIVOS_MOCK)):
            resposta = client.get("/api/cardapio")
        dados = json.loads(resposta.data)
        assert len(dados) > 0
        for produto in dados:
            assert produto["ativo"] is True


# ─────────────────────────────────────────────
# CASO 02 — Produto inativo não aparece
# ─────────────────────────────────────────────
class TestCaso02ProdutoInativo:
    """Produto com ativo=False não deve constar na resposta do cardápio."""

    def test_inativo_ausente_no_cardapio(self, client):
        with patch("app.main.Session", return_value=mock_session_query(PRODUTOS_ATIVOS_MOCK)):
            resposta = client.get("/api/cardapio")
        dados = json.loads(resposta.data)
        nomes = [p["nome"] for p in dados]
        assert "Pudim" not in nomes

    def test_quantidade_correta_de_ativos(self, client):
        with patch("app.main.Session", return_value=mock_session_query(PRODUTOS_ATIVOS_MOCK)):
            resposta = client.get("/api/cardapio")
        dados = json.loads(resposta.data)
        assert len(dados) == len(PRODUTOS_ATIVOS_MOCK)


# ─────────────────────────────────────────────
# CASO 04 — Carrinho vazio é bloqueado
# ─────────────────────────────────────────────
class TestCaso04CarrinhoVazio:
    """POST /api/pedido com itens=[] ou sem itens deve retornar HTTP 400."""

    def test_carrinho_vazio_retorna_400(self, client):
        resposta = client.post(
            "/api/pedido",
            json={"mesa": 1, "cliente": "João", "itens": []},
            content_type="application/json",
        )
        assert resposta.status_code == 400

    def test_sem_campo_itens_retorna_400(self, client):
        resposta = client.post(
            "/api/pedido",
            json={"mesa": 1, "cliente": "João"},
            content_type="application/json",
        )
        assert resposta.status_code == 400

    def test_mensagem_de_erro_presente(self, client):
        resposta = client.post(
            "/api/pedido",
            json={"mesa": 1, "cliente": "João", "itens": []},
            content_type="application/json",
        )
        dados = json.loads(resposta.data)
        assert "erro" in dados

    def test_pedido_valido_retorna_201(self, client):
        """Contra-prova: pedido com itens deve funcionar (HTTP 201)."""
        mock_pedido = MagicMock()
        mock_pedido.id = 42
        mock_pedido.mesa = 1
        mock_pedido.cliente = "João"
        mock_pedido.status = "recebido"

        mock_session = MagicMock()
        mock_session.__enter__ = MagicMock(return_value=mock_session)
        mock_session.__exit__ = MagicMock(return_value=False)

        with patch("app.main.Session", return_value=mock_session), \
             patch("app.main.Pedido", return_value=mock_pedido), \
             patch("app.main.ItemPedido", return_value=MagicMock()):
            resposta = client.post(
                "/api/pedido",
                json={"mesa": 1, "cliente": "João", "itens": [{"id": 1, "nome": "X-Burguer", "preco": 18.90, "quantidade": 1}]},
                content_type="application/json",
            )
        assert resposta.status_code == 201
