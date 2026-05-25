import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";

const API = "http://localhost:5001";

function Cardapio() {
  const { numero } = useParams();
  const navigate = useNavigate();

  const nome = sessionStorage.getItem("clienteNome");

  const [produtos, setProdutos] = useState([]);
  const [carrinho, setCarrinho] = useState({});
  const [carregando, setCarregando] = useState(true);
  const [enviando, setEnviando] = useState(false);
  const [erro, setErro] = useState("");

  // Redireciona se não tiver nome
  useEffect(() => {
    if (!nome) navigate(`/mesa/${numero}`);
  }, [nome, numero, navigate]);

  // Busca cardápio
  useEffect(() => {
    fetch(`${API}/api/cardapio`)
      .then((r) => r.json())
      .then((data) => { setProdutos(data); setCarregando(false); })
      .catch(() => { setErro("Erro ao carregar cardápio."); setCarregando(false); });
  }, []);

  function adicionar(produto) {
    setCarrinho((prev) => ({
      ...prev,
      [produto.id]: {
        ...produto,
        quantidade: (prev[produto.id]?.quantidade || 0) + 1,
      },
    }));
  }

  function remover(id) {
    setCarrinho((prev) => {
      const atual = { ...prev };
      if (atual[id]?.quantidade > 1) {
        atual[id] = { ...atual[id], quantidade: atual[id].quantidade - 1 };
      } else {
        delete atual[id];
      }
      return atual;
    });
  }

  const itensCarrinho = Object.values(carrinho);
  const total = itensCarrinho.reduce((s, i) => s + i.preco * i.quantidade, 0);

  async function enviarPedido() {
    if (itensCarrinho.length === 0) return;
    setEnviando(true);
    try {
      const res = await fetch(`${API}/api/pedido`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          mesa: Number(numero),
          cliente: nome,
          itens: itensCarrinho.map((i) => ({
            id: i.id,
            nome: i.nome,
            preco: i.preco,
            quantidade: i.quantidade,
          })),
        }),
      });
      if (!res.ok) throw new Error();
      const data = await res.json();
      sessionStorage.setItem("pedidoId", data.pedido_id);
      navigate(`/mesa/${numero}/confirmacao`);
    } catch {
      setErro("Erro ao enviar pedido. Tente novamente.");
      setEnviando(false);
    }
  }

  // Agrupa produtos por categoria
  const categorias = [...new Set(produtos.map((p) => p.categoria))];

  if (carregando) return <div style={styles.loading}>Carregando cardápio...</div>;

  return (
    <div style={styles.container}>
      {/* Cabeçalho */}
      <div style={styles.header}>
        <div>
          <h1 style={styles.titulo}>🍽️ Cardápio</h1>
          <p style={styles.subtitulo}>Mesa {numero} · {nome}</p>
        </div>
        {itensCarrinho.length > 0 && (
          <div style={styles.carrinhoResumo}>
            🛒 {itensCarrinho.reduce((s, i) => s + i.quantidade, 0)} itens
          </div>
        )}
      </div>

      {erro && <p style={styles.erro}>{erro}</p>}

      {/* Lista por categoria */}
      {categorias.map((cat) => (
        <div key={cat} style={styles.secao}>
          <h2 style={styles.categoria}>{cat}</h2>
          {produtos
            .filter((p) => p.categoria === cat)
            .map((p) => {
              const qtd = carrinho[p.id]?.quantidade || 0;
              return (
                <div key={p.id} style={styles.produto}>
                  <div style={styles.produtoInfo}>
                    <span style={styles.produtoNome}>{p.nome}</span>
                    <span style={styles.produtoDesc}>{p.descricao}</span>
                    <span style={styles.produtoPreco}>R$ {p.preco.toFixed(2)}</span>
                  </div>
                  <div style={styles.controles}>
                    {qtd > 0 ? (
                      <>
                        <button style={styles.btnMenos} onClick={() => remover(p.id)}>−</button>
                        <span style={styles.qtd}>{qtd}</span>
                      </>
                    ) : null}
                    <button style={styles.btnMais} onClick={() => adicionar(p)}>+</button>
                  </div>
                </div>
              );
            })}
        </div>
      ))}

      {/* Rodapé com total e botão */}
      {itensCarrinho.length > 0 && (
        <div style={styles.rodape}>
          <div style={styles.totalLinha}>
            <span>Total</span>
            <strong>R$ {total.toFixed(2)}</strong>
          </div>
          <button
            style={{ ...styles.btnEnviar, opacity: enviando ? 0.7 : 1 }}
            onClick={enviarPedido}
            disabled={enviando}
          >
            {enviando ? "Enviando..." : "Fazer Pedido ✓"}
          </button>
        </div>
      )}
    </div>
  );
}

const styles = {
  container: { maxWidth: "480px", margin: "0 auto", padding: "0 0 120px", backgroundColor: "#fafafa", minHeight: "100vh" },
  loading: { textAlign: "center", padding: "80px 20px", color: "#666" },
  header: {
    backgroundColor: "#f97316", color: "#fff", padding: "20px 16px",
    display: "flex", justifyContent: "space-between", alignItems: "center",
    position: "sticky", top: 0, zIndex: 10,
  },
  titulo: { margin: 0, fontSize: "22px" },
  subtitulo: { margin: "4px 0 0", fontSize: "14px", opacity: 0.9 },
  carrinhoResumo: {
    backgroundColor: "rgba(255,255,255,0.2)", borderRadius: "20px",
    padding: "6px 14px", fontSize: "14px", fontWeight: "bold",
  },
  secao: { padding: "0 16px" },
  categoria: { fontSize: "16px", color: "#f97316", borderBottom: "2px solid #f97316", paddingBottom: "4px", marginTop: "24px" },
  produto: {
    display: "flex", justifyContent: "space-between", alignItems: "center",
    padding: "14px 0", borderBottom: "1px solid #e5e7eb",
  },
  produtoInfo: { display: "flex", flexDirection: "column", gap: "2px", flex: 1 },
  produtoNome: { fontWeight: "600", fontSize: "15px", color: "#1a1a1a" },
  produtoDesc: { fontSize: "12px", color: "#888" },
  produtoPreco: { fontSize: "14px", fontWeight: "bold", color: "#f97316" },
  controles: { display: "flex", alignItems: "center", gap: "8px", marginLeft: "12px" },
  btnMais: {
    width: "32px", height: "32px", borderRadius: "50%",
    backgroundColor: "#f97316", color: "#fff", border: "none",
    fontSize: "20px", cursor: "pointer", display: "flex", alignItems: "center", justifyContent: "center",
  },
  btnMenos: {
    width: "32px", height: "32px", borderRadius: "50%",
    backgroundColor: "#e5e7eb", color: "#333", border: "none",
    fontSize: "20px", cursor: "pointer",
  },
  qtd: { fontSize: "16px", fontWeight: "bold", minWidth: "20px", textAlign: "center" },
  rodape: {
    position: "fixed", bottom: 0, left: "50%", transform: "translateX(-50%)",
    width: "100%", maxWidth: "480px", backgroundColor: "#fff",
    padding: "16px", boxShadow: "0 -4px 12px rgba(0,0,0,0.1)",
  },
  totalLinha: { display: "flex", justifyContent: "space-between", fontSize: "16px", marginBottom: "12px" },
  btnEnviar: {
    width: "100%", padding: "14px", backgroundColor: "#16a34a",
    color: "#fff", border: "none", borderRadius: "8px",
    fontSize: "16px", fontWeight: "bold", cursor: "pointer",
  },
  erro: { color: "#ef4444", textAlign: "center", padding: "8px 16px" },
};

export default Cardapio;
