import React, { useState, useEffect } from 'react';
import { useParams, useLocation, useNavigate } from 'react-router-dom';

const PedidoDetalhe = () => {
    const { id } = useParams();
    const location = useLocation();
    const navigate = useNavigate();
    const [pedido, setPedido] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [mensagem, setMensagem] = useState('');

    useEffect(() => {
        // Se veio por state, usa os dados, senão busca da API
        if (location.state?.pedido) {
            setPedido(location.state.pedido);
            setLoading(false);
        } else {
            buscarPedidoDaAPI();
        }
    }, [id, location.state]);

    const buscarPedidoDaAPI = async () => {
        try {
            const token = localStorage.getItem('token');
            const response = await fetch(`http://localhost:5000/api/pedidos/${id}`, {
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                }
            });
            
            if (!response.ok) {
                throw new Error(`Erro ${response.status}: ${response.statusText}`);
            }
            
            const dados = await response.json();
            setPedido(dados);
        } catch (error) {
            console.error('Erro ao buscar pedido:', error);
            setError('Erro ao carregar pedido. Tente novamente.');
        } finally {
            setLoading(false);
        }
    };

    const alterarEstadoPedido = async (novoEstado) => {
        try {
            const token = localStorage.getItem('token');
            const response = await fetch(`http://localhost:5000/api/pedido/${id}/estado`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({
                    novo_estado: novoEstado
                })
            });

            if (!response.ok) {
                const erroData = await response.json();
                throw new Error(erroData.mensagem || `Erro ${response.status}`);
            }

            const resultado = await response.json();
            setPedido(resultado.pedido);
            setMensagem(`✅ ${resultado.message}`);
            
            // Limpar mensagem após 3 segundos
            setTimeout(() => setMensagem(''), 3000);
            
        } catch (error) {
            console.error('Erro ao alterar estado:', error);
            setMensagem(`❌ Erro: ${error.message}`);
        }
    };

    const getProximoEstado = (estadoAtual) => {
        // Sequência: 0 → 1 → 2 → 3
        if (estadoAtual < 3) {
            return estadoAtual + 1;
        }
        return estadoAtual; // Se já estiver no último estado, mantém
    };

    const getTextoEstado = (estado) => {
        switch (estado) {
            case 0: return 'Aguardando';
            case 1: return 'A Caminho';
            case 2: return 'Entregue';
            case 3: return 'Finalizado';
            default: return 'Desconhecido';
        }
    };

    const getCorEstado = (estado) => {
        switch (estado) {
            case 0: return '#ffc107'; // Amarelo
            case 1: return '#17a2b8'; // Azul
            case 2: return '#28a745'; // Verde
            case 3: return '#6c757d'; // Cinza
            default: return '#dc3545'; // Vermelho
        }
    };

    const voltarParaLista = () => {
        navigate('/pedidos');
    };

    if (loading) {
        return (
            <div className="container mt-4">
                <div className="text-center py-5">
                    <div className="spinner-border text-primary" role="status">
                        <span className="visually-hidden">Carregando...</span>
                    </div>
                    <p className="mt-2">Carregando pedido...</p>
                </div>
            </div>
        );
    }

    if (error || !pedido) {
        return (
            <div className="container mt-4">
                <div className="alert alert-danger text-center" role="alert">
                    {error || 'Pedido não encontrado'}
                </div>
                <button className="btn btn-secondary" onClick={voltarParaLista}>
                    ← Voltar para Lista
                </button>
            </div>
        );
    }

    const proximoEstado = getProximoEstado(pedido.estado);
    const podeAvancarEstado = pedido.estado < 3;

    return (
        <div className="container mt-4">
            <div className="card">
                <div className="card-header d-flex justify-content-between align-items-center">
                    <h2 className="mb-0">Detalhes do Pedido #{pedido.id.toString().padStart(3, '0')}</h2>
                    <button className="btn btn-secondary" onClick={voltarParaLista}>
                        ← Voltar para Lista
                    </button>
                </div>
                
                <div className="card-body">
                    {/* Mensagem de status */}
                    {mensagem && (
                        <div className={`alert ${mensagem.includes('✅') ? 'alert-success' : 'alert-danger'} mb-4`}>
                            {mensagem}
                        </div>
                    )}

                    {/* Informações do Pedido */}
                    <div className="row mb-4">
                        <div className="col-md-6">
                            <h5>Informações do Pedido</h5>
                            <div className="mb-2">
                                <strong>ID:</strong> #{pedido.id.toString().padStart(3, '0')}
                            </div>
                            <div className="mb-2">
                                <strong>Responsável:</strong> {pedido.id_responsavel}
                            </div>
                        </div>
                        <div className="col-md-6">
                            <h5>Status do Pedido</h5>
                            <div className="mb-3">
                                <span 
                                    className="badge"
                                    style={{
                                        backgroundColor: getCorEstado(pedido.estado),
                                        color: 'white',
                                        padding: '8px 16px',
                                        fontSize: '1rem',
                                        fontWeight: 'bold',
                                        display: 'inline-block',
                                        marginBottom: '12px'
                                    }}
                                >
                                    {getTextoEstado(pedido.estado)}
                                </span>
                            </div>
                            
                            {/* Botão para alterar estado */}
                            {podeAvancarEstado && (
                                <button
                                    className="btn btn-primary mt-2"
                                    onClick={() => alterarEstadoPedido(proximoEstado)}
                                >
                                    Avançar para: {getTextoEstado(proximoEstado)} →
                                </button>
                            )}
                            
                            {!podeAvancarEstado && (
                                <p className="text-muted mt-2">
                                    <em>Pedido finalizado - não é possível alterar o estado</em>
                                </p>
                            )}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default PedidoDetalhe;