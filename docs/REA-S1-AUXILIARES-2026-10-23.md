# S1: comparador e auxiliares de vetores — continuação de 23/10/2026

Rodada direta `s1-followup-2026-10-23-1934`, em resposta à lista do Claude das 19:26 e à ordem humana de assumir a execução. Alvo `fxLuceneLib.dll`, SHA-256 `20908415a56a8bf63ad4500a2696e6da38a10191402a36b4d84fc577b61c82e1`. Ghidra 12.1.4, JDK21, `-noanalysis`, cópia de projeto anterior preservado; não é Evidence MCP REA, nem execução do original.

Quatro entradas conferidas independentemente por Capstone 5.0.6/pefile 2024.8.26: 128 instruções, 345 bytes. `0x10026740` já constava do catálogo via Claude: é revisita, não função nova. As outras três entradas acrescentam observações ao catálogo, de 516 para 519. Isso não mede cobertura global.

## Resultados e limites

* `0x10026740`: compara duas strings UTF-16. Comprimentos iguais seguem para igualdade; quando a candidata é maior, existem vias de busca de substring, comparação do sufixo por unidades de 16 bits e comparação de prefixo. A seleção depende de três argumentos escalares; o ramo do sufixo exige o segundo igual a 1, e o do prefixo exige segundo igual ao terceiro. Nomes públicos e semântica dos argumentos ainda não foram provados. Esse comparador **não demonstra uma fórmula de distância entre palavras**.
* `0x100322b0`: calcula `(fim - início) >> 2` sobre dois ponteiros de um contêiner. O valor retornado nessa via é contagem de elementos de quatro bytes. Não nomear esse retorno como limite de proximidade.
* `0x1001e530`: acessa a posição de um elemento como base acrescida do índice vezes quatro. Não fornece unidade textual ou significado público do índice.
* `0x1002d9b0`: inicializa um contêiner através de dois auxiliares e devolve o argumento recebido. Os tipos completos continuam provisórios.

As cópias das opções e os acessos aos vetores em `0x10024fc0`, `0x1001fa90` e `0x100280d0` foram consultados como contexto preservado. Não são novas decompilações nem prova de que o significado de cada offset foi concluído. O bloco de 24 bytes é copiado para endereços locais diferentes em cada função: um deslocamento da pilha não é automaticamente o mesmo offset do objeto de opções.

Continuam abertos +3/+0xc, regra e unidade final de +0x10, tabela integral de escapes/erros e exceções até a interface. S1 segue parcial; critérios, pesos e observações VM permanecem como estavam.

Evidências públicas: `testes/resultados/s1-followup-2026-10-23/machine-checks.json` e `docs/windows-evidence/foxit-rea/headless-cross-checks-s1-followup-2026-10-23.json`. Corpos e projeto completos permanecem fora do Git em `analysis-local/headless/s1-followup-2026-10-23-1934`.

## Segundo lote: consumidor concreto de +0xc e contexto dos offsets

Rodada `s1-option-consumers-2026-10-23-2010`: sete entradas, 67 instruções/158 bytes conferidos. Duas entradas de busca em conjuntos já constavam do catálogo e são revisitas. Cinco endereços acrescentam registros, sem aumentar um indicador funcional.

Em `0x100243b0`, a cópia das opções começa no local `EBP-0x40` (cópias em `0x10024423/0x10024433`). O inteiro `+0xc` está, portanto, em `EBP-0x34`. `0x10024692` compara esse local com o resultado de `0x100321f0`. Se forem diferentes, a via segue; se forem iguais, chama `0x1002e060` para consultar o conjunto e descarta o documento quando essa consulta é falsa. Há também o filtro independente `0x10032210`/`0x1002e0c0`.

Os corpos dos getters confirmam que `0x100321f0` e `0x10032210` retornam o campo `+4` de seus contêineres, obtidos pelos wrappers `0x1002aa80/0x1002aac0`. Não são getters do bloco de opções. A interpretação desse campo como contagem é compatível com o layout de conjunto observado; o fato forte é a leitura do campo e a condição de igualdade descrita acima. O nome público, a origem na UI e todos os valores válidos de `+0xc` ainda não foram demonstrados. O padrão `-1` sozinho não prova um domínio enumerado.

`0x1001a9f0` armazena quatro palavras consecutivas no contexto usado por `0x10024fc0`. A segunda é o ponteiro das opções, consistente com as leituras de `contexto[1]+6/+7` no filtro de offsets. O construtor não aplica uma transformação oculta a uma distância. Essa ligação não resolve a regra matemática do limite `+0x10`.

Evidências: `testes/resultados/s1-followup-2026-10-23/option-consumers-machine.json` e `docs/windows-evidence/foxit-rea/headless-cross-checks-s1-option-consumers-2026-10-23.json`. S1 permanece parcial; +3, distância/unidade e a tabela integral de escapes/erros continuam abertos.
