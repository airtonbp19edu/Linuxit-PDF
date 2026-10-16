# Histórico

- 2026-10-16: investigação inicial REA/Ghidra publicada em `f5073e4`.
- 2026-10-16: pedido mestre adotado; prioridade Linux/Flatpak e destino Linuxit-PDF preservados. Inventário integral e rastreamento das 21 etapas adicionados. Percentuais do exemplo do pedido não foram usados.
- 2026-10-16: `5312ae0` publicado, com inventário integral (3.276 arquivos) e correspondência ZIP verificada.
- 2026-10-16: base própria MIT integrada; busca por páginas/marcadores/comentários implementada. 34 testes próprios passaram na fonte e no payload. Testes diferenciais Foxit permanecem pendentes; Flatpak real em validação.
- 2026-10-16: `739ed14` publicado com o leitor e seus testes. O sandbox detectou colisão de bibliotecas e ausência do provedor OpenSSL; o empacotamento passou a usar `runtime-lib` e incluir o provedor com licença.
- 2026-10-16: bundle final 0.1.0 passou no sandbox instalado e no launcher normal; SHA-256 e manifesto em `releases/`. Testes da fonte: 34/34; payload corrigido: 34/34; quatro verificações do harness real aprovadas. A distribuição continua em desenvolvimento.
- 2026-10-16: `b709a4f04dea272b31bb0f1ae4d31d492c7bdf9b` confirmado no remoto com árvore limpa; artefato e relatórios publicados. O relatório de sincronização registra esse commit já confirmado; o HEAD do registro posterior é verificado novamente fora da árvore.
