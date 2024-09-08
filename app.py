# Executar comando a baixo
# pip install redis flask

# Rodar projeto com o seguinte comando
# redis-server

# Rodar arquivo .py

# Realizar testes no Postman na url http://127.0.0.1:5000/ testando os métodos abaixo

from flask import Flask, request, jsonify
import redis

# Conectar ao Redis
client = redis.Redis(host='localhost', port=6379, db=0)

app = Flask(__name__)

# Rota para adicionar uma pessoa à fila
@app.route('/add', methods=['POST'])
def add_person():
    data = request.json
    nome = data.get('nome')
    numero = data.get('numero')
    
    client.rpush('fila_ingressos', f'{numero}: {nome}')
    return jsonify({"message": "Pessoa adicionada à fila"}), 201

# Rota para exibir a fila atual
@app.route('/exibir', methods=['GET'])
def show_queue():
    fila = client.lrange('fila_ingressos', 0, -1)
    # Decodifica bytes para string
    fila = [pessoa.decode('utf-8') for pessoa in fila]
    return jsonify({"fila": fila}), 200

# Rota para remover a primeira pessoa da fila
@app.route('/remover', methods=['DELETE'])
def remove_person():
    pessoa = client.lpop('fila_ingressos')
    if pessoa:
        return jsonify({"removido": pessoa.decode('utf-8')}), 200
    else:
        return jsonify({"message": "Fila vazia"}), 404

if __name__ == '__main__':
    app.run(debug=True)
