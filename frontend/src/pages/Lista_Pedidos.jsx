import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

const PedidosLista = () => {
    const [pedidos, setPedidos] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const navigate = useNavigate();

    // Carregar pedidos da API
    useEffect(() => {
        const carregarPedidos = async () => {
            try {
                const token = localStorage.getItem('token');
                if (!token) {
                    navigate('/login');
                    return;
                }

                const response = await fetch('http://localhost:5000/api/pedidos', {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    }
                });

                if (!response.ok) {
                    throw new Error(`Erro ${response.status}: ${response.statusText}`);
                }

                const dadosPedidos = await response.json();
                setPedidos(dadosPedidos);
                setLoading(false);
            } catch (error) {
                console.error('Erro ao carregar pedidos:', error);
                setError('Erro ao carregar pedidos. Tente novamente.');
                setLoading(false);
            }
        };

        carregarPedidos();
    }, [navigate]);

    const goBack = () => {
        navigate(-1);
    };

    const criarNovoPedido = () => {
        navigate('/pedido');
    };

    // Função para redirecionar para os detalhes do pedido
    const verDetalhesPedido = (pedido) => {
        navigate(`/pedido/${pedido.id}`, { 
            state: { pedido } // Passa os dados do pedido como state
        });
    };

    // Função para retornar a classe CSS baseada no status
    const getStatusClass = (estado) => {
        switch (estado) {
            case 0: // Aguardando
                return 'status-aguardando';
            case 1: // A caminho
                return 'status-caminho';
            case 2: // Entregue
                return 'status-entregue';
            case 3: // Finalizado
                return 'status-finalizado';
            default:
                return 'status-desconhecido';
        }
    };

    if (loading) {
        return (
            <div className="pedidos-lista-container">
                <div className="text-center py-5">
                    <div className="spinner-border text-primary" role="status">
                        <span className="visually-hidden">Carregando...</span>
                    </div>
                    <p className="mt-2">Carregando pedidos...</p>
                </div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="pedidos-lista-container">
                <div className="alert alert-danger text-center" role="alert">
                    {error}
                </div>
            </div>
        );
    }

    return (
        <div className="pedidos-lista-container">
            <div className="boxH1ResPadraoDesktop">
                <div className="mesPremiadoPadraoDesktop">
                    <h1 className="h1ResPadraoDesktop">Lista de Pedidos</h1>
                </div>
                <div style={{ display: 'flex', gap: '10px', alignItems: 'center' }}>
                    <button 
                        className="btn btn-primary"
                        onClick={criarNovoPedido}
                        style={{ 
                            padding: '8px 16px', 
                            backgroundColor: '#28a745', 
                            border: 'none', 
                            borderRadius: '4px',
                            color: 'white',
                            cursor: 'pointer'
                        }}
                    >
                        ➕ Novo Pedido
                    </button>
                    <button 
                        className="svgXSairTabelas" 
                        data-placement="bottom" 
                        onClick={goBack}
                        aria-label="Voltar"
                        style={{
                            background: 'none',
                            border: 'none',
                            cursor: 'pointer',
                            padding: '5px'
                        }}
                    >
                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none">
                            <path
                                d="M13.541 12.0007L17.3955 8.14623C17.5857 7.93898 17.6884 7.66631 17.6823 7.38512C17.6762 7.10394 17.5618 6.83597 17.3628 6.63716C17.1639 6.43835 16.8958 6.32406 16.6147 6.31815C16.3335 6.31223 16.0609 6.41515 15.8537 6.60542L15.8547 6.60442L12.0002 10.4589L8.1457 6.60442C7.93845 6.41429 7.66578 6.31154 7.38459 6.31764C7.10341 6.32374 6.83544 6.4382 6.63663 6.63714C6.43782 6.83608 6.32353 7.10412 6.31762 7.38531C6.3117 7.6665 6.41462 7.93911 6.60489 8.14623L6.60389 8.14523L10.4584 11.9997L6.60389 15.8543C6.49544 15.9538 6.40825 16.0742 6.34756 16.2083C6.28687 16.3423 6.25393 16.4873 6.25074 16.6344C6.24755 16.7816 6.27417 16.9278 6.32899 17.0644C6.38382 17.201 6.46571 17.3251 6.56975 17.4292C6.67378 17.5333 6.7978 17.6153 6.93435 17.6702C7.0709 17.7251 7.21715 17.7518 7.36429 17.7487C7.51143 17.7456 7.65643 17.7128 7.79055 17.6522C7.92467 17.5916 8.04513 17.5045 8.1447 17.3961L8.1457 17.3951L12.0002 13.5406L15.8547 17.3951C15.9542 17.5035 16.0746 17.5907 16.2087 17.6514C16.3428 17.7121 16.4878 17.745 16.6349 17.7482C16.7821 17.7514 16.9283 17.7248 17.0649 17.67C17.2015 17.6151 17.3256 17.5333 17.4297 17.4292C17.5338 17.3252 17.6157 17.2012 17.6707 17.0646C17.7256 16.9281 17.7523 16.7818 17.7492 16.6347C17.7461 16.4875 17.7133 16.3425 17.6526 16.2084C17.592 16.0743 17.5049 15.9538 17.3965 15.8543L17.3955 15.8533L13.541 12.0007Z"
                                fill="black" />
                        </svg>
                    </button>
                </div>
            </div>

            <div className="container">
                <div className="row">
                    <div className="col-xxl">
                        <div className="card">
                            <div className="card-body">
                                <div className="form-group">
                                    {pedidos.length === 0 ? (
                                        <div className="text-center py-5">
                                            <p className="text-muted">Nenhum pedido encontrado.</p>
                                            <button 
                                                className="btn btn-primary mt-3"
                                                onClick={criarNovoPedido}
                                            >
                                                ➕ Criar Primeiro Pedido
                                            </button>
                                        </div>
                                    ) : (
                                        <div>
                                            <div className="d-flex justify-content-between align-items-center mb-3">
                                                <h5 className="mb-0">Total de pedidos: {pedidos.length}</h5>
                                            </div>
                                            <table className="table table-hover" style={{ width: '100%' }}>
                                                <thead>
                                                    <tr>
                                                        <th>ID do Pedido</th>
                                                        <th>Status</th>
                                                        <th>Ações</th>
                                                    </tr>
                                                </thead>
                                                <tbody>
                                                    {pedidos.map((pedido) => (
                                                        <tr key={pedido.id} className="trtabela">
                                                            <td>#{pedido.id.toString().padStart(3, '0')}</td>
                                                            <td>
                                                                <span className={`status-badge ${getStatusClass(pedido.estado)}`}>
                                                                    {pedido.estado_texto}
                                                                </span>
                                                            </td>
                                                            <td>
                                                                <button 
                                                                    className="btn btn-info btn-sm"
                                                                    onClick={() => verDetalhesPedido(pedido)}
                                                                    style={{
                                                                        padding: '4px 8px',
                                                                        fontSize: '0.875rem',
                                                                        backgroundColor: '#17a2b8',
                                                                        border: 'none',
                                                                        borderRadius: '4px',
                                                                        color: 'white',
                                                                        cursor: 'pointer'
                                                                    }}
                                                                >
                                                                    👁️ Ver Detalhes
                                                                </button>
                                                            </td>
                                                        </tr>
                                                    ))}
                                                </tbody>
                                            </table>
                                        </div>
                                    )}
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            {/* CSS para os status */}
            <style jsx>{`
                .status-badge {
                    padding: 4px 12px;
                    border-radius: 20px;
                    font-size: 0.875rem;
                    font-weight: 500;
                }
                .status-aguardando {
                    background-color: #fff3cd;
                    color: #856404;
                    border: 1px solid #ffeaa7;
                }
                .status-caminho {
                    background-color: #cce7ff;
                    color: #004085;
                    border: 1px solid #b3d7ff;
                }
                .status-entregue {
                    background-color: #d4edda;
                    color: #155724;
                    border: 1px solid #c3e6cb;
                }
                .status-finalizado {
                    background-color: #e2e3e5;
                    color: #383d41;
                    border: 1px solid #d6d8db;
                }
                .status-desconhecido {
                    background-color: #f8d7da;
                    color: #721c24;
                    border: 1px solid #f5c6cb;
                }
                .trtabela:hover {
                    background-color: #f8f9fa;
                    cursor: pointer;
                }
            `}</style>
        </div>
    );
};

export default PedidosLista;