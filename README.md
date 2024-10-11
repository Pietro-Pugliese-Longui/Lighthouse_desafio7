# Indicium Airflow Hands-on Tutorial

## Requisitos

O desafio foi realizado no sistema operacional Linux Mint;
É necessário ter o [Docker engine](https://docs.docker.com/engine/install/ubuntu/);
Clonar o repositório.

## Preparando o ambiente

Agora para fazer com que o Airflow funcione com o docker é necessário exportar algumas variáveis de ambiente primeiramente o id:

```bash
export AIRFLOW_UID=$(id -u)
```
Agora precisa exportar o grupo do docker no usuário do airflow, para isto utilize o comando:

```bash
getent group docker
```
Este comando retornará um número, decore este número.

Agora você deve adicionar este número na linha 54 do arquivo docker-compose.yaml clonado e salvar o arquivo.

Com isto o airflow deve funcionar normalmente.

## Airflow

Para rodar o Airflow deve utilizar o comando dentro do diretório do arquivo docker-compose.yaml:

```bash
docker compose up
```
Após um tempo deve ser possível acessar o airflow no url localhost:8080, o usuário é airflow e a senha é airflow. 

Agora na aba Admin/variables é necessário criar uma variável com o nome my_email e o valor ser seu e-mail da indicium.

Por fim basta executar a DAG DesafioAirflow, os arquivos requiridos estarão na pasta data após a DAG ser executada. 