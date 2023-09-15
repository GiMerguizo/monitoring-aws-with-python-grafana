import boto3

# Configurar o cliente do AWS Lambda
session = boto3.Session(
    aws_access_key_id='',
    aws_secret_access_key='',
    region_name=''
)

lambda_client = session.client('lambda')

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

print(resposta)
