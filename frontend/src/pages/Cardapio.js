import { useEffect, useState } from "react";

function Cardapio() {
  const [dados, setDados] = useState(null);

  useEffect(() => {
    fetch("http://localhost:5001")
      .then((res) => res.json())
      .then((data) => setDados(data))
      .catch((err) => console.error(err));
  }, []);

  return (
    <div>
      <h1>Cardápio</h1>

      {dados ? (
        <p>{dados.mensagem}</p>
      ) : (
        <p>Carregando...</p>
      )}
    </div>
  );
}

export default Cardapio;