# Pendências de análise e pontos de retomada

Atualização 2026-10-19T20:35:22.468299-03:00: [entrega e contratos próprios0.1.16](../docs/EXECUCAO-SEM-VM.md),564/564 por ambiente e auditoria independente11controles/5smoke/3GTK sem rebuild. Desktop0.1.16 passou9/9 em cada uma de duas repetições novas, após correção da sequência FUSE do probe. Source/app/bundle preservados durante a auditoria; VM intocada. S11, famílias completas,50S12 e19 critérios amplos continuam abertos; nuvem direta adiada. Histórico abaixo.

Atualização 2026-10-19T14:43:28-03:00: [entrega própria0.1.15/lotes](../docs/LOTES-FUNCIONALIDADES.md),490/490 por ambiente e auditoria instalada aprovada. Os19 critérios amplos permanecem abertos, sem mudança de pesos. VM suspensa no checkpoint09:54:23; nenhuma inspeção/entrada nova. Os estados anteriores abaixo são históricos.

Atualização 2026-10-18T23:56:42-03:00: [P02 validada offline](../docs/P02-COLETOR-VALIDADO-2026-10-18.md).
Coletor corrigido instalado com token interativo limitado; startup/pf/col/end
completos, dez Inputs/RX/isolamento conferidos e parada normal sem Foxit.
P03 pronta para novo observador e preflight/controle visual. Rede desligada.
P01 provisória preservada; registros anteriores abaixo são históricos.

P01 do plano executada no recorte provisório de111 operações/25 famílias,
com matriz/contratos reconciliados. [Execução P01–P03](../docs/EXECUCAO-P01-P03-2026-10-18.md):
controle do relógio21:49:22 falhou após10 segundos externos; P02 bloqueada e
P03 não iniciada. Nenhum status/peso de critério antigo alterado.

Execução organizada no [plano P01–P10](../docs/PLANO-DE-CONTINUIDADE.md).
[Mapeamento estruturado](plano-continuidade.json) cobre exatamente os 19 critérios
abaixo e as 25 famílias. Nenhum status/peso foi alterado pelo planejamento.

Continuação mais recente: [senha e parada](../docs/VM-SENHA-E-PARADA-2026-10-18.md).
Relógio21:24:14 sem avanço após dez segundos externos: testes suspensos, Foxit
já fechado/cabooff. Primeiro restabelecer resposta e integrar coletor corrigido
em RunId novo/IDs curtos. D15 correto em abertura nova observado; UI05 extra
parcial e D20 sem residual neste contexto não encerram os contratos amplos.
Consolidado C18 atual12 iguais/cinco inconclusivos, com11 medições preservadas
euma nova D11. Os19 critérios e pesos abaixo continuam iguais.

Estado atualizado em **18/10/2026** após a campanha inicial na VM offline; os critérios da etapa 13
e os pesos foram preservados. A suíte própria atual passou 400/400 em fonte,
payload e sandbox. As análises estáticas anteriores não foram reiniciadas.
[A revisão da medição](../docs/MEDICAO-PROGRESSO.md) separa o índice histórico
45,13% da conclusão global da recodificação, cujo percentual é indeterminado.
O índice não atribui pontos aos avanços dentro de critérios ainda parciais.
A [fonte estruturada](pendencias-analises.json) registra **todos os 19 critérios
não concluídos em 13 etapas**, cruzados com [progresso.json](progresso.json).
As frações abaixo medem somente critérios `done`; estados `partial`, `pending`,
`blocked` e `unknown` continuam distintos e não ganham peso por terem uma nota.

Em 17/10/2026, o usuário excluiu o assistente de IA e recursos generativos do
Foxit. Aplicar o [escopo autorizado](../docs/ESCOPO.md) a todos os próximos
alvos e contratos. Nenhuma das 25 famílias atuais foi removida ou concluída
por essa exclusão; pendências e pesos permanecem preservados.

## Causas e próximos passos

| Etapa | Fração verificada | Estado e próximo passo |
|---|---:|---|
|01|100%|API agora consultável: regras/rulesets200 vazios e main sem proteção; configurações preservadas.|
|03|50%|RTTI de CPDF_BackgroundDrawer e ligações de busca/reflow refinadas; contexto0x138 e fronteiras restantes abertas.|
|05|42,9%|Limpeza separa chamadas virtuais, recursos condicionais e contadores com/sem LOCK; ownership e contextos completos abertos.|
|07|33,3%|323 entradas (152 REA+171 diretas); 48 novas em oito lotes. Inventário global e tipos completos desconhecidos.|
|08|13,0%|Busca+0x14 ligada a enum e+5 a stemming efetivo; offsets3/6/7/0xc/0x10 ainda parciais. Geometria/tipos/algoritmos completos pendentes.|
|09|9,1%|Novo fluxo rastreável de texto/enum/argumento de busca e contratos geométricos; algoritmos e ownership universais pendentes.|
|10|20%|Ambiente offline/original executável validados. Campanha14observados/5parciais/1inconclusivo; variantes restantes abertas.|
|11|25%|CFindToolDlgAdv e tabela7911/7913 ligados; handler comum e DDX distintos mantêm ambiguidade. UI01–UI10 exigem original.|
|12|12,5%|25 famílias,23 subconjuntos/duas propostas (nuvem adiada),50 planos completos not_run; referência original parcial.|
|15|33,3%|0.1.13: cinco tipos de anotação e comentário/autor ampliados, com TIFF/OCR anteriores;400/400 por ambiente. Famílias completas, operações restantes e duas propostas abertas.|
|16|33,3%|Seis métodos GTK novos de anotações na0.1.13 e anteriores preservados. Desktop/portais/AT-SPI/impressora abertos.|
|18|10%|17/17 próprios preservados; consolidado12 medições iguais (11 preservadas/uma nova D11),5 inconclusivas. Famílias completas abertas.|
|19|14,3%|Autor corrigido na fonte:Foxit1/Linuxit1;403/403 testes Linux. Outros protocolos/operações e famílias abertas; pacote0.1.13 anterior.|
|21|50%|Entrega 0.1.13 validada; publicação/auditoria nas notas. 19 critérios amplos ainda abertos.|

A etapa **13 tem seus dois critérios de projeto verificados (100%)** e não é
parcial por falta de VM. Isso não fecha a fase A, a implementação nem a paridade.
As etapas 02/04/06/14/17/20 também mantêm os critérios atuais concluídos;
resultados históricos não foram apresentados como novas execuções nesta revisão.

## Limites efetivamente registrados

| Evento documentado | Evidência | Significado para a retomada |
|---|---|---|
| `provider_timeout` em 1.801,7 s, limite 1.800 s | [FOXIT-REA.md](../docs/FOXIT-REA.md) | Autoanálise completa não concluída. Perfis dirigidos posteriores produziram resultados examinados e preservados; continuar deles. |
| Análise automática em 600 s e `cleanup_incomplete` | [REA-IMPRESSAO-WINDOWS.md](../docs/REA-IMPRESSAO-WINDOWS.md) | Tentativa MCP produziu zero novas observações. Resultados posteriores Ghidra direto `-noanalysis` têm proveniência própria e não devem ser repetidos/contados como MCP. |
| Possível interrupção futura por tokens/contexto | Risco de continuidade solicitado pelo usuário; causa não confirmada nas evidências examinadas | Manter o trabalho restante parcial/pendente e salvar o ponto exato de retomada. Não atribuir automaticamente os timeouts nem todas as lacunas a tokens. |

Não foi encontrado registro de esgotamento de tokens nos relatórios de projeto
e notas consultados. O campo correspondente permanece `null` em cada pendência;
a lista de eventos confirmados está vazia. Isso não afirma que chats perdidos
tenham tido ou deixado de ter esse problema.

## Checkpoint ao concluir um lote ou interromper uma análise

Acrescentar uma nota em [notas-continuidade.md](notas-continuidade.md) após cada
lote delimitado de alvos e antes de trocar de etapa. Usar o horário real de
São Paulo e conservar os resultados completos em `analysis-local/`.

```text
AAAA/MM/DD às HH:mm (America/Sao_Paulo, UTC-03:00)
Etapa/família e identidade/hash do original:
Ferramenta, versão, perfil e pasta da rodada:
Alvos iniciados / efetivamente examinados / pendentes:
Último resultado conferido e seus limites:
Evidências completas locais / metadados publicáveis:
Próximo comando ou ação e condição para prosseguir:
Causa de interrupção: evento comprovado ou null; risco de tokens separado:
Verificações feitas e não realizadas:
Estado Git, commit e confirmação remota ou bloqueio:
```

Uma saída salva ainda não examinada continua sem crédito de conclusão.
Após interrupção, conferir manifesto/checkpoint, identidade e árvore Git;
retomar no primeiro alvo pendente e preservar os anteriores. Uma nova IA não
precisa refazer a análise inicial nem supor resultados ausentes.

Conferir coerência do registro com `python scripts/check_architecture.py`.
Registro histórico do checkpoint inicial: índice **43,33%**, paridade **0/25**,
catálogo **248** e pesos/revisão então preservados. Não descreve os totais atuais.


Retomada 2026-10-17T20:17:24-03:00: conferir publicação/auditoria nas notas.
[Quatro acessores de reflow](../docs/REA-REFLOW-LAYOUT.md) examinados; não
repetir estes nem os helpers de sincronização. Nuvem adiada explicitamente.


## Marco0.1.9: pastas sincronizadas

Fluxo local autorizado e implementado; APIs de provedores continuam adiadas.
Fonte/payload/sandbox290/290 aprovados, dois controles de concessão fora HOME.
Portal real e sincronizador real exigem desktop/cliente, sem VM Foxit.
A referência10/dinâmica11/comparações18/19 exige original em contenção offline.
[Tabela de dependências](../docs/PASTAS-SINCRONIZADAS.md). Publicação/auditoria
nas notas;23subconjuntos/2propostas e pesos preservados.


## Continuação estática de 18/10/2026

[Relatório](../docs/REA-ESTATICA-BUSCA-IMPRESSAO-2026-10-18.md): 16 novas entradas examinadas em três lotes,
823 instruções/2.831 bytes conferidos; checkpoints privados preservados.
Catálogo 275, sem mudar pesos, estados dos critérios ou paridade.
Próximos alvos: helpers 15cb590/15cb720/15cbb70/15cb8a0/15cb130, métricas
this+98/slot+20, pré-condições e escritores de arrays; provedor de busca+58,
seis offsets e contexto IDs7911/7913; contexto0x138, 1b57340/1b5a420 e
consumidores BackgroundDrawer. Original, desktop e impressão não executados.


## Continuação da fila estática — 18/10/2026

[Relatório](../docs/REA-ESTATICA-CONTINUACAO-2026-10-18.md):48 novas entradas em oito lotes;6.830 instruções/25.919 bytes selecionados conferidos.
Catálogo323=152REA+171diretas. Tipos viewer/página/diálogo, stemming efetivo,
interface de índice, escritores de estado/arrays e ciclo de vida refinados.
Algoritmos grandes, limites/ownership e comportamento original permanecem parciais.
A fila da nota anterior foi examinada; os novos recortes estão no relatório.
Roteiro43,33%,21 critérios em14 etapas e paridade0/25 preservados.


## Leitura remota resolvida em18/10/2026

Critério de consulta da etapa1 verificado após repositório público:HTTP200
para regras/rulesets, ambos vazios; mainprotected=false. Nenhuma configuração
alterada. [Evidência](../docs/REGRAS-REMOTAS-2026-10-18.md). Roteiro43,93%,
38done/20abertos em13etapas; paridade0/25. Pesos e definições intactos.
