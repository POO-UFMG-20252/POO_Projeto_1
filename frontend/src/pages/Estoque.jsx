import React, { useState, useEffect } from 'react';

const EstoqueVisualizacao = () => {
  // Estados para as matrizes
  const [matrizArmazem, setMatrizArmazem] = useState([]);
  const [matrizLoja, setMatrizLoja] = useState([]);
  const [produtos, setProdutos] = useState([]);
  const [produtoSelecionado, setProdutoSelecionado] = useState(null);
  const [modoMovimento, setModoMovimento] = useState(false);

  // Configurações
  const [tamanhoArmazem, setTamanhoArmazem] = useState({ linhas: 5, colunas: 5 });
  const [tamanhoLoja, setTamanhoLoja] = useState({ linhas: 3, colunas: 3 });
  const [capacidadeMaxima, setCapacidadeMaxima] = useState(500);

  // Simulação de produtos do backend
  const simularProdutosBackend = () => {
    const produtosMock = [
      { id: 1, nome: "Refrigerante Lata", quantidade: 300, localizacao: 'armazem', posicao: { linha: 0, coluna: 0 } },
      { id: 2, nome: "Água Mineral", quantidade: 450, localizacao: 'armazem', posicao: { linha: 0, coluna: 1 } },
      { id: 3, nome: "Suco Natural", quantidade: 200, localizacao: 'armazem', posicao: { linha: 1, coluna: 2 } },
      { id: 4, nome: "Energético", quantidade: 480, localizacao: 'armazem', posicao: { linha: 2, coluna: 1 } },
      { id: 5, nome: "Chá Gelado", quantidade: 150, localizacao: 'armazem', posicao: { linha: 3, coluna: 3 } },
      { id: 6, nome: "Refrigerante 2L", quantidade: 350, localizacao: 'loja', posicao: { linha: 0, coluna: 0 } },
      { id: 7, nome: "Cerveja", quantidade: 500, localizacao: 'loja', posicao: { linha: 1, coluna: 1 } },
      { id: 8, nome: "Água com Gás", quantidade: 280, localizacao: 'loja', posicao: { linha: 2, coluna: 2 } }
    ];
    
    setProdutos(produtosMock);
    return produtosMock;
  };

  // Função para inicializar matriz vazia
  const inicializarMatrizVazia = (linhas, colunas, tipo) => {
    const matriz = [];
    for (let i = 0; i < linhas; i++) {
      const linha = [];
      for (let j = 0; j < colunas; j++) {
        linha.push({
          quantidade: 0,
          porcentagem: 0,
          linha: i,
          coluna: j,
          produto: null,
          ocupada: false,
          tipo: tipo
        });
      }
      matriz.push(linha);
    }
    return matriz;
  };

  // Função para mapear produtos para as matrizes
  const mapearProdutosParaMatrizes = (produtosList) => {
    // Inicializar matrizes vazias
    const novaMatrizArmazem = inicializarMatrizVazia(tamanhoArmazem.linhas, tamanhoArmazem.colunas, 'armazem');
    const novaMatrizLoja = inicializarMatrizVazia(tamanhoLoja.linhas, tamanhoLoja.colunas, 'loja');

    // Preencher matrizes com produtos
    produtosList.forEach(produto => {
      const { linha, coluna } = produto.posicao;
      const porcentagem = (produto.quantidade / capacidadeMaxima) * 100;
      
      const celula = {
        quantidade: produto.quantidade,
        porcentagem: porcentagem,
        linha: linha,
        coluna: coluna,
        produto: produto.nome,
        produtoId: produto.id,
        ocupada: true,
        tipo: produto.localizacao
      };

      if (produto.localizacao === 'armazem' && linha < tamanhoArmazem.linhas && coluna < tamanhoArmazem.colunas) {
        novaMatrizArmazem[linha][coluna] = celula;
      } else if (produto.localizacao === 'loja' && linha < tamanhoLoja.linhas && coluna < tamanhoLoja.colunas) {
        novaMatrizLoja[linha][coluna] = celula;
      }
    });

    setMatrizArmazem(novaMatrizArmazem);
    setMatrizLoja(novaMatrizLoja);
  };

  // Função para adicionar produto aleatório no armazém
  const adicionarProdutoAleatorio = () => {
    const nomesProdutos = [
      "Refrigerante Lata", "Água Mineral", "Suco Natural", "Energético", 
      "Chá Gelado", "Refrigerante 2L", "Cerveja", "Água com Gás", 
      "Suco de Laranja", "Refrigerante Guaraná"
    ];
    
    // Encontrar posição vazia no armazém
    let posicaoEncontrada = false;
    let linha, coluna;
    
    while (!posicaoEncontrada) {
      linha = Math.floor(Math.random() * tamanhoArmazem.linhas);
      coluna = Math.floor(Math.random() * tamanhoArmazem.colunas);
      
      const celula = matrizArmazem[linha]?.[coluna];
      if (!celula?.ocupada) {
        posicaoEncontrada = true;
      }
    }

    const novoProduto = {
      id: Date.now(),
      nome: nomesProdutos[Math.floor(Math.random() * nomesProdutos.length)],
      quantidade: Math.floor(Math.random() * capacidadeMaxima) + 1,
      localizacao: 'armazem',
      posicao: { linha, coluna }
    };

    const novosProdutos = [...produtos, novoProduto];
    setProdutos(novosProdutos);
    mapearProdutosParaMatrizes(novosProdutos);
  };

  // Função para mover produto entre matrizes
  const moverProduto = (produtoId, novaLocalizacao, novaPosicao) => {
    const novosProdutos = produtos.map(produto => {
      if (produto.id === produtoId) {
        return {
          ...produto,
          localizacao: novaLocalizacao,
          posicao: novaPosicao
        };
      }
      return produto;
    });

    setProdutos(novosProdutos);
    mapearProdutosParaMatrizes(novosProdutos);
    setProdutoSelecionado(null);
    setModoMovimento(false);
  };

  // Função para selecionar produto para movimento
  const selecionarProdutoParaMovimento = (produtoId, localizacaoAtual) => {
    const produto = produtos.find(p => p.id === produtoId);
    setProdutoSelecionado(produto);
    setModoMovimento(true);
  };

  // Função para cancelar movimento
  const cancelarMovimento = () => {
    setProdutoSelecionado(null);
    setModoMovimento(false);
  };

  // Função para lidar com clique na célula (quando em modo movimento)
  const handleCliqueCelula = (linha, coluna, tipoMatriz) => {
    if (!modoMovimento || !produtoSelecionado) return;

    // Verificar se a célula de destino está vazia
    const matrizDestino = tipoMatriz === 'armazem' ? matrizArmazem : matrizLoja;
    
    if (matrizDestino[linha][coluna].ocupada) {
      alert('Célula de destino já está ocupada!');
      return;
    }

    // Mover o produto
    moverProduto(produtoSelecionado.id, tipoMatriz, { linha, coluna });
  };

  // Função para remover produto
  const removerProduto = (produtoId) => {
    const novosProdutos = produtos.filter(produto => produto.id !== produtoId);
    setProdutos(novosProdutos);
    mapearProdutosParaMatrizes(novosProdutos);
    setProdutoSelecionado(null);
    setModoMovimento(false);
  };

  // Inicializar quando o componente montar
  useEffect(() => {
    const produtosIniciais = simularProdutosBackend();
    mapearProdutosParaMatrizes(produtosIniciais);
  }, []);

  // Atualizar matrizes quando configurações mudarem
  useEffect(() => {
    mapearProdutosParaMatrizes(produtos);
  }, [tamanhoArmazem, tamanhoLoja, capacidadeMaxima]);

  // Função para determinar a cor baseada na porcentagem
  const getCorPorPorcentagem = (porcentagem, ocupada, tipo) => {
    if (!ocupada) return tipo === 'armazem' ? '#f8f9fa' : '#f0f8ff';
    
    if (porcentagem >= 80) return '#ff4444';
    if (porcentagem >= 50) return '#ffaa00';
    if (porcentagem >= 20) return '#44ff44';
    return tipo === 'armazem' ? '#aaffaa' : '#aaddff';
  };

  // Componente de Matriz
  const Matriz = ({ matriz, titulo, tipo }) => {
    return (
      <div className="matriz-section">
        <h3>{titulo} ({matriz.length}x{matriz[0]?.length || 0})</h3>
        <div 
          className={`matriz-grid ${tipo}`}
          style={{
            gridTemplateColumns: `repeat(${matriz[0]?.length || 0}, 1fr)`
          }}
        >
          {matriz.map((linha, indexLinha) =>
            linha.map((celula, indexColuna) => (
              <div
                key={`${tipo}-${indexLinha}-${indexColuna}`}
                className={`celula-estoque ${celula.ocupada ? 'ocupada' : 'vazia'} ${
                  modoMovimento && celula.ocupada && celula.produtoId === produtoSelecionado?.id ? 'selecionada' : ''
                } ${modoMovimento && !celula.ocupada ? 'destino-potencial' : ''}`}
                style={{
                  backgroundColor: getCorPorPorcentagem(celula.porcentagem, celula.ocupada, tipo),
                  border: celula.ocupada ? '2px solid #333' : '2px dashed #ccc',
                  cursor: modoMovimento ? 'pointer' : celula.ocupada ? 'pointer' : 'default'
                }}
                title={
                  celula.ocupada 
                    ? `Produto: ${celula.produto}\nPosição: ${celula.linha},${celula.coluna}\nQuantidade: ${celula.quantidade}\nOcupação: ${celula.porcentagem.toFixed(1)}%`
                    : `Posição: ${celula.linha},${celula.coluna}\nCélula Vazia`
                }
                onClick={() => {
                  if (modoMovimento) {
                    handleCliqueCelula(celula.linha, celula.coluna, tipo);
                  } else if (celula.ocupada) {
                    selecionarProdutoParaMovimento(celula.produtoId, tipo);
                  }
                }}
              >
                <div className="celula-conteudo">
                  <div className="celula-posicao">
                    {celula.linha},{celula.coluna}
                  </div>
                  {celula.ocupada ? (
                    <>
                      <div className="celula-produto">
                        {celula.produto}
                      </div>
                      <div className="celula-quantidade">
                        {celula.quantidade} uni
                      </div>
                      <div className="celula-porcentagem">
                        {celula.porcentagem.toFixed(1)}%
                      </div>
                    </>
                  ) : (
                    <div className="celula-vazia">
                      {modoMovimento ? '↘️ Mover para cá' : 'Vazio'}
                    </div>
                  )}
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    );
  };

  return (
    <div className="estoque-container">
      <h1>Gestão de Estoque - Armazém e Loja</h1>
      
      {/* Modo Movimento */}
      {modoMovimento && produtoSelecionado && (
        <div className="modo-movimento-banner">
          <div className="movimento-info">
            <strong>Modo Movimento:</strong> Movendo {produtoSelecionado.nome} 
            ({produtoSelecionado.quantidade} unidades) de {produtoSelecionado.localizacao === 'armazem' ? 'Armazém' : 'Loja'}
          </div>
          <div className="movimento-acoes">
            <span>Clique em uma célula vazia para mover o produto</span>
            <button onClick={cancelarMovimento} className="btn-cancelar">
              ❌ Cancelar
            </button>
          </div>
        </div>
      )}

      {/* Controles */}
      <div className="controles">
        <div className="controle-grupo">
          <label>Capacidade Máxima:</label>
          <input
            type="number"
            min="1"
            value={capacidadeMaxima}
            onChange={(e) => setCapacidadeMaxima(parseInt(e.target.value) || 500)}
          />
        </div>
        
        <button onClick={adicionarProdutoAleatorio} className="btn-adicionar">
          + Adicionar Produto no Armazém
        </button>

        {produtoSelecionado && !modoMovimento && (
          <div className="controle-selecionado">
            <span>Produto selecionado: {produtoSelecionado.nome}</span>
            <button 
              onClick={() => removerProduto(produtoSelecionado.id)}
              className="btn-remover"
            >
              🗑️ Remover
            </button>
          </div>
        )}
      </div>

      {/* Layout das Matrizes */}
      <div className="matrizes-container">
        <Matriz 
          matriz={matrizArmazem} 
          titulo="🏭 Armazém" 
          tipo="armazem" 
        />
        
        <div className="separador-matrizes">
          <div className="setas-movimento">
            <div>⬅️ Mover para Loja</div>
            <div>➡️ Mover para Armazém</div>
          </div>
        </div>

        <Matriz 
          matriz={matrizLoja} 
          titulo="🏪 Loja" 
          tipo="loja" 
        />
      </div>

      {/* Legenda */}
      <div className="legenda">
        <div className="item-legenda">
          <div className="cor-legenda" style={{backgroundColor: '#f8f9fa'}}></div>
          <span>Armazém Vazio</span>
        </div>
        <div className="item-legenda">
          <div className="cor-legenda" style={{backgroundColor: '#f0f8ff'}}></div>
          <span>Loja Vazia</span>
        </div>
        <div className="item-legenda">
          <div className="cor-legenda" style={{backgroundColor: '#aaffaa'}}></div>
          <span>0-20%</span>
        </div>
        <div className="item-legenda">
          <div className="cor-legenda" style={{backgroundColor: '#44ff44'}}></div>
          <span>20-50%</span>
        </div>
        <div className="item-legenda">
          <div className="cor-legenda" style={{backgroundColor: '#ffaa00'}}></div>
          <span>50-80%</span>
        </div>
        <div className="item-legenda">
          <div className="cor-legenda" style={{backgroundColor: '#ff4444'}}></div>
          <span>80-100%</span>
        </div>
      </div>

      {/* Lista de Produtos */}
      <div className="lista-produtos">
        <h3>Inventário Total ({produtos.length} produtos)</h3>
        <div className="produtos-grid">
          {produtos.map(produto => (
            <div key={produto.id} className={`card-produto ${produto.localizacao}`}>
              <div className="produto-info">
                <strong>{produto.nome}</strong>
                <div>Quantidade: {produto.quantidade} unidades</div>
                <div>
                  Local: {produto.localizacao === 'armazem' ? '🏭 Armazém' : '🏪 Loja'} 
                  - Posição: {produto.posicao.linha},{produto.posicao.coluna}
                </div>
                <div>Ocupação: {((produto.quantidade / capacidadeMaxima) * 100).toFixed(1)}%</div>
              </div>
              <div className="produto-acoes">
                <button 
                  onClick={() => selecionarProdutoParaMovimento(produto.id, produto.localizacao)}
                  className="btn-mover"
                >
                  📦 Mover
                </button>
                <button 
                  onClick={() => removerProduto(produto.id)}
                  className="btn-remover"
                >
                  🗑️
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Informações */}
      <div className="informacoes">
        <p>
          <strong>Como usar:</strong> Clique em um produto para selecioná-lo, depois clique em "Mover" 
          e selecione uma célula vazia na outra matriz para transferir o produto.
        </p>
        <p>
          <strong>Capacidade por célula:</strong> {capacidadeMaxima} unidades | 
          <strong> Armazém:</strong> {tamanhoArmazem.linhas}×{tamanhoArmazem.colunas} | 
          <strong> Loja:</strong> {tamanhoLoja.linhas}×{tamanhoLoja.colunas}
        </p>
      </div>
    </div>
  );
};

export default EstoqueVisualizacao;