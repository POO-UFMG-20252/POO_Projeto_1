import React, { useState, useEffect } from "react";
import { useLocation, useNavigate, useParams } from "react-router-dom";

const FuncionarioDetalhe = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { cpf } = useParams();

  const [funcionario, setFuncionario] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [modalAberto, setModalAberto] = useState(false);
  const [modalDemissaoAberto, setModalDemissaoAberto] = useState(false);
  const [novoSalario, setNovoSalario] = useState(0);
  const [motivoDemissao, setMotivoDemissao] = useState("");
  const [mensagem, setMensagem] = useState("");

  useEffect(() => {
    const buscarFuncionario = async () => {
      try {
        setLoading(true);
        setError(null);

        const token = localStorage.getItem('token');
        if (!token) {
          navigate('/login');
          return;
        }

        if (location.state?.funcionario) {
          setFuncionario(location.state.funcionario);
          setNovoSalario(location.state.funcionario.salario || 0);
        } else if (cpf) {
          const response = await fetch(`http://localhost:5000/api/funcionarios/${cpf}`, {
            method: 'GET',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': `Bearer ${token}`
            }
          });

          if (!response.ok) {
            throw new Error(`Erro ${response.status}: ${response.statusText}`);
          }

          const dadosFuncionario = await response.json();
          setFuncionario(dadosFuncionario);
          setNovoSalario(dadosFuncionario.salario || 0);
        }
      } catch (error) {
        console.error('Erro ao carregar funcionário:', error);
        setError('Erro ao carregar dados do funcionário. Tente novamente.');
      } finally {
        setLoading(false);
      }
    };

    buscarFuncionario();
  }, [cpf, location.state, navigate]);

  const demitirFuncionario = async () => {
    if (!motivoDemissao.trim()) {
      setMensagem("❌ Por favor, informe o motivo da demissão.");
      return;
    }

    try {
      const token = localStorage.getItem('token');
      if (!token) {
        navigate('/login');
        return;
      }

      const response = await fetch('http://localhost:5000/api/funcionarios', {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          cpf: funcionario.cpf,
          motivo: motivoDemissao
        })
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.mensagem || `Erro ${response.status}: ${response.statusText}`);
      }

      const resultado = await response.json();
      
      setMensagem(`✅ Funcionário ${funcionario.nome} demitido com sucesso!`);
      setFuncionario(prev => ({ ...prev, ativo: false }));
      setModalDemissaoAberto(false);
      setMotivoDemissao("");

      // Redirecionar para lista após 2 segundos
      setTimeout(() => {
        navigate('/funcionarios');
      }, 2000);

    } catch (error) {
      console.error('Erro ao demitir funcionário:', error);
      setMensagem(`❌ Erro ao demitir funcionário: ${error.message}`);
    }
  };

  const abrirModalDemissao = () => {
    if (funcionario && !funcionario.ativo) {
      setMensagem("❌ Este funcionário já está demitido.");
      return;
    }
    setModalDemissaoAberto(true);
    setMensagem("");
  };

  const fecharModalDemissao = () => {
    setModalDemissaoAberto(false);
    setMotivoDemissao("");
  };

  

  const voltarParaLista = () => {
    navigate(-1);
  };

  if (loading) {
    return (
      <div className="funcionario-container" style={{ padding: "20px", maxWidth: "400px", margin: "0 auto", fontFamily: "Arial, sans-serif" }}>
        <div style={{ textAlign: 'center' }}>Carregando dados do funcionário...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="funcionario-container" style={{ padding: "20px", maxWidth: "400px", margin: "0 auto", fontFamily: "Arial, sans-serif" }}>
        <div style={{ color: '#dc3545', textAlign: 'center' }}>{error}</div>
        <button 
          onClick={voltarParaLista}
          style={{ marginTop: "20px", padding: "8px 12px", backgroundColor: "#6c757d", color: "white", border: "none", borderRadius: "4px" }}
        >
          ← Voltar
        </button>
      </div>
    );
  }

  if (!funcionario) {
    return (
      <div className="funcionario-container" style={{ padding: "20px", maxWidth: "400px", margin: "0 auto", fontFamily: "Arial, sans-serif" }}>
        <div style={{ textAlign: 'center' }}>Funcionário não encontrado</div>
        <button 
          onClick={voltarParaLista}
          style={{ marginTop: "20px", padding: "8px 12px", backgroundColor: "#6c757d", color: "white", border: "none", borderRadius: "4px" }}
        >
          ← Voltar
        </button>
      </div>
    );
  }
  
  return (
    <div className="funcionario-container" style={{ padding: "20px", maxWidth: "500px", margin: "0 auto", fontFamily: "Arial, sans-serif", border: "1px solid #ccc", borderRadius: "8px" }}>
      
      <button 
        onClick={voltarParaLista}
        style={{ marginBottom: "20px", padding: "8px 12px", backgroundColor: "#6c757d", color: "white", border: "none", borderRadius: "4px" }}
      >
        ← Voltar
      </button>

      <h2>Detalhes do Funcionário</h2>

      <div style={{ marginBottom: "10px" }}><b>Nome:</b> {funcionario.nome}</div>
      <div style={{ marginBottom: "10px" }}><b>CPF:</b> {funcionario.cpf}</div>
      <div style={{ marginBottom: "10px" }}><b>Email:</b> {funcionario.email}</div>
      <div style={{ marginBottom: "10px" }}><b>Data de Nascimento:</b> {funcionario.data_nascimento}</div>
      <div style={{ marginBottom: "10px" }}><b>Data de Admissão:</b> {funcionario.data_admissao}</div>
      <div style={{ marginBottom: "10px" }}><b>Tipo:</b> {funcionario.tipo === 0 ? 'Gerente' : funcionario.tipo === 1 ? 'Repositor' : 'Caixa'}</div>
      <div style={{ marginBottom: "10px" }}>
        <b>Status:</b> {funcionario.ativo ? "✅ Ativo" : "❌ Demitido"}
      </div>
      <div style={{ marginBottom: "20px" }}><b>Salário:</b> R$ {funcionario.salario}</div>

      <div style={{ display: "flex", gap: "10px", marginBottom: "20px", flexWrap: "wrap" }}>
        <button 
          onClick={abrirModalDemissao} 
          style={{ padding: "10px", backgroundColor: "#f44336", color: "white", border: "none", borderRadius: "4px" }}
          disabled={!funcionario.ativo}
        >
          🛑 Demitir
        </button>
      </div>

      {mensagem && (
        <div style={{ 
          marginBottom: "20px", 
          padding: "10px", 
          borderRadius: "4px", 
          backgroundColor: mensagem.includes("❌") ? "#f8d7da" : "#d4edda",
          color: mensagem.includes("❌") ? "#721c24" : "#155724",
          border: `1px solid ${mensagem.includes("❌") ? "#f5c6cb" : "#c3e6cb"}`
        }}>
          {mensagem}
        </div>
      )}

      {/* Modal de Demissão */}
      {modalDemissaoAberto && (
        <div style={{ position: "fixed", top: 0, left: 0, width: "100%", height: "100%", backgroundColor: "rgba(0,0,0,0.5)", display: "flex", alignItems: "center", justifyContent: "center", zIndex: 1000 }}>
          <div style={{ backgroundColor: "white", padding: "20px", borderRadius: "8px", minWidth: "400px", maxWidth: "500px" }}>
            <h3>Confirmar Demissão</h3>
            <p style={{ marginBottom: "15px" }}>
              Tem certeza que deseja demitir <strong>{funcionario.nome}</strong>?
            </p>
            
            <div style={{ marginBottom: "15px" }}>
              <label style={{ display: "block", marginBottom: "5px", fontWeight: "bold" }}>
                Motivo da Demissão:
              </label>
              <textarea
                value={motivoDemissao}
                onChange={(e) => setMotivoDemissao(e.target.value)}
                placeholder="Digite o motivo da demissão..."
                style={{ width: "100%", padding: "8px", minHeight: "80px", border: "1px solid #ccc", borderRadius: "4px" }}
              />
            </div>

            <div style={{ display: "flex", justifyContent: "flex-end", gap: "10px" }}>
              <button 
                onClick={fecharModalDemissao} 
                style={{ padding: "8px 16px", backgroundColor: "#6c757d", color: "white", border: "none", borderRadius: "4px" }}
              >
                Cancelar
              </button>
              <button 
                onClick={demitirFuncionario} 
                style={{ padding: "8px 16px", backgroundColor: "#f44336", color: "white", border: "none", borderRadius: "4px" }}
                disabled={!motivoDemissao.trim()}
              >
                Confirmar Demissão
              </button>
            </div>
          </div>
        </div>
      )}


    </div>
  );
};

export default FuncionarioDetalhe;