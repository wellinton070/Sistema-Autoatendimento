import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import Identificacao from "./pages/Identificacao";
import Cardapio from "./pages/Cardapio";
import Confirmacao from "./pages/Confirmacao";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/mesa/:numero" element={<Identificacao />} />
        <Route path="/mesa/:numero/cardapio" element={<Cardapio />} />
        <Route path="/mesa/:numero/confirmacao" element={<Confirmacao />} />
        <Route path="*" element={<Navigate to="/mesa/1" />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
