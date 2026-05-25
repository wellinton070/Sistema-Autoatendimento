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
from app.main import app, PRODUTOS


@pytest.fixture
def client():
    """Cria um cliente de teste Flask isolado."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


# ─────────────────────────────────────────────
# CASO 01 — Retorna apenas produtos ativos
# ─────────────────────────────────────────────
class TestCaso01CardapioAtivos:
    """GET /api/cardapio deve retornar somente os produtos com ativo=True."""

    def test_status_code_200(self, client):
        resposta = client.get("/api/cardapio")
        assert resposta.status_code == 200, "Esperado HTTP 200"

    def test_retorna_lista(self, client):
        resposta = client.get("/api/cardapio")
        dados = json.loads(resposta.data)
        assert isinstance(dados, list), "Resposta deve ser uma lista"

    def test_todos_os_itens_sao_ativos(self, client):
        resposta = client.get("/api/cardapio")
        dados = json.loads(resposta.data)
        assert len(dados) > 0, "Deve haver ao menos um produto ativo"
        for produto in dados:
            assert produto["ativo"] is True, (
                f"Produto '{produto['nome']}' não deveria aparecer (ativo=False)"
            )


# ─────────────────────────────────────────────
# CASO 02 — Produto inativo não aparece
# ─────────────────────────────────────────────
class TestCaso02ProdutoInativo:
    """Produto com ativo=False não deve constar na resposta do cardápio."""

    def test_inativo_ausente_no_cardapio(self, client):
        # Identifica nomes de produtos inativos nos dados de teste
        inativos = [p["nome"] for p in PRODUTOS if not p["ativo"]]
        assert len(inativos) > 0, "Precisa haver ao menos um produto inativo nos dados de teste"

        resposta = client.get("/api/cardapio")
        dados = json.loads(resposta.data)
        nomes_retornados = [p["nome"] for p in dados]

        for nome_inativo in inativos:
            assert nome_inativo not in nomes_retornados, (
                f"'{nome_inativo}' está inativo mas apareceu no cardápio"
            )

    def test_quantidade_correta_de_ativos(self, client):
        qtd_ativos_esperada = sum(1 for p in PRODUTOS if p["ativo"])
        resposta = client.get("/api/cardapio")
        dados = json.loads(resposta.data)
        assert len(dados) == qtd_ativos_esperada, (
            f"Esperava {qtd_ativos_esperada} produto(s) ativo(s), "
            f"mas recebeu {len(dados)}"
        )


# ─────────────────────────────────────────────
# CASO 04 — Carrinho vazio é bloqueado
# ─────────────────────────────────────────────
class TestCaso04CarrinhoVazio:
    """POST /api/pedido com itens=[] ou sem itens deve retornar HTTP 400."""

    def test_carrinho_vazio_retorna_400(self, client):
        resposta = client.post(
            "/api/pedido",
            json={"itens": []},
            content_type="application/json",
        )
        assert resposta.status_code == 400, "Carrinho vazio deve retornar HTTP 400"

    def test_sem_campo_itens_retorna_400(self, client):
        resposta = client.post(
            "/api/pedido",
            json={},
            content_type="application/json",
        )
        assert resposta.status_code == 400, "Body sem 'itens' deve retornar HTTP 400"

    def test_mensagem_de_erro_presente(self, client):
        resposta = client.post(
            "/api/pedido",
            json={"itens": []},
            content_type="application/json",
        )
        dados = json.loads(resposta.data)
        assert "erro" in dados, "Resposta deve conter campo 'erro'"

    def test_pedido_valido_retorna_201(self, client):
        """Contra-prova: pedido com itens deve funcionar (HTTP 201)."""
        resposta = client.post(
            "/api/pedido",
            json={"itens": [{"id": 1, "qtd": 2}]},
            content_type="application/json",
        )
        assert resposta.status_code == 201, "Pedido válido deve retornar HTTP 201"
