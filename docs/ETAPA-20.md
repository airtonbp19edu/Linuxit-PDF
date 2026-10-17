# Etapa 20 — Flatpak 0.1.2 de desenvolvimento

Continuação autorizada em **17/10/2026**, após as correções da etapa 19.
O Flatpak **0.1.2**, branch `devel`, passou em 104/104 testes próprios em
cada ambiente fonte Linux, payload e sandbox instalado, sem skips. O pacote
e as evidências foram baixados e conferidos; versões anteriores preservadas.
A confirmação remota da entrega será registrada após o push.

O host Windows não oferece GTK/Poppler/Flatpak e WSL continua ausente.
Foi verificado acesso ao GitHub Actions já habilitado no próprio repositório.
O [fluxo manual Linux](../.github/workflows/linux-flatpak.yml) usa um runner
efêmero do GitHub, container Debian 13 e usuário de build dedicado. Não altera
componentes do Windows nem executa originais Foxit. O container permite o
sandbox Flatpak aninhado; a credencial do checkout não é persistida e o token
do job tem somente leitura do conteúdo do repositório. Ações oficiais são
fixadas por SHA, e nenhum workflow é disparado automaticamente a cada push.

Sequência em [`scripts/ci_linux_flatpak.sh`](../scripts/ci_linux_flatpak.sh):

1. Dependências GTK/Cairo, ponte GI, Poppler e CUPS em Debian 13; tela Xvfb e
   Openbox dedicados para a aplicação própria.
2. Perfil Linux da etapa 17: suíte completa da fonte sem skips e smoke GTK.
3. Flatpak pelo builder existente, com `runtime-lib`, loader pareado, módulos
   OpenSSL, avisos/licenças e manifesto de pacotes.
4. Igualdade dos hashes fonte/payload; suíte completa pelo Python do payload.
5. Instalação do runtime 25.08 e do candidato no perfil CI; suíte e smoke no
   sandbox instalado, além de lançamento normal e captura da janela própria.
6. Metadados do candidato somente após todos os controles passarem. Qualquer
   falha/skip impede aprovar o pacote; os logs e relatórios são preservados.

[`scripts/record_linux_candidate.py`](../scripts/record_linux_candidate.py)
confere resultados e registra hashes, commits, contagens, runtime e origem.
Os artefatos do CI ficam retidos por 14 dias; o pacote e as evidências examinadas
foram importados em `releases/` e `testes/resultados/0.1.2/`. Não há assinatura digital,
declaração de estabilidade, impressão física ou comparação com Foxit nessa
campanha. A VM offline do original continua sendo uma pendência separada.

Os critérios históricos da etapa 20 para 0.1.1 permanecem preservados. A nova
execução e seus resultados examinados estão registrados abaixo; a existência
do workflow ou o número da versão, isoladamente, não são prova de build.


Primeira execução real: run `39036345773`, commit `0c89ea04ffcddf525fef7955f0142b035bf030ec`. A fonte executou 103 casos: 101 passaram, uma falha e um erro, zero skips; smoke GTK 5/5. Ver [relatório preservado](../testes/resultados/etapa-20-linux-attempt1-2026-10-17.json). Foram corrigidos o isolamento dos controles sintéticos de TEMP e a recursão de sinais GTK da barra lateral, esta última encontrada no stderr. A rodada posterior confirmou as correções; a primeira não aprovou pacote.


## Resultado examinado — 17/10/2026

O [run 39037892892](https://github.com/airtonbp19edu/Linuxit-PDF/actions/runs/39037892892), no commit `e8f9c2e4f48dfc1e5b3cf2a8a6cfe97edb0ee899`, passou.
Em Debian 13, Python 3.13.5 e Xvfb/Openbox, foram executados **104 testes completos
em cada ambiente**: fonte copiada, payload com runtime próprio e Flatpak instalado.
Zero falhas, erros ou skips. Inclui 14 testes do backend de anexos, 14 do
controlador e cinco casos GTK, incluindo os quatro antes sem execução e o
novo controle de troca/ocultação/restauração da barra lateral.

- [Fonte Linux](../testes/resultados/0.1.2/source-intermediate.json),
  [payload](../testes/resultados/0.1.2/payload-tests.json) e
  [sandbox instalado](../testes/resultados/0.1.2/sandbox-tests.json).
- [Igualdade de 83 arquivos fonte/payload](../testes/resultados/0.1.2/source-payload-integrity.json).
- Smoke GTK da fonte 5/5; [sandbox](../testes/resultados/0.1.2/sandbox-smoke.json) 5/5;
  [lançamento normal](../testes/resultados/0.1.2/flatpak-normal-launch.json) 3/3.
- [Revisão do download, logs e captura](../testes/resultados/0.1.2/validation-review.json).

Artefato importado: [LinuxitPDF-0.1.2-x86_64.flatpak](../releases/LinuxitPDF-0.1.2-x86_64.flatpak),
**35.584.088 bytes**, SHA-256
`9d29459d7aff8ca6859cda0846cd698d285b36c3a8de2f463ff87002740cd7ba`.
O ZIP de download conferiu com o digest do GitHub
`e174c761da208fdb5eaa4be65556d3f6ba366dd6b662678f280cf4e60aaaa67d`.
Os 7 relatórios do candidato foram conferidos por hash; a fonte local
coincide com o snapshot examinado. Builder com rastreabilidade de arquivos/pacotes corrigida, runtime
25.08, loader pareado e `runtime-lib`; manifesto de pacotes/licenças incluído.
Versões 0.1.0/0.1.1 e seus manifestos foram preservados.

A captura foi examinada: PDF próprio renderizado e controles visíveis.
O cabeçalho lateral está recortado nessa tela virtual e é um ajuste pendente;
não se aprova todo layout por uma captura. Logs sem traceback/recursão na
rodada aprovada; há aviso de ausência do barramento AT-SPI, portanto tecnologias
assistivas não foram validadas. Desktop real, portais e impressão física
continuam pendentes. O acesso adicional ao checkout no sandbox é do harness,
somente leitura, com escrita liberada à pasta de relatórios.

Os 17 subconjuntos do corpus exato da etapa 18 não foram repetidos nesta rodada;
os 13/4 daquela campanha são um snapshot preservado. Não confundir os 104 testes
próprios com os 20 casos dinâmicos do original ou os 50 de aceitação completos.
Sem Foxit no CI e sem novas observações REA/Ghidra. Paridade 0/25, cobertura
global desconhecida e pesos/estados dos critérios preservados: roteiro 43,33%.

Próximo roteiro: auditoria incremental da etapa 21. Corrigir layout, validar
desktop/plataforma e retomar contratos/famílias ainda parciais. Observar o Foxit
apenas quando a VM offline estiver validada. A confirmação da publicação remota
será acrescentada após push e comparação do HEAD real.


## Auditoria do runtime antes da distribuição

O primeiro candidato funcional (run 39036788146, SHA `c0df14...`) foi retido
localmente. Sua lista tinha somente 25 pacotes porque `dpkg-query` não encontrava
as bibliotecas referidas por `/lib` no Debian com `/usr` unificado e recebia
caminhos de extensões já copiadas ao stage. Esse candidato não foi publicado.
Ver [checkpoint](../testes/resultados/etapa-20-runtime-audit-checkpoint-2026-10-17.json).

O builder agora rastreia cada arquivo de terceiro copiado e consulta caminhos
lexicais e resolvidos. Arquivos sem pacote/aviso identificado interrompem a
construção. Caches MIME/GSettings/ícones/pixbuf têm os insumos e seus pacotes
explicitados, e overlays GI/Cairo exigem seu aviso próprio. A auditoria fica
dentro do pacote e no [relatório de origem](../testes/resultados/0.1.2/runtime-origins.json).

No candidato final: **2803 arquivos de runtime atribuídos**,
**214 arquivos ELF**, **149 pacotes Debian**
com versões e avisos de copyright. A lista inclui libc, OpenSSL, loader SVG,
ponte GI/Cairo, typelibs, módulos Python e dados copiados. Loader pareado,
`runtime-lib`, módulos OpenSSL, base MIT e pypdf BSD preservados. A rodada final
repetiu e passou nos 104 testes em cada ambiente, smoke e launcher. A auditoria
registra proveniência/distribuição e não afirma suporte completo ou paridade.
