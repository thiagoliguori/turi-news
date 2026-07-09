# Feed da Turi News

A plataforma Turi News (index.html) lê os arquivos desta pasta ao abrir e mostra as
notícias com uma caixinha de seleção em cada uma. Cada tarefa diária tem o seu arquivo,
para nunca uma sobrescrever a outra:

- `feed/saude.json` — tarefa **A saúde em News**
- `feed/tecnologia.json` — tarefa **A tecnologia em saúde**

Os arquivos atuais são **exemplos** (campo `"exemplo": true`) e somem da tela assim que
as tarefas publicarem o feed real.

## Formato do arquivo

```json
{
  "fonte": "A tecnologia em saúde",
  "data": "2026-07-09",
  "geradoEm": "2026-07-09T09:07:00-03:00",
  "itens": [
    {
      "titulo": "Título da notícia",
      "resumo": "Resumo de uma linha (o que vira o texto no WhatsApp).",
      "veiculo": "Nature Medicine",
      "link": "https://..."
    }
  ]
}
```

- `veiculo` é opcional: se faltar, a plataforma deduz pelo domínio do link.
- O `resumo` é usado direto na mensagem do WhatsApp, então mantenha em uma linha.

## Como cada tarefa publica o feed

No final da tarefa, depois de gerar o docx, monte um `itens.json` (array de
`{titulo, link, resumo, veiculo}`) e rode o publicador:

```bash
python3 /Users/thiagoliguori/Desktop/Claude/turi-news/scripts/publish_feed.py \
  --key tecnologia \
  --fonte "A tecnologia em saúde" \
  --items itens.json
```

Para a outra tarefa, troque por `--key saude --fonte "A saúde em News"`.

O script escreve `feed/<key>.json` com a data de hoje e faz commit/push automático no
GitHub Pages. Use `--no-push` para testar sem publicar.
