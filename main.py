from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

resultados = []

HTML = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Bot Bac Bo Analisador</title>

<style>
body {
    font-family: Arial, sans-serif;
    background: #111827;
    color: white;
    margin: 0;
    padding: 20px;
}

.container {
    max-width: 500px;
    margin: auto;
}

h1 {
    text-align: center;
}

.card {
    background: #1f2937;
    border-radius: 15px;
    padding: 20px;
    margin-top: 15px;
}

button {
    width: 31%;
    padding: 16px 5px;
    border: none;
    border-radius: 12px;
    color: white;
    font-size: 16px;
    font-weight: bold;
    cursor: pointer;
}

.azul {
    background: #1976d2;
}

.vermelho {
    background: #dc2626;
}

.empate {
    background: #6b7280;
}

.resultado {
    font-size: 18px;
    margin: 10px 0;
}

.barra {
    height: 12px;
    background: #374151;
    border-radius: 10px;
    overflow: hidden;
}

.preenchimento {
    height: 100%;
}

.azul-barra {
    background: #2196f3;
}

.vermelho-barra {
    background: #ef4444;
}

.empate-barra {
    background: #9ca3af;
}

.historico {
    display: flex;
    flex-wrap: wrap;
    gap: 7px;
}

.bolinha {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
}

.limpar {
    width: 100%;
    margin-top: 15px;
    background: #374151;
}
</style>
</head>

<body>

<div class="container">

<h1>🎲 Bac Bo Analisador</h1>

<div class="card">

<h3>Registrar resultado</h3>

<button class="azul" onclick="registrar('azul')">
🔵 Azul
</button>

<button class="vermelho" onclick="registrar('vermelho')">
🔴 Vermelho
</button>

<button class="empate" onclick="registrar('empate')">
⚪ Empate
</button>

</div>

<div class="card">

<h3>📊 Estatísticas</h3>

<div class="resultado">
🔵 Azul: <span id="azul">0</span>%
</div>
<div class="barra">
<div id="barraAzul" class="preenchimento azul-barra" style="width:0%"></div>
</div>

<br>

<div class="resultado">
🔴 Vermelho: <span id="vermelho">0</span>%
</div>
<div class="barra">
<div id="barraVermelho" class="preenchimento vermelho-barra" style="width:0%"></div>
</div>

<br>

<div class="resultado">
⚪ Empate: <span id="empate">0</span>%
</div>
<div class="barra">
<div id="barraEmpate" class="preenchimento empate-barra" style="width:0%"></div>
</div>

<p>Total de resultados: <span id="total">0</span></p>

</div>

<div class="card">

<h3>📋 Últimos resultados</h3>

<div id="historico" class="historico"></div>

</div>

<div class="card">

<h3>📌 Leitura do histórico</h3>

<p id="leitura">
Registre alguns resultados para começar a análise.
</p>

</div>

<div class="card">

<button class="limpar" onclick="limpar()">
🗑️ Limpar histórico
</button>

</div>

</div>

<script>

async function registrar(cor) {

    await fetch('/registrar', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            resultado: cor
        })
    });

    atualizar();
}

async function atualizar() {

    const resposta = await fetch('/dados');
    const dados = await resposta.json();

    document.getElementById('azul').innerText = dados.porcentagens.azul;
    document.getElementById('vermelho').innerText = dados.porcentagens.vermelho;
    document.getElementById('empate').innerText = dados.porcentagens.empate;

    document.getElementById('barraAzul').style.width =
        dados.porcentagens.azul + '%';

    document.getElementById('barraVermelho').style.width =
        dados.porcentagens.vermelho + '%';

    document.getElementById('barraEmpate').style.width =
        dados.porcentagens.empate + '%';

    document.getElementById('total').innerText = dados.total;

    const historico = document.getElementById('historico');
    historico.innerHTML = '';

    dados.ultimos.forEach(cor => {

        const bolinha = document.createElement('div');

        bolinha.className = 'bolinha';

        if (cor === 'azul') {
            bolinha.style.background = '#1976d2';
            bolinha.innerText = 'A';
        }

        if (cor === 'vermelho') {
            bolinha.style.background = '#dc2626';
            bolinha.innerText = 'V';
        }

        if (cor === 'empate') {
            bolinha.style.background = '#6b7280';
            bolinha.innerText = 'E';
        }

        historico.appendChild(bolinha);
    });

    document.getElementById('leitura').innerText =
        dados.leitura;
}

async function limpar() {

    if (!confirm('Deseja apagar todo o histórico?')) {
        return;
    }

    await fetch('/limpar', {
        method: 'POST'
    });

    atualizar();
}

atualizar();

</script>

</body>
</html>
"""


@app.route("/")
def inicio():
    return render_template_string(HTML)


@app.route("/registrar", methods=["POST"])
def registrar():

    dados = request.get_json(silent=True) or {}
    resultado = dados.get("resultado")

    if resultado not in ["azul", "vermelho", "empate"]:
        return jsonify({"erro": "Resultado inválido"}), 400

    resultados.append(resultado)

    return jsonify({"ok": True})


@app.route("/dados")
def dados():

    total = len(resultados)

    azul = resultados.count("azul")
    vermelho = resultados.count("vermelho")
    empate = resultados.count("empate")

    if total > 0:
        p_azul = round((azul / total) * 100, 1)
        p_vermelho = round((vermelho / total) * 100, 1)
        p_empate = round((empate / total) * 100, 1)
    else:
        p_azul = 0
        p_vermelho = 0
        p_empate = 0

    if total < 5:
        leitura = "Poucos resultados registrados. Continue registrando para ter um histórico maior."

    else:
        maior = max(
            [("Azul", p_azul), ("Vermelho", p_vermelho), ("Empate", p_empate)],
            key=lambda x: x[1]
        )

        leitura = (
            f"No histórico registrado, {maior[0]} aparece com "
            f"{maior[1]}%. Isso descreve apenas o histórico e "
            f"não garante o próximo resultado."
        )

    return jsonify({
        "total": total,
        "porcentagens": {
            "azul": p_azul,
            "vermelho": p_vermelho,
            "empate": p_empate
        },
        "ultimos": resultados[-20:],
        "leitura": leitura
    })


@app.route("/limpar", methods=["POST"])
def limpar():

    resultados.clear()

    return jsonify({"ok": True})


if __name__ == "__main__":
    import os

    porta = int(os.environ.get("PORT", 10000))

    app.run(
        host="0.0.0.0",
        port=porta
    )
