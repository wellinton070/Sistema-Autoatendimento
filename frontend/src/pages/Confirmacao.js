import { useParams, useNavigate } from "react-router-dom";

function Confirmacao() {
  const { numero } = useParams();
  const navigate = useNavigate();
  const nome = sessionStorage.getItem("clienteNome");
  const pedidoId = sessionStorage.getItem("pedidoId");

  return (
    <div style={styles.container}>
      <div style={styles.card}>
        <div style={styles.icone}>✅</div>
        <h1 style={styles.titulo}>Pedido enviado!</h1>
        <p style={styles.texto}>
          Obrigado, <strong>{nome}</strong>!<br />
          Seu pedido <strong>#{pedidoId}</strong> foi recebido pela cozinha.
        </p>
        <p style={styles.mesa}>Mesa {numero}</p>
        <div style={styles.status}>
          <span style={styles.dot} />
          Preparando seu pedido...
        </div>
        <button
          style={styles.botao}
          onClick={() => navigate(`/mesa/${numero}/cardapio`)}
        >
          Adicionar mais itens
        </button>
      </div>
    </div>
  );
}

const styles = {
  container: {
    minHeight: "100vh",
    backgroundColor: "#f0fdf4",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    padding: "16px",
  },
  card: {
    backgroundColor: "#fff",
    borderRadius: "16px",
    padding: "48px 32px",
    maxWidth: "400px",
    width: "100%",
    textAlign: "center",
    boxShadow: "0 4px 24px rgba(0,0,0,0.08)",
  },
  icone: { fontSize: "72px", marginBottom: "16px" },
  titulo: { fontSize: "28px", color: "#16a34a", margin: "0 0 16px" },
  texto: { fontSize: "16px", color: "#444", lineHeight: "1.6", marginBottom: "8px" },
  mesa: { fontSize: "14px", color: "#888", marginBottom: "24px" },
  status: {
    display: "inline-flex", alignItems: "center", gap: "8px",
    backgroundColor: "#fef9c3", color: "#854d0e",
    padding: "8px 16px", borderRadius: "20px", fontSize: "14px",
    marginBottom: "32px",
  },
  dot: {
    width: "8px", height: "8px", borderRadius: "50%",
    backgroundColor: "#eab308", display: "inline-block",
  },
  botao: {
    padding: "12px 24px",
    backgroundColor: "#f97316",
    color: "#fff",
    border: "none",
    borderRadius: "8px",
    fontSize: "15px",
    cursor: "pointer",
    fontWeight: "bold",
  },
};

export default Confirmacao;
