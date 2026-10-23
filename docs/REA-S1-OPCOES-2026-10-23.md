# S1 — opções da busca e preferências

Revisão de **2026/10/23**, America/Sao_Paulo (UTC−03:00), por Codex.
Continuação da análise estática iniciada em 22/10; não houve execução do Foxit,
uso da VM, alteração do aplicativo próprio ou publicação de pacote.

O lote resolve a identidade de três campos antes sem nome completo: ignorar
largura de caracteres asiáticos, ignorar acentos e intervalo de proximidade.
Os campos **+3 e +0xc da estrutura de 24 bytes continuam sem semântica completa**.
Isso mantém S1 parcial e não demonstra paridade com o original.

## Identidade e método

Alvo: `FoxitPDFReader.exe`, SHA-256
`90208c9e8da92c8e546b76c8f4a2f8fb999105d124e663bbea6744fb6bb6b3a6`.
O hash foi novamente conferido antes e depois desta revisão.

Foram reutilizados os seis resultados de
`analysis-local/headless/s1-options-2026-10-22/`, produzidos pelo Ghidra
12.1.4, JDK 21 e script de sementes do REA 6.7.0, em modo complementar direto
`-noanalysis`. Esses resultados **não são Evidence de chamadas MCP REA**.
O pseudocódigo, assembly e projeto permanecem fora do Git.

As seis entradas têm **2.553 instruções e 8.709 bytes** conferidos pelo
[relatório de máquina](../testes/resultados/s1-options-2026-10-22/machine-checks.json).
Quatro entradas são novas no catálogo anterior deste lote; duas são revisitas,
conforme os [metadados](windows-evidence/foxit-rea/headless-cross-checks-s1-options-2026-10-22.json).

| Entrada | Bytes do corpo registrado | Papel examinado | Contagem |
| --- | ---: | --- | --- |
| `0x1724390` | 1.320 | Inicialização do objeto e leitura das preferências, valores padrão e limites | Nova |
| `0x1783ac0` | 3.157 | Construção e encaminhamento por valor do bloco de opções da busca | Revisita |
| `0x17901e0` | 753 | Início da busca; revisão da cópia condicional das preferências para o diálogo | Revisita; ver ressalva de limites abaixo |
| `0x17bf8c0` | 2.645 | Laço de trabalho de outra via da busca, eventos e flags de normalização | Nova |
| `0x17c14f0` | 420 | Construção de flags de busca e chamada condicional do normalizador | Nova |
| `0x17fcc30` | 414 | Gravação das preferências e atualização dos valores globais | Nova |

O registro de `0x17901e0` exige cuidado: seu pseudocódigo atravessa destinos fora
dos `body_ranges` retornados e contém trechos externos mal tipados e misturados.
Portanto, a conferência automática de 753 bytes **não valida todo o texto
descompilado** dessa entrada. O trecho relevante `0x17907b0–0x17907e5` foi
decodificado novamente dos bytes originais por Capstone 5.0.6, separadamente.
Também foram examinados os excertos `0x17fc130–0x17fc223` e
`0x17cb850–0x17cb935`, sem contá-los como novas funções descompiladas.
O [registro da revisão](../testes/resultados/s1-options-2026-10-22/review.json)
preserva os hashes, limites e contagens desses excertos; o texto completo fica em
`analysis-local/headless/s1-options-2026-10-23-supplement.json`.

## Mapa dos campos confirmados

Os deslocamentos da primeira coluna pertencem ao **bloco de opções de 24 bytes
encaminhado ao mecanismo da DLL**. Os deslocamentos da UI, da página de
preferências e da estrutura externa de entrada são layouts diferentes.

| Campo do mecanismo | Semântica rastreada | Chave em `Preferences\Search` | Padrão | Global | Campo do diálogo |
| --- | --- | --- | ---: | --- | --- |
| byte `+6` | Ignorar largura dos caracteres asiáticos | `bIgnoreFullWidth` | 0 | `0x6d1ec2c` | `+0x20e4` |
| byte `+7` | Ignorar diacríticos e acentos | `bIgnoreAccents` | 0 | `0x6b6fb14` | `+0x20e0` |
| inteiro `+0x10` | Intervalo da busca por proximidade | `iProxRange` | 900 | `0x6b6fb1c` | `+0x20ec` |

Em `0x1724390`, as chaves são lidas por chamadas virtuais à interface de
preferências; a seção literal está em `0x53df2e8`, a chave de acentos em
`0x53df32c`, a de largura em `0x53df34c` e a de proximidade em `0x53df3a4`.
A identificação decorre das strings UTF-16 efetivamente lidas do arquivo,
dos destinos globais e dos consumidores; não decorre apenas de nomes do analista.

O trecho `0x17907b0` testa `dialog+0x20dc`. Quando o campo é zero, copia os
globais para `+0x20e0`, `+0x20e4`, `+0x20e8` e `+0x20ec`. Quando ele é diferente
de zero, salta essa cópia. Isso sustenta a distinção entre valores padrão e
valores fornecidos para aquela busca; não demonstra sozinho a experiência
visível de todas as formas de abrir o diálogo.

Na construção em `0x1783ac0`, as leituras de `dialog+0x20e4` e `+0x20e0`
ocorrem em `0x1783c6b` e `0x1783c79`. Os resultados booleanos são armazenados
nos bytes `+6` e `+7` do bloco local. Em `0x1783cb4`, o código lê
`dialog+0x20ec` e o coloca no inteiro `+0x10`. A cópia do bloco para a pilha
da chamada seguinte é visível, por exemplo, em `0x1783efb–0x1783f12`.

## Preferências, controles e limites

A troca de dados em `0x17fc130` liga os campos da página de preferências aos
controles abaixo. O recurso de diálogo 6515, idioma 1033, foi novamente
conferido pelos bytes e hash
`fefbcd358f93002961a02c74eb44bac2d6a1fea4d841f70f52e15c135b87b23b`.

| Campo na página de preferências | Controle | Texto ou papel identificado |
| --- | --- | --- |
| `+0x390` | 8016 (`0x1f50`) | Ignorar largura dos caracteres asiáticos |
| `+0x38c` | 8023 (`0x1f57`) | Ignorar diacríticos e acentos |
| `+0x39c` | 8021 (`0x1f55`) | Valor numérico do intervalo de proximidade |

O controlador numérico de proximidade é validado no intervalo **1–10.000** em
`0x17fc1c8–0x17fc1e4`. O carregador `0x1724390` também limita o global
correspondente a 1–10.000. O limite não foi inferido de uma legenda do recurso.

A função de gravação `0x17fcc30` escreve as mesmas chaves de preferências e,
em seguida, atualiza os globais: página `+0x38c` para acentos, `+0x390` para
largura e `+0x39c` para proximidade. O caminho de leitura, o estado intermediário
e a gravação ficam assim ligados estaticamente.

As preferências vizinhas **não são o mesmo parâmetro**: `iMaxDocs` tem padrão
500 e global `0x6b6fb18`; `iCacheSize` tem padrão 100 e global `0x6b6fb0c`.
O número 900 pertence a `iProxRange`; não é tempo limite, máximo de resultados
ou tamanho de cache neste caminho examinado. As unidades e todos os detalhes
de aplicação da distância ainda exigem a revisão do consumidor na DLL.

## Valores fornecidos por outra estrutura

A entrada antiga `0x17cb490`, já preservada e revisitada sem nova contagem,
recebe uma estrutura externa com **outro layout**. Nela, o byte `+8` vai para
`dialog+0x20e0`, o byte `+9` para `dialog+0x20e4` e o inteiro `+0xc` para
`dialog+0x20ec`. As instruções `0x17cb8aa` e `0x17cb8c5`, com saltos assinados
`JGE` e `JLE`, aplicam o intervalo 1–10.000 à proximidade recebida.
Ao final, a via marca `dialog+0x20dc=1`, impedindo a substituição posterior
pelos valores padrão nesse trecho do início da busca.

**O `+0xc` dessa estrutura externa é proximidade, mas o `+0xc` do bloco de
24 bytes do mecanismo não recebeu esse nome.** Igualdade de deslocamentos em
objetos diferentes não estabelece igualdade de significado. Da mesma forma,
os bytes externos `+8/+9` não substituem os bytes `+7/+6` do mecanismo.

## Outros consumidores examinados

Em `0x17c14f0`, o código limpa o campo de flags `objeto+0x98` e combina bits a
partir do estado de outro objeto. O global de acentos ativa o bit `0x10`; o de
largura ativa `0x20`. Se qualquer um estiver ligado, há chamada a `0x1628890`
com as condições **largura, acentos, 0**, nessa ordem, antes de atualizar o
texto usado por essa via. O mesmo sentido dos bits `0x10/0x20` reaparece em
`0x17bf8c0`; um consumidor recebe a máscara `flags & 0x33`.

O laço de `0x17bf8c0` também contém espera por evento, fila de identificadores,
proteção por objeto de sincronização, consulta ao byte `objeto+0x114` durante
o processamento e sinalização de um evento em `objeto+0x134`. Isso identifica
um caminho de trabalho paralelo da busca, mas não prova que seja a mesma flag
ou o mesmo ciclo de vida do cancelamento da DLL. O encadeamento completo da
UI para esses escritores continua separado dessa observação.

A semântica exata de normalização Unicode e dos casos de entrada transformados
é uma pergunta própria da análise da `lucene++.dll`; este mapa de preferências
não substitui a leitura daquele código nem uma campanha dinâmica.

## Campos ainda abertos e próximos alvos

| Campo do bloco do mecanismo | Fato observado | O que ainda falta |
| --- | --- | --- |
| byte `+3` | Construção examinada fornece o valor 1; o bloco segue sendo copiado e encaminhado | Identificar consumidor efetivo e significado, inclusive se é reservado ou usado apenas por outras vias |
| inteiro `+0xc` | Construção examinada fornece `-1` | Nomear o domínio e a regra do filtro comparado nos consumidores; `-1` não basta para afirmar um contrato público |
| inteiro `+0x10` | Chave, padrão, UI e limites identificados como proximidade | Determinar unidades, condições e aplicação completa na filtragem de resultados da DLL |

Para `+0xc`, a continuação justificada é seguir a comparação e os getters em
`0x100243b0`, `0x100321f0`, `0x10032210`, `0x1002aa80` e `0x1002aac0`, sempre
conferindo qual cópia das opções está sendo usada. Para `+3`, devem ser
rastreados o primeiro DWORD copiado por `0x1003f6b0` e os seus destinatários;
não foi atribuído um nome por exclusão das demais opções.

Nenhum critério amplo, peso, família de paridade, versão ou release foi
encerrado por este lote. Há quatro novas entradas examinadas, duas revisitas
e excertos adicionais com proveniência própria, e não seis novas funções ou
uma conclusão global da busca.
