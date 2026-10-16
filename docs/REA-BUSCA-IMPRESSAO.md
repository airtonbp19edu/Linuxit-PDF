# Continuação da busca e impressão — 16/10/2026

Foram executadas duas sessões dirigidas do REA/Ghidra e cinco extrações
complementares no projeto Ghidra preservado. O catálogo passou de 131 para
**191 entradas distintas examinadas**. Existem 152 entradas por REA, mais
39 entradas exclusivas do backend complementar. Repetições entre perfis não
contam como novas funções; descompilar não equivale a recuperar um contrato completo.

Os quatro módulos aprofundados continuam sendo quatro dos 141 PE inventariados.
A cobertura global permanece indeterminada. O roteiro continua em 43,33% e a
paridade verificada em 0/25 famílias: nenhum desses indicadores foi aumentado
apenas pela quantidade de chamadas ou arquivos produzidos.

## Busca

O controle de palavra inteira (`+0x1d50`) e o de diferenciação de caixa
(`+0x1d54`) chegam a uma estrutura de consulta pela rotina `0x17790d0`.
No campo `+0xc`, os bits `0x2` e `0x1`, respectivamente, são combinados.
Isso prolonga a antiga observação que só ligava as caixas ao estado da janela.

Na rotina `0x1783ac0`, foi identificado um argumento de **24 bytes**, copiado
por instruções de 16 e 8 bytes. O layout observado inclui:

| Offset | Origem observada |
|---|---|
| 0, 1 | bits de caixa e palavra inteira da consulta |
| 2 | opção de anexos `+0x1d64` |
| 3 | constante 1, significado ainda desconhecido |
| 4 | proximidade, condicionada ao escopo e modo 2 |
| 5, 6, 7 | estados `+0x1d74`, `+0x20e4`, `+0x20e0`, sem nomes confirmados |
| 8 | modo obtido por uma tabela de três valores |
| 12 | constante -1, significado ainda desconhecido |
| 16 | estado `+0x20ec`, significado ainda desconhecido |
| 20 | estado `+0x1e54` após validação de contexto |

O layout e seus endereços estão em
[`search-print-contracts.json`](windows-evidence/foxit-rea/search-print-contracts.json).
Não se atribuiu um campo inventado ao stemming. Ainda faltam a interpretação
de todos os campos, os algoritmos linguísticos e os caminhos completos de anexos.
Nem toda busca do documento foi demonstrada como dependente desse índice.

As entradas `0x1774a40` e `0x1784720` foram examinadas. A seleção de uma ou outra
é observável no comando de busca; isso não transforma seus nomes de analista
em símbolos originais recuperados.

A flag `+0x1dd8`, escrita pelo comando New Search, tem consumidores confirmados.
Em `0x1794b40`, um processamento de até cinco mensagens termina quando ela é
acionada; Escape e uma liberação de mouse correspondente chamam New Search.
Em `0x1767ea0`, a flag encerra um caminho de iteração. O cancelamento é
cooperativo nesses pontos, sem prova de interrupção instantânea de todo o motor.

## Impressão

As duas construções pendentes, `0x1645c30` e `0x1645f50`, foram examinadas e
compartilham a tabela virtual `0x53d6bfc`. A segunda mantém vetores de entrada
e ativa um estado diferente; a assinatura exata e todos os significados dos
campos ainda são provisórios.

Foram localizados caminhos concretos de GDI:

| Rotinas | Chamadas observadas |
|---|---|
| `0x166e180`, `0x166e960`, `0x1698cf0` | `StartDocW`, `EndDoc` |
| `0x166d160`, `0x166d410`, `0x166f160` | `StartPage`, `EndPage` |
| `0x1684700` | DPI X/Y, largura/altura física, offsets físicos X/Y |

Há verificações de falha de início de documento/página, iteração e estado de
cancelamento. O fluxo tem ramificações com outro objeto de saída, portanto não
se afirma que toda saída passe pelo mesmo caminho GDI.

Os seletores de `GetDeviceCaps` são `0x58`, `0x5a`, `0x6e`, `0x6f`, `0x70`
e `0x71`. A observação dá suporte à separação entre papel físico, DPI e margens
não imprimíveis. Ainda faltam a ligação de todos os despachos virtuais, as
transformações geométricas completas e a seleção de saída vetorial/raster.
Nenhum trabalho físico foi enviado ou comparado.

## Execução isolada

O kernel recusou um ELF x86 mínimo próprio com `ENOEXEC`. O mesmo programa
passou sob QEMU-i386. O Wine x64 executou seu controle, enquanto o caminho
WOW64 nativo terminou em SIGSEGV antes de uma aplicação x86 funcionar.

Foram verificados 40 arquivos de pacotes Debian, incluindo QEMU e dependências
Wine/i386, sem instalação global. Um runtime inteiramente Win32 sob QEMU,
com adaptadores próprios para os processos filhos, passou duas vezes no
controle de `cmd.exe`; a configuração final exige saída 0 e a mensagem esperada.

O **Foxit carregou nesse runtime, mas não abriu uma interface utilizável**.
O log registra uma exceção C++ cujo ThrowInfo corresponde a
`CInvalidArgException`. Posteriormente há `INT 0x29`, com ECX 7, no endereço
preferencial `0x4ba55ee`. A causa original da exceção não está determinada.
O erro subsequente não foi tratado como simples instrução de CPU ausente nem
contornado por alteração do executável.

Os originais permaneceram somente para leitura, sem rede, contas ou outros
checkouts montados. Não houve observação funcional de busca/impressão no Foxit.
O relato anterior de falha de ShellExecute descreve as tentativas antigas;
o bloqueio atual é mais específico e está em
[`dynamic-followup.json`](windows-evidence/foxit-rea/dynamic-followup.json).

## Aplicação independente e pacote

O Linuxit PDF 0.1.1 acrescenta **Destacar todas as ocorrências**. Desmarcar a
opção mantém o destaque somente no resultado selecionado; Próximo/Anterior
movem o destaque sem refazer a pesquisa. Os resultados e suas coordenadas
são preservados. A preferência é de apresentação e não copia o layout binário
do original.

Também foi corrigido o encerramento de uma janela com navegação ou debounce
pendentes. A suíte passou com **37 casos**, na fonte e no payload, incluindo
verificação dos pixels Cairo e dos callbacks após destruição. O Flatpak passou
em cinco verificações dentro do sandbox real. Esses testes são próprios.

O pacote e seu hash estão no [manifesto](../releases/manifest.json). Os formatos
Windows e outras famílias funcionais não foram retomados neste marco.

## Evidência e reprodução

As sessões `search-print-01` e `search-print-02` estão fora do Git. Seus exports
e snapshots de encerramento foram gravados. São 31 observações MCP nesta etapa,
com uma entrada já examinada anteriormente. Um resultado de `0x177ad50`
excedeu o limite de resposta; seu registro completo foi recuperado do export,
preservando o erro de transporte. A tentativa de paginação após fechamento
falhou e também foi registrada.

O primeiro perfil capturou sete seeds. Duas entradas foram acrescentadas ao
arquivo depois da captura, razão das duas consultas recusadas; `seeds-used.tsv`
preserva os sete valores efetivamente usados. O segundo perfil definiu os
24 alvos antes da abertura. Não se atribui sucesso às consultas recusadas.

```bash
python3 scripts/manifest_foxit_rea.py \
  --session-root /workspace/foxit-rea-analysis \
  --output-dir docs/windows-evidence/foxit-rea
python3 scripts/catalog_foxit_headless.py --evidence-root /workspace/foxit-rea-analysis
python3 scripts/catalog_foxit_functions.py
python3 scripts/check_foxit_emulation.py
```

O backend complementar usou `-process FoxitPDFReader.exe -noanalysis` no
projeto preservado. Corpos e tipos podem diferir entre perfis; a variante
complementar de `0x17901e0`, por exemplo, ficou menor que o corpo observado
pelo MCP. Assembly, pseudocódigo e bancos completos permanecem locais.
