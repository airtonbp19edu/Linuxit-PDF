# Alocação dos arrays de reflow —19/10/2026

**Continuação de23/10/2026:** [S4 — consumidores e extensões](REA-S4-REFLOW-2026-10-23.md)
liga os arrays a escala, posição e limites. O helper final copiado para+0x68 recebe
quatro zeros nessa via; a referência a retângulo abaixo não significa bounds calculados
das páginas. A=1/B=N e a escrita condicional dos mapas foram refinados, mantendo
abertos unidades físicas, domínio integral de índices e todos os caminhos de falha.

Mesmo original e perfil fixados no relatório de transições. A varredura local
Capstone de0x15c9c90..0x15cdfff localizou atribuições a+0x3c/+0x40/+0x44/+0x48/+0x4c.
Isso é levantamento de candidatos, não análise global de todos os chamadores.
O construtor0x15c9c90 já estava preservado:foi relido, sem contá-lo como nova entrada.
Ele aloca48/4c em4Nbytes,N obtido do getter virtual+0x1c do viewer,e zera os
ponteiros3c/40/44. Multiplicações de alocação usam saturação para0xffffffff quando
o produto excede32bits; resposta do alocador/exceções não foi observada dinamicamente.

Dois métodos novos0x15cd760/0x15cd860 foram examinados no Ghidra e conferidos
com Capstone:177instruções/525bytes. O projeto anterior foi copiado,preservado;
não houve nova importação do original nem execução do Foxit. Catálogo327entradas
(152REA+175diretas),incluindo as duas transições da rodada anterior de hoje.

0x15cd760 consulta novamente N,atualiza+0x78 e,quando mudou,libera e realoca os
arrays48/4c em4Nbytes. Ao terminar marca+0x50=1. Inicialização de todos os
elementos e domínio dos índices ainda dependem dos demais escritores/chamadores.

0x15cd860 obtém contagens A/B de15cb840/15cbb90 e grava+0x54/+0x58.
Libera/recria3c em4Bbytes,40 em4Abytes e44 em4(B+1)bytes;zera essas regiões.
Para os N itens usa os mapas48/4c para agregar máximos das métricas de página
em3c/40. Depois constrói somas prefixadas em44 com44[0]=0 e B incrementos.
Marca+0x50=0 e copia um retângulo para+0x68..+0x74.

As leituras e chamadas sustentam papéis de grupos/eixos; nomes finais,todas as
unidades,overflow da soma B+1 e segurança de todos os índices não foram provados.
Não declarar erro do Foxit com base nesses recortes estáticos ou no pseudocódigo.
Tipos/ownership,callbacks,concorrência e o universo de chamadas continuam abertos.

[Metadados](windows-evidence/foxit-rea/headless-cross-checks-static-reflow-arrays-2026-10-19.json),
[sementes](windows-evidence/foxit-rea/static-reflow-arrays-2026-10-19-seeds.tsv),
[conferência](../testes/resultados/static-reflow-arrays-2026-10-19/machine-checks.json).
Raw completo/projeto ficam emanalysis-local/headless/static-reflow-arrays-2026-10-19/,
ignorados pelo Git. Nenhum pseudocódigo ou recurso original foi incorporado ao app.
