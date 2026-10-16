# Consumidores e geometria de impressão — 16/10/2026

Seis entradas pendentes foram descompiladas e examinadas com Ghidra direto
`-noanalysis`, usando o script de seeds do REA. O catálogo passou de **194 para
200 entradas distintas**: 152 REA e 48 exclusivas do backend complementar.
Os registros anteriores foram preservados. O progresso geral permanece em
**43,33%**, com paridade diferencial em **0/25 famílias**.

REA 6.5.0, Ghidra 12.1.4, Temurin JDK 21.0.12.1 e Node 24.22.0 foram
conferidos nesta rodada; os dez controles do provedor Ghidra passaram.
PeFile 2024.8.26 e Capstone 5.0.6, fixados nas dependências de análise do
projeto, foram preparados em `analysis-local/python-deps`, sem instalação
global. A disponibilidade do REA foi verificada pelo CLI; estas seis
observações são do backend direto, **não de uma sessão MCP do REA**.

## Resultados examinados

| Entrada | Corpo observado | Contrato parcial confirmado |
|---|---:|---|
| `0x1668750` | 867 bytes | Inicialização não negativa, últimos índices de coluna/linha, escala e ajustes com métricas físicas |
| `0x1667fe0` | 417 bytes | Obtenção/cache de limites, transformação pelo primeiro elemento e guarda de coleção vazia |
| `0x1655e00` | 953 bytes | Estado gráfico, cópia de transformação de 24 bytes, ajuste de translação e submissão |
| `0x16561c0` | 1.282 bytes | Preparação de fonte GDI, caminho alternativo em falha e submissão ao mesmo destino |
| `0x1665780` | 676 bytes | Enumeração de handlers, combinação de estados e escolha entre dois caminhos de saída |
| `0x166fe90` | 679 bytes | Lookup, preparação de transformação/opções e ciclo virtual de um objeto de saída |

Em `0x1668750`, a montagem confirma comparações **inteiras** com os últimos
índices de duas dimensões. O Ghidra tipou um desses slots como `float`, mas
o slot de pilha é reutilizado posteriormente. Essa assinatura não deve ser
copiada para uma implementação. As instruções também confirmam truncamento
para inteiro após escala, cálculo distinto na última posição e uso de papel
físico, offsets e DPI mapeados no marco anterior. O vínculo com a orientação
e os nomes visuais das flags ainda não estão fechados.

`0x1667fe0` lê quatro valores e um estado associado pelo objeto em `+0x5c`;
quando ausente, começa com zeros. Guarda os limites em `+0x44` e o estado em
`+0x54`. Depois usa o primeiro elemento da coleção para preparar uma
transformação e aplicá-la aos limites. A coleção vazia segue para diagnóstico
e `INT3`; isso é um caminho estático observado, não um erro reproduzido na UI.

Os consumidores `0x1655e00` e `0x16561c0`, chamados pelo produtor estudado no
marco anterior, convergem para `0x1b5baf0`. O primeiro copia seis palavras de
32 bits para uma transformação, ajusta em ponto flutuante seus dois termos
de translação e administra referências/temporários. O segundo chama
`CreateFontIndirectW`; no ramo de sucesso, libera o handle com `DeleteObject`.
Na falha de criação há um caminho alternativo ainda sem contrato visual
completo. O padrão `0x42480000` corresponde a float32 **50,0**, mas sua unidade
não foi identificada. A presença da API de fonte não basta para classificar
todos os elementos dessa coleção nem demonstrar reprodução visual equivalente.

`0x1665780` percorre uma coleção pelos slots virtuais `+0x64`/`+0x68`, chama
handlers em `+0x24` e interrompe a busca ao obter sucesso. O resultado se
combina com um byte de capacidade e os campos `+0x8c`/`+0x90` para escolher
`0x1665a30` ou `0x1664c00`. Os tipos concretos e os significados das flags
continuam pendentes; não se atribui ainda um nome raster/vetorial aos ramos.

`0x166fe90` verifica a entrada e o lookup, obtém um objeto por `0x2d226d0`,
inicializa seis valores com padrão de transformação identidade e prepara
opções condicionadas pelo campo `+0x70`, incluindo `0xffffff`. A montagem
confirma as chamadas virtuais `+4`, `+8`, `+0xc` e descarte. A classe e o
significado visual dessas opções ainda precisam ser determinados.

## Conferências e limitações

Os hashes do original antes/depois coincidem com a referência preservada.
O Ghidra salvou o novo projeto e terminou com sucesso. A conferência
independente pelo Capstone decodificou **1.484 instruções / 4.874 bytes**:
todos os endereços coincidem com as seis listagens examinadas. Isso verifica
a decodificação dos intervalos selecionados; não prova que as fronteiras,
assinaturas ou interpretações estejam completas. PeFile confirmou os dois
nomes de importação GDI diretamente na tabela PE.

Não houve execução funcional do Foxit, impressão física, comparação
diferencial, alteração de comportamento do Linuxit ou novo Flatpak. A etapa
10 continua bloqueada pelo ambiente isolado, conforme [ETAPA-10.md](ETAPA-10.md).

- [Identidade e diagnóstico das ferramentas](windows-evidence/foxit-rea/windows-followup-readiness.json).
- [Metadados das seis entradas](windows-evidence/foxit-rea/headless-cross-checks-windows-followup-2026-10-16.json).
- [Observações, endereços de suporte e conferência independente](windows-evidence/foxit-rea/windows-print-followup-contracts.json).
- [Verificações da rodada](../testes/resultados/rea-consumidores-windows-2026-10-16.json).
- [Notas com data e horário de São Paulo](../progresso/notas-continuidade.md).

Resultados completos e projeto: `analysis-local/headless/windows-print-02`.
Pseudocódigo, montagem e banco Ghidra não entram no Git. O gerador de metadados
aceita `--round windows-print-02`, verifica a identidade registrada e limita
a coleta à rodada indicada; os manifestos anteriores não são regravados.

Próximos alvos: `0x166d050`, `0x165f5d0`, `0x16678c0`, `0x16678d0`,
`0x16678e0`, `0x16678f0`, `0x1665a30`, `0x1664c00`, `0x2d226d0` e `0x1b5baf0`.
Completar seus tipos, arredondamento, opções e tratamento de falhas antes de
transportar contratos adicionais para código próprio. O fluxo integral de
impressão permanece parcial.
