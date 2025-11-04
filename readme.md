# Como rodar?

## Backend
* Dentro da pasta backend, rodar o comando pip install -r requirements.txt para instalar as dependencias necessárias (Flask, Flask-CORS)
* Ainda dentro da pasta backend rode o comando python3 src/main.py para subir o servidor no endereço http://localhost:5000

## Fronted
* Instalar o node.js e o npm: https://docs.npmjs.com/downloading-and-installing-node-js-and-npm
* Dentro da pasta frontend, rodar o comando npm install para instalar as dependencias necessárias
* Ainda dentro da pasta frontend rode o comando npm run dev para subir o cliente no endereço http://localhost:5173

# Como testar ?

Os testes podem ser feitos tanto pelo frontend quanto através da ferramenta Bruno (https://www.usebruno.com/) que permite a interação direta com o backend através de requisições HTTP. Para fazer os testes via Bruno você deve baixar a aplicação e importar a pasta backend/collection/UFMG-POO-TRABALHO-1 para dentro dele para carregar as configurações do projeto (no menu superior selecione Collection > Open collections > Selecione a pasta backend/collection/UFMG-POO-TRABALHO-1). Antes de inicar os testes você também deve configuar as variáveis de ambiente no Bruno, para isso basta clicar em "No environments" no canto superior direito e selecionar "test-env" para usar as variávies que preparamos para os testes. Após esses passos, o Bruno estára configurado para a realização dos testes.

Para facilitar os testes pré criamos algumas entidade no banco de dados. Caso queira recriá-las basta excluir o aquivo backend/resources/bancodedados.db.

Criamos um usuário de cada tipo para facilitar o teste das funcionalidade:

**Gerente**
Usuario: 12345678901
Senha: 123456

**Caixa**
Usuario: 12345678902
Senha: 123456

**Repositor**
Usuario: 12345678903
Senha: 123456