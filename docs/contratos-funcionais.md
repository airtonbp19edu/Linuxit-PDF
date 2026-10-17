# Registro de contratos funcionais — etapa 12

Gerado de `especificacao-funcional.json` por `scripts/validate_functional_spec.py`.

Escopo: **25 famílias identificadas**, **50 cenários planejados**; 15 subconjuntos implementados e 10 propostas futuras. O inventário global permanece aberto.

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
| [Busca em anexos](#search-attachments) | Proposta; não implementado |
| [Índice persistente/pesquisa de coleção](#search-index) | Proposta; não implementado |
| [Stemming/proximidade/coringas](#search-language) | Proposta; não implementado |
| [Seleção/cópia/snapshot](#selection) | Subconjunto atual; lacunas abertas |
| [Prévia/plano de impressão](#printing) | Subconjunto atual; lacunas abertas |
| [Livreto/N-up/mosaico](#imposition) | Subconjunto atual; lacunas abertas |
| [Criar/mover/gravar marcadores](#bookmarks-edit) | Subconjunto atual; lacunas abertas |
| [Anotações/undo/gravação](#annotations) | Subconjunto atual; lacunas abertas |
| [AcroForm/XFA/eventos](#forms) | Proposta; não implementado |
| [Anexos/portfólios](#attachments) | Subconjunto atual; lacunas abertas |
| [Assinaturas/certificados](#signatures) | Proposta; não implementado |
| [Senhas/permissões/RMS](#security) | Proposta; não implementado |
| [Acessibilidade/voz](#accessibility) | Proposta; não implementado |
| [Medição/calibração](#measurement) | Subconjunto atual; lacunas abertas |
| [Camadas/mídia/3D](#layers-media) | Subconjunto atual; lacunas abertas |
| [Preferências/tema/persistência](#preferences) | Subconjunto atual; lacunas abertas |
| [Nuvem/colaboração](#cloud) | Proposta; não implementado |
| [Criação/conversão](#conversion) | Proposta; não implementado |
| [Integrações de sistema/atualização](#platform) | Proposta; não implementado |

<a id="open-render"></a>

## Abrir PDF e renderizar páginas

Abrir PDF local, inspecionar páginas/metadados e renderizar páginas. Salvar cópia é cópia do arquivo; não edição PDF.

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

Fontes: [app/rendering.py](../app/rendering.py), [app/main.py](../app/main.py), [app/async_core.py](../app/async_core.py), [docs/ETAPA-11.md](../docs/ETAPA-11.md), [docs/windows-evidence/foxit-rea/ui-state-contracts-2026-10-16.json](../docs/windows-evidence/foxit-rea/ui-state-contracts-2026-10-16.json).

Testes próprios existentes, sem nova execução nesta tabela: [test_cache_distinguishes_documents](../tests/test_regressions.py); [test_latest_renderer_skips_obsolete_queue_entries](../tests/test_viewer.py).

Relacionados aos planos dinâmicos/UI: D01, D02, D13, D14, D15, D19, D20.

<a id="navigation"></a>

## Navegação/rotação/zoom

Navegar por página, aplicar zoom/ajuste e rotação de visualização, sem gravar a rotação no PDF.

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

Fontes: [app/main.py](../app/main.py), [app/page_cache.py](../app/page_cache.py), [app/rendering.py](../app/rendering.py), [docs/ETAPA-11.md](../docs/ETAPA-11.md), [docs/windows-evidence/foxit-rea/ui-state-contracts-2026-10-16.json](../docs/windows-evidence/foxit-rea/ui-state-contracts-2026-10-16.json), [docs/windows-evidence/foxit-rea/zoom-presets.json](../docs/windows-evidence/foxit-rea/zoom-presets.json).

Testes próprios existentes, sem nova execução nesta tabela: [test_search_navigation_selection_and_rotation](../tests/test_gui.py); [test_intrinsic_rotation_and_cropbox_match_text_geometry](../tests/test_regressions.py).

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

Fontes: [app/search_engine.py](../app/search_engine.py), [app/main.py](../app/main.py), [app/rendering.py](../app/rendering.py), [docs/REA-BUSCA-IMPRESSAO.md](../docs/REA-BUSCA-IMPRESSAO.md), [docs/windows-evidence/foxit-rea/search-print-contracts.json](../docs/windows-evidence/foxit-rea/search-print-contracts.json).

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

Fontes: [app/search_engine.py](../app/search_engine.py), [app/pdf_panels.py](../app/pdf_panels.py), [docs/REA-BUSCA-IMPRESSAO.md](../docs/REA-BUSCA-IMPRESSAO.md), [docs/windows-evidence/foxit-rea/search-print-contracts.json](../docs/windows-evidence/foxit-rea/search-print-contracts.json), [docs/windows-evidence/foxit-rea/search-checkbox-bindings.json](../docs/windows-evidence/foxit-rea/search-checkbox-bindings.json).

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

Fontes: [app/search_engine.py](../app/search_engine.py), [app/pdf_panels.py](../app/pdf_panels.py), [docs/REA-BUSCA-IMPRESSAO.md](../docs/REA-BUSCA-IMPRESSAO.md), [docs/windows-evidence/foxit-rea/search-print-contracts.json](../docs/windows-evidence/foxit-rea/search-print-contracts.json).

Testes próprios existentes, sem nova execução nesta tabela: [test_comment_subject_and_contents_are_searchable_without_author](../tests/test_search_scopes.py).

Relacionados aos planos dinâmicos/UI: D08, D09.

<a id="search-attachments"></a>

## Busca em anexos

Requisito futuro: buscar texto em anexos suportados, preservando a origem de cada hit.

**Entradas**

- PDF com anexos, consulta, seletor de escopo e formatos de anexo explicitamente suportados.
- Limites de tamanho, recursão, tempo e cancelamento ainda a definir por contrato de formato.

**Saídas**

- Proposta: hits com caminho/identidade do anexo e localização interna distinguíveis da página principal.

**Erros e casos excepcionais**

- Anexo binário, cifrado ou formato sem extrator: Proposta: registrar anexo não pesquisado e razão, sem prometer que zero hits implica cobertura total.
- Anexo excede limite ou contém recursão: Proposta: interromper esse ramo e informar resultado parcial.

**Estado e efeitos**

- Proposta: extração temporária controlada, sem executar anexos ou modificar o original.

**Critérios planejados**

- **S12-07-1** (nominal, proposta futura, `not_run`): dado PDF sintético com anexo textual contendo alvo; fixture ainda a especializar. Ação: Pesquisar incluindo anexos. Esperado: Proposta: ao menos um hit identifica o anexo e não recebe uma página principal fictícia.
- **S12-07-2** (exception, proposta futura, `not_run`): dado Mesmo PDF com um anexo não suportado. Ação: Pesquisar incluindo anexos. Esperado: Proposta: indicar que esse anexo não foi pesquisado; não declarar cobertura integral.

**Lacunas da referência Foxit**

- Travessia completa, extratores, formatos, limites, ordenação e associação de resultados no original.

Fontes: [docs/REA-BUSCA-IMPRESSAO.md](../docs/REA-BUSCA-IMPRESSAO.md), [docs/windows-evidence/foxit-rea/search-print-contracts.json](../docs/windows-evidence/foxit-rea/search-print-contracts.json).

Relacionados aos planos dinâmicos/UI: D16.

<a id="search-index"></a>

## Índice persistente/pesquisa de coleção

Requisito futuro: índice persistente de coleção com identidade, atualização e consulta cancelável.

**Entradas**

- Lista explícita de diretórios/documentos locais e versão do índice.
- Consulta e política de inclusão/atualização; não indexar perfis pessoais implicitamente.

**Saídas**

- Proposta: índice versionado e hits identificando documento, posição e estado de atualização.

**Erros e casos excepcionais**

- Documento movido/alterado ou entrada obsoleta: Proposta: invalidar/reindexar a entrada e marcar resultados desatualizados.
- Índice corrompido ou disco sem espaço: Proposta: falhar sem substituir um índice íntegro por saída incompleta.

**Estado e efeitos**

- Proposta: escrita apenas no diretório de índice autorizado; fontes permanecem intactas.

**Critérios planejados**

- **S12-08-1** (nominal, proposta futura, `not_run`): dado Coleção sintética de dois documentos e índice em pasta nova. Ação: Construir índice e consultar um termo presente em um documento. Esperado: Proposta: hit identifica o documento correto e a versão do índice.
- **S12-08-2** (exception, proposta futura, `not_run`): dado Uma fonte foi alterada após indexação. Ação: Consultar sem atualização completa. Esperado: Proposta: resultado não deve ser apresentado como atual sem indicar/iniciar atualização.

**Lacunas da referência Foxit**

- Formato e manutenção do índice completo, exclusões, locking, recuperação e disponibilidade Reader.

Fontes: [docs/windows-evidence/foxit-rea/index-interface.json](../docs/windows-evidence/foxit-rea/index-interface.json), [docs/FOXIT-REA.md](../docs/FOXIT-REA.md).

<a id="search-language"></a>

## Stemming/proximidade/coringas

Requisito futuro: semânticas distintas de stemming, proximidade e coringas; não confundir com busca literal própria.

**Entradas**

- Consulta, idioma, modo e parâmetros de proximidade/coringas explícitos.
- Escopo e analisador de texto versionado.

**Saídas**

- Proposta: hits acompanhados do modo/analisador usado; resultados reprodutíveis para o corpus definido.

**Erros e casos excepcionais**

- Sintaxe ou combinação de flags não suportada: Proposta: rejeitar a consulta com motivo; não reinterpretar silenciosamente como busca literal.
- Expansão de termos excede limite: Proposta: limitar e indicar truncamento ou recusar a consulta.

**Estado e efeitos**

- Proposta: cancelamento e limites compartilhados com a consulta; original intacto.

**Critérios planejados**

- **S12-09-1** (nominal, proposta futura, `not_run`): dado Corpus sintético com duas palavras separadas por distâncias conhecidas. Ação: Executar proximidade com duas distâncias explícitas. Esperado: Proposta: a diferença de hits decorre da distância registrada e é reproduzível.
- **S12-09-2** (exception, proposta futura, `not_run`): dado Consulta com coringa/operador cuja sintaxe não foi implementada. Ação: Executar esse modo. Esperado: Proposta: erro claro, sem alegar equivalência ao Foxit.

**Lacunas da referência Foxit**

- Stemming por idioma, distância/proximidade, escaping, expansão e combinações com índice.

Fontes: [docs/REA-BUSCA-IMPRESSAO.md](../docs/REA-BUSCA-IMPRESSAO.md), [docs/windows-evidence/foxit-rea/search-print-contracts.json](../docs/windows-evidence/foxit-rea/search-print-contracts.json), [docs/ETAPA-11.md](../docs/ETAPA-11.md).

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

Fontes: [app/print_window.py](../app/print_window.py), [app/worker_cli.py](../app/worker_cli.py), [app/cups_backend.py](../app/cups_backend.py), [app/windows_print.py](../app/windows_print.py), [docs/REA-IMPRESSAO-CONSUMIDORES.md](../docs/REA-IMPRESSAO-CONSUMIDORES.md), [docs/windows-evidence/foxit-rea/windows-print-followup-contracts.json](../docs/windows-evidence/foxit-rea/windows-print-followup-contracts.json).

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

Fontes: [app/imposition.py](../app/imposition.py), [app/worker_cli.py](../app/worker_cli.py), [docs/REA-IMPRESSAO-CONSUMIDORES.md](../docs/REA-IMPRESSAO-CONSUMIDORES.md), [docs/windows-evidence/foxit-rea/windows-print-followup-contracts.json](../docs/windows-evidence/foxit-rea/windows-print-followup-contracts.json).

Testes próprios existentes, sem nova execução nesta tabela: [test_booklet_generated_sides_and_binding](../tests/test_regressions.py); [test_nup_worker_rejects_fractional_count](../tests/test_regressions.py); [test_worker_prepares_nup_and_poster](../tests/test_regressions.py).

Relacionados aos planos dinâmicos/UI: D18.

<a id="bookmarks-edit"></a>

## Criar/mover/gravar marcadores

Atual: painel de títulos/níveis/destinos somente leitura. Criar/mover/gravar marcadores permanece requisito futuro.

**Entradas**

- PDF e outline; títulos, níveis e destinos locais ou ausentes.
- Edição futura exigirá operação explícita e destino de cópia.

**Saídas**

- Atual: lista de marcadores com title, page e level.
- Proposta futura: outline alterado em cópia, conservando títulos/destinos não editados.

**Erros e casos excepcionais**

- Destino ausente ou não resolvido: Painel mantém page=null; não inventar página.
- Outline parcial ou objeto malformado: Leitura tolera partes não resolvidas; integridade completa e diagnóstico detalhado ainda são lacunas.

**Estado e efeitos**

- Atual não grava outline nem PDF; edição/undo/persistência não implementados.

**Critérios planejados**

- **S12-13-1** (nominal, contrato próprio atual, `not_run`): dado Fixture com dois marcadores. Ação: Inspecionar o painel. Esperado: Dois títulos, nível registrado e destino local conhecido ou null; nenhuma escrita no PDF.
- **S12-13-2** (exception, contrato próprio atual, `not_run`): dado Marcador sem página local. Ação: Exibir seu destino. Esperado: Não atribuir a primeira página por padrão.

**Lacunas da referência Foxit**

- Disponibilidade Reader dos diálogos, movimento hierárquico, undo/redo e persistência.

Fontes: [app/pdf_panels.py](../app/pdf_panels.py), [docs/FOXIT-REA.md](../docs/FOXIT-REA.md), [docs/ETAPA-11.md](../docs/ETAPA-11.md).

Testes próprios existentes, sem nova execução nesta tabela: [test_bookmark_without_local_page_is_not_given_a_fake_destination](../tests/test_search_scopes.py).

Relacionados aos planos dinâmicos/UI: D07, UI09, UI10.

<a id="annotations"></a>

## Anotações/undo/gravação

Atual: leitura de comentários/anotações de tipos selecionados. Criar/editar/undo/gravar são futuros.

**Entradas**

- PDF com /Annots; subtype, /Contents, /Subj, /T e página.
- Tipos atuais incluem nota, texto, destaque, sublinhado, desenho e outros enumerados no painel.

**Saídas**

- Atual: page, type, author, text de exibição, contents e subject separados.
- Proposta futura: alterações serializadas com aparência e histórico em cópia.

**Erros e casos excepcionais**

- Anotação individual não pode ser decodificada: O painel ignora esse objeto e continua; não afirmar inventário integral.
- Tipo não pertence ao conjunto lido: Não é exposto como comentário suportado por essa rotina.

**Estado e efeitos**

- Atual não muda anotação, undo ou arquivo.

**Critérios planejados**

- **S12-14-1** (nominal, contrato próprio atual, `not_run`): dado Fixture com nota contendo assunto e conteúdo distintos. Ação: Inspecionar o painel. Esperado: Assunto separado, comentário alvo e autor permanecem campos distintos na página conhecida.
- **S12-14-2** (exception, contrato próprio atual, `not_run`): dado Objeto de anotação isolado inválido. Ação: Ler os demais comentários. Esperado: A falha de um objeto não deve ser reportada como criação/edição bem-sucedida de anotação.

**Lacunas da referência Foxit**

- Replies, aparências, edição, autoria, undo/redo, salvamento e disponibilidade Reader.

Fontes: [app/pdf_panels.py](../app/pdf_panels.py), [app/search_engine.py](../app/search_engine.py), [docs/FOXIT-REA.md](../docs/FOXIT-REA.md).

Testes próprios existentes, sem nova execução nesta tabela: [test_comment_subject_and_contents_are_searchable_without_author](../tests/test_search_scopes.py).

Relacionados aos planos dinâmicos/UI: D08, D09, D19.

<a id="forms"></a>

## AcroForm/XFA/eventos

Requisito futuro: separar AcroForm de XFA e tratar campos, validação, eventos e persistência por tecnologia.

**Entradas**

- PDF sintético com campos e valores tipados, tecnologia identificada e operação de edição.
- Política explícita para JavaScript/eventos e arquivo de saída.

**Saídas**

- Proposta: valores/estados de campo e cópia reabrível; suporte declarado por tecnologia, sem prometer XFA por presença de AcroForm.

**Erros e casos excepcionais**

- Valor não passa validação de campo: Proposta: recusar/indicar o erro sem registrar valor como aceito.
- Tecnologia/evento não suportado: Proposta: declarar limitação; não executar código ou alegar persistência de campo não compreendido.

**Estado e efeitos**

- Proposta: operações sobre cópia sintética; original e ações externas preservados.

**Critérios planejados**

- **S12-15-1** (nominal, proposta futura, `not_run`): dado AcroForm sintético de texto e escolha, fixture ainda a criar. Ação: Alterar valores e salvar cópia. Esperado: Proposta: reabrir a cópia preserva valores e tipos definidos no corpus.
- **S12-15-2** (exception, proposta futura, `not_run`): dado Campo com restrição conhecida e valor inválido. Ação: Tentar confirmar a edição. Esperado: Proposta: erro identificável e valor anterior preservado.

**Lacunas da referência Foxit**

- Motor de formulários, eventos, XFA, cálculo/validação e gravação; FRMSPlgV2 é RMS, não prova de formulários.

Fontes: [docs/FOXIT-REA.md](../docs/FOXIT-REA.md).

<a id="attachments"></a>

## Anexos/portfólios

Atual: backend/worker e código GTK de painel para listar/salvar anexo do catálogo plano. Controlador portável testado; execução GTK ainda pendente. Portfólios, /Kids e anexos exclusivos de anotações ficam pendentes.

**Entradas**

- PDF local com catálogo plano de anexos; operação de listar sem decodificar payloads.
- Índice da entrada, SHA-256 da listagem e pasta de destino existente controlada pelo usuário.
- No painel: selecionar entrada, escolher pasta e confirmar; cancelar não inicia extração.

**Saídas**

- Listagem com índices distintos, nomes, tamanho declarado opcional e indicação de nome permitido; tamanho declarado não é tamanho medido.
- Extração retorna nome/caminho, tamanho real e hash SHA-256 dos bytes; mantém o PDF original.
- Código da UI: lista sob demanda, seleção, Salvar selecionado e estados de carga/erro; widgets ainda não executados neste ambiente.

**Erros e casos excepcionais**

- Caminhos, nomes reservados, caracteres de controle ou nome fora do limite: Recusar extração antes de criar arquivo; a listagem conserva o nome e indica a recusa.
- Destino já existe, inclusive outra entrada com o mesmo nome: FileExistsError, sem sobrescrita; escolher outra pasta para extrair essa entrada.
- PDF mudou, índice/hash inválido, pasta ausente ou payload acima de 64 MiB: Falha explícita antes da gravação; tamanho real é checado após decodificar o stream.
- Portfólio /Collection, árvore /Kids ou senha não vazia necessária: Recurso ainda não suportado; não apresentar inventário vazio como sucesso.
- Seleção/documento mudou durante a escolha de pasta ou resultado assíncrono tornou-se obsoleto: Token de seleção inválido não inicia extração; callbacks antigos não substituem dados/estado do novo documento.

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
- Execução do painel GTK/Linux, portfólios, /Kids, anexos exclusivos de anotações e senha continuam pendentes; comportamento Foxit não observado.

Fontes: [app/pdf_attachments.py](../app/pdf_attachments.py), [app/worker_cli.py](../app/worker_cli.py), [app/attachment_tasks.py](../app/attachment_tasks.py), [app/main.py](../app/main.py), [docs/FOXIT-REA.md](../docs/FOXIT-REA.md).

Testes próprios existentes, sem nova execução nesta tabela: [test_listing_keeps_duplicate_entries_and_does_not_decode_payloads](../tests/test_pdf_attachments.py); [test_extract_preserves_binary_content_hash_and_original](../tests/test_pdf_attachments.py); [test_unsafe_pdf_names_are_reported_and_refused_without_writes](../tests/test_pdf_attachments.py); [test_worker_protocol_lists_extracts_and_reports_conflict](../tests/test_pdf_attachments.py); [test_stale_listing_callback_cannot_replace_a_new_document](../tests/test_attachment_tasks.py); [test_real_worker_extracts_selected_attachment_and_restores_buttons](../tests/test_attachment_tasks.py); [test_refresh_invalidates_the_selection_captured_before_a_dialog](../tests/test_attachment_tasks.py).

Relacionados aos planos dinâmicos/UI: D16.

<a id="signatures"></a>

## Assinaturas/certificados

Requisito futuro: distinguir aparência de assinatura, assinatura criptográfica e validação de certificado.

**Entradas**

- PDF de laboratório assinado e material de confiança de teste; nenhum certificado pessoal.
- Operação de inspecionar/validar; assinatura futura exige chave e autorização separadas.

**Saídas**

- Proposta: estado de integridade criptográfica separado de confiança/tempo/revogação e da aparência visual.

**Erros e casos excepcionais**

- Sem dados de confiança/revogação offline: Proposta: resultado indeterminado para essa dimensão; não apresentar validade global.
- Bytes assinados foram alterados: Proposta: informar falha de integridade mesmo se a aparência continuar visível.

**Estado e efeitos**

- Proposta: validação local não assina nem altera PDF; nenhuma chave real ou serviço remoto nesta fase.

**Critérios planejados**

- **S12-17-1** (nominal, proposta futura, `not_run`): dado PDF assinado por certificado sintético e trust store de laboratório. Ação: Inspecionar assinatura offline. Esperado: Proposta: relatar integridade, confiança e indisponibilidade de revogação como dimensões distintas.
- **S12-17-2** (exception, proposta futura, `not_run`): dado Cópia com modificação dentro da região assinada. Ação: Revalidar. Esperado: Proposta: falha de integridade, sem confundir a imagem da assinatura com prova criptográfica.

**Lacunas da referência Foxit**

- Fluxos Reader, assinatura versus validação, cadeias, políticas e comportamento offline; plugins não provam suporte completo.

Fontes: [docs/FOXIT-REA.md](../docs/FOXIT-REA.md).

<a id="security"></a>

## Senhas/permissões/RMS

Requisito futuro: senha e permissões PDF separadas de RMS/serviços externos. Atual só tenta senha vazia.

**Entradas**

- PDF cifrado sintético, senha conhecida de laboratório e política de permissões.
- Cancelar/abrir, sem recuperar senha nem contornar mecanismos do documento.

**Saídas**

- Proposta: abertura autenticada ou recusa; permissões e proteção externa identificadas separadamente.

**Erros e casos excepcionais**

- Senha incorreta ou cancelamento: Proposta: não expor conteúdo como se autenticado e não gravar senha em logs.
- RMS requer serviço indisponível offline: Proposta: declarar indisponibilidade, sem bypass nem falso estado desbloqueado.

**Estado e efeitos**

- Proposta: manter segredo apenas no escopo necessário; original cifrado permanece íntegro.

**Critérios planejados**

- **S12-18-1** (nominal, proposta futura, `not_run`): dado PDF cifrado com senha sintética conhecida. Ação: Abrir com a senha correta em ambiente de teste. Esperado: Proposta: conteúdo autorizado acessível; senha não aparece no relatório de evidências.
- **S12-18-2** (exception, proposta futura, `not_run`): dado Mesmo PDF com senha errada ou cancelamento. Ação: Tentar abrir. Esperado: Proposta: recusa/cancelamento distinto de sucesso; original inalterado.

**Lacunas da referência Foxit**

- Entrada de senha, enforcement de permissões, RMS e mensagens do original; o fluxo completo não está implementado.

Fontes: [docs/FOXIT-REA.md](../docs/FOXIT-REA.md).

Relacionados aos planos dinâmicos/UI: D15.

<a id="accessibility"></a>

## Acessibilidade/voz

Requisito futuro: estrutura acessível, teclado e leitura por voz com ordem e tecnologia assistiva verificadas.

**Entradas**

- PDF marcado sintético, idioma, foco e ação por teclado.
- Tecnologia assistiva/voz identificada; texto alternativo e ordem lógica de referência.

**Saídas**

- Proposta: nomes/papéis/estados acessíveis e sequência de leitura comparável ao corpus, sem alegar conformidade ainda.

**Erros e casos excepcionais**

- PDF sem tags ou ordem incompleta: Proposta: indicar limitação e distinguir extração visual de ordem semântica.
- Síntese de voz indisponível: Proposta: informar indisponibilidade sem travar navegação/fechamento.

**Estado e efeitos**

- Proposta: áudio apenas quando solicitado; sem envio de conteúdo a serviço externo implícito.

**Critérios planejados**

- **S12-19-1** (nominal, proposta futura, `not_run`): dado PDF de duas colunas com tags e ordem esperada, fixture a criar. Ação: Percorrer por teclado/leitor de tela. Esperado: Proposta: sequência e nomes registrados contra a ordem definida no corpus.
- **S12-19-2** (exception, proposta futura, `not_run`): dado Mesmo teste sem serviço de voz instalado. Ação: Solicitar leitura por voz. Esperado: Proposta: indisponibilidade explícita e UI responsiva.

**Lacunas da referência Foxit**

- APIs, árvore acessível, ordem, voz, foco, atalhos e cobertura real do Reader.

Fontes: [docs/FOXIT-REA.md](../docs/FOXIT-REA.md).

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

Preferência própria system/light/dark com migração legada e persistência; sem equivalência de todos os ajustes Foxit.

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

Fontes: [app/appearance.py](../app/appearance.py), [docs/FOXIT-REA.md](../docs/FOXIT-REA.md).

Testes próprios existentes, sem nova execução nesta tabela: [test_theme_persistence_and_contrast](../tests/test_viewer.py); [test_fresh_system_theme_initializes_and_migrates_legacy](../tests/test_consolidation.py).

<a id="cloud"></a>

## Nuvem/colaboração

Requisito futuro: integrações por provedor explícito, com contas/consentimento e estado offline separados.

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

Fontes: [docs/FOXIT-REA.md](../docs/FOXIT-REA.md).

<a id="conversion"></a>

## Criação/conversão

Requisito futuro: separar criação PDF de exportação/reformatação e identificar o que existe no Reader versus Editor.

**Entradas**

- Formato fonte sintético explicitamente suportado, opções e caminho novo de saída.
- Nenhum recurso pago/Editor é presumido por aparecer em um template.

**Saídas**

- Proposta: arquivo reabrível no formato declarado e relatório de perdas/limitações.
- Exportar página PNG já existente não significa conversão completa para formatos editáveis.

**Erros e casos excepcionais**

- Formato ou recurso não suportado: Proposta: recusar com identificação do formato, sem criar saída com extensão enganosa.
- Falha durante conversão: Proposta: não apresentar arquivo parcial como exportação concluída.

**Estado e efeitos**

- Proposta: fontes intactas e saída separada; sem serviço remoto implícito.

**Critérios planejados**

- **S12-24-1** (nominal, proposta futura, `not_run`): dado Fonte sintética de formato escolhido e contrato ainda a especializar. Ação: Converter para PDF em caminho novo. Esperado: Proposta: PDF reabre e conserva páginas/texto dentro da tolerância que o contrato de formato definir.
- **S12-24-2** (exception, proposta futura, `not_run`): dado Formato fora da lista suportada. Ação: Solicitar conversão. Esperado: Proposta: recusa explícita; não apenas renomear extensão.

**Lacunas da referência Foxit**

- Inventário real Reader/Editor, fidelidade, formatos, OCR e serviços; não implementado como família completa.

Fontes: [docs/FOXIT-REA.md](../docs/FOXIT-REA.md).

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
