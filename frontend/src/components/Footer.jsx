import React from 'react'

const Footer = () => {
    return (
    <footer className="bg-secondary text-white text-center py-3 mt-auto">
      <p className="mb-1">
        Sistema de Gestão de Supermercado - v1.0
      </p>
      <small>
        Desenvolvido com React + Python | Projeto Acadêmico - {new Date().getFullYear()}
      </small>
    </footer>
  );
}

export default Footer