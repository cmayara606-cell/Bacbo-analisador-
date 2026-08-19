import os
from flask import Flask, request

app = Flask(__name__)

resultados = []

@app.route("/")
def inicio():
    return "Bot Bac Bo analisador online!"

@app.route("/webhook", methods=["POST"])
def webhook():
    dados = request.get_json(silent=True) or {}

    mensagem = dados.get("message", {})
    texto = mensagem.get("text", "").lower().strip()

    if texto in ["azul", "🔵"]:
        resultados.append("azul")
    elif texto in ["vermelho", "🔴"]:
        resultados.append("vermelho")
    elif texto in ["empate", "⚪"]:
        resultados.append("empate")
    elif texto == "/start":
        return "OK"

    return "OK"

@app.route("/status")
def status():
    total = len(resultados)

    if total == 0:
        return "Nenhum resultado registrado ainda."

    azul = resultados.count("azul")
    vermelho = resultados.count("vermelho")
    empate = resultados.count("empate")

    def porcentagem(valor):
        return round((valor / total) * 100, 1)

    ultimos = resultados[-10:]

    return (
        f"Total: {total}\n"
        f"🔵 Azul: {azul} ({porcentagem(azul)}%)\n"
        f"🔴 Vermelho: {vermelho} ({porcentagem(vermelho)}%)\n"
        f"⚪ Empate: {empate} ({porcentagem(empate)}%)\n\n"
        f"Últimos 10: {', '.join(ultimos)}"
    )

if __name__ == "__main__":
    porta = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=porta)
