# Qualidade de Software — Estratégia de Testes

### Funcionalidades principais

1. Exibição do Cardápio Digital
2. Realização de Pedido pelo Cliente
3. Gestão de Pedidos em Tempo Real (Painel da Cozinha)

---

### 1. Exibição do Cardápio Digital

**Regras de negócio:**
- O cliente acessa o cardápio escaneando o QR Code da mesa.
- Somente produtos ativos são exibidos, organizados por categoria.
- O número da mesa é identificado automaticamente pela URL (ex: `/mesa/3`).

**Caso de Teste 01 — Cardápio exibe apenas produtos ativos**  Positivo · Unitário
> GET `/api/cardapio` → retorna somente produtos com `ativo = true`, organizados por categoria.

**Caso de Teste 02 — Produto inativo não aparece no cardápio**  Negativo · Unitário
> GET `/api/cardapio` com produto `ativo = false` cadastrado → produto **não aparece** na resposta.

---

### 2. Realização de Pedido pelo Cliente

**Regras de negócio:**
- O carrinho precisa ter pelo menos 1 item para confirmar o pedido.
- O número da mesa é obrigatório e capturado automaticamente via QR Code.
- Após a confirmação, o pedido é salvo no banco e a cozinha é notificada.

**Caso de Teste 03 — Pedido enviado com sucesso** Positivo · E2E
> Cliente na mesa 5 adiciona itens e confirma → pedido salvo com status `pendente` e confirmação exibida na tela.

**Caso de Teste 04 — Pedido com carrinho vazio não é enviado**  Negativo · Unitário
> Cliente clica em "Confirmar Pedido" sem nenhum item → pedido bloqueado com mensagem de erro.

---

### 3. Gestão de Pedidos em Tempo Real (Painel da Cozinha)

**Regras de negócio:**
- Pedidos chegam em tempo real no painel, sem recarregar a página.
- O operador pode atualizar o status para `Em Preparo` ou `Pronto`.
- Pedidos são exibidos em ordem cronológica.

**Caso de Teste 05 — Pedido aparece em tempo real no painel**  Positivo · Integração
> Cliente confirma pedido na mesa 2 → pedido aparece no painel da cozinha em menos de 3 segundos.

**Caso de Teste 06 — Múltiplos pedidos simultâneos chegam na ordem correta**  Negativo/Estresse · Integração
> Mesas 1, 3 e 7 enviam pedidos quase ao mesmo tempo → todos aparecem no painel na ordem certa, sem perda ou duplicação.


