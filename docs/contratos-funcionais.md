# Registro de contratos funcionais — etapa 12

Gerado de `especificacao-funcional.json` por `scripts/validate_functional_spec.py`.

Escopo: **25 famílias identificadas**, **50 cenários planejados**; 23 subconjuntos implementados e 2 propostas futuras. O inventário global permanece aberto.

O campo esperado é do contrato próprio atual ou de uma proposta explicitamente identificada. Expectativas/observações Foxit permanecem `null`. Referenciar um teste existente não o executa novamente nem comprova paridade. As duas situações de cada família são um início de cobertura, não uma lista exaustiva.

Os campos `fixture_refs` apontam materiais já disponíveis; cenários que pedem outros documentos continuam dependendo da criação/especialização do corpus descrito em sua condição inicial.

Índices internos de página usam base zero; páginas em relatórios de observação usam base um.

O assistente de IA do Foxit e recursos generativos estão fora do escopo por decisão do usuário em 17/10/2026; ver [escopo do projeto](ESCOPO.md). As 25 famílias atuais e os registros históricos são preservados.

| Família | Estado do contrato |
|---|---|
| [Abrir PDF e renderizar páginas](#open-render) | Subconjunto atual; lacunas abertas |
| [Navegação/rotação/zoom](#navigation) | Subconjunto atual; lacunas abertas |
| [Apresentação ajustar/preencher](#presentation) | Subconjunto atual; lacunas abertas |
| [Busca literal/palavra inteira/maiúsculas](#search-text) | Subconjunto atual; lacunas abertas |
| [Busca em marcadores](#search-bookmarks) | Subconjunto atual; lacunas abertas |
| [Busca em comentários](#search-comments) | Subconjunto atual; lacunas abertas |
| [Busca em anexos](#search-attachments) | Subconjunto atual; lacunas abertas |
| [Índice persistente/pesquisa de coleção](#search-index) | Subconjunto atual; lacunas abertas |
| [Stemming/proximidade/coringas](#search-language) | Subconjunto atual; lacunas abertas |
| [Seleção/cópia/snapshot](#selection) | Subconjunto atual; lacunas abertas |
| [Prévia/plano de impressão](#printing) | Subconjunto atual; lacunas abertas |
| [Livreto/N-up/mosaico](#imposition) | Subconjunto atual; lacunas abertas |
| [Criar/mover/gravar marcadores](#bookmarks-edit) | Subconjunto atual; lacunas abertas |
| [Anotações/undo/gravação](#annotations) | Subconjunto atual; lacunas abertas |
| [AcroForm/XFA/eventos](#forms) | Subconjunto atual; lacunas abertas |
| [Anexos/portfólios](#attachments) | Subconjunto atual; lacunas abertas |
| [Assinaturas/certificados](#signatures) | Subconjunto atual; lacunas abertas |
| [Senhas/permissões/RMS](#security) | Subconjunto atual; lacunas abertas |
| [Acessibilidade/voz](#accessibility) | Subconjunto atual; lacunas abertas |
| [Medição/calibração](#measurement) | Subconjunto atual; lacunas abertas |
| [Camadas/mídia/3D](#layers-media) | Subconjunto atual; lacunas abertas |
| [Preferências/tema/persistência](#preferences) | Subconjunto atual; lacunas abertas |
| [Nuvem/colaboração](#cloud) | Proposta; não implementado |
| [Criação/conversão](#conversion) | Subconjunto atual; lacunas abertas |
| [Integrações de sistema/atualização](#platform) | Proposta; não implementado |

<a id="open-render"></a>

## Abrir PDF e renderizar páginas

Abrir PDF local, inspecionar páginas/metadados e renderizar páginas. Salvar cópia é cópia do arquivo; não edição PDF. Fonte0.1.9: fluxo local de pasta preferida/últimas pastas e cópias novas com publicação completa/exclusiva. Envio remoto é do sincronizador externo; fonte/payload/sandbox290/290 aprovados; cliente real e portal em desktop ainda pendentes.

**Entradas**

- Caminho de PDF local legível; página interna baseada em zero.
- Viewport, tamanho solicitado e identidade do documento para cache.

**Saídas**

- document_info: pages, sizes após CropBox/rotação intrínseca e metadata (title, author, subject, creator, producer).
- Imagem de página concluída; render obsoleto não deve substituir o documento atual.

**Erros e casos excepcionais**

- Arquivo ausente, inválido, vazio ou protegido sem senha vazia válida: Falha do parser/worker; abertura não pode ser registrada como bem-sucedida. Mensagens e preservação do documento anterior precisam de teste GUI.
- Processo de renderização falha, excede tempo ou é cancelado: Erro/cancelamento sem publicar imagem parcial; subprocesso cancelável tem prazo próprio.

**Estado e efeitos**

- Cache local pode ser criado; original permanece sem edição.
- Abertura/fechamento muda o documento e invalida trabalhos da geração anterior.

**Critérios planejados**

- **S12-01-1** (nominal, contrato próprio atual, `not_run`): dado busca-escopos.pdf legível. Ação: Inspecionar e abrir as duas páginas. Esperado: pages=2; tamanhos positivos; a imagem de cada página pertence ao documento aberto.
- **S12-01-2** (exception, contrato próprio atual, `not_run`): dado Arquivo inexistente ou PDF inválido. Ação: Solicitar inspeção/abertura. Esperado: O parser/worker falha; não produzir uma página válida fictícia.

**Lacunas da referência Foxit**

- Comportamento Foxit para senha, corrupção, recuperação e todos os estados de abertura.
- O leitor atual não possui um fluxo completo de entrada de senha.

Fontes: [app/rendering.py](../app/rendering.py), [app/main.py](../app/main.py), [app/async_core.py](../app/async_core.py), [app/local_files.py](../app/local_files.py), [app/folder_dialogs.py](../app/folder_dialogs.py), [docs/PASTAS-SINCRONIZADAS.md](../docs/PASTAS-SINCRONIZADAS.md), [docs/ETAPA-11.md](../docs/ETAPA-11.md), [docs/windows-evidence/foxit-rea/ui-state-contracts-2026-10-16.json](../docs/windows-evidence/foxit-rea/ui-state-contracts-2026-10-16.json), [docs/REA-ESTATICA-BUSCA-IMPRESSAO-2026-10-18.md](../docs/REA-ESTATICA-BUSCA-IMPRESSAO-2026-10-18.md), [docs/REA-ESTATICA-CONTINUACAO-2026-10-18.md](../docs/REA-ESTATICA-CONTINUACAO-2026-10-18.md).

Testes próprios existentes, sem nova execução nesta tabela: [test_cache_distinguishes_documents](../tests/test_regressions.py); [test_latest_renderer_skips_obsolete_queue_entries](../tests/test_viewer.py); [test_final_name_is_absent_while_real_copy_is_in_progress](../tests/test_sync_folders.py); [test_save_copy_uses_worker_preserves_original_and_only_confirms_local_save](../tests/test_sync_folders_gtk.py).

Relacionados aos planos dinâmicos/UI: D01, D02, D13, D14, D15, D19, D20.

<a id="navigation"></a>

## Navegação/rotação/zoom

Navegar por página, aplicar zoom/ajuste e rotação de visualização, sem gravar a rotação no PDF. Fonte 0.1.8: Rotação visual anterior preservada; nova operação rotate-page salva /Rotate permanentemente em cópia, sem alterar caixas/página fonte. Fonte0.1.9: fluxo local de pasta preferida/últimas pastas e cópias novas com publicação completa/exclusiva. Envio remoto é do sincronizador externo; fonte/payload/sandbox290/290 aprovados; cliente real e portal em desktop ainda pendentes.

**Entradas**

- Documento carregado e índice solicitado; indicação UI usa página baseada em um.
- Ação anterior/próxima, percentual de zoom, ajustar página/largura ou giro.

**Saídas**

- Página exibida, zoom/posição e orientação atualizados.
- Resultados de busca/miniaturas navegam para destinos conhecidos.

**Erros e casos excepcionais**

- Página ou entrada textual fora do domínio: Não acessar índice inexistente; registrar a política atual de clamp/entrada no teste GUI.
- Render antigo termina depois de nova navegação: A geração atual prevalece; callback antigo não substitui a página selecionada.

**Estado e efeitos**

- Estado de leitura local; não altera a árvore de páginas do arquivo.
- Zoom/rotação devem conservar consistência entre texto, seleção e imagem.

**Critérios planejados**

- **S12-02-1** (nominal, contrato próprio atual, `not_run`): dado PDF de duas páginas na primeira página. Ação: Navegar para a segunda e girar a visualização. Esperado: Página selecionada é a segunda; transformação visual permanece coerente com a geometria.
- **S12-02-2** (exception, contrato próprio atual, `not_run`): dado Render da página anterior ainda em andamento. Ação: Mudar página e aguardar os callbacks. Esperado: O resultado obsoleto não toma o lugar da página atual.

**Lacunas da referência Foxit**

- Limites e modos efetivos Foxit dependem da classe/estado ativo.
- Updaters de zoom só enviam desabilitação nos limites; política completa não foi reconstruída.

Fontes: [app/main.py](../app/main.py), [app/page_cache.py](../app/page_cache.py), [app/rendering.py](../app/rendering.py), [app/pdf_changes.py](../app/pdf_changes.py), [app/edit_tasks.py](../app/edit_tasks.py), [app/worker_cli.py](../app/worker_cli.py), [docs/SEGURANCA-ACESSIBILIDADE.md](../docs/SEGURANCA-ACESSIBILIDADE.md), [app/local_files.py](../app/local_files.py), [app/folder_dialogs.py](../app/folder_dialogs.py), [docs/PASTAS-SINCRONIZADAS.md](../docs/PASTAS-SINCRONIZADAS.md), [docs/ETAPA-11.md](../docs/ETAPA-11.md), [docs/windows-evidence/foxit-rea/ui-state-contracts-2026-10-16.json](../docs/windows-evidence/foxit-rea/ui-state-contracts-2026-10-16.json), [docs/windows-evidence/foxit-rea/zoom-presets.json](../docs/windows-evidence/foxit-rea/zoom-presets.json), [docs/REA-ESTATICA-BUSCA-IMPRESSAO-2026-10-18.md](../docs/REA-ESTATICA-BUSCA-IMPRESSAO-2026-10-18.md), [docs/REA-ESTATICA-CONTINUACAO-2026-10-18.md](../docs/REA-ESTATICA-CONTINUACAO-2026-10-18.md).

Testes próprios existentes, sem nova execução nesta tabela: [test_search_navigation_selection_and_rotation](../tests/test_gui.py); [test_intrinsic_rotation_and_cropbox_match_text_geometry](../tests/test_regressions.py); [test_five_panel_headers_fit_default_and_small_window](../tests/test_sidebar_layout_gtk.py); [test_combined_edits_preserve_tree_destinations_geometry_and_source](../tests/test_extended_edits.py); [test_final_name_is_absent_while_real_copy_is_in_progress](../tests/test_sync_folders.py); [test_save_copy_uses_worker_preserves_original_and_only_confirms_local_save](../tests/test_sync_folders_gtk.py).

Relacionados aos planos dinâmicos/UI: D03, UI03, UI04.

<a id="presentation"></a>

## Apresentação ajustar/preencher

Apresentação GTK com ajustar/preencher, pan, zoom e ponteiro; não implica suporte a mídia embutida.

**Entradas**

- Documento, tamanhos de página, página inicial e dimensões do monitor/view.
- Ações de navegação, fit/fill, pan e cor do ponteiro.

**Saídas**

- Janela de apresentação com página assíncrona e imagem centralizada/recortada segundo o modo.
- Estado de erro visível quando a renderização falha.

**Erros e casos excepcionais**

- Renderização falha: A janela registra o erro; não reutilizar imagem de documento diferente.
- Janela fecha durante tarefa: Cancelar/descartar tarefas e impedir atualização de widgets destruídos.

**Estado e efeitos**

- Estado de tela/ponteiro é local; original não é modificado.

**Critérios planejados**

- **S12-03-1** (nominal, contrato próprio atual, `not_run`): dado Página retrato e viewport paisagem. Ação: Alternar ajustar página e preencher. Esperado: A escala e o centro respeitam o modo próprio; não atribuir esse cálculo ao Foxit.
- **S12-03-2** (exception, contrato próprio atual, `not_run`): dado Worker retorna falha de imagem. Ação: Entregar o erro à apresentação. Esperado: Exibir estado de falha, mantendo o ciclo de vida da janela válido.

**Lacunas da referência Foxit**

- Ajuste/preenchimento, atalhos e múltiplos monitores do original não foram observados.

Fontes: [app/presentation.py](../app/presentation.py), [app/page_cache.py](../app/page_cache.py), [docs/FOXIT-REA.md](../docs/FOXIT-REA.md).

Testes próprios existentes, sem nova execução nesta tabela: [test_presentation_fit_fill_center_and_error](../tests/test_viewer.py); [test_presentation_handles_portrait_and_landscape](../tests/test_viewer.py).

Relacionados aos planos dinâmicos/UI: D03.

<a id="search-text"></a>

## Busca literal/palavra inteira/maiúsculas

Busca literal em texto de páginas, com caixa/palavra inteira e extensões próprias de acentos/hifenização.

**Entradas**

- Consulta de até 256 caracteres; opções imutáveis; max_hits padrão 5000.
- Identidade do arquivo, cancelamento e callback de lotes por página.

**Saídas**

- Lista ordenada de ocorrências com source=page_text, page, width, height, rects, text e snippet.
- Somente geometria conhecida é destacada; texto segue NFC/casefold segundo a opção.

**Erros e casos excepcionais**

- Consulta maior que 256 caracteres: ValueError; nenhuma busca é iniciada.
- Arquivo mudou após indexação: RuntimeError pedindo reabertura; não reutilizar resultados antigos.
- Consulta vazia, max_hits<=0 ou cancelamento prévio: Lista vazia; cancelamento posterior preserva apenas resultados já emitidos.

**Estado e efeitos**

- Cache limitado por páginas e identidade do arquivo.
- Sem fonte selecionada, a UI pede uma fonte; preferência de destaque não refaz a busca.

**Critérios planejados**

- **S12-04-1** (nominal, contrato próprio atual, `not_run`): dado Fixture de busca; só páginas, sem caixa/palavra inteira. Ação: Pesquisar alvo. Esperado: Contrato próprio: três ocorrências; palavra inteira reduz para duas.
- **S12-04-2** (exception, contrato próprio atual, `not_run`): dado Consulta com 257 caracteres. Ação: Chamar TextSearchIndex.search. Esperado: ValueError antes de extrair páginas.

**Lacunas da referência Foxit**

- Normalização e algoritmos completos do Foxit; ordem/limites/destaques precisam de comparação.

Fontes: [app/search_engine.py](../app/search_engine.py), [app/main.py](../app/main.py), [app/rendering.py](../app/rendering.py), [docs/REA-BUSCA-IMPRESSAO.md](../docs/REA-BUSCA-IMPRESSAO.md), [docs/windows-evidence/foxit-rea/search-print-contracts.json](../docs/windows-evidence/foxit-rea/search-print-contracts.json), [docs/REA-ESTATICA-CONTINUACAO-2026-10-18.md](../docs/REA-ESTATICA-CONTINUACAO-2026-10-18.md).

Testes próprios existentes, sem nova execução nesta tabela: [test_options_and_real_pdf](../tests/test_search.py); [test_global_limit_progress_and_cancel_cover_metadata](../tests/test_search_scopes.py); [test_highlight_preference_and_navigation_change_pixels_without_new_search](../tests/test_search_highlights.py).

Relacionados aos planos dinâmicos/UI: D04, D05, D06, D10, D11, D12, UI08.

<a id="search-bookmarks"></a>

## Busca em marcadores

Pesquisa em títulos de marcadores; leitura e navegação não equivalem a edição/persistência.

**Entradas**

- Consulta e flags; include_bookmarks=True, demais fontes conforme seleção.
- Títulos, nível e destinos locais conhecidos; página ausente fica null.

**Saídas**

- Hits source=bookmark, rects=[] e destino local ou page=null.
- Na busca combinada, marcadores vêm após o texto de páginas no contrato próprio.

**Erros e casos excepcionais**

- Destino não resolvido: Resultado continua sem página; não inventar destino nem retângulo.
- Documento mudou: Rejeitar o cache e pedir reabertura.

**Estado e efeitos**

- Metadados são cacheados por identidade; seleção pode navegar, sem editar o outline.

**Critérios planejados**

- **S12-05-1** (nominal, contrato próprio atual, `not_run`): dado Fixture com dois títulos contendo alvo, só marcadores. Ação: Pesquisar alvo e selecionar os resultados. Esperado: Dois hits; um aponta à segunda página e outro permanece page=null; rects=[] em ambos.
- **S12-05-2** (exception, contrato próprio atual, `not_run`): dado Hit de marcador sem destino local. Ação: Selecionar esse resultado. Esperado: Não fabricar página de destino ou retângulo de destaque.

**Lacunas da referência Foxit**

- Classe dos IDs 7911/7913 e comportamento de busca/navegação Foxit.
- A junção estrutural de ID 7913 ao handler de +0x1d58 continua ambígua.

Fontes: [app/search_engine.py](../app/search_engine.py), [app/pdf_panels.py](../app/pdf_panels.py), [docs/REA-BUSCA-IMPRESSAO.md](../docs/REA-BUSCA-IMPRESSAO.md), [docs/windows-evidence/foxit-rea/search-print-contracts.json](../docs/windows-evidence/foxit-rea/search-print-contracts.json), [docs/windows-evidence/foxit-rea/search-checkbox-bindings.json](../docs/windows-evidence/foxit-rea/search-checkbox-bindings.json), [docs/REA-ESTATICA-CONTINUACAO-2026-10-18.md](../docs/REA-ESTATICA-CONTINUACAO-2026-10-18.md).

Testes próprios existentes, sem nova execução nesta tabela: [test_bookmark_without_local_page_is_not_given_a_fake_destination](../tests/test_search_scopes.py); [test_ui_toggles_scopes_and_navigates_bookmark_result](../tests/test_search_scopes.py).

Relacionados aos planos dinâmicos/UI: D07, UI06.

<a id="search-comments"></a>

## Busca em comentários

Busca em assunto/conteúdo de comentários, sem pesquisar autor no contrato atual.

**Entradas**

- Consulta, flags e include_comments=True; comentários com página associada.
- As demais fontes podem ficar desativadas.

**Saídas**

- Hits source=comment, página conhecida e rects=[].
- Assunto e conteúdo são pesquisáveis; autor é apenas metadado de painel.

**Erros e casos excepcionais**

- Sem texto pesquisável ou termo ausente: Nenhum hit correspondente; não tratar ausência como falha de motor.
- Cache pertence a arquivo alterado: Falhar e pedir reabertura antes de publicar novos resultados.

**Estado e efeitos**

- A leitura não cria nem altera anotações; pode navegar à página.

**Critérios planejados**

- **S12-06-1** (nominal, contrato próprio atual, `not_run`): dado Só comentários da fixture. Ação: Pesquisar assunto, depois alvo. Esperado: Uma ocorrência em cada consulta; o campo assunto é separado do conteúdo.
- **S12-06-2** (exception, contrato próprio atual, `not_run`): dado Só comentários, consulta Autor. Ação: Pesquisar com o contrato atual. Esperado: Zero hits pelo autor, mesmo que o painel o exponha.

**Lacunas da referência Foxit**

- Campos e tipos pesquisados no Foxit; política de autor, assunto, replies e ordem.

Fontes: [app/search_engine.py](../app/search_engine.py), [app/pdf_panels.py](../app/pdf_panels.py), [docs/REA-BUSCA-IMPRESSAO.md](../docs/REA-BUSCA-IMPRESSAO.md), [docs/windows-evidence/foxit-rea/search-print-contracts.json](../docs/windows-evidence/foxit-rea/search-print-contracts.json), [docs/REA-ESTATICA-CONTINUACAO-2026-10-18.md](../docs/REA-ESTATICA-CONTINUACAO-2026-10-18.md).

Testes próprios existentes, sem nova execução nesta tabela: [test_comment_subject_and_contents_are_searchable_without_author](../tests/test_search_scopes.py).

Relacionados aos planos dinâmicos/UI: D08, D09.

<a id="search-attachments"></a>

## Busca em anexos

Fonte0.1.6: busca em anexos UTF-8 e texto de PDF de catálogo/árvores/anotações, com omissões explícitas e sem execução/recursão.

**Entradas**

- PDF host, consulta literal/coringa/proximidade, flags e seletor de anexos.
- Até100 anexos;2MiB por payload/8MiB total,100 páginas e2MiB de texto por anexo; limites pós-decodificação.

**Saídas**

- Hits com índice/nome/SHA256 do anexo, hash do host e página interna; sem página/retângulo do host inventado.
- Omissões e possível corte expostos separadamente, inclusive na UI.

**Erros e casos excepcionais**

- Formato não suportado, bytes inválidos, PDF cifrado ou limite: Omitir esse anexo com razão e declarar pesquisa parcial.
- Host alterado/estrutura inválida ou worker indisponível: Falhar sem afirmar cobertura completa; cancelar encerra o worker.

**Estado e efeitos**

- Sem execução/exportação de anexos ou alteração da fonte; worker cancelável.
- Sem OCR, recursão de anexos internos, portfólios ou senha; limite real aplicado após extração.

**Critérios planejados**

- **S12-07-1** (nominal, contrato próprio atual, `not_run`): dado PDF sintético com anexo textual contendo alvo; fixture ainda a especializar. Ação: Pesquisar incluindo anexos. Esperado: Encontrar o termo no anexo suportado e identificar índice/nome/página interna sem destino principal fictício.
- **S12-07-2** (exception, contrato próprio atual, `not_run`): dado Mesmo PDF com um anexo não suportado. Ação: Pesquisar incluindo anexos. Esperado: Informar o anexo omitido e seu motivo; UI deve indicar anexos parciais.

**Lacunas da referência Foxit**

- Travessia completa, extratores, formatos, limites, ordenação e associação de resultados no original.

Fontes: [app/attachment_search.py](../app/attachment_search.py), [app/search_tasks.py](../app/search_tasks.py), [app/search_matching.py](../app/search_matching.py), [app/pdf_attachments.py](../app/pdf_attachments.py), [app/search_engine.py](../app/search_engine.py), [app/worker_cli.py](../app/worker_cli.py), [app/main.py](../app/main.py), [docs/REA-BUSCA-IMPRESSAO.md](../docs/REA-BUSCA-IMPRESSAO.md), [docs/windows-evidence/foxit-rea/search-print-contracts.json](../docs/windows-evidence/foxit-rea/search-print-contracts.json), [docs/REA-ESTATICA-CONTINUACAO-2026-10-18.md](../docs/REA-ESTATICA-CONTINUACAO-2026-10-18.md).

Testes próprios existentes, sem nova execução nesta tabela: [test_embedded_pdf_page_is_distinct_from_host_and_model_keeps_scope](../tests/test_attachment_search.py); [test_unsupported_invalid_utf8_malformed_and_encrypted_pdf_report_omissions](../tests/test_attachment_search.py); [test_cancellation_terminates_the_actual_child_and_does_not_create_files](../tests/test_attachment_search.py); [test_attachment_scope_displays_partial_coverage_and_distinct_identity](../tests/test_search_extensions_gtk.py); [test_old_attachment_results_do_not_repopulate_another_document](../tests/test_search_extensions_gtk.py).

Relacionados aos planos dinâmicos/UI: D16.

<a id="search-index"></a>

## Índice persistente/pesquisa de coleção

Fonte0.1.6: snapshot JSON local versionado de texto de PDFs explicitamente escolhidos, com consulta e exclusão de fontes desatualizadas.

**Entradas**

- Lista explícita de1–100 PDFs e arquivo .linuxit-index.json escolhido para criação/atualização.
- Consulta/flags/mode; até64MiB por fonte/256MiB total,1000 páginas,16MiB texto e64MiB índice.

**Saídas**

- Índice próprio versionado com SHA256 do corpo/fontes; varredura de texto durante consulta, sem formato Lucene/FTS.
- Hits identificam caminho absoluto/SHA256/página e fontes alteradas são excluídas;5000 hits/350 linhas na UI com aviso.

**Erros e casos excepcionais**

- Fonte ausente/alterada após indexação: Excluir seus hits e indicar atualização explícita; revalidar antes de abrir resultado.
- Índice inválido, fonte criptografada ou falha de gravação: Recusar operação; preservar índice anterior íntegro e limpar temporário em falhas tratadas.

**Estado e efeitos**

- Não varrer pastas automaticamente nem alterar PDFs; gravação só no destino escolhido.
- Índice contém texto e caminhos locais; não é portátil entre máquinas e não faz OCR.
- Atualização revalida fontes/índice e usa temporário/os.replace; cancelamento forçado pode deixar temporário ou ocorrer após commit.

**Critérios planejados**

- **S12-08-1** (nominal, contrato próprio atual, `not_run`): dado Coleção sintética de dois documentos e índice em pasta nova. Ação: Construir índice e consultar um termo presente em um documento. Esperado: Criar/reabrir índice e localizar termo no PDF/página corretos, sem alterar fontes.
- **S12-08-2** (exception, contrato próprio atual, `not_run`): dado Uma fonte foi alterada após indexação. Ação: Consultar sem atualização completa. Esperado: Excluir a fonte alterada e indicar que precisa atualizar o índice.

**Lacunas da referência Foxit**

- Formato e manutenção do índice completo, exclusões, locking, recuperação e disponibilidade Reader.

Fontes: [app/collection_index.py](../app/collection_index.py), [app/collection_window.py](../app/collection_window.py), [app/search_tasks.py](../app/search_tasks.py), [app/search_matching.py](../app/search_matching.py), [app/worker_cli.py](../app/worker_cli.py), [app/main.py](../app/main.py), [docs/windows-evidence/foxit-rea/index-interface.json](../docs/windows-evidence/foxit-rea/index-interface.json), [docs/FOXIT-REA.md](../docs/FOXIT-REA.md), [docs/REA-ESTATICA-BUSCA-IMPRESSAO-2026-10-18.md](../docs/REA-ESTATICA-BUSCA-IMPRESSAO-2026-10-18.md), [docs/REA-ESTATICA-CONTINUACAO-2026-10-18.md](../docs/REA-ESTATICA-CONTINUACAO-2026-10-18.md).

Testes próprios existentes, sem nova execução nesta tabela: [test_build_reopen_worker_and_query_preserve_sources_and_real_pages](../tests/test_collection_index.py); [test_changed_missing_sources_are_excluded_until_explicit_rebuild](../tests/test_collection_index.py); [test_update_failure_preserves_old_index_and_removes_temporary](../tests/test_collection_index.py); [test_collection_build_query_and_open_result_on_its_actual_page](../tests/test_search_extensions_gtk.py); [test_collection_changed_result_is_refused_before_opening](../tests/test_search_extensions_gtk.py); [test_closing_collection_terminates_pending_worker_without_callbacks](../tests/test_search_extensions_gtk.py).

<a id="search-language"></a>

## Stemming/proximidade/coringas

Fonte0.1.6: coringas por palavra e proximidade ordenada com contratos próprios; stemming/idiomas/Lucene ainda pendentes.

**Entradas**

- Consulta de até256 caracteres antes da normalização e modo explícito.
- Coringa: um padrão até64 caracteres normalizados, até8* ou?; proximidade:2–8 palavras ordenadas/distância total0–50.

**Saídas**

- Hits não sobrepostos; proximidade destaca intervalo com palavras intermediárias, sem cruzar bloco/página do documento.
- Mesma semântica para páginas, metadados, anexos e coleção, respeitando fronteiras de extração.

**Erros e casos excepcionais**

- Padrão/sintaxe/modo ou distância inválida: Erro explícito, sem reinterpretar silenciosamente como literal.
- Palavra acima de4096 caracteres nos modos avançados: Recusar operação ou omitir anexo com razão; não executar regex nem expansão ilimitada.

**Estado e efeitos**

- Preservar modo literal, inclusive* e? literais e casefold com expansão Unicode.
- NFC/casefold e opção de acentos compartilhados; palavra inteira só precisa de flag no modo literal.
- Stemming não implementado e não exposto como recurso funcional.

**Critérios planejados**

- **S12-09-1** (nominal, contrato próprio atual, `not_run`): dado Corpus sintético com duas palavras separadas por distâncias conhecidas. Ação: Executar proximidade com duas distâncias explícitas. Esperado: Duas consultas com distâncias diferentes produzem hits conforme distância total/ordem documentadas.
- **S12-09-2** (exception, contrato próprio atual, `not_run`): dado Consulta com coringa/operador cuja sintaxe não foi implementada. Ação: Executar esse modo. Esperado: Recusar sintaxe/operador não suportado sem trocar silenciosamente para literal.

**Lacunas da referência Foxit**

- Stemming por idioma, distância/proximidade, escaping, expansão e combinações com índice.

Fontes: [app/search_matching.py](../app/search_matching.py), [app/search_engine.py](../app/search_engine.py), [app/attachment_search.py](../app/attachment_search.py), [app/collection_index.py](../app/collection_index.py), [app/main.py](../app/main.py), [app/collection_window.py](../app/collection_window.py), [docs/REA-BUSCA-IMPRESSAO.md](../docs/REA-BUSCA-IMPRESSAO.md), [docs/windows-evidence/foxit-rea/search-print-contracts.json](../docs/windows-evidence/foxit-rea/search-print-contracts.json), [docs/ETAPA-11.md](../docs/ETAPA-11.md), [docs/REA-ESTATICA-BUSCA-IMPRESSAO-2026-10-18.md](../docs/REA-ESTATICA-BUSCA-IMPRESSAO-2026-10-18.md), [docs/REA-ESTATICA-CONTINUACAO-2026-10-18.md](../docs/REA-ESTATICA-CONTINUACAO-2026-10-18.md).

Testes próprios existentes, sem nova execução nesta tabela: [test_proximity_uses_total_intervening_words_and_query_order](../tests/test_search_modes.py); [test_invalid_syntax_distance_and_expansion_are_rejected](../tests/test_search_modes.py); [test_page_geometry_keeps_owner_rectangles_for_both_modes](../tests/test_search_modes.py); [test_mode_controls_geometry_distance_and_bad_syntax](../tests/test_search_extensions_gtk.py).

Relacionados aos planos dinâmicos/UI: UI07.

<a id="selection"></a>

## Seleção/cópia/snapshot

Seleção retangular de palavras e cópia; snapshot de região; sem garantir ordem semântica ou permissões completas.

**Entradas**

- Retângulo em pixels e transformação da página atual.
- Mapa de palavras ou imagem da página; ação de copiar/snapshot.

**Saídas**

- Texto de palavras intersectadas, agrupado por bloco/linha; cópia para clipboard.
- Snapshot de região visual ou exportação de página em PNG segundo a ação.

**Erros e casos excepcionais**

- Nenhuma palavra intersecta a seleção: Status de nenhum texto; não copiar texto inventado.
- Extração falha ou documento/página muda: Erro ou descarte do resultado antigo; não copiar conteúdo de outro documento.

**Estado e efeitos**

- Pode alterar clipboard ou gerar arquivo solicitado; não editar PDF.
- Permissões PDF e seleção semântica completa não estão estabelecidas.

**Critérios planejados**

- **S12-10-1** (nominal, contrato próprio atual, `not_run`): dado PDF sintético e retângulo contendo uma palavra conhecida. Ação: Selecionar e copiar. Esperado: Clipboard contém a palavra selecionada; a seleção acompanha a transformação da imagem.
- **S12-10-2** (exception, contrato próprio atual, `not_run`): dado Retângulo sobre região sem texto. Ação: Concluir seleção de texto. Esperado: Status informa ausência de texto; nenhum conteúdo fictício é produzido.

**Lacunas da referência Foxit**

- Ordem lógica, texto bidirecional, permissões de cópia, snapping e coordenadas de todos os modos do original.

Fontes: [app/main.py](../app/main.py), [app/rendering.py](../app/rendering.py), [docs/FOXIT-REA.md](../docs/FOXIT-REA.md).

Testes próprios existentes, sem nova execução nesta tabela: [test_search_navigation_selection_and_rotation](../tests/test_gui.py); [test_intrinsic_rotation_and_cropbox_match_text_geometry](../tests/test_regressions.py).

<a id="printing"></a>

## Prévia/plano de impressão

Preparar PDF de saída, mostrar prévia e enviar ao backend escolhido; envio não comprova impressão física.

**Entradas**

- PDF, intervalo, subconjunto par/ímpar, ordem, papel, orientação e modo.
- Destino save-pdf, impressora CUPS ou adaptador Windows; opções específicas do backend.

**Saídas**

- PDF preparado e prévia; em salvar PDF, arquivo no destino solicitado.
- Em CUPS, resposta de aceitação/erro do comando lp; Windows usa o adaptador próprio.

**Erros e casos excepcionais**

- Nenhuma impressora ou comando lp ausente: Backend recusa envio com mensagem; salvar PDF é um destino independente.
- Worker de preparação falha ou ultrapassa prazo: Erro; não enviar ao spooler saída reconhecida como incompleta.
- Rasterização excede 45 MP por página: Recusar a preparação como imagem; DPI atual é limitado entre 72 e 600.

**Estado e efeitos**

- Gera PDF temporário; impressão física tem efeito externo somente após ação de envio.
- Testes nesta fase devem usar salvar/cancelar ou backend simulado; sem impressoras do host na VM.

**Critérios planejados**

- **S12-11-1** (nominal, contrato próprio atual, `not_run`): dado Fixture e destino Salvar como PDF. Ação: Preparar saída e reabri-la. Esperado: Arquivo reabre e preserva o plano escolhido; sucesso de geração não é prova de impressão física.
- **S12-11-2** (exception, contrato próprio atual, `not_run`): dado Comando lp indisponível. Ação: Solicitar envio ao CUPS. Esperado: RuntimeError explícito; nenhum sucesso de envio é reportado.

**Lacunas da referência Foxit**

- Predefinições, margens, fontes, flags, spooler físico e estados completos do original.

Fontes: [app/print_window.py](../app/print_window.py), [app/worker_cli.py](../app/worker_cli.py), [app/cups_backend.py](../app/cups_backend.py), [app/windows_print.py](../app/windows_print.py), [docs/REA-IMPRESSAO-CONSUMIDORES.md](../docs/REA-IMPRESSAO-CONSUMIDORES.md), [docs/windows-evidence/foxit-rea/windows-print-followup-contracts.json](../docs/windows-evidence/foxit-rea/windows-print-followup-contracts.json), [docs/AVANCO-SEM-VM.md](../docs/AVANCO-SEM-VM.md), [docs/REA-ESTATICA-BUSCA-IMPRESSAO-2026-10-18.md](../docs/REA-ESTATICA-BUSCA-IMPRESSAO-2026-10-18.md), [docs/REA-ESTATICA-CONTINUACAO-2026-10-18.md](../docs/REA-ESTATICA-CONTINUACAO-2026-10-18.md).

Testes próprios existentes, sem nova execução nesta tabela: [test_booklet_preview_sides_binding_and_submit](../tests/test_gui.py); [test_manual_booklet_sides_are_not_duplex](../tests/test_regressions.py).

Relacionados aos planos dinâmicos/UI: D17, UI02, UI05.

<a id="imposition"></a>

## Livreto/N-up/mosaico

Composição independente em livreto, N-up e mosaico, herdada da base MIT e adaptada.

**Entradas**

- Índices selecionados, ordem, papel e orientação.
- N-up em {1,2,4,6,9,16}; livreto com binding/lados; mosaico com escala/sobreposição/área imprimível.

**Saídas**

- PDF de faces/folhas; ordem e páginas em branco conforme modo.
- Livreto separa ambas/frente/verso; frente/verso manual não solicita duplex automático.
- Na fonte pós-0.1.1, conteúdo/caixas são normalizados para a origem do CropBox após rotação; a cópia não substitui o stream do reader original. Ver docs/ETAPA-19.md.

**Erros e casos excepcionais**

- N-up fora do conjunto, incluindo quantidade fracionária: ValueError; não preparar saída como se a quantidade fosse válida.
- Mosaico excede limites próprios de folhas: ValueError; limitar a expansão do trabalho antes de gerar saída excessiva.

**Estado e efeitos**

- Somente arquivo de saída; nenhum envio físico nesta função.
- Escalas e margens próprias não são apresentadas como geometria reconstruída do Foxit.

**Critérios planejados**

- **S12-12-1** (nominal, contrato próprio atual, `not_run`): dado PDF sintético de oito páginas. Ação: Gerar livreto em ambos os lados e reabrir. Esperado: Quatro faces; ordem das duplas própria verificável, sem alterar o original.
- **S12-12-2** (exception, contrato próprio atual, `not_run`): dado pages_per_sheet=4.5. Ação: Preparar modo multiple. Esperado: ValueError, sem aceitar silenciosamente uma quantidade inteira diferente.

**Lacunas da referência Foxit**

- Geometria completa, rotações, margens e ordenação de todas as combinações no Foxit.

Fontes: [app/imposition.py](../app/imposition.py), [app/worker_cli.py](../app/worker_cli.py), [docs/REA-IMPRESSAO-CONSUMIDORES.md](../docs/REA-IMPRESSAO-CONSUMIDORES.md), [docs/windows-evidence/foxit-rea/windows-print-followup-contracts.json](../docs/windows-evidence/foxit-rea/windows-print-followup-contracts.json), [docs/AVANCO-SEM-VM.md](../docs/AVANCO-SEM-VM.md), [docs/REA-ESTATICA-BUSCA-IMPRESSAO-2026-10-18.md](../docs/REA-ESTATICA-BUSCA-IMPRESSAO-2026-10-18.md), [docs/REA-ESTATICA-CONTINUACAO-2026-10-18.md](../docs/REA-ESTATICA-CONTINUACAO-2026-10-18.md).

Testes próprios existentes, sem nova execução nesta tabela: [test_booklet_generated_sides_and_binding](../tests/test_regressions.py); [test_nup_worker_rejects_fractional_count](../tests/test_regressions.py); [test_worker_prepares_nup_and_poster](../tests/test_regressions.py); [test_actual_size_centers_the_visible_crop_not_the_media_origin](../tests/test_imposition_cropbox.py); [test_intrinsic_rotation_keeps_shifted_crop_aligned](../tests/test_imposition_cropbox.py); [test_inputs_and_in_memory_page_geometry_are_preserved](../tests/test_imposition_cropbox.py); [test_poster_single_sheet_and_tiles_keep_crop_placement_without_marks](../tests/test_imposition_cropbox.py).

Relacionados aos planos dinâmicos/UI: D18.

<a id="bookmarks-edit"></a>

## Criar/mover/gravar marcadores

Fonte0.1.10: criar/renomear, mover subárvore por pai/posição e excluir subárvore em cópia; ligações, destinos e contagens preservados no subconjunto. Histórico de rascunho permite desfazer/refazer antes de salvar; cópias já salvas preservadas.

**Entradas**

- PDF local não criptografado, sem assinatura/Perms/XFA/Collection, fonte identificada por SHA-256.
- Operação selecionada, página base zero para marcador/nota ou nome do campo Tx e texto; destino novo com pasta existente.
- Operação adicional de formulário/árvore/anotação descrita em docs/EDICAO-COM-HISTORICO.md; histórico de até100 passos.

**Saídas**

- Cópia PDF nova e exclusiva, fonte identificada por hash e preservada; rascunho validado após cada operação.
- UI de histórico com desfazer/refazer no rascunho; cópias já salvas preservadas. GTK/Linux exercitado;333/333 por ambiente fonte/payload/sandbox, sem observação original.

**Erros e casos excepcionais**

- Fonte mudou ou destino já existe, inclusive o próprio original: Recusar a gravação; não sobrescrever arquivos.
- PDF criptografado, assinatura/campo Sig, Perms, XFA ou Collection: Recurso não suportado para gravação; não remover proteção ou invalidar assinatura.
- Operação/índice/texto/retângulo inválido; campo ausente, não Tx, ReadOnly ou MaxLen excedido: Falha antes de publicar destino; lote não é aplicado parcialmente à fonte.
- Controle/aparência/opção/árvore/anotação fora do subconjunto ou origem alterada: Recusar a alteração sem avançar o histórico ou publicar uma cópia parcial em falha tratada.

**Estado e efeitos**

- Fonte clonada em memória; gravação temporária privada, reabertura e rechecagem de identidade antes da criação exclusiva do destino.
- Falhas tratadas removem arquivo novo criado; término forçado/timeout pode deixar temporário ou saída parcial e exige conferir destino.
- Não executar ações ou scripts PDF. Sem persistência em cima do original e sem garantia de preservação de assinatura; documentos com assinatura são recusados.
- Confirmação capturada por documento/geração; reabrir o mesmo caminho durante diálogo invalida a operação antiga.
- Reconstituir cópia temporária e inspecionar antes de avançar histórico; falha mantém cursor/refazer e original; fechar cancela worker. Gravação interrompida exige conferir destino.

**Critérios planejados**

- **S12-13-1** (nominal, contrato próprio atual, `not_run`): dado Fixture com dois marcadores. Ação: Inspecionar o painel. Esperado: Dois títulos, nível registrado e destino local conhecido ou null; nenhuma escrita no PDF.
- **S12-13-2** (exception, contrato próprio atual, `not_run`): dado Marcador sem página local. Ação: Exibir seu destino. Esperado: Não atribuir a primeira página por padrão.

**Lacunas da referência Foxit**

- Disponibilidade Reader dos diálogos, movimento hierárquico, undo/redo e persistência.

Fontes: [app/pdf_panels.py](../app/pdf_panels.py), [app/pdf_changes.py](../app/pdf_changes.py), [app/edit_tasks.py](../app/edit_tasks.py), [app/worker_cli.py](../app/worker_cli.py), [app/main.py](../app/main.py), [docs/SEGURANCA-ACESSIBILIDADE.md](../docs/SEGURANCA-ACESSIBILIDADE.md), [app/local_files.py](../app/local_files.py), [app/folder_dialogs.py](../app/folder_dialogs.py), [docs/PASTAS-SINCRONIZADAS.md](../docs/PASTAS-SINCRONIZADAS.md), [app/pdf_form_controls.py](../app/pdf_form_controls.py), [app/edit_history.py](../app/edit_history.py), [app/edit_dialogs.py](../app/edit_dialogs.py), [app/edit_window.py](../app/edit_window.py), [docs/EDICAO-COM-HISTORICO.md](../docs/EDICAO-COM-HISTORICO.md), [testes/resultados/0.1.10/validation-review.json](../testes/resultados/0.1.10/validation-review.json), [docs/FOXIT-REA.md](../docs/FOXIT-REA.md), [docs/ETAPA-11.md](../docs/ETAPA-11.md).

Testes próprios existentes, sem nova execução nesta tabela: [test_bookmark_without_local_page_is_not_given_a_fake_destination](../tests/test_search_scopes.py); [test_combined_copy_preserves_source_metadata_attachment_and_previous_objects](../tests/test_pdf_changes.py); [test_encryption_signature_permissions_xfa_and_portfolio_are_explicitly_unsupported](../tests/test_pdf_changes.py); [test_real_dialogs_and_worker_create_bookmark_note_and_form_copies](../tests/test_copy_edit_gtk.py); [test_reopening_same_document_during_dialog_blocks_stale_save](../tests/test_copy_edit_gtk.py); [test_existing_destination_is_preserved_and_busy_state_is_released](../tests/test_copy_edit_gtk.py); [test_combined_edits_preserve_tree_destinations_geometry_and_source](../tests/test_extended_edits.py); [test_final_name_is_absent_while_real_copy_is_in_progress](../tests/test_sync_folders.py); [test_save_copy_uses_worker_preserves_original_and_only_confirms_local_save](../tests/test_sync_folders_gtk.py); [test_info_distinguishes_checkbox_radio_choice_combo_and_multiselect](../tests/test_advanced_edits.py); [test_checkbox_sets_and_clears_value_and_visible_appearance](../tests/test_advanced_edits.py); [test_radio_activates_only_the_selected_widget_and_can_clear](../tests/test_advanced_edits.py); [test_radio_no_toggle_off_is_enforced](../tests/test_advanced_edits.py); [test_single_and_combo_values_indices_and_generated_appearances_roundtrip](../tests/test_advanced_edits.py); [test_multiselect_uses_export_values_and_canonical_indices](../tests/test_advanced_edits.py); [test_choice_selection_can_be_cleared](../tests/test_advanced_edits.py); [test_invalid_values_do_not_publish_partial_batch](../tests/test_advanced_edits.py); [test_read_only_and_unsupported_button_appearance_are_explicit](../tests/test_advanced_edits.py); [test_editable_combo_and_duplicate_exports_are_rejected](../tests/test_advanced_edits.py); [test_inherited_checkbox_flags_and_type_are_respected](../tests/test_advanced_edits.py); [test_checkbox_widget_absent_from_pages_is_unsupported](../tests/test_advanced_edits.py); [test_closed_outline_counts_remain_closed_after_move](../tests/test_advanced_edits.py); [test_move_preserves_subtree_destinations_and_sibling_links](../tests/test_advanced_edits.py); [test_move_child_to_root_and_reorder_same_parent](../tests/test_advanced_edits.py); [test_delete_bookmark_removes_subtree_and_last_root](../tests/test_advanced_edits.py); [test_move_into_descendant_invalid_positions_and_boolean_paths_are_refused](../tests/test_advanced_edits.py); [test_highlight_and_rectangle_roundtrip_geometry_print_flags_and_text](../tests/test_advanced_edits.py); [test_delete_supported_annotation_preserves_widgets_and_other_pages](../tests/test_advanced_edits.py); [test_locked_notes_widgets_and_replies_are_not_deleted](../tests/test_advanced_edits.py); [test_invalid_annotation_geometry_and_extra_parameters_are_rejected](../tests/test_advanced_edits.py); [test_undo_redo_rebuild_actual_pdfs_and_save_current_cursor_only](../tests/test_edit_history.py); [test_undo_all_restores_base_and_disables_save_until_redone](../tests/test_edit_history.py); [test_new_branch_discards_redo_but_invalid_branch_preserves_it](../tests/test_edit_history.py); [test_operation_values_are_defensively_copied](../tests/test_edit_history.py); [test_changed_original_blocks_add_undo_redo_and_save](../tests/test_edit_history.py); [test_existing_destination_is_not_overwritten_and_draft_survives](../tests/test_edit_history.py); [test_closed_session_refuses_work_and_removes_private_previews](../tests/test_edit_history.py); [test_pre_cancelled_session_does_not_start_worker](../tests/test_edit_history.py); [test_buttons_undo_redo_save_selected_history_and_preserve_prior_copy](../tests/test_edit_draft_gtk.py); [test_real_form_dialog_checkbox_radio_list_and_multiselect](../tests/test_edit_draft_gtk.py); [test_real_move_and_delete_bookmark_dialogs_use_updated_paths](../tests/test_edit_draft_gtk.py); [test_real_area_annotation_dialog_and_delete_keep_other_annotations](../tests/test_edit_draft_gtk.py); [test_failed_operation_and_existing_destination_keep_history_usable](../tests/test_edit_draft_gtk.py); [test_cancel_dialog_and_reopen_parent_close_draft_without_publishing](../tests/test_edit_draft_gtk.py); [test_cancelling_save_and_repeated_clicks_do_not_duplicate_writes](../tests/test_edit_draft_gtk.py); [test_saved_form_and_highlight_render_with_poppler](../tests/test_edit_draft_gtk.py).

Relacionados aos planos dinâmicos/UI: D07, UI09, UI10.

<a id="annotations"></a>

## Anotações/undo/gravação

Fonte0.1.10: criar/editar Text, acrescentar Highlight de área e Square, excluir esses três tipos desbloqueados sem dependentes. Histórico de rascunho com desfazer/refazer; sem redação, apagamento seguro, popup/respostas ou edição universal.

**Entradas**

- PDF local não criptografado, sem assinatura/Perms/XFA/Collection, fonte identificada por SHA-256.
- Operação selecionada, página base zero para marcador/nota ou nome do campo Tx e texto; destino novo com pasta existente.
- Operação adicional de formulário/árvore/anotação descrita em docs/EDICAO-COM-HISTORICO.md; histórico de até100 passos.

**Saídas**

- Cópia PDF nova e exclusiva, fonte identificada por hash e preservada; rascunho validado após cada operação.
- UI de histórico com desfazer/refazer no rascunho; cópias já salvas preservadas. GTK/Linux exercitado;333/333 por ambiente fonte/payload/sandbox, sem observação original.

**Erros e casos excepcionais**

- Fonte mudou ou destino já existe, inclusive o próprio original: Recusar a gravação; não sobrescrever arquivos.
- PDF criptografado, assinatura/campo Sig, Perms, XFA ou Collection: Recurso não suportado para gravação; não remover proteção ou invalidar assinatura.
- Operação/índice/texto/retângulo inválido; campo ausente, não Tx, ReadOnly ou MaxLen excedido: Falha antes de publicar destino; lote não é aplicado parcialmente à fonte.
- Controle/aparência/opção/árvore/anotação fora do subconjunto ou origem alterada: Recusar a alteração sem avançar o histórico ou publicar uma cópia parcial em falha tratada.

**Estado e efeitos**

- Fonte clonada em memória; gravação temporária privada, reabertura e rechecagem de identidade antes da criação exclusiva do destino.
- Falhas tratadas removem arquivo novo criado; término forçado/timeout pode deixar temporário ou saída parcial e exige conferir destino.
- Não executar ações ou scripts PDF. Sem persistência em cima do original e sem garantia de preservação de assinatura; documentos com assinatura são recusados.
- Confirmação capturada por documento/geração; reabrir o mesmo caminho durante diálogo invalida a operação antiga.
- Reconstituir cópia temporária e inspecionar antes de avançar histórico; falha mantém cursor/refazer e original; fechar cancela worker. Gravação interrompida exige conferir destino.

**Critérios planejados**

- **S12-14-1** (nominal, contrato próprio atual, `not_run`): dado Fixture com nota contendo assunto e conteúdo distintos. Ação: Inspecionar o painel. Esperado: Assunto separado, comentário alvo e autor permanecem campos distintos na página conhecida.
- **S12-14-2** (exception, contrato próprio atual, `not_run`): dado Objeto de anotação isolado inválido. Ação: Ler os demais comentários. Esperado: A falha de um objeto não deve ser reportada como criação/edição bem-sucedida de anotação.

**Lacunas da referência Foxit**

- Replies, aparências, edição, autoria, undo/redo, salvamento e disponibilidade Reader.

Fontes: [app/pdf_panels.py](../app/pdf_panels.py), [app/search_engine.py](../app/search_engine.py), [app/pdf_changes.py](../app/pdf_changes.py), [app/edit_tasks.py](../app/edit_tasks.py), [app/worker_cli.py](../app/worker_cli.py), [app/main.py](../app/main.py), [docs/SEGURANCA-ACESSIBILIDADE.md](../docs/SEGURANCA-ACESSIBILIDADE.md), [app/local_files.py](../app/local_files.py), [app/folder_dialogs.py](../app/folder_dialogs.py), [docs/PASTAS-SINCRONIZADAS.md](../docs/PASTAS-SINCRONIZADAS.md), [app/pdf_form_controls.py](../app/pdf_form_controls.py), [app/edit_history.py](../app/edit_history.py), [app/edit_dialogs.py](../app/edit_dialogs.py), [app/edit_window.py](../app/edit_window.py), [docs/EDICAO-COM-HISTORICO.md](../docs/EDICAO-COM-HISTORICO.md), [testes/resultados/0.1.10/validation-review.json](../testes/resultados/0.1.10/validation-review.json), [docs/FOXIT-REA.md](../docs/FOXIT-REA.md).

Testes próprios existentes, sem nova execução nesta tabela: [test_comment_subject_and_contents_are_searchable_without_author](../tests/test_search_scopes.py); [test_combined_copy_preserves_source_metadata_attachment_and_previous_objects](../tests/test_pdf_changes.py); [test_encryption_signature_permissions_xfa_and_portfolio_are_explicitly_unsupported](../tests/test_pdf_changes.py); [test_real_dialogs_and_worker_create_bookmark_note_and_form_copies](../tests/test_copy_edit_gtk.py); [test_reopening_same_document_during_dialog_blocks_stale_save](../tests/test_copy_edit_gtk.py); [test_existing_destination_is_preserved_and_busy_state_is_released](../tests/test_copy_edit_gtk.py); [test_combined_edits_preserve_tree_destinations_geometry_and_source](../tests/test_extended_edits.py); [test_final_name_is_absent_while_real_copy_is_in_progress](../tests/test_sync_folders.py); [test_save_copy_uses_worker_preserves_original_and_only_confirms_local_save](../tests/test_sync_folders_gtk.py); [test_info_distinguishes_checkbox_radio_choice_combo_and_multiselect](../tests/test_advanced_edits.py); [test_checkbox_sets_and_clears_value_and_visible_appearance](../tests/test_advanced_edits.py); [test_radio_activates_only_the_selected_widget_and_can_clear](../tests/test_advanced_edits.py); [test_radio_no_toggle_off_is_enforced](../tests/test_advanced_edits.py); [test_single_and_combo_values_indices_and_generated_appearances_roundtrip](../tests/test_advanced_edits.py); [test_multiselect_uses_export_values_and_canonical_indices](../tests/test_advanced_edits.py); [test_choice_selection_can_be_cleared](../tests/test_advanced_edits.py); [test_invalid_values_do_not_publish_partial_batch](../tests/test_advanced_edits.py); [test_read_only_and_unsupported_button_appearance_are_explicit](../tests/test_advanced_edits.py); [test_editable_combo_and_duplicate_exports_are_rejected](../tests/test_advanced_edits.py); [test_inherited_checkbox_flags_and_type_are_respected](../tests/test_advanced_edits.py); [test_checkbox_widget_absent_from_pages_is_unsupported](../tests/test_advanced_edits.py); [test_closed_outline_counts_remain_closed_after_move](../tests/test_advanced_edits.py); [test_move_preserves_subtree_destinations_and_sibling_links](../tests/test_advanced_edits.py); [test_move_child_to_root_and_reorder_same_parent](../tests/test_advanced_edits.py); [test_delete_bookmark_removes_subtree_and_last_root](../tests/test_advanced_edits.py); [test_move_into_descendant_invalid_positions_and_boolean_paths_are_refused](../tests/test_advanced_edits.py); [test_highlight_and_rectangle_roundtrip_geometry_print_flags_and_text](../tests/test_advanced_edits.py); [test_delete_supported_annotation_preserves_widgets_and_other_pages](../tests/test_advanced_edits.py); [test_locked_notes_widgets_and_replies_are_not_deleted](../tests/test_advanced_edits.py); [test_invalid_annotation_geometry_and_extra_parameters_are_rejected](../tests/test_advanced_edits.py); [test_undo_redo_rebuild_actual_pdfs_and_save_current_cursor_only](../tests/test_edit_history.py); [test_undo_all_restores_base_and_disables_save_until_redone](../tests/test_edit_history.py); [test_new_branch_discards_redo_but_invalid_branch_preserves_it](../tests/test_edit_history.py); [test_operation_values_are_defensively_copied](../tests/test_edit_history.py); [test_changed_original_blocks_add_undo_redo_and_save](../tests/test_edit_history.py); [test_existing_destination_is_not_overwritten_and_draft_survives](../tests/test_edit_history.py); [test_closed_session_refuses_work_and_removes_private_previews](../tests/test_edit_history.py); [test_pre_cancelled_session_does_not_start_worker](../tests/test_edit_history.py); [test_buttons_undo_redo_save_selected_history_and_preserve_prior_copy](../tests/test_edit_draft_gtk.py); [test_real_form_dialog_checkbox_radio_list_and_multiselect](../tests/test_edit_draft_gtk.py); [test_real_move_and_delete_bookmark_dialogs_use_updated_paths](../tests/test_edit_draft_gtk.py); [test_real_area_annotation_dialog_and_delete_keep_other_annotations](../tests/test_edit_draft_gtk.py); [test_failed_operation_and_existing_destination_keep_history_usable](../tests/test_edit_draft_gtk.py); [test_cancel_dialog_and_reopen_parent_close_draft_without_publishing](../tests/test_edit_draft_gtk.py); [test_cancelling_save_and_repeated_clicks_do_not_duplicate_writes](../tests/test_edit_draft_gtk.py); [test_saved_form_and_highlight_render_with_poppler](../tests/test_edit_draft_gtk.py).

Relacionados aos planos dinâmicos/UI: D08, D09, D19.

<a id="forms"></a>

## AcroForm/XFA/eventos

Fonte0.1.10: Tx anterior, checkbox com aparências existentes, radio simples, combos sem texto livre e listas simples/múltiplas em cópia nova; rótulos/valores/índices e ReadOnly herdado conferidos. XFA/eventos/combos editáveis e formatos não suportados permanecem pendentes.

**Entradas**

- PDF local não criptografado, sem assinatura/Perms/XFA/Collection, fonte identificada por SHA-256.
- Operação selecionada, página base zero para marcador/nota ou nome do campo Tx e texto; destino novo com pasta existente.
- Operação adicional de formulário/árvore/anotação descrita em docs/EDICAO-COM-HISTORICO.md; histórico de até100 passos.

**Saídas**

- Cópia PDF nova e exclusiva, fonte identificada por hash e preservada; rascunho validado após cada operação.
- UI de histórico com desfazer/refazer no rascunho; cópias já salvas preservadas. GTK/Linux exercitado;333/333 por ambiente fonte/payload/sandbox, sem observação original.

**Erros e casos excepcionais**

- Fonte mudou ou destino já existe, inclusive o próprio original: Recusar a gravação; não sobrescrever arquivos.
- PDF criptografado, assinatura/campo Sig, Perms, XFA ou Collection: Recurso não suportado para gravação; não remover proteção ou invalidar assinatura.
- Operação/índice/texto/retângulo inválido; campo ausente, não Tx, ReadOnly ou MaxLen excedido: Falha antes de publicar destino; lote não é aplicado parcialmente à fonte.
- Controle/aparência/opção/árvore/anotação fora do subconjunto ou origem alterada: Recusar a alteração sem avançar o histórico ou publicar uma cópia parcial em falha tratada.

**Estado e efeitos**

- Fonte clonada em memória; gravação temporária privada, reabertura e rechecagem de identidade antes da criação exclusiva do destino.
- Falhas tratadas removem arquivo novo criado; término forçado/timeout pode deixar temporário ou saída parcial e exige conferir destino.
- Não executar ações ou scripts PDF. Sem persistência em cima do original e sem garantia de preservação de assinatura; documentos com assinatura são recusados.
- Confirmação capturada por documento/geração; reabrir o mesmo caminho durante diálogo invalida a operação antiga.
- Reconstituir cópia temporária e inspecionar antes de avançar histórico; falha mantém cursor/refazer e original; fechar cancela worker. Gravação interrompida exige conferir destino.

**Critérios planejados**

- **S12-15-1** (nominal, contrato próprio atual, `not_run`): dado AcroForm sintético com campo Tx editável, sem XFA ou assinatura. Ação: Preencher o campo Tx e salvar cópia nova. Esperado: Reabrir a cópia confirma o texto; páginas e original são preservados. Widgets de escolha não estão neste subconjunto.
- **S12-15-2** (exception, contrato próprio atual, `not_run`): dado AcroForm sintético com campo Tx ReadOnly ou MaxLen excedido. Ação: Tentar alterar o campo e salvar cópia. Esperado: Recusar a operação sem saída nova; preservar o original.

**Lacunas da referência Foxit**

- Motor de formulários, eventos, XFA, cálculo/validação e gravação; FRMSPlgV2 é RMS, não prova de formulários.

Fontes: [app/pdf_changes.py](../app/pdf_changes.py), [app/edit_tasks.py](../app/edit_tasks.py), [app/worker_cli.py](../app/worker_cli.py), [app/main.py](../app/main.py), [app/local_files.py](../app/local_files.py), [app/folder_dialogs.py](../app/folder_dialogs.py), [docs/PASTAS-SINCRONIZADAS.md](../docs/PASTAS-SINCRONIZADAS.md), [app/pdf_form_controls.py](../app/pdf_form_controls.py), [app/edit_history.py](../app/edit_history.py), [app/edit_dialogs.py](../app/edit_dialogs.py), [app/edit_window.py](../app/edit_window.py), [docs/EDICAO-COM-HISTORICO.md](../docs/EDICAO-COM-HISTORICO.md), [testes/resultados/0.1.10/validation-review.json](../testes/resultados/0.1.10/validation-review.json), [docs/FOXIT-REA.md](../docs/FOXIT-REA.md), [docs/AVANCO-SEM-VM.md](../docs/AVANCO-SEM-VM.md).

Testes próprios existentes, sem nova execução nesta tabela: [test_combined_copy_preserves_source_metadata_attachment_and_previous_objects](../tests/test_pdf_changes.py); [test_encryption_signature_permissions_xfa_and_portfolio_are_explicitly_unsupported](../tests/test_pdf_changes.py); [test_real_dialogs_and_worker_create_bookmark_note_and_form_copies](../tests/test_copy_edit_gtk.py); [test_reopening_same_document_during_dialog_blocks_stale_save](../tests/test_copy_edit_gtk.py); [test_existing_destination_is_preserved_and_busy_state_is_released](../tests/test_copy_edit_gtk.py); [test_nested_field_inherits_read_only_and_max_length](../tests/test_pdf_changes.py); [test_form_max_length_and_value_types_are_enforced](../tests/test_pdf_changes.py); [test_final_name_is_absent_while_real_copy_is_in_progress](../tests/test_sync_folders.py); [test_save_copy_uses_worker_preserves_original_and_only_confirms_local_save](../tests/test_sync_folders_gtk.py); [test_info_distinguishes_checkbox_radio_choice_combo_and_multiselect](../tests/test_advanced_edits.py); [test_checkbox_sets_and_clears_value_and_visible_appearance](../tests/test_advanced_edits.py); [test_radio_activates_only_the_selected_widget_and_can_clear](../tests/test_advanced_edits.py); [test_radio_no_toggle_off_is_enforced](../tests/test_advanced_edits.py); [test_single_and_combo_values_indices_and_generated_appearances_roundtrip](../tests/test_advanced_edits.py); [test_multiselect_uses_export_values_and_canonical_indices](../tests/test_advanced_edits.py); [test_choice_selection_can_be_cleared](../tests/test_advanced_edits.py); [test_invalid_values_do_not_publish_partial_batch](../tests/test_advanced_edits.py); [test_read_only_and_unsupported_button_appearance_are_explicit](../tests/test_advanced_edits.py); [test_editable_combo_and_duplicate_exports_are_rejected](../tests/test_advanced_edits.py); [test_inherited_checkbox_flags_and_type_are_respected](../tests/test_advanced_edits.py); [test_checkbox_widget_absent_from_pages_is_unsupported](../tests/test_advanced_edits.py); [test_closed_outline_counts_remain_closed_after_move](../tests/test_advanced_edits.py); [test_move_preserves_subtree_destinations_and_sibling_links](../tests/test_advanced_edits.py); [test_move_child_to_root_and_reorder_same_parent](../tests/test_advanced_edits.py); [test_delete_bookmark_removes_subtree_and_last_root](../tests/test_advanced_edits.py); [test_move_into_descendant_invalid_positions_and_boolean_paths_are_refused](../tests/test_advanced_edits.py); [test_highlight_and_rectangle_roundtrip_geometry_print_flags_and_text](../tests/test_advanced_edits.py); [test_delete_supported_annotation_preserves_widgets_and_other_pages](../tests/test_advanced_edits.py); [test_locked_notes_widgets_and_replies_are_not_deleted](../tests/test_advanced_edits.py); [test_invalid_annotation_geometry_and_extra_parameters_are_rejected](../tests/test_advanced_edits.py); [test_undo_redo_rebuild_actual_pdfs_and_save_current_cursor_only](../tests/test_edit_history.py); [test_undo_all_restores_base_and_disables_save_until_redone](../tests/test_edit_history.py); [test_new_branch_discards_redo_but_invalid_branch_preserves_it](../tests/test_edit_history.py); [test_operation_values_are_defensively_copied](../tests/test_edit_history.py); [test_changed_original_blocks_add_undo_redo_and_save](../tests/test_edit_history.py); [test_existing_destination_is_not_overwritten_and_draft_survives](../tests/test_edit_history.py); [test_closed_session_refuses_work_and_removes_private_previews](../tests/test_edit_history.py); [test_pre_cancelled_session_does_not_start_worker](../tests/test_edit_history.py); [test_buttons_undo_redo_save_selected_history_and_preserve_prior_copy](../tests/test_edit_draft_gtk.py); [test_real_form_dialog_checkbox_radio_list_and_multiselect](../tests/test_edit_draft_gtk.py); [test_real_move_and_delete_bookmark_dialogs_use_updated_paths](../tests/test_edit_draft_gtk.py); [test_real_area_annotation_dialog_and_delete_keep_other_annotations](../tests/test_edit_draft_gtk.py); [test_failed_operation_and_existing_destination_keep_history_usable](../tests/test_edit_draft_gtk.py); [test_cancel_dialog_and_reopen_parent_close_draft_without_publishing](../tests/test_edit_draft_gtk.py); [test_cancelling_save_and_repeated_clicks_do_not_duplicate_writes](../tests/test_edit_draft_gtk.py); [test_saved_form_and_highlight_render_with_poppler](../tests/test_edit_draft_gtk.py).

<a id="attachments"></a>

## Anexos/portfólios

Atual0.1.4: catálogo plano/árvores Kids aninhadas e anexos de anotação; backend, controlador e seis métodos GTK testados em fonte/payload/Flatpak127/127. Portfólios e senha não vazia pendentes.

**Entradas**

- PDF local com catálogo plano ou árvore de anexos /Kids e anexos de anotação /FileAttachment; listagem não decodifica payloads.
- Índice da entrada, SHA-256 da listagem e pasta de destino existente controlada pelo usuário.
- No painel: selecionar entrada, escolher pasta e confirmar; cancelar não inicia extração.

**Saídas**

- Listagem com índices distintos, nomes, tamanho declarado opcional e indicação de nome permitido; tamanho declarado não é tamanho medido. Origem catalog/annotation e página de anotação em base zero; índice distinto para cada referência.
- Extração retorna nome/caminho, tamanho real e hash SHA-256 dos bytes; mantém o PDF original.
- UI: lista sob demanda, salva seleção e mostra página da anotação. Seis métodos GTK do painel passaram em fonte/payload/sandbox0.1.4; desktop/portais/acessibilidade pendentes.

**Erros e casos excepcionais**

- Caminhos, nomes reservados, caracteres de controle ou nome fora do limite: Recusar extração antes de criar arquivo; a listagem conserva o nome e indica a recusa.
- Destino já existe, inclusive outra entrada com o mesmo nome: FileExistsError, sem sobrescrita; escolher outra pasta para extrair essa entrada.
- PDF mudou, índice/hash inválido, pasta ausente ou payload acima de 64 MiB: Falha explícita antes da gravação; tamanho real é checado após decodificar o stream.
- Portfólio /Collection ou senha não vazia necessária: Recurso ainda não suportado; não apresentar inventário vazio como sucesso.
- Seleção/documento mudou durante a escolha de pasta ou resultado assíncrono tornou-se obsoleto: Token de seleção inválido não inicia extração; callbacks antigos não substituem dados/estado do novo documento.
- Ciclos/nós repetidos, profundidade acima64, mais4000 nós ou estrutura Kids/Names inválida: Falha explícita na listagem; não truncar silenciosamente. Limite1000 entradas no conjunto catálogo/anotações.

**Estado e efeitos**

- Extrai somente a entrada solicitada, sem executar ou abrir seu conteúdo; nenhum acesso remoto.
- Nomes não são normalizados/renomeados silenciosamente; payloads não são lidos durante listagem.
- A pasta deve ser controlada pelo usuário; não há garantia contra outro processo trocando diretórios durante a gravação.
- Limites de parsing/memória não são impostos pela checagem de 64 MiB após descompressão; usar o worker e seus limites onde disponíveis.
- Extração já autorizada pode terminar após troca de documento; status antigo não é aplicado ao novo. Fechar janela bloqueia tarefas ainda não iniciadas/callbacks, sem garantir interrupção de subprocesso já em execução.

**Critérios planejados**

- **S12-16-1** (nominal, contrato próprio atual, `not_run`): dado anexos-simples.pdf e uma pasta existente nova e vazia. Ação: Listar, usar o índice e SHA-256 devolvidos e extrair nota-sintetica.txt. Esperado: Bytes, tamanho e hash coincidem com anexos-simples.json; nada é executado.
- **S12-16-2** (exception, contrato próprio atual, `not_run`): dado Nome de anexo ../fora.txt. Ação: Extrair. Esperado: A listagem marca o nome como não permitido e a extração falha sem criar arquivo fora ou dentro da pasta.

**Lacunas da referência Foxit**

- Política e comportamento Foxit ainda não observados; backend atual é contrato independente.
- Portfólios completos e senha não vazia continuam pendentes; extensão própria de árvores/anotações não prova comportamento Foxit. Desktop e acessibilidade pendentes.

Fontes: [app/pdf_attachments.py](../app/pdf_attachments.py), [app/worker_cli.py](../app/worker_cli.py), [app/attachment_tasks.py](../app/attachment_tasks.py), [app/main.py](../app/main.py), [docs/FOXIT-REA.md](../docs/FOXIT-REA.md).

Testes próprios existentes, sem nova execução nesta tabela: [test_listing_keeps_duplicate_entries_and_does_not_decode_payloads](../tests/test_pdf_attachments.py); [test_extract_preserves_binary_content_hash_and_original](../tests/test_pdf_attachments.py); [test_unsafe_pdf_names_are_reported_and_refused_without_writes](../tests/test_pdf_attachments.py); [test_worker_protocol_lists_extracts_and_reports_conflict](../tests/test_pdf_attachments.py); [test_stale_listing_callback_cannot_replace_a_new_document](../tests/test_attachment_tasks.py); [test_real_worker_extracts_selected_attachment_and_restores_buttons](../tests/test_attachment_tasks.py); [test_refresh_invalidates_the_selection_captured_before_a_dialog](../tests/test_attachment_tasks.py); [test_panel_saves_selected_file_and_shows_conflict_without_overwrite](../tests/test_attachment_panel_gtk.py); [test_sidebar_buttons_switch_hide_and_restore_without_recursive_callbacks](../tests/test_attachment_panel_gtk.py); [test_long_attachment_name_keeps_header_and_save_button_inside_panel](../tests/test_sidebar_layout_gtk.py); [test_nested_tree_preserves_duplicate_name_indices_and_bytes](../tests/test_attachment_trees.py).

Relacionados aos planos dinâmicos/UI: D16.

<a id="signatures"></a>

## Assinaturas/certificados

Inspeção offline de integridade CMS destacada, separada da confiança do certificado. Sem assinatura de documentos, aprovação de cadeia, revogação, carimbo de tempo ou suporte PAdES/LTV completo.

**Entradas**

- PDF não criptografado até 64 MiB; até 16 campos Sig; CMS DER até 2 MiB; quatro intervalos ByteRange válidos.

**Saídas**

- Status de integridade, cobertura da revisão/arquivo atual e trust_chain_verified=false; sem modificação do PDF ou rede.

**Erros e casos excepcionais**

- Entrada não suportada, falha de autenticação/integridade ou cancelamento: ByteRange/Contents/DER malformado, filtro não suportado ou verificador ausente: status explícito sem aprovação.

**Estado e efeitos**

- Falha de CMS pode ser adulteração ou algoritmo não suportado; nunca atesta confiança/caráter jurídico.
- Fonte preservada; workers limitados e temporários privados. Limpeza sem garantia de apagamento seguro.

**Critérios planejados**

- **S12-17-1** (nominal, contrato próprio atual, `not_run`): dado PDF não criptografado até 64 MiB; até 16 campos Sig; CMS DER até 2 MiB; quatro intervalos ByteRange válidos. Ação: Executar o subconjunto local descrito. Esperado: Status de integridade, cobertura da revisão/arquivo atual e trust_chain_verified=false; sem modificação do PDF ou rede.
- **S12-17-2** (exception, contrato próprio atual, `not_run`): dado Entrada inválida ou recurso explicitamente não suportado. Ação: Solicitar a operação local. Esperado: ByteRange/Contents/DER malformado, filtro não suportado ou verificador ausente: status explícito sem aprovação.

**Lacunas da referência Foxit**

- Fluxos Reader, assinatura versus validação, cadeias, políticas e comportamento offline; plugins não provam suporte completo.

Fontes: [app/pdf_signatures.py](../app/pdf_signatures.py), [app/signature_window.py](../app/signature_window.py), [app/search_tasks.py](../app/search_tasks.py), [app/worker_cli.py](../app/worker_cli.py), [app/main.py](../app/main.py), [docs/SEGURANCA-ACESSIBILIDADE.md](../docs/SEGURANCA-ACESSIBILIDADE.md), [docs/FOXIT-REA.md](../docs/FOXIT-REA.md).

Testes próprios existentes, sem nova execução nesta tabela: [test_real_detached_cms_integrity_is_separate_from_certificate_trust](../tests/test_pdf_signatures.py); [test_modified_signed_bytes_fail_cryptographic_verification](../tests/test_pdf_signatures.py); [test_appended_bytes_report_only_signed_revision_coverage](../tests/test_pdf_signatures.py); [test_unsupported_filter_or_invalid_byte_range_never_report_verified](../tests/test_pdf_signatures.py); [test_der_bounds_and_padding_are_checked](../tests/test_pdf_signatures.py); [test_unsigned_fields_and_count_limit_are_explicit](../tests/test_pdf_signatures.py); [test_encrypted_pdf_input_size_and_invalid_request_are_refused](../tests/test_pdf_signatures.py); [test_missing_verifier_and_source_changes_do_not_approve_integrity](../tests/test_pdf_signatures.py); [test_real_worker_roundtrip_and_cancelled_request](../tests/test_pdf_signatures.py); [test_invalid_worker_confirmation_is_rejected](../tests/test_pdf_signatures.py); [test_integrity_ui_reports_verification_without_certificate_trust](../tests/test_signature_gtk.py); [test_unsigned_and_encrypted_inputs_have_distinct_results](../tests/test_signature_gtk.py).

<a id="security"></a>

## Senhas/permissões/RMS

Autenticar senha conhecida, inspecionar permissões, criar cópia AES-256 ou cópia sem criptografia com senha de proprietário. RMS e abertura cifrada integrada ao leitor continuam pendentes. Fonte0.1.9: fluxo local de pasta preferida/últimas pastas e cópias novas com publicação completa/exclusiva. Envio remoto é do sincronizador externo; fonte/payload/sandbox290/290 aprovados; cliente real e portal em desktop ainda pendentes.

**Entradas**

- PDF local sintético até 64 MiB, senha conhecida ou duas senhas novas distintas de 8–64 ASCII imprimíveis.
- Fonte SHA-256, seis permissões declaradas e destino novo.

**Saídas**

- Estado de autenticação/role/permissões sem senha no resultado; nova cópia AES-256 R6 verificada ou plaintext somente para owner autenticado.

**Erros e casos excepcionais**

- Entrada não suportada, falha de autenticação/integridade ou cancelamento: Credencial errada, role usuário para exportação plaintext, documento Sig/Perms/XFA/Collection, destino existente ou fonte alterada: recusa explícita.

**Estado e efeitos**

- Segredos por stdin; mensagens fixas, sem recuperação de senha ou chamada de serviço RMS.
- Fonte preservada; workers limitados e temporários privados. Limpeza sem garantia de apagamento seguro.

**Critérios planejados**

- **S12-18-1** (nominal, contrato próprio atual, `not_run`): dado PDF local sintético até 64 MiB, senha conhecida ou duas senhas novas distintas de 8–64 ASCII imprimíveis. Ação: Executar o subconjunto local descrito. Esperado: Estado de autenticação/role/permissões sem senha no resultado; nova cópia AES-256 R6 verificada ou plaintext somente para owner autenticado.
- **S12-18-2** (exception, contrato próprio atual, `not_run`): dado Entrada inválida ou recurso explicitamente não suportado. Ação: Solicitar a operação local. Esperado: Credencial errada, role usuário para exportação plaintext, documento Sig/Perms/XFA/Collection, destino existente ou fonte alterada: recusa explícita.

**Lacunas da referência Foxit**

- Entrada de senha, enforcement de permissões, RMS e mensagens do original; o fluxo completo não está implementado.

Fontes: [app/pdf_security.py](../app/pdf_security.py), [app/security_window.py](../app/security_window.py), [app/search_tasks.py](../app/search_tasks.py), [app/worker_cli.py](../app/worker_cli.py), [app/main.py](../app/main.py), [docs/SEGURANCA-ACESSIBILIDADE.md](../docs/SEGURANCA-ACESSIBILIDADE.md), [app/local_files.py](../app/local_files.py), [app/folder_dialogs.py](../app/folder_dialogs.py), [docs/PASTAS-SINCRONIZADAS.md](../docs/PASTAS-SINCRONIZADAS.md), [docs/FOXIT-REA.md](../docs/FOXIT-REA.md), [docs/AVANCO-SEM-VM.md](../docs/AVANCO-SEM-VM.md).

Testes próprios existentes, sem nova execução nesta tabela: [test_unencrypted_inspection_identity_pages_and_permissions](../tests/test_pdf_security.py); [test_aes256_roundtrip_roles_permissions_metadata_and_attachments](../tests/test_pdf_security.py); [test_each_permission_flag_and_accessibility_bit_are_preserved](../tests/test_pdf_security.py); [test_encrypted_inspection_correct_wrong_and_missing_credentials](../tests/test_pdf_security.py); [test_new_password_limits_and_distinct_roles](../tests/test_pdf_security.py); [test_invalid_protocol_and_permission_types_rejected](../tests/test_pdf_security.py); [test_encrypted_source_not_unprotected_or_rewritten](../tests/test_pdf_security.py); [test_signed_xfa_portfolio_and_permissions_sources_refused](../tests/test_pdf_security.py); [test_stale_source_and_source_size_page_output_limits](../tests/test_pdf_security.py); [test_existing_destination_and_source_never_overwritten](../tests/test_pdf_security.py); [test_handled_partial_write_removed_and_error_sanitized](../tests/test_pdf_security.py); [test_concurrent_destination_preserved](../tests/test_pdf_security.py); [test_real_worker_secret_transport_and_error_channel](../tests/test_pdf_security.py); [test_cancellation_and_invalid_confirmation_never_report_success](../tests/test_pdf_security.py); [test_accessible_text_validation_limit_and_source_change](../tests/test_pdf_security.py); [test_accessible_text_refuses_encrypted_pdf_even_with_empty_password](../tests/test_pdf_security.py); [test_accessible_text_adapter_rejects_invalid_reply_and_supports_cancel](../tests/test_pdf_security.py); [test_only_owner_authentication_can_create_unprotected_copy](../tests/test_pdf_security.py); [test_owner_copy_stale_destination_and_partial_failure_are_safe](../tests/test_pdf_security.py); [test_owner_copy_refuses_special_restrictions_and_signature_fields](../tests/test_pdf_security.py); [test_inspect_protect_and_secrets_cleared_without_source_change](../tests/test_security_accessibility_gtk.py); [test_encrypted_inspection_wrong_and_owner_credentials](../tests/test_security_accessibility_gtk.py); [test_password_mismatch_and_cancelled_destination_create_nothing](../tests/test_security_accessibility_gtk.py); [test_document_change_during_destination_dialog_discards_request](../tests/test_security_accessibility_gtk.py); [test_cancel_and_destroy_stop_actual_security_process](../tests/test_security_accessibility_gtk.py); [test_owner_copy_is_readable_by_main_reader_and_original_is_preserved](../tests/test_security_accessibility_gtk.py); [test_owner_copy_rejects_opening_password_and_clears_it](../tests/test_security_accessibility_gtk.py); [test_final_name_is_absent_while_real_copy_is_in_progress](../tests/test_sync_folders.py); [test_save_copy_uses_worker_preserves_original_and_only_confirms_local_save](../tests/test_sync_folders_gtk.py).

Relacionados aos planos dinâmicos/UI: D15.

<a id="accessibility"></a>

## Acessibilidade/voz

Texto extraído da página em Gtk.TextView/ATK.Text, nomes acessíveis e navegação F6/Shift+F6/Ctrl+Shift+T. Sem OCR/voz, garantia de ordem semântica, teste com leitor de tela real ou conformidade integral.

**Entradas**

- PDF não criptografado, página válida e ação do usuário; texto até 1 MiB UTF-8.
- Foco e estado do documento/geração capturados antes da tarefa.

**Saídas**

- Texto selecionável e acessível da página, status/cancelamento e descarte de resposta obsoleta.

**Erros e casos excepcionais**

- Entrada não suportada, falha de autenticação/integridade ou cancelamento: PDF cifrado, limite de texto excedido ou Poppler indisponível: erro explícito sem texto parcial apresentado como completo.

**Estado e efeitos**

- Troca de documento/fechamento cancela worker e descarta atualização antiga.
- Fonte preservada; workers limitados e temporários privados. Limpeza sem garantia de apagamento seguro.

**Critérios planejados**

- **S12-19-1** (nominal, contrato próprio atual, `not_run`): dado PDF não criptografado, página válida e ação do usuário; texto até 1 MiB UTF-8. Ação: Executar o subconjunto local descrito. Esperado: Texto selecionável e acessível da página, status/cancelamento e descarte de resposta obsoleta.
- **S12-19-2** (exception, contrato próprio atual, `not_run`): dado Entrada inválida ou recurso explicitamente não suportado. Ação: Solicitar a operação local. Esperado: PDF cifrado, limite de texto excedido ou Poppler indisponível: erro explícito sem texto parcial apresentado como completo.

**Lacunas da referência Foxit**

- APIs, árvore acessível, ordem, voz, foco, atalhos e cobertura real do Reader.

Fontes: [app/accessible_reader.py](../app/accessible_reader.py), [app/pdf_security.py](../app/pdf_security.py), [app/search_tasks.py](../app/search_tasks.py), [app/worker_cli.py](../app/worker_cli.py), [app/main.py](../app/main.py), [docs/SEGURANCA-ACESSIBILIDADE.md](../docs/SEGURANCA-ACESSIBILIDADE.md), [docs/FOXIT-REA.md](../docs/FOXIT-REA.md).

Testes próprios existentes, sem nova execução nesta tabela: [test_unencrypted_inspection_identity_pages_and_permissions](../tests/test_pdf_security.py); [test_aes256_roundtrip_roles_permissions_metadata_and_attachments](../tests/test_pdf_security.py); [test_each_permission_flag_and_accessibility_bit_are_preserved](../tests/test_pdf_security.py); [test_encrypted_inspection_correct_wrong_and_missing_credentials](../tests/test_pdf_security.py); [test_new_password_limits_and_distinct_roles](../tests/test_pdf_security.py); [test_invalid_protocol_and_permission_types_rejected](../tests/test_pdf_security.py); [test_encrypted_source_not_unprotected_or_rewritten](../tests/test_pdf_security.py); [test_signed_xfa_portfolio_and_permissions_sources_refused](../tests/test_pdf_security.py); [test_stale_source_and_source_size_page_output_limits](../tests/test_pdf_security.py); [test_existing_destination_and_source_never_overwritten](../tests/test_pdf_security.py); [test_handled_partial_write_removed_and_error_sanitized](../tests/test_pdf_security.py); [test_concurrent_destination_preserved](../tests/test_pdf_security.py); [test_real_worker_secret_transport_and_error_channel](../tests/test_pdf_security.py); [test_cancellation_and_invalid_confirmation_never_report_success](../tests/test_pdf_security.py); [test_accessible_text_validation_limit_and_source_change](../tests/test_pdf_security.py); [test_accessible_text_refuses_encrypted_pdf_even_with_empty_password](../tests/test_pdf_security.py); [test_accessible_text_adapter_rejects_invalid_reply_and_supports_cancel](../tests/test_pdf_security.py); [test_only_owner_authentication_can_create_unprotected_copy](../tests/test_pdf_security.py); [test_owner_copy_stale_destination_and_partial_failure_are_safe](../tests/test_pdf_security.py); [test_owner_copy_refuses_special_restrictions_and_signature_fields](../tests/test_pdf_security.py); [test_real_poppler_text_is_exposed_through_atk_text_interface](../tests/test_security_accessibility_gtk.py); [test_no_text_and_encrypted_pages_have_explicit_limits](../tests/test_security_accessibility_gtk.py); [test_obsolete_page_text_does_not_replace_newer_page](../tests/test_security_accessibility_gtk.py); [test_f6_focus_regions_names_and_list_arrow_delegation](../tests/test_security_accessibility_gtk.py); [test_text_limit_and_document_close_clear_the_accessible_window](../tests/test_security_accessibility_gtk.py); [test_closing_text_worker_terminates_its_real_descendant_on_linux](../tests/test_security_accessibility_gtk.py).

Relacionados aos planos dinâmicos/UI: UI10.

<a id="measurement"></a>

## Medição/calibração

Atual: distância entre pontos na visualização, convertida de pontos PDF para centímetros; sem calibração personalizada.

**Entradas**

- Dois pontos em pixels, tamanho da página rotacionada e dimensão da imagem.
- Página usa a escala base de 72 pontos por polegada.

**Saídas**

- Distância euclidiana em cm, exibida com duas casas decimais.
- Não calcular área/perímetro/calibração como se implementados.

**Erros e casos excepcionais**

- Não há imagem ou tamanhos de página: A função retorna sem atualizar medida.
- Documento usa escala/calibração especial: A igualdade com medida física/especializada não foi estabelecida; exigir contrato de calibração futuro.

**Estado e efeitos**

- Somente status/overlay de leitura; não cria anotação de medida no PDF.

**Critérios planejados**

- **S12-20-1** (nominal, contrato próprio atual, `not_run`): dado Imagem e página com escala conhecida; pontos separados por 72 pontos PDF. Ação: Medir o segmento horizontal. Esperado: Contrato próprio: 2,54 cm, formatado com duas casas decimais.
- **S12-20-2** (exception, contrato próprio atual, `not_run`): dado Página sem pixbuf/tamanhos disponíveis. Ação: Concluir gesto de medida. Esperado: Nenhuma nova medida válida é publicada.

**Lacunas da referência Foxit**

- Unidades, calibração, snapping, precisão, áreas e perímetros do original.

Fontes: [app/main.py](../app/main.py), [docs/FOXIT-REA.md](../docs/FOXIT-REA.md).

<a id="layers-media"></a>

## Camadas/mídia/3D

Atual: listar nomes de OCGs. Alternar visibilidade, mídia e 3D são contratos futuros distintos.

**Entradas**

- PDF com /OCProperties e /OCGs; nomes de camadas.
- Mídia/3D exigirá identificar formato, ação e isolamento próprios.

**Saídas**

- Atual: lista de nomes de camadas; não implica motor de composição de OCG nem playback.

**Erros e casos excepcionais**

- OCProperties ausente ou não decodificável: Painel fornece lista vazia; não alegar suporte a camadas inexistentes.
- PDF contém mídia/3D não implementados: Nenhum fluxo de reprodução equivalente é estabelecido pelo painel de nomes.

**Estado e efeitos**

- Leitura não muda visibilidade persistida nem executa conteúdo embutido.

**Critérios planejados**

- **S12-21-1** (nominal, contrato próprio atual, `not_run`): dado PDF sintético com OCGs nomeados, fixture a criar. Ação: Inspecionar painel. Esperado: Lista os nomes lidos, sem anunciar reprodução de mídia ou alteração de camada.
- **S12-21-2** (exception, contrato próprio atual, `not_run`): dado PDF sem OCProperties. Ação: Inspecionar painel. Esperado: layers=[]; não criar uma camada fictícia.

**Lacunas da referência Foxit**

- Combinações OCG, visibilidade, persistência, codecs, eventos e suporte U3D/Reader.

Fontes: [app/pdf_panels.py](../app/pdf_panels.py), [docs/FOXIT-REA.md](../docs/FOXIT-REA.md).

<a id="preferences"></a>

## Preferências/tema/persistência

Preferência própria system/light/dark com migração legada e persistência; sem equivalência de todos os ajustes Foxit. Fonte0.1.9: fluxo local de pasta preferida/últimas pastas e cópias novas com publicação completa/exclusiva. Envio remoto é do sincronizador externo; fonte/payload/sandbox290/290 aprovados; cliente real e portal em desktop ainda pendentes.

**Entradas**

- Modo system, light ou dark e arquivo de configuração em perfil sintético.
- JSON existente com chaves conhecidas e de versões futuras.

**Saídas**

- Modo válido e aparência aplicada; persistência preserva chaves desconhecidas.
- Falha de leitura/configuração inválida recai em modo system conforme o caminho de leitura/migração.

**Erros e casos excepcionais**

- Modo fora do conjunto ao salvar: ValueError; não aceitar um modo arbitrário.
- JSON inválido/arquivo ausente: Leitura tolerante e tentativa de migração, sem impor arquivo inválido como preferência válida.

**Estado e efeitos**

- Grava preferences.json próprio de forma temporária/atômica; não muda configuração do Foxit.

**Critérios planejados**

- **S12-22-1** (nominal, contrato próprio atual, `not_run`): dado Configuração com modo dark e uma chave desconhecida. Ação: Salvar modo light e reabrir a preferência. Esperado: Modo light preservado e chave desconhecida conservada.
- **S12-22-2** (exception, contrato próprio atual, `not_run`): dado Modo inventado ao salvar. Ação: Chamar save_mode. Esperado: ValueError, sem tratar o modo como suportado.

**Lacunas da referência Foxit**

- Defaults, esquemas de persistência e dependências de todas as preferências do original.

Fontes: [app/appearance.py](../app/appearance.py), [app/local_files.py](../app/local_files.py), [app/folder_dialogs.py](../app/folder_dialogs.py), [docs/PASTAS-SINCRONIZADAS.md](../docs/PASTAS-SINCRONIZADAS.md), [docs/FOXIT-REA.md](../docs/FOXIT-REA.md).

Testes próprios existentes, sem nova execução nesta tabela: [test_theme_persistence_and_contrast](../tests/test_viewer.py); [test_fresh_system_theme_initializes_and_migrates_legacy](../tests/test_consolidation.py); [test_final_name_is_absent_while_real_copy_is_in_progress](../tests/test_sync_folders.py); [test_save_copy_uses_worker_preserves_original_and_only_confirms_local_save](../tests/test_sync_folders_gtk.py).

<a id="cloud"></a>

## Nuvem/colaboração

Requisito futuro: integrações por provedor explícito, com contas/consentimento e estado offline separados. Adiado por decisão explícita do usuário: Deixar nuvem para depois. Família preservada, sem alteração de pesos. Autorizado apenas um fluxo auxiliar de arquivos locais em pasta sincronizada por outro programa; isso não implementa a integração remota desta família.

**Entradas**

- Provedor, operação, documento e autorização específica; testes iniciais usam backend local simulado.
- Credenciais/serviços reais ficam fora desta campanha.

**Saídas**

- Proposta: resultado remoto com identidade/versão ou indisponibilidade; nenhuma publicação implícita.

**Erros e casos excepcionais**

- Sem rede ou token expirado: Proposta: estado offline/autenticação necessária; sem repetir envio silenciosamente.
- Conflito de versão ou cancelamento: Proposta: preservar a cópia local e pedir resolução explícita antes de substituir conteúdo remoto.

**Estado e efeitos**

- Proposta: operações remotas somente em tarefa especificamente autorizada; não implementar transmissão nesta etapa.

**Critérios planejados**

- **S12-23-1** (nominal, proposta futura, `not_run`): dado Backend simulado de coleção remota e documento sintético. Ação: Simular download de uma versão identificada. Esperado: Proposta: receber os bytes/versionamento corretos sem usar conta real.
- **S12-23-2** (exception, proposta futura, `not_run`): dado Mesmo provedor simulado em estado offline. Ação: Solicitar sincronização. Esperado: Proposta: indicar indisponibilidade e preservar a cópia local; nenhum falso sucesso.

**Lacunas da referência Foxit**

- Contratos por provedor, serviços disponíveis, autorização, colaboração e conflitos; presença de plugins não valida APIs.

Fontes: [docs/PASTAS-SINCRONIZADAS.md](../docs/PASTAS-SINCRONIZADAS.md), [docs/FOXIT-REA.md](../docs/FOXIT-REA.md).

<a id="conversion"></a>

## Criação/conversão

Fonte0.1.12: TIFF multipágina em blocos, todas as páginas do IFD principal, até100 páginas totais junto de PNG/JPEG/BMP/WebP simples. RGB8, orientação por página e limites agregados; animações e variantes não decodificáveis recusadas. OCR0.1.11 preservado com limite próprio20 páginas. 14 novos controles portáveis passaram; Linux/GTK e novo pacote aguardam CI. Família completa e referência Foxit permanecem parciais.

**Entradas**

- Lista explícita de1–100 arquivos PNG/JPEG/BMP/WebP simples ou TIFF multipágina; até100 páginas somadas, DPI72–600 e destino.pdf novo.
- OCR: PDF local não criptografado de1–20 páginas, SHA256 da fonte, idioma por/eng/por+eng,150/300DPI e destino.pdf novo.

**Saídas**

- PDF reaberto com páginas e dimensões verificadas, orientação EXIF aplicada e transparência sobre branco.
- Confirmação com hashes de fontes/resultado, tamanhos de página e DPI. RGB Flate sem nova perda JPEG; sem gestão ICC.
- OCR: cópia rasterizada com camada de texto, hashes, dimensões e aviso das páginas sem texto detectado; sem preservação de links/formulários/assinaturas/metadados.
- TIFF: páginas por arquivo em ordem interna, proveniência por página com input/frame/frame_count e input_count; RGB8 sem ICC/precisão16bit/metadados. Uma falha recusa o lote completo.

**Erros e casos excepcionais**

- Formato inválido/animado, limite excedido ou fonte alterada: Recusar lote inteiro e remover temporários em falha tratada; nenhuma fonte é alterada.
- Destino existente ou que aparece durante a conversão: Recusar criação sem sobrescrever arquivo.
- Cancelamento/fechamento da janela: Encerrar worker e descartar callbacks antigos; avisar para conferir destino, pois pode haver temporário/saída parcial ou já concluída.
- OCR indisponível, idioma ausente, PDF criptografado, geometria/limite/tempo inválidos ou renderização incompleta: Recusar sem publicar cópia concluída; original preservado.

**Estado e efeitos**

- Fontes intactas; sem varredura, serviço remoto ou execução de anexos.
- Metadados EXIF/ICC não são copiados. Limites e garantia de limpeza somente para falhas tratadas constam no contrato.

**Critérios planejados**

- **S12-24-1** (nominal, contrato próprio atual, `not_run`): dado PNG/JPEG sintéticos ordenados e DPI suportado. Ação: Converter para PDF em caminho novo. Esperado: Criar novo PDF RGB com orientação, ordem e dimensões declaradas; fontes intactas.
- **S12-24-2** (exception, contrato próprio atual, `not_run`): dado Arquivo GIF ou PNG/JPEG inválido. Ação: Solicitar conversão. Esperado: Recusar lote sem criar saída concluída e sem substituir arquivo existente.

**Lacunas da referência Foxit**

- Inventário real Reader/Editor, fidelidade, formatos, OCR e serviços; não implementado como família completa.

Fontes: [app/pdf_creation.py](../app/pdf_creation.py), [app/creation_window.py](../app/creation_window.py), [app/search_tasks.py](../app/search_tasks.py), [app/worker_cli.py](../app/worker_cli.py), [app/main.py](../app/main.py), [docs/CRIACAO-IMAGENS.md](../docs/CRIACAO-IMAGENS.md), [app/local_files.py](../app/local_files.py), [app/folder_dialogs.py](../app/folder_dialogs.py), [docs/PASTAS-SINCRONIZADAS.md](../docs/PASTAS-SINCRONIZADAS.md), [testes/resultados/0.1.10/validation-review.json](../testes/resultados/0.1.10/validation-review.json), [app/pdf_ocr.py](../app/pdf_ocr.py), [app/ocr_window.py](../app/ocr_window.py), [docs/OCR-LOCAL.md](../docs/OCR-LOCAL.md), [testes/resultados/ocr-portable-2026-10-18-round1.json](../testes/resultados/ocr-portable-2026-10-18-round1.json), [testes/resultados/0.1.11/validation-review.json](../testes/resultados/0.1.11/validation-review.json), [docs/TIFF-MULTIPAGINA.md](../docs/TIFF-MULTIPAGINA.md), [testes/resultados/tiff-multipage-portable-2026-10-18-round2.json](../testes/resultados/tiff-multipage-portable-2026-10-18-round2.json), [testes/resultados/tiff-creation-existing-2026-10-18-round2.json](../testes/resultados/tiff-creation-existing-2026-10-18-round2.json), [docs/FOXIT-REA.md](../docs/FOXIT-REA.md).

Testes próprios existentes, sem nova execução nesta tabela: [test_order_dimensions_lossless_rgb_and_source_identity](../tests/test_pdf_creation.py); [test_alpha_and_palette_transparency_are_composited_on_white](../tests/test_pdf_creation.py); [test_exif_orientation_applied_and_private_metadata_not_copied](../tests/test_pdf_creation.py); [test_corrupt_unsupported_animated_and_truncated_inputs_leave_no_output](../tests/test_pdf_creation.py); [test_partial_final_write_removed_on_handled_failure](../tests/test_pdf_creation.py); [test_ordered_creation_opens_actual_pdf_and_poppler_renders_pixels](../tests/test_creation_gtk.py); [test_cancel_and_destroy_kill_real_worker_without_stale_callbacks](../tests/test_creation_gtk.py); [test_pinned_fixture_manifest_matches_sources_and_oriented_dimensions](../tests/test_pdf_creation.py); [test_final_name_is_absent_while_real_copy_is_in_progress](../tests/test_sync_folders.py); [test_save_copy_uses_worker_preserves_original_and_only_confirms_local_save](../tests/test_sync_folders_gtk.py); [test_bmp_webp_and_single_tiff_preserve_pixels_dimensions_and_order](../tests/test_pdf_creation.py); [test_webp_alpha_is_composited_over_white](../tests/test_pdf_creation.py); [test_multiframe_tiff_is_imported_and_animated_webp_is_refused](../tests/test_pdf_creation.py); [test_bmp_renamed_as_jpeg_is_identified_by_content](../tests/test_pdf_creation.py); [test_real_worker_supports_compressed_tiff_without_external_conversion](../tests/test_pdf_creation.py); [test_bmp_webp_tiff_selection_worker_and_opening](../tests/test_creation_gtk.py); [test_raster_copy_pipeline_preserves_order_dimensions_hashes_and_original](../tests/test_pdf_ocr.py); [test_encrypted_input_is_rejected_without_attempting_empty_password](../tests/test_pdf_ocr.py); [test_real_english_worker_adds_searchable_text_and_keeps_scan](../tests/test_ocr_linux.py); [test_cancel_stops_worker_and_its_actual_tesseract_child](../tests/test_ocr_linux.py); [test_menu_workflow_recognizes_opens_and_renders_actual_copy](../tests/test_ocr_gtk.py); [test_file_order_expands_all_tiff_pages_with_dimensions_and_provenance](../tests/test_tiff_multipage.py); [test_each_frame_orientation_is_applied_once_without_leaking_tags](../tests/test_tiff_multipage.py); [test_cyclic_out_of_range_and_truncated_ifd_chains_are_not_silently_shortened](../tests/test_tiff_multipage.py); [test_real_worker_reports_input_count_frame_mapping_and_page_count](../tests/test_tiff_multipage.py); [test_tiff_block_order_expands_pages_and_poppler_renders_each_color](../tests/test_creation_gtk.py); [test_multipage_tiff_import_feeds_searchable_ocr_without_losing_blank_page](../tests/test_ocr_linux.py).

<a id="platform"></a>

## Integrações de sistema/atualização

Requisito futuro: contratos separados para portais Linux/Flatpak, associação de arquivos, impressão e atualização.

**Entradas**

- Ação específica do sistema, arquivo autorizado pelo portal ou artefato de atualização identificado.
- Backend/ambiente versionados; nenhum instalador ou atualização é executado pela especificação.

**Saídas**

- Proposta: autorização/handle do portal ou cancelamento; atualização com origem/estado verificável e política própria.
- O Flatpak devel e os adaptadores existentes são evidências parciais, não paridade de todas as integrações Windows.

**Erros e casos excepcionais**

- Portal cancelado ou acesso revogado: Proposta: não usar caminhos não autorizados e preservar o documento atual.
- Atualização sem integridade/origem verificável: Proposta: não instalar; manter a versão corrente utilizável.

**Estado e efeitos**

- Proposta: associações, instalações e alterações do sistema exigem tarefa/escopo explícitos; esta etapa não as executa.

**Critérios planejados**

- **S12-25-1** (nominal, proposta futura, `not_run`): dado Desktop Linux/Flatpak de teste e PDF selecionado em portal. Ação: Conceder acesso e abrir o arquivo. Esperado: Proposta: abrir apenas o recurso autorizado, registrando ambiente e URI/caminho aplicável.
- **S12-25-2** (exception, proposta futura, `not_run`): dado Portal foi cancelado pelo usuário. Ação: Retornar à aplicação. Esperado: Proposta: nenhum acesso ampliado nem sucesso falso; documento corrente preservado.

**Lacunas da referência Foxit**

- Portais em desktop real, integração shell/browser, atualização, rollback e equivalência do adaptador Windows.

Fontes: [docs/instalacao.md](../docs/instalacao.md), [app/platform_runtime.py](../app/platform_runtime.py), [app/cups_backend.py](../app/cups_backend.py), [docs/FOXIT-REA.md](../docs/FOXIT-REA.md).

A especificação de referência e a consolidação da fase A continuam parciais. Não promover propostas, presença de recursos ou testes próprios a funcionalidade Foxit recuperada.
