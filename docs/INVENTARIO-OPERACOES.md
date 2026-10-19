# Inventário operacional provisório — P01

Revisão2 de evidência em 2026-10-19T00:36:40-03:00: [P03 parcial](P03-BUSCA-IMPRESSAO-2026-10-19.md); 111 recortes/25 famílias e estados de implementação preservados. Resumos de busca/impressão atualizados no JSON, sem aceitação integral. A revisão1 abaixo é histórica.

Revisão 1 em 2026-10-18T22:17:54-03:00. **111 recortes operacionais em 25 famílias.**

Fonte: [inventário estruturado](../progresso/inventario-operacoes-v1.json). [Reconciliação](../testes/resultados/p01-2026-10-18/reconciliation.json).

**Não é porcentagem de reconstrução.** As operações têm tamanhos diferentes, o inventário global permanece aberto e nenhum peso foi definido. O catálogo separa presença de código delimitado, testes relacionados já executados, observação parcial do original e equivalência ainda não verificada.

403 testes Linux são evidência anterior do CI 39172130287, não executados novamente. 106 arquivos atuais de app conferem com o manifesto desse CI. Todos os 50 planos completos S12 continuam not_run; nenhum teste relacionado aprova automaticamente uma operação inteira.

## Estado por família

“Código delimitado” indica um subconjunto rastreável, sem aceitação integral da operação. A coluna de pendências conta somente os recortes listados sem código; zero nessa coluna não encerra as lacunas da família descritas abaixo.

| Família | Recortes | Código delimitado | Pendentes/adiados | Original |
|---|---:|---:|---:|---|
|Abrir PDF e renderizar páginas|6|4|2|Subconjunto observado|
|Navegação/rotação/zoom|4|4|0|Subconjunto observado|
|Apresentação ajustar/preencher|3|2|1|Sem observação examinada|
|Busca literal/palavra inteira/maiúsculas|6|6|0|Subconjunto observado|
|Busca em marcadores|2|2|0|Subconjunto observado|
|Busca em comentários|3|2|1|Subconjunto observado|
|Busca em anexos|3|2|1|Sem observação examinada|
|Índice persistente/pesquisa de coleção|3|2|1|Sem observação examinada|
|Stemming/proximidade/coringas|3|2|1|Sem observação examinada|
|Seleção/cópia/snapshot|3|2|1|Sem observação examinada|
|Prévia/plano de impressão|4|2|2|Subconjunto observado|
|Livreto/N-up/mosaico|3|3|0|Subconjunto observado|
|Criar/mover/gravar marcadores|4|4|0|Sem observação examinada|
|Anotações/undo/gravação|13|11|2|Sem observação examinada|
|AcroForm/XFA/eventos|9|6|3|Sem observação examinada|
|Anexos/portfólios|4|2|2|Subconjunto observado|
|Assinaturas/certificados|5|2|3|Sem observação examinada|
|Senhas/permissões/RMS|5|3|2|Subconjunto observado|
|Acessibilidade/voz|4|2|2|Sem observação examinada|
|Medição/calibração|4|1|3|Sem observação examinada|
|Camadas/mídia/3D|4|1|3|Sem observação examinada|
|Preferências/tema/persistência|3|2|1|Sem observação examinada|
|Nuvem/colaboração|3|0|3|Sem observação examinada|
|Criação/conversão|5|3|2|Sem observação examinada|
|Integrações de sistema/atualização|5|1|4|Sem observação examinada|

## Abrir PDF e renderizar páginas

Abertura/erros/cópia em recortes; senha correta em abertura independente D15 abriu 8 páginas. Não é contrato completo de recuperação/renderização.

**Lacunas:** Abertura cifrada integrada, recuperação e demais falhas/cancelamento/renderização; testar o ciclo completo de documento e tarefas.

| Operação | Estado do código | Aceitação e limites |
|---|---|---|
|`open-render/inspect` — Inspecionar páginas, caixas e metadados|Código em subconjunto ([fonte](../app/rendering.py#L67))|PDF local legível => páginas/tamanhos/metadados; erro de parser não produz documento válido fictício.|
|`open-render/render` — Renderizar página e reutilizar cache|Código em subconjunto ([fonte](../app/rendering.py#L126))|PDF, página e largura => imagem válida associada à identidade do documento; cache não mistura documentos.|
|`open-render/obsolete` — Descartar renderização obsoleta|Código em subconjunto ([fonte](../app/main.py#L895))|Troca/fechamento durante render => callback antigo não substitui documento atual.|
|`open-render/copy` — Salvar cópia local completa e exclusiva|Código em subconjunto ([fonte](../app/local_files.py#L106))|Origem identificada e destino novo => cópia completa sem sobrescrita; não afirmar sincronização remota.|
|`open-render/password-open` — Abrir PDF cifrado integrado ao leitor|Pendente/caracterizar Reader|PDF protegido e senha conhecida => abrir/renderizar, cancelar ou rejeitar erro sem perder documento anterior; fluxo integrado ainda pendente.|
|`open-render/recovery` — Recuperar documentos danificados|Pendente/caracterizar Reader|PDF danificado recuperável ou irrecuperável => política e mensagens a caracterizar no Reader antes de implementar.|

## Navegação/rotação/zoom

Página/zoom/rotaçãoD03 em recorte e sequência1→8→1 no PDF cifradoD15; extremos/modos completos ainda abertos.

**Lacunas:** Limites/modos efetivos, estados primeira/intermediária/última/sem documento e interação com rotação/CropBox.

| Operação | Estado do código | Aceitação e limites |
|---|---|---|
|`navigation/goto` — Ir para página válida|Código em subconjunto ([fonte](../app/main.py#L1035))|Documento e índice => página correta; limites/sem documento não acessam índice inválido.|
|`navigation/zoom` — Aplicar zoom e ajuste|Código em subconjunto ([fonte](../app/main.py#L1076))|Zoom/ajuste e viewport => página posicionada no recorte próprio; limites Foxit ainda requerem UI04.|
|`navigation/view-rotation` — Rotacionar visualização|Código em subconjunto ([fonte](../app/main.py#L1084))|Rotação visual => tela e coordenadas coerentes sem alterar arquivo fonte.|
|`navigation/saved-rotation` — Persistir rotação em cópia|Código em subconjunto ([fonte](../app/pdf_changes.py#L264))|Página e ângulo aceito => /Rotate persistido na cópia, fonte preservada.|

## Apresentação ajustar/preencher

No dynamic observation of this family found in the examined preserved reports.

**Lacunas:** Ajustar/preencher, atalhos, foco e múltiplos monitores observados no alvo e validados no desktop.

| Operação | Estado do código | Aceitação e limites |
|---|---|---|
|`presentation/fit-fill` — Apresentar com ajustar/preencher|Código em subconjunto ([fonte](../app/presentation.py#L238))|Página e modo ajustar/preencher => enquadramento esperado no contrato próprio.|
|`presentation/pan` — Mover página na apresentação|Código em subconjunto ([fonte](../app/presentation.py#L339))|Página retrato/paisagem e movimento => pan limitado ao conteúdo e viewport.|
|`presentation/monitors` — Apresentar em múltiplos monitores|Pendente/caracterizar Reader|Desktop com monitores distintos => foco, tela escolhida e atalhos comparados; teste real pendente.|

## Busca literal/palavra inteira/maiúsculas

Literal/palavra/caixa/no-sources e missing-term exato em recortes. Consulta vazia sem resposta de backend continua inconclusiva.

**Lacunas:** Destinos e ordenação mista, destaques, normalização completa, limites/cancelamento e vazio sem presumir retorno de backend.

| Operação | Estado do código | Aceitação e limites |
|---|---|---|
|`search-text/literal` — Pesquisar texto literal|Código em subconjunto ([fonte](../app/search_engine.py#L145))|Consulta literal em páginas => contagem, origem e coordenadas; opções de fontes explícitas.|
|`search-text/whole` — Aplicar palavra inteira|Código em subconjunto ([fonte](../app/search_matching.py#L55))|Consulta e texto => respeitar fronteiras de palavra do contrato próprio.|
|`search-text/case` — Distinguir maiúsculas/minúsculas|Código em subconjunto ([fonte](../app/search_matching.py#L5))|Consulta e opção de caixa => resultados conforme configuração, inclusive expansão casefold.|
|`search-text/normalization` — Normalizar acentos e hifenização|Código em subconjunto ([fonte](../app/search_engine.py#L32))|Texto/colunas => normalização própria sem unir colunas indevidamente; algoritmo Foxit completo aberto.|
|`search-text/highlight` — Destacar e navegar por ocorrências|Código em subconjunto ([fonte](../app/main.py#L1570))|Resultado e destaque global => pixels/navegação atualizados sem nova busca indevida.|
|`search-text/cancel` — Cancelar pesquisa e descartar resultados antigos|Código em subconjunto ([fonte](../app/main.py#L1625))|Consulta alterada/fechamento => encerrar tarefa antiga e não repopular resultados obsoletos.|

## Busca em marcadores

Dois resultados e seleção observados; ativação/destinos permanecem inconclusivos.

**Lacunas:** Ativação/destinos dos dois resultados, ordenação e associação dinâmica 7911/7913.

| Operação | Estado do código | Aceitação e limites |
|---|---|---|
|`search-bookmarks/titles` — Pesquisar títulos de marcadores|Código em subconjunto ([fonte](../app/search_engine.py#L117))|Consulta só marcadores => resultados independentes com destino local quando conhecido.|
|`search-bookmarks/destinations` — Ativar resultados com destino válido ou ausente|Código em subconjunto ([fonte](../app/main.py#L1570))|Hit com página ou sem destino => navegar apenas quando conhecido; não inventar página0. Ativação Foxit ainda inconclusiva.|

## Busca em comentários

Corpo/assunto/autor da nota sintética observados. Autor corrigido na fonte; demais tipos e busca mista abertos.

**Lacunas:** Demais tipos/campos/respostas, duplicação, destinos e ordenação; empacotar correção de autor já validada na fonte.

| Operação | Estado do código | Aceitação e limites |
|---|---|---|
|`search-comments/body-subject` — Pesquisar assunto/conteúdo de comentário|Código em subconjunto ([fonte](../app/search_engine.py#L117))|Nota sintética e consulta => assunto e conteúdo pesquisáveis; fontes/ordem explícitas.|
|`search-comments/author` — Pesquisar autor de comentário|Código em subconjunto ([fonte](../app/search_engine.py#L117))|Autor1 na nota preservada => um hit página1; correção na fonte posterior ao Flatpak.|
|`search-comments/replies` — Pesquisar respostas e demais tipos/campos|Pendente/caracterizar Reader|Comentários vinculados/respostas => extração, duplicação e destinos a caracterizar antes de equivalência.|

## Busca em anexos

No dynamic observation of this family found in the examined preserved reports.

**Lacunas:** Travessia/extratores/formatos/limites e associação de resultados comparados com o original.

| Operação | Estado do código | Aceitação e limites |
|---|---|---|
|`search-attachments/utf8` — Pesquisar anexo UTF-8|Código em subconjunto ([fonte](../app/attachment_search.py#L23))|Anexo UTF8/BOM => hits ligados à identidade do anexo; nenhuma execução de anexo.|
|`search-attachments/pdf` — Pesquisar texto de PDF anexado|Código em subconjunto ([fonte](../app/attachment_search.py#L23))|PDF anexado => página interna separada da página do hospedeiro e omissões explícitas.|
|`search-attachments/formats` — Cobrir demais extratores e travessia completa|Pendente/caracterizar Reader|Formato/catálogo ainda não suportado => caracterizar extração/limites/ordem; não converter omissão em busca completa.|

## Índice persistente/pesquisa de coleção

No dynamic observation of this family found in the examined preserved reports.

**Lacunas:** Disponibilidade Reader, manutenção/exclusões/locking/recuperação e formatos do índice; caracterizar suporte antes de ampliar.

| Operação | Estado do código | Aceitação e limites |
|---|---|---|
|`search-index/build` — Construir snapshot de coleção|Código em subconjunto ([fonte](../app/collection_index.py#L73))|PDFs escolhidos e índice local => snapshot versionado com identidade de fontes.|
|`search-index/query` — Consultar índice e excluir fonte alterada|Código em subconjunto ([fonte](../app/collection_index.py#L132))|Índice e consulta => hits de fontes válidas; fonte ausente/alterada excluída até rebuild explícito.|
|`search-index/maintenance` — Manter índice completo e recuperação|Pendente/caracterizar Reader|Índice Reader, exclusões e falha concorrente => formato/manutenção/locking a caracterizar; snapshot próprio não prova equivalência.|

## Stemming/proximidade/coringas

No dynamic observation of this family found in the examined preserved reports.

**Lacunas:** Stemming por idioma, distância/proximidade, escaping/expansão e combinação com índice.

| Operação | Estado do código | Aceitação e limites |
|---|---|---|
|`search-language/wildcard` — Pesquisar coringas por palavra|Código em subconjunto ([fonte](../app/search_matching.py#L91))|Token com coringa => casar palavras Unicode completas segundo contrato próprio.|
|`search-language/proximity` — Pesquisar proximidade ordenada|Código em subconjunto ([fonte](../app/search_matching.py#L91))|Termos e distância => respeitar ordem e palavras intermediárias no contrato próprio; algoritmo Foxit não confirmado.|
|`search-language/stemming` — Aplicar stemming por idioma|Pendente/caracterizar Reader|Idioma e consulta => regras de derivação/expansão a caracterizar; não implementado como algoritmo Foxit.|

## Seleção/cópia/snapshot

No dynamic observation of this family found in the examined preserved reports.

**Lacunas:** Ordem lógica/bidirecional, permissões, snapping e coordenadas em todos os modos previstos.

| Operação | Estado do código | Aceitação e limites |
|---|---|---|
|`selection/text` — Selecionar e copiar palavras por área|Código em subconjunto ([fonte](../app/main.py#L1491))|Região da visualização => palavras/cópia com transformação coerente no recorte próprio.|
|`selection/snapshot` — Copiar snapshot de região|Código em subconjunto ([fonte](../app/main.py#L1453))|Região da página => imagem do recorte, sem declarar ordem semântica de texto; teste dedicado não mapeado nesta revisão.|
|`selection/bidi` — Garantir ordem lógica e texto bidirecional|Pendente/caracterizar Reader|PDF com colunas/texto bidirecional => ordenação, snapping e permissões ainda por especificar/comparar.|

## Prévia/plano de impressão

Prévia/cancelarD17; UI05extra com confirmação de lote/No. Não houve impressão física nem prova de saída completa.

**Lacunas:** Predefinições/margens/fontes/flags e fluxo completo da fila; impressão física e encerramento após impressão.

| Operação | Estado do código | Aceitação e limites |
|---|---|---|
|`printing/preview` — Preparar prévia e opções de impressão|Código em subconjunto ([fonte](../app/print_window.py#L1261))|Documento e opções => prévia correspondente ao plano próprio; envio/saída final são controles separados.|
|`printing/submit` — Enviar arquivo ao backend Linux|Código em subconjunto ([fonte](../app/cups_backend.py#L397))|PDF preparado e destino => chamada ao backend e resultado de submissão; não prova papel impresso.|
|`printing/physical` — Imprimir e cancelar em dispositivo físico|Pendente/caracterizar Reader|Impressora/papel reais => escala/margens/duplex/fila/cancelamento conferidos; ambiente ainda pendente.|
|`printing/shutdown` — Encerrar após impressão sem processo preso|Pendente/caracterizar Reader|Trabalho/fechamento => inspecionar processos/esperas; splwow64 anterior continua sem causa definitiva.|

## Livreto/N-up/mosaico

Prévia de ordem em livreto/N-up observada; saída e parâmetros correspondentes ainda inconclusivos.

**Lacunas:** Saída PDF com margens/medidas/ordem correspondentes, rotações e combinações de livreto/N-up/mosaico.

| Operação | Estado do código | Aceitação e limites |
|---|---|---|
|`imposition/booklet` — Compor livreto|Código em subconjunto ([fonte](../app/imposition.py#L267))|Páginas, papel, lado e encadernação => sequência/posições próprias; parâmetros/saída Foxit ainda inconclusivos.|
|`imposition/nup` — Compor N-up|Código em subconjunto ([fonte](../app/imposition.py#L205))|Páginas e grade/ordem => células e CropBox corretos no contrato próprio.|
|`imposition/poster` — Compor mosaico|Código em subconjunto ([fonte](../app/imposition.py#L515))|Página/escala/papel/sobreposição => tiles próprios; marcas dependem de Cairo e têm validação separada.|

## Criar/mover/gravar marcadores

No dynamic observation of this family found in the examined preserved reports.

**Lacunas:** Diálogos e persistência completa, disponibilidade Reader, hierarquia/destinos/histórico em comparação.

| Operação | Estado do código | Aceitação e limites |
|---|---|---|
|`bookmarks-edit/create` — Criar marcador em cópia|Código em subconjunto ([fonte](../app/pdf_changes.py#L264))|Título/página => novo marcador na cópia, arquivo original preservado.|
|`bookmarks-edit/rename` — Renomear marcador|Código em subconjunto ([fonte](../app/pdf_changes.py#L264))|Caminho/título => renomear o nó escolhido preservando destinos e estrutura.|
|`bookmarks-edit/move` — Mover subárvore de marcadores|Código em subconjunto ([fonte](../app/pdf_changes.py#L190))|Caminho, pai e posição => mover sem ciclos, preservando filhos/destinos/contagens.|
|`bookmarks-edit/delete` — Excluir subárvore em cópia|Código em subconjunto ([fonte](../app/pdf_changes.py#L190))|Caminho => excluir subárvore e manter árvore restante consistente.|

## Anotações/undo/gravação

No dynamic observation of this family found in the examined preserved reports.

**Lacunas:** Respostas/popup/vínculos, aparências e operações restantes; tipos simples atuais não aprovam edição universal.

| Operação | Estado do código | Aceitação e limites |
|---|---|---|
|`annotations/note` — Criar nota Text|Código em subconjunto ([fonte](../app/pdf_changes.py#L264))|Página, texto e retângulo => nota Text imprimível dentro do CropBox, em cópia.|
|`annotations/highlight` — Criar destaque de área|Código em subconjunto ([fonte](../app/pdf_changes.py#L264))|Página e retângulo => Highlight com QuadPoints e texto no recorte suportado.|
|`annotations/rectangle` — Criar retângulo|Código em subconjunto ([fonte](../app/pdf_changes.py#L264))|Retângulo dentro da página => Square imprimível com geometria persistida.|
|`annotations/underline` — Criar sublinhado|Código em subconjunto ([fonte](../app/pdf_annotations.py#L40))|Página e geometria válida => sublinhado com aparência vetorial própria embutida; fonte preservada.|
|`annotations/strikeout` — Criar tachado|Código em subconjunto ([fonte](../app/pdf_annotations.py#L40))|Página e geometria válida => tachado com aparência vetorial própria embutida; fonte preservada.|
|`annotations/squiggly` — Criar ondulado|Código em subconjunto ([fonte](../app/pdf_annotations.py#L40))|Página e geometria válida => ondulado com aparência vetorial própria embutida; fonte preservada.|
|`annotations/ellipse` — Criar elipse|Código em subconjunto ([fonte](../app/pdf_annotations.py#L40))|Página e geometria válida => elipse com aparência vetorial própria embutida; fonte preservada.|
|`annotations/line` — Criar linha|Código em subconjunto ([fonte](../app/pdf_annotations.py#L40))|Página e geometria válida => linha com aparência vetorial própria embutida; fonte preservada.|
|`annotations/comment-author` — Editar comentário e autor|Código em subconjunto ([fonte](../app/pdf_changes.py#L264))|Anotação simples desbloqueada e texto/autor => alterar/limpar metadados sem mudar geometria/aparência.|
|`annotations/delete` — Excluir anotação simples|Código em subconjunto ([fonte](../app/pdf_changes.py#L264))|Índice atual => excluir somente tipo simples sem bloqueios/vínculos/dependentes, preservando widgets.|
|`annotations/history` — Desfazer/refazer rascunho|Código em subconjunto ([fonte](../app/edit_history.py#L71))|Histórico do rascunho => reconstruir cursor correto sem alterar fonte/cópias já salvas.|
|`annotations/replies` — Editar respostas/popup e vínculos|Pendente/caracterizar Reader|Threads/popup/dependentes => caracterizar autoria, vínculos, persistência e disponibilidade Reader.|
|`annotations/freehand` — Desenho livre e demais tipos|Pendente/caracterizar Reader|Geometria de desenho/tipo ainda ausente => especificar, implementar e comparar antes de declarar suporte.|

## AcroForm/XFA/eventos

No dynamic observation of this family found in the examined preserved reports.

**Lacunas:** Combo editável/texto livre/aparência primeiro; depois eventos, cálculo/validação, XFA e formas restantes de acordo com disponibilidade e contrato.

| Operação | Estado do código | Aceitação e limites |
|---|---|---|
|`forms/text` — Preencher campo Tx|Código em subconjunto ([fonte](../app/pdf_changes.py#L264))|Campo terminal e texto => respeitar ReadOnly/MaxLen herdados e persistir valor/aparência em cópia.|
|`forms/checkbox` — Marcar/desmarcar checkbox|Código em subconjunto ([fonte](../app/pdf_form_controls.py#L123))|Checkbox com aparências existentes e booleano => /V e /AS coerentes; ReadOnly recusado.|
|`forms/radio` — Selecionar radio simples|Código em subconjunto ([fonte](../app/pdf_form_controls.py#L123))|Grupo e estado válido => ativar somente widget selecionado; respeitar NoToggleToOff.|
|`forms/combo-fixed` — Selecionar combo sem texto livre|Código em subconjunto ([fonte](../app/pdf_form_controls.py#L123))|Opção existente => valor/índice/aparência coerentes; export/label preservados no subconjunto.|
|`forms/list-single` — Selecionar lista simples|Código em subconjunto ([fonte](../app/pdf_form_controls.py#L123))|Lista simples e opção ou vazio => seleção única ou limpeza consistente.|
|`forms/list-multiple` — Selecionar lista múltipla|Código em subconjunto ([fonte](../app/pdf_form_controls.py#L123))|Conjunto de exports => valores e índices canônicos persistidos sem duplicação.|
|`forms/combo-editable` — Preencher combo com texto livre|Pendente/caracterizar Reader|Texto fora de Opt em combo editável => gerar valor/aparência, preservar opções e ReadOnly; ainda recusado atualmente.|
|`forms/events` — Calcular e validar eventos de formulário|Pendente/caracterizar Reader|Campo com cálculo/validação/evento => delimitar motor, regras e efeitos antes de implementação.|
|`forms/xfa` — Processar XFA|Pendente/caracterizar Reader|Formulário XFA => disponibilidade e contrato do alvo ainda a caracterizar; edição atual recusa.|

## Anexos/portfólios

Anexo sintético listado/extraído,22bytes/hash iguais; políticas/portfólios completos abertos.

**Lacunas:** Portfólios e senha não vazia, políticas de extração; completar comparação e desktop/acessibilidade.

| Operação | Estado do código | Aceitação e limites |
|---|---|---|
|`attachments/list` — Listar catálogo/árvores/anotações|Código em subconjunto ([fonte](../app/pdf_attachments.py#L145))|PDF suportado => índices/nomes/origens de anexos sem decodificar payload na listagem.|
|`attachments/extract` — Extrair anexo sem sobrescrever|Código em subconjunto ([fonte](../app/pdf_attachments.py#L163))|Índice/hash e destino novo => bytes conferidos; nomes perigosos/mudança de fonte recusados.|
|`attachments/portfolio` — Abrir portfólio completo|Pendente/caracterizar Reader|Portfólio => inventário e navegação/extração a caracterizar; subset atual recusa explicitamente.|
|`attachments/encrypted` — Extrair anexo com senha não vazia|Pendente/caracterizar Reader|PDF cifrado com credencial conhecida => integração de senha/limites pendente; não contornar permissões.|

## Assinaturas/certificados

No dynamic observation of this family found in the examined preserved reports.

**Lacunas:** Assinatura de documentos, confiança/cadeia/revogação/tempo e PAdES/LTV; CMS atual só verifica integridade no recorte documentado.

| Operação | Estado do código | Aceitação e limites |
|---|---|---|
|`signatures/inspect` — Inspecionar campos e cobertura assinada|Código em subconjunto ([fonte](../app/pdf_signatures.py#L70))|Campos/ByteRange/Contents => cobertura da revisão e limites explícitos; não afirmar arquivo atual integralmente assinado indevidamente.|
|`signatures/cms-integrity` — Verificar integridade CMS offline|Código em subconjunto ([fonte](../app/pdf_signatures.py#L45))|CMS destacado e bytes => resultado de integridade separado de confiança de certificado.|
|`signatures/sign` — Assinar documento|Pendente/caracterizar Reader|Documento e certificado sintético autorizado => assinatura/persistência a especificar e implementar; inspeção atual não assina.|
|`signatures/trust` — Validar cadeia/confiança/revogação|Pendente/caracterizar Reader|Certificado e política => confiança/cadeia/revogação ainda sem fluxo completo; não inferir de CMS íntegro.|
|`signatures/timestamp-ltv` — Processar carimbo de tempo/PAdES/LTV|Pendente/caracterizar Reader|Assinatura e materiais de validação => contrato, tempo e cobertura ainda pendentes.|

## Senhas/permissões/RMS

Cancelar/senha errada anteriores e correta na abertura independente D15. Permissões/RMS/fluxo universal não observados.

**Lacunas:** Fluxo cifrado integrado, aplicação de permissões e mensagens; RMS segue sem contrato completo e exige ambiente autorizado.

| Operação | Estado do código | Aceitação e limites |
|---|---|---|
|`security/inspect` — Autenticar senha conhecida e inspecionar permissões|Código em subconjunto ([fonte](../app/pdf_security.py#L66))|PDF e senha opcional => papel/autenticação/permissões ou erro sem expor segredo.|
|`security/protect` — Criar cópia AES-256|Código em subconjunto ([fonte](../app/pdf_security.py#L91))|PDF suportado e senhas/permissões => cópia AES256 nova; fonte/metadados/anexos preservados no recorte.|
|`security/owner-copy` — Criar cópia sem cifra com senha de proprietário|Código em subconjunto ([fonte](../app/pdf_security.py#L157))|Autenticação de proprietário => cópia legível nova; senha só de abertura insuficiente.|
|`security/enforcement` — Aplicar permissões em todos os fluxos|Pendente/caracterizar Reader|Permissões PDF e leitura/cópia/impressão/edição => política consistente entre interfaces, workers e erro; fluxo global pendente.|
|`security/rms` — Processar proteção RMS autorizada|Pendente/caracterizar Reader|Documento RMS e ambiente autorizado => caracterizar serviço/contrato sem contornar proteção; dependência externa não resolvida.|

## Acessibilidade/voz

No dynamic observation of this family found in the examined preserved reports.

**Lacunas:** AT-SPI/leitor de tela real, ordem semântica, voz, foco/atalhos e cobertura efetiva.

| Operação | Estado do código | Aceitação e limites |
|---|---|---|
|`accessibility/text` — Expor texto da página por ATK.Text|Código em subconjunto ([fonte](../app/accessible_reader.py#L11))|Página suportada => texto Poppler em Gtk.TextView/ATK.Text com limites; não é garantia de ordem semântica.|
|`accessibility/keyboard` — Navegar por regiões pelo teclado|Código em subconjunto ([fonte](../app/main.py#L2016))|F6/ShiftF6 e foco atual => regiões/nomes acessíveis e delegação de setas no recorte testado.|
|`accessibility/screen-reader` — Validar leitor de tela e ordem real|Pendente/caracterizar Reader|Desktop AT-SPI e leitor de tela real => foco, ordem e feedback conferidos; CI sem barramento não aprova.|
|`accessibility/voice` — Ler em voz alta|Pendente/caracterizar Reader|Texto e controles de voz => disponibilidade Reader, síntese e interrupção ainda a delimitar; OCR não implementa voz.|

## Medição/calibração

No dynamic observation of this family found in the examined preserved reports.

**Lacunas:** Calibração/unidades, snapping/precisão, áreas e perímetros.

| Operação | Estado do código | Aceitação e limites |
|---|---|---|
|`measurement/distance` — Medir distância entre pontos|Código em subconjunto ([fonte](../app/main.py#L1515))|Dois pontos da visualização => distância convertida a centímetros no contrato atual; teste dedicado não mapeado.|
|`measurement/calibrate` — Calibrar escala e unidades|Pendente/caracterizar Reader|Distância conhecida/unidade => calibração e snapping/precisão persistidos conforme contrato futuro.|
|`measurement/area` — Medir área|Pendente/caracterizar Reader|Polígono/região => área em unidade calibrada; operação ainda pendente.|
|`measurement/perimeter` — Medir perímetro|Pendente/caracterizar Reader|Traçado/polígono => perímetro em unidade calibrada; operação ainda pendente.|

## Camadas/mídia/3D

No dynamic observation of this family found in the examined preserved reports.

**Lacunas:** Alternar/persistir OCG, combinações, mídia/codecs/eventos e 3D conforme disponibilidade real do Reader.

| Operação | Estado do código | Aceitação e limites |
|---|---|---|
|`layers-media/list` — Listar nomes de camadas OCG|Código em subconjunto ([fonte](../app/pdf_panels.py#L32))|PDF com OCG => nomes listados; isso não altera visibilidade nem comprova suporte a mídia.|
|`layers-media/toggle` — Alternar e persistir visibilidade OCG|Pendente/caracterizar Reader|Combinação de camadas => render e estado de visibilidade coerentes; implementação/persistência pendentes.|
|`layers-media/media` — Reproduzir mídia embutida|Pendente/caracterizar Reader|Mídia/codecs/eventos => caracterizar disponibilidade Reader e controles antes de implementar.|
|`layers-media/3d` — Interagir com conteúdo 3D|Pendente/caracterizar Reader|U3D/conteúdo3D => caracterizar disponibilidade Reader/render/estado; presença de plugin não comprova suporte.|

## Preferências/tema/persistência

No dynamic observation of this family found in the examined preserved reports.

**Lacunas:** Defaults, persistência e interdependência dos ajustes restantes; tema/pastas atuais já preservados.

| Operação | Estado do código | Aceitação e limites |
|---|---|---|
|`preferences/theme` — Persistir e aplicar tema|Código em subconjunto ([fonte](../app/appearance.py#L39))|system/light/dark => persistência/migração e contraste no recorte próprio.|
|`preferences/folders` — Persistir pasta preferida e últimas pastas|Código em subconjunto ([fonte](../app/local_files.py#L27))|Pasta explícita local => preferência por operação, fallback e esquecimento sem apagar arquivos/contas.|
|`preferences/remaining` — Cobrir demais ajustes e defaults|Pendente/caracterizar Reader|Preferências do Reader => inventariar defaults/interdependência/esquema e implementar ajustes restantes.|

## Nuvem/colaboração

No dynamic observation of this family found in the examined preserved reports.

**Lacunas:** APIs/login/upload/colaboração remota adiados. Manter visíveis sem executá-los ou somar conclusão.

| Operação | Estado do código | Aceitação e limites |
|---|---|---|
|`cloud/login` — Autenticar provedor remoto|Adiada pelo usuário|Conta/provedor => integração adiada pelo usuário; não iniciar credenciais/APIs.|
|`cloud/transfer` — Transferir arquivos por API de nuvem|Adiada pelo usuário|Arquivos/provedor => upload/download direto adiados; cópia local não é transferência remota.|
|`cloud/collaboration` — Colaborar remotamente e resolver conflitos|Adiada pelo usuário|Participantes/versões => contratos remotos adiados; cliente sincronizador externo é fluxo separado.|

## Criação/conversão

No dynamic observation of this family found in the examined preserved reports.

**Lacunas:** Inventário Reader/Editor, formatos/conversões restantes, fidelidade/OCR e variantes recusadas; preservar TIFF multipágina 100/OCR 20 atuais.

| Operação | Estado do código | Aceitação e limites |
|---|---|---|
|`conversion/images` — Criar PDF de imagens simples|Código em subconjunto ([fonte](../app/pdf_creation.py#L103))|PNG/JPEG/BMP/WebP suportados e ordem/DPI => PDF RGB com geometria/proveniência e publicação exclusiva.|
|`conversion/tiff` — Expandir TIFF multipágina|Código em subconjunto ([fonte](../app/pdf_creation.py#L51))|TIFF válido => páginas em ordem e orientação, até100 totais; variantes inválidas recusadas sem saída parcial.|
|`conversion/ocr` — Gerar cópia PDF pesquisável local|Código em subconjunto ([fonte](../app/pdf_ocr.py#L96))|PDF/imagens e idioma por/eng => camada pesquisável local até20 páginas, limites/cancelamento; sem avaliação universal de acurácia.|
|`conversion/animation` — Converter animações/variantes ainda recusadas|Pendente/caracterizar Reader|Imagem animada/variante não suportada => definir frames, ordem e limites antes de suporte; recusa atual não é implementação.|
|`conversion/other-formats` — Cobrir demais conversões disponíveis no Reader|Pendente/caracterizar Reader|Formato de entrada/saída => inventário Reader versus Editor e fidelidade ainda abertos.|

## Integrações de sistema/atualização

No dynamic observation of this family found in the examined preserved reports.

**Lacunas:** Portais/concessão persistente reais, associação de arquivos, atualização/rollback e adaptador Windows posterior.

| Operação | Estado do código | Aceitação e limites |
|---|---|---|
|`platform/worker-runtime` — Selecionar runtime de worker|Código em subconjunto ([fonte](../app/platform_runtime.py#L7))|Ambiente/plataforma => Python/runtime pareado para subprocesso; não valida toda integração de sistema.|
|`platform/portal` — Validar portal real e concessão persistente|Pendente/caracterizar Reader|Desktop/Flatpak e pasta foraHOME => selecionar, conceder/negar e reabrir após reinício; simulação de resposta do diálogo não aprova interação real.|
|`platform/association` — Associar e abrir PDF pelo desktop|Pendente/caracterizar Reader|Arquivo e shell Linux => launcher/associação e parâmetros reais conferidos no desktop; cobertura completa pendente.|
|`platform/update` — Atualizar e reverter entrega|Pendente/caracterizar Reader|Pacote/versão anterior => atualização/rollback e persistência a definir/validar; distribuição de bundle não fecha todo fluxo.|
|`platform/windows` — Validar Linuxit nativo no Windows|Pendente/caracterizar Reader|Executável/adaptador Windows => UI, subprocessos, associação e impressão próprios; prioridade posterior ao Linux.|

## O que foi reconciliado

- D11-missing exato, D15 independente, D16 e préviasD17/D18 agora aparecem como observações limitadas; não são famílias completas.
- Busca por autor é correção posterior na fonte; o Flatpak0.1.13 continua anterior. Consolidado preservado12 métricas iguais/cinco inconclusivas.
- Coletor e paradas da VM não são comportamento funcional Foxit; P02/P03 exigem ambiente responsivo e novos controles.
- Runtime observado em uma família não preenche automaticamente foxit_expected/foxit_observed dos50 planos de aceitação.
- Nuvem direta permanece adiada; IA/generativos e UPDF fora do escopo; inventário Reader/Editor ainda aberto.

P01 concluída para o inventário provisório v1. A faseA, os critérios amplos das21 etapas e a conclusão da recodificação continuam abertos. Próximo uso: selecionar uma operação, examinar suas evidências e fechar contratos/implementação/comparação separadamente.

Verificações reproduzíveis: `python scripts/check_operation_catalog.py` e
`python scripts/validate_functional_spec.py --check-render docs/contratos-funcionais.md`.
Resultado deste marco em [review.json](../testes/resultados/p01-2026-10-18/review.json).
