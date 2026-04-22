import requests
from requests.auth import HTTPBasicAuth
import json
import os
from datetime import datetime

# Configurações via Variáveis de Ambiente (Secrets do GitHub)
URL = "https://primeup.atlassian.net/rest/api/3/issue/MEC-15/worklog"
EMAIL = os.getenv("JIRA_EMAIL")
TOKEN = os.getenv("JIRA_TOKEN")

def log_work():
    # Verifica se é fim de semana (0=Segunda, 5=Sábado, 6=Domingo)
    if datetime.now().weekday() >= 5:
        print("Fim de semana. Pulando lançamento.")
        return

    auth = HTTPBasicAuth(EMAIL, TOKEN)
    headers = {"Accept": "application/json", "Content-Type": "application/json"}

    # Formata a data atual para o padrão Jira
    now = datetime.now().strftime("%Y-%m-%dT09:00:00.000+0000")

    payload = json.dumps({
        "timeSpentSeconds": 32400, # 9 horas
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

    response = requests.post(URL, data=payload, headers=headers, auth=auth)

    if response.status_code == 201:
        print(f"Sucesso! Horas lançadas para {now}")
    else:
        print(f"Erro {response.status_code}: {response.text}")

if __name__ == "__main__":
    log_work()
