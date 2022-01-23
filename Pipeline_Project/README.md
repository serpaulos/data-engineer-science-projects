# Projeto para Pipeline de Dados
### **# projeto em andamento**

> Projeto sugerido pela https://stacktecnologias.com.br/ para por em pratica alguns conceitos em Data Engineer. No projeto apresentado a equipe, compostas por: <br>
> - Engenheiro de dados (minha parte no projeto)
> - Analista de dados
> - Gerente de Projeto
> - Cientista de Dados

## Tabela de Conteudos
- [Informações Gerais](#Informações-Gerais)
- [Tecnologias](#Tecnologias)
- [Status do Projeto](#Status-do-Projeto)
- [Melhorias](#melhorias)
- [Reconhecimentos](#Reconhecimentos)
- [Contato](#Contato)
<!-- * [License](#license) -->


## Informações-Gerais 
- Foi utilizado o conjunto de Dados: https://www.kaggle.com/olistbr/brazilian-ecommerce
- O projeto trata da empresa brasileira de E-Commerce Olist. Uma startup brasileira que atua no segmento de e-commerce.
- O desafio assumido pela equipe foi de desenhar um algoritimo em Machine Learning para Previsão de Vendas
- Estou destacando neste documento a parte executada para o pipeline de dados e tarefas inerentes ao Engenheiro de Dados.

## Tecnologias
- Python
- Pandas
- Airflow
- Docker (Docker compose)
- Minio(S3)
- Mysql

## Status-do-Projeto
Project is: _em desenvolivimento_

# Detalhes-do-Projeto

* Containers criados para o projeto utilizando Docker-compose
    * Airflow(e dependencias)
    * Mysql
    * Spark
    * Jupyter-notebook
    * Minio

* Estrutura das pastas utilizadas no projeto
    * Airflow
        * dags (pasta onde são armazenadas as dags do airflow)
        * config (pasta para o arquivo airflow.cfg para configurações)
        * data (para utlizada para manipulação de dados)
        * logs (arquivos de log)
        * plugins (possiveis plugins utlizados no airflow)
        * parquet_saved (para utlizada para manipulação de dados)
        * parquet_read (para utlizada para manipulação de dados)
        * temp (para utlizada para manipulação de dados)
    * Data_files
        * data (pasta para armazenar dados de fontes diversas fora do datalake, como csv, json, etc. Para testes diversos) 
        * dbs (pasta para armazenamento de arquivos relacionados com banco de dados como script de carga e criação de banco de dados)
    * Datalake (onde serão salvos/replicados os buckets criados dentro do minio)
    * Mysql-db (criada para salvar/persistir os dados do database na maquina(host docker) para não perder dados caso o container seja deletado ou tenha problema)
    * Notebook (pasta para salvar os arquivos notebook do Jupyter criados para teste de conceito antes da implementação/automação no airflow)
    * Postgres-data (criada para salvar/persistir os dados do database na maquina(host docker) para não perder dados caso o container seja deletado ou tenha problema)

- Script desenhado para criação da estrutura de pastas
    * CriaPastas.bat (script para criação da estrutura de pastas, a pasta raiz para o projeto será stack_project)
- Buckets criados no datalake MINIO para processamento
    * Landing
    * Processing
    * Curated

- Arquivos csv feito upload para bucket Landing utilizando script python
    * olist_customers_dataset.csv
    * olist_geolocation_dataset.csv
    * olist_order_items_dataset.csv
    * olist_order_payments_dataset.csv
    * olist_order_reviews_dataset.csv
    * olist_orders_dataset.csv
    * olist_products_dataset.csv
    * olist_sellers_dataset.csv
    * product_category_name_translation.csv

- Sequencia de processamento no jupyter notebook
    * Executar os seguintes notebooks em order:
        * move_files_to_bucket_landing.ipynb
        * python_csv_to_parket.ipynb

- Sequencia de processamento no airflow
    * Executar os seguintes notebooks em order:
        * carrega_dados_landing.py
        * converte_csv_para_parquet.py

## Melhorias
Projeto ainda em desenvolivimento e como ainda estou aprendendo a utilizar diversas tecnologias, ainda tenho muito o que aprender e ainda existe muito espaço para melhorias.


## Reconhecimentos
- Este projeto foi sugerido por (https://stacktecnologias.com.br/)
- Muito obrigado ao [@RodrigoSantana](https://www.linkedin.com/in/rodrigo-santana-ferreira-0ab041128/) e ao [@FelipeSantana](https://www.linkedin.com/in/felipesf/) por proporcionar este desafio ;)


## Contato
Criado por [@paulosilvajr](https://www.linkedin.com/in/paulosilvajr/) - fique a vontade para entrar em contato!