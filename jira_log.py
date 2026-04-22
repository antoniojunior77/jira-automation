import requests
from requests.auth import HTTPBasicAuth
import json
import os
from datetime import datetime

# Configurações
URL = "https://primeup.atlassian.net/rest/api/3/issue/MEC-15/worklog"
EMAIL = os.getenv("JIRA_EMAIL")
TOKEN = os.getenv("JIRA_TOKEN")

def log_work():
    # Verifica fim de semana
    if datetime.now().weekday() >= 5:
        print("Fim de semana. Pulando.")
        return

    auth = HTTPBasicAuth(EMAIL, TOKEN)
    headers = {"Accept": "application/json", "Content-Type": "application/json"}

    # Ajustado para 09:00 da manhã no fuso de Brasília (-0300)
    now = datetime.now().strftime("%Y-%m-%dT09:00:00.000-0300")

    payload = json.dumps({
        "timeSpentSeconds": 32400, # 9h
        "comment": {
            "type": "doc",
            "version": 1,
            "content": [
                {
                    "type": "paragraph",
                    "content": [{"text": "Demandas MEC - Atividades de sustentação e arquitetura.", "type": "text"}]
                }
            ]
        },
        "started": now
    })

    print(f"Tentando lançar para a data: {now}")
    response = requests.post(URL, data=payload, headers=headers, auth=auth)

    if response.status_code == 201:
        print(f"Sucesso! Status 201 - Horas gravadas no Jira.")
    else:
        print(f"Erro {response.status_code}!")
        print(f"Resposta do Servidor: {response.text}")

if __name__ == "__main__":
    log_work()
