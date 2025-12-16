#!/usr/bin/env python3
"""
Script para mesclar a landing page com o mapa existente.

Estrutura final:
1. Landing page (seções de marketing)
2. Mapa completo (código original preservado)
"""

# Ler landing page
with open('index_new.html', 'r', encoding='utf-8') as f:
    landing_html = f.read()

# Ler mapa original
with open('index.html', 'r', encoding='utf-8') as f:
    original_html = f.read()

# Extrair apenas o conteúdo do body do original (mapa)
# Vamos pegar do <div class="header"> até o final do body
import re

# Encontrar onde começa o conteúdo do mapa (após <body>)
body_start = original_html.find('<body>')
body_end = original_html.rfind('</body>')

if body_start == -1 or body_end == -1:
    print("Erro: não encontrou tags <body>")
    exit(1)

# Pegar todo o conteúdo do body
map_body_content = original_html[body_start + 6:body_end].strip()

# Pegar os estilos CSS do original (entre <style> e </style>)
style_start = original_html.find('<style>')
style_end = original_html.find('</style>') + 8

if style_start != -1 and style_end != -1:
    map_styles = original_html[style_start:style_end]
else:
    map_styles = ""

# Pegar os scripts do original (entre <script> e </script>)
# Vamos pegar TODOS os scripts
scripts = []
pos = 0
while True:
    script_start = original_html.find('<script', pos)
    if script_start == -1:
        break

    script_end = original_html.find('</script>', script_start)
    if script_end == -1:
        break

    scripts.append(original_html[script_start:script_end + 9])
    pos = script_end + 9

map_scripts = '\n'.join(scripts)

# Substituir no template da landing
# Adicionar estilos do mapa no CSS da landing
landing_html = landing_html.replace(
    '/* (Todo o CSS do mapa será preservado aqui) */',
    map_styles.replace('<style>', '').replace('</style>', '')
)

# Adicionar o conteúdo do mapa na seção #app-section
landing_html = landing_html.replace(
    '<!-- TODO: Preservar código do mapa aqui -->',
    map_body_content
)

# Adicionar scripts antes do </body>
landing_html = landing_html.replace(
    '</body>',
    f'{map_scripts}\n</body>'
)

# Atualizar título
landing_html = landing_html.replace(
    '<title>GreenGate - Triagem Ambiental Automatizada para Mato Grosso</title>',
    '<title>GreenGate - Triagem Ambiental Automatizada | Mato Grosso</title>'
)

# Salvar versão final
with open('index_final.html', 'w', encoding='utf-8') as f:
    f.write(landing_html)

print("OK - Landing page + Mapa mesclados com sucesso!")
print("Arquivo criado: index_final.html")
print(f"Total de linhas: {len(landing_html.splitlines())}")
