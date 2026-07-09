# Turi News

Ferramenta de uso pessoal para gerar a mensagem "Turi News" enviada em um grupo de WhatsApp sobre inteligência artificial na saúde.

**Como funciona**

1. Cole links de notícias, artigos científicos, PDFs ou vídeos do YouTube (um por linha).
2. A página lê o conteúdo de cada link e gera um resumo de uma linha com a API da Anthropic (Claude), direto do navegador.
3. A mensagem formatada aparece pronta para copiar e colar no WhatsApp.

**Configuração**

É preciso ter uma chave da API Anthropic (console.anthropic.com). A chave fica salva apenas no localStorage do navegador. Nada é enviado a servidores próprios: o site é 100% estático (GitHub Pages).
