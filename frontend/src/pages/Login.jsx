import React, { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'

const Login = () => {
    const [formData, setFormData] = useState({
        cpf: '',
        senha: ''
    })
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState('')
    const navigate = useNavigate()

    const handleChange = (e) => {
        const { name, value } = e.target
        setFormData(prevState => ({
            ...prevState,
            [name]: value
        }))
        // Limpa o erro quando o usuário começa a digitar
        if (error) setError('')
    }

    const formatarCPF = (value) => {
        // Remove tudo que não é dígito
        const cpf = value.replace(/\D/g, '')
        
        // Aplica a formatação do CPF
        if (cpf.length <= 3) return cpf
        if (cpf.length <= 6) return `${cpf.slice(0, 3)}.${cpf.slice(3)}`
        if (cpf.length <= 9) return `${cpf.slice(0, 3)}.${cpf.slice(3, 6)}.${cpf.slice(6)}`
        return `${cpf.slice(0, 3)}.${cpf.slice(3, 6)}.${cpf.slice(6, 9)}-${cpf.slice(9, 11)}`
    }

    const handleCPFChange = (e) => {
        const formattedCPF = formatarCPF(e.target.value)
        setFormData(prevState => ({
            ...prevState,
            cpf: formattedCPF
        }))
        if (error) setError('')
    }

    const validarFormulario = () => {
        if (!formData.cpf.trim()) {
            setError('CPF é obrigatório')
            return false
        }
        
        if (!formData.senha.trim()) {
            setError('Senha é obrigatória')
            return false
        }

        // Validação básica de CPF (11 dígitos)
        const cpfLimpo = formData.cpf.replace(/\D/g, '')
        if (cpfLimpo.length !== 11) {
            setError('CPF deve ter 11 dígitos')
            return false
        }

        return true
    }

    const handleSubmit = async (e) => {
        e.preventDefault()
        
        if (!validarFormulario()) return

        setLoading(true)
        setError('')

        try {
            // Preparar dados para a API
            const dadosLogin = {
                cpf: formData.cpf.replace(/\D/g, ''), // Remove formatação do CPF
                senha: formData.senha
            }

            console.log('Enviando dados de login:', dadosLogin)

            // Fazer requisição para a API
            const response = await fetch('http://localhost:5000/api/autenticacao/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(dadosLogin)
            })

            const data = await response.json()

            if (!response.ok) {
                throw new Error(data.message || 'Erro ao fazer login')
            }

            console.log('Login bem-sucedido:', data)
            
            // Salvar o token no localStorage
            localStorage.setItem('token', data.token)
            
            // Redirecionar para a página principal
            navigate('/')
            
        } catch (error) {
            console.error('Erro no login:', error)
            setError(error.message)
        } finally {
            setLoading(false)
        }
    }

    return (
        <div className='auth'>
            <h1>Login</h1>
            <form onSubmit={handleSubmit}>
                <input 
                    required 
                    type="text" 
                    name="cpf"
                    placeholder='CPF' 
                    value={formData.cpf}
                    onChange={handleCPFChange}
                    maxLength="14"
                    disabled={loading}
                />    
                <input 
                    required 
                    type="password" 
                    name="senha"
                    placeholder='Senha' 
                    value={formData.senha}
                    onChange={handleChange}
                    disabled={loading}
                />
                <button type="submit" disabled={loading}>
                    {loading ? 'Entrando...' : 'Login'}
                </button>
                {error && <p className="error-message">{error}</p>}
            </form>

            <style jsx>{`
                .auth {
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    justify-content: center;
                    height: 100vh;
                    background-color: #f5f5f5;
                }
                
                h1 {
                    margin-bottom: 20px;
                    color: #333;
                }
                
                form {
                    display: flex;
                    flex-direction: column;
                    gap: 15px;
                    width: 300px;
                    padding: 30px;
                    background: white;
                    border-radius: 8px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                }
                
                input {
                    padding: 12px;
                    border: 1px solid #ddd;
                    border-radius: 4px;
                    font-size: 16px;
                }
                
                input:focus {
                    outline: none;
                    border-color: #007bff;
                }
                
                button {
                    padding: 12px;
                    background-color: #007bff;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    font-size: 16px;
                    cursor: pointer;
                    transition: background-color 0.3s;
                }
                
                button:hover:not(:disabled) {
                    background-color: #0056b3;
                }
                
                button:disabled {
                    background-color: #6c757d;
                    cursor: not-allowed;
                }
                
                .error-message {
                    color: #dc3545;
                    text-align: center;
                    margin: 0;
                    font-size: 14px;
                }
                
                span {
                    text-align: center;
                    color: #666;
                }
                
                a {
                    color: #007bff;
                    text-decoration: none;
                }
                
                a:hover {
                    text-decoration: underline;
                }
            `}</style>
        </div>
    )
}

export default Login