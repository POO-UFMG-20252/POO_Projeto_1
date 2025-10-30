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

  const tiposFuncionario = [
    { value: '', label: 'Selecione o tipo' },
    { value: 'CLT', label: 'CLT' },
    { value: 'PJ', label: 'PJ' },
    { value: 'Estagiário', label: 'Estagiário' },
    { value: 'Freelancer', label: 'Freelancer' }
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
    
    // Aqui você pode implementar a validação completa do CPF
    // Por simplicidade, vou retornar true para CPFs com 11 dígitos
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

  const handleSubmit = (e) => {
    e.preventDefault();
    
    const formErrors = validateForm();
    
    if (Object.keys(formErrors).length === 0) {
      // Formulário válido - aqui você pode enviar os dados para a API
      console.log('Dados do funcionário:', formData);
      setSubmitted(true);
      
      // Limpa o formulário após 3 segundos
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
          <button type="submit" className="submit-btn">
            Cadastrar Funcionário
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
          >
            Limpar Campos
          </button>
        </div>
      </form>
    </div>
  );
};

export default CadastroFuncionario;