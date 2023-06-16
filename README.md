# reward-yourself-back
## Requerimentos:

* Python 3.8
* Poetry 1.5.1
* MySQL 8.0.33-0

## Configuração de ambiente

Primeiramente, é necessário criar um banco vazio no MySQL(Sugestão de nome: `reward_yourself`). 
Após criar o banco, crie um arquivo python chamado `local_settings` na pasta `/reward_yourself` do projeto.
Esse arquivo será o que irá conter as variáveis de ambiente do sistema. Copie e cole as seguintes variáveis neste arquivo, substituindo os valores entre `<>` para os valores que você possui.
```python
DEBUG = True
SECRET_KEY = "<Sua SECRET_KEY>"

SITE_URL = "http://127.0.0.1:8000"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '<Nome do banco criado>',
        'USER': '<Seu usuário de acesso ao MySQL>',
        'PASSWORD': '<Sua senha de acesso ao MySQL>',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```
Após isso, na raiz do projeto, rode o seguinte comando para criar o virtual environment:
```shell
poetry install
```
Com isso, o Poetry irá instalar todos os pacotes necessários para rodar o projeto. Neste momento é necessário rodar as migrações para a criação das tabelas e relacionamentos do banco. Para isso, rode o seguinte comando:
```shell
poetry run python manage.py migrate
```
Para criar um usuário administrador, rode o seguinte comando:
```shell
poetry run python manage.py loaddata user_admin
```
O usuário terá as seguintes credenciais:
* **username:** admin
* **password:** qwert123
* **email:** admin@admin.com

Assim, o ambiente estará devidamento configurado. Para subir o sistema, rode o seguinte comando:
```shell
poetry run python manage.py runserver
```
Com isso, o sistema estará rodando na seguinte URL: http://127.0.0.1:8000 \
Para acessar o Django admin, onde poderá visualizar os objetos do banco e, também, será possível modifica-los manualmente, basta acessar, logando com o usuário criado anteriormente, a URL: [127.0.0.1:8000/admin/](127.0.0.1:8000/admin/).