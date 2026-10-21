# Estudo: renderização de modelos 3D U3D/PRC (etapa E20)

Registrado em 2026/10/20 (America/Sao_Paulo, UTC-03:00). **Estudo apenas: nada foi implementado.**

> **Adiado pelo usuário em 2026/10/20 às 21:18** (decisão D04): o 3D fica para uma atualização
> futura. Este documento guarda tudo o que foi levantado para a implementação posterior; a seção
> "Guia para a implementação futura" no fim é o ponto de partida. As perguntas D-3D-1 a D-3D-3
> continuam em aberto e devem ser feitas ao usuário antes de começar.
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


## Guia para a implementação futura

Tudo abaixo foi levantado em 20/10/2026 para não precisar ser refeito. Itens marcados
**(conferir)** vêm de conhecimento geral e devem ser checados na norma antes de programar.

### O que o Foxit oferece (referência funcional, não código)

- Documentação do Foxit PDF Editor: abre 3D em **U3D, PRC e glTF**; girar, girar livre (spin),
  deslocar e aproximar; **árvore do modelo** com mostrar/ocultar partes; efeitos visuais (modos de
  exibição/iluminação); criar e gerenciar vistas; **medir** e comentar partes do modelo; modo de
  leitura seguro com pergunta de confiança antes de ativar o conteúdo 3D (depende das configurações
  de ativação do próprio PDF).
- Foxit PDF Reader 11 (2021): passou a abrir PRC; comentários 2D sobre o modelo; medidas viram
  comentários; medida de raio e encaixe (snap). Inserir modelo 3D na página é do Editor Pro (pago).
- Instalação analisada (Foxit Reader 2025.2.0.33046, inventário em `engenharia-reversa/`):
  plugin `plugins/U3DBrowser.fpi` (905.312 bytes, SHA-256 `89568b04…4e7a`; importa MFC, GDI+ e
  CRT, sem Direct3D) e o executável principal importa `d3d11.dll`, `dxgi.dll` e
  `D3DCOMPILER_47.dll`. Leitura estática apenas: indica desenho por GPU (Direct3D 11) no programa
  principal e interface 3D no plugin; **não** foi observado em execução nem se sabe se o motor é
  próprio ou licenciado. Textos de interface do plugin: `lang/*/U3DBrowserlang_*.xml`.

### Estruturas do PDF que o leitor precisa entender (ISO 32000, seção de 3D)

- Anotação `/Subtype /3D`: `/3DD` (fluxo 3D ou referência a outro), `/3DV` (vista inicial:
  índice, nome ou dicionário), `/3DA` (ativação: `/A` quando ativar — PO/PV/XA; `/D` quando
  desativar; `/AIS`/`/DIS` estado; `/TB` barra de ferramentas; `/NP` painel de navegação),
  `/3DI` (interativo), `/3DB` (caixa da vista), `/AP` (pôster — já usado na E16).
- Fluxo 3D: `/Subtype /U3D` ou `/PRC`; `/VA` (vistas), `/DV` (vista padrão), `/AN` (animação),
  `/Resources`, `/ColorSpace`; JavaScript 3D em `/OnInstantiate` — **nunca executar**.
- Vista 3D (`/Type /3DView`): `/XN`/`/IN` nomes; `/MS` + `/C2W` (matriz câmera→mundo) ou
  `/U3DPath`; `/CO` distância ao centro de órbita; `/P` projeção (`/Subtype /P` perspectiva com
  `/FOV`, ou `/O` ortográfica com escala); `/BG` fundo; `/RM` modo de exibição (Solid, Wireframe,
  Transparent…); `/LS` esquema de luz (Artwork, None, White, Day, Night, Hard, Primary, Blue, Red,
  Cube, CAD, Headlamp); `/SA` cortes; `/NA` nós (visibilidade, opacidade, modo, matriz por nó).
- PDF 2.0 trouxe medidas 3D (`/3DMeasure`) e comentários associados a vistas **(conferir)**.

### U3D (ECMA-363, gratuita)

- Arquivo em blocos: cada bloco tem tipo (32 bits), tamanho dos dados, tamanho dos metadados.
- Tipos principais **(conferir na 4ª edição)**: cabeçalho `0x00443355`; cadeia de modificadores
  `0xFFFFFF14`; nós grupo/modelo/luz/vista `0xFFFFFF21`–`0xFFFFFF24`; declaração de malha CLOD
  `0xFFFFFF31`, continuação da malha base `0xFFFFFF3B`, continuação progressiva `0xFFFFFF3C`;
  conjuntos de pontos/linhas `0xFFFFFF36`/`0xFFFFFF37` (continuações `…3E`/`…3F`); modificador de
  sombreamento `0xFFFFFF45`; recursos de luz e vista `0xFFFFFF51`/`0xFFFFFF52`; shader
  `0xFFFFFF53`; material `0xFFFFFF54`; textura `0xFFFFFF55` (continuação `0xFFFFFF5C`); movimento
  `0xFFFFFF56`.
- Dificuldade principal: os dados de malha usam um **codificador aritmético por bits** com
  contextos estáticos e adaptativos e valores quantizados; a malha base dá a geometria inicial e as
  continuações progressivas refinam a resolução. Um primeiro recorte viável é ler a malha base
  (e, depois, aplicar as continuações progressivas até a resolução máxima).
- Referência aberta: Universal 3D Sample Software (Apache-2.0) para conferir o decodificador.

### PRC (ISO 14739-1; norma vendida pela ISO)

- Arquivo com assinatura `PRC`, cabeçalho com identificadores e "file structures"; cada estrutura
  tem seções (globais, árvore, tesselação, geometria, geometria extra) comprimidas com zlib e
  codificadas por bits (inteiros de tamanho variável, valores compactados) **(conferir)**.
- Recorte viável: seções de árvore + tesselação (triângulos 3D com normais, tesselação comprimida,
  arames e marcações), cores/materiais e a hierarquia de peças. B-Rep/NURBS exatos ficam fora
  (os visualizadores usam a tesselação que vem no arquivo).
- Referência aberta: nanoPRC (AGPL-3.0 ou licença comercial) — só consultar ou usar com decisão
  explícita do usuário (D-3D-2).

### glTF (aberto, Khronos)

- O Foxit também aceita glTF em PDF. É o formato mais simples dos três (JSON + buffers binários,
  especificação gratuita); o suporte em PDF veio numa extensão recente da norma **(conferir qual
  documento ISO e como o fluxo é marcado)**.

### Arquitetura proposta no Linuxit

1. **Worker `model3d-load`** (processo isolado, como os demais): entrada = PDF + índice da
   anotação 3D (a lista já existe em `pdf_media._entries`); saída = JSON limitado com vértices,
   normais e índices (base64 de float32/uint32), árvore de nós com matrizes, materiais e as vistas
   `/VA` convertidas (câmera, projeção, fundo, modo, luz). Limites sugeridos: 2 milhões de
   triângulos, 10 mil nós, 256 MiB descomprimidos, tempo máximo; nenhuma rede; nenhum JavaScript.
2. **Desenhista próprio**: projeção perspectiva/ortográfica, profundidade (z-buffer em imagem ou
   ordenação por profundidade), sombreamento plano/Gouraud simples com a luz da vista; primeiro por
   software (cairo/imagem) e, se faltar desempenho, `Gtk.GLArea` do GTK 3 (OpenGL do runtime).
3. **Janela 3D**: começa no pôster (comportamento atual da E16) e só ativa a cena por ação do
   usuário (equivalente ao modo seguro do Foxit); girar/deslocar/aproximar com mouse e teclado,
   lista de vistas, árvore de peças com mostrar/ocultar, modos de exibição; acessível por teclado.
4. **Depois**: medidas (distância, raio, ângulo com encaixe), cortes (`/SA`), comentários em vistas.

### Testes e corpus

- Corpus próprio gerado por ferramentas abertas: U3D pelo MeshLab (exportação U3D via IDTF, plugin
  `io_u3d`, GPL) ou pelo conversor IDTF da biblioteca U3D (Apache-2.0); PRC pelo Asymptote (LGPL);
  glTF à mão (JSON). Registrar, como na E17/E18, o resultado esperado de cada arquivo (número de
  triângulos, caixa envolvente, cores por peça, vistas).
- Testes de pixels por vista (cor de cada peça num ponto conhecido), recusas por limite, arquivo
  truncado/malformado sem travar, cancelamento.

### Código atual onde isso se encaixa

- `app/pdf_media.py`: `_entries` (lista anotações 3D com `poster`, `model_embedded`, `views`),
  `extract_media` (salva o modelo), `render_poster` (pôster em PNG).
- `app/media_assets_window.py`: `MediaAssetsWindow._poster` e `Poster3DWindow` (aviso de cena não
  interativa) — ponto natural para o botão "Ativar 3D".
- Catálogo: operação `layers-media/3d` (pendente, adiada) e `layers-media/3d-poster` (feita).
- Testes de referência: `tests/test_media_3d_poster.py`, aceitação S12-21-3/4.

### Esforço estimado (em etapas pequenas como E12–E19)

| Parte | Etapas |
|---|---|
| Desenhista com girar/aproximar/vistas | 1–2 |
| Leitor U3D (casos comuns) | 2–3 |
| Leitor PRC (tesselação) | 3–4 |
| Árvore de peças e mostrar/ocultar | ~1 |
| glTF | ~1 |
| Medidas e cortes | 2+ |

### Fontes adicionais (20/10/2026)

- [Foxit — Work on 3D Content in PDFs](https://resource-cms.foxit.com/foxit-pdf-editor-for-windows/work-3d-content-in-pdfs)
- [BetaNews — Foxit PDF Reader 11 e ferramentas 3D](https://betanews.com/article/foxit-pdf-reader-11/)
