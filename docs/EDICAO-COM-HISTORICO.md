# Edição de cópia com histórico

Fonte de desenvolvimento **0.1.10**, em validação. O Flatpak publicado anterior
é 0.1.9; este documento não declara novo pacote aprovado antes das evidências.
Contrato próprio MIT, sem transportar código ou recursos Foxit.

Em **Arquivo → Editar cópia com desfazer/refazer…**, escolha a operação e a
página. Cada alteração aceita é aplicada a uma cópia temporária, reaberta e
inspecionada pelo worker. O histórico só avança se essa verificação passar.
Desfazer/refazer reconstituem o rascunho; uma nova alteração após desfazer
descarta a ramificação de refazer. Limite de 100 operações por sessão.

**Salvar cópia nova…** aplica somente as operações ativas a um arquivo novo,
com fonte identificada por SHA-256 e publicação exclusiva. O PDF aberto e
as cópias já salvas permanecem preservados ao desfazer o rascunho. Reabrir ou
fechar o documento fecha seu editor e invalida trabalho anterior. Fechar durante
uma gravação pode deixar saída já concluída ou parcial: conferir o destino.

Atalhos na janela do rascunho: Ctrl+Z desfaz, Ctrl+Shift+Z ou Ctrl+Y refazem.
O foco em campos de entrada não dispara o histórico global da janela.

## Operações adicionais

- **Mover marcadores:** escolher marcador, novo pai ou nível principal e posição
  depois de retirá-lo da origem. Move a subárvore preservando destinos, títulos,
  ações armazenadas e propriedades; não executa ações PDF. Recusa mover para
  si mesmo ou para descendente, caminhos/posições inválidos e árvores acima dos
  limites de profundidade/contagem. Recalcula links e contagens de visibilidade,
  preservando o estado aberto/fechado. Exclusão remove a subárvore da árvore ativa.
- **Formulários:** checkbox usa aparências Off/ligada já presentes; radio simples
  atualiza o grupo e a aparência de cada opção. Listas, combos sem texto livre e
  listas com seleção múltipla usam valores de exportação, rótulos e índices
  ordenados. ReadOnly herdado é respeitado. Campos Tx anteriores continuam disponíveis.
- **Anotações:** destaque amarelo de uma área retangular e retângulo, com comentário
  opcional. Coordenadas são pontos PDF antes da rotação, dentro do CropBox.
  Exclusão lógica de Text/Square/Highlight desbloqueadas, sem popup/respostas
  relacionados. Não exclui widgets de formulário, links ou tipos não suportados.

O editor usa as informações do rascunho atual ao pedir caminhos, índices e
valores; não reutiliza índices anteriores a uma exclusão/movimentação aceita.
Os comandos anteriores que gravam uma alteração por cópia continuam disponíveis.

## Limites explícitos

As famílias permanecem parciais. Não há XFA, JavaScript/cálculos/eventos de
formulário, edição livre de combo, botões de ação, radio com estados repetidos,
aparências de checkbox ausentes, valores/rótulos de opções duplicados ou widgets
de lista com valor local. Nomes que ativariam a ambiguidade de alias da biblioteca
são recusados antes da gravação. Omissões de controles são informadas na interface.

Opções por campo limitadas a 512, widgets a 128, valores/rótulos a 4096 bytes;
até 512 controles adicionais são descritos. O worker aceita no máximo 1 MiB de
pedido de edição. Os limites anteriores de texto, assinaturas, criptografia,
portfólios, árvores de marcadores e recursos do worker permanecem.

Pypdf 6.20.1 não gera diretamente a aparência de listas com `/Opt` em pares.
O adaptador próprio gera a aparência usando rótulos e depois restaura opções,
valores de exportação e índices. A biblioteca vendorizada não foi modificada.
Cobertura de fontes/Unicode e fidelidade visual universal não são garantidas.
Exclusão de anotações/marcadores é lógica: não é redação nem apagamento seguro
de bytes órfãos do arquivo PDF. Notas antigas com respostas/popup são recusadas
para exclusão; não se remove uma cadeia por inferência.

## Verificações desta rodada

21 testes portáveis de novos controles/árvores/anotações e oito de histórico
passaram em PDFs sintéticos reais. A primeira tentativa encontrou três falhas
de aparência `/Opt`; o adaptador corrigiu esse caminho. Um teste de histórico
falhou por import da biblioteca antes de configurar o caminho; execução corrigida
passou. Relatórios anteriores foram preservados, sem contar falhas como sucesso.

Regressão local de edição: 42 passaram e cinco GTK foram omitidos por falta
de GTK/X11 no Windows. Isso não valida interface Linux. Oito testes GTK novos
cobrem diálogos, botões/histórico, destinos existentes, geração do documento,
cancelamento e renderização Poppler; execução completa no Linux ainda pendente
neste checkpoint. Suítes anteriores de 290 casos referem-se à versão 0.1.9.

Fontes principais: `app/pdf_form_controls.py`, `app/pdf_changes.py`,
`app/edit_history.py`, `app/edit_tasks.py`, `app/edit_dialogs.py`, `app/edit_window.py`.
Testes: `tests/test_advanced_edits.py`, `tests/test_edit_history.py`,
`tests/test_edit_draft_gtk.py`. Relatórios portáveis em
`testes/resultados/advanced-edits-portable-2026-10-18-round2.json` e
`testes/resultados/edit-history-portable-2026-10-18-round2.json`.

Catálogo REA preservado em 323 entradas. Original não executado; equivalência
Foxit continua 0/25, roteiro 43,33% e 21 critérios amplos abertos. Formatos/OCR,
demais anotações, formulários e integrações ainda precisam de trabalho próprio.

## Primeira validação Linux do editor

[CI327/327](https://github.com/airtonbp19edu/Linuxit-PDF/actions/runs/39098594089),
fonte7b0b1572626cc603221a0e70a5006fb1b6eff6f7: zero falhas/erros/skips; oito
GTK novos passaram, smoke5/5 e corpus próprio17/17. Captura do editor examinada.
[Revisão](../testes/resultados/0.1.10-source/review.json). Este resultado pertence
ao commit do editor; as adições posteriores de formatos e a conferência de
pixel amarelo exigem a próxima validação integral da fonte/payload/sandbox.
