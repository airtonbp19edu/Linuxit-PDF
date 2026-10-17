# Linuxit PDF

Leitor de PDF para Linux, com implementação própria a partir da base MIT
Winux/Print&View e investigação incremental do Foxit Reader com REA/Ghidra.
O código do original não é incorporado ao aplicativo.
O assistente de IA do Foxit e recursos generativos ficam [fora do escopo](docs/ESCOPO.md),
conforme a decisão do usuário em 17/10/2026.

A versão **0.1.4 de desenvolvimento** contém navegação, seleção, apresentação,
temas, busca em texto/marcadores/comentários e preparação de impressão em
livreto/N-up/mosaico. Inclui o painel para listar e salvar anexos de catálogo,
árvores `/Kids` e anotações de página, as correções de origem do CropBox e preservação da página em memória,
além da correção de recursão nos botões da barra lateral.
A base e as adaptações têm [proveniência registrada](docs/proveniencia-base.json).

A [correção do painel lateral](docs/ETAPA-16-LAYOUT.md) preserva o mínimo
calculado pelo GTK: títulos e ícones ficam visíveis, inclusive ao redimensionar,
ocultar/restaurar o painel e alternar o modo de leitura. Dez cenários de
geometria passaram, comparados com dez falhas na fonte anterior.

**127 testes próprios passaram em cada ambiente**: fonte Linux, payload e
Flatpak instalado, sem falhas/erros/skips. Foram conferidos 83 arquivos da
aplicação e nove relatórios selados; smoke GTK 5/5 e launcher 3/3 passaram.
Teste em Debian 13/tela X11 virtual; desktop real, acessibilidade, portais,
impressão física e comparação Foxit continuam pendentes. A janela solicitada
com 760 px ficou 924 px por outros controles; não se afirma suporte real a 760 px.
Portfólios, senha não vazia de anexos e demais famílias continuam pendentes.
O pacote é `devel`, sem assinatura digital e sem declaração de estabilidade.

A [campanha sem VM](docs/AVANCO-SEM-VM.md) aprovou os 17 subconjuntos próprios
com os mesmos arquivos/protocolos da etapa18; quatro bloqueios Poppler resolvidos.
Foram examinadas27 novas entradas estáticas; catálogo236, sem cobertura global presumida.
O kit privado preservado deve ser usado na VM offline para observar o Foxit.
Paridade comprovada permanece **0/25**, e o roteiro permanece **43,33%**.

A [revisão das 21 etapas](docs/REVISAO-ETAPAS.md) auditou a instalação 0.1.3:
2.803 arquivos de dependências, 214 ELF e 149 arquivos de licença e créditos conferidos.
Sete controles do auditor e um novo smoke 5/5 passaram. Os relatórios das
suítes completas 114/114 do 0.1.3 foram conferidos, sem repetir essas suítes
nesta revisão. Os 21 critérios abertos permanecem registrados.

- [Baixar Flatpak 0.1.4](releases/LinuxitPDF-0.1.4-x86_64.flatpak) e [instalação](docs/instalacao.md)
- [Execução das frentes sem VM e entrega0.1.4](docs/AVANCO-SEM-VM.md)
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
- [Etapa 16: painel Anexos e controlador](docs/ETAPA-16.md)
- [Retomada da etapa 16: geometria lateral corrigida no 0.1.3](docs/ETAPA-16-LAYOUT.md)
- [Etapa 17: fonte intermediária e comando de validação Linux](docs/ETAPA-17.md)
- [Etapa 18: campanha comparativa e importação de observações offline](docs/ETAPA-18.md)
- [Etapa 19: correções de posicionamento de páginas recortadas](docs/ETAPA-19.md)
- [Etapa 20: Flatpak 0.1.2, testes Linux e limites](docs/ETAPA-20.md)
- [Etapa 21: auditoria do pacote publicado e obrigações abertas](docs/ETAPA-21.md)
- [Pendências por etapa: VM, análises e pontos de retomada](progresso/pendencias-analises.md)
- [Captura do Flatpak em execução](testes/resultados/0.1.4/linuxit-flatpak-0.1.4.png)
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
