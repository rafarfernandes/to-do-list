To-Do List - Django Project
Visão Geral
Este é um aplicativo de gerenciamento de tarefas (To-Do List) desenvolvido com o Framework Django. Permite que os usuários criem, atualizem e excluam tarefas de forma intuitiva. 

Índice
Instruções de Instalação
Documentação das Rotas/Endpoints
Tecnologias Utilizadas


Instruções de Instalação
Siga os passos abaixo para configurar e executar o projeto localmente:

Pré-requisitos
Python 3.8 ou superior
Git
Ambiente virtual (recomendado: venv)
Gerenciador de pacotes pip
Passo a Passo
Clone o repositório

bash
Copiar código
git clone <URL_DO_REPOSITORIO>
cd to-do-list
Crie e ative o ambiente virtual

bash
Copiar código
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
Instale as dependências

bash
Copiar código
pip install -r requirements.txt
Configure as variáveis de ambiente
Crie um arquivo .env na raiz do projeto e defina as configurações necessárias. Exemplo:

env
Copiar código
DEBUG=True
SECRET_KEY=sua-chave-secreta
Execute as migrações do banco de dados

bash
Copiar código
python manage.py migrate
Inicie o servidor de desenvolvimento

bash
Copiar código
python manage.py runserver
Acesse o aplicativo
Abra o navegador 

Documentação das Rotas/Endpoints
Rotas Públicas
Método	Endpoint	Descrição
GET	/	Página inicial
GET	/login/	Página de login
GET	/register/	Página de registro
Rotas Protegidas
Método	Endpoint	Descrição
GET	/tasks/	Lista de todas as tarefas do usuário
POST	/tasks/add/	Criação de uma nova tarefa
GET	/tasks/<id>/	Visualiza os detalhes de uma tarefa
PUT	/tasks/<id>/	Atualiza os dados de uma tarefa
DELETE	/tasks/<id>/	Exclui uma tarefa
Tecnologias Utilizadas
Backend: Django 4.2
Escolhi Django devido à sua robustez, facilidade para trabalhar com modelos ORM e recursos nativos para autenticação e administração.

Frontend: HTML, Bootstrap 5 e um pouco de CSS
Utilizado para estilizar a interface do usuário com responsividade e consistência.

Banco de Dados: MYSQL 
Por ser um banco de dados leve e prático, foi escolhido para simplificar o ambiente de desenvolvimento.

Outros:

dotenv para gerenciamento de variáveis de ambiente.
gunicorn (em produção).


Autenticação de Usuário
Para proteger os dados dos usuários e permitir experiências personalizadas.

CRUD com ORM
Operações de Create, Read, Update e Delete foram implementadas para gerenciar as tarefas.

Organização de Código
Utilizei boas práticas, como separação de responsabilidades em views, templates e URLs.