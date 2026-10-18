# Linuxit PDF

Leitor de PDF para Linux, com implementação própria a partir da base MIT
Winux/Print&View e investigação incremental do Foxit Reader com REA/Ghidra.
O código do original não é incorporado ao aplicativo.
O assistente de IA do Foxit e recursos generativos ficam [fora do escopo](docs/ESCOPO.md),
conforme a decisão do usuário em 17/10/2026.

A fonte posterior ao pacote0.1.13 [corrige a busca pelo autor de comentários](docs/BUSCA-AUTOR-COMENTARIOS.md):
**403/403 testes Linux**,17/17 contratos próprios e11/11 recortes comparados
com métricas iguais. Cinco recortes inconclusivos e um pendente permanecem.
O Flatpak publicado continua0.1.13, anterior à correção; nenhum pacote novo.

A 0.1.13 acrescenta [sublinhado, tachado, ondulado, elipse e linha](docs/ANOTACOES-AMPLIADAS.md),
com aparência própria e edição de comentário/autor no histórico de cópia.

A 0.1.12 acrescenta [TIFF multipágina](docs/TIFF-MULTIPAGINA.md), com todas as
páginas em blocos, orientação por página e limite de 100 páginas na criação.
O OCR continua limitado a 20 páginas.

A 0.1.11 acrescenta [OCR local em português e inglês](docs/OCR-LOCAL.md) para uma
cópia rasterizada pesquisável. Preserva o original, informa páginas sem texto
detectado e explicita as perdas de links/formulários/assinaturas na nova cópia.

A versão **0.1.13 de desenvolvimento** contém navegação, seleção, apresentação,
temas, busca em texto/marcadores/comentários e preparação de impressão em
livreto/N-up/mosaico. Inclui o painel para listar e salvar anexos de catálogo,
árvores `/Kids` e anotações de página, as correções de origem do CropBox e preservação da página em memória,
além da correção de recursão nos botões da barra lateral. O menu Arquivo oferece
[marcador, nota e campo de texto em cópia nova](docs/COPIA-EDITADA.md), sem
sobrescrever a origem ou arquivos existentes.
A 0.1.6 acrescenta [busca em anexos, coringas/proximidade e coleção persistente](docs/BUSCA-COLECOES.md), com omissões e fontes desatualizadas explícitas.
A base e as adaptações têm [proveniência registrada](docs/proveniencia-base.json).

A 0.1.10 acrescenta [editor de cópia com desfazer/refazer](docs/EDICAO-COM-HISTORICO.md),
checkbox/radio/listas, mover/excluir marcadores, destaque/retângulo e exclusão
restrita de anotações. Criação de PDF aceita também BMP, WebP e TIFF de um quadro.
OCR foi acrescentado no subconjunto da 0.1.11. O [Flatpak 0.1.10 foi auditado](testes/resultados/0.1.10/audit/review.json),
com sete controles e cinco novos smoke checks aprovados.

A [correção do painel lateral](docs/ETAPA-16-LAYOUT.md) preserva o mínimo
calculado pelo GTK: títulos e ícones ficam visíveis, inclusive ao redimensionar,
ocultar/restaurar o painel e alternar o modo de leitura. Dez cenários de
geometria passaram, comparados com dez falhas na fonte anterior.

**Na entrega0.1.13,400 testes próprios passaram em cada ambiente**: fonte Linux, payload e
Flatpak instalado, sem falhas/erros/skips. Foram conferidos 106 arquivos da
aplicação e 11 relatórios selados; smoke GTK 5/5 e launcher 3/3 passaram.
Teste em Debian 13/tela X11 virtual; desktop real, acessibilidade, portais,
impressão física e comparação Foxit continuam pendentes. A janela solicitada
com 760 px ficou 924 px por outros controles; não se afirma suporte real a 760 px.
Portfólios, senha não vazia de anexos e demais famílias continuam pendentes.
O pacote é `devel`, sem assinatura digital e sem declaração de estabilidade.

A [campanha sem VM](docs/AVANCO-SEM-VM.md) aprovou os 17 subconjuntos próprios
com os mesmos arquivos/protocolos da etapa18; quatro bloqueios Poppler resolvidos.
O catálogo tem **323 entradas examinadas** (152 REA + 171 diretas exclusivas).
A [continuação estática de 18/10/2026](docs/REA-ESTATICA-CONTINUACAO-2026-10-18.md)
examinou mais 48 entradas de busca, impressão e reflow, com tipos e estados
refinados; essa rodada estática não executou o original.
A [primeira campanha na VM offline](docs/VM-FOXIT-2026-10-18.md) executou o Foxit:
11 recortes C18 comparados,10 com métricas iguais e1 divergência em busca por autor.
Há5 recortes inconclusivos e1 ainda sem observação no protocolo exato.
**Conclusão total da recodificação: percentual indeterminado.** O índice histórico
do checklist é **45,13%**, mas não registra avanços dentro dos critérios parciais
e não mede quanto do código está reconstruído. [Medição e evolução das entregas](docs/MEDICAO-PROGRESSO.md).
Paridade integral comprovada permanece **0/25** famílias identificadas.

A [revisão das 21 etapas](docs/REVISAO-ETAPAS.md) auditou a instalação 0.1.3:
2.803 arquivos de dependências, 214 ELF e 149 arquivos de licença e créditos conferidos.
Sete controles do auditor e um novo smoke 5/5 passaram. Os relatórios das
suítes completas 114/114 do 0.1.3 foram conferidos, sem repetir essas suítes
nesta revisão. Os 21 critérios então abertos foram preservados nessa revisão; o registro atual
tem 19 após a consulta da API e a validação do ambiente offline do original em 18/10.
A [auditoria da entrega0.1.5](testes/resultados/0.1.5/audit/review.json) também
passou: mesmo bundle reinstalado,85 arquivos app e dependências verificados,
sete controles e novo smoke 5/5. Esta auditoria não repete as suítes152/152.

- [Baixar Flatpak 0.1.13](releases/LinuxitPDF-0.1.13-x86_64.flatpak) e [instalação e acesso ao download](docs/instalacao.md)
- [Execução das frentes sem VM e entrega 0.1.5](docs/AVANCO-SEM-VM.md)
- [Pastas sincronizadas: uso, limites e dependências de VM](docs/PASTAS-SINCRONIZADAS.md)
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
- [Captura do Flatpak em execução](testes/resultados/0.1.13/linuxit-flatpak-0.1.13.png)
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

A análise local identificou 3.276 arquivos, 141 módulos PE, 323 entradas de
funções examinadas e 9.973 registros internos de chamadas. O universo completo
de funções/funcionalidades ainda não está fechado; registros não são funções
únicas nem paridade verificada. Binários Foxit, templates completos, bancos
Ghidra e decompilações permanecem fora do repositório.


A 0.1.7 acrescenta [criação de PDF de PNG/JPEG](docs/CRIACAO-IMAGENS.md),
com ordem/DPI e fontes preservadas.17 testes novos do backend e cinco GTK
passaram nas três suítes de 212 casos. Demais formatos/OCR continuam pendentes.

A [auditoria independente da 0.1.7](testes/resultados/0.1.7/audit/review.json)
reinstalou o mesmo pacote publicado e conferiu os arquivos/licenças: sete
controles e cinco verificações funcionais passaram. As suítes de 212 casos
são evidências da construção; não foram repetidas nesta auditoria.


A 0.1.8 inclui [operações locais de segurança, texto acessível, integridade CMS
e edição ampliada em cópias](docs/SEGURANCA-ACESSIBILIDADE.md).
267/267 testes próprios por ambiente Linux; nuvem adiada pelo usuário.


A 0.1.9 acrescenta [pastas sincronizadas locais](docs/PASTAS-SINCRONIZADAS.md):
pasta preferida, últimas pastas e cópias novas publicadas completas. Envio é do
cliente externo; APIs remotas continuam adiadas. Guia separa VM e desktop.

A [auditoria independente da 0.1.9](testes/resultados/0.1.9/audit/review.json)
reinstalou o mesmo bundle publicado: arquivos conferidos, sete controles e
cinco novas verificações funcionais aprovados. Não repetiu as suítes completas.

A0.1.10 acrescenta [edição de cópia com histórico](docs/EDICAO-COM-HISTORICO.md):
checkbox/radio/listas, mover/excluir subárvores, destaque/retângulo/exclusão
restrita e desfazer/refazer do rascunho. BMP/WebP/TIFF simples também aceitos.
As cópias já salvas permanecem preservadas. No marco 0.1.10, OCR ainda estava
pendente; foi acrescentado no subconjunto da 0.1.11. As famílias completas seguem abertas.

[Auditoria independente da 0.1.11](testes/resultados/0.1.11/audit/review.json):
mesmo bundle reinstalado, modelos/dependências/avisos conferidos, sete controles
e cinco novos smoke checks aprovados; suítes363/363 não repetidas pela auditoria.

[Auditoria independente da 0.1.12](testes/resultados/0.1.12/audit/review.json):
mesmo bundle reinstalado, modelos/dependências/avisos conferidos, sete controles
e cinco novos smoke checks aprovados; suítes380/380 não repetidas pela auditoria.

[Auditoria independente da 0.1.13](testes/resultados/0.1.13/audit/review.json):
mesmo bundle reinstalado, modelos/dependências/avisos conferidos, sete controles
e cinco novos smoke checks aprovados; suítes400/400 não repetidas pela auditoria.
