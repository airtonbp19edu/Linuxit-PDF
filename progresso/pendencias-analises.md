# Pendências de análise e pontos de retomada

Revisão em **17/10/2026**, atualizada durante a continuação sem VM; os critérios da etapa13 foram preservados.
A [fonte estruturada](pendencias-analises.json) registra **todos os 21 critérios
não concluídos em 14 etapas**, cruzados com [progresso.json](progresso.json).
As frações abaixo medem somente critérios `done`; estados `partial`, `pending`,
`blocked` e `unknown` continuam distintos e não ganham peso por terem uma nota.

Em 17/10/2026, o usuário excluiu o assistente de IA e recursos generativos do
Foxit. Aplicar o [escopo autorizado](../docs/ESCOPO.md) a todos os próximos
alvos e contratos. Nenhuma das 25 famílias atuais foi removida ou concluída
por essa exclusão; pendências e pesos permanecem preservados.

## Causas e próximos passos

| Etapa | Fração verificada | Estado e próximo passo |
|---|---:|---|
|01|80%|Detalhes de regras/proteção recusados por API403 do plano; sem mudar segurança/faturamento.|
|03|50%|RTTI confirmou renderers/reflow e demais classes; fronteiras restantes ainda abertas.|
|05|42,9%|ImageRenderer eReflowViewer identificados; seguir recursos/slots e demais ciclos de vida.|
|07|33,3%|259 entradas(152REA+107diretas),sete métodos de layout novos na retomada; inventário global/tipos incompletos.|
|08|13,0%|Completar fluxo/algoritmos restantes e campos3/5/6/7/12/16/20 da busca; não repetir dez alvos desta continuação.|
|09|9,1%|Arestas de renderer/clip/reflow refinadas; algoritmos/tipos/ownership universais pendentes.|
|10|0%|VM/contenção offline e observaçãoD01–D20 ainda pendentes.|
|11|25%|CReflowViewerEx esclarece fábricaUI; IDs7911/7913 e demais contextos não resolvidos. UI01–UI10 exigem original.|
|12|12,5%|25 famílias,23 subconjuntos/duas propostas (nuvem adiada),50 planos completos not_run; referência original parcial.|
|15|33,3%|Segurança/texto acessível/CMS/edição em cópia na0.1.8,267/267 por ambiente; demais operações e duas propostas abertas.|
|16|33,3%|16 novos métodos GTK passaram; texto ATK/foco/cancelamento e UI de segurança/CMS/cópia. Desktop/portais/AT-SPI/impressora abertos.|
|18|10%|Corpus preservado17/17 repetido na0.1.7; zero comparações originais.|
|19|14,3%|Regressões próprias aprovadas; divergências Foxit ainda dependem de observação offline.|
|21|50%|Entrega 0.1.8 validada; publicação/auditoria nas notas.21 critérios amplos ainda abertos.|

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
Progresso geral **43,33%**, paridade **0/25**, catálogo **248** e pesos/revisão
permanecem preservados nesta revisão.


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
