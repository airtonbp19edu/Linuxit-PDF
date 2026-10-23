# Exportação para DOCX e ODT editáveis — 23/10/2026

Claude, 2026/10/23 às 15:40 (America/Sao_Paulo, UTC-03:00). Item 5 da lista de desenvolvimento
pedida pelo usuário. Ramo `claude/exportacao-office`, ainda **sem integração à `main`** e fora do
candidato 0.1.19.

## O que faz

- **Onde aparece.** Na janela de exportação há duas opções novas: **Documento Word editável
  (.docx)** e **Documento ODF editável (.odt)**.
- **Como lê o PDF.** O texto vem do Poppler (`pdftotext -bbox-layout`), na ordem de leitura que
  ele informa. Cada bloco vira um parágrafo, com tamanho de fonte aproximado pela altura da linha,
  e palavras hifenizadas no fim da linha são unidas.
- **Páginas.** Cada página do PDF começa uma página nova no documento. Uma página sem texto vira
  um parágrafo vazio, para manter a contagem.
- **Escrita própria.** Os pacotes WordprocessingML e OpenDocument são escritos pelo
  `app/office_export.py`, sem modelo de terceiros. No ODT, `mimetype` é a primeira entrada e vai
  sem compressão.
- **Conferência antes de publicar.** O pacote é relido como XML, e o número de inícios de página
  precisa bater com o PDF. Valem os mesmos guardas das outras exportações: identidade do original
  conferida antes e depois, destino novo (nunca sobrescreve) e publicação atômica.
- **Relatório.** O resultado informa `paragraphs`, `images_exported: false` e
  `layout_preserved: false`.

## Testes e conferência

- `tests/test_office_export.py`: 6 casos novos. Cobrem parágrafos, escape de XML e caracteres de
  controle, páginas vazias, pacotes válidos, ODT com mimetype armazenado, recusa de contagem
  divergente, PDF real com Poppler, recusa de sobrescrita e de extensão errada.
- **Suíte local completa:** 566 aprovados contra 560 na `main`. As 2 falhas e os 46 erros do
  ambiente de nuvem são os mesmos nos dois casos; não há falha nova.
- **CI Linux:** `no-vm-validation`, run [40004191241](https://github.com/airtonbp19edu/Linuxit-PDF/actions/runs/40004191241)
  no commit c5d3663. Suíte completa **750/750** (zero falhas, erros e pulos), aceitação **81/81** e
  smoke GTK aprovado.
- **LibreOffice (headless, local):**
  - o DOCX convertido para PDF deu **2 páginas** com "Primeira pagina" e "Segunda pagina";
  - o ODT convertido para texto trouxe os dois parágrafos.
  - Hashes em [review.json](../testes/resultados/exportacao-office-2026-10-23/review.json).

## Limites declarados

- Imagens, tabelas, colunas, cores e fontes exatas não são reproduzidas; é uma exportação de texto
  editável.
- Não foi testado no Microsoft Word.
- Isto não é comparação com o Foxit nem afirma paridade.
