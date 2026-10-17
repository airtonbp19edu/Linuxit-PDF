# Linuxit PDF

Leitor de PDF para Linux, com implementação própria a partir da base MIT
Winux/Print&View e investigação incremental do Foxit Reader com REA/Ghidra.
O código do original não é incorporado ao aplicativo.
O assistente de IA do Foxit e recursos generativos ficam [fora do escopo](docs/ESCOPO.md),
conforme a decisão do usuário em 17/10/2026.

A versão 0.1.1 já contém navegação, seleção, apresentação, temas, prévia e
preparação de impressão em livreto/N-up/mosaico. A busca pesquisa separadamente
texto, marcadores e comentários, com filtros de palavra inteira e maiúsculas,
cancelamento e navegação por resultados. É possível destacar todas as ocorrências
ou somente a selecionada, sem refazer a pesquisa. A base e as adaptações têm
[proveniência registrada](docs/proveniencia-base.json).

No código-fonte em desenvolvimento após esse pacote, há também
[listagem e extração local de anexos](docs/ETAPA-15.md), com backend testado.
O [painel Anexos está ligado ao código GTK](docs/ETAPA-16.md); seus 14 testes
portáveis de controle passaram, e a execução visual GTK/Linux segue pendente.
A [etapa 17](docs/ETAPA-17.md) oferece um verificador da cópia intermediária:
compilação Python, hashes e testes portáveis separados da aprovação GTK/Linux.
A [etapa 18](docs/ETAPA-18.md) registra 13 verificações próprias de uma campanha
comparativa; quatro dependem de Poppler e a observação do Foxit aguarda a VM.
A [etapa 19](docs/ETAPA-19.md) corrigiu deslocamentos de páginas recortadas na
preparação da impressão e a alteração indevida da página de origem em memória.
Nove testes portáveis passaram; a correção ainda não está no Flatpak publicado.

Os 37 testes próprios passaram no código-fonte e no runtime empacotado.
O Flatpak também passou na instalação e execução real no sandbox: abertura,
renderização, busca em marcadores/comentários e geração de livreto.
Esses testes não demonstram equivalência integral com o Foxit; a recuperação
de várias famílias funcionais e o suporte nativo Windows continuam pendentes.

- [Baixar Flatpak 0.1.1](releases/LinuxitPDF-0.1.1-x86_64.flatpak) e [instalação](docs/instalacao.md)
- [Hashes e manifesto](releases/manifest.json)
- [Progresso e metodologia das 21 etapas](progresso/progresso.md)
- [Retomada do desenvolvimento e ambiente local](docs/RETOMADA.md)
- [O que preparar e como continuar a etapa 10](docs/COMO-CONTINUAR.md)
- [Notas datadas para continuidade entre IAs](progresso/notas-continuidade.md)
- [Matriz de paridade](progresso/matriz-paridade.csv)
- [Investigação REA do Foxit](docs/FOXIT-REA.md) e [continuação de busca/impressão](docs/REA-BUSCA-IMPRESSAO.md)
- [Continuação da impressão no Windows e ferramentas verificadas](docs/REA-IMPRESSAO-WINDOWS.md)
- [Consumidores e geometria de impressão: seis entradas adicionais](docs/REA-IMPRESSAO-CONSUMIDORES.md)
- [Etapa 11: condições estáticas da interface e validação pendente](docs/ETAPA-11.md)
- [Etapa 12: contratos das 25 famílias e cenários de aceitação planejados](docs/ETAPA-12.md)
- [Etapa 13: arquitetura revisada e fronteiras verificadas](docs/ETAPA-13.md)
- [Etapa 14: base do projeto e execução portável conferidas](docs/ETAPA-14.md)
- [Etapa 15: backend de anexos e validação sem VM](docs/ETAPA-15.md)
- [Etapa 16: painel Anexos, controlador testado e validação GTK pendente](docs/ETAPA-16.md)
- [Etapa 17: fonte intermediária e comando de validação Linux](docs/ETAPA-17.md)
- [Etapa 18: campanha comparativa e importação de observações offline](docs/ETAPA-18.md)
- [Etapa 19: correções de posicionamento de páginas recortadas](docs/ETAPA-19.md)
- [Pendências por etapa: VM, análises e pontos de retomada](progresso/pendencias-analises.md)
- [Captura do Flatpak em execução](testes/resultados/0.1.1/linuxit-flatpak-0.1.1.png)
- [Arquitetura](docs/arquitetura.md) e [contratos implementados](docs/especificacao.md)
- [Resultados dos testes](testes/resultados/) e [PDF de referência próprio](testes/fixtures/)

Para executar o código no Linux, instale Python 3, GTK 3 com PyGObject/Cairo,
Pillow, cryptography, Poppler e os clientes CUPS. O pypdf 6.20.1 acompanha o
código com sua licença. Em Debian/Ubuntu:

```bash
sudo apt install python3-gi python3-cairo python3-gi-cairo python3-pil \
  python3-cryptography gir1.2-gtk-3.0 poppler-utils cups-client
bash scripts/run.sh testes/fixtures/busca-escopos.pdf
```

No ambiente de nuvem preparado, use o overlay documentado no relatório de
instalação e uma tela X11 para executar os testes GTK:

```bash
DISPLAY=:101 \
PYTHONPATH=/workspace/.print-view-runtime/gi-cairo/usr/lib/python3/dist-packages \
/usr/bin/python3 scripts/run_tests.py --output /tmp/linuxit-tests-novo.json
```

A análise local identificou 3.276 arquivos, 141 módulos PE, 209 entradas de
funções examinadas e 9.973 registros internos de chamadas. O universo completo
de funções/funcionalidades ainda não está fechado; registros não são funções
únicas nem paridade verificada. Binários Foxit, templates completos, bancos
Ghidra e decompilações permanecem fora do repositório.
