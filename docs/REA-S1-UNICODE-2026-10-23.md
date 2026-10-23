# S1 — largura, acentos e normalização Unicode

Revisão de Codex em 23/10/2026. Horário e identidades completas nos registros de
revisão vinculados abaixo. Complementa a
[preparação da consulta](REA-S1-CONSULTA-E-CANCELAMENTO-2026-10-22.md) e a revisão
paralela das opções. Este relatório resolve o destino dos dois booleanos da
normalização no recorte examinado; não encerra S1 nem prova paridade do app.

## Identidade e método

O módulo examinado foi `lucene++.dll`, PE x86, SHA-256
`52bc60eda1744d5d354e216baeb1692611262ca064a0f2f54b5b064b8ad0484d`.
O arquivo continua no diretório original autorizado. Não foi executado.

Foram reutilizados os dois resultados produzidos em 22/10 e examinadas sete
entradas adicionais em cópias sucessivas do projeto preservado: Ghidra 12.1.4,
Temurin JDK 21 e script de sementes do REA 6.7.0, perfil direto `-noanalysis`.
Embora o REA MCP esteja conectado na sessão de retomada, estes resultados são
do backend complementar e não são apresentados como Evidence IDs do MCP.

Os projetos e os resultados completos ficam em `analysis-local/headless/`,
fora do Git. Hash do original conferido antes e depois de cada lote. Capstone
5.0.6/pefile2024.8.26 conferiram todos os endereços de **637 instruções e
1.895 bytes em nove entradas**. A conferência verifica instruções e bytes,
sem transformar assinaturas automáticas em tipos recuperados.

| Lote | Entradas | Instruções | Bytes | Registro |
|---|---:|---:|---:|---|
| `s1-unicode-2026-10-22` | 2 | 299 | 913 | [máquina](../testes/resultados/s1-unicode-2026-10-22/machine-checks.json) |
| `s1-unicode-internals-2026-10-23` | 4 | 193 | 544 | [máquina](../testes/resultados/s1-unicode-internals-2026-10-23/machine-checks.json) |
| `s1-unicode-tables-2026-10-23` | 3 | 145 | 438 | [máquina](../testes/resultados/s1-unicode-tables-2026-10-23/machine-checks.json) |

As nove entradas não constavam no catálogo anterior de 350. Os destinos de
saltos finais incluídos nos corpos, como `0x102ca2c0` e `0x102ca2e0`, não foram
contados novamente. Três trechos auxiliares de decomposição foram apenas
disassemblados diretamente; seus hashes estão no registro de amostras e eles
também não aumentam o catálogo de funções decompiladas.

## Caminho e ordem dos parâmetros

O chamador `fxLuceneLib.dll!0x10032410`, já examinado, extrai os bytes +6 e +7
da cópia das opções. Se um deles estiver habilitado, chama o import
`DealsText::PDFText_UnicodeDeals` passando, nesta ordem, **+6, +7, zero**.
Isso foi conferido nas instruções `0x10032492`–`0x100324b2`, e não deduzido
apenas da assinatura do decompilador.

O destino exportado `lucene++.dll!0x10297d80` preserva a ordem dos três
booleanos e chama `0x102c9540`. O último argumento deste helper é um vetor
opcional de quantidades produzidas por unidade de entrada; o wrapper passa
ponteiro nulo. O primeiro argumento aparente do pseudocódigo é armazenamento
oculto do retorno, não uma opção extra da busca.

| Campo do chamador | Booleano no helper | Efeito estático estabelecido |
|---|---|---|
| Opções +6 | primeiro | Habilita a passagem pela decomposição também para unidades cujo byte de propriedade +3 é zero; isso inclui os caracteres fullwidth examinados |
| Opções +7 | segundo | Permite conservar decomposições de uma base com marcas e elimina as unidades de categoria interna `0x0c` |
| Constante zero | terceiro | Quando habilitado, elimina especificamente U+0640, ARABIC TATWEEL; permanece desabilitado neste caminho da busca |

Os nomes de preferência `bIgnoreFullWidth` e `bIgnoreAccents` vêm da revisão
do produtor das opções; aqui o destino foi conferido independentemente. Não se
renomeia o terceiro booleano como remoção de espaços ou de toda a escrita árabe.

## Regras efetivas e limites da normalização

`0x102c9540` percorre unidades UTF-16 de entrada. Para cada unidade consulta a
propriedade por `0x102c8e30`. Se o primeiro booleano estiver desligado e o byte
de propriedade +3 for zero, conserva essa unidade. Nos demais casos solicita
decomposição por `0x102c90f0`.

O helper de decomposição reúne resultados de `0x102c93c0`. Este consulta uma
tabela de decomposição e expande recursivamente os seus elementos. Na ausência
de decomposição na tabela, há tratamentos explícitos de Æ/æ/Œ/œ para pares
AE/ae/OE/oe; as outras unidades permanecem como estão. Esses tratamentos
internos não significam que a saída pública sempre expanda as ligaturas.

Há duas guardas posteriores importantes:

1. Com o segundo booleano desligado, uma expansão com mais de uma unidade é
   substituída pela unidade original.
2. Com o segundo booleano ligado, se a expansão contiver mais de uma unidade
   que não pertença à categoria `0x0c`, a unidade original também é restaurada.

Só depois dessas guardas o helper concatena as partes e aplica os filtros de
categoria e tatweel. Portanto, trocar a rotina por uma normalização genérica
NFKD seguida de remoção indiscriminada de marcas mudaria casos do contrato
estático observado.

## A categoria filtrada não é “todo acento”

`0x102c9520` chama `0x102c8cc0` e compara o resultado com `0x0c`.
`0x102c8cc0` lê o primeiro byte de um registro de seis bytes, retornado por
`0x102c9f40`. Esse último faz três consultas nas tabelas PE em `0x1045afb8`,
`0x1045c0b8` e `0x1045ebf8`; a base dos registros é `0x10451570`.

Uma leitura independente das tabelas percorreu as 65.536 unidades do BMP.
**1.024 unidades** têm categoria `0x0c`. Comparadas ao banco Unicode15.0 do
Python usado apenas para identificação, 1.023 são `Mn` e uma é `Mc`:
**U+1734 HANUNOO SIGN PAMUDPOD**. Essa diferença foi preservada; a tabela do
original não foi declarada igual à categoria Mn moderna. A primeira hipótese
do verificador, de igualdade completa, falhou e foi substituída por um
registro das categorias realmente encontradas, sem esconder a divergência.

Os exemplos examinados incluem U+0301, U+05B0 e U+064B na categoria removida.
U+0903 tem categoria interna `0x0a` e U+0488 tem `0x0b`; ambos permanecem no
filtro analisado. Assim, remover todas as categorias Unicode M também mudaria
o comportamento. A versão exata do banco Unicode original continua aberta.

Registro: [tabelas e amostras identificadas](../testes/resultados/s1-unicode-tables-2026-10-23/static-table-check.json).

## Amostras derivadas, sem executar o original

A tabela abaixo mostra **previsões de um modelo estático** dos ramos e dados
examinados. Elas não são saídas capturadas do Foxit, testes diferenciais nem
resultados do Linuxit. As letras não foram convertidas para minúsculas nesta
tabela, pois essa etapa pertence ao chamador.

| Entrada | +6 desligado/+7 desligado | Somente +6 ligado | Somente +7 ligado | Ambos ligados |
|---|---|---|---|---|
| `é` | `é` | `é` | `e` | `e` |
| `e` + U+0301 | mesma sequência | mesma sequência | `e` | `e` |
| `Ａ` U+FF21 | `Ａ` | `A` | `Ａ` | `A` |
| `＊` U+FF0A | `＊` | `*` | `＊` | `*` |
| `ﬁ` U+FB01 | `ﬁ` | `ﬁ` | `ﬁ` | `ﬁ` |
| `Æ` / `Œ` | inalteradas | inalteradas | inalteradas | inalteradas |
| `ᾈ` U+1F88 | `ᾈ` | `ᾈ` | `Α` | `Α` |
| U+0903 / U+0488 | inalterados | inalterados | inalterados | inalterados |
| `ـ` U+0640 | `ـ` | `ـ` | `ـ` | `ـ` |

U+0640 só é eliminado ao habilitar o terceiro booleano, que o caminho de busca
examinado passa como zero. Os 11 grupos de amostras e os quatro pares de flags
estão no [registro do modelo estático](../testes/resultados/s1-unicode-tables-2026-10-23/static-model-samples.json).
O código auxiliar que lê as tabelas e os trechos originais ficam privados em
`analysis-local/`; nenhuma tabela Unicode extraída foi incorporada ao app.

## Lacunas preservadas

- O nome integral do byte de propriedade +3 não foi recuperado. Seu endereço,
  valores nas amostras e papel no desvio estão estabelecidos; não recebeu um
  nome de propriedade Unicode por suposição.
- O laço principal lê unidades de 16 bits, sem composição explícita de pares
  substitutos nesse ponto. Comportamento integral fora do BMP e de UTF-16
  inválido não foi demonstrado.
- O vetor opcional foi identificado estruturalmente; o wrapper usado pela
  busca passa nulo. Seus demais consumidores não foram rastreados.
- Não houve testes de alocação insuficiente, normalização completa de todos
  os caracteres, execução no Foxit, equivalência no Linuxit ou avaliação do
  índice. As amostras estáticas não substituem esses trabalhos.
- Esta subfrente não altera o estado global de S1, os critérios, B3,
  percentuais, fonte do app, candidato0.1.19 ou releases.

Registro consolidado desta revisão:
[review.json](../testes/resultados/s1-unicode-tables-2026-10-23/review.json).
