# Monitorando a AWS com Python e Grafana
Pegando métricas da AWS usando scripts em Python e fazendo-os de fonte de dados para monitoramento no Grafana

# Dados AWS com Python
Exemplos de Scripts em Python para coletar dados de alguns serviços da AWS

## Serviços
- Cost Explorer (Billing)
- Monitoring Code Storage (Lambda)

## Requisitos
- Ter uma instância EC2 rodando:
    - Python
    - Grafana
    - Docker
    - Portas abertas: 
        - 3000:3000
        - 8080:8080

## Etapas
- Verificar as versões do python e pip
```
python --version ou python3 --version
pip --version ou pip3 --version
```
- Instalar o Flask e o boto3 <br>
```
pip install flask
pip install boto3
```

- Criar um arquivo python para rodar (`aplicacao.py`)

- Configurar a aws cli
`aws configure`

- Rodar o script <br>
`python3 aplicacao.py`

### Transformar o script em uma imagem Docker
- Criar um Dockerfile
    ```
    FROM python:3.9.17-alpine
    RUN pip install boto3
    RUN pip install flask
    COPY aplicacao.py /aplicacao.py
    CMD ["python3","aplicacao.py"]
    ```
- Construir a imagem: `docker image build -t python-scripts .`

- Rodar o container: `docker run --name=python -p 8080:8080 -d python-scripts`

- (Opcional) Fazer um docker-compose
```
python:
    image: python-scripts
    container_name: scripts-py
    ports:
      - '8080:8080'
```

### Grafana
- Configurar uma nova conexão no Grafana <br>
Home > Connections > Add new connection > JSON API > Create a JSON API data source
    - Save & Test


## Criando uma api em Python
- Criar uma conta no site: https://replit.com/~


## Referências
:link: [Como Criar API com Python - Crie a Sua Própria API no Python](https://youtu.be/WWVEymSt1iI) <br>
:link: [Monitoring Lambda code storage](https://docs.aws.amazon.com/pt_br/lambda/latest/operatorguide/code-storage.html) <br>
:link: [Best practices for managing code storage
](https://docs.aws.amazon.com/pt_br/lambda/latest/operatorguide/code-storage-best-practice.html) <br>
:link: [Docker: Criando a Docker Image com o Python e Flask](https://ebasso.net/wiki/index.php?title=Docker:_Criando_a_Docker_Image_com_o_Python_e_Flask)
