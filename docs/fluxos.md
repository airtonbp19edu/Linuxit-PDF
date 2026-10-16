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
  Graphic --> Submit[Destino comum 0x1b5baf0]
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
