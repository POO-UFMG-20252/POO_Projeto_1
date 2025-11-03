import React, { useState } from 'react';

const CadastroFuncionario = () => {
  const [formData, setFormData] = useState({
    nome: '',
    cpf: '',
    email: '',
    dataNascimento: '',
    salario: '',
    tipoFuncionario: ''
  });

  const [errors, setErrors] = useState({});
  const [submitted, setSubmitted] = useState(false);
  const [loading, setLoading] = useState(false);

  const tiposFuncionario = [
    { value: '', label: 'Selecione o tipo' },
    { value: 'Gerente', label: 'Gerente' },
    { value: 'Caixa', label: 'Caixa' },
    { value: 'Repositor', label: 'Repositor' },
  ];

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prevState => ({
      ...prevState,
      [name]: value
    }));
    
    // Limpa o erro do campo quando o usuário começa a digitar
    if (errors[name]) {
      setErrors(prevState => ({
        ...prevState,
        [name]: ''
      }));
    }
  };

  const validateForm = () => {
    const newErrors = {};

    // Validação do nome
    if (!formData.nome.trim()) {
      newErrors.nome = 'Nome é obrigatório';
    } else if (formData.nome.trim().length < 2) {
      newErrors.nome = 'Nome deve ter pelo menos 2 caracteres';
    }

    // Validação do CPF
    if (!formData.cpf.trim()) {
      newErrors.cpf = 'CPF é obrigatório';
    } else if (!validarCPF(formData.cpf)) {
      newErrors.cpf = 'CPF inválido';
    }

    // Validação do email
    if (!formData.email.trim()) {
      newErrors.email = 'Email é obrigatório';
    } else if (!validarEmail(formData.email)) {
      newErrors.email = 'Email inválido';
    }

    // Validação da data de nascimento
    if (!formData.dataNascimento) {
      newErrors.dataNascimento = 'Data de nascimento é obrigatória';
    } else if (!validarDataNascimento(formData.dataNascimento)) {
      newErrors.dataNascimento = 'Funcionário deve ter pelo menos 18 anos';
    }

    // Validação do salário
    if (!formData.salario) {
      newErrors.salario = 'Salário é obrigatório';
    } else if (parseFloat(formData.salario) <= 0) {
      newErrors.salario = 'Salário deve ser maior que zero';
    }

    // Validação do tipo de funcionário
    if (!formData.tipoFuncionario) {
      newErrors.tipoFuncionario = 'Tipo de funcionário é obrigatório';
    }

    return newErrors;
  };

  const validarCPF = (cpf) => {
    // Remove caracteres não numéricos
    cpf = cpf.replace(/[^\d]/g, '');
    
    // Verifica se tem 11 dígitos
    if (cpf.length !== 11) return false;
    
    // Verifica se todos os dígitos são iguais
    if (/^(\d)\1+$/.test(cpf)) return false;
    
    return true;
  };

  const validarEmail = (email) => {
    const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return regex.test(email);
  };

  const validarDataNascimento = (data) => {
    const dataNascimento = new Date(data);
    const hoje = new Date();
    const idade = hoje.getFullYear() - dataNascimento.getFullYear();
    const mes = hoje.getMonth() - dataNascimento.getMonth();
    
    if (mes < 0 || (mes === 0 && hoje.getDate() < dataNascimento.getDate())) {
      return idade - 1 >= 18;
    }
    return idade >= 18;
  };

  const formatarCPF = (value) => {
    // Remove tudo que não é dígito
    const cpf = value.replace(/\D/g, '');
    
    // Aplica a formatação do CPF
    if (cpf.length <= 3) return cpf;
    if (cpf.length <= 6) return `${cpf.slice(0, 3)}.${cpf.slice(3)}`;
    if (cpf.length <= 9) return `${cpf.slice(0, 3)}.${cpf.slice(3, 6)}.${cpf.slice(6)}`;
    return `${cpf.slice(0, 3)}.${cpf.slice(3, 6)}.${cpf.slice(6, 9)}-${cpf.slice(9, 11)}`;
  };

  const handleCPFChange = (e) => {
    const formattedCPF = formatarCPF(e.target.value);
    setFormData(prevState => ({
      ...prevState,
      cpf: formattedCPF
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    const formErrors = validateForm();
    
    if (Object.keys(formErrors).length === 0) {
      setLoading(true);
      
      try {
        // Preparar dados para a API
        const dadosParaAPI = {
          nome: formData.nome.trim(),
          cpf: formData.cpf.replace(/\D/g, ''), // Remove formatação
          email: formData.email.trim(),
          data_nascimento: formData.dataNascimento,
          salario: parseFloat(formData.salario),
          tipo: formData.tipoFuncionario
        };

        console.log('Enviando dados para API:', dadosParaAPI);

        // Fazer requisição para a API
        const response = await fetch('http://localhost:5000/funcionarios', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(dadosParaAPI)
        });

        const data = await response.json();

        if (!response.ok) {
          throw new Error(data.message || 'Erro ao cadastrar funcionário');
        }

        console.log('Resposta da API:', data);
        setSubmitted(true);
        
        setTimeout(() => {
          setFormData({
            nome: '',
            cpf: '',
            email: '',
            dataNascimento: '',
            salario: '',
            tipoFuncionario: ''
          });
          setSubmitted(false);
        }, 3000);

      } catch (error) {
        console.error('Erro ao cadastrar funcionário:', error);
        setErrors({ submit: error.message });
      } finally {
        setLoading(false);
      }
    } else {
      setErrors(formErrors);
    }
  };

  return (
    <div className="cadastro-container">
      <div className="cadastro-header">
        <h1>Cadastro de Funcionário</h1>
        <p>Preencha os dados abaixo para cadastrar um novo funcionário</p>
      </div>

      {submitted && (
        <div className="success-message">
          ✅ Funcionário cadastrado com sucesso!
        </div>
      )}

      {errors.submit && (
        <div className="error-message-global">
          ❌ {errors.submit}
        </div>
      )}

      <form onSubmit={handleSubmit} className="cadastro-form">
        <div className="form-row">
          <div className="form-group">
            <label htmlFor="nome">Nome Completo *</label>
            <input
              type="text"
              id="nome"
              name="nome"
              value={formData.nome}
              onChange={handleChange}
              className={errors.nome ? 'error' : ''}
              placeholder="Digite o nome completo"
              disabled={loading}
            />
            {errors.nome && <span className="error-message">{errors.nome}</span>}
          </div>

          <div className="form-group">
            <label htmlFor="cpf">CPF *</label>
            <input
              type="text"
              id="cpf"
              name="cpf"
              value={formData.cpf}
              onChange={handleCPFChange}
              className={errors.cpf ? 'error' : ''}
              placeholder="000.000.000-00"
              maxLength="14"
              disabled={loading}
            />
            {errors.cpf && <span className="error-message">{errors.cpf}</span>}
          </div>
        </div>

        <div className="form-row">
          <div className="form-group">
            <label htmlFor="email">Email *</label>
            <input
              type="email"
              id="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              className={errors.email ? 'error' : ''}
              placeholder="exemplo@empresa.com"
              disabled={loading}
            />
            {errors.email && <span className="error-message">{errors.email}</span>}
          </div>

          <div className="form-group">
            <label htmlFor="dataNascimento">Data de Nascimento *</label>
            <input
              type="date"
              id="dataNascimento"
              name="dataNascimento"
              value={formData.dataNascimento}
              onChange={handleChange}
              className={errors.dataNascimento ? 'error' : ''}
              disabled={loading}
            />
            {errors.dataNascimento && <span className="error-message">{errors.dataNascimento}</span>}
          </div>
        </div>

        <div className="form-row">
          <div className="form-group">
            <label htmlFor="salario">Salário *</label>
            <input
              type="number"
              id="salario"
              name="salario"
              value={formData.salario}
              onChange={handleChange}
              className={errors.salario ? 'error' : ''}
              placeholder="0.00"
              step="0.01"
              min="0"
              disabled={loading}
            />
            {errors.salario && <span className="error-message">{errors.salario}</span>}
          </div>

          <div className="form-group">
            <label htmlFor="tipoFuncionario">Tipo de Funcionário *</label>
            <select
              id="tipoFuncionario"
              name="tipoFuncionario"
              value={formData.tipoFuncionario}
              onChange={handleChange}
              className={errors.tipoFuncionario ? 'error' : ''}
              disabled={loading}
            >
              {tiposFuncionario.map((tipo) => (
                <option key={tipo.value} value={tipo.value}>
                  {tipo.label}
                </option>
              ))}
            </select>
            {errors.tipoFuncionario && <span className="error-message">{errors.tipoFuncionario}</span>}
          </div>
        </div>

        <div className="form-actions">
          <button 
            type="submit" 
            className="submit-btn"
            disabled={loading}
          >
            {loading ? 'Cadastrando...' : 'Cadastrar Funcionário'}
          </button>
          <button 
            type="button" 
            className="clear-btn"
            onClick={() => {
              setFormData({
                nome: '',
                cpf: '',
                email: '',
                dataNascimento: '',
                salario: '',
                tipoFuncionario: ''
              });
              setErrors({});
            }}
            disabled={loading}
          >
            Limpar Campos
          </button>
        </div>
      </form>

      <style jsx>{`
        .cadastro-container {
          max-width: 800px;
          margin: 0 auto;
          padding: 20px;
        }
        
        .cadastro-header {
          text-align: center;
          margin-bottom: 30px;
        }
        
        .cadastro-header h1 {
          color: #333;
          margin-bottom: 10px;
        }
        
        .cadastro-header p {
          color: #666;
        }
        
        .success-message {
          background-color: #d4edda;
          color: #155724;
          padding: 12px;
          border-radius: 4px;
          margin-bottom: 20px;
          text-align: center;
          font-weight: bold;
        }
        
        .error-message-global {
          background-color: #f8d7da;
          color: #721c24;
          padding: 12px;
          border-radius: 4px;
          margin-bottom: 20px;
          text-align: center;
          font-weight: bold;
        }
        
        .cadastro-form {
          background: white;
          padding: 30px;
          border-radius: 8px;
          box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        
        .form-row {
          display: flex;
          gap: 20px;
          margin-bottom: 20px;
        }
        
        .form-group {
          flex: 1;
          display: flex;
          flex-direction: column;
        }
        
        label {
          margin-bottom: 5px;
          font-weight: 600;
          color: #333;
        }
        
        input, select {
          padding: 10px;
          border: 1px solid #ddd;
          border-radius: 4px;
          font-size: 14px;
        }
        
        input.error, select.error {
          border-color: #dc3545;
        }
        
        .error-message {
          color: #dc3545;
          font-size: 12px;
          margin-top: 5px;
        }
        
        .form-actions {
          display: flex;
          gap: 15px;
          justify-content: flex-end;
          margin-top: 30px;
        }
        
        .submit-btn {
          background-color: #007bff;
          color: white;
          border: none;
          padding: 12px 30px;
          border-radius: 4px;
          cursor: pointer;
          font-weight: 600;
        }
        
        .submit-btn:disabled {
          background-color: #6c757d;
          cursor: not-allowed;
        }
        
        .submit-btn:hover:not(:disabled) {
          background-color: #0056b3;
        }
        
        .clear-btn {
          background-color: #6c757d;
          color: white;
          border: none;
          padding: 12px 20px;
          border-radius: 4px;
          cursor: pointer;
        }
        
        .clear-btn:hover:not(:disabled) {
          background-color: #545b62;
        }
        
        @media (max-width: 768px) {
          .form-row {
            flex-direction: column;
            gap: 15px;
          }
        }
      `}</style>
    </div>
  );
};

export default CadastroFuncionario;