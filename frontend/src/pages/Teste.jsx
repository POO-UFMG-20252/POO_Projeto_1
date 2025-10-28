import React, { useState, useEffect } from 'react';

function Teste() {
    const [itensEstoque, setItensEstoque] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetchEstoque();
    }, []);

    const fetchEstoque = async () => {
        try {
            const response = await fetch('http://localhost:5000/api/estoque');
            const data = await response.json();
            setItensEstoque(data);
            setLoading(false);
        } catch (error) {
            console.error('Erro ao buscar dados:', error);
            setLoading(false);
        }
    };

    if (loading) return <div>Carregando...</div>;

    return (
        <div>
            <h1>Estoque</h1>
            {/* Sua renderização dos itens aqui */}
            {itensEstoque.map(item => (
                <div key={item.id}>
                    <h3>{item.nome}</h3>
                    <p>Quantidade: {item.quantidade}</p>
                    <p>Localização: {item.localizacao}</p>
                    <p>Posição: Linha {item.posicao.linha}, Coluna {item.posicao.coluna}</p>
                </div>
            ))}
        </div>
    );
}

export default Teste;