import React, { useState } from "react";


const RegistroPonto = () => {
  const [mensagem, setMensagem] = useState("");
  const [hora, setHora] = useState("");

  const baterPonto = () => {
    const agora = new Date().toLocaleTimeString();
    setHora(agora);
    setMensagem("✅ Ponto batido com sucesso!");
  };

  const finalizarTurno = () => {
    const agora = new Date().toLocaleTimeString();
    setHora(agora);
    setMensagem("✅ Turno finalizado com sucesso!");
  };

  return (
    <div className="registro-container">
      <div className="registro-header">Registro de Ponto</div>

      <div className="registro-body">
        <div className="registro-botoes">
          <button className="btn-registro btn-bater" onClick={baterPonto}>
            🕒 Bater Ponto
          </button>
          <button className="btn-registro btn-finalizar" onClick={finalizarTurno}>
            🛑 Finalizar Turno
          </button>
        </div>

        {mensagem && (
          <div className="mensagem">
            <strong>{mensagem}</strong>
            <div className="horario">Horário: <b>{hora}</b></div>
          </div>
        )}
      </div>
    </div>
  );
};

export default RegistroPonto;
