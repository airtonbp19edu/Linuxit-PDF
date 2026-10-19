# Inventário operacional provisório — P01

Revisão 14, conferida em 2026-10-19T14:36:34.919108-03:00. **111 recortes conhecidos em 25 famílias; inventário global aberto.**

Fonte: [catálogo estruturado](../progresso/inventario-operacoes-v1.json). [Execução dos lotes](LOTES-FUNCIONALIDADES.md).

**Não é percentual de reconstrução.** Código delimitado, testes próprios, observações parciais do original e aceitação integral são estados distintos. Nenhuma família integral foi aprovada; todos os 50 planos completos S12 permanecem abertos.

Evidência própria atual: **490 testes Linux aprovados**, [casos e hashes](../testes/resultados/lotes-2026-10-19/release-validated-cases.json). A evidência informa separadamente os ambientes executados. Os403 testes/106 arquivos da revisão inicial são evidência histórica, sem aprovação integral das operações.

## Estado por família

Zero na coluna de pendências significa somente que os recortes listados têm código. Não encerra a família, seu inventário global ou suas lacunas.

| Família | Recortes | Código delimitado | Pendentes | Adiados |
|---|---:|---:|---:|---:|
|Abrir PDF e renderizar páginas|6|6|0|0|
|Navegação/rotação/zoom|4|4|0|0|
|Apresentação ajustar/preencher|3|3|0|0|
|Busca literal/palavra inteira/maiúsculas|6|6|0|0|
|Busca em marcadores|2|2|0|0|
|Busca em comentários|3|3|0|0|
|Busca em anexos|3|3|0|0|
|Índice persistente/pesquisa de coleção|3|3|0|0|
|Stemming/proximidade/coringas|3|3|0|0|
|Seleção/cópia/snapshot|3|2|1|0|
|Prévia/plano de impressão|4|2|2|0|
|Livreto/N-up/mosaico|3|3|0|0|
|Criar/mover/gravar marcadores|4|4|0|0|
|Anotações/undo/gravação|13|13|0|0|
|AcroForm/XFA/eventos|9|7|2|0|
|Anexos/portfólios|4|4|0|0|
|Assinaturas/certificados|5|3|2|0|
|Senhas/permissões/RMS|5|4|1|0|
|Acessibilidade/voz|4|3|1|0|
|Medição/calibração|4|4|0|0|
|Camadas/mídia/3D|4|2|2|0|
|Preferências/tema/persistência|3|3|0|0|
|Nuvem/colaboração|3|0|0|3|
|Criação/conversão|5|5|0|0|
|Integrações de sistema/atualização|5|1|4|0|
|Total|111|93|15|3|

## Abrir PDF e renderizar páginas

Abertura/erros/cópia em recortes; senha correta em abertura independenteD15 abriu8 páginas. Não é contrato completo de recuperação/renderização.

**Lacunas da família:** Broad damaged/encrypted format corpus, permission/edit/print integration beyond this reading subset and full original lifecycle comparison remain open.

| Operação | Estado do código | Aceitação e limites do recorte |
|---|---|---|
|`open-render/inspect` — Inspecionar páginas, caixas e metadados|Código em subconjunto ([fonte](../app/rendering.py#L67))|PDF local legível => páginas/tamanhos/metadados; erro de parser não produz documento válido fictício.|
|`open-render/render` — Renderizar página e reutilizar cache|Código em subconjunto ([fonte](../app/rendering.py#L126))|PDF, página e largura => imagem válida associada à identidade do documento; cache não mistura documentos.|
|`open-render/obsolete` — Descartar renderização obsoleta|Código em subconjunto ([fonte](../app/main.py#L1064))|Troca/fechamento durante render => callback antigo não substitui documento atual.|
|`open-render/copy` — Salvar cópia local completa e exclusiva|Código em subconjunto ([fonte](../app/local_files.py#L106))|Origem identificada e destino novo => cópia completa sem sobrescrita; não afirmar sincronização remota.|
|`open-render/password-open` — Abrir PDF cifrado integrado ao leitor|Código em subconjunto ([fonte](../app/document_session.py#L35))|Credential via stdin, private reading representation and first-render commit; reject/cancel preserves prior document. Original unchanged; printing the representation remains refused.|
|`open-render/recovery` — Recuperar documentos danificados|Código em subconjunto ([fonte](../app/document_session.py#L35))|Explicit consent permits pypdf best-effort recovery; broken xref fixture opens, irrecoverable input fails without replacing prior document. No universal repair guarantee.|

## Navegação/rotação/zoom

UI03/04 em geometria.pdf: sem documento controles pálidos; Next1→2→3, Last8/8 e Next mantém8/8. Menu1% e6400%; menos/mais nos extremos mantêm os valores. FitPage47.15%, PAGE0011/8. Recorte visual sem vínculo comprovado aos IDs estáticos; entradas arbitrárias e demais modos abertos.

**Lacunas da família:** Complete original modes/inputs/focus and static-ID correspondence remain open; own input/zoom/CropBox/rotation controls passed in0.1.14.

| Operação | Estado do código | Aceitação e limites do recorte |
|---|---|---|
|`navigation/goto` — Ir para página válida|Código em subconjunto ([fonte](../app/main.py#L1194))|Documento e índice => página correta; limites/sem documento não acessam índice inválido.|
|`navigation/zoom` — Aplicar zoom e ajuste|Código em subconjunto ([fonte](../app/main.py#L1246))|Zoom/ajuste e viewport => página posicionada no recorte próprio; limites Foxit ainda requerem UI04.|
|`navigation/view-rotation` — Rotacionar visualização|Código em subconjunto ([fonte](../app/main.py#L1254))|Rotação visual => tela e coordenadas coerentes sem alterar arquivo fonte.|
|`navigation/saved-rotation` — Persistir rotação em cópia|Código em subconjunto ([fonte](../app/pdf_changes.py#L274))|Página e ângulo aceito => /Rotate persistido na cópia, fonte preservada.|

## Apresentação ajustar/preencher

No dynamic observation of this family found in the examined preserved reports.

**Lacunas da família:** Real Linux desktop/compositor and physical dual-monitor/hotplug behavior; original presentation remains unobserved. Own GTK control tests and virtual desktop evidence are separate.

| Operação | Estado do código | Aceitação e limites do recorte |
|---|---|---|
|`presentation/fit-fill` — Apresentar com ajustar/preencher|Código em subconjunto ([fonte](../app/presentation.py#L320))|Página e modo ajustar/preencher => enquadramento esperado no contrato próprio.|
|`presentation/pan` — Mover página na apresentação|Código em subconjunto ([fonte](../app/presentation.py#L427))|Página retrato/paisagem e movimento => pan limitado ao conteúdo e viewport.|
|`presentation/monitors` — Apresentar em múltiplos monitores|Código em subconjunto ([fonte](../app/presentation.py#L158))|Select enumerated GDK monitor and request fullscreen; track granted state, fallback on removal. Physical compositor/device behavior and Foxit comparison remain open.|

## Busca literal/palavra inteira/maiúsculas

D12 no corpus5000: Stop ativo encerra e preserva232 resultados; troca para geometria mantém busca em12.pdf; fechar12.pdf durante busca encerra em1738 e conserva lista parcial. Contagens não determinísticas/latência não medida; contrato próprio não substituído. D10 misto anterior preservado.

**Lacunas da família:** Destinos e ordenação mista, destaques, normalização completa, limites/cancelamento e vazio sem presumir retorno de backend.

| Operação | Estado do código | Aceitação e limites do recorte |
|---|---|---|
|`search-text/literal` — Pesquisar texto literal|Código em subconjunto ([fonte](../app/search_engine.py#L161))|Consulta literal em páginas => contagem, origem e coordenadas; opções de fontes explícitas.|
|`search-text/whole` — Aplicar palavra inteira|Código em subconjunto ([fonte](../app/search_matching.py#L59))|Consulta e texto => respeitar fronteiras de palavra do contrato próprio.|
|`search-text/case` — Distinguir maiúsculas/minúsculas|Código em subconjunto ([fonte](../app/search_matching.py#L5))|Consulta e opção de caixa => resultados conforme configuração, inclusive expansão casefold.|
|`search-text/normalization` — Normalizar acentos e hifenização|Código em subconjunto ([fonte](../app/search_engine.py#L32))|Texto/colunas => normalização própria sem unir colunas indevidamente; algoritmo Foxit completo aberto.|
|`search-text/highlight` — Destacar e navegar por ocorrências|Código em subconjunto ([fonte](../app/main.py#L1833))|Resultado e destaque global => pixels/navegação atualizados sem nova busca indevida.|
|`search-text/cancel` — Cancelar pesquisa e descartar resultados antigos|Código em subconjunto ([fonte](../app/main.py#L1891))|Consulta alterada/fechamento => encerrar tarefa antiga e não repopular resultados obsoletos.|

## Busca em marcadores

D07: dois hits selecionam marcadores no painel; ativação nativa do primeiro navega1→2. Seleção/duplo clique no resultado não provou salto; segundo mantém página2 sem diálogo. Não inferir destino nulo.

**Lacunas da família:** Ativação/destinos dos dois resultados, ordenação e associação dinâmica 7911/7913.

| Operação | Estado do código | Aceitação e limites do recorte |
|---|---|---|
|`search-bookmarks/titles` — Pesquisar títulos de marcadores|Código em subconjunto ([fonte](../app/search_engine.py#L127))|Consulta só marcadores => resultados independentes com destino local quando conhecido.|
|`search-bookmarks/destinations` — Ativar resultados com destino válido ou ausente|Código em subconjunto ([fonte](../app/main.py#L1833))|Hit com página ou sem destino => navegar apenas quando conhecido; não inventar página0. Ativação Foxit ainda inconclusiva.|

## Busca em comentários

Recortes de corpo/assunto/autor preservados; D10 seleciona nota na página1 e abre Format sem editar. Autor corrigido somente na fonte; demais tipos/respostas ainda abertos.

**Lacunas da família:** Demais tipos/campos/respostas, duplicação, destinos e ordenação; empacotar correção de autor já validada na fonte.

| Operação | Estado do código | Aceitação e limites do recorte |
|---|---|---|
|`search-comments/body-subject` — Pesquisar assunto/conteúdo de comentário|Código em subconjunto ([fonte](../app/search_engine.py#L127))|Nota sintética e consulta => assunto e conteúdo pesquisáveis; fontes/ordem explícitas.|
|`search-comments/author` — Pesquisar autor de comentário|Código em subconjunto ([fonte](../app/search_engine.py#L127))|Autor1 na nota preservada => um hit página1; correção na fonte posterior ao Flatpak.|
|`search-comments/replies` — Pesquisar respostas e demais tipos/campos|Código em subconjunto ([fonte](../app/pdf_comments.py#L47))|Own inspection exposes stable object IDs, parent/type/depth, deduplicates aliases, preserves distinct same-text objects, reports invalid/partial graphs. Runtime validation pending; no equivalence asserted.|

## Busca em anexos

No dynamic observation of this family found in the examined preserved reports.

**Lacunas da família:** Travessia/extratores/formatos/limites e associação de resultados comparados com o original.

| Operação | Estado do código | Aceitação e limites do recorte |
|---|---|---|
|`search-attachments/utf8` — Pesquisar anexo UTF-8|Código em subconjunto ([fonte](../app/attachment_search.py#L24))|Anexo UTF8/BOM => hits ligados à identidade do anexo; nenhuma execução de anexo.|
|`search-attachments/pdf` — Pesquisar texto de PDF anexado|Código em subconjunto ([fonte](../app/attachment_search.py#L24))|PDF anexado => página interna separada da página do hospedeiro e omissões explícitas.|
|`search-attachments/formats` — Cobrir demais extratores e travessia completa|Código em subconjunto ([fonte](../app/attachment_formats.py#L34))|Formato/catálogo ainda não suportado => caracterizar extração/limites/ordem; não converter omissão em busca completa.|

## Índice persistente/pesquisa de coleção

No dynamic observation of this family found in the examined preserved reports.

**Lacunas da família:** Disponibilidade Reader, manutenção/exclusões/locking/recuperação e formatos do índice; caracterizar suporte antes de ampliar.

| Operação | Estado do código | Aceitação e limites do recorte |
|---|---|---|
|`search-index/build` — Construir snapshot de coleção|Código em subconjunto ([fonte](../app/collection_index.py#L90))|PDFs escolhidos e índice local => snapshot versionado com identidade de fontes.|
|`search-index/query` — Consultar índice e excluir fonte alterada|Código em subconjunto ([fonte](../app/collection_index.py#L160))|Índice e consulta => hits de fontes válidas; fonte ausente/alterada excluída até rebuild explícito.|
|`search-index/maintenance` — Manter índice completo e recuperação|Código em subconjunto ([fonte](../app/collection_index.py#L90))|Índice Reader, exclusões e falha concorrente => formato/manutenção/locking a caracterizar; snapshot próprio não prova equivalência.|

## Stemming/proximidade/coringas

No dynamic observation of this family found in the examined preserved reports.

**Lacunas da família:** Stemming por idioma, distância/proximidade, escaping/expansão e combinação com índice.

| Operação | Estado do código | Aceitação e limites do recorte |
|---|---|---|
|`search-language/wildcard` — Pesquisar coringas por palavra|Código em subconjunto ([fonte](../app/search_matching.py#L95))|Token com coringa => casar palavras Unicode completas segundo contrato próprio.|
|`search-language/proximity` — Pesquisar proximidade ordenada|Código em subconjunto ([fonte](../app/search_matching.py#L95))|Termos e distância => respeitar ordem e palavras intermediárias no contrato próprio; algoritmo Foxit não confirmado.|
|`search-language/stemming` — Aplicar stemming por idioma|Código em subconjunto ([fonte](../app/search_matching.py#L95))|Idioma e consulta => regras de derivação/expansão a caracterizar; não implementado como algoritmo Foxit.|

## Seleção/cópia/snapshot

No dynamic observation of this family found in the examined preserved reports.

**Lacunas da família:** Ordem lógica/bidirecional, permissões, snapping e coordenadas em todos os modos previstos.

| Operação | Estado do código | Aceitação e limites do recorte |
|---|---|---|
|`selection/text` — Selecionar e copiar palavras por área|Código em subconjunto ([fonte](../app/main.py#L1745))|Região da visualização => palavras/cópia com transformação coerente no recorte próprio.|
|`selection/snapshot` — Copiar snapshot de região|Código em subconjunto ([fonte](../app/main.py#L1704))|Região da página => imagem do recorte, sem declarar ordem semântica de texto; teste dedicado não mapeado nesta revisão.|
|`selection/bidi` — Garantir ordem lógica e texto bidirecional|Pendente/caracterizar|PDF com colunas/texto bidirecional => ordenação, snapping e permissões ainda por especificar/comparar.|

## Prévia/plano de impressão

Duas novas saídas virtuais13.pdf/14.pdf; fechamento normal e consulta posterior sem Foxit/atualizador/splwow64, fila vazia. Espera histórica não reproduzida nem explicada; impressão física e fluxo completo abertos.

**Lacunas da família:** Predefinições/margens/fontes/flags e fluxo completo da fila; impressão física e encerramento após impressão.

| Operação | Estado do código | Aceitação e limites do recorte |
|---|---|---|
|`printing/preview` — Preparar prévia e opções de impressão|Código em subconjunto ([fonte](../app/print_window.py#L1261))|Documento e opções => prévia correspondente ao plano próprio; envio/saída final são controles separados.|
|`printing/submit` — Enviar arquivo ao backend Linux|Código em subconjunto ([fonte](../app/cups_backend.py#L397))|PDF preparado e destino => chamada ao backend e resultado de submissão; não prova papel impresso.|
|`printing/physical` — Imprimir e cancelar em dispositivo físico|Pendente/caracterizar|Impressora/papel reais => escala/margens/duplex/fila/cancelamento conferidos; ambiente ainda pendente.|
|`printing/shutdown` — Encerrar após impressão sem processo preso|Pendente/caracterizar|Trabalho/fechamento => inspecionar processos/esperas; splwow64 anterior continua sem causa definitiva.|

## Livreto/N-up/mosaico

N-up A4 retrato2x2/horizontal/margem4mm gerou2 páginas, sequência1-4/5-8 igual em C18-D18-nup. Mosaico200%/sobreposição5mm sem marcas/legendas gerou48 páginas, todas renderizadas. Livreto5mm/medianiz3mm, geometria e combinações completas ainda abertos.

**Lacunas da família:** Saída PDF com margens/medidas/ordem correspondentes, rotações e combinações de livreto/N-up/mosaico.

| Operação | Estado do código | Aceitação e limites do recorte |
|---|---|---|
|`imposition/booklet` — Compor livreto|Código em subconjunto ([fonte](../app/imposition.py#L277))|Páginas, papel, lado e encadernação => sequência/posições próprias; parâmetros/saída Foxit ainda inconclusivos.|
|`imposition/nup` — Compor N-up|Código em subconjunto ([fonte](../app/imposition.py#L215))|Páginas e grade/ordem => células e CropBox corretos no contrato próprio.|
|`imposition/poster` — Compor mosaico|Código em subconjunto ([fonte](../app/imposition.py#L525))|Página/escala/papel/sobreposição => tiles próprios; marcas dependem de Cairo e têm validação separada.|

## Criar/mover/gravar marcadores

No dynamic observation of this family found in the examined preserved reports.

**Lacunas da família:** Diálogos e persistência completa, disponibilidade Reader, hierarquia/destinos/histórico em comparação.

| Operação | Estado do código | Aceitação e limites do recorte |
|---|---|---|
|`bookmarks-edit/create` — Criar marcador em cópia|Código em subconjunto ([fonte](../app/pdf_changes.py#L274))|Título/página => novo marcador na cópia, arquivo original preservado.|
|`bookmarks-edit/rename` — Renomear marcador|Código em subconjunto ([fonte](../app/pdf_changes.py#L274))|Caminho/título => renomear o nó escolhido preservando destinos e estrutura.|
|`bookmarks-edit/move` — Mover subárvore de marcadores|Código em subconjunto ([fonte](../app/pdf_changes.py#L191))|Caminho, pai e posição => mover sem ciclos, preservando filhos/destinos/contagens.|
|`bookmarks-edit/delete` — Excluir subárvore em cópia|Código em subconjunto ([fonte](../app/pdf_changes.py#L191))|Caminho => excluir subárvore e manter árvore restante consistente.|

## Anotações/undo/gravação

No dynamic observation of this family found in the examined preserved reports.

**Lacunas da família:** Respostas/popup/vínculos, aparências e operações restantes; tipos simples atuais não aprovam edição universal.

| Operação | Estado do código | Aceitação e limites do recorte |
|---|---|---|
|`annotations/note` — Criar nota Text|Código em subconjunto ([fonte](../app/pdf_changes.py#L274))|Página, texto e retângulo => nota Text imprimível dentro do CropBox, em cópia.|
|`annotations/highlight` — Criar destaque de área|Código em subconjunto ([fonte](../app/pdf_changes.py#L274))|Página e retângulo => Highlight com QuadPoints e texto no recorte suportado.|
|`annotations/rectangle` — Criar retângulo|Código em subconjunto ([fonte](../app/pdf_changes.py#L274))|Retângulo dentro da página => Square imprimível com geometria persistida.|
|`annotations/underline` — Criar sublinhado|Código em subconjunto ([fonte](../app/pdf_annotations.py#L40))|Página e geometria válida => sublinhado com aparência vetorial própria embutida; fonte preservada.|
|`annotations/strikeout` — Criar tachado|Código em subconjunto ([fonte](../app/pdf_annotations.py#L40))|Página e geometria válida => tachado com aparência vetorial própria embutida; fonte preservada.|
|`annotations/squiggly` — Criar ondulado|Código em subconjunto ([fonte](../app/pdf_annotations.py#L40))|Página e geometria válida => ondulado com aparência vetorial própria embutida; fonte preservada.|
|`annotations/ellipse` — Criar elipse|Código em subconjunto ([fonte](../app/pdf_annotations.py#L40))|Página e geometria válida => elipse com aparência vetorial própria embutida; fonte preservada.|
|`annotations/line` — Criar linha|Código em subconjunto ([fonte](../app/pdf_annotations.py#L40))|Página e geometria válida => linha com aparência vetorial própria embutida; fonte preservada.|
|`annotations/comment-author` — Editar comentário e autor|Código em subconjunto ([fonte](../app/pdf_changes.py#L274))|Anotação simples desbloqueada e texto/autor => alterar/limpar metadados sem mudar geometria/aparência.|
|`annotations/delete` — Excluir anotação simples|Código em subconjunto ([fonte](../app/pdf_changes.py#L274))|Índice atual => excluir somente tipo simples sem bloqueios/vínculos/dependentes, preservando widgets.|
|`annotations/history` — Desfazer/refazer rascunho|Código em subconjunto ([fonte](../app/edit_history.py#L71))|Histórico do rascunho => reconstruir cursor correto sem alterar fonte/cópias já salvas.|
|`annotations/replies` — Editar respostas/popup e vínculos|Código em subconjunto ([fonte](../app/pdf_changes.py#L274))|Threads/popup/dependentes => caracterizar autoria, vínculos, persistência e disponibilidade Reader.|
|`annotations/freehand` — Desenho livre e demais tipos|Código em subconjunto ([fonte](../app/pdf_annotations.py#L110))|Geometria de desenho/tipo ainda ausente => especificar, implementar e comparar antes de declarar suporte.|

## AcroForm/XFA/eventos

No dynamic observation of this family found in the examined preserved reports.

**Lacunas da família:** Combo editável/texto livre/aparência primeiro; depois eventos, cálculo/validação, XFA e formas restantes de acordo com disponibilidade e contrato.

| Operação | Estado do código | Aceitação e limites do recorte |
|---|---|---|
|`forms/text` — Preencher campo Tx|Código em subconjunto ([fonte](../app/pdf_changes.py#L274))|Campo terminal e texto => respeitar ReadOnly/MaxLen herdados e persistir valor/aparência em cópia.|
|`forms/checkbox` — Marcar/desmarcar checkbox|Código em subconjunto ([fonte](../app/pdf_form_controls.py#L127))|Checkbox com aparências existentes e booleano => /V e /AS coerentes; ReadOnly recusado.|
|`forms/radio` — Selecionar radio simples|Código em subconjunto ([fonte](../app/pdf_form_controls.py#L127))|Grupo e estado válido => ativar somente widget selecionado; respeitar NoToggleToOff.|
|`forms/combo-fixed` — Selecionar combo sem texto livre|Código em subconjunto ([fonte](../app/pdf_form_controls.py#L127))|Opção existente => valor/índice/aparência coerentes; export/label preservados no subconjunto.|
|`forms/list-single` — Selecionar lista simples|Código em subconjunto ([fonte](../app/pdf_form_controls.py#L127))|Lista simples e opção ou vazio => seleção única ou limpeza consistente.|
|`forms/list-multiple` — Selecionar lista múltipla|Código em subconjunto ([fonte](../app/pdf_form_controls.py#L127))|Conjunto de exports => valores e índices canônicos persistidos sem duplicação.|
|`forms/combo-editable` — Preencher combo com texto livre|Código em subconjunto ([fonte](../app/pdf_form_controls.py#L127))|Texto fora de Opt em combo editável => gerar valor/aparência, preservar opções e ReadOnly; ainda recusado atualmente.|
|`forms/events` — Calcular e validar eventos de formulário|Pendente/caracterizar|Campo com cálculo/validação/evento => delimitar motor, regras e efeitos antes de implementação.|
|`forms/xfa` — Processar XFA|Pendente/caracterizar|Formulário XFA => disponibilidade e contrato do alvo ainda a caracterizar; edição atual recusa.|

## Anexos/portfólios

Anexo sintético listado/extraído,22bytes/hash iguais; políticas/portfólios completos abertos.

**Lacunas da família:** Portfólios e senha não vazia, políticas de extração; completar comparação e desktop/acessibilidade.

| Operação | Estado do código | Aceitação e limites do recorte |
|---|---|---|
|`attachments/list` — Listar catálogo/árvores/anotações|Código em subconjunto ([fonte](../app/pdf_attachments.py#L149))|PDF suportado => índices/nomes/origens de anexos sem decodificar payload na listagem.|
|`attachments/extract` — Extrair anexo sem sobrescrever|Código em subconjunto ([fonte](../app/pdf_attachments.py#L170))|Índice/hash e destino novo => bytes conferidos; nomes perigosos/mudança de fonte recusados.|
|`attachments/portfolio` — Abrir portfólio completo|Código em subconjunto ([fonte](../app/pdf_attachments.py#L149))|Portfólio => inventário e navegação/extração a caracterizar; subset atual recusa explicitamente.|
|`attachments/encrypted` — Extrair anexo com senha não vazia|Código em subconjunto ([fonte](../app/attachment_tasks.py#L92))|PDF cifrado com credencial conhecida => integração de senha/limites pendente; não contornar permissões.|

## Assinaturas/certificados

No dynamic observation of this family found in the examined preserved reports.

**Lacunas da família:** Assinatura de documentos, confiança/cadeia/revogação/tempo e PAdES/LTV; CMS atual só verifica integridade no recorte documentado.

| Operação | Estado do código | Aceitação e limites do recorte |
|---|---|---|
|`signatures/inspect` — Inspecionar campos e cobertura assinada|Código em subconjunto ([fonte](../app/pdf_signatures.py#L70))|Campos/ByteRange/Contents => cobertura da revisão e limites explícitos; não afirmar arquivo atual integralmente assinado indevidamente.|
|`signatures/cms-integrity` — Verificar integridade CMS offline|Código em subconjunto ([fonte](../app/pdf_signatures.py#L45))|CMS destacado e bytes => resultado de integridade separado de confiança de certificado.|
|`signatures/sign` — Assinar documento|Código em subconjunto ([fonte](../app/pdf_signing.py#L28))|Documento e certificado sintético autorizado => assinatura/persistência a especificar e implementar; inspeção atual não assina.|
|`signatures/trust` — Validar cadeia/confiança/revogação|Pendente/caracterizar|Certificado e política => confiança/cadeia/revogação ainda sem fluxo completo; não inferir de CMS íntegro.|
|`signatures/timestamp-ltv` — Processar carimbo de tempo/PAdES/LTV|Pendente/caracterizar|Assinatura e materiais de validação => contrato, tempo e cobertura ainda pendentes.|

## Senhas/permissões/RMS

Cancelar/senha errada anteriores e correta na abertura independenteD15. Permissões/RMS/fluxo universal não observados.

**Lacunas da família:** Fluxo cifrado integrado, aplicação de permissões e mensagens; RMS segue sem contrato completo e exige ambiente autorizado.

| Operação | Estado do código | Aceitação e limites do recorte |
|---|---|---|
|`security/inspect` — Autenticar senha conhecida e inspecionar permissões|Código em subconjunto ([fonte](../app/pdf_security.py#L66))|PDF e senha opcional => papel/autenticação/permissões ou erro sem expor segredo.|
|`security/protect` — Criar cópia AES-256|Código em subconjunto ([fonte](../app/pdf_security.py#L91))|PDF suportado e senhas/permissões => cópia AES256 nova; fonte/metadados/anexos preservados no recorte.|
|`security/owner-copy` — Criar cópia sem cifra com senha de proprietário|Código em subconjunto ([fonte](../app/pdf_security.py#L157))|Autenticação de proprietário => cópia legível nova; senha só de abertura insuficiente.|
|`security/enforcement` — Aplicar permissões em todos os fluxos|Código em subconjunto ([fonte](../app/pdf_attachments.py#L30))|Permissões PDF e leitura/cópia/impressão/edição => política consistente entre interfaces, workers e erro; fluxo global pendente.|
|`security/rms` — Processar proteção RMS autorizada|Pendente/caracterizar|Documento RMS e ambiente autorizado => caracterizar serviço/contrato sem contornar proteção; dependência externa não resolvida.|

## Acessibilidade/voz

No dynamic observation of this family found in the examined preserved reports.

**Lacunas da família:** AT-SPI/leitor de tela real, ordem semântica, voz, foco/atalhos e cobertura efetiva.

| Operação | Estado do código | Aceitação e limites do recorte |
|---|---|---|
|`accessibility/text` — Expor texto da página por ATK.Text|Código em subconjunto ([fonte](../app/accessible_reader.py#L12))|Página suportada => texto Poppler em Gtk.TextView/ATK.Text com limites; não é garantia de ordem semântica.|
|`accessibility/keyboard` — Navegar por regiões pelo teclado|Código em subconjunto ([fonte](../app/main.py#L2369))|F6/ShiftF6 e foco atual => regiões/nomes acessíveis e delegação de setas no recorte testado.|
|`accessibility/screen-reader` — Validar leitor de tela e ordem real|Pendente/caracterizar|Desktop AT-SPI e leitor de tela real => foco, ordem e feedback conferidos; CI sem barramento não aprova.|
|`accessibility/voice` — Ler em voz alta|Código em subconjunto ([fonte](../app/speech.py#L9))|Texto e controles de voz => disponibilidade Reader, síntese e interrupção ainda a delimitar; OCR não implementa voz.|

## Medição/calibração

No dynamic observation of this family found in the examined preserved reports.

**Lacunas da família:** Calibração/unidades, snapping/precisão, áreas e perímetros.

| Operação | Estado do código | Aceitação e limites do recorte |
|---|---|---|
|`measurement/distance` — Medir distância entre pontos|Código em subconjunto ([fonte](../app/main.py#L1764))|Dois pontos da visualização => distância convertida a centímetros no contrato atual; teste dedicado não mapeado.|
|`measurement/calibrate` — Calibrar escala e unidades|Código em subconjunto ([fonte](../app/measurement.py#L21))|Distância conhecida/unidade => calibração e snapping/precisão persistidos conforme contrato futuro.|
|`measurement/area` — Medir área|Código em subconjunto ([fonte](../app/measurement.py#L37))|Polígono/região => área em unidade calibrada; operação ainda pendente.|
|`measurement/perimeter` — Medir perímetro|Código em subconjunto ([fonte](../app/measurement.py#L37))|Traçado/polígono => perímetro em unidade calibrada; operação ainda pendente.|

## Camadas/mídia/3D

No dynamic observation of this family found in the examined preserved reports.

**Lacunas da família:** Alternar/persistir OCG, combinações, mídia/codecs/eventos e 3D conforme disponibilidade real do Reader.

| Operação | Estado do código | Aceitação e limites do recorte |
|---|---|---|
|`layers-media/list` — Listar nomes de camadas OCG|Código em subconjunto ([fonte](../app/pdf_panels.py#L34))|PDF com OCG => nomes listados; isso não altera visibilidade nem comprova suporte a mídia.|
|`layers-media/toggle` — Alternar e persistir visibilidade OCG|Código em subconjunto ([fonte](../app/pdf_layers.py#L39))|Combinação de camadas => render e estado de visibilidade coerentes; implementação/persistência pendentes.|
|`layers-media/media` — Reproduzir mídia embutida|Pendente/caracterizar|Mídia/codecs/eventos => caracterizar disponibilidade Reader e controles antes de implementar.|
|`layers-media/3d` — Interagir com conteúdo 3D|Pendente/caracterizar|U3D/conteúdo3D => caracterizar disponibilidade Reader/render/estado; presença de plugin não comprova suporte.|

## Preferências/tema/persistência

No dynamic observation of this family found in the examined preserved reports.

**Lacunas da família:** Defaults, persistência e interdependência dos ajustes restantes; tema/pastas atuais já preservados.

| Operação | Estado do código | Aceitação e limites do recorte |
|---|---|---|
|`preferences/theme` — Persistir e aplicar tema|Código em subconjunto ([fonte](../app/appearance.py#L39))|system/light/dark => persistência/migração e contraste no recorte próprio.|
|`preferences/folders` — Persistir pasta preferida e últimas pastas|Código em subconjunto ([fonte](../app/local_files.py#L27))|Pasta explícita local => preferência por operação, fallback e esquecimento sem apagar arquivos/contas.|
|`preferences/remaining` — Cobrir demais ajustes e defaults|Código em subconjunto ([fonte](../app/reading_preferences.py#L29))|Preferências do Reader => inventariar defaults/interdependência/esquema e implementar ajustes restantes.|

## Nuvem/colaboração

No dynamic observation of this family found in the examined preserved reports.

**Lacunas da família:** APIs/login/upload/colaboração remota adiados. Manter visíveis sem executá-los ou somar conclusão.

| Operação | Estado do código | Aceitação e limites do recorte |
|---|---|---|
|`cloud/login` — Autenticar provedor remoto|Adiado pelo usuário|Conta/provedor => integração adiada pelo usuário; não iniciar credenciais/APIs.|
|`cloud/transfer` — Transferir arquivos por API de nuvem|Adiado pelo usuário|Arquivos/provedor => upload/download direto adiados; cópia local não é transferência remota.|
|`cloud/collaboration` — Colaborar remotamente e resolver conflitos|Adiado pelo usuário|Participantes/versões => contratos remotos adiados; cliente sincronizador externo é fluxo separado.|

## Criação/conversão

No dynamic observation of this family found in the examined preserved reports.

**Lacunas da família:** Inventário Reader/Editor, formatos/conversões restantes, fidelidade/OCR e variantes recusadas; preservar TIFF multipágina 100/OCR 20 atuais.

| Operação | Estado do código | Aceitação e limites do recorte |
|---|---|---|
|`conversion/images` — Criar PDF de imagens simples|Código em subconjunto ([fonte](../app/pdf_creation.py#L104))|PNG/JPEG/BMP/WebP suportados e ordem/DPI => PDF RGB com geometria/proveniência e publicação exclusiva.|
|`conversion/tiff` — Expandir TIFF multipágina|Código em subconjunto ([fonte](../app/pdf_creation.py#L52))|TIFF válido => páginas em ordem e orientação, até100 totais; variantes inválidas recusadas sem saída parcial.|
|`conversion/ocr` — Gerar cópia PDF pesquisável local|Código em subconjunto ([fonte](../app/pdf_ocr.py#L96))|PDF/imagens e idioma por/eng => camada pesquisável local até20 páginas, limites/cancelamento; sem avaliação universal de acurácia.|
|`conversion/animation` — Converter animações/variantes ainda recusadas|Código em subconjunto ([fonte](../app/pdf_creation.py#L104))|Imagem animada/variante não suportada => definir frames, ordem e limites antes de suporte; recusa atual não é implementação.|
|`conversion/other-formats` — Cobrir demais conversões disponíveis no Reader|Código em subconjunto ([fonte](../app/pdf_creation.py#L104))|Formato de entrada/saída => inventário Reader versus Editor e fidelidade ainda abertos.|

## Integrações de sistema/atualização

No dynamic observation of this family found in the examined preserved reports.

**Lacunas da família:** Portais/concessão persistente reais, associação de arquivos, atualização/rollback e adaptador Windows posterior.

| Operação | Estado do código | Aceitação e limites do recorte |
|---|---|---|
|`platform/worker-runtime` — Selecionar runtime de worker|Código em subconjunto ([fonte](../app/platform_runtime.py#L7))|Ambiente/plataforma => Python/runtime pareado para subprocesso; não valida toda integração de sistema.|
|`platform/portal` — Validar portal real e concessão persistente|Pendente/caracterizar|Desktop/Flatpak e pasta foraHOME => selecionar, conceder/negar e reabrir após reinício; simulação de resposta do diálogo não aprova interação real.|
|`platform/association` — Associar e abrir PDF pelo desktop|Pendente/caracterizar|Arquivo e shell Linux => launcher/associação e parâmetros reais conferidos no desktop; cobertura completa pendente.|
|`platform/update` — Atualizar e reverter entrega|Pendente/caracterizar|Pacote/versão anterior => atualização/rollback e persistência a definir/validar; distribuição de bundle não fecha todo fluxo.|
|`platform/windows` — Validar Linuxit nativo no Windows|Pendente/caracterizar|Executável/adaptador Windows => UI, subprocessos, associação e impressão próprios; prioridade posterior ao Linux.|

## Limites da medição

As contagens não têm pesos de complexidade e o denominador completo é desconhecido. Recortes e testes relacionados não aprovam operações inteiras. Nuvem direta permanece adiada; IA generativa está excluída. A VM continua suspensa no checkpoint documentado em RETOMADA.md.
