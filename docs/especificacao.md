# Contratos implementados e critérios de comparação

A especificação distingue observações no Foxit, decisões próprias e obrigações
não reconstruídas. A matriz em `progresso/matriz-paridade.csv` é o inventário
funcional aberto; cada família precisa de casos adicionais antes de ser encerrada.

O [escopo autorizado](ESCOPO.md) exclui o assistente de IA do Foxit e recursos
generativos, por decisão do usuário em 17/10/2026. As 25 famílias atuais não
incluíam uma obrigação dedicada de IA e permanecem inalteradas.

O detalhamento da etapa 12 está no [registro de contratos funcionais](contratos-funcionais.md)
e em sua [fonte estruturada](especificacao-funcional.json): 25 famílias, entradas,
saídas, erros, efeitos e 50 cenários de aceitação planejados. Subconjuntos atuais
e propostas futuras estão identificados separadamente. A especificação de
referência ainda é parcial; expectativas e observações Foxit desconhecidas
permanecem nulas. Consulte também [ETAPA-12.md](ETAPA-12.md).

## Busca por documento

**Evidência Foxit:** os controles Whole Words, Case Sensitive, Include Page Text,
Include Bookmarks e Include Comments são ligados ao estado da janela. O código
observa trabalho ativo antes de retomá-lo. A continuação confirmou bits de caixa/palavra inteira, um argumento de 24 bytes
e consumidores da flag de cancelamento; o significado de todos os campos e os
algoritmos permanecem parciais (`REA-BUSCA-IMPRESSAO.md`).

**Contrato próprio implementado:** consulta literal de até 256 caracteres,
normalização NFC e casefold opcional; palavra inteira considera letras,
números, marcas Unicode e sublinhado. Ignorar acentos e unir hifenização são
extensões herdadas da base própria, sem alegação de igualdade ao Foxit.

As fontes são independentes: texto das páginas, títulos de marcadores, conteúdo
e assunto de comentários. Autor do comentário não entra na busca nesta versão.
A seleção inicial pesquisa apenas páginas. Com nenhuma fonte selecionada, a UI
pede uma fonte e não inicia trabalho. A ordem é texto por página, marcadores e
comentários; o limite global padrão é 5.000 ocorrências. Resultados das páginas
conservam geometria. Marcadores e comentários navegam para a página associada,
sem inventar retângulos de destaque; destinos sem página local continuam sem
página. A hifenização só se aplica ao texto geométrico das páginas.

Cancelamento interrompe a emissão de resultados. O modelo mantém a identidade
do arquivo e rejeita PDF alterado; resultados antigos não atualizam outra
consulta/documento. O processamento da estrutura PDF pelo pypdf não é
interrompido no meio de uma chamada; o cancelamento é conferido antes/depois
nas fronteiras de trabalho. As opções são capturadas por requisição imutável.

A preferência **Destacar todas as ocorrências** vem ativa. Desativada, apenas
a ocorrência selecionada é desenhada; a navegação move o destaque e o conjunto
de resultados permanece igual. Alternar a preferência não inicia outra busca.
Metadados sem coordenadas não recebem retângulos inventados. Fechar a janela
cancela tarefas e timers; navegação agendada não acessa widgets destruídos.

**Testes próprios:** `tests/test_search_highlights.py` verifica pixels e ciclo
de vida com GTK/Cairo, além de `tests/test_search_scopes.py`, testes anteriores de busca,
GUI e regressão, com PDFs gerados pelo projeto. Verificam escopos, assunto,
maiúsculas, limite, cancelamento, alteração de arquivo, destino ausente,
Unicode e navegação da interface. São testes de implementação.

**Critério diferencial pendente:** executar a mesma consulta/flags no Foxit com
o mesmo PDF e registrar contagem, origem, ordem, destino e erros. Só então
marcar os cenários correspondentes como equivalentes ou divergentes.

**Não implementado:** busca em conteúdo de anexos, stemming, proximidade,
coringas e índice persistente de coleções. Suas opções não são exibidas como
se funcionassem. Busca em comentários não equivale a edição de anotações.

## Impressão e visualização

A base própria preserva preparação de PDF em livreto, N-up e mosaico, com
prévia, CUPS e adaptador Windows. Testes reabrem saídas com pypdf e verificam
quantidade/ordem de páginas; testes GTK exercitam a prévia. Essa geometria é
código independente pré-existente, sem derivação do pseudocódigo Foxit.

A [correção própria da etapa 19](ETAPA-19.md), na fonte posterior ao pacote
0.1.1, normaliza a origem do CropBox e desvincula a cópia da referência da
página original antes de transformar o conteúdo. Nove testes portáveis
verificam posições no PDF, rotações, modos e preservação da origem em memória.
Não foram executados GTK, rasterização ou impressão física nesta rodada.

Os registros Foxit confirmam troca de modos, notificação, encaminhamento por
documento e parte do ciclo de vida do objeto de impressão. Não confirmam ainda
que a imposição própria reproduza toda geometria, margem, rotação ou escolha
de papel do Foxit. Impressão física, estados de impressora e spooler precisam
de casos reais, incluindo falhas e cancelamento.

## Erros e limitações

O contrato próprio de [anexos da etapa 15](ETAPA-15.md) lista e extrai entradas
de catálogo plano `/Names/EmbeddedFiles`, por índice e hash do documento. Mantém
nomes duplicados como entradas distintas, recusa nomes perigosos e usa criação
exclusiva para preservar arquivos existentes. Tamanho declarado e real são
distintos; o limite de 64 MiB do payload real é aplicado após descompressão.
O [painel da etapa 16](ETAPA-16.md) está ligado no código GTK, com controlador
portável testado e cinco casos GTK aprovados em cada suíte Linux/payload/sandbox
0.1.2; layout completo e desktop real ainda pendentes. Portfólios, /Kids,
senha não vazia e anexos exclusivos de anotações continuam não implementados.
Esses testes não são paridade Foxit.

Casos de PDF inválido, senha, corrupção, assinaturas, XFA e serviços externos
exigem especificações/corpus próprios. Não se converte presença de código ou
controle em suporte funcional. As 25 famílias da matriz continuam abertas.
