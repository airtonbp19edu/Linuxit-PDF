# Registro de contratos funcionais — etapa 12

Gerado de `especificacao-funcional.json` por `scripts/validate_functional_spec.py`.

Escopo: **25 famílias identificadas**, **65 cenários planejados**; 25 subconjuntos implementados e 0 propostas futuras. O inventário global permanece aberto.

O campo esperado é do contrato próprio atual ou de uma proposta explicitamente identificada. Execuções próprias registradas: **65**, das quais 65 aprovadas; cada uma aponta o arquivo de resultado e a revisão do código. Expectativas/observações Foxit dos cenários completos S12 permanecem `null`. Observações parciais preservadas por família são registradas separadamente. Referenciar um teste existente não o executa novamente nem comprova paridade. As duas situações de cada família são um início de cobertura, não uma lista exaustiva.

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
| [Nuvem/colaboração](#cloud) | Subconjunto atual; lacunas abertas |
| [Criação/conversão](#conversion) | Subconjunto atual; lacunas abertas |
| [Integrações de sistema/atualização](#platform) | Subconjunto atual; lacunas abertas |

<a id="open-render"></a>

## Abrir PDF e renderizar páginas

Abertura local transacional com senha, cópia privada de leitura e recuperação consentida de estruturas interpretáveis pelo pypdf. Valida render inicial antes da troca. Falha/cancelamento preserva leitura anterior. Original não é sobrescrito; recuperação universal, assinatura da representação e impressão cifrada/recuperada não aprovadas.

**Entradas**

- Caminho de PDF local legível; página interna baseada em zero.
- Viewport, tamanho solicitado e identidade do documento para cache.
- Senha opcional até127caracteres e consentimento separado para leitura recuperada.

**Saídas**

- document_info: pages, sizes após CropBox/rotação intrínseca e metadata (title, author, subject, creator, producer).
- Imagem de página concluída; render obsoleto não deve substituir o documento atual.
- Sessão preparada e primeira imagem verificadas antes da troca; representação privada cifrada/recuperada quando necessária.

**Erros e casos excepcionais**

- Arquivo ausente, inválido, vazio ou protegido sem senha vazia válida: Falha do parser/worker; abertura não pode ser registrada como bem-sucedida. Mensagens e preservação do documento anterior precisam de teste GUI.
- Processo de renderização falha, excede tempo ou é cancelado: Erro/cancelamento sem publicar imagem parcial; subprocesso cancelável tem prazo próprio.
- Senha incorreta, recuperação recusada ou candidato inválido: Manter documento anterior; mostrar erro fixo sem credencial; permitir cancelar.

**Estado e efeitos**

- Cache local pode ser criado; original permanece sem edição.
- Abertura/fechamento muda o documento e invalida trabalhos da geração anterior.
- Representação temporária usada somente para leitura, com leases para leitores ativos; original intacto.

**Critérios planejados**

- **S12-01-1** (nominal, contrato próprio atual, `passed`): dado busca-escopos.pdf legível. Ação: Inspecionar e abrir as duas páginas. Esperado: pages=2; tamanhos positivos; a imagem de cada página pertence ao documento aberto. Execução própria em 2026-10-20T15:17:52-03:00, revisão `ba38ca70e875`, fronteira worker info + rendering.render_page: [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e10.json).
- **S12-01-2** (exception, contrato próprio atual, `passed`): dado Arquivo inexistente ou PDF inválido. Ação: Solicitar inspeção/abertura. Esperado: O parser/worker falha; não produzir uma página válida fictícia. Execução própria em 2026-10-20T15:17:52-03:00, revisão `ba38ca70e875`, fronteira worker info: [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e10.json).

**Lacunas da referência Foxit**

- D15 independent correct password and bounded opening/error/copy variants are observed; remaining recovery/rendering states remain open.
- The own security backend authenticates known passwords, but opening/rendering in the main viewer does not have the complete password flow.

**Observação parcial preservada do original:** Abertura/erros/cópia em recortes; senha correta em abertura independenteD15 abriu8 páginas. Não é contrato completo de recuperação/renderização.

Evidências: [docs/VM-FOXIT-2026-10-18.md](../docs/VM-FOXIT-2026-10-18.md), [docs/VM-SENHA-E-PARADA-2026-10-18.md](../docs/VM-SENHA-E-PARADA-2026-10-18.md).

Fontes: [app/rendering.py](../app/rendering.py), [app/main.py](../app/main.py), [app/async_core.py](../app/async_core.py), [app/local_files.py](../app/local_files.py), [app/folder_dialogs.py](../app/folder_dialogs.py), [docs/PASTAS-SINCRONIZADAS.md](../docs/PASTAS-SINCRONIZADAS.md), [app/document_session.py](../app/document_session.py), [app/navigation.py](../app/navigation.py), [app/page_surface.py](../app/page_surface.py), [docs/LEITURA-ABERTURA-NAVEGACAO-APRESENTACAO.md](../docs/LEITURA-ABERTURA-NAVEGACAO-APRESENTACAO.md), [testes/resultados/0.1.16/validation-review.json](../testes/resultados/0.1.16/validation-review.json), [docs/ETAPA-11.md](../docs/ETAPA-11.md), [docs/windows-evidence/foxit-rea/ui-state-contracts-2026-10-16.json](../docs/windows-evidence/foxit-rea/ui-state-contracts-2026-10-16.json), [docs/REA-ESTATICA-BUSCA-IMPRESSAO-2026-10-18.md](../docs/REA-ESTATICA-BUSCA-IMPRESSAO-2026-10-18.md), [docs/REA-ESTATICA-CONTINUACAO-2026-10-18.md](../docs/REA-ESTATICA-CONTINUACAO-2026-10-18.md), [docs/VM-FOXIT-2026-10-18.md](../docs/VM-FOXIT-2026-10-18.md), [docs/VM-SENHA-E-PARADA-2026-10-18.md](../docs/VM-SENHA-E-PARADA-2026-10-18.md).

Testes próprios existentes, sem nova execução nesta tabela: [test_cache_distinguishes_documents](../tests/test_regressions.py); [test_latest_renderer_skips_obsolete_queue_entries](../tests/test_viewer.py); [test_final_name_is_absent_while_real_copy_is_in_progress](../tests/test_sync_folders.py); [test_save_copy_uses_worker_preserves_original_and_only_confirms_local_save](../tests/test_sync_folders_gtk.py); [test_broken_xref_requires_consent_then_recovers_content](../tests/test_document_session.py); [test_cancellation_before_worker_leaves_no_reading_file](../tests/test_document_session.py); [test_close_waits_for_active_reader_and_removes_private_view](../tests/test_document_session.py); [test_invalid_request_and_existing_view_are_refused](../tests/test_document_session.py); [test_irrecoverable_and_empty_sources_do_not_publish_view](../tests/test_document_session.py); [test_owner_password_can_read_without_rewriting_original_permissions](../tests/test_document_session.py); [test_password_is_absent_from_argv_and_worker_errors](../tests/test_document_session.py); [test_password_required_then_invalid_then_correct_in_real_worker](../tests/test_document_session.py); [test_plain_session_preserves_original_identity_and_no_view_copy](../tests/test_document_session.py); [test_private_reading_file_is_not_world_readable](../tests/test_document_session.py); [test_unicode_password_and_original_permission_policy](../tests/test_document_session.py); [test_page_bounds_and_rejected_nonintegers](../tests/test_document_session.py); [test_rotated_fit_page_stays_in_viewport](../tests/test_document_session.py); [test_zoom_percent_decimal_and_clamped_bounds](../tests/test_document_session.py); [test_authenticated_open_renders_searches_and_presents_without_mutating_source](../tests/test_reading_workflows_gtk.py); [test_cancel_password_and_wrong_password_preserve_previous_document](../tests/test_reading_workflows_gtk.py); [test_changed_source_after_initial_render_does_not_commit](../tests/test_reading_workflows_gtk.py); [test_document_close_cancels_open_and_resets_controls](../tests/test_reading_workflows_gtk.py); [test_failed_open_preserves_document_page_and_image](../tests/test_reading_workflows_gtk.py); [test_first_render_failure_does_not_commit_candidate](../tests/test_reading_workflows_gtk.py); [test_real_password_dialog_masks_and_clears_entry](../tests/test_reading_workflows_gtk.py); [test_recovery_decline_then_accept_preserves_original_and_content](../tests/test_reading_workflows_gtk.py); [test_superseded_open_cannot_replace_newer_document_and_cleans_session](../tests/test_reading_workflows_gtk.py).

Relacionados aos planos dinâmicos/UI: D01, D02, D13, D14, D15, D19, D20.

<a id="navigation"></a>

## Navegação/rotação/zoom

Navegação por página e teclado com limites, zoom digitável1–6400% e ajustar página/largura, rotação/CropBox e viewport virtual. Raster tem limite de resolução; não promete nitidez ilimitada ou geometria integral Foxit.

**Entradas**

- Documento carregado e índice solicitado; indicação UI usa página baseada em um.
- Ação anterior/próxima, percentual de zoom, ajustar página/largura ou giro.
- Percentual de zoom finito1–6400; página inteira limitada ao documento.

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

- **S12-02-1** (nominal, contrato próprio atual, `passed`): dado PDF de duas páginas na primeira página. Ação: Navegar para a segunda e girar a visualização. Esperado: Página selecionada é a segunda; transformação visual permanece coerente com a geometria. Execução própria em 2026-10-20T15:17:52-03:00, revisão `ba38ca70e875`, fronteira PDFWindow.goto_page/_rotate: [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e10.json).
- **S12-02-2** (exception, contrato próprio atual, `passed`): dado Render da página anterior ainda em andamento. Ação: Mudar página e aguardar os callbacks. Esperado: O resultado obsoleto não toma o lugar da página atual. Execução própria em 2026-10-20T15:17:54-03:00, revisão `ba38ca70e875`, fronteira PDFWindow.request_render callbacks: [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e10.json).

**Lacunas da referência Foxit**

- Limites e modos efetivos Foxit dependem da classe/estado ativo.
- Updaters de zoom só enviam desabilitação nos limites; política completa não foi reconstruída.

**Observação parcial preservada do original:** UI03/04 em geometria.pdf: sem documento controles pálidos; Next1→2→3, Last8/8 e Next mantém8/8. Menu1% e6400%; menos/mais nos extremos mantêm os valores. FitPage47.15%, PAGE0011/8. Recorte visual sem vínculo comprovado aos IDs estáticos; entradas arbitrárias e demais modos abertos.

Evidências: [docs/VM-FOXIT-2026-10-18.md](../docs/VM-FOXIT-2026-10-18.md), [docs/VM-SENHA-E-PARADA-2026-10-18.md](../docs/VM-SENHA-E-PARADA-2026-10-18.md), [docs/P03-INTERFACE-E-PARADA-2026-10-19.md](../docs/P03-INTERFACE-E-PARADA-2026-10-19.md).

Fontes: [app/main.py](../app/main.py), [app/page_cache.py](../app/page_cache.py), [app/rendering.py](../app/rendering.py), [app/pdf_changes.py](../app/pdf_changes.py), [app/edit_tasks.py](../app/edit_tasks.py), [app/worker_cli.py](../app/worker_cli.py), [docs/SEGURANCA-ACESSIBILIDADE.md](../docs/SEGURANCA-ACESSIBILIDADE.md), [app/local_files.py](../app/local_files.py), [app/folder_dialogs.py](../app/folder_dialogs.py), [docs/PASTAS-SINCRONIZADAS.md](../docs/PASTAS-SINCRONIZADAS.md), [app/document_session.py](../app/document_session.py), [app/navigation.py](../app/navigation.py), [app/page_surface.py](../app/page_surface.py), [docs/LEITURA-ABERTURA-NAVEGACAO-APRESENTACAO.md](../docs/LEITURA-ABERTURA-NAVEGACAO-APRESENTACAO.md), [testes/resultados/0.1.16/validation-review.json](../testes/resultados/0.1.16/validation-review.json), [docs/ETAPA-11.md](../docs/ETAPA-11.md), [docs/windows-evidence/foxit-rea/ui-state-contracts-2026-10-16.json](../docs/windows-evidence/foxit-rea/ui-state-contracts-2026-10-16.json), [docs/windows-evidence/foxit-rea/zoom-presets.json](../docs/windows-evidence/foxit-rea/zoom-presets.json), [docs/REA-ESTATICA-BUSCA-IMPRESSAO-2026-10-18.md](../docs/REA-ESTATICA-BUSCA-IMPRESSAO-2026-10-18.md), [docs/REA-ESTATICA-CONTINUACAO-2026-10-18.md](../docs/REA-ESTATICA-CONTINUACAO-2026-10-18.md), [docs/VM-FOXIT-2026-10-18.md](../docs/VM-FOXIT-2026-10-18.md), [docs/VM-SENHA-E-PARADA-2026-10-18.md](../docs/VM-SENHA-E-PARADA-2026-10-18.md), [docs/P03-INTERFACE-E-PARADA-2026-10-19.md](../docs/P03-INTERFACE-E-PARADA-2026-10-19.md).

Testes próprios existentes, sem nova execução nesta tabela: [test_search_navigation_selection_and_rotation](../tests/test_gui.py); [test_intrinsic_rotation_and_cropbox_match_text_geometry](../tests/test_regressions.py); [test_five_panel_headers_fit_default_and_small_window](../tests/test_sidebar_layout_gtk.py); [test_combined_edits_preserve_tree_destinations_geometry_and_source](../tests/test_extended_edits.py); [test_final_name_is_absent_while_real_copy_is_in_progress](../tests/test_sync_folders.py); [test_save_copy_uses_worker_preserves_original_and_only_confirms_local_save](../tests/test_sync_folders_gtk.py); [test_page_bounds_and_rejected_nonintegers](../tests/test_document_session.py); [test_rotated_fit_page_stays_in_viewport](../tests/test_document_session.py); [test_zoom_percent_decimal_and_clamped_bounds](../tests/test_document_session.py); [test_keyboard_page_changes_do_not_move_focus_to_thumbnail_list](../tests/test_reading_workflows_gtk.py); [test_page_entries_clamp_and_restore_invalid_value_and_disable_edges](../tests/test_reading_workflows_gtk.py); [test_rotated_cropbox_geometry_matches_selection_and_presentation](../tests/test_reading_workflows_gtk.py); [test_zoom_extremes_use_logical_surface_and_reject_nonfinite_input](../tests/test_reading_workflows_gtk.py).

Relacionados aos planos dinâmicos/UI: D03, UI03, UI04.

<a id="presentation"></a>

## Apresentação ajustar/preencher

Apresentação GTK ajustar/preencher, pan/zoom/ponteiro, sessão/rotação herdadas, foco/F6/Tab/Escape e seleção de monitor/fallback. Fullscreen depende do compositor; validação virtual não aprova hardware físico.

**Entradas**

- Documento, tamanhos de página, página inicial e dimensões do monitor/view.
- Ações de navegação, fit/fill, pan e cor do ponteiro.
- MonitorGDK selecionado e eventos de remoção/restauração; sessão/rotação herdadas.

**Saídas**

- Janela de apresentação com página assíncrona e imagem centralizada/recortada segundo o modo.
- Estado de erro visível quando a renderização falha.

**Erros e casos excepcionais**

- Renderização falha: A janela registra o erro; não reutilizar imagem de documento diferente.
- Janela fecha durante tarefa: Cancelar/descartar tarefas e impedir atualização de widgets destruídos.

**Estado e efeitos**

- Estado de tela/ponteiro é local; original não é modificado.

**Critérios planejados**

- **S12-03-1** (nominal, contrato próprio atual, `passed`): dado Página retrato e viewport paisagem. Ação: Alternar ajustar página e preencher. Esperado: A escala e o centro respeitam o modo próprio; não atribuir esse cálculo ao Foxit. Execução própria em 2026-10-20T15:17:56-03:00, revisão `ba38ca70e875`, fronteira PresentationWindow fit/fill: [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e10.json).
- **S12-03-2** (exception, contrato próprio atual, `passed`): dado Worker retorna falha de imagem. Ação: Entregar o erro à apresentação. Esperado: Exibir estado de falha, mantendo o ciclo de vida da janela válido. Execução própria em 2026-10-20T15:17:58-03:00, revisão `ba38ca70e875`, fronteira PresentationWindow render failure: [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e10.json).

**Lacunas da referência Foxit**

- Ajuste/preenchimento, atalhos e múltiplos monitores do original não foram observados.

Fontes: [app/presentation.py](../app/presentation.py), [app/page_cache.py](../app/page_cache.py), [app/document_session.py](../app/document_session.py), [app/navigation.py](../app/navigation.py), [app/page_surface.py](../app/page_surface.py), [docs/LEITURA-ABERTURA-NAVEGACAO-APRESENTACAO.md](../docs/LEITURA-ABERTURA-NAVEGACAO-APRESENTACAO.md), [testes/resultados/0.1.16/validation-review.json](../testes/resultados/0.1.16/validation-review.json), [docs/FOXIT-REA.md](../docs/FOXIT-REA.md).

Testes próprios existentes, sem nova execução nesta tabela: [test_presentation_fit_fill_center_and_error](../tests/test_viewer.py); [test_presentation_handles_portrait_and_landscape](../tests/test_viewer.py); [test_monitor_selection_removal_and_fullscreen_request](../tests/test_reading_workflows_gtk.py); [test_presentation_keys_respect_control_focus_and_restore_parent_focus](../tests/test_reading_workflows_gtk.py); [test_rotated_cropbox_geometry_matches_selection_and_presentation](../tests/test_reading_workflows_gtk.py).

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

- **S12-04-1** (nominal, contrato próprio atual, `passed`): dado Fixture de busca; só páginas, sem caixa/palavra inteira. Ação: Pesquisar alvo. Esperado: Contrato próprio: três ocorrências; palavra inteira reduz para duas. Execução própria em 2026-10-20T15:17:59-03:00, revisão `ba38ca70e875`, fronteira search_engine.TextSearchIndex: [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e10.json).
- **S12-04-2** (exception, contrato próprio atual, `passed`): dado Consulta com 257 caracteres. Ação: Chamar TextSearchIndex.search. Esperado: ValueError antes de extrair páginas. Execução própria em 2026-10-20T15:17:59-03:00, revisão `ba38ca70e875`, fronteira search_engine.TextSearchIndex: [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e10.json).

**Lacunas da referência Foxit**

- Normalização e algoritmos completos do Foxit; ordem/limites/destaques precisam de comparação.

**Observação parcial preservada do original:** D12 no corpus5000: Stop ativo encerra e preserva232 resultados; troca para geometria mantém busca em12.pdf; fechar12.pdf durante busca encerra em1738 e conserva lista parcial. Contagens não determinísticas/latência não medida; contrato próprio não substituído. D10 misto anterior preservado.

Evidências: [docs/VM-FOXIT-2026-10-18.md](../docs/VM-FOXIT-2026-10-18.md), [docs/VM-BUSCA-2026-10-18-2020.md](../docs/VM-BUSCA-2026-10-18-2020.md), [docs/P03-BUSCA-IMPRESSAO-2026-10-19.md](../docs/P03-BUSCA-IMPRESSAO-2026-10-19.md), [docs/P03-CANCELAMENTO-MOSAICO-2026-10-19.md](../docs/P03-CANCELAMENTO-MOSAICO-2026-10-19.md).

Fontes: [app/search_engine.py](../app/search_engine.py), [app/main.py](../app/main.py), [app/rendering.py](../app/rendering.py), [testes/resultados/0.1.16/validation-review.json](../testes/resultados/0.1.16/validation-review.json), [docs/REA-BUSCA-IMPRESSAO.md](../docs/REA-BUSCA-IMPRESSAO.md), [docs/windows-evidence/foxit-rea/search-print-contracts.json](../docs/windows-evidence/foxit-rea/search-print-contracts.json), [docs/REA-ESTATICA-CONTINUACAO-2026-10-18.md](../docs/REA-ESTATICA-CONTINUACAO-2026-10-18.md), [docs/VM-FOXIT-2026-10-18.md](../docs/VM-FOXIT-2026-10-18.md), [docs/VM-BUSCA-2026-10-18-2020.md](../docs/VM-BUSCA-2026-10-18-2020.md), [docs/P03-BUSCA-IMPRESSAO-2026-10-19.md](../docs/P03-BUSCA-IMPRESSAO-2026-10-19.md), [docs/P03-CANCELAMENTO-MOSAICO-2026-10-19.md](../docs/P03-CANCELAMENTO-MOSAICO-2026-10-19.md).

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

- **S12-05-1** (nominal, contrato próprio atual, `passed`): dado Fixture com dois títulos contendo alvo, só marcadores. Ação: Pesquisar alvo e selecionar os resultados. Esperado: Dois hits; um aponta à segunda página e outro permanece page=null; rects=[] em ambos. Execução própria em 2026-10-20T15:17:59-03:00, revisão `ba38ca70e875`, fronteira PDFWindow find bar + _select_search_hit: [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e10.json).
- **S12-05-2** (exception, contrato próprio atual, `passed`): dado Hit de marcador sem destino local. Ação: Selecionar esse resultado. Esperado: Não fabricar página de destino ou retângulo de destaque. Execução própria em 2026-10-20T15:18:02-03:00, revisão `ba38ca70e875`, fronteira PDFWindow _select_search_hit: [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e10.json).

**Lacunas da referência Foxit**

- Classe dos IDs 7911/7913 e comportamento de busca/navegação Foxit.
- A junção estrutural de ID 7913 ao handler de +0x1d58 continua ambígua.

**Observação parcial preservada do original:** D07: dois hits selecionam marcadores no painel; ativação nativa do primeiro navega1→2. Seleção/duplo clique no resultado não provou salto; segundo mantém página2 sem diálogo. Não inferir destino nulo.

Evidências: [docs/VM-FOXIT-2026-10-18.md](../docs/VM-FOXIT-2026-10-18.md), [docs/VM-BUSCA-2026-10-18-2020.md](../docs/VM-BUSCA-2026-10-18-2020.md), [docs/P03-BUSCA-IMPRESSAO-2026-10-19.md](../docs/P03-BUSCA-IMPRESSAO-2026-10-19.md).

Fontes: [app/search_engine.py](../app/search_engine.py), [app/pdf_panels.py](../app/pdf_panels.py), [testes/resultados/0.1.16/validation-review.json](../testes/resultados/0.1.16/validation-review.json), [docs/REA-BUSCA-IMPRESSAO.md](../docs/REA-BUSCA-IMPRESSAO.md), [docs/windows-evidence/foxit-rea/search-print-contracts.json](../docs/windows-evidence/foxit-rea/search-print-contracts.json), [docs/windows-evidence/foxit-rea/search-checkbox-bindings.json](../docs/windows-evidence/foxit-rea/search-checkbox-bindings.json), [docs/REA-ESTATICA-CONTINUACAO-2026-10-18.md](../docs/REA-ESTATICA-CONTINUACAO-2026-10-18.md), [docs/VM-FOXIT-2026-10-18.md](../docs/VM-FOXIT-2026-10-18.md), [docs/VM-BUSCA-2026-10-18-2020.md](../docs/VM-BUSCA-2026-10-18-2020.md), [docs/P03-BUSCA-IMPRESSAO-2026-10-19.md](../docs/P03-BUSCA-IMPRESSAO-2026-10-19.md).

Testes próprios existentes, sem nova execução nesta tabela: [test_bookmark_without_local_page_is_not_given_a_fake_destination](../tests/test_search_scopes.py); [test_ui_toggles_scopes_and_navigates_bookmark_result](../tests/test_search_scopes.py).

Relacionados aos planos dinâmicos/UI: D07, UI06.

<a id="search-comments"></a>

## Busca em comentários

Subconjunto próprio: assunto, conteúdo e autor pesquisados separadamente; respostas /IRT na mesma página, IDs de objetos, rich text textual e avisos de vínculos inválidos. Não modifica anotações.

**Entradas**

- Consulta, flags e include_comments=True; comentários com página associada.
- As demais fontes podem ficar desativadas.

**Saídas**

- Hits source=comment, página conhecida e rects=[].
- Assunto, conteúdo e autor são pesquisáveis pelas mesmas opções de consulta; resultados de metadados não recebem retângulos inventados.
- Hits identificam campo e comentário/resposta; referências repetidas ao mesmo objeto não duplicam resultados. Comentários distintos com texto igual são preservados.

**Erros e casos excepcionais**

- Sem texto pesquisável ou termo ausente: Nenhum hit correspondente; não tratar ausência como falha de motor.
- Cache pertence a arquivo alterado: Falhar e pedir reabertura antes de publicar novos resultados.

**Estado e efeitos**

- A leitura não cria nem altera anotações; pode navegar à página.

**Critérios planejados**

- **S12-06-1** (nominal, contrato próprio atual, `passed`): dado Só comentários da fixture. Ação: Pesquisar assunto, depois alvo. Esperado: Uma ocorrência em cada consulta; o campo assunto é separado do conteúdo. Execução própria em 2026-10-20T15:18:04-03:00, revisão `ba38ca70e875`, fronteira search_engine.TextSearchIndex: [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e10.json).
- **S12-06-2** (exception, contrato próprio atual, `passed`): dado Só comentários, consulta Autor. Ação: Pesquisar o campo de autor com o contrato corrigido na fonte posterior ao pacote0.1.13. Esperado: Uma ocorrência source=comment na página1 do fixture preservado; autoria é pesquisável junto de assunto/conteúdo. Execução própria em 2026-10-20T15:18:04-03:00, revisão `ba38ca70e875`, fronteira search_engine.TextSearchIndex: [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e10.json).

**Lacunas da referência Foxit**

- Demais tipos e campos pesquisados, respostas, duplicação entre campos, ordenação e destinos da busca mista. A observação inicial cobre somente a nota sintética preservada.

**Observação parcial preservada do original:** Recortes de corpo/assunto/autor preservados; D10 seleciona nota na página1 e abre Format sem editar. Autor corrigido somente na fonte; demais tipos/respostas ainda abertos.

Evidências: [docs/VM-FOXIT-2026-10-18.md](../docs/VM-FOXIT-2026-10-18.md), [docs/BUSCA-AUTOR-COMENTARIOS.md](../docs/BUSCA-AUTOR-COMENTARIOS.md), [docs/P03-BUSCA-IMPRESSAO-2026-10-19.md](../docs/P03-BUSCA-IMPRESSAO-2026-10-19.md).

Fontes: [app/search_engine.py](../app/search_engine.py), [app/pdf_panels.py](../app/pdf_panels.py), [app/pdf_comments.py](../app/pdf_comments.py), [testes/resultados/0.1.16/validation-review.json](../testes/resultados/0.1.16/validation-review.json), [docs/REA-BUSCA-IMPRESSAO.md](../docs/REA-BUSCA-IMPRESSAO.md), [docs/windows-evidence/foxit-rea/search-print-contracts.json](../docs/windows-evidence/foxit-rea/search-print-contracts.json), [docs/REA-ESTATICA-CONTINUACAO-2026-10-18.md](../docs/REA-ESTATICA-CONTINUACAO-2026-10-18.md), [docs/VM-FOXIT-2026-10-18.md](../docs/VM-FOXIT-2026-10-18.md), [testes/resultados/vm-2026-10-18/foxit-observations.json](../testes/resultados/vm-2026-10-18/foxit-observations.json), [docs/BUSCA-AUTOR-COMENTARIOS.md](../docs/BUSCA-AUTOR-COMENTARIOS.md), [docs/P03-BUSCA-IMPRESSAO-2026-10-19.md](../docs/P03-BUSCA-IMPRESSAO-2026-10-19.md).

Testes próprios existentes, sem nova execução nesta tabela: [test_comment_subject_contents_and_author_are_searchable](../tests/test_search_scopes.py); [test_preserved_author_only_term_matches_the_recorded_page](../tests/test_search_comment_author.py); [test_author_matching_respects_case_whole_words_and_accents](../tests/test_search_comment_author.py); [test_comment_without_author_still_searches_subject_and_body](../tests/test_search_comment_author.py).

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

- **S12-07-1** (nominal, contrato próprio atual, `passed`): dado PDF sintético com anexo textual contendo alvo; fixture ainda a especializar. Ação: Pesquisar incluindo anexos. Esperado: Encontrar o termo no anexo suportado e identificar índice/nome/página interna sem destino principal fictício. Execução própria em 2026-10-20T15:18:04-03:00, revisão `ba38ca70e875`, fronteira worker search-attachments: [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e10.json).
- **S12-07-2** (exception, contrato próprio atual, `passed`): dado Mesmo PDF com um anexo não suportado. Ação: Pesquisar incluindo anexos. Esperado: Informar o anexo omitido e seu motivo; UI deve indicar anexos parciais. Execução própria em 2026-10-20T15:18:05-03:00, revisão `ba38ca70e875`, fronteira worker search-attachments: [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e10.json).

**Lacunas da referência Foxit**

- Travessia completa, extratores, formatos, limites, ordenação e associação de resultados no original.

Fontes: [app/attachment_search.py](../app/attachment_search.py), [app/search_tasks.py](../app/search_tasks.py), [app/search_matching.py](../app/search_matching.py), [app/pdf_attachments.py](../app/pdf_attachments.py), [app/search_engine.py](../app/search_engine.py), [app/worker_cli.py](../app/worker_cli.py), [app/main.py](../app/main.py), [app/attachment_formats.py](../app/attachment_formats.py), [app/attachment_rtf.py](../app/attachment_rtf.py), [app/attachment_images.py](../app/attachment_images.py), [testes/resultados/0.1.16/validation-review.json](../testes/resultados/0.1.16/validation-review.json), [docs/REA-BUSCA-IMPRESSAO.md](../docs/REA-BUSCA-IMPRESSAO.md), [docs/windows-evidence/foxit-rea/search-print-contracts.json](../docs/windows-evidence/foxit-rea/search-print-contracts.json), [docs/REA-ESTATICA-CONTINUACAO-2026-10-18.md](../docs/REA-ESTATICA-CONTINUACAO-2026-10-18.md).

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

- **S12-08-1** (nominal, contrato próprio atual, `passed`): dado Coleção sintética de dois documentos e índice em pasta nova. Ação: Construir índice e consultar um termo presente em um documento. Esperado: Criar/reabrir índice e localizar termo no PDF/página corretos, sem alterar fontes. Execução própria em 2026-10-20T15:18:05-03:00, revisão `ba38ca70e875`, fronteira worker index-build/index-search: [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e10.json).
- **S12-08-2** (exception, contrato próprio atual, `passed`): dado Uma fonte foi alterada após indexação. Ação: Consultar sem atualização completa. Esperado: Excluir a fonte alterada e indicar que precisa atualizar o índice. Execução própria em 2026-10-20T15:18:05-03:00, revisão `ba38ca70e875`, fronteira worker index-search: [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e10.json).

**Lacunas da referência Foxit**

- Formato e manutenção do índice completo, exclusões, locking, recuperação e disponibilidade Reader.

Fontes: [app/collection_index.py](../app/collection_index.py), [app/collection_window.py](../app/collection_window.py), [app/search_tasks.py](../app/search_tasks.py), [app/search_matching.py](../app/search_matching.py), [app/worker_cli.py](../app/worker_cli.py), [app/main.py](../app/main.py), [app/collection_recovery.py](../app/collection_recovery.py), [testes/resultados/0.1.16/validation-review.json](../testes/resultados/0.1.16/validation-review.json), [docs/windows-evidence/foxit-rea/index-interface.json](../docs/windows-evidence/foxit-rea/index-interface.json), [docs/FOXIT-REA.md](../docs/FOXIT-REA.md), [docs/REA-ESTATICA-BUSCA-IMPRESSAO-2026-10-18.md](../docs/REA-ESTATICA-BUSCA-IMPRESSAO-2026-10-18.md), [docs/REA-ESTATICA-CONTINUACAO-2026-10-18.md](../docs/REA-ESTATICA-CONTINUACAO-2026-10-18.md).

Testes próprios existentes, sem nova execução nesta tabela: [test_build_reopen_worker_and_query_preserve_sources_and_real_pages](../tests/test_collection_index.py); [test_changed_missing_sources_are_excluded_until_explicit_rebuild](../tests/test_collection_index.py); [test_update_failure_preserves_old_index_and_removes_temporary](../tests/test_collection_index.py); [test_collection_build_query_and_open_result_on_its_actual_page](../tests/test_search_extensions_gtk.py); [test_collection_changed_result_is_refused_before_opening](../tests/test_search_extensions_gtk.py); [test_closing_collection_terminates_pending_worker_without_callbacks](../tests/test_search_extensions_gtk.py).

<a id="search-language"></a>

## Stemming/proximidade/coringas

Atual (0.1.16): busca literal, coringas por palavra, proximidade ordenada e radicais por 36 opções de algoritmos Snowball 3.1.1 escolhidas explicitamente (sem detecção automática de idioma). Equivalência com o mecanismo do original (Lucene), tokenização universal e combinações com índice continuam abertas.

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

- **S12-09-1** (nominal, contrato próprio atual, `passed`): dado Corpus sintético com duas palavras separadas por distâncias conhecidas. Ação: Executar proximidade com duas distâncias explícitas. Esperado: Duas consultas com distâncias diferentes produzem hits conforme distância total/ordem documentadas. Execução própria em 2026-10-20T15:18:05-03:00, revisão `ba38ca70e875`, fronteira search_engine.TextSearchIndex: [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e10.json).
- **S12-09-2** (exception, contrato próprio atual, `passed`): dado Consulta com coringa/operador cuja sintaxe não foi implementada. Ação: Executar esse modo. Esperado: Recusar sintaxe/operador não suportado sem trocar silenciosamente para literal. Execução própria em 2026-10-20T15:18:05-03:00, revisão `ba38ca70e875`, fronteira search_engine.TextSearchIndex: [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e10.json).

**Lacunas da referência Foxit**

- Stemming por idioma, distância/proximidade, escaping, expansão e combinações com índice.

Fontes: [app/search_matching.py](../app/search_matching.py), [app/search_engine.py](../app/search_engine.py), [app/attachment_search.py](../app/attachment_search.py), [app/collection_index.py](../app/collection_index.py), [app/main.py](../app/main.py), [app/collection_window.py](../app/collection_window.py), [docs/proveniencia-snowball.json](../docs/proveniencia-snowball.json), [app/search_languages.py](../app/search_languages.py), [testes/resultados/0.1.16/validation-review.json](../testes/resultados/0.1.16/validation-review.json), [docs/REA-BUSCA-IMPRESSAO.md](../docs/REA-BUSCA-IMPRESSAO.md), [docs/windows-evidence/foxit-rea/search-print-contracts.json](../docs/windows-evidence/foxit-rea/search-print-contracts.json), [docs/ETAPA-11.md](../docs/ETAPA-11.md), [docs/REA-ESTATICA-BUSCA-IMPRESSAO-2026-10-18.md](../docs/REA-ESTATICA-BUSCA-IMPRESSAO-2026-10-18.md), [docs/REA-ESTATICA-CONTINUACAO-2026-10-18.md](../docs/REA-ESTATICA-CONTINUACAO-2026-10-18.md).

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

- **S12-10-1** (nominal, contrato próprio atual, `passed`): dado PDF sintético e retângulo contendo uma palavra conhecida. Ação: Selecionar e copiar. Esperado: Clipboard contém a palavra selecionada; a seleção acompanha a transformação da imagem. Execução própria em 2026-10-20T15:18:05-03:00, revisão `ba38ca70e875`, fronteira PDFWindow _finish_text_selection + clipboard: [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e10.json).
- **S12-10-2** (exception, contrato próprio atual, `passed`): dado Retângulo sobre região sem texto. Ação: Concluir seleção de texto. Esperado: Status informa ausência de texto; nenhum conteúdo fictício é produzido. Execução própria em 2026-10-20T15:18:07-03:00, revisão `ba38ca70e875`, fronteira PDFWindow _finish_text_selection: [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e10.json).

**Lacunas da referência Foxit**

- Ordem lógica, texto bidirecional, permissões de cópia, snapping e coordenadas de todos os modos do original.

Fontes: [app/main.py](../app/main.py), [app/rendering.py](../app/rendering.py), [app/text_selection.py](../app/text_selection.py), [app/character_selection.py](../app/character_selection.py), [app/character_extraction.py](../app/character_extraction.py), [testes/resultados/0.1.16/validation-review.json](../testes/resultados/0.1.16/validation-review.json), [docs/FOXIT-REA.md](../docs/FOXIT-REA.md).

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

- **S12-11-1** (nominal, contrato próprio atual, `passed`): dado Fixture e destino Salvar como PDF. Ação: Preparar saída e reabri-la. Esperado: Arquivo reabre e preserva o plano escolhido; sucesso de geração não é prova de impressão física. Execução própria em 2026-10-20T15:18:09-03:00, revisão `ba38ca70e875`, fronteira worker prepare-print: [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e10.json).
- **S12-11-2** (exception, contrato próprio atual, `passed`): dado Comando lp indisponível. Ação: Solicitar envio ao CUPS. Esperado: RuntimeError explícito; nenhum sucesso de envio é reportado. Execução própria em 2026-10-20T15:18:09-03:00, revisão `ba38ca70e875`, fronteira cups_backend.print_file: [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e10.json).

**Lacunas da referência Foxit**

- Predefinições, margens, fontes, flags, spooler físico e estados completos do original.

**Observação parcial preservada do original:** Duas novas saídas virtuais13.pdf/14.pdf; fechamento normal e consulta posterior sem Foxit/atualizador/splwow64, fila vazia. Espera histórica não reproduzida nem explicada; impressão física e fluxo completo abertos.

Evidências: [docs/VM-FOXIT-2026-10-18.md](../docs/VM-FOXIT-2026-10-18.md), [docs/P03-BUSCA-IMPRESSAO-2026-10-19.md](../docs/P03-BUSCA-IMPRESSAO-2026-10-19.md), [docs/P03-CANCELAMENTO-MOSAICO-2026-10-19.md](../docs/P03-CANCELAMENTO-MOSAICO-2026-10-19.md).

Fontes: [app/print_window.py](../app/print_window.py), [app/worker_cli.py](../app/worker_cli.py), [app/cups_backend.py](../app/cups_backend.py), [app/windows_print.py](../app/windows_print.py), [app/print_tasks.py](../app/print_tasks.py), [app/print_queue.py](../app/print_queue.py), [testes/resultados/0.1.16/validation-review.json](../testes/resultados/0.1.16/validation-review.json), [docs/REA-IMPRESSAO-CONSUMIDORES.md](../docs/REA-IMPRESSAO-CONSUMIDORES.md), [docs/windows-evidence/foxit-rea/windows-print-followup-contracts.json](../docs/windows-evidence/foxit-rea/windows-print-followup-contracts.json), [docs/AVANCO-SEM-VM.md](../docs/AVANCO-SEM-VM.md), [docs/REA-ESTATICA-BUSCA-IMPRESSAO-2026-10-18.md](../docs/REA-ESTATICA-BUSCA-IMPRESSAO-2026-10-18.md), [docs/REA-ESTATICA-CONTINUACAO-2026-10-18.md](../docs/REA-ESTATICA-CONTINUACAO-2026-10-18.md), [docs/VM-FOXIT-2026-10-18.md](../docs/VM-FOXIT-2026-10-18.md), [docs/P03-BUSCA-IMPRESSAO-2026-10-19.md](../docs/P03-BUSCA-IMPRESSAO-2026-10-19.md), [docs/P03-CANCELAMENTO-MOSAICO-2026-10-19.md](../docs/P03-CANCELAMENTO-MOSAICO-2026-10-19.md).

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

- **S12-12-1** (nominal, contrato próprio atual, `passed`): dado PDF sintético de oito páginas. Ação: Gerar livreto em ambos os lados e reabrir. Esperado: Quatro faces; ordem das duplas própria verificável, sem alterar o original. Execução própria em 2026-10-20T15:18:09-03:00, revisão `ba38ca70e875`, fronteira worker prepare-print (booklet): [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e10.json).
- **S12-12-2** (exception, contrato próprio atual, `passed`): dado pages_per_sheet=4.5. Ação: Preparar modo multiple. Esperado: ValueError, sem aceitar silenciosamente uma quantidade inteira diferente. Execução própria em 2026-10-20T15:18:09-03:00, revisão `ba38ca70e875`, fronteira imposition.prepare_output: [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e10.json).

**Lacunas da referência Foxit**

- Geometria completa, rotações, margens e ordenação de todas as combinações no Foxit.

**Observação parcial preservada do original:** N-up A4 retrato2x2/horizontal/margem4mm gerou2 páginas, sequência1-4/5-8 igual em C18-D18-nup. Mosaico200%/sobreposição5mm sem marcas/legendas gerou48 páginas, todas renderizadas. Livreto5mm/medianiz3mm, geometria e combinações completas ainda abertos.

Evidências: [docs/VM-FOXIT-2026-10-18.md](../docs/VM-FOXIT-2026-10-18.md), [docs/P03-BUSCA-IMPRESSAO-2026-10-19.md](../docs/P03-BUSCA-IMPRESSAO-2026-10-19.md), [docs/P03-CANCELAMENTO-MOSAICO-2026-10-19.md](../docs/P03-CANCELAMENTO-MOSAICO-2026-10-19.md).

Fontes: [app/imposition.py](../app/imposition.py), [app/worker_cli.py](../app/worker_cli.py), [testes/resultados/0.1.16/validation-review.json](../testes/resultados/0.1.16/validation-review.json), [docs/REA-IMPRESSAO-CONSUMIDORES.md](../docs/REA-IMPRESSAO-CONSUMIDORES.md), [docs/windows-evidence/foxit-rea/windows-print-followup-contracts.json](../docs/windows-evidence/foxit-rea/windows-print-followup-contracts.json), [docs/AVANCO-SEM-VM.md](../docs/AVANCO-SEM-VM.md), [docs/REA-ESTATICA-BUSCA-IMPRESSAO-2026-10-18.md](../docs/REA-ESTATICA-BUSCA-IMPRESSAO-2026-10-18.md), [docs/REA-ESTATICA-CONTINUACAO-2026-10-18.md](../docs/REA-ESTATICA-CONTINUACAO-2026-10-18.md), [docs/VM-FOXIT-2026-10-18.md](../docs/VM-FOXIT-2026-10-18.md), [docs/P03-BUSCA-IMPRESSAO-2026-10-19.md](../docs/P03-BUSCA-IMPRESSAO-2026-10-19.md), [docs/P03-CANCELAMENTO-MOSAICO-2026-10-19.md](../docs/P03-CANCELAMENTO-MOSAICO-2026-10-19.md).

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

- **S12-13-1** (nominal, contrato próprio atual, `passed`): dado Fixture com dois marcadores. Ação: Inspecionar o painel. Esperado: Dois títulos, nível registrado e destino local conhecido ou null; nenhuma escrita no PDF. Execução própria em 2026-10-20T15:18:09-03:00, revisão `ba38ca70e875`, fronteira worker panels: [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e10.json).
- **S12-13-2** (exception, contrato próprio atual, `passed`): dado Marcador sem página local. Ação: Exibir seu destino. Esperado: Não atribuir a primeira página por padrão. Execução própria em 2026-10-20T15:18:10-03:00, revisão `ba38ca70e875`, fronteira worker panels: [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e10.json).

**Lacunas da referência Foxit**

- Disponibilidade Reader dos diálogos, movimento hierárquico, undo/redo e persistência.

Fontes: [app/pdf_panels.py](../app/pdf_panels.py), [app/pdf_changes.py](../app/pdf_changes.py), [app/edit_tasks.py](../app/edit_tasks.py), [app/worker_cli.py](../app/worker_cli.py), [app/main.py](../app/main.py), [docs/SEGURANCA-ACESSIBILIDADE.md](../docs/SEGURANCA-ACESSIBILIDADE.md), [app/local_files.py](../app/local_files.py), [app/folder_dialogs.py](../app/folder_dialogs.py), [docs/PASTAS-SINCRONIZADAS.md](../docs/PASTAS-SINCRONIZADAS.md), [app/pdf_form_controls.py](../app/pdf_form_controls.py), [app/edit_history.py](../app/edit_history.py), [app/edit_dialogs.py](../app/edit_dialogs.py), [app/edit_window.py](../app/edit_window.py), [docs/EDICAO-COM-HISTORICO.md](../docs/EDICAO-COM-HISTORICO.md), [testes/resultados/0.1.10/validation-review.json](../testes/resultados/0.1.10/validation-review.json), [testes/resultados/0.1.16/validation-review.json](../testes/resultados/0.1.16/validation-review.json), [docs/FOXIT-REA.md](../docs/FOXIT-REA.md), [docs/ETAPA-11.md](../docs/ETAPA-11.md).

Testes próprios existentes, sem nova execução nesta tabela: [test_bookmark_without_local_page_is_not_given_a_fake_destination](../tests/test_search_scopes.py); [test_combined_copy_preserves_source_metadata_attachment_and_previous_objects](../tests/test_pdf_changes.py); [test_encryption_signature_permissions_xfa_and_portfolio_are_explicitly_unsupported](../tests/test_pdf_changes.py); [test_real_dialogs_and_worker_create_bookmark_note_and_form_copies](../tests/test_copy_edit_gtk.py); [test_reopening_same_document_during_dialog_blocks_stale_save](../tests/test_copy_edit_gtk.py); [test_existing_destination_is_preserved_and_busy_state_is_released](../tests/test_copy_edit_gtk.py); [test_combined_edits_preserve_tree_destinations_geometry_and_source](../tests/test_extended_edits.py); [test_final_name_is_absent_while_real_copy_is_in_progress](../tests/test_sync_folders.py); [test_save_copy_uses_worker_preserves_original_and_only_confirms_local_save](../tests/test_sync_folders_gtk.py); [test_info_distinguishes_checkbox_radio_choice_combo_and_multiselect](../tests/test_advanced_edits.py); [test_checkbox_sets_and_clears_value_and_visible_appearance](../tests/test_advanced_edits.py); [test_radio_activates_only_the_selected_widget_and_can_clear](../tests/test_advanced_edits.py); [test_radio_no_toggle_off_is_enforced](../tests/test_advanced_edits.py); [test_single_and_combo_values_indices_and_generated_appearances_roundtrip](../tests/test_advanced_edits.py); [test_multiselect_uses_export_values_and_canonical_indices](../tests/test_advanced_edits.py); [test_choice_selection_can_be_cleared](../tests/test_advanced_edits.py); [test_invalid_values_do_not_publish_partial_batch](../tests/test_advanced_edits.py); [test_read_only_and_unsupported_button_appearance_are_explicit](../tests/test_advanced_edits.py); [test_editable_combo_and_duplicate_exports_are_rejected](../tests/test_advanced_edits.py); [test_inherited_checkbox_flags_and_type_are_respected](../tests/test_advanced_edits.py); [test_checkbox_widget_absent_from_pages_is_unsupported](../tests/test_advanced_edits.py); [test_closed_outline_counts_remain_closed_after_move](../tests/test_advanced_edits.py); [test_move_preserves_subtree_destinations_and_sibling_links](../tests/test_advanced_edits.py); [test_move_child_to_root_and_reorder_same_parent](../tests/test_advanced_edits.py); [test_delete_bookmark_removes_subtree_and_last_root](../tests/test_advanced_edits.py); [test_move_into_descendant_invalid_positions_and_boolean_paths_are_refused](../tests/test_advanced_edits.py); [test_highlight_and_rectangle_roundtrip_geometry_print_flags_and_text](../tests/test_advanced_edits.py); [test_delete_supported_annotation_preserves_widgets_and_other_pages](../tests/test_advanced_edits.py); [test_locked_notes_widgets_and_replies_are_not_deleted](../tests/test_advanced_edits.py); [test_invalid_annotation_geometry_and_extra_parameters_are_rejected](../tests/test_advanced_edits.py); [test_undo_redo_rebuild_actual_pdfs_and_save_current_cursor_only](../tests/test_edit_history.py); [test_undo_all_restores_base_and_disables_save_until_redone](../tests/test_edit_history.py); [test_new_branch_discards_redo_but_invalid_branch_preserves_it](../tests/test_edit_history.py); [test_operation_values_are_defensively_copied](../tests/test_edit_history.py); [test_changed_original_blocks_add_undo_redo_and_save](../tests/test_edit_history.py); [test_existing_destination_is_not_overwritten_and_draft_survives](../tests/test_edit_history.py); [test_closed_session_refuses_work_and_removes_private_previews](../tests/test_edit_history.py); [test_pre_cancelled_session_does_not_start_worker](../tests/test_edit_history.py); [test_buttons_undo_redo_save_selected_history_and_preserve_prior_copy](../tests/test_edit_draft_gtk.py); [test_real_form_dialog_checkbox_radio_list_and_multiselect](../tests/test_edit_draft_gtk.py); [test_real_move_and_delete_bookmark_dialogs_use_updated_paths](../tests/test_edit_draft_gtk.py); [test_real_area_annotation_dialog_and_delete_keep_other_annotations](../tests/test_edit_draft_gtk.py); [test_failed_operation_and_existing_destination_keep_history_usable](../tests/test_edit_draft_gtk.py); [test_cancel_dialog_and_reopen_parent_close_draft_without_publishing](../tests/test_edit_draft_gtk.py); [test_cancelling_save_and_repeated_clicks_do_not_duplicate_writes](../tests/test_edit_draft_gtk.py); [test_saved_form_and_highlight_render_with_poppler](../tests/test_edit_draft_gtk.py).

Relacionados aos planos dinâmicos/UI: D07, UI09, UI10.

<a id="annotations"></a>

## Anotações/undo/gravação

Atual (0.1.16): notas (Text), retângulo (Square), marcações de área (Highlight, Underline, StrikeOut, Squiggly), Ink, Circle, Line, Polygon, PolyLine, Caret, FreeText e Stamp com aparência própria (Unicode, fontes incorporadas), mover anotações simples, comentários com respostas e popup, edição de autor/comentário e exclusão de conversa limitada; rascunho com desfazer/refazer e original preservado. Redação, edição universal de qualquer anotação e disponibilidade exata no Reader continuam abertas.

**Entradas**

- PDF local não criptografado, sem assinatura/Perms/XFA/Collection, fonte identificada por SHA-256.
- Operação selecionada, página base zero para marcador/nota ou nome do campo Tx e texto; destino novo com pasta existente.
- Operação adicional de formulário/árvore/anotação descrita em docs/EDICAO-COM-HISTORICO.md; histórico de até100 passos.
- Anotações adicionais: geometria antes da rotação dentro do CropBox, área/linha mínima0,25 ponto; comentário até64KiB e autor até4KiB. Contrato em docs/ANOTACOES-AMPLIADAS.md.

**Saídas**

- Cópia PDF nova e exclusiva, fonte identificada por hash e preservada; rascunho validado após cada operação.
- UI de histórico com desfazer/refazer no rascunho; cópias já salvas preservadas. GTK/Linux exercitado na0.1.13;400/400 por ambiente fonte/payload/sandbox, sem observação original.
- Novas anotações com Form XObject de aparência indireto; update-annotation preserva aparência/geometria e altera apenas Contents/T. GTK/Linux da nova fonte validado;400/400 por ambiente, sem paridade original.

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

- **S12-14-1** (nominal, contrato próprio atual, `passed`): dado Fixture com nota contendo assunto e conteúdo distintos. Ação: Inspecionar o painel. Esperado: Assunto separado, comentário alvo e autor permanecem campos distintos na página conhecida. Execução própria em 2026-10-20T15:18:10-03:00, revisão `ba38ca70e875`, fronteira worker panels: [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e10.json).
- **S12-14-2** (exception, contrato próprio atual, `passed`): dado Objeto de anotação isolado inválido. Ação: Ler os demais comentários. Esperado: A falha de um objeto não deve ser reportada como criação/edição bem-sucedida de anotação. Execução própria em 2026-10-20T15:18:10-03:00, revisão `ba38ca70e875`, fronteira worker panels: [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e10.json).

**Lacunas da referência Foxit**

- Replies, aparências, edição, autoria, undo/redo, salvamento e disponibilidade Reader.

Fontes: [app/pdf_panels.py](../app/pdf_panels.py), [app/search_engine.py](../app/search_engine.py), [app/pdf_changes.py](../app/pdf_changes.py), [app/edit_tasks.py](../app/edit_tasks.py), [app/worker_cli.py](../app/worker_cli.py), [app/main.py](../app/main.py), [docs/SEGURANCA-ACESSIBILIDADE.md](../docs/SEGURANCA-ACESSIBILIDADE.md), [app/local_files.py](../app/local_files.py), [app/folder_dialogs.py](../app/folder_dialogs.py), [docs/PASTAS-SINCRONIZADAS.md](../docs/PASTAS-SINCRONIZADAS.md), [app/pdf_form_controls.py](../app/pdf_form_controls.py), [app/edit_history.py](../app/edit_history.py), [app/edit_dialogs.py](../app/edit_dialogs.py), [app/edit_window.py](../app/edit_window.py), [docs/EDICAO-COM-HISTORICO.md](../docs/EDICAO-COM-HISTORICO.md), [testes/resultados/0.1.10/validation-review.json](../testes/resultados/0.1.10/validation-review.json), [app/pdf_annotations.py](../app/pdf_annotations.py), [docs/ANOTACOES-AMPLIADAS.md](../docs/ANOTACOES-AMPLIADAS.md), [testes/resultados/annotation-extensions-portable-2026-10-18-round3.json](../testes/resultados/annotation-extensions-portable-2026-10-18-round3.json), [testes/resultados/0.1.13/validation-review.json](../testes/resultados/0.1.13/validation-review.json), [app/annotation_geometry.py](../app/annotation_geometry.py), [app/text_appearance.py](../app/text_appearance.py), [app/pdf_edit_security.py](../app/pdf_edit_security.py), [testes/resultados/0.1.16/validation-review.json](../testes/resultados/0.1.16/validation-review.json), [docs/FOXIT-REA.md](../docs/FOXIT-REA.md).

Testes próprios existentes, sem nova execução nesta tabela: [test_comment_subject_contents_and_author_are_searchable](../tests/test_search_scopes.py); [test_combined_copy_preserves_source_metadata_attachment_and_previous_objects](../tests/test_pdf_changes.py); [test_encryption_signature_permissions_xfa_and_portfolio_are_explicitly_unsupported](../tests/test_pdf_changes.py); [test_real_dialogs_and_worker_create_bookmark_note_and_form_copies](../tests/test_copy_edit_gtk.py); [test_reopening_same_document_during_dialog_blocks_stale_save](../tests/test_copy_edit_gtk.py); [test_existing_destination_is_preserved_and_busy_state_is_released](../tests/test_copy_edit_gtk.py); [test_combined_edits_preserve_tree_destinations_geometry_and_source](../tests/test_extended_edits.py); [test_final_name_is_absent_while_real_copy_is_in_progress](../tests/test_sync_folders.py); [test_save_copy_uses_worker_preserves_original_and_only_confirms_local_save](../tests/test_sync_folders_gtk.py); [test_info_distinguishes_checkbox_radio_choice_combo_and_multiselect](../tests/test_advanced_edits.py); [test_checkbox_sets_and_clears_value_and_visible_appearance](../tests/test_advanced_edits.py); [test_radio_activates_only_the_selected_widget_and_can_clear](../tests/test_advanced_edits.py); [test_radio_no_toggle_off_is_enforced](../tests/test_advanced_edits.py); [test_single_and_combo_values_indices_and_generated_appearances_roundtrip](../tests/test_advanced_edits.py); [test_multiselect_uses_export_values_and_canonical_indices](../tests/test_advanced_edits.py); [test_choice_selection_can_be_cleared](../tests/test_advanced_edits.py); [test_invalid_values_do_not_publish_partial_batch](../tests/test_advanced_edits.py); [test_read_only_and_unsupported_button_appearance_are_explicit](../tests/test_advanced_edits.py); [test_editable_combo_and_duplicate_exports_are_rejected](../tests/test_advanced_edits.py); [test_inherited_checkbox_flags_and_type_are_respected](../tests/test_advanced_edits.py); [test_checkbox_widget_absent_from_pages_is_unsupported](../tests/test_advanced_edits.py); [test_closed_outline_counts_remain_closed_after_move](../tests/test_advanced_edits.py); [test_move_preserves_subtree_destinations_and_sibling_links](../tests/test_advanced_edits.py); [test_move_child_to_root_and_reorder_same_parent](../tests/test_advanced_edits.py); [test_delete_bookmark_removes_subtree_and_last_root](../tests/test_advanced_edits.py); [test_move_into_descendant_invalid_positions_and_boolean_paths_are_refused](../tests/test_advanced_edits.py); [test_highlight_and_rectangle_roundtrip_geometry_print_flags_and_text](../tests/test_advanced_edits.py); [test_delete_supported_annotation_preserves_widgets_and_other_pages](../tests/test_advanced_edits.py); [test_locked_notes_widgets_and_replies_are_not_deleted](../tests/test_advanced_edits.py); [test_invalid_annotation_geometry_and_extra_parameters_are_rejected](../tests/test_advanced_edits.py); [test_undo_redo_rebuild_actual_pdfs_and_save_current_cursor_only](../tests/test_edit_history.py); [test_undo_all_restores_base_and_disables_save_until_redone](../tests/test_edit_history.py); [test_new_branch_discards_redo_but_invalid_branch_preserves_it](../tests/test_edit_history.py); [test_operation_values_are_defensively_copied](../tests/test_edit_history.py); [test_changed_original_blocks_add_undo_redo_and_save](../tests/test_edit_history.py); [test_existing_destination_is_not_overwritten_and_draft_survives](../tests/test_edit_history.py); [test_closed_session_refuses_work_and_removes_private_previews](../tests/test_edit_history.py); [test_pre_cancelled_session_does_not_start_worker](../tests/test_edit_history.py); [test_buttons_undo_redo_save_selected_history_and_preserve_prior_copy](../tests/test_edit_draft_gtk.py); [test_real_form_dialog_checkbox_radio_list_and_multiselect](../tests/test_edit_draft_gtk.py); [test_real_move_and_delete_bookmark_dialogs_use_updated_paths](../tests/test_edit_draft_gtk.py); [test_real_area_annotation_dialog_and_delete_keep_other_annotations](../tests/test_edit_draft_gtk.py); [test_failed_operation_and_existing_destination_keep_history_usable](../tests/test_edit_draft_gtk.py); [test_cancel_dialog_and_reopen_parent_close_draft_without_publishing](../tests/test_edit_draft_gtk.py); [test_cancelling_save_and_repeated_clicks_do_not_duplicate_writes](../tests/test_edit_draft_gtk.py); [test_saved_form_and_highlight_render_with_poppler](../tests/test_edit_draft_gtk.py); [test_all_five_types_roundtrip_with_printable_embedded_appearance](../tests/test_annotation_extensions.py); [test_text_markup_quad_order_and_line_and_ellipse_metadata_are_distinct](../tests/test_annotation_extensions.py); [test_offsets_and_page_rotations_do_not_double_transform_geometry](../tests/test_annotation_extensions.py); [test_horizontal_vertical_and_reversed_lines_keep_endpoint_direction](../tests/test_annotation_extensions.py); [test_boundary_strokes_have_positive_clipped_boxes_and_small_areas_renderable_numbers](../tests/test_annotation_extensions.py); [test_squiggly_geometry_has_bounded_commands_even_on_extreme_page](../tests/test_annotation_extensions.py); [test_invalid_area_and_crop_coordinates_refuse_the_entire_batch](../tests/test_annotation_extensions.py); [test_invalid_line_points_page_and_extra_fields_are_rejected](../tests/test_annotation_extensions.py); [test_utf8_comment_and_author_limits_and_nonstring_values_are_enforced](../tests/test_annotation_extensions.py); [test_edit_and_clear_comment_author_preserve_geometry_appearance_and_other_content](../tests/test_annotation_extensions.py); [test_locked_related_and_unsupported_annotations_cannot_be_changed_or_deleted](../tests/test_annotation_extensions.py); [test_deleting_new_types_uses_current_indices_and_preserves_forms_notes_and_other_page](../tests/test_annotation_extensions.py); [test_real_worker_protocol_lists_new_types_and_author_and_refuses_source_and_destination_changes](../tests/test_annotation_extensions.py); [test_history_undo_redo_comment_delete_and_failed_branch_preserve_saved_copy](../tests/test_annotation_extensions.py); [test_real_dialogs_create_all_five_types_and_history_recreates_deleted_shape](../tests/test_annotation_extensions_gtk.py); [test_comment_dialog_prefills_selected_annotation_accepts_multiline_and_can_clear](../tests/test_annotation_extensions_gtk.py); [test_invalid_line_is_explained_in_dialog_and_cancel_does_not_change_draft](../tests/test_annotation_extensions_gtk.py); [test_saved_five_appearances_have_expected_poppler_pixels_and_unfilled_interiors](../tests/test_annotation_extensions_gtk.py); [test_offset_cropbox_and_rotation_render_line_at_transformed_location](../tests/test_annotation_extensions_gtk.py); [test_edited_nontext_annotation_comment_is_searchable_after_reopening_saved_copy](../tests/test_annotation_extensions_gtk.py).

Relacionados aos planos dinâmicos/UI: D08, D09, D19.

<a id="forms"></a>

## AcroForm/XFA/eventos

Atual (0.1.16): preenchimento em cópia nova de texto, checkbox com aparências existentes, rádio, listas simples/múltiplas e combo, inclusive combo editável com texto livre (0.1.15). Cálculos AFSimple_Calculate SUM/AVG/PRD/MIN/MAX e validação AFRange_Validate por gramática fechada, com dependências até64 níveis e ciclos recusados; nenhum JavaScript é executado. Fonte posterior à 0.1.16: AFNumber_Format e AFNumber_Keystroke (etapa E03) com estilos de separador 0–4, moeda, sinal ou parênteses; o valor fica sem formatação, a aparência mostra o número formatado e a entrada aceita vírgula decimal nos estilos com vírgula. AFDate_FormatEx e AFDate_KeystrokeEx (etapa E04) com dia, mês e ano numéricos e separadores / - . ou espaço; datas inexistentes são recusadas, o valor fica como digitado e a aparência mostra a data formatada. AFSpecial_Format/AFSpecial_Keystroke 0–3 (etapa E05) guardam só os dígitos e mostram a máscara; AFSpecial_KeystrokeEx com máscara livre (9, A, O, X e literais, como CEP 99999-999) aceita o texto com ou sem os literais e guarda o texto mascarado. Leitura XFA (etapa E06): o formulário XFA é detectado (pacote único ou lista de pacotes, híbrido ou só XFA, dinâmico) e os valores do pacote datasets são listados por caminho SOM, como form1[0].nome[0], em diálogo somente leitura; o modelo e os scripts XFA não são interpretados nem executados, DOCTYPE/entidades são recusados e há limites de 8 MiB, profundidade 64, 5000 valores e 4096 caracteres por valor. Preenchimento XFA híbrido (etapa E07): em PDF com campos AcroForm e XFA, os preenchimentos de texto e eventos são aceitos e todo valor de texto que mudou (digitado ou calculado) é copiado para o elemento correspondente do pacote datasets, achado pelo nome do campo sem os subformulários sem nome (#subform); o resto do XML fica byte a byte, a cópia é reaberta e conferida, e um campo sem dado correspondente, outras alterações, formulários só XFA, texto rico e ligações explícitas (dataRef/global) são recusados. Renderização XFA dinâmica, JavaScript geral, negativos em vermelho, datas com nomes de mês ou horas e eventos arbitrários continuam abertos.

**Entradas**

- PDF local não criptografado, sem assinatura/Perms/XFA/Collection, fonte identificada por SHA-256.
- Operação selecionada, página base zero para marcador/nota ou nome do campo Tx e texto; destino novo com pasta existente.
- Operação adicional de formulário/árvore/anotação descrita em docs/EDICAO-COM-HISTORICO.md; histórico de até100 passos.

**Saídas**

- Cópia PDF nova e exclusiva, fonte identificada por hash e preservada; rascunho validado após cada operação.
- UI de histórico com desfazer/refazer no rascunho; cópias já salvas preservadas. GTK/Linux exercitado;333/333 por ambiente fonte/payload/sandbox, sem observação original.

**Erros e casos excepcionais**

- Fonte mudou ou destino já existe, inclusive o próprio original: Recusar a gravação; não sobrescrever arquivos.
- PDF criptografado, assinatura/campo Sig, Perms ou Collection; formulário só XFA; em XFA híbrido, alteração que não seja preenchimento de campo ligado aos dados: Recurso não suportado para gravação; não remover proteção ou invalidar assinatura.
- Operação/índice/texto/retângulo inválido; campo ausente, não Tx, ReadOnly ou MaxLen excedido: Falha antes de publicar destino; lote não é aplicado parcialmente à fonte.
- Controle/aparência/opção/árvore/anotação fora do subconjunto ou origem alterada: Recusar a alteração sem avançar o histórico ou publicar uma cópia parcial em falha tratada.

**Estado e efeitos**

- Fonte clonada em memória; gravação temporária privada, reabertura e rechecagem de identidade antes da criação exclusiva do destino.
- Falhas tratadas removem arquivo novo criado; término forçado/timeout pode deixar temporário ou saída parcial e exige conferir destino.
- Não executar ações ou scripts PDF. Sem persistência em cima do original e sem garantia de preservação de assinatura; documentos com assinatura são recusados.
- Confirmação capturada por documento/geração; reabrir o mesmo caminho durante diálogo invalida a operação antiga.
- Reconstituir cópia temporária e inspecionar antes de avançar histórico; falha mantém cursor/refazer e original; fechar cancela worker. Gravação interrompida exige conferir destino.

**Critérios planejados**

- **S12-15-1** (nominal, contrato próprio atual, `passed`): dado AcroForm sintético com campo Tx editável, sem XFA ou assinatura. Ação: Preencher o campo Tx e salvar cópia nova. Esperado: Reabrir a cópia confirma o texto; páginas e original são preservados. Widgets de escolha não estão neste subconjunto. Execução própria em 2026-10-20T15:18:10-03:00, revisão `ba38ca70e875`, fronteira worker copy-edit: [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e10.json).
- **S12-15-2** (exception, contrato próprio atual, `passed`): dado AcroForm sintético com campo Tx ReadOnly ou MaxLen excedido. Ação: Tentar alterar o campo e salvar cópia. Esperado: Recusar a operação sem saída nova; preservar o original. Execução própria em 2026-10-20T15:18:11-03:00, revisão `ba38ca70e875`, fronteira worker copy-edit: [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e10.json).
- **S12-15-3** (nominal, contrato próprio atual, `passed`): dado AcroForm sintético com preço e quantidade (AFNumber_Keystroke com vírgula decimal) e total calculado com AFNumber_Format(2, 2, 0, 0, "R$ ", true). Ação: Preencher preço 1234,5 e quantidade 2 com cálculos e salvar cópia nova. Esperado: O total guarda 2469 sem formatação e a aparência mostra R$ 2.469,00; nenhum JavaScript é executado; o original é preservado. Execução própria em 2026-10-20T15:18:11-03:00, revisão `ba38ca70e875`, fronteira worker copy-edit (fill-form-events): [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e10.json).
- **S12-15-4** (nominal, contrato próprio atual, `passed`): dado AcroForm sintético com campo de data (AFDate_KeystrokeEx e AFDate_FormatEx "dd/mm/yyyy"). Ação: Preencher 1/2/2026 com eventos e salvar cópia nova. Esperado: O campo guarda 1/2/2026 como digitado e a aparência mostra 01/02/2026; nenhum JavaScript é executado; original preservado. Execução própria em 2026-10-20T15:18:11-03:00, revisão `ba38ca70e875`, fronteira worker copy-edit (fill-form-events): [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e10.json).
- **S12-15-5** (exception, contrato próprio atual, `passed`): dado Mesmo formulário de data. Ação: Preencher 31/02/2026 e tentar salvar cópia. Esperado: Recusar a data inexistente sem criar saída; original preservado. Execução própria em 2026-10-20T15:18:11-03:00, revisão `ba38ca70e875`, fronteira worker copy-edit (fill-form-events): [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e10.json).
- **S12-15-6** (nominal, contrato próprio atual, `passed`): dado AcroForm sintético com cep (AFSpecial_KeystrokeEx "99999-999") e telefone (AFSpecial_Keystroke/Format 2). Ação: Preencher cep 01310100 e telefone 5551234567 com eventos e salvar cópia nova. Esperado: cep guarda 01310-100; telefone guarda só os dígitos e aparece como (555) 123-4567; nenhum JavaScript é executado; original preservado. Execução própria em 2026-10-20T15:18:11-03:00, revisão `ba38ca70e875`, fronteira worker copy-edit (fill-form-events): [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e10.json).
- **S12-15-7** (exception, contrato próprio atual, `passed`): dado Mesmo formulário de máscaras. Ação: Preencher cep com letra ou telefone com 8 dígitos e tentar salvar. Esperado: Recusar cada caso sem criar saída; original preservado. Execução própria em 2026-10-20T15:18:12-03:00, revisão `ba38ca70e875`, fronteira worker copy-edit (fill-form-events): [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e10.json).
- **S12-15-8** (nominal, contrato próprio atual, `passed`): dado PDF sintético XFA híbrido: campos AcroForm form1[0].nome[0] e form1[0].extra[0] e pacotes template/datasets com nome, dois itens e obs vazio. Ação: Ler os painéis do documento. Esperado: Listar form1[0].nome[0]=Ana Souza, form1[0].itens[0].item[0]=Caneta, item[1]=Caderno e obs vazio, marcado como híbrido; nenhum script executado; original preservado. Execução própria em 2026-10-20T15:18:12-03:00, revisão `ba38ca70e875`, fronteira worker panels (XFA datasets): [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e10.json).
- **S12-15-9** (nominal, contrato próprio atual, `passed`): dado O mesmo PDF XFA e o formulário AcroForm sem XFA, abertos na janela. Ação: Abrir Campos de formulário XFA… depois de carregados os painéis. Esperado: Diálogo somente leitura com quatro linhas, a primeira form1[0].nome[0] = Ana Souza, resumo híbrido que avisa que scripts não são executados; no PDF sem XFA, aviso de que não há formulário XFA. Execução própria em 2026-10-20T15:18:12-03:00, revisão `ba38ca70e875`, fronteira PDFWindow _xfa_dialog: [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e10.json).
- **S12-15-10** (nominal, contrato próprio atual, `passed`): dado O mesmo PDF XFA híbrido. Ação: Preencher form1[0].nome[0] com "Bia Lima" e salvar cópia nova. Esperado: Na cópia reaberta, o campo AcroForm e o valor form1[0].nome[0] do pacote datasets são "Bia Lima"; os demais dados XFA não mudam; original preservado. Execução própria em 2026-10-20T15:18:10-03:00, revisão `ba38ca70e875`, fronteira worker copy-edit (XFA hybrid fill): [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e10.json).
- **S12-15-11** (exception, contrato próprio atual, `passed`): dado O mesmo PDF XFA híbrido. Ação: Preencher form1[0].extra[0], que não tem dado XFA correspondente, ou adicionar um marcador. Esperado: Recusar cada caso sem criar saída, para não deixar AcroForm e dados XFA divergentes; original preservado. Execução própria em 2026-10-20T15:18:10-03:00, revisão `ba38ca70e875`, fronteira worker copy-edit (XFA hybrid fill): [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e10.json).

**Lacunas da referência Foxit**

- Motor de formulários, eventos, XFA, cálculo/validação e gravação; FRMSPlgV2 é RMS, não prova de formulários.

Fontes: [app/pdf_changes.py](../app/pdf_changes.py), [app/edit_tasks.py](../app/edit_tasks.py), [app/worker_cli.py](../app/worker_cli.py), [app/main.py](../app/main.py), [app/local_files.py](../app/local_files.py), [app/folder_dialogs.py](../app/folder_dialogs.py), [docs/PASTAS-SINCRONIZADAS.md](../docs/PASTAS-SINCRONIZADAS.md), [app/pdf_form_controls.py](../app/pdf_form_controls.py), [app/edit_history.py](../app/edit_history.py), [app/edit_dialogs.py](../app/edit_dialogs.py), [app/edit_window.py](../app/edit_window.py), [docs/EDICAO-COM-HISTORICO.md](../docs/EDICAO-COM-HISTORICO.md), [testes/resultados/0.1.10/validation-review.json](../testes/resultados/0.1.10/validation-review.json), [app/pdf_form_events.py](../app/pdf_form_events.py), [app/pdf_edit_security.py](../app/pdf_edit_security.py), [testes/resultados/0.1.16/validation-review.json](../testes/resultados/0.1.16/validation-review.json), [app/pdf_xfa.py](../app/pdf_xfa.py), [app/pdf_panels.py](../app/pdf_panels.py), [docs/FOXIT-REA.md](../docs/FOXIT-REA.md), [docs/AVANCO-SEM-VM.md](../docs/AVANCO-SEM-VM.md).

Testes próprios existentes, sem nova execução nesta tabela: [test_combined_copy_preserves_source_metadata_attachment_and_previous_objects](../tests/test_pdf_changes.py); [test_encryption_signature_permissions_xfa_and_portfolio_are_explicitly_unsupported](../tests/test_pdf_changes.py); [test_real_dialogs_and_worker_create_bookmark_note_and_form_copies](../tests/test_copy_edit_gtk.py); [test_reopening_same_document_during_dialog_blocks_stale_save](../tests/test_copy_edit_gtk.py); [test_existing_destination_is_preserved_and_busy_state_is_released](../tests/test_copy_edit_gtk.py); [test_nested_field_inherits_read_only_and_max_length](../tests/test_pdf_changes.py); [test_form_max_length_and_value_types_are_enforced](../tests/test_pdf_changes.py); [test_final_name_is_absent_while_real_copy_is_in_progress](../tests/test_sync_folders.py); [test_save_copy_uses_worker_preserves_original_and_only_confirms_local_save](../tests/test_sync_folders_gtk.py); [test_info_distinguishes_checkbox_radio_choice_combo_and_multiselect](../tests/test_advanced_edits.py); [test_checkbox_sets_and_clears_value_and_visible_appearance](../tests/test_advanced_edits.py); [test_radio_activates_only_the_selected_widget_and_can_clear](../tests/test_advanced_edits.py); [test_radio_no_toggle_off_is_enforced](../tests/test_advanced_edits.py); [test_single_and_combo_values_indices_and_generated_appearances_roundtrip](../tests/test_advanced_edits.py); [test_multiselect_uses_export_values_and_canonical_indices](../tests/test_advanced_edits.py); [test_choice_selection_can_be_cleared](../tests/test_advanced_edits.py); [test_invalid_values_do_not_publish_partial_batch](../tests/test_advanced_edits.py); [test_read_only_and_unsupported_button_appearance_are_explicit](../tests/test_advanced_edits.py); [test_editable_combo_and_duplicate_exports_are_rejected](../tests/test_advanced_edits.py); [test_inherited_checkbox_flags_and_type_are_respected](../tests/test_advanced_edits.py); [test_checkbox_widget_absent_from_pages_is_unsupported](../tests/test_advanced_edits.py); [test_closed_outline_counts_remain_closed_after_move](../tests/test_advanced_edits.py); [test_move_preserves_subtree_destinations_and_sibling_links](../tests/test_advanced_edits.py); [test_move_child_to_root_and_reorder_same_parent](../tests/test_advanced_edits.py); [test_delete_bookmark_removes_subtree_and_last_root](../tests/test_advanced_edits.py); [test_move_into_descendant_invalid_positions_and_boolean_paths_are_refused](../tests/test_advanced_edits.py); [test_highlight_and_rectangle_roundtrip_geometry_print_flags_and_text](../tests/test_advanced_edits.py); [test_delete_supported_annotation_preserves_widgets_and_other_pages](../tests/test_advanced_edits.py); [test_locked_notes_widgets_and_replies_are_not_deleted](../tests/test_advanced_edits.py); [test_invalid_annotation_geometry_and_extra_parameters_are_rejected](../tests/test_advanced_edits.py); [test_undo_redo_rebuild_actual_pdfs_and_save_current_cursor_only](../tests/test_edit_history.py); [test_undo_all_restores_base_and_disables_save_until_redone](../tests/test_edit_history.py); [test_new_branch_discards_redo_but_invalid_branch_preserves_it](../tests/test_edit_history.py); [test_operation_values_are_defensively_copied](../tests/test_edit_history.py); [test_changed_original_blocks_add_undo_redo_and_save](../tests/test_edit_history.py); [test_existing_destination_is_not_overwritten_and_draft_survives](../tests/test_edit_history.py); [test_closed_session_refuses_work_and_removes_private_previews](../tests/test_edit_history.py); [test_pre_cancelled_session_does_not_start_worker](../tests/test_edit_history.py); [test_buttons_undo_redo_save_selected_history_and_preserve_prior_copy](../tests/test_edit_draft_gtk.py); [test_real_form_dialog_checkbox_radio_list_and_multiselect](../tests/test_edit_draft_gtk.py); [test_real_move_and_delete_bookmark_dialogs_use_updated_paths](../tests/test_edit_draft_gtk.py); [test_real_area_annotation_dialog_and_delete_keep_other_annotations](../tests/test_edit_draft_gtk.py); [test_failed_operation_and_existing_destination_keep_history_usable](../tests/test_edit_draft_gtk.py); [test_cancel_dialog_and_reopen_parent_close_draft_without_publishing](../tests/test_edit_draft_gtk.py); [test_cancelling_save_and_repeated_clicks_do_not_duplicate_writes](../tests/test_edit_draft_gtk.py); [test_saved_form_and_highlight_render_with_poppler](../tests/test_edit_draft_gtk.py); [test_paths_follow_som_indices_and_skip_groups](../tests/test_pdf_xfa.py); [test_doctype_entities_malformed_and_depth_are_refused](../tests/test_pdf_xfa.py); [test_field_count_value_length_and_size_are_bounded](../tests/test_pdf_xfa.py); [test_hybrid_packet_array_is_listed_without_changing_the_file](../tests/test_pdf_xfa.py); [test_elements_split_across_packets_use_the_joined_document](../tests/test_pdf_xfa.py); [test_text_fill_updates_acroform_and_datasets_and_preserves_the_rest](../tests/test_pdf_xfa.py); [test_calculated_values_are_mirrored_too](../tests/test_pdf_xfa.py); [test_unbound_field_other_operations_and_xfa_only_are_refused_without_output](../tests/test_pdf_xfa.py); [test_only_bound_fields_are_offered_and_value_reaches_the_operation](../tests/test_xfa_gtk.py).

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

- **S12-16-1** (nominal, contrato próprio atual, `passed`): dado anexos-simples.pdf e uma pasta existente nova e vazia. Ação: Listar, usar o índice e SHA-256 devolvidos e extrair nota-sintetica.txt. Esperado: Bytes, tamanho e hash coincidem com anexos-simples.json; nada é executado. Execução própria em 2026-10-20T15:18:15-03:00, revisão `ba38ca70e875`, fronteira worker attachments/extract-attachment: [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e10.json).
- **S12-16-2** (exception, contrato próprio atual, `passed`): dado Nome de anexo ../fora.txt. Ação: Extrair. Esperado: A listagem marca o nome como não permitido e a extração falha sem criar arquivo fora ou dentro da pasta. Execução própria em 2026-10-20T15:18:15-03:00, revisão `ba38ca70e875`, fronteira worker attachments/extract-attachment: [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e10.json).

**Lacunas da referência Foxit**

- D16 synthetic listing/extraction22bytes/hash observed; full policies and availability remain open.
- Portfolios and nonempty-password attachment workflow remain unsupported; desktop/accessibility pending.

**Observação parcial preservada do original:** Anexo sintético listado/extraído,22bytes/hash iguais; políticas/portfólios completos abertos.

Evidências: [docs/VM-FOXIT-2026-10-18.md](../docs/VM-FOXIT-2026-10-18.md).

Fontes: [app/pdf_attachments.py](../app/pdf_attachments.py), [app/worker_cli.py](../app/worker_cli.py), [app/attachment_tasks.py](../app/attachment_tasks.py), [app/main.py](../app/main.py), [testes/resultados/0.1.16/validation-review.json](../testes/resultados/0.1.16/validation-review.json), [docs/FOXIT-REA.md](../docs/FOXIT-REA.md), [docs/VM-FOXIT-2026-10-18.md](../docs/VM-FOXIT-2026-10-18.md).

Testes próprios existentes, sem nova execução nesta tabela: [test_listing_keeps_duplicate_entries_and_does_not_decode_payloads](../tests/test_pdf_attachments.py); [test_extract_preserves_binary_content_hash_and_original](../tests/test_pdf_attachments.py); [test_unsafe_pdf_names_are_reported_and_refused_without_writes](../tests/test_pdf_attachments.py); [test_worker_protocol_lists_extracts_and_reports_conflict](../tests/test_pdf_attachments.py); [test_stale_listing_callback_cannot_replace_a_new_document](../tests/test_attachment_tasks.py); [test_real_worker_extracts_selected_attachment_and_restores_buttons](../tests/test_attachment_tasks.py); [test_refresh_invalidates_the_selection_captured_before_a_dialog](../tests/test_attachment_tasks.py); [test_panel_saves_selected_file_and_shows_conflict_without_overwrite](../tests/test_attachment_panel_gtk.py); [test_sidebar_buttons_switch_hide_and_restore_without_recursive_callbacks](../tests/test_attachment_panel_gtk.py); [test_long_attachment_name_keeps_header_and_save_button_inside_panel](../tests/test_sidebar_layout_gtk.py); [test_nested_tree_preserves_duplicate_name_indices_and_bytes](../tests/test_attachment_trees.py).

Relacionados aos planos dinâmicos/UI: D16.

<a id="signatures"></a>

## Assinaturas/certificados

Atual (0.1.16): inspeção offline da integridade CMS destacada; assinatura CMS/SHA256 invisível em cópia nova com PEM escolhido, verificada antes de publicar; política explícita offline com CA PEM, CRL PEM/DER e horário com fuso, e verificação de carimbos RFC3161 já presentes contra os bytes da assinatura. A assinatura criada não inclui carimbo. Assinaturas múltiplas (etapa E08): toda assinatura nova é uma revisão incremental anexada aos bytes exatos da origem (objetos novos, AcroForm atualizado e seção de referência cruzada do mesmo tipo da anterior, tabela ou fluxo); cada assinatura anterior continua cobrindo a própria revisão e é reverificada antes de publicar. Recusas: assinatura existente que não verifica, certificação DocMDP P=1, direitos de uso UR3, PDF criptografado, XFA e portfólio; limite de 15 assinaturas. Carimbo de documento (etapa E09): campos /ETSI.RFC3161 (DocTimeStamp) são reconhecidos; a integridade confere a assinatura do token e o resumo (messageImprint SHA-256/384/512) contra os bytes cobertos, e o horário só aparece se verificar; com política offline, a TSA precisa encadear até a CA escolhida (openssl ts -verify, sem âncoras do sistema). Assinar depois de um carimbo mantém os dois válidos. DSS (etapa E10): certificados e CRLs do dicionário /DSS do PDF (até 64 certificados e 32 CRLs de até 1 MiB) entram na validação offline: certificados só ajudam a montar o caminho até a CA escolhida, nunca viram âncora; CRLs servem para a revogação; respostas OCSP e entradas VRI são contadas, não usadas; DSS inválido é informado e ignorado. Criar carimbos de documento, gravar DSS (LTV), OCSP e validação legal continuam abertos.

**Entradas**

- PDF não criptografado até 64 MiB; até 16 campos Sig; CMS DER até 2 MiB; quatro intervalos ByteRange válidos.

**Saídas**

- Status de integridade, cobertura da revisão/arquivo atual e trust_chain_verified=false; sem modificação do PDF ou rede.

**Erros e casos excepcionais**

- Entrada não suportada, falha de autenticação/integridade ou cancelamento: ByteRange/Contents/DER malformado, filtro não suportado ou verificador ausente: status explícito sem aprovação.
- Nova assinatura em PDF já assinado com DocMDP P=1, UR3 ou assinatura existente inválida: Recusar sem criar saída; a revisão assinada nunca é reescrita.

**Estado e efeitos**

- Falha de CMS pode ser adulteração ou algoritmo não suportado; nunca atesta confiança/caráter jurídico.
- Fonte preservada; workers limitados e temporários privados. Limpeza sem garantia de apagamento seguro.

**Critérios planejados**

- **S12-17-1** (nominal, contrato próprio atual, `passed`): dado PDF não criptografado até 64 MiB; até 16 campos Sig; CMS DER até 2 MiB; quatro intervalos ByteRange válidos. Ação: Executar o subconjunto local descrito. Esperado: Status de integridade, cobertura da revisão/arquivo atual e trust_chain_verified=false; sem modificação do PDF ou rede. Execução própria em 2026-10-20T15:18:15-03:00, revisão `ba38ca70e875`, fronteira worker sign-copy/signature-info: [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e10.json).
- **S12-17-2** (exception, contrato próprio atual, `passed`): dado Entrada inválida ou recurso explicitamente não suportado. Ação: Solicitar a operação local. Esperado: ByteRange/Contents/DER malformado, filtro não suportado ou verificador ausente: status explícito sem aprovação. Execução própria em 2026-10-20T15:18:16-03:00, revisão `ba38ca70e875`, fronteira worker signature-info: [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e10.json).
- **S12-17-3** (nominal, contrato próprio atual, `passed`): dado Cópia já assinada (S12-17-1) e a mesma identidade PEM sintética. Ação: Assinar de novo, gerando outra cópia. Esperado: A nova cópia começa com os bytes exatos da assinada; a primeira assinatura continua verificada para a própria revisão (não cobre o arquivo todo) e a segunda cobre o arquivo inteiro. Execução própria em 2026-10-20T15:18:17-03:00, revisão `ba38ca70e875`, fronteira worker sign-copy/signature-info (incremental): [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e10.json).
- **S12-17-4** (exception, contrato próprio atual, `passed`): dado PDF sintético com certificação DocMDP P=1 (nenhuma alteração permitida). Ação: Tentar assinar. Esperado: Recusar citando DocMDP P=1, sem criar saída; original preservado. Execução própria em 2026-10-20T15:18:19-03:00, revisão `ba38ca70e875`, fronteira worker sign-copy (incremental): [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e10.json).
- **S12-17-5** (nominal, contrato próprio atual, `passed`): dado PDF sintético com carimbo de documento RFC 3161 de uma TSA sintética local. Ação: Inspecionar as assinaturas sem política e com política offline (CA da TSA e outra CA). Esperado: O campo aparece como carimbo de documento, integridade verificada, cobrindo o arquivo e com horário; confiável só com a CA da TSA; nenhuma rede. Execução própria em 2026-10-20T15:18:19-03:00, revisão `ba38ca70e875`, fronteira worker signature-info (document timestamp): [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e10.json).
- **S12-17-6** (exception, contrato próprio atual, `passed`): dado O mesmo PDF carimbado com um byte coberto alterado. Ação: Inspecionar as assinaturas. Esperado: O carimbo não é aprovado e nenhum horário é informado. Execução própria em 2026-10-20T15:18:20-03:00, revisão `ba38ca70e875`, fronteira worker signature-info (document timestamp): [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e10.json).
- **S12-17-7** (nominal, contrato próprio atual, `passed`): dado PDF assinado por um certificado emitido por uma CA intermediária ausente da assinatura; depois, revisão com DSS contendo o intermediário e as CRLs da cadeia. Ação: Verificar com política offline que escolhe só a CA raiz e exige revogação. Esperado: Sem DSS a cadeia não fecha; com DSS a cadeia e a revogação são verificadas offline, e o resumo do DSS aparece (1 certificado, 2 CRLs); nenhuma rede. Execução própria em 2026-10-20T15:18:21-03:00, revisão `ba38ca70e875`, fronteira worker signature-info (trust policy + DSS): [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e10.json).
- **S12-17-8** (exception, contrato próprio atual, `passed`): dado A mesma cadeia, com a CRL do DSS revogando o certificado do signatário. Ação: Verificar com a mesma política. Esperado: Integridade e cadeia verificadas, revogação não; a política não é satisfeita. Execução própria em 2026-10-20T15:18:23-03:00, revisão `ba38ca70e875`, fronteira worker signature-info (trust policy + DSS): [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e10.json).

**Lacunas da referência Foxit**

- Fluxos Reader, assinatura versus validação, cadeias, políticas e comportamento offline; plugins não provam suporte completo.

Fontes: [app/pdf_signatures.py](../app/pdf_signatures.py), [app/signature_window.py](../app/signature_window.py), [app/search_tasks.py](../app/search_tasks.py), [app/worker_cli.py](../app/worker_cli.py), [app/main.py](../app/main.py), [docs/SEGURANCA-ACESSIBILIDADE.md](../docs/SEGURANCA-ACESSIBILIDADE.md), [app/pdf_signing.py](../app/pdf_signing.py), [app/signature_trust.py](../app/signature_trust.py), [testes/resultados/0.1.16/validation-review.json](../testes/resultados/0.1.16/validation-review.json), [docs/FOXIT-REA.md](../docs/FOXIT-REA.md).

Testes próprios existentes, sem nova execução nesta tabela: [test_real_detached_cms_integrity_is_separate_from_certificate_trust](../tests/test_pdf_signatures.py); [test_modified_signed_bytes_fail_cryptographic_verification](../tests/test_pdf_signatures.py); [test_appended_bytes_report_only_signed_revision_coverage](../tests/test_pdf_signatures.py); [test_unsupported_filter_or_invalid_byte_range_never_report_verified](../tests/test_pdf_signatures.py); [test_der_bounds_and_padding_are_checked](../tests/test_pdf_signatures.py); [test_unsigned_fields_and_count_limit_are_explicit](../tests/test_pdf_signatures.py); [test_encrypted_pdf_input_size_and_invalid_request_are_refused](../tests/test_pdf_signatures.py); [test_missing_verifier_and_source_changes_do_not_approve_integrity](../tests/test_pdf_signatures.py); [test_real_worker_roundtrip_and_cancelled_request](../tests/test_pdf_signatures.py); [test_invalid_worker_confirmation_is_rejected](../tests/test_pdf_signatures.py); [test_integrity_ui_reports_verification_without_certificate_trust](../tests/test_signature_gtk.py); [test_unsigned_and_encrypted_inputs_have_distinct_results](../tests/test_signature_gtk.py); [test_three_signatures_each_cover_their_revision](../tests/test_incremental_signatures.py); [test_cross_reference_stream_source_gets_a_stream_update](../tests/test_incremental_signatures.py); [test_certification_without_changes_usage_rights_and_broken_previous_signature_are_refused](../tests/test_incremental_signatures.py); [test_timestamp_is_recognised_verified_and_trusted_only_with_its_ca](../tests/test_document_timestamps.py); [test_changed_covered_bytes_and_wrong_imprint_fail](../tests/test_document_timestamps.py); [test_signature_after_a_timestamp_keeps_both_valid](../tests/test_document_timestamps.py); [test_intermediate_and_crls_from_dss_complete_the_offline_chain](../tests/test_dss_validation.py); [test_revoked_signer_in_dss_crl_and_dss_root_is_not_an_anchor](../tests/test_dss_validation.py); [test_malformed_dss_is_reported_and_ignored](../tests/test_dss_validation.py).

<a id="security"></a>

## Senhas/permissões/RMS

Atual (0.1.16): abrir com senha conhecida em sessão autenticada (0.1.14), inspecionar permissões, criar cópia AES-256 ou sem criptografia com senha de proprietário, e editar/imprimir documento cifrado conforme as permissões, preservando criptografia, senhas e permissões na cópia (RC4-128, AES-128, AES-256-R5 e AES-256 conferidos). Fluxo de pasta preferida/sincronizada com cópias de publicação exclusiva. RMS, outros perfis de cifra e cliente sincronizador real continuam abertos.

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

- **S12-18-1** (nominal, contrato próprio atual, `passed`): dado PDF local sintético até 64 MiB, senha conhecida ou duas senhas novas distintas de 8–64 ASCII imprimíveis. Ação: Executar o subconjunto local descrito. Esperado: Estado de autenticação/role/permissões sem senha no resultado; nova cópia AES-256 R6 verificada ou plaintext somente para owner autenticado. Execução própria em 2026-10-20T15:18:24-03:00, revisão `ba38ca70e875`, fronteira worker protect-copy/security-info/owner-copy: [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e10.json).
- **S12-18-2** (exception, contrato próprio atual, `passed`): dado Entrada inválida ou recurso explicitamente não suportado. Ação: Solicitar a operação local. Esperado: Credencial errada, role usuário para exportação plaintext, documento Sig/Perms/XFA/Collection, destino existente ou fonte alterada: recusa explícita. Execução própria em 2026-10-20T15:18:25-03:00, revisão `ba38ca70e875`, fronteira worker security-info/owner-copy/protect-copy: [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e10.json).

**Lacunas da referência Foxit**

- Entrada de senha, enforcement de permissões, RMS e mensagens do original; o fluxo completo não está implementado.

**Observação parcial preservada do original:** Cancelar/senha errada anteriores e correta na abertura independenteD15. Permissões/RMS/fluxo universal não observados.

Evidências: [docs/VM-FOXIT-2026-10-18.md](../docs/VM-FOXIT-2026-10-18.md), [docs/VM-SENHA-E-PARADA-2026-10-18.md](../docs/VM-SENHA-E-PARADA-2026-10-18.md).

Fontes: [app/pdf_security.py](../app/pdf_security.py), [app/security_window.py](../app/security_window.py), [app/search_tasks.py](../app/search_tasks.py), [app/worker_cli.py](../app/worker_cli.py), [app/main.py](../app/main.py), [docs/SEGURANCA-ACESSIBILIDADE.md](../docs/SEGURANCA-ACESSIBILIDADE.md), [app/local_files.py](../app/local_files.py), [app/folder_dialogs.py](../app/folder_dialogs.py), [docs/PASTAS-SINCRONIZADAS.md](../docs/PASTAS-SINCRONIZADAS.md), [app/pdf_edit_security.py](../app/pdf_edit_security.py), [testes/resultados/0.1.16/validation-review.json](../testes/resultados/0.1.16/validation-review.json), [docs/FOXIT-REA.md](../docs/FOXIT-REA.md), [docs/AVANCO-SEM-VM.md](../docs/AVANCO-SEM-VM.md), [docs/VM-FOXIT-2026-10-18.md](../docs/VM-FOXIT-2026-10-18.md), [docs/VM-SENHA-E-PARADA-2026-10-18.md](../docs/VM-SENHA-E-PARADA-2026-10-18.md).

Testes próprios existentes, sem nova execução nesta tabela: [test_unencrypted_inspection_identity_pages_and_permissions](../tests/test_pdf_security.py); [test_aes256_roundtrip_roles_permissions_metadata_and_attachments](../tests/test_pdf_security.py); [test_each_permission_flag_and_accessibility_bit_are_preserved](../tests/test_pdf_security.py); [test_encrypted_inspection_correct_wrong_and_missing_credentials](../tests/test_pdf_security.py); [test_new_password_limits_and_distinct_roles](../tests/test_pdf_security.py); [test_invalid_protocol_and_permission_types_rejected](../tests/test_pdf_security.py); [test_encrypted_source_not_unprotected_or_rewritten](../tests/test_pdf_security.py); [test_signed_xfa_portfolio_and_permissions_sources_refused](../tests/test_pdf_security.py); [test_stale_source_and_source_size_page_output_limits](../tests/test_pdf_security.py); [test_existing_destination_and_source_never_overwritten](../tests/test_pdf_security.py); [test_handled_partial_write_removed_and_error_sanitized](../tests/test_pdf_security.py); [test_concurrent_destination_preserved](../tests/test_pdf_security.py); [test_real_worker_secret_transport_and_error_channel](../tests/test_pdf_security.py); [test_cancellation_and_invalid_confirmation_never_report_success](../tests/test_pdf_security.py); [test_accessible_text_validation_limit_and_source_change](../tests/test_pdf_security.py); [test_accessible_text_refuses_encrypted_pdf_even_with_empty_password](../tests/test_pdf_security.py); [test_accessible_text_adapter_rejects_invalid_reply_and_supports_cancel](../tests/test_pdf_security.py); [test_only_owner_authentication_can_create_unprotected_copy](../tests/test_pdf_security.py); [test_owner_copy_stale_destination_and_partial_failure_are_safe](../tests/test_pdf_security.py); [test_owner_copy_refuses_special_restrictions_and_signature_fields](../tests/test_pdf_security.py); [test_inspect_protect_and_secrets_cleared_without_source_change](../tests/test_security_accessibility_gtk.py); [test_encrypted_inspection_wrong_and_owner_credentials](../tests/test_security_accessibility_gtk.py); [test_password_mismatch_and_cancelled_destination_create_nothing](../tests/test_security_accessibility_gtk.py); [test_document_change_during_destination_dialog_discards_request](../tests/test_security_accessibility_gtk.py); [test_cancel_and_destroy_stop_actual_security_process](../tests/test_security_accessibility_gtk.py); [test_owner_copy_is_readable_by_main_reader_and_original_is_preserved](../tests/test_security_accessibility_gtk.py); [test_owner_copy_rejects_opening_password_and_clears_it](../tests/test_security_accessibility_gtk.py); [test_final_name_is_absent_while_real_copy_is_in_progress](../tests/test_sync_folders.py); [test_save_copy_uses_worker_preserves_original_and_only_confirms_local_save](../tests/test_sync_folders_gtk.py).

Relacionados aos planos dinâmicos/UI: D15.

<a id="accessibility"></a>

## Acessibilidade/voz

Atual (0.1.16): texto da página em Gtk.TextView/ATK.Text com sessão autenticada, nomes acessíveis, navegação F6/Shift+F6/Ctrl+Shift+T e probe AT-SPI entre processos. Voz local eSpeak PT/EN gera WAV privado e reprodução GStreamer controlada (reproduzir/pausar/parar/volume). Ordem semântica garantida, leitor de tela real, áudio físico e conformidade integral continuam abertos.

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

- **S12-19-1** (nominal, contrato próprio atual, `passed`): dado PDF não criptografado, página válida e ação do usuário; texto até 1 MiB UTF-8. Ação: Executar o subconjunto local descrito. Esperado: Texto selecionável e acessível da página, status/cancelamento e descarte de resposta obsoleta. Execução própria em 2026-10-20T15:18:26-03:00, revisão `ba38ca70e875`, fronteira worker accessible-text: [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e10.json).
- **S12-19-2** (exception, contrato próprio atual, `passed`): dado Entrada inválida ou recurso explicitamente não suportado. Ação: Solicitar a operação local. Esperado: PDF cifrado, limite de texto excedido ou Poppler indisponível: erro explícito sem texto parcial apresentado como completo. Execução própria em 2026-10-20T15:18:26-03:00, revisão `ba38ca70e875`, fronteira worker accessible-text: [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e10.json).

**Lacunas da referência Foxit**

- APIs, árvore acessível, ordem, voz, foco, atalhos e cobertura real do Reader.

Fontes: [app/accessible_reader.py](../app/accessible_reader.py), [app/pdf_security.py](../app/pdf_security.py), [app/search_tasks.py](../app/search_tasks.py), [app/worker_cli.py](../app/worker_cli.py), [app/main.py](../app/main.py), [docs/SEGURANCA-ACESSIBILIDADE.md](../docs/SEGURANCA-ACESSIBILIDADE.md), [app/speech.py](../app/speech.py), [app/local_playback.py](../app/local_playback.py), [app/media_window.py](../app/media_window.py), [testes/resultados/0.1.16/validation-review.json](../testes/resultados/0.1.16/validation-review.json), [docs/FOXIT-REA.md](../docs/FOXIT-REA.md).

Testes próprios existentes, sem nova execução nesta tabela: [test_unencrypted_inspection_identity_pages_and_permissions](../tests/test_pdf_security.py); [test_aes256_roundtrip_roles_permissions_metadata_and_attachments](../tests/test_pdf_security.py); [test_each_permission_flag_and_accessibility_bit_are_preserved](../tests/test_pdf_security.py); [test_encrypted_inspection_correct_wrong_and_missing_credentials](../tests/test_pdf_security.py); [test_new_password_limits_and_distinct_roles](../tests/test_pdf_security.py); [test_invalid_protocol_and_permission_types_rejected](../tests/test_pdf_security.py); [test_encrypted_source_not_unprotected_or_rewritten](../tests/test_pdf_security.py); [test_signed_xfa_portfolio_and_permissions_sources_refused](../tests/test_pdf_security.py); [test_stale_source_and_source_size_page_output_limits](../tests/test_pdf_security.py); [test_existing_destination_and_source_never_overwritten](../tests/test_pdf_security.py); [test_handled_partial_write_removed_and_error_sanitized](../tests/test_pdf_security.py); [test_concurrent_destination_preserved](../tests/test_pdf_security.py); [test_real_worker_secret_transport_and_error_channel](../tests/test_pdf_security.py); [test_cancellation_and_invalid_confirmation_never_report_success](../tests/test_pdf_security.py); [test_accessible_text_validation_limit_and_source_change](../tests/test_pdf_security.py); [test_accessible_text_refuses_encrypted_pdf_even_with_empty_password](../tests/test_pdf_security.py); [test_accessible_text_adapter_rejects_invalid_reply_and_supports_cancel](../tests/test_pdf_security.py); [test_only_owner_authentication_can_create_unprotected_copy](../tests/test_pdf_security.py); [test_owner_copy_stale_destination_and_partial_failure_are_safe](../tests/test_pdf_security.py); [test_owner_copy_refuses_special_restrictions_and_signature_fields](../tests/test_pdf_security.py); [test_real_poppler_text_is_exposed_through_atk_text_interface](../tests/test_security_accessibility_gtk.py); [test_no_text_and_encrypted_pages_have_explicit_limits](../tests/test_security_accessibility_gtk.py); [test_obsolete_page_text_does_not_replace_newer_page](../tests/test_security_accessibility_gtk.py); [test_f6_focus_regions_names_and_list_arrow_delegation](../tests/test_security_accessibility_gtk.py); [test_text_limit_and_document_close_clear_the_accessible_window](../tests/test_security_accessibility_gtk.py); [test_closing_text_worker_terminates_its_real_descendant_on_linux](../tests/test_security_accessibility_gtk.py).

Relacionados aos planos dinâmicos/UI: UI10.

<a id="measurement"></a>

## Medição/calibração

Atual (0.1.16): janela de medidas sobre a página com calibração por comprimento conhecido, distância, perímetro e área em mm/cm/m/in/ft, grade em pontos PDF e restrição angular de 45 graus. Fonte posterior à 0.1.16 (etapa E25, decisão D01): régua, janela de medidas e tamanho da página exibem vírgula decimal (ex.: 2,54 cm). Encaixe automático em caminhos vetoriais, precisão comparada ao original e paridade completa continuam abertos.

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

- **S12-20-1** (nominal, contrato próprio atual, `passed`): dado Imagem e página com escala conhecida; pontos separados por 72 pontos PDF. Ação: Medir o segmento horizontal. Esperado: Contrato próprio: 2,54 cm, formatado com duas casas decimais. Execução própria em 2026-10-20T15:18:26-03:00, revisão `ba38ca70e875`, fronteira PDFWindow _finish_measure: [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e10.json).
- **S12-20-2** (exception, contrato próprio atual, `passed`): dado Página sem pixbuf/tamanhos disponíveis. Ação: Concluir gesto de medida. Esperado: Nenhuma nova medida válida é publicada. Execução própria em 2026-10-20T15:18:28-03:00, revisão `ba38ca70e875`, fronteira PDFWindow _finish_measure: [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e10.json).

**Lacunas da referência Foxit**

- Unidades, calibração, snapping, precisão, áreas e perímetros do original.

Fontes: [app/main.py](../app/main.py), [app/measurement.py](../app/measurement.py), [app/measurement_window.py](../app/measurement_window.py), [testes/resultados/0.1.16/validation-review.json](../testes/resultados/0.1.16/validation-review.json), [docs/FOXIT-REA.md](../docs/FOXIT-REA.md).

<a id="layers-media"></a>

## Camadas/mídia/3D

Atual (0.1.16): listar OCGs, alternar visibilidade temporária (default ON/OFF, locks e grupos exclusivos) e salvar a visibilidade em cópia nova com criptografia preservada. Movie/RichMedia com arquivos incorporados, Sound PCM8/16 (convertido para WAV) e 3D podem ser listados/extraídos; áudio/vídeo locais têm reprodução explícita; desde a etapa E26 a reprodução só começa depois do pré-carregamento, evitando que um arquivo curto termine de imediato. Renderizador U3D/PRC, eventos de mídia e todas as configurações opcionais continuam abertos.

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

- **S12-21-1** (nominal, contrato próprio atual, `passed`): dado PDF sintético com OCGs nomeados, fixture a criar. Ação: Inspecionar painel. Esperado: Lista os nomes lidos, sem anunciar reprodução de mídia ou alteração de camada. Execução própria em 2026-10-20T15:18:28-03:00, revisão `ba38ca70e875`, fronteira worker panels: [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e10.json).
- **S12-21-2** (exception, contrato próprio atual, `passed`): dado PDF sem OCProperties. Ação: Inspecionar painel. Esperado: layers=[]; não criar uma camada fictícia. Execução própria em 2026-10-20T15:18:28-03:00, revisão `ba38ca70e875`, fronteira worker panels: [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e10.json).

**Lacunas da referência Foxit**

- Combinações OCG, visibilidade, persistência, codecs, eventos e suporte U3D/Reader.

Fontes: [app/pdf_panels.py](../app/pdf_panels.py), [app/pdf_layers.py](../app/pdf_layers.py), [app/local_playback.py](../app/local_playback.py), [app/media_window.py](../app/media_window.py), [app/pdf_media.py](../app/pdf_media.py), [app/media_assets_window.py](../app/media_assets_window.py), [testes/resultados/0.1.16/validation-review.json](../testes/resultados/0.1.16/validation-review.json), [docs/FOXIT-REA.md](../docs/FOXIT-REA.md).

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

- **S12-22-1** (nominal, contrato próprio atual, `passed`): dado Configuração com modo dark e uma chave desconhecida. Ação: Salvar modo light e reabrir a preferência. Esperado: Modo light preservado e chave desconhecida conservada. Execução própria em 2026-10-20T15:18:29-03:00, revisão `ba38ca70e875`, fronteira appearance.save_mode/read_mode: [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e10.json).
- **S12-22-2** (exception, contrato próprio atual, `passed`): dado Modo inventado ao salvar. Ação: Chamar save_mode. Esperado: ValueError, sem tratar o modo como suportado. Execução própria em 2026-10-20T15:18:29-03:00, revisão `ba38ca70e875`, fronteira appearance.save_mode: [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e10.json).

**Lacunas da referência Foxit**

- Defaults, esquemas de persistência e dependências de todas as preferências do original.

Fontes: [app/appearance.py](../app/appearance.py), [app/local_files.py](../app/local_files.py), [app/folder_dialogs.py](../app/folder_dialogs.py), [docs/PASTAS-SINCRONIZADAS.md](../docs/PASTAS-SINCRONIZADAS.md), [app/reading_preferences.py](../app/reading_preferences.py), [app/tool_preferences.py](../app/tool_preferences.py), [testes/resultados/0.1.16/validation-review.json](../testes/resultados/0.1.16/validation-review.json), [docs/FOXIT-REA.md](../docs/FOXIT-REA.md).

Testes próprios existentes, sem nova execução nesta tabela: [test_theme_persistence_and_contrast](../tests/test_viewer.py); [test_fresh_system_theme_initializes_and_migrates_legacy](../tests/test_consolidation.py); [test_final_name_is_absent_while_real_copy_is_in_progress](../tests/test_sync_folders.py); [test_save_copy_uses_worker_preserves_original_and_only_confirms_local_save](../tests/test_sync_folders_gtk.py).

<a id="cloud"></a>

## Nuvem/colaboração

Atual (E28): a nuvem é atendida pelo fluxo de pasta sincronizada escolhido pelo usuário em 17/10/2026 às 20:51 e confirmado como fechamento do ciclo em 20/10/2026 às 12:38. Um cliente externo (OneDrive, Dropbox, Nextcloud, Syncthing ou outro) sincroniza uma pasta local; o Linuxit guarda essa pasta como preferida, abre os PDFs dela pelos seletores do sistema, salva cópias exclusivas e completas (sem sobrescrever e sem publicar arquivo parcial) e informa só "salva localmente", deixando envio, autenticação e conflitos para o cliente externo. Uma troca externa do PDF aberto bloqueia salvar e editar até reabrir, e um nome que o cliente criou nesse meio-tempo nunca é sobrescrito. Não há conta, senha, token nem transmissão pelo Linuxit. Continuam adiados por decisão do usuário ("Deixar nuvem para depois", 17/10/2026): login em provedor, transferência por API e colaboração remota (operações cloud/login, cloud/transfer e cloud/collaboration). Cliente sincronizador real ainda não foi testado.

**Entradas**

- Pasta local escolhida explicitamente e sincronizada por um cliente externo; o Linuxit não detecta contas nem pastas.
- PDF aberto dessa pasta e nome novo para a cópia, pelo seletor do sistema (FileChooser/portal).

**Saídas**

- Cópia completa e idêntica publicada com o nome final na pasta; o estado diz "salva localmente" e que o envio é do sincronizador.
- Preferência de pasta em $XDG_CONFIG_HOME/linuxit-pdf/folders.json, só com caminhos locais; esquecer a pasta não apaga arquivos.

**Erros e casos excepcionais**

- O cliente externo trocou o PDF aberto: Bloquear salvar e editar até reabrir; nenhuma cópia parte do documento antigo.
- O destino já existe ou surge durante a gravação (por exemplo, vindo de outro computador): Recusar sem sobrescrever e sem falso sucesso; original preservado.
- Pasta preferida ausente, inválida ou sem permissão: Pedir nova escolha ou usar outra pasta; nenhuma rede ou conta é usada.

**Estado e efeitos**

- Grava só arquivos locais e a preferência de pastas; temporários .linuxit-* podem ser vistos pelo sincronizador até a publicação.
- Envio, autenticação, versões e conflitos remotos ficam com o cliente externo; o Linuxit nunca afirma envio remoto.

**Critérios planejados**

- **S12-23-1** (nominal, contrato próprio atual, `passed`): dado Pasta local sincronizada escolhida como preferida, com um PDF sintético dentro (cliente externo representado pela própria pasta; sem cliente real). Ação: Abrir o PDF pela opção da pasta sincronizada e salvar uma cópia com nome novo na mesma pasta. Esperado: O seletor abre na pasta preferida; a cópia aparece completa e idêntica com o nome final, sem temporários; o estado diz "salva localmente" e que o envio é do sincronizador; original preservado; nenhuma conta ou rede. Execução própria em 2026-10-20T15:18:29-03:00, revisão `ba38ca70e875`, fronteira PDFWindow _open_sync_folder/_save_copy + worker copy-file: [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e10.json).
- **S12-23-2** (exception, contrato próprio atual, `passed`): dado O mesmo PDF aberto da pasta sincronizada. Ação: O cliente externo troca o PDF aberto e, depois de reabrir, cria um arquivo com o nome escolhido para a cópia. Esperado: Salvar fica bloqueado até reabrir; depois, o arquivo criado pelo cliente não é sobrescrito; nenhum falso sucesso; arquivos preservados. Execução própria em 2026-10-20T15:18:30-03:00, revisão `ba38ca70e875`, fronteira PDFWindow _save_copy + worker copy-file: [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e10.json).

**Lacunas da referência Foxit**

- Contratos por provedor, serviços disponíveis, autorização, colaboração e conflitos; presença de plugins não valida APIs.

Fontes: [docs/PASTAS-SINCRONIZADAS.md](../docs/PASTAS-SINCRONIZADAS.md), [app/local_files.py](../app/local_files.py), [app/folder_dialogs.py](../app/folder_dialogs.py), [app/main.py](../app/main.py), [app/worker_cli.py](../app/worker_cli.py), [testes/resultados/0.1.16/validation-review.json](../testes/resultados/0.1.16/validation-review.json), [testes/resultados/0.1.16/desktop/review.json](../testes/resultados/0.1.16/desktop/review.json), [docs/FOXIT-REA.md](../docs/FOXIT-REA.md).

Testes próprios existentes, sem nova execução nesta tabela: [test_worker_roundtrip_preserves_source_and_never_claims_remote_sync](../tests/test_sync_folders.py); [test_existing_file_and_destination_race_are_never_overwritten](../tests/test_sync_folders.py); [test_final_name_is_absent_while_real_copy_is_in_progress](../tests/test_sync_folders.py); [test_source_changed_before_or_during_copy_refuses_publication](../tests/test_sync_folders.py); [test_invalid_relative_missing_and_unknown_settings_are_refused](../tests/test_sync_folders.py); [test_save_copy_uses_worker_preserves_original_and_only_confirms_local_save](../tests/test_sync_folders_gtk.py); [test_external_replacement_blocks_save_and_edit_until_reopen](../tests/test_sync_folders_gtk.py); [test_existing_destination_is_preserved_and_failure_is_shown](../tests/test_sync_folders_gtk.py).

<a id="conversion"></a>

## Criação/conversão

Fonte0.1.12: TIFF multipágina em blocos, todas as páginas do IFD principal, até100 páginas totais junto de PNG/JPEG/BMP/WebP simples. RGB8, orientação por página e limites agregados; animações e variantes não decodificáveis recusadas. OCR0.1.11 preservado com limite próprio20 páginas. Fonte/payload/sandbox380/380 passaram, incluindo14 novos portáveis,2 GTK e1 integração real TIFF→PDF→OCR; uma expectativa histórica de recusa TIFF foi adaptada. Família completa e referência Foxit permanecem parciais.

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

- **S12-24-1** (nominal, contrato próprio atual, `passed`): dado PNG/JPEG sintéticos ordenados e DPI suportado. Ação: Converter para PDF em caminho novo. Esperado: Criar novo PDF RGB com orientação, ordem e dimensões declaradas; fontes intactas. Execução própria em 2026-10-20T15:18:32-03:00, revisão `ba38ca70e875`, fronteira worker images-to-pdf: [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e10.json).
- **S12-24-2** (exception, contrato próprio atual, `passed`): dado Arquivo GIF ou PNG/JPEG inválido. Ação: Solicitar conversão. Esperado: Recusar lote sem criar saída concluída e sem substituir arquivo existente. Execução própria em 2026-10-20T15:18:33-03:00, revisão `ba38ca70e875`, fronteira worker images-to-pdf: [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e10.json).

**Lacunas da referência Foxit**

- Inventário real Reader/Editor, fidelidade, formatos, OCR e serviços; não implementado como família completa.

Fontes: [app/pdf_creation.py](../app/pdf_creation.py), [app/creation_window.py](../app/creation_window.py), [app/search_tasks.py](../app/search_tasks.py), [app/worker_cli.py](../app/worker_cli.py), [app/main.py](../app/main.py), [docs/CRIACAO-IMAGENS.md](../docs/CRIACAO-IMAGENS.md), [app/local_files.py](../app/local_files.py), [app/folder_dialogs.py](../app/folder_dialogs.py), [docs/PASTAS-SINCRONIZADAS.md](../docs/PASTAS-SINCRONIZADAS.md), [testes/resultados/0.1.10/validation-review.json](../testes/resultados/0.1.10/validation-review.json), [app/pdf_ocr.py](../app/pdf_ocr.py), [app/ocr_window.py](../app/ocr_window.py), [docs/OCR-LOCAL.md](../docs/OCR-LOCAL.md), [testes/resultados/ocr-portable-2026-10-18-round1.json](../testes/resultados/ocr-portable-2026-10-18-round1.json), [testes/resultados/0.1.11/validation-review.json](../testes/resultados/0.1.11/validation-review.json), [docs/TIFF-MULTIPAGINA.md](../docs/TIFF-MULTIPAGINA.md), [testes/resultados/tiff-multipage-portable-2026-10-18-round2.json](../testes/resultados/tiff-multipage-portable-2026-10-18-round2.json), [testes/resultados/tiff-creation-existing-2026-10-18-round2.json](../testes/resultados/tiff-creation-existing-2026-10-18-round2.json), [testes/resultados/tiff-multipage-portable-2026-10-18-round3.json](../testes/resultados/tiff-multipage-portable-2026-10-18-round3.json), [testes/resultados/0.1.12/validation-review.json](../testes/resultados/0.1.12/validation-review.json), [testes/resultados/0.1.16/validation-review.json](../testes/resultados/0.1.16/validation-review.json), [docs/FOXIT-REA.md](../docs/FOXIT-REA.md).

Testes próprios existentes, sem nova execução nesta tabela: [test_order_dimensions_lossless_rgb_and_source_identity](../tests/test_pdf_creation.py); [test_alpha_and_palette_transparency_are_composited_on_white](../tests/test_pdf_creation.py); [test_exif_orientation_applied_and_private_metadata_not_copied](../tests/test_pdf_creation.py); [test_corrupt_unsupported_animated_and_truncated_inputs_leave_no_output](../tests/test_pdf_creation.py); [test_partial_final_write_removed_on_handled_failure](../tests/test_pdf_creation.py); [test_ordered_creation_opens_actual_pdf_and_poppler_renders_pixels](../tests/test_creation_gtk.py); [test_cancel_and_destroy_kill_real_worker_without_stale_callbacks](../tests/test_creation_gtk.py); [test_pinned_fixture_manifest_matches_sources_and_oriented_dimensions](../tests/test_pdf_creation.py); [test_final_name_is_absent_while_real_copy_is_in_progress](../tests/test_sync_folders.py); [test_save_copy_uses_worker_preserves_original_and_only_confirms_local_save](../tests/test_sync_folders_gtk.py); [test_bmp_webp_and_single_tiff_preserve_pixels_dimensions_and_order](../tests/test_pdf_creation.py); [test_webp_alpha_is_composited_over_white](../tests/test_pdf_creation.py); [test_multiframe_tiff_is_imported_and_animated_webp_is_refused](../tests/test_pdf_creation.py); [test_bmp_renamed_as_jpeg_is_identified_by_content](../tests/test_pdf_creation.py); [test_real_worker_supports_compressed_tiff_without_external_conversion](../tests/test_pdf_creation.py); [test_bmp_webp_tiff_selection_worker_and_opening](../tests/test_creation_gtk.py); [test_raster_copy_pipeline_preserves_order_dimensions_hashes_and_original](../tests/test_pdf_ocr.py); [test_encrypted_input_is_rejected_without_attempting_empty_password](../tests/test_pdf_ocr.py); [test_real_english_worker_adds_searchable_text_and_keeps_scan](../tests/test_ocr_linux.py); [test_cancel_stops_worker_and_its_actual_tesseract_child](../tests/test_ocr_linux.py); [test_menu_workflow_recognizes_opens_and_renders_actual_copy](../tests/test_ocr_gtk.py); [test_file_order_expands_all_tiff_pages_with_dimensions_and_provenance](../tests/test_tiff_multipage.py); [test_each_frame_orientation_is_applied_once_without_leaking_tags](../tests/test_tiff_multipage.py); [test_cyclic_out_of_range_and_truncated_ifd_chains_are_not_silently_shortened](../tests/test_tiff_multipage.py); [test_real_worker_reports_input_count_frame_mapping_and_page_count](../tests/test_tiff_multipage.py); [test_tiff_block_order_expands_pages_and_poppler_renders_each_color](../tests/test_creation_gtk.py); [test_multipage_tiff_import_feeds_searchable_ocr_without_losing_blank_page](../tests/test_ocr_linux.py).

<a id="platform"></a>

## Integrações de sistema/atualização

Atual (0.1.16): abrir PDF pelo seletor do sistema (GtkFileChooserNative, portal quando disponível), que entrega somente o arquivo escolhido; cancelar preserva o documento corrente. No Flatpak, concessão persistente, revogação pelo portal de documentos e associação de arquivos foram verificadas 9/9 em desktop efêmero. A janela de instalação informa versão e comando de atualização do sistema, sem consulta remota nem instalação pelo aplicativo. Desktop físico, impressão do sistema e Windows completo continuam abertos.

**Entradas**

- Ação do usuário no seletor do sistema: portal no Flatpak ou com GTK_USE_PORTAL, diálogo nativo fora dele.
- Arquivo autorizado pelo seletor; nenhum outro caminho da pasta é aberto.

**Saídas**

- Documento escolhido aberto na janela, ou nenhuma mudança quando o seletor é cancelado.
- Informação de versão e do comando de atualização do sistema, sem executar atualização.

**Erros e casos excepcionais**

- Seletor cancelado ou acesso revogado: Não abrir outro arquivo nem usar caminho não autorizado; o documento corrente permanece aberto.
- Seletor sem arquivo local disponível: Mensagem de erro; o documento corrente permanece aberto.
- Pedido de atualização: O aplicativo não baixa nem instala atualizações; indica o gerenciador do sistema.

**Estado e efeitos**

- A escolha aceita registra a última pasta nas preferências do usuário; nenhum outro estado do sistema é alterado.
- Associação de arquivos e permissões persistentes pertencem ao Flatpak e ao portal; o aplicativo não as altera.

**Critérios planejados**

- **S12-25-1** (nominal, contrato próprio atual, `passed`): dado Desktop Linux de teste com xdg-desktop-portal; aplicativo com GTK_USE_PORTAL=1, um documento aberto e outro PDF escolhido no seletor. Ação: Usar Abrir pelo seletor do sistema, escolher o arquivo no portal e confirmar. Esperado: Abrir somente o arquivo escolhido; a chamada e a resposta passam pelo portal; o documento anterior não é alterado e nenhum outro arquivo da pasta é aberto. Execução própria em 2026-10-20T15:18:33-03:00, revisão `ba38ca70e875`, fronteira PDFWindow._choose_open_native via xdg-desktop-portal: [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e10.json).
- **S12-25-2** (exception, contrato próprio atual, `passed`): dado Mesmo desktop de teste com um documento aberto. Ação: Abrir o seletor do sistema e cancelar no portal. Esperado: Nenhum acesso ampliado, erro ou sucesso falso; o documento corrente continua aberto. Execução própria em 2026-10-20T15:19:06-03:00, revisão `ba38ca70e875`, fronteira PDFWindow._choose_open_native via xdg-desktop-portal: [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e10.json).

**Lacunas da referência Foxit**

- Portais em desktop real, integração shell/browser, atualização, rollback e equivalência do adaptador Windows.

Fontes: [docs/instalacao.md](../docs/instalacao.md), [app/folder_dialogs.py](../app/folder_dialogs.py), [app/main.py](../app/main.py), [app/installation_info.py](../app/installation_info.py), [app/platform_runtime.py](../app/platform_runtime.py), [app/cups_backend.py](../app/cups_backend.py), [testes/aceitacao/casos_portal.py](../testes/aceitacao/casos_portal.py), [scripts/check_native_portal.py](../scripts/check_native_portal.py), [scripts/check_desktop_integrations.py](../scripts/check_desktop_integrations.py), [testes/resultados/0.1.16/desktop/review.json](../testes/resultados/0.1.16/desktop/review.json), [docs/FOXIT-REA.md](../docs/FOXIT-REA.md).

A especificação de referência e a consolidação da fase A continuam parciais. Não promover propostas, presença de recursos ou testes próprios a funcionalidade Foxit recuperada.
