# Plano de continuidade do Linuxit PDF

Checkpoint 2026-10-19T01:08:44-03:00: [P03 suspensa pelo relógio](P03-PARADA-2026-10-19-0105.md). Busca ativa no corpus5000 observada; Stop enviado uma vez, efeito desconhecido. Relógio01:02:45 sem avanço e capturas iguais após10s externos. Nenhuma nova entrada, rede, reboot/pause/kill após constatação; hostrunning/cabooff, original/observador0048 sem estado final confirmado. P02 concluída, P03 parcial/bloqueada; não superar a parada automaticamente. Gerador próprio preservado em scripts/prepare_search_cancel_variant.py. Histórico abaixo.

Execução em 2026-10-19T00:36:40-03:00: P01 provisória preservada, P02 concluída e [P03 parcial](P03-BUSCA-IMPRESSAO-2026-10-19.md). Novo lote examinou busca/destinos, UI02/UI05 e saídas reais de N-up/livreto. Estado atual em execucao-plano.json; sem encerrar critérios amplos.

Organizado em 2026-10-18T21:54:16-03:00. Base examinada: `c62ae3c4aece24f902c26f66aeeb81a4995f9b3c`.

Este plano organiza **todos os 19 critérios ainda abertos e as 25 famílias identificadas**. P01–P10 são pacotes de execução; as 21 etapas antigas, seus pesos e evidências continuam preservados. O inventário global de operações ainda está aberto: novas descobertas entram no catálogo e no plano.

[Fonte estruturada](../progresso/plano-continuidade.json) · [retomada do ambiente](RETOMADA.md) · [última parada da VM](VM-SENHA-E-PARADA-2026-10-18.md).

[Conferência da criação do plano em 0d0de4c](../testes/resultados/plano-continuidade-2026-10-18.json): cobertura dos 19 critérios, 25 famílias e 50 planos, referências e dependências verificadas. Esse relatório histórico corresponde à criação em 0d0de4c; hashes referem-se àquela versão, não às atualizações de execução.

## Execução atual de P01–P03

P01 concluída para o catálogo provisório v1 de 111 recortes/25 famílias; inventário global aberto. P02 concluída no ambiente/observador offline; P03 pronta com novo observador e controle antes do original. [Validação P02](P02-COLETOR-VALIDADO-2026-10-18.md). [Relatório da execução](EXECUCAO-P01-P03-2026-10-18.md) e [estado estruturado](../progresso/execucao-plano.json). A situação inicial abaixo permanece histórica.

## Estado de partida

- Fonte: 403/403 testes Linux registrados; pacote 0.1.13/devel:400/400 por ambiente no marco publicado. A correção de busca por autor ainda não está nesse pacote.
- Comparação: 12 medições iguais/cinco inconclusivas; não equivalem a 25 famílias aprovadas. Há 50 planos completos S12, com dois de cloud adiados.
- Checklist histórico: 45,13%, 39 critérios done/19 abertos; percentual global da reconstrução continua indeterminado.
- Último estado da VM registrado: relógio parado em 21:24:14, Foxit fechado/cabo desligado. Não reinspecionada nem acionada por este planejamento. Coletor 2020 terminou com erro; não esperar respostas dele; script corrigido não instalado/integrado, tarefa 2130 não criada.

## Ordem de execução e dependências

| Etapa | Entrega | Ambiente | Pode iniciar |
|---|---|---|---|
|P01|Inventário de operações e medição|Sem VM; código e evidências preservadas|Agora, nos recursos disponíveis|
|P02|Validar o coletor e o ambiente do original|VM Windows offline, após voltar a responder|Quando VM voltar a responder|
|P03|Completar as observações do Foxit|VM offline aprovada em P02|P02|
|P04|Concluir análise estática dirigida|REA/Ghidra, sem executar original|Agora, nos recursos disponíveis|
|P05|Consolidar contratos e casos de aceitação|Sem VM para preparar; P03/P04 para afirmar comportamento do original|P01|
|P06|Implementar funções PDF em lotes pequenos|Código próprio/Linux; VM para comprovar equivalência|P01|
|P07|Validar integração no desktop Linux real|Desktop Linux, Flatpak, cliente sincronizador e impressora; sem VM Foxit|Agora, nos recursos disponíveis|
|P08|Comparar, corrigir e executar aceitação|Resultados do original offline e reconstrução Linux; dispositivos conforme caso|P03|
|P09|Gerar e validar os marcos Flatpak|CI Linux e sandbox instalado; sem original Foxit|Agora, nos recursos disponíveis|
|P10|Auditar o fechamento e preparar a continuidade|Repositório, relatórios e ambientes das etapas anteriores|Agora, nos recursos disponíveis|

**Começar sem VM:** P01 (inventário/reconciliação), P06/B01 (combo editável com contrato já suficiente) e P04 (análise dirigida). P05 pode preparar fixtures/contratos; P07 exige desktop/cliente/impressora reais nas tarefas correspondentes. Não aguardar a VM para avançar essas frentes.

**Sequência do original:** P02 → P03 → P08. Evidências obtidas alimentam P04/P05 e correções de P06. P09 é repetida nos marcos de entrega; P10 acompanha o fechamento.

A ordem é por entregas pequenas: dependência de encerramento não impede iniciar uma tarefa independente com contrato já suficiente. P06/P08 retornam às etapas de análise quando falta evidência. Não é necessário terminar toda uma família para publicar um avanço utilizável.

## P01 — Inventário de operações e medição

**Ambiente:** Sem VM; código e evidências preservadas.

- Decompor cada uma das 25 famílias em operações pequenas, com entrada, saída e critério de aceitação.
- Conferir código, testes, especificação e matriz; corrigir registros atuais desatualizados sem reescrever evidência histórica. Exemplos: D11-missing já observado; D15 independente já observado; autor corrigido somente na fonte; impressão e anexos com observações limitadas.
- Separar implementado, testado no Linux, observado no original e comparado. Registrar desconhecido, indisponível no contexto, adiado e excluído sem convertê-los em concluído.
- Delimitar recursos do Reader 2025.2.0.33046; rótulos/templates do Editor ou plugins não demonstram disponibilidade.
- Versionar catálogo de operações. Definir eventual medição do escopo conhecido com critérios/pesos explícitos, mantendo a porcentagem global nula enquanto o denominador continuar aberto.

**Entregar:** Inventário operacional versionado, por família, com fonte e evidência por operação. Especificação/matriz reconciliadas e lista explícita de operações ainda desconhecidas.

**Concluir quando:** 25 famílias examinadas no nível de operações; toda afirmação de implementação/validação tem referência. Catálogo declarado provisório se restarem funções por descobrir. Não aprova paridade.

## P02 — Validar o coletor e o ambiente do original

**Ambiente:** VM Windows offline, após voltar a responder.

- Revalidar segundos e resposta de uma aplicação de controle; não assumir recuperação pelo estado running do VirtualBox.
- Confirmar ausência do Foxit antes de manutenção breve já autorizada. Instalar o script corrigido em tarefa interativa limitada com RunId novo, preservando o anterior.
- Manter rede desligada antes dos testes; conferir identidade, dez Inputs, negação de escrita, shares/USB/clipboard e demais controles documentados.
- Validar IDs curtos como pf/col/end, recibos completos e parada do coletor sem iniciar Foxit. Arquivar resultados antigos antes de liberar somente suas propriedades.
- Antes de executar o original, novo preflight e controle visual. Se relógio/ambiente parar, somente observar após 10 segundos externos, interromper entradas, salvar e avisar; sem pause/reboot automático.

**Entregar:** Manifesto do novo observador, hash/perfil, contenção e recibos preflight/coleta/stop examinados.

**Concluir quando:** Coletor corrigido realmente instalado e validado ponta a ponta, com recibos completos e token limitado. Controles do host já passados não substituem esta integração.

## P03 — Completar as observações do Foxit

**Ambiente:** VM offline aprovada em P02.

- D07/D10: ativação e destino de cada resultado, busca mista e alternativas de ordenação; não tratar seleção sem navegação como destino nulo.
- D12: tornar trabalho ativo observável e medir cancelar, trocar e fechar durante a busca. O corpus250 páginas já concluído não provou cancelamento.
- D18: gerar saída PDF com parâmetros realmente correspondentes aos protocolos de livreto/N-up/mosaico; conferir margens, giro, sequência e dimensões. Prévia visual não aprova o stream.
- D20: investigar a espera anterior em splwow64 e encerramento após impressão. O fechamento sem residual do lote2020 fica preservado como contexto distinto.
- Revisar UI01–UI10 por variante: impressão sem/com documento, navegação, limites de zoom, todas as abas no par planejado, fontes 7911/7913, proximidade/índice, destaques e diálogos de marcadores.
- Não repetir D11-missing ou D15 independente como pendência. D11-vazio mantém métrica inconclusiva enquanto Search não produzir resposta de backend.
- Estender observações para operações das demais famílias e os 50 planos; registrar disponibilidade Reader e requisitos de serviço sem ligar a VM offline a serviços remotos.

**Entregar:** Observações por variante com corpus/opções/identidades, evidência privada e metadados publicáveis. Fila de observações insuficientes ou indisponíveis no contexto, com causa explícita.

**Concluir quando:** Protocolos selecionados reproduzíveis e observáveis; cada lacuna aprovada para comparação ou declarada inconclusiva. Fechamento amplo exige também as operações descobertas em P01/P04.

**Para encerramento completo:** evidências de P01. Isso não bloqueia os preparos independentes.

## P04 — Concluir análise estática dirigida

**Ambiente:** REA/Ghidra, sem executar original.

- Retomar catálogo 323 e projetos preservados; conferir ferramentas/perfis realmente disponíveis e não contar as 48 entradas anteriores novamente.
- Busca/reflow: alocação/tamanhos e chamadores dos cinco arrays; transições0x15cd6e0/0x15cc9b0; atribuição de dialog+0x1e48, campos restantes e algoritmo0x1003f6b0.
- Impressão/geometria: contexto0x138, serviços de imagem, concorrência, estados, ownership, falhas e fluxos completos de consumidores.
- Resolver fronteiras do motor PDF, ciclo de vida dos componentes, assinaturas/tipos e fluxos das outras famílias conforme lacunas operacionais.
- Confrontar IDs7911/7913 com observação dinâmica; preservar ambiguidades onde a evidência não resolve.
- Checkpoint por lote: identidade, perfil, entradas novas versus reaproveitadas, resultados examinados, falhas, inferências e próximo alvo. Sem IA ou recursos proprietários na implementação.

**Entregar:** Contratos de tipos, diagramas e catálogo incrementais com evidência técnica examinada. Lista de ambiguidades e fronteiras ainda não resolvidas.

**Concluir quando:** Cada recorte tem tipos/estados/ownership rastreáveis. Os critérios universais antigos só fecham quando o universo definido estiver coberto, não ao terminar uma fila de sementes.

**Para encerramento completo:** evidências de P01, P03. Isso não bloqueia os preparos independentes.

## P05 — Consolidar contratos e casos de aceitação

**Ambiente:** Sem VM para preparar; P03/P04 para afirmar comportamento do original.

- Detalhar entradas, saídas, mensagens, efeitos, cancelamento e limites por operação, diferenciando contrato próprio e comportamento observado.
- Transformar os 50 planos S12 em procedimentos executáveis; adicionar casos por risco/descoberta. Dois planos da família cloud continuam adiados.
- Preparar fixtures sintéticas determinísticas, oráculos e medidas; conectar variantesD/UI e recortesC18 aos contratos sem contar um subconjunto como família completa.
- Definir tolerâncias/ordem/unidades antes de comparar. Indisponibilidade, dependência externa e caso não executado não recebem passed.
- Atualizar contratos-funcionais.md pelo validador/render oficial, preservando proveniência e versões.

**Entregar:** Especificação funcional e planos executáveis por operação; matriz de evidência e dependência.

**Concluir quando:** Contrato de cada operação implementada verificável; faseA só consolidada com lacunas explicitadas e obrigações ainda abertas visíveis.

**Para encerramento completo:** evidências de P03, P04. Isso não bloqueia os preparos independentes.

## P06 — Implementar funções PDF em lotes pequenos

**Ambiente:** Código próprio/Linux; VM para comprovar equivalência.

- Executar B01–B09 abaixo por operação já suficientemente especificada; não esperar encerrar todas as famílias para iniciar o primeiro lote.
- Primeira entrega candidata: combo AcroForm editável, texto livre e aparência; preservar Opt, valores/índices, ReadOnly/flags, original, histórico e cópias já salvas.
- Para cada operação: backend, worker e interface, erros/cancelamento e persistência; testes necessários de resultado e regressão no Linux.
- Preservar base MIT/BSD e independência do código. Recusas atuais de formatos/recurso não suportado permanecem explícitas até implementação verificada.
- Não implementar como fato comportamentos Foxit ainda inferidos. Lacunas de contrato voltam a P03/P04/P05; APIs cloud permanecem adiadas.

**Entregar:** Incrementos de código/testes/GUI e nota de operação concluída com limites. Atualização do inventário operacional sem promover família inteira por um recurso.

**Concluir quando:** Lote passa nos testes pertinentes da fonte Linux e tem comportamento/persistência examinados. Equivalência aguarda P08.

**Para encerramento completo:** evidências de P05. Isso não bloqueia os preparos independentes.

## P07 — Validar integração no desktop Linux real

**Ambiente:** Desktop Linux, Flatpak, cliente sincronizador e impressora; sem VM Foxit.

- Portais reais de abrir/salvar e concessão persistente fora HOME: permitido/negado, reabrir após reiniciar e restrições do sandbox.
- Pastas sincronizadas com cliente real: salvar cópia local, envio externo, rede indisponível, conflito/mudança concorrente, sem anunciar upload a partir de simples gravação local.
- AT-SPI/leitor de tela real, foco, teclado e ordem de leitura; manter distinção entre texto acessível exposto e conformidade integral.
- Impressão física via backend Linux: papel/escala/margens, frente-verso suportado, cancelamento, fila e erros de dispositivo.
- Associação de PDF, launcher, persistência/tema, múltiplos monitores e testes de interação não representados pelo CI headless.

**Entregar:** Relatórios de desktop/dispositivo, versão/distro/portal/cliente e evidências examinadas.

**Concluir quando:** Cada integração tem resultado real e limitações registradas. CI e impressão virtual não substituem os cenários de equipamento.

**Para encerramento completo:** evidências de P06. Isso não bloqueia os preparos independentes.

## P08 — Comparar, corrigir e executar aceitação

**Ambiente:** Resultados do original offline e reconstrução Linux; dispositivos conforme caso.

- Preservar consolidado12 medições iguais/cinco inconclusivas; resolver inconclusivos sem transformar ausência de observação em igualdade.
- Executar cada plano S12 nominal/exceção no escopo autorizado, ligando fixture/protocolo/evidências/oráculos. Cloud adiada mantém seus casos sem execução.
- Comparar por operação: contagens/destinos, estado persistido, geometria/pixels e arquivos quando pertinente; não depender só de igualdade de textos digitados manualmente.
- Para cada divergência: reproduzir, corrigir em P06, testar regressão e repetir só os cenários afetados. Registrar diferenças intencionais como lacuna/decisão, nunca equivalência automática.
- Validar cargas grandes, entradas inválidas, concorrência e cancelamento; separar falhas do ambiente, do observador e do aplicativo.

**Entregar:** Matriz diferencial por operação/família, regressões e relatório de aceitação com proveniência.

**Concluir quando:** Cada caso aceito tem execução e evidência examinada nas duas aplicações. Os50 planos iniciais não são catálogo completo; família só verificada após todas as suas obrigações delimitadas.

**Para encerramento completo:** evidências de P05, P06, P07. Isso não bloqueia os preparos independentes.

## P09 — Gerar e validar os marcos Flatpak

**Ambiente:** CI Linux e sandbox instalado; sem original Foxit.

- Empacotar por marco útil, sem aguardar toda a reconstrução. Incluir a correção de busca por autor que ainda está só na fonte.
- Versionar manifesto, manter runtime/loader pareados e proveniência/licenças; gerar bundle novo após mudanças do app.
- Executar suíte apropriada completa em fonte/payload/sandbox, smoke e launcher; examinar capturas e diferenças reais, sem skips usados como aprovação de GUI.
- Reinstalar e auditar o mesmo bundle publicado sem rebuild; conferir download, tamanho, SHA256 e instruções de instalação.
- Publicar código/pacote/relatórios e confirmar remoto. Documentação ou plano não exigem gerar pacote novo.

**Entregar:** Flatpak de desenvolvimento e manifesto, relatórios selados de builder/auditor e recibos de publicação.

**Concluir quando:** Bytes testados iguais aos publicados; versão e limites claros. Aceitar entrega parcial não declara aplicação inteira concluída.

**Para encerramento completo:** evidências de P06. Isso não bloqueia os preparos independentes.

## P10 — Auditar o fechamento e preparar a continuidade

**Ambiente:** Repositório, relatórios e ambientes das etapas anteriores.

- Conferir um a um os 19 critérios antigos mapeados abaixo, com evidência técnica examinada e pesos intactos.
- Auditar implementação, comparação, licenças/proveniência, pacote, testes e bloqueios; manter conclusão global nula se inventário ainda aberto.
- Conferir nuvem adiada e Windows posterior. Não declarar conclusão global enquanto obrigações desses itens permanecerem no escopo; eventual mudança exige decisão/histórico explícito.
- A cada lote, mesmo antes do encerramento: atualizar RETOMADA, pendências, notas com horário real de São Paulo; commit/push e recibo externo de sincronização.

**Entregar:** Auditoria final do escopo efetivamente entregue, lista de obrigações restantes e passagem reproduzível para outra IA.

**Concluir quando:** Cada done tem evidência suficiente; bloqueios/adiamentos continuam abertos. Release utilizável e conclusão de toda a reconstrução são avaliações separadas.

**Para encerramento completo:** evidências de P01, P02, P03, P04, P05, P06, P07, P08, P09. Isso não bloqueia os preparos independentes.

## Lotes de implementação de P06

A descrição indica o trabalho restante; não promete que todas as funções existam no Reader. Caracterizar disponibilidade e contrato antes de implementá-las como equivalência. B01 é a próxima entrega própria já identificada.

| Lote | Famílias | Trabalho restante |
|---|---|---|
|B01 — Formulários|forms|Combo editável primeiro; depois cálculo/validação/eventos, XFA e formatos restantes conforme disponibilidade Reader e contratos próprios examinados.|
|B02 — Marcadores e anotações|bookmarks-edit, annotations|Diálogos e persistência completos de marcadores; respostas/popup, aparências, autoria, desenho livre e demais anotações suportadas pelo alvo; histórico e vínculos.|
|B03 — Abertura, senhas e permissões|open-render, security|Entrada de senha integrada à abertura/renderização/busca; cancelar/erro, propagação controlada ao worker, permissões e recuperação. RMS exige caracterização/ambiente próprio, sem contornar proteção.|
|B04 — Busca|search-text, search-bookmarks, search-comments, search-attachments, search-index, search-language|Destinos/ordem/destaques e respostas; anexos e índices completos, normalização, idiomas/stemming/proximidade/coringas. Contratos atuais independentes não provam algoritmo Foxit.|
|B05 — Leitura e navegação|navigation, presentation, selection|Limites de zoom/ajuste, navegação em estados extremos, múltiplos monitores, seleção/ordem lógica, texto bidirecional e geometria em rotação.|
|B06 — Impressão e imposição|printing, imposition|Predefinições/flags, parâmetros e fluxo de fila; geometria, margens/rotações/ordem de livreto,N-up,mosaico; saída equivalente antes de aprovar.|
|B07 — Anexos e conversões|attachments, conversion|Portfólios, senha não vazia e políticas de extração; formatos/conversões adicionais confirmados no Reader, OCR/fidelidade e variantes de imagem ainda recusadas. TIFF 100/OCR 20 já entregues não são refeitos como novidade.|
|B08 — Assinaturas, medição e conteúdo especial|signatures, measurement, layers-media|Assinar versus validar, cadeia/revogação/tempo/PAdES conforme contrato; unidades/calibração/snapping/área/perímetro; visibilidade OCG/persistência, mídia e 3D conforme suporte real do alvo.|
|B09 — Preferências, acessibilidade e sistema|preferences, accessibility, platform|Preferências ainda ausentes, foco/voz/ordem acessível, portais/associação/atualização/rollback e adaptadores. Validação real em P07; Windows posteriormente.|
|B10 — Nuvem direta — adiada|cloud|Preservar cadastro/contratos pendentes; não iniciar login/APIs/upload/colaboração remota. Pastas sincronizadas locais já autorizadas seguem em P07.|

## Inventário por família: preservar e completar

Cada linha tem dois planos S12 iniciais ligados na fonte estruturada. Eles são o ponto de partida da aceitação, não uma lista exaustiva da família.

| Família | Base preservada | Falta |
|---|---|---|
|Abrir PDF e renderizar páginas (B03)|Leitura/render e cópias locais implementados em subconjunto; D02/D13/D14 limitados e D15 independente observados.|Abertura cifrada integrada, recuperação e demais falhas/cancelamento/renderização; testar o ciclo completo de documento e tarefas.|
|Navegação/rotação/zoom (B05)|Navegação/zoom/rotação próprios; geometria original parcial e D15 navegação1/8/1.|Limites/modos efetivos, estados primeira/intermediária/última/sem documento e interação com rotação/CropBox.|
|Apresentação ajustar/preencher (B05)|Apresentação GTK própria; comparação integral ausente.|Ajustar/preencher, atalhos, foco e múltiplos monitores observados no alvo e validados no desktop.|
|Busca literal/palavra inteira/maiúsculas (B04)|Literal/palavra inteira/caixa próprios e recortes comparados; D11-missing exato observado.|Destinos e ordenação mista, destaques, normalização completa, limites/cancelamento e vazio sem presumir retorno de backend.|
|Busca em marcadores (B04)|Dois hits observados; destinos inconclusivos.|Ativação/destinos dos dois resultados, ordenação e associação dinâmica 7911/7913.|
|Busca em comentários (B04)|Autor corrigido na fonte 168381b,403/403 Linux registrados; Flatpak0.1.13 anterior à correção.|Demais tipos/campos/respostas, duplicação, destinos e ordenação; empacotar correção de autor já validada na fonte.|
|Busca em anexos (B04)|Extratores UTF8/PDF e contratos próprios da 0.1.6; comparação integral ausente.|Travessia/extratores/formatos/limites e associação de resultados comparados com o original.|
|Índice persistente/pesquisa de coleção (B04)|Snapshot JSON local de PDFs selecionados; não equivale ao índice completo do Foxit.|Disponibilidade Reader, manutenção/exclusões/locking/recuperação e formatos do índice; caracterizar suporte antes de ampliar.|
|Stemming/proximidade/coringas (B04)|Coringas/proximidade próprios em subconjunto; stemming ainda pendente.|Stemming por idioma, distância/proximidade, escaping/expansão e combinação com índice.|
|Seleção/cópia/snapshot (B05)|Seleção retangular/cópia/snapshot próprios em subconjunto.|Ordem lógica/bidirecional, permissões, snapping e coordenadas em todos os modos previstos.|
|Prévia/plano de impressão (B06)|Prévia/plano próprios e observação original D17 limitados; sem impressão física aprovada.|Predefinições/margens/fontes/flags e fluxo completo da fila; impressão física e encerramento após impressão.|
|Livreto/N-up/mosaico (B06)|Livreto/N-up/mosaico próprios; prévia original observada, saída correspondente inconclusiva.|Saída PDF com margens/medidas/ordem correspondentes, rotações e combinações de livreto/N-up/mosaico.|
|Criar/mover/gravar marcadores (B02)|Criar/renomear/mover/excluir subárvore em cópia e histórico de rascunho na 0.1.10.|Diálogos e persistência completa, disponibilidade Reader, hierarquia/destinos/histórico em comparação.|
|Anotações/undo/gravação (B02)|Oito tipos simples delimitados, cinco marcas adicionais e edição comentário/autor na 0.1.13.|Respostas/popup/vínculos, aparências e operações restantes; tipos simples atuais não aprovam edição universal.|
|AcroForm/XFA/eventos (B01)|Tx/checkbox/radio/combos sem texto livre/listas em cópia; histórico e ReadOnly no subconjunto.|Combo editável/texto livre/aparência primeiro; depois eventos, cálculo/validação, XFA e formas restantes de acordo com disponibilidade e contrato.|
|Anexos/portfólios (B07)|Catálogo/árvores/anotação próprios; anexo original 22 bytes/hash comparado.|Portfólios e senha não vazia, políticas de extração; completar comparação e desktop/acessibilidade.|
|Assinaturas/certificados (B08)|Inspeção/integridade CMS offline separada de confiança.|Assinatura de documentos, confiança/cadeia/revogação/tempo e PAdES/LTV; CMS atual só verifica integridade no recorte documentado.|
|Senhas/permissões/RMS (B03)|Senha conhecida/permissões/cópias AES-256 e remoção com senha de proprietário em subconjunto; D15 original observado.|Fluxo cifrado integrado, aplicação de permissões e mensagens; RMS segue sem contrato completo e exige ambiente autorizado.|
|Acessibilidade/voz (B09)|TextView/ATK.Text, nomes e atalhos próprios; validação AT-SPI real pendente.|AT-SPI/leitor de tela real, ordem semântica, voz, foco/atalhos e cobertura efetiva.|
|Medição/calibração (B08)|Distância em centímetros entre pontos; sem calibração personalizada.|Calibração/unidades, snapping/precisão, áreas e perímetros.|
|Camadas/mídia/3D (B08)|Listagem de nomes OCG; alternância/mídia/3D não implementadas integralmente.|Alternar/persistir OCG, combinações, mídia/codecs/eventos e 3D conforme disponibilidade real do Reader.|
|Preferências/tema/persistência (B09)|Tema system/light/dark e pastas locais persistidos.|Defaults, persistência e interdependência dos ajustes restantes; tema/pastas atuais já preservados.|
|Nuvem/colaboração (B10)|Integração direta adiada; fluxo de pasta local não a implementa.|APIs/login/upload/colaboração remota adiados. Manter visíveis sem executá-los ou somar conclusão.|
|Criação/conversão (B07)|PNG/JPEG/BMP/WebP simples, TIFF até 100 páginas e OCR local até 20, com limites registrados.|Inventário Reader/Editor, formatos/conversões restantes, fidelidade/OCR e variantes recusadas; preservar TIFF multipágina 100/OCR 20 atuais.|
|Integrações de sistema/atualização (B09)|Flatpak/launcher/controles fora HOME próprios; desktop real e adaptadores completos pendentes.|Portais/concessão persistente reais, associação de arquivos, atualização/rollback e adaptador Windows posterior.|

## Cobertura dos 19 critérios antigos

Este cruzamento não altera status ou peso. Critério amplo só passa a done mediante evidência de todas as obrigações que ele exige.

| Etapa antiga | Critério ainda aberto | Estado preservado | Plano |
|---|---|---|---|
|03|Motor PDF e fronteiras de todos os subsistemas identificados|pending|P04|
|05|Ciclo de vida de todos os componentes reconstruído|pending|P04|
|07|Universo relevante e assinaturas/saídas de todas as funções definidos|pending|P01, P04|
|08|Fluxo completo de impressão reconstruído|partial|P03, P04, P05|
|08|Fluxo completo de busca reconstruído|partial|P03, P04, P05|
|08|Demais famílias funcionais investigadas profundamente|pending|P03, P04, P05|
|09|Diagramas e estados rastreáveis por subsistema|partial|P04, P05|
|09|Algoritmos completos de todas as famílias especificados|pending|P04, P05|
|10|Cenários locais observados e registrados|partial|P02, P03|
|10|Integrações autorizadas e casos excepcionais observados|partial|P02, P03|
|11|Disponibilidade e comportamento de todas as interações observados|partial|P03|
|12|Entradas/saídas/erros e critérios detalhados por funcionalidade|partial|P01, P05|
|12|Fase A consolidada sem lacunas não declaradas|pending|P01, P05|
|15|Todas as demais famílias implementadas e testadas|partial|P06|
|16|Demais interações e integrações funcionais|partial|P06, P07|
|18|Cenários diferenciais executados no original e na reconstrução|partial|P08|
|18|Resultados e divergências por família disponíveis|partial|P08|
|19|Divergências originais medidas e corrigidas|partial|P06, P08|
|21|Obrigações viáveis encerradas e bloqueios declarados|pending|P09, P10|

## Medição e encerramento

P01 precisa distinguir, por operação: prevista; implementada com referência de código; testada no Linux; observada no original; comparada; aceita; ou lacuna/indisponível/adiada. Um teste pode cobrir várias operações ou somente um caso: sua quantidade não é denominador de funcionalidades.

Se uma medição operacional for adotada, publicar versão do catálogo, critérios e pesos antes de pontuar. Apresentá-la como cobertura daquele escopo conhecido; manter a cobertura global desconhecida nula. Preservar a série antiga 45,13% como checklist. Criar este plano não acrescenta progresso de implementação.

Uma entrega Linux/Flatpak utilizável pode ocorrer em P09 com limitações explícitas. Conclusão de toda a reconstrução exige inventário delimitado, critérios antigos fechados, operações e validação suficientes e obrigações adiadas resolvidas ou alteradas por decisão explícita. Não declarar 100% com cloud/Windows/famílias ainda no escopo e pendentes.

## Posteriores, adiados e excluídos

- **Windows nativo:** posterior à prioridade Linux. Testar o Foxit na VM Windows não valida o Linuxit no Windows; adaptador, UI, associação, descendentes e impressão precisam de evidência própria.
- **Nuvem direta:** permanece adiada. Dois planos S12 da família cloud não serão executados por este roteiro sem nova priorização; não recebem passed. Pastas sincronizadas locais continuam em P07.
- **IA/generativos do Foxit e UPDF:** fora do escopo; não criar etapas de implementação/paridade para esses recursos. Inventários históricos preservados.

## Protocolo de cada lote e passagem para outra IA

1. Ler AGENTS, RETOMADA e este plano; escolher uma operação/variante e confirmar seus pré-requisitos.
2. Executar lote delimitado e examinar resultado. Guardar originais/capturas completas fora do Git.
3. Registrar o que passou, o que falhou e o que não foi executado; separar implementação própria, Linux, original e comparação.
4. Atualizar inventário/pendências/RETOMADA e acrescentar nota com horário real de São Paulo. Marcar done somente com evidência examinada.
5. Fazer commit/push autorizado e confirmar remoto por verify_git_sync.py com recibo fora da árvore. Flatpak somente quando houver marco de entrega do app.
6. Se a VM parar: observar após dez segundos externos sem nova entrada, suspender testes, salvar e avisar. Não pausar/retomar/reiniciar automaticamente.

**Próxima instrução sugerida:** “Leia AGENTS.md, docs/RETOMADA.md e docs/PLANO-DE-CONTINUIDADE.md. Execute P01, começando pela reconciliação das evidências recentes; se a VM continuar indisponível, avance em P06/B01 com testes Linux e preserve a fila P02/P03.”
