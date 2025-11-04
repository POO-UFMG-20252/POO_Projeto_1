import React, { useState } from "react";

const RegistroPonto = () => {
  const [mensagem, setMensagem] = useState("");
  const [hora, setHora] = useState("");
  const [carregando, setCarregando] = useState(false);

  const baterPonto = async (tipo) => {
    setCarregando(true);
    setMensagem("");
    
    try {
      const token = localStorage.getItem('token');
      
      if (!token) {
        setMensagem("❌ Você precisa estar logado para bater ponto");
        setCarregando(false);
        return;
      }

      console.log("Enviando requisição para bater ponto...");
      
      const response = await fetch('http://localhost:5000/api/funcionarios/ponto', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ tipo })
      });

      console.log("Resposta recebida:", response.status);

      const data = await response.json();

      if (response.ok) {
        const agora = new Date().toLocaleTimeString();
        setHora(agora);
        setMensagem(`✅ ${data.message}`);
      } else {
        setMensagem(`❌ Erro: ${data.message || 'Erro desconhecido'}`);
      }
    } catch (error) {
      console.error("Erro completo:", error);
      setMensagem("❌ Erro ao conectar com o servidor. Verifique se o backend está rodando.");
    } finally {
      setCarregando(false);
    }
  };

  const baterEntrada = () => baterPonto(0);
  const baterSaida = () => baterPonto(1);

  return (
    <div className="registro-container">
      <div className="registro-header">Registro de Ponto</div>

      <div className="registro-body">
        <div className="registro-botoes">
          <button 
            className="btn-registro btn-bater" 
            onClick={baterEntrada}
            disabled={carregando}
          >
            {carregando ? "⏳" : "🕒"} Bater Entrada
          </button>
          <button 
            className="btn-registro btn-finalizar" 
            onClick={baterSaida}
            disabled={carregando}
          >
            {carregando ? "⏳" : "🛑"} Bater Saída
          </button>
        </div>

        {mensagem && (
          <div className={`mensagem ${mensagem.includes('❌') ? 'erro' : 'sucesso'}`}>
            <strong>{mensagem}</strong>
            {mensagem.includes('✅') && (
              <div className="horario">Horário registrado: <b>{hora}</b></div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default RegistroPonto;