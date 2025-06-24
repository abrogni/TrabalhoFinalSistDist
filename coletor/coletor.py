from flask import Flask, request, jsonify, render_template_string
import time

app = Flask(__name__)
leituras = []  # Lista para armazenar as últimas leituras

@app.route("/leitura", methods=["POST"])
def receber_leitura():
    dados = request.json
    agora = time.strftime("%H:%M:%S")
    print(f"[{agora}] Leitura recebida: {dados}")
    
    dados["timestamp"] = agora
    leituras.append(dados)

    # Mantém só as 20 últimas
    if len(leituras) > 20:
        leituras.pop(0)

    return {"status": "ok"}

@app.route("/dados")
def dados():
    return jsonify(leituras)

@app.route("/painel")
def painel():
    return render_template_string("""
<!DOCTYPE html>
<html>
<head>
    <title>Painel de Sensores</title>
    <meta charset="UTF-8">
    <style>
        body { font-family: Arial; padding: 20px; background: #f4f4f4; }
        table { border-collapse: collapse; width: 100%; background: white; }
        th, td { border: 1px solid #ccc; padding: 8px; text-align: center; }
        th { background-color: #007BFF; color: white; }
    </style>
</head>
<body>
    <h1>Painel de Leituras dos Sensores</h1>
    <table id="tabela">
        <thead>
            <tr>
                <th>Horário</th>
                <th>Sensor ID</th>
                <th>Temperatura (°C)</th>
                <th>Umidade (%)</th>
            </tr>
        </thead>
        <tbody></tbody>
    </table>

    <script>
        async function carregarDados() {
            const res = await fetch("/dados");
            const dados = await res.json();
            const tbody = document.querySelector("#tabela tbody");
            tbody.innerHTML = "";
            dados.reverse().forEach(l => {
                const linha = `<tr>
                    <td>${l.timestamp}</td>
                    <td>${l.sensor_id}</td>
                    <td>${l.temperatura}</td>
                    <td>${l.umidade}</td>
                </tr>`;
                tbody.innerHTML += linha;
            });
        }

        setInterval(carregarDados, 2000);
        carregarDados();
    </script>
</body>
</html>
    """)

app.run(host="0.0.0.0", port=5000)
