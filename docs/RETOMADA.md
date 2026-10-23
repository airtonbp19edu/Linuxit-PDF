# Retomada do Linuxit PDF

**Atualização — 2026/10/23 às 01:11 (America/Sao_Paulo, UTC-03:00):** autoria Airton+coautoria Codex confirmada em695f9bf; retomada Codex agendada23/10 às05:30, Claude confirmou05:10. S1:54 observações/47 entradas novas/7 revisitas,7.904 instruções/27.660 bytes; catálogo350→397 (152REA+245diretas). Opções+6/+7/+0x10, normalização, consultas concretas e fábrica UI esclarecidas; errata+0x2044=CCriticalSection aplicada. S1 eS3 seguem parciais, com lacunas declaradas. VM/E30 em preflight pelo Codex, sem Foxit lançado até este checkpoint; Claude cuida Windows/app. Candidato0.1.19, workflows e critérios preservados. [S1](REA-S1-AVALIACAO-2026-10-23.md), [divisão](DIVISAO-TAREFAS-2026-10-23.md).

## Coordenação vigente entre Claude e Codex

Esta seção e `progresso/notas-continuidade.md` são os pontos de consulta para as
duas IAs. Atualizar o estado aqui antes de assumir uma frente e registrar o lote
com data/hora, evidências examinadas, pendências e commit. Não tomar os avisos
históricos abaixo como instrução nova.

| Frente | Responsável/estado | Referência |
|---|---|---|
| Registro A4–A6, Passo7 | Codex: registrado nesta rodada | `progresso/etapas-pequenas.json`:E32/E33/E34 |
| S1: algoritmo/opções/classes da busca | Codex: dez lotes revisados,47 entradas novas; S1 parcial; próximos alvos no relatório de23/10 | `docs/REA-S1-AVALIACAO-2026-10-23.md` |
| S2/S3/S4 | Abertas; avisar antes de assumir | `docs/ORDEM-CODEX-2026-10-22.md` |
| Windows A6 | Claude em `claude/windows-installer`; parcial, não duplicar | `testes/resultados/a6-windows-2026-10-22/review.json` |
| Candidato0.1.19 | Fonte9fb4f3a, CI39869848800,744/744 por ambiente; retido | `testes/resultados/0.1.19/review.json` |
| Publicação/B3/VM/equipamentos | Aguardam decisão ou ambiente do usuário | Não iniciar por inferência |

Para o Claude: os avisos das12:07 sobre trabalho sem commit e os de19:16 sobre
esperarPasso4 são históricos. Tudo até7558bce está no GitHub. Não publicar o
primeiro candidato7f0f9c1, substituído pela correção da identidade da redação.
Não incorporar os workflows do ramoWindows àmain enquanto preservar a árvore do
candidato for necessário àE29. Fonte/aplicativoLinux não foram alterados noPasso7.


**REA no Codex — 2026/10/22 às 00:43:** registro aplicado e diagnóstico saudável, comunicação MCP independente aprovada (REA6.7.0/207 ferramentas), sem abrir binários ou VM. Reiniciar Codex para carregar no chat. [Resultado e capacidades](REA-CODEX-CONFIGURACAO-2026-10-22.md).

**Estado mais recente (2026/10/21 às 21:40):** ver [RETOMADA-2026-10-21](RETOMADA-2026-10-21.md). A E29 está resolvida; os avisos de prioridade abaixo são históricos. **Lista do que fazer agora (Claude e Codex):** [O-QUE-FAZER-AGORA-2026-10-22](O-QUE-FAZER-AGORA-2026-10-22.md).

**Para o Claude na retomada (2026/10/20 às 17:43):** leia o [recado direto sobre a resolução da E29](PRIORIDADE-E29-ERRO-403-RELEASE.md#recado-direto-ao-claude-na-retomada). Causa confirmada e fluxo corrigido; não refazer o diagnóstico. A próxima publicação real ainda é o comprovante pendente.

**PRIORIDADE (pedido do usuário em 2026/10/20 às 17:09, America/Sao_Paulo):** antes de qualquer outra etapa, identificar por que o token do GitHub Actions recebe **HTTP 403 ao criar releases** (E29). Instruções, fatos já verificados e diagnóstico sugerido em [PRIORIDADE-E29-ERRO-403-RELEASE.md](PRIORIDADE-E29-ERRO-403-RELEASE.md). A 0.1.17 já está publicada; não publicar nem apagar releases.

**E29 — diagnóstico confirmado em 2026/10/20 às 17:22:** mesmo token criou rascunhos na main (201/201), mas alvo antigo com workflows diferentes recebeu403. Causa e correção no documento prioritário vinculado acima. Fluxo corrigido passou em conferência somente leitura (CI39491077708), oito guardas aprovadas. Releases/VM intactas. Falta validar a próxima publicação automática autorizada; E29 permanece aberta nesse critério. Não repetir análise da causa nem publicar nova versão nesta rodada.

Situação atual (feito, em andamento, falta) e avisos ao usuário: [AVISOS-E-STATUS.md](AVISOS-E-STATUS.md).

Atualização 2026/10/20 às 00:19 (America/Sao_Paulo, UTC-03:00): defeito RFC 3161 com OpenSSL 3.0 corrigido; registros atuais reconciliados com o código 0.1.16; **46 dos 50 planos de aceitação S12 executados e aprovados** como contrato próprio na revisão 841557d ([como executar](../testes/aceitacao/README.md), [resultado](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24.json)); suíte própria 571/571 local e no CI Debian 13 (execução 39363684386, aceitação 46/46). Fila vigente no topo de [tarefas-pendentes](../progresso/tarefas-pendentes.md). Detalhes na última nota de continuidade.

Relatório completo solicitado em2026-10-19T21:38:45.818557-03:00: [RELATORIO-COMPLETO-LINUXIT-PDF-2026-10-19.md](RELATORIO-COMPLETO-LINUXIT-PDF-2026-10-19.md) e [HTML integral para abrir no navegador](RELATORIO-COMPLETO-LINUXIT-PDF-2026-10-19.html). Fotografia b2bb821,25famílias/111operações/21etapas/58critérios/19pendências/50planos/329entradas estáticas/564testes/17versões/75módulos/60interfaces;78documentos e38registros estruturados completos,143commits. Capítulos13–15 explicam a demora,o fechamento e divergências documentais. Conferidos317hashes de fontes e117textos integrais noHTML; não é nova análise do original,execução de testes ou mudança de critérios. App/Flatpak0.1.16 preservados e VM intocada.

Entrega confirmada 2026-10-19T20:34:43.442911-03:00: fonte e Flatpak **0.1.16/devel**,564/564 testes próprios por ambiente,490 IDs anteriores preservados e74 novos. Publicação técnica517afaf; assetv0.1.16-devel/SHA256 completo e download público HTTP200/118393760bytes conferidos. Auditoria independente11controles/5smoke/3GTK no mesmo bundle sem rebuild,177 arquivos app/3684runtime/483ELF/297avisos e versões fonte conferidos. Desktop0.1.16 portal persistente/revogação/associação/atualização9/9 em cada uma de duas repetições novas, e Windows próprio5/5 em probe separado. [Estado e limites](EXECUCAO-SEM-VM.md). S11, famílias integrais,50S12 e19 critérios amplos continuam abertos. VM suspensa/intocada, nuvem direta adiada; percentual global desconhecido. Histórico abaixo.

Marco 2026-10-19T20:25:14-03:00: fonte e Flatpak **0.1.16/devel** aprovados em564/564 testes próprios por ambiente (fonte Linux,payload,sandbox instalado),490 IDs anteriores preservados e74 novos. Pacote publicado como [prerelease](https://github.com/airtonbp19edu/Linuxit-PDF/releases/tag/v0.1.16-devel); download completo e auditoria independente ainda em andamento. Portal/associação/atualização9/9 no pacote0.1.15 e Windows próprio5/5 em probes separados. Catálogo estático329(152REA+177diretas), seis entradas novas examinadas. VM suspensa/intocada; nuvem direta adiada. S11, famílias integrais,50S12 e19 critérios amplos continuam abertos; isso não é porcentagem global da reconstrução. Histórico abaixo.

Checkpoint 2026-10-19T20:18:59.629581-03:00: [execução sem VM](EXECUCAO-SEM-VM.md). Portal persistente/revogação/associação/atualização passaram9/9 no pacote0.1.15 (CI39339986089/e61d174); Windows próprio5/5. Aviso de falhaa5ebda9 corrigido, histórico preservado. Novo Flatpak0.1.16 CI39339330479 em execução, ainda não publicado; último pacote0.1.15 preservado. Seis novas entradas estáticas, catálogo329(152REA+177diretas). VM suspensa/intocada; nuvem direta adiada; famílias completas,50S12 e19 critérios amplos permanecem abertos. Histórico abaixo.

Atualização 2026-10-19T15:28:46-03:00: Fonte0.1.16 em execução abrangente sem VM: [estado/contratos](EXECUCAO-SEM-VM.md), S01–S03 aprovados516/516 Linux na revisão5a4729e. S04 acrescenta edição cifrada preservando senhas/permissões, impressão da sessão/camadas e cancelamento CUPS;10 portáveis e regressões14+8 passaram, Linux/probe pendentes. Último Flatpak0.1.15 preservado. VM suspensa/intocada, nuvem direta adiada, famílias integrais e critérios intactos. Próximo S05 anexos/índice/idiomas enquanto CI S04 executa.

Entrega0.1.15 confirmada em2026-10-19T14:43:28-03:00: [lotes e pendências](LOTES-FUNCIONALIDADES.md),490/490 testes próprios por ambiente fonte/payload/sandbox. Auditoria do mesmo bundle sem rebuild aprovada:7controles/5smoke/3GTK,160 arquivos app e3414 de dependências conferidos,181 avisos/versões fonte. Download público HTTP200,58072096bytes/SHA256 confere. Publicação técnica d0d9bec; notas finais recebem commit próprio. Item23/nuvem direta adiado; famílias integrais e50S12 abertos, VM0930 suspensa e intocada. Não é conclusão global nem paridade. Histórico abaixo.

Atualização 2026-10-19T14:36:34-03:00: [lotes4–25 e entrega própria0.1.15](LOTES-FUNCIONALIDADES.md). **490/490 testes próprios por ambiente** fonte Linux/payload/Flatpak,0falhas/erros/skips;432 IDs preservados e58 novos. AT-SPI entre processos, portal real X11, voz WAV e camadas por pixels aprovados nos recortes sintéticos; nove telas examinadas. Pacote preparado, publicação/auditoria independente a confirmar. Item23/nuvem direta permanece adiado; VM0930 suspensa no relógio09:54:23 e intocada. Famílias completas/paridade0/25,50 aceitaçõesS12 e19 critérios amplos continuam abertos. Histórico abaixo.

Atualização 2026-10-19T14:19:59-03:00: [sequência dos25 itens em lotes](LOTES-FUNCIONALIDADES.md) percorrida com implementações próprias4–25, nuvem direta23 adiada. Fonte0.1.15 em validação consolidada; último pacote0.1.14 preservado. Lote13–15 passou465/465 Linux e19–21 teve CI aprovado (relatório a consolidar). Não é conclusão das famílias; VM suspensa, critérios/pesos/paridade intactos. Próximo: resultados/probes e entrega consolidada.

Atualização 2026-10-19T12:39:30-03:00: sequência dos25 itens em lotes de3 em [LOTES-FUNCIONALIDADES.md](LOTES-FUNCIONALIDADES.md). Lote4–6 implementado na fonte0.1.15,7 testes portáveis passaram/2 GTK pendentes; Linux ainda não validado. Nuvem direta23 permanece adiada por confirmação do usuário. Último pacote0.1.14 preservado; VM suspensa e critérios/paridade intactos.

Entrega0.1.14 confirmada em2026-10-19T12:20:01-03:00: [relatório](LEITURA-ABERTURA-NAVEGACAO-APRESENTACAO.md),432/432 próprios por ambiente; auditoria instalada7controles/5smoke/3GTK passou sem rebuild e download público HTTP200/hash/tamanho confere. Commit de publicação38cb933; evidências emtestes/resultados/0.1.14/. Dois monitores virtuais/layout/hotplug aprovados na fonte; físico/Wayland/original e famílias completas pendentes. VM0930 permanece suspensa; nenhuma entrada nesta rodada. Próximo sem VM: P06/B01, comboAcroForm editável, conforme contratos. Histórico abaixo.

Atualização 2026-10-19T12:12:33-03:00: [leitura, navegação e apresentação0.1.14](LEITURA-ABERTURA-NAVEGACAO-APRESENTACAO.md). **432/432 testes próprios por ambiente** fonte Linux/payload/Flatpak, sem falhas/erros/skips;14 portáveis e15 GTK novos. Pacote0.1.14/devel contém abertura transacional com senha/recuperação, zoom1–6400/viewport virtual e apresentação com seleção de monitor. Monitores físicos e comparação integral Foxit pendentes; usuário sem desktop Linux com duas telas. VM0930 permanece suspensa no relógio09:54:23. Não encerra famílias nem P01–P03; critérios/paridade intactos. Histórico abaixo.

Atualização 2026-10-19T10:53:45-03:00: [implementação dos itens1–3 da lista de funcionalidades](LEITURA-ABERTURA-NAVEGACAO-APRESENTACAO.md). Fonte0.1.14 em validação: abertura transacional com senha/recuperação, zoom digitável1–6400/viewport virtual e apresentação com seleção de monitor. 14 testes portáveis passaram; Linux/GTK e pacote ainda pendentes. Usuário não dispõe de Linux com dois monitores. Não é conclusão de famílias nem dos pacotesP01–P03; VM0930 continua suspensa no checkpoint anterior. Critérios e paridade intactos.

Checkpoint 2026-10-19T09:58:26-03:00: [UI03/04 e nova parada da VM](P03-INTERFACE-E-PARADA-2026-10-19.md). Navegação1→2→3→8 e limites de zoom1%/6400% observados; FitPage47.15%. Relógio09:54:23 sem avanço entre capturas separadas por35.6s externos. Usuário confirmou travamento e encerrou por hoje. Entradas suspensas; sem rede/reboot/pause/kill/stop após constatação. Hostrunning/cabooff, janela Foxit visível; estado final de processos/coletor0930 e integridade pós-parada não confirmados. P03 parcial/bloqueada; não superar a parada automaticamente.13 métricas iguais/quatro inconclusivas e app/Flatpak/critérios intactos. Registros anteriores abaixo são históricos.

Atualização 2026-10-19T09:26:14-03:00: [D12 observado e novas saídas de impressão](P03-CANCELAMENTO-MOSAICO-2026-10-19.md). Stop ativo→232 resultados; troca mantém busca original; fechar aba ativa encerra→1738. N-up4mm comparado:13 métricas iguais/quatro inconclusivas no consolidado; mosaico200%/5mm gerou48 páginas. Foxit fechado normalmente, zero residual/fila, dez Inputs íntegros, cabooff. Coletor0113 Ready/result0 sem recibo end; novo observador/preflight antes de reabrir. P03 parcial, pronta para próximo lote; não há parada atual confirmada. App/Flatpak/critérios intactos. Registros anteriores abaixo são históricos.

Checkpoint 2026-10-19T01:08:44-03:00: [P03 suspensa pelo relógio](P03-PARADA-2026-10-19-0105.md). Busca ativa no corpus5000 observada; Stop enviado uma vez, efeito desconhecido. Relógio01:02:45 sem avanço e capturas iguais após10s externos. Nenhuma nova entrada, rede, reboot/pause/kill após constatação; hostrunning/cabooff, original/observador0048 sem estado final confirmado. P02 concluída, P03 parcial/bloqueada; não superar a parada automaticamente. Gerador próprio preservado em scripts/prepare_search_cancel_variant.py. Histórico abaixo.

Atualização 2026-10-19T00:36:40-03:00: [P03 busca/impressão parcial](P03-BUSCA-IMPRESSAO-2026-10-19.md). P02 concluída; P03 executou original offline com coletor2359 limitado. D07 seleção versus ativação1→2; D10 seis hits; D12 sem Stop ativo. N-up2/livreto4 páginas gerados, reabertos e renderizados, com parâmetros distintos de C18; comparação ainda aberta. UI05 par correto/No, UI02 sem documento; Foxit fechado sem residual identificado e tarefa2359 Ready/result0, cabooff e dez Inputs intactos. Não enviar comandos ao coletor encerrado; próximo RunId/preflight. Fila detalhada no relatório; critérios/pesos/app/pacote intactos. Registros anteriores abaixo são históricos.

Atualização 2026-10-18T23:56:42-03:00: [P02 validada offline](P02-COLETOR-VALIDADO-2026-10-18.md).
Coletor corrigido instalado com token interativo limitado; startup/pf/col/end
completos, dez Inputs/RX/isolamento conferidos e parada normal sem Foxit.
P03 pronta para novo observador e preflight/controle visual. Rede desligada.
P01 provisória preservada; registros anteriores abaixo são históricos.

Retomada mais recente: [controle de entrada da VM](VM-RETOMADA-2026-10-18-2336.md), em 2026-10-18T23:39:28-03:00.
Relógio23:36:09 sem avanço após10 segundos externos; duas capturas VBox idênticas.
P02 permanece bloqueada e P03 não iniciada; nenhuma entrada/deploy/rede/reboot.
P01 provisória preservada. Não superar a parada automaticamente. Registros
anteriores abaixo são históricos; estado em progresso/execucao-plano.json.

Pedido P01–P03 executado até o limite do ambiente: [P01 concluída para catálogo
provisório; P02/P03 bloqueadas](EXECUCAO-P01-P03-2026-10-18.md). Inventário111
recortes/25 famílias em INVENTARIO-OPERACOES.md; matriz/contratos reconciliados.
Nova conferência do relógio:21:49:22 sem avanço, duas capturas idênticas após
espera externa. Sem entrada/deploy/rede/reboot; não esperar respostas de2020.
Quando o guest responder, validar P02 antes de original/P03. Histórico abaixo.

Sequência para prosseguir: [plano P01–P10](PLANO-DE-CONTINUIDADE.md),
com os 19 critérios abertos e as 25 famílias mapeados. Primeiro P01: inventário
operacional/reconciliação; primeira entrega própria candidata P06/B01: combo
AcroForm editável. Análise estática P04 e testes Linux podem avançar sem VM.
P02/P03 permanecem sujeitos à resposta da VM e contenção; o plano não retomou
os testes suspensos nem alterou o aplicativo ou os pesos.

**Testes suspensos pela regra do usuário:** relógio permaneceu em21:24:14 após
dez segundos externos. Foxit já fechado normalmente, zero processos confirmado
na manutenção; rede desligada. Não reiniciar/pausar automaticamente. Último lote:
D15 senha correta em abertura independente,8 páginas e navegação1→8→1;
UI05 extra com duas abas/No observado. Ver [checkpoint e próximo passo](VM-SENHA-E-PARADA-2026-10-18.md).
Coletor2020 terminou com erro1; guardas de nomes/capacidade corrigidas no código,
com controles no host, ainda sem instalação/integração no guest. Tarefa2130 não
criada. Após restaurar resposta, validar coletor novo/IDs curtos/offline/limitado
antes de executar o original. Pendências amplas e pacote preservados.

Nova rodada offline2020: consulta exata D11 retornou zero e passou na comparação.
Consolidado12/12 medições iguais, cinco inconclusivas; onze preservadas/uma nova.
UI01 com documento/cancelar observado; destinos D07 ainda abertos. Ver
[relatório atual](VM-BUSCA-2026-10-18-2020.md). App/Flatpak intactos; não são famílias completas.

VM, rodada posterior: [segundos habilitados e continuação offline](VM-RELOGIO-SEGUNDOS.md).
UI01 sem documento/cancelar e D07 com dois resultados observados; destinos ainda
inconclusivos devido à resposta intermitente do ambiente. RunId `vm-20261018-1940`;
`probe-stop:stop` confirmado completed em `followup.json`; coletor encerrado,
não enviar novos comandos a ele. Última coleta: Foxit PID5280 com janela; manter offline.
Dez Inputs e identidade conferidos novamente; nenhum critério amplo encerrado.

Atualização posterior ao pacote: [busca por autor corrigida](BUSCA-AUTOR-COMENTARIOS.md) na fonte,
**403/403 testes Linux** e 11/11 medições iguais na comparação anterior.
Naquele marco havia cinco inconclusivos e um pendente; o consolidado atual está acima. O Flatpak 0.1.13 continua
anterior à correção, com 400/400 por ambiente no marco de entrega. Nenhum novo
pacote nesta rodada. D20: espera observada em splwow64.exe; causa aberta.

Fonte e Flatpak **0.1.13/devel**, com [anotações adicionais](ANOTACOES-AMPLIADAS.md):
sublinhado, tachado e ondulado por área, elipse e linha em qualquer direção.
Aparência vetorial própria vermelha. Edição de comentário/autor e exclusão
restritas a oito tipos simples desbloqueados, sem vínculos ou dependentes.
Rascunho com desfazer/refazer; original e cópias salvas preservados.

**Na entrega 0.1.13, 400/400 testes próprios por ambiente**: fonte, payload e sandbox instalado,
sem falhas/erros/skips. Novos: 14 portáveis e seis GTK/Poppler; todos os 380 IDs
anteriores preservados. 106 arquivos app e 11 relatórios CI conferidos;
smoke 5/5 e launcher 3/3. Publicação confirmada; auditoria independente do mesmo bundle aprovada com
sete controles e cinco novos smoke checks, sem rebuild.
Os testes próprios não são paridade Foxit; pacotes/relatórios anteriores preservados.

[TIFF multipágina](TIFF-MULTIPAGINA.md), até 100 páginas na criação, e
[OCR local](OCR-LOCAL.md), até 20 páginas, preservados. Demais anotações,
formulários e famílias completas permanecem abertos. Pastas sincronizadas:
controles fora HOME negado/concedido passaram novamente; cliente real,
portal/concessão persistente, AT-SPI e impressão física ainda pendentes, sem VM Foxit.

Arquitetura: 44 módulos/58 interfaces; catálogo: 323 (152 REA + 171 diretas),
23 subconjuntos/duas propostas em 25 famílias. Índice histórico do checklist:
**45,13%**, 39 done/19 abertos. Conclusão global da recodificação indeterminada;
paridade **0/25**, cobertura global desconhecida. Original observado parcialmente na VM offline.
APIs de nuvem adiadas/IA excluída. Não reiniciar análises preservadas.

[Medição revisada](MEDICAO-PROGRESSO.md): o índice do checklist ignora avanços dentro
de critérios parciais. Não o usar como porcentagem do código reconstruído.
Relatar entregas concretas, validação própria e operações restantes separadamente.

VM: [primeira campanha offline de 18/10](VM-FOXIT-2026-10-18.md) observou o original com
perfil limitado, RX exercitado e hashes preservados. Dos17 recortes C18:
Na campanha inicial:11 comparados,10 iguais/1 divergente (autor). Na fonte
corrigida:11/11 métricas iguais;5 inconclusivos/1pendente preservados.
D01–D20:14 observados no recorte,5 parciais,1 inconclusivo; cancelamento, destinos
dos hits e saída de imposição abertos. D20 deixou processo sem janela; manter
rede desligada e investigar. Nenhuma proteção do host foi alterada.

Instruções permanentes e registros de marcos anteriores abaixo; a síntese acima
e as notas mais recentes definem o estado atual.

## Primeiro ao retomar

1. Ler `progresso/projeto.json`, `progresso/progresso.json`,
   `progresso/tarefas-pendentes.md` e `progresso/matriz-paridade.csv`.
2. Conferir Git local/remoto e preservar mudanças alheias. Publicação de marcos
   está autorizada; sem reset destrutivo/force push. Não precisa criar worktree.
3. Ler o registro de [pendências](../progresso/pendencias-analises.md) e o
   [escopo sem IA](ESCOPO.md). UPDF e assistente generativo permanecem excluídos.
4. Continuar de um alvo/contrato específico; não reiniciar análise geral.
   Atualizar notas com data/hora real de São Paulo após cada lote.

## Passagem para outra IA — 2026/10/18 às 19:13 (America/Sao_Paulo, UTC-03:00)

Este é o arquivo principal de retomada pedido pelo usuário. O histórico completo
fica em [notas-continuidade.md](../progresso/notas-continuidade.md), sempre com
novas notas ao final. Não depende do chat anterior.

Checkout local: `A:\OneDrive\Airton - Profissional\Airton - Professor\Desenvolvimento\Codex\Linuxit-PDF`.
Repositório: [Linuxit-PDF](https://github.com/airtonbp19edu/Linuxit-PDF), branch `main`.
Antes deste checkpoint, HEAD local/remoto confirmado em
`d7bf1fb5d3b626394e58dba24642f4a77500295a`, árvore limpa. Este checkpoint altera
somente documentação; conferir o novo HEAD remoto ao retomar.

Último trabalho técnico: campanha real do Foxit na VM offline, documentada em
[VM-FOXIT-2026-10-18.md](VM-FOXIT-2026-10-18.md). D01–D20 têm 14 recortes observados,
cinco parciais e um inconclusivo. Dos 17 recortes C18: 11 importados, 10 métricas
iguais e uma divergente; cinco inconclusivos e um pendente. A divergência de autor foi medida nessa campanha; a correção posterior na fonte
está em [BUSCA-AUTOR-COMENTARIOS.md](BUSCA-AUTOR-COMENTARIOS.md), com validação
específica registrada nesse relatório. O pacote0.1.13 publicado é anterior à correção.

O CI [39163934943](https://github.com/airtonbp19edu/Linuxit-PDF/actions/runs/39163934943)
validou novamente 400/400 testes próprios na fonte Linux e 17/17 recortes de
backend; 16 controles do comparador passaram no Windows. Nenhum teste novo é
executado por este checkpoint. App e Flatpak continuam 0.1.13/devel; o marco
da VM não mudou o aplicativo nem gerou pacote. Paridade integral 0/25; 19 critérios
abertos. Os 45,13% medem apenas o checklist histórico, não o código reconstruído.

### Estado da VM a reconferir antes de qualquer ação

O último estado examinado foi o da campanha, não uma nova inspeção deste
checkpoint: VirtualBox 7.2.20, VM `Windows 10`, UUID
`9c404eab-84aa-488e-89c2-18577e82c768`, Windows 10 Pro 19045.3803,
10.000 MB/4 vCPUs, conta sintética local `IA Machine` em sessão limitada.
Cabo de rede desligado, zero shares/USB capturado, clipboard/drag-and-drop/VRDE/
áudio desligados. Na coleta final havia Foxit PID 5464 respondendo sem janela
e Notepad PID 1056. PIDs podem mudar; conferir processos, sem assumir que saíram.
Não religar rede com qualquer processo do original ativo.

O coletor da rodada `vm-20261018-1710` recebeu `probe-stop:stop` e encerrou.
Não enviar novos comandos esperando resposta desse coletor. Nova rodada requer
um RunId novo, relançar o script próprio como tarefa interativa limitada e
revalidar contenção, identidade, escrita negada e controle visual antes do Foxit.
Os scripts publicados não provisionam sozinhos o ambiente nem religam a rede.

Referência no guest: `C:\Linuxit\Reference\FoxitPDFReader.exe`; arquivos sintéticos
em `C:\Linuxit\Input`; saídas em `C:\Linuxit\Results`. Reference/Input/Protocol
foram conferidos com escrita negada. SHA-256 do executável em `progresso/projeto.json`.
Não restaurar snapshot, regenerar o corpus ou sobrescrever evidências da campanha
para iniciar outro lote. Nenhum original deve ser executado no host comum.

### Ordem recomendada do trabalho restante

1. Investigar D20: processo sem janela após fechar. A continuação por Computer Use
   confirmou PID5464 e espera da thread2508 em splwow64.exe/PID3880. Preservar
   evidências; essa cadeia pontual ainda não determina causa nem saída completa.
2. Completar os protocolos exatos: D07/D10 (cada resultado de busca e seu destino,
   alternativas de ordenação), D11 (termo/fontes preservados), D12 (cancelamento,
   troca e fechamento durante busca ativa), D15 (senha correta em abertura
   independente), D18 (margens correspondentes e ordem/medidas da saída PDF).
   Completar UI01–UI10, inclusive comportamento dos IDs 7911/7913.
3. Preservar a correção de busca por autor e seus contratos/regressões; ampliar
   casos por tipo de comentário e campo antes de encerrar a família. A ordem mista observada
   com Relevance Ranking ainda exige mais observação antes de mudar o Linuxit.
4. Continuar operações locais e contratos incompletos: combos AcroForm editáveis
   com texto livre/aparência, demais formulários/anotações e limites de conversão/OCR.
   Ampliar casos por família; os 50 planos completos de aceitação não foram executados.
5. Continuar alvos estáticos específicos listados abaixo e em
   [pendencias-analises.md](../progresso/pendencias-analises.md), sem repetir os lotes
   REA/Ghidra já examinados. Há 323 entradas catalogadas; denominador global aberto.
6. Validar desktop Linux real: portais/concessão persistente, cliente externo
   de pasta sincronizada e conflitos, AT-SPI e impressão física. Essas atividades
   não dependem da VM Foxit. Gerar/auditar Flatpak apenas nos marcos de entrega.

IA generativa permanece excluída e APIs diretas de nuvem adiadas. Pastas
sincronizadas locais estão no escopo; não substituir por integração de provedor.

### Onde estão as provas

- Publicáveis: [testes/resultados/vm-2026-10-18/](../testes/resultados/vm-2026-10-18/),
  especialmente `session.json`, `dynamic-cases.json`, `foxit-observations.json`,
  `comparison.json` e `review.json`. Os relatórios CI mantêm a identidade da fonte testada.
- Privadas locais: `analysis-local/vm-20261018-1710/` (telas, relatórios e saídas)
  e `analysis-local/no-vm-release-artifact-12149742247/` (artefato CI conferido).
  Não entram no Git; um clone em outro computador não as recupera.
- Corpus preservado: `analysis-local/comparison-stage18-final/input/`; kit externo
  em `A:\Airtonbp19\LabKits\Linuxit-PDF-20261018-1630`. Não gerar outro no mesmo lugar.
- Estado estruturado: `progresso/progresso.json`, `progresso/pendencias-analises.json`
  e `progresso/matriz-paridade.csv`. Preservar pesos, histórico e distinção entre
  testes próprios, observação original e paridade integral.

## Próximas frentes

- Próxima operação própria sem VM: combos AcroForm editáveis, com texto livre,
  preservação de `/Opt` e geração de aparência. Definir e testar flags/ReadOnly,
  limites, valores fora da lista e histórico antes de integrar. Ainda não implementado.

- Estática 03/05/07/08/09/11: alocação/tamanhos e chamadores dos arrays;
  15cd6e0/15cc9b0; atribuição do provedor ativo em dialog+1e48 e campos restantes
  de SearchOption; contexto0x138, serviços de imagem e ownership. As48 entradas
  desta continuação não devem ser repetidas. Tipos viewer/página/diálogo e
  stemming efetivo foram ligados; IDs7911/7913 ainda têm ambiguidade de comportamento.
- Contratos12/lógica15/UI16: ampliar operações e duas propostas, com nuvem adiada pelo usuário;
  23 subconjuntos parciais e 44 módulos/58 interfaces documentados.
- Runtime: desktop real, portais, AT-SPI, impressora física e serviços externos
  precisam de seus ambientes/equipamentos/contas. Isso é distinto da VM Foxit.
- VM10/11/18/19: completar as variantes da primeira campanha offline e UI01–UI10,
  importar apenas medidas com protocolos/evidências correspondentes e corrigir
  diferenças. Já existem observações originais parciais; os 50 cenários completos
  de aceitação continuam sem execução integral.
- API01 encerrada por nova leitura: regras/rulesetsHTTP200 vazios e main
  protected=false após repositório público. Nenhuma configuração foi alterada.
  Ver REGRAS-REMOTAS-2026-10-18.md.

**Ainda há trabalho viável sem VM.** Aprovar um pacote não encerra essas etapas.
Os checkpoints anteriores estão preservados em
[arquivo histórico](RETOMADA-CHECKPOINTS-2026-10-17.md); suas antigas pendências
GTK/Poppler/pacote não descrevem a entrega atual.

## Ferramentas e ambiente

Estado da campanha de 18/10/2026: VM offline operacional com 10.000 MB/4 vCPUs,
controle visual e original exercitados; detalhes e limitações no checkpoint acima.

Diagnóstico histórico de 18/10/2026 às 01:21: a VM tinha 8000 MB/duas vCPUs;
o usuário relatava lentidão. O log registrava
Integridade da Memória ativa e backend NEM com mensagem Snail execution mode.
Naquela rodada não houve alteração de proteções nem execução do original e o
NAT estava ativo. Esse diagnóstico antecede a configuração e a campanha offline;
não descreve a última contenção verificada. Histórico nas notas de continuidade.

Windows local com Python3.13.15; último diagnóstico sem WSL/GTK/Flatpak.
Linux foi exercitado no CI Debian13 com GTK/Cairo/Poppler/CUPS e X11 virtual,
pelo código primeiro e Flatpak depois. Usar `/usr/bin/python3` para as extensões
nativas; Python do PATH pode ser incompatível.

Ferramentas confirmadas: REA6.5.0, Ghidra12.1.4, Temurin21.0.12.1 e Node24.22.0.
As rodadas novas são Ghidra direto `-noanalysis` com seed script REA, **não nova
observação MCP**. Caminhos: `A:\Programas\ghidra_12.1.4_PUBLIC`,
`A:\Programas\Eclipse Temurin JDK`, original em
`A:\Programas\Foxit PDF Reader\Foxit PDF Reader\FoxitPDFReader.exe`.
Hash de referência em `progresso/projeto.json`.

`scripts/analyze_foxit_headless.py --project-snapshot <projeto concluído>` copia
um projeto preservado para nova rodada; nunca modifica a origem. Selecionar
`--subject-sha256` para a DLL pinada; projetos e metadados exigem hash compatível. Manifestos
anteriores devem ser preservados. Originais/decompilações não entram no Git.
Não lançar Foxit no host normal; [preparação da contenção](COMO-CONTINUAR.md).

## Verificações

```bash
/usr/bin/python3 scripts/validate_functional_spec.py --check-render docs/contratos-funcionais.md
/usr/bin/python3 scripts/check_architecture.py
/usr/bin/python3 scripts/run_tests.py --output /tmp/linuxit-testes-novos.json
```

O último comando exige dependências Linux e tela para completar 400 testes sem
skips. Fluxos manuais de CI: `no-vm-validation.yml` (fonte/corpus),
`linux-flatpak.yml` (fonte/payload/sandbox) e `delivery-audit.yml` (bundle
publicado reinstalado sem rebuild). Fontes/licenças, builder pareado e
`runtime-lib` devem ser preservados. Instruções: [instalação](instalacao.md).
