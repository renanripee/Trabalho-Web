# 🎫 Sistema de Eventos - Trabalho Web

Este é um sistema de gerenciamento de eventos desenvolvido com **Django** como parte do trabalho da disciplina de Desenvolvimento Web.

## 🧰 Tecnologias Utilizadas

- Python 3.10+
- Django 4.x
- SQLite (padrão)
- Bootstrap 5
- HTML/CSS/JS

## 🚀 Como rodar o projeto

### 1. Clone o repositório

```bash
git clone https://github.com/renanripee/Trabalho-Web.git
cd Trabalho-Web
```

### 2. Crie e ative um ambiente virtual

```bash
python -m venv venv
# No Windows:
venv\Scripts\activate
# No Linux/Mac:
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
# Caso não exista, rode:
pip install django
```

### 4. Rode as migrações
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Inicie o servidor de desenvolvimento
```bash
python manage.py runserver
```

Por fim, acesse o projeto em http://localhost:8000

## 👥 Tipos de usuários

- admin — pode gerenciar usuários e eventos
- criador — pode criar eventos e ver inscritos
- normal — pode se inscrever em eventos

## 🗂️ Estrutura do projeto

- usuarios/ — app responsável pelos usuários e autenticação
- eventos/ — app responsável pelos eventos e inscrições
- templates/ — HTMLs com base no Bootstrap
- static/ — arquivos estáticos (CSS, JS, imagens)

## ✅ Funcionalidades

- Login e cadastro de usuários com três tipos distintos
- Criação, edição e exclusão de eventos
- Inscrição de usuários em eventos
- Visualização de inscritos por criadores

## 📝 Licença
Este projeto é acadêmico e sem fins lucrativos.

