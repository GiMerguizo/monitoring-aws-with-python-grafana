import boto3
import datetime
from flask import Flask, jsonify

# Configurar o cliente do AWS Lambda

session = boto3.Session(
    aws_access_key_id='',
    aws_secret_access_key='',
    region_name=''
)

# Configurações clientes aws
lambda_client = session.client('lambda')
ce_client = session.client('ce')

app = Flask(__name__)

# Inicializar a variável para armazenar o tamanho total do armazenamento de código
total_code_size_bytes = total_code_size = 0
total_functions = 0

# Iterar sobre cada função Lambda e somar o tamanho do armazenamento de código
def get_page_code_size(page):
    global total_code_size_bytes
    global total_functions

    for function in page['Functions']:
        function_name = function['FunctionName']

        versions_response = lambda_client.list_versions_by_function(FunctionName=function_name)

        for version in versions_response['Versions']:
            code_size = function['CodeSize']
            total_code_size_bytes += code_size

        total_functions += 1
        # print(f"Função: {function_name}, Tamanho do Código: {code_size} bytes")

paginas = lambda_client.get_paginator('list_functions')
for page in paginas.paginate():
    get_page_code_size(page)

# Exibir o tamanho total do armazenamento de código de todas as funções
total_code_size = total_code_size_bytes / (1024 ** 3)
print(f"Tamanho Total do Armazenamento de Código: {total_code_size:.2f} GB")
print(f"Total de Funções: {total_functions}")

# Dicionário para as infomrções
resposta = {'total_functions': total_functions, 'total_armazenamento': total_code_size}

# Código para pegar as métricas do cost explorer
start_date = datetime.datetime(2023, 1, 1)
end_date = datetime.datetime(2023, 8, 31)

start_date_latest = datetime.datetime(2023, 8, 1)
end_date_latest = datetime.datetime(2023, 8, 31)

metric = 'BlendedCost'

response = ce_client.get_cost_and_usage(
    TimePeriod={
        'Start': start_date.strftime('%Y-%m-%d'),
        'End': end_date.strftime('%Y-%m-%d')
    },
    Granularity='MONTHLY',
    Metrics=[metric]
)

response_tag_costcenter = ce_client.get_cost_and_usage(
    TimePeriod={
        'Start': start_date_latest.strftime('%Y-%m-%d'),
        'End': end_date_latest.strftime('%Y-%m-%d')
    },
    Granularity='MONTHLY',
    Metrics=[metric],
    GroupBy=[
        {
            'Type': 'TAG',
            'Key': 'cost-center',
        },
    ],
)

response_tag_costproject = ce_client.get_cost_and_usage(
    TimePeriod={
        'Start': start_date_latest.strftime('%Y-%m-%d'),
        'End': end_date_latest.strftime('%Y-%m-%d')
    },
    Granularity='MONTHLY',
    Metrics=[metric],
    GroupBy=[
        {
            'Type': 'TAG',
            'Key': 'cost-project',
        },
    ],
)

# Iniciando o Flask
@app.route('/')
def homepage():
    return 'A API está no ar'

@app.route('/storage')
def storage():
    return jsonify(resposta)

@app.route('/explorer')
def explorer():
    return jsonify(response)

@app.route('/explorer/cost-project')
def cost_project():
    return jsonify(response_tag_costproject)

@app.route('/explorer/cost-center')
def cost_center():
    return jsonify(response_tag_costcenter)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9091)