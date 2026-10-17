# Fluxos e estados

O fluxo do original permanece parcial. As ligações abaixo são da implementação
independente, apoiada nos contratos e nas observações em `FOXIT-REA.md`.

```mermaid
flowchart TD
  Change[Consulta/opções/documento mudam] --> Cancel[Cancelar geração anterior]
  Cancel --> Capture[Capturar consulta e opções imutáveis]
  Capture --> Sources{Fontes selecionadas?}
  Sources -- não --> Feedback[Pedir uma fonte, sem iniciar trabalho]
  Sources -- sim --> Worker[Worker da geração atual]
  Worker --> Pages[Texto e geometria por página, se selecionado]
  Pages --> Metadata[Marcadores/comentários, se selecionados]
  Metadata --> Bound[Limite global e cancelamento]
  Bound --> Gate{Documento e geração ainda atuais?}
  Gate -- sim --> Results[Publicar resultados na UI]
  Gate -- não --> Discard[Descartar resultados obsoletos]
  Results --> Destination{Destino local conhecido?}
  Destination -- sim --> Navigate[Navegar; destacar apenas geometria conhecida]
  Destination -- não --> NoPage[Resultado sem página inventada]
```

O índice de páginas rejeita mudanças na identidade do PDF. A leitura de
metadados pelo pypdf não pode ser interrompida no meio de uma chamada; o worker
confere cancelamento nas fronteiras, e a UI filtra gerações obsoletas.

```mermaid
flowchart LR
  Options[Opções semânticas] --> Prepare[Preparação PDF no worker]
  Prepare --> Output[PDF de folhas/faces]
  Output --> Preview[Prévia]
  Output --> Backend[CUPS ou adaptador Windows]
```

Esse fluxo preservado da base própria não prova que a geometria resultante
seja idêntica à do Foxit. Os testes internos verificam exemplos de ordem,
quantidade, rotação e recorte; o spooler físico e os casos diferenciais estão
pendentes.

## Caminhos estáticos do Foxit examinados neste marco

```mermaid
flowchart LR
  Boxes[Controles de busca] --> Flags[Bits de caixa e palavra inteira]
  Flags --> Options[Argumento parcial de 24 bytes]
  Options --> Index[Chamadas do caminho de índice]
  NewSearch[New Search] --> Flag[Flag cooperativa]
  Flag --> Consumers[Consumidores e processamento de mensagens]
  Factory[Fábricas de impressão] --> Objects[Objetos e tabelas virtuais]
  GDI[Caminhos GDI localizados] --> Doc[StartDoc / EndDoc]
  Doc --> Pages[StartPage / EndPage]
  Capabilities[DPI e limites físicos] --> Geometry[Consumidores geométricos pendentes]
```

O diagrama não une os objetos de fábrica ao spooler por uma aresta ainda não
demonstrada. Os caminhos completos e o comportamento dinâmico do original
continuam parciais; endereços e provas em `REA-BUSCA-IMPRESSAO.md`.

## Continuação dos consumidores e da geometria

As seis entradas da rodada seguinte estendem os caminhos observados, conforme
`REA-IMPRESSAO-CONSUMIDORES.md`. As setas mostram chamadas verificadas;
não representam uma integração completa com o spooler ou equivalência visual.

```mermaid
flowchart TD
  Collections[Produtor 0x1663a80] --> Graphic[Consumidor 0x1655e00]
  Collections --> Font[Consumidor com fonte 0x16561c0]
  Graphic --> Submit[Inserção em estrutura 0x1b5baf0]
  Font --> Submit
  Bounds[Despacho 0x1663410] --> Handlers[0x1665780]
  Bounds --> Output[0x166fe90]
  Handlers --> RouteA[0x1665a30]
  Handlers --> RouteB[0x1664c00]
  Output --> Factory[Objeto por 0x2d226d0 e chamadas virtuais]
  Placement[Posicionamento 0x1668750] --> Rectangle[Limites transformados 0x1667fe0]
```

Assinaturas e tipos concretos permanecem provisórios. A montagem confirmou
que um slot inicialmente comparado como inteiro foi tipado como float pelo
decompilador devido ao reuso posterior; não transportar essa assinatura para
o código próprio sem completar o contrato.

## Continuação estática de 17/10/2026

Os 21 alvos das duas primeiras rodadas sem VM foram examinados e conferidos
com Capstone. As ligações abaixo são chamadas estáticas; não ligam uma
estrutura encadeada a uma impressora sem examinar seus consumidores.
Detalhes e limites: [avanço sem VM](AVANCO-SEM-VM.md).

```mermaid
flowchart TD
  Route[0x1665780: seleção parcial] --> A[0x1665a30]
  Route --> B[0x1664c00: iteração em blocos]
  A --> Start[0x1b93280: inicialização de estado]
  Start --> Continue[0x1b89510: iteração cooperativa, final2]
  B --> Size[0x166a5b0: limites e offsets]
  B --> Buffer[0x165f970: preparação de objeto e dimensões]
  Buffer --> Setup[0x209c440: armazenamento CFX_DIBitmap]
  B --> Tile[0x1665090: contexto de bloco]
  Tile --> Process[0x1666020: processamento e limpeza]
  A --> Poll[Estado 2/3 ou cancelamento cooperativo]
  Insert[0x1b5baf0] --> List[0x1f21ff0: inserção de nó]
```

Há estados/defaults e relações de chamada suficientes para aprofundamento,
mas não para nomear todas as flags, reconstruir assinaturas ou declarar o
fluxo integral de impressão. A assinatura de `0x1665090` tem artefatos de stack;
corpos de funções anteriores incluem destinos de salto em outros intervalos.
Os getters UI não identificaram a classe ativa; IDs 7911/7913 seguem ambíguos.

## Anexos da implementação independente — fonte 0.1.4

```mermaid
flowchart TD
  PDF[PDF e identidade SHA-256] --> Catalog[Percorrer árvore do catálogo]
  Catalog --> Guard{Estrutura e limites válidos?}
  Guard -- não --> Error[Erro explícito; sem inventário truncado]
  Guard -- sim --> Annot[Enumerar anexos de anotação por página]
  Annot --> List[Indexar referências, origem e página]
  List --> Select[Capturar seleção e hash antes do diálogo]
  Select --> Valid{Documento e geração ainda atuais?}
  Valid -- não --> Cancel[Não iniciar extração]
  Valid -- sim --> Read[Validar nome, ler uma entrada e revalidar hash]
  Read --> Create[Criação exclusiva do destino]
```

Extração já autorizada pode concluir após trocar o documento; callbacks antigos
não atualizam a nova janela. A leitura não executa o conteúdo incorporado.
O limite de 64 MiB é posterior à descompressão e não constitui limite de memória.


## Continuação estática adicional em17/10/2026

0x1666490 calcula fator limitado inferiormente a1 conforme campo+0x8c e
encaminha0x16664e0.0x1b8a2b0 prepara/continua auxiliar+0xe4 e o libera ao
terminar; retorno1 não é confirmação de impressão física.0x1b8d860 configura
recursos e referências compartilhadas, com tipos de chamada ainda provisórios.
0x880490 inicializa sob demanda objeto por área cliente/estado de rolagem;
classe e disponibilidade visual não confirmadas. [Evidências](AVANCO-SEM-VM.md).


A continuação0.1.6 confirmou por RTTI **CPDF_ImageRenderer** em1c68ca0 e
**CReflowViewerEx/IPDFViewer** em15c5010. O objeto criado por15c6550/880490
agora tem contexto de reflow identificado.0x20a6f70 pode retornar1 para clip
vazio; não tratar esse retorno como sucesso de impressão. Assinaturas/stack
permanecem provisórias. [Evidências](BUSCA-COLECOES.md).
