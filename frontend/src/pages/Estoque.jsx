import React, { useState, useEffect } from 'react';

const EstoqueVisualizacao = () => {
  // Estados para as matrizes
  const [matrizArmazem, setMatrizArmazem] = useState([]);
  const [matrizLoja, setMatrizLoja] = useState([]);
  const [produtos, setProdutos] = useState([]);
  const [produtoSelecionado, setProdutoSelecionado] = useState(null);
  const [modoMovimento, setModoMovimento] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Configurações (agora vindo do backend)
  const [tamanhoArmazem, setTamanhoArmazem] = useState({ linhas: 5, colunas: 5 });
  const [tamanhoLoja, setTamanhoLoja] = useState({ linhas: 3, colunas: 3 });
  const [capacidadeMaxima, setCapacidadeMaxima] = useState(500);

  // Função para buscar dados completos do backend
  const buscarDadosBackend = async () => {
    try {
      setLoading(true);
      setError(null);
      
      console.log('🔍 Buscando dados do backend...');
      
      const token = localStorage.getItem('token');
      if (!token) {
        throw new Error('Usuário não autenticado');
      }

      const response = await fetch('http://localhost:5000/api/estoque/visualizacao', {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      });
      
      if (!response.ok) {
        if (response.status === 401) {
          throw new Error('Sessão expirada. Faça login novamente.');
        }
        throw new Error(`Erro HTTP: ${response.status}`);
      }
      
      const dadosBackend = await response.json();
      console.log('✅ Dados recebidos do backend:', dadosBackend);
      
      // Atualizar estados com dados do backend
      setMatrizArmazem(dadosBackend.matrizArmazem || []);
      setMatrizLoja(dadosBackend.matrizLoja || []);
      setProdutos(dadosBackend.produtos || []);
      setTamanhoArmazem(dadosBackend.tamanhoArmazem || { linhas: 5, colunas: 5 });
      setTamanhoLoja(dadosBackend.tamanhoLoja || { linhas: 3, colunas: 3 });
      setCapacidadeMaxima(dadosBackend.capacidadeMaxima || 500);
      
      return dadosBackend;
      
    } catch (error) {
      console.error('❌ Erro ao buscar dados do backend:', error);
      setError(error.message);
      return null;
    } finally {
      setLoading(false);
    }
  };

  // Função para mover produto no backend
  const moverProdutoBackend = async (idItem, novaPosX, novaPosY, novoLocal) => {
    try {
      const token = localStorage.getItem('token');
      if (!token) {
        throw new Error('Usuário não autenticado');
      }

      const response = await fetch('http://localhost:5000/api/estoque/mover', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          id_item: idItem,
          novo_pos_x: novaPosX,
          novo_pos_y: novaPosY,
          novo_local: novoLocal
        })
      });
      
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || 'Erro ao mover produto');
      }
      
      const resultado = await response.json();
      console.log('✅ Produto movido com sucesso:', resultado);
      
      // Recarregar dados após mover
      await buscarDadosBackend();
      return true;
      
    } catch (error) {
      console.error('❌ Erro ao mover produto:', error);
      alert(`Erro ao mover produto: ${error.message}`);
      return false;
    }
  };

  // Função para remover produto no backend
  const removerProdutoBackend = async (idItem) => {
    try {
      const token = localStorage.getItem('token');
      if (!token) {
        throw new Error('Usuário não autenticado');
      }

      const response = await fetch(`http://localhost:5000/api/estoque/remover/${idItem}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      });
      
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || 'Erro ao remover produto');
      }
      
      const resultado = await response.json();
      console.log('✅ Produto removido com sucesso:', resultado);
      
      // Recarregar dados após remover
      await buscarDadosBackend();
      return true;
      
    } catch (error) {
      console.error('❌ Erro ao remover produto:', error);
      alert(`Erro ao remover produto: ${error.message}`);
      return false;
    }
  };

  // Função para selecionar produto para movimento
  const selecionarProdutoParaMovimento = (produtoId, localizacaoAtual) => {
    // Encontrar o item correto baseado no produtoId e localização
    let itemEncontrado = null;
    
    // Buscar nas matrizes
    const todasCelulas = [...matrizArmazem.flat(), ...matrizLoja.flat()];
    const celula = todasCelulas.find(cel => 
      cel.ocupada && cel.produtoId === produtoId && cel.local === localizacaoAtual
    );
    
    if (celula) {
      itemEncontrado = {
        id: celula.produtoId,
        nome: celula.produto,
        quantidade: celula.quantidade,
        localizacao: celula.local,
        posicao: { linha: celula.linha, coluna: celula.coluna },
        // Precisamos do ID do item (não do produto) para a movimentação
        itemId: celula.id || produtoId // Usar ID da célula se disponível
      };
    }
    
    if (itemEncontrado) {
      setProdutoSelecionado(itemEncontrado);
      setModoMovimento(true);
      console.log('📦 Produto selecionado para movimento:', itemEncontrado);
    } else {
      console.error('❌ Produto não encontrado para movimento:', { produtoId, localizacaoAtual });
    }
  };

  // Função para cancelar movimento
  const cancelarMovimento = () => {
    setProdutoSelecionado(null);
    setModoMovimento(false);
  };

  // Função para lidar com clique na célula (quando em modo movimento)
  const handleCliqueCelula = async (linha, coluna, tipoMatriz) => {
    if (!modoMovimento || !produtoSelecionado) return;

    // Não permitir mover para o mesmo local
    if (tipoMatriz === produtoSelecionado.localizacao) {
      alert('Selecione uma célula no outro local (Armazém ↔ Loja)');
      return;
    }

    // Verificar se a célula de destino está vazia
    const matrizDestino = tipoMatriz === 'armazem' ? matrizArmazem : matrizLoja;
    
    if (matrizDestino[linha] && matrizDestino[linha][coluna] && matrizDestino[linha][coluna].ocupada) {
      alert('Célula de destino já está ocupada!');
      return;
    }

    console.log('🚚 Movendo produto:', {
      de: produtoSelecionado.localizacao,
      para: tipoMatriz,
      posicao: { linha, coluna },
      produto: produtoSelecionado
    });

    // Mover o produto no backend
    const sucesso = await moverProdutoBackend(
      produtoSelecionado.itemId || produtoSelecionado.id,
      linha,
      coluna,
      tipoMatriz
    );

    if (sucesso) {
      setProdutoSelecionado(null);
      setModoMovimento(false);
    }
  };

  // Função para remover produto
  const removerProduto = async (produtoId) => {
    if (!window.confirm('Tem certeza que deseja remover este produto?')) {
      return;
    }

    console.log('🗑️ Removendo produto:', produtoId);
    
    // Encontrar o ID do item (não do produto)
    let itemId = produtoId;
    
    // Buscar nas matrizes para encontrar o ID correto do item
    const todasCelulas = [...matrizArmazem.flat(), ...matrizLoja.flat()];
    const celula = todasCelulas.find(cel => 
      cel.ocupada && cel.produtoId === produtoId
    );
    
    if (celula && celula.id) {
      itemId = celula.id;
    }

    const sucesso = await removerProdutoBackend(itemId);
    
    if (sucesso) {
      setProdutoSelecionado(null);
      setModoMovimento(false);
    }
  };

  // Carregar dados do backend quando o componente montar
  useEffect(() => {
    buscarDadosBackend();
  }, []);

  // Função para recarregar dados
  const recarregarDados = async () => {
    await buscarDadosBackend();
  };

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
    if (!matriz || matriz.length === 0) {
      return (
        <div className="matriz-section">
          <h3>{titulo}</h3>
          <div className="matriz-vazia">Carregando...</div>
        </div>
      );
    }

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

  // Estados de loading e error
  if (loading) {
    return (
      <div className="estoque-container">
        <div className="loading-estoque">
          <h1>Gestão de Estoque - Armazém e Loja</h1>
          <div className="spinner-container">
            <div className="spinner"></div>
            <p>Carregando dados do estoque...</p>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="estoque-container">
        <h1>Gestão de Estoque - Armazém e Loja</h1>
        <div className="error-container">
          <h3>❌ Erro ao carregar dados</h3>
          <p>{error}</p>
          <button onClick={recarregarDados} className="btn-recarregar">
            🔄 Tentar Novamente
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="estoque-container">
      <div className="header-com-botoes">
        <h1>Gestão de Estoque - Armazém e Loja</h1>
        <button onClick={recarregarDados} className="btn-recarregar">
          🔄 Atualizar Dados
        </button>
      </div>
      
      {/* Modo Movimento */}
      {modoMovimento && produtoSelecionado && (
        <div className="modo-movimento-banner">
          <div className="movimento-info">
            <strong>Modo Movimento:</strong> Movendo {produtoSelecionado.nome} 
            ({produtoSelecionado.quantidade} unidades) de {produtoSelecionado.localizacao === 'armazem' ? 'Armazém' : 'Loja'}
          </div>
          <div className="movimento-acoes">
            <span>Clique em uma célula vazia no {produtoSelecionado.localizacao === 'armazem' ? 'Loja' : 'Armazém'} para mover o produto</span>
            <button onClick={cancelarMovimento} className="btn-cancelar">
              ❌ Cancelar
            </button>
          </div>
        </div>
      )}

      {/* Controles */}
      <div className="controles">
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
                  {produto.posicao && ` - Posição: ${produto.posicao.linha},${produto.posicao.coluna}`}
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
        <p className="backend-info">
          <strong>🔗 Conectado ao Backend:</strong> Dados em tempo real do banco de dados
        </p>
      </div>
    </div>
  );
};

export default EstoqueVisualizacao;