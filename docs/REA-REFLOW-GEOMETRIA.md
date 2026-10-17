# Layout de reflow — cálculo de limites e predicado

Continuação estática de 17/10/2026, após os quatro acessores do
[lote anterior](REA-REFLOW-LAYOUT.md). Ghidra 12.1.4/Temurin 21,
perfil direto `-noanalysis`, sementes pelo script REA e Capstone 5.0.6/pefile.
Referência SHA-256
`90208c9e8da92c8e546b76c8f4a2f8fb999105d124e663bbea6744fb6bb6b3a6`.
Original não executado; não é evidência nova do MCP REA.

| Slot em `0x53d34bc` | Entrada | Bytes | Observação estática examinada |
|---|---|---:|---|
|`+0x04`|`0x15cc3b0`|339|Produz quatro inteiros de saída; índice negativo zera todos. Nos demais casos, consulta duas posições, ajusta pelos campos `this+4/+8` com um conversor auxiliar e compõe limites usando métricas do objeto em `this+0x98` e o double do contexto `+0x30`. Um predicado intermediário falso mantém a saída zerada.|
|`+0x08`|`0x15cc140`|622|Lê dois índices em arrays referidos por `this+0x48/+0x4c`, calcula quatro inteiros com posições e extensões escaladas, soma os campos `this+4/+8`; há ramos pelo estado do contexto (`+8`, valores 0/2), quantidade de linhas/colunas e primeiro/último elemento.|
|`+0x1c`|`0x15ccab0`|387|Predicado booleano sobre limites e posições escaladas, estado corrente em `this+0x20` e dimensões obtidas por helper. Converte `this+4/+8` para float e aplica máscara de sinal, combinando comparações de limites e igualdade do índice corrente.|

**Três entradas adicionais distintas, 1.348 bytes/412 instruções**, conferidas
contra Capstone por endereço e cobertura de bytes. Ponteiros dos três slots
conferidos diretamente no PE. A máscara em `0x6573ec0` contém quatro palavras
`0x7fffffff`; os ANDPS examinados removem o sinal do float convertido. Isso não
comprova domínio de entradas, tolerância numérica ou comportamento com NaN/overflow.

O catálogo chega a **259 entradas = 152 REA + 107 diretas exclusivas**.
Slots/associações não são contados como funções extras. Não há denominador global
ou prova de equivalência funcional. Os nomes numéricos são identidades, não nomes
de API recuperados do produto.

## Inferências e lacunas

A disposição de quatro inteiros e os pares posição/extensão sustentam a
**inferência** de limites geométricos. O consumo de `this+4/+8` nestes cálculos
refina a hipótese de deslocamentos dos acessores anteriores, mas não fecha
tipo/classe base, unidades, origem do sistema de coordenadas ou contrato público.
Não promover a estrutura de saída a RECT público sem rastrear seus consumidores.

No corpo `0x15cc140`, o índice é usado nos arrays antes de uma checagem local de
limites. O chamador pode impor uma pré-condição ainda não rastreada; não interpretar
essa ausência isolada como vulnerabilidade ou como autorização para copiar acesso
inseguro na implementação própria. Para `0x15cc3b0`, guarda negativa e saída
zerada são observações estáticas, não uma garantia sobre todo índice positivo.

O descompilador não tipou todos os receptores/argumentos. Por exemplo, chamadas
de métricas `0x15c7100/0x15c7010` usam ECX carregado de `this+0x98` no assembly;
não confiar apenas na assinatura reduzida sugerida no pseudocódigo. Os helpers
não foram examinados integralmente nem contados como novas funções nesta rodada.
Não há algoritmo completo de reflow nem disponibilidade da interface observada.

## Evidência e continuidade

[Sementes](windows-evidence/foxit-rea/reflow-layout-consumers-2026-10-17-seeds.tsv),
[metadados](windows-evidence/foxit-rea/headless-cross-checks-reflow-layout-consumers-2026-10-17.json),
[instruções](../testes/resultados/reflow-layout-consumers-2026-10-17/machine-checks.json),
[ponteiros e máscara](../testes/resultados/reflow-layout-consumers-2026-10-17/vtable-joins.json).
Projeto anterior copiado e preservado; resultados completos em
`analysis-local/headless/reflow-layout-consumers-2026-10-17/`, ignorado pelo Git.
Nenhum código ou recurso Foxit foi incorporado ao Linuxit PDF.

Próximos alvos: `0x15cc510/0x15cc520` (posições), `0x15ccd20` (predicado),
`0x15cbc10` (limites de contexto), `0x15c9c60` (conversor) e métricas sobre o
objeto `this+0x98`; escritores dos campos `+4/+8/+0x5c/+0x60` e pré-condições
dos índices continuam abertos. Conferir catálogo antes de criar lote novo;
não repetir os sete métodos de layout ou helpers de sincronização já examinados.
Busca, ownership, IDs 7911/7913 e demais famílias permanecem incompletos.
Roteiro 43,33% e paridade 0/25 preservados; causa de tokens não confirmada/null.
