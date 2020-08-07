*********************************************
Uma Aplicação de Blog feita em flask
*********************************************

|pyversion|

Criando ambiente virtual
########################

Após o download da aplicação, dentro da pasta do projeto, é necessário instalar um ambiente virtual de desenvolvimento,
para isso é necessário instalar os módulos ``pip`` e ``virtualenv``. Em seguida, execute::

$ python -m virtualenv venv

Após isso ative o ambiente virtual (no linux)::

$ source venv/bin/activate

Isso irá configurar um ambiente de desenvolvimento isolado do seu sistema, em seguida
vamos instalar os pacotes necessários para a aplicação::

$ pip install -r requeriments.txt

Com isso, tudo necessário para a aplicação rodar já instara instalado.

Configuração
###################
Variáveis de ambiente
**********************

A aplicação contém algumas variáveis de ambiente para
configuração, que são:

:FLASK_APP: arquivo que inicia o flask, o valor padrão é 'microblog.py'

:DATABASE_URL: URL de conexão com o banco
:SECRET_KEY: configura a chave para a aplicação
:SQLALCHEMY_TRACK_MODIFICATIONS [Opcional]: ativa o rastreamento de operações no banco
:SQLALCHEMY_ECHO [Opcional]: ativa o log de operações do banco de dados
:MAIL_SERVER: servidor SMTP
:MAIL_PORT: porta SMTP
:MAIL_USE_TLS: Usa TLS na conexão de email
:MAIL_USERNAME: Usuário de email
:MAIL_PASSWORD: Senha do email
:ADMINS: Lista de emails do administrador
:ELASTICSEARCH_URL [Opcional]: URL do servidor ElasticSearch
:REDIS_URL [Opcional]: URL de servidor Redis

Essas variáveis são lidas de um arquivo ``.flaskenv`` na raíz do projeto.

Configurar traduções
*************************

As linguagens aceitas pelo sistema deve ser configurado no arquivo ``config.py``, especificando-se uma lista de linguagens
a serem aceitas nas requisições para gerar as traduções, conforme o exemplo:

.. code-block::

    LANGUAGES = ['pt', 'en']

Para configurar as traduções basta seguir os seguintes passos:

1º - Iniciar o ``flask babel``::


$ flask translate init linguagem_escolhida


2º - Cria o arquivo de tradução e atualiza quando necessário::

$ flask translate update

3º - Compila os arquivos de tradução::

$ flask translate compile

Configurar Banco de dados
***************************

Após definir as variáveis de ambiente, você deve escolher um banco de dados suportado pela aplicação [SQLite | MySql | PostgreSql],
o banco usado por padrão será sempre o SQLite, portanto se faz necessário possuir ele instalado no sistema, caso não se deseje configurar
outro banco de dados relacional.

Para configurar a migração e os scripts de banco de dados, siga os seguintes passos:

1º Cria um novo repositório de migração::

$ flask db init

2º Gera os scripts de migração::

$ flask db migrate

3º Cria as tabelas especificadas nos arquivos de migração::

$ flask db upgrade

Configurar Redis e RQ task queue
************************************

Para utilizar o redis junto com o task queue RQ, primeiro configure a variáel de
ambiente REDIS_URL, depois inicie o servidor redis::

$ redis-server

Após o servidor estar iniciado, é necessário iniciar a task queue::

$ rq worker personalblog_tasks

Configurar para o uso de Full Text Search com ElasticSearch
*************************************************************

Para fazer uso de um servidor ``ElasticSearch`` basta configurar
a variável de ambiente ``ELASTICSEARCH_URL``, após isso o sistema estará apto a fazer consultas.


Iniciar a aplicação
################################

Depois de configurado e com o ambiente virtual ativado, basta rodar o comando::

$ flask run




.. |pyversion| image:: https://img.shields.io/badge/python-3-green
    :alt: Supported Python versions.
    :target: https://www.python.org/download/releases/3.0/