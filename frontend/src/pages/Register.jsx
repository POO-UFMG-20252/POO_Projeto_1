import React from 'react'
import { Link } from 'react-router-dom'

const Register = () => {
    return (
        <div className='auth'>
            <h1>Register</h1>
            <form >
                <input required type="text" placeholder='CPF' />
                <input required type="email" placeholder='email' />   
                <input required type="password" placeholder='Senha' />
                <button>Register</button>
                <p>Isso é um erro</p>
                <span>Voce tem conta? <Link to="/login">Login</Link></span>
            </form>
        </div>
    )
}

export default Register