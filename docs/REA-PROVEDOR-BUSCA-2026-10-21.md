# Provedor do índice de busca: carga, criação, liberação e descarga — 21/10/2026

Registrado em 2026/10/21 às 20:19 (America/Sao_Paulo, UTC-03:00). Esta é a etapa pequena **E22**
(“Estática: chamadores e tipos da busca”), que avança as etapas 3, 5, 7, 8 e 9 do roteiro.
Os critérios dessas etapas são amplos (“todos os subsistemas”, “todas as famílias”) e continuam
abertos. Nenhum status, peso ou índice foi alterado por este lote.

## Ambiente desta rodada

Pela primeira vez a análise estática rodou no ambiente de nuvem do Claude, sem depender do PC
ligado à VM:

- **Executável:** `FoxitPDFReader.exe`, copiado somente para leitura de `A:\Programas\Foxit PDF Reader`.
  O SHA-256 `90208c9e…b3a6` confere com a referência fixada.
- **DLL de indexação:** `fxLuceneLib.dll`. O SHA-256 `20908415…82e1` também confere.
- **Ghidra:** 12.1.4 PUBLIC, revisão `8b6bbb85`, a mesma da tag oficial `Ghidra_12.1.4_build`.
  Foram copiados do PC só os módulos necessários: Framework, Base, Decompiler para Linux x86-64,
  Microsoft*, PDB e o processador x86.
- **Execução:** OpenJDK 21.0.12 e o script de sementes do REA **6.7.0**. Antes era o 6.5.0; o
  formato `rea-ghidra-seeds-v1` é o mesmo.
- **Tentativas preservadas:** duas falharam antes de importar o executável e ficam em
  `analysis-local/` com os sufixos `-attempt1-sla-mtime` e `-attempt2-missing-sinc`. Na cópia, os
  `.sla` ficaram mais antigos que os `.slaspec`, e faltavam os `.sinc`. A rodada válida usou os
  `.sla` distribuídos, sem recompilar o Sleigh.
- **O que não aconteceu:** não houve análise pelo MCP do REA, o Foxit não foi executado e a VM
  não recebeu nenhum comando.

São **sete entradas novas**, em duas rodadas de Ghidra `-noanalysis`, com **1.128 instruções e
3.992 bytes** conferidos contra os bytes do PE por Capstone 5.0.6 e pefile 2024.8.26. Todas as
fronteiras de instrução conferem. O catálogo passa de **329 para 336 entradas distintas**: 152
pelo REA e 184 diretas. As 329 linhas anteriores ficaram idênticas.

| Entrada | Instruções | Bytes | Papel observado |
|---|---:|---:|---|
| `0x172a2e0` | 42 | 141 | Monta o caminho `…\fxLuceneLib.dll` e chama `LoadLibraryW` uma vez por processo |
| `0x1728ab0` | 15 | 35 | `GetProcAddress("NewIndexHandle")` e salto ao export; devolve 0 sem módulo ou export |
| `0x1728850` | 16 | 39 | `GetProcAddress("DeleteIndexHandle")` e salto ao export, se houver módulo e argumento |
| `0x1770e90` | 52 | 163 | Criação do diálogo: guarda o dono, carrega a DLL, cria o provedor sob demanda e abre o recurso 6359 |
| `0x1776070` | 100 | 329 | Liga sob demanda a interface `SmartRedact`/`AutoRedaction` ao diálogo (`+0x1df8`) |
| `0x175eb50` | 676 | 2.585 | Destrutor de **CFindToolDlgAdv**: espera a thread de busca, fecha o handle e libera o provedor |
| `0x1726b90` | 227 | 700 | Destrutor de **CFindToolModule**: espera outra thread global e chama `FreeLibrary` |

## O que este lote fecha

A [continuação de 18/10](REA-ESTATICA-CONTINUACAO-2026-10-18.md) deixou em aberto o
escritor ou fábrica que atribui a instância ativa a `dialog+0x1e48`. A cadeia agora está ligada
estaticamente, byte a byte:

1. **Carga.** `0x172a2e0` pede ao objeto dono (chamada virtual `+0x184`) um diretório. Em seguida
   anexa a ele o texto literal `\fxLuceneLib.dll`. Se o global `0x6d1ec34` estiver vazio, chama
   `LoadLibraryW` com o caminho completo e guarda o módulo nesse global. As chamadas seguintes
   reaproveitam o mesmo módulo.
2. **Criação.** `0x1770e90` grava o dono em `dialog+0x1d7c` e chama a carga. Se `dialog+0x1e48`
   for zero, grava ali o retorno de `0x1728ab0(0)`.
3. **Fábrica na DLL.** O export `NewIndexHandle` (`0x10033c90`) aloca **0x20 bytes** e salta para
   `0x10037e40`. Esse construtor, já preservado, instala a vtable de **fxindex::fxLuncenLib**
   (grafia do binário). O provedor ativo do diálogo é, portanto, essa classe de 32 bytes, criada
   pela DLL. Isso vale enquanto o export existir. Sem módulo ou export, o campo fica zero.
4. **Liberação.** O destrutor `0x175eb50` faz quatro coisas, nesta ordem:
   - consulta `GetExitCodeThread` sobre a thread de `+0x1e3c`;
   - se ela ainda estiver ativa (`0x103`, STILL_ACTIVE), espera com `WaitForSingleObject(INFINITE)`
     e destrói o objeto da thread pelo slot `+4`;
   - fecha o handle `+0x1e40` com `CloseHandle`;
   - **depois disso** entrega `+0x1e48` ao wrapper `0x1728850` e zera o campo.

   O export `DeleteIndexHandle` (`0x10033c70`) chama o destrutor virtual com exclusão (slot 0,
   argumento 1).
5. **Descarga.** O destrutor de **CFindToolModule** (`0x1726b90`) espera a thread global
   `0x6d1ec6c` e libera os objetos de interface que guarda. No fim, chama `FreeLibrary` sobre
   `0x6d1ec34` e zera o global.

A conferência repetível está em
[`structural-joins.json`](../testes/resultados/static-search-provider-2026-10-21/structural-joins.json),
gerado por [`scripts/check_search_provider_joins.py`](../scripts/check_search_provider_joins.py).
O script relê os dois binários pelos hashes fixados e confere strings, imports, exports, RTTI e as
instruções de cada elo, gravando só endereços e nomes.

## Observações que não viram contrato

- **Sem teste do endereço obtido.** O wrapper de liberação `0x1728850` não testa o resultado de
  `GetProcAddress` antes do salto; testa só o módulo e o argumento. O de criação testa. Fica
  registrado como observação de bytes, não como defeito comprovado em execução.
- **Plugin de redação.** `0x1776070` usa os textos `SmartRedact`, `FoxitInnerPluginFoxitSmartRedact`,
  `Protect_Panel_Redaction`, `Ribbon_Category_Protect` e `AutoRedaction`. Por chamadas virtuais
  ainda não resolvidas, ele guarda em `dialog+0x1df8` um objeto obtido do gerenciador de plugins.
  Isso liga estaticamente o diálogo de busca avançada à redação automática (“pesquisar e redigir”).
  Os significados de `+0x19c`, `+0x518`, `+0x278`, `+0x34` e `+0xb4` do dono são inferências e
  não foram promovidos a nomes.
- **Coincidências de offset.** Outros acessos a `+0x1e48` fora da faixa do diálogo (`0x117f0a0`,
  `0x1180d60`, `0x1a74350`, `0x1bfc8e0`, `0x3bd9c00`) pertencem a outras estruturas pelo contexto.
  Não foram somados nem associados ao provedor.
- **Pontos ainda abertos.** A ordem real entre as threads, as falhas de carga e o caminho exato
  devolvido por `+0x184` não foram observados. Ver a VM e a etapa E24.

## Consequência para o Linuxit PDF

O índice próprio (`app/search_*`) não usa essas classes nem esse código. O contrato útil é de
ciclo de vida: o provedor do índice nasce sob demanda na primeira abertura do diálogo. Antes de
liberá-lo, a busca em andamento precisa terminar (join da thread de trabalho). O módulo do índice
só é descarregado pelo dono, depois de esperar suas próprias threads. Na implementação própria,
a busca roda em processos de trabalho isolados: `app/search_tasks.py` aguarda o fim do processo com
`proc.wait()`. Ainda não há teste específico para a ordem “terminar a busca e só então liberar o
índice”. Este lote documenta a referência para a comparação futura, sem afirmar paridade.

## Evidências

- Sementes: [principal](windows-evidence/foxit-rea/static-search-provider-2026-10-21-seeds.tsv)
  (SHA-256 `ee561b79…4fe9`) e [dono do módulo](windows-evidence/foxit-rea/static-search-provider-owner-2026-10-21-seeds.tsv)
  (`6567e15f…0fbe`).
- Metadados: [rodada principal](windows-evidence/foxit-rea/headless-cross-checks-static-search-provider-2026-10-21.json)
  e [dono do módulo](windows-evidence/foxit-rea/headless-cross-checks-static-search-provider-owner-2026-10-21.json).
- Conferência de máquina: [principal](../testes/resultados/static-search-provider-2026-10-21/machine-checks.json)
  (6 entradas, 901 instruções, 3.292 bytes) e [dono](../testes/resultados/static-search-provider-owner-2026-10-21/machine-checks.json)
  (1 entrada, 227 instruções, 700 bytes).
- Resultados brutos, pseudocódigo e projetos ficam fora do Git, em
  `analysis-local/headless/static-search-provider*-2026-10-21/`, no ambiente onde a rodada foi
  feita. Nenhum código descompilado foi incorporado ao aplicativo nem versionado.

## Próximos recortes

Não repetir estas sete entradas. Ficam abertos:

- os chamadores de `0x1770e90` (quem abre o diálogo e com qual dono);
- a classe da thread `+0x1e3c` e o laço de busca que ela executa;
- os campos `+3/+6/+7/+0xc/+0x10` das opções e o algoritmo `0x1003f6b0`;
- o contexto `0x138` e os serviços de imagem da impressão;
- os tamanhos e a propriedade dos cinco arrays do reflow.
