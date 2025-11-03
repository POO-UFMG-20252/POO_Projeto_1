import React, { useState, useEffect, useRef } from 'react';

const Caixa = () => {
    const [operador, setOperador] = useState({
        id: 1,
        local: "Caixa Principal"
    });

    const [searchTerm, setSearchTerm] = useState('');
    const [suggestions, setSuggestions] = useState([]);
    const [showSuggestions, setShowSuggestions] = useState(false);
    const [produtosSelecionados, setProdutosSelecionados] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [showModalPix, setShowModalPix] = useState(false);
    const [dadosVenda, setDadosVenda] = useState(null);
    const suggestionsRef = useRef(null);

    // Buscar produtos do backend
    useEffect(() => {
        const buscarProdutos = async () => {
            if (searchTerm.trim() === '' || searchTerm.length < 2) {
                setSuggestions([]);
                setShowSuggestions(false);
                return;
            }

            setLoading(true);
            setError('');

            try {
                const token = localStorage.getItem('token');
                if (!token) {
                    throw new Error('Usuário não autenticado');
                }

                const response = await fetch(`http://localhost:5000/api/produto/buscar?q=${encodeURIComponent(searchTerm)}`, {
                    method: 'GET',
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        'Content-Type': 'application/json',
                    },
                });

                if (!response.ok) {
                    throw new Error('Erro ao buscar produtos');
                }

                const produtos = await response.json();
                setSuggestions(produtos);
                setShowSuggestions(produtos.length > 0);
                
            } catch (error) {
                console.error('Erro ao buscar produtos:', error);
                setError('Erro ao buscar produtos. Tente novamente.');
                setSuggestions([]);
                setShowSuggestions(false);
            } finally {
                setLoading(false);
            }
        };

        const timeoutId = setTimeout(buscarProdutos, 300);
        return () => clearTimeout(timeoutId);
    }, [searchTerm]);

    // Fecha as sugestões quando clicar fora
    useEffect(() => {
        const handleClickOutside = (event) => {
            if (suggestionsRef.current && !suggestionsRef.current.contains(event.target)) {
                setShowSuggestions(false);
            }
        };

        document.addEventListener('mousedown', handleClickOutside);
        return () => {
            document.removeEventListener('mousedown', handleClickOutside);
        };
    }, []);

    const handleSearchChange = (e) => {
        setSearchTerm(e.target.value);
    };

    const destacarTexto = (texto, termo) => {
        if (!texto || !termo) return texto;
        
        const regex = new RegExp(`(${termo})`, 'gi');
        return texto.split(regex).map((part, index) => 
            regex.test(part) ? <mark key={index}>{part}</mark> : part
        );
    };

    const handleSelectProduto = (produtoSelecionado) => {
        setProdutosSelecionados(prevProdutos => {
            const existente = prevProdutos.find(
                prod => prod.id === produtoSelecionado.id
            );

            if (existente) {
                return prevProdutos.map(prod =>
                    prod.id === produtoSelecionado.id
                        ? { 
                            ...prod, 
                            quantidade: prod.quantidade + 1,
                            total: (prod.quantidade + 1) * prod.preco
                        }
                        : prod
                );
            } else {
                return [
                    ...prevProdutos,
                    {
                        ...produtoSelecionado,
                        quantidade: 1,
                        total: produtoSelecionado.preco,
                        uniqueId: Date.now()
                    }
                ];
            }
        });

        setSearchTerm("");
        setShowSuggestions(false);
    };

    const handleRemoveProduto = (uniqueId) => {
        setProdutosSelecionados(prev =>
            prev.filter(produto => produto.uniqueId !== uniqueId)
        );
    };

    const handleUpdateQuantidade = (uniqueId, novaQuantidade) => {
        if (novaQuantidade < 1) return;

        setProdutosSelecionados(prevProdutos =>
            prevProdutos.map(produto =>
                produto.uniqueId === uniqueId
                    ? {
                        ...produto,
                        quantidade: novaQuantidade,
                        total: novaQuantidade * produto.preco
                    }
                    : produto
            )
        );
    };

    const calcularTotalVenda = () => {
        return produtosSelecionados.reduce((total, produto) => total + produto.total, 0);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        
        if (produtosSelecionados.length === 0) {
            alert('Adicione pelo menos um produto para realizar a venda.');
            return;
        }

        setLoading(true);
        setError('');

        try {
            const token = localStorage.getItem('token');
            if (!token) {
                throw new Error('Usuário não autenticado');
            }

            const itensVenda = produtosSelecionados.map(produto => ({
                id: produto.id,
                nome: produto.nome,
                preco: produto.preco,
                quantidade: produto.quantidade
            }));

            console.log('Enviando venda:', itensVenda);

            const response = await fetch('http://localhost:5000/api/caixa/venda/processar', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ itens: itensVenda })
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.message || 'Erro ao processar venda');
            }

            console.log('Venda processada com sucesso:', data);
            
            // Mostrar modal com dados do PIX
            setDadosVenda(data);
            setShowModalPix(true);
            
        } catch (error) {
            console.error('Erro ao processar venda:', error);
            setError(error.message);
            alert(`Erro ao processar venda: ${error.message}`);
        } finally {
            setLoading(false);
        }
    };

    const handleFecharModal = () => {
        setShowModalPix(false);
        setDadosVenda(null);
        // Limpar carrinho após fechar o modal
        setProdutosSelecionados([]);
    };

    const copiarCodigoPix = () => {
        if (dadosVenda?.codigo_pix) {
            navigator.clipboard.writeText(dadosVenda.codigo_pix);
            alert('Código PIX copiado para a área de transferência!');
        }
    };

    return (
        <div className="container p-4">
            <form onSubmit={handleSubmit}>
                <div className="row">
                    <div className="col-md-12 mx-auto">
                        <div className="card text-center">
                            <div className="card-body">
                                <p className="areatitles1">Sistema de Caixa</p>

                                <input
                                    type="hidden"
                                    id="operadorId"
                                    value={operador.id}
                                />

                                <div className="form-group search-container">
                                    <label htmlFor="searchProduto" className="form-label">
                                        Pesquisar Produto
                                    </label>
                                    <input
                                        type="text"
                                        id="searchProduto"
                                        className="form-control"
                                        placeholder="Digite o nome do produto ou marca (mínimo 2 caracteres)"
                                        value={searchTerm}
                                        onChange={handleSearchChange}
                                        disabled={loading}
                                    />

                                    {loading && (
                                        <div className="text-muted mt-2">
                                            <small>Buscando produtos...</small>
                                        </div>
                                    )}

                                    {error && (
                                        <div className="text-danger mt-2">
                                            <small>{error}</small>
                                        </div>
                                    )}

                                    {showSuggestions && (
                                        <ul
                                            ref={suggestionsRef}
                                            className="list-group suggestions-list"
                                        >
                                            {suggestions.map(produto => (
                                                <li
                                                    key={produto.id}
                                                    className="list-group-item list-group-item-action suggestion-item"
                                                    onClick={() => handleSelectProduto(produto)}
                                                >
                                                    <div className="suggestion-content">
                                                        <div className="suggestion-texto">
                                                            <div className="suggestion-nome">
                                                                {destacarTexto(produto.nome, searchTerm)}
                                                            </div>
                                                            {produto.marca && (
                                                                <div className="suggestion-marca">
                                                                    Marca: {destacarTexto(produto.marca, searchTerm)}
                                                                </div>
                                                            )}
                                                        </div>
                                                        <div className="suggestion-preco">
                                                            R$ {produto.preco.toFixed(2)}
                                                        </div>
                                                    </div>
                                                </li>
                                            ))}
                                        </ul>
                                    )}
                                </div>

                                <div className="p-4 lista-produtos-wrapper">
                                    <div className="row">
                                        <div className="col-md-12 mx-auto">
                                            <div className="card text-center">
                                                <div className="card-body">
                                                    <p className="areatitles1 mt-4">
                                                        <strong>Carrinho de Compras</strong>
                                                    </p>
                                                    
                                                    {produtosSelecionados.length > 0 && (
                                                        <div className="total-venda mb-3">
                                                            <h5>Total da Venda: <strong>R$ {calcularTotalVenda().toFixed(2)}</strong></h5>
                                                        </div>
                                                    )}

                                                    <div className="produtos-container">
                                                        <table className="table table-bordered table-hover produtos-table">
                                                            <thead className="table-header">
                                                                <tr>
                                                                    <th className="table-cell-border">Produto</th>
                                                                    <th className="table-cell-border">Marca</th>
                                                                    <th className="table-cell-border">Preço Unit.</th>
                                                                    <th className="table-cell-border">Quantidade</th>
                                                                    <th className="table-cell-border">Total</th>
                                                                    <th className="table-cell-border">Ações</th>
                                                                </tr>
                                                            </thead>
                                                            <tbody>
                                                                {produtosSelecionados.map(produto => (
                                                                    <tr key={produto.uniqueId} className="table-row">
                                                                        <td className="table-cell-border">{produto.nome}</td>
                                                                        <td className="table-cell-border">{produto.marca || '-'}</td>
                                                                        <td className="table-cell-border">R$ {produto.preco.toFixed(2)}</td>
                                                                        <td className="table-cell-border">
                                                                            <div className="quantidade-controls">
                                                                                <button
                                                                                    type="button"
                                                                                    className="btn btn-sm btn-outline-secondary"
                                                                                    onClick={() => handleUpdateQuantidade(produto.uniqueId, produto.quantidade - 1)}
                                                                                    disabled={produto.quantidade <= 1}
                                                                                >
                                                                                    -
                                                                                </button>
                                                                                <span className="mx-2">{produto.quantidade}</span>
                                                                                <button
                                                                                    type="button"
                                                                                    className="btn btn-sm btn-outline-secondary"
                                                                                    onClick={() => handleUpdateQuantidade(produto.uniqueId, produto.quantidade + 1)}
                                                                                >
                                                                                    +
                                                                                </button>
                                                                            </div>
                                                                        </td>
                                                                        <td className="table-cell-border">
                                                                            <strong>R$ {produto.total.toFixed(2)}</strong>
                                                                        </td>
                                                                        <td className="table-cell-border">
                                                                            <button
                                                                                type="button"
                                                                                className="btn btn-danger btn-sm btn-remove"
                                                                                onClick={() => handleRemoveProduto(produto.uniqueId)}
                                                                                disabled={loading}
                                                                            >
                                                                                Remover
                                                                            </button>
                                                                        </td>
                                                                    </tr>
                                                                ))}
                                                                {produtosSelecionados.length === 0 && (
                                                                    <tr>
                                                                        <td colSpan="6" className="text-muted table-cell-border">
                                                                            Nenhum produto selecionado. Use a pesquisa acima para adicionar produtos.
                                                                        </td>
                                                                    </tr>
                                                                )}
                                                            </tbody>
                                                        </table>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>

                                <div className="mt-4">
                                    <button 
                                        type="submit" 
                                        className="btn btn-primary btn-submit"
                                        disabled={loading || produtosSelecionados.length === 0}
                                    >
                                        {loading ? 'Processando...' : `Finalizar Venda - R$ ${calcularTotalVenda().toFixed(2)}`}
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </form>

            {/* Modal PIX */}
            {showModalPix && dadosVenda && (
                <div className="modal-backdrop show d-block">
                    <div className="modal d-block" tabIndex="-1">
                        <div className="modal-dialog modal-dialog-centered">
                            <div className="modal-content">
                                <div className="modal-header bg-success text-white">
                                    <h5 className="modal-title">✅ Pagamento via PIX</h5>
                                </div>
                                <div className="modal-body text-center">
                                    <div className="p-4">
                                        <div className="mb-4">
                                            <h4>Total da Compra</h4>
                                            <h2 className="text-success">R$ {dadosVenda.total_venda.toFixed(2)}</h2>
                                        </div>
                                        
                                        <div className="mb-4">
                                            <h5>Código PIX</h5>
                                            <div className="p-3 bg-light rounded">
                                                <code className="fs-5 text-primary">{dadosVenda.codigo_pix}</code>
                                            </div>
                                            <button 
                                                className="btn btn-outline-primary btn-sm mt-2"
                                                onClick={copiarCodigoPix}
                                            >
                                                📋 Copiar Código
                                            </button>
                                        </div>
                                        
                                        <div className="alert alert-info">
                                            <small>
                                                💡 Use este código para pagar via PIX em qualquer app bancário.<br/>
                                                A venda será confirmada automaticamente.
                                            </small>
                                        </div>
                                    </div>
                                </div>
                                <div className="modal-footer">
                                    <button 
                                        type="button" 
                                        className="btn btn-success"
                                        onClick={handleFecharModal}
                                    >
                                        ✅ Venda Concluída
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            )}

            <style jsx>{`
                .search-container {
                    position: relative;
                }

                .suggestions-list {
                    position: absolute;
                    top: 100%;
                    left: 0;
                    right: 0;
                    z-index: 1000;
                    max-height: 200px;
                    overflow-y: auto;
                }

                .suggestion-item {
                    cursor: pointer;
                    transition: background-color 0.2s;
                }

                .suggestion-item:hover {
                    background-color: #f8f9fa;
                }

                .suggestion-content {
                    display: flex;
                    justify-content: space-between;
                    align-items: flex-start;
                }

                .suggestion-texto {
                    flex: 1;
                    text-align: left;
                }

                .suggestion-nome {
                    font-weight: bold;
                    margin-bottom: 2px;
                }

                .suggestion-marca {
                    font-size: 0.85em;
                    color: #6c757d;
                }

                .suggestion-preco {
                    font-weight: bold;
                    color: #28a745;
                    white-space: nowrap;
                    margin-left: 10px;
                }

                mark {
                    background-color: #fff3cd;
                    padding: 1px 2px;
                    border-radius: 2px;
                }

                .quantidade-controls {
                    display: flex;
                    align-items: center;
                    justify-content: center;
                }

                .quantidade-controls button {
                    width: 30px;
                    height: 30px;
                }

                .total-venda {
                    background-color: #e9ecef;
                    padding: 10px;
                    border-radius: 5px;
                    border-left: 4px solid #28a745;
                }

                .btn-submit:disabled {
                    opacity: 0.6;
                    cursor: not-allowed;
                }

                .areatitles1 {
                    font-size: 1.5rem;
                    font-weight: bold;
                    color: #333;
                    margin-bottom: 1rem;
                }

                .table-cell-border {
                    vertical-align: middle;
                }

                .btn-remove {
                    white-space: nowrap;
                }

                .modal-backdrop {
                    background-color: rgba(0, 0, 0, 0.5);
                }
            `}</style>
        </div>
    );
};

export default Caixa;