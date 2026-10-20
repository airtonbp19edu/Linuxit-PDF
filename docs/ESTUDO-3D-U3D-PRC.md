# Estudo: renderização de modelos 3D U3D/PRC (etapa E20)

Registrado em 2026/10/20 (America/Sao_Paulo, UTC-03:00). **Estudo apenas: nada foi implementado.**
O objetivo é escolher um caminho para que o Linuxit PDF mostre, gire e aproxime modelos 3D
embutidos em PDF, e levar a decisão ao usuário.

## Ponto de partida (código atual)

- A janela de mídia lista anotações 3D, informa se há modelo incorporado (U3D ou PRC), quantas
  vistas existem e se há imagem de apresentação (E16).
- O modelo pode ser salvo como arquivo; a imagem de apresentação (pôster) é exibida como figura
  fixa, com aviso de que a cena não é interativa (E16, `app/pdf_media.py`, `app/media_assets_window.py`).
- Não há leitor de U3D/PRC nem renderizador 3D. JavaScript 3D, animações e vistas com seção não
  são executados.

## O que um renderizador precisa

1. **Decodificar** o modelo: U3D (ECMA-363) ou PRC (ISO 14739-1) até chegar a malhas de
   triângulos com normais, cores/materiais e a hierarquia de nós.
2. **Desenhar** as malhas: projeção, iluminação simples, profundidade; em GTK 3.
3. **Interagir**: girar, aproximar, deslocar, escolher vistas pré-definidas (/VA do /3DD).
4. **Isolar**: dados de modelo são entrada não confiável (formatos binários complexos). O
   decodificador deve rodar em processo separado com limites, como os demais workers do aplicativo.

## Bibliotecas abertas encontradas

| Opção | Formato | Licença | Situação | Observações |
|---|---|---|---|---|
| Universal 3D Sample Software (SourceForge) | U3D (ler e escrever, segundo a descrição) | Apache-2.0 | Última atualização em 2016; download de 36,3 MiB; avaliações relatam falhas, pouca documentação e problemas de memória | Implementação de referência do ECMA-363 em C++. |
| ningfei/u3d (GitHub) | U3D (foco em **gerar** U3D e converter IDTF) | Apache-2.0 | 17 commits, sem releases; pacote no conda-forge; CMake; depende de libpng, libjpeg e zlib | A parte de renderização foi removida; o README não descreve API de leitura. É o que o MeshLab usa para **exportar** U3D (o plugin `io_u3d` do MeshLab só exporta). |
| nanoPRC (GitHub mvrhel/nanoPRC) | PRC (ler; escreve malhas tesseladas) | **AGPL-3.0** ou licença comercial | 99 commits, sem releases; CMake; vinculações Python; visualizador de demonstração com SDL3 | Exporta JSON/STL/OBJ. Não escreve NURBS/B-Rep exatos; a página não confirma leitura de B-Rep. Usado por visualizadores de terceiros (3dpdf-viewer, ExcelsisViewer). |
| Asymptote (gerador PRC) | PRC (só escrita) | LGPL (projeto Asymptote) | Ativo | Não lê PRC; serve só para gerar fixtures. |

Visualizadores comerciais (Acrobat, PDF-XChange, HOOPS Exchange) leem U3D/PRC, mas são
proprietários e estão fora de escopo. Nenhum material do Foxit é usado.

## Caminhos possíveis

### A — Decodificador próprio (Python) + renderizador próprio por software

- U3D: decodificar o subconjunto mais comum de ECMA-363 (bloco de declaração/continuação de malha
  CLOD na resolução máxima, materiais básicos e nós). PRC: ler o subconjunto **tesselado** (seções
  de árvore e tesselação, triângulos com ou sem compressão), seguindo a especificação pública da
  Adobe (PRC 1.0) e a ISO 14739-1.
- Desenho por software com cairo/numpy em worker isolado (sem depender de OpenGL no sandbox);
  interação girando a câmera e redesenhando a imagem.
- **Licença:** mantém o aplicativo inteiramente MIT, sem dependência nova.
- **Custo:** o maior em desenvolvimento (bit-stream U3D com compressão e quantização; árvore PRC
  extensa). Desempenho limitado a modelos médios (ordem de 100 mil triângulos).
- **Risco:** cobertura parcial dos arquivos reais; precisa de corpus próprio de U3D/PRC gerado por
  ferramentas abertas (MeshLab/IDTF para U3D, Asymptote para PRC).

### B — Bibliotecas existentes em executável auxiliar isolado

- U3D pela Sample Software (Apache-2.0, compatível com MIT) compilada como pequeno executável que
  converte U3D em malha (JSON/OBJ). PRC pelo nanoPRC também como executável separado.
- Desenho como em A, ou com `Gtk.GLArea` (OpenGL do runtime Freedesktop) se o desempenho exigir.
- **Licença:** U3D sem problema. **nanoPRC é AGPL-3.0**: distribuí-lo no Flatpak obriga a oferecer
  o código-fonte dele e a manter suas modificações sob AGPL; o restante do aplicativo pode continuar
  MIT se o nanoPRC ficar em processo separado (agregação), mas isso precisa ser uma decisão
  consciente do dono do projeto. A licença comercial do nanoPRC é alternativa paga.
- **Custo:** menor no decodificador, maior em empacotamento (compilação C++ no manifesto Flatpak,
  manutenção de código de 2016 com problemas relatados).
- **Risco:** código antigo/pouco mantido recebendo entrada não confiável (exige isolamento rigoroso
  e fuzzing básico).

### C — Manter o recorte atual

- Pôster, metadados e extração do modelo para abrir em programa externo (por exemplo, MeshLab
  com IDTF ou visualizadores PRC). Sem custo novo; a família 3D continua parcial.

## Tamanho estimado no pacote

| Item | Acréscimo aproximado |
|---|---|
| A (Python próprio) | dezenas de KiB de código; nenhuma biblioteca nova |
| B — U3D Sample Software | biblioteca C++ compilada (a fonte compactada tem 36,3 MiB; o binário final é bem menor, a medir) |
| B — nanoPRC | biblioteca C/C++ pequena + licença AGPL a acompanhar (a medir) |
| `Gtk.GLArea` | já faz parte do GTK 3 do runtime; sem acréscimo |

Os tamanhos de B só podem ser medidos compilando; não foram medidos neste estudo.

## Proposta

1. **Primeiro:** renderizador próprio por software para malhas de triângulos (girar, aproximar,
   vistas /VA), em worker isolado, testado por pixels — é necessário em qualquer caminho.
2. **U3D:** decodificador próprio do subconjunto comum (caminho A). Se a cobertura em arquivos reais
   ficar insuficiente, usar a Sample Software (Apache-2.0) como executável auxiliar (caminho B).
3. **PRC:** decodificador próprio do subconjunto tesselado (caminho A). Usar o nanoPRC só se o
   usuário aceitar a AGPL para esse componente separado.
4. Antes de implementar: montar corpus próprio de U3D/PRC com ferramentas abertas e registrar o
   resultado esperado de cada arquivo, como nas etapas E17 e E18.

## Decisões pedidas ao usuário

- **D-3D-1:** seguir a proposta (renderizador próprio + decodificadores próprios), ficar no recorte
  atual (C) ou priorizar bibliotecas existentes (B)?
- **D-3D-2:** aceita incluir um componente **AGPL-3.0** (nanoPRC) em processo separado no Flatpak,
  se o decodificador próprio de PRC não bastar?
- **D-3D-3:** qual formato vem primeiro: U3D (mais comum em PDFs de engenharia antigos) ou PRC
  (padrão ISO, mais comum em PDFs CAD recentes)?

## Fontes consultadas (20/10/2026)

- [Universal 3D — Wikipedia](https://en.wikipedia.org/wiki/Universal_3D)
- [Universal 3D Sample Software — SourceForge](https://sourceforge.net/p/u3d)
- [ningfei/u3d — GitHub](https://github.com/ningfei/u3d)
- [MeshLab, plugin io_u3d (somente exportação)](https://github.com/cnr-isti-vclab/meshlab/blob/main/src/meshlabplugins/io_u3d/io_u3d.cpp)
- [PRC (file format) — Wikipedia](https://en.wikipedia.org/wiki/PRC_(file_format))
- [nanoPRC — GitHub](https://github.com/mvrhel/nanoPRC)
- [3dpdf-viewer, PR com base no nanoPRC](https://github.com/theJamess/3dpdf-viewer/pull/2)
- [ExcelsisViewer — GitHub](https://github.com/simonsystem609/ExcelsisViewer)
- [HOOPS Exchange — PRC Reader (comercial, referência)](https://docs.techsoft3d.com/exchange/2024/start/format/prc_reader.html)
