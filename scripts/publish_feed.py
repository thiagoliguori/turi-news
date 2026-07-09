#!/usr/bin/env python3
"""Publica um feed da Turi News no repositório GitHub.

Cada tarefa diária de notícias chama este script no final, passando seus itens.
Ele escreve feed/<key>.json (com a data de hoje) e faz commit/push no repositório,
para que a plataforma Turi News (GitHub Pages) mostre as notícias com caixinhas de
seleção.

Uso:
  python3 publish_feed.py --key tecnologia --fonte "A tecnologia em saúde" --items itens.json

Onde itens.json é um array JSON de objetos:
  [
    { "titulo": "...", "link": "https://...", "resumo": "resumo de uma linha", "veiculo": "Nature Medicine" }
  ]
O campo "veiculo" é opcional (se faltar, a plataforma deduz pelo domínio do link).
"""
import argparse
import datetime
import json
import os
import subprocess

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def git(repo, *args, check=True):
    return subprocess.run(["git", "-C", repo, *args], check=check)


def main():
    ap = argparse.ArgumentParser(description="Publica um feed da Turi News.")
    ap.add_argument("--key", required=True, choices=["saude", "tecnologia"],
                    help="Qual arquivo de feed atualizar (feed/<key>.json).")
    ap.add_argument("--fonte", required=True,
                    help='Nome da tarefa, ex.: "A saúde em News".')
    ap.add_argument("--items", required=True,
                    help="Arquivo JSON com um array de itens {titulo, link, resumo, veiculo}.")
    ap.add_argument("--repo", default=REPO, help="Raiz do repositório turi-news.")
    ap.add_argument("--no-push", action="store_true",
                    help="Só escreve o arquivo, sem commit/push (para testes).")
    args = ap.parse_args()

    with open(args.items, encoding="utf-8") as f:
        raw = json.load(f)
    if not isinstance(raw, list):
        raise SystemExit("O arquivo --items deve conter um array JSON de notícias.")

    itens = []
    for it in raw:
        link = str(it.get("link") or "").strip()
        if not link:
            continue
        itens.append({
            "titulo": str(it.get("titulo") or "").strip(),
            "resumo": str(it.get("resumo") or "").strip(),
            "veiculo": str(it.get("veiculo") or "").strip(),
            "link": link,
        })
    if not itens:
        raise SystemExit("Nenhum item com link encontrado; nada a publicar.")

    now = datetime.datetime.now().astimezone()
    payload = {
        "fonte": args.fonte,
        "data": now.strftime("%Y-%m-%d"),
        "geradoEm": now.isoformat(timespec="seconds"),
        "itens": itens,
    }

    feed_dir = os.path.join(args.repo, "feed")
    os.makedirs(feed_dir, exist_ok=True)
    rel = os.path.join("feed", args.key + ".json")
    path = os.path.join(args.repo, rel)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"Feed escrito em {path} com {len(itens)} itens.")

    if args.no_push:
        return

    try:
        git(args.repo, "pull", "--rebase", "--autostash", "-q", check=False)
    except Exception:
        pass
    git(args.repo, "add", rel)
    staged = subprocess.run(["git", "-C", args.repo, "diff", "--cached", "--quiet"]).returncode
    if staged != 0:
        git(args.repo, "commit", "-q", "-m", f"feed: {args.fonte} {payload['data']}")
        git(args.repo, "push", "-q")
        print("Publicado no GitHub Pages.")
    else:
        print("Sem mudanças no feed; nada a publicar.")


if __name__ == "__main__":
    main()
