# Tarefas atuais e ponto de retomada

**Atualização — 2026/10/23 às 01:11 (America/Sao_Paulo, UTC-03:00):** autoria Airton+coautoria Codex confirmada em695f9bf; retomada Codex agendada23/10 às05:30, Claude confirmou05:10. S1:54 observações/47 entradas novas/7 revisitas,7.904 instruções/27.660 bytes; catálogo350→397 (152REA+245diretas). Opções+6/+7/+0x10, normalização, consultas concretas e fábrica UI esclarecidas; errata+0x2044=CCriticalSection aplicada. S1 eS3 seguem parciais, com lacunas declaradas. VM/E30 em preflight pelo Codex, sem Foxit lançado até este checkpoint; Claude cuida Windows/app. Candidato0.1.19, workflows e critérios preservados. [S1](../docs/REA-S1-AVALIACAO-2026-10-23.md), [divisão](../docs/DIVISAO-TAREFAS-2026-10-23.md).

## Fila atualizada em22/10/2026

- S1/busca estática:loteCodex concluído em sete entradas novas, catálogo350; S1 parcial. Retomar pelos alvos do relatório, sem duplicar sementes catalogadas.
- Passo7:E32/E33 registrados;E34 continua parcial por Windows/limites universais.
- Windows:capturar InstallLocation real e conteúdo do destino antes de nova correção, conforme relatórioA6.
- Publicar0.1.19:aguarda autorização específica; depois download público/auditoria/desktop.
- VM/equipamentos/B3 continuam dependências externas.

## Fila histórica — 2026/10/19 às 23:55 (America/Sao_Paulo, UTC-03:00)

Esta tabela é a fila vigente. Tudo abaixo dela é histórico, inclusive a tabela da entrega 0.1.13 no fim do arquivo.

| Frente | Próximo trabalho | Depende de |
|---|---|---|
| Aceitação própria (S12) | Executar os casos elegíveis com fixtures identificadas por hash e registrar o resultado por revisão do código | Nada externo |
| Formulários | Contrato para XFA e JavaScript geral (o combo editável e os cálculos declarativos já existem) | Implementação própria |
| Assinaturas | Assinaturas incrementais/múltiplas, DocTimeStamp e PAdES-LTV (CA/CRL e verificação RFC 3161 já existem) | Implementação própria |
| Camadas/mídia/3D | Renderizador U3D/PRC (listar/extrair 3D, mídia e camadas salvas já existem) | Implementação própria |
| Estática | Chamadores, tipos e propriedade/liberação a partir dos resultados preservados; não repetir sementes já feitas | Ghidra e original no PC Windows |
| Original (VM) | Retomar só com autorização do usuário e controle do relógio; testes suspensos desde 09:54:23 de 19/10 | VM offline operacional |
| Ambientes reais | Cliente sincronizador real, impressora, áudio/leitor de tela, monitores físicos, RMS | Equipamentos e materiais |
| Nuvem direta | Adiada pelo usuário | Nova priorização |

Entrega confirmada 2026-10-19T20:34:43.442911-03:00: fonte e Flatpak **0.1.16/devel**,564/564 testes próprios por ambiente,490 IDs anteriores preservados e74 novos. Publicação técnica517afaf; assetv0.1.16-devel/SHA256 completo e download público HTTP200/118393760bytes conferidos. Auditoria independente11controles/5smoke/3GTK no mesmo bundle sem rebuild,177 arquivos app/3684runtime/483ELF/297avisos e versões fonte conferidos. Desktop0.1.16 portal persistente/revogação/associação/atualização9/9 em cada uma de duas repetições novas, e Windows próprio5/5 em probe separado. [Estado e limites](../docs/EXECUCAO-SEM-VM.md). S11, famílias integrais,50S12 e19 critérios amplos continuam abertos. VM suspensa/intocada, nuvem direta adiada; percentual global desconhecido. Histórico abaixo.

Marco 2026-10-19T20:25:14-03:00: fonte e Flatpak **0.1.16/devel** aprovados em564/564 testes próprios por ambiente (fonte Linux,payload,sandbox instalado),490 IDs anteriores preservados e74 novos. Pacote publicado como [prerelease](https://github.com/airtonbp19edu/Linuxit-PDF/releases/tag/v0.1.16-devel); download completo e auditoria independente ainda em andamento. Portal/associação/atualização9/9 no pacote0.1.15 e Windows próprio5/5 em probes separados. Catálogo estático329(152REA+177diretas), seis entradas novas examinadas. VM suspensa/intocada; nuvem direta adiada. S11, famílias integrais,50S12 e19 critérios amplos continuam abertos; isso não é porcentagem global da reconstrução. Histórico abaixo.

Atualização 2026-10-19T15:28:46-03:00: Fonte0.1.16 em execução abrangente sem VM: [estado/contratos](../docs/EXECUCAO-SEM-VM.md), S01–S03 aprovados516/516 Linux na revisão5a4729e. S04 acrescenta edição cifrada preservando senhas/permissões, impressão da sessão/camadas e cancelamento CUPS;10 portáveis e regressões14+8 passaram, Linux/probe pendentes. Último Flatpak0.1.15 preservado. VM suspensa/intocada, nuvem direta adiada, famílias integrais e critérios intactos. Próximo S05 anexos/índice/idiomas enquanto CI S04 executa.

Entrega0.1.15 confirmada em2026-10-19T14:43:28-03:00: [lotes e pendências](../docs/LOTES-FUNCIONALIDADES.md),490/490 testes próprios por ambiente fonte/payload/sandbox. Auditoria do mesmo bundle sem rebuild aprovada:7controles/5smoke/3GTK,160 arquivos app e3414 de dependências conferidos,181 avisos/versões fonte. Download público HTTP200,58072096bytes/SHA256 confere. Publicação técnica d0d9bec; notas finais recebem commit próprio. Item23/nuvem direta adiado; famílias integrais e50S12 abertos, VM0930 suspensa e intocada. Não é conclusão global nem paridade. Histórico abaixo.

Atualização 2026-10-19T14:36:34-03:00: [lotes4–25 e entrega própria0.1.15](../docs/LOTES-FUNCIONALIDADES.md). **490/490 testes próprios por ambiente** fonte Linux/payload/Flatpak,0falhas/erros/skips;432 IDs preservados e58 novos. AT-SPI entre processos, portal real X11, voz WAV e camadas por pixels aprovados nos recortes sintéticos; nove telas examinadas. Pacote preparado, publicação/auditoria independente a confirmar. Item23/nuvem direta permanece adiado; VM0930 suspensa no relógio09:54:23 e intocada. Famílias completas/paridade0/25,50 aceitaçõesS12 e19 critérios amplos continuam abertos. Histórico abaixo.

Atualização 2026-10-19T14:19:59-03:00: [sequência dos25 itens em lotes](../docs/LOTES-FUNCIONALIDADES.md) percorrida com implementações próprias4–25, nuvem direta23 adiada. Fonte0.1.15 em validação consolidada; último pacote0.1.14 preservado. Lote13–15 passou465/465 Linux e19–21 teve CI aprovado (relatório a consolidar). Não é conclusão das famílias; VM suspensa, critérios/pesos/paridade intactos. Próximo: resultados/probes e entrega consolidada.

Atualização 2026-10-19T12:39:30-03:00: sequência dos25 itens em lotes de3 em [LOTES-FUNCIONALIDADES.md](../docs/LOTES-FUNCIONALIDADES.md). Lote4–6 implementado na fonte0.1.15,7 testes portáveis passaram/2 GTK pendentes; Linux ainda não validado. Nuvem direta23 permanece adiada por confirmação do usuário. Último pacote0.1.14 preservado; VM suspensa e critérios/paridade intactos.

Atualização 2026-10-19T12:12:33-03:00: [leitura, navegação e apresentação0.1.14](../docs/LEITURA-ABERTURA-NAVEGACAO-APRESENTACAO.md). **432/432 testes próprios por ambiente** fonte Linux/payload/Flatpak, sem falhas/erros/skips;14 portáveis e15 GTK novos. Pacote0.1.14/devel contém abertura transacional com senha/recuperação, zoom1–6400/viewport virtual e apresentação com seleção de monitor. Monitores físicos e comparação integral Foxit pendentes; usuário sem desktop Linux com duas telas. VM0930 permanece suspensa no relógio09:54:23. Não encerra famílias nem P01–P03; critérios/paridade intactos. Histórico abaixo.

Checkpoint 2026-10-19T09:58:26-03:00: [UI03/04 e nova parada da VM](../docs/P03-INTERFACE-E-PARADA-2026-10-19.md). Navegação1→2→3→8 e limites de zoom1%/6400% observados; FitPage47.15%. Relógio09:54:23 sem avanço entre capturas separadas por35.6s externos. Usuário confirmou travamento e encerrou por hoje. Entradas suspensas; sem rede/reboot/pause/kill/stop após constatação. Hostrunning/cabooff, janela Foxit visível; estado final de processos/coletor0930 e integridade pós-parada não confirmados. P03 parcial/bloqueada; não superar a parada automaticamente.13 métricas iguais/quatro inconclusivas e app/Flatpak/critérios intactos. Registros anteriores abaixo são históricos.

Atualização 2026-10-19T09:26:14-03:00: [D12 observado e novas saídas de impressão](../docs/P03-CANCELAMENTO-MOSAICO-2026-10-19.md). Stop ativo→232 resultados; troca mantém busca original; fechar aba ativa encerra→1738. N-up4mm comparado:13 métricas iguais/quatro inconclusivas no consolidado; mosaico200%/5mm gerou48 páginas. Foxit fechado normalmente, zero residual/fila, dez Inputs íntegros, cabooff. Coletor0113 Ready/result0 sem recibo end; novo observador/preflight antes de reabrir. P03 parcial, pronta para próximo lote; não há parada atual confirmada. App/Flatpak/critérios intactos. Registros anteriores abaixo são históricos.

Checkpoint 2026-10-19T01:08:44-03:00: [P03 suspensa pelo relógio](../docs/P03-PARADA-2026-10-19-0105.md). Busca ativa no corpus5000 observada; Stop enviado uma vez, efeito desconhecido. Relógio01:02:45 sem avanço e capturas iguais após10s externos. Nenhuma nova entrada, rede, reboot/pause/kill após constatação; hostrunning/cabooff, original/observador0048 sem estado final confirmado. P02 concluída, P03 parcial/bloqueada; não superar a parada automaticamente. Gerador próprio preservado em scripts/prepare_search_cancel_variant.py. Histórico abaixo.

Atualização 2026-10-19T00:36:40-03:00: [P03 busca/impressão parcial](../docs/P03-BUSCA-IMPRESSAO-2026-10-19.md). P02 concluída; P03 executou original offline com coletor2359 limitado. D07 seleção versus ativação1→2; D10 seis hits; D12 sem Stop ativo. N-up2/livreto4 páginas gerados, reabertos e renderizados, com parâmetros distintos de C18; comparação ainda aberta. UI05 par correto/No, UI02 sem documento; Foxit fechado sem residual identificado e tarefa2359 Ready/result0, cabooff e dez Inputs intactos. Não enviar comandos ao coletor encerrado; próximo RunId/preflight. Fila detalhada no relatório; critérios/pesos/app/pacote intactos. Registros anteriores abaixo são históricos.

Atualização 2026-10-18T23:56:42-03:00: [P02 validada offline](../docs/P02-COLETOR-VALIDADO-2026-10-18.md).
Coletor corrigido instalado com token interativo limitado; startup/pf/col/end
completos, dez Inputs/RX/isolamento conferidos e parada normal sem Foxit.
P03 pronta para novo observador e preflight/controle visual. Rede desligada.
P01 provisória preservada; registros anteriores abaixo são históricos.

Retomada mais recente: [controle de entrada da VM](../docs/VM-RETOMADA-2026-10-18-2336.md), em 2026-10-18T23:39:28-03:00.
Relógio23:36:09 sem avanço após10 segundos externos; duas capturas VBox idênticas.
P02 permanece bloqueada e P03 não iniciada; nenhuma entrada/deploy/rede/reboot.
P01 provisória preservada. Não superar a parada automaticamente. Registros
anteriores abaixo são históricos; estado em progresso/execucao-plano.json.

Estado de execução: [P01–P03](../docs/EXECUCAO-P01-P03-2026-10-18.md),
[catálogo111](inventario-operacoes-v1.json) e [estado por etapa](execucao-plano.json).
P01 concluída para inventário provisório; P02 bloqueada pelo relógio21:49:22,
P03 não iniciada. Restaurar resposta antes de deploy do coletor; manter regra
de não reiniciar/pausar automaticamente. Os19 critérios amplos continuam abertos.

Fila organizada: [plano P01–P10](../docs/PLANO-DE-CONTINUIDADE.md) e
[fonte estruturada](plano-continuidade.json). Toda pendência conhecida das 25
famílias e dos 19 critérios tem etapa, dependência, entrega e condição de conclusão.
Começar P01; sem VM, priorizar P06/B01 (combo editável) e P04 (estática dirigida).
Preparar contratos em P05 e validar recursos Linux disponíveis em P07/P09.
P02 antecede novas observações do original; manter a interrupção registrada.

Último checkpoint: [senha e parada da VM](../docs/VM-SENHA-E-PARADA-2026-10-18.md).
Relógio21:24:14 não avançou na confirmação após10 segundos; testes suspensos,
Foxit fechado/cabooff, sem reboot automático. Primeiro restaurar resposta e
validar coletor corrigido em RunId novo, com recibos curtos e contenção limitada.
D15 senha correta em abertura nova observado; não repetir como pendência.
UI05 duas abas com PDF protegido é variante extra; par planejado ainda aberto.
D20 fechou normalmente neste contexto, sem resolver a espera anterior de impressão.

Nova rodada offline2020: consulta exata D11 retornou zero e passou na comparação.
Consolidado12/12 medições iguais, cinco inconclusivas; onze preservadas/uma nova.
UI01 com documento/cancelar observado; destinos D07 ainda abertos. Ver
[relatório atual](../docs/VM-BUSCA-2026-10-18-2020.md). App/Flatpak intactos; não são famílias completas.

VM: [segundos habilitados e rodada posterior](../docs/VM-RELOGIO-SEGUNDOS.md).
UI01 sem documento/cancelar e D07 com dois marcadores observados; destinos
inconclusivos por resposta intermitente. `probe-stop:stop` da rodada vm-20261018-1940
confirmado completed em `followup.json`; coletor encerrado. Última coleta tinha
Foxit5280 com janela; manter offline e revalidar resposta visual antes de retomar.

Atualização posterior ao pacote: [busca por autor corrigida](../docs/BUSCA-AUTOR-COMENTARIOS.md) na fonte,
**403/403 testes Linux** e 11/11 medições iguais na comparação anterior.
Naquele marco havia cinco inconclusivos e um pendente; o consolidado atual está acima. O Flatpak 0.1.13 continua
anterior à correção, com 400/400 por ambiente no marco de entrega. Nenhum novo
pacote nesta rodada. D20: espera observada em splwow64.exe; causa aberta.

Fonte e Flatpak **0.1.13/devel**, com [anotações adicionais](../docs/ANOTACOES-AMPLIADAS.md):
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

[TIFF multipágina](../docs/TIFF-MULTIPAGINA.md), até 100 páginas na criação, e
[OCR local](../docs/OCR-LOCAL.md), até 20 páginas, preservados. Demais anotações,
formulários e famílias completas permanecem abertos. Pastas sincronizadas:
controles fora HOME negado/concedido passaram novamente; cliente real,
portal/concessão persistente, AT-SPI e impressão física ainda pendentes, sem VM Foxit.

Arquitetura: 44 módulos/58 interfaces; catálogo: 323 (152 REA + 171 diretas),
23 subconjuntos/duas propostas em 25 famílias. Índice histórico do checklist:
**45,13%**, 39 done/19 abertos. Conclusão global da recodificação indeterminada;
paridade **0/25**, cobertura global desconhecida. Original observado parcialmente na VM offline.
APIs de nuvem adiadas/IA excluída. Não reiniciar análises preservadas.

[Medição revisada](../docs/MEDICAO-PROGRESSO.md): os índices do checklist não quantificam as
funcionalidades implementadas. O índice só sobe ao fechar critérios por inteiro;
entregas parciais devem ser acompanhadas pelos recursos e evidências de cada versão.

VM: [primeira campanha offline de 18/10](../docs/VM-FOXIT-2026-10-18.md) observou o original com
perfil limitado, RX exercitado e hashes preservados. Dos17 recortes C18:
Na campanha inicial:11 comparados,10 iguais/1 divergente (autor). Na fonte
corrigida:11/11 métricas iguais;5 inconclusivos/1pendente preservados.
D01–D20:14 observados no recorte,5 parciais,1 inconclusivo; cancelamento, destinos
dos hits e saída de imposição abertos. D20 deixou processo sem janela; manter
rede desligada e investigar. Nenhuma proteção do host foi alterada.

Tabela histórica da entrega 0.1.13 (superada pela fila atual no topo):

| Frente | Próximo trabalho | Dependência |
|---|---|---|
|Entrega 0.1.13|Publicação e auditoria independente confirmadas; preservar evidências|Concluída neste marco, sem VM Foxit|
|Pastas sincronizadas|Portal real/concessão persistente e cliente externo, envio/conflitos/rede|Desktop Linux/cliente, sem VM Foxit|
|Operações locais|Priorizar combos AcroForm editáveis (texto livre/aparência); demais formulários/anotações, OCR e plataforma|Implementação própria sem VM|
|Estática|Tamanhos/alocação e chamadores dos arrays; provedor ativo/offsets restantes da busca; contexto0x138 e serviços de imagem; comportamento7911/7913|REA/Ghidra sem executar original|
|10 e parte dinâmica da 11|Completar variantes pendentes e UI01–UI10; investigar D20|VM offline operacional; campanha inicial preservada|
|18/19|Busca por autor corrigida na fonte posterior ao pacote0.1.13; validar e ampliar comparações; ver docs/BUSCA-AUTOR-COMENTARIOS.md|VM para novas observações; implementação/testes próprios no Linux|
|Desktop/AT-SPI/impressão|Portais, leitor de tela, impressora e Windows posterior|Ambientes/equipamentos próprios|
|Nuvem direta|APIs/login/upload/colaboração remota adiados|Nova priorização do usuário|

50 planos de aceitação completos `not_run`; D01–D20 com14 observados/5parciais/1inconclusivo. Dez de UI sem execução integral.
Pesos intactos; causa de tokens não confirmada/null. Preservar relatórios/corpus.
