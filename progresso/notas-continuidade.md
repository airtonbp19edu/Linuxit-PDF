# Notas de continuidade entre IAs

Registros por rodada, em ordem cronológica. Usar o horário de São Paulo e
preservar as notas anteriores. A sequência técnica completa também está em
`historico.md`, `tarefas-pendentes.md` e `../docs/RETOMADA.md`.

## 2026/10/16 às 20:02 (America/Sao_Paulo, UTC-03:00) — rodada iniciada

Pedido: continuar a engenharia reversa local e no GitHub e sempre deixar uma
nota datada para outras IAs. Checkout inicial limpo em `main`, commit
`62fe1e34d3e589e71974860199f0a756ebcbb41e` (última publicação confirmada na
rodada anterior; a confirmação remota desta rodada ainda está pendente).

REA 6.5.0, Ghidra 12.1.4, JDK Temurin 21.0.12.1 e Node 24.22.0 conferidos.
O diagnóstico explícito do provedor Ghidra passou nos dez controles. Isso não
valida uma interface Foxit isolada nem implica disponibilidade de IDA/Hopper.

Foi iniciada a análise estática complementar das seis entradas de impressão
pendentes: `0x1668750`, `0x1667fe0`, `0x1655e00`, `0x16561c0`, `0x1665780`,
`0x166fe90`. Backend direto Ghidra `-noanalysis` com script de seeds do REA;
não contar como resultado MCP. Resultados completos e projeto separados em
`analysis-local/headless/windows-print-02`, ignorado pelo Git. Ainda não há
novo resultado tecnicamente examinado nesta nota de início.

O conector GitHub usado nas rodadas anteriores apareceu não instalado/não
conectado nesta rodada; foi oferecida a conexão. O Git local também está sendo
verificado sem interação. Publicação nova ainda não confirmada.

A etapa 10 permanece dependente de ambiente offline isolado; os 20 cenários
preparados não foram observados. Nenhuma execução funcional do Foxit nesta
rodada. Manter progresso em 43,33% e paridade 0/25 até evidência suficiente.

Atualização durante a rodada: o Git local autenticou com sucesso em consulta
não interativa e confirmou `62fe1e34d3e589e71974860199f0a756ebcbb41e` no remoto.
É possível tentar a publicação pelo Git normal; o conector não é necessário
para esse caminho. Não há nova publicação confirmada neste ponto do registro.

## 2026/10/16 às 20:14 (America/Sao_Paulo, UTC-03:00) — análise local concluída

As seis entradas pendentes foram descompiladas e examinadas: `0x1668750`,
`0x1667fe0`, `0x1655e00`, `0x16561c0`, `0x1665780` e `0x166fe90`.
O catálogo agora tem **200 entradas distintas (152 REA + 48 diretas)**;
as 194 anteriores e seus manifestos foram preservados.

Avanços: limites e últimos índices de posicionamento; transformação e guarda
de coleção vazia; dois consumidores com destino comum; preparação de fonte
GDI; enumeração de handlers e dois caminhos de saída. Um slot inicialmente
comparado como inteiro foi tipado como float pelo Ghidra por reuso posterior.
Assinaturas e semântica completa continuam provisórias.

Evidências publicáveis: `docs/REA-IMPRESSAO-CONSUMIDORES.md`, metadados em
`docs/windows-evidence/foxit-rea/headless-cross-checks-windows-followup-2026-10-16.json`
e `windows-print-followup-contracts.json` no mesmo diretório. Diagnóstico atual
em `windows-followup-readiness.json`; verificações em
`testes/resultados/rea-consumidores-windows-2026-10-16.json`.
Resultados completos, montagem e projeto ficam somente em
`analysis-local/headless/windows-print-02`. Dependências PeFile/Capstone
instaladas em `analysis-local/python-deps`, sem alteração do Python global.

Verificações: dez controles REA/Ghidra aprovados; seis descompilações completas;
hashes dos resultados conferidos; Capstone confirmou todos os endereços das
1.484 instruções / 4.874 bytes; as importações CreateFontIndirectW/DeleteObject
foram verificadas na tabela PE. Sintaxe Python e links locais conferidos no
relatório. Original intacto, sem execução funcional, sem mudança no leitor e
sem novo Flatpak. Roteiro 43,33%, paridade 0/25, etapa 10 ainda bloqueada.

O gerador de metadados ganhou `--round`, com validação de identidade e recusa
de diretório fora de `evidence-root/headless`. Notas datadas agora são uma
instrução explícita em `AGENTS.md`, conforme o pedido do usuário.

Próximo passo estático: seguir `0x166d050`, `0x165f5d0`, `0x16678c0`,
`0x16678d0`, `0x16678e0`, `0x16678f0`, `0x1665a30`, `0x1664c00`,
`0x2d226d0` e `0x1b5baf0`. A etapa 10 requer primeiro a VM offline descrita
em `docs/COMO-CONTINUAR.md`. Não reiniciar as análises preservadas.

Publicação: consulta Git autenticada confirmou a base remota; envio do novo
marco será feito após esta anotação. A confirmação posterior será acrescentada
ao final deste arquivo com o hash do marco já publicado.

## 2026/10/16 às 20:15 (America/Sao_Paulo, UTC-03:00) — publicação confirmada

Marco técnico publicado em `main`:
[`c696ca939ec1d523786d570a74acd21ae20e11a7`](https://github.com/airtonbp19edu/Linuxit-PDF/commit/c696ca939ec1d523786d570a74acd21ae20e11a7).
O envio pelo Git normal passou, e `git ls-remote origin refs/heads/main`
confirmou esse hash às 20:15. Não foi necessário instalar ou reconectar o
plugin GitHub. O conector pode continuar ausente; a autenticação Git local
funcionou nesta rodada e deve ser reconferida em futuras sessões.

Esta anotação registra um commit já confirmado, sem tentar conter o hash do
próprio commit. Após publicá-la, conferir novamente HEAD local/remoto e árvore
limpa; o comprovante final fica em
`analysis-local/github-round02-sync-verified.json`, fora dos arquivos versionados.
Próximos alvos e limitações são os da nota das 20:14 e do relatório dos
consumidores. Nenhuma atividade da etapa 10 foi marcada como concluída.

## 2026/10/16 às 23:47 (America/Sao_Paulo, UTC-03:00) — início da etapa 11 em paralelo

O usuário pediu avançar a engenharia reversa da interface enquanto prepara a
VM da etapa 10. Base local limpa e remoto reconfirmado em
`acda307e952ba614efe1d2511dd8e162047cc99b`. A etapa 11 tem 25% verificados:
inventário e nove controles ligados ao estado; a observação de todas as
interações ainda depende da execução isolada do original.

Iniciada análise estática de nove entradas ainda não catalogadas, com Ghidra
direto `-noanalysis` e seeds do REA, em novo projeto
`analysis-local/headless/windows-ui-01`. Alvos: `0x803920`, `0x861470`,
`0x85d1a0`, `0x85ddd0`, `0x85de30`, `0x80eab0`, `0x1788db0`, `0x1788e10`
e `0x1788d70`. Não tratar resultados como MCP; não contar antes de examinar.

Preparados um cruzamento contextual das tabelas de comandos com os corpos de
função e dez cenários de observação da interface, todos `not_run`. IDs iguais
em contextos diferentes, propriedades declaradas em templates e conexões de
botões não demonstram disponibilidade no Reader. Nenhum original executado.
Publicação do novo marco ainda pendente desta rodada.

## 2026/10/16 às 23:58 (America/Sao_Paulo, UTC-03:00) — etapa 11 estática examinada

Nove entradas novas examinadas em `analysis-local/headless/windows-ui-01`,
com Ghidra direto `-noanalysis` e seeds REA, sem execução do Foxit. Catálogo:
**209 entradas distintas (152 REA + 57 diretas)**, preservando as 200 anteriores
e três manifestos. As nove descompilações foram examinadas junto à montagem.

Avanços: atualização de Abrir/Imprimir/Próxima página/Zoom/Imprimir todas as
abas e armazenamento de três opções de busca. Zoom nos limites 64 e 0,01
envia desabilitação; outros ramos não habilitam explicitamente. Imprimir todas
as abas exige mais de um objeto aceito por predicado ainda parcial. A tabela
associa os IDs 7911/7913 ao mesmo handler, mas ele escreve somente `+0x1d58`;
o vínculo ao texto das páginas `+0x1d60` permanece ambíguo. Não converter essa
junção estrutural em comportamento comprovado ou mudar o leitor com base nela.

Relatório: `docs/ETAPA-11.md`. Metadados em `docs/windows-evidence/foxit-rea/`:
`headless-cross-checks-ui-2026-10-16.json`, `ui-availability-windows-2026-10-16.json`
e `ui-state-contracts-2026-10-16.json`. Helper novo:
`scripts/catalog_foxit_ui_availability.py`, com identidade, dez registros PE
contextuais e recusa de sobrescrita. Estados/conexões declarados foram reunidos
dos dez metadados FX existentes, sem reextrair ou publicar templates.

Verificações: dez controles REA/Ghidra; nove resultados com hashes conferidos;
Capstone confirmou 242 instruções / 641 bytes; PeFile conferiu importações
e constantes de zoom. Sintaxe de 105 arquivos Python e 32 links conferidos.
Cinco regressões do preparador passaram. Campanha nova em
`analysis-local/dynamic/windows-ui-01`, com guia e dez cenários UI `not_run`,
além dos 20 casos da etapa 10; campanhas anteriores preservadas. Relatório de
validação: `testes/resultados/etapa-11-estatica-windows-2026-10-16.json`.

O critério restante da etapa 11 depende de observação: etapa 11 25%, roteiro
43,33%, paridade 0/25. Sem comportamento novo no aplicativo, suíte GTK completa,
teste diferencial ou Flatpak novo. Próximos alvos: `0x859920`, `0x687ae0`,
`0x5f5370` e `0x48f10ef`; esclarecer classes e IDs 7911/7913. Executar UI01–UI10
com D01–D20 quando a VM estiver validada. Publicação será confirmada a seguir
com o hash do marco já verificado.
