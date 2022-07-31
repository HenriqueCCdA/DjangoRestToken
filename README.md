# API-DRF

Uma API simples para o cadastro de usuario em um banco de dados. Os campos requiridos para o cadastro são:

* email (username)
* password
* name
* phone
* institution
* role

O email foi utilizado como **username** portanto foi criado um usuário costumizado do Django.

Neste projeto foi usa do **Django Rest Framework (DFR)** como framework web para a construção da API. para os teste automáticos foi utilizado o framework **pytest**.

---

## 1) Rota de cadastro

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

## 2) Rota de login
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
## 3) Rota para um recurso protegido
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


## 4) Configurando o projeto
---

### 4.1) Criando virtualenv ambiente de produção

```console
python -m venv .venv --upgrade-deps
source .venv/bin/activate
pip install -r requirements.txt
```

### 4.2) Instalando depência de produção

```console
pip install -r requirements.txt
```

### 4.3) Instalando depência de desenvolvimento

```console
pip install -r requirements.txt requirements-dev.txt
```

### 4.4) Criando ambiente de desenvolvimento com pip-tools

```console
pip-sync requirements.txt requirements-dev.txt
```

### 4.5) Rodando os teste

```console
pytest -vv
```