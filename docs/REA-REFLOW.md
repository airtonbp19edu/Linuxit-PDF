# Recursos auxiliares de reflow — 17/10/2026

Continuação dos alvos apontados em [BUSCA-COLECOES.md](BUSCA-COLECOES.md).
Ghidra 12.1.4/JDK 21, backend direto `-noanalysis`, script de seeds do REA;
não é evidência nova do MCP REA e não houve execução do original. SHA-256
fixado em `progresso/projeto.json`. Projeto anterior copiado, sem modificá-lo:
`analysis-local/headless/no-vm-context-2026-10-17/project`.

As duas entradas foram descompiladas e examinadas, com **111 instruções/467
bytes** conferidos contra Capstone 5.0.6/pefile 2024.8.26. O catálogo passa de
248 a **250 entradas distintas: 152 REA + 98 adicionais diretas**. O universo
global permanece desconhecido; isso não é porcentagem de recodificação.

| Entrada | Bytes | Resultado limitado |
|---|---:|---|
| `0x15c5e00` | 57 | Obtém objeto pelo slot virtual zero da referência em `this+0x6c`, lê o campo `+0x8c` entre chamadas pareadas a `0x1f21a80`/`0x1f21ac0`, sobre contexto `+0xb8`. Há transferência para auxiliar compartilhado em `0x1b64ed0`; esse corpo não é contado como outra função única. A hipótese de sincronização ainda requer examinar os helpers. |
| `0x15c9c90` | 410 | Construtor inicializa estados e instala vtables base `0x53d2f74` e derivada `0x53d34bc`. RTTI liga-as exatamente a `IPDFViewerLayout` e `CReflowViewerLayout`. Consulta contagem por slot virtual `+0x1c` da entrada de contexto e prepara dois buffers de quatro bytes por elemento, com teste de overflow. Sem prova dos tipos/ownership completos dos buffers ou da disponibilidade do reflow na UI. |

O construtor `0x15c5010` de `CReflowViewerEx`, examinado anteriormente, chama
essas entradas. O novo join distingue viewer e layout de reflow, sem atribuir
todos os getters da UI a essa classe. Assinaturas inferidas pelo descompilador
permanecem provisórias, especialmente convenções/argumentos não tipados.
Não há recuperação de algoritmo completo de paginação ou comportamento Foxit.

[Metadados por rodada](windows-evidence/foxit-rea/headless-cross-checks-reflow-resources-2026-10-17.json),
[seeds](windows-evidence/foxit-rea/reflow-resources-2026-10-17-seeds.tsv),
[checagem de máquina](../testes/resultados/reflow-resources-2026-10-17/machine-checks.json)
e [RTTI](../testes/resultados/reflow-resources-2026-10-17/rtti.json).
Resultados completos, assembly, pseudocódigo e projeto somente em
`analysis-local/headless/reflow-resources-2026-10-17/`, ignorado pelo Git.
Nenhum código/recurso Foxit foi incorporado à aplicação.

Próximos alvos: helpers `0x1f21a80`/`0x1f21ac0` e slots relevantes de
`CReflowViewerLayout`/`CPDF_ImageRenderer`; campos 3/5/6/7/12/16/20 da busca
e IDs 7911/7913 seguem abertos. Pesos, critérios, paridade 0/25 e dependências
da VM não mudaram. Sem evidência de esgotamento de tokens nesta rodada.
