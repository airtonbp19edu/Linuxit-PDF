# S2 — fechamento do fluxo de impressão (em andamento)

Claude, 2026/10/23 desde 12:05 (America/Sao_Paulo, UTC-03:00). Documento de trabalho; o critério
"Fluxo completo de impressão reconstruído" (etapa 8) só muda depois da revisão final.

Ambiente: Ghidra 12.1.4 copiado do PC (módulos Framework, Base, Decompiler linux_x86_64, x86 com
.sla distribuídos e .sinc de data antiga para não recompilar), REA 6.7.0 (script de sementes),
`scripts/analyze_foxit_headless.py` -noanalysis. Alvo `FoxitPDFReader.exe` SHA-256
`90208c9e…b3a6` conferido antes e depois. O Foxit não foi executado. Tentativas falhas preservadas
em `analysis-local/headless/claude-s2-1-attempt{1,2,3}-*` (Sleigh tentando recompilar).

## Lote 1 (`claude-s2-1`, 9 entradas) — achados

- `0x165f8a0` (total do laço externo): modo `associado+0xb0==5` soma, por entrada ativa, linhas×colunas
  (`+0x34 × +0x38`) e grava o índice inicial de cada entrada em `+0x3c`; modos `associado+0xc8` 1 ou 2
  dão uma única unidade; nos demais, `ceil(entradas / 0x165ef50(2))`.
- `0x166f160` (trabalhador do modo 5): localiza a entrada cujo intervalo contém a unidade, calcula a
  geometria da parte (`0x1668f60`), prepara e desenha (`0x1663a80`, `0x1663410`, `0x1663870`), deriva
  coluna e linha por `%`/`/` do número de colunas, chama `0x1662a30` e `0x1660ae0`, e ao fim da última
  parte da entrada chama `0x165fa90`. `StartPage/EndPage` por parte quando não há destino alternativo.
  Interpretação: impressão em partes (pôster/mosaico).
- `0x1667620` (chamado após cada unidade): abre a impressora, chama **`GetJobW`** (thunk `0x48ed07e`,
  nível 2) com o identificador do trabalho; lê `JOB_INFO_2W.Status` (+0x34). Se o estado mudou e tem
  `0x106` (ERROR|DELETING|DELETED), devolve o estado e o coordenador encerra o laço. **É a detecção do
  cancelamento pela fila do Windows.** Guarda o último estado em `base+0x88`.
- `0x166b420` (decisão antes de `StartDocW`): sem interface em `base+0x5c` devolve 1; com ela, reúne
  dados da impressora (`0x164e220`: porta, driver e atributos LOCAL/NETWORK/SHARED de
  `PRINTER_INFO_2W`), modo, lista de páginas ativas e pergunta à interface se pode imprimir.
- `0x1671680` (após `ResetDCW`): relê `GetDeviceCaps` LOGPIXELSX/Y, PHYSICALWIDTH/HEIGHT e
  PHYSICALOFFSETX/Y para a configuração e recalcula a escala da entrada conforme o modo de escala.
- `0x1659ff0`/`0x165d1f0`: guarda RAII da via RAW; o destrutor fecha a impressora (`ClosePrinter`).
- `0x1b88c60`: destrói o contexto de 0x138 bytes liberando `+0xe4`, `+0x120` (se `+0x11d`), `+0x124`,
  `+0x78`, `+0x7c`, referência contada `+0xbc`, ponteiro compartilhado `+0x6c` e o bloco `+0x44`.
- `0x166d990` (via alternativa): zera `base+0x14`, passa pela mesma decisão `0x166b420` (recusa avisa
  o handler `base+0x80` slot `+0xc`), cria um documento de destino (`0x1667a20`), percorre as mesmas
  unidades com teste de `base+0x14`, despacha os mesmos trabalhadores com destino alternativo (sem
  `StartPage/EndPage`) e finaliza em `0x166f990`.

## Próximo lote (`claude-s2-2`, em execução)

Identidade da via alternativa (`0x1667a20`, `0x1669c10`, `0x1670ee0`, `0x1671120`, `0x166f990`),
helpers de partes (`0x1668f60`, `0x1662a30`, `0x1660ae0`, `0x165fa90`), modo/escala (`0x165ef50`,
`0x1667330`, `0x1667590`) e quatro escritores candidatos da flag de cancelamento `+0x14`
(`0x164d340`, `0x1674d80`, `0x167e980`, `0x167f090`, por varredura de `mov [reg+0x14], 1`).
