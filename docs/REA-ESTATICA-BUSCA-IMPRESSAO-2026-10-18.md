# Busca, impressão e geometria — continuação estática de 18/10/2026

Foram examinadas **16 entradas adicionais distintas**, em três lotes novos,
com Ghidra 12.1.4, Temurin 21.0.12.1 e script de sementes do REA 6.5.0.
Perfil direto `-noanalysis`, em cópias sucessivas do projeto preservado;
não são novas observações MCP do REA. O executável original não foi executado.
Referência SHA-256:
`90208c9e8da92c8e546b76c8f4a2f8fb999105d124e663bbea6744fb6bb6b3a6`.

Capstone 5.0.6 e pefile 2024.8.26 conferiram **823 instruções/2.831 bytes**
nos corpos selecionados, com todos os endereços iguais às listagens Ghidra.
Isso verifica a decodificação, sem provar tipos, fronteiras universais ou
equivalência funcional. Corpos podem incluir auxiliares compartilhados por
salto; estes não são contados novamente como entradas.

O catálogo passa de 259 a **275 entradas: 152 REA + 123 diretas exclusivas**.
Alvos já catalogados foram descartados da nova fila. Não há denominador global
conhecido; a contagem não representa porcentagem de código reconstruído.

## Geometria e reflow: sete entradas

| Entrada | Bytes do corpo selecionado | Observação examinada |
|---|---:|---|
| `0x15cc510` | 5 | Retorna zero sem ler o receptor; não comprova posição variável. |
| `0x15cc520` | 209 | Índice negativo retorna zero. Demais índices acessam o array `this+0x48`; modos de contexto 0/2 usam caminho inteiro, os demais combinam métricas e escala. Há guarda superior e conversão final truncada. |
| `0x15ccd20` | 66 | Para operandos finitos, testa quatro limites superiores contra 2.147.483.647. Não testa limites inferiores nem validade completa de retângulo. |
| `0x15c9c60` | 34 | Converte inteiro de 32 bits com sinal para double e remove o sinal do resultado; retorno por x87. Unidades e contrato público não identificados. |
| `0x15cbc10` | 23 | Copia quatro palavras do objeto referenciado por `this+0x98`, nos offsets `+0x28/+0x2c/+0x30/+0x34`, para a saída. Tipo público da estrutura ainda desconhecido. |
| `0x15c7010` | 28 | Consulta slot virtual `+0x20`; se houver resultado, lê sua palavra `+0x10`, senão retorna zero. |
| `0x15c7100` | 28 | Mesma forma de consulta, lendo a palavra `+0x14`. Não foram demonstrados os tipos concretos dessas duas métricas. |

O dado em `0x531f9c0` é double **2.147.483.647**, conferido diretamente no PE.
A máscara em `0x6573ed0` contém duas palavras de 64 bits
`0x7fffffffffffffff`: remove o sinal de doubles. Interpretar esses bytes
isoladamente como NaN não descreve seu papel na operação de máscara.

No caminho escalado de `0x15cc520`, duas conversões passam por **float32 antes
de double**; outras duas vão diretamente de inteiro para double. O pseudocódigo
reduz essa diferença. Não substituir a sequência por aritmética real exata ao
descrever sua precisão. `CVTTSD2SI` faz a conversão final; guarda superior não
fecha o domínio inferior, overflow ou pré-condições dos chamadores.

O acesso ao array antecede uma checagem local de limite superior. Isso exige
rastrear os chamadores; não é, isoladamente, diagnóstico de vulnerabilidade.
As comparações `COMISD/JA/SETBE` também não devem ser transcritas como testes
genéricos `<=` para NaN sem examinar domínio e configuração de exceções.

## Busca: quatro entradas e um campo refinado

| Entrada | Bytes | Observação examinada |
|---|---:|---|
| `0x177fc50` | 292 | Chama slot `+0x58` do provedor. No ramo de retorno zero, guarda texto em `dialog+0x1e50`, inicializa `+0x1e54` e chama o parser abaixo. O assembly coloca 0 ou 9 em EAX; a assinatura `void` sugerida pelo Ghidra é incompleta. |
| `0x17323e0` | 375 | Compara quatro textos UTF-16 exatos: `1.0.0`, `1.1.0`, `1.2.0`, `1.3.0`. Quando reconhece, grava respectivamente 0/1/2/3 e retorna 1; outro texto retorna 0 sem escrever a saída. Não é um parser genérico de versões. |
| `0x1775e30` | 45 | Adaptador de argumentos variáveis para formatação; entrada nula leva ao helper com `0x80070057` e `INT3` no corpo selecionado. Não é uma transição do worker de busca. |
| `0x1775c70` | 433 | Usa `FormatMessageW`, `GetLastError/SetLastError` e `LocalFree`, com escrita em objeto de texto contado por referências. É formatação de texto, sem provar normalização, stemming ou interpretação da consulta. |

O chamador **já catalogado** `0x1783ac0` foi conferido em pontos delimitados,
sem ser somado como nova entrada. A chamada em `0x1783cee` testa EAX e abandona
esse caminho se ele não for zero. Em `0x1783d10`, copia `dialog+0x1e54` para
`EBP-0x68`: offset **`+0x14`** da estrutura de 24 bytes em `EBP-0x7c`.

Assim, esse campo recebe a enumeração de textos reconhecidos do provedor nesse
caminho. Ainda não se identifica isso como versão do formato PDF, versão do
produto instalado ou ABI pública. A classe do provedor e o significado visual
do código 9 continuam abertos. Os offsets `+3/+5/+6/+7/+0xc/+0x10` permanecem
sem significado completo; o controle de stemming não foi associado por palpite.

## Impressão: tipos, estado e ciclo de vida

| Entrada | Bytes | Observação examinada |
|---|---:|---|
| `0x1b5bbb0` | 8 | Testa a palavra de 32 bits `receiver+0x74 == 2`. No chamador preservado, o receptor vem de um elemento de coleção. Não comprova conclusão física da impressão. |
| `0x1b8a760` | 57 | Aloca `0xb8` bytes e chama `0x1b88120`, devolvendo ponteiro ou nulo por um objeto de saída. O chamador transfere esse ponteiro. |
| `0x1b88120` | 300 | Instala vtable `0x54151a0`; a cadeia MSVC RTTI identifica exatamente **CPDF_BackgroundDrawer**. Inicializa campos e três grupos compatíveis com transformação identidade, sem fechar o pipeline gráfico. |
| `0x1b88590` | 599 | Inicializa o contexto de `0x138` bytes usado no fluxo anterior, incluindo sentinela -1 em `+0x110`, byte 1 em `+0x114`, estado zerado e ponteiros nulos. Não instala diretamente uma vtable no corpo selecionado; sua classe ainda não foi identificada. |
| `0x1b88c60` | 329 | Caminhos distintos de limpeza: chamadas virtuais, flag `+0x11d` para o recurso `+0x120`, contador sem LOCK no objeto `+0xbc`, contadores com LOCK no controle `+0x6c` e finalização do membro `+0x40`. Inclui salto ao auxiliar compartilhado `0x1f0fae0`, sem contá-lo como outra entrada. |

RTTI liga `0x54151a0` ao locator `0x65ab368`, TypeDescriptor `0x6c9c940` e
nome `.?AVCPDF_BackgroundDrawer@@`. Esse auxiliar é distinto do contexto de
`0x138` bytes. Também não se deve unir campos `+0x74` de receptores diferentes
apenas porque os offsets coincidem. Ownership completo, estado do pipeline e
pré-condições de concorrência continuam parciais.

## Evidências, falhas e continuidade

- Geometria: [metadados](windows-evidence/foxit-rea/headless-cross-checks-static-geometry-state-2026-10-18.json), [máquina](../testes/resultados/static-geometry-state-2026-10-18/machine-checks.json) e [constantes/observações](../testes/resultados/static-geometry-state-2026-10-18/observations.json).
- Estado/ciclo de vida: [metadados](windows-evidence/foxit-rea/headless-cross-checks-static-search-print-state-2026-10-18.json), [máquina](../testes/resultados/static-search-print-state-2026-10-18/machine-checks.json) e [observações](../testes/resultados/static-search-print-state-2026-10-18/observations.json).
- Tipos/parser: [metadados](windows-evidence/foxit-rea/headless-cross-checks-static-search-print-types-2026-10-18.json), [máquina](../testes/resultados/static-search-print-types-2026-10-18/machine-checks.json) e [joins estruturais](../testes/resultados/static-search-print-types-2026-10-18/structural-joins.json).
- [Revisão agregada e identidade das ferramentas](../testes/resultados/static-analysis-2026-10-18/review.json).

Os três projetos e resultados completos ficam em `analysis-local/headless/`,
nas pastas com os nomes dos lotes, ignoradas pelo Git. Checkpoints foram salvos
após cada lote. O primeiro comando Capstone falhou por falta do import no PATH
Python padrão; usar `PYTHONPATH=analysis-local/python-deps` resolveu com as
dependências existentes, sem instalação nova. As três rodadas Ghidra terminaram.
Não houve timeout ou evidência de esgotamento de tokens nesta rodada.

Próximos alvos delimitados: `0x15cb590/0x15cb720/0x15cbb70/0x15cb8a0/0x15cb130`,
tipo do receptor `this+0x98` e seu slot `+0x20`; escritores e pré-condições dos
arrays. Na busca, classe do provedor `+0x58`, seis offsets ainda abertos e
contextos dos IDs 7911/7913. Na impressão, tipo do contexto de `0x138` bytes,
avanço `0x1b57340`, cursor `0x1b5a420` e consumidores do BackgroundDrawer.
Conferir novamente o catálogo antes de gerar sementes.

Nenhuma implementação Foxit foi transportada para o aplicativo. Fonte, versão
e Flatpak 0.1.9 foram preservados; testes GTK/Flatpak não foram repetidos.
Roteiro **43,33%**, paridade **0/25**, 21 critérios abertos e dependências de
VM foram mantidos. A observação dinâmica e a equivalência seguem pendentes.
