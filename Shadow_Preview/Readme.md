# Shadow Preview

Il nous avait été donnée un lien github vers le repository du challenge. [shadow preview](https://github.com/Darylabrador/CTF-Challs)

En lisant les fichiers notamment `entripoint.sh` :
```bash
#!/bin/sh
set -eu

SERVICE="${SERVICE:-all}"

start_proxy() {
  mkdir -p /tmp/nginx/client_body /tmp/nginx/proxy /tmp/nginx/fastcgi /tmp/nginx/uwsgi /tmp/nginx/scgi
  /usr/sbin/nginx -c /app/nginx/nginx.conf -g 'daemon off;' &
  PROXY_PID="$!"
}

start_internal() {
  cd /app/internal
  BIND_ADDR="0.0.0.0"
  if [ "$SERVICE" = "all" ]; then
    BIND_ADDR="127.0.0.1"
  fi
  /venv/bin/gunicorn \
    -w 2 \
    -b "${BIND_ADDR}:9000" \
    app:app \
    --access-logfile - \
    --error-logfile - &
  INTERNAL_PID="$!"
}

start_web() {
  cd /app/web
  /usr/local/bin/node index.js &
  WEB_PID="$!"
}

stop_all() {
  kill -TERM "${WEB_PID:-0}" "${INTERNAL_PID:-0}" "${PROXY_PID:-0}" 2>/dev/null || true
  wait "${WEB_PID:-0}" 2>/dev/null || true
  wait "${INTERNAL_PID:-0}" 2>/dev/null || true
  wait "${PROXY_PID:-0}" 2>/dev/null || true
}

trap stop_all INT TERM

case "$SERVICE" in
  web)
    start_web
    wait "$WEB_PID"
    ;;

  internal)
    start_internal
    wait "$INTERNAL_PID"
    ;;

  all)
    start_proxy
    start_internal
    start_web

    while :; do
      if ! kill -0 "$INTERNAL_PID" 2>/dev/null; then
        stop_all
        exit 1
      fi
      if ! kill -0 "$WEB_PID" 2>/dev/null; then
        stop_all
        exit 1
      fi
      sleep 1
    done
    ;;

  *)
    echo "[entrypoint] ERREUR: SERVICE='$SERVICE' invalide (attendu: web | internal | all)"
    exit 1
    ;;
esac
```
On peut voir dans Bind address qu'il ecoute tout les interface au port `9000`
```bash
cd /app/internal
  BIND_ADDR="0.0.0.0"
  if [ "$SERVICE" = "all" ]; then
    BIND_ADDR="127.0.0.1"
  fi
  /venv/bin/gunicorn \
    -w 2 \
    -b "${BIND_ADDR}:9000" \
    app:app \
    --access-logfile - \
    --error-logfile - &
  INTERNAL_PID="$!"
```
Et dans `app.py`:
```python
from flask import Flask, request, Response
import os
import ipaddress

app = Flask(__name__)
FLAG = os.environ.get("FLAG", "CTF{dev_flag}")

def is_internal(ip: str) -> bool:
    try:
        addr = ipaddress.ip_address(ip)
        return addr.is_private or addr.is_loopback
    except ValueError:
        return False

@app.get("/flag")
def flag():
    rip = request.remote_addr or ""
    if not is_internal(rip):
        return Response("Forbidden: internal requests only\n", status=403)
    return Response(f"{FLAG}\n", mimetype="text/plain")

@app.get("/")
def index():
    return "internal-admin: ok\n"
```

Ce qui nous interesse ici, c'est qu'il y a un route `/flag`
De là, j'ai testé `http://127.0.0.1:9000/flag` mais ça n'a pas marché. Oops! XD


J'ai alors regardé le code JS et il y avait :
```javascript
function isBlockedHost(hostname) {
  const blocked = new Set(["internal", "localhost", "127.0.0.1"]);
  if (blocked.has(hostname)) return true;
  if (hostname.endsWith(".internal")) return true;
  return false;
}
```

Donc, `127.0.0.1` est bloqué mais vu qu'il ecoute tout les port `0.0.0.0`, pas de soucis! Teste de `http://0.0.0.0:9000/flag`

**_Boom_** ! 🥳 Gagné! Flag trouvé!
**First Blood** 🩸😎
