# Continuação estática — busca, impressão, reflow e estados

Foram examinadas **48 entradas adicionais** em oito lotes preservados: 43 no
executável e cinco em `fxLuceneLib.dll`. Ghidra 12.1.4, Temurin 21.0.12.1 e o
script de sementes do REA 6.5.0 trabalharam em perfil direto `-noanalysis`.
Não houve nova observação MCP do REA nem execução do Foxit ou da DLL.

Capstone 5.0.6 e pefile 2024.8.26 conferiram **6.830 instruções e 25.919 bytes**
dos corpos selecionados. O catálogo passa de 275 a **323 entradas distintas**:
152 provenientes do REA e 171 diretas exclusivas. As 275 linhas anteriores
permaneceram idênticas. Slots e auxiliares por salto não foram somados como
funções únicas. O denominador global continua desconhecido.

| Lote de 18/10/2026 | Entradas | Instruções | Bytes selecionados |
|---|---:|---:|---:|
| static-remaining-core | 8 | 140 | 460 |
| static-remaining-context | 11 | 1.697 | 5.243 |
| static-index-options | 5 | 2.454 | 9.355 |
| static-reflow-preconditions | 9 | 392 | 1.417 |
| static-ui-contexts | 5 | 1.289 | 6.052 |
| static-reflow-writers | 5 | 179 | 585 |
| static-reflow-builders | 3 | 669 | 2.778 |
| static-dispatch-links | 2 | 10 | 29 |

Os resultados completos, pseudocódigo e projetos permanecem fora do Git, em
`analysis-local/headless/<lote>-2026-10-18/`. Sementes e metadados estão em
`docs/windows-evidence/foxit-rea/`; cada lote tem `machine-checks.json` em
`testes/resultados/<lote>-2026-10-18/`. A [revisão agregada](../testes/resultados/static-remaining-2026-10-18/review.json)
vincula as evidências por SHA-256. A rodada anterior de 16 entradas foi preservada.

## Identidades e ferramentas

- Executável: `90208c9e8da92c8e546b76c8f4a2f8fb999105d124e663bbea6744fb6bb6b3a6`.
- DLL de indexação: `20908415a56a8bf63ad4500a2696e6da38a10191402a36b4d84fc577b61c82e1`.

Os quatro scripts de análise/catalogação agora aceitam sujeitos do inventário
fixado, mantendo o executável como padrão. A cópia de projeto exige identidade
compatível; o conferidor exige PE x86. A varredura de um diretório misto filtra
as rodadas por hash antes de coletar resultados. Metadados com destino explícito
recusam sobrescrita. O catálogo usa o nome do módulo associado ao hash.

Passaram **11 controles próprios das ferramentas**, incluindo rejeição de hash
desconhecido, DLL sem seleção explícita, projeto/rodada de outro sujeito,
sobrescrita e mistura de módulos. São controles de proveniência e integridade,
sem substituir testes do aplicativo ou paridade Foxit.

## Reflow: tipos, métricas, estados e arrays

O construtor preservado `0x15c5010` passa o receptor do viewer ao construtor de
layout `0x15c9c90`, que o guarda em `layout+0x98`. RTTI identifica a vtable
`0x53d31f8` como **CReflowViewerEx**. Seu slot `+0x1c` aponta para `0x15c6fc0`,
getter do contador `+0x24`; o slot `+0x20` aponta para `0x15c6e30`.

Esse último verifica índice não negativo e menor que a contagem virtual, usa
um vetor/cache e cria sob demanda um objeto de `0x7c` bytes com `0x15c5500`.
Sua vtable `0x53d3310` tem RTTI **CReflowViewerPageEx**, com base **IPDFViewerPage**
em `0x53d2c50`. Isso liga as leituras `page+0x10/+0x14` dos helpers da rodada
anterior a um tipo concreto neste caminho. Unidades e contrato público completo
das métricas ainda não foram demonstrados. Vetor inconsistente leva a diagnóstico
e `INT3`; fora do intervalo retorna nulo.

`0x15cb8a0` lê um array em `+0x44` ou retorna zero se nulo. `0x15cbe90` combina
os arrays `+0x3c` e `+0x48`; os dois leitores não têm guarda superior local.
`0x15cbbc0` percorre a contagem `+0x78` quando positiva, consulta o viewer e,
se a página existe, chama `0x15cb7b0`: **array48[i] = i; array4c[i] = 0**.
Isso fecha esse escritor, sem provar tamanhos alocados e domínio de todos os
chamadores. `0x15c9e30` libera os cinco membros `+0x3c/+0x40/+0x44/+0x48/+0x4c`
quando presentes; `0x15c9ef0` envolve a limpeza e pode liberar o objeto de `0x9c`.

Os helpers `0x15cb130/0x15cb590/0x15cb720/0x15cbb70/0x15cba00/0x15cbaf0`
refinam escala, margens e offsets conforme o modo. A constante double em
`0x65735e0` é **0,5**. Em `0x15cb590`, a divisão inteira por dois precede a
conversão para double e a soma da constante; não substituir pela divisão real.

`0x15cd700` força modo zero e flag falsa quando a contagem `+0x78` é menor que
dois; no outro caminho grava modo/flag e pode normalizar estado 7 para 2.
`0x15cd800` grava o estado `context+4`. `0x15cd5e0/0x15cd640` inicializam escala
float 1 e dois campos zerados, chamam conversores distintos e os marcam em
caso de retorno não zero; o segundo também propaga escala e estado ao contexto.
Não unir esses campos aos de outra estrutura por coincidência de offsets.

`0x15cc770/0x15cc7b0/0x15cc6b0` ligam esses conversores à atualização virtual,
escala e posição. `0x15cda80` limita a escala entre dois doubles no modo 1;
`0x15cda10` conserva a escala anterior para a transição. `0x15ca680` exige saída
e página válidas e preenche coordenadas/índice. O método maior `0x15ca780` foi
examinado em recortes: condições de entrada, consulta da página, transformação,
modos e atribuições de saída. Sua tipagem de pilha e algoritmo completo seguem
parciais; constantes inteiras mostradas como floats no pseudocódigo não foram
adotadas como tipos reais.

**Ressalva de fronteira:** o corpo selecionado pelo Ghidra para `0x15ca460`
contém só **37 bytes**, enquanto o pseudocódigo alcança casos fora dele. Houve
conferência suplementar com Capstone de `0x15ca460..0x15ca4e1` (130 bytes) e
dos quatro destinos da tabela `0x15ca4e4`. Esses bytes se sobrepõem ao corpo
selecionado e **não foram somados** ao total. A tabela de dados não foi tratada
como instruções; não se declara que a fronteira Ghidra foi corrigida.

## Busca: opções e provedor de índice

O adaptador `0x17cb490` recebe uma estrutura de configurações **distinta** de
`SearchOption` (24 bytes). Os bytes 0/1/2/3/4/6/7 correspondem neste caminho a
palavra inteira, caixa, marcadores, comentários, anexos, stemming e destaque.
Os campos de 32 bits `+0xc/+0x10` alimentam `dialog+0x20ec/+0x20e8`, limitados
entre **1 e 10.000**. Os significados completos desses limites e dos flags
`dialog+0x20e0/+0x20e4` continuam abertos. O construtor inicia os dois limites
em 900 e 500, respectivamente; os setters não provam os valores efetivos de
preferências carregadas em runtime.

`0x1794f80` e `0x17885a0` derivam `dialog+0x1d74` de stemming solicitado e da
ausência de palavra inteira/caixa, atualizando o controle 8035. Ligado ao
produtor preservado `0x1783ac0`, isso associa **SearchOption+5 a stemming
efetivo neste caminho**. `+0x14` conserva a enumeração de quatro textos de
versão identificada anteriormente. `+3/+6/+7/+0xc/+0x10` continuam sem contrato
completo. Os métodos `0x1788cb0/0x1788b70` tratam seleção/refresh; candidatos
heurísticos não foram promovidos a escritores de stemming.

Na DLL, `0x1000c990` instala a interface base `fxindex::fxIndexLib`.
A fábrica preservada `0x10037e40` depois instala `0x100d841c`; o RTTI tem o nome
exato **fxindex::fxLuncenLib** (grafia do binário). Os 28 slots concretos já
estavam catalogados e não são novas entradas. O slot `+0x58` aponta para
`0x1003af20`; seu auxiliar novo `0x1003ac90` constrói consulta pelo campo
`version` com o texto `*` e extrai a versão armazenada.

Isso fornece uma implementação concreta compatível com a interface. *(Atualização de
21/10/2026: a atribuição ativa foi ligada em [REA-PROVEDOR-BUSCA-2026-10-21.md](REA-PROVEDOR-BUSCA-2026-10-21.md).)* Ainda
faltava provar o escritor/fábrica que atribui a instância ativa a `dialog+0x1e48`;
não se afirma que todo provedor do diálogo seja essa classe. `0x174b670` revelou
limpeza de árvore/nós, corrigindo a hipótese inicial de fábrica. `0x1787510`
consulta interface global e pode retornar `0x80004005`; também não fecha essa
atribuição. `0x17eef40` percorre resultados/propriedades, com tipos parciais.

`0x100385f0` copia texto UTF-16 para buffer alocado. `0x1003a5e0` constrói uma
BooleanQuery e condiciona filtro de anexos à opção, com seleção de chaves por
versão. `0x1003f6b0`, de 7.655 bytes selecionados, teve **semântica examinada
apenas em recortes**: cópia de 24 bytes, teste de byte 5, limpeza de palavra
inteira/caixa quando ativo, limpeza local de byte 4 e testes de enum/sentinela.
O acordo de 2.454 instruções do lote inteiro não fecha o algoritmo Lucene,
cancelamento, todas as combinações, ownership ou assinaturas da DLL.

## Impressão e ciclo de vida

`0x1b57340` avança o objeto ativo; ao observar estado interno 2 ou 3, copia-o
para `receiver+0x74`, chama limpeza, libera e zera o ponteiro `+0x70`. Outros
estados conservam o objeto. Isso não comprova impressão física concluída.
`0x1b5a420` retorna `receiver+0x50`, cujo tipo exato permanece aberto.
`0x1b88520` inicializa 56 bytes com valores numéricos, sem instalar vtable;
valores que o Ghidra nomeia `UNK` não foram classificados como ponteiros.

Foram examinados os três slots de **CPDF_BackgroundDrawer**: destruição em
`0x1b88ea0`, preparação/consumo em `0x1b8e560` e trabalho em `0x1b8cf60`.
RTTI distingue a base **IPDF_BackgroundDrawer**. Há liberação do membro `+0xa4`,
do contexto `+0x1c` e de controle compartilhado por contadores atômicos.
O trabalho cria recursos, configura transformação/clipping e tenta alocar
imagem com redução de escala pela metade após falha; a outra entrada prepara
regiões e chega ao consumidor preservado `0x20a6f70`.

O contexto de **0x138 bytes** continua sem classe/contrato completo. Assinaturas
de pilha, ownership universal, formatos, concorrência e resultado de impressão
permanecem parciais. Os números de estado não receberam nomes de UI inferidos.

## Diálogo e IDs 7911/7913

O construtor `0x1758c70` usa recurso **6359** e instala RTTI **CFindToolDlgAdv**,
inclusive uma vtable secundária deslocada em `0xa8`. Seu slot primário `+0x28`
aponta para `0x1777de0`, que salta ao accessor `0x1779780`; este retorna o mapa
`0x53e1550`, com entradas em `0x53e0e78`. Assim, a classe e a tabela foram
associadas estaticamente.

As entradas `0x53e1118/0x53e1130` de IDs **7911/7913** continuam apontando para
o mesmo handler `0x1788db0`. Ele atualiza `+0x1d58`, enquanto o DDX preservado
associa 7911 a `+0x1d58` e 7913 a `+0x1d60`. Não foi inventado um segundo
efeito para resolver a discrepância. Visibilidade, interatividade, sincronização
DDX e comportamento final dos controles ainda exigem observação offline.
O construtor foi examinado quanto a tipo, recurso e campos de estado, sem
declarar reconstruídos seus 5.340 bytes de semântica completa.

## Verificações e próximo ponto

As [ligações estruturais](../testes/resultados/static-remaining-2026-10-18/structural-joins.json)
e [11 controles das ferramentas](../testes/resultados/static-remaining-2026-10-18/tool-controls.json)
estão publicados junto dos metadados. Um helper local de notas falhou por
ausência de `tzdata`; o horário foi registrado com UTC−03:00 explícito, sem
instalação. Uma inspeção avulsa falhou por import fora do diretório do helper;
a execução pelo arquivo local resolveu. As oito rodadas Ghidra e conferências
de máquina terminaram; não houve timeout ou esgotamento de tokens comprovado.

A fila delimitada da rodada anterior foi coberta, com as lacunas semânticas
acima preservadas. Próximos recortes possíveis: alocação/tamanhos dos cinco
arrays e demais chamadores; transições `0x15cd6e0/0x15cc9b0`; atribuição ativa
de `dialog+0x1e48`, campos restantes e algoritmo `0x1003f6b0`; estrutura de
`0x138`, serviços de imagem e concorrência. Consultar o catálogo antes de
novas sementes. Não repetir estas 48 entradas como novas funções.

Fonte do aplicativo, builder, Flatpak e versão **0.1.9/devel** foram preservados.
As suítes de 290 casos por ambiente são evidências anteriores, não repetidas.
Os verificadores de contratos, arquitetura, progresso e auditoria do repositório
foram executados para este marco, sem nova instalação. Roteiro **43,33%**,
37 critérios concluídos/21 abertos e paridade **0/25** permanecem iguais.
Etapas 10, dinâmica da 11 e comparação 18/19 dependem da VM offline. Cliente
de nuvem local, portal, AT-SPI e impressora dependem de desktop/equipamentos
próprios; APIs remotas de nuvem seguem adiadas e recursos de IA excluídos.
