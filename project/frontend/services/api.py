import urllib.request
import urllib.error
import json
import logging
import os

logger = logging.getLogger(__name__)

API_BASE = os.getenv("API_BASE_URL", "http://localhost:5000")


def _request(method: str, path: str, data: dict = None) -> dict:
    url = f"{API_BASE}{path}"
    body = json.dumps(data).encode() if data else None
    headers = {"Content-Type": "application/json", "Accept": "application/json"}

    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        try:
            return json.loads(body)
        except Exception:
            return {"error": f"HTTP {e.code}: {body}"}
    except Exception as e:
        logger.error(f"Erro na requisição {method} {url}: {e}")
        return {"error": str(e)}


def get_metrics():
    return _request("GET", "/dashboard/metrics")

def get_critical(limite=15):
    return _request("GET", f"/dashboard/critical?limite={limite}")

def listar_convenios(status=None, empresa=None, tipo=None):
    params = []
    if status:
        params.append(f"status={urllib.parse.quote(status)}")
    if empresa:
        params.append(f"empresa={urllib.parse.quote(empresa)}")
    if tipo:
        params.append(f"tipo={urllib.parse.quote(tipo)}")
    qs = "?" + "&".join(params) if params else ""
    return _request("GET", f"/convenios{qs}")

def buscar_convenio(cid: int):
    return _request("GET", f"/convenios/{cid}")

def criar_convenio(data: dict):
    return _request("POST", "/convenios", data)

def atualizar_convenio(cid: int, data: dict):
    return _request("PUT", f"/convenios/{cid}", data)

def deletar_convenio(cid: int):
    return _request("DELETE", f"/convenios/{cid}")

def executar_monitoramento():
    return _request("POST", "/monitoramento/run")

def get_logs_monitoramento(n=10):
    return _request("GET", f"/monitoramento/logs?n={n}")

def health_check():
    return _request("GET", "/health")

import urllib.parse
