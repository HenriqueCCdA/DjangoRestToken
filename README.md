# API-DRF

Uma API simples para o cadastro de usuario em um banco de dados. Os campos requeridos para o cadastro são:

* email (username)
* password
* name
* phone
* institution
* role

O email foi utilizado como **username** portanto foi criado um usuário costumizado do Django.

Neste projeto foi usa do **Django Rest Framework (DFR)** como framework web para a construção da API. para os teste automáticos foi utilizado o framework **pytest**.

---

# Index

  - [1) Rotas](#1-rotas)
    - [1.1) Rota de cadastro](#11-rota-de-cadastro)
    - [1.2) Rota de login](#12-rota-de-login)
    - [1.3) Rota para um recurso protegido](#13-rota-para-um-recurso-protegido)
  - [2) Subindo o servidor](#2-subindo-o-servidor)
    - [2.1) setup inicial](#21-setup-inicial)
    - [2.2) Rodando o servido](#22-rodando-o-servido)
  - [3) Desenvolvimento](#3-desenvolvimento)
    - [3.1) Instalando dependencias de desenvolvimento](#31-instalando-dependencias-de-desenvolvimento)
    - [3.2) Rodando os teste](#32-rodando-os-teste)
  - [4) Banco de dados](#4-banco-de-dados)
    - [4.1) Usando o postgres via docker:](#41-usando-o-postgres-via-docker)

---

## 1) Rotas
---
### 1.1) Rota de cadastro

---

>* endpoint http://127.0.0.1:8000/api/v2/registrar/ - POST
>
> Rota para registrar um usuario via o método post. Caso o **payload** seja valido e o usuario não exista esta rota ira salvar usuario e gera o **token**. O **email** foi usado como **username**.
>
> Exemplo de Requisição:

```json
{
    "email":"test1@email.com",
    "password1":"123456!!",
    "password2":"123456!!",
    "name":"test1",
    "phone":"1111111",
    "institution":"UFRJ",
    "role":"Medico"
}
```

> Reposta:

```json
{
    "id": 3,
    "email": "test1@email.com",
    "token": "0308fd7c9ad2ae6ad277525d223db69a4889a702",
    "name": "test1",
    "phone": "1111111",
    "institution": "UFRJ",
    "role": "Medico"
}
```
> Exemplo de requisição usando **curl**

```bash
curl --request POST \
  --url http://127.0.0.1:8000/api/v2/registrar/ \
  --header 'Content-Type: application/json' \
  --data '{
    "email":"test1@email.com",
    "password1":"123456!!",
    "password2":"123456!!",
    "name":"test1",
    "phone":"1111111",
    "institution":"UFRJ",
    "role":"Medico"
  }'
```

---


### 1.2) Rota de login

---

> * http://127.0.0.1:8000/api/v2/login/ - POST
>
> Rota serve para obter o token de um usuario cadastrado. Caso o **payload** seja valido será retornado o **token**.
>
> Exemplo de Requisição:

```json
{
    "username":"test1@email.com",
    "password":"123456!!",
}
```

> Reposta:

```json
{
    "token": "0308fd7c9ad2ae6ad277525d223db69a4889a702",
}
```

> Exemplo de requisição usando **curl**

```bash
curl --request POST \
  --url http://127.0.0.1:8000/api/v2/login/ \
  --header 'Content-Type: application/json' \
  --data '{
	"username": "test1@email.com",
	"password": "123456!!"
}'
```

---


### 1.3) Rota para um recurso protegido

---

>  http://127.0.0.1:8000/api/v2/view_protefida/ - GET
>
> Rota serve para testar um rota protegida. Para acessar os recursos dessa rotar é preciso passar um **token** no cabeçalho da requisição.
>
> Exemplo de requisição usando **curl**

```bash
curl --request GET \
  --url http://127.0.0.1:8000/api/v2/view_protegida/ \
  --header 'Authorization: Token 0308fd7c9ad2ae6ad277525d223db69a4889a702' \
  --header 'Content-Type: application/json'
```

---

## 2) Subindo o servidor
---

### 2.1) setup inicial
---
Instalação inicial, necessário fazer apenas uma vez.

```console
python -m venv .venv --upgrade-deps
source .venv/bin/activate
pip install -r requirements.txt
cp contrib/env-sample .env
```

Para usar o `sqlite` o arquivo `.env` fica assim:

```
DEBUG=false
SECRET_KEY=Sua chave secreta
ALLOWED_HOSTS=localhost, 127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

Para usar o `postgres` o arquivo `.env` fica assim:

```
DEBUG=false
SECRET_KEY=Sua chave secreta
ALLOWED_HOSTS=localhost, 127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
DATABASE_URL=postgres://seu_user_db:seu_password_db@localhost:5432/seu_db
```

Agora pode-se fazer a migração com:

```console
python manage.py migrate
```

---

### 2.2) Rodando o servido

---

```console
python manage.py runserver
```

---

### 3) Desenvolvimento

---

### 3.1) Instalando dependencias de desenvolvimento

---

```console
pip-sync requirements.txt requirements-dev.txt
```

---

### 3.2) Rodando os teste

---

```console
pytest -vv
```

---

## 4) Banco de dados

---

### 4.1) Usando o postgres via docker

---

Subir o container

```consolse
docker-compose -f docker-compose.yml up -d
```

Configurar `DATABASE_URL` no arquivo `.env` para

```
postgres://api:apirest@localhost:5434/api
```
---
