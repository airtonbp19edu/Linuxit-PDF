# Busca pelo autor dos comentários

A fonte posterior ao Flatpak 0.1.13 pesquisa também o campo de autor das
anotações. O pacote publicado 0.1.13 permanece com a implementação anterior;
esta rodada trabalha primeiro com a fonte Linux, sem gerar outro Flatpak.

## Problema e evidência

Na [campanha offline](VM-FOXIT-2026-10-18.md), o Foxit encontrou um comentário
na página 1 ao pesquisar `Autor` com apenas comentários habilitados. O Linuxit
retornava zero. No mesmo fixture preservado, o termo está somente em `/T`:
autor `Autor não pesquisável`, assunto `Assunto separado`, conteúdo `comentário alvo`.
O nome do autor no fixture é histórico; o dado observado mostrou que ele é pesquisável.

A busca própria concatenava somente assunto e conteúdo, embora a extração já
fornecesse o autor. Agora inclui os três campos e aplica as opções existentes
de caixa, palavra inteira e acentos. Resultados mantêm `source=comment`, página
conhecida e `rects=[]`. O escopo de comentários continua explícito e a leitura
não altera o PDF. Ordenação entre fontes e duplicação de termos em vários campos
ainda são contratos próprios, sem equivalência geral comprovada.

O protocolo C18-D09-author e o fixture não mudaram. A expectativa própria foi
atualizada de zero para um, com o histórico e a referência da observação no plano.
Os relatórios anteriores permanecem intactos, inclusive a divergência original.

## Validação desta fonte

Três regressões portáveis foram executadas contra o código anterior: duas
falharam, sem erro de infraestrutura, e a de comentário sem autor passou.
Com a correção, as três passaram. Cobrem o fixture preservado, isolamento de
escopo, destino, ausência de geometria, identidade do arquivo, caixa/palavra
inteira/acentos e comentário sem autor. O teste de escopo existente foi renomeado
para refletir o contrato e o caso GTK foi ampliado para buscar/navegar por autor.
Os 16 controles do comparador passaram. O CI
[39172130287](https://github.com/airtonbp19edu/Linuxit-PDF/actions/runs/39172130287),
fonte `168381b15a501a5a53c933e8b8f3f479559630cb`, passou **403/403 testes** sem
falhas/erros/skips, incluindo o caso GTK ampliado, e smoke GTK 5/5. Dos 400 IDs
anteriores, 399 foram preservados e um renomeado; há três métodos novos.
Os 106 arquivos app correspondem à fonte do CI; somente `search_engine.py`
mudou desde a validação anterior.

A campanha no mesmo corpus passou 17/17 contratos próprios. Reimportando as
observações originais preservadas com os mesmos hashes de fixture e protocolo,
os **11 recortes comparados coincidem**, com zero divergências nessas medidas.
Permanecem cinco inconclusivos e um aguardando observação exata. Não houve nova
execução das buscas do original nesta rodada. A diferença inicial continua
preservada no relatório da campanha anterior.

Artefato 12152449979, 443.026 bytes, SHA-256
`0f83658a30a646da916ef516c33fe7a67509cf5eba7e4412ccdc658bc84c43d3`, conferido
contra o digest do GitHub. Resultados e selos na
[revisão publicável](../testes/resultados/busca-autor-2026-10-18/review.json).
Estes 403 testes validam a fonte; não são nova aprovação de payload/sandbox.

## Limites e continuidade

Os 50 planos completos de aceitação não foram executados. Paridade de família
continua não verificada. A correção deste recorte não encerra busca/comentários,
nem as etapas amplas 10/11/12/15/16/18/19/21. Pesos e índice do checklist preservados.
Próximos alvos da VM são destinos dos hits, protocolo D11, cancelamento ativo,
abertura independente com senha e imposição com parâmetros equivalentes.

## Continuação do diagnóstico D20

O Gerenciador de Tarefas do guest confirmou que `FoxitPDFReader.exe`, PID 5464,
permanece em segundo plano, sem janela do aplicativo. A análise de cadeia de
espera mostrou threads 6804 e 2508; a segunda tem como dependência
`splwow64.exe`, PID 3880. A captura foi examinada e seu hash registrado em
`testes/resultados/busca-autor-2026-10-18/d20-followup.json`. A imagem proprietária
permanece em `analysis-local/resume-20261018-1918/`.

A mensagem genérica do Windows menciona E/S de rede. Isso não comprova tráfego
externo: a configuração foi conferida novamente com zero cabos conectados,
shares e USB capturado, clipboard/drag-and-drop/VRDE/áudio desligados. Não se
atribuiu uma causa definitiva à espera. Nenhum processo foi encerrado, o Foxit
não foi relançado e o coletor anterior não foi reiniciado. D20 continua parcial
quanto à causa e ao encerramento integral; não foi marcado como sucesso.
