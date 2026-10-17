# Retomada do Linuxit PDF

Contexto reconstruído em **16/10/2026**, a pedido do usuário, a partir do
repositório e de seus registros de continuidade. Este arquivo permite seguir
o desenvolvimento mesmo sem acesso ao chat original.

Para os passos que o usuário precisa preparar e uma mensagem pronta para
retomar em outro chat, leia [Como continuar](COMO-CONTINUAR.md).

Leia também as [notas datadas de continuidade](../progresso/notas-continuidade.md),
atualizadas a cada rodada com horário de São Paulo, evidências e próximo passo.

Checkpoint mais recente: [etapa 21](ETAPA-21.md). Bundle 0.1.2/devel
reinstalado sem rebuild e auditado: 83 arquivos da aplicação, 2.803 dependências,
214 ELF e 149 avisos conferidos nos bytes da instalação. Sete controles do
auditor e novo smoke GTK 5/5 passaram; fonte e bundles não foram alterados.
Os 104/104 por ambiente da [etapa 20](ETAPA-20.md) são evidência histórica
preservada, sem repetição completa nesta rodada.

Etapa 21 segue 50%, com encerramento pendente: 21 critérios abertos em 14 etapas,
roteiro 43,33% e paridade 0/25. Próximo trabalho concreto: retomar etapa 16,
corrigir cabeçalho lateral recortado e verificar geometria/captura GTK. Depois
repetir quatro subconjuntos Poppler no corpus preservado da etapa 18. Desktop real,
acessibilidade, portais e impressão física pendentes; comparação original exige
VM offline. O roteiro tem 21 etapas; a continuidade retorna às pendências já registradas.

A [etapa 18](ETAPA-18.md) preparou a campanha com 17 subconjuntos
de backend: 13 observados/aprovados e quatro bloqueados por Poppler. Dezesseis
testes do comparador passaram; modelo Foxit vazio importado com zero
comparações. Preservar a mesma pasta `analysis-local/comparison-stage18-final/`
para a futura observação do original: corpus em `input/`, modelo JSON na raiz.
Sem execução do Foxit, paridade 0/25 e critérios diferenciais ainda pendentes.

A [etapa 17](ETAPA-17.md) oferece a verificação de uma cópia da
fonte atual com hashes, compilação Python e testes portáveis. O comando
`scripts/check_intermediate.py --profile linux` exige a suíte completa sem
skips e smoke GTK antes de aprovar esse runtime. Neste Windows, o perfil Linux
é recusado por falta do ambiente. A aprovação histórica do Flatpak 0.1.1 foi preservada; a etapa 20 acrescenta
validação da fonte atual e do novo pacote, sem validar todo desktop ou Foxit.

## Base recuperada

- Repositório: <https://github.com/airtonbp19edu/Linuxit-PDF>, branch `main`.
- Commit de origem: `0f08daa66d4bd5576f7c1386de1a8674e974bfba`.
- Árvore: `35f5bae42e363755b9e6dab06516632463d12676`.
- Os **211 arquivos** desse commit foram recuperados e conferidos por tamanho
  e hash de objeto Git, incluindo os dois Flatpaks publicados.
- O Git local foi restaurado com o commit original e histórico raso, equivalente
  a uma cópia com profundidade 1. Na rodada posterior, a consulta autenticada
  `git ls-remote` passou pelo terminal. O conector GitHub não é necessário se
  essa autenticação continuar disponível; conferir novamente antes de publicar.
  Consulte as notas datadas para o resultado do envio e o próximo ponto de retomada.

O checkout foi verificado limpo antes de acrescentar este ponto de retomada,
seus links e o relatório local de verificação. O usuário autorizou publicar a
continuidade no GitHub. O fluxo acordado é desenvolver e testar pelo código-fonte
no Linux e gerar Flatpak nos marcos de entrega.

## Objetivo e decisões preservadas

Desenvolver uma implementação independente com contratos funcionais do Foxit
Reader **2025.2.0.33046 x86** como referência. A base própria MIT
Winux/Print&View e o pypdf distribuído com sua licença já foram integrados.
**Linux/Flatpak tem prioridade; Windows vem depois.** UPDF está fora do escopo.
Em **17/10/2026**, o usuário excluiu também o assistente de IA do Foxit e
recursos generativos: ver [ESCOPO.md](ESCOPO.md). Preservar inventários
históricos, sem investigar ou implementar IA nas próximas rodadas.
Preservar a proveniência e manter código, recursos e decompilações Foxit fora
da implementação e do Git.

A versão de entrega é **0.1.2 de desenvolvimento**, Flatpak `devel`, ID
`io.github.airtonbp19edu.LinuxitPDF`. O leitor já possui navegação, zoom,
rotação, seleção, apresentação, temas, painéis de metadados, busca em texto,
marcadores e comentários, controle dos destaques e preparação de impressão
em livreto/N-up/mosaico.

O roteiro registrado está em **43,33%**. A cobertura global da engenharia
reversa permanece indeterminada e a paridade diferencial comprovada está em
**0/25 famílias identificadas**. A recuperação deste checkout não altera
esses indicadores. O catálogo contém 209 entradas examinadas: 152 REA e 57
adicionais diretas.

Em **17/10/2026**, a [etapa 12](ETAPA-12.md) avançou com contratos das 25
famílias e 50 cenários planejados: 14 descrevem subconjuntos atuais e 11 são
propostas futuras. A fonte estruturada é `docs/especificacao-funcional.json`;
o [registro legível](contratos-funcionais.md) é gerado pelo validador. Dez
verificações portáveis passaram, mas os 50 cenários completos seguem `not_run`.
O detalhamento está `partial`, a fase A continua aberta e a etapa 12 permanece
12,5% verificada. Próximo passo: especializar fixtures e tornar os casos
executáveis, começando por abertura, busca, navegação e prévia; comparar com o
Foxit na mesma fixture quando a VM estiver validada.

A [etapa 13](ETAPA-13.md) foi revisada em **17/10/2026** para a versão 0.1.1:
19 módulos, 11 interfaces e vínculo com as 25 famílias. Seus dois critérios de
projeto já estavam concluídos; permanecem 100% sem fechar a implementação.
O [registro de pendências](../progresso/pendencias-analises.md) cobre os 21
critérios abertos, distingue VM/análise/código/runtime e fixa checkpoints para
interrupções. Timeouts de execução estão documentados; esgotamento de tokens
não foi confirmado nos relatórios examinados. Causas desconhecidas ficam nulas.

A [etapa 14](ETAPA-14.md) foi conferida em **17/10/2026**: o projeto existente
mantém licenças/proveniência e os dois critérios já concluídos. O novo
`scripts/check_project.py` passou em seis controles portáveis de subprocessos
próprios; resultados em `testes/resultados/etapa-14-projeto-2026-10-17.json`.
GUI/Linux/Flatpak não foram repetidos. Próxima etapa do roteiro: 15, com
contratos suficientes e escopo sem IA; demais pendências continuam registradas.

A [etapa 15](ETAPA-15.md) avançou sem VM: listagem/extração própria de anexos
planos pelo worker, com 14 testes portáveis aprovados. A especificação atual
tem 15 subconjuntos e 10 propostas; a arquitetura tem 20 módulos e 13 interfaces.
O critério abrangente da etapa 15 está `partial`, mantendo 33,3% verificados e
roteiro 43,33%. Mudanças somente no código-fonte em desenvolvimento após o
Flatpak 0.1.1. Ainda faltam integração GTK/Linux, portfólios e casos complexos;
a comparação com o original segue pendente da VM/contenção. Próximo passo
concreto: integrar listagem/extração à UI em Linux e testar com o novo corpus.

A [etapa 16](ETAPA-16.md) conectou o painel Anexos ao código GTK, com carga sob
demanda, seleção e escolha de pasta. O controlador portável passou em 14 testes
após corrigir UTF-8 do worker. **Os quatro testes GTK não foram executados**:
faltam GTK/tela e WSL continua não instalado. Critério abrangente `partial`,
sem aumento dos percentuais; código-fonte em desenvolvimento, sem novo Flatpak.
Arquitetura atual: 21 módulos/15 interfaces. Próximo passo: rodar os testes reais
do painel e a suíte completa em Linux com GTK/Poppler e tela, sem exigir a VM
do Foxit. Não promover testes do controlador a validação visual.

## Onde trabalhar

- Interface e ciclo de vida: `app/main.py`.
- Busca, geometria e metadados: `app/search_engine.py`, `app/rendering.py` e
  `app/pdf_panels.py`.
- Listagem/extração de anexos: `app/pdf_attachments.py` e comandos do worker.
- Controle do painel Anexos: `app/attachment_tasks.py`, ligado à janela GTK.
- Impressão e imposição: `app/imposition.py`, `app/print_window.py`,
  `app/worker_cli.py`, `app/cups_backend.py` e `app/windows_print.py`.
- Contratos e arquitetura: `docs/especificacao.md`, `docs/especificacao-funcional.json`,
  `docs/contratos-funcionais.md`, `docs/ETAPA-12.md`, `docs/arquitetura.md`,
  `docs/arquitetura-componentes.json` e `docs/ETAPA-13.md`.
- Investigação: `docs/FOXIT-REA.md`, `docs/REA-BUSCA-IMPRESSAO.md`,
  `docs/relatorio-dinamico.md` e `docs/windows-evidence/foxit-rea/`.
- Agenda e indicadores: `progresso/tarefas-pendentes.md`, `projeto.json`,
  `progresso.json`, `matriz-paridade.csv` e `historico.md`, dentro de `progresso/`.
- Último marco: `relatorio-final.md` e `releases/manifest.json`.

## Verificação nesta máquina

Ambiente de retomada: **Windows, Python 3.13.15**, sem WSL, GTK/PyGObject,
Cairo ou Flatpak disponíveis. A cópia permite editar o projeto e exercitar seus
módulos portáveis. A suíte gráfica exige preparar o ambiente Linux descrito em
`README.md` e `docs/instalacao.md`.

A busca inicial pelo PATH não detectou as ferramentas de análise já instaladas.
A verificação pelos caminhos locais confirmou **REA 6.5.0, Ghidra 12.1.4,
Temurin JDK 21.0.12.1 e Node 24.22.0**. O diagnóstico explícito do provedor
Ghidra passou, incluindo o controle nativo de processos do Windows. O REA é
executado pelo driver MCP do projeto; sua disponibilidade independe de uma
ferramenta REA aparecer diretamente no catálogo deste chat.

Localizações confirmadas:

- Ghidra: `A:\Programas\ghidra_12.1.4_PUBLIC`.
- JDK: `A:\Programas\Eclipse Temurin JDK`.
- Original: `A:\Programas\Foxit PDF Reader\Foxit PDF Reader\FoxitPDFReader.exe`,
  com SHA-256 igual ao registrado em `progresso/projeto.json`.
- Material original adicional: pasta `Desenvolvimento\Foxit` indicada pelo usuário.
- REA: pacote `rea-agents` no cache `_npx` local; obter o caminho atual pelo
  `package.json` e executar `scripts/rea.mjs` pelo Node.

As sessões completas ficam em `analysis-local/`, ignorado pelo Git. O driver
`scripts/rea_mcp_queue.py` aceita `--node <node.exe> --rea <scripts/rea.mjs>`
no Windows. O suporte Ghidra do REA neste sistema é experimental.
O [marco de impressão no Windows](REA-IMPRESSAO-WINDOWS.md) registra o timeout
da análise MCP e as três novas rotinas examinadas com Ghidra direto.
O [marco dos consumidores](REA-IMPRESSAO-CONSUMIDORES.md) acrescenta seis
entradas examinadas e uma conferência independente das instruções com Capstone.
REA 6.5.0 e seus dez controles Ghidra foram reconferidos; o novo projeto fica
em `analysis-local/headless/windows-print-02`. O Git local autenticou em
consulta ao remoto; veja as notas para a confirmação da publicação desta rodada.

Foram aprovadas **7 verificações locais**: sintaxe de 101 arquivos Python;
metadados do PDF sintético; busca em marcadores e seus destinos; busca em
conteúdo/assunto de comentários; palavra inteira Unicode; geração e reabertura
de livreto; hashes SHA-256 dos dois Flatpaks. O relatório está em
`testes/resultados/retomada-windows-2026-10-16.json`.

Os resultados históricos de **37/37 testes na fonte e no payload**, mais
**5/5 verificações no sandbox Flatpak**, foram preservados. A suíte completa
ainda precisa ser executada neste novo ambiente Linux. Esses resultados
históricos e as verificações locais são de implementação própria; a comparação
funcional com o Foxit continua pendente.

## Próxima sequência de trabalho

Consultar primeiro o [registro completo de pendências](../progresso/pendencias-analises.md)
e verificar sua coerência com `python scripts/check_architecture.py`.
Cada lote deve terminar com checkpoint datado e próximo alvo exato. A revisão
da etapa 13 não exige repetir a importação geral nem as rodadas concluídas.

O usuário autorizou avançar a etapa 11 estaticamente enquanto prepara a VM.
[ETAPA-11.md](ETAPA-11.md) registra nove entradas novas, condições de atualização
e uma ambiguidade de IDs que precisa de contexto de classe. Os próximos alvos
da interface são `0x859920`, `0x687ae0`, `0x5f5370` e `0x48f10ef`. Projeto e
resultados completos ficam em `analysis-local/headless/windows-ui-01`. Os dez
cenários de interface continuam sem observação; o preparador os inclui em
campanhas novas. A fração verificada da etapa 11 permanece 25%.

1. Pendência de ambiente: **etapa 10**. A preparação e os 20 cenários estão
   em `docs/ETAPA-10.md`; `scripts/prepare_foxit_dynamic.py` gera o corpus e o kit
   offline. O Windows 11 Home local não oferece Sandbox; WSL não está instalado
   e o usuário não tem VM. Primeiro disponibilizar um guest Windows offline
   descartável ou recuperar a contenção Linux/Wine, sem lançar o original no
   perfil normal do host. Nenhum cenário Foxit foi observado nesta rodada.
2. Continuar as etapas 08/09 de análise dirigida por REA/Ghidra. O executável
   original já foi localizado e validado. O projeto headless do ambiente
   anterior ainda não foi localizado; os caminhos `/workspace/foxit-rea-analysis`
   dos relatórios não existem nesta máquina. Preservar os resumos anteriores e
   registrar separadamente cada novo perfil e resultado.
3. Completar os contratos de busca e impressão antes de ampliar sua implementação.
   Preparar Linux com GTK 3/PyGObject/Cairo, Poppler e clientes CUPS para executar
   `scripts/run_tests.py --output <novo-arquivo.json>` com uma tela disponível.
4. Seguir também a agenda existente: diagnosticar a `CInvalidArgException` do Foxit
   antes da UI, em contenção offline; completar os campos desconhecidos da
   estrutura de busca de 24 bytes; seguir os dez próximos alvos apontados em
   `REA-IMPRESSAO-CONSUMIDORES.md`. Os seis consumidores pendentes do primeiro
   marco Windows já foram examinados; não repetir essa rodada.
5. Executar o mesmo corpus no original e no Linuxit para medir as diferenças.
   Edição/persistência de marcadores, anotações, formulários e outras famílias
   continuam na matriz de pendências.

Atualizar evidências e progresso a cada marco verificado, preservando os pesos
das 21 etapas e o trabalho existente. A análise inicial já está documentada;
continuar a partir dos resultados preservados.
