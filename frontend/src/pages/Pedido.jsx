import React, { useState } from 'react';

const CadastroVendas = () => {
    const [operador] = useState({
        id: 1,
        local: "Nome do Evento"
    });

    const [nomeProduto, setNomeProduto] = useState('');
    const [quantidade, setQuantidade] = useState(1);
    const [produtosSelecionados, setProdutosSelecionados] = useState([]);

    const handleAdicionarProduto = (e) => {
        e.preventDefault();
        
        if (nomeProduto.trim() === '') {
            alert('Por favor, digite o nome do produto');
            return;
        }

        if (quantidade <= 0) {
            alert('A quantidade deve ser maior que zero');
            return;
        }

        const novoProduto = {
            id: Date.now() + Math.random(),
            nome: nomeProduto.trim(),
            quantidade: quantidade,
        };

        setProdutosSelecionados(prev => [...prev, novoProduto]);
        setNomeProduto('');
        setQuantidade(1);
    };

    const handleRemoveProduto = (id) => {
        setProdutosSelecionados(prev =>
            prev.filter(produto => produto.id !== id)
        );
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        console.log('Evento ID:', operador.id);
        console.log('Produtos selecionados:', produtosSelecionados);
        // Aqui você pode adicionar a lógica de pagamento
    };

    const calcularTotalItens = () => {
        return produtosSelecionados.reduce((total, produto) => total + produto.quantidade, 0);
    };

    return (
        <div className="container py-4">
            <div className="row justify-content-center">
                <div className="col-lg-10 col-md-12">
                    <div className="card shadow-lg border-0">
                        <div className="card-header bg-primary text-white py-3">
                            <h2 className="h4 mb-0 text-center">
                                <i className="bi bi-cart-plus me-2"></i>
                                Realizar Pedido
                            </h2>
                        </div>
                        
                        <div className="card-body p-4">
                            {/* Formulário de Adição de Produtos */}
                            <div className="adicionar-produto-section mb-5">
                                <h4 className="text-primary mb-4">
                                    <i className="bi bi-plus-circle me-2"></i>
                                    Adicionar Produto
                                </h4>
                                
                                <div className="row g-3 align-items-end">
                                    <div className="col-md-6">
                                        <label htmlFor="nomeProduto" className="form-label fw-semibold">
                                            Nome do Produto
                                        </label>
                                        <input
                                            type="text"
                                            id="nomeProduto"
                                            className="form-control form-control-lg"
                                            placeholder="Digite o nome do produto..."
                                            value={nomeProduto}
                                            onChange={(e) => setNomeProduto(e.target.value)}
                                            onKeyPress={(e) => e.key === 'Enter' && handleAdicionarProduto(e)}
                                        />
                                    </div>
                                    
                                    <div className="col-md-3">
                                        <label htmlFor="quantidade" className="form-label fw-semibold">
                                            Quantidade
                                        </label>
                                        <input
                                            type="number"
                                            id="quantidade"
                                            className="form-control form-control-lg"
                                            min="1"
                                            value={quantidade}
                                            onChange={(e) => setQuantidade(parseInt(e.target.value) || 1)}
                                        />
                                    </div>
                                    
                                    <div className="col-md-3">
                                        <button
                                            type="button"
                                            className="btn btn-success btn-lg w-100 py-3"
                                            onClick={handleAdicionarProduto}
                                        >
                                            <i className="bi bi-plus-lg me-2"></i>
                                            Adicionar
                                        </button>
                                    </div>
                                </div>
                            </div>

                            {/* Lista de Produtos Selecionados */}
                            <div className="lista-produtos-section">
                                <div className="d-flex justify-content-between align-items-center mb-4">
                                    <h4 className="text-primary mb-0">
                                        <i className="bi bi-list-check me-2"></i>
                                        Produtos Selecionados
                                    </h4>
                                    <span className="badge bg-primary fs-6">
                                        Total: {calcularTotalItens()} itens
                                    </span>
                                </div>

                                <div className="table-responsive">
                                    <table className="table table-hover align-middle">
                                        <thead className="table-primary">
                                            <tr>
                                                <th scope="col" className="py-3 ps-4">
                                                    <i className="bi bi-box me-2"></i>
                                                    Produto
                                                </th>
                                                <th scope="col" className="py-3 text-center">
                                                    <i className="bi bi-hash me-2"></i>
                                                    Quantidade
                                                </th>
                                                <th scope="col" className="py-3 text-center">
                                                    <i className="bi bi-gear me-2"></i>
                                                    Ações
                                                </th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            {produtosSelecionados.map((produto, index) => (
                                                <tr key={produto.id} className={index % 2 === 0 ? 'table-light' : ''}>
                                                    <td className="ps-4 fw-semibold">
                                                        {produto.nome}
                                                    </td>
                                                    <td className="text-center">
                                                        <span className="badge bg-secondary fs-6">
                                                            {produto.quantidade}
                                                        </span>
                                                    </td>
                                                    <td className="text-center">
                                                        <button
                                                            type="button"
                                                            className="btn btn-outline-danger btn-sm"
                                                            onClick={() => handleRemoveProduto(produto.id)}
                                                            title="Remover produto"
                                                        >
                                                            <i className="bi bi-trash me-1"></i>
                                                            Remover
                                                        </button>
                                                    </td>
                                                </tr>
                                            ))}
                                            
                                            {produtosSelecionados.length === 0 && (
                                                <tr>
                                                    <td colSpan="3" className="text-center py-5">
                                                        <div className="text-muted">
                                                            <i className="bi bi-cart-x display-4 d-block mb-3"></i>
                                                            <h5>Nenhum produto adicionado</h5>
                                                            <p className="mb-0">Adicione produtos usando o formulário acima</p>
                                                        </div>
                                                    </td>
                                                </tr>
                                            )}
                                        </tbody>
                                    </table>
                                </div>
                            </div>

                            {/* Resumo e Botão de Pagamento */}
                            {produtosSelecionados.length > 0 && (
                                <div className="resumo-section mt-5 pt-4 border-top">
                                    <div className="row justify-content-between align-items-center">
                                        <div className="col-md-6">
                                            <div className="d-flex align-items-center">
                                                <i className="bi bi-info-circle text-primary me-2 fs-5"></i>
                                                <div>
                                                    <h6 className="mb-1 fw-semibold">Resumo da Venda</h6>
                                                    <p className="mb-0 text-muted">
                                                        {produtosSelecionados.length} produto(s) • {calcularTotalItens()} item(s) no total
                                                    </p>
                                                </div>
                                            </div>
                                        </div>
                                        <div className="col-md-4 text-end">
                                            <button 
                                                type="submit" 
                                                className="btn btn-primary btn-lg px-5 py-3 w-100"
                                                onClick={handleSubmit}
                                            >
                                                <i className="bi bi-credit-card me-2"></i>
                                                Confirmar Pedido
                                            </button>
                                        </div>
                                    </div>
                                </div>
                            )}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default CadastroVendas;