# Layout de reflow — quatro acessores examinados

Continuação estática em 17/10/2026, após os helpers de sincronização.
Ghidra 12.1.4, Temurin 21, backend direto `-noanalysis` e seed script REA;
não é nova evidência do MCP REA. Referência fixada pelo SHA-256
`90208c9e8da92c8e546b76c8f4a2f8fb999105d124e663bbea6744fb6bb6b3a6`.
Nenhuma execução do original ou incorporação de código/recursos à aplicação.

O construtor e RTTI já examinados ligam a tabela `0x53d34bc` a
`CReflowViewerLayout`. Nesta rodada foram conferidos os quatro ponteiros PE
abaixo, suas funções de entrada e a correspondência Ghidra/Capstone.

| Slot relativo à tabela | Entrada única | Bytes | Conclusão limitada |
|---|---|---:|---|
|`+0x0c`|`0x15cbc70`|4|Retorna o campo de 32 bits em `this+0x5c`.|
|`+0x10`|`0x15cbc60`|4|Retorna o campo de 32 bits em `this+0x60`.|
|`+0x14`|`0x15cc600`|6|Lê o campo de 32 bits em `this+4` e aplica negação x86.|
|`+0x18`|`0x15cc610`|6|Lê o campo de 32 bits em `this+8` e aplica negação x86.|

**Quatro entradas adicionais distintas, 20 bytes e dez instruções**; catálogo
**256 = 152 REA + 104 adicionais diretas exclusivas**. Ponteiros/slots são
associações estruturais e não unidades extras de função. Não há denominador
global conhecido, percentual de código recuperado ou paridade comprovada.

Os campos continuam sem tipo/semântica completos. Não os nomear largura,
altura, origem, margem ou escala sem rastrear consumidores e escritores.
Em particular, a negação x86 descreve o valor de 32 bits, sem provar domínio
matemático/geometria ou tratamento de overflow. Não foi observado despacho
virtual em execução, disponibilidade da UI ou algoritmo integral de reflow.

Projeto anterior foi copiado, preservando-o, para
`analysis-local/headless/reflow-layout-2026-10-17/`. Respostas integrais,
pseudocódigo, assembly e projeto permanecem ignorados pelo Git.

[Sementes](windows-evidence/foxit-rea/reflow-layout-2026-10-17-seeds.tsv),
[metadados da rodada](windows-evidence/foxit-rea/headless-cross-checks-reflow-layout-2026-10-17.json),
[checagem de máquina](../testes/resultados/reflow-layout-2026-10-17/machine-checks.json),
[ponteiros PE](../testes/resultados/reflow-layout-2026-10-17/vtable-joins.json).

Próximos alvos: consumidores/escritores destes campos; slots não examinados
`+0x04/+0x08/+0x1c` da mesma tabela (`0x15cc3b0`, `0x15cc140`, `0x15ccab0`).
Ownership/tipos, campos da busca 3/5/6/7/12/16/20 e IDs 7911/7913 continuam
abertos. Não repetir os quatro acessores nem os helpers Enter/Leave já examinados.
Pesos, critérios, 43,33% do roteiro e paridade 0/25 permanecem preservados.
