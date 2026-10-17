# Pendências de análise e pontos de retomada

Revisão em **17/10/2026**, solicitada pelo usuário ao avançar a etapa 13.
A [fonte estruturada](pendencias-analises.json) registra **todos os 21 critérios
não concluídos em 14 etapas**, cruzados com [progresso.json](progresso.json).
As frações abaixo medem somente critérios `done`; estados `partial`, `pending`,
`blocked` e `unknown` continuam distintos e não ganham peso por terem uma nota.

Em 17/10/2026, o usuário excluiu o assistente de IA e recursos generativos do
Foxit. Aplicar o [escopo autorizado](../docs/ESCOPO.md) a todos os próximos
alvos e contratos. Nenhuma das 25 famílias atuais foi removida ou concluída
por essa exclusão; pendências e pesos permanecem preservados.

## Causas e próximos passos

| Etapa | Fração verificada | Estado atual e próximo passo |
|---|---:|---|
| 01 — Diagnóstico | 80% | Detalhes de proteção/regras recusados por API403 do plano; metadado main protected=false. Sem alteração de segurança/faturamento. |
| 03 — Tecnologia | 50% | RTTI confirmou três classes ligadas às vtables e candidatos CPDF parser/segurança. Restantes fronteiras/subsistemas ainda abertos. |
| 05 — Dependências | 42,9% | Configuração compartilhada/referências examinadas; seguir1b8a7a0/1b8ae20 para fábrica/finalização auxiliar. Ciclos de vida restantes não fechados. |
| 07 — Catálogo | 33,3% |240 entradas (152 REA+88 diretas);31 novas neste pedido. Universo relevante/tipos ainda abertos, cobertura global indeterminada. |
| 08 — Descompilação | 13,0% | Quatro lotes novos examinados. Seguir16664e0, demais render/saída e campos3/5/6/7/12/16/20 da busca. Não repetir lotes concluídos. |
| 09 — Fluxos | 9,1% | Estados/continuação/recursos refinados, sem fechamento universal. Completar arestas, tipos, algoritmos e ownership com provas. |
| 10 — Dinâmica | 0% | VM/contenção offline pendente; original não observado. Kit/cenáriosD01–D20 preparados permanecem not_run. |
| 11 — Interface | 25% | Alvos antigos e880490 examinados; seguir15c6550/872f20, identificar classe/IDs7911/7913. ObservarUI01–UI10 no guest. |
| 12 — Especificação | 12,5% |25 famílias/16 subconjuntos/nove propostas.50 planos completos not_run. Ampliar contratos/fixtures próprios sem VM; confirmar referência na contenção. |
| 15 — Lógica | 33,3% | Anexos Kids/anotações e cópias com marcador/nota/Tx em 0.1.5;152/152 por ambiente. Expandir demais operações/famílias, portfólios/senha conforme contrato. |
| 16 — Interface | 33,3% | Seis métodos GTK de anexos, cinco novos de cópia e layout aprovados no X11 virtual. Desktop/portal/AT-SPI/impressora e demais interações abertos. |
| 18 — Comparativos | 10% |17/17 subconjuntos próprios no corpus/protocolos preservados, repetidos na0.1.5; Poppler resolvido. Zero comparações originais; requer VM offline. |
| 19 — Incompatibilidades | 14,3% | Regressões próprias de CropBox/memória/GTK/layout aprovadas na0.1.5. Divergências Foxit só após observar original. |
| 21 — Auditoria final | 50% | Entrega 0.1.5 validada; confirmar publicação/auditoria nas notas.21 critérios amplos abertos, incluindo trabalho ainda viável sem VM. |

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
Progresso geral **43,33%**, paridade **0/25**, catálogo **240** e pesos/revisão
permanecem preservados nesta revisão.
