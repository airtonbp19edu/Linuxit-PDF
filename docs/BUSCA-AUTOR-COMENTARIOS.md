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
Os 16 controles do comparador passaram. A validação completa no Linux e a nova
comparação com a observação preservada ainda aguardam o CI neste checkpoint.

## Limites e continuidade

Os 50 planos completos de aceitação não foram executados. Paridade de família
continua não verificada. A correção deste recorte não encerra busca/comentários,
nem as etapas amplas 10/11/12/15/16/18/19/21. Pesos e índice do checklist preservados.
Próximos alvos da VM são destinos dos hits, protocolo D11, cancelamento ativo,
abertura independente com senha e imposição com parâmetros equivalentes.
