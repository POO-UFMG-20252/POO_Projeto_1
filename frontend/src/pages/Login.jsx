import React from 'react'
import { Link } from 'react-router-dom'

const Login = () => {
    return (
        <div className='auth'>
            <h1>Login</h1>
            <form >
                <input required type="text" placeholder='CPF' />    
                <input required type="password" placeholder='Senha' />
                <button>Login</button>
                <p>Isso é um erro</p>
                <span>Ainda não tem conta? <Link to="/register">Register</Link></span>
            </form>
        </div>
    )
}

export default Login