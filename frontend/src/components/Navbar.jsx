import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import Logo from "../img/logo.png";
import Perfil from "../img/perfil.png";

const Navbar = () => {
  const [showDropdown, setShowDropdown] = useState(false);
  const [usuario, setUsuario] = useState(null);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  // Buscar informações do usuário ao carregar o componente
  useEffect(() => {
    const buscarUsuario = async () => {
      try {
        const token = localStorage.getItem('token');
        if (!token) {
          navigate('/login');
          return;
        }

        const response = await fetch('http://localhost:5000/api/autenticacao/usuario', {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
        });

        if (response.ok) {
          const userData = await response.json();
          setUsuario(userData);
        } else {
          // Token inválido, redirecionar para login
          localStorage.removeItem('token');
          navigate('/login');
        }
      } catch (error) {
        console.error('Erro ao buscar usuário:', error);
        localStorage.removeItem('token');
        navigate('/login');
      } finally {
        setLoading(false);
      }
    };

    buscarUsuario();
  }, [navigate]);

  const handleLogout = () => {
    localStorage.removeItem('token');
    setUsuario(null);
    navigate('/login');
  };

  const handleProfileClick = () => {
    setShowDropdown(!showDropdown);
  };

  // Se ainda está carregando, não mostra nada
  if (loading) {
    return <div className="navbar-loading">Carregando...</div>;
  }

  // Se não tem usuário, não mostra a navbar
  if (!usuario) {
    return null;
  }

  // Definir rotas baseadas no tipo de usuário
  const getRotasPermitidas = () => {
    const tipo = usuario.tipo;
    
    switch(tipo) {
      case 0: // Gerente
        return [
          { path: "/estoque", icon: "📦", label: "Estoque" },
          { path: "/funcionarios", icon: "👥", label: "Funcionários" },
          { path: "/lista_pedidos", icon: "📋", label: "Pedidos" },
          { path: "/vendas", icon: "💰", label: "Vendas" },
          { path: "/produtos", icon: "🏷️", label: "Produtos" }
        ];
      
      case 1: // Repositor
        return [
          { path: "/estoque", icon: "📦", label: "Estoque" },
          { path: "/lista_pedidos", icon: "📋", label: "Pedidos" }
        ];
      
      case 2: // Caixa
        return [
          { path: "/caixa", icon: "💰", label: "Caixa" },
          { path: "/vendas", icon: "📊", label: "Vendas" }
        ];
      
      default:
        return [];
    }
  };

  const rotasPermitidas = getRotasPermitidas();

  // Mapear tipo para texto
  const getTipoTexto = (tipo) => {
    const tipos = {
      0: 'Gerente',
      1: 'Repositor', 
      2: 'Caixa'
    };
    return tipos[tipo] || 'Usuário';
  };

  return (
    <div className='navbar'>
      <div className='navbar-container'>
        <div className='navbar-logo'>
          <img src={Logo} alt="Supermercado Logo" />
          <span className='logo-text'>Supermercado</span>
        </div>
        
        <div className='navbar-links'>
          {rotasPermitidas.map((rota, index) => (
            <Link key={index} className='nav-link' to={rota.path}>
              <div className='nav-icon'>{rota.icon}</div>
              <h6>{rota.label}</h6>
            </Link>
          ))}
        </div>

        <div className='navbar-profile'>
          <div className='profile-container' onClick={handleProfileClick}>
            <img src={Perfil} alt="Perfil do Usuário" className='profile-image' />
            <div className='profile-info'>
              <span className='profile-name'>{usuario.nome}</span>
              <span className='profile-role'>{getTipoTexto(usuario.tipo)}</span>
            </div>
            <div className='dropdown-arrow'>▼</div>
          </div>
          
          {showDropdown && (
            <div className='profile-dropdown'>
              <div className='dropdown-user-info'>
                <strong>{usuario.nome}</strong>
                <small>{usuario.email}</small>
                <small>Cargo: {getTipoTexto(usuario.tipo)}</small>
              </div>
              <div className='dropdown-divider'></div>
              <button onClick={handleLogout} className='dropdown-item logout-btn'>
                <div className='dropdown-icon'>🚪</div>
                Sair
              </button>
            </div>
          )}
        </div>
      </div>

      <style jsx>{`
        .navbar-loading {
          padding: 10px;
          text-align: center;
          background: #f8f9fa;
        }
        
        .navbar {
          background: #2c3e50;
          color: white;
          padding: 0 20px;
          box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        
        .navbar-container {
          display: flex;
          align-items: center;
          justify-content: space-between;
          max-width: 1200px;
          margin: 0 auto;
          height: 70px;
        }
        
        .navbar-logo {
          display: flex;
          align-items: center;
          gap: 10px;
        }
        
        .navbar-logo img {
          height: 40px;
        }
        
        .logo-text {
          font-size: 20px;
          font-weight: bold;
          color: #ecf0f1;
        }
        
        .navbar-links {
          display: flex;
          gap: 30px;
          align-items: center;
        }
        
        .nav-link {
          display: flex;
          flex-direction: column;
          align-items: center;
          text-decoration: none;
          color: #bdc3c7;
          transition: color 0.3s;
          padding: 8px 12px;
          border-radius: 6px;
        }
        
        .nav-link:hover {
          color: #ecf0f1;
          background: rgba(255,255,255,0.1);
        }
        
        .nav-icon {
          font-size: 20px;
          margin-bottom: 4px;
        }
        
        .nav-link h6 {
          margin: 0;
          font-size: 12px;
          font-weight: 500;
        }
        
        .navbar-profile {
          position: relative;
        }
        
        .profile-container {
          display: flex;
          align-items: center;
          gap: 10px;
          cursor: pointer;
          padding: 8px 12px;
          border-radius: 6px;
          transition: background 0.3s;
        }
        
        .profile-container:hover {
          background: rgba(255,255,255,0.1);
        }
        
        .profile-image {
          width: 40px;
          height: 40px;
          border-radius: 50%;
          object-fit: cover;
        }
        
        .profile-info {
          display: flex;
          flex-direction: column;
        }
        
        .profile-name {
          font-weight: 600;
          font-size: 14px;
        }
        
        .profile-role {
          font-size: 12px;
          color: #bdc3c7;
        }
        
        .dropdown-arrow {
          font-size: 10px;
          color: #bdc3c7;
        }
        
        .profile-dropdown {
          position: absolute;
          top: 100%;
          right: 0;
          background: white;
          border-radius: 8px;
          box-shadow: 0 4px 20px rgba(0,0,0,0.15);
          min-width: 200px;
          z-index: 1000;
          margin-top: 5px;
        }
        
        .dropdown-user-info {
          padding: 15px;
          border-bottom: 1px solid #eee;
        }
        
        .dropdown-user-info strong {
          display: block;
          color: #2c3e50;
          margin-bottom: 5px;
        }
        
        .dropdown-user-info small {
          display: block;
          color: #7f8c8d;
          font-size: 11px;
        }
        
        .dropdown-item {
          display: flex;
          align-items: center;
          gap: 10px;
          width: 100%;
          padding: 12px 15px;
          border: none;
          background: none;
          text-decoration: none;
          color: #2c3e50;
          cursor: pointer;
          transition: background 0.3s;
        }
        
        .dropdown-item:hover {
          background: #f8f9fa;
        }
        
        .logout-btn {
          color: #e74c3c;
        }
        
        .dropdown-divider {
          height: 1px;
          background: #ecf0f1;
          margin: 5px 0;
        }
      `}</style>
    </div>
  );
};

export default Navbar;