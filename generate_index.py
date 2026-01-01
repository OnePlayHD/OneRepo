from pathlib import Path
import re
import unicodedata

# Constantes

ZIP_REPO = re.compile(r"One\.repo-\d+(?:\.\d+)*\.zip")

# Utils

def extrair_versao(nome: str):
    m = re.search(r"One\.repo-(\d+(?:\.\d+)*)\.zip", nome)
    return tuple(map(int, m.group(1).split("."))) if m else ()

def remover_acentos(texto: str) -> str:
    return ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn'
    ).lower()

# Repositórios Kodi (apenas One.repo)

def encontrar_repos_kodi(raiz: Path) -> list[Path]:
    encontrados = []
    for item in raiz.rglob("One.repo-*.zip"):
        versao = extrair_versao(item.name)
        if versao:
            encontrados.append((versao, item))

    if not encontrados:
        return []

    maior = max(v for v, _ in encontrados)
    return [p for v, p in encontrados if v == maior]

# Index handling

def gerar_index(pasta: Path, raiz: Path):
    index = pasta / "index.html"
    repos_kodi = encontrar_repos_kodi(raiz)

    linhas_html = [
        "<!DOCTYPE html>",
        "<html lang='pt-BR'>",
        "<head>",
        '<meta charset="utf-8">',
        "<title>Directory listing</title>",
        "<style>",
        "body { font-family: Arial, sans-serif; background:#f9f9f9; color:#333; padding:20px; }",
        "h1 { color:#222; }",
        "pre { background:#fff; padding:10px; border-radius:8px; box-shadow:0 0 5px rgba(0,0,0,0.1); }",
        "a { text-decoration:none; color:#0066cc; }",
        "a:hover { text-decoration:underline; }",
        "</style>",
        "</head>",
        "<body>",
        "<h1>Directory listing</h1>",
        "<hr/>",
    ]

    # Botão voltar
    if pasta != raiz:
        linhas_html.append('<a href="../index.html">← Voltar</a><br><br>')

    linhas_html.append("<pre>")

    for item in sorted(pasta.iterdir(), key=lambda x: (not x.is_dir(), x.name.lower())):
        if item.name.startswith(".") or item.name == "index.html":
            continue

        if item.is_dir():
            linhas_html.append(f'📁 <a href="{item.name}/index.html">{item.name}/</a>')
        elif item.is_file():
            linhas_html.append(f'📄 <a href="{item.name}">{item.name}</a>')

    linhas_html.extend([
        "</pre>",
        "</body>",
        "</html>",
    ])

    index.write_text("\n".join(linhas_html), encoding="utf-8")
    print(f"✔ index atualizado: {index}")

        # BLOCO KODI (SOMENTE NA RAIZ)
    
    if pasta == raiz and repos_kodi:
        with index.open("a", encoding="utf-8") as f:
            f.write("\n<!-- REPOSITORIO KODI (FORA DO HTML) -->\n")
            f.write('<div id="Repositorio-KODI" style="display:none">\n<table>\n')
            for repo in repos_kodi:
                rel = repo.relative_to(raiz).as_posix()
                f.write(f'<tr><td><a href="{rel}">{rel}</a></td></tr>\n')
            f.write("</table>\n</div>\n")

        print("✔ bloco Kodi adicionado")

# Varredura bottom-up

def varrer(pasta: Path, raiz: Path):
    for sub in pasta.iterdir():
        if sub.is_dir() and not sub.name.startswith("."):
            varrer(sub, raiz)
    gerar_index(pasta, raiz)

# Main

if __name__ == "__main__":
    raiz = Path(".")
    varrer(raiz, raiz)
