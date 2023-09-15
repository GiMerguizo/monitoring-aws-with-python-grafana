import boto3
import datetime
from flask import Flask, jsonify

# Configurações da aws
session = boto3.Session(
    aws_access_key_id='',
    aws_secret_access_key='',
    region_name=''
)

ce_client = session.client('ce')

start_date = datetime.datetime(2023, 1, 1)
end_date = datetime.datetime(2023, 8, 17)

metric = 'BlendedCost'

response = ce_client.get_cost_and_usage(
    TimePeriod={
        'Start': start_date.strftime('%Y-%m-%d'),
        'End': end_date.strftime('%Y-%m-%d')
    },
    Granularity='MONTHLY',
    Metrics=[metric]
)

print(response)

app = Flask(__name__)

@app.route('/explorer')
def cost():
    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
