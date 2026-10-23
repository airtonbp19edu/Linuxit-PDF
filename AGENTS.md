# Linuxit PDF — continuidade do projeto

**Continuidade — 2026/10/23 às 14:13:** Codex assumiu somente o diagnósticoOCR/mídiaWindows após45min sem atividade observada. Dois erros do CI39984153516 identificados: fonteLinux fixa e gtksink ausente; correções em ramo próprio458e3b3, novo CI39993158728 em andamento. Pausasredação/XFA e reservaVM preservadas; sem alterarapp/tests/workflowsmain, candidato ou critérios. [Checkpoint](docs/CONTINUIDADE-OCR-MIDIA-WINDOWS-2026-10-23.md).

**Coordenação — 2026/10/23 às 12:17:** monitor de interrupção de Claude ativo a cada10min, assunção após45min sem mensagem/commit relevante ou entrega explícita. Primeira amostra salva; nenhuma interrupção confirmada. S1/S2/S3 reservadas por Claude; lotesCodex anteriores apenas salvos, sem nova análise. VM tem reserva independente e não foi acessada. Claude informou retorno15:20; combinar entrega pelo chat. Protocolo: [continuidade](docs/COORDENACAO-INTERRUPCOES-2026-10-23.md).

**Marco estático — 2026/10/23 às 06:06 (America/Sao_Paulo, UTC−03:00):** mais seis entradas de BooleanWeight/scorers e oito de reflow revisadas;931 instruções/2.760 bytes conferidos. Catálogo410→424 (152REA+272diretas). Nesta retomada05:30:31 observações,27 novas/4 revisitas,3.511 instruções/11.500 bytes. S1/S2/S3/S4 integrais permanecem parciais; os lotes encerram recortes delimitados. Claude observou UI01/cancelar e UI02 na VM e conserva a reserva; Codex não acessou a VM na retomada. Candidato0.1.19, app/tests/aceitação, workflows, releases e critérios/pesos preservados pelo Codex. [Pesos/scorers](docs/REA-S1-PESOS-E-SCORERS-2026-10-23.md), [reflow](docs/REA-S4-REFLOW-2026-10-23.md).

**Retomada — 2026/10/23 às 05:46 (America/Sao_Paulo, UTC−03:00):** retorno pontual das05:30 executado e automação removida após cumprir a finalidade. Claude reservou VM/E30 às02:17; sem LIBEREI no minichat, Codex não acessou a VM nesta retomada. Última ação anterior: Abrir com documento em01:29:57, Cancelar ainda não enviado; interrupção por limite de uso, sem travamento confirmado. S2/S3:17 observações conferidas,13 entradas novas/4 revisitas,2.580 instruções/8.740 bytes; catálogo397→410 (152REA+258diretas). Laço GDI, DEVMODE/RAW e seletores do resumo de comentários detalhados; S1/S2/S3 integrais continuam parciais. S4 e pesos da busca em análise dirigida. App, candidato0.1.19, workflows, critérios/pesos e releases preservados pelo Codex. [S2](docs/REA-S2-CONTINUACAO-2026-10-23.md), [S3](docs/REA-S3-ANOTACOES-RESUMO-2026-10-23.md), [E30](docs/VM-E30-INTERRUPCAO-E-RETOMADA-2026-10-23.md).

**DIVISÃO DE TAREFAS EM VIGOR (2026/10/23 às 00:50):** [DIVISAO-TAREFAS-2026-10-23](docs/DIVISAO-TAREFAS-2026-10-23.md). Ajuste das 01:05: Claude: instalador Windows, correções no app do que a VM revelar, kit E23, proposta B3, revisão 0.1.19. Codex: S1, VM/E30 (operador exclusivo), S2, S3/C1, S4. Chat: cada um escreve só no próprio arquivo (CHAT-CLAUDE.txt / CHAT-CODEX.txt). **VM (00:57, pedido do usuário):** se o Codex não conseguir concluir a E30 (LIBEREI/BLOQUEADO no chat, ou mais de 60 min sem atividade com a E30 pendente), o Claude assume, depois de escrever PEGUEI E30; nunca os dois na VM ao mesmo tempo. Os dois trabalham ao mesmo tempo, sem parar a cada etapa nesta rodada (pedido do usuário às 00:44). Retorno após interrupção: **Claude 05:10, Codex 05:30**; o Codex deve agendar o próprio retorno. Continuam proibidos: publicar release, decidir B3, VM pelo Codex enquanto o Claude estiver nela.

**AUTORIA CONFIRMADA PELO USUÁRIO — 2026/10/23 às 00:39 (America/Sao_Paulo):** manter `Airtonbp19 <airtonbp19.edu@gmail.com>` como autor dos novos commits do Codex e incluir exatamente uma vez, ao final da mensagem, `Co-authored-by: Codex <noreply@openai.com>`. O usuário escolheu manter sua conta, sem conta separada para o Codex. Não reescrever commits antigos nem alterar as configurações do Claude. A opção `commit_attribution` não foi encontrada na configuração instalada; a garantia nesta rodada é o trailer explícito conferido no commit, não uma configuração global presumida. Coautoria registrada não garante uma conta separada na lista lateral de contribuidores. Evidências em [COAUTORIA-CODEX-2026-10-23](docs/COAUTORIA-CODEX-2026-10-23.md).

**MINICHAT CLAUDE ↔ CODEX:** cada agente escreve apenas seu arquivo local ignorado: Codex em `CHAT-CODEX.txt`, Claude em `CHAT-CLAUDE.txt`; cada um lê o outro antes e depois das tarefas. `CHAT-IA.txt` é histórico, pois gravações concorrentes apagaram linhas. Usar horário real e PEGUEI/TERMINEI/LIBEREI. O registro oficial continua nos avisos e nas notas de continuidade. Retorno Codex05:30 executado em23/10 e automação pontual removida; Claude havia confirmado05:10. Sinais VM no ramo `codex/vm-status`, com avanço normal e sem sobrescrever histórico.

**Atualização — 2026/10/23 às 01:11 (America/Sao_Paulo, UTC-03:00):** autoria Airton+coautoria Codex confirmada em695f9bf; retomada Codex agendada23/10 às05:30, Claude confirmou05:10. S1:54 observações/47 entradas novas/7 revisitas,7.904 instruções/27.660 bytes; catálogo350→397 (152REA+245diretas). Opções+6/+7/+0x10, normalização, consultas concretas e fábrica UI esclarecidas; errata+0x2044=CCriticalSection aplicada. S1 eS3 seguem parciais, com lacunas declaradas. VM/E30 em preflight pelo Codex, sem Foxit lançado até este checkpoint; Claude cuida Windows/app. Candidato0.1.19, workflows e critérios preservados. [S1](docs/REA-S1-AVALIACAO-2026-10-23.md), [divisão](docs/DIVISAO-TAREFAS-2026-10-23.md).

**Estado mais recente (2026/10/21 às 21:40):** ver [RETOMADA-2026-10-21](docs/RETOMADA-2026-10-21.md). A E29 está resolvida; os avisos de prioridade abaixo são históricos. **Lista do que fazer agora (Claude e Codex):** [O-QUE-FAZER-AGORA-2026-10-22](docs/O-QUE-FAZER-AGORA-2026-10-22.md).

**CODEX, LEIA PRIMEIRO:** [ORDEM-CODEX-2026-10-22](docs/ORDEM-CODEX-2026-10-22.md). O diagnóstico das12:07 é histórico: o trabalho A4/A5/A6 já foi salvo e os Passos1–3 receberam registros e validação Linux. Passos4–6 receberam a autorização posterior do usuário e foram executados; o Passo7 recebeu autorização posterior e foi registrado; a publicação continua aguardando autorização específica. A mesma ordem lista o restante do projeto.

**PRIORIDADE (pedido do usuário em 2026/10/20 às 17:09, America/Sao_Paulo):** antes de qualquer outra etapa, identificar por que o token do GitHub Actions recebe **HTTP 403 ao criar releases** (E29). Instruções, fatos já verificados e diagnóstico sugerido em [docs/PRIORIDADE-E29-ERRO-403-RELEASE.md](docs/PRIORIDADE-E29-ERRO-403-RELEASE.md). A 0.1.17 já está publicada; não publicar nem apagar releases.

**E29 — diagnóstico confirmado em 2026/10/20 às 17:22:** mesmo token criou rascunhos na main (201/201), mas alvo antigo com workflows diferentes recebeu403. Causa e correção no documento prioritário vinculado acima. Fluxo corrigido passou em conferência somente leitura (CI39491077708), oito guardas aprovadas. Releases/VM intactas. Falta validar a próxima publicação automática autorizada; E29 permanece aberta nesse critério. Não repetir análise da causa nem publicar nova versão nesta rodada.

Atualização 2026/10/20 às 00:19 (America/Sao_Paulo, UTC-03:00): defeito RFC 3161 com OpenSSL 3.0 corrigido; registros atuais reconciliados com o código 0.1.16; **46 dos 50 planos de aceitação S12 executados e aprovados** como contrato próprio na revisão 841557d ([como executar](testes/aceitacao/README.md), [resultado](testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24.json)); suíte própria 571/571 local e no CI Debian 13 (execução 39363684386, aceitação 46/46). Fila vigente no topo de [tarefas-pendentes](progresso/tarefas-pendentes.md). Detalhes na última nota de continuidade.

Relatório completo solicitado em2026-10-19T21:38:45.818557-03:00: [RELATORIO-COMPLETO-LINUXIT-PDF-2026-10-19.md](docs/RELATORIO-COMPLETO-LINUXIT-PDF-2026-10-19.md) e [HTML integral para abrir no navegador](docs/RELATORIO-COMPLETO-LINUXIT-PDF-2026-10-19.html). Fotografia b2bb821,25famílias/111operações/21etapas/58critérios/19pendências/50planos/329entradas estáticas/564testes/17versões/75módulos/60interfaces;78documentos e38registros estruturados completos,143commits. Capítulos13–15 explicam a demora,o fechamento e divergências documentais. Conferidos317hashes de fontes e117textos integrais noHTML; não é nova análise do original,execução de testes ou mudança de critérios. App/Flatpak0.1.16 preservados e VM intocada.

Entrega confirmada 2026-10-19T20:34:43.442911-03:00: fonte e Flatpak **0.1.16/devel**,564/564 testes próprios por ambiente,490 IDs anteriores preservados e74 novos. Publicação técnica517afaf; assetv0.1.16-devel/SHA256 completo e download público HTTP200/118393760bytes conferidos. Auditoria independente11controles/5smoke/3GTK no mesmo bundle sem rebuild,177 arquivos app/3684runtime/483ELF/297avisos e versões fonte conferidos. Desktop0.1.16 portal persistente/revogação/associação/atualização9/9 em cada uma de duas repetições novas, e Windows próprio5/5 em probe separado. [Estado e limites](docs/EXECUCAO-SEM-VM.md). S11, famílias integrais,50S12 e19 critérios amplos continuam abertos. VM suspensa/intocada, nuvem direta adiada; percentual global desconhecido. Histórico abaixo.

Marco 2026-10-19T20:25:14-03:00: fonte e Flatpak **0.1.16/devel** aprovados em564/564 testes próprios por ambiente (fonte Linux,payload,sandbox instalado),490 IDs anteriores preservados e74 novos. Pacote publicado como [prerelease](https://github.com/airtonbp19edu/Linuxit-PDF/releases/tag/v0.1.16-devel); download completo e auditoria independente ainda em andamento. Portal/associação/atualização9/9 no pacote0.1.15 e Windows próprio5/5 em probes separados. Catálogo estático329(152REA+177diretas), seis entradas novas examinadas. VM suspensa/intocada; nuvem direta adiada. S11, famílias integrais,50S12 e19 critérios amplos continuam abertos; isso não é porcentagem global da reconstrução. Histórico abaixo.

Checkpoint 2026-10-19T20:18:59.629581-03:00: [execução sem VM](docs/EXECUCAO-SEM-VM.md). Portal persistente/revogação/associação/atualização passaram9/9 no pacote0.1.15 (CI39339986089/e61d174); Windows próprio5/5. Aviso de falhaa5ebda9 corrigido, histórico preservado. Novo Flatpak0.1.16 CI39339330479 em execução, ainda não publicado; último pacote0.1.15 preservado. Seis novas entradas estáticas, catálogo329(152REA+177diretas). VM suspensa/intocada; nuvem direta adiada; famílias completas,50S12 e19 critérios amplos permanecem abertos. Histórico abaixo.

Atualização 2026-10-19T15:28:46-03:00: Fonte0.1.16 em execução abrangente sem VM: [estado/contratos](docs/EXECUCAO-SEM-VM.md), S01–S03 aprovados516/516 Linux na revisão5a4729e. S04 acrescenta edição cifrada preservando senhas/permissões, impressão da sessão/camadas e cancelamento CUPS;10 portáveis e regressões14+8 passaram, Linux/probe pendentes. Último Flatpak0.1.15 preservado. VM suspensa/intocada, nuvem direta adiada, famílias integrais e critérios intactos. Próximo S05 anexos/índice/idiomas enquanto CI S04 executa.

Entrega0.1.15 confirmada em2026-10-19T14:43:28-03:00: [lotes e pendências](docs/LOTES-FUNCIONALIDADES.md),490/490 testes próprios por ambiente fonte/payload/sandbox. Auditoria do mesmo bundle sem rebuild aprovada:7controles/5smoke/3GTK,160 arquivos app e3414 de dependências conferidos,181 avisos/versões fonte. Download público HTTP200,58072096bytes/SHA256 confere. Publicação técnica d0d9bec; notas finais recebem commit próprio. Item23/nuvem direta adiado; famílias integrais e50S12 abertos, VM0930 suspensa e intocada. Não é conclusão global nem paridade. Histórico abaixo.

Atualização 2026-10-19T14:36:34-03:00: [lotes4–25 e entrega própria0.1.15](docs/LOTES-FUNCIONALIDADES.md). **490/490 testes próprios por ambiente** fonte Linux/payload/Flatpak,0falhas/erros/skips;432 IDs preservados e58 novos. AT-SPI entre processos, portal real X11, voz WAV e camadas por pixels aprovados nos recortes sintéticos; nove telas examinadas. Pacote preparado, publicação/auditoria independente a confirmar. Item23/nuvem direta permanece adiado; VM0930 suspensa no relógio09:54:23 e intocada. Famílias completas/paridade0/25,50 aceitaçõesS12 e19 critérios amplos continuam abertos. Histórico abaixo.

Atualização 2026-10-19T14:19:59-03:00: [sequência dos25 itens em lotes](docs/LOTES-FUNCIONALIDADES.md) percorrida com implementações próprias4–25, nuvem direta23 adiada. Fonte0.1.15 em validação consolidada; último pacote0.1.14 preservado. Lote13–15 passou465/465 Linux e19–21 teve CI aprovado (relatório a consolidar). Não é conclusão das famílias; VM suspensa, critérios/pesos/paridade intactos. Próximo: resultados/probes e entrega consolidada.

Atualização 2026-10-19T12:39:30-03:00: sequência dos25 itens em lotes de3 em [LOTES-FUNCIONALIDADES.md](docs/LOTES-FUNCIONALIDADES.md). Lote4–6 implementado na fonte0.1.15,7 testes portáveis passaram/2 GTK pendentes; Linux ainda não validado. Nuvem direta23 permanece adiada por confirmação do usuário. Último pacote0.1.14 preservado; VM suspensa e critérios/paridade intactos.

Entrega0.1.14 confirmada em2026-10-19T12:20:01-03:00: [relatório](docs/LEITURA-ABERTURA-NAVEGACAO-APRESENTACAO.md),432/432 próprios por ambiente; auditoria instalada7controles/5smoke/3GTK passou sem rebuild e download público HTTP200/hash/tamanho confere. Commit de publicação38cb933; evidências emtestes/resultados/0.1.14/. Dois monitores virtuais/layout/hotplug aprovados na fonte; físico/Wayland/original e famílias completas pendentes. VM0930 permanece suspensa; nenhuma entrada nesta rodada. Próximo sem VM: P06/B01, comboAcroForm editável, conforme contratos. Histórico abaixo.

Atualização 2026-10-19T12:12:33-03:00: [leitura, navegação e apresentação0.1.14](docs/LEITURA-ABERTURA-NAVEGACAO-APRESENTACAO.md). **432/432 testes próprios por ambiente** fonte Linux/payload/Flatpak, sem falhas/erros/skips;14 portáveis e15 GTK novos. Pacote0.1.14/devel contém abertura transacional com senha/recuperação, zoom1–6400/viewport virtual e apresentação com seleção de monitor. Monitores físicos e comparação integral Foxit pendentes; usuário sem desktop Linux com duas telas. VM0930 permanece suspensa no relógio09:54:23. Não encerra famílias nem P01–P03; critérios/paridade intactos. Histórico abaixo.

Atualização 2026-10-19T10:53:45-03:00: [implementação dos itens1–3 da lista de funcionalidades](docs/LEITURA-ABERTURA-NAVEGACAO-APRESENTACAO.md). Fonte0.1.14 em validação: abertura transacional com senha/recuperação, zoom digitável1–6400/viewport virtual e apresentação com seleção de monitor. 14 testes portáveis passaram; Linux/GTK e pacote ainda pendentes. Usuário não dispõe de Linux com dois monitores. Não é conclusão de famílias nem dos pacotesP01–P03; VM0930 continua suspensa no checkpoint anterior. Critérios e paridade intactos.

Checkpoint 2026-10-19T09:58:26-03:00: [UI03/04 e nova parada da VM](docs/P03-INTERFACE-E-PARADA-2026-10-19.md). Navegação1→2→3→8 e limites de zoom1%/6400% observados; FitPage47.15%. Relógio09:54:23 sem avanço entre capturas separadas por35.6s externos. Usuário confirmou travamento e encerrou por hoje. Entradas suspensas; sem rede/reboot/pause/kill/stop após constatação. Hostrunning/cabooff, janela Foxit visível; estado final de processos/coletor0930 e integridade pós-parada não confirmados. P03 parcial/bloqueada; não superar a parada automaticamente.13 métricas iguais/quatro inconclusivas e app/Flatpak/critérios intactos. Registros anteriores abaixo são históricos.

Atualização 2026-10-19T09:26:14-03:00: [D12 observado e novas saídas de impressão](docs/P03-CANCELAMENTO-MOSAICO-2026-10-19.md). Stop ativo→232 resultados; troca mantém busca original; fechar aba ativa encerra→1738. N-up4mm comparado:13 métricas iguais/quatro inconclusivas no consolidado; mosaico200%/5mm gerou48 páginas. Foxit fechado normalmente, zero residual/fila, dez Inputs íntegros, cabooff. Coletor0113 Ready/result0 sem recibo end; novo observador/preflight antes de reabrir. P03 parcial, pronta para próximo lote; não há parada atual confirmada. App/Flatpak/critérios intactos. Registros anteriores abaixo são históricos.

Checkpoint 2026-10-19T01:08:44-03:00: [P03 suspensa pelo relógio](docs/P03-PARADA-2026-10-19-0105.md). Busca ativa no corpus5000 observada; Stop enviado uma vez, efeito desconhecido. Relógio01:02:45 sem avanço e capturas iguais após10s externos. Nenhuma nova entrada, rede, reboot/pause/kill após constatação; hostrunning/cabooff, original/observador0048 sem estado final confirmado. P02 concluída, P03 parcial/bloqueada; não superar a parada automaticamente. Gerador próprio preservado em scripts/prepare_search_cancel_variant.py. Histórico abaixo.

Atualização 2026-10-19T00:36:40-03:00: [P03 busca/impressão parcial](docs/P03-BUSCA-IMPRESSAO-2026-10-19.md). P02 concluída; P03 executou original offline com coletor2359 limitado. D07 seleção versus ativação1→2; D10 seis hits; D12 sem Stop ativo. N-up2/livreto4 páginas gerados, reabertos e renderizados, com parâmetros distintos de C18; comparação ainda aberta. UI05 par correto/No, UI02 sem documento; Foxit fechado sem residual identificado e tarefa2359 Ready/result0, cabooff e dez Inputs intactos. Não enviar comandos ao coletor encerrado; próximo RunId/preflight. Fila detalhada no relatório; critérios/pesos/app/pacote intactos. Registros anteriores abaixo são históricos.

Atualização 2026-10-18T23:56:42-03:00: [P02 validada offline](docs/P02-COLETOR-VALIDADO-2026-10-18.md).
Coletor corrigido instalado com token interativo limitado; startup/pf/col/end
completos, dez Inputs/RX/isolamento conferidos e parada normal sem Foxit.
P03 pronta para novo observador e preflight/controle visual. Rede desligada.
P01 provisória preservada; registros anteriores abaixo são históricos.

Retomada mais recente: [controle de entrada da VM](docs/VM-RETOMADA-2026-10-18-2336.md), em 2026-10-18T23:39:28-03:00.
Relógio23:36:09 sem avanço após10 segundos externos; duas capturas VBox idênticas.
P02 permanece bloqueada e P03 não iniciada; nenhuma entrada/deploy/rede/reboot.
P01 provisória preservada. Não superar a parada automaticamente. Registros
anteriores abaixo são históricos; estado em progresso/execucao-plano.json.

Execução P01–P03: docs/EXECUCAO-P01-P03-2026-10-18.md. P01 concluída no
catálogo provisório111 recortes/25 famílias; global aberto. P02 bloqueada no
controle atual do relógio21:49:22 após10 segundos externos; P03 não iniciada.
Nenhuma entrada/deploy/rede/reboot emitidos. Scripts/check_operation_catalog.py
e validate_functional_spec.py validam inventário/observação parcial separada.
Estado atual: progresso/execucao-plano.json; critérios antigos intactos.

Plano de execução: [P01–P10](docs/PLANO-DE-CONTINUIDADE.md), com inventário por família,
dependências e critérios de conclusão. São pacotes de continuidade; não substituem
as 21 etapas ponderadas. Começar por P01; sem VM, P06/B01 e P04 podem avançar
com seus contratos/recursos. Testes do original exigem P02, sem revogar a regra
de interrupção pelo relógio. Criar o plano não encerra nenhuma atividade técnica.

Checkpoint mais recente: [senha e parada da VM](docs/VM-SENHA-E-PARADA-2026-10-18.md).
D15 correto em abertura independente abriu8 páginas; UI05 extra/recusa e D20
fechamento normal sem processo residual observados neste contexto. Relógio parou
em21:24:14, confirmado após10 segundos externos; entradas suspensas, usuário
avisado, sem pause/reboot. Foxit já fechado/cabooff. Coletor2020 Ready/result1;
não esperar respostas dele. Guardas do transporte corrigidas/testadas no host,
mas novo script não instalado no guest; tarefa2130 não criada. Retomar pela
validação do coletor com IDs curtos quando a VM responder. Não encerrar famílias.

Nova rodada offline2020: consulta exata D11 retornou zero e passou na comparação.
Consolidado12/12 medições iguais, cinco inconclusivas; onze preservadas/uma nova.
UI01 com documento/cancelar observado; destinos D07 ainda abertos. Ver
[relatório atual](docs/VM-BUSCA-2026-10-18-2020.md). App/Flatpak intactos; não são famílias completas.

Instrução do usuário em 18/10/2026: acompanhar os segundos do relógio da VM.
Se deixarem de avançar ou o ambiente não responder, interromper os testes,
salvar checkpoint com a última ação confirmada e avisar o usuário. Não repetir
cliques nem classificar a parada como falha Foxit; preservar pendências. Ver
protocolo em docs/VM-RELOGIO-SEGUNDOS.md.

Rodada posterior da VM: [relógio com segundos e diagnóstico](docs/VM-RELOGIO-SEGUNDOS.md).
RunId vm-20261018-1940: UI01/D07 parciais, resposta intermitente; não inferir falha
Foxit ou destino nulo. Dez Inputs/identidade preservados. `probe-stop:stop`
confirmado completed; coletor encerrado, ver followup.json. Última coleta tinha
Foxit5280 com janela; manter offline. Nenhum critério amplo encerrado.

Atualização posterior ao pacote: [busca por autor corrigida](docs/BUSCA-AUTOR-COMENTARIOS.md) na fonte,
**403/403 testes Linux** e 11/11 medições iguais na comparação anterior.
Naquele marco havia cinco inconclusivos e um pendente; o consolidado atual está acima. O Flatpak 0.1.13 continua
anterior à correção, com 400/400 por ambiente no marco de entrega. Nenhum novo
pacote nesta rodada. D20: espera observada em splwow64.exe; causa aberta.

Fonte e Flatpak **0.1.13/devel**, com [anotações adicionais](docs/ANOTACOES-AMPLIADAS.md):
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

[TIFF multipágina](docs/TIFF-MULTIPAGINA.md), até 100 páginas na criação, e
[OCR local](docs/OCR-LOCAL.md), até 20 páginas, preservados. Demais anotações,
formulários e famílias completas permanecem abertos. Pastas sincronizadas:
controles fora HOME negado/concedido passaram novamente; cliente real,
portal/concessão persistente, AT-SPI e impressão física ainda pendentes, sem VM Foxit.

Arquitetura: 44 módulos/58 interfaces; catálogo: 323 (152 REA + 171 diretas),
23 subconjuntos/duas propostas em 25 famílias. Índice histórico do checklist:
**45,13%**, 39 done/19 abertos. Conclusão global da recodificação indeterminada;
paridade **0/25**, cobertura global desconhecida. Original observado parcialmente na VM offline.
APIs de nuvem adiadas/IA excluída. Não reiniciar análises preservadas.

Medição revisada em 18/10/2026: [explicação e evidências](docs/MEDICAO-PROGRESSO.md).
Não apresentar o índice do checklist como percentual do código reconstruído. Critérios parciais
pontuam zero no índice antigo; relatar entregas e operações pendentes em separado.
Testes, módulos e famílias com subconjuntos não são denominador de conclusão.

VM: [primeira campanha offline de 18/10](docs/VM-FOXIT-2026-10-18.md) observou o original com
perfil limitado, RX exercitado e hashes preservados. Dos17 recortes C18:
Na campanha inicial:11 comparados,10 iguais/1 divergente (autor). Na fonte
corrigida:11/11 métricas iguais;5 inconclusivos/1pendente preservados.
D01–D20:14 observados no recorte,5 parciais,1 inconclusivo; cancelamento, destinos
dos hits e saída de imposição abertos. D20 deixou processo sem janela; manter
rede desligada e investigar. Nenhuma proteção do host foi alterada.

Instruções permanentes e registros de marcos anteriores abaixo; a síntese acima
e as notas mais recentes definem o estado atual.

Ponto de retomada e estado do ambiente local: `docs/RETOMADA.md`.
Desenvolva e teste pelo código-fonte no Linux; gere Flatpak nos marcos de
entrega, conforme a preferência confirmada pelo usuário em 16/10/2026.

Leia primeiro `progresso/projeto.json`, `progresso/progresso.json`,
`progresso/tarefas-pendentes.md`, `progresso/matriz-paridade.csv` e Git local/remoto.
Não reinicie análises já preservadas. O destino autorizado é este repositório;
Linux/Flatpak tem prioridade, com Windows posteriormente. UPDF permanece fora
do escopo. O pedido mestre autoriza reconstrução incremental, testes e pushes
progressivos; a antiga limitação a somente análise foi ampliada por esse pedido.

Decisão do usuário em 17/10/2026: assistente de IA do Foxit e recursos
generativos estão fora da engenharia reversa, implementação e paridade.
Fonte: `docs/ESCOPO.md` e `scope_exclusions` de `progresso/projeto.json`.
Preservar o inventário histórico de AiAssistant.fpi; não criar alvos/cenários
ou funcionalidades de IA. As 25 famílias atuais permanecem, com operações
PDF e colaboração sem IA no escopo. Pesos e critérios não foram alterados.

- Preserve trabalho de outros colaboradores, sem reset destrutivo ou force push.
- Use REA/Ghidra com seus comandos realmente disponíveis. Registre identidades,
  perfis, falhas, inferências e lacunas; não conte slots como funções únicas.
- Os originais e resultados completos ficam fora do Git. Não incorpore código,
  DLLs, templates ou recursos Foxit à implementação e não contorne proteções.
- A base própria MIT Winux/Print&View e o pypdf BSD têm licenças/proveniência
  preservadas. Reaproveitamento da base não é nova recuperação do Foxit.
- Execute o original somente na contenção offline documentada, com mounts
  mínimos e prefixo sintético. Falhas do Wine não são comportamento do Foxit.
- Testes próprios não contam como paridade diferencial. O universo completo
  de funcionalidades ainda é aberto; cobertura global desconhecida fica nula.
- Atualize verificações e progresso por marco. `scripts/update_progress.py`
  calcula os pesos fixados; mudar critérios/pesos requer histórico explícito.
  Uma atividade `done` exige evidência técnica examinada, além de arquivo existente.
- Publique cada marco autorizado e confirme o remoto. O comprovante final pode
  ser gerado por `scripts/verify_git_sync.py` fora da árvore, evitando autorreferência.
- O último pacote publicado é 0.1.16 de desenvolvimento, branch Flatpak `devel`. Não declare versão estável,
  projeto completo ou 100% sem critérios verificados.
- A criação de worktrees não é necessária neste ambiente isolado.

Fonte: `docs/especificacao.md`, `docs/FOXIT-REA.md`, `docs/proveniencia-base.json`.
Testes: `scripts/run_tests.py` (GUI requer X11/Wayland). Atual0.1.3:
114/114 na fonte Linux, payload e Flatpak instalado, zero falhas/erros/skips;
inclui três métodos de geometria lateral, cinco do painel e sete do auditor.
Recorte lateral corrigido e capturas examinadas. Desktop/acessibilidade,
portais/impressão física pendentes; pedido 760 resulta924 por outros controles.
Empacotamento: `scripts/build_flatpak.py`; não misture bibliotecas nativas com
`/app/lib` padrão. Use `runtime-lib`, loader pareado e módulos OpenSSL incluídos.
A instalação em desktop e o cenário do sandbox estão em `docs/instalacao.md`.

Marcos de busca/impressão: `docs/REA-BUSCA-IMPRESSAO.md` e metadados vinculados.
Catálogo atual: 209 entradas (152 REA + 57 adicionais diretas), cobertura global
indeterminada. Wine/QEMU passa no controle x86; o Foxit carrega mas termina com
CInvalidArgException antes da UI. Não confunda isso com paridade funcional.
Em Linux, use `/usr/bin/python3` para GTK/Cairo (Python 3.13); o Python do PATH pode ser
3.12 e não carrega as extensões do sistema. Os pesos do roteiro não mudaram.

Retomada Windows: `docs/REA-IMPRESSAO-WINDOWS.md`. REA 6.5.0/Ghidra 12.1.4/JDK 21
foram diagnosticados; a análise MCP do executável expirou em 600 s. Três novas
entradas foram examinadas pelo backend direto `-noanalysis`. O projeto dessa
rodada e as respostas completas estão em `analysis-local/`, ignorado pelo Git.
Use `scripts/analyze_foxit_headless.py` para o backend complementar e preserve
os manifestos anteriores ao gerar os metadados de uma nova rodada.

Continuação estática: `docs/REA-IMPRESSAO-CONSUMIDORES.md`. As seis entradas
pendentes de geometria/consumidores foram examinadas e conferidas com Capstone.
Projeto e resultados completos em `analysis-local/headless/windows-print-02`.
Próximos alvos e ressalvas de tipagem constam no relatório. O gerador de
metadados aceita `--round` para preservar a proveniência de cada rodada.

Checkpoint histórico da etapa 11, cujo trabalho estático segue autorizado enquanto o
usuário prepara a VM da etapa 10. Ver `docs/ETAPA-11.md`: nove entradas de
interface examinadas, dez associações contextuais conferidas e ambiguidade
dos IDs 7911/7913 preservada. Não promover tabelas/estados de templates a
comportamento observado. Próximos alvos e lacunas constam no relatório.

Em 17/10/2026 o usuário pediu também a etapa 12. Contratos estruturados em
`docs/especificacao-funcional.json`, registro derivado em
`docs/contratos-funcionais.md` e limites em `docs/ETAPA-12.md`: 25 famílias,
50 cenários planejados, 14 subconjuntos atuais e 11 propostas. Validar com
`scripts/validate_functional_spec.py --check-render docs/contratos-funcionais.md`.
Detalhamento parcial, fase A aberta; testes próprios e propostas não são
observações do original. Preparar casos executáveis por família enquanto a
VM não está disponível, preservando os indicadores e os critérios existentes.

Em 17/10/2026 o usuário pediu seguir a etapa 13 e registrar as pendências por
VM e possíveis limites de tokens. Ver `docs/ETAPA-13.md`,
`docs/arquitetura-componentes.json` e `progresso/pendencias-analises.md`/`.json`.
Os dois critérios de projeto da etapa 13 já estavam `done`; não aumentar os
indicadores por esta revisão. `scripts/check_architecture.py` confere os módulos,
25 famílias e todos os critérios ainda abertos. Marcas/legendas de mosaico
dependem de Cairo; a ausência desse import faz o ramo retornar sem as marcas.
Preservar a distinção entre VM, análise estática, implementação e runtime Linux.
Os timeouts documentados de 1.801,7 s e 600 s não comprovam esgotamento de tokens.
Só atribuir uma interrupção a tokens com evidência; causa desconhecida fica
`null`. Salvar checkpoint após cada lote de alvos e antes de trocar de etapa,
com resultados examinados/pendentes, perfil, evidências, próximo passo e Git.

Etapa 14 conferida em 17/10/2026: `docs/ETAPA-14.md`. O projeto já estava
criado; conservar base e licenças. `scripts/check_project.py` verifica pontos
de entrada e seis controles de worker, sem GTK/Foxit; resultados completos
em `analysis-local/project-stage14-2026-10-17/`. Os dois critérios já estavam
`done`; suíte Linux/GUI/Flatpak não foi repetida. Próxima etapa do roteiro: 15,
com contratos suficientes e dentro do escopo sem IA, mantendo as pendências.

Etapa 15 iniciada sem VM em 17/10/2026: `docs/ETAPA-15.md`. Backend próprio
`app/pdf_attachments.py` e comandos worker `attachments`/`extract-attachment`
listam/extraem anexos de catálogo plano por índice/hash, sem sobrescrita.
14 testes portáveis passaram. GUI, /Kids, portfólios, senha e anexos exclusivos
de anotações continuam pendentes; tamanho real só é limitado após decodificação.
Fonte em desenvolvimento após o Flatpak 0.1.1, sem pacote novo. Arquitetura atual:
20 módulos/13 interfaces; especificação atual: 15 subconjuntos/10 propostas.
Critério amplo da etapa 15 `partial`; pesos e roteiro 43,33% preservados.
Runner aceita `--pattern test_pdf_attachments.py --temp-dir <pasta-gravavel>`
e registra que a execução é parcial. Próximo passo: integrar em GTK/Linux e
validar a UI; comparação Foxit segue dependente da contenção offline.

Etapa 16 em 17/10/2026: `docs/ETAPA-16.md`. Painel Anexos ligado no código de
`app/main.py`, com Atualizar/Salvar selecionado e escolha de pasta. Coordenação
em `app/attachment_tasks.py`: carga sob demanda, gerações e seleção capturada
antes do diálogo; extração já autorizada pode concluir após trocar documento,
sem atualizar o status do novo. 14 testes portáveis passaram após corrigir
UTF-8 do subprocesso. Quatro testes reais GTK ficaram `skipped` por ausência
de GTK/tela; não declarar widgets/layout validados. WSL reconfirmado ausente.
Arquitetura atual: 21 módulos/15 referências de interfaces, nove fechamentos
sem gi/Cairo. Critério amplo da 16 `partial`, pesos e roteiro 43,33% preservados.
Fonte após o Flatpak 0.1.1, sem pacote novo. Próximo passo: executar os quatro
testes GTK e a suíte Linux com tela/Poppler, preservando relatórios anteriores.

A etapa 10 permanece pendente, conforme `docs/ETAPA-10.md`. O preparador
`scripts/prepare_foxit_dynamic.py` gera 20 cenários e kit offline sem executar o
original. Windows 11 Home local sem Sandbox, WSL ausente, usuário sem VM.
Preparação e testes do kit não contam como observação dinâmica; casos `not_run`.

## Notas de continuidade entre IAs

Retomada16/layout: `docs/ETAPA-16-LAYOUT.md`. Run39040860414, fonte
64f76865381b35b4f8204131ef547f210d5d09db. GtkPaned shrink=False preserva mínimo
lateral: antes mínimo221/divisor158/x=-63; depois divisor221/x=0. Mesmo oráculo
corrigido:0/10 antes,10/10 depois. Primeiro diagnóstico comparava só pai/filho
ambos deslocados; passed:true inicial não foi adotado. Três métodos GTK novos
cobrem cinco painéis/duas larguras, divisor/ocultação/leitura e anexo longo.
114/114 em cada suíte fonte/payload/sandbox, smoke 5/5, launcher 3/3. Versão0.1.3,
83 arquivos fonte/payload iguais; 2803 arquivos de dependências/149 pacotes
atribuídos. Relatórios em `testes/resultados/0.1.3/`; raw/logs ignorados em
`analysis-local/sidebar-release-artifact-12104530284/`. Capturas examinadas;
pedido 760 virou924 de largura real, não afirmar suporte real a 760. Notas20/21
abaixo são históricas quanto ao recorte; pesos/paridade/21 critérios abertos
preservados. Próximo passo: quatro subconjuntos Poppler no corpus preservado18;
original exige VM offline, desktop/portais/acessibilidade/impressão pendentes.

Etapa 21: `docs/ETAPA-21.md`. Auditor `scripts/audit_delivery.py`, receita
manual `delivery-audit.yml` e `scripts/ci_audit_delivery.sh`. Run 39039390847,
código 2e6671825317a7e7846193973113f090365db4f9: bundle 0.1.2 publicado
reinstalado sem rebuild, deployment/OSTree/runtime conferidos, bytes de 83
arquivos app e 2803 de dependências/214 ELF, 149 avisos presentes e hasheados.
Sete controles sintéticos e novo smoke instalado 5/5 passaram. Suíte completa
104/104 da20 não foi repetida; app, versão e bundles preservados. Relatórios em
`testes/resultados/etapa-21/`, raw em `analysis-local/stage21-artifact-12103157602/`.
37 critérios done recebem conferência de links, sem repetir toda REA; 21 abertos
em 14 etapas preservados. Critério de encerramento21 permanece pending (50%);
pesos/paridade intactos. Próximo trabalho sem VM: retomar16 para medir/corrigir
recorte lateral com GTK/captura, depois quatro subconjuntos Poppler no corpus da etapa 18.
O roteiro tem 21 etapas; VM original, fase A e implementação ainda abertas.

Etapa 20: `docs/ETAPA-20.md`, entrega 0.1.2/devel. Workflow manual
`.github/workflows/linux-flatpak.yml` em Debian 13, Xvfb/Openbox e sandbox Flatpak
aninhado no runner efêmero; não alterar Windows ou executar Foxit no CI.
Run 39037892892, fonte e8f9c2e4f48dfc1e5b3cf2a8a6cfe97edb0ee899: 104/104 em
cada suíte fonte/payload/sandbox, 83 arquivos fonte/payload iguais, smoke 5/5,
launcher 3/3. Runtime auditado: 2803 arquivos, 214 ELF e 149 pacotes Debian
com avisos; `runtime-origins.json` acompanha o bundle/relatórios. Cinco casos GTK passaram; recursão dos botões laterais corrigida.
Bundle SHA-256 9d29459d7aff8ca6859cda0846cd698d285b36c3a8de2f463ff87002740cd7ba.
Relatórios em `testes/resultados/0.1.2/`, raw em
`analysis-local/stage20-artifact-12103031377/`. Captura examinada mostra
cabeçalho lateral recortado; acessibilidade sem bus AT-SPI no CI não validada.
Fonte/testes atuais superam as pendências de GTK/pacote das notas históricas
15/16/17/19 abaixo. A campanha de 17 subconjuntos no mesmo corpus da etapa 18
não foi repetida nesta rodada; preservar kit da VM. Critérios/pesos e paridade
não mudaram. Próximo roteiro: 21, auditoria incremental sem encerrar obrigações.

Etapa 19: `docs/ETAPA-19.md`. Normalização de impressão em `app/imposition.py`
agora desvincula a cópia da referência indireta e desloca conteúdo/caixas para
a origem do CropBox após rotação. Corrige deslocamento e mutação do stream do
reader em memória; não deriva geometria Foxit. Nove testes portáveis passaram
em `tests/test_imposition_cropbox.py`; mosaico foi testado sem marcas/legendas.
Regressão copiou os mesmos oito arquivos da etapa 18: 13 subconjuntos aprovados,
quatro bloqueados por Poppler. Dados em `analysis-local/stage19-measurements/`;
kit anterior da VM preservado. Snapshots antigos não aprovam esta nova fonte;
GTK/Linux completo e novo Flatpak continuam pendentes. Critério diferencial
da 19 segue pending; pesos, paridade e versão publicada preservados.

Etapa 18: `docs/ETAPA-18.md`, `testes/plano-comparativo.json` e
`scripts/run_comparison_campaign.py`. São 17 subconjuntos ligados a D01–D20;
13 verificações próprias passaram e quatro dependem de Poppler. Dezesseis
controles do comparador passaram; são dados sintéticos, nunca observação Foxit.
Conservar `analysis-local/comparison-stage18-final/` e seu corpus para a VM.
Importador exige hash de fixture/protocolo/evidência e registro de contenção;
igualdade de medidas manuais não aprova automaticamente uma família. Os 20
casos dinâmicos e 50 de aceitação continuam sem execução completa; critérios
diferenciais da etapa 18 pendentes, pesos e paridade 0/25 preservados.

Etapa 17: `docs/ETAPA-17.md` e `scripts/check_intermediate.py`. Criar diretórios
e relatórios novos por rodada. `portable` compila/testa uma cópia de `app/`,
sem aprovar GUI/Linux. `linux` exige dependências/tela X11, suíte completa sem
skips e smoke GTK. Critérios históricos `done` da 17 pertencem à versão 0.1.1;
a revalidação da fonte posterior é separada e ainda parcial. Não atualizar o
manifesto da versão publicada sem gerar/testar um novo pacote.

A pedido do usuário em 16/10/2026, ao concluir cada rodada registre uma nota em
`progresso/notas-continuidade.md`, com data e horário reais de São Paulo no
formato `AAAA/MM/DD às HH:mm (America/Sao_Paulo, UTC-03:00)`. Informe o que foi
feito, ferramentas/perfis, evidências locais e publicáveis, verificações,
limitações, estado Git/publicação e o próximo passo concreto. Acrescente novas
notas ao final; preserve notas anteriores. Não dependa do histórico do chat.
Não declare publicação remota sem confirmação; registre bloqueios de acesso.

A pedido do usuário em 20/10/2026, todo aviso dado ao usuário (resultado,
bloqueio, publicação, CI em andamento, pedido de ação) também é registrado em
`docs/AVISOS-E-STATUS.md` no GitHub e copiado para a pasta local do projeto
como `AVISOS-LOCAL.md` (ignorado pelo Git). Atualize a seção "Situação atual"
(feito, em andamento, falta) e acrescente o aviso datado ao histórico.

Fila de execução em etapas pequenas (pedido do usuário em 20/10/2026): `progresso/etapas-pequenas.json`,
renderizada em `docs/ETAPAS-PEQUENAS.md` por `scripts/render_small_steps.py` e copiada para
`ETAPAS-LOCAL.md` na pasta local. Seguir a ordem; o que não precisa da VM vem primeiro.

A pedido do usuário em 20/10/2026 às 00:58: ao concluir uma etapa da lista, pare e aguarde a confirmação
do usuário antes de iniciar a próxima. Não avance automaticamente.
