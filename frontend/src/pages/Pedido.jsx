import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

const CadastroVendas = () => {
    const navigate = useNavigate();
    const [operador] = useState({
        id: 1,
        local: "Nome do Evento"
    });

    const [nomeProduto, setNomeProduto] = useState('');
    const [marcaProduto, setMarcaProduto] = useState('');
    const [precoProduto, setPrecoProduto] = useState('');
    const [quantidade, setQuantidade] = useState(1);
    const [produtosSelecionados, setProdutosSelecionados] = useState([]);
    const [loading, setLoading] = useState(false);
    const [mensagem, setMensagem] = useState('');

    const handleAdicionarProduto = (e) => {
        e.preventDefault();
        
        if (!nomeProduto.trim() || !marcaProduto.trim()) {
            setMensagem('❌ Por favor, preencha nome e marca do produto');
            return;
        }

        if (!precoProduto || parseFloat(precoProduto) <= 0) {
            setMensagem('❌ Preço deve ser maior que zero');
            return;
        }

        if (quantidade <= 0) {
            setMensagem('❌ Quantidade deve ser maior que zero');
            return;
        }

        // Verificar se o produto já foi adicionado (mesmo nome e marca)
        const produtoExistente = produtosSelecionados.find(p => 
            p.nome.toLowerCase() === nomeProduto.toLowerCase() && 
            p.marca.toLowerCase() === marcaProduto.toLowerCase()
        );
        
        if (produtoExistente) {
            // Atualizar quantidade se o produto já existe
            setProdutosSelecionados(prev =>
                prev.map(p =>
                    p.nome.toLowerCase() === nomeProduto.toLowerCase() && 
                    p.marca.toLowerCase() === marcaProduto.toLowerCase()
                        ? { 
                            ...p, 
                            quantidade: p.quantidade + quantidade,
                            preco: precoProduto // Atualizar preço também
                        }
                        : p
                )
            );
        } else {
            // Adicionar novo produto
            const novoProduto = {
                nome: nomeProduto.trim(),
                marca: marcaProduto.trim(),
                preco: parseFloat(precoProduto),
                quantidade: quantidade,
            };

            setProdutosSelecionados(prev => [...prev, novoProduto]);
        }

        // Limpar formulário
        setNomeProduto('');
        setMarcaProduto('');
        setPrecoProduto('');
        setQuantidade(1);
        setMensagem('✅ Produto adicionado com sucesso!');
    };

    const handleRemoveProduto = (index) => {
        setProdutosSelecionados(prev =>
            prev.filter((_, i) => i !== index)
        );
        setMensagem('✅ Produto removido!');
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        
        if (produtosSelecionados.length === 0) {
            setMensagem('❌ Adicione pelo menos um produto ao pedido');
            return;
        }

        setLoading(true);
        setMensagem('');

        try {
            const token = localStorage.getItem('token');
            if (!token) {
                navigate('/login');
                return;
            }

            // Preparar dados para a API no formato [nome, marca, preco, quantidade]
            const listaProdutos = produtosSelecionados.map(produto => [
                produto.nome,
                produto.marca,
                produto.preco,
                produto.quantidade
            ]);

            const pedidoData = {
                lista_produtos: listaProdutos
            };

            const response = await fetch('http://localhost:5000/api/pedido', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify(pedidoData)
            });

            if (response.ok) {
                const resultado = await response.json();
                setMensagem(`✅ Pedido #${resultado.pedido.id} criado com sucesso!`);
                
                // Limpar formulário
                setProdutosSelecionados([]);
                setNomeProduto('');
                setMarcaProduto('');
                setPrecoProduto('');
                setQuantidade(1);

                // Redirecionar após 2 segundos
                setTimeout(() => {
                    navigate('/');
                }, 20000);
            } else {
                const erro = await response.json();
                setMensagem(`❌ Erro: ${erro.mensagem || 'Erro ao criar pedido'}`);
            }
        } catch (error) {
            console.error('Erro ao criar pedido:', error);
            setMensagem('❌ Erro de conexão ao criar pedido');
        } finally {
            setLoading(false);
        }
    };

    const calcularTotalItens = () => {
        return produtosSelecionados.reduce((total, produto) => total + produto.quantidade, 0);
    };

    const calcularValorTotal = () => {
        return produtosSelecionados.reduce((total, produto) => total + (produto.preco * produto.quantidade), 0);
    };

    return (
        <div className="container py-4">
            <div className="row justify-content-center">
                <div className="col-lg-10 col-md-12">
                    <div className="card shadow-lg border-0">
                        <div className="card-header bg-primary text-white py-3">
                            <h2 className="h4 mb-0 text-center">
                                <i className="bi bi-cart-plus me-2"></i>
                                Criar Novo Pedido
                            </h2>
                        </div>
                        
                        <div className="card-body p-4">
                            {/* Mensagem de status */}
                            {mensagem && (
                                <div className={`alert ${mensagem.includes('✅') ? 'alert-success' : 'alert-danger'} mb-4`}>
                                    {mensagem}
                                </div>
                            )}

                            {/* Formulário de Adição de Produtos */}
                            <div className="adicionar-produto-section mb-5">
                                <h4 className="text-primary mb-4">
                                    <i className="bi bi-plus-circle me-2"></i>
                                    Adicionar Produto
                                </h4>
                                
                                <div className="row g-3 align-items-end">
                                    <div className="col-md-4">
                                        <label htmlFor="nomeProduto" className="form-label fw-semibold">
                                            Nome do Produto
                                        </label>
                                        <input
                                            type="text"
                                            id="nomeProduto"
                                            className="form-control form-control-lg"
                                            value={nomeProduto}
                                            onChange={(e) => setNomeProduto(e.target.value)}
                                            placeholder="Ex: Arroz, Feijão..."
                                        />
                                    </div>
                                    
                                    <div className="col-md-3">
                                        <label htmlFor="marcaProduto" className="form-label fw-semibold">
                                            Marca
                                        </label>
                                        <input
                                            type="text"
                                            id="marcaProduto"
                                            className="form-control form-control-lg"
                                            value={marcaProduto}
                                            onChange={(e) => setMarcaProduto(e.target.value)}
                                            placeholder="Ex: Tio João, Camil..."
                                        />
                                    </div>
                                    
                                    <div className="col-md-2">
                                        <label htmlFor="precoProduto" className="form-label fw-semibold">
                                            Preço (R$)
                                        </label>
                                        <input
                                            type="number"
                                            id="precoProduto"
                                            className="form-control form-control-lg"
                                            step="0.01"
                                            min="0.01"
                                            value={precoProduto}
                                            onChange={(e) => setPrecoProduto(e.target.value)}
                                            placeholder="0.00"
                                        />
                                    </div>
                                    
                                    <div className="col-md-2">
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
                                    
                                    <div className="col-md-1">
                                        <button
                                            type="button"
                                            className="btn btn-success btn-lg w-200 py-50"
                                            onClick={handleAdicionarProduto}
                                            disabled={!nomeProduto.trim() || !marcaProduto.trim() || !precoProduto}
                                            title="Adicionar produto ao pedido"
                                        >
                                            <i className="bi bi-plus-lg"></i>
                                        </button>
                                    </div>
                                </div>
                            </div>

                            {/* Lista de Produtos Selecionados */}
                            <div className="lista-produtos-section">
                                <div className="d-flex justify-content-between align-items-center mb-4">
                                    <h4 className="text-primary mb-0">
                                        <i className="bi bi-list-check me-2"></i>
                                        Produtos do Pedido
                                    </h4>
                                    <div>
                                        <span className="badge bg-primary fs-6 me-2">
                                            {calcularTotalItens()} itens
                                        </span>
                                        <span className="badge bg-success fs-6">
                                            R$ {calcularValorTotal().toFixed(2)}
                                        </span>
                                    </div>
                                </div>

                                <div className="table-responsive">
                                    <table className="table table-hover align-middle">
                                        <thead className="table-primary">
                                            <tr>
                                                <th scope="col" className="py-3 ps-4">Produto</th>
                                                <th scope="col" className="py-3">Marca</th>
                                                <th scope="col" className="py-3 text-center">Preço Unit.</th>
                                                <th scope="col" className="py-3 text-center">Quantidade</th>
                                                <th scope="col" className="py-3 text-center">Subtotal</th>
                                                <th scope="col" className="py-3 text-center">Ações</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            {produtosSelecionados.map((produto, index) => (
                                                <tr key={index} className={index % 2 === 0 ? 'table-light' : ''}>
                                                    <td className="ps-4 fw-semibold">{produto.nome}</td>
                                                    <td className="fw-semibold text-muted">{produto.marca}</td>
                                                    <td className="text-center">R$ {produto.preco.toFixed(2)}</td>
                                                    <td className="text-center">
                                                        <span className="badge bg-secondary fs-6">
                                                            {produto.quantidade}
                                                        </span>
                                                    </td>
                                                    <td className="text-center fw-bold text-primary">
                                                        R$ {(produto.preco * produto.quantidade).toFixed(2)}
                                                    </td>
                                                    <td className="text-center">
                                                        <button
                                                            type="button"
                                                            className="btn btn-outline-danger btn-sm"
                                                            onClick={() => handleRemoveProduto(index)}
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
                                                    <td colSpan="6" className="text-center py-5">
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

                            {/* Resumo e Botão de Pedido */}
                            {produtosSelecionados.length > 0 && (
                                <div className="resumo-section mt-5 pt-4 border-top">
                                    <div className="row justify-content-between align-items-center">
                                        <div className="col-md-6">
                                            <div className="d-flex align-items-center">
                                                <i className="bi bi-receipt text-primary me-2 fs-5"></i>
                                                <div>
                                                    <h6 className="mb-1 fw-semibold">Resumo do Pedido</h6>
                                                    <p className="mb-0 text-muted">
                                                        {produtosSelecionados.length} produto(s) • {calcularTotalItens()} item(s)
                                                    </p>
                                                    <p className="mb-0 fw-bold text-success">
                                                        Total: R$ {calcularValorTotal().toFixed(2)}
                                                    </p>
                                                </div>
                                            </div>
                                        </div>
                                        <div className="col-md-4 text-end">
                                            <button 
                                                type="button" 
                                                className="btn btn-primary btn-lg px-5 py-3 w-100"
                                                onClick={handleSubmit}
                                                disabled={loading}
                                            >
                                                {loading ? (
                                                    <>
                                                        <span className="spinner-border spinner-border-sm me-2" />
                                                        Criando Pedido...
                                                    </>
                                                ) : (
                                                    <>
                                                        <i className="bi bi-check-circle me-2"></i>
                                                        Confirmar Pedido
                                                    </>
                                                )}
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