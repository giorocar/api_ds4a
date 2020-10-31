from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/<int:valor1>,<int:valor2>')
def dummy_api(valor1:int, valor2:int):
    return jsonify(date="suma "+str(valor1+valor2))

if __name__ == '__main__':
    app.run()
