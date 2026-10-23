# Continuidade do diagnóstico OCR/mídia Windows — 23/10/2026

Codex assumiu este recorte após mais de45minutos sem alteração observada nos
commits/mensagens de Claude, conforme o monitor autorizado. Base exata:
`c140765bbeac6e7661af6ed27e123722ad125669`, ramo Windows de Claude.
As pausas de redação/XFA e a reserva independente da VM foram preservadas.

## Diagnóstico examinado

CI[39984153516](https://github.com/airtonbp19edu/Linuxit-PDF/actions/runs/39984153516),
artefato12514358528. ZIP53518bytes, SHA-256
`ff79ccf7342e0b0a1f273aef5adb2e50eae0d8eba2b015ea51fceebc56520412`.
O conteúdo foi baixado e examinado; o status globalfailure não bastava para
classificar os testes. O relatório mostra55 casos,52 aprovados,dois erros e
um pulado. Aceitação79/79. Era um subconjunto diagnóstico, sem instalador;
o guarda final também recusa certificar Windows por esse motivo.

Dois erros identificados pelos tracebacks:

1. O teste TIFF multipágina ainda carregava uma fonte por caminhoLinux fixo.
   Agora usa `scan_font(64)`, o mesmo seletor de fonte real já introduzido por
   Claude para os demais testes. Nenhuma asserção foi removida.
2. A janela de mídia precisava de `gtksink`, ausente no ambiente do runner.
   O pacoteGTK do GStreamer é separado do pacote geral de pluginsgood no
   MSYS2/UCRT64. Acrescentado `mingw-w64-ucrt-x86_64-gst-plugin-gtk` à instalação
   do workflow neste ramo. Não foi trocado por fakesink, ignorado o teste ou
   ocultado o erro. O empacotador existente já copia `lib/gstreamer-1.0`.

Fonte primária consultada em23/10:
[pacoteGTK do MSYS2](https://packages.msys2.org/packages/mingw-w64-ucrt-x86_64-gst-plugin-gtk),
que contém `libgstgtk.dll` e depende deGTK3/GStreamerBase.

## Validação e limites

A correção deve ser validada novamente no runner Windows com os mesmos módulos.
Um diagnóstico aprovado não certifica a suíte completa, o instalador, codecs de
vídeo reais, áudio físico ou o Windows do usuário. O único puloLinux esperado no
subconjunto é a conferência `/proc` de processosTesseract. Se surgirem outros
erros, preservar relatórios e continuar a partir deles.

Este ramo deriva do Windows de Claude e conserva suas mudanças ainda fora da
main. Não integrar a main por inferência nem publicarrelease. Candidato0.1.19 e
árvore de workflows da main permanecem preservados. Este lote não executa Foxit,
não acessa VM e não altera critérios/pesos ou paridade.
