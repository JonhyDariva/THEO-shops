#!/usr/bin/env python3
"""gera o baixar.bat de um short a partir do resultado salvo do elevenlabs.

uso (quem roda é o claude, no ambiente dele, depois de consultar o status das gerações):
  python3 motor/links.py 002 status.json mapa.json > baixar.bat

status.json  resposta crua do creative_get_flow_run_status (tem 'generations' com id e content_url)
mapa.json    {"clipes/002/c01.mp4": "<generation_id>", "audio/002/f01.mp3": "<generation_id>", ...}

os links são assinados e vencem em cerca de 2 horas: gerar, dar push e rodar logo.
"""
import json, sys

n, st, mp = sys.argv[1:4]
g = {x['id']: x['content_url'] for x in json.load(open(st))['generations']}
m = json.load(open(mp))
L = ['@echo off', 'cd /d "%~dp0"', f'if not exist "clipes\\{n}" mkdir "clipes\\{n}"', f'if not exist "audio\\{n}" mkdir "audio\\{n}"',
     f'echo baixando {len(m)} arquivos do short {n}...']
for dest in sorted(m):
    u = g[m[dest]]
    assert '%' not in u, 'link com % quebra no .bat'
    w = dest.replace('/', '\\')
    L.append(f'curl.exe -sS -L -f -o "{w}" "{u}" && echo ok {dest} || echo FALHOU {dest}')
L += ['echo.', 'echo pronto. confira se apareceu FALHOU em alguma linha.', 'pause']
sys.stdout.write('\r\n'.join(L) + '\r\n')
