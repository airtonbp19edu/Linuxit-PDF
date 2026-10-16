# Continuação da impressão no Windows — 16/10/2026

As etapas 08/09 foram retomadas com o mesmo executável Foxit preservado.
Três novas entradas de impressão foram examinadas, levando o catálogo de
**191 a 194 entradas distintas**: 152 pelo REA e 42 exclusivas do backend
complementar. A aplicação publicada continua em 0.1.1. O roteiro permanece
em **43,33%**, com paridade diferencial em **0/25 famílias**.

## Ferramentas e identidade

Foram localizados REA 6.5.0, Ghidra 12.1.4, Temurin JDK 21.0.12.1 e Node
24.22.0. Os dez controles do diagnóstico explícito do provedor Ghidra passaram,
incluindo o componente nativo do Windows. O SHA-256 do Foxit coincide com
`progresso/projeto.json` e permaneceu igual ao fim da análise.

O driver `scripts/rea_mcp_queue.py` passou a aceitar `--node`, permitindo usar
`scripts/rea.mjs` diretamente no Windows, e a usar UTF-8 nos pipes MCP. A
inicialização, o catálogo, a abertura do alvo e sua identidade foram verificados.
O suporte Windows Ghidra do REA é experimental.

## Tentativas preservadas

A primeira sessão abriu o alvo, mas o sandbox recusou a substituição atômica
do arquivo `current.json` do driver. A sessão seguinte foi iniciada com acesso
nativo autorizado. A importação e as três seeds foram aplicadas; a análise
automática atingiu 600 segundos antes do primeiro resultado de função.

O REA retornou `cleanup_incomplete` associado ao tempo excedido. A sessão foi
encerrada e verificou-se que sua JVM já havia parado. Arquivos temporários e
registros foram conservados localmente. Essa tentativa produziu **zero novas
observações de funções pelo MCP**; as consultas restantes não foram executadas.

O backend complementar foi então executado com **`-noanalysis`**, pelo novo
`scripts/analyze_foxit_headless.py`, usando a seed script distribuída com o REA.
As três descompilações terminaram e seus resultados foram examinados junto
às instruções de máquina. Esse caminho é Ghidra direto; seus resultados não
são apresentados como evidências MCP do REA.

## Observações técnicas

| Entrada | Corpo observado | Avanço |
|---|---:|---|
| `0x1668ac0` | 1.184 bytes | Saída de quatro inteiros, ramificação por modo, dimensões físicas, offsets, DPI, escala e posicionamento |
| `0x1663a80` | 1.009 bytes | Dois conjuntos de saídas produzidos por chamadas virtuais e encaminhados a consumidores distintos |
| `0x1663410` | 413 bytes | Conversão de limites em origem/dimensões, seleção de caminho e falha por objeto ausente |

Em `0x1668ac0`, o ramo controlado por `+0xb0 == 5` usa divisão e resto para
derivar índices a partir da entrada selecionada. Os campos de papel físico,
offsets e DPI, identificados no marco anterior, aparecem nos cálculos. Foram
confirmadas constantes float32 próximas de **+0,2** e **−0,2**, e float64
**0,5**, lidas do arquivo original e ligadas às instruções correspondentes.
O outro ramo combina uma escala por entrada com ajustes de posicionamento
e metade de uma diferença positiva, padrão compatível com centralização.
O nome do modo 5 e o significado visual das flags continuam sem confirmação.

Em `0x1663a80`, há dois contadores virtuais, em `+0x10` e `+0xc`, seguidos por
produtores em `+0x18` e `+0x14`. Seis valores de tamanho float são inicializados
com o padrão de uma transformação afim identidade. As saídas seguem para
`0x1655e00` e `0x16561c0`; um marcador de entrada `+8`, inicialmente exigido
como zero, recebe 1. Os tipos concretos e a classificação raster/vetorial
dessas saídas ainda precisam ser determinados.

Em `0x1663410`, as subtrações de limites antes dos dois despachos foram
confirmadas na montagem. O helper `0x16584c0` seleciona o caminho. Um deles
exige a consulta `0x1667c30`, com retorno de falha quando ausente, e encaminha
para `0x1665780`; o outro segue para `0x166fe90`. A assinatura gerada pelo
Ghidra permanece provisória.

## Evidências e próximo passo

- [Diagnóstico e tentativas](windows-evidence/foxit-rea/windows-readiness.json).
- [Metadados dos três resultados](windows-evidence/foxit-rea/headless-cross-checks-windows-2026-10-16.json).
- [Contratos parciais, constantes e endereços de suporte](windows-evidence/foxit-rea/windows-print-contracts.json).
- [Verificações desta retomada](../testes/resultados/retomada-rea-windows-2026-10-16.json).

Os 191 registros anteriores foram preservados; a agregação de manifestos usa
o hash do alvo e o endereço como identidade, evitando contar repetições. Os
geradores passaram a preservar UTF-8 e caminhos de metadados portáveis. O
recálculo do roteiro manteve os critérios e os indicadores anteriores.

Resultados completos e o novo projeto Ghidra estão em
`analysis-local/headless/windows-print-01/`, ignorado pelo Git. As sessões MCP
e seus erros também permanecem em `analysis-local/`. O projeto headless antigo
do ambiente `/workspace` ainda não foi localizado.

Os próximos alvos são `0x1668750`, `0x1667fe0`, `0x1655e00`, `0x16561c0`,
`0x1665780` e `0x166fe90`. É necessário completar seus contratos, os casos
de margem/rotação e a observação do original antes de afirmar equivalência.
Nenhuma execução funcional do Foxit, impressão física ou comparação
diferencial foi realizada nesta rodada. O desenvolvimento continua pelo
código-fonte; não foi gerado outro Flatpak.
