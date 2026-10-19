# Transições de reflow —19/10/2026

Entrada original fixada por SHA256 `90208c9e8da92c8e546b76c8f4a2f8fb999105d124e663bbea6744fb6bb6b3a6`.
Ghidra12.1.4/JDK21, backend direto `-noanalysis`, script de sementes REA6.5.0.
Não é nova análise pelo MCP REA. O Foxit não foi executado e a VM não recebeu comandos.

As entradas0x15cd6e0 e0x15cc9b0 ainda não constavam do catálogo. Foram examinadas
com decompilador e instruções e conferidas contra os bytes do PE via
Capstone5.0.6/pefile2024.8.26:85instruções,268bytes,duas entradas distintas.
Catálogo passa de323 para325entradas:152REA e173diretas exclusivas. Não é
contagem de funcionalidades completas nem atribuição de tipos definitivos.

0x15cd6e0 transporta um argumento de oito bytes para o campo+0x30 do contexto
apontado por objeto+0x0c. MOVSD e consumidores prévios sustentam a interpretação
como valor escalar double; nome/semântica exata do campo continuam inferência.

0x15cc9b0 consulta os helpers de posição0x15cc510/0x15cc520 e escolhe três
ramos conforme flags+0x30/+0x2c. Um ramo usa limites do contexto e contagens
+0x54/+0x58; outro conserva deslocamentos float+0x34/+0x38; o terceiro combina
geometria e escalar do contexto. A constante referida em0x6573a20 tem bytes
`000000000000f0bf`,double−1.0:é inversão de sinal nesse recorte, sem evidência
de fator de centralização0.5. Ao final atualiza+0x30=1,+0x2c=0 e posições
inteiras+4/+8. Conversões, limites e convenção visual não são paridade observada.

Resultados completos/projeto local ignorados:
`analysis-local/headless/static-reflow-transitions-2026-10-19/`.
[Metadados](windows-evidence/foxit-rea/headless-cross-checks-static-reflow-transitions-2026-10-19.json),
[sementes](windows-evidence/foxit-rea/static-reflow-transitions-2026-10-19-seeds.tsv),
[conferência de máquina](../testes/resultados/static-reflow-transitions-2026-10-19/machine-checks.json).
Nenhum código descompilado foi incorporado à implementação ou versionado.

Próximos recortes estáticos continuam abertos:alocação/tamanhos/propriedade dos
cinco arrays e todos os chamadores; atribuição ativa de dialog+0x1e48; campos
restantes/algoritmo de busca e contexto0x138/serviços de imagem/concorrência.
As duas transições deste relatório não devem ser repetidas como novas entradas.
