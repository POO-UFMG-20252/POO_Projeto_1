import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import Logo from "../img/logo.png";
import Perfil from "../img/perfil.png";

const Navbar = () => {
  const [showDropdown, setShowDropdown] = useState(false);
  const navigate = useNavigate();

  const handleLogout = () => {
    // Lógica de logout aqui
    console.log("Logout realizado");
    navigate("/login");
  };

  const handleProfileClick = () => {
    setShowDropdown(!showDropdown);
  };

  return (
    <div className='navbar'>
      <div className='navbar-container'>
        <div className='navbar-logo'>
          <img src={Logo} alt="Supermercado Logo" />
          <span className='logo-text'>Supermercado</span>
        </div>
        
        <div className='navbar-links'>
          <Link className='nav-link' to="/estoque">
            <div className='nav-icon'>📦</div>
            <h6>Estoque</h6>
          </Link>
          
          <Link className='nav-link' to="/funcionarios">
            <div className='nav-icon'>👥</div>
            <h6>Funcionários</h6>
          </Link>
          
          <Link className='nav-link' to="/produtos">
            <div className='nav-icon'>🏷️</div>
            <h6>Produtos</h6>
          </Link>
          
          <Link className='nav-link' to="/lista_pedidos">
            <div className='nav-icon'>📋</div>
            <h6>Pedidos</h6>
          </Link>

          <Link className='nav-link' to="/vendas">
            <div className='nav-icon'>💰</div>
            <h6>Vendas</h6>
          </Link>
        </div>

        <div className='navbar-profile'>
          <div className='profile-container' onClick={handleProfileClick}>
            <img src={Perfil} alt="Perfil do Usuário" className='profile-image' />
            <span className='profile-name'>Luigi</span>
            <div className='dropdown-arrow'>▼</div>
          </div>
          {/*
          {showDropdown && (
            <div className='profile-dropdown'>
              <Link to="/perfil" className='dropdown-item'>
                <div className='dropdown-icon'>👤</div>
                Meu Perfil
              </Link>
              <Link to="/configuracoes" className='dropdown-item'>
                <div className='dropdown-icon'>⚙️</div>
                Configurações
              </Link>
              <div className='dropdown-divider'></div>
              <button onClick={handleLogout} className='dropdown-item logout-btn'>
                <div className='dropdown-icon'>🚪</div>
                Sair
              </button>
            </div>
          )}
          */}
        </div>
      </div>
    </div>
  );
};

export default Navbar;