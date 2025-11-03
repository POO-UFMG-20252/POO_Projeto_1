import React, { useState, useEffect } from 'react';

const EventosLista = () => {
    const [funcionarios, setFuncionarios] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const carregarFuncionarios = async () => {
            try {
                setLoading(true);
                setError(null);

                const token = localStorage.getItem('token');
                if (!token) {
                    navigate('/login');
                    return;
                }
                
                const response = await fetch('http://localhost:5000/api/funcionarios', {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    }
                });

                if (!response.ok) {
                    throw new Error(`Erro ${response.status}: ${response.statusText}`);
                }

                const dadosFuncionarios = await response.json();
                setFuncionarios(dadosFuncionarios);
                
            } catch (error) {
                console.error('Erro ao carregar funcionários:', error);
                setError('Erro ao carregar lista de funcionários. Tente novamente.');
            } finally {
                setLoading(false);
            }
        };

        carregarFuncionarios();
    }, []);

    const goBack = () => {
        window.history.back();
    };

    const redirecionar = () => {
        // Lógica de redirecionamento
        console.log('Redirecionando...');
    };

    const irParaCadastro = () => {
        window.location.href = '/cadastro_func';
    };

    // Função para formatar a data no formato brasileiro
    const formatarData = (dataString) => {
        if (!dataString) return '-';
        try {
            const data = new Date(dataString);
            return data.toLocaleDateString('pt-BR');
        } catch {
            return dataString;
        }
    };

    if (loading) {
        return (
            <div className="eventos-lista-container">
                <div className="loading-container">
                    <div className="loading">Carregando funcionários...</div>
                </div>
                <style jsx>{`
                    .loading-container {
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        height: 200px;
                    }
                    .loading {
                        text-align: center;
                        font-size: 18px;
                        color: #666;
                    }
                `}</style>
            </div>
        );
    }

    if (error) {
        return (
            <div className="eventos-lista-container">
                <div className="error-container">
                    <div className="error-message">{error}</div>
                    <button 
                        className="btn-retry"
                        onClick={() => window.location.reload()}
                    >
                        Tentar Novamente
                    </button>
                </div>
                <style jsx>{`
                    .error-container {
                        display: flex;
                        flex-direction: column;
                        justify-content: center;
                        align-items: center;
                        height: 200px;
                        gap: 20px;
                    }
                    .error-message {
                        color: #dc3545;
                        font-size: 16px;
                        text-align: center;
                    }
                    .btn-retry {
                        background-color: #007bff;
                        color: white;
                        border: none;
                        padding: 10px 20px;
                        border-radius: 6px;
                        cursor: pointer;
                    }
                    .btn-retry:hover {
                        background-color: #0056b3;
                    }
                `}</style>
            </div>
        );
    }

    return (
        <div className="eventos-lista-container">
            <div className="boxH1ResPadraoDesktop">
                <div className="mesPremiadoPadraoDesktop">
                    <h1 className="h1ResPadraoDesktop">Lista de Funcionários</h1>
                    <div className="total-funcionarios">
                        Total: {funcionarios.length} funcionário(s)
                    </div>
                </div>
                <div className="botoes-header">
                    <button 
                        className="btn-cadastrar-funcionario"
                        onClick={irParaCadastro}
                    >
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16" style={{ marginRight: '8px' }}>
                            <path d="M8 4a.5.5 0 0 1 .5.5v3h3a.5.5 0 0 1 0 1h-3v3a.5.5 0 0 1-1 0v-3h-3a.5.5 0 0 1 0-1h3v-3A.5.5 0 0 1 8 4z"/>
                        </svg>
                        Cadastrar Funcionário
                    </button>
                    <button 
                        className="svgXSairTabelas" 
                        data-placement="bottom" 
                        onClick={goBack}
                        aria-label="Voltar"
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
                                    {funcionarios.length === 0 ? (
                                        <div className="no-data">
                                            Nenhum funcionário cadastrado
                                        </div>
                                    ) : (
                                        <table className="table table-hover" style={{ width: '100%' }}>
                                            <thead>
                                                <tr>
                                                    <th>CPF</th>
                                                    <th>Nome do Funcionário</th>
                                                    <th>Data de Admissão</th>
                                                </tr>
                                            </thead>
                                            <tbody>
                                                {funcionarios.map((funcionario) => (
                                                    <tr key={funcionario.cpf} className="trtabela">
                                                        <td>{funcionario.cpf}</td>
                                                        <td>{funcionario.nome}</td>
                                                        <td>{formatarData(funcionario.data_admissao)}</td>
                                                    </tr>
                                                ))}
                                            </tbody>
                                        </table>
                                    )}
                                    
                                    <button 
                                        id="btnRedirecionar" 
                                        className="btn btn-primary" 
                                        style={{ display: 'none' }} 
                                        onClick={redirecionar}
                                    >
                                        Redirecionar
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <style jsx>{`
                .eventos-lista-container {
                    padding: 20px;
                }
                
                .boxH1ResPadraoDesktop {
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    margin-bottom: 30px;
                    padding: 20px;
                    background: white;
                    border-radius: 8px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }
                
                .mesPremiadoPadraoDesktop {
                    display: flex;
                    flex-direction: column;
                    gap: 5px;
                }
                
                .total-funcionarios {
                    color: #666;
                    font-size: 14px;
                    font-weight: normal;
                }
                
                .botoes-header {
                    display: flex;
                    align-items: center;
                    gap: 15px;
                }
                
                .btn-cadastrar-funcionario {
                    display: flex;
                    align-items: center;
                    background-color: #007bff;
                    color: white;
                    border: none;
                    padding: 10px 20px;
                    border-radius: 6px;
                    font-size: 14px;
                    font-weight: 600;
                    cursor: pointer;
                    transition: background-color 0.3s ease;
                }
                
                .btn-cadastrar-funcionario:hover {
                    background-color: #0056b3;
                }
                
                .h1ResPadraoDesktop {
                    margin: 0;
                    color: #333;
                    font-size: 28px;
                    font-weight: 600;
                }
                
                .svgXSairTabelas {
                    background: none;
                    border: none;
                    cursor: pointer;
                    padding: 8px;
                    border-radius: 4px;
                    transition: background-color 0.3s;
                }
                
                .svgXSairTabelas:hover {
                    background-color: #f8f9fa;
                }
                
                .card {
                    border: none;
                    border-radius: 8px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                }
                
                .card-body {
                    padding: 0;
                }
                
                .table {
                    margin-bottom: 0;
                }
                
                .table th {
                    background-color: #f8f9fa;
                    border-bottom: 2px solid #dee2e6;
                    font-weight: 600;
                    color: #495057;
                    padding: 15px;
                }
                
                .table td {
                    vertical-align: middle;
                    padding: 12px 15px;
                }
                
                .trtabela:hover {
                    background-color: #f8f9fa;
                    cursor: pointer;
                }
                
                .no-data {
                    text-align: center;
                    padding: 40px;
                    color: #666;
                    font-style: italic;
                }
            `}</style>
        </div>
    );
};

export default EventosLista;