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

As fontes são independentes: texto das páginas, títulos de marcadores, conteúdo,
assunto e autor de comentários. A fonte posterior ao pacote 0.1.13 inclui autor
após a [divergência medida na VM offline](VM-FOXIT-2026-10-18.md); o pacote
0.1.13 publicado ainda mantém o comportamento anterior. A busca por autor usa
as mesmas opções de caixa, palavra inteira e acentos, sem geometria inventada.
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
GUI e regressão, com PDFs gerados pelo projeto. Verificam escopos, assunto, autor,
maiúsculas, limite, cancelamento, alteração de arquivo, destino ausente,
Unicode e navegação da interface. São testes de implementação.

**Critério diferencial pendente:** executar a mesma consulta/flags no Foxit com
o mesmo PDF e registrar contagem, origem, ordem, destino e erros. Só então
marcar os cenários correspondentes como equivalentes ou divergentes.

A fonte/pacote 0.1.6 acrescenta [busca em anexos, coringas/proximidade e coleção
persistente](BUSCA-COLECOES.md). São contratos próprios limitados: UTF-8 e texto
PDF, padrões por palavra e proximidade ordenada, índice JSON de seleção explícita.
Omissões, corte e fontes desatualizadas são informados. **Stemming**, OCR,
recursão de anexos e demais formatos/serviços continuam não implementados.
Os novos testes GTK exercitam as buscas e a abertura da página da coleção;
não constituem observação Foxit ou execução completa dos50 planos de aceitação.

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

O contrato próprio de [anexos](AVANCO-SEM-VM.md), ampliado na fonte 0.1.4,
lista e extrai entradas de catálogo `/Names/EmbeddedFiles`, incluindo árvores
`/Kids` aninhadas, e anexos de anotação `/FileAttachment`, por índice e hash. Mantém
nomes duplicados como entradas distintas, recusa nomes perigosos e usa criação
exclusiva para preservar arquivos existentes. Tamanho declarado e real são
distintos; o limite de 64 MiB do payload real é aplicado após descompressão.
O [painel da etapa 16](ETAPA-16.md) está ligado no código GTK, com controlador
portável testado. Seis métodos GTK do painel passaram na suíte da fonte Linux
0.1.4 e0.1.5, incluindo payload/sandbox. As entregas 0.1.2/0.1.3 têm
suas evidências históricas preservadas. Portfólios e senha não vazia continuam
não implementados. Ciclos/nós repetidos, pares inválidos, mais de 4.000 nós,
profundidade acima de 64 e mais de 1.000 entradas causam falha explícita.
Esses testes não são paridade Foxit.

Casos de PDF inválido, senha, corrupção, assinaturas, XFA e serviços externos
exigem especificações/corpus próprios. Não se converte presença de código ou
controle em suporte funcional. As 25 famílias da matriz continuam abertas.


## Geometria do painel lateral

A [retomada da etapa 16](ETAPA-16-LAYOUT.md) usa o mínimo calculado pelo GTK
para manter título e ícones na área visível. Cinco painéis/duas larguras,
divisor/ocultação/leitura e anexo longo foram testados no 0.1.3. Pedido760 px
resulta924 px por outros controles; não se afirma suporte a 760 reais. Esse é
um contrato próprio de layout, sem observação/comparação Foxit.

## Alterações em cópia nova

A fonte/pacote0.1.5 acrescenta marcador principal, nota Text e campo AcroForm
Tx em arquivo novo, preservando a origem e recusando sobrescrita. Limites e
falhas em [COPIA-EDITADA.md](COPIA-EDITADA.md).16 testes do backend, quatro do
worker e cinco métodos GTK passaram em cada suíte completa152/152 da fonte,
payload e sandbox. Não implementa edição arbitrária, undo, XFA/portfólio ou
alteração de PDF criptografado/assinado. Não há observação Foxit/paridade.
