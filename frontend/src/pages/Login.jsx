import React, { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'

const Login = () => {
    const [cpf, setCpf] = useState('')
    const [senha, setSenha] = useState('')
    const [erro, setErro] = useState('')
    const navigate = useNavigate()

    const handleSubmit = async (e) => {
        e.preventDefault()
        setErro('')

        try {
            const response = await fetch('http://localhost:5000/api/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ cpf, senha }),
            })

            const data = await response.json()

            if (response.ok) {
                localStorage.setItem('usuario', JSON.stringify(data.usuario))
                localStorage.setItem('token', data.token || 'fake-token')
                navigate('/')
            } else {
                setErro(data.message || 'Erro ao fazer login')
            }
        } catch (error) {
            setErro('Erro de conexão com o servidor')
        }
    }

    return (
        <div className='auth'>
            <h1>Login</h1>
            <form onSubmit={handleSubmit}>
                <input 
                    required 
                    type="text" 
                    placeholder='CPF' 
                    value={cpf}
                    onChange={(e) => setCpf(e.target.value)}
                />    
                <input 
                    required 
                    type="password" 
                    placeholder='Senha' 
                    value={senha}
                    onChange={(e) => setSenha(e.target.value)}
                />
                <button type="submit">Login</button>
                {erro && <p className="error">{erro}</p>}
                <span>Ainda não tem conta? <Link to="/register">Register</Link></span>
            </form>
        </div>
    )
}

export default Login
