# Registro de contratos funcionais — etapa 12

Gerado de `especificacao-funcional.json` por `scripts/validate_functional_spec.py`.

Escopo: **25 famílias identificadas**, **81 cenários planejados**; 25 subconjuntos implementados e 0 propostas futuras. O inventário global permanece aberto.

O campo esperado é do contrato próprio atual ou de uma proposta explicitamente identificada. Execuções próprias registradas: **81**, das quais 81 aprovadas; cada uma aponta o arquivo de resultado e a revisão do código. Expectativas/observações Foxit dos cenários completos S12 permanecem `null`. Observações parciais preservadas por família são registradas separadamente. Referenciar um teste existente não o executa novamente nem comprova paridade. As duas situações de cada família são um início de cobertura, não uma lista exaustiva.

Os campos `fixture_refs` apontam materiais já disponíveis; cenários que pedem outros documentos continuam dependendo da criação/especialização do corpus descrito em sua condição inicial.

Índices internos de página usam base zero; páginas em relatórios de observação usam base um.

A4: **116 operações conhecidas** detalhadas individualmente em [contratos operacionais](contratos-operacoes-v1.json), com entradas, saídas, limites, erros, efeitos, cancelamento e fontes. A cobertura desta lista não fecha o universo Foxit. Âncoras line_at_review/hash são fotografia da revisão; o validador resolve os símbolos atuais por AST.

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

Abertura local transacional com senha, cópia privada de leitura e recuperação consentida de estruturas interpretáveis pelo pypdf. Valida render inicial antes da troca. Falha/cancelamento preserva leitura anterior. Corpus de PDFs danificados (etapa E17, testes/fixtures/danificados/): reparos silenciosos do leitor (xref deslocado, objeto ausente, /Length errado) também pedem consentimento; a recuperação reconstrói o fim perdido do arquivo, deixa em branco conteúdo de página ilegível, omite página inexistente da árvore e informa as categorias de reparo; sem páginas reais, recusa sem cópia de leitura. Original não é sobrescrito; recuperação universal, assinatura da representação e impressão cifrada/recuperada não aprovadas.

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

- **S12-01-1** (nominal, contrato próprio atual, `passed`): dado busca-escopos.pdf legível. Ação: Inspecionar e abrir as duas páginas. Esperado: pages=2; tamanhos positivos; a imagem de cada página pertence ao documento aberto. Execução própria em 2026-10-21T21:24:09-03:00, revisão `ac89254204fb`, fronteira worker info + rendering.render_page: [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e31.json).
- **S12-01-2** (exception, contrato próprio atual, `passed`): dado Arquivo inexistente ou PDF inválido. Ação: Solicitar inspeção/abertura. Esperado: O parser/worker falha; não produzir uma página válida fictícia. Execução própria em 2026-10-21T21:24:09-03:00, revisão `ac89254204fb`, fronteira worker info: [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e31.json).
- **S12-01-3** (nominal, contrato próprio atual, `passed`): dado Corpus próprio testes/fixtures/danificados/: stream-truncado.pdf (cortado no meio do conteúdo da página 2), pagina-ausente.pdf (Kids aponta para objeto inexistente) e xref-deslocado.pdf (tabela xref deslocada). Ação: Abrir cada um sem consentimento e depois com recuperação consentida. Esperado: Sem consentimento: recovery_required. Com consentimento: cópia de leitura com 2, 1 e 2 páginas respectivamente; o Poppler desenha exatamente esse número de páginas; texto preservado onde existe e página com conteúdo perdido em branco; fixtures intactas. Execução própria em 2026-10-21T21:24:10-03:00, revisão `ac89254204fb`, fronteira worker document-open (corpus danificado) + Poppler: [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e31.json).
- **S12-01-4** (exception, contrato próprio atual, `passed`): dado catalogo-sem-paginas.pdf (catálogo aponta para árvore de páginas inexistente) e nao-pdf.pdf (bytes arbitrários). Ação: Abrir com recuperação consentida. Esperado: Recusar os dois sem cópia de leitura e sem página fictícia; fixtures intactas. Execução própria em 2026-10-21T21:24:11-03:00, revisão `ac89254204fb`, fronteira worker document-open (corpus danificado): [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e31.json).

**Lacunas da referência Foxit**

- D15 independent correct password and bounded opening/error/copy variants are observed; remaining recovery/rendering states remain open.
- The own security backend authenticates known passwords, but opening/rendering in the main viewer does not have the complete password flow.

**Observação parcial preservada do original:** Abertura/erros/cópia em recortes; senha correta em abertura independenteD15 abriu8 páginas. Não é contrato completo de recuperação/renderização.

Evidências: [docs/VM-FOXIT-2026-10-18.md](../docs/VM-FOXIT-2026-10-18.md), [docs/VM-SENHA-E-PARADA-2026-10-18.md](../docs/VM-SENHA-E-PARADA-2026-10-18.md).

Fontes: [app/rendering.py](../app/rendering.py), [app/main.py](../app/main.py), [app/async_core.py](../app/async_core.py), [app/local_files.py](../app/local_files.py), [app/folder_dialogs.py](../app/folder_dialogs.py), [docs/PASTAS-SINCRONIZADAS.md](../docs/PASTAS-SINCRONIZADAS.md), [app/document_session.py](../app/document_session.py), [app/navigation.py](../app/navigation.py), [app/page_surface.py](../app/page_surface.py), [docs/LEITURA-ABERTURA-NAVEGACAO-APRESENTACAO.md](../docs/LEITURA-ABERTURA-NAVEGACAO-APRESENTACAO.md), [testes/resultados/0.1.16/validation-review.json](../testes/resultados/0.1.16/validation-review.json), [docs/ETAPA-11.md](../docs/ETAPA-11.md), [docs/windows-evidence/foxit-rea/ui-state-contracts-2026-10-16.json](../docs/windows-evidence/foxit-rea/ui-state-contracts-2026-10-16.json), [docs/REA-ESTATICA-BUSCA-IMPRESSAO-2026-10-18.md](../docs/REA-ESTATICA-BUSCA-IMPRESSAO-2026-10-18.md), [docs/REA-ESTATICA-CONTINUACAO-2026-10-18.md](../docs/REA-ESTATICA-CONTINUACAO-2026-10-18.md), [docs/VM-FOXIT-2026-10-18.md](../docs/VM-FOXIT-2026-10-18.md), [docs/VM-SENHA-E-PARADA-2026-10-18.md](../docs/VM-SENHA-E-PARADA-2026-10-18.md).

Testes próprios existentes, sem nova execução nesta tabela: [test_cache_distinguishes_documents](../tests/test_regressions.py); [test_latest_renderer_skips_obsolete_queue_entries](../tests/test_viewer.py); [test_final_name_is_absent_while_real_copy_is_in_progress](../tests/test_sync_folders.py); [test_save_copy_uses_worker_preserves_original_and_only_confirms_local_save](../tests/test_sync_folders_gtk.py); [test_broken_xref_requires_consent_then_recovers_content](../tests/test_document_session.py); [test_cancellation_before_worker_leaves_no_reading_file](../tests/test_document_session.py); [test_close_waits_for_active_reader_and_removes_private_view](../tests/test_document_session.py); [test_invalid_request_and_existing_view_are_refused](../tests/test_document_session.py); [test_irrecoverable_and_empty_sources_do_not_publish_view](../tests/test_document_session.py); [test_owner_password_can_read_without_rewriting_original_permissions](../tests/test_document_session.py); [test_password_is_absent_from_argv_and_worker_errors](../tests/test_document_session.py); [test_password_required_then_invalid_then_correct_in_real_worker](../tests/test_document_session.py); [test_plain_session_preserves_original_identity_and_no_view_copy](../tests/test_document_session.py); [test_private_reading_file_is_not_world_readable](../tests/test_document_session.py); [test_unicode_password_and_original_permission_policy](../tests/test_document_session.py); [test_page_bounds_and_rejected_nonintegers](../tests/test_document_session.py); [test_rotated_fit_page_stays_in_viewport](../tests/test_document_session.py); [test_zoom_percent_decimal_and_clamped_bounds](../tests/test_document_session.py); [test_authenticated_open_renders_searches_and_presents_without_mutating_source](../tests/test_reading_workflows_gtk.py); [test_cancel_password_and_wrong_password_preserve_previous_document](../tests/test_reading_workflows_gtk.py); [test_changed_source_after_initial_render_does_not_commit](../tests/test_reading_workflows_gtk.py); [test_document_close_cancels_open_and_resets_controls](../tests/test_reading_workflows_gtk.py); [test_failed_open_preserves_document_page_and_image](../tests/test_reading_workflows_gtk.py); [test_first_render_failure_does_not_commit_candidate](../tests/test_reading_workflows_gtk.py); [test_real_password_dialog_masks_and_clears_entry](../tests/test_reading_workflows_gtk.py); [test_recovery_decline_then_accept_preserves_original_and_content](../tests/test_reading_workflows_gtk.py); [test_superseded_open_cannot_replace_newer_document_and_cleans_session](../tests/test_reading_workflows_gtk.py); [test_fixtures_match_the_manifest_and_the_generator](../tests/test_damaged_corpus.py); [test_every_fixture_follows_its_expected_outcome_through_the_real_worker](../tests/test_damaged_corpus.py); [test_repair_labels_are_fixed_text_only](../tests/test_damaged_corpus.py).

Relacionados aos planos dinâmicos/UI: D01, D02, D13, D14, D15, D19, D20.

### Contratos individuais de operações

#### `open-render/inspect` — Inspecionar páginas, caixas e metadados

Estado: `current_bounded_source`; base: `current_linuxit_source`.

**Entradas:** Caminho de PDF local, bytes identificados por SHA-256, parser pypdf.

**Saídas:** Objeto pages/sizes/metadata com título, autor, assunto, criador e produtor; tamanhos consideram CropBox e rotação intrínseca.

**Limites:** A sessão de leitura aceita 1–20000 páginas e fonte não vazia até 256 MiB; parser não estabelece integridade semântica de todo conteúdo.

**Erros:** Arquivo vazio, parser inválido ou senha ausente → erro de leitura, sem páginas fictícias.

**Estado e efeitos:** Lê metadados e geometria, sem editar a fonte.

**Cancelamento:** Inspeção síncrona no worker; a geração da abertura descarta resposta tardia.

Fontes/requisitos: [app/rendering.py — document_info](../app/rendering.py).

Planos relacionados da família: S12-01-1, S12-01-2, S12-01-3, S12-01-4. Não são aceitação completa desta operação. Nova execução neste registro: `not_run`; expectativa e observação integral Foxit: `null`.

#### `open-render/render` — Renderizar página e reutilizar cache

Estado: `current_bounded_source`; base: `current_linuxit_source`.

**Entradas:** PDF da sessão, índice interno inteiro, largura de destino, diretório de cache, chave e formato PNG/JPEG.

**Saídas:** Imagem validada pelo tamanho e assinatura, associada à identidade do PDF/página/largura/formato.

**Limites:** Render requer Poppler/pdftocairo e dimensões finitas; limite de pixels e prazo do renderizador continuam aplicáveis.

**Erros:** Formato desconhecido, tamanho inválido, saída truncada ou pdftocairo ausente → erro sem imagem publicada como concluída.

**Estado e efeitos:** Pode criar arquivo de cache e processo pdftocairo; original não muda.

**Cancelamento:** Evento de cancelamento encerra subprocesso e rejeita cache incompleto; callback da geração antiga não desenha.

Fontes/requisitos: [app/rendering.py — render_page](../app/rendering.py).

Planos relacionados da família: S12-01-1, S12-01-2, S12-01-3, S12-01-4. Não são aceitação completa desta operação. Nova execução neste registro: `not_run`; expectativa e observação integral Foxit: `null`.

#### `open-render/obsolete` — Descartar renderização obsoleta

Estado: `current_bounded_source`; base: `current_linuxit_source`.

**Entradas:** Conclusão assíncrona contendo chave de documento, página, zoom e geração capturada no pedido.

**Saídas:** Só o pedido ainda atual atualiza pixbuf, status e geometria.

**Limites:** Fila de LatestRenderer ignora entradas substituídas; validade é identidade, não apenas caminho textual.

**Erros:** Concluir render antigo depois de abrir outro PDF → resultado ignorado, preservando tela atual.

**Estado e efeitos:** Substitui somente imagem/estado visual da geração atual; nenhum PDF é escrito.

**Cancelamento:** Fechar/trocar documento invalida geração e cancela trabalhos; callback já enfileirado deve validar novamente.

Fontes/requisitos: [app/main.py — PDFWindow.request_render](../app/main.py).

Planos relacionados da família: S12-01-1, S12-01-2, S12-01-3, S12-01-4. Não são aceitação completa desta operação. Nova execução neste registro: `not_run`; expectativa e observação integral Foxit: `null`.

#### `open-render/copy` — Salvar cópia local completa e exclusiva

Estado: `current_bounded_source`; base: `current_linuxit_source`.

**Entradas:** Origem local, identidade esperada e caminho .pdf novo em pasta existente.

**Saídas:** Cópia integral publicada exclusivamente e recibo do salvamento local.

**Limites:** Fonte até 512 MiB; pasta precisa oferecer publicação sem sobrescrita; arquivo remoto placeholder precisa estar disponível localmente.

**Erros:** Destino existente, fonte alterada ou publicação exclusiva indisponível → erro sem substituir arquivo existente.

**Estado e efeitos:** Cria cópia final só após copiar e conferir identidade; sucesso local não confirma sincronização remota.

**Cancelamento:** Cópia roda no worker; cancelamento/timeout pode exigir conferir pasta; não promete revogar cópia já publicada.

Fontes/requisitos: [app/local_files.py — copy_local_document](../app/local_files.py).

Planos relacionados da família: S12-01-1, S12-01-2, S12-01-3, S12-01-4. Não são aceitação completa desta operação. Nova execução neste registro: `not_run`; expectativa e observação integral Foxit: `null`.

#### `open-render/password-open` — Abrir PDF cifrado integrado ao leitor

Estado: `current_bounded_source`; base: `current_linuxit_source`.

**Entradas:** PDF cifrado, senha conhecida até 127 caracteres enviada por stdin, sessão privada e página inicial.

**Saídas:** Autenticação user/owner, representação privada de leitura e commit somente após primeiro render válido.

**Limites:** Senha não vai em argv/log; fonte até 256 MiB, representação até 512 MiB; política original /P é mantida na sessão.

**Erros:** Senha errada ou render inicial falho → erro fixo sem credencial, documento anterior preservado.

**Estado e efeitos:** Arquivo temporário privado e leases; fonte permanece cifrada, senha só em memória da sessão.

**Cancelamento:** Recusar diálogo ou cancelar abertura destrói candidato e preserva sessão anterior; lease ativo adia remoção de representação.

Fontes/requisitos: [app/document_session.py — prepare_document](../app/document_session.py), [app/main.py — PDFWindow.open_document](../app/main.py).

Planos relacionados da família: S12-01-1, S12-01-2, S12-01-3, S12-01-4. Não são aceitação completa desta operação. Nova execução neste registro: `not_run`; expectativa e observação integral Foxit: `null`.

#### `open-render/recovery` — Recuperar documentos danificados

Estado: `current_bounded_source`; base: `current_linuxit_source`.

**Entradas:** PDF danificado, consentimento explícito recover e destino privado da sessão. Extensão A6: edição recebe recover consentido e SHA-256 do original danificado, operações próprias e destino novo.

**Saídas:** Representação legível e categorias de reparo (xref, EOF, objeto ausente, conteúdo ilegível ou página omitida). reader_for_edit normaliza página/estrutura recuperável para edição de cópia, reabre strict e conserva verificações de autenticação/permissão no backend; sem reparo universal.

**Limites:** Recuperação melhor esforço; 1–20000 páginas reais, até 256 MiB na fonte/512 MiB na representação; não promete conteúdo perdido recuperado.

**Erros:** Recuperação recusada ou nenhuma página real recuperável → erro sem publicar representação nem trocar documento.

**Estado e efeitos:** Repara cópia privada; página com stream ilegível pode ficar branca e nó de página inexistente pode ser omitido.

**Cancelamento:** Cancelar candidato antes do commit mantém documento anterior e remove temporários liberados; não há reparo in-place.

Fontes/requisitos: [app/document_session.py — prepare_document](../app/document_session.py), [app/main.py — PDFWindow.open_document](../app/main.py), [app/recovered_edit.py — reader_for_edit](../app/recovered_edit.py).

Planos relacionados da família: S12-01-1, S12-01-2, S12-01-3, S12-01-4. Não são aceitação completa desta operação. Nova execução neste registro: `not_run`; expectativa e observação integral Foxit: `null`.


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

- **S12-02-1** (nominal, contrato próprio atual, `passed`): dado PDF de duas páginas na primeira página. Ação: Navegar para a segunda e girar a visualização. Esperado: Página selecionada é a segunda; transformação visual permanece coerente com a geometria. Execução própria em 2026-10-21T21:24:11-03:00, revisão `ac89254204fb`, fronteira PDFWindow.goto_page/_rotate: [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e31.json).
- **S12-02-2** (exception, contrato próprio atual, `passed`): dado Render da página anterior ainda em andamento. Ação: Mudar página e aguardar os callbacks. Esperado: O resultado obsoleto não toma o lugar da página atual. Execução própria em 2026-10-21T21:24:13-03:00, revisão `ac89254204fb`, fronteira PDFWindow.request_render callbacks: [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e31.json).

**Lacunas da referência Foxit**

- Limites e modos efetivos Foxit dependem da classe/estado ativo.
- Updaters de zoom só enviam desabilitação nos limites; política completa não foi reconstruída.

**Observação parcial preservada do original:** UI03/04 em geometria.pdf: sem documento controles pálidos; Next1→2→3, Last8/8 e Next mantém8/8. Menu1% e6400%; menos/mais nos extremos mantêm os valores. FitPage47.15%, PAGE0011/8. Recorte visual sem vínculo comprovado aos IDs estáticos; entradas arbitrárias e demais modos abertos.

Evidências: [docs/VM-FOXIT-2026-10-18.md](../docs/VM-FOXIT-2026-10-18.md), [docs/VM-SENHA-E-PARADA-2026-10-18.md](../docs/VM-SENHA-E-PARADA-2026-10-18.md), [docs/P03-INTERFACE-E-PARADA-2026-10-19.md](../docs/P03-INTERFACE-E-PARADA-2026-10-19.md).

Fontes: [app/main.py](../app/main.py), [app/page_cache.py](../app/page_cache.py), [app/rendering.py](../app/rendering.py), [app/pdf_changes.py](../app/pdf_changes.py), [app/edit_tasks.py](../app/edit_tasks.py), [app/worker_cli.py](../app/worker_cli.py), [docs/SEGURANCA-ACESSIBILIDADE.md](../docs/SEGURANCA-ACESSIBILIDADE.md), [app/local_files.py](../app/local_files.py), [app/folder_dialogs.py](../app/folder_dialogs.py), [docs/PASTAS-SINCRONIZADAS.md](../docs/PASTAS-SINCRONIZADAS.md), [app/document_session.py](../app/document_session.py), [app/navigation.py](../app/navigation.py), [app/page_surface.py](../app/page_surface.py), [docs/LEITURA-ABERTURA-NAVEGACAO-APRESENTACAO.md](../docs/LEITURA-ABERTURA-NAVEGACAO-APRESENTACAO.md), [testes/resultados/0.1.16/validation-review.json](../testes/resultados/0.1.16/validation-review.json), [docs/ETAPA-11.md](../docs/ETAPA-11.md), [docs/windows-evidence/foxit-rea/ui-state-contracts-2026-10-16.json](../docs/windows-evidence/foxit-rea/ui-state-contracts-2026-10-16.json), [docs/windows-evidence/foxit-rea/zoom-presets.json](../docs/windows-evidence/foxit-rea/zoom-presets.json), [docs/REA-ESTATICA-BUSCA-IMPRESSAO-2026-10-18.md](../docs/REA-ESTATICA-BUSCA-IMPRESSAO-2026-10-18.md), [docs/REA-ESTATICA-CONTINUACAO-2026-10-18.md](../docs/REA-ESTATICA-CONTINUACAO-2026-10-18.md), [docs/VM-FOXIT-2026-10-18.md](../docs/VM-FOXIT-2026-10-18.md), [docs/VM-SENHA-E-PARADA-2026-10-18.md](../docs/VM-SENHA-E-PARADA-2026-10-18.md), [docs/P03-INTERFACE-E-PARADA-2026-10-19.md](../docs/P03-INTERFACE-E-PARADA-2026-10-19.md).

Testes próprios existentes, sem nova execução nesta tabela: [test_search_navigation_selection_and_rotation](../tests/test_gui.py); [test_intrinsic_rotation_and_cropbox_match_text_geometry](../tests/test_regressions.py); [test_five_panel_headers_fit_default_and_small_window](../tests/test_sidebar_layout_gtk.py); [test_combined_edits_preserve_tree_destinations_geometry_and_source](../tests/test_extended_edits.py); [test_final_name_is_absent_while_real_copy_is_in_progress](../tests/test_sync_folders.py); [test_save_copy_uses_worker_preserves_original_and_only_confirms_local_save](../tests/test_sync_folders_gtk.py); [test_page_bounds_and_rejected_nonintegers](../tests/test_document_session.py); [test_rotated_fit_page_stays_in_viewport](../tests/test_document_session.py); [test_zoom_percent_decimal_and_clamped_bounds](../tests/test_document_session.py); [test_keyboard_page_changes_do_not_move_focus_to_thumbnail_list](../tests/test_reading_workflows_gtk.py); [test_page_entries_clamp_and_restore_invalid_value_and_disable_edges](../tests/test_reading_workflows_gtk.py); [test_rotated_cropbox_geometry_matches_selection_and_presentation](../tests/test_reading_workflows_gtk.py); [test_zoom_extremes_use_logical_surface_and_reject_nonfinite_input](../tests/test_reading_workflows_gtk.py).

Relacionados aos planos dinâmicos/UI: D03, UI03, UI04.

### Contratos individuais de operações

#### `navigation/goto` — Ir para página válida

Estado: `current_bounded_source`; base: `current_linuxit_source`.

**Entradas:** Documento aberto, número interno de página inteiro e parâmetro force opcional.

**Saídas:** Página atual limitada aos extremos válidos e pedido de render correspondente.

**Limites:** Sem documento não há salto; entrada de UI baseada em um converte uma vez para índice baseado em zero.

**Erros:** Índice fora dos extremos → navegação fica no extremo; bool/decimal não é índice válido no domínio Navigation.

**Estado e efeitos:** Muda página, seleção visual e render; não muda conteúdo do arquivo.

**Cancelamento:** Ação de UI é síncrona; render anterior é invalidado ao pedir a nova página.

Fontes/requisitos: [app/main.py — PDFWindow.goto_page](../app/main.py).

Planos relacionados da família: S12-02-1, S12-02-2. Não são aceitação completa desta operação. Nova execução neste registro: `not_run`; expectativa e observação integral Foxit: `null`.

#### `navigation/zoom` — Aplicar zoom e ajuste

Estado: `current_bounded_source`; base: `current_linuxit_source`.

**Entradas:** Modo fit-page/fit-width ou percentual digitado e viewport disponível.

**Saídas:** Largura/escala e superfície virtual coerentes com CropBox/rotação.

**Limites:** Percentual 1–6400; dimensão máxima de render é limitada pela superfície virtual, não alocação ilimitada do zoom.

**Erros:** Percentual não numérico ou não finito → rejeitar entrada; extremos são limitados a 1/6400 no domínio.

**Estado e efeitos:** Atualiza escala, scroll e render, sem /Rotate salvo.

**Cancelamento:** Troca de zoom invalida render anterior; o ajuste síncrono não tem tarefa longa para cancelar.

Fontes/requisitos: [app/main.py — PDFWindow._fit_page](../app/main.py).

Planos relacionados da família: S12-02-1, S12-02-2. Não são aceitação completa desta operação. Nova execução neste registro: `not_run`; expectativa e observação integral Foxit: `null`.

#### `navigation/view-rotation` — Rotacionar visualização

Estado: `current_bounded_source`; base: `current_linuxit_source`.

**Entradas:** Página atual e incremento de rotação visual pelo controle da UI.

**Saídas:** Página girada e transformações tela↔PDF atualizadas.

**Limites:** Rotação de visualização é separada da rotação persistida no PDF.

**Erros:** Sem documento/página → não publicar rotação ou coordenadas válidas fictícias.

**Estado e efeitos:** Muda orientação visual/cache; arquivo original não é regravado.

**Cancelamento:** Ação síncrona; nova geração de render descarta conclusão na orientação anterior.

Fontes/requisitos: [app/main.py — PDFWindow._rotate](../app/main.py).

Planos relacionados da família: S12-02-1, S12-02-2. Não são aceitação completa desta operação. Nova execução neste registro: `not_run`; expectativa e observação integral Foxit: `null`.

#### `navigation/saved-rotation` — Persistir rotação em cópia

Estado: `current_bounded_source`; base: `current_linuxit_source`.

**Entradas:** Operação rotate-page com page inteiro e angle em -270,-180,-90,90,180,270; hash atual e cópia nova.

**Saídas:** /Rotate da página atualizado na cópia verificada.

**Limites:** Não aceita 0/45/360 nem página fora do documento; lote de alterações até 1000.

**Erros:** Ângulo não suportado ou página inexistente → ValueError antes da publicação final.

**Estado e efeitos:** Escreve cópia; não gira bytes de conteúdo nem muda fonte; entra no histórico de rascunho.

**Cancelamento:** Desfazer remove operação do rascunho; cancelamento do worker não altera fonte nem cópia já salva.

Fontes/requisitos: [app/pdf_changes.py — _apply](../app/pdf_changes.py).

Planos relacionados da família: S12-02-1, S12-02-2. Não são aceitação completa desta operação. Nova execução neste registro: `not_run`; expectativa e observação integral Foxit: `null`.


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

- **S12-03-1** (nominal, contrato próprio atual, `passed`): dado Página retrato e viewport paisagem. Ação: Alternar ajustar página e preencher. Esperado: A escala e o centro respeitam o modo próprio; não atribuir esse cálculo ao Foxit. Execução própria em 2026-10-21T21:24:15-03:00, revisão `ac89254204fb`, fronteira PresentationWindow fit/fill: [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e31.json).
- **S12-03-2** (exception, contrato próprio atual, `passed`): dado Worker retorna falha de imagem. Ação: Entregar o erro à apresentação. Esperado: Exibir estado de falha, mantendo o ciclo de vida da janela válido. Execução própria em 2026-10-21T21:24:17-03:00, revisão `ac89254204fb`, fronteira PresentationWindow render failure: [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e31.json).

**Lacunas da referência Foxit**

- Ajuste/preenchimento, atalhos e múltiplos monitores do original não foram observados.

Fontes: [app/presentation.py](../app/presentation.py), [app/page_cache.py](../app/page_cache.py), [app/document_session.py](../app/document_session.py), [app/navigation.py](../app/navigation.py), [app/page_surface.py](../app/page_surface.py), [docs/LEITURA-ABERTURA-NAVEGACAO-APRESENTACAO.md](../docs/LEITURA-ABERTURA-NAVEGACAO-APRESENTACAO.md), [testes/resultados/0.1.16/validation-review.json](../testes/resultados/0.1.16/validation-review.json), [docs/FOXIT-REA.md](../docs/FOXIT-REA.md).

Testes próprios existentes, sem nova execução nesta tabela: [test_presentation_fit_fill_center_and_error](../tests/test_viewer.py); [test_presentation_handles_portrait_and_landscape](../tests/test_viewer.py); [test_monitor_selection_removal_and_fullscreen_request](../tests/test_reading_workflows_gtk.py); [test_presentation_keys_respect_control_focus_and_restore_parent_focus](../tests/test_reading_workflows_gtk.py); [test_rotated_cropbox_geometry_matches_selection_and_presentation](../tests/test_reading_workflows_gtk.py).

Relacionados aos planos dinâmicos/UI: D03.

### Contratos individuais de operações

#### `presentation/fit-fill` — Apresentar com ajustar/preencher

Estado: `current_bounded_source`; base: `current_linuxit_source`.

**Entradas:** Sessão aberta, página e modo ajustar/preencher com dimensões da janela de apresentação.

**Saídas:** Enquadramento completo em ajustar ou recorte preenchendo viewport em preencher.

**Limites:** Respeita proporção, rotação e dimensões válidas; não é transformação persistida.

**Erros:** Documento ausente → erro Abra um documento antes de iniciar a apresentação.

**Estado e efeitos:** Cria janela de apresentação, cache e render próprios; não modifica PDF.

**Cancelamento:** Fechar apresentação cancela/ignora renders da janela; mudança de modo substitui pedido anterior.

Fontes/requisitos: [app/presentation.py — PresentationWindow._target_width_for](../app/presentation.py).

Planos relacionados da família: S12-03-1, S12-03-2. Não são aceitação completa desta operação. Nova execução neste registro: `not_run`; expectativa e observação integral Foxit: `null`.

#### `presentation/pan` — Mover página na apresentação

Estado: `current_bounded_source`; base: `current_linuxit_source`.

**Entradas:** Posição de arraste/tecla/roda, tamanho da página escalada e viewport.

**Saídas:** Deslocamento limitado pelo excesso de conteúdo nos dois eixos.

**Limites:** Pan depende de conteúdo maior que viewport; passo de teclas 110 e roda 95 pixels no código atual.

**Erros:** Movimento além da borda → posição limitada ao pan possível, sem mover para área vazia ilimitada.

**Estado e efeitos:** Só altera enquadramento/laser visual na apresentação.

**Cancelamento:** Interação local síncrona; fechar janela encerra animação, sem tarefa de arquivo pendente.

Fontes/requisitos: [app/presentation.py — PresentationWindow._pan_bounds](../app/presentation.py).

Planos relacionados da família: S12-03-1, S12-03-2. Não são aceitação completa desta operação. Nova execução neste registro: `not_run`; expectativa e observação integral Foxit: `null`.

#### `presentation/monitors` — Apresentar em múltiplos monitores

Estado: `current_bounded_source`; base: `current_linuxit_source`.

**Entradas:** Índice de monitor enumerado por GDK e solicitação de fullscreen.

**Saídas:** Solicitação ao compositor e estado concedido observado; fallback quando monitor desaparece.

**Limites:** Monitores virtuais testados separadamente de monitores físicos; compositor pode recusar fullscreen.

**Erros:** Monitor removido/inválido → atualizar enumeração e usar fallback, sem prometer posição física não observada.

**Estado e efeitos:** Move janela/fullscreen; não muda configuração de monitores do host.

**Cancelamento:** Fechar apresentação sai de fullscreen; mudança de monitor substitui escolha local sem aguardar render antigo.

Fontes/requisitos: [app/presentation.py — PresentationWindow._refresh_monitors](../app/presentation.py), [app/presentation.py — PresentationWindow._fullscreen_on_selected_monitor](../app/presentation.py).

Planos relacionados da família: S12-03-1, S12-03-2. Não são aceitação completa desta operação. Nova execução neste registro: `not_run`; expectativa e observação integral Foxit: `null`.


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

- **S12-04-1** (nominal, contrato próprio atual, `passed`): dado Fixture de busca; só páginas, sem caixa/palavra inteira. Ação: Pesquisar alvo. Esperado: Contrato próprio: três ocorrências; palavra inteira reduz para duas. Execução própria em 2026-10-21T21:24:18-03:00, revisão `ac89254204fb`, fronteira search_engine.TextSearchIndex: [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e31.json).
- **S12-04-2** (exception, contrato próprio atual, `passed`): dado Consulta com 257 caracteres. Ação: Chamar TextSearchIndex.search. Esperado: ValueError antes de extrair páginas. Execução própria em 2026-10-21T21:24:18-03:00, revisão `ac89254204fb`, fronteira search_engine.TextSearchIndex: [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e31.json).

**Lacunas da referência Foxit**

- Normalização e algoritmos completos do Foxit; ordem/limites/destaques precisam de comparação.

**Observação parcial preservada do original:** D12 no corpus5000: Stop ativo encerra e preserva232 resultados; troca para geometria mantém busca em12.pdf; fechar12.pdf durante busca encerra em1738 e conserva lista parcial. Contagens não determinísticas/latência não medida; contrato próprio não substituído. D10 misto anterior preservado.

Evidências: [docs/VM-FOXIT-2026-10-18.md](../docs/VM-FOXIT-2026-10-18.md), [docs/VM-BUSCA-2026-10-18-2020.md](../docs/VM-BUSCA-2026-10-18-2020.md), [docs/P03-BUSCA-IMPRESSAO-2026-10-19.md](../docs/P03-BUSCA-IMPRESSAO-2026-10-19.md), [docs/P03-CANCELAMENTO-MOSAICO-2026-10-19.md](../docs/P03-CANCELAMENTO-MOSAICO-2026-10-19.md).

Fontes: [app/search_engine.py](../app/search_engine.py), [app/main.py](../app/main.py), [app/rendering.py](../app/rendering.py), [testes/resultados/0.1.16/validation-review.json](../testes/resultados/0.1.16/validation-review.json), [docs/REA-BUSCA-IMPRESSAO.md](../docs/REA-BUSCA-IMPRESSAO.md), [docs/windows-evidence/foxit-rea/search-print-contracts.json](../docs/windows-evidence/foxit-rea/search-print-contracts.json), [docs/REA-ESTATICA-CONTINUACAO-2026-10-18.md](../docs/REA-ESTATICA-CONTINUACAO-2026-10-18.md), [docs/VM-FOXIT-2026-10-18.md](../docs/VM-FOXIT-2026-10-18.md), [docs/VM-BUSCA-2026-10-18-2020.md](../docs/VM-BUSCA-2026-10-18-2020.md), [docs/P03-BUSCA-IMPRESSAO-2026-10-19.md](../docs/P03-BUSCA-IMPRESSAO-2026-10-19.md), [docs/P03-CANCELAMENTO-MOSAICO-2026-10-19.md](../docs/P03-CANCELAMENTO-MOSAICO-2026-10-19.md).

Testes próprios existentes, sem nova execução nesta tabela: [test_options_and_real_pdf](../tests/test_search.py); [test_global_limit_progress_and_cancel_cover_metadata](../tests/test_search_scopes.py); [test_highlight_preference_and_navigation_change_pixels_without_new_search](../tests/test_search_highlights.py).

Relacionados aos planos dinâmicos/UI: D04, D05, D06, D10, D11, D12, UI08.

### Contratos individuais de operações

#### `search-text/literal` — Pesquisar texto literal

Estado: `current_bounded_source`; base: `current_linuxit_source`.

**Entradas:** Consulta Unicode, flags explícitas de fontes e TextSearchIndex da sessão.

**Saídas:** Hits com origem, página, intervalo/snippet e geometria quando conhecida, mais avisos/limite.

**Limites:** Entrada até 256 caracteres; max_hits padrão 5000; vazio retorna zero; texto não pesquisável não vira OCR automático.

**Erros:** Fonte alterada entre indexação e consulta → RuntimeError e pedido de reabertura; não usar coordenadas antigas.

**Estado e efeitos:** Cacheia extração por identidade e preenche resultados; não grava PDF.

**Cancelamento:** Evento cancel é consultado entre páginas/lotes; resultados da geração anterior não entram na nova lista.

Fontes/requisitos: [app/search_engine.py — TextSearchIndex.search](../app/search_engine.py).

Planos relacionados da família: S12-04-1, S12-04-2. Não são aceitação completa desta operação. Nova execução neste registro: `not_run`; expectativa e observação integral Foxit: `null`.

#### `search-text/whole` — Aplicar palavra inteira

Estado: `current_bounded_source`; base: `current_linuxit_source`.

**Entradas:** Texto normalizado, consulta e whole_words booleano.

**Saídas:** Spans somente quando ambos os limites não pertencem a palavra Unicode.

**Limites:** Palavra inclui categorias Unicode L/N/M e underscore; não equivale ao segmentador linguístico completo Foxit.

**Erros:** Consulta vazia → nenhum span; ocorrência dentro de palavra

**Estado e efeitos:** Cálculo puro sobre strings, sem alterar índice nem PDF.

**Cancelamento:** Gerador de spans não tem token próprio; o chamador de busca interrompe entre páginas/lotes.

Fontes/requisitos: [app/search_matching.py — literal_spans](../app/search_matching.py).

Planos relacionados da família: S12-04-1, S12-04-2. Não são aceitação completa desta operação. Nova execução neste registro: `not_run`; expectativa e observação integral Foxit: `null`.

#### `search-text/case` — Distinguir maiúsculas/minúsculas

Estado: `current_bounded_source`; base: `current_linuxit_source`.

**Entradas:** Texto e consulta, match_case e ignore_accents.

**Saídas:** Texto normalizado NFC e, quando solicitado, casefold/remoção NFD de marcas; offsets mapeados pelo índice.

**Limites:** Expansão casefold admite até 768 caracteres normalizados após limite de 256 na entrada.

**Erros:** Modo/consulta inválidos na validação → ValueError; normalização não autoriza regex livre.

**Estado e efeitos:** Função pura; cache de página mantém mapeamento para geometria original.

**Cancelamento:** Não há processo cancelável nesta transformação curta; busca externa controla interrupção.

Fontes/requisitos: [app/search_matching.py — normalized](../app/search_matching.py).

Planos relacionados da família: S12-04-1, S12-04-2. Não são aceitação completa desta operação. Nova execução neste registro: `not_run`; expectativa e observação integral Foxit: `null`.

#### `search-text/normalization` — Normalizar acentos e hifenização

Estado: `current_bounded_source`; base: `current_linuxit_source`.

**Entradas:** Texto extraído, posições de linhas/colunas, flags de acento e junção de hifens.

**Saídas:** Hits mapeados de texto normalizado para retângulos reais sem unir colunas arbitrariamente.

**Limites:** Junção por hífen é opcional; ordem de leitura é heurística delimitada, não recuperação universal de layout.

**Erros:** Geometria ausente → resultado sem retângulo inventado; fonte alterada

**Estado e efeitos:** Cria representação normalizada em memória, original preservado.

**Cancelamento:** page_hits recebe cancel; retorno parcial não deve ser apresentado como varredura concluída.

Fontes/requisitos: [app/search_engine.py — page_hits](../app/search_engine.py).

Planos relacionados da família: S12-04-1, S12-04-2. Não são aceitação completa desta operação. Nova execução neste registro: `not_run`; expectativa e observação integral Foxit: `null`.

#### `search-text/highlight` — Destacar e navegar por ocorrências

Estado: `current_bounded_source`; base: `current_linuxit_source`.

**Entradas:** Hit selecionado, tipo de origem, página/retângulos conhecidos e highlight_all.

**Saídas:** Seleção de resultado, destaque e navegação apropriados ao tipo.

**Limites:** Hit textual pode navegar; marcador seleciona painel; resultados de anexo não viram coordenadas no hospedeiro.

**Erros:** Página/destino desconhecidos → selecionar/listar sem salto para página zero nem retângulo fictício.

**Estado e efeitos:** Muda UI, cache e destaque; não refaz consulta ao só trocar highlight_all.

**Cancelamento:** Seleção síncrona; render do novo destino verifica geração antes de exibir.

Fontes/requisitos: [app/main.py — PDFWindow._select_search_hit](../app/main.py).

Planos relacionados da família: S12-04-1, S12-04-2. Não são aceitação completa desta operação. Nova execução neste registro: `not_run`; expectativa e observação integral Foxit: `null`.

#### `search-text/cancel` — Cancelar pesquisa e descartar resultados antigos

Estado: `current_bounded_source`; base: `current_linuxit_source`.

**Entradas:** Busca ativa e ações Stop, consulta nova, documento fechado/trocado.

**Saídas:** Tarefa sinalizada, resultados antigos impedidos de repovoar a geração atual.

**Limites:** Sem latência máxima de parada comprovada; contagens parciais dependem do instante de interrupção.

**Erros:** Worker cancelado → estado cancelado/resultado parcial conforme chamador, nunca busca completa silenciosamente.

**Estado e efeitos:** Libera geração/trabalho; não modifica fonte nem históricos já salvos.

**Cancelamento:** Cancelamento é cooperativo e subprocesso cancelável; não repetir comandos à VM travada.

Fontes/requisitos: [app/main.py — PDFWindow._start_search](../app/main.py).

Planos relacionados da família: S12-04-1, S12-04-2. Não são aceitação completa desta operação. Nova execução neste registro: `not_run`; expectativa e observação integral Foxit: `null`.


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

- **S12-05-1** (nominal, contrato próprio atual, `passed`): dado Fixture com dois títulos contendo alvo, só marcadores. Ação: Pesquisar alvo, selecionar os resultados e ativar o marcador no painel. Esperado: Dois hits; um aponta à segunda página e outro permanece page=null; rects=[] em ambos. Selecionar o resultado só seleciona o marcador (página não muda, como no Foxit em E24); ativar o marcador leva à segunda página. Execução própria em 2026-10-21T21:24:18-03:00, revisão `ac89254204fb`, fronteira PDFWindow find bar + _select_search_hit: [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e31.json).
- **S12-05-2** (exception, contrato próprio atual, `passed`): dado Hit de marcador sem destino local. Ação: Selecionar esse resultado. Esperado: Não fabricar página de destino ou retângulo de destaque. Execução própria em 2026-10-21T21:24:21-03:00, revisão `ac89254204fb`, fronteira PDFWindow _select_search_hit: [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e31.json).

**Lacunas da referência Foxit**

- Classe dos IDs 7911/7913 e comportamento de busca/navegação Foxit.
- A junção estrutural de ID 7913 ao handler de +0x1d58 continua ambígua.

**Observação parcial preservada do original:** D07: dois hits selecionam marcadores no painel; ativação nativa do primeiro navega1→2. Seleção/duplo clique no resultado não provou salto; segundo mantém página2 sem diálogo. Não inferir destino nulo. E24 (21/10/2026): seleção e duplo clique no resultado de marcador mantêm a página; ordem Relevance Ranking marcadores→texto→comentário. Decisão do usuário: Linuxit segue esse comportamento.

Evidências: [docs/VM-FOXIT-2026-10-18.md](../docs/VM-FOXIT-2026-10-18.md), [docs/VM-BUSCA-2026-10-18-2020.md](../docs/VM-BUSCA-2026-10-18-2020.md), [docs/P03-BUSCA-IMPRESSAO-2026-10-19.md](../docs/P03-BUSCA-IMPRESSAO-2026-10-19.md), [docs/VM-E24-2026-10-21.md](../docs/VM-E24-2026-10-21.md).

Fontes: [app/search_engine.py](../app/search_engine.py), [app/pdf_panels.py](../app/pdf_panels.py), [testes/resultados/0.1.16/validation-review.json](../testes/resultados/0.1.16/validation-review.json), [docs/REA-BUSCA-IMPRESSAO.md](../docs/REA-BUSCA-IMPRESSAO.md), [docs/windows-evidence/foxit-rea/search-print-contracts.json](../docs/windows-evidence/foxit-rea/search-print-contracts.json), [docs/windows-evidence/foxit-rea/search-checkbox-bindings.json](../docs/windows-evidence/foxit-rea/search-checkbox-bindings.json), [docs/REA-ESTATICA-CONTINUACAO-2026-10-18.md](../docs/REA-ESTATICA-CONTINUACAO-2026-10-18.md), [docs/VM-FOXIT-2026-10-18.md](../docs/VM-FOXIT-2026-10-18.md), [docs/VM-BUSCA-2026-10-18-2020.md](../docs/VM-BUSCA-2026-10-18-2020.md), [docs/P03-BUSCA-IMPRESSAO-2026-10-19.md](../docs/P03-BUSCA-IMPRESSAO-2026-10-19.md), [docs/VM-E24-2026-10-21.md](../docs/VM-E24-2026-10-21.md).

Testes próprios existentes, sem nova execução nesta tabela: [test_bookmark_without_local_page_is_not_given_a_fake_destination](../tests/test_search_scopes.py); [test_ui_toggles_scopes_and_bookmark_result_keeps_page](../tests/test_search_scopes.py); [test_bookmark_result_selects_bookmark_without_changing_page](../tests/test_search_foxit_order_gtk.py); [test_results_list_bookmarks_then_page_text_then_comments](../tests/test_search_foxit_order_gtk.py).

Relacionados aos planos dinâmicos/UI: D07, UI06.

### Contratos individuais de operações

#### `search-bookmarks/titles` — Pesquisar títulos de marcadores

Estado: `current_bounded_source`; base: `current_linuxit_source`.

**Entradas:** Consulta e fonte marcadores habilitada, títulos/árvore lidos do PDF.

**Saídas:** Hits independentes source=bookmark com título e referência ao nó.

**Limites:** Destino pode estar ausente; texto segue flags Unicode/limite da busca.

**Erros:** Marcador sem destino → hit ainda pode ser listado; não inventar número de página.

**Estado e efeitos:** Lê outline e adiciona resultados sem editar marcadores.

**Cancelamento:** Consulta de metadados respeita cancelamento do índice; UI ignora geração obsoleta.

Fontes/requisitos: [app/search_engine.py — TextSearchIndex._metadata_hits](../app/search_engine.py).

Planos relacionados da família: S12-05-1, S12-05-2. Não são aceitação completa desta operação. Nova execução neste registro: `not_run`; expectativa e observação integral Foxit: `null`.

#### `search-bookmarks/destinations` — Ativar resultados com destino válido ou ausente

Estado: `current_bounded_source`; base: `current_linuxit_source`.

**Entradas:** Hit de marcador e ativação posterior do próprio nó no painel.

**Saídas:** Selecionar hit só destaca marcador; ativar nó navega quando há destino local conhecido.

**Limites:** Seleção de busca e ativação do marcador são ações distintas; URI/ação remota não é salto local presumido.

**Erros:** Destino não resolvido → manter página atual; não inferir que página zero é destino.

**Estado e efeitos:** Seleção de painel e, na ativação válida, página atual; PDF preservado.

**Cancelamento:** Ação síncrona; mudança de documento invalida associação ao nó antigo.

Fontes/requisitos: [app/main.py — PDFWindow._select_search_hit](../app/main.py).

Planos relacionados da família: S12-05-1, S12-05-2. Não são aceitação completa desta operação. Nova execução neste registro: `not_run`; expectativa e observação integral Foxit: `null`.


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

- **S12-06-1** (nominal, contrato próprio atual, `passed`): dado Só comentários da fixture. Ação: Pesquisar assunto, depois alvo. Esperado: Uma ocorrência em cada consulta; o campo assunto é separado do conteúdo. Execução própria em 2026-10-21T21:24:24-03:00, revisão `ac89254204fb`, fronteira search_engine.TextSearchIndex: [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e31.json).
- **S12-06-2** (exception, contrato próprio atual, `passed`): dado Só comentários, consulta Autor. Ação: Pesquisar o campo de autor com o contrato corrigido na fonte posterior ao pacote0.1.13. Esperado: Uma ocorrência source=comment na página1 do fixture preservado; autoria é pesquisável junto de assunto/conteúdo. Execução própria em 2026-10-21T21:24:24-03:00, revisão `ac89254204fb`, fronteira search_engine.TextSearchIndex: [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e31.json).

**Lacunas da referência Foxit**

- Demais tipos e campos pesquisados, respostas, duplicação entre campos, ordenação e destinos da busca mista. A observação inicial cobre somente a nota sintética preservada.

**Observação parcial preservada do original:** Recortes de corpo/assunto/autor preservados; D10 seleciona nota na página1 e abre Format sem editar. Autor corrigido somente na fonte; demais tipos/respostas ainda abertos.

Evidências: [docs/VM-FOXIT-2026-10-18.md](../docs/VM-FOXIT-2026-10-18.md), [docs/BUSCA-AUTOR-COMENTARIOS.md](../docs/BUSCA-AUTOR-COMENTARIOS.md), [docs/P03-BUSCA-IMPRESSAO-2026-10-19.md](../docs/P03-BUSCA-IMPRESSAO-2026-10-19.md).

Fontes: [app/search_engine.py](../app/search_engine.py), [app/pdf_panels.py](../app/pdf_panels.py), [app/pdf_comments.py](../app/pdf_comments.py), [testes/resultados/0.1.16/validation-review.json](../testes/resultados/0.1.16/validation-review.json), [docs/REA-BUSCA-IMPRESSAO.md](../docs/REA-BUSCA-IMPRESSAO.md), [docs/windows-evidence/foxit-rea/search-print-contracts.json](../docs/windows-evidence/foxit-rea/search-print-contracts.json), [docs/REA-ESTATICA-CONTINUACAO-2026-10-18.md](../docs/REA-ESTATICA-CONTINUACAO-2026-10-18.md), [docs/VM-FOXIT-2026-10-18.md](../docs/VM-FOXIT-2026-10-18.md), [testes/resultados/vm-2026-10-18/foxit-observations.json](../testes/resultados/vm-2026-10-18/foxit-observations.json), [docs/BUSCA-AUTOR-COMENTARIOS.md](../docs/BUSCA-AUTOR-COMENTARIOS.md), [docs/P03-BUSCA-IMPRESSAO-2026-10-19.md](../docs/P03-BUSCA-IMPRESSAO-2026-10-19.md).

Testes próprios existentes, sem nova execução nesta tabela: [test_comment_subject_contents_and_author_are_searchable](../tests/test_search_scopes.py); [test_preserved_author_only_term_matches_the_recorded_page](../tests/test_search_comment_author.py); [test_author_matching_respects_case_whole_words_and_accents](../tests/test_search_comment_author.py); [test_comment_without_author_still_searches_subject_and_body](../tests/test_search_comment_author.py).

Relacionados aos planos dinâmicos/UI: D08, D09.

### Contratos individuais de operações

#### `search-comments/body-subject` — Pesquisar assunto/conteúdo de comentário

Estado: `current_bounded_source`; base: `current_linuxit_source`.

**Entradas:** Consulta, fonte comentários e registros de assunto/conteúdo inspecionados.

**Saídas:** Hits source=comment ligados à identidade do objeto e página quando conhecida.

**Limites:** Metadados textuais não executam rich text/scripts; inclui assuntos/conteúdos dentro dos limites do inspetor.

**Erros:** Grafo de anotações inválido → aviso de inspeção parcial, sem afirmar busca completa.

**Estado e efeitos:** Lê comentários e produz resultados; não edita texto/autor.

**Cancelamento:** Inspeção e índice usam cancel; resultados de tarefa antiga são descartados pela geração.

Fontes/requisitos: [app/search_engine.py — TextSearchIndex._metadata_hits](../app/search_engine.py).

Planos relacionados da família: S12-06-1, S12-06-2. Não são aceitação completa desta operação. Nova execução neste registro: `not_run`; expectativa e observação integral Foxit: `null`.

#### `search-comments/author` — Pesquisar autor de comentário

Estado: `current_bounded_source`; base: `current_linuxit_source`.

**Entradas:** Consulta e campo /T de autor de comentário, além dos demais campos pesquisáveis.

**Saídas:** Hit do comentário quando o autor casa; identidade evita deduplicar objetos distintos só por texto igual.

**Limites:** Busca por autor é textual, não autenticação de identidade nem prova de autoria.

**Erros:** Autor ausente → não acrescentar autor fictício; consulta ausente no autor não elimina hits de conteúdo.

**Estado e efeitos:** Não altera comentário nem assinatura; correção própria já está na fonte.

**Cancelamento:** Segue cancelamento da busca e invalidação por documento/consulta.

Fontes/requisitos: [app/search_engine.py — TextSearchIndex._metadata_hits](../app/search_engine.py).

Planos relacionados da família: S12-06-1, S12-06-2. Não são aceitação completa desta operação. Nova execução neste registro: `not_run`; expectativa e observação integral Foxit: `null`.

#### `search-comments/replies` — Pesquisar respostas e demais tipos/campos

Estado: `current_bounded_source`; base: `current_linuxit_source`.

**Entradas:** Reader, cancel opcional e grafo de Annots, IRT/RT/Popup.

**Saídas:** Comentários com IDs estáveis, pai/tipo/profundidade e avisos de grafos parciais.

**Limites:** Até 50000 anotações, texto 65536 e profundidade 64; aliases são deduplicados por objeto.

**Erros:** Ciclo, resposta sem pai ou referência inconsistente → aviso/registro parcial, sem fundir objetos distintos iguais em texto.

**Estado e efeitos:** Somente inspeção; não conserta vínculos silenciosamente.

**Cancelamento:** Callback cancel interrompe inspeção; lista parcial mantém aviso de incompletude.

Fontes/requisitos: [app/pdf_comments.py — inspect_comments](../app/pdf_comments.py).

Planos relacionados da família: S12-06-1, S12-06-2. Não são aceitação completa desta operação. Nova execução neste registro: `not_run`; expectativa e observação integral Foxit: `null`.


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

- **S12-07-1** (nominal, contrato próprio atual, `passed`): dado PDF sintético com anexo textual contendo alvo; fixture ainda a especializar. Ação: Pesquisar incluindo anexos. Esperado: Encontrar o termo no anexo suportado e identificar índice/nome/página interna sem destino principal fictício. Execução própria em 2026-10-21T21:24:24-03:00, revisão `ac89254204fb`, fronteira worker search-attachments: [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e31.json).
- **S12-07-2** (exception, contrato próprio atual, `passed`): dado Mesmo PDF com um anexo não suportado. Ação: Pesquisar incluindo anexos. Esperado: Informar o anexo omitido e seu motivo; UI deve indicar anexos parciais. Execução própria em 2026-10-21T21:24:24-03:00, revisão `ac89254204fb`, fronteira worker search-attachments: [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e31.json).

**Lacunas da referência Foxit**

- Travessia completa, extratores, formatos, limites, ordenação e associação de resultados no original.

Fontes: [app/attachment_search.py](../app/attachment_search.py), [app/search_tasks.py](../app/search_tasks.py), [app/search_matching.py](../app/search_matching.py), [app/pdf_attachments.py](../app/pdf_attachments.py), [app/search_engine.py](../app/search_engine.py), [app/worker_cli.py](../app/worker_cli.py), [app/main.py](../app/main.py), [app/attachment_formats.py](../app/attachment_formats.py), [app/attachment_rtf.py](../app/attachment_rtf.py), [app/attachment_images.py](../app/attachment_images.py), [testes/resultados/0.1.16/validation-review.json](../testes/resultados/0.1.16/validation-review.json), [docs/REA-BUSCA-IMPRESSAO.md](../docs/REA-BUSCA-IMPRESSAO.md), [docs/windows-evidence/foxit-rea/search-print-contracts.json](../docs/windows-evidence/foxit-rea/search-print-contracts.json), [docs/REA-ESTATICA-CONTINUACAO-2026-10-18.md](../docs/REA-ESTATICA-CONTINUACAO-2026-10-18.md).

Testes próprios existentes, sem nova execução nesta tabela: [test_embedded_pdf_page_is_distinct_from_host_and_model_keeps_scope](../tests/test_attachment_search.py); [test_unsupported_invalid_utf8_malformed_and_encrypted_pdf_report_omissions](../tests/test_attachment_search.py); [test_cancellation_terminates_the_actual_child_and_does_not_create_files](../tests/test_attachment_search.py); [test_attachment_scope_displays_partial_coverage_and_distinct_identity](../tests/test_search_extensions_gtk.py); [test_old_attachment_results_do_not_repopulate_another_document](../tests/test_search_extensions_gtk.py).

Relacionados aos planos dinâmicos/UI: D16.

### Contratos individuais de operações

#### `search-attachments/utf8` — Pesquisar anexo UTF-8

Estado: `current_bounded_source`; base: `current_linuxit_source`.

**Entradas:** PDF hospedeiro, consulta, flags, anexos com extensão textual e max_hits.

**Saídas:** Hits ligados a índice/nome do anexo e trechos UTF-8/BOM; omissões explícitas.

**Limites:** 100 anexos por busca, 2 MiB por conteúdo/texto e 8 MiB de payload total.

**Erros:** Bytes binários/UTF-8 inválido ou limite excedido → omissão com motivo, sem executar conteúdo.

**Estado e efeitos:** Decodifica passivamente em worker; não extrai arquivo público nem altera hospedeiro.

**Cancelamento:** invoke_attachment_search recebe cancel e timeout 120 s; geração antiga não substitui resultados novos.

Fontes/requisitos: [app/attachment_search.py — search_attachment_text](../app/attachment_search.py).

Planos relacionados da família: S12-07-1, S12-07-2. Não são aceitação completa desta operação. Nova execução neste registro: `not_run`; expectativa e observação integral Foxit: `null`.

#### `search-attachments/pdf` — Pesquisar texto de PDF anexado

Estado: `current_bounded_source`; base: `current_linuxit_source`.

**Entradas:** PDF anexado, consulta e índice de anexo identificado no hospedeiro.

**Saídas:** Hit preserva página interna do PDF anexo separada da página do hospedeiro.

**Limites:** PDF anexado até 100 páginas e limites de payload 2/8 MiB; não autentica senha própria do anexo.

**Erros:** PDF cifrado ou grande demais → omissão PDF anexo criptografado/excede páginas, não busca vazia completa.

**Estado e efeitos:** Abre bytes anexados para extração passiva, sem execução nem alteração do PDF externo.

**Cancelamento:** Worker de busca cancelável; conteúdo temporário limpo no encerramento da tarefa.

Fontes/requisitos: [app/attachment_search.py — search_attachment_text](../app/attachment_search.py).

Planos relacionados da família: S12-07-1, S12-07-2. Não são aceitação completa desta operação. Nova execução neste registro: `not_run`; expectativa e observação integral Foxit: `null`.

#### `search-attachments/formats` — Cobrir demais extratores e travessia completa

Estado: `current_bounded_source`; base: `current_linuxit_source`.

**Entradas:** Payload de anexo e extensão txt/csv/md/log/json/xml/PDF/Office/HTML/RTF ou imagem com OCR opt-in.

**Saídas:** Texto passivo e hits; formatos/partes omitidos descritos em avisos.

**Limites:** Office até 2000 entradas, 256 partes e 2 MiB expandidos; OCR até 10 imagens por busca; sem macros executadas.

**Erros:** DTD/entidade, contêiner cifrado, parte repetida ou extensão não suportada → omissão/ValueError do extrator.

**Estado e efeitos:** Pode invocar OCR explicitamente; texto Office não preserva layout nem fórmulas calculadas.

**Cancelamento:** Extrator de bytes é síncrono; worker externo tem cancel/timeout e não confirma busca concluída após interrupção.

Fontes/requisitos: [app/attachment_formats.py — extract_passive_text](../app/attachment_formats.py).

Planos relacionados da família: S12-07-1, S12-07-2. Não são aceitação completa desta operação. Nova execução neste registro: `not_run`; expectativa e observação integral Foxit: `null`.


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

- **S12-08-1** (nominal, contrato próprio atual, `passed`): dado Coleção sintética de dois documentos e índice em pasta nova. Ação: Construir índice e consultar um termo presente em um documento. Esperado: Criar/reabrir índice e localizar termo no PDF/página corretos, sem alterar fontes. Execução própria em 2026-10-21T21:24:24-03:00, revisão `ac89254204fb`, fronteira worker index-build/index-search: [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e31.json).
- **S12-08-2** (exception, contrato próprio atual, `passed`): dado Uma fonte foi alterada após indexação. Ação: Consultar sem atualização completa. Esperado: Excluir a fonte alterada e indicar que precisa atualizar o índice. Execução própria em 2026-10-21T21:24:24-03:00, revisão `ac89254204fb`, fronteira worker index-search: [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e31.json).

**Lacunas da referência Foxit**

- Formato e manutenção do índice completo, exclusões, locking, recuperação e disponibilidade Reader.

Fontes: [app/collection_index.py](../app/collection_index.py), [app/collection_window.py](../app/collection_window.py), [app/search_tasks.py](../app/search_tasks.py), [app/search_matching.py](../app/search_matching.py), [app/worker_cli.py](../app/worker_cli.py), [app/main.py](../app/main.py), [app/collection_recovery.py](../app/collection_recovery.py), [testes/resultados/0.1.16/validation-review.json](../testes/resultados/0.1.16/validation-review.json), [docs/windows-evidence/foxit-rea/index-interface.json](../docs/windows-evidence/foxit-rea/index-interface.json), [docs/FOXIT-REA.md](../docs/FOXIT-REA.md), [docs/REA-ESTATICA-BUSCA-IMPRESSAO-2026-10-18.md](../docs/REA-ESTATICA-BUSCA-IMPRESSAO-2026-10-18.md), [docs/REA-ESTATICA-CONTINUACAO-2026-10-18.md](../docs/REA-ESTATICA-CONTINUACAO-2026-10-18.md).

Testes próprios existentes, sem nova execução nesta tabela: [test_build_reopen_worker_and_query_preserve_sources_and_real_pages](../tests/test_collection_index.py); [test_changed_missing_sources_are_excluded_until_explicit_rebuild](../tests/test_collection_index.py); [test_update_failure_preserves_old_index_and_removes_temporary](../tests/test_collection_index.py); [test_collection_build_query_and_open_result_on_its_actual_page](../tests/test_search_extensions_gtk.py); [test_collection_changed_result_is_refused_before_opening](../tests/test_search_extensions_gtk.py); [test_closing_collection_terminates_pending_worker_without_callbacks](../tests/test_search_extensions_gtk.py).

### Contratos individuais de operações

#### `search-index/build` — Construir snapshot de coleção

Estado: `current_bounded_source`; base: `current_linuxit_source`.

**Entradas:** Lista explícita de 1–100 PDFs e destino .linuxit-index.json, expected_index_sha256 quando atualizar.

**Saídas:** Snapshot com schema, data, hashes de fontes, texto por página e body_sha256.

**Limites:** 1000 páginas, 64 MiB/PDF, 256 MiB fontes, 16 MiB texto e 64 MiB índice; fontes cifradas recusadas.

**Erros:** Fonte repetida/mudada, índice alterado ou lock presente → erro sem substituir snapshot anterior.

**Estado e efeitos:** Adquire trava local, cria backup/temporário e publica índice atômico conferido.

**Cancelamento:** Worker cancelável via invoke_collection; trava/temporários são tratados ao sair; não remover trava de outro processo automaticamente.

Fontes/requisitos: [app/collection_index.py — build_index](../app/collection_index.py).

Planos relacionados da família: S12-08-1, S12-08-2. Não são aceitação completa desta operação. Nova execução neste registro: `not_run`; expectativa e observação integral Foxit: `null`.

#### `search-index/query` — Consultar índice e excluir fonte alterada

Estado: `current_bounded_source`; base: `current_linuxit_source`.

**Entradas:** Índice próprio válido, consulta, flags e limite inteiro de 1–5000.

**Saídas:** Hits com caminho, página, snippet, hash; lista stale e limit_reached.

**Limites:** Consulta não reconstrói índice; fonte ausente/alterada é excluída até rebuild explícito.

**Erros:** Schema/hash inválido ou índice mudado durante consulta → erro; fonte stale vira registro explícito.

**Estado e efeitos:** Somente leitura de índice/fontes e lista de resultados.

**Cancelamento:** Consulta em worker aceita cancel; não publicar relatório final de geração antiga.

Fontes/requisitos: [app/collection_index.py — search_index](../app/collection_index.py).

Planos relacionados da família: S12-08-1, S12-08-2. Não são aceitação completa desta operação. Nova execução neste registro: `not_run`; expectativa e observação integral Foxit: `null`.

#### `search-index/maintenance` — Manter índice completo e recuperação

Estado: `current_bounded_source`; base: `current_linuxit_source`.

**Entradas:** Snapshot atual, lista de documentos, hash esperado e escolha rebuild/backup/restore/revisar trava.

**Saídas:** Snapshot novo conferido ou relatório de backup/restauração/trava local.

**Limites:** Operações sobre formato Linuxit; trava abandonada exige revisão PID, não prova de locking distribuído/NFS.

**Erros:** Hash diferente/lock de processo ativo → recusa; backup inválido

**Estado e efeitos:** Pode criar .lock/backup e substituir exclusivamente índice próprio após validação.

**Cancelamento:** Cancelar confirmação não inicia manutenção; worker cancelável; publicação já concluída não é desfeita automaticamente.

Fontes/requisitos: [app/collection_index.py — build_index](../app/collection_index.py), [app/collection_window.py — CollectionWindow._maintain](../app/collection_window.py).

Planos relacionados da família: S12-08-1, S12-08-2. Não são aceitação completa desta operação. Nova execução neste registro: `not_run`; expectativa e observação integral Foxit: `null`.


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

- **S12-09-1** (nominal, contrato próprio atual, `passed`): dado Corpus sintético com duas palavras separadas por distâncias conhecidas. Ação: Executar proximidade com duas distâncias explícitas. Esperado: Duas consultas com distâncias diferentes produzem hits conforme distância total/ordem documentadas. Execução própria em 2026-10-21T21:24:25-03:00, revisão `ac89254204fb`, fronteira search_engine.TextSearchIndex: [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e31.json).
- **S12-09-2** (exception, contrato próprio atual, `passed`): dado Consulta com coringa/operador cuja sintaxe não foi implementada. Ação: Executar esse modo. Esperado: Recusar sintaxe/operador não suportado sem trocar silenciosamente para literal. Execução própria em 2026-10-21T21:24:25-03:00, revisão `ac89254204fb`, fronteira search_engine.TextSearchIndex: [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e31.json).

**Lacunas da referência Foxit**

- Stemming por idioma, distância/proximidade, escaping, expansão e combinações com índice.

Fontes: [app/search_matching.py](../app/search_matching.py), [app/search_engine.py](../app/search_engine.py), [app/attachment_search.py](../app/attachment_search.py), [app/collection_index.py](../app/collection_index.py), [app/main.py](../app/main.py), [app/collection_window.py](../app/collection_window.py), [docs/proveniencia-snowball.json](../docs/proveniencia-snowball.json), [app/search_languages.py](../app/search_languages.py), [testes/resultados/0.1.16/validation-review.json](../testes/resultados/0.1.16/validation-review.json), [docs/REA-BUSCA-IMPRESSAO.md](../docs/REA-BUSCA-IMPRESSAO.md), [docs/windows-evidence/foxit-rea/search-print-contracts.json](../docs/windows-evidence/foxit-rea/search-print-contracts.json), [docs/ETAPA-11.md](../docs/ETAPA-11.md), [docs/REA-ESTATICA-BUSCA-IMPRESSAO-2026-10-18.md](../docs/REA-ESTATICA-BUSCA-IMPRESSAO-2026-10-18.md), [docs/REA-ESTATICA-CONTINUACAO-2026-10-18.md](../docs/REA-ESTATICA-CONTINUACAO-2026-10-18.md).

Testes próprios existentes, sem nova execução nesta tabela: [test_proximity_uses_total_intervening_words_and_query_order](../tests/test_search_modes.py); [test_invalid_syntax_distance_and_expansion_are_rejected](../tests/test_search_modes.py); [test_page_geometry_keeps_owner_rectangles_for_both_modes](../tests/test_search_modes.py); [test_mode_controls_geometry_distance_and_bad_syntax](../tests/test_search_extensions_gtk.py).

Relacionados aos planos dinâmicos/UI: UI07.

### Contratos individuais de operações

#### `search-language/wildcard` — Pesquisar coringas por palavra

Estado: `current_bounded_source`; base: `current_linuxit_source`.

**Entradas:** Modo wildcard e um token Unicode contendo * ou ?.

**Saídas:** Spans de palavras completas que casam com o glob próprio.

**Limites:** Até 64 caracteres, 8 coringas, ao menos letra/número; token de texto até 4096; não é regex.

**Erros:** Padrão só coringas, pontuação indevida ou token grande → ValueError, sem fallback literal silencioso.

**Estado e efeitos:** Cálculo em memória sobre texto; não altera índice/disco.

**Cancelamento:** Gerador síncrono; busca externa consulta cancel entre páginas e lotes.

Fontes/requisitos: [app/search_matching.py — query_spans](../app/search_matching.py).

Planos relacionados da família: S12-09-1, S12-09-2. Não são aceitação completa desta operação. Nova execução neste registro: `not_run`; expectativa e observação integral Foxit: `null`.

#### `search-language/proximity` — Pesquisar proximidade ordenada

Estado: `current_bounded_source`; base: `current_linuxit_source`.

**Entradas:** 2–8 palavras em ordem e proximidade inteira 0–50.

**Saídas:** Span cobre primeira à última palavra quando intervalo total satisfaz limite.

**Limites:** Mantém ordem desejada e não cruza arbitrariamente limites da representação textual da página.

**Erros:** Uma palavra, distância negativa/bool ou pontuação de regex → ValueError.

**Estado e efeitos:** Cálculo puro; não aprende regras nem reescreve documento.

**Cancelamento:** Interrupção controlada pelo chamador da página; não possui subprocesso próprio.

Fontes/requisitos: [app/search_matching.py — query_spans](../app/search_matching.py).

Planos relacionados da família: S12-09-1, S12-09-2. Não são aceitação completa desta operação. Nova execução neste registro: `not_run`; expectativa e observação integral Foxit: `null`.

#### `search-language/stemming` — Aplicar stemming por idioma

Estado: `current_bounded_source`; base: `current_linuxit_source`.

**Entradas:** Modo stem-<código> de idioma suportado e 1–8 palavras Unicode.

**Saídas:** Spans de sequências com radicais Snowball iguais em ordem.

**Limites:** 36 idiomas de search_languages; token até 4096; stemming não é tradução nem semântica universal.

**Erros:** Idioma/helper indisponível ou consulta fora da gramática → erro, não aproximação ao algoritmo Foxit.

**Estado e efeitos:** Carrega stemmer local; não envia texto à nuvem.

**Cancelamento:** Busca externa cancelável; cálculo do stemmer não anuncia SLA de interrupção por token.

Fontes/requisitos: [app/search_matching.py — query_spans](../app/search_matching.py), [app/search_languages.py — python_stemmer](../app/search_languages.py).

Planos relacionados da família: S12-09-1, S12-09-2. Não são aceitação completa desta operação. Nova execução neste registro: `not_run`; expectativa e observação integral Foxit: `null`.


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

- **S12-10-1** (nominal, contrato próprio atual, `passed`): dado PDF sintético e retângulo contendo uma palavra conhecida. Ação: Selecionar e copiar. Esperado: Clipboard contém a palavra selecionada; a seleção acompanha a transformação da imagem. Execução própria em 2026-10-21T21:24:25-03:00, revisão `ac89254204fb`, fronteira PDFWindow _finish_text_selection + clipboard: [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e31.json).
- **S12-10-2** (exception, contrato próprio atual, `passed`): dado Retângulo sobre região sem texto. Ação: Concluir seleção de texto. Esperado: Status informa ausência de texto; nenhum conteúdo fictício é produzido. Execução própria em 2026-10-21T21:24:27-03:00, revisão `ac89254204fb`, fronteira PDFWindow _finish_text_selection: [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e31.json).

**Lacunas da referência Foxit**

- Ordem lógica, texto bidirecional, permissões de cópia, snapping e coordenadas de todos os modos do original.

Fontes: [app/main.py](../app/main.py), [app/rendering.py](../app/rendering.py), [app/text_selection.py](../app/text_selection.py), [app/character_selection.py](../app/character_selection.py), [app/character_extraction.py](../app/character_extraction.py), [testes/resultados/0.1.16/validation-review.json](../testes/resultados/0.1.16/validation-review.json), [docs/FOXIT-REA.md](../docs/FOXIT-REA.md).

Testes próprios existentes, sem nova execução nesta tabela: [test_search_navigation_selection_and_rotation](../tests/test_gui.py); [test_intrinsic_rotation_and_cropbox_match_text_geometry](../tests/test_regressions.py).

### Contratos individuais de operações

#### `selection/text` — Selecionar e copiar palavras por área

Estado: `current_bounded_source`; base: `current_linuxit_source`.

**Entradas:** Arraste na página exibida e transformação tela↔PDF atual, caixas de palavras da sessão.

**Saídas:** Texto selecionado/copiar conforme região e geometria disponível.

**Limites:** Respeita permissão de extração; ordem extraída depende da representação textual do PDF.

**Erros:** Sem mapa/permissão/página → seleção não deve copiar texto não autorizado ou inventado.

**Estado e efeitos:** Seleção e clipboard podem mudar; original permanece intacto.

**Cancelamento:** Soltar conclui seleção local; trocar documento descarta mapas e seleção pendentes.

Fontes/requisitos: [app/main.py — PDFWindow._finish_text_selection](../app/main.py).

Planos relacionados da família: S12-10-1, S12-10-2. Não são aceitação completa desta operação. Nova execução neste registro: `not_run`; expectativa e observação integral Foxit: `null`.

#### `selection/snapshot` — Copiar snapshot de região

Estado: `current_bounded_source`; base: `current_linuxit_source`.

**Entradas:** Retângulo positivo na página exibida e imagem renderizada atual.

**Saídas:** Imagem recortada para clipboard/uso explícito do usuário.

**Limites:** Snapshot não contém necessariamente texto/estrutura; deve respeitar permissão de cópia.

**Erros:** Área fora da página, vazia ou documento ausente → não publicar imagem válida fictícia.

**Estado e efeitos:** Pode mudar clipboard com pixels; não escreve PDF nem exporta automaticamente.

**Cancelamento:** Ação local de recorte; fechar documento limpa seleção; não há fila remota.

Fontes/requisitos: [app/main.py — PDFWindow._finish_snapshot](../app/main.py).

Planos relacionados da família: S12-10-1, S12-10-2. Não são aceitação completa desta operação. Nova execução neste registro: `not_run`; expectativa e observação integral Foxit: `null`.

#### `selection/bidi` — Garantir ordem lógica e texto bidirecional

Estado: `current_bounded_source`; base: `current_linuxit_source`.

**Entradas:** Texto Unicode, caixas reais, carets Pango e offsets âncora/foco.

**Saídas:** Intervalo textual e retângulos/caret, com movimentos visuais por linha.

**Limites:** Até 100000 caracteres; limites de grafema e bidi nativos quando disponíveis; fallback delimitado.

**Erros:** Offset fora do texto, coordenada não finita ou mapa acima do limite → ValueError.

**Estado e efeitos:** Estado de seleção somente em memória; não reordena conteúdo salvo.

**Cancelamento:** Transformações síncronas; carregamento do mapa é invalidado ao trocar página/documento.

Fontes/requisitos: [app/character_selection.py — select_range](../app/character_selection.py).

Planos relacionados da família: S12-10-1, S12-10-2. Não são aceitação completa desta operação. Nova execução neste registro: `not_run`; expectativa e observação integral Foxit: `null`.


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

- **S12-11-1** (nominal, contrato próprio atual, `passed`): dado Fixture e destino Salvar como PDF. Ação: Preparar saída e reabri-la. Esperado: Arquivo reabre e preserva o plano escolhido; sucesso de geração não é prova de impressão física. Execução própria em 2026-10-21T21:24:28-03:00, revisão `ac89254204fb`, fronteira worker prepare-print: [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e31.json).
- **S12-11-2** (exception, contrato próprio atual, `passed`): dado Comando lp indisponível. Ação: Solicitar envio ao CUPS. Esperado: RuntimeError explícito; nenhum sucesso de envio é reportado. Execução própria em 2026-10-21T21:24:29-03:00, revisão `ac89254204fb`, fronteira cups_backend.print_file: [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e31.json).

**Lacunas da referência Foxit**

- Predefinições, margens, fontes, flags, spooler físico e estados completos do original.

**Observação parcial preservada do original:** Duas novas saídas virtuais13.pdf/14.pdf; fechamento normal e consulta posterior sem Foxit/atualizador/splwow64, fila vazia. Espera histórica não reproduzida nem explicada; impressão física e fluxo completo abertos.

Evidências: [docs/VM-FOXIT-2026-10-18.md](../docs/VM-FOXIT-2026-10-18.md), [docs/P03-BUSCA-IMPRESSAO-2026-10-19.md](../docs/P03-BUSCA-IMPRESSAO-2026-10-19.md), [docs/P03-CANCELAMENTO-MOSAICO-2026-10-19.md](../docs/P03-CANCELAMENTO-MOSAICO-2026-10-19.md).

Fontes: [app/print_window.py](../app/print_window.py), [app/worker_cli.py](../app/worker_cli.py), [app/cups_backend.py](../app/cups_backend.py), [app/windows_print.py](../app/windows_print.py), [app/print_tasks.py](../app/print_tasks.py), [app/print_queue.py](../app/print_queue.py), [testes/resultados/0.1.16/validation-review.json](../testes/resultados/0.1.16/validation-review.json), [docs/REA-IMPRESSAO-CONSUMIDORES.md](../docs/REA-IMPRESSAO-CONSUMIDORES.md), [docs/windows-evidence/foxit-rea/windows-print-followup-contracts.json](../docs/windows-evidence/foxit-rea/windows-print-followup-contracts.json), [docs/AVANCO-SEM-VM.md](../docs/AVANCO-SEM-VM.md), [docs/REA-ESTATICA-BUSCA-IMPRESSAO-2026-10-18.md](../docs/REA-ESTATICA-BUSCA-IMPRESSAO-2026-10-18.md), [docs/REA-ESTATICA-CONTINUACAO-2026-10-18.md](../docs/REA-ESTATICA-CONTINUACAO-2026-10-18.md), [docs/VM-FOXIT-2026-10-18.md](../docs/VM-FOXIT-2026-10-18.md), [docs/P03-BUSCA-IMPRESSAO-2026-10-19.md](../docs/P03-BUSCA-IMPRESSAO-2026-10-19.md), [docs/P03-CANCELAMENTO-MOSAICO-2026-10-19.md](../docs/P03-CANCELAMENTO-MOSAICO-2026-10-19.md).

Testes próprios existentes, sem nova execução nesta tabela: [test_booklet_preview_sides_binding_and_submit](../tests/test_gui.py); [test_manual_booklet_sides_are_not_duplex](../tests/test_regressions.py).

Relacionados aos planos dinâmicos/UI: D17, UI02, UI05.

### Contratos individuais de operações

#### `printing/preview` — Preparar prévia e opções de impressão

Estado: `current_bounded_source`; base: `current_linuxit_source`.

**Entradas:** Documento da sessão e job com intervalo, papel, orientação, escala/imposição e camadas.

**Saídas:** Prévia das folhas planejadas pelo mesmo backend de preparação próprio.

**Limites:** Prévia visual não certifica driver, papel físico nem spooler; política /P aplicada à sessão.

**Erros:** Intervalo/mode inválido ou preparação falha → erro na prévia, sem enviar trabalho.

**Estado e efeitos:** Cria PDF/rasters temporários de prévia; não altera fonte.

**Cancelamento:** Mudar opções cancela/ignora prévias antigas; fechar janela libera temporários após leitores.

Fontes/requisitos: [app/print_window.py — PrintWindow._draw_preview](../app/print_window.py).

Planos relacionados da família: S12-11-1, S12-11-2. Não são aceitação completa desta operação. Nova execução neste registro: `not_run`; expectativa e observação integral Foxit: `null`.

#### `printing/submit` — Enviar arquivo ao backend Linux

Estado: `current_bounded_source`; base: `current_linuxit_source`.

**Entradas:** PDF preparado, nome de impressora e job com opções aceitas pelo CUPS.

**Saídas:** Recibo do lp com identificação do trabalho quando reconhecida.

**Limites:** Requer cups-client e impressora selecionada; cancelamento posterior só usa ID validado do próprio recibo.

**Erros:** lp ausente, nenhuma impressora ou retorno não zero → RuntimeError com diagnóstico, sem declarar impressão concluída.

**Estado e efeitos:** Envia trabalho externo à fila, que pode persistir após fechar janela.

**Cancelamento:** Antes do envio pode cancelar preparação; depois exige cancel_job e confirmação da fila, sem garantir papel não saiu.

Fontes/requisitos: [app/cups_backend.py — print_file](../app/cups_backend.py).

Planos relacionados da família: S12-11-1, S12-11-2. Não são aceitação completa desta operação. Nova execução neste registro: `not_run`; expectativa e observação integral Foxit: `null`.

#### `printing/physical` — Imprimir e cancelar em dispositivo físico

Estado: `pending_environment_or_reference`; base: `proposed_independent_requirement`.

**Entradas:** Impressora e papel reais, régua, job identificado, driver e configuração duplex/escala.

**Saídas:** Plano de aceitação física com medidas, frente/verso, fila e cancelamento observados.

**Limites:** Ainda depende de equipamentos; CUPS virtual não fecha este contrato físico.

**Erros:** Papel/driver divergente, atolamento ou cancelamento não confirmado → registrar falha/inconclusivo, sem afirmar conformidade.

**Estado e efeitos:** Pode consumir papel/tinta e alterar fila; executar só campanha específica.

**Cancelamento:** Solicitar cancelamento do ID da campanha e conferir fila/dispositivo; requisito proposto, não medição já executada.

Fontes/requisitos: [docs/O-QUE-FAZER-AGORA-2026-10-22.md](../docs/O-QUE-FAZER-AGORA-2026-10-22.md).

Planos relacionados da família: S12-11-1, S12-11-2. Não são aceitação completa desta operação. Nova execução neste registro: `not_run`; expectativa e observação integral Foxit: `null`.

#### `printing/shutdown` — Encerrar após impressão sem processo preso

Estado: `pending_environment_or_reference`; base: `proposed_independent_requirement`.

**Entradas:** Job concluído/cancelado e sequência de fechamento com observador de processos autorizado.

**Saídas:** Evidências de janela, processos residuais e fila após fechamento normal.

**Limites:** Espera splwow64 previamente vista não tem causa definitiva; não atribuir falha a Foxit por VM parada.

**Erros:** Processo residual ou relógio congelado → preservar evidência/inconclusivo e interromper entradas.

**Estado e efeitos:** Não requer kill automático; investigação do original só em contenção e campanha autorizada.

**Cancelamento:** Ao congelar, salvar checkpoint e avisar; encerramento residual segue decisão D06 e contexto da campanha, nunca dedução automática.

Fontes/requisitos: [docs/VM-SENHA-E-PARADA-2026-10-18.md](../docs/VM-SENHA-E-PARADA-2026-10-18.md).

Planos relacionados da família: S12-11-1, S12-11-2. Não são aceitação completa desta operação. Nova execução neste registro: `not_run`; expectativa e observação integral Foxit: `null`.


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

- **S12-12-1** (nominal, contrato próprio atual, `passed`): dado PDF sintético de oito páginas. Ação: Gerar livreto em ambos os lados e reabrir. Esperado: Quatro faces; ordem das duplas própria verificável, sem alterar o original. Execução própria em 2026-10-21T21:24:29-03:00, revisão `ac89254204fb`, fronteira worker prepare-print (booklet): [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e31.json).
- **S12-12-2** (exception, contrato próprio atual, `passed`): dado pages_per_sheet=4.5. Ação: Preparar modo multiple. Esperado: ValueError, sem aceitar silenciosamente uma quantidade inteira diferente. Execução própria em 2026-10-21T21:24:29-03:00, revisão `ac89254204fb`, fronteira imposition.prepare_output: [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e31.json).

**Lacunas da referência Foxit**

- Geometria completa, rotações, margens e ordenação de todas as combinações no Foxit.

**Observação parcial preservada do original:** N-up A4 retrato2x2/horizontal/margem4mm gerou2 páginas, sequência1-4/5-8 igual em C18-D18-nup. Mosaico200%/sobreposição5mm sem marcas/legendas gerou48 páginas, todas renderizadas. Livreto5mm/medianiz3mm, geometria e combinações completas ainda abertos.

Evidências: [docs/VM-FOXIT-2026-10-18.md](../docs/VM-FOXIT-2026-10-18.md), [docs/P03-BUSCA-IMPRESSAO-2026-10-19.md](../docs/P03-BUSCA-IMPRESSAO-2026-10-19.md), [docs/P03-CANCELAMENTO-MOSAICO-2026-10-19.md](../docs/P03-CANCELAMENTO-MOSAICO-2026-10-19.md).

Fontes: [app/imposition.py](../app/imposition.py), [app/worker_cli.py](../app/worker_cli.py), [testes/resultados/0.1.16/validation-review.json](../testes/resultados/0.1.16/validation-review.json), [docs/REA-IMPRESSAO-CONSUMIDORES.md](../docs/REA-IMPRESSAO-CONSUMIDORES.md), [docs/windows-evidence/foxit-rea/windows-print-followup-contracts.json](../docs/windows-evidence/foxit-rea/windows-print-followup-contracts.json), [docs/AVANCO-SEM-VM.md](../docs/AVANCO-SEM-VM.md), [docs/REA-ESTATICA-BUSCA-IMPRESSAO-2026-10-18.md](../docs/REA-ESTATICA-BUSCA-IMPRESSAO-2026-10-18.md), [docs/REA-ESTATICA-CONTINUACAO-2026-10-18.md](../docs/REA-ESTATICA-CONTINUACAO-2026-10-18.md), [docs/VM-FOXIT-2026-10-18.md](../docs/VM-FOXIT-2026-10-18.md), [docs/P03-BUSCA-IMPRESSAO-2026-10-19.md](../docs/P03-BUSCA-IMPRESSAO-2026-10-19.md), [docs/P03-CANCELAMENTO-MOSAICO-2026-10-19.md](../docs/P03-CANCELAMENTO-MOSAICO-2026-10-19.md).

Testes próprios existentes, sem nova execução nesta tabela: [test_booklet_generated_sides_and_binding](../tests/test_regressions.py); [test_nup_worker_rejects_fractional_count](../tests/test_regressions.py); [test_worker_prepares_nup_and_poster](../tests/test_regressions.py); [test_actual_size_centers_the_visible_crop_not_the_media_origin](../tests/test_imposition_cropbox.py); [test_intrinsic_rotation_keeps_shifted_crop_aligned](../tests/test_imposition_cropbox.py); [test_inputs_and_in_memory_page_geometry_are_preserved](../tests/test_imposition_cropbox.py); [test_poster_single_sheet_and_tiles_keep_crop_placement_without_marks](../tests/test_imposition_cropbox.py).

Relacionados aos planos dinâmicos/UI: D18.

### Contratos individuais de operações

#### `imposition/booklet` — Compor livreto

Estado: `current_bounded_source`; base: `current_linuxit_source`.

**Entradas:** PDF, seleção, papel, binding left/right e sides both/front/back; margens de segurança/lombada.

**Saídas:** Folhas com pares de livreto e preenchimento branco quando necessário.

**Limites:** Frente/verso manual é diferente de duplex do driver; CropBox/rotação normalizados na cópia.

**Erros:** Lados desconhecidos, geometria inválida ou permissão de impressão negada → ValueError/PermissionError.

**Estado e efeitos:** Gera PDF imposto; não muda stream/caixas da fonte em memória.

**Cancelamento:** Preparação no worker cancelável; uma folha já enviada ao CUPS exige cancelamento separado.

Fontes/requisitos: [app/imposition.py — create_booklet](../app/imposition.py).

Planos relacionados da família: S12-12-1, S12-12-2. Não são aceitação completa desta operação. Nova execução neste registro: `not_run`; expectativa e observação integral Foxit: `null`.

#### `imposition/nup` — Compor N-up

Estado: `current_bounded_source`; base: `current_linuxit_source`.

**Entradas:** PDF, intervalo, ordem, papel/orientação, pages_per_sheet, layout e margem.

**Saídas:** PDF com páginas escaladas em células corretas preservando recorte próprio.

**Limites:** Grades aceitas 1/2/4/6/9/16; margem em mm e coordenadas em pontos.

**Erros:** pages_per_sheet fora da lista ou CropBox sem área → ValueError antes do envio.

**Estado e efeitos:** Gera cópia temporária/saída própria, sem modificar source reader.

**Cancelamento:** Cancelamento do worker interrompe preparação; não revoga PDF já publicado/enviado.

Fontes/requisitos: [app/imposition.py — create_nup](../app/imposition.py).

Planos relacionados da família: S12-12-1, S12-12-2. Não são aceitação completa desta operação. Nova execução neste registro: `not_run`; expectativa e observação integral Foxit: `null`.

#### `imposition/poster` — Compor mosaico

Estado: `current_bounded_source`; base: `current_linuxit_source`.

**Entradas:** Página, papel/área imprimível, escala, sobreposição, margens, marcas e rótulos.

**Saídas:** Tiles em PDF, com marcas/legendas vetoriais quando Cairo disponível.

**Limites:** Até 100 folhas por página e 300 no trabalho; geometria da impressora limita área útil.

**Erros:** Sobreposição/escala exigindo mais folhas que limite → ValueError orienta reduzir; não truncar pôster silenciosamente.

**Estado e efeitos:** Escreve PDF de mosaico; sem alteração da fonte.

**Cancelamento:** Worker/geração de prévia canceláveis; envio e cancelamento da fila têm recibos separados.

Fontes/requisitos: [app/imposition.py — create_poster](../app/imposition.py).

Planos relacionados da família: S12-12-1, S12-12-2. Não são aceitação completa desta operação. Nova execução neste registro: `not_run`; expectativa e observação integral Foxit: `null`.


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

- **S12-13-1** (nominal, contrato próprio atual, `passed`): dado Fixture com dois marcadores. Ação: Inspecionar o painel. Esperado: Dois títulos, nível registrado e destino local conhecido ou null; nenhuma escrita no PDF. Execução própria em 2026-10-21T21:24:29-03:00, revisão `ac89254204fb`, fronteira worker panels: [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e31.json).
- **S12-13-2** (exception, contrato próprio atual, `passed`): dado Marcador sem página local. Ação: Exibir seu destino. Esperado: Não atribuir a primeira página por padrão. Execução própria em 2026-10-21T21:24:29-03:00, revisão `ac89254204fb`, fronteira worker panels: [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e31.json).

**Lacunas da referência Foxit**

- Disponibilidade Reader dos diálogos, movimento hierárquico, undo/redo e persistência.

Fontes: [app/pdf_panels.py](../app/pdf_panels.py), [app/pdf_changes.py](../app/pdf_changes.py), [app/edit_tasks.py](../app/edit_tasks.py), [app/worker_cli.py](../app/worker_cli.py), [app/main.py](../app/main.py), [docs/SEGURANCA-ACESSIBILIDADE.md](../docs/SEGURANCA-ACESSIBILIDADE.md), [app/local_files.py](../app/local_files.py), [app/folder_dialogs.py](../app/folder_dialogs.py), [docs/PASTAS-SINCRONIZADAS.md](../docs/PASTAS-SINCRONIZADAS.md), [app/pdf_form_controls.py](../app/pdf_form_controls.py), [app/edit_history.py](../app/edit_history.py), [app/edit_dialogs.py](../app/edit_dialogs.py), [app/edit_window.py](../app/edit_window.py), [docs/EDICAO-COM-HISTORICO.md](../docs/EDICAO-COM-HISTORICO.md), [testes/resultados/0.1.10/validation-review.json](../testes/resultados/0.1.10/validation-review.json), [testes/resultados/0.1.16/validation-review.json](../testes/resultados/0.1.16/validation-review.json), [docs/FOXIT-REA.md](../docs/FOXIT-REA.md), [docs/ETAPA-11.md](../docs/ETAPA-11.md).

Testes próprios existentes, sem nova execução nesta tabela: [test_bookmark_without_local_page_is_not_given_a_fake_destination](../tests/test_search_scopes.py); [test_combined_copy_preserves_source_metadata_attachment_and_previous_objects](../tests/test_pdf_changes.py); [test_encryption_signature_permissions_xfa_and_portfolio_are_explicitly_unsupported](../tests/test_pdf_changes.py); [test_real_dialogs_and_worker_create_bookmark_note_and_form_copies](../tests/test_copy_edit_gtk.py); [test_reopening_same_document_during_dialog_blocks_stale_save](../tests/test_copy_edit_gtk.py); [test_existing_destination_is_preserved_and_busy_state_is_released](../tests/test_copy_edit_gtk.py); [test_combined_edits_preserve_tree_destinations_geometry_and_source](../tests/test_extended_edits.py); [test_final_name_is_absent_while_real_copy_is_in_progress](../tests/test_sync_folders.py); [test_save_copy_uses_worker_preserves_original_and_only_confirms_local_save](../tests/test_sync_folders_gtk.py); [test_info_distinguishes_checkbox_radio_choice_combo_and_multiselect](../tests/test_advanced_edits.py); [test_checkbox_sets_and_clears_value_and_visible_appearance](../tests/test_advanced_edits.py); [test_radio_activates_only_the_selected_widget_and_can_clear](../tests/test_advanced_edits.py); [test_radio_no_toggle_off_is_enforced](../tests/test_advanced_edits.py); [test_single_and_combo_values_indices_and_generated_appearances_roundtrip](../tests/test_advanced_edits.py); [test_multiselect_uses_export_values_and_canonical_indices](../tests/test_advanced_edits.py); [test_choice_selection_can_be_cleared](../tests/test_advanced_edits.py); [test_invalid_values_do_not_publish_partial_batch](../tests/test_advanced_edits.py); [test_read_only_and_unsupported_button_appearance_are_explicit](../tests/test_advanced_edits.py); [test_editable_combo_and_duplicate_exports_are_rejected](../tests/test_advanced_edits.py); [test_inherited_checkbox_flags_and_type_are_respected](../tests/test_advanced_edits.py); [test_checkbox_widget_absent_from_pages_is_unsupported](../tests/test_advanced_edits.py); [test_closed_outline_counts_remain_closed_after_move](../tests/test_advanced_edits.py); [test_move_preserves_subtree_destinations_and_sibling_links](../tests/test_advanced_edits.py); [test_move_child_to_root_and_reorder_same_parent](../tests/test_advanced_edits.py); [test_delete_bookmark_removes_subtree_and_last_root](../tests/test_advanced_edits.py); [test_move_into_descendant_invalid_positions_and_boolean_paths_are_refused](../tests/test_advanced_edits.py); [test_highlight_and_rectangle_roundtrip_geometry_print_flags_and_text](../tests/test_advanced_edits.py); [test_delete_supported_annotation_preserves_widgets_and_other_pages](../tests/test_advanced_edits.py); [test_locked_notes_widgets_and_replies_are_not_deleted](../tests/test_advanced_edits.py); [test_invalid_annotation_geometry_and_extra_parameters_are_rejected](../tests/test_advanced_edits.py); [test_undo_redo_rebuild_actual_pdfs_and_save_current_cursor_only](../tests/test_edit_history.py); [test_undo_all_restores_base_and_disables_save_until_redone](../tests/test_edit_history.py); [test_new_branch_discards_redo_but_invalid_branch_preserves_it](../tests/test_edit_history.py); [test_operation_values_are_defensively_copied](../tests/test_edit_history.py); [test_changed_original_blocks_add_undo_redo_and_save](../tests/test_edit_history.py); [test_existing_destination_is_not_overwritten_and_draft_survives](../tests/test_edit_history.py); [test_closed_session_refuses_work_and_removes_private_previews](../tests/test_edit_history.py); [test_pre_cancelled_session_does_not_start_worker](../tests/test_edit_history.py); [test_buttons_undo_redo_save_selected_history_and_preserve_prior_copy](../tests/test_edit_draft_gtk.py); [test_real_form_dialog_checkbox_radio_list_and_multiselect](../tests/test_edit_draft_gtk.py); [test_real_move_and_delete_bookmark_dialogs_use_updated_paths](../tests/test_edit_draft_gtk.py); [test_real_area_annotation_dialog_and_delete_keep_other_annotations](../tests/test_edit_draft_gtk.py); [test_failed_operation_and_existing_destination_keep_history_usable](../tests/test_edit_draft_gtk.py); [test_cancel_dialog_and_reopen_parent_close_draft_without_publishing](../tests/test_edit_draft_gtk.py); [test_cancelling_save_and_repeated_clicks_do_not_duplicate_writes](../tests/test_edit_draft_gtk.py); [test_saved_form_and_highlight_render_with_poppler](../tests/test_edit_draft_gtk.py).

Relacionados aos planos dinâmicos/UI: D07, UI09, UI10.

### Contratos individuais de operações

#### `bookmarks-edit/create` — Criar marcador em cópia

Estado: `current_bounded_source`; base: `current_linuxit_source`.

**Entradas:** kind add-bookmark, title não vazio e page inteiro válido, identidade/hash e destino novo.

**Saídas:** Novo nó de marcador com título e destino local na cópia.

**Limites:** Título até 4096 bytes; árvore até 2048 entradas e 32 níveis no inspetor.

**Erros:** Título vazio/página fora da faixa → ValueError, sem arquivo final parcial.

**Estado e efeitos:** Adiciona operação ao rascunho; salvar copia árvore sem alterar fonte.

**Cancelamento:** Desfazer antes de salvar remove criação; cópia salva permanece independente do histórico.

Fontes/requisitos: [app/pdf_changes.py — _apply](../app/pdf_changes.py).

Planos relacionados da família: S12-13-1, S12-13-2. Não são aceitação completa desta operação. Nova execução neste registro: `not_run`; expectativa e observação integral Foxit: `null`.

#### `bookmarks-edit/rename` — Renomear marcador

Estado: `current_bounded_source`; base: `current_linuxit_source`.

**Entradas:** Caminho ordinal do nó e title novo não vazio.

**Saídas:** Mesmo nó/destino/filhos com título atualizado.

**Limites:** Caminho tem 1–32 índices de 0–2047; título até 4096 bytes.

**Erros:** Caminho não encontrado ou título inválido → erro sem renomear outro nó por coincidência.

**Estado e efeitos:** Rascunho e cópia própria apenas; destinos preservados.

**Cancelamento:** Undo/redo por reconstrução do rascunho; cancelar diálogo não cria operação.

Fontes/requisitos: [app/pdf_changes.py — _apply](../app/pdf_changes.py).

Planos relacionados da família: S12-13-1, S12-13-2. Não são aceitação completa desta operação. Nova execução neste registro: `not_run`; expectativa e observação integral Foxit: `null`.

#### `bookmarks-edit/move` — Mover subárvore de marcadores

Estado: `current_bounded_source`; base: `current_linuxit_source`.

**Entradas:** path de origem, parent de destino (raiz=[]), position medida após retirada.

**Saídas:** Nó e subárvore movidos com destinos e contagens de irmãos coerentes.

**Limites:** Proibido mover para própria subárvore; profundidade 32 e posição dentro do pai atual.

**Erros:** Ciclo/posição fora da faixa/pai ausente → ValueError sem árvore parcial publicada.

**Estado e efeitos:** Reestrutura cópia/rascunho; fonte não muda.

**Cancelamento:** Undo reconstrói árvore anterior; trocar documento fecha sessão de edição antiga.

Fontes/requisitos: [app/pdf_changes.py — _change_outline](../app/pdf_changes.py).

Planos relacionados da família: S12-13-1, S12-13-2. Não são aceitação completa desta operação. Nova execução neste registro: `not_run`; expectativa e observação integral Foxit: `null`.

#### `bookmarks-edit/delete` — Excluir subárvore em cópia

Estado: `current_bounded_source`; base: `current_linuxit_source`.

**Entradas:** Caminho ordinal do marcador no estado atual do rascunho.

**Saídas:** Remove nó e todos os descendentes; restante do outline consistente.

**Limites:** Não é remoção apenas do título; confirmar consequências da subárvore.

**Erros:** Caminho inexistente ou árvore cíclica/inválida → erro sem excluir nó diferente.

**Estado e efeitos:** Exclui subárvore na cópia, preservando páginas e fonte.

**Cancelamento:** Cancelar confirmação conserva árvore; undo antes do save restaura rascunho.

Fontes/requisitos: [app/pdf_changes.py — _change_outline](../app/pdf_changes.py).

Planos relacionados da família: S12-13-1, S12-13-2. Não são aceitação completa desta operação. Nova execução neste registro: `not_run`; expectativa e observação integral Foxit: `null`.


<a id="annotations"></a>

## Anotações/undo/gravação

Atual (0.1.16): notas (Text), retângulo (Square), marcações de área (Highlight, Underline, StrikeOut, Squiggly), Ink, Circle, Line, Polygon, PolyLine, Caret, FreeText e Stamp com aparência própria (Unicode, fontes incorporadas), mover anotações simples, comentários com respostas e popup, edição de autor/comentário e exclusão de conversa limitada; rascunho com desfazer/refazer e original preservado. Cor e opacidade (etapa E12): retângulos, elipses, linhas, destaques, sublinhados, tachados, ondulados, desenhos, polígonos, polilinhas e marcas de inserção já existentes recebem nova cor RGB e opacidade de 10% a 100%; /C e /CA são gravados e a aparência é redesenhada a partir da geometria da própria anotação (destaque com mesclagem Multiply); notas, texto livre e carimbos ficam de fora. Redimensionar (etapa E13): retângulos, elipses e texto livre recebem novo /Rect dentro da página; os dois primeiros são redesenhados na cor e opacidade atuais e o texto livre é diagramado de novo com fontes incorporadas; /RD antigo é removido. Marcar redação (etapa E14): áreas retangulares viram anotações /Redact pendentes (QuadPoints, /IC preto para a aplicação futura) com contorno tracejado vermelho próprio; nada é removido do conteúdo; a marca aparece na lista de comentários e pode ser movida, redimensionada, recolorida, comentada ou excluída. Aplicar redação (etapa E15): numa cópia nova, cada página com marcas é renderizada sem anotações a 150 ou 300 DPI, as áreas são pintadas com a cor de preenchimento e o conteúdo da página vira essa única imagem; páginas sem marcas ficam byte a byte; marcas e anotações sobre as áreas saem, campo de formulário sob área é recusado, objetos órfãos são descartados e a árvore de estrutura é removida quando existe; marcadores, metadados e anexos não são verificados. Redação de texto vetorial sem rasterizar, edição universal de qualquer anotação e disponibilidade exata no Reader continuam abertas.

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

- **S12-14-1** (nominal, contrato próprio atual, `passed`): dado Fixture com nota contendo assunto e conteúdo distintos. Ação: Inspecionar o painel. Esperado: Assunto separado, comentário alvo e autor permanecem campos distintos na página conhecida. Execução própria em 2026-10-21T21:24:29-03:00, revisão `ac89254204fb`, fronteira worker panels: [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e31.json).
- **S12-14-2** (exception, contrato próprio atual, `passed`): dado Objeto de anotação isolado inválido. Ação: Ler os demais comentários. Esperado: A falha de um objeto não deve ser reportada como criação/edição bem-sucedida de anotação. Execução própria em 2026-10-21T21:24:30-03:00, revisão `ac89254204fb`, fronteira worker panels: [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e31.json).
- **S12-14-3** (nominal, contrato próprio atual, `passed`): dado PDF sintético com um retângulo vermelho criado pelo próprio aplicativo. Ação: Mudar a cor para azul com opacidade de 50% e salvar cópia nova. Esperado: A cópia guarda /C azul e /CA 0,5, a aparência é redesenhada e o Poppler desenha a borda em azul-claro; original preservado. Execução própria em 2026-10-21T21:24:30-03:00, revisão `ac89254204fb`, fronteira worker copy-edit (style-annotation) + Poppler: [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e31.json).
- **S12-14-4** (exception, contrato próprio atual, `passed`): dado O mesmo PDF, com uma nota (Text) e o retângulo. Ação: Pedir nova cor para a nota e opacidade de 5% para o retângulo. Esperado: Recusar os dois pedidos sem criar saída; original preservado. Execução própria em 2026-10-21T21:24:31-03:00, revisão `ac89254204fb`, fronteira worker copy-edit (style-annotation): [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e31.json).
- **S12-14-5** (nominal, contrato próprio atual, `passed`): dado PDF sintético com um retângulo criado pelo aplicativo em [20,200,120,280]. Ação: Redimensionar para [40,150,200,290] e salvar cópia nova. Esperado: O /Rect passa a [40,150,200,290]; o Poppler desenha a borda na nova posição e nada na borda antiga; original preservado. Execução própria em 2026-10-21T21:24:31-03:00, revisão `ac89254204fb`, fronteira worker copy-edit (resize-annotation) + Poppler: [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e31.json).
- **S12-14-6** (exception, contrato próprio atual, `passed`): dado O mesmo PDF, com uma nota e o retângulo. Ação: Redimensionar a nota e levar o retângulo para fora da página. Esperado: Recusar os dois pedidos sem criar saída; original preservado. Execução própria em 2026-10-21T21:24:32-03:00, revisão `ac89254204fb`, fronteira worker copy-edit (resize-annotation): [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e31.json).
- **S12-14-7** (nominal, contrato próprio atual, `passed`): dado PDF sintético com o texto "SEGREDO 123" em uma página de 300×300 pontos. Ação: Marcar a área [30,190,160,222] para redação com o comentário "CPF" e salvar cópia nova. Esperado: A cópia tem uma anotação /Redact com esse /Rect e QuadPoints; o conteúdo da página é idêntico ao original e o texto continua extraível e visível no Poppler, com contorno vermelho na borda; original preservado. Execução própria em 2026-10-21T21:24:32-03:00, revisão `ac89254204fb`, fronteira worker copy-edit (add-redaction) + Poppler: [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e31.json).
- **S12-14-8** (exception, contrato próprio atual, `passed`): dado A cópia marcada do caso anterior e o PDF original. Ação: Redimensionar a marca e depois excluí-la; pedir uma marca fora da página e outra com chave extra (texto de sobreposição). Esperado: A marca redimensionada mantém o tipo /Redact com QuadPoints atualizados e some ao ser excluída; os dois pedidos inválidos são recusados sem criar saída; originais preservados. Execução própria em 2026-10-21T21:24:33-03:00, revisão `ac89254204fb`, fronteira worker copy-edit (add-redaction, resize-annotation, delete-annotation): [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e31.json).
- **S12-14-9** (nominal, contrato próprio atual, `passed`): dado PDF sintético de duas páginas: na primeira, "SEGREDO 123", uma imagem vermelha e "publico"; na segunda, "PAGINA DOIS". Uma marca de redação cobre o segredo e a imagem. Ação: Aplicar a redação a 150 DPI numa cópia nova. Esperado: Nenhum objeto decodificado da cópia contém "SEGREDO 123" nem os bytes da imagem; a página 1 não tem texto extraível nem anotações e o Poppler mostra preto na área e o texto "publico" visível; a página 2 tem o mesmo conteúdo do original; original preservado. Execução própria em 2026-10-21T21:24:33-03:00, revisão `ac89254204fb`, fronteira worker redact-copy + Poppler: [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e31.json).
- **S12-14-10** (exception, contrato próprio atual, `passed`): dado O PDF sem marcas, o PDF marcado com um campo de formulário sob a área e um destino já existente. Ação: Aplicar a redação em cada caso. Esperado: Recusar os três pedidos com mensagem própria, sem criar ou alterar arquivos. Execução própria em 2026-10-21T21:24:29-03:00, revisão `ac89254204fb`, fronteira worker redact-copy: [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e31.json).

**Lacunas da referência Foxit**

- Replies, aparências, edição, autoria, undo/redo, salvamento e disponibilidade Reader.

Fontes: [app/pdf_panels.py](../app/pdf_panels.py), [app/search_engine.py](../app/search_engine.py), [app/pdf_changes.py](../app/pdf_changes.py), [app/edit_tasks.py](../app/edit_tasks.py), [app/worker_cli.py](../app/worker_cli.py), [app/main.py](../app/main.py), [docs/SEGURANCA-ACESSIBILIDADE.md](../docs/SEGURANCA-ACESSIBILIDADE.md), [app/local_files.py](../app/local_files.py), [app/folder_dialogs.py](../app/folder_dialogs.py), [docs/PASTAS-SINCRONIZADAS.md](../docs/PASTAS-SINCRONIZADAS.md), [app/pdf_form_controls.py](../app/pdf_form_controls.py), [app/edit_history.py](../app/edit_history.py), [app/edit_dialogs.py](../app/edit_dialogs.py), [app/edit_window.py](../app/edit_window.py), [docs/EDICAO-COM-HISTORICO.md](../docs/EDICAO-COM-HISTORICO.md), [testes/resultados/0.1.10/validation-review.json](../testes/resultados/0.1.10/validation-review.json), [app/pdf_annotations.py](../app/pdf_annotations.py), [docs/ANOTACOES-AMPLIADAS.md](../docs/ANOTACOES-AMPLIADAS.md), [testes/resultados/annotation-extensions-portable-2026-10-18-round3.json](../testes/resultados/annotation-extensions-portable-2026-10-18-round3.json), [testes/resultados/0.1.13/validation-review.json](../testes/resultados/0.1.13/validation-review.json), [app/annotation_geometry.py](../app/annotation_geometry.py), [app/text_appearance.py](../app/text_appearance.py), [app/pdf_edit_security.py](../app/pdf_edit_security.py), [testes/resultados/0.1.16/validation-review.json](../testes/resultados/0.1.16/validation-review.json), [app/annotation_style.py](../app/annotation_style.py), [app/pdf_redaction.py](../app/pdf_redaction.py), [docs/FOXIT-REA.md](../docs/FOXIT-REA.md).

Testes próprios existentes, sem nova execução nesta tabela: [test_comment_subject_contents_and_author_are_searchable](../tests/test_search_scopes.py); [test_combined_copy_preserves_source_metadata_attachment_and_previous_objects](../tests/test_pdf_changes.py); [test_encryption_signature_permissions_xfa_and_portfolio_are_explicitly_unsupported](../tests/test_pdf_changes.py); [test_real_dialogs_and_worker_create_bookmark_note_and_form_copies](../tests/test_copy_edit_gtk.py); [test_reopening_same_document_during_dialog_blocks_stale_save](../tests/test_copy_edit_gtk.py); [test_existing_destination_is_preserved_and_busy_state_is_released](../tests/test_copy_edit_gtk.py); [test_combined_edits_preserve_tree_destinations_geometry_and_source](../tests/test_extended_edits.py); [test_final_name_is_absent_while_real_copy_is_in_progress](../tests/test_sync_folders.py); [test_save_copy_uses_worker_preserves_original_and_only_confirms_local_save](../tests/test_sync_folders_gtk.py); [test_info_distinguishes_checkbox_radio_choice_combo_and_multiselect](../tests/test_advanced_edits.py); [test_checkbox_sets_and_clears_value_and_visible_appearance](../tests/test_advanced_edits.py); [test_radio_activates_only_the_selected_widget_and_can_clear](../tests/test_advanced_edits.py); [test_radio_no_toggle_off_is_enforced](../tests/test_advanced_edits.py); [test_single_and_combo_values_indices_and_generated_appearances_roundtrip](../tests/test_advanced_edits.py); [test_multiselect_uses_export_values_and_canonical_indices](../tests/test_advanced_edits.py); [test_choice_selection_can_be_cleared](../tests/test_advanced_edits.py); [test_invalid_values_do_not_publish_partial_batch](../tests/test_advanced_edits.py); [test_read_only_and_unsupported_button_appearance_are_explicit](../tests/test_advanced_edits.py); [test_editable_combo_and_duplicate_exports_are_rejected](../tests/test_advanced_edits.py); [test_inherited_checkbox_flags_and_type_are_respected](../tests/test_advanced_edits.py); [test_checkbox_widget_absent_from_pages_is_unsupported](../tests/test_advanced_edits.py); [test_closed_outline_counts_remain_closed_after_move](../tests/test_advanced_edits.py); [test_move_preserves_subtree_destinations_and_sibling_links](../tests/test_advanced_edits.py); [test_move_child_to_root_and_reorder_same_parent](../tests/test_advanced_edits.py); [test_delete_bookmark_removes_subtree_and_last_root](../tests/test_advanced_edits.py); [test_move_into_descendant_invalid_positions_and_boolean_paths_are_refused](../tests/test_advanced_edits.py); [test_highlight_and_rectangle_roundtrip_geometry_print_flags_and_text](../tests/test_advanced_edits.py); [test_delete_supported_annotation_preserves_widgets_and_other_pages](../tests/test_advanced_edits.py); [test_locked_notes_widgets_and_replies_are_not_deleted](../tests/test_advanced_edits.py); [test_invalid_annotation_geometry_and_extra_parameters_are_rejected](../tests/test_advanced_edits.py); [test_undo_redo_rebuild_actual_pdfs_and_save_current_cursor_only](../tests/test_edit_history.py); [test_undo_all_restores_base_and_disables_save_until_redone](../tests/test_edit_history.py); [test_new_branch_discards_redo_but_invalid_branch_preserves_it](../tests/test_edit_history.py); [test_operation_values_are_defensively_copied](../tests/test_edit_history.py); [test_changed_original_blocks_add_undo_redo_and_save](../tests/test_edit_history.py); [test_existing_destination_is_not_overwritten_and_draft_survives](../tests/test_edit_history.py); [test_closed_session_refuses_work_and_removes_private_previews](../tests/test_edit_history.py); [test_pre_cancelled_session_does_not_start_worker](../tests/test_edit_history.py); [test_buttons_undo_redo_save_selected_history_and_preserve_prior_copy](../tests/test_edit_draft_gtk.py); [test_real_form_dialog_checkbox_radio_list_and_multiselect](../tests/test_edit_draft_gtk.py); [test_real_move_and_delete_bookmark_dialogs_use_updated_paths](../tests/test_edit_draft_gtk.py); [test_real_area_annotation_dialog_and_delete_keep_other_annotations](../tests/test_edit_draft_gtk.py); [test_failed_operation_and_existing_destination_keep_history_usable](../tests/test_edit_draft_gtk.py); [test_cancel_dialog_and_reopen_parent_close_draft_without_publishing](../tests/test_edit_draft_gtk.py); [test_cancelling_save_and_repeated_clicks_do_not_duplicate_writes](../tests/test_edit_draft_gtk.py); [test_saved_form_and_highlight_render_with_poppler](../tests/test_edit_draft_gtk.py); [test_all_five_types_roundtrip_with_printable_embedded_appearance](../tests/test_annotation_extensions.py); [test_text_markup_quad_order_and_line_and_ellipse_metadata_are_distinct](../tests/test_annotation_extensions.py); [test_offsets_and_page_rotations_do_not_double_transform_geometry](../tests/test_annotation_extensions.py); [test_horizontal_vertical_and_reversed_lines_keep_endpoint_direction](../tests/test_annotation_extensions.py); [test_boundary_strokes_have_positive_clipped_boxes_and_small_areas_renderable_numbers](../tests/test_annotation_extensions.py); [test_squiggly_geometry_has_bounded_commands_even_on_extreme_page](../tests/test_annotation_extensions.py); [test_invalid_area_and_crop_coordinates_refuse_the_entire_batch](../tests/test_annotation_extensions.py); [test_invalid_line_points_page_and_extra_fields_are_rejected](../tests/test_annotation_extensions.py); [test_utf8_comment_and_author_limits_and_nonstring_values_are_enforced](../tests/test_annotation_extensions.py); [test_edit_and_clear_comment_author_preserve_geometry_appearance_and_other_content](../tests/test_annotation_extensions.py); [test_locked_related_and_unsupported_annotations_cannot_be_changed_or_deleted](../tests/test_annotation_extensions.py); [test_deleting_new_types_uses_current_indices_and_preserves_forms_notes_and_other_page](../tests/test_annotation_extensions.py); [test_real_worker_protocol_lists_new_types_and_author_and_refuses_source_and_destination_changes](../tests/test_annotation_extensions.py); [test_history_undo_redo_comment_delete_and_failed_branch_preserve_saved_copy](../tests/test_annotation_extensions.py); [test_real_dialogs_create_all_five_types_and_history_recreates_deleted_shape](../tests/test_annotation_extensions_gtk.py); [test_comment_dialog_prefills_selected_annotation_accepts_multiline_and_can_clear](../tests/test_annotation_extensions_gtk.py); [test_invalid_line_is_explained_in_dialog_and_cancel_does_not_change_draft](../tests/test_annotation_extensions_gtk.py); [test_saved_five_appearances_have_expected_poppler_pixels_and_unfilled_interiors](../tests/test_annotation_extensions_gtk.py); [test_offset_cropbox_and_rotation_render_line_at_transformed_location](../tests/test_annotation_extensions_gtk.py); [test_edited_nontext_annotation_comment_is_searchable_after_reopening_saved_copy](../tests/test_annotation_extensions_gtk.py); [test_every_supported_type_becomes_blue_and_half_transparent](../tests/test_annotation_style.py); [test_full_opacity_keeps_solid_colour_and_restyle_can_repeat](../tests/test_annotation_style.py); [test_notes_bad_colour_and_too_low_opacity_are_refused_without_output](../tests/test_annotation_style.py); [test_dialog_offers_styleable_records_with_current_style_and_returns_operation](../tests/test_annotation_style_gtk.py); [test_square_and_circle_are_redrawn_in_the_new_rectangle](../tests/test_annotation_resize.py); [test_freetext_is_laid_out_again_for_the_new_size](../tests/test_annotation_resize.py); [test_line_outside_page_and_tiny_rectangles_are_refused](../tests/test_annotation_resize.py); [test_resize_dialog_prefills_the_current_rectangle_and_returns_the_new_one](../tests/test_annotation_style_gtk.py); [test_mark_is_a_pending_redact_annotation_and_content_is_untouched](../tests/test_redaction_marks.py); [test_mark_is_listed_as_editable](../tests/test_redaction_marks.py); [test_mark_can_be_resized_commented_restyled_and_deleted](../tests/test_redaction_marks.py); [test_invalid_marks_are_refused](../tests/test_redaction_marks.py); [test_poppler_draws_the_outline_and_keeps_the_marked_text_visible](../tests/test_redaction_marks.py); [test_redaction_dialog_returns_a_mark_without_applying_anything](../tests/test_annotation_style_gtk.py); [test_text_and_image_under_the_mark_are_gone_and_other_pages_are_intact](../tests/test_redaction_apply.py); [test_overlapping_annotations_go_and_others_stay](../tests/test_redaction_apply.py); [test_rotated_page_is_painted_in_page_space](../tests/test_redaction_apply.py); [test_structure_tree_is_dropped](../tests/test_redaction_apply.py); [test_refusals_create_nothing](../tests/test_redaction_apply.py); [test_worker_round_trip_and_confirmation](../tests/test_redaction_apply.py); [test_marks_in_the_draft_are_applied_to_a_new_copy](../tests/test_redaction_gtk.py); [test_confirmation_dialog_returns_the_chosen_resolution](../tests/test_redaction_gtk.py).

Relacionados aos planos dinâmicos/UI: D08, D09, D19.

### Contratos individuais de operações

#### `annotations/note` — Criar nota Text

Estado: `current_bounded_source`; base: `current_linuxit_source`.

**Entradas:** Página, texto, rect e author opcional em coordenadas PDF.

**Saídas:** Anotação /Text imprimível com geometria e texto persistidos em cópia.

**Limites:** Área dentro de CropBox; texto até 64 KiB UTF-8; autor até 4096 bytes.

**Erros:** Retângulo fora da página ou texto inválido → ValueError sem anotação parcial.

**Estado e efeitos:** Anexa anotação à página do rascunho, sem mudar conteúdo da página.

**Cancelamento:** Cancelar diálogo não cria operação; undo remove nota no rascunho e mantém cópias já salvas.

Fontes/requisitos: [app/pdf_changes.py — _apply](../app/pdf_changes.py).

Planos relacionados da família: S12-14-1, S12-14-2, S12-14-3, S12-14-4, S12-14-5, S12-14-6, S12-14-7, S12-14-8, S12-14-9, S12-14-10. Não são aceitação completa desta operação. Nova execução neste registro: `not_run`; expectativa e observação integral Foxit: `null`.

#### `annotations/highlight` — Criar destaque de área

Estado: `current_bounded_source`; base: `current_linuxit_source`.

**Entradas:** Página, retângulo positivo e comentário da operação add-highlight.

**Saídas:** /Highlight com QuadPoints e aparência própria na área escolhida.

**Limites:** Geometria por área não reconstrói seleção semântica multilinha universal.

**Erros:** Área fora de CropBox ou vazia → rejeição antes da publicação.

**Estado e efeitos:** Cria anotação sobre conteúdo; não altera texto original.

**Cancelamento:** Segue undo/redo do rascunho; cancelar preparação não publica cópia final.

Fontes/requisitos: [app/pdf_changes.py — _apply](../app/pdf_changes.py).

Planos relacionados da família: S12-14-1, S12-14-2, S12-14-3, S12-14-4, S12-14-5, S12-14-6, S12-14-7, S12-14-8, S12-14-9, S12-14-10. Não são aceitação completa desta operação. Nova execução neste registro: `not_run`; expectativa e observação integral Foxit: `null`.

#### `annotations/rectangle` — Criar retângulo

Estado: `current_bounded_source`; base: `current_linuxit_source`.

**Entradas:** Página, rect dentro do CropBox e texto.

**Saídas:** /Square imprimível com retângulo e aparência persistidos.

**Limites:** Coordenadas finitas em pontos PDF; preenchimento/estilo seguem aparência própria.

**Erros:** Retângulo invertido/fora da página → ValueError.

**Estado e efeitos:** Anotação de desenho separada do conteúdo; fonte intacta.

**Cancelamento:** Diálogo cancelado descarta pedido; undo refaz rascunho sem o Square.

Fontes/requisitos: [app/pdf_changes.py — _apply](../app/pdf_changes.py).

Planos relacionados da família: S12-14-1, S12-14-2, S12-14-3, S12-14-4, S12-14-5, S12-14-6, S12-14-7, S12-14-8, S12-14-9, S12-14-10. Não são aceitação completa desta operação. Nova execução neste registro: `not_run`; expectativa e observação integral Foxit: `null`.

#### `annotations/underline` — Criar sublinhado

Estado: `current_bounded_source`; base: `current_linuxit_source`.

**Entradas:** Página, rect e comentário em add-underline.

**Saídas:** /Underline e QuadPoints com aparência vetorial própria vermelha.

**Limites:** Área mínima 0,25 ponto em cada eixo; coordenadas absolutas até 10 milhões; texto até 64 KiB.

**Erros:** Área pequena, fora de CropBox ou coordenadas não finitas → ValueError.

**Estado e efeitos:** Adiciona anotação vetorial à cópia, sem riscar bytes do conteúdo.

**Cancelamento:** Undo/redo remove/reaplica no rascunho; cancelamento do worker mantém fonte.

Fontes/requisitos: [app/pdf_annotations.py — create_annotation](../app/pdf_annotations.py).

Planos relacionados da família: S12-14-1, S12-14-2, S12-14-3, S12-14-4, S12-14-5, S12-14-6, S12-14-7, S12-14-8, S12-14-9, S12-14-10. Não são aceitação completa desta operação. Nova execução neste registro: `not_run`; expectativa e observação integral Foxit: `null`.

#### `annotations/strikeout` — Criar tachado

Estado: `current_bounded_source`; base: `current_linuxit_source`.

**Entradas:** Página, rect e comentário em add-strikeout.

**Saídas:** /StrikeOut com aparência vetorial própria no meio da área.

**Limites:** Mínimo 0,25 ponto em ambos os eixos; não calcula baseline tipográfica real.

**Erros:** Área inválida ou texto acima de 64 KiB → ValueError.

**Estado e efeitos:** Adiciona anotação; texto da página continua pesquisável e não é redação.

**Cancelamento:** Undo remove marca do rascunho; cópia já salva não é modificada.

Fontes/requisitos: [app/pdf_annotations.py — create_annotation](../app/pdf_annotations.py).

Planos relacionados da família: S12-14-1, S12-14-2, S12-14-3, S12-14-4, S12-14-5, S12-14-6, S12-14-7, S12-14-8, S12-14-9, S12-14-10. Não são aceitação completa desta operação. Nova execução neste registro: `not_run`; expectativa e observação integral Foxit: `null`.

#### `annotations/squiggly` — Criar ondulado

Estado: `current_bounded_source`; base: `current_linuxit_source`.

**Entradas:** Página, rect e comentário em add-squiggly.

**Saídas:** /Squiggly com caminho ondulado vetorial e QuadPoints.

**Limites:** Geometria finita e área mínima 0,25 ponto, dentro do CropBox.

**Erros:** Coordenada fora da página ou área degenerada → ValueError sem aparência truncada válida.

**Estado e efeitos:** Cria marca de revisão; não altera conteúdo nem fonte.

**Cancelamento:** Cancelamento do diálogo descarta geometria; histórico pode desfazer/refazer.

Fontes/requisitos: [app/pdf_annotations.py — create_annotation](../app/pdf_annotations.py).

Planos relacionados da família: S12-14-1, S12-14-2, S12-14-3, S12-14-4, S12-14-5, S12-14-6, S12-14-7, S12-14-8, S12-14-9, S12-14-10. Não são aceitação completa desta operação. Nova execução neste registro: `not_run`; expectativa e observação integral Foxit: `null`.

#### `annotations/ellipse` — Criar elipse

Estado: `current_bounded_source`; base: `current_linuxit_source`.

**Entradas:** Página, rect e comentário em add-ellipse.

**Saídas:** /Circle com elipse vetorial inscrita no retângulo.

**Limites:** Rect positivo mínimo 0,25 ponto por eixo, até 10 milhões em módulo.

**Erros:** Área/coord fora dos limites → ValueError.

**Estado e efeitos:** Anotação separada com aparência própria; PDF original preservado.

**Cancelamento:** Undo/redo no rascunho; worker cancelado não modifica fonte.

Fontes/requisitos: [app/pdf_annotations.py — create_annotation](../app/pdf_annotations.py).

Planos relacionados da família: S12-14-1, S12-14-2, S12-14-3, S12-14-4, S12-14-5, S12-14-6, S12-14-7, S12-14-8, S12-14-9, S12-14-10. Não são aceitação completa desta operação. Nova execução neste registro: `not_run`; expectativa e observação integral Foxit: `null`.

#### `annotations/line` — Criar linha

Estado: `current_bounded_source`; base: `current_linuxit_source`.

**Entradas:** Página, dois extremos [x1,y1,x2,y2] e comentário.

**Saídas:** /Line com /L e aparência na direção dos extremos, inclusive diagonal invertida.

**Limites:** Comprimento mínimo 0,25 ponto; todos os pontos dentro de CropBox.

**Erros:** Extremos coincidentes/fora da página → rejeição; não ordenar extremos como retângulo.

**Estado e efeitos:** Adiciona traço vetorial e bounds próprios na cópia.

**Cancelamento:** Cancelar captura descarta extremos; undo remove operação do histórico.

Fontes/requisitos: [app/pdf_annotations.py — create_annotation](../app/pdf_annotations.py).

Planos relacionados da família: S12-14-1, S12-14-2, S12-14-3, S12-14-4, S12-14-5, S12-14-6, S12-14-7, S12-14-8, S12-14-9, S12-14-10. Não são aceitação completa desta operação. Nova execução neste registro: `not_run`; expectativa e observação integral Foxit: `null`.

#### `annotations/comment-author` — Editar comentário e autor

Estado: `current_bounded_source`; base: `current_linuxit_source`.

**Entradas:** Página, índice da anotação atual e strings text/author.

**Saídas:** /Contents e /T atualizados ou limpos sem alterar geometria.

**Limites:** Texto até 64 KiB, autor até 4096 bytes; somente tipos suportados desbloqueados e sem dependentes no comando simples.

**Erros:** Índice stale, lock, popup/resposta dependente ou tipo incompatível → recusa, sem editar widget.

**Estado e efeitos:** Muda metadados na cópia; não prova identidade de autor.

**Cancelamento:** Cancelar diálogo preserva metadados; undo reconstrói texto/autor anteriores do rascunho.

Fontes/requisitos: [app/pdf_changes.py — _apply](../app/pdf_changes.py).

Planos relacionados da família: S12-14-1, S12-14-2, S12-14-3, S12-14-4, S12-14-5, S12-14-6, S12-14-7, S12-14-8, S12-14-9, S12-14-10. Não são aceitação completa desta operação. Nova execução neste registro: `not_run`; expectativa e observação integral Foxit: `null`.

#### `annotations/style` — Mudar cor e opacidade de anotação existente

Estado: `current_bounded_source`; base: `current_linuxit_source`.

**Entradas:** Página, índice, color RGB de três componentes e opacity.

**Saídas:** /C, /CA e aparência normal regeneradas com ExtGState; Multiply para highlight.

**Limites:** Opacidade 0,1–1; tipos STYLEABLE incluindo Redact, sem locks/vínculos incompatíveis.

**Erros:** Text/FreeText/Stamp ou anotação com popup/respostas → recusa do comando de estilo simples.

**Estado e efeitos:** Altera aparência de anotação, sem rasterizar página; geometria mantida.

**Cancelamento:** Cancelar diálogo não modifica rascunho; undo restaura estilo anterior.

Fontes/requisitos: [app/annotation_style.py — restyle_annotation](../app/annotation_style.py).

Planos relacionados da família: S12-14-1, S12-14-2, S12-14-3, S12-14-4, S12-14-5, S12-14-6, S12-14-7, S12-14-8, S12-14-9, S12-14-10. Não são aceitação completa desta operação. Nova execução neste registro: `not_run`; expectativa e observação integral Foxit: `null`.

#### `annotations/resize` — Redimensionar retângulo, elipse ou texto livre

Estado: `current_bounded_source`; base: `current_linuxit_source`.

**Entradas:** Página, índice e novo rect dentro do CropBox.

**Saídas:** /Rect atualizado, /RD removido e aparência refeita; Redact atualiza QuadPoints.

**Limites:** Aceita Square/Circle/FreeText/Redact; outros tipos exigem operação específica.

**Erros:** Tipo não redimensionável, lock ou dependentes → erro, sem deslocar widgets/conversa.

**Estado e efeitos:** Muda anotação na cópia; FreeText pode redispor texto com fonte incorporada.

**Cancelamento:** Undo reconstrói estado anterior; cancelar geometria descarta pedido.

Fontes/requisitos: [app/annotation_geometry.py — resize_annotation](../app/annotation_geometry.py).

Planos relacionados da família: S12-14-1, S12-14-2, S12-14-3, S12-14-4, S12-14-5, S12-14-6, S12-14-7, S12-14-8, S12-14-9, S12-14-10. Não são aceitação completa desta operação. Nova execução neste registro: `not_run`; expectativa e observação integral Foxit: `null`.

#### `annotations/redaction-mark` — Marcar áreas para redação (sem aplicar)

Estado: `current_bounded_source`; base: `current_linuxit_source`.

**Entradas:** Página, retângulo e comentário opcional.

**Saídas:** /Redact com Rect/QuadPoints, IC preto e AP própria tracejada vermelha.

**Limites:** Só marca intenção; conteúdo original continua presente até aplicação; texto até 64 KiB.

**Erros:** Área fora do CropBox/chaves extras → ValueError.

**Estado e efeitos:** Cria anotação pendente movível/redimensionável; não remove informações.

**Cancelamento:** Cancelar marca/undo conserva página; exclusão simples remove somente intenção.

Fontes/requisitos: [app/annotation_style.py — create_redaction](../app/annotation_style.py).

Planos relacionados da família: S12-14-1, S12-14-2, S12-14-3, S12-14-4, S12-14-5, S12-14-6, S12-14-7, S12-14-8, S12-14-9, S12-14-10. Não são aceitação completa desta operação. Nova execução neste registro: `not_run`; expectativa e observação integral Foxit: `null`.

#### `annotations/redaction-apply` — Aplicar redação em cópia nova

Estado: `current_bounded_source`; base: `current_linuxit_source`.

**Entradas:** PDF com marcas /Redact, novo destino e DPI permitido. Extensão A6: mode=vector explícito, com mesmo hash/destino/marcas; raster continua default.

**Saídas:** Cópia com páginas marcadas rasterizadas sem anotações, áreas cobertas e objetos órfãos removidos; relatório de perdas. Modo vetorial conservador remove objetos BT inteiros, caminhos pintados inteiros e usos de imagem inteiros que intersectam a marca; preserva texto/vetores públicos admitidos sem rasterizar.

**Limites:** 150/300 DPI, até 50 páginas marcadas, 512 marcas e 45 MP por página; não promete remoção em anexos/metadados/títulos. Perfil vetorial: fontes Type1 Standard14 sem descritores/larguras/custom encoding; sem gs, clipping, Form XObjects, marked content, inline image ou texto com contorno (Tr1/2); operações desconhecidas recusadas. Até200000 operações/página e stack64; derivações numéricas devem ser finitas.

**Erros:** Cifrado/assinado/XFA/portfólio, widget sobreposto ou nenhum Redact → recusa sem saída final.; Operador/estrutura gráfica fora do perfil vetorial ou geometria composta não finita → ValueError sem publicar cópia; oferecer escolha explícita do modo raster, sem fallback silencioso.

**Estado e efeitos:** Substitui conteúdo das páginas marcadas por imagem; remove anotações sobrepostas e estrutura quando presente; páginas não marcadas preservadas. No modo vector remove Thumb/PieceInfo/StructParents/SeparationInfo da página, XObjects não usados e objetos órfãos, além das anotações/estrutura tratadas pelo backend comum; não busca segredos em metadata/anexos/outras páginas.

**Cancelamento:** Worker cancelável/timeout 900 s; se interrompido antes de publicar não criar cópia final; destino existente nunca sobrescrito.

Fontes/requisitos: [app/pdf_redaction.py — redact_copy](../app/pdf_redaction.py), [app/vector_redaction.py — redact_page](../app/vector_redaction.py).

Planos relacionados da família: S12-14-1, S12-14-2, S12-14-3, S12-14-4, S12-14-5, S12-14-6, S12-14-7, S12-14-8, S12-14-9, S12-14-10. Não são aceitação completa desta operação. Nova execução neste registro: `not_run`; expectativa e observação integral Foxit: `null`.

#### `annotations/delete` — Excluir anotação simples

Estado: `current_bounded_source`; base: `current_linuxit_source`.

**Entradas:** Página e índice de anotação simples no rascunho atual.

**Saídas:** Anotação removida de Annots com resto da página preservado.

**Limites:** Não é remoção universal; exige tipo suportado, desbloqueado e sem popup/respostas/vínculos.

**Erros:** Widget, tipo estranho, lock ou dependente → ValueError, sem excluir conteúdo relacionado por suposição.

**Estado e efeitos:** Altera cópia/rascunho; fonte e cópias anteriores ficam intactas.

**Cancelamento:** Confirmar/cancelar antes da operação; undo restaura anotação no rascunho.

Fontes/requisitos: [app/pdf_changes.py — _apply](../app/pdf_changes.py).

Planos relacionados da família: S12-14-1, S12-14-2, S12-14-3, S12-14-4, S12-14-5, S12-14-6, S12-14-7, S12-14-8, S12-14-9, S12-14-10. Não são aceitação completa desta operação. Nova execução neste registro: `not_run`; expectativa e observação integral Foxit: `null`.

#### `annotations/history` — Desfazer/refazer rascunho

Estado: `current_bounded_source`; base: `current_linuxit_source`.

**Entradas:** EditSession, operação válida e cursor atual de alterações.

**Saídas:** Undo/redo reconstrói cópia do rascunho correspondente ao cursor.

**Limites:** Até 100 passos na UI; novo add após undo elimina ramo redo; worker aceita no máximo 1000 operações por lote.

**Erros:** Undo vazio, redo vazio ou adicionar após 100 passos → ValueError; save sem alteração também recusado.

**Estado e efeitos:** Rascunho temporário substituído, nunca fonte/cópias já salvas.

**Cancelamento:** Cancelar tarefa de reconstrução mantém fonte e não aprova rascunho incompleto.

Fontes/requisitos: [app/edit_history.py — EditSession.undo](../app/edit_history.py).

Planos relacionados da família: S12-14-1, S12-14-2, S12-14-3, S12-14-4, S12-14-5, S12-14-6, S12-14-7, S12-14-8, S12-14-9, S12-14-10. Não são aceitação completa desta operação. Nova execução neste registro: `not_run`; expectativa e observação integral Foxit: `null`.

#### `annotations/replies` — Editar respostas/popup e vínculos

Estado: `current_bounded_source`; base: `current_linuxit_source`.

**Entradas:** Página/índice alvo, resposta text/author e comando popup/update/delete-conversation quando escolhido.

**Saídas:** /IRT e /RT, popup e conversa persistidos no subconjunto suportado.

**Limites:** Profundidade de conversa 64; exige referência indireta, mesma página e tipos sem locks.

**Erros:** Conversa cíclica/entre páginas, alvo direto ou bloqueado → recusa atômica.

**Estado e efeitos:** Adiciona/edita dependentes somente na cópia; exclusão da conversa exige seleção própria.

**Cancelamento:** Cancelar diálogo conserva conversa; histórico desfaz lote no rascunho, não cópia já publicada.

Fontes/requisitos: [app/pdf_changes.py — _apply](../app/pdf_changes.py), [app/annotation_geometry.py — conversation_members](../app/annotation_geometry.py).

Planos relacionados da família: S12-14-1, S12-14-2, S12-14-3, S12-14-4, S12-14-5, S12-14-6, S12-14-7, S12-14-8, S12-14-9, S12-14-10. Não são aceitação completa desta operação. Nova execução neste registro: `not_run`; expectativa e observação integral Foxit: `null`.

#### `annotations/freehand` — Desenho livre e demais tipos

Estado: `current_bounded_source`; base: `current_linuxit_source`.

**Entradas:** Página, 1–32 caminhos de pares XY e comentário.

**Saídas:** /Ink com InkList e aparência vetorial própria.

**Limites:** Até 4096 pontos no total, dois por traço, variação mínima 0,25 ponto; coordenadas dentro de CropBox.

**Erros:** Traço degenerado, ímpar ou fora da página → ValueError.

**Estado e efeitos:** Adiciona desenho sem rasterizar conteúdo, fonte preservada.

**Cancelamento:** Limpar/cancelar captura descarta caminhos; undo remove operação Ink inteira.

Fontes/requisitos: [app/pdf_annotations.py — create_ink](../app/pdf_annotations.py), [app/edit_dialogs.py — ink_operation_dialog](../app/edit_dialogs.py).

Planos relacionados da família: S12-14-1, S12-14-2, S12-14-3, S12-14-4, S12-14-5, S12-14-6, S12-14-7, S12-14-8, S12-14-9, S12-14-10. Não são aceitação completa desta operação. Nova execução neste registro: `not_run`; expectativa e observação integral Foxit: `null`.


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

- **S12-15-1** (nominal, contrato próprio atual, `passed`): dado AcroForm sintético com campo Tx editável, sem XFA ou assinatura. Ação: Preencher o campo Tx e salvar cópia nova. Esperado: Reabrir a cópia confirma o texto; páginas e original são preservados. Widgets de escolha não estão neste subconjunto. Execução própria em 2026-10-21T21:24:34-03:00, revisão `ac89254204fb`, fronteira worker copy-edit: [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e31.json).
- **S12-15-2** (exception, contrato próprio atual, `passed`): dado AcroForm sintético com campo Tx ReadOnly ou MaxLen excedido. Ação: Tentar alterar o campo e salvar cópia. Esperado: Recusar a operação sem saída nova; preservar o original. Execução própria em 2026-10-21T21:24:35-03:00, revisão `ac89254204fb`, fronteira worker copy-edit: [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e31.json).
- **S12-15-3** (nominal, contrato próprio atual, `passed`): dado AcroForm sintético com preço e quantidade (AFNumber_Keystroke com vírgula decimal) e total calculado com AFNumber_Format(2, 2, 0, 0, "R$ ", true). Ação: Preencher preço 1234,5 e quantidade 2 com cálculos e salvar cópia nova. Esperado: O total guarda 2469 sem formatação e a aparência mostra R$ 2.469,00; nenhum JavaScript é executado; o original é preservado. Execução própria em 2026-10-21T21:24:35-03:00, revisão `ac89254204fb`, fronteira worker copy-edit (fill-form-events): [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e31.json).
- **S12-15-4** (nominal, contrato próprio atual, `passed`): dado AcroForm sintético com campo de data (AFDate_KeystrokeEx e AFDate_FormatEx "dd/mm/yyyy"). Ação: Preencher 1/2/2026 com eventos e salvar cópia nova. Esperado: O campo guarda 1/2/2026 como digitado e a aparência mostra 01/02/2026; nenhum JavaScript é executado; original preservado. Execução própria em 2026-10-21T21:24:35-03:00, revisão `ac89254204fb`, fronteira worker copy-edit (fill-form-events): [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e31.json).
- **S12-15-5** (exception, contrato próprio atual, `passed`): dado Mesmo formulário de data. Ação: Preencher 31/02/2026 e tentar salvar cópia. Esperado: Recusar a data inexistente sem criar saída; original preservado. Execução própria em 2026-10-21T21:24:35-03:00, revisão `ac89254204fb`, fronteira worker copy-edit (fill-form-events): [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e31.json).
- **S12-15-6** (nominal, contrato próprio atual, `passed`): dado AcroForm sintético com cep (AFSpecial_KeystrokeEx "99999-999") e telefone (AFSpecial_Keystroke/Format 2). Ação: Preencher cep 01310100 e telefone 5551234567 com eventos e salvar cópia nova. Esperado: cep guarda 01310-100; telefone guarda só os dígitos e aparece como (555) 123-4567; nenhum JavaScript é executado; original preservado. Execução própria em 2026-10-21T21:24:35-03:00, revisão `ac89254204fb`, fronteira worker copy-edit (fill-form-events): [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e31.json).
- **S12-15-7** (exception, contrato próprio atual, `passed`): dado Mesmo formulário de máscaras. Ação: Preencher cep com letra ou telefone com 8 dígitos e tentar salvar. Esperado: Recusar cada caso sem criar saída; original preservado. Execução própria em 2026-10-21T21:24:36-03:00, revisão `ac89254204fb`, fronteira worker copy-edit (fill-form-events): [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e31.json).
- **S12-15-8** (nominal, contrato próprio atual, `passed`): dado PDF sintético XFA híbrido: campos AcroForm form1[0].nome[0] e form1[0].extra[0] e pacotes template/datasets com nome, dois itens e obs vazio. Ação: Ler os painéis do documento. Esperado: Listar form1[0].nome[0]=Ana Souza, form1[0].itens[0].item[0]=Caneta, item[1]=Caderno e obs vazio, marcado como híbrido; nenhum script executado; original preservado. Execução própria em 2026-10-21T21:24:36-03:00, revisão `ac89254204fb`, fronteira worker panels (XFA datasets): [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e31.json).
- **S12-15-9** (nominal, contrato próprio atual, `passed`): dado O mesmo PDF XFA e o formulário AcroForm sem XFA, abertos na janela. Ação: Abrir Campos de formulário XFA… depois de carregados os painéis. Esperado: Diálogo somente leitura com quatro linhas, a primeira form1[0].nome[0] = Ana Souza, resumo híbrido que avisa que scripts não são executados; no PDF sem XFA, aviso de que não há formulário XFA. Execução própria em 2026-10-21T21:24:36-03:00, revisão `ac89254204fb`, fronteira PDFWindow _xfa_dialog: [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e31.json).
- **S12-15-10** (nominal, contrato próprio atual, `passed`): dado O mesmo PDF XFA híbrido. Ação: Preencher form1[0].nome[0] com "Bia Lima" e salvar cópia nova. Esperado: Na cópia reaberta, o campo AcroForm e o valor form1[0].nome[0] do pacote datasets são "Bia Lima"; os demais dados XFA não mudam; original preservado. Execução própria em 2026-10-21T21:24:34-03:00, revisão `ac89254204fb`, fronteira worker copy-edit (XFA hybrid fill): [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e31.json).
- **S12-15-11** (exception, contrato próprio atual, `passed`): dado O mesmo PDF XFA híbrido. Ação: Preencher form1[0].extra[0], que não tem dado XFA correspondente, ou adicionar um marcador. Esperado: Recusar cada caso sem criar saída, para não deixar AcroForm e dados XFA divergentes; original preservado. Execução própria em 2026-10-21T21:24:34-03:00, revisão `ac89254204fb`, fronteira worker copy-edit (XFA hybrid fill): [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e31.json).

**Lacunas da referência Foxit**

- Motor de formulários, eventos, XFA, cálculo/validação e gravação; FRMSPlgV2 é RMS, não prova de formulários.

Fontes: [app/pdf_changes.py](../app/pdf_changes.py), [app/edit_tasks.py](../app/edit_tasks.py), [app/worker_cli.py](../app/worker_cli.py), [app/main.py](../app/main.py), [app/local_files.py](../app/local_files.py), [app/folder_dialogs.py](../app/folder_dialogs.py), [docs/PASTAS-SINCRONIZADAS.md](../docs/PASTAS-SINCRONIZADAS.md), [app/pdf_form_controls.py](../app/pdf_form_controls.py), [app/edit_history.py](../app/edit_history.py), [app/edit_dialogs.py](../app/edit_dialogs.py), [app/edit_window.py](../app/edit_window.py), [docs/EDICAO-COM-HISTORICO.md](../docs/EDICAO-COM-HISTORICO.md), [testes/resultados/0.1.10/validation-review.json](../testes/resultados/0.1.10/validation-review.json), [app/pdf_form_events.py](../app/pdf_form_events.py), [app/pdf_edit_security.py](../app/pdf_edit_security.py), [testes/resultados/0.1.16/validation-review.json](../testes/resultados/0.1.16/validation-review.json), [app/pdf_xfa.py](../app/pdf_xfa.py), [app/pdf_panels.py](../app/pdf_panels.py), [docs/FOXIT-REA.md](../docs/FOXIT-REA.md), [docs/AVANCO-SEM-VM.md](../docs/AVANCO-SEM-VM.md).

Testes próprios existentes, sem nova execução nesta tabela: [test_combined_copy_preserves_source_metadata_attachment_and_previous_objects](../tests/test_pdf_changes.py); [test_encryption_signature_permissions_xfa_and_portfolio_are_explicitly_unsupported](../tests/test_pdf_changes.py); [test_real_dialogs_and_worker_create_bookmark_note_and_form_copies](../tests/test_copy_edit_gtk.py); [test_reopening_same_document_during_dialog_blocks_stale_save](../tests/test_copy_edit_gtk.py); [test_existing_destination_is_preserved_and_busy_state_is_released](../tests/test_copy_edit_gtk.py); [test_nested_field_inherits_read_only_and_max_length](../tests/test_pdf_changes.py); [test_form_max_length_and_value_types_are_enforced](../tests/test_pdf_changes.py); [test_final_name_is_absent_while_real_copy_is_in_progress](../tests/test_sync_folders.py); [test_save_copy_uses_worker_preserves_original_and_only_confirms_local_save](../tests/test_sync_folders_gtk.py); [test_info_distinguishes_checkbox_radio_choice_combo_and_multiselect](../tests/test_advanced_edits.py); [test_checkbox_sets_and_clears_value_and_visible_appearance](../tests/test_advanced_edits.py); [test_radio_activates_only_the_selected_widget_and_can_clear](../tests/test_advanced_edits.py); [test_radio_no_toggle_off_is_enforced](../tests/test_advanced_edits.py); [test_single_and_combo_values_indices_and_generated_appearances_roundtrip](../tests/test_advanced_edits.py); [test_multiselect_uses_export_values_and_canonical_indices](../tests/test_advanced_edits.py); [test_choice_selection_can_be_cleared](../tests/test_advanced_edits.py); [test_invalid_values_do_not_publish_partial_batch](../tests/test_advanced_edits.py); [test_read_only_and_unsupported_button_appearance_are_explicit](../tests/test_advanced_edits.py); [test_editable_combo_and_duplicate_exports_are_rejected](../tests/test_advanced_edits.py); [test_inherited_checkbox_flags_and_type_are_respected](../tests/test_advanced_edits.py); [test_checkbox_widget_absent_from_pages_is_unsupported](../tests/test_advanced_edits.py); [test_closed_outline_counts_remain_closed_after_move](../tests/test_advanced_edits.py); [test_move_preserves_subtree_destinations_and_sibling_links](../tests/test_advanced_edits.py); [test_move_child_to_root_and_reorder_same_parent](../tests/test_advanced_edits.py); [test_delete_bookmark_removes_subtree_and_last_root](../tests/test_advanced_edits.py); [test_move_into_descendant_invalid_positions_and_boolean_paths_are_refused](../tests/test_advanced_edits.py); [test_highlight_and_rectangle_roundtrip_geometry_print_flags_and_text](../tests/test_advanced_edits.py); [test_delete_supported_annotation_preserves_widgets_and_other_pages](../tests/test_advanced_edits.py); [test_locked_notes_widgets_and_replies_are_not_deleted](../tests/test_advanced_edits.py); [test_invalid_annotation_geometry_and_extra_parameters_are_rejected](../tests/test_advanced_edits.py); [test_undo_redo_rebuild_actual_pdfs_and_save_current_cursor_only](../tests/test_edit_history.py); [test_undo_all_restores_base_and_disables_save_until_redone](../tests/test_edit_history.py); [test_new_branch_discards_redo_but_invalid_branch_preserves_it](../tests/test_edit_history.py); [test_operation_values_are_defensively_copied](../tests/test_edit_history.py); [test_changed_original_blocks_add_undo_redo_and_save](../tests/test_edit_history.py); [test_existing_destination_is_not_overwritten_and_draft_survives](../tests/test_edit_history.py); [test_closed_session_refuses_work_and_removes_private_previews](../tests/test_edit_history.py); [test_pre_cancelled_session_does_not_start_worker](../tests/test_edit_history.py); [test_buttons_undo_redo_save_selected_history_and_preserve_prior_copy](../tests/test_edit_draft_gtk.py); [test_real_form_dialog_checkbox_radio_list_and_multiselect](../tests/test_edit_draft_gtk.py); [test_real_move_and_delete_bookmark_dialogs_use_updated_paths](../tests/test_edit_draft_gtk.py); [test_real_area_annotation_dialog_and_delete_keep_other_annotations](../tests/test_edit_draft_gtk.py); [test_failed_operation_and_existing_destination_keep_history_usable](../tests/test_edit_draft_gtk.py); [test_cancel_dialog_and_reopen_parent_close_draft_without_publishing](../tests/test_edit_draft_gtk.py); [test_cancelling_save_and_repeated_clicks_do_not_duplicate_writes](../tests/test_edit_draft_gtk.py); [test_saved_form_and_highlight_render_with_poppler](../tests/test_edit_draft_gtk.py); [test_paths_follow_som_indices_and_skip_groups](../tests/test_pdf_xfa.py); [test_doctype_entities_malformed_and_depth_are_refused](../tests/test_pdf_xfa.py); [test_field_count_value_length_and_size_are_bounded](../tests/test_pdf_xfa.py); [test_hybrid_packet_array_is_listed_without_changing_the_file](../tests/test_pdf_xfa.py); [test_elements_split_across_packets_use_the_joined_document](../tests/test_pdf_xfa.py); [test_text_fill_updates_acroform_and_datasets_and_preserves_the_rest](../tests/test_pdf_xfa.py); [test_calculated_values_are_mirrored_too](../tests/test_pdf_xfa.py); [test_unbound_field_other_operations_and_xfa_only_are_refused_without_output](../tests/test_pdf_xfa.py); [test_only_bound_fields_are_offered_and_value_reaches_the_operation](../tests/test_xfa_gtk.py).

### Contratos individuais de operações

#### `forms/text` — Preencher campo Tx

Estado: `current_bounded_source`; base: `current_linuxit_source`.

**Entradas:** Mapa de 1–256 campos terminais /Tx para strings e cópia nova.

**Saídas:** /V e aparência de widgets atualizados; em híbridos suportados espelha datasets XFA.

**Limites:** ReadOnly/MaxLen herdados; texto até 64 KiB; campo com referência indireta e widgets de página.

**Erros:** Campo inexistente, readonly, MaxLen excedido ou widget não localizável → erro sem cópia parcial.

**Estado e efeitos:** Preenche cópia verificada, não executa JavaScript nem muda original.

**Cancelamento:** Cancelar entrada não adiciona operação; desfazer volta a valores anteriores no rascunho.

Fontes/requisitos: [app/pdf_changes.py — _apply](../app/pdf_changes.py).

Planos relacionados da família: S12-15-1, S12-15-2, S12-15-3, S12-15-4, S12-15-5, S12-15-6, S12-15-7, S12-15-8, S12-15-9, S12-15-10, S12-15-11. Não são aceitação completa desta operação. Nova execução neste registro: `not_run`; expectativa e observação integral Foxit: `null`.

#### `forms/checkbox` — Marcar/desmarcar checkbox

Estado: `current_bounded_source`; base: `current_linuxit_source`.

**Entradas:** Mapa de controles, nome de checkbox e valor booleano real.

**Saídas:** /V e /AS mudam entre /Off e estado ligado já existente.

**Limites:** Exige aparências Off/On válidas, até 128 widgets por controle e 256 controles por operação.

**Erros:** String 'true', ReadOnly ou aparências incompatíveis → recusa.

**Estado e efeitos:** Atualiza valor/aparência da cópia, sem redesenhar aparência de botão inexistente.

**Cancelamento:** Cancelamento do diálogo conserva seleção; histórico desfaz preenchimento antes de save.

Fontes/requisitos: [app/pdf_form_controls.py — fill_controls](../app/pdf_form_controls.py).

Planos relacionados da família: S12-15-1, S12-15-2, S12-15-3, S12-15-4, S12-15-5, S12-15-6, S12-15-7, S12-15-8, S12-15-9, S12-15-10, S12-15-11. Não são aceitação completa desta operação. Nova execução neste registro: `not_run`; expectativa e observação integral Foxit: `null`.

#### `forms/radio` — Selecionar radio simples

Estado: `current_bounded_source`; base: `current_linuxit_source`.

**Entradas:** Nome de grupo radio e estado exportado existente ou Off permitido.

**Saídas:** Somente widget selecionado fica On, /V do grupo coerente.

**Limites:** NoToggleToOff respeitado; estados repetidos ou grupo sem widgets suportados não aceitos.

**Erros:** Estado ausente ou limpar grupo que proíbe Off → ValueError.

**Estado e efeitos:** Muda seleção do grupo na cópia sem alterar opções originais.

**Cancelamento:** Cancelar diálogo conserva grupo; undo/redo restaura seleção anterior.

Fontes/requisitos: [app/pdf_form_controls.py — fill_controls](../app/pdf_form_controls.py).

Planos relacionados da família: S12-15-1, S12-15-2, S12-15-3, S12-15-4, S12-15-5, S12-15-6, S12-15-7, S12-15-8, S12-15-9, S12-15-10, S12-15-11. Não são aceitação completa desta operação. Nova execução neste registro: `not_run`; expectativa e observação integral Foxit: `null`.

#### `forms/combo-fixed` — Selecionar combo sem texto livre

Estado: `current_bounded_source`; base: `current_linuxit_source`.

**Entradas:** Nome do combo de seleção única e opção exportada existente.

**Saídas:** Valor/índice/aparência coerentes; export e label preservados.

**Limites:** Até 512 opções; export/labels duplicados e valores locais ambíguos recusados.

**Erros:** Texto fora de Opt ou campo readonly → erro, sem converter silenciosamente a combo editável.

**Estado e efeitos:** Muda só seleção da cópia; lista Opt preservada.

**Cancelamento:** Cancelar seleção conserva valor; undo remove operação do rascunho.

Fontes/requisitos: [app/pdf_form_controls.py — fill_controls](../app/pdf_form_controls.py).

Planos relacionados da família: S12-15-1, S12-15-2, S12-15-3, S12-15-4, S12-15-5, S12-15-6, S12-15-7, S12-15-8, S12-15-9, S12-15-10, S12-15-11. Não são aceitação completa desta operação. Nova execução neste registro: `not_run`; expectativa e observação integral Foxit: `null`.

#### `forms/list-single` — Selecionar lista simples

Estado: `current_bounded_source`; base: `current_linuxit_source`.

**Entradas:** Lista de uma opção exportada ou lista vazia para limpeza.

**Saídas:** /V único ou vazio e /I coerente com aparências.

**Limites:** Campo lista de seleção única; no máximo um valor e opções até 512.

**Erros:** Dois valores, repetidos ou ausentes nas opções → ValueError.

**Estado e efeitos:** Atualiza seleção/limpeza na cópia e widgets ligados.

**Cancelamento:** Cancelar diálogo conserva índice; undo/redo opera sobre rascunho.

Fontes/requisitos: [app/pdf_form_controls.py — fill_controls](../app/pdf_form_controls.py).

Planos relacionados da família: S12-15-1, S12-15-2, S12-15-3, S12-15-4, S12-15-5, S12-15-6, S12-15-7, S12-15-8, S12-15-9, S12-15-10, S12-15-11. Não são aceitação completa desta operação. Nova execução neste registro: `not_run`; expectativa e observação integral Foxit: `null`.

#### `forms/list-multiple` — Selecionar lista múltipla

Estado: `current_bounded_source`; base: `current_linuxit_source`.

**Entradas:** Lista de valores exportados distintos para um controle MultiSelect.

**Saídas:** /V e /I canônicos na ordem de opções, sem duplicação.

**Limites:** Até 512 opções; readonly e referências de widgets verificadas.

**Erros:** Duplicata/valor ausente/controle single → erro sem gravar subconjunto válido parcial.

**Estado e efeitos:** Preenche conjunto na cópia; não reorganiza opções originais.

**Cancelamento:** Cancelar confirmação conserva conjunto anterior; histórico desfaz lote.

Fontes/requisitos: [app/pdf_form_controls.py — fill_controls](../app/pdf_form_controls.py).

Planos relacionados da família: S12-15-1, S12-15-2, S12-15-3, S12-15-4, S12-15-5, S12-15-6, S12-15-7, S12-15-8, S12-15-9, S12-15-10, S12-15-11. Não são aceitação completa desta operação. Nova execução neste registro: `not_run`; expectativa e observação integral Foxit: `null`.

#### `forms/combo-editable` — Preencher combo com texto livre

Estado: `current_bounded_source`; base: `current_linuxit_source`.

**Entradas:** Campo Combo+Edit de seleção única e texto livre fora ou dentro de Opt.

**Saídas:** /V livre com aparência gerada e /I somente quando corresponde à opção.

**Limites:** Até 4096 bytes por texto, sem controles ASCII; conserva Opt e ReadOnly.

**Erros:** MultiSelect, readonly ou texto excessivo → ValueError; não exige opção preexistente.

**Estado e efeitos:** Cria aparência do texto próprio na cópia; não executa eventos desconhecidos.

**Cancelamento:** Cancelar diálogo conserva texto; undo reconstrói valor anterior.

Fontes/requisitos: [app/pdf_form_controls.py — fill_controls](../app/pdf_form_controls.py), [app/pdf_form_controls.py — describe_control](../app/pdf_form_controls.py).

Planos relacionados da família: S12-15-1, S12-15-2, S12-15-3, S12-15-4, S12-15-5, S12-15-6, S12-15-7, S12-15-8, S12-15-9, S12-15-10, S12-15-11. Não são aceitação completa desta operação. Nova execução neste registro: `not_run`; expectativa e observação integral Foxit: `null`.

#### `forms/events` — Calcular e validar eventos de formulário

Estado: `current_bounded_source`; base: `current_linuxit_source`.

**Entradas:** Valores de entrada e /AA de cálculo/validação/formatação reconhecidos. Extensão A6: comando separado fill-form-javascript, opt-in, com values textuais para campos /Tx e eventos K/V/C/F.

**Saídas:** Valores calculados e aparências numéricas/data/máscara; /V mantém dado sem formatação quando adequado. QuickJS-NG executa JavaScript ECMAScript real no subconjunto event/getField/numFields/getNthFieldName e helpers AF admitidos; falha de script recusa lote completo. O comando declarativo anterior permanece separado.

**Limites:** Gramática fechada AFSimple/AFRange/AFNumber/AFDate numérico/AFSpecial; até 128 regras e script 16384; não é motor JS geral. QuickJS 0.15.1.1: CPU 1s, heap32MiB, stack512KiB e timeout externo6s; sem callbacks Python, filesystem/rede/DOM; sem scripts document/open/page e sem API Acrobat universal.

**Erros:** Ciclo, campo inexistente, script fora da gramática ou validação falha → recusa de todo lote.; API JS não suportada, event.rc=false, script acima de tempo/memória ou dependência QuickJS ausente → Erro atômico, sem executar a ação desconhecida nem publicar campos parcialmente alterados.

**Estado e efeitos:** Interpretação declarativa em cópia atômica; sem eval, rede ou chamadas JavaScript.

**Cancelamento:** Cancelar diálogo não calcula; worker pode ser cancelado antes da cópia final, sem persistir metade dos campos.

Fontes/requisitos: [app/pdf_form_events.py — calculate_form_values](../app/pdf_form_events.py), [app/pdf_form_events.py — inspect_form_events](../app/pdf_form_events.py), [app/pdf_form_javascript.py — run_form_javascript](../app/pdf_form_javascript.py).

Planos relacionados da família: S12-15-1, S12-15-2, S12-15-3, S12-15-4, S12-15-5, S12-15-6, S12-15-7, S12-15-8, S12-15-9, S12-15-10, S12-15-11. Não são aceitação completa desta operação. Nova execução neste registro: `not_run`; expectativa e observação integral Foxit: `null`.

#### `forms/xfa` — Processar XFA

Estado: `current_bounded_source`; base: `current_linuxit_source`.

**Entradas:** XDP único ou array de pacotes; datasets e nomes SOM; híbrido AcroForm para edição suportada. Extensão A6: create_xfa_flow_copy com hash, values por SOM e instances add/remove em grupo repetido; destino novo.

**Saídas:** Detecção/dynamic flag, valores somente leitura; espelhamento de texto híbrido com XML preservado fora dos trechos editados. Cópia com layout fluido próprio top-to-bottom, subform repetido por occur min/max, datasets e AcroForm/AP coerentes; não renderiza template XFA arbitrário.

**Limites:** Inspeção/espelhamento híbrido:8MiB,64 pacotes/níveis,5000 valores,4096 por valor; não executa template/script. Layout fluido próprio fica no comando A6 separado, sem renderizar XFA arbitrário. Até100 páginas/5000 linhas,256 valores/100 operações de instância; sem scripts/FormCalc, positioned layout, binding complexo ou Unicode fora de CP1252. Original cifrado/assinado recusado.

**Erros:** DOCTYPE/entidades, XFA-only para escrita, rich text ou binding dataRef/global → Recusa no espelhamento híbrido básico; XFA-only/layout fluido só no comando separado A6 se todo o modelo suportado for validado.; XFA com layout/script/binding não suportado ou repetição fora de min/max → Recusar cópia fluida inteira; não executar XML/script nem converter silenciosamente só campos conhecidos.

**Estado e efeitos:** Inspeção passiva; edição híbrida suportada grava cópia e verifica igualdade AcroForm/datasets.

**Cancelamento:** Parser XML é síncrono; worker/diálogo canceláveis antes do commit; nenhum script XFA roda.

Fontes/requisitos: [app/pdf_xfa.py — inspect_xfa](../app/pdf_xfa.py), [app/pdf_xfa.py — write_field_values](../app/pdf_xfa.py), [app/pdf_xfa_flow.py — create_xfa_flow_copy](../app/pdf_xfa_flow.py).

Planos relacionados da família: S12-15-1, S12-15-2, S12-15-3, S12-15-4, S12-15-5, S12-15-6, S12-15-7, S12-15-8, S12-15-9, S12-15-10, S12-15-11. Não são aceitação completa desta operação. Nova execução neste registro: `not_run`; expectativa e observação integral Foxit: `null`.


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

- **S12-16-1** (nominal, contrato próprio atual, `passed`): dado anexos-simples.pdf e uma pasta existente nova e vazia. Ação: Listar, usar o índice e SHA-256 devolvidos e extrair nota-sintetica.txt. Esperado: Bytes, tamanho e hash coincidem com anexos-simples.json; nada é executado. Execução própria em 2026-10-21T21:24:39-03:00, revisão `ac89254204fb`, fronteira worker attachments/extract-attachment: [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e31.json).
- **S12-16-2** (exception, contrato próprio atual, `passed`): dado Nome de anexo ../fora.txt. Ação: Extrair. Esperado: A listagem marca o nome como não permitido e a extração falha sem criar arquivo fora ou dentro da pasta. Execução própria em 2026-10-21T21:24:39-03:00, revisão `ac89254204fb`, fronteira worker attachments/extract-attachment: [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e31.json).

**Lacunas da referência Foxit**

- D16 synthetic listing/extraction22bytes/hash observed; full policies and availability remain open.
- Portfolios and nonempty-password attachment workflow remain unsupported; desktop/accessibility pending.

**Observação parcial preservada do original:** Anexo sintético listado/extraído,22bytes/hash iguais; políticas/portfólios completos abertos.

Evidências: [docs/VM-FOXIT-2026-10-18.md](../docs/VM-FOXIT-2026-10-18.md).

Fontes: [app/pdf_attachments.py](../app/pdf_attachments.py), [app/worker_cli.py](../app/worker_cli.py), [app/attachment_tasks.py](../app/attachment_tasks.py), [app/main.py](../app/main.py), [testes/resultados/0.1.16/validation-review.json](../testes/resultados/0.1.16/validation-review.json), [docs/FOXIT-REA.md](../docs/FOXIT-REA.md), [docs/VM-FOXIT-2026-10-18.md](../docs/VM-FOXIT-2026-10-18.md).

Testes próprios existentes, sem nova execução nesta tabela: [test_listing_keeps_duplicate_entries_and_does_not_decode_payloads](../tests/test_pdf_attachments.py); [test_extract_preserves_binary_content_hash_and_original](../tests/test_pdf_attachments.py); [test_unsafe_pdf_names_are_reported_and_refused_without_writes](../tests/test_pdf_attachments.py); [test_worker_protocol_lists_extracts_and_reports_conflict](../tests/test_pdf_attachments.py); [test_stale_listing_callback_cannot_replace_a_new_document](../tests/test_attachment_tasks.py); [test_real_worker_extracts_selected_attachment_and_restores_buttons](../tests/test_attachment_tasks.py); [test_refresh_invalidates_the_selection_captured_before_a_dialog](../tests/test_attachment_tasks.py); [test_panel_saves_selected_file_and_shows_conflict_without_overwrite](../tests/test_attachment_panel_gtk.py); [test_sidebar_buttons_switch_hide_and_restore_without_recursive_callbacks](../tests/test_attachment_panel_gtk.py); [test_long_attachment_name_keeps_header_and_save_button_inside_panel](../tests/test_sidebar_layout_gtk.py); [test_nested_tree_preserves_duplicate_name_indices_and_bytes](../tests/test_attachment_trees.py).

Relacionados aos planos dinâmicos/UI: D16.

### Contratos individuais de operações

#### `attachments/list` — Listar catálogo/árvores/anotações

Estado: `current_bounded_source`; base: `current_linuxit_source`.

**Entradas:** PDF legível da sessão, catálogo EmbeddedFiles/Kids e FileAttachment de página.

**Saídas:** Índices, nomes, origem catalog/annotation, página e identidade sem decodificar payload na listagem.

**Limites:** Até 1000 anexos, 4000 nós e profundidade 64; lista não prova payload íntegro.

**Erros:** Árvore cíclica, nó misturando Kids/Names ou FileSpec inválido → erro sem lista completa fictícia.

**Estado e efeitos:** Somente leitura dos metadados e estado de seleção do painel.

**Cancelamento:** Refresh em worker; fechar/trocar documento invalida listagem antiga por geração.

Fontes/requisitos: [app/pdf_attachments.py — list_attachments](../app/pdf_attachments.py).

Planos relacionados da família: S12-16-1, S12-16-2. Não são aceitação completa desta operação. Nova execução neste registro: `not_run`; expectativa e observação integral Foxit: `null`.

#### `attachments/extract` — Extrair anexo sem sobrescrever

Estado: `current_bounded_source`; base: `current_linuxit_source`.

**Entradas:** Índice do anexo, SHA-256 do hospedeiro e pasta de destino nova.

**Saídas:** Bytes do payload e recibo de arquivo extraído conferidos.

**Limites:** Até 64 MiB por payload após decodificar; nome seguro até 240 bytes; não executa anexo.

**Erros:** Nome com caminho/reservado, destino existente ou fonte alterada → recusa sem sobrescrita.

**Estado e efeitos:** Publica arquivo explícito em pasta escolhida; anexo original preservado.

**Cancelamento:** Extração já autorizada pode concluir após troca de documento sem atualizar status do novo; timeout pede conferir destino.

Fontes/requisitos: [app/pdf_attachments.py — extract_attachment](../app/pdf_attachments.py).

Planos relacionados da família: S12-16-1, S12-16-2. Não são aceitação completa desta operação. Nova execução neste registro: `not_run`; expectativa e observação integral Foxit: `null`.

#### `attachments/portfolio` — Abrir portfólio completo

Estado: `current_bounded_source`; base: `current_linuxit_source`.

**Entradas:** PDF com /Collection dicionário válido e EmbeddedFiles suportados.

**Saídas:** Inventário e extração dos anexos com mesmos IDs/controles; não implementa navegador universal de portfólio.

**Limites:** Esquemas, apresentação e ações particulares do portfólio não são executados.

**Erros:** /Collection não dicionário ou árvore de anexos inválida → erro, não portfólio vazio fictício.

**Estado e efeitos:** Leitura passiva/listagem; extração só por escolha explícita.

**Cancelamento:** Cancelamento da listagem/worker não muda portfólio; extração publicada precisa tratamento independente.

Fontes/requisitos: [app/pdf_attachments.py — list_attachments](../app/pdf_attachments.py), [app/pdf_attachments.py — _document](../app/pdf_attachments.py).

Planos relacionados da família: S12-16-1, S12-16-2. Não são aceitação completa desta operação. Nova execução neste registro: `not_run`; expectativa e observação integral Foxit: `null`.

#### `attachments/encrypted` — Extrair anexo com senha não vazia

Estado: `current_bounded_source`; base: `current_linuxit_source`.

**Entradas:** Sessão autenticada e permissão de extração, ou PDF com senha vazia válida no backend direto.

**Saídas:** Listagem sobre representação privada; extração autorizada conforme política original.

**Limites:** Senha é da sessão, não argumento de linha de comando; liberação de lease só após leitura terminar.

**Erros:** PDF exige senha sem sessão ou /P nega extração ao usuário → erro; owner segue papel autenticado.

**Estado e efeitos:** Usa temporário privado sem publicar versão descifrada do hospedeiro.

**Cancelamento:** Cancelamento fecha lease e invalida callback; extração já confirmada não é apagada ao trocar documento.

Fontes/requisitos: [app/attachment_tasks.py — AttachmentPanelController.refresh](../app/attachment_tasks.py), [app/main.py — PDFWindow._load_side_panels](../app/main.py).

Planos relacionados da família: S12-16-1, S12-16-2. Não são aceitação completa desta operação. Nova execução neste registro: `not_run`; expectativa e observação integral Foxit: `null`.


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

- **S12-17-1** (nominal, contrato próprio atual, `passed`): dado PDF não criptografado até 64 MiB; até 16 campos Sig; CMS DER até 2 MiB; quatro intervalos ByteRange válidos. Ação: Executar o subconjunto local descrito. Esperado: Status de integridade, cobertura da revisão/arquivo atual e trust_chain_verified=false; sem modificação do PDF ou rede. Execução própria em 2026-10-21T21:24:39-03:00, revisão `ac89254204fb`, fronteira worker sign-copy/signature-info: [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e31.json).
- **S12-17-2** (exception, contrato próprio atual, `passed`): dado Entrada inválida ou recurso explicitamente não suportado. Ação: Solicitar a operação local. Esperado: ByteRange/Contents/DER malformado, filtro não suportado ou verificador ausente: status explícito sem aprovação. Execução própria em 2026-10-21T21:24:40-03:00, revisão `ac89254204fb`, fronteira worker signature-info: [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e31.json).
- **S12-17-3** (nominal, contrato próprio atual, `passed`): dado Cópia já assinada (S12-17-1) e a mesma identidade PEM sintética. Ação: Assinar de novo, gerando outra cópia. Esperado: A nova cópia começa com os bytes exatos da assinada; a primeira assinatura continua verificada para a própria revisão (não cobre o arquivo todo) e a segunda cobre o arquivo inteiro. Execução própria em 2026-10-21T21:24:42-03:00, revisão `ac89254204fb`, fronteira worker sign-copy/signature-info (incremental): [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e31.json).
- **S12-17-4** (exception, contrato próprio atual, `passed`): dado PDF sintético com certificação DocMDP P=1 (nenhuma alteração permitida). Ação: Tentar assinar. Esperado: Recusar citando DocMDP P=1, sem criar saída; original preservado. Execução própria em 2026-10-21T21:24:43-03:00, revisão `ac89254204fb`, fronteira worker sign-copy (incremental): [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e31.json).
- **S12-17-5** (nominal, contrato próprio atual, `passed`): dado PDF sintético com carimbo de documento RFC 3161 de uma TSA sintética local. Ação: Inspecionar as assinaturas sem política e com política offline (CA da TSA e outra CA). Esperado: O campo aparece como carimbo de documento, integridade verificada, cobrindo o arquivo e com horário; confiável só com a CA da TSA; nenhuma rede. Execução própria em 2026-10-21T21:24:44-03:00, revisão `ac89254204fb`, fronteira worker signature-info (document timestamp): [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e31.json).
- **S12-17-6** (exception, contrato próprio atual, `passed`): dado O mesmo PDF carimbado com um byte coberto alterado. Ação: Inspecionar as assinaturas. Esperado: O carimbo não é aprovado e nenhum horário é informado. Execução própria em 2026-10-21T21:24:46-03:00, revisão `ac89254204fb`, fronteira worker signature-info (document timestamp): [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e31.json).
- **S12-17-7** (nominal, contrato próprio atual, `passed`): dado PDF assinado por um certificado emitido por uma CA intermediária ausente da assinatura; depois, revisão com DSS contendo o intermediário e as CRLs da cadeia. Ação: Verificar com política offline que escolhe só a CA raiz e exige revogação. Esperado: Sem DSS a cadeia não fecha; com DSS a cadeia e a revogação são verificadas offline, e o resumo do DSS aparece (1 certificado, 2 CRLs); nenhuma rede. Execução própria em 2026-10-21T21:24:47-03:00, revisão `ac89254204fb`, fronteira worker signature-info (trust policy + DSS): [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e31.json).
- **S12-17-8** (exception, contrato próprio atual, `passed`): dado A mesma cadeia, com a CRL do DSS revogando o certificado do signatário. Ação: Verificar com a mesma política. Esperado: Integridade e cadeia verificadas, revogação não; a política não é satisfeita. Execução própria em 2026-10-21T21:24:48-03:00, revisão `ac89254204fb`, fronteira worker signature-info (trust policy + DSS): [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e31.json).

**Lacunas da referência Foxit**

- Fluxos Reader, assinatura versus validação, cadeias, políticas e comportamento offline; plugins não provam suporte completo.

Fontes: [app/pdf_signatures.py](../app/pdf_signatures.py), [app/signature_window.py](../app/signature_window.py), [app/search_tasks.py](../app/search_tasks.py), [app/worker_cli.py](../app/worker_cli.py), [app/main.py](../app/main.py), [docs/SEGURANCA-ACESSIBILIDADE.md](../docs/SEGURANCA-ACESSIBILIDADE.md), [app/pdf_signing.py](../app/pdf_signing.py), [app/signature_trust.py](../app/signature_trust.py), [testes/resultados/0.1.16/validation-review.json](../testes/resultados/0.1.16/validation-review.json), [docs/FOXIT-REA.md](../docs/FOXIT-REA.md).

Testes próprios existentes, sem nova execução nesta tabela: [test_real_detached_cms_integrity_is_separate_from_certificate_trust](../tests/test_pdf_signatures.py); [test_modified_signed_bytes_fail_cryptographic_verification](../tests/test_pdf_signatures.py); [test_appended_bytes_report_only_signed_revision_coverage](../tests/test_pdf_signatures.py); [test_unsupported_filter_or_invalid_byte_range_never_report_verified](../tests/test_pdf_signatures.py); [test_der_bounds_and_padding_are_checked](../tests/test_pdf_signatures.py); [test_unsigned_fields_and_count_limit_are_explicit](../tests/test_pdf_signatures.py); [test_encrypted_pdf_input_size_and_invalid_request_are_refused](../tests/test_pdf_signatures.py); [test_missing_verifier_and_source_changes_do_not_approve_integrity](../tests/test_pdf_signatures.py); [test_real_worker_roundtrip_and_cancelled_request](../tests/test_pdf_signatures.py); [test_invalid_worker_confirmation_is_rejected](../tests/test_pdf_signatures.py); [test_integrity_ui_reports_verification_without_certificate_trust](../tests/test_signature_gtk.py); [test_unsigned_and_encrypted_inputs_have_distinct_results](../tests/test_signature_gtk.py); [test_three_signatures_each_cover_their_revision](../tests/test_incremental_signatures.py); [test_cross_reference_stream_source_gets_a_stream_update](../tests/test_incremental_signatures.py); [test_certification_without_changes_usage_rights_and_broken_previous_signature_are_refused](../tests/test_incremental_signatures.py); [test_timestamp_is_recognised_verified_and_trusted_only_with_its_ca](../tests/test_document_timestamps.py); [test_changed_covered_bytes_and_wrong_imprint_fail](../tests/test_document_timestamps.py); [test_signature_after_a_timestamp_keeps_both_valid](../tests/test_document_timestamps.py); [test_intermediate_and_crls_from_dss_complete_the_offline_chain](../tests/test_dss_validation.py); [test_revoked_signer_in_dss_crl_and_dss_root_is_not_an_anchor](../tests/test_dss_validation.py); [test_malformed_dss_is_reported_and_ignored](../tests/test_dss_validation.py).

### Contratos individuais de operações

#### `signatures/inspect` — Inspecionar campos e cobertura assinada

Estado: `current_bounded_source`; base: `current_linuxit_source`.

**Entradas:** PDF local e pedido de inspeção, ByteRange/Contents dos campos de assinatura.

**Saídas:** Estado por assinatura/revisão, cobertura integral da revisão versus arquivo atual, avisos e metadados.

**Limites:** Fonte até 64 MiB; aceita dois intervalos cujo vão contém somente Contents hexadecimal; cifrados recusados.

**Erros:** ByteRange fora da revisão ou Contents divergente → assinatura inválida/diagnóstico, sem aprovado fictício.

**Estado e efeitos:** Somente leitura e temporários de verificação; não altera assinatura.

**Cancelamento:** invoke_signature_inspection aceita cancel; resultado velho não atualiza outro documento.

Fontes/requisitos: [app/pdf_signatures.py — inspect_pdf_signatures](../app/pdf_signatures.py).

Planos relacionados da família: S12-17-1, S12-17-2, S12-17-3, S12-17-4, S12-17-5, S12-17-6, S12-17-7, S12-17-8. Não são aceitação completa desta operação. Nova execução neste registro: `not_run`; expectativa e observação integral Foxit: `null`.

#### `signatures/cms-integrity` — Verificar integridade CMS offline

Estado: `current_bounded_source`; base: `current_linuxit_source`.

**Entradas:** CMS destacado DER e bytes exatos cobertos pela revisão.

**Saídas:** Integridade criptográfica válida/inválida/indisponível separada de confiança.

**Limites:** Suporta CMS destacado esperado; verificação por OpenSSL ou mecanismo Windows; nenhuma validade jurídica inferida.

**Erros:** DER truncado, assinatura incorreta ou backend indisponível → falha/indisponível, não certificado confiável.

**Estado e efeitos:** Pode criar temporários e subprocesso, sem rede e sem fonte regravada.

**Cancelamento:** Cancelamento do chamador encerra worker; verificação já feita não é uma operação de assinatura.

Fontes/requisitos: [app/pdf_signatures.py — _verify_detached](../app/pdf_signatures.py).

Planos relacionados da família: S12-17-1, S12-17-2, S12-17-3, S12-17-4, S12-17-5, S12-17-6, S12-17-7, S12-17-8. Não são aceitação completa desta operação. Nova execução neste registro: `not_run`; expectativa e observação integral Foxit: `null`.

#### `signatures/sign` — Assinar documento

Estado: `current_bounded_source`; base: `current_linuxit_source`.

**Entradas:** PDF e certificado/chave PEM selecionados, senha opcional e novo destino.

**Saídas:** CMS SHA-256 invisível adbe.pkcs7.detached em revisão incremental da fonte exata.

**Limites:** Até 15 assinaturas existentes; anteriores devem verificar; reserva CMS 32768; sem LTV automático.

**Erros:** DocMDP P=1, UR3, cifrado, XFA, portfólio, chave inválida ou assinatura anterior inválida → recusa.

**Estado e efeitos:** Anexa revisão em cópia preservando bytes anteriores; reabre e verifica cobertura e assinaturas.

**Cancelamento:** Worker cancelável antes da publicação; nunca apagar fonte nem revogar cópia já assinada por cancelar UI depois.

Fontes/requisitos: [app/pdf_signing.py — sign_pdf_copy](../app/pdf_signing.py).

Planos relacionados da família: S12-17-1, S12-17-2, S12-17-3, S12-17-4, S12-17-5, S12-17-6, S12-17-7, S12-17-8. Não são aceitação completa desta operação. Nova execução neste registro: `not_run`; expectativa e observação integral Foxit: `null`.

#### `signatures/trust` — Validar cadeia/confiança/revogação

Estado: `current_bounded_source`; base: `current_linuxit_source`.

**Entradas:** CMS/conteúdo, CA e CRL locais explícitos e data com fuso; DSS opcional.

**Saídas:** Cadeia, revogação e integridade separados; DSS Certs só ajuda cadeia não confiável por si. Extensão A6: OCSP DER local/DSS é verificado offline; estado good+fresh autenticado exigido para não-âncoras sob a política aplicável, revoked prevalece.

**Limites:** 1–16 raízes/até16 CRLs explícitas, arquivos até1MiB; até8 signatários/64 certs; DSS Certs ajuda cadeia sem virar âncora; OCSP local é tratado pela extensão A6; VRI não estabelece PAdES-LTA completo. OCSP: até32 respostas DER locais,1MiB cada; ausência/tempo/assinatura não verificável não vira estado good; não consulta responder online.

**Erros:** CA sem CA=true, data sem fuso, CRL incompatível ou OpenSSL ausente → erro/estado indeterminado, sem confiança automática.

**Estado e efeitos:** Verificação offline, sem obter certificado pessoal/rede; âncoras só as selecionadas.

**Cancelamento:** Cancelamento do worker interrompe consulta; nunca transforma timeout em revogado ou confiável.

Fontes/requisitos: [app/signature_trust.py — verify_trust](../app/signature_trust.py).

Planos relacionados da família: S12-17-1, S12-17-2, S12-17-3, S12-17-4, S12-17-5, S12-17-6, S12-17-7, S12-17-8. Não são aceitação completa desta operação. Nova execução neste registro: `not_run`; expectativa e observação integral Foxit: `null`.

#### `signatures/timestamp-ltv` — Processar carimbo de tempo/PAdES/LTV

Estado: `current_bounded_source`; base: `current_linuxit_source`.

**Entradas:** Token RFC3161 existente em CMS ou DocTimeStamp e bytes cobertos, CA local opcional. Extensão A6: append_dss_copy com certificados/CRL/OCSP locais; prepare_document_timestamp com pasta nova e complete_document_timestamp com TimeStampResp DER, destino e trust_policy explícita.

**Saídas:** Assinatura/imprint verificados, generationTime só confiável quando validado e TSA avaliada pela CA explícita. DSS incremental preservando bytes e VRI anterior, deduplicação global; preparação offline cria manifest/document.pending/timestamp.tsq com nonce128/SHA256; conclusão valida nonce/imprint/TSA/CA e publica DocTimeStamp incremental.

**Limites:** SHA-256/384/512; inspeção não cria carimbo nem DSS/LTV; OCSP online fora deste subconjunto. Sem contato TSA/OCSP/AIA automático; PDF64MiB, item1MiB, token32KiB, até64 certificados/32CRLs/32OCSP; exige assinatura anterior verificada, recusa DocMDP P1/UR3/cifrado/XFA/portfólio. Não é garantia PAdES-LTA universal.

**Erros:** TSTInfo ausente, algoritmo não suportado ou imprint errado → carimbo inválido; relógio local não substitui TSA.; TimeStampResp com nonce/imprint/assinatura/CA incompatíveis ou DSS excedendo orçamento → Recusar publicação incremental; preservar fonte e kit preparado para inspeção, sem confiar no relógio local como TSA.

**Estado e efeitos:** Somente lê token e DSS; nenhum registro novo de longo prazo é escrito.

**Cancelamento:** Worker cancelável, sem publicação; cancelamento deixa análise incompleta explicitamente.

Fontes/requisitos: [app/pdf_signatures.py — _verify_document_timestamp](../app/pdf_signatures.py), [app/signature_trust.py — verify_document_timestamp](../app/signature_trust.py), [app/pdf_preservation.py — append_dss_copy](../app/pdf_preservation.py), [app/pdf_preservation.py — prepare_document_timestamp](../app/pdf_preservation.py), [app/pdf_preservation.py — complete_document_timestamp](../app/pdf_preservation.py).

Planos relacionados da família: S12-17-1, S12-17-2, S12-17-3, S12-17-4, S12-17-5, S12-17-6, S12-17-7, S12-17-8. Não são aceitação completa desta operação. Nova execução neste registro: `not_run`; expectativa e observação integral Foxit: `null`.


<a id="security"></a>

## Senhas/permissões/RMS

Atual (0.1.16): abrir com senha conhecida em sessão autenticada (0.1.14), inspecionar permissões, criar cópia AES-256 ou sem criptografia com senha de proprietário, e editar/imprimir documento cifrado conforme as permissões, preservando criptografia, senhas e permissões na cópia (RC4-128, AES-128, AES-256-R5 e AES-256 conferidos). Fluxo de pasta preferida/sincronizada com cópias de publicação exclusiva. RMS, outros perfis de cifra e cliente sincronizador real continuam abertos. Corpus de criptografia (etapa E18, testes/fixtures/criptografia/): RC4-40, RC4-128, AES-128, AES-256 (R6) e AES-128 com /EncryptMetadata false, cada um aberto com senha de usuário/proprietário/errada/ausente, editado preservando V/R/Length/P/EncryptMetadata e com as permissões do usuário respeitadas, e preparado para impressão a partir da cópia de leitura; metadados XMP em claro (filtro Identity) passaram a ser lidos e regravados corretamente.

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

- **S12-18-1** (nominal, contrato próprio atual, `passed`): dado PDF local sintético até 64 MiB, senha conhecida ou duas senhas novas distintas de 8–64 ASCII imprimíveis. Ação: Executar o subconjunto local descrito. Esperado: Estado de autenticação/role/permissões sem senha no resultado; nova cópia AES-256 R6 verificada ou plaintext somente para owner autenticado. Execução própria em 2026-10-21T21:24:50-03:00, revisão `ac89254204fb`, fronteira worker protect-copy/security-info/owner-copy: [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e31.json).
- **S12-18-2** (exception, contrato próprio atual, `passed`): dado Entrada inválida ou recurso explicitamente não suportado. Ação: Solicitar a operação local. Esperado: Credencial errada, role usuário para exportação plaintext, documento Sig/Perms/XFA/Collection, destino existente ou fonte alterada: recusa explícita. Execução própria em 2026-10-21T21:24:51-03:00, revisão `ac89254204fb`, fronteira worker security-info/owner-copy/protect-copy: [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e31.json).
- **S12-18-3** (nominal, contrato próprio atual, `passed`): dado Corpus próprio testes/fixtures/criptografia/: o mesmo documento de 2 páginas em RC4-40, RC4-128, AES-128, AES-256 e AES-128 com metadados em claro; senha de usuário e de proprietário sintéticas. Ação: Abrir cada perfil com a senha de usuário, adicionar um marcador com a senha de proprietário em cópia nova e preparar impressão a partir da leitura. Esperado: Abre com 2 páginas, texto e título XMP legíveis e as permissões do usuário (imprimir só em baixa qualidade, sem copiar nem modificar); a cópia editada mantém V/R/Length/P/EncryptMetadata, abre com a senha de usuário e tem o marcador; o PDF de impressão tem 2 páginas; originais preservados. Execução própria em 2026-10-21T21:24:52-03:00, revisão `ac89254204fb`, fronteira worker document-open/copy-edit/prepare-print (corpus de criptografia): [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e31.json).
- **S12-18-4** (exception, contrato próprio atual, `passed`): dado Os mesmos cinco perfis. Ação: Abrir sem senha e com senha errada; com a senha de usuário, tentar adicionar um marcador (modificar não permitido). Esperado: Pedir senha, recusar a senha errada e recusar a edição sem criar arquivo; originais preservados. Execução própria em 2026-10-21T21:24:56-03:00, revisão `ac89254204fb`, fronteira worker document-open/copy-edit (corpus de criptografia): [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e31.json).

**Lacunas da referência Foxit**

- Entrada de senha, enforcement de permissões, RMS e mensagens do original; o fluxo completo não está implementado.

**Observação parcial preservada do original:** Cancelar/senha errada anteriores e correta na abertura independenteD15. Permissões/RMS/fluxo universal não observados.

Evidências: [docs/VM-FOXIT-2026-10-18.md](../docs/VM-FOXIT-2026-10-18.md), [docs/VM-SENHA-E-PARADA-2026-10-18.md](../docs/VM-SENHA-E-PARADA-2026-10-18.md).

Fontes: [app/pdf_security.py](../app/pdf_security.py), [app/security_window.py](../app/security_window.py), [app/search_tasks.py](../app/search_tasks.py), [app/worker_cli.py](../app/worker_cli.py), [app/main.py](../app/main.py), [docs/SEGURANCA-ACESSIBILIDADE.md](../docs/SEGURANCA-ACESSIBILIDADE.md), [app/local_files.py](../app/local_files.py), [app/folder_dialogs.py](../app/folder_dialogs.py), [docs/PASTAS-SINCRONIZADAS.md](../docs/PASTAS-SINCRONIZADAS.md), [app/pdf_edit_security.py](../app/pdf_edit_security.py), [testes/resultados/0.1.16/validation-review.json](../testes/resultados/0.1.16/validation-review.json), [app/pdf_crypt_compat.py](../app/pdf_crypt_compat.py), [docs/FOXIT-REA.md](../docs/FOXIT-REA.md), [docs/AVANCO-SEM-VM.md](../docs/AVANCO-SEM-VM.md), [docs/VM-FOXIT-2026-10-18.md](../docs/VM-FOXIT-2026-10-18.md), [docs/VM-SENHA-E-PARADA-2026-10-18.md](../docs/VM-SENHA-E-PARADA-2026-10-18.md).

Testes próprios existentes, sem nova execução nesta tabela: [test_unencrypted_inspection_identity_pages_and_permissions](../tests/test_pdf_security.py); [test_aes256_roundtrip_roles_permissions_metadata_and_attachments](../tests/test_pdf_security.py); [test_each_permission_flag_and_accessibility_bit_are_preserved](../tests/test_pdf_security.py); [test_encrypted_inspection_correct_wrong_and_missing_credentials](../tests/test_pdf_security.py); [test_new_password_limits_and_distinct_roles](../tests/test_pdf_security.py); [test_invalid_protocol_and_permission_types_rejected](../tests/test_pdf_security.py); [test_encrypted_source_not_unprotected_or_rewritten](../tests/test_pdf_security.py); [test_signed_xfa_portfolio_and_permissions_sources_refused](../tests/test_pdf_security.py); [test_stale_source_and_source_size_page_output_limits](../tests/test_pdf_security.py); [test_existing_destination_and_source_never_overwritten](../tests/test_pdf_security.py); [test_handled_partial_write_removed_and_error_sanitized](../tests/test_pdf_security.py); [test_concurrent_destination_preserved](../tests/test_pdf_security.py); [test_real_worker_secret_transport_and_error_channel](../tests/test_pdf_security.py); [test_cancellation_and_invalid_confirmation_never_report_success](../tests/test_pdf_security.py); [test_accessible_text_validation_limit_and_source_change](../tests/test_pdf_security.py); [test_accessible_text_refuses_encrypted_pdf_even_with_empty_password](../tests/test_pdf_security.py); [test_accessible_text_adapter_rejects_invalid_reply_and_supports_cancel](../tests/test_pdf_security.py); [test_only_owner_authentication_can_create_unprotected_copy](../tests/test_pdf_security.py); [test_owner_copy_stale_destination_and_partial_failure_are_safe](../tests/test_pdf_security.py); [test_owner_copy_refuses_special_restrictions_and_signature_fields](../tests/test_pdf_security.py); [test_inspect_protect_and_secrets_cleared_without_source_change](../tests/test_security_accessibility_gtk.py); [test_encrypted_inspection_wrong_and_owner_credentials](../tests/test_security_accessibility_gtk.py); [test_password_mismatch_and_cancelled_destination_create_nothing](../tests/test_security_accessibility_gtk.py); [test_document_change_during_destination_dialog_discards_request](../tests/test_security_accessibility_gtk.py); [test_cancel_and_destroy_stop_actual_security_process](../tests/test_security_accessibility_gtk.py); [test_owner_copy_is_readable_by_main_reader_and_original_is_preserved](../tests/test_security_accessibility_gtk.py); [test_owner_copy_rejects_opening_password_and_clears_it](../tests/test_security_accessibility_gtk.py); [test_final_name_is_absent_while_real_copy_is_in_progress](../tests/test_sync_folders.py); [test_save_copy_uses_worker_preserves_original_and_only_confirms_local_save](../tests/test_sync_folders_gtk.py); [test_fixtures_match_the_manifest_and_independent_readers](../tests/test_encryption_corpus.py); [test_open_with_user_owner_wrong_and_missing_password](../tests/test_encryption_corpus.py); [test_edit_keeps_the_profile_and_follows_user_permissions](../tests/test_encryption_corpus.py); [test_print_preparation_uses_the_reading_copy_and_low_quality_only](../tests/test_encryption_corpus.py).

Relacionados aos planos dinâmicos/UI: D15.

### Contratos individuais de operações

#### `security/inspect` — Autenticar senha conhecida e inspecionar permissões

Estado: `current_bounded_source`; base: `current_linuxit_source`.

**Entradas:** PDF e credencial opcional transmitida em pedido privado.

**Saídas:** Tipo de cifra, papel user/owner, flags de permissão e autenticação.

**Limites:** PDFs suportados pelo parser; não contorna senha nem RMS.

**Erros:** Credencial errada, método não suportado ou fonte alterada → SecurityError sem divulgar segredo.

**Estado e efeitos:** Somente leitura/temporários; sem alteração do arquivo.

**Cancelamento:** invoke_security aceita cancel e timeout; credenciais não ficam no argv/log do worker.

Fontes/requisitos: [app/pdf_security.py — inspect_pdf_security](../app/pdf_security.py).

Planos relacionados da família: S12-18-1, S12-18-2, S12-18-3, S12-18-4. Não são aceitação completa desta operação. Nova execução neste registro: `not_run`; expectativa e observação integral Foxit: `null`.

#### `security/protect` — Criar cópia AES-256

Estado: `current_bounded_source`; base: `current_linuxit_source`.

**Entradas:** PDF suportado não cifrado, senhas e mapa de permissões; destino novo.

**Saídas:** Cópia AES-256 conferida com autenticação e flags solicitadas.

**Limites:** Até 1000 páginas no backend; cryptography requerido; preservar páginas/metadados/anexos no recorte.

**Erros:** Assinado/XFA/portfólio/já cifrado, destino existente ou runtime sem crypto → SecurityError.

**Estado e efeitos:** Cria cópia protegida; fonte continua idêntica; não transmite senhas.

**Cancelamento:** Worker cancelável antes de publicar; pedido concluído não é desfeito ao fechar janela.

Fontes/requisitos: [app/pdf_security.py — protect_pdf_copy](../app/pdf_security.py).

Planos relacionados da família: S12-18-1, S12-18-2, S12-18-3, S12-18-4. Não são aceitação completa desta operação. Nova execução neste registro: `not_run`; expectativa e observação integral Foxit: `null`.

#### `security/owner-copy` — Criar cópia sem cifra com senha de proprietário

Estado: `current_bounded_source`; base: `current_linuxit_source`.

**Entradas:** PDF cifrado, senha de proprietário válida e destino novo.

**Saídas:** Cópia legível autorizada pelo owner com páginas preservadas.

**Limites:** Senha de abertura user sozinha não autoriza remover proteção.

**Erros:** Papel diferente de owner ou cópia não verificável → recusa sem saída final.

**Estado e efeitos:** Publica cópia sem cifra; original cifrado fica intacto.

**Cancelamento:** Cancelar antes do commit elimina temporários; cópia já publicada é arquivo independente.

Fontes/requisitos: [app/pdf_security.py — unprotect_owner_copy](../app/pdf_security.py).

Planos relacionados da família: S12-18-1, S12-18-2, S12-18-3, S12-18-4. Não são aceitação completa desta operação. Nova execução neste registro: `not_run`; expectativa e observação integral Foxit: `null`.

#### `security/enforcement` — Aplicar permissões em todos os fluxos

Estado: `current_bounded_source`; base: `current_linuxit_source`.

**Entradas:** Papel e /P originais da sessão, operação copy/print/modify/annotate/fill/assemble.

**Saídas:** Aceitar ou negar em UI e worker conforme operação e papel autenticado.

**Limites:** RC4-40/128 e AES-128/256 R6 corpus próprio; XMP Identity preservado no recorte; não é RMS.

**Erros:** Permissão negada → erro explícito antes de extrair/imprimir/editar; senha user não equivale a owner.

**Estado e efeitos:** Sessão guarda política original mesmo com representação legível; edição preserva cifra/P/ID no subconjunto.

**Cancelamento:** Cancelar operação nega publicação futura da tarefa, sem alterar política nem permissões do original.

Fontes/requisitos: [app/pdf_attachments.py — _document](../app/pdf_attachments.py), [app/imposition.py — _reader](../app/imposition.py), [app/main.py — PDFWindow._reading_permission](../app/main.py).

Planos relacionados da família: S12-18-1, S12-18-2, S12-18-3, S12-18-4. Não são aceitação completa desta operação. Nova execução neste registro: `not_run`; expectativa e observação integral Foxit: `null`.

#### `security/rms` — Processar proteção RMS autorizada

Estado: `pending_environment_or_reference`; base: `proposed_independent_requirement`.

**Entradas:** Documento RMS e ambiente de serviço/licença legitimamente autorizado.

**Saídas:** Proposta: relatar disponibilidade e permissões do serviço, sem remover proteção.

**Limites:** Sem adaptador RMS implementado/contrato Reader caracterizado; credenciais e serviço externos pendentes.

**Erros:** Serviço/licença indisponível → informar não suportado/indisponível, não tentar contornar proteção.

**Estado e efeitos:** Nenhuma chamada de serviço nesta entrega; sem upload/credencial automática.

**Cancelamento:** Proposta: cancelar antes da autenticação/transação externa e preservar original; comportamento específico ainda não observado.

Fontes/requisitos: [docs/ESCOPO.md](../docs/ESCOPO.md).

Planos relacionados da família: S12-18-1, S12-18-2, S12-18-3, S12-18-4. Não são aceitação completa desta operação. Nova execução neste registro: `not_run`; expectativa e observação integral Foxit: `null`.


<a id="accessibility"></a>

## Acessibilidade/voz

Atual (0.1.16): texto da página em Gtk.TextView/ATK.Text com sessão autenticada, nomes acessíveis, navegação F6/Shift+F6/Ctrl+Shift+T e probe AT-SPI entre processos. Voz local eSpeak PT/EN gera WAV privado e reprodução GStreamer controlada (reproduzir/pausar/parar/volume). Ordem de leitura em colunas (etapa E19): o texto acessível (e a camada de texto de cópias com OCR) é lido coluna por coluna por heurística própria limitada sobre as caixas de linha do Poppler — vão vertical cruzado por poucas linhas, linhas de largura total separando faixas, até três níveis; sem vão claro, de cima para baixo. Tabelas, legendas dentro de colunas, texto girado e estrutura marcada não são analisados. Ordem semântica garantida, leitor de tela real, áudio físico e conformidade integral continuam abertos.

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

- **S12-19-1** (nominal, contrato próprio atual, `passed`): dado PDF não criptografado, página válida e ação do usuário; texto até 1 MiB UTF-8. Ação: Executar o subconjunto local descrito. Esperado: Texto selecionável e acessível da página, status/cancelamento e descarte de resposta obsoleta. Execução própria em 2026-10-21T21:24:59-03:00, revisão `ac89254204fb`, fronteira worker accessible-text: [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e31.json).
- **S12-19-2** (exception, contrato próprio atual, `passed`): dado Entrada inválida ou recurso explicitamente não suportado. Ação: Solicitar a operação local. Esperado: PDF cifrado, limite de texto excedido ou Poppler indisponível: erro explícito sem texto parcial apresentado como completo. Execução própria em 2026-10-21T21:24:59-03:00, revisão `ac89254204fb`, fronteira worker accessible-text: [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e31.json).
- **S12-19-3** (nominal, contrato próprio atual, `passed`): dado PDF sintético de duas colunas com título e rodapé de largura total; no fluxo de conteúdo, a coluna da direita vem antes da esquerda. Ação: Pedir o texto acessível da página. Esperado: Título, as quatro linhas da coluna esquerda, as quatro da direita e o rodapé, nessa ordem; original preservado. Execução própria em 2026-10-21T21:25:00-03:00, revisão `ac89254204fb`, fronteira worker accessible-text (duas colunas): [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e31.json).
- **S12-19-4** (exception, contrato próprio atual, `passed`): dado PDF sintético de uma coluna com linhas de larguras variadas e uma única linha deslocada à direita. Ação: Pedir o texto acessível da página. Esperado: Sem vão claro entre colunas, o texto sai de cima para baixo, sem inventar colunas; original preservado. Execução própria em 2026-10-21T21:25:00-03:00, revisão `ac89254204fb`, fronteira worker accessible-text (uma coluna): [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e31.json).

**Lacunas da referência Foxit**

- APIs, árvore acessível, ordem, voz, foco, atalhos e cobertura real do Reader.

Fontes: [app/accessible_reader.py](../app/accessible_reader.py), [app/pdf_security.py](../app/pdf_security.py), [app/search_tasks.py](../app/search_tasks.py), [app/worker_cli.py](../app/worker_cli.py), [app/main.py](../app/main.py), [docs/SEGURANCA-ACESSIBILIDADE.md](../docs/SEGURANCA-ACESSIBILIDADE.md), [app/speech.py](../app/speech.py), [app/local_playback.py](../app/local_playback.py), [app/media_window.py](../app/media_window.py), [testes/resultados/0.1.16/validation-review.json](../testes/resultados/0.1.16/validation-review.json), [app/reading_order.py](../app/reading_order.py), [app/rendering.py](../app/rendering.py), [docs/FOXIT-REA.md](../docs/FOXIT-REA.md).

Testes próprios existentes, sem nova execução nesta tabela: [test_unencrypted_inspection_identity_pages_and_permissions](../tests/test_pdf_security.py); [test_aes256_roundtrip_roles_permissions_metadata_and_attachments](../tests/test_pdf_security.py); [test_each_permission_flag_and_accessibility_bit_are_preserved](../tests/test_pdf_security.py); [test_encrypted_inspection_correct_wrong_and_missing_credentials](../tests/test_pdf_security.py); [test_new_password_limits_and_distinct_roles](../tests/test_pdf_security.py); [test_invalid_protocol_and_permission_types_rejected](../tests/test_pdf_security.py); [test_encrypted_source_not_unprotected_or_rewritten](../tests/test_pdf_security.py); [test_signed_xfa_portfolio_and_permissions_sources_refused](../tests/test_pdf_security.py); [test_stale_source_and_source_size_page_output_limits](../tests/test_pdf_security.py); [test_existing_destination_and_source_never_overwritten](../tests/test_pdf_security.py); [test_handled_partial_write_removed_and_error_sanitized](../tests/test_pdf_security.py); [test_concurrent_destination_preserved](../tests/test_pdf_security.py); [test_real_worker_secret_transport_and_error_channel](../tests/test_pdf_security.py); [test_cancellation_and_invalid_confirmation_never_report_success](../tests/test_pdf_security.py); [test_accessible_text_validation_limit_and_source_change](../tests/test_pdf_security.py); [test_accessible_text_refuses_encrypted_pdf_even_with_empty_password](../tests/test_pdf_security.py); [test_accessible_text_adapter_rejects_invalid_reply_and_supports_cancel](../tests/test_pdf_security.py); [test_only_owner_authentication_can_create_unprotected_copy](../tests/test_pdf_security.py); [test_owner_copy_stale_destination_and_partial_failure_are_safe](../tests/test_pdf_security.py); [test_owner_copy_refuses_special_restrictions_and_signature_fields](../tests/test_pdf_security.py); [test_real_poppler_text_is_exposed_through_atk_text_interface](../tests/test_security_accessibility_gtk.py); [test_no_text_and_encrypted_pages_have_explicit_limits](../tests/test_security_accessibility_gtk.py); [test_obsolete_page_text_does_not_replace_newer_page](../tests/test_security_accessibility_gtk.py); [test_f6_focus_regions_names_and_list_arrow_delegation](../tests/test_security_accessibility_gtk.py); [test_text_limit_and_document_close_clear_the_accessible_window](../tests/test_security_accessibility_gtk.py); [test_closing_text_worker_terminates_its_real_descendant_on_linux](../tests/test_security_accessibility_gtk.py); [test_two_columns_with_full_width_title_and_footer](../tests/test_reading_order.py); [test_three_columns_and_bands_separated_by_wide_lines](../tests/test_reading_order.py); [test_single_column_and_unclear_gutter_keep_top_to_bottom](../tests/test_reading_order.py); [test_accessible_text_reads_column_by_column](../tests/test_reading_order.py); [test_ocr_copy_text_layer_is_read_column_by_column](../tests/test_reading_order.py).

Relacionados aos planos dinâmicos/UI: UI10.

### Contratos individuais de operações

#### `accessibility/text` — Expor texto da página por ATK.Text

Estado: `current_bounded_source`; base: `current_linuxit_source`.

**Entradas:** Sessão/página autorizada e caixas de linhas Poppler.

**Saídas:** Texto em Gtk.TextView/ATK.Text, ordenado por heurística própria de colunas.

**Limites:** Heurística até três níveis e linhas full-width; não garante ordem semântica de PDF malformado.

**Erros:** Permissão de extração negada → PermissionError; sem texto

**Estado e efeitos:** Janela de leitura e mapa acessível; original intacto.

**Cancelamento:** Carregamento em worker/geração; trocar página/documento descarta texto antigo.

Fontes/requisitos: [app/accessible_reader.py — AccessibleTextWindow](../app/accessible_reader.py).

Planos relacionados da família: S12-19-1, S12-19-2, S12-19-3, S12-19-4. Não são aceitação completa desta operação. Nova execução neste registro: `not_run`; expectativa e observação integral Foxit: `null`.

#### `accessibility/keyboard` — Navegar por regiões pelo teclado

Estado: `current_bounded_source`; base: `current_linuxit_source`.

**Entradas:** Tecla F6/ShiftF6, região de foco atual e controles disponíveis.

**Saídas:** Foco alterna regiões acessíveis com nomes; setas delegadas ao controle adequado.

**Limites:** Atalhos dependem da janela/foco; não substituir navegação interna de campos textuais.

**Erros:** Região oculta/inexistente → escolher região disponível sem foco em widget destruído.

**Estado e efeitos:** Só estado de foco/seleção; nenhuma escrita de arquivo.

**Cancelamento:** Ação síncrona; fechar diálogo restaura foco possível, sem tarefa longa.

Fontes/requisitos: [app/main.py — PDFWindow._focus_region](../app/main.py).

Planos relacionados da família: S12-19-1, S12-19-2, S12-19-3, S12-19-4. Não são aceitação completa desta operação. Nova execução neste registro: `not_run`; expectativa e observação integral Foxit: `null`.

#### `accessibility/screen-reader` — Validar leitor de tela e ordem real

Estado: `pending_environment_or_reference`; base: `proposed_independent_requirement`.

**Entradas:** Desktop Linux real, bus AT-SPI e leitor de tela escolhido.

**Saídas:** Proposta: evidências faladas de foco, ordem, rótulos e mudanças do documento.

**Limites:** Probe AT-SPI próprio não é prova de Orca/áudio real no dispositivo do usuário.

**Erros:** Leitor/bus indisponível ou leitura incorreta → pendente/inconclusivo, não declarar acessibilidade integral.

**Estado e efeitos:** Pode emitir áudio/alterar foco durante campanha específica.

**Cancelamento:** Proposta: parar fala e restaurar foco; a interação real ainda depende do ambiente.

Fontes/requisitos: [docs/EXECUCAO-SEM-VM.md](../docs/EXECUCAO-SEM-VM.md).

Planos relacionados da família: S12-19-1, S12-19-2, S12-19-3, S12-19-4. Não são aceitação completa desta operação. Nova execução neste registro: `not_run`; expectativa e observação integral Foxit: `null`.

#### `accessibility/voice` — Ler em voz alta

Estado: `current_bounded_source`; base: `current_linuxit_source`.

**Entradas:** Texto explícito, voz pt-br/en, velocidade e destino .wav novo ou reprodução escolhida.

**Saídas:** WAV PCM mono e reprodução controlada pelo usuário.

**Limites:** Até 20000 caracteres, 80–300 palavras/minuto e áudio até 64 MiB; eSpeak NG/local requerido.

**Erros:** Voz inválida, eSpeak ausente ou WAV inválido → erro sem áudio concluído falso.

**Estado e efeitos:** Gera WAV local; play explícito pode emitir som; texto não vai à nuvem.

**Cancelamento:** Synthesis via worker cancelável; Stop da reprodução encerra áudio próprio sem encerrar outros sons do host.

Fontes/requisitos: [app/speech.py — export_speech](../app/speech.py).

Planos relacionados da família: S12-19-1, S12-19-2, S12-19-3, S12-19-4. Não são aceitação completa desta operação. Nova execução neste registro: `not_run`; expectativa e observação integral Foxit: `null`.


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

- **S12-20-1** (nominal, contrato próprio atual, `passed`): dado Imagem e página com escala conhecida; pontos separados por 72 pontos PDF. Ação: Medir o segmento horizontal. Esperado: Contrato próprio: 2,54 cm, formatado com duas casas decimais. Execução própria em 2026-10-21T21:25:00-03:00, revisão `ac89254204fb`, fronteira PDFWindow _finish_measure: [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e31.json).
- **S12-20-2** (exception, contrato próprio atual, `passed`): dado Página sem pixbuf/tamanhos disponíveis. Ação: Concluir gesto de medida. Esperado: Nenhuma nova medida válida é publicada. Execução própria em 2026-10-21T21:25:02-03:00, revisão `ac89254204fb`, fronteira PDFWindow _finish_measure: [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e31.json).

**Lacunas da referência Foxit**

- Unidades, calibração, snapping, precisão, áreas e perímetros do original.

Fontes: [app/main.py](../app/main.py), [app/measurement.py](../app/measurement.py), [app/measurement_window.py](../app/measurement_window.py), [testes/resultados/0.1.16/validation-review.json](../testes/resultados/0.1.16/validation-review.json), [docs/FOXIT-REA.md](../docs/FOXIT-REA.md).

### Contratos individuais de operações

#### `measurement/distance` — Medir distância entre pontos

Estado: `current_bounded_source`; base: `current_linuxit_source`.

**Entradas:** Dois pontos da página exibida e transformação PDF, unidade cm por padrão.

**Saídas:** Distância apresentada com duas casas e vírgula: 72 pt = 2,54 cm sem calibração.

**Limites:** Só página exibida; domínio exige dois pontos distintos, finitos e até 2 milhões em módulo.

**Erros:** Sem página ou pontos repetidos → não publicar medida; domínio lança ValueError.

**Estado e efeitos:** Desenha marca/resultado em UI, não grava anotação PDF automaticamente.

**Cancelamento:** Cancelar captura limpa pontos; nova página invalida escala visual anterior.

Fontes/requisitos: [app/main.py — PDFWindow._finish_measure](../app/main.py), [app/measurement.py — measure](../app/measurement.py).

Planos relacionados da família: S12-20-1, S12-20-2. Não são aceitação completa desta operação. Nova execução neste registro: `not_run`; expectativa e observação integral Foxit: `null`.

#### `measurement/calibrate` — Calibrar escala e unidades

Estado: `current_bounded_source`; base: `current_linuxit_source`.

**Entradas:** Dois pontos de referência, comprimento conhecido positivo e unidade mm/cm/m/in/ft.

**Saídas:** Fator mm_por_ponto calculado para medidas seguintes.

**Limites:** Comprimento e fator até 1e12, referência de comprimento positivo; snapping grade 0–1000pt/ângulo 0–180.

**Erros:** Unidade desconhecida ou referência degenerada → ValueError, sem escala infinita.

**Estado e efeitos:** Altera configuração de medição da sessão; não transforma geometria da página.

**Cancelamento:** Cancelar diálogo conserva calibração anterior; cálculo é síncrono.

Fontes/requisitos: [app/measurement.py — calibrated_scale](../app/measurement.py).

Planos relacionados da família: S12-20-1, S12-20-2. Não são aceitação completa desta operação. Nova execução neste registro: `not_run`; expectativa e observação integral Foxit: `null`.

#### `measurement/area` — Medir área

Estado: `current_bounded_source`; base: `current_linuxit_source`.

**Entradas:** Polígono com 3–512 vértices, unidade e fator calibrado.

**Saídas:** Área absoluta em unidade ao quadrado pelo método shoelace translado.

**Limites:** Polígono simples; fechamento inicial/final duplicado é normalizado; sem áreas curvas/auto-interseção.

**Erros:** Auto-interseção, zero área ou unidade/fator inválido → ValueError, sem área enganosa.

**Estado e efeitos:** Resultado e desenho locais; não cria objeto PDF de medida por si.

**Cancelamento:** Cancelar captura descarta polígono; operação matemática síncrona sem processo persistente.

Fontes/requisitos: [app/measurement.py — measure](../app/measurement.py).

Planos relacionados da família: S12-20-1, S12-20-2. Não são aceitação completa desta operação. Nova execução neste registro: `not_run`; expectativa e observação integral Foxit: `null`.

#### `measurement/perimeter` — Medir perímetro

Estado: `current_bounded_source`; base: `current_linuxit_source`.

**Entradas:** Lista de 2–512 pontos, unidade e fator calibrado.

**Saídas:** Soma fechada de distâncias, incluindo último→primeiro.

**Limites:** Este comando mede perímetro fechado, não polilinha aberta; coordenadas finitas até 2 milhões.

**Erros:** Pontos consecutivos iguais/unidade inválida → ValueError.

**Estado e efeitos:** Mostra medida/desenho em memória, fonte preservada.

**Cancelamento:** Cancelar captura não publica resultado; cálculo puro não tem job de cancelamento.

Fontes/requisitos: [app/measurement.py — measure](../app/measurement.py).

Planos relacionados da família: S12-20-1, S12-20-2. Não são aceitação completa desta operação. Nova execução neste registro: `not_run`; expectativa e observação integral Foxit: `null`.


<a id="layers-media"></a>

## Camadas/mídia/3D

Atual (0.1.16): listar OCGs, alternar visibilidade temporária (default ON/OFF, locks e grupos exclusivos) e salvar a visibilidade em cópia nova com criptografia preservada. Movie/RichMedia com arquivos incorporados, Sound PCM8/16 (convertido para WAV) e 3D podem ser listados/extraídos; áudio/vídeo locais têm reprodução explícita; desde a etapa E26 a reprodução só começa depois do pré-carregamento, evitando que um arquivo curto termine de imediato. Imagem de apresentação 3D (etapa E16): a aparência normal da anotação 3D (o pôster) é desenhada como imagem fixa, no tamanho do retângulo da anotação, numa janela com aviso de que a cena não é interativa; a lista informa se há pôster, modelo incorporado e quantas vistas; anotação sem pôster é recusada com motivo. Renderizador U3D/PRC e interação com a cena estão adiados pelo usuário para atualização futura (decisão de 20/10/2026, guia em docs/ESTUDO-3D-U3D-PRC.md); eventos de mídia e todas as configurações opcionais continuam abertos.

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

- **S12-21-1** (nominal, contrato próprio atual, `passed`): dado PDF sintético com OCGs nomeados, fixture a criar. Ação: Inspecionar painel. Esperado: Lista os nomes lidos, sem anunciar reprodução de mídia ou alteração de camada. Execução própria em 2026-10-21T21:25:02-03:00, revisão `ac89254204fb`, fronteira worker panels: [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e31.json).
- **S12-21-2** (exception, contrato próprio atual, `passed`): dado PDF sem OCProperties. Ação: Inspecionar painel. Esperado: layers=[]; não criar uma camada fictícia. Execução própria em 2026-10-21T21:25:02-03:00, revisão `ac89254204fb`, fronteira worker panels: [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e31.json).
- **S12-21-3** (nominal, contrato próprio atual, `passed`): dado PDF sintético com duas anotações 3D com modelo U3D: a primeira com imagem de apresentação (caixa azul com a metade esquerda vermelha, BBox 50×25 num retângulo 100×50); a segunda sem imagem. Ação: Listar a mídia e pedir a imagem de apresentação da primeira. Esperado: A lista marca imagem e modelo em cada uma e informa que não há renderizador 3D; o PNG tem proporção 2:1, vermelho à esquerda e azul à direita, e a resposta diz que a cena não é interativa; original preservado. Execução própria em 2026-10-21T21:25:02-03:00, revisão `ac89254204fb`, fronteira worker media-info + media-poster: [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e31.json).
- **S12-21-4** (exception, contrato próprio atual, `passed`): dado O mesmo PDF. Ação: Pedir a imagem da anotação sem pôster, pedir com extensão .jpg e pedir com identidade SHA-256 errada. Esperado: Os três pedidos são recusados sem criar arquivos; original preservado. Execução própria em 2026-10-21T21:25:03-03:00, revisão `ac89254204fb`, fronteira worker media-poster: [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e31.json).

**Lacunas da referência Foxit**

- Combinações OCG, visibilidade, persistência, codecs, eventos e suporte U3D/Reader.

Fontes: [app/pdf_panels.py](../app/pdf_panels.py), [app/pdf_layers.py](../app/pdf_layers.py), [app/local_playback.py](../app/local_playback.py), [app/media_window.py](../app/media_window.py), [app/pdf_media.py](../app/pdf_media.py), [app/media_assets_window.py](../app/media_assets_window.py), [testes/resultados/0.1.16/validation-review.json](../testes/resultados/0.1.16/validation-review.json), [docs/FOXIT-REA.md](../docs/FOXIT-REA.md).

Testes próprios existentes, sem nova execução nesta tabela: [test_listing_reports_poster_model_and_views_without_a_renderer](../tests/test_media_3d_poster.py); [test_poster_is_the_annotation_appearance_scaled_to_its_rectangle](../tests/test_media_3d_poster.py); [test_poster_without_model_and_page_rendering_show_the_same_appearance](../tests/test_media_3d_poster.py); [test_refusals_publish_nothing](../tests/test_media_3d_poster.py); [test_poster_window_shows_the_appearance_and_says_the_scene_is_not_interactive](../tests/test_media_assets_gtk.py).

### Contratos individuais de operações

#### `layers-media/list` — Listar nomes de camadas OCG

Estado: `current_bounded_source`; base: `current_linuxit_source`.

**Entradas:** Reader e /OCProperties/OCGs e configuração default.

**Saídas:** Nomes/IDs e estado das camadas suportadas; inventário de mídia separado.

**Limites:** Até 256 OCG; nomes não provam visibilidade nem renderer 3D.

**Erros:** OCG repetida, BaseState incompatível ou estrutura inválida → erro explícito.

**Estado e efeitos:** Somente inspeção de metadados; sem ação de mídia executada.

**Cancelamento:** Painel usa worker com geração; resposta antiga não muda novo documento.

Fontes/requisitos: [app/pdf_panels.py — inspect_document_panels](../app/pdf_panels.py).

Planos relacionados da família: S12-21-1, S12-21-2, S12-21-3, S12-21-4. Não são aceitação completa desta operação. Nova execução neste registro: `not_run`; expectativa e observação integral Foxit: `null`.

#### `layers-media/toggle` — Alternar e persistir visibilidade OCG

Estado: `current_bounded_source`; base: `current_linuxit_source`.

**Entradas:** IDs de camadas visíveis e configuração atual; sessão autenticada quando cifrado.

**Saídas:** Representação de leitura e render com configuração escolhida; save pode persistir configuração sem flatten.

**Limites:** Até 256 camadas e cópia privada até 64 MiB; Locked/RBGroups respeitados.

**Erros:** Camada bloqueada, seleção inválida ou grupo exclusivo conflitante → erro e seleção anterior preservada.

**Estado e efeitos:** Cria representação privada; salvar cópia altera configuração OCG mantendo conteúdo/cifra no recorte.

**Cancelamento:** Mudar seleção invalida render antigo; cancelar/fechar remove representação quando leases liberados.

Fontes/requisitos: [app/pdf_layers.py — create_layer_view](../app/pdf_layers.py), [app/main.py — PDFWindow._layer_toggled](../app/main.py).

Planos relacionados da família: S12-21-1, S12-21-2, S12-21-3, S12-21-4. Não são aceitação completa desta operação. Nova execução neste registro: `not_run`; expectativa e observação integral Foxit: `null`.

#### `layers-media/media` — Reproduzir mídia embutida

Estado: `current_bounded_source`; base: `current_linuxit_source`.

**Entradas:** Anotação Movie/RichMedia/Sound e índice/identidade; destino com extensão preservada.

**Saídas:** Extração de bytes incorporados ou WAV PCM; reprodução GStreamer somente explícita.

**Limites:** PDF/payload até 64 MiB, 5000 páginas, 10000 anotações/página e 256 recursos; PCM 8/16 bit,1–2 canais,8–192kHz.

**Erros:** URI externa, codec ausente ou conteúdo não incorporado → omissão/erro, não download nem execução de ação PDF.

**Estado e efeitos:** Cria arquivo escolhido e player local quando solicitado; sem autoplay de scripts.

**Cancelamento:** Extração em worker cancelável; Stop encerra apenas player criado pelo app.

Fontes/requisitos: [app/pdf_media.py — extract_media](../app/pdf_media.py).

Planos relacionados da família: S12-21-1, S12-21-2, S12-21-3, S12-21-4. Não são aceitação completa desta operação. Nova execução neste registro: `not_run`; expectativa e observação integral Foxit: `null`.

#### `layers-media/3d-poster` — Imagem de apresentação de anotações 3D

Estado: `current_bounded_source`; base: `current_linuxit_source`.

**Entradas:** Anotação /3D com aparência normal, source identity e destino .png.

**Saídas:** PNG estático ajustado ao Rect/BBox/Matrix e aviso de que não é cena interativa.

**Limites:** Requer Poppler/pdftocairo; modelo U3D/PRC não é interpretado pelo poster.

**Erros:** Sem AP, fonte alterada, geometria inválida ou destino não PNG → erro sem imagem publicada.

**Estado e efeitos:** Rasteriza somente aparência para arquivo novo; modelo incorporado permanece intacto.

**Cancelamento:** Worker/cancelamento de tarefa podem interromper render; não muda estado de animação 3D inexistente.

Fontes/requisitos: [app/pdf_media.py — render_poster](../app/pdf_media.py).

Planos relacionados da família: S12-21-1, S12-21-2, S12-21-3, S12-21-4. Não são aceitação completa desta operação. Nova execução neste registro: `not_run`; expectativa e observação integral Foxit: `null`.

#### `layers-media/3d` — Interagir com conteúdo 3D

Estado: `pending_environment_or_reference`; base: `proposed_independent_requirement`.

**Entradas:** Modelo U3D/PRC e vistas, gestos de rotação/zoom e árvore de cena.

**Saídas:** Proposta futura de renderer interativo; hoje só poster/extrair modelo separados.

**Limites:** Adiado por decisão D04; sem motor U3D/PRC interativo implementado.

**Erros:** Modelo/formato sem renderer → informar limitação, não apresentar poster como interação 3D.

**Estado e efeitos:** Nenhuma interpretação dinâmica/execução de script 3D nesta entrega.

**Cancelamento:** Proposta futura: parar renderer e liberar recursos; sem runtime ativo a encerrar hoje.

Fontes/requisitos: [docs/ESTUDO-3D-U3D-PRC.md](../docs/ESTUDO-3D-U3D-PRC.md).

Planos relacionados da família: S12-21-1, S12-21-2, S12-21-3, S12-21-4. Não são aceitação completa desta operação. Nova execução neste registro: `not_run`; expectativa e observação integral Foxit: `null`.


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

- **S12-22-1** (nominal, contrato próprio atual, `passed`): dado Configuração com modo dark e uma chave desconhecida. Ação: Salvar modo light e reabrir a preferência. Esperado: Modo light preservado e chave desconhecida conservada. Execução própria em 2026-10-21T21:25:03-03:00, revisão `ac89254204fb`, fronteira appearance.save_mode/read_mode: [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e31.json).
- **S12-22-2** (exception, contrato próprio atual, `passed`): dado Modo inventado ao salvar. Ação: Chamar save_mode. Esperado: ValueError, sem tratar o modo como suportado. Execução própria em 2026-10-21T21:25:03-03:00, revisão `ac89254204fb`, fronteira appearance.save_mode: [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e31.json).

**Lacunas da referência Foxit**

- Defaults, esquemas de persistência e dependências de todas as preferências do original.

Fontes: [app/appearance.py](../app/appearance.py), [app/local_files.py](../app/local_files.py), [app/folder_dialogs.py](../app/folder_dialogs.py), [docs/PASTAS-SINCRONIZADAS.md](../docs/PASTAS-SINCRONIZADAS.md), [app/reading_preferences.py](../app/reading_preferences.py), [app/tool_preferences.py](../app/tool_preferences.py), [testes/resultados/0.1.16/validation-review.json](../testes/resultados/0.1.16/validation-review.json), [docs/FOXIT-REA.md](../docs/FOXIT-REA.md).

Testes próprios existentes, sem nova execução nesta tabela: [test_theme_persistence_and_contrast](../tests/test_viewer.py); [test_fresh_system_theme_initializes_and_migrates_legacy](../tests/test_consolidation.py); [test_final_name_is_absent_while_real_copy_is_in_progress](../tests/test_sync_folders.py); [test_save_copy_uses_worker_preserves_original_and_only_confirms_local_save](../tests/test_sync_folders_gtk.py).

### Contratos individuais de operações

#### `preferences/theme` — Persistir e aplicar tema

Estado: `current_bounded_source`; base: `current_linuxit_source`.

**Entradas:** Modo system/light/dark e arquivo de preferências do usuário.

**Saídas:** Modo lido/aplicado e persistido, seguindo sistema quando escolhido.

**Limites:** Só três modos válidos; fallback de leitura não deve ser chamado de migração universal.

**Erros:** Modo desconhecido → ValueError; arquivo ilegível

**Estado e efeitos:** Grava configuração de aparência, não modifica documentos.

**Cancelamento:** Seleção/aplicação síncronas; cancelar diálogo conserva opção anterior.

Fontes/requisitos: [app/appearance.py — save_mode](../app/appearance.py).

Planos relacionados da família: S12-22-1, S12-22-2. Não são aceitação completa desta operação. Nova execução neste registro: `not_run`; expectativa e observação integral Foxit: `null`.

#### `preferences/folders` — Persistir pasta preferida e últimas pastas

Estado: `current_bounded_source`; base: `current_linuxit_source`.

**Entradas:** Chave da operação e diretório local explicitamente escolhido.

**Saídas:** Pasta preferida por operação, fallback para caminho disponível e opção esquecer.

**Limites:** Guardar caminho não autentica conta nem comprova sincronização; pasta pode ficar offline.

**Erros:** Chave/diretório inválido → erro/fallback; esquecer não apaga arquivos nem conta externa.

**Estado e efeitos:** Persiste preferência de pasta local; nenhuma API de nuvem.

**Cancelamento:** Cancelar file chooser não confirma salvamento/pasta; transferência de arquivo tem seu próprio cancelamento.

Fontes/requisitos: [app/local_files.py — remember_folder](../app/local_files.py).

Planos relacionados da família: S12-22-1, S12-22-2. Não são aceitação completa desta operação. Nova execução neste registro: `not_run`; expectativa e observação integral Foxit: `null`.

#### `preferences/remaining` — Cobrir demais ajustes e defaults

Estado: `current_bounded_source`; base: `current_linuxit_source`.

**Entradas:** Mapa exato zoom_mode,zoom_percent,sidebar,highlight_all e preferências OCR/voz separadas.

**Saídas:** Defaults próprios validados e escrita atômica em reading.json.

**Limites:** fit-width/100/sidebar=true/highlight_all=true; percentual inteiro 1–6400; leitura de config até 8192 bytes.

**Erros:** Chave extra/tipo errado → ValueError no save; arquivo ausente/corrompido

**Estado e efeitos:** Cria diretório privado e substitui config atômica; não guarda senhas/chaves.

**Cancelamento:** Cancelar diálogo conserva config; gravação curta síncrona, sem publicação remota.

Fontes/requisitos: [app/reading_preferences.py — save_preferences](../app/reading_preferences.py), [app/main.py — PDFWindow._reading_preferences](../app/main.py).

Planos relacionados da família: S12-22-1, S12-22-2. Não são aceitação completa desta operação. Nova execução neste registro: `not_run`; expectativa e observação integral Foxit: `null`.


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

- **S12-23-1** (nominal, contrato próprio atual, `passed`): dado Pasta local sincronizada escolhida como preferida, com um PDF sintético dentro (cliente externo representado pela própria pasta; sem cliente real). Ação: Abrir o PDF pela opção da pasta sincronizada e salvar uma cópia com nome novo na mesma pasta. Esperado: O seletor abre na pasta preferida; a cópia aparece completa e idêntica com o nome final, sem temporários; o estado diz "salva localmente" e que o envio é do sincronizador; original preservado; nenhuma conta ou rede. Execução própria em 2026-10-21T21:25:03-03:00, revisão `ac89254204fb`, fronteira PDFWindow _open_sync_folder/_save_copy + worker copy-file: [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e31.json).
- **S12-23-2** (exception, contrato próprio atual, `passed`): dado O mesmo PDF aberto da pasta sincronizada. Ação: O cliente externo troca o PDF aberto e, depois de reabrir, cria um arquivo com o nome escolhido para a cópia. Esperado: Salvar fica bloqueado até reabrir; depois, o arquivo criado pelo cliente não é sobrescrito; nenhum falso sucesso; arquivos preservados. Execução própria em 2026-10-21T21:25:05-03:00, revisão `ac89254204fb`, fronteira PDFWindow _save_copy + worker copy-file: [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e31.json).

**Lacunas da referência Foxit**

- Contratos por provedor, serviços disponíveis, autorização, colaboração e conflitos; presença de plugins não valida APIs.

Fontes: [docs/PASTAS-SINCRONIZADAS.md](../docs/PASTAS-SINCRONIZADAS.md), [app/local_files.py](../app/local_files.py), [app/folder_dialogs.py](../app/folder_dialogs.py), [app/main.py](../app/main.py), [app/worker_cli.py](../app/worker_cli.py), [testes/resultados/0.1.16/validation-review.json](../testes/resultados/0.1.16/validation-review.json), [testes/resultados/0.1.16/desktop/review.json](../testes/resultados/0.1.16/desktop/review.json), [docs/FOXIT-REA.md](../docs/FOXIT-REA.md).

Testes próprios existentes, sem nova execução nesta tabela: [test_worker_roundtrip_preserves_source_and_never_claims_remote_sync](../tests/test_sync_folders.py); [test_existing_file_and_destination_race_are_never_overwritten](../tests/test_sync_folders.py); [test_final_name_is_absent_while_real_copy_is_in_progress](../tests/test_sync_folders.py); [test_source_changed_before_or_during_copy_refuses_publication](../tests/test_sync_folders.py); [test_invalid_relative_missing_and_unknown_settings_are_refused](../tests/test_sync_folders.py); [test_save_copy_uses_worker_preserves_original_and_only_confirms_local_save](../tests/test_sync_folders_gtk.py); [test_external_replacement_blocks_save_and_edit_until_reopen](../tests/test_sync_folders_gtk.py); [test_existing_destination_is_preserved_and_failure_is_shown](../tests/test_sync_folders_gtk.py).

### Contratos individuais de operações

#### `cloud/login` — Autenticar provedor remoto

Estado: `deferred_by_user`; base: `proposed_independent_requirement`.

**Entradas:** Conta/provedor e eventual credencial OAuth futura.

**Saídas:** Adiado: nenhum login direto implementado nem sessão remota criada.

**Limites:** Decisão explícita de adiar APIs diretas; uso de pasta sincronizada externa é outro fluxo.

**Erros:** Tentativa de usar login direto → funcionalidade indisponível; nunca pedir/salvar token sem trabalho autorizado.

**Estado e efeitos:** Nenhuma credencial/token/rede criada por este contrato.

**Cancelamento:** Cancelamento não tem transação ativa; fluxo OAuth só será detalhado se adiamento for revogado.

Fontes/requisitos: decisão de adiamento; ver escopo da família.

Planos relacionados da família: S12-23-1, S12-23-2. Não são aceitação completa desta operação. Nova execução neste registro: `not_run`; expectativa e observação integral Foxit: `null`.

#### `cloud/transfer` — Transferir arquivos por API de nuvem

Estado: `deferred_by_user`; base: `proposed_independent_requirement`.

**Entradas:** Arquivo/provedor e escolha futura upload/download.

**Saídas:** Adiado: nenhum recibo de transferência remota; salvar pasta confirma só cópia local.

**Limites:** Não equiparar cópia local a upload ou sucesso do cliente sincronizador.

**Erros:** Sem cliente/pasta disponível → erro local; não inventar resultado remoto.

**Estado e efeitos:** Nenhuma API/objeto remoto alterado; apenas fluxo local existente separado.

**Cancelamento:** Transferência direta inexiste; cliente externo controla cancelamento/sincronização próprios.

Fontes/requisitos: decisão de adiamento; ver escopo da família.

Planos relacionados da família: S12-23-1, S12-23-2. Não são aceitação completa desta operação. Nova execução neste registro: `not_run`; expectativa e observação integral Foxit: `null`.

#### `cloud/collaboration` — Colaborar remotamente e resolver conflitos

Estado: `deferred_by_user`; base: `proposed_independent_requirement`.

**Entradas:** Participantes, arquivo e versões remotas futuras.

**Saídas:** Adiado: sem coedição/revisão remota direta implementada.

**Limites:** Não enviar convites/mensagens nem acessar identidade de terceiros por mera proposta.

**Erros:** Conflito/serviço indisponível deverá ser especificado quando escopo reabrir; hoje informar não suportado. → Não aprovar a operação; Conflito/serviço indisponível deverá ser especificado quando escopo reabrir; hoje informar não suportado.

**Estado e efeitos:** Nenhum participante/permissão/versão remota é alterado.

**Cancelamento:** Não há tarefa colaborativa ativa para cancelar; não revogar versões externas automaticamente.

Fontes/requisitos: decisão de adiamento; ver escopo da família.

Planos relacionados da família: S12-23-1, S12-23-2. Não são aceitação completa desta operação. Nova execução neste registro: `not_run`; expectativa e observação integral Foxit: `null`.


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

- **S12-24-1** (nominal, contrato próprio atual, `passed`): dado PNG/JPEG sintéticos ordenados e DPI suportado. Ação: Converter para PDF em caminho novo. Esperado: Criar novo PDF RGB com orientação, ordem e dimensões declaradas; fontes intactas. Execução própria em 2026-10-21T21:25:07-03:00, revisão `ac89254204fb`, fronteira worker images-to-pdf: [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e31.json).
- **S12-24-2** (exception, contrato próprio atual, `passed`): dado Arquivo GIF ou PNG/JPEG inválido. Ação: Solicitar conversão. Esperado: Recusar lote sem criar saída concluída e sem substituir arquivo existente. Execução própria em 2026-10-21T21:25:07-03:00, revisão `ac89254204fb`, fronteira worker images-to-pdf: [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e31.json).

**Lacunas da referência Foxit**

- Inventário real Reader/Editor, fidelidade, formatos, OCR e serviços; não implementado como família completa.

Fontes: [app/pdf_creation.py](../app/pdf_creation.py), [app/creation_window.py](../app/creation_window.py), [app/search_tasks.py](../app/search_tasks.py), [app/worker_cli.py](../app/worker_cli.py), [app/main.py](../app/main.py), [docs/CRIACAO-IMAGENS.md](../docs/CRIACAO-IMAGENS.md), [app/local_files.py](../app/local_files.py), [app/folder_dialogs.py](../app/folder_dialogs.py), [docs/PASTAS-SINCRONIZADAS.md](../docs/PASTAS-SINCRONIZADAS.md), [testes/resultados/0.1.10/validation-review.json](../testes/resultados/0.1.10/validation-review.json), [app/pdf_ocr.py](../app/pdf_ocr.py), [app/ocr_window.py](../app/ocr_window.py), [docs/OCR-LOCAL.md](../docs/OCR-LOCAL.md), [testes/resultados/ocr-portable-2026-10-18-round1.json](../testes/resultados/ocr-portable-2026-10-18-round1.json), [testes/resultados/0.1.11/validation-review.json](../testes/resultados/0.1.11/validation-review.json), [docs/TIFF-MULTIPAGINA.md](../docs/TIFF-MULTIPAGINA.md), [testes/resultados/tiff-multipage-portable-2026-10-18-round2.json](../testes/resultados/tiff-multipage-portable-2026-10-18-round2.json), [testes/resultados/tiff-creation-existing-2026-10-18-round2.json](../testes/resultados/tiff-creation-existing-2026-10-18-round2.json), [testes/resultados/tiff-multipage-portable-2026-10-18-round3.json](../testes/resultados/tiff-multipage-portable-2026-10-18-round3.json), [testes/resultados/0.1.12/validation-review.json](../testes/resultados/0.1.12/validation-review.json), [testes/resultados/0.1.16/validation-review.json](../testes/resultados/0.1.16/validation-review.json), [docs/FOXIT-REA.md](../docs/FOXIT-REA.md).

Testes próprios existentes, sem nova execução nesta tabela: [test_order_dimensions_lossless_rgb_and_source_identity](../tests/test_pdf_creation.py); [test_alpha_and_palette_transparency_are_composited_on_white](../tests/test_pdf_creation.py); [test_exif_orientation_applied_and_private_metadata_not_copied](../tests/test_pdf_creation.py); [test_corrupt_unsupported_animated_and_truncated_inputs_leave_no_output](../tests/test_pdf_creation.py); [test_partial_final_write_removed_on_handled_failure](../tests/test_pdf_creation.py); [test_ordered_creation_opens_actual_pdf_and_poppler_renders_pixels](../tests/test_creation_gtk.py); [test_cancel_and_destroy_kill_real_worker_without_stale_callbacks](../tests/test_creation_gtk.py); [test_pinned_fixture_manifest_matches_sources_and_oriented_dimensions](../tests/test_pdf_creation.py); [test_final_name_is_absent_while_real_copy_is_in_progress](../tests/test_sync_folders.py); [test_save_copy_uses_worker_preserves_original_and_only_confirms_local_save](../tests/test_sync_folders_gtk.py); [test_bmp_webp_and_single_tiff_preserve_pixels_dimensions_and_order](../tests/test_pdf_creation.py); [test_webp_alpha_is_composited_over_white](../tests/test_pdf_creation.py); [test_multiframe_tiff_is_imported_and_animated_webp_is_refused](../tests/test_pdf_creation.py); [test_bmp_renamed_as_jpeg_is_identified_by_content](../tests/test_pdf_creation.py); [test_real_worker_supports_compressed_tiff_without_external_conversion](../tests/test_pdf_creation.py); [test_bmp_webp_tiff_selection_worker_and_opening](../tests/test_creation_gtk.py); [test_raster_copy_pipeline_preserves_order_dimensions_hashes_and_original](../tests/test_pdf_ocr.py); [test_encrypted_input_is_rejected_without_attempting_empty_password](../tests/test_pdf_ocr.py); [test_real_english_worker_adds_searchable_text_and_keeps_scan](../tests/test_ocr_linux.py); [test_cancel_stops_worker_and_its_actual_tesseract_child](../tests/test_ocr_linux.py); [test_menu_workflow_recognizes_opens_and_renders_actual_copy](../tests/test_ocr_gtk.py); [test_file_order_expands_all_tiff_pages_with_dimensions_and_provenance](../tests/test_tiff_multipage.py); [test_each_frame_orientation_is_applied_once_without_leaking_tags](../tests/test_tiff_multipage.py); [test_cyclic_out_of_range_and_truncated_ifd_chains_are_not_silently_shortened](../tests/test_tiff_multipage.py); [test_real_worker_reports_input_count_frame_mapping_and_page_count](../tests/test_tiff_multipage.py); [test_tiff_block_order_expands_pages_and_poppler_renders_each_color](../tests/test_creation_gtk.py); [test_multipage_tiff_import_feeds_searchable_ocr_without_losing_blank_page](../tests/test_ocr_linux.py).

### Contratos individuais de operações

#### `conversion/images` — Criar PDF de imagens simples

Estado: `current_bounded_source`; base: `current_linuxit_source`.

**Entradas:** Lista ordenada de imagens, DPI/fit/opções e destino PDF novo.

**Saídas:** PDF RGB com páginas e geometria derivadas, ordem preservada e recibo.

**Limites:** Até 100 entradas/páginas,45 MP por imagem,150 MP total; formatos aceitos por decodificador validado.

**Erros:** Imagem inválida, orçamento excedido ou destino existente → erro sem PDF final parcial.

**Estado e efeitos:** Decodifica cópias e publica PDF novo; originais de imagem preservados.

**Cancelamento:** Worker cancelável com timeout 120 s; cancelar antes de publicar remove temporários.

Fontes/requisitos: [app/pdf_creation.py — create_pdf_from_images](../app/pdf_creation.py).

Planos relacionados da família: S12-24-1, S12-24-2. Não são aceitação completa desta operação. Nova execução neste registro: `not_run`; expectativa e observação integral Foxit: `null`.

#### `conversion/tiff` — Expandir TIFF multipágina

Estado: `current_bounded_source`; base: `current_linuxit_source`.

**Entradas:** TIFF suportado, ordem de frames explícita e opções de criação.

**Saídas:** Páginas do TIFF em ordem com orientação/tamanho conferidos.

**Limites:** Até 100 páginas totais; limites de pixels compartilhados; não promete todas as variantes TIFF.

**Erros:** IFD cíclico/BigTIFF não suportado/frames inválidos → recusa sem converter só prefixo silenciosamente.

**Estado e efeitos:** Lê múltiplos frames e cria PDF novo, TIFF intacto.

**Cancelamento:** Mesmo worker cancelável da criação de imagens; arquivo final só aparece após validação.

Fontes/requisitos: [app/pdf_creation.py — _tiff_page_count](../app/pdf_creation.py).

Planos relacionados da família: S12-24-1, S12-24-2. Não são aceitação completa desta operação. Nova execução neste registro: `not_run`; expectativa e observação integral Foxit: `null`.

#### `conversion/ocr` — Gerar cópia PDF pesquisável local

Estado: `current_bounded_source`; base: `current_linuxit_source`.

**Entradas:** PDF/imagens, páginas escolhidas, idiomas por/eng instalados, layout psm e destino novo.

**Saídas:** PDF pesquisável com camada de texto e relatório de páginas/idiomas; precisão não universal.

**Limites:** Até 20 páginas selecionadas,45 MP/página,150 MP total; PSM 3/6/11 e Tesseract/Poppler.

**Erros:** Idioma ausente, tempo por página excedido ou raster grande → erro sem saída final; não afirmar OCR perfeito.

**Estado e efeitos:** Cria cópia OCR; estrutura/anotações/metadados podem ter limites explicitados, fonte preservada.

**Cancelamento:** Worker cancelável com timeout geral 600 s; não publicar parcialmente reconhecido como completo.

Fontes/requisitos: [app/pdf_ocr.py — create_searchable_copy](../app/pdf_ocr.py).

Planos relacionados da família: S12-24-1, S12-24-2. Não são aceitação completa desta operação. Nova execução neste registro: `not_run`; expectativa e observação integral Foxit: `null`.

#### `conversion/animation` — Converter animações/variantes ainda recusadas

Estado: `current_bounded_source`; base: `current_linuxit_source`.

**Entradas:** GIF/APNG suportado e escolha explícita de importar todos os quadros.

**Saídas:** PDF com um frame por página na ordem; tempos/animação não são preservados.

**Limites:** Até 100 páginas e orçamento de pixels; APNG com default separado não suportado.

**Erros:** Sem confirmação multiframe ou APNG com default separado → ValueError, sem escolher frame silenciosamente.

**Estado e efeitos:** Gera PDF estático novo; imagem animada original intacta.

**Cancelamento:** Cancelar confirmação não decodifica job; worker usa cancelamento da criação de imagens.

Fontes/requisitos: [app/pdf_creation.py — create_pdf_from_images](../app/pdf_creation.py).

Planos relacionados da família: S12-24-1, S12-24-2. Não são aceitação completa desta operação. Nova execução neste registro: `not_run`; expectativa e observação integral Foxit: `null`.

#### `conversion/other-formats` — Cobrir demais conversões disponíveis no Reader

Estado: `current_bounded_source`; base: `current_linuxit_source`.

**Entradas:** Imagem estática/animada/TIFF suportada, ou formato de documento solicitado.

**Saídas:** Conversões de imagens existentes; Office/HTML/RTF em anexos fornecem texto passivo, não conversão visual universal.

**Limites:** PDF→DOCX/planilha/edição universal e fidelidade Office permanecem fora do subconjunto de criação.

**Erros:** Formato não decodificável como imagem → erro; extração textual não deve ser rotulada como conversão fiel.

**Estado e efeitos:** Nenhum aplicativo Office/arquivo anexado é executado automaticamente.

**Cancelamento:** Criação suportada cancelável; formato não implementado não inicia job fictício.

Fontes/requisitos: [app/pdf_creation.py — create_pdf_from_images](../app/pdf_creation.py).

Planos relacionados da família: S12-24-1, S12-24-2. Não são aceitação completa desta operação. Nova execução neste registro: `not_run`; expectativa e observação integral Foxit: `null`.


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

- **S12-25-1** (nominal, contrato próprio atual, `passed`): dado Desktop Linux de teste com xdg-desktop-portal; aplicativo com GTK_USE_PORTAL=1, um documento aberto e outro PDF escolhido no seletor. Ação: Usar Abrir pelo seletor do sistema, escolher o arquivo no portal e confirmar. Esperado: Abrir somente o arquivo escolhido; a chamada e a resposta passam pelo portal; o documento anterior não é alterado e nenhum outro arquivo da pasta é aberto. Execução própria em 2026-10-21T21:25:08-03:00, revisão `ac89254204fb`, fronteira PDFWindow._choose_open_native via xdg-desktop-portal: [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e31.json).
- **S12-25-2** (exception, contrato próprio atual, `passed`): dado Mesmo desktop de teste com um documento aberto. Ação: Abrir o seletor do sistema e cancelar no portal. Esperado: Nenhum acesso ampliado, erro ou sucesso falso; o documento corrente continua aberto. Execução própria em 2026-10-21T21:25:41-03:00, revisão `ac89254204fb`, fronteira PDFWindow._choose_open_native via xdg-desktop-portal: [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e31.json).

**Lacunas da referência Foxit**

- Portais em desktop real, integração shell/browser, atualização, rollback e equivalência do adaptador Windows.

Fontes: [docs/instalacao.md](../docs/instalacao.md), [app/folder_dialogs.py](../app/folder_dialogs.py), [app/main.py](../app/main.py), [app/installation_info.py](../app/installation_info.py), [app/platform_runtime.py](../app/platform_runtime.py), [app/cups_backend.py](../app/cups_backend.py), [testes/aceitacao/casos_portal.py](../testes/aceitacao/casos_portal.py), [scripts/check_native_portal.py](../scripts/check_native_portal.py), [scripts/check_desktop_integrations.py](../scripts/check_desktop_integrations.py), [testes/resultados/0.1.16/desktop/review.json](../testes/resultados/0.1.16/desktop/review.json), [docs/FOXIT-REA.md](../docs/FOXIT-REA.md).

### Contratos individuais de operações

#### `platform/worker-runtime` — Selecionar runtime de worker

Estado: `current_bounded_source`; base: `current_linuxit_source`.

**Entradas:** sys.executable, ambiente empacotado e caminho do módulo worker.

**Saídas:** Python correto pareado com runtime e opções de subprocesso, incluindo janela oculta no Windows.

**Limites:** Não misturar biblioteca nativa do sistema com /app/lib; caminho Windows GUI pode exigir python.exe.

**Erros:** Runtime/dependência não localizados → falha de worker, não sucesso vazio.

**Estado e efeitos:** Inicia subprocessos próprios; não altera instalação Python do host.

**Cancelamento:** Chamadores têm cancel/timeouts próprios; resolver executável em si é função curta síncrona.

Fontes/requisitos: [app/platform_runtime.py — worker_python](../app/platform_runtime.py).

Planos relacionados da família: S12-25-1, S12-25-2. Não são aceitação completa desta operação. Nova execução neste registro: `not_run`; expectativa e observação integral Foxit: `null`.

#### `platform/portal` — Validar portal real e concessão persistente

Estado: `pending_environment_or_reference`; base: `proposed_independent_requirement`.

**Entradas:** Desktop Linux/Flatpak, file chooser e pasta fora de HOME com decisão conceder/negar.

**Saídas:** Evidência de concessão persistente, leitura por processo novo e revogação; próprio probe existente separado.

**Limites:** Document portal real e compositor/bus/FUSE necessários; simulação de diálogo não substitui ambiente.

**Erros:** Negação/revogação → novo processo deve falhar ao ler; ausência do portal

**Estado e efeitos:** Pode criar concessão em documents portal; não ampliar filesystem de todo host.

**Cancelamento:** Cancelar diálogo não cria autorização; encerramento do probe só restaura serviço que ele próprio criou.

Fontes/requisitos: [docs/EXECUCAO-SEM-VM.md](../docs/EXECUCAO-SEM-VM.md).

Planos relacionados da família: S12-25-1, S12-25-2. Não são aceitação completa desta operação. Nova execução neste registro: `not_run`; expectativa e observação integral Foxit: `null`.

#### `platform/association` — Associar e abrir PDF pelo desktop

Estado: `pending_environment_or_reference`; base: `proposed_independent_requirement`.

**Entradas:** Arquivo .pdf e shell desktop com launcher instalado.

**Saídas:** Ativação do app com caminho correto e evidência da associação no ambiente testado.

**Limites:** Probe Linux próprio não certifica todos os desktops nem associação Windows.

**Erros:** Desktop entry/caminho/launcher inválido → falha observada, não declarar associação instalada por arquivo existente.

**Estado e efeitos:** Pode registrar/selecionar associação na campanha própria; restaurar preferência anterior do ambiente quando aplicável.

**Cancelamento:** Cancelar escolha não muda app padrão; fechar app não desfaz associação persistida.

Fontes/requisitos: [docs/EXECUCAO-SEM-VM.md](../docs/EXECUCAO-SEM-VM.md).

Planos relacionados da família: S12-25-1, S12-25-2. Não são aceitação completa desta operação. Nova execução neste registro: `not_run`; expectativa e observação integral Foxit: `null`.

#### `platform/update` — Atualizar e reverter entrega

Estado: `pending_environment_or_reference`; base: `proposed_independent_requirement`.

**Entradas:** Bundle anterior/novo, branch devel e preferências existentes.

**Saídas:** Atualização/rollback instalados com versão e preferências conferidas no recorte próprio.

**Limites:** Probes 0.1.14↔0.1.16 não provam todo caminho futuro nem atualização automática de qualquer origem.

**Erros:** Hash/runtime/versão incompatíveis → falha de instalação, preservando evidência e dados do usuário.

**Estado e efeitos:** Muda deployment Flatpak e histórico OSTree; fonte de publicação separada.

**Cancelamento:** Cancelar install segue Flatpak; verificar deployment ativo após interrupção, não inferir versão pelo download.

Fontes/requisitos: [docs/EXECUCAO-SEM-VM.md](../docs/EXECUCAO-SEM-VM.md).

Planos relacionados da família: S12-25-1, S12-25-2. Não são aceitação completa desta operação. Nova execução neste registro: `not_run`; expectativa e observação integral Foxit: `null`.

#### `platform/windows` — Validar Linuxit nativo no Windows

Estado: `pending_environment_or_reference`; base: `proposed_independent_requirement`.

**Entradas:** Fonte própria no Windows/GTK e futuro instalador, associação e impressão reais.

**Saídas:** Probe de runtime/UI/subprocessos próprio; instalador/suíte completa ainda precisa evidências específicas.

**Limites:** Windows tem prioridade posterior ao Linux; smoke MSYS2 não equivale a instalador validado no PC do usuário.

**Erros:** Dependência GTK/Cairo/Poppler ausente ou adaptador falho → erro de ambiente, sem aprovação do sistema completo.

**Estado e efeitos:** Pode preparar pacote próprio; não alterar VM Foxit nem proteções do host por dedução.

**Cancelamento:** Workers próprios canceláveis; instalação/desinstalação requer fluxo do instalador e preservação dos documentos.

Fontes/requisitos: [docs/EXECUCAO-SEM-VM.md](../docs/EXECUCAO-SEM-VM.md).

Planos relacionados da família: S12-25-1, S12-25-2. Não são aceitação completa desta operação. Nova execução neste registro: `not_run`; expectativa e observação integral Foxit: `null`.


A especificação de referência e a consolidação da fase A continuam parciais. Não promover propostas, presença de recursos ou testes próprios a funcionalidade Foxit recuperada.
