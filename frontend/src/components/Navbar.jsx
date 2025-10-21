import React from 'react'
import {Link} from 'react-router-dom'
import Logo from "../img/logo.png"

const Navbar = () => {
    return (
        <div className='navbar'>
            <div className='container'>
                <div className='logo'>
                    <img src={Logo} alt="" />
                </div>
                <div className='links'>
                    <Link className='link' to="/?cat=estoque">
                    <h6>Estoque</h6>
                    </Link>
                    <Link className='link' to="/?cat=funcionarios">
                    <h6>Funcionarios</h6>
                    </Link>
                    <Link className='link' to="/?cat=produtos">
                    <h6>Produtos</h6>
                    </Link>
                    <Link className='link' to="/?cat=pedidos">
                    <h6>Pedidos</h6>
                    </Link>
                    <span>Luigi</span>
                    <span>Logout</span>
                </div>
            </div>
        </div>
    )
}

export default Navbar