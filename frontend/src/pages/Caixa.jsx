import React, { useState, useEffect, useRef } from 'react';

const CadastroEventos = () => {
    const [operador, setOperador] = useState({
        id: 1,
        local: "Nome do Evento"
    });

    const [searchTerm, setSearchTerm] = useState('');
    const [suggestions, setSuggestions] = useState([]);
    const [showSuggestions, setShowSuggestions] = useState(false);
    const [equipamentosSelecionados, setEquipamentosSelecionados] = useState([]);
    const suggestionsRef = useRef(null);

    // Mock data
    const equipamentosMock = [
        { id: 1, nome: "Notebook Dell", fabricante: "Dell", numeroSerie: "SN001", patrimonio: "PAT001" },
        { id: 2, nome: "Projetor Epson", fabricante: "Epson", numeroSerie: "SN002", patrimonio: "PAT002" },
        { id: 3, nome: "Tablet Samsung", fabricante: "Samsung", numeroSerie: "SN003", patrimonio: "PAT003" },
        { id: 4, nome: "Monitor LG", fabricante: "LG", numeroSerie: "SN004", patrimonio: "PAT004" },
        { id: 5, nome: "Teclado Microsoft", fabricante: "Microsoft", numeroSerie: "SN005", patrimonio: "PAT005" }
    ];

    // Filtra equipamentos baseado no termo de pesquisa
    useEffect(() => {
        if (searchTerm.trim() === '') {
            setSuggestions([]);
            setShowSuggestions(false);
        } else {
            const filtered = equipamentosMock.filter(equipamento =>
                equipamento.nome.toLowerCase().includes(searchTerm.toLowerCase()) ||
                equipamento.fabricante.toLowerCase().includes(searchTerm.toLowerCase())
            );
            setSuggestions(filtered);
            setShowSuggestions(filtered.length > 0);
        }
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

    const handleSelectEquipamento = (equipamento) => {
        const novoEquipamento = {
            ...equipamento,
            uniqueId: Date.now() + Math.random()
        };

        setEquipamentosSelecionados(prev => [...prev, novoEquipamento]);
        setSearchTerm('');
        setShowSuggestions(false);
    };

    const handleRemoveEquipamento = (uniqueId) => {
        setEquipamentosSelecionados(prev =>
            prev.filter(equipamento => equipamento.uniqueId !== uniqueId)
        );
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        console.log('Evento ID:', operador.id);
        console.log('Equipamentos selecionados:', equipamentosSelecionados);
    };

    return (
        <div className="container p-4">
            <form onSubmit={handleSubmit}>
                <div className="row">
                    <div className="col-md-12 mx-auto">
                        <div className="card text-center">
                            <div className="card-body">
                                <p className="areatitles1">Cadastrar Compra</p>

                                <input
                                    type="hidden"
                                    id="eventoId"
                                    value={operador.id}
                                />

                                <div className="form-group search-container">
                                    <label htmlFor="searchEquipamento" className="form-label">
                                        Pesquisar Produto
                                    </label>
                                    <input
                                        type="text"
                                        id="searchEquipamento"
                                        className="form-control"
                                        placeholder="Digite o nome do equipamento"
                                        value={searchTerm}
                                        onChange={handleSearchChange}
                                    />

                                    {showSuggestions && (
                                        <ul
                                            ref={suggestionsRef}
                                            className="list-group suggestions-list"
                                        >
                                            {suggestions.map(equipamento => (
                                                <li
                                                    key={equipamento.id}
                                                    className="list-group-item list-group-item-action suggestion-item"
                                                    onClick={() => handleSelectEquipamento(equipamento)}
                                                >
                                                    <div className="suggestion-content">
                                                        <strong>{equipamento.nome}</strong>
                                                        <span className="suggestion-fabricante">
                                                            {equipamento.fabricante}
                                                        </span>
                                                    </div>
                                                </li>
                                            ))}
                                        </ul>
                                    )}
                                </div>

                                <div className="p-4 lista-equipamentos-wrapper">
                                    <div className="row">
                                        <div className="col-md-12 mx-auto">
                                            <div className="card text-center">
                                                <div className="card-body">
                                                    <p className="areatitles1 mt-4">
                                                        <strong>Lista de Produtos Selecionados</strong>
                                                    </p>
                                                    <div className="equipamentos-container">
                                                        <table className="table table-bordered table-hover equipamentos-table">
                                                            <thead className="table-header">
                                                                <tr>
                                                                    <th className="table-cell-border">Nome</th>
                                                                    <th className="table-cell-border">Fabricante</th>
                                                                    <th className="table-cell-border">N° de Série</th>
                                                                    <th className="table-cell-border">Quantidade</th>
                                                                    <th className="table-cell-border">Ação</th>
                                                                </tr>
                                                            </thead>
                                                            <tbody>
                                                                {equipamentosSelecionados.map(equipamento => (
                                                                    <tr key={equipamento.uniqueId} className="table-row">
                                                                        <td className="table-cell-border">{equipamento.nome}</td>
                                                                        <td className="table-cell-border">{equipamento.fabricante}</td>
                                                                        <td className="table-cell-border">{equipamento.numeroSerie}</td>
                                                                        <td className="table-cell-border">{equipamento.quantidade}</td>
                                                                        <td className="table-cell-border">
                                                                            <button
                                                                                type="button"
                                                                                className="btn btn-danger btn-sm btn-remove"
                                                                                onClick={() => handleRemoveEquipamento(equipamento.uniqueId)}
                                                                            >
                                                                                Remover
                                                                            </button>
                                                                        </td>
                                                                    </tr>
                                                                ))}
                                                                {equipamentosSelecionados.length === 0 && (
                                                                    <tr>
                                                                        <td colSpan="5" className="text-muted table-cell-border">
                                                                            Nenhum equipamento selecionado
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
                                    <button type="submit" className="btn btn-primary btn-submit">
                                        Pagamento
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </form>
        </div>
    );
};

export default CadastroEventos;