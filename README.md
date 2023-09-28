# MVP 03 - Project HomeBroker 

Projeto de uma aplicação responsavel por comprar e vender ações.

---

## Componente C: Orders Service
 + Executa ordens de compra e venda de ações;
 + Registra o histórico de transações dos usuários para acompanhamento e análise.
 

---
### Execução através do Docker

Certifique-se de ter o [Docker](https://docs.docker.com/engine/install/) 
instalado e em execução em sua máquina.

Navegue até o diretório que contém o Dockerfile e o requirements.txt no terminal.
Execute **como administrador** o seguinte comando para construir a imagem Docker:


```
docker build -t orders-service .
```

Caso nao esteja criada, execute o comando abaixo, para a criação de uma nova
network:

```
docker network create <my_network> 
```

Para a execução o container basta executar, **como administrador**, seguinte o comando:

```
docker run -p 5000:5000 --name orders-service --network <my_network> orders-service
```
