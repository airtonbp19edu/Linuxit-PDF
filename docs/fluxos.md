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
