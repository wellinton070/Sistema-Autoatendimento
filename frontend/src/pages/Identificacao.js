import { useState } from "react";
import { useParams, useNavigate } from "react-router-dom";

function Identificacao() {
  const { numero } = useParams();
  const navigate = useNavigate();
  const [nome, setNome] = useState("");
  const [erro, setErro] = useState("");

  function handleEntrar(e) {
    e.preventDefault();
    if (!nome.trim()) {
      setErro("Por favor, informe seu nome.");
      return;
    }
    // Salva nome na sessionStorage para usar nas próximas telas
    sessionStorage.setItem("clienteNome", nome.trim());
    sessionStorage.setItem("clienteMesa", numero);
    navigate(`/mesa/${numero}/cardapio`);
  }

  return (
    <div style={styles.container}>
      <div style={styles.card}>
        <div style={styles.emoji}>🍽️</div>
        <h1 style={styles.titulo}>Bem-vindo!</h1>
        <p style={styles.subtitulo}>Mesa <strong>{numero}</strong></p>

        <form onSubmit={handleEntrar} style={styles.form}>
          <label style={styles.label}>Qual é o seu nome?</label>
          <input
            style={styles.input}
            type="text"
            placeholder="Ex: João Silva"
            value={nome}
            onChange={(e) => { setNome(e.target.value); setErro(""); }}
            autoFocus
          />
          {erro && <p style={styles.erro}>{erro}</p>}
          <button style={styles.botao} type="submit">
            Ver Cardápio →
          </button>
        </form>
      </div>
    </div>
  );
}

const styles = {
  container: {
    minHeight: "100vh",
    backgroundColor: "#f97316",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    padding: "16px",
  },
  card: {
    backgroundColor: "#fff",
    borderRadius: "16px",
    padding: "40px 32px",
    width: "100%",
    maxWidth: "400px",
    textAlign: "center",
    boxShadow: "0 4px 24px rgba(0,0,0,0.12)",
  },
  emoji: { fontSize: "64px", marginBottom: "8px" },
  titulo: { fontSize: "28px", margin: "0 0 4px", color: "#1a1a1a" },
  subtitulo: { color: "#666", marginBottom: "32px", fontSize: "16px" },
  form: { display: "flex", flexDirection: "column", gap: "12px" },
  label: { textAlign: "left", fontSize: "14px", color: "#444", fontWeight: "600" },
  input: {
    padding: "12px 16px",
    borderRadius: "8px",
    border: "2px solid #e5e7eb",
    fontSize: "16px",
    outline: "none",
  },
  botao: {
    padding: "14px",
    backgroundColor: "#f97316",
    color: "#fff",
    border: "none",
    borderRadius: "8px",
    fontSize: "16px",
    fontWeight: "bold",
    cursor: "pointer",
    marginTop: "8px",
  },
  erro: { color: "#ef4444", fontSize: "14px", margin: "0" },
};

export default Identificacao;
