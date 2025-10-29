import React, { useState } from "react";

const FuncionarioDetalhe = () => {
  // Dados mockados de um único funcionário
  const funcionario = {
    nome: "João Silva",
    cpf: "123.456.789-00",
    pontoBateu: false,
    salario: 2500
  };

  const [pontoBateu] = useState(funcionario.pontoBateu);
  const [modalAberto, setModalAberto] = useState(false);
  const [novoSalario, setNovoSalario] = useState(funcionario.salario);
  const [salarioAtual, setSalarioAtual] = useState(funcionario.salario);
  const [mensagem, setMensagem] = useState("");



  const demitirFuncionario = () => {
    setMensagem(`⚠️ Funcionário ${funcionario.nome} demitido!`);
  };

  const abrirModal = () => setModalAberto(true);
  const fecharModal = () => setModalAberto(false);

  const atualizarSalario = () => {
    setSalarioAtual(novoSalario);
    setMensagem(`💰 Salário atualizado para R$ ${novoSalario}`);
    fecharModal();
  };

  return (
    <div className="funcionario-container" style={{ padding: "20px", maxWidth: "400px", margin: "0 auto", fontFamily: "Arial, sans-serif", border: "1px solid #ccc", borderRadius: "8px" }}>
      <h2>Detalhes do Funcionário</h2>

      <div style={{ marginBottom: "10px" }}><b>Nome:</b> {funcionario.nome}</div>
      <div style={{ marginBottom: "10px" }}><b>CPF:</b> {funcionario.cpf}</div>
      <div style={{ marginBottom: "10px" }}>
        <b>Status de Ponto:</b> {pontoBateu ? "✅ Bateu ponto" : "❌ Não bateu ponto"}
      </div>
      <div style={{ marginBottom: "20px" }}><b>Salário:</b> R$ {salarioAtual}</div>

      <div style={{ display: "flex", gap: "10px", marginBottom: "20px" }}>
        <button onClick={demitirFuncionario} style={{ padding: "10px", backgroundColor: "#f44336", color: "white", border: "none", borderRadius: "4px" }}>
          🛑 Demitir
        </button>
        <button onClick={abrirModal} style={{ padding: "10px", backgroundColor: "#2196F3", color: "white", border: "none", borderRadius: "4px" }}>
          💰 Aumentar Salário
        </button>
      </div>

      {mensagem && <div style={{ marginBottom: "20px", color: "#333" }}>{mensagem}</div>}

      {modalAberto && (
        <div style={{ position: "fixed", top: 0, left: 0, width: "100%", height: "100%", backgroundColor: "rgba(0,0,0,0.5)", display: "flex", alignItems: "center", justifyContent: "center" }}>
          <div style={{ backgroundColor: "white", padding: "20px", borderRadius: "8px", minWidth: "300px" }}>
            <h3>Aumentar Salário</h3>
            <input
              type="number"
              value={novoSalario}
              onChange={(e) => setNovoSalario(Number(e.target.value))}
              style={{ width: "100%", padding: "8px", marginBottom: "10px" }}
            />
            <div style={{ display: "flex", justifyContent: "flex-end", gap: "10px" }}>
              <button onClick={fecharModal} style={{ padding: "8px 12px" }}>Cancelar</button>
              <button onClick={atualizarSalario} style={{ padding: "8px 12px", backgroundColor: "#2196F3", color: "white", border: "none", borderRadius: "4px" }}>Salvar</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default FuncionarioDetalhe;
