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

| Etapa | Fração já verificada | O que falta e como retomar |
|---|---:|---|
| 01 — Diagnóstico | 80% | Acesso às regras remotas de proteção pela API continua desconhecido. Git push/ls-remote não prova essas regras. Não depende da VM. |
| 03 — Tecnologia | 50% | Análise estática das fronteiras do motor PDF e dos demais subsistemas; continuar consultas dirigidas em [FOXIT-REA.md](../docs/FOXIT-REA.md). |
| 05 — Dependências | 42,9% | Completar o ciclo de vida dos componentes no [grafo preservado](../docs/dependencias.md); análise estática ainda viável sem VM. |
| 07 — Catálogo | 33,3% | O universo relevante não está fechado. Expandir as 209 entradas examinadas sem contar slots como funções únicas; manter cobertura global desconhecida. |
| 08 — Descompilação | 13,0% | Busca e impressão parciais, demais famílias abertas. Seguir alvos de [impressão](../docs/REA-IMPRESSAO-CONSUMIDORES.md) e campos incompletos de [busca](../docs/REA-BUSCA-IMPRESSAO.md). Timeout de execução histórico não é esgotamento de tokens. |
| 09 — Fluxos | 9,1% | Completar arestas, estados, tipos e algoritmos a partir dos [fluxos parciais](../docs/fluxos.md); não conectar objetos sem prova. |
| 10 — Dinâmica | 0% | **Ambiente offline pendente**: Windows 11 Home local sem Sandbox, WSL ausente e VM ainda não disponibilizada, segundo o último diagnóstico/retorno do usuário. Validar VM ou contenção equivalente antes de executar o original; observar D01–D20. Kit pronto não é observação. |
| 11 — Interface | 25% | **VM para observar UI01–UI10**, além de trabalho estático: seguir `0x859920`, `0x687ae0`, `0x5f5370`, `0x48f10ef` e resolver contexto dos IDs 7911/7913. Ver [ETAPA-11.md](../docs/ETAPA-11.md). |
| 12 — Especificação | 12,5% | **VM para confirmar a referência**, além de corpus, subfunções, análises e critérios ainda incompletos. Os 50 cenários completos seguem planejados; especializar fixtures e executar primeiro os subconjuntos próprios. Ver [ETAPA-12.md](../docs/ETAPA-12.md). |
| 15 — Lógica | 33,3% | Backend de anexos planos implementado com 14 testes; critério abrangente `partial`. Integrar GUI no Linux e ampliar famílias por contratos suficientes; portfólios, /Kids e anexos por anotação pendentes. Ver [ETAPA-15.md](../docs/ETAPA-15.md). |
| 16 — Interface/integrações | 33,3% | Integrar funcionalidades implementadas e validar GUI/portais/plataformas em Linux adequado. GTK/Cairo ausentes no Windows atual; entrega Windows e impressão física também abertas. |
| 18 — Comparativos | 10% | **VM/contenção para executar o original**, corpus equivalente no Linuxit e relatório diferencial por família. Preparar fixtures/harness pode avançar antes da VM. |
| 19 — Incompatibilidades | 14,3% | **Resultados diferenciais dependentes do original** antes de medir/corrigir incompatibilidades. Regressões próprias corrigidas não substituem essa medição. |
| 21 — Auditoria final | 50% | Depende da implementação, análises e comparações ainda abertas, incluindo a VM. Auditar novamente as obrigações antes de declarar conclusão. |

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
Progresso geral **43,33%**, paridade **0/25**, catálogo **209** e pesos/revisão
permanecem preservados nesta revisão.
