# Gerenciador de Tarefas - **To Do List**

Este é um aplicativo de gerenciador de tarefas desenvolvido com **Django** e outras tecnologias modernas para a gestão de tarefas diárias. O objetivo deste aplicativo é permitir que os usuários se registrem, se autentiquem, criem, editem e excluam suas tarefas de forma prática.

---

## **Sumário**

- [Instruções de Instalação](#instruções-de-instalação)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Rotas e Endpoints](#rotas-e-endpoints)
- [Como Usar](#como-usar)
- [To Do List de Funcionalidades](#to-do-list-de-funcionalidades)

---

### **Instruções de Instalação**

Para rodar a aplicação localmente, siga os seguintes passos:

1. **Clone o repositório**:
   ```bash
   git clone https://github.com/seu-usuario/nome-do-repositorio.git
   cd nome-do-repositorio
Crie e ative um ambiente virtual (recomendado): Para sistemas Unix (Linux/macOS):

bash
Copiar código
python3 -m venv venv
source venv/bin/activate
Para Windows:

bash
Copiar código
python -m venv venv
venv\Scripts\activate
Instale as dependências do projeto:

bash
Copiar código
pip install -r requirements.txt
Configure o banco de dados: Se estiver usando MySQL (como recomendado):

Instale o MySQL no seu sistema e crie um banco de dados com o nome da sua escolha.
No arquivo settings.py, configure a conexão com o banco MySQL.
Exemplo de configuração:

python
Copiar código
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'nome_do_banco',
        'USER': 'usuario',
        'PASSWORD': 'senha',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
Realize as migrações do banco de dados:

bash
Copiar código
python manage.py migrate
Crie um superusuário (opcional):

bash
Copiar código
python manage.py createsuperuser
Inicie o servidor de desenvolvimento:

bash
Copiar código
python manage.py runserver
A aplicação estará disponível em http://127.0.0.1:8000.

Tecnologias Utilizadas
Django: O framework principal utilizado para construir a aplicação. O Django é ideal para esse tipo de aplicação, pois é robusto, seguro e rápido para desenvolvimento de back-end. Ele inclui funcionalidades como autenticação de usuários, ORM (Object-Relational Mapping) para interagir com bancos de dados, entre outros.

MariaDB: Sistema de gerenciamento de banco de dados relacional. Utilizado para armazenar as tarefas, usuários e outras informações da aplicação. O MariaDB foi escolhido devido à sua confiabilidade, escalabilidade e compatibilidade com Django.

Redis : Utilizado para melhorar o desempenho da aplicação, armazenando dados temporários (como sessões ou cache). Ele pode ser configurado para otimizar o uso de recursos em uma aplicação de larga escala.

Certbot & Nginx: Para configuração do HTTPS e proxy reverso, garantindo que a aplicação seja segura e tenha uma comunicação criptografada com os usuários.

Gunicorn: Servidor WSGI para Python, utilizado para rodar a aplicação Django em produção. O Gunicorn trabalha muito bem com o Nginx, que atua como proxy reverso.

Rotas e Endpoints
A seguir, estão listados os principais endpoints e suas funções na aplicação:

Autenticação de Usuário
POST /api/token/ - Login e geração de tokens JWT:

Body:
json
Copiar código
{
  "username": "user1",
  "password": "password123"
}
Resposta (caso sucesso):
json
Copiar código
{
  "access": "access_token",
  "refresh": "refresh_token"
}
POST /api/token/refresh/ - Renova o token de acesso com um token de atualização:

Body:
json
Copiar código
{
  "refresh": "refresh_token"
}
Resposta:
json
Copiar código
{
  "access": "new_access_token"
}
Gerenciamento de Tarefas
GET /tasks/ - Lista todas as tarefas do usuário autenticado:

Resposta:
json
Copiar código
[
  {
    "id": 1,
    "title": "Tarefa 1",
    "description": "Descrição da tarefa",
    "created_at": "2024-12-09T10:00:00Z",
    "completed": false
  }
]
POST /tasks/ - Cria uma nova tarefa:

Body:
json
Copiar código
{
  "title": "Nova Tarefa",
  "description": "Descrição da tarefa"
}
Resposta:
json
Copiar código
{
  "id": 2,
  "title": "Nova Tarefa",
  "description": "Descrição da tarefa",
  "created_at": "2024-12-09T12:00:00Z",
  "completed": false
}
PUT /tasks/{id}/ - Atualiza uma tarefa existente:

Body:
json
Copiar código
{
  "title": "Tarefa Atualizada",
  "description": "Descrição atualizada",
  "completed": true
}
DELETE /tasks/{id}/ - Deleta uma tarefa:

Resposta: 204 No Content (sem corpo)
Como Usar
Após o deploy ou execução local, o usuário pode acessar a plataforma no endereço configurado.
O cadastro de usuário é feito na página de registro, e o login é feito com o uso de tokens JWT.
Após o login, o usuário pode acessar o painel de tarefas, onde pode criar, editar, visualizar e excluir suas tarefas.
To Do List de Funcionalidades
A seguir, a lista das funcionalidades a serem implementadas ou que estão em desenvolvimento:

Cadastro de Usuário: O usuário pode criar uma conta para gerenciar suas tarefas.
Login via JWT: O usuário faz login com credenciais, e um token de autenticação é gerado para sessões subsequentes.
Gerenciamento de Tarefas: O usuário pode criar, editar, listar e excluir tarefas.
Marcar Tarefa como Concluída: O usuário pode marcar tarefas como concluídas.
Filtro de Tarefas: Exibir tarefas com base no status (pendente ou concluída).
Notificações: Notificação quando uma tarefa for criada ou alterada.
Conclusão
Este gerenciador de tarefas foi desenvolvido para fornecer uma interface simples e intuitiva, utilizando Django para o backend, MySQL como banco de dados e JWT para a autenticação do usuário. Ele permite ao usuário gerenciar suas tarefas de forma eficiente, com autenticação segura e escalabilidade futura com Redis.
