# Notas de continuidade entre IAs

Registros por rodada, em ordem cronológica. Usar o horário de São Paulo e
preservar as notas anteriores. A sequência técnica completa também está em
`historico.md`, `tarefas-pendentes.md` e `../docs/RETOMADA.md`.

## 2026/10/16 às 20:02 (America/Sao_Paulo, UTC-03:00) — rodada iniciada

Pedido: continuar a engenharia reversa local e no GitHub e sempre deixar uma
nota datada para outras IAs. Checkout inicial limpo em `main`, commit
`62fe1e34d3e589e71974860199f0a756ebcbb41e` (última publicação confirmada na
rodada anterior; a confirmação remota desta rodada ainda está pendente).

REA 6.5.0, Ghidra 12.1.4, JDK Temurin 21.0.12.1 e Node 24.22.0 conferidos.
O diagnóstico explícito do provedor Ghidra passou nos dez controles. Isso não
valida uma interface Foxit isolada nem implica disponibilidade de IDA/Hopper.

Foi iniciada a análise estática complementar das seis entradas de impressão
pendentes: `0x1668750`, `0x1667fe0`, `0x1655e00`, `0x16561c0`, `0x1665780`,
`0x166fe90`. Backend direto Ghidra `-noanalysis` com script de seeds do REA;
não contar como resultado MCP. Resultados completos e projeto separados em
`analysis-local/headless/windows-print-02`, ignorado pelo Git. Ainda não há
novo resultado tecnicamente examinado nesta nota de início.

O conector GitHub usado nas rodadas anteriores apareceu não instalado/não
conectado nesta rodada; foi oferecida a conexão. O Git local também está sendo
verificado sem interação. Publicação nova ainda não confirmada.

A etapa 10 permanece dependente de ambiente offline isolado; os 20 cenários
preparados não foram observados. Nenhuma execução funcional do Foxit nesta
rodada. Manter progresso em 43,33% e paridade 0/25 até evidência suficiente.

Atualização durante a rodada: o Git local autenticou com sucesso em consulta
não interativa e confirmou `62fe1e34d3e589e71974860199f0a756ebcbb41e` no remoto.
É possível tentar a publicação pelo Git normal; o conector não é necessário
para esse caminho. Não há nova publicação confirmada neste ponto do registro.

## 2026/10/16 às 20:14 (America/Sao_Paulo, UTC-03:00) — análise local concluída

As seis entradas pendentes foram descompiladas e examinadas: `0x1668750`,
`0x1667fe0`, `0x1655e00`, `0x16561c0`, `0x1665780` e `0x166fe90`.
O catálogo agora tem **200 entradas distintas (152 REA + 48 diretas)**;
as 194 anteriores e seus manifestos foram preservados.

Avanços: limites e últimos índices de posicionamento; transformação e guarda
de coleção vazia; dois consumidores com destino comum; preparação de fonte
GDI; enumeração de handlers e dois caminhos de saída. Um slot inicialmente
comparado como inteiro foi tipado como float pelo Ghidra por reuso posterior.
Assinaturas e semântica completa continuam provisórias.

Evidências publicáveis: `docs/REA-IMPRESSAO-CONSUMIDORES.md`, metadados em
`docs/windows-evidence/foxit-rea/headless-cross-checks-windows-followup-2026-10-16.json`
e `windows-print-followup-contracts.json` no mesmo diretório. Diagnóstico atual
em `windows-followup-readiness.json`; verificações em
`testes/resultados/rea-consumidores-windows-2026-10-16.json`.
Resultados completos, montagem e projeto ficam somente em
`analysis-local/headless/windows-print-02`. Dependências PeFile/Capstone
instaladas em `analysis-local/python-deps`, sem alteração do Python global.

Verificações: dez controles REA/Ghidra aprovados; seis descompilações completas;
hashes dos resultados conferidos; Capstone confirmou todos os endereços das
1.484 instruções / 4.874 bytes; as importações CreateFontIndirectW/DeleteObject
foram verificadas na tabela PE. Sintaxe Python e links locais conferidos no
relatório. Original intacto, sem execução funcional, sem mudança no leitor e
sem novo Flatpak. Roteiro 43,33%, paridade 0/25, etapa 10 ainda bloqueada.

O gerador de metadados ganhou `--round`, com validação de identidade e recusa
de diretório fora de `evidence-root/headless`. Notas datadas agora são uma
instrução explícita em `AGENTS.md`, conforme o pedido do usuário.

Próximo passo estático: seguir `0x166d050`, `0x165f5d0`, `0x16678c0`,
`0x16678d0`, `0x16678e0`, `0x16678f0`, `0x1665a30`, `0x1664c00`,
`0x2d226d0` e `0x1b5baf0`. A etapa 10 requer primeiro a VM offline descrita
em `docs/COMO-CONTINUAR.md`. Não reiniciar as análises preservadas.

Publicação: consulta Git autenticada confirmou a base remota; envio do novo
marco será feito após esta anotação. A confirmação posterior será acrescentada
ao final deste arquivo com o hash do marco já publicado.

## 2026/10/16 às 20:15 (America/Sao_Paulo, UTC-03:00) — publicação confirmada

Marco técnico publicado em `main`:
[`c696ca939ec1d523786d570a74acd21ae20e11a7`](https://github.com/airtonbp19edu/Linuxit-PDF/commit/c696ca939ec1d523786d570a74acd21ae20e11a7).
O envio pelo Git normal passou, e `git ls-remote origin refs/heads/main`
confirmou esse hash às 20:15. Não foi necessário instalar ou reconectar o
plugin GitHub. O conector pode continuar ausente; a autenticação Git local
funcionou nesta rodada e deve ser reconferida em futuras sessões.

Esta anotação registra um commit já confirmado, sem tentar conter o hash do
próprio commit. Após publicá-la, conferir novamente HEAD local/remoto e árvore
limpa; o comprovante final fica em
`analysis-local/github-round02-sync-verified.json`, fora dos arquivos versionados.
Próximos alvos e limitações são os da nota das 20:14 e do relatório dos
consumidores. Nenhuma atividade da etapa 10 foi marcada como concluída.

## 2026/10/16 às 23:47 (America/Sao_Paulo, UTC-03:00) — início da etapa 11 em paralelo

O usuário pediu avançar a engenharia reversa da interface enquanto prepara a
VM da etapa 10. Base local limpa e remoto reconfirmado em
`acda307e952ba614efe1d2511dd8e162047cc99b`. A etapa 11 tem 25% verificados:
inventário e nove controles ligados ao estado; a observação de todas as
interações ainda depende da execução isolada do original.

Iniciada análise estática de nove entradas ainda não catalogadas, com Ghidra
direto `-noanalysis` e seeds do REA, em novo projeto
`analysis-local/headless/windows-ui-01`. Alvos: `0x803920`, `0x861470`,
`0x85d1a0`, `0x85ddd0`, `0x85de30`, `0x80eab0`, `0x1788db0`, `0x1788e10`
e `0x1788d70`. Não tratar resultados como MCP; não contar antes de examinar.

Preparados um cruzamento contextual das tabelas de comandos com os corpos de
função e dez cenários de observação da interface, todos `not_run`. IDs iguais
em contextos diferentes, propriedades declaradas em templates e conexões de
botões não demonstram disponibilidade no Reader. Nenhum original executado.
Publicação do novo marco ainda pendente desta rodada.

## 2026/10/16 às 23:58 (America/Sao_Paulo, UTC-03:00) — etapa 11 estática examinada

Nove entradas novas examinadas em `analysis-local/headless/windows-ui-01`,
com Ghidra direto `-noanalysis` e seeds REA, sem execução do Foxit. Catálogo:
**209 entradas distintas (152 REA + 57 diretas)**, preservando as 200 anteriores
e três manifestos. As nove descompilações foram examinadas junto à montagem.

Avanços: atualização de Abrir/Imprimir/Próxima página/Zoom/Imprimir todas as
abas e armazenamento de três opções de busca. Zoom nos limites 64 e 0,01
envia desabilitação; outros ramos não habilitam explicitamente. Imprimir todas
as abas exige mais de um objeto aceito por predicado ainda parcial. A tabela
associa os IDs 7911/7913 ao mesmo handler, mas ele escreve somente `+0x1d58`;
o vínculo ao texto das páginas `+0x1d60` permanece ambíguo. Não converter essa
junção estrutural em comportamento comprovado ou mudar o leitor com base nela.

Relatório: `docs/ETAPA-11.md`. Metadados em `docs/windows-evidence/foxit-rea/`:
`headless-cross-checks-ui-2026-10-16.json`, `ui-availability-windows-2026-10-16.json`
e `ui-state-contracts-2026-10-16.json`. Helper novo:
`scripts/catalog_foxit_ui_availability.py`, com identidade, dez registros PE
contextuais e recusa de sobrescrita. Estados/conexões declarados foram reunidos
dos dez metadados FX existentes, sem reextrair ou publicar templates.

Verificações: dez controles REA/Ghidra; nove resultados com hashes conferidos;
Capstone confirmou 242 instruções / 641 bytes; PeFile conferiu importações
e constantes de zoom. Sintaxe de 105 arquivos Python e 32 links conferidos.
Cinco regressões do preparador passaram. Campanha nova em
`analysis-local/dynamic/windows-ui-01`, com guia e dez cenários UI `not_run`,
além dos 20 casos da etapa 10; campanhas anteriores preservadas. Relatório de
validação: `testes/resultados/etapa-11-estatica-windows-2026-10-16.json`.

O critério restante da etapa 11 depende de observação: etapa 11 25%, roteiro
43,33%, paridade 0/25. Sem comportamento novo no aplicativo, suíte GTK completa,
teste diferencial ou Flatpak novo. Próximos alvos: `0x859920`, `0x687ae0`,
`0x5f5370` e `0x48f10ef`; esclarecer classes e IDs 7911/7913. Executar UI01–UI10
com D01–D20 quando a VM estiver validada. Publicação será confirmada a seguir
com o hash do marco já verificado.

## 2026/10/16 às 23:59 (America/Sao_Paulo, UTC-03:00) — etapa 11 publicada

Marco técnico publicado e confirmado por `git ls-remote`:
[`62f9925d2f8c7ec722371671b27b527aea2e888e`](https://github.com/airtonbp19edu/Linuxit-PDF/commit/62f9925d2f8c7ec722371671b27b527aea2e888e).
A árvore estava limpa após o envio. Esta nota registra um hash já confirmado;
o commit da própria nota será verificado depois, sem autorreferência. Comprovante
final em `analysis-local/github-ui-sync-verified.json`, fora dos arquivos
versionados. Continuar pelos alvos/ressalvas da nota das 23:58; observação da
interface na VM continua pendente, sem aumentar artificialmente os indicadores.

## 2026/10/17 às 00:12 (America/Sao_Paulo, UTC-03:00) — etapa 12: contratos detalhados

O usuário pediu avançar a etapa 12 enquanto prepara a VM. Base local/remota
conferida em `4a298a103efbecd8c58313723cd4861895f8dd20`. Detalhadas as 25 famílias
da matriz em `docs/especificacao-funcional.json`; registro derivado em
`docs/contratos-funcionais.md` e limites em `docs/ETAPA-12.md`. Há 50 cenários
planejados, um nominal e um excepcional por família: 14 famílias descrevem
subconjuntos atuais, 11 permanecem propostas futuras. Escopos, entradas, saídas,
erros, efeitos, fontes, testes e lacunas explicitados. Valores esperados e
observados no Foxit permanecem `null`; todos os 50 casos completos `not_run`.

Ferramentas desta rodada: Python 3.13.15, AST, Git e módulos portáveis próprios
com pypdf BSD já incluído. Nenhuma nova sessão REA/Ghidra, função do original
examinada ou execução do Foxit. Catálogo preservado em 209 entradas. Materiais
REA/Ghidra anteriores usados como referências estáticas, sem recontagem.

Verificações: `scripts/validate_functional_spec.py` conferiu os IDs/estados da
matriz, 19 referências distintas a testes e 25 fontes locais, IDs D/UI, fixtures
existentes e coerência JSON/Markdown. Sete recusas de evidências inválidas
passaram. Dez verificações portáveis de subcondições passaram: inspeção,
destinos de marcadores, campos de comentários, limites/estados de busca,
fronteiras Unicode, mudança do PDF, ordem de faces do livreto, N-up inválido e
PDF vazio. Sintaxe de 106 arquivos Python e 127 links locais conferidos.
Relatório publicável: `testes/resultados/etapa-12-especificacao-2026-10-17.json`.
Scripts auxiliares/resultados completos preservados em
`analysis-local/check_stage12_source.py`, `analysis-local/finalize_stage12.py`
e `analysis-local/stage12-source-checks/`, ignorados pelo Git.

O detalhamento da etapa 12 passa de `pending` a `partial`; consolidação da
fase A continua pendente. Pesos/revisão não mudaram: etapa 12 12,5%, roteiro
43,33%, paridade 0/25 e cobertura global desconhecida. Dez verificações
portáveis não executam os 50 planos completos nem repetem a suíte GTK no Linux.
Sem alteração de comportamento do aplicativo, novo pacote ou versão.

Próximo passo: especializar o corpus e tornar os cenários executáveis por
família; iniciar por abertura, busca, navegação e prévia. Quando a VM estiver
validada, observar a mesma fixture no original e comparar resultados. Confirmar
disponibilidade Reader para famílias futuras e resolver lacunas estáticas de
busca/interface/impressão antes de promover propostas a contratos recuperados.
Publicação deste marco ainda pendente; a nota seguinte registrará somente
um hash cuja presença no remoto tenha sido conferida.

## 2026/10/17 às 00:13 (America/Sao_Paulo, UTC-03:00) — etapa 12 publicada

Marco técnico enviado por Git normal e confirmado por `git ls-remote`:
[`76893ea50b3465c426413d4229b981c46bf06550`](https://github.com/airtonbp19edu/Linuxit-PDF/commit/76893ea50b3465c426413d4229b981c46bf06550).
Árvore limpa após o envio; autenticação Git disponível. Esta nota registra um
hash já confirmado; o commit da própria nota será verificado depois, sem
autorreferência. Comprovante final em
`analysis-local/github-stage12-sync-verified.json`, ignorado pelo Git.
Continuar pelos contratos/ressalvas da nota das 00:12 e por `docs/ETAPA-12.md`;
os 50 casos completos permanecem planejados, a fase A aberta e os indicadores
preservados. Nenhum bloqueio de publicação nesta rodada.

## 2026/10/17 às 00:23 (America/Sao_Paulo, UTC-03:00) — etapa 13 e pendências de análise

O usuário pediu seguir a etapa 13 e registrar etapas parciais por falta da VM
ou possíveis limites de tokens. Base local limpa e remoto confirmados em
`052da732b410fa9919d4050a21d4f1e1eb8bafdb`. Os dois critérios de projeto da etapa
13 já estavam `done`; foram reexaminados e detalhados para a versão 0.1.1.
Não houve mudança de critérios, pesos, revisão ou estados das atividades.

Entregas: `docs/ETAPA-13.md`, revisão de `docs/arquitetura.md` e inventário em
`docs/arquitetura-componentes.json`, com 19 módulos próprios, 11 interfaces e
vínculo com as 25 famílias da etapa 12. As propostas permanecem futuras.
O ciclo adiado rendering/search_engine, a coordenação ainda nas janelas e a
diferença entre cancelamento cooperativo, entrega por geração e timeout de
subprocesso foram explicitados. Inspeção do código confirmou import condicional
Cairo em `imposition._merge_poster_marks`: se indisponível, o ramo retorna sem
marcas/legendas. Esse módulo foi excluído da garantia de fechamento sem
GTK/Cairo; sete módulos satisfazem a checagem de imports local. Não alterar a
implementação por uma suposição de arquitetura idealizada.

`progresso/pendencias-analises.md` e `.json` cobrem exatamente os 21 critérios
ainda abertos em 14 etapas, com estado atual, motivo/evidência e próximo passo.
Dependência direta de observação/comparação do original: 10/11/12/18/19; a 21
depende também desses resultados. 11/12 têm trabalho sem VM; 03/05/07/08/09
ainda exigem análise, 15/16 implementação/integração e 01 acesso a regras pela
API. Não atribuir todas as pendências à VM. A etapa 13 de projeto está verificada
pelos critérios existentes e não se torna parcial por falta dela.

Relatórios examinados comprovam provider_timeout após 1.801,7 s e tentativa
MCP automática limitada a 600 s; não comprovam esgotamento de tokens. A lista
de eventos confirmados de tokens fica vazia e o campo por pendência `null`.
Não há afirmação sobre o conteúdo dos chats perdidos. Risco de interrupção
futura de contexto/tokens tratado com checkpoint após cada lote e antes de
mudar de etapa: identidade, perfil, alvos examinados/pendentes, evidências,
último resultado conferido, próxima ação, causa comprovada ou nula e Git.

Ferramentas: Python 3.13.15, AST e Git; nenhuma sessão nova REA/Ghidra ou
execução Foxit. `scripts/check_architecture.py` conferiu módulos/símbolos,
fechamentos de imports, famílias e completude do registro de pendências.
Resultado examinado em `testes/resultados/etapa-13-arquitetura-2026-10-17.json`:
hashes dos 19 módulos, 18 arquivos de evidência de pendências, sintaxe de 107
arquivos e 72 links locais conferidos. Registro da etapa 12 continua válido.
Comparação com o progresso do commit base confirmou critérios/estados/pesos
preservados. Auxiliares em `analysis-local/build_stage13_records.py` e
`analysis-local/finalize_stage13.py`, ignorados pelo Git.

Etapa 13: 100% dos dois critérios de projeto; roteiro 43,33%, paridade 0/25,
catálogo 209. Fonte do aplicativo inalterada, sem suíte GTK repetida ou Flatpak
novo. Próximo passo sem VM: especializar fixtures e tornar os casos próprios
da etapa 12 executáveis, incluindo marcas/legendas de mosaico em Linux/Cairo;
para análise estática seguir os quatro helpers da interface e os dez alvos
de impressão já registrados. Na VM validada, observar D01–D20 e UI01–UI10.
Publicação do marco ainda pendente; a nota seguinte registrará um hash já
confirmado no remoto, e o comprovante final ficará fora dos arquivos versionados.

## 2026/10/17 às 00:24 (America/Sao_Paulo, UTC-03:00) — etapa 13 publicada

Marco técnico publicado por Git normal e confirmado com `git ls-remote`:
[`6cb0820be25b8a1e56f4106642b3fce528af1182`](https://github.com/airtonbp19edu/Linuxit-PDF/commit/6cb0820be25b8a1e56f4106642b3fce528af1182).
Árvore limpa após o envio. Esta nota registra um hash previamente confirmado;
o commit da própria nota será verificado ao fim, sem autorreferência.
Comprovante final: `analysis-local/github-stage13-sync-verified.json`, ignorado
pelo Git. Sem bloqueio de publicação nesta rodada. Retomar pelo registro de
pendências e checkpoint da nota das 00:23; não repetir análises concluídas,
atribuir lacunas a tokens sem prova ou contar planejamento como implementação.

## 2026/10/17 às 00:32 (America/Sao_Paulo, UTC-03:00) — escopo sem IA e etapa 14

O usuário declarou zero interesse na IA integrada do Foxit, autorizou deixá-la
de fora e pediu seguir à etapa 14. Base local limpa e remoto confirmados em
`791ae8e5eb8b7e2dc3bc6d276ccf8345f5a8ef0a`. A exclusão é explícita em
`docs/ESCOPO.md`, `scope_exclusions` de `progresso/projeto.json` e `AGENTS.md`:
assistente IA e recursos generativos ficam fora de análise, implementação e
paridade futuras. Chat/resumo/tradução/explicação por IA estão incluídos na
exclusão. Os registros gerais anteriores de `plugins/AiAssistant.fpi` e rótulos
são preservados como inventário incidental; não foram alvos das últimas
rodadas dirigidas. Nenhum recurso de IA foi implementado no Linuxit.

As 25 famílias existentes não tinham obrigação dedicada de IA; matriz e
catálogo ficaram byte a byte preservados após normalização de fim de linha.
Operações PDF e colaboração sem IA continuam no escopo. Pesos, nomes/estados
dos critérios e revisão do roteiro não mudaram. Especificação, arquitetura e
pendências apontam à mesma decisão; verificadores rejeitam divergência de
escopo. O hash do pedido inicial foi mantido como proveniência histórica.

Etapa 14: o projeto já estava criado e seus dois critérios `done`. Conservaram-se
a base MIT, proveniência Winux/Print&View, pypdf 6.20.1 BSD, estrutura e pontos
de entrada. Relatório e instruções em `docs/ETAPA-14.md`.
Novo `scripts/check_project.py` confere arquivos essenciais, licenças, versão,
entrada Linux e executa seis controles portáveis de worker em subprocessos:
info, painéis, livreto, comando ausente, JSON inválido e PDF vazio. **6/6
passaram**, com reabertura real do PDF gerado; fixture/arquivos conferidos
inalterados. Logs e PDFs em `analysis-local/project-stage14-2026-10-17/`,
ignorados pelo Git; resultado publicável em
`testes/resultados/etapa-14-projeto-2026-10-17.json`.

Ferramentas: Python 3.13.15, pypdf vendorizado, AST e Git; nenhuma sessão nova
REA/Ghidra nem execução Foxit. Duas verificações de recusa por escopo passaram;
arquitetura e registro da etapa 12 continuam válidos. Sintaxe de 108 arquivos
e 189 links locais conferidos. A comparação com o commit base confirmou
os 19 módulos do app, matriz e catálogo inalterados e critérios/pesos/estados
preservados. Auxiliares da rodada em `analysis-local/record_stage14_scope.py`
e `analysis-local/finalize_stage14.py`, ignorados pelo Git.

O ambiente Python/PATH examinado não tem gi/Cairo/cryptography, Poppler, CUPS
ou Flatpak; Pillow está disponível. GUI, marcas Cairo de mosaico, impressão
física e os 50 cenários completos não foram executados. Os resultados Linux
37/37, payload 37/37 e sandbox 5/5 continuam históricos; não foram repetidos.
Etapa 14 mantém 100% dos critérios existentes, roteiro 43,33%, paridade 0/25
e catálogo 209; sem versão/pacote novo. Pendências de VM/análise e causas de
interrupção desconhecidas continuam no registro, sem atribuir esgotamento de
tokens onde não foi comprovado.

Próxima etapa do roteiro: 15, lógica principal por contratos suficientes,
dentro do escopo sem IA. Retomar os cenários próprios/corpus e alvos estáticos
já registrados; observar D01–D20/UI01–UI10 somente na contenção offline validada.
Publicação deste marco ainda pendente; a nota seguinte registrará um hash
confirmado no remoto e o comprovante final ficará em `analysis-local/`.

## 2026/10/17 às 00:33 (America/Sao_Paulo, UTC-03:00) — etapa 14 e escopo publicados

Marco técnico enviado por Git normal e confirmado por `git ls-remote`:
[`39e176cc3665abcc48f73f0e52f55492032f1871`](https://github.com/airtonbp19edu/Linuxit-PDF/commit/39e176cc3665abcc48f73f0e52f55492032f1871).
Árvore limpa após o envio. Esta nota usa um hash já confirmado; o commit da
própria nota será conferido ao fim, sem autorreferência. Comprovante final em
`analysis-local/github-stage14-sync-verified.json`, ignorado pelo Git. Sem
bloqueio de publicação nesta rodada. Retomar pela nota das 00:32 e pela etapa
15 quando autorizada, preservando a exclusão da IA, os critérios existentes
e as pendências de análise/VM.

## 2026/10/17 às 00:47 (America/Sao_Paulo, UTC-03:00) — etapa 15: anexos planos sem VM

O usuário pediu a próxima etapa que não dependesse de VM. Retomada a etapa 15,
com base local limpa e remoto confirmado em
`4db1b254079ddde86a0c3779937432d8da518e08`. Implementado contrato próprio de
listagem/extração local de anexos planos em `app/pdf_attachments.py`, com o pypdf
BSD já incluído; nenhuma análise nova do Foxit ou recurso de IA.

O worker recebeu `attachments` e `extract-attachment`. Listagem mantém índices
distintos para nomes duplicados e não decodifica payloads. Extração exige o
SHA-256 da listagem, revalida identidade, recusa nomes perigosos e grava com
criação exclusiva, preservando destinos existentes e o PDF. Retorna tamanho
real/hash; não executa anexos. Limites próprios: 1.000 entradas na listagem,
64 MiB no payload real após decodificação. Esse limite não garante memória
máxima do parser. Pasta de saída deve ser controlada pelo usuário.

Subconjunto explícito: catálogo plano `/Names/EmbeddedFiles`; /Collection,
/Kids e senha não vazia retornam erro. GUI, portfólios, anexos exclusivos de
anotações e busca em anexos continuam pendentes. Código-fonte em desenvolvimento
após o Flatpak 0.1.1; não foi gerado pacote nem declarada versão estável nova.
Contrato/uso: `docs/ETAPA-15.md`; matriz e especificação atualizadas somente para
a família attachments: 15 subconjuntos/10 propostas, ainda 25 famílias abertas.
Os 50 planos completos de comparação não foram encerrados por testes próprios.

Ferramentas: Python 3.13.15, pypdf 6.20.1, unittest, AST e Git no Windows atual.
Nenhuma sessão nova REA/Ghidra ou execução do original. Catálogo original
preservado em 209 entradas. Arquitetura atual: 20 módulos/13 interfaces, oito
fechamentos locais sem gi/Cairo. O verificador estrutural passa a declarar
ausência de teste de comportamento pela checagem, em vez de afirmar que o
comportamento do aplicativo não mudou em rodadas futuras.

**14/14 testes portáveis passaram**, sem skips: bytes/hash/original, nomes
duplicados/perigosos, conflitos, identidade antes/durante leitura, limites,
PDF inválido, recursos não suportados e protocolo real de subprocesso. Seis
regressões dos comandos anteriores também passaram. Corpus público próprio em
`testes/fixtures/anexos-simples.pdf` e `.json`, com extração e hashes conferidos
em `analysis-local/stage15-fixture-check/`. Sintaxe de 110 arquivos Python e
213 links locais conferidos; registros de arquitetura/especificação válidos.

Resultados publicáveis: `testes/resultados/etapa-15-anexos-tests-2026-10-17.json`,
`etapa-15-worker-regression-2026-10-17.json` e `etapa-15-anexos-2026-10-17.json`.
O último conserva hashes de fontes, testes, corpus e limites. Auxiliares em
`analysis-local/record_stage15_contract.py`, `verify_stage15.py` e
`check_stage15_links.py`; logs anteriores em
`analysis-local/project-stage15-regression-2026-10-17/`, ignorados pelo Git.

A primeira tentativa de 12 testes falhou ainda no setUp por WinError 5 na
pasta temporária do sandbox. Não era falha funcional do backend nem limite
de tokens. Os testes passaram usando pasta gravável do projeto; o runner agora
aceita `--pattern` e `--temp-dir`, sem mudar a seleção padrão da suíte completa,
e registra explicitamente a execução de subconjunto. Rodada final:
`python scripts/run_tests.py --pattern test_pdf_attachments.py --temp-dir analysis-local/test-temp-stage15-final --output testes/resultados/etapa-15-anexos-tests-2026-10-17.json`.
Preservar relatórios existentes e usar nomes novos ao repetir.

Critério amplo da etapa 15: `pending` → `partial`; pesos, nomes e revisão
inalterados. Fração da 15 permanece 33,3%, roteiro 43,33%, paridade 0/25.
Nenhuma suíte completa GTK/Linux, comparação Foxit, impressão física ou Flatpak
repetida; as pendências de VM permanecem separadas das de implementação.
Próximo passo sem VM: integrar listagem/extração em GTK/Linux e exercitar UI
com o corpus; ampliar portfólios/árvores complexas só com contratos próprios
suficientes. Publicação deste marco ainda pendente; nota seguinte usará hash
já confirmado e comprovante final fora dos arquivos versionados.

## 2026/10/17 às 00:49 (America/Sao_Paulo, UTC-03:00) — etapa 15 publicada

Marco técnico enviado por Git normal e confirmado por `git ls-remote`:
[`8dc53c2aa96ada4dc5e8fa12963841f94188115d`](https://github.com/airtonbp19edu/Linuxit-PDF/commit/8dc53c2aa96ada4dc5e8fa12963841f94188115d).
Árvore limpa após o envio. Esta nota usa hash já confirmado; o commit da própria
nota será conferido depois, sem autorreferência. Comprovante final em
`analysis-local/github-stage15-sync-verified.json`, ignorado pelo Git. Sem
bloqueio de publicação nesta rodada. Retomar pela nota das 00:47 e
`docs/ETAPA-15.md`: integração GTK/Linux do backend e casos complexos pendentes,
mantendo a exclusão da IA, as limitações de teste e o Flatpak 0.1.1 anterior.

## 2026/10/17 às 01:06 (America/Sao_Paulo, UTC-03:00) — etapa 16: painel Anexos no código

O usuário pediu a próxima etapa sem VM. Avançada a integração da etapa 16,
com base local limpa e remoto confirmado em
`b065c9928b50c191ba7458328754104ed8eda6eb`. Painel Anexos adicionado à barra
lateral e Exibir em `app/main.py`, com Atualizar, seleção e Salvar selecionado…
para pasta escolhida. Código-fonte após o Flatpak 0.1.1, sem pacote novo.

Novo `app/attachment_tasks.py` coordena carga sob demanda, seleção imutável
por geração/documento/índice/hash e mensagens/status. Callbacks obsoletos não
substituem o documento atual; atualizar a lista ou trocar documento durante
o diálogo invalida a seleção anterior. Cancelar não grava. Extração já
confirmada pode concluir após trocar documento, sem substituir o status do
novo; fechar janela bloqueia tarefas ainda não iniciadas/callbacks, sem
prometer parar subprocesso já iniciado. Nomes recusados ficam visíveis com
motivo e botão desativado. Não há abertura/execução automática do conteúdo.

**14/14 testes portáveis do controlador passaram**, com callbacks adiados
controlados e workers reais sobre PDFs próprios. Cobrem concorrência, seleção,
erros e efeitos em arquivo. A primeira rodada foi 13/14: stderr acentuado era
decodificado incorretamente no Windows. O comando do worker usa agora `-X utf8`;
o teste de erro de portfólio passou na rodada corrigida. Ambos os relatórios
foram preservados; isso é falha/correção de codificação, não esgotamento de tokens.

**0 testes GTK aprovados; 4 skipped.** São casos reais de painel/salvar/conflito,
cancelar pasta, mudar documento durante diálogo e nome inválido em
`tests/test_attachment_panel_gtk.py`. Não foram executados por ausência de
gi/Cairo/tela. Os testes portáveis usam runner controlado e não validam layout,
widgets nem dispatch GLib real. Não transformar esses resultados em aprovação
da GUI. `wsl --list --quiet` reconfirmou WSL não instalado, sem instalá-lo.

Ferramentas: Python 3.13.15, unittest, AST e Git; nenhuma sessão nova REA/Ghidra,
observação do original ou recurso IA. Backend `pdf_attachments.py`, worker CLI,
catálogo original e decisão de escopo preservados em relação à base. Arquitetura
atual: 21 módulos/15 referências de interfaces, nove fechamentos locais sem
gi/Cairo. Especificação/matriz seguem 25 famílias, 15 subconjuntos/10 propostas.
Sintaxe de 113 arquivos e 221 links locais conferidos, além das ligações AST
da janela a criação/carga/limpeza/fechamento/salvamento do painel. Ligações AST
também não executam GTK. Pesos e revisão preservados; somente o critério amplo
da etapa 16 mudou `pending` → `partial`.

Relatório: `docs/ETAPA-16.md`. Evidências em `testes/resultados/`:
`etapa-16-controlador-tests-2026-10-17.json`,
`etapa-16-controlador-tests-fixed-2026-10-17.json`,
`etapa-16-gtk-disponibilidade-2026-10-17.json` e
`etapa-16-painel-anexos-2026-10-17.json`. O resumo conserva hashes das fontes,
status pass/fail/skip separados e limitações. Dados locais/diagnóstico bruto
em `analysis-local/stage16-verification/`; coletor ajustado para ler também
stderr UTF-16 do WSL, preservando o registro original. Auxiliares em
`analysis-local/record_stage16_contract.py` e `verify_stage16.py`, ignorados.

Etapa 16 mantém 33,3% verificados, roteiro 43,33%, catálogo Foxit 209 e paridade
0/25. Sem suíte completa Linux, renderização visual do novo painel, impressão
física ou Flatpak novo. Próximo passo sem VM do Foxit: executar os quatro testes
GTK e a suíte completa em Linux com GTK/Poppler e tela, inspecionar o painel e
corrigir achados. As pendências do runtime Linux e da VM do original continuam
separadas. Publicação deste marco ainda pendente; a nota seguinte usará hash
previamente confirmado e o comprovante final ficará fora dos arquivos versionados.

## 2026/10/17 às 01:08 (America/Sao_Paulo, UTC-03:00) — etapa 16 publicada

Marco técnico publicado por Git normal e confirmado por `git ls-remote`:
[`73f7786883c183ea948bf45dcdc427f308c2894d`](https://github.com/airtonbp19edu/Linuxit-PDF/commit/73f7786883c183ea948bf45dcdc427f308c2894d).
Árvore limpa após o envio. Esta nota usa hash já confirmado; o commit da
própria nota será conferido ao fim, sem autorreferência. Comprovante final em
`analysis-local/github-stage16-sync-verified.json`, ignorado pelo Git. Sem
bloqueio de publicação. Retomar pela nota das 01:06 e `docs/ETAPA-16.md`,
preservando a distinção entre 14 testes portáveis aprovados e quatro GTK
sem execução, a exclusão da IA e o Flatpak 0.1.1 do marco anterior.

## 2026/10/17 às 01:28 (America/Sao_Paulo, UTC-03:00) — etapa 17, cópia intermediária da fonte

Pedido atual: próxima etapa sem depender da VM do Foxit. Criado
`scripts/check_intermediate.py`, com perfis `portable` e `linux`. Uma cópia
isolada de `app/` e avisos MIT/BSD fica em diretório novo sob `analysis-local/`;
hashes são conferidos antes/depois dos testes. Não é instalador nem pacote
Flatpak. Testes/runner continuam no checkout e recebem a cópia por
`PRINT_VIEW_TEST_APP`. Sem alterações ao código do aplicativo nesta rodada.

**80 módulos Python da cópia compilaram; 32/32 testes portáveis passaram**,
sem falhas/skips: 14 do backend, 14 do controlador e quatro do verificador.
Workers reais e PDFs próprios verificam listagem, extração e estados de erro.
Os quatro controles do verificador rejeitam app diferente, contagens/casos
inconsistentes, skips, suíte vazia/incompleta e alterações na fonte. Isso não
valida GUI/Linux. O perfil `portable` registra `linux_source_runtime_passed: false`.

O perfil `linux` foi exercitado neste Windows e retornou erro esperado de
pré-requisitos, **zero testes Linux executados/aprovados**. Ele exige Linux,
GTK/PyGObject/Cairo e ponte GI, Pillow/cryptography, Poppler/CUPS e X11 funcional;
depois exige suíte completa sem skips e cinco verificações GTK reais. Os quatro
casos do painel da etapa 16 continuam sem execução. Usar `/usr/bin/python3`
em Linux; X11/Xwayland ou `xvfb-run` porque testes antigos dependem de DISPLAY.

Comparação de hashes com o manifesto preservado do payload 0.1.1:
2 arquivos novos, 2 alterados,
0 removidos, 79 iguais. Não foi feita nova
extração do Flatpak. Manifesto/pacote publicado 0.1.1/devel preservados. A
fonte pós-0.1.1 ainda precisa de validação Linux e novo empacotamento.

Ferramentas: Python 3.13.15, py_compile, unittest, SHA-256 e Git. Nenhuma nova
sessão REA/Ghidra ou execução original; IA/generativos continuam excluídos.
Evidências publicáveis: `docs/ETAPA-17.md`, `testes/resultados/etapa-17-fonte-portavel-2026-10-17.json` e `testes/resultados/etapa-17-linux-indisponivel-2026-10-17.json`.
Cópias/bytecode/logs privados em `analysis-local/intermediate-stage17-portable/`
e `analysis-local/intermediate-stage17-linux/`. Este coletor local só registra
evidências examinadas e preserva critérios/pesos. Não houve esgotamento de
tokens confirmado. As pendências da VM do original e do runtime Linux são distintas.

Os critérios históricos da 17 já estavam `done` pela versão 0.1.1; não usá-los
como aprovação do novo painel. Novo campo `current_source_revalidation`
registra o checkpoint parcial sem mudar nenhum critério/status/peso/revisão.
Roteiro 43,33%, paridade 0/25, catálogo 209, cobertura global desconhecida/null.
Próximo passo: executar o perfil Linux, corrigir achados e inspecionar o painel,
então gerar/testar o Flatpak do novo marco. Etapa 18 diferencial aguarda o
original em contenção offline; preparação própria não conta como paridade.
Publicação desta rodada pendente; confirmar o remoto e registrar hash já
verificado em nota posterior, sem autorreferência.

Conferência adicional às 01:29: dois controles CLI recusaram diretório e
relatório existentes com saída 2, sem sobrescrever nada. Sintaxe de 115 arquivos
Python e 58 links locais passou, além de arquitetura e contratos. Resumo em
`testes/resultados/etapa-17-verificacao-2026-10-17.json`, com hashes do novo
verificador/teste. Todas as fontes do aplicativo e os pacotes publicados são
idênticos ao HEAD anterior; critérios/status/pesos/revisão também preservados.

## 2026/10/17 às 01:31 (America/Sao_Paulo, UTC-03:00) — etapa 17 publicada

Marco técnico enviado por Git normal e confirmado por `git ls-remote`:
[`6ab035f0f598542ab11b81de838bcfd4d5381991`](https://github.com/airtonbp19edu/Linuxit-PDF/commit/6ab035f0f598542ab11b81de838bcfd4d5381991).
HEAD local/remoto iguais e árvore limpa após o envio. Esta nota registra hash
já verificado; o commit da própria nota será conferido ao fim, sem
autorreferência. Comprovante final em
`analysis-local/github-stage17-sync-verified.json`, ignorado pelo Git.
Sem bloqueio de publicação. Retomar por `docs/ETAPA-17.md` e pela nota das 01:28:
32 testes portáveis aprovados; execução Linux/GTK da fonte atual e Flatpak
novo pendentes. A VM do Foxit continua necessária só para a observação do
original e comparação diferencial. IA excluída; pacote publicado 0.1.1/devel
e todos os critérios/pesos preservados.

## 2026/10/17 às 01:50 (America/Sao_Paulo, UTC-03:00) — etapa 18, campanha comparativa preparada

Pedido: próxima etapa sem depender da VM. Criados `testes/plano-comparativo.json`
e `scripts/run_comparison_campaign.py`: 17 verificações de subconjuntos do
backend ligadas aos cenários D existentes e seis das 25 famílias. O corpus da
etapa 10 foi reutilizado pelo gerador próprio, sem abrir/importar originais.
Fonte do aplicativo, licenças e Flatpak 0.1.1/devel não foram modificados.

**13 verificações próprias passaram; quatro bloqueadas por falta de pdftotext**.
Resultados examinados: duas páginas; marcadores em página 2/null; comentários
e assunto em página 1; autor, consulta vazia/inexistente/sem fontes com zero;
PDF inválido/vazio recusados pelo parser; anexo salvo com 22 bytes/hash; livreto
com quatro páginas e rótulos 8,1/2,7/6,3/4,5; N-up com duas páginas e rótulos
1,2,3,4/5,6,7,8. Ordem extraída do conteúdo PDF não prova posicionamento visual,
margens, geometria ou impressão física. D04/D05/D06/D10 continuam com medidas
null e `blocked_runtime`. Não foi simulada extração de texto para aprová-los.

**16 testes do comparador passaram**, com registros/evidências inventados para
controle, nunca Foxit. Cobrem integridade/vínculo de fixture e protocolo,
identidade antes/depois e sessão offline declarada, evidência ausente/alterada,
caminho externo, duplicatas, valores desconhecidos/contagens incoerentes,
destino base 1/null e ordem. Mostram que esperado próprio não vira observado
original, erro/indisponibilidade são inconclusivos e app bloqueado não compara.
Uma primeira bateria de 14 passou; a ampliação para 16 fortaleceu o vínculo
do protocolo da própria campanha e a distinção entre tipos. Ambos preservados.

Execução CLI com modelo original vazio confirmou **0 medidas Foxit, 0 matches,
0 diferenças e 17 aguardando original**. O importador futuro valida registros
e hashes, sem iniciar o original e sem provar sozinho a origem da evidência
manual. Igualdade das medidas registradas precisa de revisão; não aprova
família nem altera automaticamente a paridade. Exit 0 no compare indica
importação válida, inclusive se houver diferenças. Corpus/protocolo devem ser
os mesmos nas duas observações; o modelo tem medidas originais null.

Ferramentas/perfis: Python 3.13.15, subprocessos sobre APIs reais próprias,
pypdf BSD 6.20.1, unittest, SHA-256 e Git; Windows, sem GTK/Poppler/WSL utilizável
no checkpoint anterior. Nenhuma nova sessão REA/Ghidra, execução do original,
GUI Linux, pacote ou impressão física. IA/generativos continuam excluídos.
Nenhum esgotamento de tokens confirmado; lacunas continuam classificadas por
VM/observação/implementação/runtime, com causas de tokens null.

Evidências publicáveis: `docs/ETAPA-18.md`, plano e relatórios
`testes/resultados/etapa-18-campanha-2026-10-17.json`,
`etapa-18-campanha-final-2026-10-17.json`,
`etapa-18-controles-tests-2026-10-17.json`,
`etapa-18-controles-extended-tests-2026-10-17.json` e
`etapa-18-comparacao-sem-original-2026-10-17.json` nessa pasta.
Dados completos privados: `analysis-local/comparison-stage18/` e
`analysis-local/comparison-stage18-final/` (corpus `input/`, saídas/probes e
modelo `foxit-observations-template.json`). Conservar a pasta final para a VM;
copiar plano/modelo para input antes de compartilhá-la somente leitura.

Critérios/status/pesos/revisão preservados; método já done recebe evidências,
os dois critérios diferenciais seguem pending e o checkpoint de preparação é
partial separado. Todos os 20 casos dinâmicos completos e os 50 de aceitação
seguem sem execução completa; não usar os 13 subconjuntos como esses casos.
Etapa 18 10%, roteiro 43,33%, paridade 0/25, catálogo 209, cobertura global
desconhecida/null. Pendências/retomada atualizadas, sem mudar a matriz.

Próximo passo: rodar a campanha com Poppler em Linux e a validação GTK da etapa
17; quando a VM estiver pronta, observar exatamente o mesmo corpus e opções,
importar e revisar as evidências. Etapa 19 diferencial só avança após medir
divergências originais. Publicação desta rodada ainda pendente; confirmar o
remoto e acrescentar uma nota com hash já verificado, sem autorreferência.

O auxiliar local de registro encontrou inicialmente KeyError ao usar `items`
em vez da chave existente `unfinished_criteria`; corrigido antes da nota e da
verificação final. Isso não foi erro de execução do aplicativo nem limite de tokens.

Conferência adicional às 01:51: sintaxe de 117 arquivos Python e 91 links locais
aprovados; CLI recusou relatório/diretório existentes e protocolo divergente,
sem sobrescrita ou relatório enganoso. Arquitetura e contratos coerentes;
83 arquivos da aplicação, pacotes, planos D/UI/S12 e todos os critérios/status/
pesos/revisão idênticos à base. Resumo com hashes em
`testes/resultados/etapa-18-verificacao-2026-10-17.json`.
Plano e modelo vazio já foram copiados, com hashes conferidos, para
`analysis-local/comparison-stage18-final/input/plano-comparativo.json` e
`observacoes-comparativas-template.json` nessa pasta. São dois arquivos de
instrução/coleta adicionais, não novas fixtures PDF; os oito arquivos do
corpus original da campanha seguem intactos. Diretório pronto para o futuro
mount somente leitura; observações preenchidas devem ir para Results na VM.

## 2026/10/17 às 01:53 (America/Sao_Paulo, UTC-03:00) — etapa 18 publicada

Marco técnico enviado por Git normal e confirmado por `git ls-remote`:
[`65d9c685084018e336644f4f8bebf1928bc71cfa`](https://github.com/airtonbp19edu/Linuxit-PDF/commit/65d9c685084018e336644f4f8bebf1928bc71cfa).
HEAD local/remoto iguais e árvore limpa após o envio. Esta nota usa o hash já
verificado; seu próprio commit será conferido ao fim, sem autorreferência.
Comprovante final em `analysis-local/github-stage18-sync-verified.json`,
ignorado pelo Git. Sem bloqueio de publicação. Retomar por `docs/ETAPA-18.md`
e pela nota das 01:50: 13 subconjuntos próprios aprovados, quatro bloqueados por
Poppler, 16 testes sintéticos do comparador aprovados e zero comparações reais
Foxit. Kit local preservado na pasta da campanha final, com plano/modelo em
input; preparar runtime Linux e depois a observação do original na VM offline.
Critérios diferenciais ainda pendentes; IA excluída e Flatpak 0.1.1 preservado.

## 2026/10/17 às 10:06 (America/Sao_Paulo, UTC-03:00) — etapa 19, duas correções próprias de impressão

Pedido: próxima etapa, sem VM disponível no checkpoint anterior. Reproduzidos
dois defeitos do código próprio de imposição: origem de CropBox ignorada na
colocação do conteúdo e mutação do stream de uma página do reader em memória
durante normalização da rotação. Corrigidos em `app/imposition.py`: cópia
desvinculada da referência indireta antes de transformar; conteúdo e caixas
deslocados para origem do recorte após rotação. Biblioteca pypdf BSD intacta;
base própria MIT preservada, sem código Foxit incorporado ou proteções alteradas.

Controle quantitativo com PDF próprio de recorte 200x300 pt e origem 70,80:
marcador saía em 287,637795/380,944882, em vez de 217,637795/300,944882 pt.
Erro antes 70/80 pt; depois 0/0. O arquivo de entrada nunca foi regravado.
Outra reprodução confirmou stream do reader alterado antes e preservado
depois, com geometria original preservada em ambos. Versão anterior carregada
do commit-base 255cb708f20cbcb1a6484e7baba8c86b908fd8b8 no mesmo runtime pypdf para o
controle antes/depois. Fonte anterior, PDFs e provas completos privados em
`analysis-local/stage19-measurements/`; público só medições/hashes/limites.

**9/9 métodos de regressão passaram, sem falhas/skips**, com PDFs gerados por
`tests/test_imposition_cropbox.py`. Casos: recortes positivos/negativos,
tamanho real/ajuste, rotações 0/90/180/270, N-up seis por folha nas quatro
ordens oferecidas, livreto esquerda/direita/ambas/frente/verso com brancos,
worker real de três modos, mosaico folha única/tiles com rotação, origem zero
e preservação do conteúdo/geometria em memória. Mosaico testado sem marcas ou
legendas, pois Cairo não está disponível. Método de medição usa baselines e
matrizes do PDF reaberto; não é renderização/pixels ou impressão física.

Antes do patch, oito métodos rodaram com um sucesso e 20 falhas de asserção
incluindo subcasos. O JSON inicial mantém a contagem unittest; a lista `cases`
não enumera todos os subcasos falhos, limitação do runner registrada no guia.
Após o patch, os mesmos oito passaram. Acrescentado o caso de mosaico e
repetida a suíte: nove passaram. As três saídas foram preservadas, sem somar
subcasos como métodos independentes e sem confundir falhas com tokens.

Regressão dos 17 subconjuntos da etapa 18: **13 passaram, quatro bloqueados
por pdftotext**. O auxiliar privado trocou apenas a fábrica do corpus por cópia
byte a byte dos oito arquivos preservados; probes/APIs/contratos reais mantidos.
Hashes de fixture e protocolo idênticos; kit antigo da VM e arquivos de input
intactos. Nova campanha em `analysis-local/stage19-measurements/campaign/` e
relatório com a fonte atual, zero observações Foxit e campos originais null.

Ferramentas/perfis: Python 3.13.15, pypdf 6.20.1, unittest, subprocessos do
worker, AST/Git e medidas de transformações de PDF. Nenhuma nova sessão
REA/Ghidra ou execução do original; catálogo continua 209. IA/generativos
excluídos. Sem GTK/Linux completo, Poppler, impressora ou Flatpak novo.
Interrupção por tokens não constatada; pendências/diferencial continuam com
causa null onde não confirmada.

Relatório `docs/ETAPA-19.md`; evidências publicáveis em `testes/resultados/`:
`etapa-19-cropbox-before-2026-10-17.json`,
`etapa-19-cropbox-after-2026-10-17.json`,
`etapa-19-cropbox-final-2026-10-17.json`,
`etapa-19-cropbox-medidas-2026-10-17.json` e
`etapa-19-campanha-regressao-2026-10-17.json`. Especificação adiciona quatro
referências de testes; os 50 cenários completos não foram reclassificados.
Etapa 17 explicitamente marcada como snapshot portável anterior à alteração;
etapa 18 registra a regressão da fonte nova sem mudar seus critérios.

Critérios/status/pesos/revisão preservados: etapa 19 14,3%, roteiro 43,33%,
paridade 0/25 e cobertura global desconhecida/null. Critério de regressões
próprias já done recebeu evidências técnicas; divergências Foxit seguem pending.
Pacote publicado 0.1.1/devel intacto; esta correção e anexos são fonte posterior.
Próximo passo: testar/inspecionar fonte atual em Linux com GTK/Cairo/Poppler e
painel Anexos; depois gerar/testar Flatpak do novo marco. Observar original
na VM offline antes de medir/corrigir incompatibilidades Foxit.
Publicação desta rodada ainda pendente; confirmar remoto e registrar hash já
verificado em nota posterior, sem autorreferência.

Conferência final da etapa 19 às 10:08: sintaxe de 118 arquivos Python e
93 links locais aprovados; quatro PDFs de prova com hashes conferidos,
corpus/protocolos iguais e somente `app/imposition.py` alterado no aplicativo.
Arquitetura: 21 módulos, 15 interfaces e nove fechamentos locais sem gi/Cairo;
especificação: 25 famílias, 50 casos planejados, 30 referências de testes e
27 fontes. Resumo em `testes/resultados/etapa-19-verificacao-2026-10-17.json`.
Ambiente nativo reconferido: Python 3.13.15/Windows sem gi, Cairo, cryptography,
Poppler e Flatpak; WSL retorna 1 informando que não está instalado. Diagnóstico
e stdout/stderr completos em `analysis-local/stage19-environment/`. Não foi
instalado ou habilitado componente do sistema para essa verificação.

## 2026/10/17 às 10:12 (America/Sao_Paulo, UTC-03:00) — etapa 19 publicada

Marco técnico enviado por Git normal e confirmado por `git ls-remote`:
[`6e1220da352e35607910a4eb5a7ebf16389042ea`](https://github.com/airtonbp19edu/Linuxit-PDF/commit/6e1220da352e35607910a4eb5a7ebf16389042ea).
HEAD local/remoto iguais e árvore limpa após o envio. Esta nota usa hash já
verificado; seu próprio commit será conferido ao fim, sem autorreferência.
Comprovante final em `analysis-local/github-stage19-sync-verified.json`,
ignorado pelo Git. Sem bloqueio de publicação. Retomar por `docs/ETAPA-19.md`
e pela nota das 10:06: duas correções próprias, nove métodos portáveis e 13
subconjuntos do corpus preservado aprovados, quatro bloqueados por Poppler.
GTK/Linux completo e pacote novo continuam pendentes; WSL ausente reconfirmado.
Fonte nova não está no Flatpak publicado 0.1.1/devel. Nenhuma divergência
Foxit foi medida; aguardar original na VM offline. Pesos, paridade e exclusão
da IA preservados.

## 2026/10/17 às 10:21 (America/Sao_Paulo, UTC-03:00) — etapa 20, preparação de execução Linux no GitHub

Usuário autorizou seguir a próxima etapa após concluir a 19. Marco da 19 e nota
publicados/confirmados: técnico `6e1220da352e35607910a4eb5a7ebf16389042ea`,
HEAD `35e106ccb8c2c1702bcc2008a2025a1cad7f4bd8`; comprovante ignorado em
`analysis-local/github-stage19-sync-verified.json`. Árvore estava limpa.

Host continua Windows sem gi/Cairo/Poppler/Flatpak, WSL retorna não instalado.
A API do repositório confirmou Actions já habilitado e permissão para workflow
pela autenticação Git existente. Nenhuma credencial salva no Git ou exibida.
Preparado workflow manual `.github/workflows/linux-flatpak.yml`: runner Linux
efêmero com Debian 13, usuário CI, tela/buses dedicados e sandbox Flatpak
aninhado. Checkout sem persistir credenciais, token somente contents:read e
ações oficiais fixadas nos commits consultados da API. Container privilegiado
é restrito ao runner efêmero, necessário para o sandbox aninhado; não altera
o host Windows. Original não é transferido ou executado.

Fonte candidata 0.1.2 (devel), arquitetura/metainfo alinhados. Pacote publicado
0.1.1 e seu manifesto permanecem intactos. Fluxo exige suíte completa Linux
sem skips e smoke, build pelo builder original, igualdade fonte/payload, suíte
do payload e do sandbox instalado, smoke e launcher/captura. Metadados finais
só são gerados após os controles. Nada disso ainda foi executado neste
checkpoint; não há artefato 0.1.2 aprovado nem mudança dos critérios/pesos.

Ferramentas: Git/API, Python, consulta às fontes oficiais GitHub e verificação
AST/arquitetura. Nenhuma nova REA/Ghidra ou observação original, IA excluída.
Estado/receitas em docs/ETAPA-20.md. Próximo passo: publicar este checkpoint,
disparar workflow manual no commit exato, acompanhar resultados, corrigir
falhas e só então importar artefato/relatórios verificados. Capacidade do GitHub
salva em analysis-local/stage20-github-capabilities.json e SHAs das ações em
analysis-local/stage20-action-pins.json. Não é confirmação de build/publicação
do candidato; confirmação remota deste checkpoint será registrada depois.


## 2026/10/17 às 10:29 (America/Sao_Paulo, UTC-03:00) — etapa 20, primeira execução Linux

- GitHub Actions executou o commit `0c89ea04ffcddf525fef7955f0142b035bf030ec` em Debian 13 com Xvfb/Openbox. Run `39036345773`: suíte de fonte com 103 casos, 101 aprovados, uma falha e um erro, zero skips; smoke GTK 5/5. Não foi gerado/aprovado pacote nessa rodada.
- Relatório examinado em `testes/resultados/etapa-20-linux-attempt1-2026-10-17.json`; logs completos ignorados em `analysis-local/stage20-logs-39036345773/` e `analysis-local/stage20-artifact-12101954551/`. Download do artefato conferido contra SHA-256 do GitHub `abc2ceaa412a8dd989f819bca9f21cb8c6e22aae8c857d2177c3e12705ad6043`.
- Os dois casos formais interrompidos eram controles sintéticos do preparador que presumiam TEMP fora do checkout. Os testes agora montam um checkout sintético dedicado e exercitam a mesma regra de contenção; `scripts/prepare_foxit_dynamic.py` não foi alterado. Cinco testes locais desse módulo passaram com TEMP dentro da árvore. Nenhum original foi usado.
- Stderr também revelou recursão nos sinais GTK da barra lateral, apesar de quatro testes de anexos marcarem sucesso. `app/main.py` bloqueia somente o handler de navegação durante sincronização programática dos botões. Os testes GTK passam a capturar exceções de callbacks, conferir painel visível e exercitar troca/ocultação/restauração. Essa correção ainda aguarda a nova execução Linux.
- Adicionado loader SVG do Debian às dependências de CI para ícones Adwaita. Uma tentativa duplicada no commit antigo (`39036707765`) foi cancelada (API 202); o helper privado agora exige árvore limpa, remoto igual e recibo inexistente antes do dispatch. A composição da nota falhou inicialmente por tzdata ausente no Python Windows; horário foi obtido com o offset UTC-03:00 do ambiente, sem instalar dependências.
- Fonte candidata 0.1.2; entrega 0.1.1 preservada, pesos/paridade inalterados. Próximo passo: publicar estas correções, disparar outra execução e examinar cada resultado antes de aprovar o bundle.


## 2026/10/17 às 10:40 (America/Sao_Paulo, UTC-03:00) — etapa 20, Flatpak 0.1.2 examinado

- Run `39036788146` aprovado, fonte `19350fbcaedc3d61843e359e3762e99cd4d0b70a`. Debian 13/Python 3.13.5, Xvfb/Openbox; suíte completa **104/104 em cada ambiente fonte, payload e sandbox**, zero falhas/erros/skips; smoke da fonte e sandbox 5/5 cada, launcher 3/3. Os quatro casos GTK antes sem execução e um novo de navegação lateral passaram.
- Corrigida recursão GtkToggleButton.clicked durante set_active; handler de navegação bloqueado somente ao sincronizar indicadores. Controles sintéticos do preparador agora usam checkout sintético; contenção real e identidade original não foram relaxadas. Loader SVG do Debian incluído no CI; builder preservado.
- Bundle `releases/LinuxitPDF-0.1.2-x86_64.flatpak`, 35.258.000 bytes, SHA-256 `c0df14e23b126a51bec430146d114ac2d5768248b59f40471b266c1b206ba944`. ZIP do artefato 12102546424 confere com SHA GitHub `948b166283ad5ee5a3f9dda38adb36aec35475bebc78b775139db2d50d82c80c`. Seis relatórios por hash e 83 arquivos da aplicação fonte/payload/local conferidos antes da importação; 0.1.1 preservado.
- Evidência publicável em `testes/resultados/0.1.2/`, manifestos/pacotes em `releases/`, relatório `docs/ETAPA-20.md`. Raw/logs ignorados em `analysis-local/stage20-artifact-12102546424/` e `analysis-local/stage20-logs-39036788146/`. Captura própria examinada: página renderizada, cabeçalho lateral recortado na tela virtual; layout completo/desktop real/portais/impressão física pendentes. AT-SPI ausente no CI: acessibilidade não validada.
- Sem execução/transporte de Foxit, sem novas análises REA/Ghidra. IA excluída. Campanha exata da etapa 18 não repetida; kit anterior preservado. Os 20 cenários originais e 50 casos completos continuam pendentes. Pesos/status dos critérios e roteiro 43,33%/paridade 0/25 preservados; famílias amplas continuam parciais.
- Estado Git: CI executou commit já confirmado no remoto; importação e documentação desta entrega ainda aguardam push/conferência. Próximo passo concreto: validar registros/links/hashes, publicar o marco e registrar o HEAD remoto. Próxima etapa do roteiro: 21, auditoria incremental, sem declarar projeto concluído.


## 2026/10/17 às 10:45 (America/Sao_Paulo, UTC-03:00) — etapa 20, retenção do primeiro candidato

A conferência final de `runtime-packages-0.1.2.tsv` revelou somente 25 pacotes: o builder consultava caminhos `/lib` não registrados pelo dpkg no Debian com `/usr` unificado e extensões já copiadas ao stage, omitindo donos/licenças de bibliotecas. O primeiro bundle funcional `c0df14...` não foi publicado; a importação descrita na nota anterior permanece local, retida para exame. Os testes funcionais e seus relatórios continuam válidos para aquele candidato, mas não bastam para aprovar distribuição.

Correção publicada no commit `e8f9c2e`: rastrear todos os arquivos de runtime copiados, consultar nomes lexicais e resolvidos, exigir donos/avisos de copyright ou proveniência explícita de caches gerados/overlay GI, incluir auditoria no payload/candidato. Loader pareado e `runtime-lib` preservados. Checkpoint público `testes/resultados/etapa-20-runtime-audit-checkpoint-2026-10-17.json`. Nova rodada Linux/Flatpak em preparação; examinar o inventário completo e repetir todos os testes antes da entrega. Documentação de entrega em rascunho local será atualizada com o candidato final.


## 2026/10/17 às 10:51 (America/Sao_Paulo, UTC-03:00) — etapa 20, candidato final com runtime auditado

Run `39037892892`, fonte `e8f9c2e4f48dfc1e5b3cf2a8a6cfe97edb0ee899`: 104/104 testes em cada ambiente fonte/payload/sandbox, zero falhas/erros/skips, smoke 5/5 e launcher 3/3. Builder corrigido rastreou 2803 arquivos de dependências, 214 ELF e 149 pacotes/avisos Debian, incluindo libc/OpenSSL/SVG/GI-Cairo. Auditoria `runtime-origins.json` no pacote e em `testes/resultados/0.1.2/`; caches gerados têm insumos/proveniência explícitos. Não confundir essa auditoria com paridade funcional.

Bundle final `LinuxitPDF-0.1.2-x86_64.flatpak`, 35584088 bytes, SHA-256 `9d29459d7aff8ca6859cda0846cd698d285b36c3a8de2f463ff87002740cd7ba`. ZIP artefato 12103031377 confere com digest GitHub `e174c761da208fdb5eaa4be65556d3f6ba366dd6b662678f280cf4e60aaaa67d`; 7 relatórios selados conferidos. 83 arquivos da aplicação fonte/payload/local iguais. Primeira importação funcional retirada para `analysis-local/first-functional-stage20-candidate/`; os relatórios públicos de 0.1.2 agora pertencem somente ao candidato final. Raw final em `analysis-local/stage20-artifact-12103031377/` e `analysis-local/stage20-logs-39037892892/`.

Captura final e logs examinados; pendências de layout lateral/desktop real/acessibilidade/portais/impressão física mantidas. Sem Foxit, novas análises REA/Ghidra ou esgotamento confirmado de tokens. Pesos/status/paridade preservados. Estado Git: código de build publicado; artefato/documentação final aguardam push/conferência. Próximo passo: verificações finais, publicação do pacote e nota com HEAD confirmado; depois auditoria incremental da etapa 21.


### 2026/10/17 às 10:52 (America/Sao_Paulo, UTC-03:00) — conferência final da etapa 20

`scripts/check_architecture.py` passou (21 módulos, 15 interfaces, 21 critérios abertos em 14 etapas). Especificação/registro renderizado conferidos: 25 famílias, 50 casos completos ainda sem execução, 32 referências de teste e 27 de fonte, 15 subconjuntos/10 propostas. Verificação estrutural examinou 119 arquivos Python e 274 links alterados, sete hashes de relatórios CI, três hashes de bundles e preservação dos manifestos/notas antigos. Runtime: 2803 arquivos/214 ELF/149 pacotes atribuídos; somente loaders.cache difere do insumo pela reescrita documentada de caminhos. Evidência `testes/resultados/etapa-20-verificacao-2026-10-17.json`. Pesos/status do roteiro preservados: 43,33%, paridade 0/25, cobertura global nula. Envio da entrega será confirmado separadamente.


## 2026/10/17 às 10:54 (America/Sao_Paulo, UTC-03:00) — publicação confirmada da etapa 20

Commit técnico `c1205f64717bb8c1d556965a54079166025c5196` enviado e confirmado por `git ls-remote`: HEAD local/remoto iguais e árvore limpa. Flatpak 0.1.2/devel, manifesto, SHA256SUMS, relatórios e instruções publicados. `git fsck --full` retornou 0 (árvore dangling informativa preservada); os sete relatórios selados também conferem nos blobs Git, após normalização de finais de linha. Workflow 39037892892 confirmado `completed/success`.

Fonte testada permanece e8f9c2e, bundle SHA `9d29459d7aff8ca6859cda0846cd698d285b36c3a8de2f463ff87002740cd7ba`; nenhum código executável mudou depois dos testes. Registro de sincronização aponta este commit técnico, sem autorreferência. Esta nota/documentação será enviada em commit seguinte e HEAD final conferido com `scripts/verify_git_sync.py` em recibo fora do checkout. Próximo ponto: etapa 21, auditoria incremental; manter implementação/paridade parciais e pendências de VM, layout lateral, desktop, acessibilidade, portais e impressão física.


## 2026/10/17 às 11:06 (America/Sao_Paulo, UTC-03:00) — etapa 21, auditoria preparada

Git local/remoto confirmado em 4ea78dd, árvore limpa na entrada. Revisados projeto/progresso/tarefas/matriz e estado da etapa 21: 58 critérios, 37 done históricos, 21 abertos em 14 etapas; nenhum peso/status alterado. Script `scripts/audit_delivery.py` conferiu localmente três checksums, sete relatórios CI, 83 arquivos e fonte no commit e8f9c2e, licenças/metadados e obrigações abertas. Sete controles sintéticos de recusa passaram em `analysis-local/stage21-controls-initial.json`; auditoria inicial em `analysis-local/stage21-portable-initial.json`. Não são observações Foxit ou uma nova suíte completa GTK.

Preparados workflow manual `delivery-audit.yml` e `scripts/ci_audit_delivery.sh`: instalar exatamente o bundle publicado 0.1.2, conferir deployment/OSTree/runtime e bytes/licenças reais e executar smoke GTK. Sem rebuild ou mudança de app/versão. Perfil Linux instalado ainda não executado neste checkpoint. Próximo passo: publicar verificador/receita, executar CI, examinar resultados, completar relatório e sincronização. Fonte/base MIT/pypdf BSD preservados; IA excluída, VM e recorte lateral continuam pendentes.


## 2026/10/17 às 11:10 (America/Sao_Paulo, UTC-03:00) — etapa 21, auditoria instalada examinada

Run 39039390847, auditor 2e6671825317a7e7846193973113f090365db4f9: instalado exatamente o bundle publicado 0.1.2, sem rebuild; SHA 9d29459d7aff8ca6859cda0846cd698d285b36c3a8de2f463ff87002740cd7ba preservado. Deployment/OSTree/runtime conferem. Bytes reais: 83 arquivos da aplicação e 2803 de dependências; 214 ELF presentes e catalogados; avisos dos 149 pacotes presentes, não vazios e hasheados. Sete controles do auditor e cinco controles de smoke GTK passaram no Linux limpo. Os 104 testes por ambiente da etapa20 não foram repetidos nem somados a essa nova execução parcial.

Relatórios examinados em `testes/resultados/etapa-21/`; ZIP 12103157602 conferiu com digest GitHub dfaf5cb282c5a9dbb4aaa78be4ee8eb6bd9a49cac39fcfc28c4e1921fe7155b4. Raw/logs ignorados em `analysis-local/stage21-artifact-12103157602/` e `analysis-local/stage21-logs-39039390847/`. Sem traceback nos logs; AT-SPI indisponível, portanto acessibilidade não validada. Original não executado, IA excluída, sem nova REA/Ghidra ou causa de tokens confirmada.

58 critérios revisados estruturalmente: links de evidência dos 37 done históricos conferidos; 21 abertos em 14 etapas preservados. Critério de encerramento da21 segue pending; etapa21 permanece 50%, roteiro43,33%, paridade0/25 e cobertura global nula. Estado Git: código da auditoria já publicado; relatórios/continuidade aguardam push e conferência. Próximo passo concreto após publicar: retomar etapa16 para corrigir cabeçalho lateral recortado, com medição GTK/captura; depois repetir quatro subconjuntos Poppler no corpus preservado da18. Comparação original exige VM offline.


### 2026/10/17 às 11:14 (America/Sao_Paulo, UTC-03:00) — verificações finais da etapa 21

Arquitetura e registro de pendências passaram; especificação/registro renderizado conferidos (25 famílias, 50 casos completos não executados, 32 referências de teste e 27 de fonte). Verificação estrutural examinou 121 arquivos Python e 95 links modificados, quatro hashes de relatórios CI, os três bundles e os metadados de release com normalização Git explícita. Notas anteriores preservadas como prefixo; app e releases sem mudança desde4ea78dd. Auditoria local novamente aprovada após atualizar os registros. Evidência `testes/resultados/etapa-21/verificacao-estrutural.json`. Workflow confirmado completed/success. Próximo passo: publicar os relatórios, confirmar HEAD remoto e registrar publicação sem autorreferência.


## 2026/10/17 às 11:15 (America/Sao_Paulo, UTC-03:00) — publicação confirmada da etapa 21

Commit técnico `ba1f5e1494759edad9cb9002d3a8802ae6d66b3e` enviado e confirmado: `git ls-remote` igual ao HEAD local, árvore limpa, `git fsck --full` retornou0 (árvore dangling informativa preservada). Quatro hashes dos relatórios CI conferidos também nos blobs Git. Código do auditor, receita Linux, resultados instalados e pendências/notas publicados; app e bundles preservados. Sincronização registra este commit técnico; a nota atual terá commit próprio e recibo externo para o HEAD final.

Etapa21 continua50%, roteiro43,33%, paridade0/25, 21 critérios abertos em14 etapas. Não houve novo original/REA/Ghidra nem teste completo dos104 casos; nesta rodada foram sete controles do auditor e cinco de smoke novos. Próximo trabalho: etapa16, medir/corrigir cabeçalho lateral e validar geometria/captura GTK. VM, desktop/acessibilidade/portais/impressão física, contratos e demais famílias continuam pendentes.


## 2026/10/17 às 11:23 (America/Sao_Paulo, UTC-03:00) — retomada da etapa 16, diagnóstico do layout

Git local/remoto ee7881c, árvore limpa na entrada; lidos projeto/progresso/tarefas/matriz e AGENTS/retomada. Próxima atividade autorizada: cabeçalho lateral recortado da captura0.1.2. Preparados `scripts/check_sidebar_layout.py` e workflow manual `sidebar-layout.yml`: medir cinco painéis em duas larguras e capturar páginas/anexos. Observação inicial ainda não executada; passed:false não será convertido em aprovação pelo modo observe-only. Hipótese estática: primeiro painel encolhe abaixo do mínimo por shrink=True/posição158; confirmar GTK antes da correção. Consultadas APIs oficiais GtkPaned.pack1/translate_coordinates; sem nova engenharia reversa do original. App, versão e bundles preservados neste checkpoint. Próximo passo: publicar diagnóstico e executar CI; resultados completos locais/ignorados, notas por lote.


## 2026/10/17 às 11:27 (America/Sao_Paulo, UTC-03:00) — etapa 16, recorte reproduzido

Run39040540957, fonte76d901e: GTK mediu mínimo221, posição158, sidebar.x=-63 e título.x=-18 em cinco painéis. Imagens examinadas confirmam recorte. Primeiro oráculo retornava passed:true por conferir filhos apenas contra pai deslocado; resultado não adotado como aprovação. Oráculo corrigido inclui corpo visível e posição mínima; testes têm guardas independentes de origem>=0. Raw em `analysis-local/sidebar-artifact-12104400034/`, ZIP conferido SHA46cc77d640bf78facb7b2c42945fe3cbbb30ef67a9a57e3af52e6c7bd241e132. Largura760 solicitada virou924 por mínimo de outros controles; não afirmar suporte real a760.

Aplicada correção mínima `shrink=False`; candidato fonte0.1.3, arquitetura/metainfo alinhados. Três métodos GTK preparados para painéis/resize/divisor/ocultação/leitura/anexo longo. Ainda não executados. CI do próximo pacote reproduzirá baseline própria76d901e e correção no mesmo oráculo, depois validará fonte/payload/sandbox. Pacote0.1.2 preservado; sem nova observação original, VM não usada, pesos/paridade inalterados. Próximo passo: publicar e testar a correção, examinar antes/depois e só então importar pacote.


## 2026/10/17 às 11:35 (America/Sao_Paulo, UTC-03:00) — etapa 16, layout e candidato0.1.3 conferidos

Run39040860414, fonte 64f76865381b35b4f8204131ef547f210d5d09db: antes0/10 e depois10/10 no mesmo oráculo corrigido. Capturas de páginas/anexos e launcher examinadas; ícones/títulos visíveis. Painel antes mínimo221, divisor158,x-63; depois divisor221,x0. Pedido760 produz924 reais; limitação explicitada. Três métodos GTK novos e suíte completa **114/114 em cada ambiente fonte/payload/sandbox**, zero falhas/erros/skips; smoke5/5 e launcher3/3. Preservados relatórios iniciais e registrada a limitação do primeiro oráculo.

Bundle0.1.3 35591904 bytes, SHA 9aa8abf269136f84ff7cb1e6e5e990490245bec26b06979a76926030b10d3120. ZIP12104530284 confere com GitHub ebfdcdaf0890b9964c1a99a99e92b09d7cce42acfd8631f9bb5197b27b57d198; 9 relatórios selados e hashes das capturas conferidos. Fonte/payload83 iguais, runtime2803/149 pacotes atribuídos. Raw em analysis-local/sidebar-release-artifact-12104530284 e logs39040860414. Sem original/REA/Ghidra ou prova de tokens esgotados; critérios/pesos43,33% e paridade0/25 preservados. Estado Git: fonte já publicada; importação/documentação final aguardam push/confirmação. Próximo passo: validações de registros e publicação; depois quatro subconjuntos Poppler no corpus18, mantendo pendências de VM/desktop/acessibilidade/portais/impressão física.


### 2026/10/17 às 11:39 (America/Sao_Paulo, UTC-03:00) — verificação final do layout0.1.3

Auditoria local do novo manifesto aprovada; arquitetura e registro renderizado passaram (21 módulos/15 interfaces, 25 famílias, 34 referências de teste/27 de fonte, 50 casos completos não executados). Prova estrutural em `testes/resultados/0.1.3/verificacao-estrutural.json`:123 AST Python,260 links modificados, nove hashes de relatórios CI, cinco capturas hasheadas e quatro bundles conferidos. Versões anteriores e prefixo de notas preservados; pesos/status mantidos43,33%/0paridade. Próximo passo: publicar entrega e confirmar Git.


## 2026/10/17 às 11:41 (America/Sao_Paulo, UTC-03:00) — publicação confirmada do layout0.1.3

Commit técnico `e0306110ba0cd5f364e400aead2212343b80e263` enviado e confirmado por ls-remote igual ao HEAD local e árvore limpa. Bundle0.1.3/devel, manifesto, nove relatórios CI, cinco capturas, testes/registros e instruções publicados. `git fsck --full` retornou0 (árvore dangling informativa preservada); nove hashes de relatórios conferidos nos blobs Git. Fonte testada64f7686; SHA do bundle9aa8abf269136f84ff7cb1e6e5e990490245bec26b06979a76926030b10d3120. Nenhum executável alterado após testes114/114 por ambiente.

Sincronização registra este commit técnico; a nota atual terá commit próprio e recibo final externo. Próximo trabalho sem VM: quatro subconjuntos Poppler no corpus preservado18, sem trocar bytes. Recorte lateral encerrado no subconjunto testado; demais critérios de interface e etapa21 seguem parciais, roteiro43,33%, paridade0/25. Desktop/acessibilidade/portais/impressão física e VM original permanecem pendentes.


## 2026/10/17 às 11:57 (America/Sao_Paulo, UTC-03:00) — revisão das 21 etapas

Revisados os 58 critérios e conteúdos técnicos de inventário, extração, módulos,
dependências, FX, catálogo e contratos estáticos; 3.276 arquivos, 141 PE, 869 FX
e 209 entradas (152 REA + 57 diretas) coerentes. Hash do executável original
reconferido somente por leitura; nenhuma execução Foxit, nova descompilação
ou observação original. Não repetidos extração e hashes de toda a pasta.

Ferramentas/perfis: Python 3.13/stdlib no Windows; check_architecture (21 módulos,
15 interfaces, 25 famílias, nove fechamentos sem GTK/Cairo), validador funcional
(15 subconjuntos/dez propostas, 50 casos not_run), seis controles worker aprovados.
Git/API somente leitura: main protected=false; três endpoints detalhados403
por limitação de plano, sem mudar proteções/conta. Critério1 segue unknown.

Auditoria Linux/Flatpak manual run39042492785, código8cb933d0c1a230eef9d71f793a082832fd2b8164:
0.1.3 publicado reinstalado sem rebuild, 83 arquivos app, 2803 dependências,
214 ELF e149 arquivos de licença/créditos conferidos. Controles7/7 e novo
smoke5/5. SHA bundle9aa8abf269136f84ff7cb1e6e5e990490245bec26b06979a76926030b10d3120;
artefato12103979848 ZIP84da060de75273d665b1b24187235f41fc5c15d088630754fea5be4c29f050db
igual ao digest GitHub. Suítes completas anteriores114/114 por ambiente tiveram
seus nove relatórios selados conferidos, sem nova execução completa.

Matriz de anexos corrigida (cinco GTK aprovados), catálogo atual209 e notas
atualizadas de contratos/arquitetura/runtime. Checkpoints e notas anteriores
preservados. Relatório docs/REVISAO-ETAPAS.md; evidências publicáveis em
testes/resultados/revisao-etapas-2026-10-17/; raw/logs em analysis-local/stage21-artifact-12103979848/,
analysis-local/stage21-logs-39042492785/ e analysis-local/stage-review-2026-10-17/.

37 done/21 critérios abertos em14 etapas, pesos/estados intactos; roteiro43,33%,
paridade0/25, cobertura global null e causa por tokens não comprovada. Etapas
02/04/06/13/14/17/20 têm critérios concluídos; implementação/fase A abertas.
Próximo passo: quatro subconjuntos Poppler no corpus preservado18, depois
contratos/estática/implementação e desktop/portais/acessibilidade/impressão.
VM offline necessária à observação do original; não diagnosticada novamente.

Git inicial limpo e local/remoto8cb933d confirmados; revisão preparada para
commit/push autorizado, ainda sem afirmar sua publicação. Conferir remoto
após publicar e gerar recibo final fora da árvore, evitando autorreferência.


## 2026/10/17 às 15:04 (America/Sao_Paulo, UTC-03:00) — retomada da publicação da revisão

O usuário pediu retomar após a tentativa de commit/push ser impedida antes
da execução: a revisão automática de aprovação informou limite de uso e não
conseguiu concluir. Isso foi falha de revisão por cota, sem avaliação de risco;
não comprova esgotamento de tokens das análises REA/Ghidra. Nenhum comando de
commit/push daquela tentativa foi executado. Nesta retomada a consulta remota
voltou a funcionar e confirmou main em8cb933d0c1a230eef9d71f793a082832fd2b8164.

Arquitetura e especificação novamente coerentes; auditoria local de integridade
do0.1.3 aprovada. Relatórios públicos conservam seus hashes. Suíte114 completa
e Foxit não foram executados novamente; pesos/estados/paridade preservados.
Próximo passo imediato: publicar a revisão preparada, confirmar remoto e salvar
nota da publicação; desenvolvimento seguinte continua nos quatro subconjuntos
Poppler do corpus preservado18. Evidência local adicional:
analysis-local/stage-review-2026-10-17/repository-audit-resumed.json.


## 2026/10/17 às 15:05 (America/Sao_Paulo, UTC-03:00) — publicação da revisão confirmada

Revisão das 21 etapas publicada no commit 496c8a6a9db59206dff5d3f092a092556031af06.
Push concluído; ls-remote retornou o mesmo HEAD e a árvore estava limpa.
A revisão automática voltou a funcionar após o limite temporário anterior;
não houve desvio da aprovação. Relatório docs/REVISAO-ETAPAS.md e onze JSONs
em testes/resultados/revisao-etapas-2026-10-17/. Código, testes, scripts e
quatro bundles anteriores preservados; pesos/estados,43,33% e paridade0/25 intactos.

Conferência pós-publicação encontrou dois hashes de metadados calculados sobre
CRLF local (architecture.json/project.json), enquanto Git armazena LF. Ambos
foram normalizados e os hashes em review.json recalculados sobre bytes Git;
conteúdo técnico e quatro relatórios CI importados permanecem idênticos. Esse
ajuste e a confirmação seguem em commit posterior, sem reescrever o histórico.
Suíte completa e Foxit não foram repetidos; próximas tarefas continuam nos
quatro subconjuntos Poppler do corpus18 e demais pendências explícitas.

Sincronizacao-git.json registra o commit técnico confirmado para evitar
autorreferência. Confirmar o HEAD seguinte por recibo fora da árvore.


## 2026/10/17 às 15:10 (America/Sao_Paulo, UTC-03:00) — execução das frentes sem VM iniciada

Pedido atual: realizar todas as etapas restantes que puderem avançar sem VM.
Primeiro lote prepara execução Linux dos 17 subconjuntos da etapa18, com os
mesmos oito arquivos próprios preservados e verificados por SHA-256. Copiados
para testes/fixtures/campaign18/ sem templates ou dados Foxit; manifesto liga
aos hashes históricos. Novo carregador recusa bytes/manifestos alterados;
cinco controles portáveis passaram. Workflow manual no-vm-validation.yml
executará Poppler e suíte completa fonte, sem executar Foxit. Entrega0.1.3
e seus relatórios permanecem inalterados; ainda não há resultado Linux novo.

Preparados 14 alvos estáticos já registrados: dez consumidores de impressão
e quatro helpers UI. Seeds em docs/windows-evidence/foxit-rea/no-vm-2026-10-17-seeds.tsv;
rodada Ghidra direta nova, sem autoanálise integral e sem repetir os projetos
passados. JDK21.0.12.1 e Node24.22.0 reconferidos. Salvar resultados completos
em analysis-local/headless/no-vm-2026-10-17/ e examinar antes de catalogar.
VM/hardware/serviços externos e contratos completos desconhecidos continuam
separados; não promover testes próprios a paridade nem declarar todas as
obrigações encerradas por ausência de VM. Estado Git: alterações preparadas
para primeiro commit/push; próximo passo executar workflow e lote Ghidra.


## 2026/10/17 às 15:16 (America/Sao_Paulo, UTC-03:00) — campanha Poppler concluída; fonte0.1.4 iniciada

CI run39057011186/b8125e2 aprovado: mesmos oito arquivos e17 protocolos da18
conferidos por hashes;17/17 subconjuntos próprios, quatro antes bloqueados agora
aprovados, zero erros/bloqueios. Suíte fonte Linux119/119, zero skips, smoke5/5.
Artefato12109996977 ZIP454e5e63245698bd53195796cc25bb84949210a3bcf22f409b824e13ecaad5de
confere com GitHub. Evidências examinadas em testes/resultados/sem-vm-2026-10-17/;
raw/logs analysis-local/no-vm-artifact-12109996977/ e no-vm-logs-39057011186/.
Fonte testada foi0.1.3; não aprova as alterações posteriores. Original0, paridade0/25.

Fonte em desenvolvimento agora0.1.4: árvores de anexos/Kids aninhadas e anexos
de anotação, ordem/índice/hash e extração sem sobrescrita preservados. Guardas
para ciclos, nós repetidos, limite64 níveis/4000 nós e estruturas inválidas.
Sete métodos novos portáveis,14 regressões backend e14 controlador passaram.
Novo caso GTK cobre árvore/anotação pelo worker real, ainda não executado nesta
fonte. Limite64MiB continua após decodificação; portfólios/senha pendentes.
Entrega atual permanece0.1.3; nenhum Flatpak0.1.4 construído ainda. Indicador
17 marca fonte alterada até teste Linux/pacote novos. Lote estático14 alvos
ainda em execução em analysis-local/headless/no-vm-2026-10-17/.

Próximo passo: examinar lote estático, validar GUI/fonte0.1.4 e atualizar contratos
antes de gerar novo pacote. Pesos/status dos critérios gerais não alterados.


## 2026/10/17 às 15:19 (America/Sao_Paulo, UTC-03:00) — lote estático14 examinado

Ghidra direto -noanalysis concluiu os14 alvos; pseudocódigo e montagem lidos.
Capstone5.0.6/pefile2024.8.26 confirmaram1075 instruções/3372bytes. Catálogo
223 entradas (152REA+71diretas); originais inalterados e não executados.
REA CLI6.5.0, JDK21.0.12.1, Node24.22.0 confirmados; sem sessão MCP nova.
0x1b5baf0 é inserção em estrutura encadeada/tail-jump: não adotar como prova de
saída gráfica. 0x48f10ef inclui helper anterior no corpo Ghidra, assinatura
parcial. Escala por72 e truncamento SSE examinados; UI continua com classes
e7911/7913 não resolvidos. Detalhes e14 próximos contratos em
docs/AVANCO-SEM-VM.md; metadados novos preservam rodadas anteriores.

Raw/projeto em analysis-local/headless/no-vm-2026-10-17/; metadados/checagem
publicáveis em docs/windows-evidence/foxit-rea/headless-cross-checks-no-vm-2026-10-17.json
e testes/resultados/sem-vm-2026-10-17/static-machine-checks.json. Etapas amplas
permanecem parciais; pesos43,33%/paridade0/25 intactos. Próximo: publicar esse
checkpoint de fonte0.1.4 e executar Linux/GTK; novos helpers estáticos dirigidos
165f620/165f970/166a5b0/1665090/1b93280 e vtable619fa3c permanecem abertos.


## 2026/10/17 às 15:23 (America/Sao_Paulo, UTC-03:00) — correção do cenário GTK novo

Run39057656179/fonte07a52ad: campanha17/17 passou; suíte127 casos com126
aprovados euma falha no novo teste GTK. O cenário chamava novamente o botão
do painel já visível, ocultando-o antes da carga do novo documento. Corrigida
a sequência do teste para verificar atualização automática do painel visível,
sem alterar a lógica da aplicação nem afrouxar suas asserções de extração.
Falha preservada em testes/resultados/sem-vm-2026-10-17/source-0.1.4-attempt1.json;
raw analysis-local/no-vm-artifact-12110077860/, ZIP1280a8012c10998244159bbe449f45f588c005fb9113997e133ef32943fb4e2e
confere com GitHub. Nenhum pacote0.1.4 aprovado por essa tentativa.

Lote complementar estático em cópia do projeto já concluiu sete seeds, ainda
aguarda exame técnico antes de catalogar. Runner agora permite copiar projeto
preservado e exige identidade registrada antes de processar novos seeds; fonte
do projeto anterior permanece intacta. Próximo: nova validação Linux e exame
dos sete resultados. Estado Git: correção preparada para commit/push autorizado.


## 2026/10/17 às 15:26 (America/Sao_Paulo, UTC-03:00) — fonte0.1.4 Linux aprovada; estática complementar

Run39057905077/b1dde48:127/127 fonteLinux, zero falhas/erros/skips, smoke5/5
e17/17 subconjuntos do corpus/protocolos preservados passaram. Seis métodosGTK
do painel, sete novos de árvores/anotações e regressões anteriores incluídos.
Artefato12110296519/ZIPcccd4b35ff89c9e3b7a62e43c3205d487874807d25d7af494df9a9aee6b9ca36
conferido; evidências publicáveis em testes/resultados/sem-vm-2026-10-17/.

Sete resultados estáticos complementares examinados em cópia do projeto prévio:
745 instruções/2453bytes conferidos; catálogo230(152REA+78diretas). Metadados
headless-cross-checks-no-vm-followup-2026-10-17.json; raw/projeto no-vm-followup-2026-10-17
em analysis-local/headless/. Tipos/stack ainda parciais; não copiar pseudocódigo.
Detalhes/limites em docs/AVANCO-SEM-VM.md. Sem Foxit/paridade; pesos preservados.

Próximo: construir Flatpak0.1.4 no workflow já existente, executar fonte/payload/
sandbox e auditar licenças/integridade antes de publicar. Entrega0.1.3 intacta.


## 2026/10/17 às 15:31 (America/Sao_Paulo, UTC-03:00) — seis consumidores e RTTI examinados

Terceiro lote: seis entradas,1185 instruções/3571bytes conferidos. Total
27 entradas novas/3005 instruções/9396bytes; catálogo236(152REA+84diretas).
RTTI PE ligou vtables a CFX_DIBitmap, CXFA_RenderContext e CReader_PrintMgrEx;
544 candidatos de tipo por prefixo não são funções nem recursos disponíveis.
Fronteira CPDF_Parser/segurança e iteração1b89510 com final2 documentadas;
assinaturas/flags e saída final permanecem parciais. Não incorporar pseudocódigo.

Raw/projeto no-vm-core-2026-10-17 em analysis-local/headless/; metadados novos
e static-core-machine-checks/technology-boundaries em testes/resultados/sem-vm-2026-10-17/.
Fluxos/dependências/contratos atualizados. Original não executado ou alterado;
0/25 paridade e pesos43,33% preservados. BuildFlatpak run39058122147 ainda
em andamento, fonte1ed350f; aplicação fonte permanece idêntica. Próximo: obter
e examinar todos os relatórios/payload/sandbox e depois auditar pacote instalado.


## 2026/10/17 às 15:37 (America/Sao_Paulo, UTC-03:00) — Flatpak0.1.4 examinado e importado

Run39058122147/fonte1ed350f:127/127 em fonte/payload/sandbox, zero falhas/erros/
skips;83 arquivos iguais, nove relatórios selados, smoke5/5, launcher3/3.
Runtime2803 arquivos/214ELF/149 pacotes/licenças atribuídos. Capturas examinadas.
Artefato12110248359/ZIPe4a8da036ea3728bb6bb8fd35eae5524e27d21cfd3dd41bc5bb2e095bffaf59b
conferiu com GitHub; bundle35587224 bytes, SHAac18251fce149471f1dbf21d555cfc66394f7a4576d7cfd44f6666044be9abb4.
Relatórios em testes/resultados/0.1.4/, raw/logs no-vm-release-artifact-12110248359
e no-vm-release-logs-39058122147 em analysis-local/. Quatro entregas antigas
preservadas. Fonte/bundle0.1.4 correspondem; não há código Foxit na implementação.

Contratos/matriz/retomada atualizados. Catálogo236/27 entradas novas, campanha
17/17 e critérios amplos43,33%/0paridade preservados. Publicação preparada;
próximo: commit/push autorizado, auditoria do pacote publicado reinstalado e
continuação dos contratos/análises/implementação, mantendo VM/hardware separados.


## 2026/10/17 às 15:44 (America/Sao_Paulo, UTC-03:00) — publicação e auditoria0.1.4 confirmadas

Push da entrega a81d60e157ab7766ad7addbf0517a197b9be86f9 confirmado por
ls-remote e árvore limpa. Run39059125514 reinstalou o mesmo bundle0.1.4 sem
rebuild:83 app/2803 dependências/214ELF/149 licenças conferidos, controles7/7
e smoke5/5. Artefato12111125301/ZIPb716ed758caf88f86a171738d59175e9e5e8ca706a73548a0ca2ef7d83a521b7
confere com GitHub. Quatro relatórios importados byte a byte para
testes/resultados/0.1.4/audit/, mais revisão local com hashes. Suíte127 não
repetida nesta auditoria; fonte/payload/sandbox da construção permanecem válidos.

Checkpoints anteriores preservados. Próximo trabalho autorizado sem VM: ampliar
a lógica PDF segundo contratos próprios verificáveis, mantendo referências
Foxit não observadas em null. Etapas amplas21 abertas/43,33%/0paridade intactas.
A confirmação/auditoria será salva no próximo commit, sem autorreferência.


## 2026/10/17 às 15:55 (America/Sao_Paulo, UTC-03:00) — fonte 0.1.5: cópias com alterações

Continuação autorizada sem VM: backend próprio pdf_changes e adaptador
edit_tasks, comandos edit-info/copy-edit e três ações no menu Arquivo. Acrescenta
marcador de nível principal, nota Text e valor de campo Tx AcroForm em cópia
nova, sem alterar a fonte. Recusa documentos criptografados, Sig/Perms/XFA/
Collection; respeita ReadOnly e MaxLen herdados. Limites de pedido/lote/texto,
retângulo/CropBox, hash antes/depois e criação exclusiva. Temp/cópia podem
permanecer após término forçado; adapter informa conferir destino no timeout.

16 testes portáveis reais passaram. Primeiro lote de14 detectou que a visão
get_fields do pypdf omite MaxLen; corrigida consulta à referência real e
herança, com novo caso ReadOnly/MaxLen em subcampo. Quatro controles de adapter
e cinco testes reais GTK preparados; GUI/Linux/pacote da0.1.5 ainda pendentes.
Fonte contém23 módulos/18 interfaces; especificação16 subconjuntos/9 propostas,
50 cenários completos ainda not_run. Revisão explícita da proposta de formulários
para subconjunto Tx, sem mudar pesos/estados dos critérios do roteiro.

Entrega publicada/auditada permanece0.1.4. Próximo: concluir controles, validar
Linux/GTK e iterar em qualquer falha antes de gerar pacote. Evidências locais
em analysis-local/copy-edit-*.json e edit-adapter-tests.json; relatório atual
será docs/COPIA-EDITADA.md. Nenhum Foxit executado/paridade alegada.


## 2026/10/17 às 16:08 (America/Sao_Paulo, UTC-03:00) — fonte 0.1.5 e quarto lote estático

Fonte979a288 publicada/confirmada por ls-remote. Run39060689958 passou152/152
com zero falhas/erros/skips, incluindo cinco métodos GTK novos; campanha17/17.
ZIP12111217423/hash1468fe6840a5f028e82b5fcc28c16609957b1df6b7001dded85e250ec55b07a6
igual ao digest GitHub. Relatórios fonte/campanha copiados byte a byte para
`testes/resultados/copia-editada-2026-10-17/`; revisão local examinada.

Quatro alvos880490/1666490/1b8a2b0/1b8d860 examinados com Ghidra direto
12.1.4 -noanalysis em cópia do projeto core, JDK21 e script de seeds REA.
Capstone929 instruções/2919 bytes conferidos;31 novas entradas no pedido,
catálogo240(152REA+88diretas),3934 instruções/12315bytes nos quatro lotes.
Raw em analysis-local/headless/no-vm-final-2026-10-17; metadados e conferência
publicáveis. Reforçada distinção entre continuação de auxiliar e impressão
física concluída; tipos/ownership ainda parciais. Próximos alvos:16664e0,
1b8a7a0,1b8ae20,15c6550,872f20 e campos de busca; IDs7911/7913 não resolvidos.

Empacotamento0.1.5 em andamento no run39060979871; pacote0.1.4 preservado.
Próximo: examinar payload/sandbox, importar novo marco somente se passar,
publicar e reinstalar/auditar sem rebuild. Critérios/pesos43,33% e0paridade
intactos; nenhum original executado. Causa de interrupção/token:null.


## 2026/10/17 às 16:14 (America/Sao_Paulo, UTC-03:00) — entrega0.1.5 validada

Fonte`979a288d3c6407162dbbbe2b7df24991f58984f8` no run39060979871:152/152 em fonte/payload/sandbox,
zero falhas/erros/skips; smoke5/5, launcher3/3. Bundle35588656bytes,
SHA2564294654075a70e033c60e8173bd3f815446f2ce58f930a31c4591a4a4723667b; ZIPbf7c18bc79f63f7107a59125e5d00f7ddf36269e2bf4d34857e19dada3a002a1 confere com GitHub.
85app/2803runtime/
214ELF/149pacotes atribuídos.
Relatórios selados conferidos, todos os25 métodos novos presentes em cada suíte.
Manifests/hashes e cinco entregas anteriores preservados. Retomada/tarefas
consolidadas, textos antigos arquivados intactos; notas anteriores preservadas.

31 novos alvos/240catálogo;16 subconjuntos/nove propostas,23 módulos/18interfaces.
Ainda há trabalho sem VM;21 critérios abertos/43,33%/0paridade preservados.
Desktop/portais/AT-SPI/impressão física e observação original continuam pendentes.
Publicação preparada; próximo: commit/push, confirmar remoto e reinstalar/auditar
este mesmo pacote sem rebuild. Não declarar auditoria/publicação sem prova.


## 2026/10/17 às 16:19 (America/Sao_Paulo, UTC-03:00) — publicação e auditoria0.1.5 confirmadas

Push técnico`539bccb46fb3d5fddca4b70bef5a0c70aadce9a5` confirmado por ls-remote/verify_git_sync e árvore limpa;
recibo externo no TEMP LinuxitPDF-0.1.5-delivery-sync-20261017-161629.json.
Run39061762374 reinstalou o mesmo bundle0.1.5 sem rebuild:85 app/2803runtime/
214ELF/149licenças byte-verificados. Controles7/7 e novo smoke5/5. As suítes
completas152/152 de fonte/payload/sandbox pertencem à construção anterior,
não repetidas na auditoria. Artefato12111836809/ZIPd0084823304456d2620519ae23294de21de85439bf7339fbbdfdd0a0941a4458
confere com digest GitHub; quatro relatórios copiados byte a byte para
`testes/resultados/0.1.5/audit/` e revisão examinada com hashes. Logs/raw privados
preservados.15 arquivos versionados anteriores comprovadamente intactos.

Pedido sem VM avançou em análise, contratos, código, UI, testes, pacote e
publicação. Catálogo240/31 novas entradas,3934 instruções/12315bytes;16
subconjuntos/nove propostas,23 módulos/18 interfaces. Ainda há trabalho sem VM,
explicitamente em tarefas/pendencias; nenhum encerramento universal declarado.
Pesos/estados dos58 critérios preservados:37 done/21 abertos,43,33%,0/25 paridade,
inventário global aberto. Nenhuma execução do original ou recurso de IA.

Próximo lote concreto: seguir16664e0/1b8a7a0/1b8ae20/15c6550/872f20 nos projetos
preservados, fechar tipos/ownership e campos da busca; ampliar contratos e
operações nas famílias ainda incompletas. Desktop/portais/AT-SPI/impressora
pedem seus ambientes. Original exige VM offline ainda pendente. Causa de
interrupção/tokens:null; timeouts antigos não são prova de esgotamento.
Esta confirmação/auditoria será publicada em commit posterior e o últimoHEAD
será verificado novamente por recibo fora da árvore para evitar autorreferência.


## 2026/10/17 às 18:02 (America/Sao_Paulo, UTC-03:00) — fonte0.1.6 e continuação estática

Pedido reiterado de avançar sem VM. Cinco entradas16664e0/1b8a7a0/1b8ae20/
15c6550/872f20 examinadas em cópia do projeto final anterior, Ghidra12.1.4
direto-noanalysis/JDK21/seed REA. Capstone517 instruções/1572bytes conferidos;
catálogo245(152REA+93diretas). 1b8ae20 é caminho auxiliar de preparação/contexto,
refinando hipótese anterior de finalização. Raw/projeto privados; metadados e
checagem publicáveis. Próximos alvos1c68ca0/15c5010/20a6f70, campos de busca eIDs.

Fonte própria0.1.6 acrescenta anexos textuais/PDF em worker cancelável, modos
coringa/proximidade e índice persistente JSON de PDFs explicitamente selecionados.
Oito métodos de modos e12 de anexos passaram; dez iniciais de índice passaram,
mais dois controles em execução. Seis testes reais GTK preparados, ainda sem
execução Linux. Nenhum original executado; limites/omissões documentados em
`docs/BUSCA-COLECOES.md`. Não contar testes portáveis como GUI ou paridade.
Pacote0.1.5 permanece publicado e intacto. Próximo: validar fonte Linux/GTK,
corrigir falhas, depois construir e auditar0.1.6. Causa por tokens/interrupção:null.


## 2026/10/17 às 18:09 (America/Sao_Paulo, UTC-03:00) — fonte Linux aprovada e classes identificadas

Fontecb3c514 publicada/confirmada; run39069391926 passou190/190 sem falhas/erros/
skips, seis métodos GTK novos, smoke5/5 e campanha17/17. Artefato12114263494,
ZIP59b6300e717d5a8d1803cc64af5287ab8e12c96a9000b493628e5eeb35634d88 confere
com GitHub. Evidências copiadas byte a byte. Capturas mostraram frame anterior
à repintura, apesar dos estados/testes corretos. Ajustado apenas o sincronismo
do teste; cancelada construção39069595028 para repetir evidência visual.

Segunda rodada3 entradas1c68ca0/15c5010/20a6f70 examinadas;372 instruções/
1651bytes. RTTI CPDF_ImageRenderer, CReflowViewerEx eIPDFViewer; fábricaUIagora
situada emreflow. Clip vazio pode retornar1 sem saída gráfica. Totaldesta
continuação8 novas entradas/248catálogo,889 instruções/3223bytes. Raw privados
em analysis-local/headless/no-vm-context-2026-10-17, metadados/checks publicáveis.
Próximos alvos15c9c90/15c5e00, slotsImageRenderer e campos da busca. Tipagem,
UI completa, paridade e origem da causa por tokens continuam sem fechamento.

Próximo: repetir fonte/capturas no novo commit do teste, examinar imagens,
construir/preservar0.1.6 e auditar instalação. Pacote0.1.5 permanece intacto.


## 2026/10/17 às 18:12 (America/Sao_Paulo, UTC-03:00) — capturas após repintura aprovadas

Run39069765892/ca7fe12 passou190/190, zero falhas/erros/skips, seis métodos GTK
novos e corpus17/17. Capturas das buscas anexos/proximidade/coleção examinadas:
contagens/resultados aparecem e proximidade destacaalpha+x+beta. Nenhuma
mudança no aplicativo para essa correção; apenas sincronismo da captura.
ZIP12113794453/6cbbdd42f525043490a2b9698cb6c426100798ddebbfdef486e05ad8ecb8d946
igual ao digest GitHub. Provas preservadas em sem-vm-continuacao-2026-10-17.
Construção0.1.6 retomada parafonteca7fe12;0.1.5 continua preservado. Próximo:
conferir três suítes do pacote, imagens/hashes/licenças, publicar e reinstalar
sem rebuild. Peso/estados/paridade intactos; nenhuma execução Foxit.


## 2026/10/17 às 18:19 (America/Sao_Paulo, UTC-03:00) — Flatpak0.1.6 validado

CIhttps://github.com/airtonbp19edu/Linuxit-PDF/actions/runs/39069918299:190/190 por suíte fonte/payload/sandbox, zero falhas/erros/skips,
32 portáveis/6GTK novos, smoke5/5 e launcher3/3. Bundle35601808bytes,
SHA256a71bca023a6bd2f671ffb7049a101a59ade185ef25bb5d3f8f0ddfeb7c399d05; artefato12115166272/ZIPa7e86c2f4b7006c870a2df459fd5f54a9ee5156f1b1fb04d589c32d1121f47adconferecomGitHub.
Relatórios selados e populações iguais conferidos.28 módulos/26 interfaces,19
subconjuntos/seis propostas, catálogo248/8 novas entradas. Critérios/estados/
pesos43,33% e0/25 paridade intactos. Próximo: publicar, confirmar remoto, reinstalar
mesmo bundle e auditar sem rebuild; continuar demais frentes ainda abertas.


## 2026/10/17 às 18:24 (America/Sao_Paulo, UTC-03:00) — publicação e auditoria 0.1.6 confirmadas

Entrega técnica `e66c2d0d97d15d9f51171b2140c0ec49a00b20a8` confirmada no GitHub com árvore limpa por recibo externo.
A auditoria independente [39070599134](https://github.com/airtonbp19edu/Linuxit-PDF/actions/runs/39070599134) reinstalou o bundle publicado sem reconstruí-lo;
90 arquivos da aplicação, 2803 do runtime, 214 ELF e 149 avisos de licenças conferidos.
Sete controles do auditor e cinco verificações funcionais no sandbox passaram.
As três suítes de 190 casos são evidência do builder anterior, não uma nova execução nesta auditoria.
ZIP SHA-256 `1a4501707856064692c3fd66f2182b23ce57d89f6ce9b19932b99b84eab6d63d` igual ao digest GitHub; quatro relatórios copiados byte a byte
para `testes/resultados/0.1.6/audit/`; arquivo completo em `analysis-local/no-vm-audit-artifact-12114588036/`.
Sem execução do original, alteração de pesos ou fechamento dos 21 critérios amplos restantes.
Próximo lote: criação própria de PDFs a partir de PNG/JPEG, com seleção explícita, limites e cópia nova;
depois validar fonte Linux e registrar separadamente do pacote 0.1.6. IA permanece fora do escopo.


## 2026/10/17 às 18:29 (America/Sao_Paulo, UTC-03:00) — criação PNG/JPEG, fonte 0.1.7

Backend próprio, janela GTK, seleção ordenada/DPI, RGB Flate, orientação EXIF,
transparência branca, hashes e publicação exclusiva implementados.16 testes
portáveis reais passaram localmente em Python3.13.15/Pillow12.3.0/pypdf6.20.1.
Fixture fixada e cinco testes GTK aguardam Linux; não declarar widgets testados.
Pillow já existente, nenhuma nova dependência ou material proprietário incorporado.
Código pós-pacote0.1.6; manifesto e sete bundles preservados.20 subconjuntos/cinco
propostas; pesos43,33%, paridade0/25 e21 critérios abertos inalterados. Sem nova
análise REA/Ghidra neste lote. Próximo: suíte Linux completa/Poppler, examinar
captura e corrigir falhas antes do marco Flatpak0.1.7.


## 2026/10/17 às 18:34 (America/Sao_Paulo, UTC-03:00) — fonte 0.1.7 e reflow examinados
+
+CI39071317244/5a60287:212/212 em Debian13/Python3.13/GTK3/X11/Poppler,
+zero falhas/erros/skips.17 métodos portáveis e cinco GTK novos. Captura real da
+criação examinada: ordem, DPI, resultado e controles legíveis. Campanha anterior
+17/17 repetida sem alterar as oito fixtures. ZIP194212bytes/SHA12fa1cddfabc568ae9780a21815b0c2466e8b3f806d5b0fcecadfa391332552a
+conferido com digest GitHub. Evidência em testes/resultados/criacao-imagens-2026-10-17;
+completo em analysis-local/no-vm-artifact-12114799597. Flatpak ainda em construção.
+
+Em paralelo local, Ghidra12.1.4/JDK21 com REA seed script/-noanalysis examinou
+15c5e00/15c9c90 em cópia do projeto anterior.111 instruções/467bytes conferidos
+por Capstone5.0.6/pefile2024.8.26; RTTI exato IPDFViewerLayout/CReflowViewerLayout.
+Body do primeiro inclui tail-helper compartilhado, sem contagem extra. Catálogo
+250(152REA+98diretas); tipos/algoritmos/ownership seguem parciais. docs/REA-REFLOW.md
+documenta próximos helpers1f21a80/1f21ac0; raw somente analysis-local/headless/reflow-resources-2026-10-17.
+Nenhuma execução original, peso alterado ou evidência de limite de tokens.
+Próximo: examinar as três suítes e capturas do pacote0.1.7, preservar versões
+anteriores e publicar somente após hashes/licenças conferidos.


## 2026/10/17 às 18:40 (America/Sao_Paulo, UTC-03:00) — Flatpak 0.1.7 validado

Builder https://github.com/airtonbp19edu/Linuxit-PDF/actions/runs/39071324606, fonte 5a6028791a3aa4306c014970a2934c39bb649943:212/212 em cada suíte fonte,
payload e sandbox, zero falhas/erros/skips.17 métodos backend/cinco GTK novos.
92 arquivos app, 2803runtime/214ELF/149pacotes atribuídos; smoke5/5 e launcher3/3.
Bundle 35614064bytes/SHA256093ee6c7ed6ab6a1c4974da836fedb3414e147dfa0554ddae9eac8ee575c9070; artefato12115651420,
ZIP84c377c46596afdea57a6580e6e6a9b51a84098b3127d38fac9fd01d50536a6e igual ao digest GitHub. Relatórios copiados byte a byte;
capturas/hash examinados.30 módulos/29 interfaces,20 subconjuntos/cinco propostas;
catálogo250, duas entradas novas examinadas nesta rodada. Critérios/pesos43,33%
e paridade0/25 mantidos. Próximo: publicar e confirmar remoto; auditoria independente
reinstala este mesmo bundle sem rebuild. Outros contratos/estática/runtime e
observação Foxit na VM permanecem abertos; não há declaração de conclusão global.


## 2026/10/17 às 18:44 (America/Sao_Paulo, UTC-03:00) — publicação e auditoria 0.1.7 confirmadas

Entrega técnica `d8dd8e363c21fd7cf21fc245e1d61a0612ee15aa` confirmada no GitHub com árvore limpa por recibo externo.
A auditoria independente [39072088580](https://github.com/airtonbp19edu/Linuxit-PDF/actions/runs/39072088580) reinstalou o bundle publicado sem reconstruí-lo;
92 arquivos da aplicação, 2803 do runtime, 214 ELF e 149 avisos de licenças conferidos.
Sete controles do auditor e cinco verificações funcionais no sandbox passaram.
As três suítes de 212 casos são evidência do builder anterior, não uma nova execução nesta auditoria.
ZIP SHA-256 `7d86b00fd0e4d400437ddeab0e864a3cc4ba50832165b5c9795de18601b68780` igual ao digest GitHub; quatro relatórios copiados byte a byte
para `testes/resultados/0.1.7/audit/`; arquivo completo em `analysis-local/no-vm-audit-artifact-12115224313/`.
Sem execução do original, alteração de pesos ou fechamento dos 21 critérios amplos restantes.
Próximos alvos estáticos: helpers1f21a80/1f21ac0 e slots de layout/renderer, sem repetir o lote examinado.
Implementação própria: ampliar segurança/assinaturas/acessibilidade/nuvem/plataforma e demais operações
parciais. Serviços, certificados e desktop real exigem ambientes específicos; original exige VM offline.
IA permanece fora do escopo. Esta rodada foi publicada sem encerrar todos os critérios amplos.


## 2026/10/17 às 19:20 (America/Sao_Paulo, UTC-03:00) — checkpoint fonte 0.1.8

Pedido em andamento: executar tudo que for possível sem VM; usuário adiou nuvem.
Implementados subconjuntos próprios: AES-256 R6, autenticação e cópia plaintext
somente owner, texto da página/ATK/F6, CMS offline sem confiança de cadeia,
renomear marcador/atualizar nota/girar em cópia. Credenciais por stdin; erros
sanitizados; diretório privado por worker e encerramento de grupo POSIX.
Testes sintéticos, sem chave pessoal; Windows .NET SignedCms e PyCA50.0.2 em
analysis-local/security-python-deps (ignorado). Linux usa OpenSSL e GTK/Poppler.
Controles portáveis novos em repetição após limpeza privada; relatórios finais
serão examinados antes da publicação. Falha inicial de teste CMS foi fixture
escapada e diretório temporário não propagado, corrigidos; não é falha Foxit.
Dois helpers estáticos Enter/LeaveCriticalSection examinados com Ghidra12.1.4
-noanalysis/Temurin21/Capstone5.0.6; catálogo252, 70bytes/32instruções novos.
Projetos/respostas completos ignorados; metadados públicos e relatório ligados.
35 módulos/40 interfaces;23 subconjuntos/2propostas.25 famílias e pesos mantidos,
43,33%/0paridade,50planos not_run. Original não executado. Pacote atual0.1.7;
fonte0.1.8 ainda não publicada neste instante. Próximo: conferir portáveis,
validadores, commit/push confirmado e suíte Linux/GTK/Flatpak; preservar marcos.


## 2026/10/17 às 19:21 (America/Sao_Paulo, UTC-03:00) — portáveis conferidos

20/20 segurança,9/9 edição ampliada,10/10 CMS e12/12 regressão do worker passaram
no Windows/Python3.13, após diretório privado por tarefa. Relatórios copiados byte
a byte em testes/resultados/0.1.8-portable/. Arquitetura35/40 e especificação25/50,
23subconjuntos/2propostas conferidas. Descoberta estática267 métodos; execução Linux
completa/GTK/Flatpak ainda pendente. Preparado commit fonte e envio autorizado.


## 2026/10/17 às 20:16 (America/Sao_Paulo, UTC-03:00) — Flatpak 0.1.8 validado

Builder https://github.com/airtonbp19edu/Linuxit-PDF/actions/runs/39074818078, fonte da13d8600326213d26dbc662f02f4f06ef40d320:267/267 em cada suíte fonte/payload/
sandbox, zero falhas/erros/skips.39 métodos portáveis e16 GTK novos; ATK.Text,
foco F6 e cancelamento real de descendente/limpeza temporária exercitados.
97 app/2804runtime/215ELF/150avisos; smoke5/5,launcher3/3.
Bundle 35984232bytes SHA256f7c4673819b42a5d8778b79308cfd8aa8ff8da0bc245cb6865fee88f5aea229e; artefato12116387596,
ZIP385e914187094364af2626b1711c2448e97707fb02599fbc48b4a55d9c564846 igual ao digest GitHub. Relatórios selados copiados byte a byte;
sete capturas/hash examinados.35módulos/40interfaces,23subconjuntos/2propostas;
catálogo252. Nuvem adiada explicitamente pelo usuário. Roteiro43,33% e paridade0/25
preservados; original não executado. Próximo: publicar/confirmar remoto, auditar
mesmo bundle sem rebuild, continuar contratos locais e estática restantes.


## 2026/10/17 às 20:17 (America/Sao_Paulo, UTC-03:00) — local/remoto verificados e retomada

Local/online iguais em da13d8600326213d26dbc662f02f4f06ef40d320, nenhum trabalho
alheio novo. Fonte Linux/GTK267/267+campanha17/17 preservadas. Builder39074818078
terminou com sucesso durante a pausa; bundle0.1.8 baixado e todas as três suítes267
sem falhas/erros/skips, hashes9 relatórios/97app/2804runtime/215ELF/150pacotes
conferidos; sete capturas examinadas. Relatórios raw copiados sem reformatar.
Oito bundles anteriores preservados. Quatro acessores de layout examinados nesta
retomada,20bytes/dez instruções, ponteiros exatos e Capstone conferidos; catálogo256.
Projetos/respostas integrais ignorados. Registro da interrupção e próximos passos
em docs/RETOMADA-INTERRUPCAO-2026-10-17.md. Nuvem adiada; pesos/paridade preservados.
Próximo: commit/push técnico, confirmar remoto e auditoria instalada do mesmo
bundle sem reconstruir; continuar contratos locais/estática sem reiniciar análises.


## 2026/10/17 às 20:21 (America/Sao_Paulo, UTC-03:00) — publicação e auditoria0.1.8 confirmadas

Entrega técnica `c6b273fdf44f2e260f0ddae092397158cf65237c` confirmada no GitHub e árvore limpa por recibo externo.
Auditoria https://github.com/airtonbp19edu/Linuxit-PDF/actions/runs/39078571081 reinstalou mesmo bundle, sem rebuild;
97app/2804runtime/215ELF/150avisos de pacotes conferidos. Sete controles do auditor
e cinco novos smoke checks passaram. Suítes267/267 em cada ambiente são evidência
anterior do builder, não repetidas nesta auditoria. ZIPc1dc5765bdc714f23853d9bc9288e043461bfa7c56d3d052affc02d3272d5afe igual ao digest
GitHub, artefato12117961659; quatro relatórios raw copiados byte a byte e revisão
em testes/resultados/0.1.8/audit/. Catálogo256/23subconjuntos/2propostas,
35módulos/40interfaces,43,33% e paridade0/25 mantidos. Original não executado.
Nuvem adiada. Próximo concreto: consumidores/escritores campos+5c/+60/+4/+8 e
slots layout+04/+08/+1c (15cc3b0/15cc140/15ccab0), campos de busca/IDs7911/7913;
continuar demais formulários/undo/anotações/formatos e plataforma própria.
Desktop/AT-SPI/impressora e original em VM ainda pendentes. Não reiniciar lotes
examinados; fontes, relatórios, nove bundles e licenças preservados.


## 2026/10/17 às 20:22 (America/Sao_Paulo, UTC-03:00) — três consumidores de layout examinados

Ghidra12.1.4 -noanalysis/Temurin21/REAseed, Capstone5.0.6 e PE conferidos:
15cc3b0/15cc140/15ccab0,1.348bytes/412instruções. Três ponteiros vtable exatos
e máscara0x7fffffff conferidos. Saídas de quatro inteiros/predicado e consumo
this+4/+8 refinam hipótese geométrica, sem tipagem/ownership/runtime completos.
Precondição de índice e receptores ECX preservados como lacunas. Relatório
docs/REA-REFLOW-GEOMETRIA.md; resultados completos ignorados por rodada nova.
Catálogo259(152REA+107diretas); slots não somados como funções. Não repetir sete
métodos de layout já examinados. Próximos15cc510/15cc520/15ccd20/15cbc10/15c9c60,
métricas this+98 e escritores dos campos, conferindo catálogo antes de seeds.
Aplicação/Flatpak0.1.8 permanece idêntico ao auditado; nenhuma suíte completa
repetida por esta análise. Roteiro43,33%,paridade0/25 e nuvem adiada preservados.
Próximo: publicar esta nota e evidência da auditoria e confirmar remoto limpo.


## 2026/10/17 às 20:51 (America/Sao_Paulo, UTC-03:00) — fonte0.1.9 pastas sincronizadas

Usuário autorizou aplicar fluxo de pastas locais sincronizadas e pediu separar VM.
Pasta explícita por seletor nativo, preferência/últimas pastas separadas do tema,
atalhos abrir/salvar e esquecer sem apagar arquivos. Sem contas/API/upload próprios.
Novo worker copy-file recusa fonte alterada externamente e destino existente.
Cópias simples/editadas/imagens/senhas publicam nome final completo via operação
atômica sem substituição; falhas/temporários e limites documentados. Temporários
.linuxit-* podem ser vistos pelo cliente externo; não há transação remota ou
garantia após término forçado. Guia docs/PASTAS-SINCRONIZADAS.md inclui tabela VM.
15 portáveis novos e20segurança/17criação/16edição passaram localmente;53regressões.
Relatórios raw em testes/resultados/0.1.9-portable/.8 GTK novos pendentes; total290
métodos declarados.37módulos/49interfaces;23subconjuntos/2propostas mantidos.
Builder prepara dois controles de pasta sintética fora HOME sem/com concessão;
isso não comprova interação com portal ou cliente real. Fonte0.1.9 ainda sem
pacote/publicação neste checkpoint;0.1.8 permanece pacote atual. Pesos43,33% e
paridade0/25 intactos, original não executado. Próximo: validadores, commit/push,
suíte Linux completa e Flatpak; examinar evidências e auditar mesmo pacote publicado.


## 2026/10/17 às 20:55 (America/Sao_Paulo, UTC-03:00) — primeiro ensaio Linux preservado

Builder39080654708 interrompeu após fonte290 casos:285pass/4errors/1fail,zero skips.
Os23casos novos passaram. Quatro doubles FolderChoice de anexos não expunham
set_current_folder/add_shortcut_folder; foram atualizados sem remover asserções.
O interceptador de cancelamento de coleção capturava Popen de renderizações
concorrentes; restringido ao comando index-search. TesteGtknovo agora ignora
corretamente ausência de gi no Windows. Aplicação não mudou por esses reparos.
Relatório raw/revisão em testes/resultados/0.1.9-attempt1/,ZIP/digest preservados.
Não contar tentativa como suíte aprovada/pacote entregue. Próximo: novo commit,
reexecutar fonte/Flatpak completos e examinar os controles de concessão de pasta.


## 2026/10/17 às 21:07 (America/Sao_Paulo, UTC-03:00) — Flatpak 0.1.9 validado

Builder https://github.com/airtonbp19edu/Linuxit-PDF/actions/runs/39080923058,
fonte `6aabe4c7a205744db60f32737a883b61ba5fc80f`: 290/290 em fonte,
payload e sandbox, sem falhas, erros ou skips. São 15 métodos portáveis e oito
GTK novos. Controles de pasta fora de HOME passaram: negação sem concessão e
leitura/cópia/reabertura/recusa de sobrescrita com concessão específica.
99 arquivos app, 2.804 de dependências, 215 ELF, 150 avisos de pacotes;
smoke 5/5 e launcher 3/3. Bundle: 35.983.584 bytes,
SHA-256 `ef9fc7c41e91a51c3ecd38c15a8c3b84d40dc350f7a3bb603876da4d40d3aede`.
Artefato 12119245506; ZIP `7e3f36437d07f2bc88709b0071f37503e8658b17544b849f4fb6881f1914360b`
igual ao digest GitHub. Onze relatórios selados copiados byte a byte e oito
capturas/hashes examinados em testes/resultados/0.1.9/.
O ensaio independente de fonte também passou 290/290 e 17/17 subconjuntos em
run 39080923451; evidências em testes/resultados/0.1.9-source/.
O primeiro ensaio independente foi preservado em 0.1.9-attempt1: 286/290,
quatro erros do double antigo; o builder anterior teve ainda uma falha de
cancelamento. A causa concorrente desse cancelamento é uma inferência;
a restrição do interceptador ao comando index-search passou nas duas reexecuções.

Não foi usado cliente de sincronização real nem interação com portal real;
a resposta nativa foi simulada nos testes GTK. O guia separa essas dependências
de desktop das etapas 10, parte dinâmica da 11 e comparações 18/19, que exigem
VM offline para o original. 37 módulos/49 interfaces, 23 subconjuntos/duas
propostas, catálogo 259, roteiro 43,33% e paridade 0/25 preservados.
APIs de nuvem adiadas; fluxo local autorizado. Original não executado.
Próximo: publicar o mesmo bundle, confirmar remoto e auditar a instalação sem
rebuild. Nove bundles anteriores preservados.


## 2026/10/17 às 21:12 (America/Sao_Paulo, UTC-03:00) — publicação e auditoria 0.1.9 confirmadas

Entrega técnica `e6bd69adcd41a0c51c0ed03b05b784d36750f026` confirmada no GitHub,
com árvore limpa por recibo externo. A auditoria independente
https://github.com/airtonbp19edu/Linuxit-PDF/actions/runs/39081734820
reinstalou o mesmo bundle, sem rebuild: 99 arquivos app, 2.804 de dependências,
215 ELF e 150 avisos de pacotes conferidos. Sete controles do auditor e cinco
novas verificações funcionais passaram. As suítes 290/290 por ambiente são
evidência anterior do builder; não foram repetidas nesta auditoria.
Artefato 12118649715, ZIP `c7c3b6fc4af8ebc6909f229a057341e6f434e2c707ac8aeb3c70dea9815eaa97`
igual ao digest GitHub. Quatro relatórios raw copiados byte a byte e revisão em
`testes/resultados/0.1.9/audit/`. Dez bundles preservados, de 0.1.0 até 0.1.9.
Catálogo 259, 23 subconjuntos/duas propostas, 37 módulos/49 interfaces,
roteiro 43,33% e paridade 0/25 mantidos. Original não executado.

Fluxo de pasta local autorizado e entregue; APIs de nuvem continuam adiadas.
Próximo passo concreto sem VM: testar seleção de pasta em portal real,
persistência de acesso após reiniciar e cliente externo em desktop Linux,
com arquivos de teste; conferir envio, mudanças externas, conflitos e perda de rede.
Os testes CI usam concessão específica, sem cliente real nem interação de portal.
AT-SPI e impressão física também exigem seus ambientes/equipamentos.
Para o original: VM offline é necessária na etapa 10 (D01–D20), parte dinâmica
da 11 (UI01–UI10) e referência diferencial das etapas 18/19. Reutilizar corpus,
protocolo e hashes preservados; não reiniciar alvos estáticos examinados.
Outras operações locais e análises estáticas continuam abertas sem VM.
Esta nota e os relatórios recebem o próximo commit; a confirmação final deve
usar recibo externo para evitar registrar o hash do próprio commit.

## 2026/10/17 às 21:20 (America/Sao_Paulo, UTC-03:00) — acesso ao download privado corrigido

O usuário informou página em branco ao abrir o link raw no navegador interno;
não informou arquivo baixado com zero bytes. HTTP público dos dois links raw
e da API retornou 404. A API autenticada confirmou repositório privado e o
arquivo 0.1.9 com 35.983.584 bytes. Git blob remoto
`a96ff93c9bc9a4dbf4c2af48d0d9d1dfcd45a330` coincide com `git hash-object` local;
SHA-256 local continua `ef9fc7c41e91a51c3ecd38c15a8c3b84d40dc350f7a3bb603876da4d40d3aede`.
Nenhum pacote foi reconstruído ou substituído; testes não foram repetidos.

README e instalação agora orientam abrir a página do arquivo em navegador
autenticado e usar Download raw, com tamanho esperado e comandos de instalação.
Visibilidade do repositório preservada. Diagnóstico sanitizado em
`analysis-local/download-access-check-019.json`, fora do Git; sem publicar
credenciais ou links temporários. A resposta específica do navegador interno
não foi instrumentada: o acesso anônimo negado é confirmado, o diagnóstico
da tela em branco usa também o relato do usuário.
Próximo: o usuário baixar autenticado e testar no desktop Linux. Dependências
de portal/cliente real e VM offline das etapas 10/11/18/19 permanecem intactas.
Publicar esta correção documental e confirmar o remoto por recibo externo.


## 2026/10/17 às 21:22 (America/Sao_Paulo, UTC-03:00) — orientação para mudança de visibilidade

O usuário informou que tornará o repositório público temporariamente. A alteração
de visibilidade não foi feita pelo agente. A última conferência HTTP pública
ainda retornou 404. As instruções agora cobrem ambas as visibilidades, para
não exigir login depois de o proprietário liberar o acesso público. Pacote,
código, testes e indicadores preservados. Próximo: confirmar o acesso público
e baixar pelo navegador habitual, usando Download raw na página do arquivo.


## 2026/10/17 às 21:23 (America/Sao_Paulo, UTC-03:00) — download público confirmado

Após a alteração feita pelo usuário, GET anônimo sem cache da API retornou
200, private=false e visibility=public. GET anônimo do arquivo no host
raw.githubusercontent.com retornou 200, Content-Length=35983584 e cabeçalho
binário flatpak\0 esperado. Não foi necessário reconstruir ou substituir o
pacote. Orientar download no navegador habitual caso o navegador interno
não entregue o arquivo. Próximo: instalar/testar no desktop Linux; demais
pendências e indicadores preservados.


## 2026/10/18 às 00:29 (America/Sao_Paulo, UTC-03:00) — investigação do aviso no Linux

O usuário relatou erro “corrompido ou faltando permissões”, sem fornecer ainda
a distribuição, o programa que exibiu o aviso ou a saída de flatpak install.
A rodada anterior foi interrompida antes do download completo; nesta rodada
foi feito novo GET anônimo completo do arquivo público via urllib. Resultado:
HTTP 200, 35.983.584 bytes, cabeçalho flatpak e SHA-256 igual ao manifesto e ao
arquivo local: ef9fc7c41e91a51c3ecd38c15a8c3b84d40dc350f7a3bb603876da4d40d3aede.
Evidência pública: testes/resultados/0.1.9/download-integrity-2026-10-18.json.
Cópia e relatório completos em analysis-local/public-flatpak-integrity-20261018-002839/.

Isso verifica o arquivo servido pelo GitHub; não verifica a cópia baixada no
Linux do usuário nem confirma a causa do erro. Não foi feita nova instalação
ou repetida a suíte: a instalação/auditoria CI anterior continua evidência
histórica separada. Nenhum pacote ou fonte foi alterado; pesos/paridade intactos.
A documentação oficial Flatpak confirma instalação de bundle por flatpak install.
Guia atualizado com SHA-256 e diagnóstico pelo terminal, sem atribuir causa ou
solicitar alteração genérica de permissões. Foi solicitado ao usuário executar
flatpak --version, sha256sum e flatpak install --user na pasta do arquivo,
enviar a saída completa e informar a distribuição. Próximo passo depende
desses dados para corrigir o problema específico. Publicar guia/evidência/nota
e confirmar o remoto; preservar versões e relatórios anteriores.


## 2026/10/18 às 00:44 (America/Sao_Paulo, UTC-03:00) — busca/impressão/reflow, três lotes estáticos examinados

Pedido: continuar análise estática; investigação do instalador deixada de lado
a pedido do usuário. Git local e remoto conferidos em 7f7eb394aa028d514f1d273065e482940bde163e,
sem alterações alheias. Ghidra 12.1.4/Temurin 21.0.12.1, script de sementes do
pacote REA 6.5.0, perfil direto -noanalysis. Nenhuma ferramenta MCP REA exposta
nesta sessão; saúde do provedor MCP não foi reavaliada. Não são novas observações MCP.
Original fixado por SHA-256 90208c9e8da92c8e546b76c8f4a2f8fb999105d124e663bbea6744fb6bb6b3a6,
conferido antes/depois; Foxit não executado. Projetos anteriores foram copiados.

Lote static-geometry-state-2026-10-18: 7 entradas examinadas; checkpoint real
2026-10-18T00:36:37.474607-03:00. Projeto/raw em analysis-local/headless/static-geometry-state-2026-10-18/.

Lote static-search-print-state-2026-10-18: 5 entradas examinadas; checkpoint real
2026-10-18T00:37:39.842519-03:00. Projeto/raw em analysis-local/headless/static-search-print-state-2026-10-18/.

Lote static-search-print-types-2026-10-18: 4 entradas examinadas; checkpoint real
2026-10-18T00:40:56.985751-03:00. Projeto/raw em analysis-local/headless/static-search-print-types-2026-10-18/.

Capstone 5.0.6/pefile 2024.8.26 conferiram 823 instruções/2.831 bytes selecionados.
Primeira tentativa de conferência falhou por ModuleNotFoundError: capstone;
resolvido usando PYTHONPATH=analysis-local/python-deps já existente, sem instalar.
Três rodadas Ghidra concluídas; sem timeout ou esgotamento de tokens comprovado.

Resultados: sete helpers de reflow (limite INT32_MAX, máscara double de sinal,
passagem intermediária por float32, métricas ainda sem tipo); quatro helpers
de busca/formatação (parser exato de textos 1.0.0..1.3.0, enum ligado ao offset+14,
retorno 0/9 oculto pela assinatura void); cinco de impressão/ciclo de vida
(RTTI CPDF_BackgroundDrawer, contexto 0x138 ainda sem classe, receptores distintos
para campos +74 e caminhos de liberação com/sem LOCK). Auxiliares compartilhados
por salto e chamadores já catalogados não contados como novas entradas.

Metadados e seeds em docs/windows-evidence/foxit-rea/headless-cross-checks-static-*.json
nas três rodadas de 18/10, verificações em testes/resultados/static-*-2026-10-18/.
Revisão agregada: testes/resultados/static-analysis-2026-10-18/review.json.
Relatório: docs/REA-ESTATICA-BUSCA-IMPRESSAO-2026-10-18.md. Catálogo 275 = 152 REA +
123 diretas exclusivas. Fonte, builder, versão e Flatpak 0.1.9 preservados; as suítes históricas
de 290 casos não foram repetidas. Testes próprios não provam paridade.
Roteiro 43,33%, 37 done/21 abertos em 14 etapas, paridade 0/25 e pesos preservados.

Próximo estático: 15cb590/15cb720/15cbb70/15cb8a0/15cb130, this+98/slot+20,
escritores/pré-condições de arrays; provedor+58 e offsets 3/5/6/7/0xc/0x10,
IDs 7911/7913; contexto 0x138, 1b57340/1b5a420 e consumidores BackgroundDrawer.
Não repetir os 16 alvos examinados. A VM segue necessária para observar o
original nas etapas 10/dinâmica da 11/18/19. IA fora do escopo; APIs de nuvem adiadas.
Próximo: verificadores estruturais, catálogo/progresso, commit/push e confirmação
remota; este checkpoint ainda não declara publicação. Usar recibo externo final.

Verificações finais locais: contratos25 famílias/50 planos/23 subconjuntos/duas
propostas; arquitetura37 módulos/49 interfaces/21 critérios em14 etapas;
auditoria do repositório aprovada, dez bundles e11 relatórios CI históricos
conferidos por hash. Não é nova instalação nem nova execução das suítes.
Metadados públicos normalizados em LF antes de fixar seus hashes, preservando
os resultados raw e manifestos anteriores. Conferir hashes staged antes do commit.


## 2026/10/18 às 00:47 (America/Sao_Paulo, UTC-03:00) — publicação estática confirmada

Marco `45417b3a546be1d51a0809ad170d420806b0a098` publicado no GitHub. Recibo externo confirmou HEAD local=remoto
e árvore limpa. São16 novas entradas examinadas, catálogo275 (152REA+123diretas),
823 instruções/2.831 bytes selecionados conferidos. Hashes staged das evidências
coincidiram antes do commit; originais/raw/projetos permaneceram fora do Git.

Relatório docs/REA-ESTATICA-BUSCA-IMPRESSAO-2026-10-18.md, revisão e três lotes
publicados; fonte/Flatpak0.1.9 preservados, sem repetir testes de runtime.
Critérios/pesos/paridade intactos; 21 critérios em14 etapas ainda abertos.
Próximos alvos estáticos e limites de tipos constam no relatório e no registro
estruturado de pendências. A VM segue necessária para a referência dinâmica.
Esta confirmação recebe commit posterior e recibo externo final, evitando
autorreferência. Não reiniciar os16 alvos já examinados.


## 2026/10/18 às 01:11 (America/Sao_Paulo, UTC-03:00) — restante da fila estática

Pedido: continuar os alvos de busca, impressão, geometria/reflow, tipos e estados
sem VM. Git local/remoto iguais em1ccd574e85b1fd9919b23a203f126a9980670723 ao iniciar;
nenhuma alteração alheia encontrada. Oito lotes Ghidra12.1.4 direto -noanalysis,
Temurin21.0.12.1 e sementes REA6.5.0; MCP REA não exposto, nenhuma nova evidência MCP.
Executável e DLL pinados por hashes do inventário; originais não executados.

48 entradas novas,6.830 instruções/25.919 bytes selecionados conferidos com
Capstone5.0.6/pefile2024.8.26. Catálogo323=152REA+171diretas;275 linhas anteriores
idênticas, sem contar28slots já conhecidos ou auxiliares compartilhados como novas entradas.
Tipos CReflowViewerEx/CReflowViewerPageEx/CFindToolDlgAdv, classefxLuncenLib,
stemming efetivo SearchOption+5, escritores de estado/arrays e limpeza de impressão refinados.
Mapa7911/7913 ligado à classe; mesmo handler e DDX distintos continuam ambíguos.
Construtor1758c70 e helpers1003f6b0/15ca780 têm semântica apenas parcial. Corpo
Ghidra15ca460 de37bytes exige ressalva:130bytes suplementares conferidos à parte,
sem somar bytes sobrepostos e sem declarar fronteira completa corrigida.

Quatro ferramentas próprias agora distinguem sujeitos pinados por hash;11controles
passaram, inclusive rejeição de sujeito/projeto incompatível, sobrescrita e mistura
de módulos. Falhas de helper:tzdata ausente e import avulso fora do diretório;
resolvidos com offsetUTC-03 explícito e execução pelo arquivo, sem instalar.
Oito rodadas concluídas; sem timeout ou causa de tokens confirmada.

Relatório:docs/REA-ESTATICA-CONTINUACAO-2026-10-18.md. Revisão:testes/resultados/static-remaining-2026-10-18/review.json; hashes públicos, máquina e joins vinculados.
Projetos/resultados completos e checkpoints por lote emanalysis-local/, ignorados.
Fonte/builder/Flatpak0.1.9 preservados;290/290 por ambiente é histórico, sem
repetição de runtime nesta rodada. Nenhum código/asset Foxit incorporado.
Critérios/pesos preservados:43,33%,37done/21abertos em14etapas,paridade0/25.

Próximos recortes:alocação/tamanhos/chamadores dos arrays,15cd6e0/15cc9b0,
atribuição ativa de dialog+1e48, cinco campos SearchOption e algoritmo Lucene,
contexto0x138/serviços de imagem/concorrência. VM offline para10/dinâmica11/18/19;
desktop real para portal/AT-SPI/cliente/impressora. Nuvem remota adiada,IA excluída.
Próximo imediato:validar contratos/arquitetura/progresso/auditoria do repositório,
revisar diff e hashes staged,commit/push e confirmar remoto. Ainda não publicado
neste checkpoint; registrar confirmação posterior sem autorreferência.

Verificação final 2026/10/18 às 01:12 (America/Sao_Paulo, UTC-03:00):
contratos25/50planos/23subconjuntos/duas propostas e arquitetura37módulos/49interfaces
conferidos. Auditoria do repositório aprovada; pacote e relatórios históricos
conferidos, sem reinstalação ou nova suíte290. Critérios/status/pesos iguais ao
baseline. Hashes dos48resultados raw e pseudocódigos, sementes/endereço/máquina,
metadados públicos e bundle preservado conferidos. Um agregador esperou o campo
opcional subject_name, ausente em dois relatórios anteriores; nome resolvido pelo
hash do inventário, preservando esses relatórios. Checkpoints por lote salvos;
normalização públicaLF registrada separada do hash original das sementes.
Publicação pendente do commit/push e recibo externo a seguir.


## 2026/10/18 às 01:14 (America/Sao_Paulo, UTC-03:00) — continuação publicada

Marco `2e2da8da8c80728bcbf6ab5f0e2929c447839665` publicado no GitHub. O recibo externo confirmou
HEAD local igual ao remoto e árvore limpa. São 48 entradas adicionais em oito
lotes; catálogo 323 (152 REA + 171 diretas), 6.830 instruções e 25.919 bytes
selecionados conferidos. Os 33 hashes das evidências coincidiram com os blobs
staged antes do commit; nenhum original, resultado completo ou projeto entrou
no Git. Os 11 controles das ferramentas e os verificadores estruturais passaram.

Relatório: docs/REA-ESTATICA-CONTINUACAO-2026-10-18.md. Limites de semântica,
fronteira 15ca460, provedor ativo, cinco campos de busca e contexto 0x138
continuam explícitos; IDs 7911/7913 têm classe/mapa identificados e ambiguidade
de comportamento preservada. Fonte/pacote 0.1.9 intactos, sem repetir runtime.
Pesos, 43,33%, 21 critérios abertos e paridade 0/25 preservados. Próximos
recortes no relatório e no registro de pendências; não reiniciar os 48 alvos.

Esta nota e os indicadores de sincronização recebem commit posterior; confirmar
também seu HEAD por recibo externo final, evitando autorreferência.

## 2026/10/18 às 01:21 (America/Sao_Paulo, UTC-03:00) — diagnóstico da VM existente

O usuário confirmou Oracle VirtualBox, 20 GB de RAM no computador, 8 GB para
a VM e dois processadores virtuais. Leitura da configuração e do log existente,
sem iniciar VM/Foxit ou alterar Windows: Windows 10 x64, RAMSize 8000 MB,
duas vCPUs, VBoxSVGA/128 MB e limite de CPU 100%. VirtualBox 7.2.20 r175154.
Oito processadores lógicos não devem ser confundidos com oito núcleos físicos.

O log aberto em 2026-10-18T03:47:44Z registra Integridade da Memória ENABLED,
VT-x indisponível para acesso direto, hipervisor Microsoft presente e
NEMR3Init: Snail execution mode is active. É um indício de contribuição do
backend NEM/WHP à lentidão, não um benchmark ou prova de causa única.
Naquela inicialização o host registrava cerca de 10 GB de RAM disponível;
também falta medir pressão de memória, armazenamento e drivers convidados.
Instalação de Guest Additions não foi confirmada por esta leitura.

Oracle documenta perda de desempenho na combinação VirtualBox/Hyper-V e que
Integridade da Memória pode manter o hipervisor ativo:
https://docs.oracle.com/en/virtualization/virtualbox/7.2/user/Troubleshooting.html
Não foi desativada proteção, alterado boot ou modificado o hipervisor.
VMware Workstation é alternativa a avaliar, sem desempenho comparativo medido.

A VM agora existe, mas a contenção offline ainda não está validada: a
configuração lida tem adaptador NAT ativo. Preparar isolamento, snapshot e
fixtures antes de executar o original. Zero novas observações Foxit, sem
mudança de critérios/pesos, roteiro 43,33%, paridade 0/25 e pacote 0.1.9.
Próximo: escolher entre diagnosticar/ajustar VirtualBox ou testar VMware;
conferir RAM livre, disco local e Guest Additions. Implementação própria e
análise estática podem continuar independentemente dessa VM.
Nota preparada para publicação; confirmar push por recibo externo.


## 2026/10/18 às 01:51 (America/Sao_Paulo, UTC-03:00) — editor próprio de cópia em validação

Pedido: avançar trabalhos sem VM enquanto o usuário a configura. Git local/remoto
91c405dc6593eb503a14f939f2bfcabb21f98540 iguais ao iniciar, árvore limpa. Implementados
controles AcroForm checkbox/radio/choice, mover/excluir subárvore de marcadores,
Highlight/Square/exclusão restrita e histórico de rascunho com desfazer/refazer.
Quatro módulos novos; fonte0.1.10, arquitetura41 módulos/54 interfaces. Nenhum
código Foxit incorporado, original não executado e catálogo323 preservado.

21 testes novos portáveis e oito do histórico passaram. Regressão de edição47
casos:42 passaram/cinco GTK omitidos no Windows; não é validação Linux. Primeiro
lote detectou três falhas de AP de choice /Opt em pares, corrigidas por adaptador
próprio sem alterar pypdf. Primeiro teste de histórico falhou por import antes
de configurar caminho; relatório de falha preservado e rodada corrigida passou.
Oito métodos GTK novos preparados, ainda sem execução. Sem timeout/tokens confirmado.

Contrato:docs/EDICAO-COM-HISTORICO.md. Relatórios portáveis emtestes/resultados/
advanced-edits-portable-2026-10-18-round2.json eedit-history-portable-2026-10-18-round2.json.
Raw e temporários emanalysis-local/. Último Flatpak0.1.9 e suas290execuções por
ambiente preservados. Critérios/pesos/43,33%/21abertos/paridade0/25 intactos.
Próximo:validar contratos/arquitetura,commit/push eCI fonte Linux, corrigir UI
se necessário; só depois gerar novo Flatpak e auditar. Nuvem remota adiada/IA excluída.
Ainda não publicado neste checkpoint; registrar confirmação remota depois.


## 2026/10/18 às 01:57 (America/Sao_Paulo, UTC-03:00) — editor Linux327/327 e formatos extras

Fonte do editor7b0b1572626cc603221a0e70a5006fb1b6eff6f7 publicada. CI39098594089
passou327/327, zero falhas/erros/skips; oito métodos GTK novos, smoke5/5 e
corpus próprio17/17. ZIP do artefato12125596640 conferido com digest GitHub
ac2d47e82abe56656b4875c1419d8779c1e74943790dfd98c1c9fdbeca53ab4c. Relatórios
e captura do editor copiados byte a byte para testes/resultados/0.1.10-source/;
captura examinada, controles e status visíveis. Não é aprovação da fonte posterior.

Acrescentados BMP/WebP/TIFF simples à criação de PDF, preservando RGB/EXIF/alpha,
limites e publicação exclusiva.22 testes portáveis passaram, cinco novos; um GTK
novo preparado. TIFF multipágina/animações eOCR continuam pendentes. O teste de
renderização do editor agora também exige pixel amarelo na área do destaque.
Fonte continua0.1.10; último Flatpak0.1.9 preservado. Contratos e referências
de testes atualizados. Escrita de progresso.json falhou uma vez com Errno22;
repetição passou, causa não confirmada. Sem esgotamento de tokens comprovado.

Próximo:commit/push da fonte posterior e buildCI com suíte atual completa333
em fonte/payload/sandbox; só importar pacote após conferir hashes, populações
e resultados. Roteiro43,33%,21 critérios abertos/paridade0/25 preservados.
IA excluída/nuvem remota adiada/original não executado.


## 2026/10/18 às 02:03 (America/Sao_Paulo, UTC-03:00) — consulta remota agora verificável

Revisão somente leitura da pendência API01 após o usuário tornar repositório
público. Regras aplicáveis a main e rulesets responderamHTTP200 comlistasvazias;
metadados mainprotected=false/protectionenabled=false; endpoint deproteção404.
Não houve alteração de proteção, visibilidade, faturamento ou configurações.
Evidência:docs/REGRAS-REMOTAS-2026-10-18.md e
testes/resultados/revisao-etapas-2026-10-18/remote-rules.json, sem credenciais.

Único critério da etapa1 que estava unknown agora done; definição/pesos e revisão
intactos. Roteiro43,33→43,93% (+0,60pp),38done/20abertos em13etapas; paridade0/25
preservada. Registro anterior403 arquivado no histórico de resolução. Esta
verificação não altera código do aplicativo nem valida original. Build0.1.10
segue emCI; registrar publicação deste marco junto da entrega após evidências.


## 2026/10/18 às 02:08 (America/Sao_Paulo, UTC-03:00) — entrega0.1.10 validada

CI39098896161, fontedf8cc464fdcff693f1b65881c4929bea2478c2a0:333/333 em cada ambiente
fonte/payload/sandbox instalado, sem falhas/erros/skips.34 portáveis e9 GTK novos.
Os290 IDs anteriores preservados. Editor de cópia, controles AcroForm, mover/
excluir marcadores, anotações de área/exclusão e BMP/WebP/TIFF simples validados.
Desfazer/refazer atua no rascunho; cópias anteriores preservadas. OCR permanece
pendente. Capturas examinadas;11 relatórios CI selados e103 arquivos app conferidos.
Runtime:2804 arquivos/215 ELF/150 avisos de pacotes, smoke5/5/launcher3/3.

BundleLinuxitPDF-0.1.10-x86_64.flatpak, 35997664 bytes,
SHA256a70ea619975e61b45ffb55f84690652c5c86d8a75a33fba36257446bc3cdeb56. Manifestos, licenças e versões anteriores
preservados; JSON/PNGs copiados byte a byte. Manifesto de entrega atualizado
somente após validação integral. Relatórios emtestes/resultados/0.1.10/, raw
emanalysis-local/no-vm-release-artifact-12126216018/; arquivoZIP comSHA256
9476ba27ea16bfb08ecb9fe6fe32f2b66401ad10bc85a441639d0a6d59543d9d
igual ao digest GitHub; artefato12126216018.
Arquitetura41/54, catálogo323,23subconjuntos/duas propostas,43,93%/20abertos e
paridade0/25 intactos. Original não executado; nuvem remota adiada/IA excluída.
Próximo:auditar repositório,commit/push do pacote e auditoria independente do
mesmo bundle instalado. Publicação ainda não confirmada neste checkpoint.


## 2026/10/18 às 02:15 (America/Sao_Paulo, UTC-03:00) — publicação e auditoria 0.1.10 confirmadas

Entrega técnica `c403fa773d9c5e43374625e37ab88dee590c4711` publicada no GitHub; ls-remote igual ao HEAD local
limpo, com recibo externo fora da árvore. Fonte do aplicativo testada:
df8cc464fdcff693f1b65881c4929bea2478c2a0. Bundle 35.997.664 bytes, SHA-256
a70ea619975e61b45ffb55f84690652c5c86d8a75a33fba36257446bc3cdeb56. Download público sem login retornou HTTP 200 e os
mesmos bytes/hash. Um auxiliar local falhou ao formatar o fuso por falta de tzdata
no Python Windows; ajustado para UTC-03:00 desta data e recibo obtido. Nenhuma
dependência do aplicativo foi alterada para isso.

Auditoria https://github.com/airtonbp19edu/Linuxit-PDF/actions/runs/39099821029 no mesmo bundle, sem rebuild: 103 arquivos app,
2.804 de dependências, 215 ELF e 150 avisos de pacotes conferidos. Sete controles
do auditor e cinco novos smoke checks passaram. As suítes 333/333 de fonte,
payload e sandbox são do builder anterior; não foram repetidas pela auditoria.
Artefato 12126102507; ZIP SHA-256 15a77f55d4f107b6c77f9aa8e98d639cb1a48e299cd3cdcc2f2be8762754cc02, igual ao digest GitHub.
Quatro relatórios copiados byte a byte e revisão em testes/resultados/0.1.10/audit/;
raw em analysis-local/no-vm-audit-artifact-12126102507/. Ferramentas: Git/API
GitHub e auditor Python próprio; execução Linux em Debian 13/Xvfb/Flatpak no CI.

Arquitetura 41 módulos/54 interfaces; catálogo 323 entradas; 23 subconjuntos e
duas propostas em 25 famílias. Roteiro 43,93%, 38 done/20 abertos em 13 etapas.
O único critério fechado nesta rodada foi a consulta de regras remotas; pesos e
definições preservados. Paridade 0/25, cobertura global desconhecida. Não houve
nova REA nem execução do Foxit; VM, rede e proteções Windows não foram alteradas.
Sem evidência de esgotamento de tokens nesta rodada. APIs de nuvem adiadas, IA
fora do escopo. Próximo trabalho próprio: OCR e demais contratos locais. Portal
real, concessão persistente, cliente de sincronização, AT-SPI e impressão física
precisam do respectivo desktop/equipamento, sem depender da VM Foxit. D01–D20,
UI01–UI10 e comparações do original exigem validar contenção offline primeiro.
Este registro de confirmação será publicado com recibo final externo separado,
evitando autorreferência. Preservar lotes estáticos e versões anteriores.


## 2026/10/18 às 10:18 (America/Sao_Paulo, UTC-03:00) — OCR local preparado sem VM

Usuário confirmou continuar sem VM. Git inicial de449459ce261b50d2fd9abe7b317eaad67bbd49
limpo e igual ao remoto main. Fonte0.1.11: pdf_ocr.py, ocr_window.py, menu e worker
ocr-copy; Tesseract local com português/inglês e Poppler. Gera cópia rasterizada
pesquisável, até20 páginas/128MiB/150ou300DPI, sem substituir fontes ou destino
existente. Perdas estruturais e páginas sem texto explícitas. Dados/modelos/
dependências serão incluídos com proveniência Debian no novo bundle.

20 controles portáveis passaram, sem falhas/erros/skips; ferramentas simuladas,
não reconhecimento. Cinco testes Linux e cinco GTK preparados, ainda não rodados.
Relatório testes/resultados/ocr-portable-2026-10-18-round1.json. Ferramentas:
Python3.13, pypdf/Pillow, Git e consulta à documentação oficial Tesseract.
Arquitetura43 módulos/57 interfaces. Roteiro43,93%,38done/20abertos, paridade0/25
preservados. Original/VM não executados nem modificados; nuvem adiada/IA excluída.
Próximo: publicar fonte, executar CI Linux completo antes de gerar/importar novo
pacote, conferir relatórios/capturas, publicar e auditar o mesmo bundle.
Pacote vigente0.1.10 e seus hashes permanecem intactos. Não declarar OCR real
ou GTK aprovados com base nos controles simulados. Sem causa de tokens confirmada.


## 2026/10/18 às 10:31 (America/Sao_Paulo, UTC-03:00) — diagnóstico da primeira validação OCR

Run39131157732/fonte2483b17:363/363 passaram na fonte Linux,362/363 no payload,
com uma falha no teste de cancelamento. A suíte sandbox não foi executada.
O teste injetava tesseract simulado via PATH; o launcher do payload prioriza
binários empacotados, logo o marcador PID do dublê não aparecia. Reconhecimento
real e demais testes passaram; não publicar esse bundle parcial. Corrigido o
oráculo para observar o processo ELF Tesseract real por /proc, iniciar OCR em
três páginas a300DPI e cancelar seu grupo; continua exigindo que o descendente
termine. Código OCR do produto não alterado por essa correção. Receita histórica
sidebar-layout também passa a instalar dependências OCR para evitar ausência.

Evidências em testes/resultados/ocr-2026-10-18-attempt1/; raw/ZIP e candidato
não aprovado em analysis-local/no-vm-release-artifact-12137114910/. ZIP SHA256
8e0d7136fe59b4f7a028eb86e4f85b64d902324e0f2da3d78736fd414b801bbf,
igual ao digest GitHub. Próximo:publicar correção e repetir suíte integral nos
três ambientes antes de importar pacote. Roteiro43,93%,38done/20abertos,
paridade0/25 e entrega0.1.10 preservados. Nenhuma VM/original executados.


## 2026/10/18 às 10:42 (America/Sao_Paulo, UTC-03:00) — OCR0.1.11 validado em fonte/payload/sandbox

CI39131964575, fonte `4c5fc65cfafea876c9e7559fe4c6cff169fe3ca3`:363/363 em cada ambiente, sem falhas,
erros ou skips. Os333 IDs anteriores preservados. Novos20 controles portáveis,
cinco Linux com Tesseract/Poppler reais e cinco GTK. Português, inglês e ambos,
150/300DPI, texto pesquisável, página vazia, CropBox/rotação/aparência e cancelamento
de descendente Tesseract exercitados. Capturas OCR/principal examinadas. Nenhuma
equivalência Foxit; nenhum original executado. Fonte desenvolvida sem VM.

Bundle LinuxitPDF-0.1.11-x86_64.flatpak, 44671928 bytes,
SHA256 30a1e9ab078194df85c0bdf841316958450b916b1f87f3312eaccd491c240c02. Artefato 12137769078, ZIP SHA256 717acab4a1237f4ebf139e711ec99920468602f6561f35af237886d5b0bbf865,
igual ao digest GitHub. Onze relatórios selados,105 arquivos app e runtime
2849 arquivos/224ELF/162 avisos de pacotes conferidos.
Modelos por/eng e executável Tesseract com proveniência Debian e licenças incluídos.
Smoke5/5 e launcher3/3; controles fora HOME negado/concedido passaram novamente.
Evidências testes/resultados/0.1.11/, raw analysis-local/no-vm-release-artifact-12137769078/.
Ferramentas: Git/API GitHub, Python próprio, Debian13/Xvfb/Flatpak no CI. Relatórios
CI copiados byte a byte; versões anteriores e análise estática preservadas.

Arquitetura43/57, catálogo323,23subconjuntos/duas propostas. Roteiro43,93%,38done/
20abertos e paridade0/25 intactos. Sem novos critérios fechados ou pesos alterados.
Rasterização remove estrutura interativa/assinaturas e OCR pode errar; contrato
em docs/OCR-LOCAL.md. Próximo:commit/push deste pacote e auditoria independente
do mesmo bundle instalado, depois TIFF multipágina e demais contratos locais.
Desktop/portal/cliente/AT-SPI/impressora e original em VM offline seguem pendentes.
APIs de nuvem adiadas/IA excluída; sem evidência de esgotamento de tokens.
Publicação deste pacote ainda requer confirmação após o commit preparado.


## 2026/10/18 às 10:46 (America/Sao_Paulo, UTC-03:00) — publicação e auditoria OCR0.1.11 confirmadas

Entrega técnica `2664f4ae7db5be45aec461f8bba1a456138585b8` confirmada no GitHub com árvore limpa por recibo
externo. Download público sem login retornou HTTP200, 44671928 bytes,
SHA256 30a1e9ab078194df85c0bdf841316958450b916b1f87f3312eaccd491c240c02, idêntico ao bundle testado.
Auditoria https://github.com/airtonbp19edu/Linuxit-PDF/actions/runs/39132852906 reinstalou mesmo bundle sem rebuild:
105app/2849runtime/224ELF/162avisos conferidos, incluindo modelos
Tesseract por/eng. Sete controles e cinco novos smoke checks passaram. Suítes
363/363 em cada ambiente são do builder; não repetidas nesta auditoria.
Artefato 12138502084, ZIP SHA256 e4276a53e7a655c0b529ee24d1995d51ba62d03f3458cf06485f01935f61f353, igual ao digest GitHub.
Quatro relatórios copiados byte a byte, revisão em testes/resultados/0.1.11/audit/;
raw em analysis-local/no-vm-audit-artifact-12138502084/. Ferramentas Git/API/Python
e CI Debian13/Xvfb/Flatpak. Roteiro43,93%,38done/20abertos/13etapas, paridade0/25,
catálogo323 e arquitetura43/57 preservados. Nenhum critério/peso alterado.
Sem VM nem original; não houve nova REA ou modificação de rede/proteções Windows.
OCR é cópia rasterizada limitada e pode errar. Nuvem adiada/IA excluída.
Próximo: TIFF multipágina e demais contratos próprios; desktop/portal/concessão
persistente/cliente/AT-SPI/impressão física exigem ambientes/equipamentos próprios.
Comparação Foxit exige validar VM offline. Sem evidência de esgotamento de tokens.
Este registro recebe commit/push e comprovante final externo separados, evitando
autorreferência. Preservar lotes estáticos e pacotes/relatórios anteriores.


## 2026/10/18 às 12:24 (America/Sao_Paulo, UTC-03:00) — TIFF multipágina preparado sem VM

Retomada em557eb792d72a0b982df7ca7e7b1de4849e7e4197, main local limpo igual ao
remoto. Fonte0.1.12: TIFF clássico/BigTIFF com todas as páginas do IFD principal,
ordem em blocos de arquivo, limite100 páginas totais, RGB8, orientação por página,
limites/hashes/pub exclusiva preservados. Validação prévia bounded de tabelas,
offsets e ciclos; Pillow continua decodificando pixels. UI explica blocos e OCR
separado com limite20 páginas. Nenhuma nova dependência, original ou ativo Foxit.

14 métodos portáveis novos passaram e22 de criação atualizados passaram. A
execução anterior de criação teve21/22 com a antiga expectativa de recusar TIFF;
teste renomeado/adaptado à nova regra, WebP animado permanece recusado. Não contar
essa substituição como método adicional. Fixture de orientação ajustada para
evitar fechamento duplicado do AppendingTiffWriter; rodada2 sem esse erro.
Relatórios tiff-multipage-portable-2026-10-18-round1/round2 e
tiff-creation-existing-2026-10-18-attempt1/round2 em testes/resultados/.
Dois GTK e uma integração Linux TIFF→PDF→OCR preparados, ainda não executados.

Ferramentas Python3.13/Pillow12.3/pypdf e Git; documentação oficial Pillow e
LibTIFF consultada. Arquitetura43/57, catálogo323,23subconjuntos/duas propostas,
roteiro43,93%,38done/20abertos e paridade0/25 preservados. Original/VM não
executados; nuvem adiada e IA fora do escopo. Sem evidência de tokens. Próximo:
publicar checkpoint, rodar suíte Linux completa nos três ambientes, importar
somente pacote aprovado, conferir capturas/hashes e publicar/auditar mesmo bundle.
Pacote0.1.11 e relatórios anteriores preservados até concluir nova entrega.


## 2026/10/18 às 12:33 (America/Sao_Paulo, UTC-03:00) — correção de fixtures TIFF entre versões Pillow

CI39140432410/fonte2b3491a:380 testes,379 passaram,1 erro no gerador BigTIFF do
Pillow11.1 (Invalid TIFF file header), antes de chamar o importador. Orientação
passou mas o gerador AppendingTiffWriter ainda emitiu erro de fechamento no Linux.
Sem payload/sandbox/pacote nesta execução. Fixtures substituídas por dois arquivos
sintéticos próprios, gerados à parte com Pillow12.3 e fixados por hash/manifesto.
Tests agora só leem BigTIFF/orientações e conferem pixels; nenhum código do produto
alterado. Gerador scripts/generate_tiff_fixtures.py preserva proveniência e exige
pasta nova.14 métodos portáveis passaram na rodada3, sem erro de fechamento.

Relatórios em testes/resultados/tiff-linux-2026-10-18-attempt1/ e
 tiff-multipage-portable-2026-10-18-round3.json; raw em
analysis-local/no-vm-release-artifact-12141228395/. ZIP SHA256
954cfbe715e8068b77f59c0a0a1ab7388295c26fe105ec5169c36e3cca88e973, igual ao digest
GitHub. Próximo:publicar correção e repetir validação completa nos três ambientes.
Pacote0.1.11 preservado,43,93%/38done/20abertos/paridade0/25 intactos. Sem VM,
original ou nova análise REA; sem evidência de esgotamento de tokens.


## 2026/10/18 às 12:43 (America/Sao_Paulo, UTC-03:00) — TIFF0.1.12 validado nos três ambientes

CI39141058408, fonte `b2ee3e324f0cb2bb23032ce82239ea56c84302d1`:380/380 por ambiente fonte/payload/sandbox,
sem falhas/erros/skips.14 novos portáveis,2 GTK e1 integração Linux TIFF→PDF→OCR.
Um teste anterior que recusava TIFF foi adaptado/renomeado:362 IDs anteriores
preservados,18 IDs novos incluem a substituição,17 métodos adicionais líquidos.
Ordem de blocos/páginas, orientação por página, modos/alpha, LZW/Group4, BigTIFF/
endianness, limites, corrupção e protocolo exercitados; pixels Poppler e OCR real.
Capturas TIFF/criação/principal examinadas; demais hashes conferidos.

Bundle LinuxitPDF-0.1.12-x86_64.flatpak, 44661792 bytes, SHA256
77cbff20cdb351272de9292ce334fb97c327fdfbef7fb3321d408fe6e5144701. Artefato12142105864, ZIP SHA256 758cb5163c572a52e777f9aa4a421b6b318ee26caef72c2dc1ff4d5847de940e, igual ao digest
GitHub.105 arquivos app/11 relatórios selados; runtime 2849arquivos/
224ELF/162avisos conferidos. Sem nova dependência. Smoke5/5,launcher3/3,
controles fora HOME negado/concedido passaram. Evidências testes/resultados/0.1.12/,
raw analysis-local/no-vm-release-artifact-12142105864/. Git/API/Python/Pillow/pypdf;
execução Debian13/Xvfb/Flatpak no CI. Relatórios copiados byte a byte.

Arquitetura43/57,catálogo323,23subconjuntos/duas propostas,43,93%/38done/20abertos,
paridade0/25 preservados. Critérios/pesos e universo global desconhecido intactos.
Original/VM não executados, nuvem adiada/IA excluída. Criação100 páginas não amplia
OCR20; RGB8 sem ICC/precisão alta, SubIFDs ou seleção individual. Próximo:publicar
e auditar mesmo pacote, continuar demais formulários/anotações/contratos/estática.
Desktop/portal/cliente/AT-SPI/impressora e comparação Foxit em VM offline abertos.
Sem evidência de esgotamento de tokens. Publicação ainda requer confirmação após
commit/push desta entrega preparada; versões anteriores preservadas.


## 2026/10/18 às 12:48 (America/Sao_Paulo, UTC-03:00) — publicação e auditoria TIFF0.1.12 confirmadas

Entrega técnica `d70773a67d471569631e0517a7990e21c2c0d21b` confirmada no GitHub com árvore limpa por recibo
externo. Download público sem login retornou HTTP200, 44661792 bytes,
SHA256 77cbff20cdb351272de9292ce334fb97c327fdfbef7fb3321d408fe6e5144701, idêntico ao bundle testado.
Auditoria https://github.com/airtonbp19edu/Linuxit-PDF/actions/runs/39141995602 reinstalou mesmo bundle sem rebuild:
105app/2849runtime/224ELF/162avisos conferidos, incluindo modelos
Tesseract por/eng. Sete controles e cinco novos smoke checks passaram. Suítes
380/380 em cada ambiente são do builder; não repetidas nesta auditoria.
Artefato 12142116724, ZIP SHA256 83246ddce1165de031a0037e5821a1d5c6447871319d63104b2e49a9489bb623, igual ao digest GitHub.
Quatro relatórios copiados byte a byte, revisão em testes/resultados/0.1.12/audit/;
raw em analysis-local/no-vm-audit-artifact-12142116724/. Ferramentas Git/API/Python
e CI Debian13/Xvfb/Flatpak. Roteiro43,93%,38done/20abertos/13etapas, paridade0/25,
catálogo323 e arquitetura43/57 preservados. Nenhum critério/peso alterado.
Sem VM nem original; não houve nova REA ou modificação de rede/proteções Windows.
TIFF usa RGB8, ordem por blocos e IFD principal; OCR separado continua limitado a20 páginas. Nuvem adiada/IA excluída.
Próximo: demais formulários/anotações/contratos próprios; desktop/portal/concessão
persistente/cliente/AT-SPI/impressão física exigem ambientes/equipamentos próprios.
Comparação Foxit exige validar VM offline. Sem evidência de esgotamento de tokens.
Este registro recebe commit/push e comprovante final externo separados, evitando
autorreferência. Preservar lotes estáticos e pacotes/relatórios anteriores.


## 2026/10/18 às 13:18 (America/Sao_Paulo, UTC-03:00) — anotações0.1.13 preparadas sem VM

Partida: local/remoto c3d56624f72fddcde8e5974672dca0d598a77bcf, árvore limpa.
Implementação própria de Underline/StrikeOut/Squiggly de área, elipse Circle e
Line em qualquer direção. Form XObjects de aparência sem fontes externas,
traço vermelho. update-annotation altera comentário/autor e preserva geometria/AP.
Exclusão ampliada aos mesmos oito tipos simples, com bloqueios/vínculos e
dependentes recusados. UI integrada ao rascunho/histórico; original/cópias salvas
preservados. Referências Adobe/PDF Association, código pypdf local, Git/Python.

14 métodos portáveis passaram em três rodadas. A primeira passou mas gerou
avisos de clonagem por streams diretos; AP passou a ser registrado como objeto
indireto antes da anotação, com asserção de regressão. Rodadas2/3 sem esses avisos.
Resultados preservados em testes/resultados/annotation-extensions-portable-2026-10-18-round*.json.
Regressões prévias de edição em relatórios annotation-advanced/copy-regression.
Seis métodos GTK/Poppler novos preparados: criação/diálogos, comentário/limpeza,
erro/cancelamento, pixels de cinco tipos, CropBox/rotação e busca após reabrir.
Ainda não executados localmente: Windows sem GTK/tela. CI integral é o próximo
passo, incluindo fonte/payload/sandbox e capturas antes da publicação do pacote.

Fonte0.1.13, pacote publicado0.1.12 preservado. Arquitetura44 módulos/58interfaces,
323 entradas estáticas preservadas,23 subconjuntos/duas propostas; roteiro43,93%,
38done/20abertos e paridade0/25 intactos. Sem nova REA/original/VM, rede ou
proteções alteradas. Nuvem adiada/IA excluída, causa de tokens não confirmada.
Contrato/limites em docs/ANOTACOES-AMPLIADAS.md. Fonte ainda requer commit/push e
confirmação; histórico, pacotes e relatórios anteriores preservados.


## 2026/10/18 às 13:35 (America/Sao_Paulo, UTC-03:00) — anotações0.1.13 validadas nos três ambientes

CI39144523775, fonte `b44476272e4e9011c5b4825ab00c8d78830354f1`:400/400 em fonte/payload/sandbox instalado,
sem falhas/erros/skips.20 métodos adicionais:14 portáveis e seis GTK/Poppler.
Todos os380 IDs anteriores preservados, sem renomeação/remoção. Aparências/AP
indiretas, geometria, limites, bloqueios/vínculos, comentários, exclusão e
histórico exercitados. Pixels de cinco tipos, CropBox deslocado/rotação e busca
de comentário após reabrir passaram. Capturas editor/comentário/página/principal
examinadas; demais hashes conferidos. Ferramentas Git/API/Python/pypdf e execução
Linux Debian13/Xvfb/GTK/Poppler/Flatpak; sem nova dependência ou nova REA.

Bundle LinuxitPDF-0.1.13-x86_64.flatpak, 44662456 bytes, SHA256
0fa316cdb5bbf124dc411d79fad7135f77cbbeb3c158f319833b3ef33f6ad024. Artefato12143356416, ZIP SHA256 67c6d0e2fa8279f21a7a483b9040f60f888847097c53a7ca4c014b8fa90c4e9b, igual ao
digest GitHub.106 arquivos app/11 relatórios selados; runtime
2849 arquivos/224ELF/162avisos conferidos.
Smoke5/5, launcher3/3, controles fora HOME negado/concedido passaram.
Evidências em testes/resultados/0.1.13/, raw analysis-local/no-vm-release-artifact-12143356416/.
Relatórios copiados byte a byte. Arquitetura44/58, catálogo323,23subconjuntos/
duas propostas,43,93%/38done/20abertos/paridade0/25 preservados. Critérios/pesos
intactos;50 planos completos de aceitação ainda not_run. Original/VM não executados,
nuvem adiada/IA excluída. Família de anotações continua parcial; demais formulários,
operações, desktop/portal/cliente/AT-SPI/impressão e comparação original abertos.
Sem evidência de esgotamento de tokens. Próximo:publicar e auditar mesmo bundle;
continuar operações/contratos locais e alvos estáticos preservando os lotes.
O download inicial do artefato por blocos maiores terminou por timeout de rede.
A retomada em 44 blocos de até 1 MiB passou, com SHA-256 integral igual ao digest GitHub;
cache e helper em analysis-local/annotation-download-12143356416-parts/ e
analysis-local/download_annotation_artifact.py. Isso não foi falha do CI nem
evidência de esgotamento de tokens.
Próxima operação própria concreta: combos AcroForm editáveis, preservando Opt,
com texto livre/aparência e testes de flags/ReadOnly/limites/histórico; ainda não
implementados. Entrega preparada ainda requer commit/push e confirmação da publicação.


## 2026/10/18 às 13:41 (America/Sao_Paulo, UTC-03:00) — publicação e auditoria anotações0.1.13 confirmadas

Entrega técnica `93a38c318bf9a8859c21c91e9b4eb3f43d49785a` confirmada no GitHub com árvore limpa por recibo
externo. Download público sem login retornou HTTP200, 44662456 bytes,
SHA256 0fa316cdb5bbf124dc411d79fad7135f77cbbeb3c158f319833b3ef33f6ad024, idêntico ao bundle testado.
Auditoria https://github.com/airtonbp19edu/Linuxit-PDF/actions/runs/39145924664 reinstalou mesmo bundle sem rebuild:
106app/2849runtime/224ELF/162avisos conferidos, incluindo modelos
Tesseract por/eng. Sete controles e cinco novos smoke checks passaram. Suítes
400/400 em cada ambiente são do builder; não repetidas nesta auditoria.
Artefato 12143676411, ZIP SHA256 fcdb80a143cdd1387fa6a9b7fb27b838b89ef478c48be7ebc6b2afc5e8af4422, igual ao digest GitHub.
Quatro relatórios copiados byte a byte, revisão em testes/resultados/0.1.13/audit/;
raw em analysis-local/no-vm-audit-artifact-12143676411/. Ferramentas Git/API/Python
e CI Debian13/Xvfb/Flatpak. Roteiro43,93%,38done/20abertos/13etapas, paridade0/25,
catálogo323 e arquitetura44/58 preservados. Nenhum critério/peso alterado.
Sem VM nem original; não houve nova REA ou modificação de rede/proteções Windows.
Novas anotações têm aparência própria, coordenadas antes da rotação e comentário/autor editáveis. Demais operações/famílias permanecem parciais. Nuvem adiada/IA excluída.
Próximo concreto sem VM: combos AcroForm editáveis com texto livre/aparência e
preservação de Opt, testando flags/ReadOnly/limites/histórico; ainda não implementados.
Demais formulários/anotações/contratos próprios continuam; desktop/portal/concessão
persistente/cliente/AT-SPI/impressão física exigem ambientes/equipamentos próprios.
Comparação Foxit exige validar VM offline. Sem evidência de esgotamento de tokens.
Este registro recebe commit/push e comprovante final externo separados, evitando
autorreferência. Preservar lotes estáticos e pacotes/relatórios anteriores.


## 2026/10/18 às 13:53 (America/Sao_Paulo, UTC-03:00) — revisão do indicador de progresso a pedido do usuário

Usuário questionou a repetição de43% desde o início. Revisão matemática e do Git:
55 snapshots de progresso/progresso.json até bc75bc4dd5b0d17c0626384a4e72e075158263bb,
com definições/pesos idênticos. Score inicial43,33%; atual43,93%. A única mudança
de pontuação foi no commit c403fa773d9c5e43374625e37ab88dee590c4711: consulta de
regras remotas da etapa1 passou unknown→done (+0,60 ponto). OCR, TIFF, anotações
e outras entregas não somaram pontos: os grandes critérios de15/16 permanecem
partial e o modelo binário lhes atribui zero. Aritmética correta, indicador
inadequado para quantificar conclusão global da recodificação. Apresentação
anterior enfatizava excessivamente esse número ao responder sobre o projeto.

scripts/update_progress.py e seus relatórios agora separam conclusão global
indeterminada (implementation_completion_percent:null), índice histórico do
checklist e entregas/validação próprias registradas. Campo legado
general_progress_percent preservado para os consumidores existentes. Nenhum
critério, peso, status ou evidência anterior foi alterado; nenhum percentual
substituto foi estimado. Documentação em docs/MEDICAO-PROGRESSO.md; orientações
atuais AGENTS/RETOMADA/tarefas/README ajustadas para não repetir a confusão.

Git/Python/Fraction usados. Evidências em
testes/resultados/revisao-indicadores-2026-10-18/: review.json com os55 snapshots,
14 manifestos e transições; reporting-check.json prova campos anteriores iguais,
106 arquivos app e bundle0.1.13 sem alteração; architecture-review.json confere
44módulos/58interfaces/20critérios abertos; delivery-record-review.json confere
evidências registradas. Relatórios selados atuais reconferidos por hash.
Não houve nova execução da suíte400/400, nova REA/Ghidra, original ou VM. Pacote,
licenças, nuvem adiada/IA excluída e paridade0/25 preservados.

Próximo trabalho funcional: combos AcroForm editáveis, com texto livre/aparência,
preservação de Opt e testes de flags/ReadOnly/limites/histórico. Uma futura
porcentagem operacional exige catálogo delimitado e pesos/aceitação explícitos,
com revisão de método registrada. Alterações de relatório preparadas para
commit/push; confirmação remota e recibo final externo após publicação.

## 2026/10/18 às 16:27 (America/Sao_Paulo, UTC-03:00) — preparação parcial da VM para Linuxit-PDF

Usuário escolheu Linuxit-PDF como primeiro projeto na preparação do laboratório
Windows 10/VirtualBox. Fonte Linux/Flatpak continua sendo a entrega própria;
a VM Windows será usada para observar Foxit e produzir a referência offline.
Nenhum original, cenário D01-D20, GUI do Linuxit ou comparação diferencial foi
executado nesta rodada. Paridade, critérios, pesos e versão não alterados.

Ferramentas: PowerShell do hospedeiro, VBoxManage/API COM oficial, Python 3.13,
SHA-256 e Git somente leitura. VM Windows 10 com Guest Additions 7.2.20,
10.000 MB/4 vCPUs. Backup completo externo à pasta da VM, 9 arquivos/21,42 GiB,
conferido por hash; boot dessa cópia não testado. Snapshot ao vivo inicial não
avançou; cancelamento normal mais pausa expôs inconsistência entre estado
externo Running e interno Suspended. Segundo snapshot concluiu preservando
memória; a instância foi encerrada, o snapshot restaurado e reaberto. Log
confirmou RESUMING -> RUNNING e tela manteve a sessão aberta. Recuperação deste
snapshot exercitada; não confundir com teste de restauração do backup completo.

Evidência privada: scripts/guia/lab-host-state.json no workspace irmão
Testes de IA; backup em B:\Backups\VirtualBox\Windows10-2026-10-18_160415;
snapshot 00-recuperar-sessao-20261018, UUID639a6bc1-bc44-4718-9e7a-b9e924619712.
Kit fora de Git/OneDrive em A:\Airtonbp19\LabKits\Linuxit-PDF-20261018-1630:
3292 arquivos/499259372 bytes copiados e verificados antes/depois; identidade
Foxit conferida contra projeto.json; oito fixtures da campanha final da etapa18
preservadas byte a byte, plano/modelo intactos, 17 casos ainda not_run.
Não regenerar corpus nem promover esses preparativos a observação funcional.

NAT ainda conectado para preparação. Acesso SSH encaminhado apenas em
127.0.0.1:2222 do hospedeiro; LabSetup/LinuxitKit temporários e somente leitura.
Bootstrap administrativo no convidado ainda depende de execução pelo usuário;
sem acesso autenticado confirmado, sem provisionamento de ferramentas ou
isolamento offline validado. Chave privada exclusiva fora do OneDrive; nenhuma
senha solicitada. Proteções do Windows do hospedeiro não desativadas.

Git local/remoto main coincidiram em 955f6c2df17c1d27c0fd0ea87be51414ad751446
antes desta nota; checkout estava limpo. Esta nota é o único arquivo alterado
neste repositório pela rodada. Sem commit/push deste preparo parcial.
Próximo passo: usuário executa Preparar-Acesso.ps1 como administrador dentro da
VM; conferir SSH/Windows/perfil local, copiar/verificar kit em C:\Linuxit e
remover compartilhamentos/clipboard/rede antes de qualquer execução Foxit,
seguindo ETAPA-10/18. Validar controle responsivo e registrar contenção real.
## 2026/10/18 às 17:03 (America/Sao_Paulo, UTC-03:00) — VM configurada; testes somente no chat do Linuxit-PDF

Usuário executou bootstrap e, nesta rodada, determinou explicitamente que os
testes de aplicativo devem ser feitos apenas no chat apropriado do projeto.
Este chat ficou restrito à infraestrutura. Nenhum Foxit, cenário funcional,
comparação, GUI do Linuxit ou suíte própria foi executado. Critérios, pesos,
paridade e versão preservados. Não iniciar testes neste chat de laboratório.

Acesso SSH por chave confirmado na conta local IA Machine. Windows 10 Pro
19045.3803, Guest Additions7.2.20, Brave155.1.97.59 e WinGet1.29.380 conferidos;
10.000MB/4vCPUs, aproximadamente56GiB livres antes do kit. Suspensão, hibernação
automática e apagamento de tela em AC configurados em zero só no convidado.
Defender/tempo real permaneceram ativos; nenhuma proteção do host foi alterada.
Não houve inscrição ESU, atualização do SO ou instalação da pilha geral REA
na VM; análise pode continuar no ambiente já existente do projeto.

Kit privado copiado para C:\Linuxit:3292 arquivos/499259372bytes conferidos
contra manifesto por SHA-256; referência mantém o hash90208c9e8da92c8e546b76c8f4a2f8fb999105d124e663bbea6744fb6bb6b3a6.
Oito fixtures da campanha final da etapa18 e protocolos/modelos preservados;
17 observações continuam not_run. Correção de herança da DACL seguida de nova
conferência completa aprovada. Reference/Input/Protocol têm RX para usuários
sem elevação; Results permite gravação à conta local. A negação de escrita
pelo token limitado ainda precisa de validação runtime no chat do projeto.

Uma tarefa auxiliar de controle interativo não chegou a abrir o Notepad:
falhou ao localizar VBoxControl no caminho inicialmente presumido. Caminho
corrigido para System32; não foi reexecutada após a orientação do usuário.
Tarefa removida e ausência de seus processos/Foxit confirmada. A infraestrutura
não ganhou aprovação de GUI por existir processo ou script. Controle do
marcador LINUXIT_RUNTIME_PROBE e contenção dentro do guest continuam pendentes.

Isolamento configurado e conferido no hospedeiro: nenhum adaptador com cabo
conectado, nenhuma pasta compartilhada, clipboard/drag-drop/áudio desligados,
zero dispositivos USB capturados e VRDE off. xHCI virtual permanece disponível,
sem passthrough do host. SSH deixa de funcionar nesse modo. Não religar NAT ou
clipboard com a referência aberta. Kit está local; não precisa de pasta pessoal.

Novo snapshot01-linuxit-configurado-offline-20261018-1701,
UUID0ba95c19-5b6d-4c6b-a6ed-0cb3e59734d6:VM pausada antes da captura,100%
concluída e retomada RUNNING confirmada, rede/clipboard ainda off. Restauração
deste novo snapshot não testada. Snapshot de recuperação anterior e backup
completo em B:\Backups\VirtualBox\Windows10-2026-10-18_160415 preservados;
inicialização a partir da cópia completa continua não testada.

Relatórios privados no workspace irmão Testes de IA:lab-host-state.json,
evidence/guest-preparation-20261018.json e
evidence/prep-linuxit-20261018-1700-host-containment.json. No convidado,
C:\Lab\Reports contém bootstrap,inventário,ajustes,stage e adiamento de testes.
Guia LEIA-ME-LABORATORIO.md atualizado. Estes registros não substituem evidência
funcional nem aprovam critérios dinâmicos da etapa10.

Próximo passo exclusivamente no chat Linuxit-PDF: consultar esta nota e os
relatórios, confirmar perfil sintético/contenção no convidado e controle de
interface antes de abrir referência; então seguir ETAPA-10/18 com os mesmos PDFs.
Código/pacote não alterados. Esta rodada acrescenta apenas esta nota ao arquivo
de continuidade; sem commit/push da configuração local da VM.

## 2026/10/18 às 18:45 (America/Sao_Paulo, UTC-03:00) — primeira campanha real do Foxit na VM offline

Pedido: continuar os testes na VM e preservar a continuidade local/remota.
As notas de infraestrutura das16:27/17:03, trazidas pelo outro chat, foram
preservadas. Main local/remoto conferidos em955f6c2df17c1d27c0fd0ea87be51414ad751446
antes desta publicação; nenhum reset, force push ou restauração do snapshot.

A revisão automática inicialmente bloqueou a manutenção com rede. O usuário
respondeu expressamente “Autorizar manutenção breve com Foxit fechado”. SSH
usado somente nesse preparo; cabo desconectado antes do controle/original.
Host/guest conferidos durante e ao fim:zero cabos conectados/shares/USB capturado,
Ethernet Disconnected, sem SMB, clipboard/drag-drop/VRDE/áudio off. Perfil
sintético local, sessão interativa limitada não elevada. RX exercitado e
repetido em Reference/Input/Protocol. Nenhuma proteção do host foi alterada.

Ferramentas: VBoxManage/API COM/Guest Additions7.2.20, PowerShell, SHA-256,
Computer Use por @oai/sky e teclado virtual nativo do VirtualBox; Python3.13,
comparador próprio e Git. Scripts próprios scripts/foxit_vm_probe.ps1 e
scripts/guest_foxit_probe.ps1 usam comandos fixos e propriedades fragmentadas;
sem transporte de código arbitrário, rede ou clipboard. Notepad com marcador
LINUXIT_RUNTIME_PROBE respondeu visualmente antes da abertura do original.
Fonte publicada com LF; hash do coletor efetivamente executado e hash publicado
separados em session.json. Não houve nova rodada REA/Ghidra nem esgotamento de
tokens confirmado. Atrasos e relógio do guest impedem conclusões de desempenho.

Foxit2025.2.0.33046x86 executado, interface/versão examinadas; SHA-256
90208c9e8da92c8e546b76c8f4a2f8fb999105d124e663bbea6744fb6bb6b3a6
antes/depois igual. Dez arquivos Input, incluindo oito fixtures preservados
da etapa18, mantiveram hashes. Results recebe somente saídas sintéticas.
Campanha D01–D20:14 observados em recortes delimitados,5 parciais,1 inconclusivo;
esses estados não significam aprovação integral dos cenários/famílias.
Abertura/navegação/zoom/rotação de visualização, busca por escopos/opções,
inválido/vazio/senha sintética, anexo, prévias, cópia/reabertura e fechamento
foram observados. Incidente de mudança de estilo no rascunho D08 revertido;
D08 repetido limpo e Input nunca gravado. IA/nuvem/contas não exercitados.

Importador aceitou11 recortes no protocolo exato:10 métricas iguais e1
divergência, Foxit encontra1 ocorrência em autor de comentários onde Linuxit
retorna0. Outros5 inconclusivos e1 sem a consulta/fontes exatas. D07/D10
precisam navegação pelos hits; contagens/ordem visual e clique no painel de
marcadores não foram promovidos a destinos de busca. D12 concluiu250 hits
antes do cancelamento. Vazio desabilita Search; não inferir busca submetida.
Prévia D18 não corresponde às margens/ordem de streams pedidas no comparador.
D15 senha correta foi inserida após rejeição, sem terceira abertura independente.
Nenhuma impressão foi enviada. Cópia9.100bytes e anexo22bytes tiveram hashes
conferidos; cópia reaberta com2páginas/2marcadores/comentário/autor visíveis.

D20: janela encerrada e reaberta, sem abas restauradas, histórico local retido;
aviso de visualizador padrão reaparece. PID antigo5464 permanece RespondingTrue
sem título; PID novo6964 ausente do relatório final. Causa/saída completa
pendentes. Notepad controle1056 permanece. Relatório final e probe-stop
recebidos/examinados; stop encerra o coletor, sem terminar o Foxit. VM mantida
offline; investigar processo residual antes de qualquer nova manutenção com rede.

CI Linux desta rodada39163934943, fonte955f6c2, artefato12149742247:
400/400 testes próprios sem falhas/erros/skips, smoke GTK5/5 e17/17 recortes
próprios no corpus preservado. ZIP442043bytes/SHA-256
a4f21ff8723c86afd6d9375e280f6b2b9d3cbbfbeea7a1b3f44c5ffa7185731d
conferidos, relatórios copiados byte a byte. 16/16 controles do importador
reexecutados no Windows; especificação25famílias/50planos e arquitetura
44módulos/58interfaces/19critérios abertos conferidas; dois scripts PowerShell
sem erros de parser. Revisão de124 arquivos privados por hash, seis selos de
relatórios e106 arquivos app iguais ao CI aprovada. Fontes app/pacote0.1.13/devel
intactas; nenhum Flatpak novo. A normalização LF de JSON próprios ganhou selos
atualizados; rascunhos anteriores preservados localmente, sem nova medição.

Publicável: docs/VM-FOXIT-2026-10-18.md e testes/resultados/vm-2026-10-18/
(session, casos, observações, comparação, CI, controles, arquitetura, índice
privado e review). Telas/cópias/logs completos e auxiliares em
analysis-local/vm-20261018-1710/ e no artefatoCI local ignorado pelo Git.
Não foram incorporados código/DLLs/recursos proprietários à implementação.

Apenas o critério ambiente isolado/original executável passou a done mediante
prova examinada. Pesos/definições preservados:checklist43,93→45,13%,39done/19abertos;
estados dinâmicos/diferenciais amplos passam a partial, sem pontuar. Percentual
global de recodificação continua null/indeterminado; nenhuma família encerrada
(0/25),50 casos completos de aceitação continuam sem execução integral.

Git neste checkpoint: alterações preparadas para commit/push; publicação ainda
não declarada nesta nota. Confirmação remota será acrescentada após sucesso,
com recibo final fora da árvore. Próximo passo concreto: completar D07/D10 e
D11 exato; tornar cancelamento observável; investigar D20; medir imposição nos
parâmetros exatos; converter a divergência de autor em contrato/regressão e
corrigir/testar a busca própria em marco posterior. Desktop Linux/portais,
AT-SPI, cliente de sincronização e impressão física seguem pendentes separados.


## 2026/10/18 às 18:47 (America/Sao_Paulo, UTC-03:00) — publicação da campanha da VM confirmada

Commit d80aafcb4c4eb2f08def8890639ec03aee997963 publicado em main no GitHub.
scripts/verify_git_sync.py conferiu o HEAD por ls-remote:local/remoto iguais,
árvore limpa e sincronização confirmada. Recibo LinuxitPDF-vm-campaign-*.json
salvo no TEMP, fora da árvore, evitando autorreferência. Este registro atualiza
current_dynamic_execution para confirmed_at_recorded_commit; o commit de
confirmação será conferido novamente com recibo final externo.

Marcos/evidências, fonte0.1.13, métricas, paridade0/25 e pendências preservados.
VM segue offline, coletor encerrado, processo residual D20 documentado.
Próximo passo: D07/D10/D11 exatos, cancelamento ativo, saída de imposição e
investigação D20; divergência de autor já medida aguarda correção própria.


## 2026/10/18 às 19:13 (America/Sao_Paulo, UTC-03:00) — checkpoint solicitado para continuar em outra IA

Usuário pediu salvar o progresso, informar pendências e o arquivo de retomada.
Arquivo principal: docs/RETOMADA.md, seção “Passagem para outra IA”. Inclui estado
consolidado, ordem de leitura, caminhos locais/publicáveis/privados, próximo
lote concreto e limites das evidências. Histórico permanece neste arquivo.

Git local/remoto conferidos em d7bf1fb5d3b626394e58dba24642f4a77500295a,
árvore limpa antes da edição. Corrigidos dois trechos antigos de RETOMADA que
ainda diziam zero observações originais e NAT ativo sem distinguir o diagnóstico
histórico; fonte factual são a campanha e os relatórios já publicados. Nenhuma
VM foi operada nem teste repetido neste checkpoint; o estado de processos/rede
é o último examinado e deve ser reconferido pela próxima IA.

Pendências priorizadas: D20/processo residual; D07/D10/destinos e ordenação;
D11/protocolo exato; D12/cancelamento ativo; D15/abertura independente com senha;
D18/saída PDF e margens exatas; UI01–UI10/IDs7911/7913. Criar regressão e corrigir
busca por autor, Foxit1/Linuxit0; completar operações AcroForm/anotações/contratos,
análise estática dirigida e testes de desktop Linux/portal/AT-SPI/sincronização/
impressão física. Cinquenta planos completos ainda sem execução integral,
19 critérios abertos e paridade integral0/25. Índice45,13% é somente checklist;
conclusão global do código continua indeterminada. IA excluída/nuvem direta adiada.

Coletor vm-20261018-1710 já encerrado; não reutilizar RunId para novos comandos.
Última coleta tinha Foxit5464 sem janela e Notepad1056; não conectar rede com
referência ativa. Para novo lote, manter corpus/saídas anteriores e revalidar
contenção, token limitado e controle visual. Evidências privadas continuam em
analysis-local e VM local; clone Git não as inclui.

Apenas docs/RETOMADA.md e esta nota mudaram; aplicativo, pacote0.1.13/devel,
progresso estruturado e relatórios selados preservados. Checkpoint preparado
para commit/push autorizado; confirmação final será por ls-remote e recibo
externo, sem depender deste chat.


## 2026/10/18 às 19:24 (America/Sao_Paulo, UTC-03:00) — retomada e correção de autor; CI pendente

Retomada no main4063ca7346db4c837d4850ac07b8c5394fc36181, local/remoto iguais,
árvore inicialmente limpa. Pedido do usuário: dar continuidade às pendências.
Fonte app/search_engine.py inclui autor de comentário na busca após a
observação offline preservada C18-D09-author. Fixture/hash/protocolo mantidos;
expectativa própria0→1 com histórico explícito, sem alterar relatórios selados.
Três regressões novas:contra a fonte anterior,duas falhas esperadas/uma passou;
contra a corrigida,3/3passaram,zero erros/skips.16controles do comparador passaram.
Caso de escopo foi renomeado para o novo contrato; caso GTK ampliado para autor.
Contrato estruturado/renderização e arquitetura conferidos. Relatório
em docs/BUSCA-AUTOR-COMENTARIOS.md. Fonte posterior ao pacote0.1.13,sem pacote novo;
CI Linux completo e nova comparação ainda pendentes neste checkpoint.

Computer Use/sky examinou Gerenciador de Tarefas do guest offline:Foxit5464
continua em segundo plano,usuário IA Machine,status Em execução. Não encerrado
nem rede religada. Diagnóstico de causa ainda em andamento; capturas privadas
em analysis-local/resume-20261018-1918. Nenhuma proteção alterada nem novo cenário
Foxit declarado aprovado. Pesos,19critérios abertos,paridade0/25 preservados.
Este commit permite validar a fonte no CI autorizado; registrar resultados
examinados e publicação final após a execução, antes de considerar a correção fechada.


## 2026/10/18 às 19:31 (America/Sao_Paulo, UTC-03:00) — busca por autor validada no Linux e cadeia de espera D20

Fonte corrigida168381b15a501a5a53c933e8b8f3f479559630cb publicada no GitHub.
CI39172130287 concluiu success; artefato12152449979 com443026bytes e SHA-256
0f83658a30a646da916ef516c33fe7a67509cf5eba7e4412ccdc658bc84c43d3
conferido contra GitHub e baixado em pasta nova analysis-local/no-vm-release-artifact-12152449979.
Relatórios realmente examinados:403/403 testes próprios na fonte Linux,
zero falhas/erros/skips,smoke GTK5/5,17/17 contratos de backend,sem bloqueios/erros.
106arquivos app correspondem ao CI; único alterado desde a campanha anterior:
search_engine.py. Dos400IDs anteriores,399preservados,um renomeado para incluir
autor,3métodos portáveis novos. O caso GTK ampliado de escopo/autor passou.

Comparação reexecutada com os mesmos17 hashes de fixture/protocolo e o registro
original preservado:testes/resultados/vm-2026-10-18/foxit-observations.json.
Onze recortes com métricas comparáveis agora coincidem (11/11),zero divergência
nessas medidas;cinco inconclusivos/um pendente preservados. Busca autor agora
Foxit1/Linuxit1,na página1. Não houve nova busca no original; essa campanha
reutiliza observações já examinadas e verifica seus hashes. Expectativa própria
atualizada com histórico,sem mudar o protocolo nem apagar o resultado antigo.
Não são onze famílias encerradas. Famílias completas0/25,50planos completos
not_run,19critérios abertos,pesos/índice45,13% preservados;recodificação globalnull.

D20 investigado via Computer Use/sky e Gerenciador de Tarefas do guest:
Foxit5464 permanece Em execução em segundo plano,sem janela. Cadeia de espera
examinada mostra threads6804e2508;2508 aguarda splwow64.exe/PID3880. Mensagem
Windows menciona E/S de rede,mas isso não prova tráfego externo nem causa raiz.
Host reconferido às19:25:running,zero cabos/shares/USB capturado,clipboard/
drag-drop/VRDE/áudio off. Nenhum processo foi terminado,original relançado,
coletor reiniciado ou proteção alterada. Janelas de diagnóstico fechadas após
captura; Explorer do guest restaurado. D20/encerramento completo continua aberto.

Provas publicáveis: docs/BUSCA-AUTOR-COMENTARIOS.md e
testes/resultados/busca-autor-2026-10-18/:review,relatóriosCI,comparação após,
três regressões antes/depois,16controles,arquitetura e d20-followup sanitizado.
Telas originais/diagnósticos completos somente em
analysis-local/resume-20261018-1918/ e campanha original ignoradas pelo Git.
Captura d20-wait-chain.png examinada por imagem e hash. Contratos/especificação,
matriz,pontos de retomada e registro de critérios atualizados sem encerrar
etapas amplas. Não houve nova REA/Ghidra. IA excluída,nuvem direta adiada.

Pacote0.1.13/devel não foi reconstruído:os400/400 de fonte/payload/sandbox
pertencem ao marco anterior.403/403 desta rodada valem apenas para a fonte nova.
Próximo passo de implementação: preparar marco de pacote após outras mudanças
úteis;não afirmar que o Flatpak antigo contém a correção. Próximo lote da VM:
D07/D10 destinos/Sort By,D11 exato,D12 cancelamento ativo,D15 abertura com senha
independente,D18 saída com margens correspondentes,UI01–UI10 e causa de D20.
Demais AcroForm/anotações/conversões,estática dirigida e desktop Linux seguem
listados em RETOMADA/tarefas-pendentes;não reiniciar análises preservadas.

Git:fonte168381b publicada e testada;este checkpoint acrescenta os resultados e
a continuidade,sem nova alteração app/testes desde o CI. Commit/push autorizado
e conferência final por verify_git_sync.py com recibo externo são o fechamento
desta rodada. Preservar evidências e alterações de outros colaboradores.


## 2026/10/18 às 19:49 (America/Sao_Paulo, UTC-03:00) — segundos na barra da VM e novo lote offline

Pedido do usuário:habilitar segundos no relógio do Windows10 da VM antes de
continuar os procedimentos restantes. HKCU Explorer\Advanced,
ShowSecondsInSystemClock DWORD1,anterior ausente;somente perfil sintético do
guest alterado,host intacto. Explorer reiniciado via Computer Use/Gerenciador
de Tarefas. Capturas examinadas19:46:26e19:46:42 confirmam relógio na barra
atualizando com data abaixo. Isso não comprova resposta do Foxit nem elimina
atraso do relógio para benchmarks. Comprovante/docs:docs/VM-RELOGIO-SEGUNDOS.md e
testes/resultados/vm-2026-10-18-segundos/clock.json. Capturas/logs privados em
analysis-local/vm-20261018-1940/.

Foxit residual5464 encerrado à força pela UI antes de manutenção;ausência
conferida visualmente e por Get-Process no guest. D20 continua sem encerramento
normal/correção da causa. Manutenção SSH breve previamente autorizada com
referência fechada. Primeira tentativa ultrapassou limite da linha de comando;
finally desligou cabo. Segunda dividiu os comandos,aplicou chave e preparou
nova tarefa/coletor limitado LinuxitProbe-vm-20261018-1940;rede desligada antes
de preflight/controle/original. Nenhuma proteção alterada ou software instalado.

Novo preflight realmente examinado:hash original90208c9e...6b3a6 preservado,
10Inputs idênticos,escrita negadaReference/Input/Protocol,EthernetDisconnected,
zero NICcabo/share/USB capturado/SMB,clipboard/drag-drop/VRDE/áudio off,
sessão1nãoelevada. ControleNotepad2300 abriu e SelectAll respondeu visualmente;
ack registrado antes de lançar original5280 offline. Coletor novo em andamento,
2horas após19:45;não confundir com coletor1710 encerrado. Guias/hash anteriores
preservados. Próximo lote:D07/D10destinos,D11exato,D12cancelamento,D15senha
independente,D18saída/UI01–UI10. Nenhum novo cenário aprovado neste checkpoint.

Git inicial main/local/remoto a2496dd3a257fa7153aeb84d6f6ff43a886e498e.
App/testes/pacote permanecem intactos;403/403 é validação anterior,não repetida.
Pesos/19critériosabertos/paridade0/25preservados. Este checkpoint do relógio
será publicado enquanto os testes da nova rodada continuam.

## 2026/10/18 às 20:09 (America/Sao_Paulo, UTC-03:00) — continuação após relógio com segundos: UI01/D07 parciais

Continuação do pedido de habilitar segundos e seguir os testes. O ajuste já
publicado em5c6277c foi preservado. Computer Use/sky, teclado nativo VirtualBox,
VBoxManage e coletor próprio limitado por GuestProperties, sem rede, shares,
clipboard ou proteções alteradas. Não houve nova REA/Ghidra nesta rodada.

UI01: Abrir sem documento alcançou Input; Cancelar voltou à área vazia.
Capturas realmente examinadas. Falta variante com PDF aberto e correlação
dinâmica do ID; UI01 não foi encerrado. D07 repetido com alvo, literal, apenas
marcadores, case/whole/stemming/attachments/highlight-all desligados: duas
instâncias, ALVO marcador e alvo externo, nessa ordem, Relevance Ranking.
Cliques/duplo clique tentados, mas destinos continuam inconclusivos devido à
resposta intermitente do ambiente. Não inferir sucesso/falha de navegação nem
destino nulo; não aprovar C18-D07 ou família por essas telas.

Relógio ficou visualmente em19:59:21 em observações sucessivas e depois avançou.
Coletor também demorou a responder. Host declarou running; VBox.log preservado
contém avisos de heartbeat/recuperação do temporizador. Dois ciclos breves de
pause/resume, sem reboot/snapshot/restauração/alteração de RAM ou CPUs. Resposta
retornou depois; causa raiz e correção permanecem não demonstradas. Tempos do
guest atrasados e pausas invalidam benchmark. Não atribuir isso ao Foxit nem
a esgotamento de tokens. Aplicativo de controle relançado pelo preflight final
não recebeu um segundo controle visual aprovado; PID não basta.

Preflight final-inputs:completed, sessão1 não elevada; identidade original e
dez hashes Input iguais ao início; escrita negada Reference/Input/Protocol,
Ethernet desconectada, zero SMB/share/USB capturado, clipboard/drag-drop/VRDE/
áudio off. Coleta checkpoint-final recuperada completed; Foxit5280 com janela,
Responding=true, Notepad2300/9584. probe-stop:stop recuperado completed; coletor
vm-20261018-1940 encerrado. Não enviar novos comandos esperando resposta dele.
VM permanece offline; não religar rede com original ativo. D20 não aprovado.

Publicável: testes/resultados/vm-2026-10-18-segundos/followup.json e
docs/VM-RELOGIO-SEGUNDOS.md; RETOMADA, AGENTS e tarefas-pendentes atualizados.
Privado: analysis-local/vm-20261018-1940/ com telas, relatórios originais,
VBox-final.log e horários host de pause/resume. Nenhum payload Foxit publicado.
Verificação ad hoc confere identidade/contenção e os dez Inputs, além dos hashes
das evidências referenciadas. Não houve alteração de app/testes nem nova suíte
Linux:403/403 da fonte corrigida é validação anterior; Flatpak0.1.13 permanece
anterior à correção e não foi reconstruído. Pesos/19abertos/45,13% do checklist,
paridade0/25 e recodificação globalnull preservados.

Próximo passo: verificar estabilidade/resposta visual do controle e preparar
novo coletor antes de continuar D07/D10 destinos/ordenação, D11 consulta exata,
D12 cancelamento ativo, D15 senha correta independente, D18 saída com parâmetros
correspondentes e UI01–UI10; investigar causa D20. As operações locais, estática
dirigida e desktop Linux seguem no ponto de retomada, sem reiniciar análises.

Git inicial main/local/remoto5c6277cb2231a846e768fb5a212b9ae2fdc63a7e.
Fechamento autorizado: publicar somente documentação/metadados deste checkpoint
e conferir remoto por verify_git_sync.py, com recibo fora da árvore para evitar
autorreferência. Nenhum reset/force push ou alteração alheia substituída.

## 2026/10/18 às 20:53 (America/Sao_Paulo, UTC-03:00) — consulta exata D11 e checkpoint antes de senha

Pedido: retomar e, se parar a VM, salvar e avisar. Regra registrada em AGENTS e
VM-RELOGIO-SEGUNDOS; observar novamente após dez segundos externos sem nova
entrada quando houver suspeita. Clock parado não define causa Foxit. Nesta
rodada não houve pause/resume/reboot/restauração nem proteção alterada.

Rodada vm-20261018-2020 preparada por manutenção SSH breve previamente autorizada
com Foxit fechado, ausência examinada em Task Manager e conferida no guest;
mesmo script próprio hash8a8b4ae...3e13, tarefa interativa limitada. Cabo off
antes dos controles e original. Token1nãoelevado, dez Inputs iguais, escrita
negada Reference/Input/Protocol e contenção host/guest conferidos. Notepad3128
selecionou o marcador; original2444 lançado offline. CUA/sky e teclado nativo
VirtualBox usados; não houve nova REA/Ghidra. Clock avançou, com atraso.

UI01: Abrir com documento e Cancelar preservaram busca-escopos.pdf página1/2;
variantes sem documento já preservadas1940. Sem correlação dinâmica do ID.
D07 repetido: alvo, só marcadores, duas instâncias/mesma ordem; seleção refletiu
painel lateral, página1 permaneceu nas tentativas; Enter terminou em New Search.
Destinos/foco/ativação continuam inconclusivos, sem inferir null/defeito.

C18-D11-missing realmente executado: termo-inexistente-123, literal, páginasoff,
marcadores/comentárioson; case/whole/stemming/anexos/highlightoff. Zero documentos
e instâncias observados; capturas opções/resultado examinadas. Comparação nova
1/1 com medidas próprias já obtidas no CI39172130287/168381b;106arquivos app
atuais iguais ao manifesto. Não repetida suíte403/403 nem pacote0.1.13/devel.
Consolidado separado12casos distintos iguais:11preservados1710 e1novo2020;
zero divergentes,cinco inconclusivos,zero aguardando original. Não repetir
contagens de etapas/famílias:19critérios/pesos45,13%/paridade0/25 preservados.

Postflight after-search-inputs trouxe payloadcompleted/identidade/dez Inputs
inalterados/escrita negada/offline. Leitor normal não recebeu Count; oito partes
realmente enumeradas recuperadas por leitura dupla idêntica, Base64 canônico,
UTF8estrito e JSON completo, hash64368979...29ba2d. Metadados preservados; isso
não prova saída da tarefa nem conclusão do transporte. Coleta complementar
after-search-collect solicitada, conferir resultado antes de novo comando.

Publicáveis: docs/VM-BUSCA-2026-10-18-2020.md,
testes/resultados/vm-2026-10-18-2020/:foxit-observations,comparison-d11,
comparison-rollup,review. Privados: analysis-local/vm-20261018-2020/ e helpers
analysis-local/prepare_probe_2020.ps1,recover_vm_report.ps1,finalize_search2020.py.
Nenhum payload Foxit publicado. Git base05218ff local/remoto confirmado; este
marco é documentação/metadados. Commit/push e recibo externo fecharão publicação.

Próximo passo concreto: D15 senha correta em abertura independente enquanto
clock/controle responderem; D07/D10destinos,D12cancelamento,D18saída e UI restantes
preservados. D11vazio continua inconclusivo: botão Search desabilitado não é
zero de backend. Se relógio/ambiente parar, interromper entradas, salvar e avisar.

## 2026/10/18 às 21:32 (America/Sao_Paulo, UTC-03:00) — D15 observado e interrupção pelo relógio

Pedido: continuar e, se parar, salvar e avisar. Prossegui na rodada
vm-20261018-2020, mantendo contenção e original já identificado. CUA/sky e teclado
nativo VirtualBox usados; nenhuma nova REA/Ghidra, análise estática reiniciada,
alteração de proteção, pause/resume/reboot ou restauração.

D15: solicitação nova/campo vazio, senha sintética correta na primeira tentativa,
sem senha errada nessa abertura; com-senha.pdf SECURED abriu8 páginas. Navegação
1→8→1 conferida. Cancelar/rejeitar continuam evidências anteriores. Variante
independente observada, sem aprovar família completa de criptografia.
UI05 adicional: busca-escopos.pdf+com-senha.pdf, Print All Tabs habilitado,
confirmação Batch Printing, Don't ask again desmarcado; No retornou à página1/8.
Não foi enviada ação de impressão. Par previsto com geometria.pdf e demais
contextos continuam pendentes; IDs não correlacionados dinamicamente.
D20: X do título fechou o Foxit normalmente, sem força. Ausência examinada em
Task Manager e confirmada0processos pela manutenção breve já autorizada. Isso
não resolve a espera anterior em splwow64 nem o contrato amplo após imprimir.

Postflight limitado completo recuperado do disco por SSH somente com Foxit
ausente: hashfec70445...75bce1, identidade e dez Inputs iguais, escrita negada,
offline host/guest. Cabo desligado em finally; não iniciado original. Tarefa2020
Ready/LastTaskResult1, não stopcompleted. Complemento after-search-collect foi
recuperado por17 partes/duas leituras idênticas, hash0f8c6bcc...ba0d59.

Dois problemas do observador identificados: nomes Count64/65/66bytes excediam
63úteis e havia256 propriedades. Fonte oficial VirtualBox consultada; controles
no instalado7.2.20 aceitaram63 e rejeitaram64. Arquivadas/removidas somente151
propriedades Result antigas de coletores encerrados (55da1940+96da1710), sem
apagar arquivos do guest ou evidências locais. Host agora rejeita recibo longo
antes de agir e exige reserva64+2; guest confere nome/tamanho/saída do Count.
Ambos scripts passaram no parser; ID longo e falta de capacidade foram rejeitados,
Command inalterado. Integração/deploy do guest corrigido NÃO realizados.
Validador estrutural conferiu44 módulos,58 interfaces,25 famílias e os19
critérios abertos; isso não executa comportamento do aplicativo.
Hashlocalnovo guestb20ad4dc...7cac1 e hostf16db312...7c756c; guest conserva8a8b4ae...3e13.
Preparador privado prepare_probe_2130.ps1 escrito, não executado; tarefa2130 não criada.

Relógio apareceu21:24:14 em observações sucessivas; após dez segundos externos
sem entrada continuou igual. Confirmação00:27:45UTC/21:27:45SãoPaulo. Testes e
entradas interrompidos; usuário avisado. Captura VBox privada também mostra
21:24:14. VBoxrunning não aprova resposta. Foxit já fechado e redeoff; causa
desconhecida, sem atribuir a Foxit, tokens ou à falha de transporte.

Publicáveis: docs/VM-SENHA-E-PARADA-2026-10-18.md e
testes/resultados/vm-2026-10-18-2020/password-followup.json,24 hashes de evidência.
Privados: analysis-local/vm-20261018-2020/, recover_probe_2020_postflight.ps1,
finalize_password_followup.py, record_password_progress.py e preparador2130.
App/Flatpak preservados, sem suíte403/403 repetida ou pacote novo; apenas scripts
de observação/documentação/metadados alterados. Consolidado12igual/cincoinconclusivo
mantido, sem nova métrica C18. Critérios/pesos45,13%/19abertos/paridade0/25 intactos.

Git base552ee5e058fded4141d21f4eff43bc45cc6f28ed local/remoto confirmado no marco
anterior. Publicar este checkpoint autorizado e confirmar HEAD remoto/árvore limpa
com verify_git_sync.py e recibo fora da árvore; não declarar push só por commit.
Próximo passo: quando a VM responder, revisão visual recente/ausência do original,
novo RunId, instalar coletor corrigido, cabooff, validar pf/col/end com token
limitado e recibos completos antes do original. Depois D07/D10destinos,D12ativo,
D18saída e UI restantes. Não enviar comandos esperando resposta do coletor2020.

## 2026/10/18 às 21:55 (America/Sao_Paulo, UTC-03:00) — pendências organizadas em etapas

Pedido: organizar tudo que falta em etapas para prosseguir. Examinados Git local
e remoto c62ae3c, AGENTS, projeto/progresso, registro dos 19 critérios, matriz das 25
famílias, especificação/50 planos, casosD/UI/C18, marcos recentes e próximos alvos
REA preservados. A memória foi consultada por palavras-chave e não teve achados
relevantes. Não houve nova inspeção/entrada na VM, execução do original, alteração
de código do app, build Flatpak ou repetição das suítes Linux.

Criados docs/PLANO-DE-CONTINUIDADE.md e progresso/plano-continuidade.json: dez
pacotes P01–P10, dez lotes B01–B10 (B10cloud adiado), inventário resumido por
família, dependências de início e de encerramento, entregas e critérios para
concluir cada etapa; cruzamento exato dos 19 critérios antigos sem modificá-los.
As21 etapas ponderadas não foram substituídas. A organização não conclui P01:
falta decompor operações e reconciliar especificação/matriz com evidências recentes.

Fila sem VM: P01 inventário/reconciliação; P06/B01 combo AcroForm editável como
próximo incremento próprio com contrato suficiente; P04 estática dirigida, sem
repetir48 entradas. P05 contratos/fixtures, P07 integrações reais Linux e P09
marcos de pacote seguem por recursos disponíveis. Sequência original P02→P03→P08:
validar coletor corrigido quando a VM responder, completar protocolos/UI e comparar.
Último relógio21:24:14/parada permanece registro anterior, não confirmação atual.
Coletor2020 terminou com erro; tarefa 2130 e deploy novo continuam não realizados.

D11-missing e D15 independente preservados como observados, sem tratá-los como
pendentes de primeira execução. D07/D10destinos,D12ativo,D18saída e espera de
impressãoD20 seguem abertos; UI05extra não equivale ao par planejado. Plano cobre
Windows nativo posterior, portal/cliente sincronizador/AT-SPI/impressora real,
assinaturas/segurança, mídias/3D, OCR/conversões e demais operações por família.
Nuvem direta e seus dois planos S12 mantidos adiados; pastas locais autorizadas
preservadas. IA/generativos e UPDF excluídos; sem mudança de escopo/pesos.

Indicadores preservados:45,13% checklist/39done/19abertos, paridade0/25 e
porcentagem global de reconstrução null. Fonte403/403 e pacote400/400 continuam
evidências anteriores, não execução desta rodada. Nenhum novo percentual foi
inferido. Guias de retomada e pendências apontam para o plano executável.

Conferência executada: os 19 critérios/25 famílias/50 planos foram mapeados sem
omissões/duplicações; dependências sem ciclos, referências presentes, dois casos
cloud adiados e critérios/pesos preservados. Verificador estrutural passou:
44 módulos/58 interfaces/25 famílias/19 critérios abertos. Relatório publicável em
testes/resultados/plano-continuidade-2026-10-18.json; relatórios locais e helpers
em analysis-local/continuation-plan-* e build/finalize/verify_continuation_plan.py.
Publicação progressiva autorizada: commit/push e conferência de remoto por
verify_git_sync.py com recibo externo. Não declarar sincronização por commit local.
Próximo passo: executar P01 em lote de reconciliação, depois operar os recursos
sem VM; P02 só quando houver resposta e controles offline novos, respeitando a
regra de parar/salvar/avisar. Nenhuma estimativa de prazo foi inventada.

## 2026/10/18 às 22:23 (America/Sao_Paulo, UTC-03:00) — P01 executada; P02/P03 interrompidas na entrada

Pedido: fazer P01–P03. P01 produziu inventário provisório111 recortes em25
famílias: 71 com código delimitado, 37 pendentes/caracterização,3cloud adiados.
49símbolos próprios localizados com linhas/hash;60métodos relacionados conferidos
na evidência403/403 do CI39172130287.106arquivos app atuais iguais ao manifesto.
Sem nova execução da suíte do app, novo original, REA ou build; contagens não
medem porcentagem global ou operações integralmente aceitas.

Matriz25linhas e especificação reconciliadas; valores anteriores preservados em
testes/resultados/p01-2026-10-18/reconciliation.json. Nove famílias agora registram
observação original parcial com evidências; D11/D15 não voltam como não observados.
Autor corrigido somente na fonte, pacote 0.1.13 preservado; 12métricas iguais/cinco
inconclusivas. Validador antes exigia runtime_observedfalse em todas as famílias;
agora aceita somente recorte com referências/escopo e rejeita paridade/aceitação
integral inventadas. Criado checker operacional; contratos humanos regenerados.
Todos50planos S12not_run,23subconjuntos/2propostas,19critérios/pesos45,13%,paridade 0/25
e porcentagem globalnull preservados. P01done é pacote provisório, não etapa7done.

P02: leitura hostVBoxrunning/cableoff e CUA/sky, sem entradas. Relógio21:49:22
igual antes/depois de dez segundos externos explícitos. Duas capturas VBox iguais,
hashba27a793...3761fc e intervalo externo maior que10s. Usuário avisado; nenhuma
entrada, manutenção de rede, deploy, nova tarefa, original, pause/resume/reboot.
P02blocked_vm_not_responsive; P03not_started_blocked_by_P02. Relógio avançou em
algum momento desde21:24:14, mas falhou agora; sem causa raiz atribuída. Não afirmar
novo inventário de processos/isolamento completo: não houve coletor novo.

Publicáveis: docs/INVENTARIO-OPERACOES.md, docs/EXECUCAO-P01-P03-2026-10-18.md,
progresso/inventario-operacoes-v1.json, execucao-plano.json e resultados/p01-2026-10-18/.
Privados: analysis-local/vm-20261018-2207/, p01_rows.py, execute_p01.py, p01_controls.py,
finish_p01_p03.py e excertos próprios p01-source-excerpts.txt. Validadores e controles
negativos conferidos:12 controles passaram, inventário111/25, contratos25/50 e nove
famílias com recortes observados; arquitetura44/58 e19 critérios abertos. Revisão
final/hashes em review.json. Guias/estados atualizados sem sobrescrever relatórios históricos.

Base Git0d0de4cc315f01b4e84087ea1ecd177f2fb5dc9a local/remoto confirmada. Fechar com
commit/push autorizado e recibo externo confirmando remoto. Próximo passo: após
resposta do guest, completar P02 com hash novo/RunId novo, perfil limitado,
contenção/offline e pf/col/end; só então P03. Não superar parada automaticamente.
Sem VM, outros pacotes próprios requerem continuidade de escopo pelo usuário.

## 2026/10/18 às 23:39 (America/Sao_Paulo, UTC-03:00) — retomada bloqueada no relógio23:36:09

Pedido retome: base local/remota `2ecf079f5af2d8adaef5834065b8f763a8657d69` e árvore limpa conferidas.
CUA/sky somente leitura encontrou a janela atual, área de trabalho e relógio
23:36:09. Reobservação após10 segundos externos explícitos manteve o horário.
Capturas VBox independentes em 2026-10-18T23:37:41.720309-03:00 e 2026-10-18T23:38:05.422463-03:00, intervalo
23.702s, bytes iguais/SHA256 `646a2cc853cacce3c8430342492c1fc1dc327a8839e0b33109751838321ad96b`.
Host running/cableoff; clipboard, drag-and-drop e VRDE desativados. Não foi
revalidado inventário de processos ou contenção completa; não afirmar Foxit
ausente só porque nenhuma janela estava visível. Causa raiz null; não inferir
parada contínua desde21:49:22, defeito Foxit ou tokens.

Regra do usuário aplicada: nenhuma entrada no guest ou ação de efeito
desconhecido; sem deploy/tarefa/rede/original/pause/reboot. Testes interrompidos e
usuário avisado. P02 permanece blocked_vm_not_responsive, P03 não iniciada;
P01 catálogo provisório111/25 preservado. App/pacote0.1.13 intactos; nenhuma suíte
app, REA, nova observação funcional do original ou build. Critérios/pesos,
45,13% do checklist, paridade0/25 e porcentagem globalnull preservados.

Privados: analysis-local/vm-resume-20261018-2336/ e este helper de checkpoint.
Publicáveis: docs/VM-RETOMADA-2026-10-18-2336.md e testes/resultados/vm-retomada-2026-10-18-2336.json; estado/plano/RETOMADA atualizados. Validação
restrita a JSON/referências, hashes/capturas e preservação dos critérios/fonte;
nenhum teste do app necessário para este checkpoint documental. Finalizar com
commit/push progressivo autorizado e recibo externo de sincronização; não
declarar publicação sem confirmação. Próximo passo: VM responder; depois
controle visual, ausência do original, coletor corrigido limitado/RunId novo,
pf/col/end e contenção offline. Somente então P03. Sem reinício automático.

## 2026/10/18 às 23:56 (America/Sao_Paulo, UTC-03:00) — P02 integrada e validada offline

Retome: base local/remota `876f00dd99373b23a685983b957d31d443f83c87` limpa confirmada. A VM voltou a atualizar:
relógio23:49:30→23:50:14, espera externa10s, capturas distintas; último23:54:56.
Notepad abriu, Task Manager Details respondeu e não mostrou Foxit na faixa
alfabética. Manutenção breve já autorizada confirmou zero processos e instalou
script próprio `b20ad4dca54ff33e7524df9d08702190539e0172ce3174dfe30b9118a277cac1` em tarefa2355 Interactive/Limited;
cabo desligado em finally antes dos testes. Sem proteções alteradas, reboot/pause.
Startup ready, pf/col/end completed recuperados completos e examinados. Sessão1
não elevada, dez Inputs iguais, identidade, RX e contenção host/guest passaram.
Notepad com marcador e menu Editar observado, sem editar. Coleta sem Foxit;
parada normal end confirmada. Primeiro read pf ainda não pronto; aguardado e
recuperado sem repetir comando. Não iniciar original com observador encerrado.

P02 completed_validated_offline, P03 ready_pending_fresh_preflight. Nenhum teste
Foxit, nova paridade ou suíte app/Flatpak nesta rodada; app preservado. Critérios,
pesos,45,13% checklist,0/25 eglobalnull intactos. Fonte403 e pacote400 históricos.
Ferramentas: Computer Use @oai/sky, VBoxManage7.2.20, SSHmanutenção e scripts
próprios. Evidências privadas analysis-local/vm-20261018-2355/ e vm-resume-20261018-2350/;
publicáveis docs/P02-COLETOR-VALIDADO-2026-10-18.md e testes/resultados/p02-2026-10-18-2355.json. Retomada/plano/pendências atualizados.
Validar JSON/recibos/hashes/referências e preservação dos critérios, publicar
marco autorizado e confirmar remoto com recibo externo. Próximo: RunId novo,
preflight/controle visual offline, depois destinos D07/D10, D12,D18 e UI.
Regra de parar/avisar se relógio ou resposta falhar permanece; causas anterioresnull.

## 2026/10/19 às 00:36 (America/Sao_Paulo, UTC-03:00) — P03 busca, destinos e saídas virtuais

Base publicada5e81af8 P02 preservada; RunId2359/tarefa limitada nova, preflight/Notepad/identidade/offline antes do original. Uma execução Foxit; recibos startup ready e pf/launch/col/c2/post/end completed completos. D07 distingue seleção no resultado de ativação nativa1→2; D10 seis hits mistos, texto2→1 e seleção da nota. D12 corpus250 terminou250 resultados antes de Stop ativo; nenhum cancelamento inferido. UI05 no par planejado/No; UI02 Print desabilitado sem PDF. N-up2 páginas e livreto4 páginas realmente gerados por Microsoft Print to PDF, recuperados após fechar original, hashes conferidos, pypdf e seis páginas Poppler70dpi examinadas. Margem5.08mm difere dos4mm C18; safety/gutter sem mapeamento. Comparações12 iguais/cinco inconclusivas preservadas, nenhuma métrica importada.

Foxit fechou normalmente; Task Manager e consulta posterior confirmaram ausência; splwow64 também ausente nessa consulta. Causa antiga continua aberta. Dez Inputs iguais/RXnegado no postflight; cabooff. Coletor end completo e tarefaReady/result0. Sete recibos2359 arquivados antes de liberar75 propriedades somente de resultado; nenhum arquivo original removido. Arquivamento1940 foi recusado antes de exclusão por propriedade ausente. Duas manutenções breves P03 com original ausente e cabooff em finally; nenhuma alteração de proteção, reboot/pause/forcekill. Último relógio00:30:58 avançando; desempenho/causa de paradas anteriores não inferidos.

Ferramentas: Computer Use @oai/sky/teclado nativo VBox, VBoxManage7.2.20, scripts próprios/SSH, pypdf/Poppler. Privados: analysis-local/vm-20261018-2359/ e helpers ignorados. Publicáveis: docs/P03-BUSCA-IMPRESSAO-2026-10-19.md e testes/resultados/p03-2026-10-19-2359.json. Catálogo revisão2/111 recortes, contratos/matriz e execução/RETOMADA atualizados só com observação parcial. Fonte/app/Flatpak0.1.13 intactos;403/400 históricos, sem suíte app nova; checklist45,13%,39 done/19 abertos, paridade0/25/globalnull preservados;50 S12 not_run e escopo sem IA/nuvem direta adiada. Validar JSON/referências, hashes/recebimentos, preservação de critérios e validadores de inventário/especificação. Publicação do marco pendente de commit/push e verificação remota nesta nota; confirmar por recibo externo sem autorreferência.

Próximo: novo RunId/observador e preflight offline; preparar variante D12 mais lenta com limite/hash fora dos dez Inputs, observar atividade antes de Stop/troca/fechar; resolver parâmetros D18 antes de comparar; completar destinos/ordenação/UI e causa D20. Não enviar comandos a2020/2355/2359 encerrados. Se relógio/resposta parar, observar após10s externos, salvar e avisar, sem reinício automático. Não fechar P03/famílias por este lote.

## 2026/10/19 às 01:08 (America/Sao_Paulo, UTC-03:00) — P03: trabalho ativo e nova parada da VM

Pedido terminarP03; base61b5a17 limpa. Gate inicial avançou00:44:48→00:45:59. Corpus sintético5000/60linhas,2.859.494bytes/hashce3fde0e23fb8c6622d434e939a03fa9a50c208cb272b5b0483fc9501339edf3, separado dos dez Inputs, reproduzido byte a byte pelo novo scripts/prepare_search_cancel_variant.py. Transporte stdin aguardou EOF: cliente próprio interrompido/cabooff, consulta confirmou arquivo ausente. SFTP8s falhou na negociação; SFTP45s passou/hash/read-only, nova tarefa0048Limited, ausência Foxit antes das manutenções, cabooff antes de original. Dependência Paramiko somente analysis-local/python-ssh. Sessão1 não elevada, startup/pf/run completos, Inputs/RX/identidade/offline verificados antes; controleNotepad/menuEdit observado. FoxitPID464 abriu12.pdf5000páginas. Busca alvo/fraseexata/fontes3/flagsfalse: Stop e progresso296/5000 às01:02:15. Entrada Stop enviada uma vez; último1001/5000 e1005ocorrências às01:02:45. Resultado/recepção da entrada desconhecidos.

Relógio01:02:45 sem avanço; capturas idênticas após44.191s externos com espera explícita10s, também iguais à captura anterior ao envio de Stop. Não atribuir causa ao Stop/Foxit/tokens. Pela regra do usuário: testes/entradas suspensos e usuário avisado; nenhuma rede/reboot/pause/kill/preflight/stop após a constatação. Hostrunning/cabooff; estado final do original/coletor0048 desconhecido, sem end. Não tentar manutenção até VM responder e original ausente. Integridade após parada não reconsultada; antes era igual.

P02concluída, P03partial_blocked_vm_clock; não declarar concluída por urgência. Preservados recortes anteriores, app/Flatpak0.1.13,403/400históricos,12métricas/cincoinconclusivas,45,13%checklist/39done/19abertos,0/25 eglobalnull,50S12not_run. Ferramentas ComputerUse/VBox/SSH/SFTP/pypdf; sem novaREA. Privados analysis-local/vm-20261019-0048/ e vm-gate-20261019-0045/. Publicáveis docs/P03-PARADA-2026-10-19-0105.md, testes/resultados/p03-2026-10-19-0048.json, gerador e trackers. Próximo: recuperar resposta; revisar Stop/coletor, depois D12 ativo/troca/fechar, D18parâmetros/mosaico e UI/Reader. Validar/preservar critérios e publicar checkpoint autorizado com confirmação remota externa; não declarar push antes do recibo.


## 2026/10/19 às 09:26 (America/Sao_Paulo, UTC-03:00) — P03 cancelamento/N-up/mosaico

Reinício offline explicitamente autorizado e desbloqueio manual; coletor0113 limitado/preflight/controle antes do Foxit. D12 Stop ativo232, troca conserva busca original, fechar aba encerra em1738; observações únicas, latência desconhecida. N-up4mm13.pdf2 páginas comparado com CI preservado; mosaico200%/5mm14.pdf48 páginas recuperado/renderizado. Pypdf/Poppler e controles do repositório, sem suíte/app/Flatpak novos.13 métricas iguais/quatro inconclusivas; famílias0/25 e critérios45.13% intactos. Foxit fechado, fila/processos zero, dez Inputs iguais, cabooff;0113 Ready/result0 sem end, não reutilizar. Relatóriodocs/P03-CANCELAMENTO-MOSAICO-2026-10-19.md; metadadostestes/resultados/p03-2026-10-19-0113/review.json; privadosanalysis-local/vm-20261019-0113 e vm-20261019-0912. Publicação em preparação; confirmar Git após commit/push por recibo externo, sem pressupor remoto. Próximo: observador novo e variantes UI/D07/D10/livreto e demais operações de P03.


## 2026/10/19 às 09:58 (America/Sao_Paulo, UTC-03:00) — P03 interface e encerramento solicitado

Base6aae418, lote0930Limited/offline: startup/pf/run completos, controle visual, dez Inputs iguais antes, RX/identidade/contenção conferidos. Uma aberturaPID2380, totalquatro P01–P03. UI03 Next1→2→3 e final8/8; UI04 min1/max6400 e controles mantêm extremos, FitPage47.15%1/8. Busca aberta mas entrada de texto não confirmada, nenhuma nova consulta submetida; UI06–10 continuam abertas. Sem app/pacote/REA/suíte novos. Coletor0113 parado teve quatro recibos arquivados/verificados antes de liberar44 slots de resultado; arquivos/propriedades de comando preservados.

Primeira suspeita de parada descartada; nova parada09:54:23 confirmada após35.598s externos/região do relógio igual. Usuário confirmou travamento e pediu salvar/encerrar. Entradas suspensas; sem rede/reboot/pause/kill/stop após constatação. Hostrunning/cabooff/USB0, janela Foxit visível; estado final de processos/coletor0930 e integridade pós-parada desconhecidos. Causa null. Ferramentas ComputerUse/@oai/sky, VBoxManage e scripts próprios; privadosanalysis-local/vm-20261019-0930. Publicáveis docs/P03-INTERFACE-E-PARADA-2026-10-19.md e testes/resultados/p03-2026-10-19-0930/review.json; RETOMADA/AGENTS/execução/inventário/contratos/matriz atualizados com observação parcial.

P03 parcial/bloqueada;13métricas/quatroinconclusivas,0/25,45.13%/39done/19abertos e50S12not_run preservados. Publicação em preparação, confirmar remoto por recibo externo após commit/push. Próximo, quando usuário retomar: conferir resposta/segundos, revisar original/coletor e integridade, novo preflight/controle se necessário; UI06–10/D07/D10/livreto e demais operações. Não superar parada automaticamente.


## 2026/10/19 às 10:53 (America/Sao_Paulo, UTC-03:00) — implementação leitura1–3, validação em andamento

Pedido refere-se aos itens1–3 da lista de funcionalidades, não aos pacotesP01–P03. Fonte0.1.14: candidato de abertura preserva documento anterior em falha/cancelamento; senha via stdin para worker e representação privada por sessão; recuperação consentida de estrutura legível pelo pypdf, original intacto. Render inicial conferido antes da troca; leases para trabalhos em curso. Domínio de página/zoom, entrada1–6400%, raster limitado/viewport virtual, geometria compartilhada; apresentação recebe rotação/sessão e possui escolha/remoção de monitor, foco/F6/Tab/Escape.

14 testes portáveis passaram no PythonWindows, sem skips; não provam GTK/Linux/Poppler. Evidênciaanalysis-local/document-session-tests/portable-01.json e cópia pública em testes/resultados/leitura-2026-10-19/portable-initial.json. Compilação sintática conferida; testesGTK preparados, execuçãoCI próxima. Sem ambiente Linux com dois monitores conforme resposta do usuário; validação física pendente. VM0930 não acionada, nenhuma nova observação Foxit;0/25 e critérios antigos preservados. Git/publicação e CI ainda em preparação neste checkpoint. Próximo: commit/push da fonte, executar CI Linux, corrigir falhas, gerar/auditar pacote e registrar limites restantes.


## 2026/10/19 às 11:07 (America/Sao_Paulo, UTC-03:00) — leitura1–3, diagnóstico Linux

Fonte candidata61553ae publicada; CI39264187175 excedeu600s na suíte, sem concluir testes, logo não aprovado. Artefato12193096818 baixado/hashff0bf14e3067bf7c5da235d1c8dbdfbf2485ab3e563157f4a29306e20b533b29 conferido; pré-requisitos Linux/GTK/Poppler passaram e corpus próprio17 passou, sem paridade nova. Logs de timeout antes do ajuste não preservavam stderr parcial; corrigido no coletor de testes. CI39265097656 em andamento parafa8e23e.

Revisão adicional: foco não é transferido às miniaturas ao navegar; alterações externas durante render/commit do candidato abortam a troca; intenção de nova abertura invalida diálogos de gravação antigos sem descartar a leitura anterior; coordenadas da lupa corrigidas no zoom virtual. Mais três testesGTK (total15 novos) e diagnóstico focado publicado antes da suíte para acesso independente aos logs. Ainda sem aprovação Linux/pacote; VM0930 intocada; critérios/paridade preservados. Próximo: examinar diagnósticos, corrigir falhas e repetir só validação necessária antes do pacote.


## 2026/10/19 às 11:14 (America/Sao_Paulo, UTC-03:00) — leitura, GTK focado aprovado e regressão localizada

CI39266242750/9ad1e1b:15/15GTK focados passaram,0falhas/erros/skips; artefato12193501834/hashceca6e4f24c0bc2ecebb62b2508262b2e0dc805f4cc217c0bda83ed1ed4e5f43 conferido. Captura de ajuste de página examinada; captura autenticada com apresentação sobreposta não adotada como prova visual e teste corrigido para capturar cada janela separadamente. RelatórioGTK preservado emtestes/resultados/leitura-2026-10-19/gtk-focused-9ad1e1b.json; aprovação apenas da fonte9ad1, não de alterações posteriores.

CI39265097656/fa8e23e excedeu600s; artefato12193128075/hash714a3cd1c7063f435cb242f4133c40f8d6ac3e5d44ac4a334eb73c6c047d711b conferido. stderr mostrou espera emOCRGTK.test_blank_page_has_explicit_no_text_notice: teste esperava desaparecimento imediato da imagem, mas abertura transacional conserva a anterior; chamava OCR cedo e abria erro modal por stamp antigo. Corrigida a espera pela conclusão da nova abertura/render, sem afrouxar a verificação de OCR. Teste de owner-copy passa a esperar o caminho realmente aberto. Falha de edição por intenção de reabertura já corrigida na geração9ad1. Cancelada somente a execuçãoCI39266242750 obsoleta, após preservar15GTK, não a VM.

Viewport evita reconfigurar ajustes idênticos; leitura recuperada fica identificada na aba/status; capturas autenticadas serão refeitas sem sobreposição. Fonte0.1.14 ainda candidata, sem novoFlatpak ou aprovação integral de famílias. Próximo: suíte completa Linux e geração/teste/auditoria do pacote. VM0930 continua suspensa e critérios antigos intactos.


## 2026/10/19 às 11:29 (America/Sao_Paulo, UTC-03:00) — regressão Linux e preparação de dois monitores virtuais

CI39267334037/156be32 executou432 testes:430 passaram,duas falhas,zero erros/skips; build/payload/sandbox não executados. Artefato12193383323/hashb29ea6e3c31284f76edd7c3b19fe7735f7ca04c2ba71d5d49bf889852346cfb4 preservado e examinado emanalysis-local/no-vm-release-artifact-12193383323. Falhas nos testes de anexos e reabertura de pasta sincronizada aceitavam a imagem/lista da sessão anterior, conservada pela abertura transacional. Esperas corrigidas para caminho confirmado e ausência de candidato pendente; verificações funcionais preservadas.

Novo scripts/check_presentation_monitors.py e workflow presentation-monitors.yml exigem dois monitores GDK reais sobre Xvfb/Xinerama e conferem fullscreen/tamanho em0→1→0. Ainda não executados neste checkpoint; não contam como teste físico. Fonte app permanece idêntica à156be32. Próximo: publicar mudanças, repetir suíte/pacote e executar controle virtual; VM0930 continua suspensa/intocada e critérios/paridade intactos.


## 2026/10/19 às 11:33 (America/Sao_Paulo, UTC-03:00) — ajuste do laboratório virtual de apresentação

CI39269569101 não aprovou monitores: Xvfb/Xinerama expôs somente um monitor GDK; nenhum teste de seleção foi executado. Artefato12195615434/hash8b272b7835dca0507d2295ea2b0db5335b0e72978877ebe3ce480668980fb995 conferido e preservado emanalysis-local/virtual-monitors-artifact-12195615434. Corrigido apenas laboratórioCI para Xephyr com duas cabeças em origens distintas, sobreXvfb; logs de servidor serão preservados. Não altera app nem aprova hardware físico. Build/suíte39269568732 continua na fonte9848f2b, app ainda idêntico. VM0930 intocada.


## 2026/10/19 às 11:36 (America/Sao_Paulo, UTC-03:00) — diagnóstico de enumeração GTK

CI39270001839 também não aprovou: Xephyr expôs duas cabeçasXinerama (1280x800@0,0 e1024x768@1280,0), masGTK viu só a área2304x800. Artefato12194752113/hashf7a5be9ffce4f40d935a044cdc9432982c3691cf775610efad62f4b56eedf66c conferido. Fonte oficialGTK3 gdkscreen-x11.c init_multihead usaRandR1.5/1.3 e fallback único, nãoXinerama. Laboratório passa aXorg dummy com duas saídasRandR; somente infraestruturaCI, app inalterado. Ainda não aprova monitores físicos. VM0930 suspensa.


## 2026/10/19 às 11:39 (America/Sao_Paulo, UTC-03:00) — dois monitores virtuais aprovados

CI39270599017/490a904 aprovou duas saídasGDK/RandR1280x800 e1024x768 comfullscreen/tamanho em0→1→0, app idêntico ao build9848f2b em andamento. Artefato12194817693 disponível para exame; não é hardware físico nemFoxit. Controle foi ampliado para conferir posição e remoção/restauração real da saída dummy ativa, sob flag exclusiva deCI; próximoCI não altera aplicativo nem a VM0930.


## 2026/10/19 às 11:41 (America/Sao_Paulo, UTC-03:00) — recorte de controles em1024 corrigido

Exame visual das capturas do artefato12194817693/hash17c0007b06edc7269d1d81233fc7c4204a9904698cb07c0619ed1f62c9652c6b mostrou conteúdo legível nas duas telas, mas linha única cortava seletor de monitor/Sair em1024x768. Mudado app/presentation.py para duas linhas centralizadas e controleCI exige seleção/ajuste/Sair completamente dentro da janela. Captura passa a esperar resize/render estabilizados. Aprovação anterior de tamanho/fullscreen não aprovava o layout; novo app exige nova suíte/pacote e testeRandR. Catálogo recebeu somente atualização de hashes, sem promover estados. VM0930 suspensa/intocada; próximoCI da fonte corrigida.


## 2026/10/19 às 11:45 (America/Sao_Paulo, UTC-03:00) — apresentação corrigida aprovada e espera de anexo ajustada

CI39271276972/1675c2c: duas telas nativasGDK/RandR, posições0,0/1280,0, fullscreen0→1→0 e remoção/restauração da saída ativa passaram. Artefato12194713477/hash862d3638ca5b4904cabc97d4acaa1bf149dbe330d4ce5994657fb67f5da6c36c conferido; capturas examinadas mostram todos os controles visíveis em1280x800 e1024x768. Evidência pública emtestes/resultados/leitura-2026-10-19/virtual-monitors/. Sem hardware físico/Foxit.

Build anterior39269568732/9848f2b:432/432 fonte e payload; sandbox431/432, uma falha no teste de anexo longo (botão desabilitado); entrega não aprovada. Artefato12195786612/hash3060c1b288215bacc109b99d5d31bd08d5b43f9ddcb3c9a9bb4cf8a654af9fe5 conferido. Teste podia aceitar metadados do documento anterior; agora exige caminho correto e um anexo carregado, mantendo asserção do nome/layout/botão. Auditoria independente terá mais3 testesGTK instalados deste recorte, no mesmo bundle sem rebuild. Build corrigido39271277016 continua; app não mudou após1675c2c. VM0930 intocada.


## 2026/10/19 às 11:52 (America/Sao_Paulo, UTC-03:00) — fonte/payload432 confirmados, sandbox em revalidação

CI39271277016/1675c2c:432/432 fonte e payload; sandbox431/432, mesma falha do teste antigo de espera de anexo longo. Artefato12195458890/hash5e22c7c2985c787dbc9ec6b1c895a93855601ab0ab9994dd20f0fc89198e0928 conferido. Relatórios próprios fonte/payload e resumo da falha emtestes/resultados/leitura-2026-10-19/. Nenhum candidato0.1.14 aprovado/publicado. Reexecução no commit a4e017a já solicitada, incluindo o teste corrigido; app idêntico à1675c2c que passou em duas telas virtuais/hotplug/layout. Próximo: exigir432/432 nos três ambientes, depois pacote/auditoria/download; VM0930 suspensa e métricas antigas intactas.


## 2026/10/19 às 12:02 (America/Sao_Paulo, UTC-03:00) — retomada do candidato sem reconstrução após falha de rede

CI39272792405/a4e017a passou432/432 fonte e payload, inclusive teste de anexo corrigido; falhou no remote-add doFlathub com erro7/Could not connect to server, antes do sandbox. Não é nova falha de teste ouFoxit. Artefato12195849163/hashZIPe765074e1265384f92b292783e521a4fb12e93c4ef7035f5176d3b5e23f4afff conferido; bundle44665656bytes/SHA795b09569ab825f2131a6ca22a919a9bebf6146a718f53288f085dba89b11e1f preservado.

Workflow linux-flatpak-resume.yml restaura fonte exata/artefato e exige mesmo hash, fonte/payload completos sem skips e integridade app; executará somente controles restantes/suíte sandbox/smoke/launcher, com retry limitado da rede. Finalização reaproveita payload instalado com hashes conferidos e não recompila. Ainda não executado/aprovado neste checkpoint. Ação oficialdownload-artifactv8.0.2 fixada noSHA9000827ccba6bdab643e8b6fd33ac0654aef8333, consultada viaAPI oficial. VM0930 suspensa/intocada; próximo: concluir sandbox e auditar pacote se aprovado.


## 2026/10/19 às 12:12 (America/Sao_Paulo, UTC-03:00) — entrega própria0.1.14 preparada

CI39272792405 fonte/payload + retomada39274463095 sandbox, mesma fontea4e017ae65784256583292ddbe502e182bb25a66:432/432 por ambiente fonte/payload/sandbox,0falhas/erros/skips;403 IDs anteriores preservados e29 novos. 109 arquivos app iguais; smoke5/5, launcher3/3 e pastas foraHOME negada/concedida passaram. Bundle conferido SHA256 795b09569ab825f2131a6ca22a919a9bebf6146a718f53288f085dba89b11e1f (44665656 bytes), manifesto e relatórios emreleases/ etestes/resultados/0.1.14/. Capturas serão conferidas e o exame visual registrado no review da entrega antes do push. Inventário revisão6:74 com código delimitado,34 pendentes,3 adiados, sem equivalência integral; contratos/matriz/retomada reconciliados. VM0930 intocada; critérios antigos,0/25 e50S12not_run preservados. Próximo: publicar, conferir download público e auditoria independente sem rebuild; validação física/original continua pendente.


## 2026/10/19 às 12:13 (America/Sao_Paulo, UTC-03:00) — candidato aprovado, capturas e integridade examinadas

Retomada39274463095 aprovada sem rebuild; fonte/payload432/432 doCI39272792405 e sandbox432/432,0falhas/erros/skips. Artefato12196314022/hashZIP2d3a4203706bddbc8246de6cdd41d685e60221818dbf8966fa05a364342231f9 conferido. Importador conferiu todos403 IDs anteriores,29novos,109 arquivos e relatórios selados, proveniência/licenças e bundle idênticoSHA795b09569ab825f2131a6ca22a919a9bebf6146a718f53288f085dba89b11e1f. Três novas capturas de leitura autenticada/apresentação/ajuste examinadas e legíveis; arquivo/página/busca corretos. Review público emtestes/resultados/0.1.14/review.json. Metadados/contratos/matriz/plano/retomada reconciliados; pesos/estágios preservados. Próximo: checks estruturais, push do pacote, download público e auditoria do mesmo bundle. VM0930 permanece suspensa, sem comandos.


## 2026/10/19 às 12:20 (America/Sao_Paulo, UTC-03:00) — publicação, download público e auditoria0.1.14 confirmados

Entrega38cb933 confirmada emorigin/main. Download público sem login HTTP200/44665656bytes/hash795b09569ab825f2131a6ca22a919a9bebf6146a718f53288f085dba89b11e1f conferidos; relatório emtestes/resultados/0.1.14/download-integrity-2026-10-19.json. Auditoria39276321508 passou sem rebuild:7controles/5smoke/3GTK adicionais,109arquivos app e2849dependências/224ELF/162avisos, identidade OSTree/runtime iguais. Artefato12197966982/hashZIP00e4f1496ad7c9a9ae05815b0b0f24d4c9f575c85476331e5585c3d9f02d377e conferido; cinco relatórios e review emtestes/resultados/0.1.14/audit/.432/432 próprios por ambiente preservados, sem repetir suíte inteira na auditoria.

VM0930 não acionada; família integral0/25,39done/19abertos/45.13% histórico e50S12not_run intactos. Inventário provisório74 com código/34pendentes/3adiados, não percentual global. Dois monitoresGDK/RandR/layout/hotplug aprovados na fonte; testes físicos/Wayland/original continuam pendentes. Próximo semVM: P06/B01, comboAcroForm editável; respeitar contratos/escopo semIA e nuvem direta adiada. Metadados desta conclusão serão publicados agora e sincronização final conferida com recibo fora da árvore.


## 2026/10/19 às 12:39 (America/Sao_Paulo, UTC-03:00) — lote4–6, fonte preparada

Pedido: executar os25 itens de3em3; usuário confirmou adiamento da nuvem direta23. Inspeção própria de respostas /IRT/RT, aliases/ciclos/cross-page e rich text, busca por campos, destino por ID e botão Parar com retenção dos resultados entregues. Python local:7 testes passaram e2 GTK não executados por falta de tela; relatório bruto em analysis-local/batches-20261019/comments-portable-02.json. A primeira tentativa falhou no import Cairo do helper antigo; fixture portada para pypdf sem GTK. Arquitetura/contratos/catálogo atualizados, evidência0.1.14 selada conservada como histórica. Fonte0.1.15 ainda sem aprovação Linux ou pacote. VM não acessada. Git ainda a publicar; próximo passo: validar lote4–6 no Linux e iniciar7–9. Nenhuma família ou critério amplo encerrado.


## 2026/10/19 às 12:46 (America/Sao_Paulo, UTC-03:00) — lote07-09

Formatos HTML/corpo DOCX/ODT, revisão/exclusão/refresh de índice com hash esperado, trava e publicação atômica; radicais Snowball3.1.1 PT/EN em leitor, anexos e índice. PyPI oficial/hash7e207fa.../COPYING e40 arquivos intactos em app/vendor/snowballstemmer; docs/proveniencia-snowball.json e aviso no build.8 novos testes portáveis passaram/1 GTK pendente,12 regressões índice e12 de anexos passaram; relatórios analysis-local/batches-20261019. Primeira rodada encontrou ordem de árvore de nomes e equivalência de radical documentar legítimas, expectativas corrigidas; hardlink negado no Windows restrito resolvido com rename exclusivo atômico nativo (Linux mantém hardlink). Falhas preservadas, sem skips aceitos como prova Linux. CI anterior39279784605 ainda em fila, fonte atual não validada no Linux, pacote0.1.14 preservado. Sem acesso à VM; nuvem direta23 adiada; nenhuma família ampla encerrada. Próximo lote10–12, publicação deste marco a confirmar.


## 2026/10/19 às 12:51 (America/Sao_Paulo, UTC-03:00) — lote10-12

Seleção separa blocos/colunas, mantém strings Unicode do Poppler e evita vizinho apenas tangente. Preparação JSON cancelável termina worker/grupo Linux e só entrega para submissão após sucesso; salvar cópia usa staging/replace, recusa original/symlink. Parâmetros não finitos, modo desconhecido e CropBox inválido são recusados.6 testes portáveis novos passaram/1 GTK pendente e9 regressões CropBox passaram; evidências analysis-local/batches-20261019/selection-print-portable.json e cropbox-regression.json. Bidi/caret completo, impressão física, estado real da fila e explicação splwow64 do original seguem pendentes. Sem Foxit/VM ou novo Flatpak. Critérios/pesos/paridade preservados. Git/publicação deste marco a confirmar; próximo13–15.


## 2026/10/19 às 12:58 (America/Sao_Paulo, UTC-03:00) — lote13-15

Marcadores/hierarquia e controles avançados revalidados21/21 no host. Novos: combo editável (texto livre, export/display, remoção deI obsoleto e AP), Ink vetorial e folha de desenho GTK em escala antes da rotação sem fundo PDF; respostas /IRT/RT da mesma página com ciclo/profundidade/locks recusados e rascunho real desfazer/refazer.7 testes novos portáveis passaram/1 GTK pendente; primeira tentativa de cadeia apontava para Widget em vez do índice real da nova resposta, fixture corrigida sem afrouxar recusa do backend. Relatórios analysis-local/batches-20261019/forms-ink-replies-02.json e advanced-edits-regression.json. JavaScript/XFA continuam não implementados; tipos/restantes do original sem caracterização. Sem VM/novo pacote, nuvem23 adiada. CI anterior ainda em fila. Git/publicação do marco a confirmar; próximo16–18.


## 2026/10/19 às 13:08 (America/Sao_Paulo, UTC-03:00) — lote16-18

Portfólios: árvore/arquivos incorporados listados e extraídos sem executar layout/ações. Painel usa lease da sessão autenticada e bloqueia extração secopy negado; busca em anexos/imposição direta também conferem permissões em PDFs cifrados com senha vazia. Assinatura local própria: PEM cert/chave escolhidos, senha stdin JSON, RSA>=2048/EC>=256, CMS SHA256 detached, ByteRange reservado/checado, campo invisível novo e publicação sem sobrescrita após validação .NET/OpenSSL independente. Cifrado/assinatura existente/XFA/portfólio recusados pelo contrato de edição.7 novos testes passaram (incluindo CMS adulterado/segredo incorreto/original preservado),14 regressões anexos e14 coordenação passaram. Smoke manual inicial usou temp padrão não gravável; nenhum dado de chave exposto, testes reais usam temp explícito gravável e passaram. Relatórios analysis-local/batches-20261019/signing-attachments-permissions-02.json e regressões; apenas chaves sintéticas próprias usadas. UI/Linux ainda pendentes; confiança/revogação/TSA/LTV/tokens/RMS não implementados. Tentativas de cancelar3 CI antigos ainda queued retornaram409, não os declarar cancelados. Sem VM/novo Flatpak, nuvem23 adiada. Git/publicação deste marco a confirmar; próximo19–21.


## 2026/10/19 às 13:22 (America/Sao_Paulo, UTC-03:00) — lote19-21

Medidas: pontos sobre snapshot atual, calibração e unidades mm/cm/m/in/ft, perímetro fechado e área de polígono simples com rejeição de interseção/degeneração/limites. Camadas: OC default ON/OFF em cópia privada, locks/RBGroups, remoção deAS para override explícito e lease por caminho para aposentar arquivos sem apagar original/arquivo ativo. Leitor principal renova caches; impressão de override temporário explicitamente bloqueada; apresentação já aberta não é revalidada. Acessibilidade usa sessão autenticada e exporta voz WAV PT/EN sem IA/rede; eSpeak/data/dependências/atribuição adicionados à receita, ainda sem build. Probe AT-SPI entre processos preparado em scripts/check_atspi_text.py e workflow, não executado no Windows.6 novos portáveis passaram/3 Linux pendentes;14 regressões DocumentSession passaram. Pixelrender/camada GTK e áudio real aguardam runner, sem alegar aprovação. Mídia/3D/leitor de tela físico continuam pendentes. Relatórios analysis-local/batches-20261019/measurement-layers-speech.json e document-session-regression.json. Sem VM/novo Flatpak/alteração de pesos; Git/publicação a confirmar. Próximo22–24 (23 nuvem direta adiada) e25.


## 2026/10/19 às 14:16 (America/Sao_Paulo, UTC-03:00) — lote22-24

Preferências próprias para próximo documento: zoommodo/percentual1–6400, painel e destaque; arquivo separado sem históricos/segredos, validação estrita e staging/replace. Conversão opt-in de todos quadros GIF/APNG/WebP para páginas estáticas com mesmos limites100páginas/150MP; default anterior preserva recusa de animações, TIFF mantém todas páginas. PPM/PGM/PBM e ICO estático acrescentados; APNG default-image separada recusado.5 testes novos portáveis passaram/1 GTK pendente e22 regressões criação passaram. Fontes/cores/frames reais conferidos no PDF, tempos/áudio descartados explicitamente. Nuvem direta23 continua adiada conforme resposta humana; nenhuma API/credencial de nuvem acrescentada. Marco Linux anterior825f1e4 confirmado465/465 sem falha/erro/skip no run39282125477; artefato12201581438 baixado/hash GitHub conferido. Não aplicar essa prova à fonte posterior. CI19–21 run39292345681 em execução. Sem VM/novo Flatpak ou critérios/pesos alterados. Git/publicação a confirmar; próximo25 e consolidação/testes.


## 2026/10/19 às 14:19 (America/Sao_Paulo, UTC-03:00) — lote25-25

Item25: abrir PDF pelo FileChooserNative do sistema com filtro/local-only, cancelamento conserva documento; janela de instalação usa identidade Flatpak fixa e orienta atualização no gerenciador do sistema, sem atualizar automaticamente. Scriptcheck_native_portal.py testa desktop efêmero X11: observa chamada/resposta real no log D-Bus do cliente nativo e seleção de fixture própria viaxdotool, ainda não executado.2 testes portáveis passaram/1 GTK preparado; docs/source markers ainda sem nova validação. Associação launcher já possuía checks históricos; permissões persistentes Flatpak/associação/update real/Windows nativo permanecem pendentes, nenhum deles marcado implementado por mera instrução. Passagem de implementação pelos25 itens concluída como recortes, não famílias completas;23 adiado,15 operações conhecidas ainda pendentes/3deferred no inventário. Lote19–21 Linux run39292345681 já sucesso; artefato a baixar/examinar. Sem VM ou pacote novo. Próximo: validar fonte consolidada, examinar screenshots/probes, corrigir falhas e publicar evidências.


## 2026/10/19 às 14:32 (America/Sao_Paulo, UTC-03:00) — lotes4–25, fonte Linux consolidada

CI39293331527, fonte2c218bb:490/490 próprios Linux, zero falhas/erros/skips;432 IDs anteriores preservados e58 novos. AT-SPI entre processos e seletor portal real X11 passaram nos recortes sintéticos. Nove capturas de interface examinadas, com limites de cada evidência registrados emtestes/resultados/lotes-2026-10-19/review.json; a primeira não exibe o painel de comentário e não serve como prova visual de destino. Arquivos brutos/digests conferidos emanalysis-local/no-vm-artifact-12206033343 e batch-ui-artifact-12207306118. Catálogo ligado à nova evidência própria sem encerrar operações/famílias. Item23 permanece adiado; VM suspensa e intocada. Pacote0.1.15 noCI39293507397 ainda em validação;0.1.14 é o último publicado. Próximo: examinar candidato, publicar e auditar o mesmo bundle.


## 2026/10/19 às 14:36 (America/Sao_Paulo, UTC-03:00) — entrega própria0.1.15 preparada

CI39293507397/fonte257425a:490/490 próprios por ambiente fonte,payload,sandbox,0falhas/erros/skips;432 IDs preservados e58 novos, com mudanças de asserções antigas explicitadas nos lotes.160 arquivos app iguais,11 relatórios selados; smoke5/5 e launcher3/3. Runtime3414arquivos/242ELF/181pacotes atribuídos, versões fonte e SnowballBSD preservados. Bundle58072096bytes/SHA256f511671c2b7a3f1e6c24a19951d586390c8a196f022f640c167b270e4ab5a2b9, artefato12208010392/ZIPcc8220f4f8a905e39d8a06a910344923e6ae9b8c1509879d4a5c262e26c3e4dc conferidos. Publicáveis emreleases/ etestes/resultados/0.1.15; rawanalysis-local/no-vm-release-artifact-12208010392. Fonte local version.py normalizada para os bytesLF exatos doGit/CI; nenhuma alteração funcional adicional. Docs/contratos/matriz/estado dos25 reconciliados,93recortes com código/15pendentes/3adiados no inventário provisório111, sem paridade integral. VM intocada, nuvem direta23 adiada e critérios/pesos intactos. Próximo: publicar, conferir download público e auditar instalação do mesmo bundle sem rebuild.


## 2026/10/19 às 14:43 (America/Sao_Paulo, UTC-03:00) —0.1.15 publicada e auditada

Publicação técnica d0d9bec confirmada; download público sem loginHTTP200/58072096bytes/SHA256f511671c2b7a3f1e6c24a19951d586390c8a196f022f640c167b270e4ab5a2b9 confere. AuditoriaCI39295926737, artefato12206104594/ZIP3a68d913121c16be673c2191b2a4cdb4e1f61c0961dde6dd9bade321dfa6c99f examinado:7controles/5smoke/3GTK passaram no mesmo bundle, sem rebuild; app160arquivos e runtime3414/242ELF/181avisos/versões fonte conferidos. Três capturas adicionais da entrega examinadas; nove novas interfaces no review por lote. Evidências publicáveis emtestes/resultados/0.1.15/audit/, download-integrity e delivery-visual-review; brutos ignorados emanalysis-local/no-vm-audit-artifact-12206104594. Ferramentas: Python/GTK3/Poppler/Flatpak, Debian13/X11 efêmero, próprio código; nenhum Foxit/REA/Ghidra executado nesta consolidação. A suíte integral490/490 por ambiente é a execução anteriorCI39293507397, não repetida na auditoria. Inventário Markdown antigo foi reconciliado comJSON atual por scripts/render_operation_catalog.py; pendências/retomada e sincronização registram o marco confirmado, sem autorreferência ao commit final. Nuvem direta23 adiada;0/25 famílias completas,50S12 e19 critérios amplos permanecem abertos, percentual global indeterminado. VM suspensa/intocada. Próximo sem VM: caret/bidi, eventos de formulário delimitados, tipos restantes de anotações e planosS12; desktop físico/portais persistentes/impressora/leitor/telas e comparação original dependem dos respectivos ambientes. Registrar commit das notas e verificar HEAD remoto/árvore limpa com comprovante fora da árvore.


## 2026/10/19 às 14:50 (America/Sao_Paulo, UTC-03:00) — execução abrangente sem VM iniciada

Pedido explícito de completar todo trabalho independente de VM. Plano e dependências emprogresso/execucao-sem-vm.json; baseline0.1.15/d0a6213/490 testes preservado. Fonte0.1.16 em desenvolvimento; evidência atual antiga movida a histórica antes de alterar código. VM suspensa e nuvem direta23 adiada permanecem intactas. Próximo: seleção por caractere/cursor e textos bidirecionais, depois eventos de formulário/anotações e demais pacotes. Nenhuma conclusão nova nesta preparação.


## 2026/10/19 às 15:08 (America/Sao_Paulo, UTC-03:00) — S01 Linux e S02/S03 preparados

S01 inicialf3212ef/CI39298287332:498/498 Linux sem falhas/erros/skips, oito novos/490 preservados; raw e ZIP12208122994 examinados/hash conferido após timeout de rede e retry streaming. Evidência pública emtestes/resultados/sem-vm-2026-10-19/s01; não aprova a extensãoPango posterior. S02 cálculos/intervalos e S03 anotações/conversas implementados;7+7 portáveis e16+21 regressões passaram;3 novosGTK e extensão nativa aguardamCI. Falhas iniciais de FloatObject/BooleanObject corrigidas e registradas. Catálogo provisório111 agora95 com código/13pendentes/3adiados, não operações completas aprovadas. Fonte0.1.16 em desenvolvimento, último pacote0.1.15 preservado; pesos/critérios/paridade/VM/nuvem intactos. Próximo: CI consolidadoS01–S03 e S04 autenticação/edição/impressão.


## 2026/10/19 às 15:26 (America/Sao_Paulo, UTC-03:00) — S01–S03 validados e S04 preparado

CI39300179043/5a4729e:516/516 Linux sem falhas/erros/skips; fonte, Pango/GTK/Poppler, aparências Unicode/fontes/pixels e eventos/conversas examinados. Artefato12211916533/ZIP08117925d8e00647fac2c72ac06ebf00116e6a78b597071159f47f97c593f3db conferido e relatórios públicos emtestes/resultados/sem-vm-2026-10-19/s01-s03/. S04 edição mantém criptografia/credenciais/permissões, transporte stdin; impressão de sessão/camadas com leases,150DPI conforme permissão e cancelamentoCUPS por recibo implementados.10 novos portáveis passaram; regressãoDocumentSession14 passou, histórico em verificação;2GTK e fila virtual própria aguardamCI. Receitas incluem cancel doCUPS e novo jobloopback; nenhum comando à VM/hostprinting. Fonte0.1.16, último pacote0.1.15 preservado, nuvem23 adiada, critérios/paridade intactos. Próximo: validar S04 e ampliar anexos/índice/idiomas S05.


## 2026/10/19 às 15:28 (America/Sao_Paulo, UTC-03:00) — checkpoint S04 antes do CI

Regressões próprias de sessão14/14 e histórico8/8 passaram;10/10 portáveis novos passaram,2GTK pendentes. ParserAST, catálogo95/13/3 e arquitetura65módulos/60interfaces conferidos. Separado jobCUPS virtual do jobGUI para preservar diagnósticos independentes; ambos exigem sucesso. Documentos de retomada apontam a fonte0.1.16 em desenvolvimento e Flatpak0.1.15 anterior, sem promover516/516 da revisãoS01–S03 à fonteS04. Próximo comando: publicar este checkpoint e executar no-vm-validation.yml; seguir S05. VM não acessada.

### 2026/10/19 às 15:43 (America/Sao_Paulo, UTC-03:00) — S05 sem VM

S04 Linux528/528 examinados (commitcc72da5); falha do primeiro CUPS preservada e
correção de URI pendente de reexecução. S05 ampliou formatos, OCR opt-in,36idiomas,
backup/recuperação/travas.11portáveis aprovados;1teste nativo não executável no host.
Fonte0.1.16 sem pacote novo,0.1.15 preservado. VM intocada; nuvem direta adiada,
paridade/critérios/pesos intactos. Próximo:S06 e CI Linux/CUPS deste checkpoint.
Publicação:commit/push e confirmação feitos em seguida; não inferir pelo texto.

### 2026/10/19 às 15:50 (America/Sao_Paulo, UTC-03:00) — S06/S07 preparados

S05 Linux540/540,portais/AT-SPI,CUPS4/4 examinados; artefatos conferidos pelo SHA.
S06 política local CA/CRL/RFC3161 e S07 voz/medidas implementados, aguardando CI.
Fonte0.1.16 sem novo pacote; VM intocada,paridade/pesos/critérios preservados.
Próximo:validar esse commit e continuar S08–S12. Commit/push serão confirmados depois.

### 2026/10/19 às 16:00 (America/Sao_Paulo, UTC-03:00) — S08/S09 e correção RFC3161

S06/S07CIaeafdea:548/549; única falha TSA, reproduções e CA/CRL passaram.
Correção ts preparada, aguardando nova integração. S08 mídia/camadas,S09 padrões
eOCR seletivo acrescentados;5+3portáveis aprovados,2integrações nativas pendentes.
Estática S11 iniciada:Ghidra-noanalysis,2sementes inéditas de transição reflow,
resultado ainda em importação,não contado. VM intocada; nuvem adiada;0.1.15mantido.
Próximo:CI corrigido,S10integrações,S11exame,S12Flatpak/auditoria.

### 2026/10/19 às 16:09 (America/Sao_Paulo, UTC-03:00) —558Linux e S10/S11

558/558 do586c7f8 examinados e SHA confirmado;TSA corrigido passou. Preparados
S10Windows nativo/desktop com portal persistente/associação/update/rollback.
Estática Ghidra2novas entradas,85instruções/268bytes conferidos comCapstone;325
entradas totais,sem código original incorporado. Primeiro checker falhou por
PYTHONPATH ausente;reexecutado comdeps locais preservadas e aprovado.
VM intocada,nuvem adiada,critérios/paridade intactos. Próximo:executar S10,
novos2GTK,S11aceitação eS12pacote/auditoria. Publicação será confirmada por Git.

### 2026/10/19 às 20:04 (America/Sao_Paulo, UTC-03:00) — Windows,alocações e candidato reprovado

WindowsCI5/5 e captura examinados;desktopupdate/rollback passaram,portal/associação
precisam repetir o probe corrigido. Flatpakprimeiro:f/p560/560,sandbox559/560;
falha de configTSA corrigida no código/fixture,novo build necessário. Candidato
reprovado preservado privadamente,0.1.15continua última entrega. Distribuição
nova viaReleaseasset>100MiB preparada com SHA/tamanho e11controles aprovados.
Estática4entradas novas total327,Capstone262instruções/793bytes. VM intocada,
critérios/paridade intactos. Próximo:publicar código/repetir build+desktop;
concluir auditoria/download e registrar limites restantes.

### 2026/10/19 às 20:10 (America/Sao_Paulo, UTC-03:00) — portal8/9 e contagens

Desktop a5ebda9:8/9 examinados,reinício preservou grant e revogação negou acesso;
primeira leitura sofreu corrida de troca do próprio portal. GuardasPID/FUSE
acrescentadas,teste ainda pendente. S11duas contagens novas conferidas,agora329
entradas e266instruções/803bytes novos no dia. Original nunca executado/VMintocada.
CI do novo pacote segueexecutando. Próximo:repetir somente desktop afetado e
consolidar/auditar candidato aprovado. Critérios/paridade/nuvem intactos.


## 2026/10/19 às 20:18 (America/Sao_Paulo, UTC-03:00) — aviso Actions corrigido e integração9/9

Usuário mostrou e-mail Run failed do workflow de desktop na revisãoa5ebda9. Era falha do teste, não do push. Corrigida em e61d174 a prontidão do portal: dono D-Bus precisa ser o PID próprio e exportação FUSE deve existir antes da leitura. CI39339986089 aprovou9/9 controles reais no Flatpak0.1.15: atualização/retorno, preferências, negar/conceder, persistência após reinício do próprio portal, revogar e associação/abertura. ZIP12228337593/f155522e25fd152b8badb25cfe5bc1cba18af7e254b39da13fa0130663e07e9f conferido; relatório emtestes/resultados/sem-vm-2026-10-19/s10-third/. As duas falhas anteriores preservadas, notificações da conta não alteradas. Documentação emdocs/CI-FALHAS-E-CORRECOES.md. Windows próprio5/5 já aprovado; seis novas entradas estáticas/266instruções803bytes catalogadas329=152REA+177diretas, sem original executado. Novo candidato0.1.16 CI39339330479 ainda em execução; último pacote publicado permanece0.1.15. VM intocada, nuvem direta adiada, pesos/paridade/critérios intactos. Próximo: examinar fonte/payload/sandbox, publicar somente se aprovado e auditar o mesmo arquivo.


## 2026/10/19 às 20:24 (America/Sao_Paulo, UTC-03:00) — candidato0.1.16 validado e asset publicado

CI39339330479/fontea5ebda9:564/564 próprios por ambiente fonte,payload,sandbox, zero falhas/erros/skips;490 IDs preservados e74 novos. 177 arquivos app e11 relatórios selados conferidos; smoke5/5 e launcher3/3. Runtime3684 arquivos/483 ELF/297 avisos e versões fonte atribuídos. Bundle118393760 bytes/SHA256ad02f4c5ebb3d3d740a1a5c56fa3f4a71b52e4ac2b94171973f92b7526190816. Asset publicado como prereleasev0.1.16-devel, sem nova compilação e sem colocar arquivo maior que100MiB no Git. Manifestos/checksums/evidências preservados no repositório; auditoria instalada e download público completo ainda pendentes. Ferramentas: Python/GTK/Pango/Poppler/Flatpak/OpenSSL/GStreamer em Debian13 efêmero, testes próprios; nenhuma execução Foxit ou entrada na VM. Windows próprio5/5 e desktop0.1.15 portal/associação/atualização9/9 aprovados separadamente. Catálogo estático329=152REA+177diretas, seis entradas novas examinadas/266instruções803bytes. Inventário provisório111:97 com recortes de código/11pendentes/3adiados; não é porcentagem da reconstrução. S11/famílias integrais/50S12/19 critérios amplos continuam abertos; nuvem direta adiada, IA excluída e pesos/paridade intactos. Próximo: push dos metadados, auditoria independente do mesmo bundle e probe desktop0.1.16; confirmar download público e HEAD remoto.


## 2026/10/19 às 20:31 (America/Sao_Paulo, UTC-03:00) — auditoria0.1.16 passou; nova corrida FUSE do probe

AuditoriaCI39341656820 aprovada, artefato12229142103/ZIP6dadd0fa61cd40b04642be4cffb8f07bcb16597a86bfddf699e271db4329a0f1 baixado. DesktopCI39341668923, artefato12228757508/ZIPc83a77f2c2a74860125421c98f2f93f85880025b4602f25bd7ae4a82f1d7e32f teve3controles aprovados e parada do portal antes dos seis restantes; logFUSE Unable to create dir preservado. Hipótese fundamentada: replace do daemon autoativado durante os quatro launches anteriores disputa desmontagem. Correção só no probe/workflow: iniciar daemon controlado antes da primeira execução Flatpak, recusar substituição de processo alheio e esperar seu próprio FUSE desmontar antes do restart. Duas repetições CI independentes preparadas. App e bundle0.1.16 inalterados; não repetir suíte564/564 ou rebuild sem motivo. Publicáveis emtestes/resultados/sem-vm-2026-10-19/s10-fourth-fuse e docs/CI-FALHAS-E-CORRECOES.md. Usuário avisado da nova falha; notificações não alteradas. VM intocada; próximo: CI duas repetições, examinar ambos os relatórios e consolidar auditoria/retomada somente com evidências aprovadas.


## 2026/10/19 às 20:34 (America/Sao_Paulo, UTC-03:00) —0.1.16 publicada e auditada; desktop9/9

Publicação técnica517afaf confirmada no GitHub, prereleasev0.1.16-devel/asset657710048. Download público sem loginHTTP200/118393760bytes/SHA256ad02f4c5ebb3d3d740a1a5c56fa3f4a71b52e4ac2b94171973f92b7526190816 confere. AuditoriaCI39341656820, artefato12229142103/ZIP6dadd0fa61cd40b04642be4cffb8f07bcb16597a86bfddf699e271db4329a0f1 examinado:11controles/5smoke/3GTK,177arquivos app,3684runtime/483ELF/297avisos e versões fonte conferidos no mesmo bundle sem rebuild. Fonte/payload/sandbox564/564 são a execução anterior39339330479, não repetida pela auditoria. DesktopCI39342162781, artefato12229257765/ZIP29232f1eeffa3c74c27e27d1e8ef037f923f7b90f04a711a75babfaeb0c95dca examinado:9/9 com0.1.14→0.1.16→0.1.14→0.1.16, preferências, grant persistente/revogação e associação/abertura real. Publicáveis emtestes/resultados/0.1.16/audit/ e desktop/, brutosanalysis-local/no-vm-audit-artifact-12229142103 e no-vm-artifact-12229257765. As notificações mostradas pelo usuário eram de testes anteriores que falharam, não de uploads; causas corrigidas e histórico mantido. Tentativa de repetir o publicador só para confirmar URL foi rejeitada pela revisão automática; confirmação resolvida por GET público somente leitura, sem nova mutação ou novo upload. Ferramentas: CI Debian13/GTK/Flatpak/OpenSSL/GStreamer; Windows próprio5/5 anterior, estática Ghidra/Capstone seis entradas novas/266instruções803bytes, catálogo329. VM intocada, nuvem direta adiada, IA excluída. S11/famílias completas/50S12/19 critérios amplos e trabalhos semVM adicionais permanecem abertos; nenhuma porcentagem global inventada ou peso alterado. Próximo: casos executáveisS12 por contrato, demais tipos/chamadores/ownership e contratos XFA/PAdES-LTV/3D; ambientes físicos/RMS precisam recursos reais. Commit das notas e comprovante HEAD remoto/árvore limpa fora da árvore para evitar autorreferência.

A correção final do probe está em1fcc603. Além do primeiro artefato desktop registrado acima, a segunda repetição independente também aprovou9/9:artefato12229856171/ZIP49e0c3d628ecdc6dc4b902d4c56e3c55f73d0032ba3912cd94cca2022c0a6c93. Ambos os relatórios incluem início controlado antes do Flatpak, término com FUSE desmontado e novo início; os três estados foram conferidos. Não afirmar que notificações futuras ou todos os desktops são universalmente livres de falhas.


## 2026/10/19 às 21:38 (America/Sao_Paulo, UTC-03:00) — relatório completo solicitado pelo usuário

Pedido:arquivo sem resumo com tudo realizado,parcial e pendente até a reconstrução/entrega,e explicação da demora. Criado docs/RELATORIO-COMPLETO-LINUXIT-PDF-2026-10-19.md (6606683bytes/134942linhas) e docs/RELATORIO-COMPLETO-LINUXIT-PDF-2026-10-19.html (8136002bytes),autônomo com20capítulos e anexos incorporados/expansíveis. Fotografia Gitb2bb821 confirmada local/remoto antes da geração:25famílias/111operações,21etapas/58critérios/19abertos,50planosS12,329entradas estáticas,564IDs de testes em três ambientes,17manifestos de versão,75módulos/60interfaces,78documentos integrais,38snapshots estruturados,143commits e1530arquivos da fotografia. Inclui notas de continuidade anteriores completas,registro por critério em português e catálogo completo. Separa compilação/Flatpak já existente,reconstrução ampla e comprovação de paridade; explica escopo aberto,checklist pouco sensível,lotes sobrepostos,campos legados,instrumentação,travamentos,retrabalho de código/CI,limites físicos e ausência de controle completo de horas. Identifica combo/voz/camadas/cálculos/portal/assinaturas já presentes apesar de campos antigos ainda dizerem pendente; não altera esses resultados históricos. Não inventa percentual global,ETA ou esgotamento de tokens.

Ferramentas:Python stdlib/AST,git archive imutável,git cat-file --batch,PowerShell ConvertFrom-Markdown/Markdig e verificador próprio HTMLParser; sem aplicativos externos,VM,REA/Ghidra ou nova suítePDF. Gerador inclui AGENTS explicitamente e aceita caminhos relativos normalizados; versões intermediárias próprias preservadas emanalysis-local/report-draft-20261019,ignoradas. scripts/generate_project_report.py,render_project_report.ps1 e check_project_report.py preservados. Fontes editoriais/temposCI emdocs/relatorios/2026-10-19. Prova emtestes/resultados/relatorio-completo-2026-10-19/review.json:317hashes de fontes,4fontes editoriais,11selosCI e177arquivos app conferidos;117textos integrais preservados noHTML,406details balanceados e20âncoras sem duplicação,nenhum recurso externo necessário. MarkdownSHA256f007d8388068a6bd23273c0f119d89f729e5003bdcb420f172fa85a6aa1af5af; HTMLSHA256dc9463286cf91d89f56b1714e2f8100be8ccab65ed1925798c81eaa2f26d76e2. Aplicativo/bundle0.1.16,critérios/pesos/paridade e adiamento de nuvem intactos; IAexcluída. Próximo técnico permanece executar aceitações própriasS12,reconciliar os campos atuais e avançar contratos/estática pendentes; original só após retomada autorizada/controleoffline. Publicar esta documentação e confirmar HEAD remoto com recibo fora da árvore; a criação do relatório não encerra atividades técnicas amplas.


## 2026/10/19 às 21:40 (America/Sao_Paulo, UTC-03:00) — conferência final do relatório integral

Versão final com títulos/espaçamento de navegação revisados:Markdown6606786bytes/134942linhas/SHA256bb4a0dda13b6057b91f34a32b39f2d88088d4151383ac3813da36df2322cae3b;HTML8136186bytes/SHA256dd27d7664b640ceba4f6ebbcbda57653a218126b67babb882848af8fe0b5b9e7. O checkpoint anterior acima descreve a versão intermediária anterior à revisão de títulos; preservado como histórico. Nova conferência aprovou317hashesGit,4fontes editoriais,117textos integrais,564IDs nos três ambientes documentados,406blocosdetails balanceados e20capítulos sem âncoras duplicadas ou dependências externas. Inventários completos e evidências preservados; o próprio aplicativo não foi reexecutado. Gerador recusa sobrescrita e normaliza caminhos de saída; rascunhos próprios preservados no diretório ignorado. O relatório é fotografia b2bb821, e os links de retomada/README foram adicionados depois; isso evita autorreferência. Próximo:publicar e conferirHEAD/árvore limpa fora da árvore. Sem alteração de código app,versão,Flatpak,critérios,pesos ouVM.

## 2026/10/19 às 23:44 (America/Sao_Paulo, UTC-03:00) — entrega integral conferida no chat do laboratório

Usuário pediu arquivo com todo o realizado, parcial e pendente até a conclusão,
e explicação completa da demora. Neste chat de infraestrutura, sem executar
aplicativos nem acessar VM, foi conferido o relatório integral já consolidado
na revisão befc320 (fotografia funcional b2bb821). Git remoto main confirmou
befc320d62c68eaff03334e0b77472617c25605c; checkout limpo na conferência e nenhuma
mudança em app/packaging/tests entre a fotografia e HEAD. API oficial GitHub
reconfirmou prerelease0.1.16, asset118393760bytes/digest igual ao manifesto;
sem novo download integral ou nova instalação.

Validador original executado com as mesmas asserções, somente o destino do
recibo redirecionado para a pasta desta entrega:317fontes Git,4editoriais,
inventários completos e117textos integrais do HTML original conferidos.
Acrescentados16registros integrais do laboratório, com aviso de que descrevem
18/10 e não são estado atual da VM. Relatório original preservado integralmente;
novo capítulo21 registra conferência e laboratório. HTML21capítulos/8226855bytes,
Markdown136326linhas/6686327bytes. Nenhuma suíte de aplicativo ou nova análise do
Foxit foi executada; testes seguem apenas no chat apropriado, parada preservada.

Entrega no workspace irmão Testes de IA, em
relatorios/Linuxit-PDF-2026-10-19-integral/:
RELATORIO-INTEGRAL-LINUXIT-PDF-2026-10-19.html e .md,
CONFERENCIA-DO-RELATORIO.json e CONFERENCIA-ORIGINAL-DO-PROJETO.json.
Hash MD8ffb0fa65a32ba91e176123ce88e796c02b30f2bd52bbe2afb29d11af16ae448;
HTMLb89bf67aaf8926759f9b71cf927049f2e9e5e0f8236638cc58c862387a92a65a.
Código,pacote,critérios,pesos e resultados anteriores preservados. Sem commit/push
nesta entrega do laboratório; esta nota local é a única alteração no projeto.


## 2026/10/20 às 00:19 (America/Sao_Paulo, UTC-03:00) — correção RFC 3161, registros reconciliados e aceitação S12 executável

Pedido do usuário: corrigir os registros desatualizados, executar os planos de aceitação e fazer correções, saindo do ciclo de relatórios sem avanço verificável.

O que foi feito:

1. **Defeito corrigido** (`de7f218`): com OpenSSL 3.0 (Ubuntu 24.04), a verificação de carimbos RFC 3161 falhava sempre, porque `openssl ts -verify` recusa uma pasta vazia como `-CAstore`. O CI usa Debian 13 (OpenSSL mais novo) e não via isso. A loja agora aponta para o próprio arquivo de âncoras explícitas. Teste novo prova que uma autoridade conhecida só pela loja do sistema (`SSL_CERT_FILE`/`SSL_CERT_DIR`) continua recusada.
2. **Registros reconciliados** (`de7f218`): os 8 textos de `scope` da especificação que ainda descreviam 0.1.6–0.1.13 foram reescritos conforme o código 0.1.16 (texto antigo em `scope_previous`); `next_action` desatualizados em `pendencias-analises.json` (antigos em `next_action_previous`); `desktop_portal_interaction_tested` em `projeto.json`; nota de reconciliação no plano; fila atual no topo de `tarefas-pendentes.md`.
3. **Aceitação S12 executável** (`841557d`): `testes/aceitacao/` com 46 casos (36 sem tela pelo worker/módulos e 10 na janela GTK real), fixtures próprias determinísticas fixadas por SHA-256 e `scripts/run_acceptance.py`. O validador da especificação passou a aceitar `passed`/`failed` somente quando o arquivo de resultado confirma caso, estado, horário, fronteira e revisão limpa. Workflow `no-vm-validation.yml` passa a executar os casos no Debian 13.
4. **Execução registrada**: revisão limpa `841557d` (00:18), **46/46 aprovados**, em `testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24.json`, aplicada à especificação e ao registro renderizado. S12-23 (nuvem adiada) e S12-25 (proposta) ficaram `not_run`.

Ferramentas e ambiente: contêiner Ubuntu 24.04 com Python 3.12, GTK 3.24, Poppler 24.02, OpenSSL 3.0.13, Xvfb e dbus, usuário de teste sem privilégios. Suíte própria completa **571/571** (564 anteriores + 7 novos), sem falhas, erros ou skips. `check_architecture.py` e `validate_functional_spec.py --check-render` aprovados. Dois defeitos injetados de propósito (limite de 256 caracteres e `pages_per_sheet` fracionário) foram detectados pelos casos, confirmando que eles não passam por construção.

Limitações:
- O ambiente local não é o Debian 13 do CI; a execução do workflow ainda está pendente.
- `check_operation_catalog.py` acusa drift esperado, porque está preso aos hashes de fontes da entrega 0.1.16; atualizar no próximo pacote validado.
- Casos aprovados são contrato próprio, não observação Foxit, paridade ou família integral.
- Nenhum pacote Flatpak novo, VM intocada, nuvem direta adiada, critérios e pesos inalterados.

Achado menor, sem alteração: a régua do visualizador exibe `2.54 cm` (ponto decimal) numa interface em português; decidir se o padrão deve ser vírgula.

Estado Git: commits `de7f218`, `841557d` e o desta nota, de autoria Claude, feitos localmente; publicação no GitHub pendente de acesso de escrita para esta sessão.

Próximo passo concreto: publicar, executar `no-vm-validation.yml` no Debian 13 e registrar o resultado. Depois, contrato próprio para os casos S12-25 (o portal já foi validado 9/9) e as frentes da fila atual em `progresso/tarefas-pendentes.md`.


## 2026/10/20 às 00:25 (America/Sao_Paulo, UTC-03:00) — CI Debian 13 confirma a rodada e avisos centralizados

Publicação confirmada no GitHub (`a43e0ba`, depois `7b11659`), commits de autoria do Claude. Workflow `no-vm-validation.yml`, execução 39363684386 em `a43e0ba`: jobs `linux-source` e `cups-queue` com sucesso. Artefato 12238690916, ZIP SHA-256 `8da34209d6dc3231fdc93a1606276f2f08fd9d36ff5b3db95404131dbe2b075f`, examinado.

Resultados do artefato:
- Suíte própria **571/571**, sem falhas, erros ou skips (Debian 13, Python 3.13.5, Poppler 25.03, OpenSSL 3.5.7).
- Aceitação **46/46** na revisão limpa `a43e0ba`; o harness tem o mesmo conteúdo de `841557d`.
- Campanha preservada 17/17, AT-SPI entre processos e portal nativo aprovados.

Evidências em `testes/resultados/aceitacao/2026-10-20/execucao-ci-debian13.json` e `ci-debian13-review.json`. A especificação continua apontando para a execução registrada de `841557d`; a do CI é confirmação independente em outro ambiente.

Novo pedido do usuário: todo aviso também vai para `docs/AVISOS-E-STATUS.md` (GitHub) e para `AVISOS-LOCAL.md` na pasta local (ignorado pelo Git). Regra registrada no AGENTS.md.

Limitações: nenhum Flatpak novo, VM intocada, nuvem adiada, critérios e pesos inalterados.

Próximo passo: entrega 0.1.17 com a correção RFC 3161, ou o primeiro item sem VM da fila em `docs/AVISOS-E-STATUS.md`.


## 2026/10/20 às 00:39 (America/Sao_Paulo, UTC-03:00) — etapas pequenas, E01 e E02 concluídas

Pedido do usuário: organizar o que falta em etapas pequenas, salvar nos repositórios e começar pelo que não precisa da VM. Lista em `progresso/etapas-pequenas.json`, renderizada em `docs/ETAPAS-PEQUENAS.md` (24 etapas e a decisão D01), com cópia local `ETAPAS-LOCAL.md`.

- **E01** (`9c10dc4`): `check_operation_catalog.py` voltou a passar. A referência própria agora é o CI 39363684386 (fonte 571/571, hashes da revisão `a43e0ba`). O trecho `verify_trust` foi refixado e o inventário renderizado, que estava desatualizado (95/13 em vez de 97/11), foi regenerado.
- **E02** (`353a30b`): a família platform passou de proposta a contrato próprio (texto anterior em `contract_previous`). S12-25-1 e S12-25-2 acionam o botão real "Abrir pelo seletor do sistema" contra `xdg-desktop-portal` num desktop X11 efêmero, dirigidos por xdotool, com preferências isoladas. Um defeito injetado no cancelamento fez o caso falhar.
- Aceitação: **48/48** na revisão limpa `353a30b` (Ubuntu 24.04), em `testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e02.json`, aplicada à especificação. Só S12-23 (nuvem adiada) fica `not_run`. Suíte própria 571/571 local.

Correção de registro: horários da E01/E02 anotados adiantados (00:36, 00:38, 00:45) foram trocados pelos horários reais dos commits.

Limitações: portal sem FUSE no ambiente local (o seletor funciona; o portal de documentos não monta); confirmação no Debian 13 pendente no CI. Nenhum Flatpak novo; VM intocada.

Próximo passo: E03, formatação AFNumber_Format por gramática fechada.


## 2026/10/20 às 00:48 (America/Sao_Paulo, UTC-03:00) — E03 concluída

- CI 39365389394 (Debian 13) confirmou a E02 na revisão `345b536`: aceitação 48/48 com os dois casos de portal real e suíte 571/571 (`testes/resultados/aceitacao/2026-10-20/ci-debian13-e02-review.json`).
- **E03** (`0600b05`): `AFNumber_Format` e `AFNumber_Keystroke` por gramática fechada em `app/pdf_form_events.py`. O `/V` fica sem formatação e a aparência mostra o número formatado. Vírgula decimal é aceita nos estilos com vírgula; negativos em vermelho são recusados explicitamente. 5 testes novos e caso S12-15-3 com a fixture `formulario-numerico.pdf`. Suíte local 576/576; aceitação 49/49 (`execucao-ubuntu24-e03.json`).
- Verificador do catálogo: `scripts/refresh_operation_pins.py` refixa trechos só deslocados e exige `--accept` depois de revisar trechos alterados. Foram revisadas e aceitas 11 operações: 10 citam o despachante `_apply`, cujo único ramo alterado é o de formulário com eventos, e `forms/events`, que teve o texto do contrato atualizado. Evidência própria desatualizada passa a ser informada, e só bloqueia se alguma operação depender dela.

Próximo passo: E04, datas em formulários.


## 2026/10/20 às 00:55 (America/Sao_Paulo, UTC-03:00) — E04 concluída

- CI 39366205486 (Debian 13) confirmou a E03 na revisão `9ab22e5`: aceitação 49/49 e suíte 576/576 (`ci-debian13-e03-review.json`).
- **E04** (`34ebb46`): `AFDate_FormatEx` e `AFDate_KeystrokeEx` com dia, mês e ano numéricos e separadores `/ - .` ou espaço. Datas inexistentes são recusadas; `yy` vale 1950–2049. O valor fica como digitado e a aparência mostra a data formatada. Nomes de mês, horas e texto no padrão são recusados explicitamente. 3 testes novos, fixture `formulario-data.pdf` e casos S12-15-4/S12-15-5. Suíte local 579/579; aceitação 51/51 (`execucao-ubuntu24-e04.json`). Trecho `calculate_form_values` revisado e refixado.

Próximo passo: E05, AFSpecial_Format.


## 2026/10/20 às 01:06 (America/Sao_Paulo, UTC-03:00) — E05 concluída; parada aguardando o usuário

- CI 39366798234 (Debian 13) confirmou a E04 na revisão `f20d23e`: aceitação 51/51 e suíte 579/579 (`ci-debian13-e04-review.json`).
- **E05** (`e8cface`): `AFSpecial_Format` e `AFSpecial_Keystroke` 0–3 guardam só os dígitos e mostram a máscara. `AFSpecial_KeystrokeEx` com máscara livre (9, A, O, X e literais) aceita o texto com ou sem os literais e guarda o texto mascarado. 4 testes novos, fixture `formulario-mascaras.pdf` e casos S12-15-6/S12-15-7. Na primeira execução, a conferência do caso S12-15-6 procurava bytes sem escape na aparência (o PDF escapa parênteses); foi corrigida para usar o texto visível via `pdftotext`. Aceitação 53/53 (`execucao-ubuntu24-e05.json`).
- Uma primeira tentativa da aceitação foi encerrada pelo ambiente (código 137) e repetida.
- Achado: `test_local_playback` (GStreamer) falhou 1 vez em 3 neste contêiner, sem relação com a E05. Fica registrado como decisão D02.
- **Regra nova do usuário (00:58)**: ao concluir uma etapa, parar e aguardar confirmação antes da próxima. Registrada em AGENTS.md e nas regras da lista. E06 permanece pendente.


## 2026/10/20 às 01:09 (America/Sao_Paulo, UTC-03:00) — decisões D01 e D02 registradas

Respostas do usuário às 01:08: D01, régua com vírgula decimal (2,54 cm); D02, tornar estável o teste de mídia como etapa própria. Criadas as etapas E25 e E26, colocadas logo depois da E05 na lista. Nada foi executado; o usuário vai continuar depois. CI 39367796407 (Debian 13) ainda confirmando a E05.


## 2026/10/20 às 01:13 (America/Sao_Paulo, UTC-03:00) — CI confirma a E05

CI 39367796407 (Debian 13) na revisão `860a958`: aceitação 53/53 e suíte 583/583, sem falhas; o teste de mídia passou no CI (`ci-debian13-e05-review.json`). Nenhuma etapa nova iniciada.


## 2026/10/20 às 10:05 (America/Sao_Paulo, UTC-03:00) — E25 concluída

Pedido do usuário às 09:58: continuar. **E25** (`db8c6fe`): `measurement.decimal_text` com vírgula decimal (decisão D01) na régua (2,54 cm), na janela de medidas (até seis algarismos significativos) e no tamanho da página (uma casa). Trecho `PDFWindow._finish_measure` revisado e refixado; texto da operação `measurement/distance` atualizado. Suíte local 584/584; aceitação 53/53 (`execucao-ubuntu24-e25.json`). Parado; E26 aguarda confirmação do usuário.


## 2026/10/20 às 10:11 (America/Sao_Paulo, UTC-03:00) — CI confirma a E25

CI 39427531619 (Debian 13) na revisão `d8c25ab`: aceitação 53/53 e suíte 584/584 (`ci-debian13-e25-review.json`). Nenhuma etapa nova iniciada.


## 2026/10/20 às 10:25 (America/Sao_Paulo, UTC-03:00) — E26 concluída

Pedido do usuário às 10:16: fazer as duas próximas da fila (E26 e E06) e parar. **E26** (`5747278`): reprodução de 25 execuções mostrou EOS a 0,02 s num WAV de 1 s; causa: sinks com `async=False` deixavam o pipeline ir a PLAYING antes de o ramo de áudio estar ligado. `play()` agora pré-carrega em PAUSED até `ASYNC_DONE` e então toca; retomar de uma pausa pré-carregada é imediato. Após a correção, 40/40 na reprodução; teste novo de duração mínima (código antigo falhou 6/10); testes de reprodução 20/20 seguidos; suíte 585/585; aceitação 53/53. Próximo: E06.


## 2026/10/20 às 10:43 (America/Sao_Paulo, UTC-03:00) — E06 concluída; CI da E26 confirmado

**E06** (`06daa9d`): novo `app/pdf_xfa.py` detecta `/AcroForm /XFA` (fluxo XDP único ou lista de pacotes; híbrido ou só XFA; `/NeedsRendering`) e lista os valores do pacote `datasets` por caminho SOM (`form1[0].nome[0]`). Somente leitura: o modelo e os scripts XFA não são interpretados nem executados. Análise expat em fluxo, recusando DOCTYPE/entidades; limites de 8 MiB, profundidade 64, 5000 valores e 4096 caracteres por valor. O pacote `datasets` é lido sozinho e, se o escritor dividiu elementos entre fluxos, a junção dos pacotes. `inspect_document_panels` devolve a chave `xfa`; o menu ganhou "Campos de formulário XFA…" (`PDFWindow._xfa_dialog`), que distingue carregando/falha/sem XFA. A gravação de cópias de PDFs XFA continua recusada (E07). Fixture nova `formulario-xfa.pdf`; 10 testes portáveis em `tests/test_pdf_xfa.py`; casos S12-15-8 (worker) e S12-15-9 (GTK). `forms/xfa` passou a `bounded_source_present` (catálogo 98/10/3); pinos de `attachments/encrypted` e `layers-media/list` revistos (só ganharam o estado XFA). README da aceitação atualizado (42 + 11 + 2 casos). Suíte local 595/595; aceitação 55/55 na revisão limpa `06daa9d` (`execucao-ubuntu24-e06.json`).

**CI da E26**: a execução 39430260690 (revisão `d07a204`) falhou nas duas tentativas com SIGSEGV logo após `Gtk-CRITICAL _gtk_css_rgba_value_get_rgba` em `test_comment_threads...test_reply_and_bookmark_hits_select_the_actual_panel_row`, sem pilha Python. Os pacotes Debian eram iguais aos da E25 aprovada, e o código da E26 não roda antes desse teste; no Ubuntu o mesmo arquivo de teste passou 25/25. O commit `95a46ba` liga `-X faulthandler` na suíte do `check_intermediate.py`; a execução 39431578427 nesse commit passou (suíte 585/585, aceitação 53/53; `ci-debian13-e26-review.json`). A queda foi registrada como decisão D03, aguardando o usuário.

Parado. Próximo: E07 e a resposta da D03, ambas aguardando confirmação do usuário. CI da E06 a disparar após a publicação.


## 2026/10/20 às 10:49 (America/Sao_Paulo, UTC-03:00) — CI confirma a E06

CI 39432901662 (Debian 13) na revisão `9abc923`: suíte 595/595 e aceitação 55/55 (`ci-debian13-e06-review.json`), sem a queda do GTK desta vez. Nenhuma etapa nova iniciada; E07 e D03 aguardam o usuário.


## 2026/10/20 às 12:25 (America/Sao_Paulo, UTC-03:00) — E27 concluída

Pedido do usuário às 10:53 (decisão D03): investigar a queda do GTK como etapa própria e, em seguida, fazer a próxima etapa. **E27** (`79851e9`; revisão em `testes/resultados/e27-gc-threads/2026-10-20/revisao.json`).

Reprodução: imagem Debian 13 local (Docker, `mirror.gcr.io/library/debian:13`, mesma lista de pacotes do CI, GTK 3.24.49-3): 11 execuções completas do `check_intermediate.py` (7 no HEAD, 4 em `d07a204`) e 17 do subconjunto inicial de testes, sem queda. Novo fluxo manual `native-crash-diagnosis.yml` + `scripts/diagnose_native_crash.py` (`c22ae74`): 6 fragmentos × 3 suítes com `G_DEBUG=fatal-criticals` e pilhas faulthandler em SIGTRAP/SIGSEGV; execução 39441225225 sem nenhum aviso crítico. Uma terceira tentativa da execução 39430260690 em `d07a204` passou. Conclusão: evento raro, dependente de tempo.

Causa: a sonda `scripts/probe_gc_threads.py` (DEBUG_SAVEALL + callbacks do gc) mostrou que o coletor cíclico automático do Python rodava em threads de trabalho e liberava objetos GTK fora da thread principal: 546 numa suíte completa em `06daa9d` (222 Button, 72 ToggleButton, ListBox, ScrolledWindow e janelas PDFWindow inteiras). O GTK 3 não é seguro entre threads; finalizar estilos em paralelo com o cálculo de CSS na thread principal explica o aviso `_gtk_css_rgba_value_get_rgba` seguido de SIGSEGV. É a melhor explicação compatível com a evidência, não uma pilha capturada.

Correção: `app/main_thread_gc.py`, instalado por `PDFWindow.__init__`, desliga a coleta automática em processos com interface e executa a mesma política geracional por um temporizador GLib (250 ms, prioridade baixa) na thread principal. Contagem de referências inalterada; processos só de worker mantêm o coletor padrão. Sonda depois: 0 objetos GTK liberados por threads de trabalho. Testes novos em `tests/test_main_thread_gc.py` (5, incluindo um que demonstra o perigo sem o módulo). Suíte local 600/600; aceitação 55/55 (`execucao-ubuntu24-e27.json`); CI 39446879815: suíte 600/600, aceitação 55/55; diagnóstico 39446885599 depois da correção: 18 suítes sem aviso crítico.

Limite: a ausência de um evento raro não se prova estatisticamente; faulthandler e o fluxo de diagnóstico ficam disponíveis. Próximo: E07, já autorizada.


## 2026/10/20 às 12:32 (America/Sao_Paulo, UTC-03:00) — E07 concluída

**E07** (`aff57e0`): `pdf_changes._editable` ganhou `allow_xfa`; só a inspeção de edição e a gravação de cópias aceitam XFA, e apenas híbrido legível com pacote datasets (proteção e assinatura continuam recusando XFA). Em XFA, `save_edited_copy` aceita só `fill-text-fields` e `fill-form-events`; compara os valores de texto antes e depois e espelha cada valor alterado (digitado ou calculado) com `pdf_xfa.write_field_values`: caminho de dados = nome do campo sem segmentos `#...` e com `[0]` onde faltar índice; substituição só do conteúdo do elemento por deslocamento de bytes do expat (elemento vazio `<x/>` vira `<x>v</x>`), escape XML, declaração UTF-8 ou ASCII (referências numéricas), reanálise de conferência, novo fluxo FlateDecode no lugar do antigo. A cópia escrita é reaberta e AcroForm e datasets precisam bater. Recusas: só XFA, campo sem dado, texto rico, outras operações, pacote dividido entre fluxos. `edit-info` traz `xfa.bound_text_fields`; o diálogo de preenchimento só oferece esses campos e avisa que os dados XFA também mudam. Fixture `formulario-xfa.pdf` ganhou `form1[0].extra[0]` sem dado XFA. S12-15-8 deixou de esperar a recusa antiga (texto anterior em `expected_previous`); novos S12-15-10 e S12-15-11. Suíte local 607/607; aceitação 57/57 na revisão limpa (`execucao-ubuntu24-e07.json`). CI Debian 13 disparado. Parado; E08 aguarda o usuário.


## 2026/10/20 às 12:37 (America/Sao_Paulo, UTC-03:00) — CI confirma a E07

CI 39449238643 (Debian 13) na revisão `aff57e0`: suíte 607/607 e aceitação 57/57 (`ci-debian13-e07-review.json`). Nenhuma etapa nova iniciada; E08 aguarda o usuário.


## 2026/10/20 às 12:47 (America/Sao_Paulo, UTC-03:00) — E28 concluída

Pedido do usuário às 12:38: procurar a decisão sobre nuvem e pastas sincronizadas e fechar o ciclo. Decisões encontradas: "Deixar nuvem para depois" (17/10/2026 19:20) e fluxo de pastas sincronizadas por cliente externo (17/10/2026 20:51; `docs/PASTAS-SINCRONIZADAS.md`, `progresso/projeto.json` → `local_folder_workflow`). A família `cloud` era `proposed_only` com S12-23 sobre provedor simulado, por isso ficava fora da aceitação.

**E28** (`033e245`): `cloud` passou a `implemented_subset` com o fluxo de pasta sincronizada; contrato anterior em `contract_previous`/`scope_previous`, casos anteriores em `expected_previous`. Novos S12-23-1 (abrir pela pasta preferida, seletor começa nela, cópia idêntica, sem temporários, estado "salva localmente… sincronizador") e S12-23-2 (troca externa bloqueia salvar até reabrir; arquivo criado pelo cliente com o mesmo nome não é sobrescrito; sem falso sucesso), na janela real com os seletores GTK respondidos como um usuário. Matriz de paridade, arquitetura, ESCOPO, projeto.json e PASTAS-SINCRONIZADAS atualizados. `cloud/login`, `cloud/transfer` e `cloud/collaboration` continuam `deferred_by_user`. `tests/test_acceptance_records.py` cria a própria família proposta, já que nenhuma real restou. Suíte 607/607; aceitação 59/59 na revisão limpa (`execucao-ubuntu24-e28.json`). Pendente fora do código: cliente sincronizador real. Parado; E08 aguarda o usuário.


## 2026/10/20 às 12:52 (America/Sao_Paulo, UTC-03:00) — CI confirma a E28

CI 39451575700 (Debian 13) na revisão `033e245`: suíte 607/607 e aceitação 59/59 (`ci-debian13-e28-review.json`). Nenhuma etapa nova iniciada; E08 aguarda o usuário.


## 2026/10/20 às 13:47 (America/Sao_Paulo, UTC-03:00) — E08 concluída

**E08** (`ae429cd`): `pdf_signing` passou a escrever a atualização incremental à mão (`_incremental_update`): objetos novos (valor e campo de assinatura), AcroForm reescrito no mesmo número (ou novo objeto + catálogo atualizado quando direto/ausente), seção `xref` clássica com subseção `0 1` ou fluxo `/Type /XRef` sem filtro (`/W [1 4 2]`), conforme a seção anterior, com `/Prev`, `/Root`, `/Info`, `/ID`. O modo incremental do pypdf 6.20.1 foi testado e descartado: na terceira assinatura reaproveitou os números 13/14 da revisão anterior e o `/V` do novo campo apontou para dados de outro objeto. `_signing_source` substitui `_editable` na assinatura: aceita campos de assinatura existentes e `/Perms` só com DocMDP P=2/3; recusa UR3, P=1, criptografia, XFA, portfólio, mais de 15 assinaturas e qualquer assinatura existente que não verifique (inspeção completa antes). Depois de montar a cópia: começa com os bytes da origem, as anteriores verificam sem cobrir o arquivo todo e a nova cobre tudo. Recusas de política usam `SigningRefused`, cuja mensagem o worker repassa (as demais falhas continuam com a mensagem genérica, para não expor dados da chave). Testes: `tests/test_incremental_signatures.py` (3 assinaturas + pdfsig 3×válida; origem com fluxo de xref gerada pelo qpdf + `qpdf --check`; recusas), teste antigo de recusa da segunda assinatura trocado. Aceitação S12-17-3 e S12-17-4. Suíte 610/610; aceitação 61/61 na revisão limpa (`execucao-ubuntu24-e08.json`). CI disparado. Próximo: E09.


## 2026/10/20 às 15:09 (America/Sao_Paulo, UTC-03:00) — E09 concluída; correção do teste da E08

**E09** (`df7207a`): `pdf_signatures._verify_document_timestamp` (openssl cms -verify -noverify extrai o TSTInfo; asn1crypto confere `tst_info`, algoritmo SHA-256/384/512 e `hashed_message` contra os bytes cobertos); `record.kind` = `document_timestamp`/`signature` e `timestamp_time`. `signature_trust.verify_document_timestamp` (openssl ts -verify com `-CAfile`/CApath vazio/CAstore da âncora, `-untrusted` com os certificados do token, CRL opcional) e `_anchors` extraído de `verify_trust`. `pdf_signing.append_signature_revision` isola o escritor incremental com reserva, usado pela assinatura e pelo gerador de carimbos `testes/aceitacao/carimbo.py`. Janela de assinaturas mostra 'Carimbo de tempo do documento · horário'. Testes `tests/test_document_timestamps.py` (3); casos S12-17-5 e S12-17-6; `signatures/timestamp-ltv` passa a recorte implementado (catálogo 99/9/3). poppler `pdfsig` não verifica ETSI.RFC3161 (lista o campo como tipo desconhecido); a assinatura posterior ele valida. Suíte 613/613; aceitação 63/63 na revisão limpa (`execucao-ubuntu24-e09.json`).

CI da E08 (39460438529, `ae429cd`): falhou só no portão de 'nenhum teste pulado' — `test_cross_reference_stream_source_gets_a_stream_update` exigia qpdf, ausente no CI (609 aprovados + 1 pulado). Corrigido em `9e75c0c`: a origem com fluxo de referência cruzada vem do escritor incremental do pypdf; `qpdf --check` só como verificação extra. O CI de `df7207a` foi cancelado e um novo foi disparado em `9e75c0c`. Próximo: E10.


## 2026/10/20 às 15:19 (America/Sao_Paulo, UTC-03:00) — E10 concluída

**E10** (`ba38ca7`): `pdf_signatures._dss_material` lê `/DSS` (`/Certs` ≤64, `/CRLs` ≤32, ≤1 MiB cada, todos analisados; `/OCSPs` e `/VRI` só contados) e o relatório ganha `dss`/`dss_error`. `signature_trust._dss_files`; `verify_trust(…, dss)` acrescenta os certificados do DSS a uma cópia de verificação do conjunto de certificados do CMS (o `openssl cms -verify` 3.0 não tem `-untrusted` e `-certfile` só procura o signatário; o conjunto de certificados não é assinado, então a integridade não muda) e as CRLs ao arquivo de âncoras; `verify_document_timestamp(…, dss)` usa `-untrusted`. Âncoras continuam só as escolhidas pelo usuário (teste com raiz posta no DSS). Revisão DSS de teste via `carimbo.add_dss` (mesmo escritor incremental). Testes `tests/test_dss_validation.py` (3); casos S12-17-7 e S12-17-8. Suíte 616/616; aceitação 65/65 na revisão limpa. CI 39472280348 em `9e75c0c` confirmou E08+E09: suíte 613/613, aceitação 63/63 (`ci-debian13-e09-review.json`). Próximo: E11 (entrega 0.1.17).


## 2026/10/20 às 15:25 (America/Sao_Paulo, UTC-03:00) — CI confirma a E10; E11 em andamento

CI 39473724324 (Debian 13) na revisão `ba38ca7`: suíte 616/616 e aceitação 65/65 (`ci-debian13-e10-review.json`). E11: `dec46c9` muda a versão para 0.1.17 (app, mapa de arquitetura, notas AppStream) e faz `record_linux_candidate.py` copiar `runtime-source-access.json` para os relatórios. Construção e testes do Flatpak no fluxo `linux-flatpak.yml` (execução 39474059660) em andamento.


## 2026/10/20 às 15:40 (America/Sao_Paulo, UTC-03:00) — E11: candidato 0.1.17 aprovado; publicação aguarda o usuário

CI 39474059660 (`linux-flatpak.yml`, revisão `dec46c9`): 616/616 em fonte, payload e sandbox, sem skips; smoke 5/5; launcher 3/3; 179 arquivos fonte/payload iguais; 3684 arquivos de runtime, 483 ELF, 297 pacotes Debian. Bundle `LinuxitPDF-0.1.17-x86_64.flatpak`, 118422768 bytes, SHA-256 `ec773a2028b63a4026c32866472504bbf7aad7e9994ce2edb78954cfb8217a71`, conferido no download do artefato. Relatórios em `testes/resultados/0.1.17/`; `releases/manifest-0.1.17.json` (igual ao candidato + distribuição), `releases/runtime-packages-0.1.17.tsv`, `releases/runtime-source-access-0.1.17.json`, `releases/notes-0.1.17.md`. `releases/manifest.json` e `SHA256SUMS` continuam em 0.1.16 até a publicação (a auditoria baixa cada linha do SHA256SUMS). A criação da release pela API voltou 403 ('Creating, editing, or deleting releases is not permitted for this session type'). Novo fluxo manual `publish-devel-release.yml` para o dono do repositório: baixa o artefato do CI do candidato, confere tamanho/SHA-256 contra o manifesto e cria a prerelease `v0.1.17-devel` com as notas, sem recompilar. Não foi disparado por esta sessão. Depois da publicação: atualizar `manifest.json`/`SHA256SUMS`, registrar `release-publication.json` e `download-integrity`, disparar `delivery-audit.yml` e `desktop-integrations.yml`.


## 2026/10/20 às 15:50 (America/Sao_Paulo, UTC-03:00) — E12 concluída

**E12** (`12dda24`): nova operação `style-annotation` (`app/annotation_style.py`): valida cor RGB 0–1 e opacidade 0,1–1; grava `/C`, `/CA` e nova `/AP /N` desenhada da geometria (`/Rect`, `/QuadPoints`, `/L`, `/InkList`, `/Vertices`), espessura de `/BS /W`, `/IC` preservado como preenchimento, ExtGState `/LinuxitStyle` com `/CA`/`/ca` (e `/BM /Multiply` em destaques). Recusa notas, FreeText, Stamp, anotações bloqueadas ou com respostas/popup. `edit-info` passa a trazer `styleable`, `color` e `opacity`; diálogo com `Gtk.ColorButton` e opacidade em %. Testes: `tests/test_annotation_style.py` (cinco tipos ficam azuis a 50%, conferidos em pixels do `pdftoppm`; repetição; recusas) e `tests/test_annotation_style_gtk.py`. Casos S12-14-3 e S12-14-4. Catálogo: nova operação `annotations/style` (112 operações; 100/9/3); 20 pinos de `_apply` revistos (só ganharam o ramo novo). Suíte 620/620; aceitação 67/67 na revisão limpa. CI disparado. Próximo: E13.


## 2026/10/20 às 15:58 (America/Sao_Paulo, UTC-03:00) — E13 concluída

**E13** (`9a10b42`): operação `resize-annotation` (`annotation_geometry.resize_annotation`): retângulo validado por `_annotation_rect` (dentro do CropBox), lado mínimo 0,25 pt, `/RD` removido; Square/Circle redesenhados por `restyle_annotation` com a cor e opacidade atuais (preto sem `/C`); FreeText diagramado de novo pelo worker `annotation-appearance`, agora compartilhado em `_text_appearance`. `edit-info` traz `resizable` e `rect`; diálogo com quatro campos já preenchidos. Testes `tests/test_annotation_resize.py` (3) e diálogo GTK; casos S12-14-5 e S12-14-6; operação `annotations/resize` no catálogo (113; 101/9/3); 20 pinos de `_apply` revistos. Suíte 624/624; aceitação 69/69 na revisão limpa. CI 39478253038 confirmou a E12 (suíte 620/620, aceitação 67/67). Próximo: E14.


## 2026/10/20 às 16:09 (America/Sao_Paulo, UTC-03:00) — E14 concluída — marcar áreas para redação

- Código `7488bc7`: operação `add-redaction` (app/pdf_changes.py) cria `/Redact` via `annotation_style.create_redaction` (Rect, QuadPoints, /IC preto, /BS tracejado, aparência própria vermelha tracejada). `/Redact` entrou em STYLEABLE, RESIZABLE (QuadPoints acompanham o novo Rect) e nos tipos editáveis/removíveis.
- Diálogo "Marcar área para redação" no rascunho de edição (edit_dialogs/edit_window).
- Testes: tests/test_redaction_marks.py (5, inclui pixels do Poppler) e teste GTK do diálogo. Suíte 630/630 sem pulos.
- Aceitação S12-14-7 e S12-14-8; execução limpa 71/71 em `execucao-ubuntu24-e14.json`. Catálogo: operação annotations/redaction-mark (114 operações, 102 com fonte própria), revisão 18.
- CI Debian 13 da E13 (execução 39479407491) confirmado: 624/624, aceitação 69/69 em 9a10b42 (`ci-debian13-e13-review.json`).
- Próximo: E15 (aplicar redação numa cópia nova, rasterizando só as páginas afetadas).


## 2026/10/20 às 16:22 (America/Sao_Paulo, UTC-03:00) — E15 concluída — aplicar redação

- Código `61f180e`: `app/pdf_redaction.py` (`redact_copy`, `invoke_redaction`), comando de worker `redact-copy`, botão "Aplicar redação em cópia nova…" no rascunho (`edit_window._apply_redaction`, diálogo `edit_dialogs.redaction_apply_dialog`, 150/300 DPI). Usa o estado atual do rascunho; original e rascunho intactos.
- Página marcada: renderizada pelo pdftocairo sem anotações e com /Rotate 0, áreas pintadas com /IC (+1 px), conteúdo trocado por uma imagem Flate. `compress_identical_objects(remove_duplicates=False, remove_unreferenced=True)` descarta o conteúdo antigo. Árvore de estrutura removida quando existe.
- Testes: tests/test_redaction_apply.py (6) e tests/test_redaction_gtk.py (2). Suíte 638/638 sem pulos. Aceitação S12-14-9/10; execução limpa 73/73. Catálogo: annotations/redaction-apply (115 operações, 103 com fonte). Módulo novo registrado na arquitetura (79 módulos). Contrato em docs/ANOTACOES-AMPLIADAS.md.
- CI Debian 13 da E14 (39481083740) confirmado: 630/630, 71/71 em 074087b.
- Bloco E12–E15 concluído. Pedido do usuário às 16:17: retomar a E08 e resolver o erro.


## 2026/10/20 às 16:33 (America/Sao_Paulo, UTC-03:00) — E08 — erro de CI resolvido; CI confirma E15

- Falha original: CI 39460438529 (ae429cd), 609/610 com 1 pulado (`test_cross_reference_stream_source_gets_a_stream_update`, qpdf ausente). Revisão: `ci-debian13-e08-falha-review.json`; seção em docs/CI-FALHAS-E-CORRECOES.md.
- Correções: 9e75c0c (fixture pelo pypdf) e f92278b (pdfsig confere 2 assinaturas válidas na cópia com xref em fluxo; `qpdf` instalado em no-vm-validation.yml).
- Confirmação: CI 39483614911 em f92278b, 638/638 sem pulos, aceitação 73/73; o teste do xref em fluxo passou (`ci-debian13-e08-fix-review.json`).
- CI 39482926923 em 500a7ed confirmou a E15: 638/638, 73/73 (`ci-debian13-e15-review.json`).
- Parado. Pendente do usuário: publicar a 0.1.17 (E11).


## 2026/10/20 às 16:43 (America/Sao_Paulo, UTC-03:00) — E11: 403 na publicação, fluxo ajustado

- Execução 39485174222 (disparada pelo usuário): download e conferência do pacote OK; `gh release create` → HTTP 403 "Resource not accessible by integration" com Contents: write. Sem rulesets. Causa provável: criar a tag em dec46c9 (workflows diferentes da main) exige permissão `workflows`.
- Tentei criar a tag por git push desta sessão: não permitido. Não insisti.
- Commit 8fbb7d5: o fluxo cria rascunho de prerelease (sem tag) com o mesmo pacote; o dono publica o rascunho na página Releases (a tag nasce no commit testado). Se a tag já existir no commit testado, publica direto.
- Próximo: usuário roda de novo "Publish tested development release (manual)" e publica o rascunho.


## 2026/10/20 às 17:01 (America/Sao_Paulo, UTC-03:00) — E11 concluída — 0.1.17 publicada e auditada

- Publicação: release 418804985, tag v0.1.17-devel → dec46c9, asset 660312363 (118422768 bytes, digest ec773a20…). Rascunho criado/publicado pela sessão do dono no navegador interno (confirmação do usuário às 16:53); pacote anexado pelo fluxo 39486650871 (publish-devel-release.yml agora só anexa a rascunho existente). Falhas 403 do token: 39485174222, 39486020955; causa não identificada (sem rulesets, sem imutabilidade; permissão padrão do repositório é leitura, mas o job recebia Contents: write).
- Download público sem login: HTTP 200, 118422768 bytes, hash igual (`download-integrity-2026-10-20.json`). `releases/manifest.json` = 0.1.17; SHA256SUMS com a linha nova.
- Auditoria: 39487498872 falhou ('Application source changed since tests' — main mais nova). `scripts/audit_delivery.py` lê app/, construtor, versão e licenças do commit testado via Git (12500d5). Reexecução 39488048823 aprovada: controles 11, smoke 5/5, GTK 3, 179 arquivos, runtime 3684/483 ELF/297 pacotes. Revisão em testes/resultados/0.1.17/audit/.
- Desktop 39487502789: 9/9 × 2 repetições com 0.1.14↔0.1.17. Revisão em testes/resultados/0.1.17/desktop/.
- Parado, aguardando o usuário.


## 2026/10/20 às 17:09 (America/Sao_Paulo, UTC-03:00) — E29 prioritária (403 ao criar release)

- Pedido do usuário: registrar como instrução prioritária o erro 403 do token do Actions ao criar releases; o Codex vai investigar. Documento: docs/PRIORIDADE-E29-ERRO-403-RELEASE.md (execuções, configurações verificadas, hipóteses, diagnóstico sugerido, regras). E29 inserida na lista como em andamento.
- Retomada do Claude agendada para 20:10: ler as notas/commits do Codex; se a E29 estiver resolvida, prosseguir com E16–E20 (autorizado pelo usuário) e parar; se não, tentar resolver com base no diagnóstico do Codex.

## 2026/10/20 às 17:14 (America/Sao_Paulo, UTC-03:00) — início E29 pelo Codex

Atualizado de befc320 para 353aa73; nota local do laboratório guardada em backup e integrada sem perda das notas remotas. E29 é prioridade exclusiva. Documentação oficial https://docs.github.com/en/rest/releases/releases?apiVersion=2022-11-28 (Create a release) confirma exigência Workflows em alvos cujos workflows diferem da main, mesmo rascunhos; GITHUB_TOKEN não recebe essa permissão. Preparado scripts/diagnose_release_403.py e fluxo manual diag-release-403.yml: três alvos, draft:true, limpeza por ID/tag/prefixo da própria execução, sem criação de refs, conferência de inventário público antes/depois. Somente contents:write; write-all não necessário antes da comparação. Execução e resultado ainda pendentes. Releases existentes, app, critérios e VM preservados.

## 2026/10/20 às 17:19 (America/Sao_Paulo, UTC-03:00) — causa E29 reproduzida

CI 39490423511/038ae75: rascunho alvo omitido201, main038ae75 201, alvo dec46c9 403. Mesmo GITHUB_TOKEN contents:write. IDs418829657/418829690 removidos DELETE204, três refs404, inventário público/asset intacto. Recibo sanitizado/hashes em testes/resultados/e29-release-403/. Documentação oficial confirma Workflows:write quando alvo difere da branch padrão, mesmo draft; GITHUB_TOKEN não admite essa autorização. Nenhum write-all/configuração/token novo necessário. Corrigido publish-devel-release.yml com preflight somente leitura, conferência de SHA/tag/digest e plano explícito (já publicado/automático elegível/rascunho do dono). Conferir somente é padrão; nesta sessão só rodar esse modo. Oito testes portáveis de guardas passaram. Não declarar E29 concluída: próximo pacote automaticamente publicado ainda deve ser comprovado em entrega autorizada, sem violar a proibição atual. App/VM/bundles preservados. Próximo: conferir o fluxo corrigido no CI em modo somente leitura e publicar a revisão final das notas.

## 2026/10/20 às 17:22 (America/Sao_Paulo, UTC-03:00) — correção E29 validada sem publicação

CI39491077708/dc49fcd aprovado: check_only:true, plano already_published para0.1.17/dec46c9, oito testes de guardas aprovados; etapas de download/envio/criação intencionalmente não executadas. Artefato12295596448/SHA256b71351fbff1b3e6665356f016432ca30cf6f0051d3448e84f0b115c9bb7dfe91 conferido. No Windows, mesmo recorte8/8 via runner padrão após ajustar importação dos testes para execução independente; sem suite completa do app. API final: rascunhos418829657/418829690 retornam404, três tags404, nenhuma sobra e releases/assets públicos iguais ao inventário inicial. Resultados e recibos em testes/resultados/e29-release-403/. AGENTS/RETOMADA/avisos/etapas atualizados; cópias locais AVISOS-LOCAL e ETAPAS-LOCAL atualizadas. A causa foi resolvida e o preflight corrigido; E29 continua em andamento exclusivamente porque o critério exige próxima publicação real automática. Não criar release/tag nesta rodada. Para o próximo pacote: workflows finalizados antes de gerar candidato e iguais até publicação, conferir plano, publicar somente bytes testados; se workflows mudaram, novo candidato ou rascunho preparado pelo dono. Nenhuma configuração da conta/token extra/VM/app/Flatpak alterada, nenhum início de próxima etapa. Próximo: commit/push e comprovar sincronismo remoto.

## 2026/10/20 às 17:43 (America/Sao_Paulo, UTC-03:00) — recado explícito para a retomada do Claude

A pedido do usuário, adicionado recado direto no documento docs/PRIORIDADE-E29-ERRO-403-RELEASE.md e ponteiro no topo de docs/RETOMADA.md. Recado registra causa confirmada, commits/evidências, fluxo corrigido e CI aprovado, modo Conferir somente, procedimento de manter workflows iguais entre candidato/publicação e alternativa do rascunho do dono. Distingue correção validada da próxima publicação automática real ainda pendente. Orienta não repetir diagnóstico nem mudar o SHA para escapar da restrição. Nenhuma mensagem enviada a outro chat, agendamento alterado, release/tag criada ou teste de app/VM executado. Notas e aviso seguem para o GitHub nesta rodada.


## 2026/10/20 às 20:12 (America/Sao_Paulo, UTC-03:00) — retomada do Claude: E29 conferida, início E16

- Conferido: CI 39490423511 (038ae75) concluído com sucesso; probe com três rascunhos (alvo omitido e main criados e apagados; dec46c9 negado); inventário público igual; releases v0.1.16-devel e v0.1.17-devel com 1 asset cada. CI 39491077708 (check_only) aprovado com plano already_published. Causa considerada resolvida para fins da retomada; o critério final (próxima publicação automática real) fica para a entrega 0.1.18: workflows finalizados antes do candidato e iguais à main até publicar.
- Prosseguindo com E16–E20 (autorização do usuário às 17:07); parar após E20.


## 2026/10/20 às 20:23 (America/Sao_Paulo, UTC-03:00) — E16 concluída — imagem de apresentação 3D

- Código `3f15382`: `pdf_media._poster`/`render_poster` (aparência /AP /N, BBox via /Matrix → Rect, pdftocairo até 1600 px, publicação exclusiva), comando de worker `media-poster`, `media_assets_window.Poster3DWindow` com aviso acessível. Lista 3D ganhou `poster`, `model_embedded`, `views`; anotação 3D só com pôster também aparece; extração de recurso sem modelo é recusada.
- Testes: tests/test_media_3d_poster.py (4) e GTK `test_poster_window_shows_the_appearance_and_says_the_scene_is_not_interactive`. Suíte 651/651 (inclui os 8 testes de preflight do Codex). Aceitação S12-21-3/4; execução limpa 75/75. Catálogo: layers-media/3d-poster (116 operações, 104 com fonte); layers-media/3d (interação) continua pendente.
- Próximo: E17 (corpus de PDFs danificados).


## 2026/10/20 às 20:35 (America/Sao_Paulo, UTC-03:00) — E17 concluída — corpus de PDFs danificados

- Código `8e38205`: `document_session` captura mensagens do pypdf (logger com handler próprio, propagate desligado, warnings registrados) e classifica em categorias fixas (`REPAIR_MARKERS`); `_check_pages` resolve conteúdos (em recuperação, decodifica e troca conteúdo ilegível por fluxo vazio, inclusive no objeto em cache usado pelo clone); `_rebuilt` tenta %%EOF e trailer mínimo; `_normalise_page_tree` remove Kids sem página e recalcula /Count; resposta ganhou `repairs`; `describe_repairs` dá texto fixo para a pergunta e o status (main.py).
- Corpus: 12 fixtures + corpus.json (gerador com --check). Testes: tests/test_damaged_corpus.py (3). Suíte 654/654. Aceitação S12-01-3/4; execução limpa 77/77.
- CI 39514692788 (74f4f76) confirmou a E16: 651/651, 75/75.
- Limite registrado: edição de leitura recuperada com fim reconstruído usa o leitor não estrito do original e pode recusar.
- Próximo: E18 (corpus de criptografia).


## 2026/10/20 às 20:45 (America/Sao_Paulo, UTC-03:00) — E18 concluída — corpus de criptografia

- Código `8d106ed`: `app/pdf_crypt_compat.py` (instalado em `pdf_dependency.configure_pdf_library`) envolve `Encryption.decrypt_object/encrypt_object` do pypdf: fluxos /Type /Metadata com /EncryptMetadata false não são decifrados (o filtro /Crypt Identity é retirado em memória, com `decoded_self` para o get_data) e são regravados em claro com /Crypt Identity na cópia cifrada. Sem efeito em outros documentos.
- Corpus: 5 PDFs + corpus.json, gerador `scripts/gerar_corpus_criptografia.py` (--check). Senhas sintéticas usuario-teste/dono-teste. Permissões: imprimir só em baixa qualidade, sem copiar/modificar/montar, anotar e formulários permitidos.
- Testes: tests/test_encryption_corpus.py (4). Suíte 658/658. Aceitação S12-18-3/4; execução limpa 79/79. Módulo novo registrado (80 módulos).
- CI 39515970950 (54e440a) confirmou a E17: 654/654, 77/77.
- Próximo: E19 (ordem de leitura em duas colunas).


## 2026/10/20 às 20:54 (America/Sao_Paulo, UTC-03:00) — E19 concluída — ordem de leitura em duas colunas

- Código `8b86243`: `app/reading_order.py` (`order_lines`, `_columns`, `_gutter`, `page_lines`); `rendering.extract_page_text` usa `pdftotext -cropbox -bbox-layout` + ordem própria em vez de `-layout`. Módulo registrado (81 módulos).
- Testes: tests/test_reading_order.py (5, inclui OCR por Tesseract). Suíte 663/663. Aceitação S12-19-3/4; execução limpa 81/81.
- CI 39517128164 (22e5e08) confirmou a E18: 658/658, 79/79.
- Próximo: E20 (estudo de renderização U3D/PRC, sem implementar).


## 2026/10/20 às 21:01 (America/Sao_Paulo, UTC-03:00) — E20 concluída — estudo U3D/PRC; bloco E16–E20 concluído

- Documento `docs/ESTUDO-3D-U3D-PRC.md` (commit cdef750): ponto de partida, requisitos (decodificar, desenhar, interagir, isolar), tabela de bibliotecas com licença e situação, caminhos A/B/C, tamanho estimado (B não medido), proposta e decisões D-3D-1..3, fontes consultadas em 20/10/2026. Decisão D04 registrada como pendente na lista de etapas.
- CI 39518058286 (d9e0b99) confirmou a E19: 663/663, 81/81.
- Bloco E16–E20 concluído conforme a retomada das 20:10. E29 (403 de release) resolvida na causa; prova final fica para a 0.1.18. Parado, aguardando o usuário.


## 2026/10/20 às 21:20 (America/Sao_Paulo, UTC-03:00) — 3D adiado (D04) e revisão de pendências

- Pedido do usuário às 21:18: deixar o 3D para atualização futura e guardar tudo o que se sabe. `docs/ESTUDO-3D-U3D-PRC.md` ganhou a seção "Guia para a implementação futura" (recursos do Foxit e evidência estática do plugin U3DBrowser.fpi/Direct3D 11, chaves PDF de 3D, blocos U3D, estrutura PRC, glTF, arquitetura proposta com worker `model3d-load`, limites, corpus e testes, código atual e esforço). D04 decidida; `layers-media/3d` com next_package future_update_3d; especificação e ESCOPO atualizados.
- Revisão de pendências: E29 (prova na 0.1.18), E12–E19 ainda fora de pacote publicado, E21/E22 (PC), E23 (equipamentos), E24 (VM), limites registrados de E15/E17/E19.


## 2026/10/20 às 22:09 (America/Sao_Paulo, UTC-03:00) — E29 exclusiva: causa conferida na documentação oficial

- Instrução do usuário às 22:06: até segunda ordem, só descobrir e resolver o erro da E29.
- Documentação oficial de Create a release confirma: alvo que adiciona/altera `.github/workflows/` em relação à branch padrão exige Workflows (write); GITHUB_TOKEN não pode recebê-la; resposta 404 ou 403. Coerente com o recibo do Codex (201/201/403, cabeçalho `contents=write; contents=write,workflows=write`).
- Candidato 0.1.18: b60b6e6 e 3871138 com árvore de workflows 59487bae… igual à main. CI 39522091373 falhou só no sandbox (pdftoppm ausente, OCR exato); corrigido em 3871138; CI 39524293929 em execução. Detalhes em docs/PRIORIDADE-E29-ERRO-403-RELEASE.md.


## 2026/10/20 às 22:38 (America/Sao_Paulo, UTC-03:00) — E29: candidato 0.1.18 aprovado

- CI 39526036575 (linux-flatpak.yml) em `2b49d68`: fonte/payload/sandbox 664/664 sem pulos, smoke 5/5, launcher 3/3, 183 arquivos fonte=pacote, runtime 3684/483 ELF/297 pacotes. Artefato 12313559782 (ZIP SHA-256 acab6423…5740). Bundle `LinuxitPDF-0.1.18-x86_64.flatpak` 118440408 bytes, SHA-256 058ebbe0ceb0904abe86e5ad2eaadef4540e42a51028341c2cd70d735ce1b985.
- Montagens anteriores: 39522091373 (b60b6e6, pdftoppm ausente no sandbox e OCR exato) e 39524293929 (3871138, OCR com grafia diferente) — só testes ajustados.
- Aceitação limpa 81/81 em 2b49d68 (`execucao-ubuntu24-e29-0.1.18.json`).
- Registros: testes/resultados/0.1.18/, releases/manifest-0.1.18.json, runtime-packages/source-access-0.1.18, notes-0.1.18.md. manifest.json e SHA256SUMS seguem em 0.1.17 até a publicação.
- Árvore de workflows do candidato e da main: 59487bae5b42163c1ccc68e0dc04218f5fd564b6.


## 2026/10/20 às 22:38 (America/Sao_Paulo, UTC-03:00) — E29: plano create_release confirmado

- publish-devel-release.yml em modo check_only (execução 39528468258, main c801404): plano `create_release`, target 2b49d68, árvores de workflow alvo/main 59487bae5b42163c1ccc68e0dc04218f5fd564b6, tag inexistente. Artefato 12314111055 (ZIP c5d03b68…b1f1); plano em testes/resultados/e29-release-403/release-plan-39528468258.json. Download/criação pulados de propósito.
- Aguardando confirmação do usuário para a publicação real (conteúdo público).


## 2026/10/20 às 23:09 (America/Sao_Paulo, UTC-03:00) — E29 concluída — 0.1.18 publicada automaticamente

- Publicação: execução 39531093804 (publish-devel-release.yml, check_only=false, main c0e0545) com GITHUB_TOKEN: release 419065220 `v0.1.18-devel` (prerelease, autor github-actions[bot]), tag → 2b49d686483989da00efd2aeeaf7512102a90508, asset 661077599 (118440408 bytes, digest sha256:058ebbe0…b985). Confirmação do usuário às 23:05.
- Download público sem login: HTTP 200, mesmo tamanho e hash. `releases/manifest.json` = 0.1.18; SHA256SUMS com a linha nova.
- Auditoria 39531197763: 11 controles, smoke 5/5, GTK 3, 183 arquivos, runtime 3684/483 ELF/297 pacotes (testes/resultados/0.1.18/audit/). Desktop 39531200040: 9/9 × 2 (testes/resultados/0.1.18/desktop/).
- E29 concluída. Instrução de foco exclusivo cumprida; aguardando o usuário.


## 2026/10/20 às 23:16 (America/Sao_Paulo, UTC-03:00) — Windows nativo reconferido

- windows-native.yml (execução 39531850858, 2d4d442, Windows Server 2022 + MSYS2 UCRT64): 5/5 (informação Poppler, geometria de caracteres, página renderizada no leitor real, cópia editada reabre, original preservado). Relatório em testes/resultados/windows-native/2026-10-20/. Não há instalador Windows nem suíte completa no Windows; impressão física não testada.


## 2026/10/20 às 23:25 (America/Sao_Paulo, UTC-03:00) — Medição de progresso conferida (sem mudança de código)

- Índice oficial recalculado de progresso/progresso.json (soma por etapa de weight_percent × peso concluído / peso total): 45,13%. Igual ao valor gravado; 39/58 critérios concluídos, 13 parciais e 6 pendentes. Nenhum critério fechou com E14–E20/E29, então progresso.json não foi alterado.
- Pontos abertos por bloco: análise do Foxit (etapas 3,5,7,8,9) ≈24; observação/comparação (10,11,18,19) ≈13; implementação (15,16) ≈9; especificação/auditoria (12,21) ≈4,5.
- implementation_completion_percent continua null (sem medida confiável). Indicadores auxiliares: etapas pequenas 25/29, operações 104/116, paridade 0/25, testes 664/664 ×3, aceitação 81/81.
- Próximo: aguardar o usuário. Pendentes: E21–E22 (PC), E23 (equipamentos), E24 (VM, só com autorização).


## 2026/10/21 às 20:24 (America/Sao_Paulo, UTC-03:00) — E22 concluída — provedor do índice de busca (análise estática na nuvem)

- Ambiente: FoxitPDFReader.exe (90208c9e…b3a6) e fxLuceneLib.dll (20908415…82e1) copiados de A:\Programas\Foxit PDF Reader; Ghidra 12.1.4 (rev 8b6bbb85) montado em /home/claude/tools a partir de A:\Programas\ghidra_12.1.4_PUBLIC (Framework, Base, Decompiler linux, Microsoft*, PDB, x86 com .sinc); OpenJDK 21.0.12; seeds do REA 6.7.0. Duas tentativas falharam antes da importação (.sla mais antigos que .slaspec; .sinc ausentes) e ficaram preservadas em analysis-local.
- Rodadas: static-search-provider-2026-10-21 (0x172a2e0, 0x1728ab0, 0x1728850, 0x1770e90, 0x1776070, 0x175eb50: 901 instr/3.292 bytes) e static-search-provider-owner-2026-10-21 (0x1726b90: 227/700). check_foxit_machine aprovado; catalog_foxit_headless + catalog_foxit_functions: 336 entradas (152 REA, 184 diretas).
- Novo scripts/check_search_provider_joins.py: relê os binários pelos hashes e confere strings/imports/exports/RTTI/instruções da cadeia; saída testes/resultados/static-search-provider-2026-10-21/structural-joins.json (all_expected_facts_present=true).
- progresso.json: evidência e nota acrescentadas aos 8 critérios abertos das etapas 3/5/7/8/9 que citavam a continuação de 18/10; status/pesos sem mudança; update_progress.py → 45,13%. progresso.md regenerado (estava em 0.1.15/323).
- Próximos recortes: chamadores de 0x1770e90; classe/laço da thread +0x1e3c; campos +3/+6/+7/+0xc/+0x10 e 0x1003f6b0; contexto 0x138; arrays do reflow. Para repetir na nuvem, recopiar os arquivos do PC (o contêiner é temporário).
- Suíte própria: 664/664 na fonte Linux (Ubuntu 24.04), sem alteração no aplicativo.


## 2026/10/21 às 21:05 (America/Sao_Paulo, UTC-03:00) — E24 concluída — comparação com o Foxit retomada na VM

- VM: snapshot 01-linuxit-configurado-offline, ligada pelo usuário; sessão desktop-hui8ndv\ia machine; controle por computer use (VirtualBoxVM liberado), teclado do host não chega ao convidado e o clipboard está desligado, então comandos via Teclado Virtual do Windows convidado (mapa de teclas em /home/claude/work-vm/osk2.py, temporário).
- Preflight PowerShell: get-filehash reference/input (hash 90208c9e… e 10 entradas iguais ao P03 0930), get-netadapter Disconnected, ps foxit* vazio, sem SMB. Postflight: entradas iguais; FoxitPDFReader PID 1220 ativo 2,5 min após fechar a janela (CPU 52,5 s constante), não encerrado.
- Observações e comparação: testes/resultados/vm-2026-10-21-e24/observations.json; 26 capturas privadas em analysis-local/vm-20261021-e24 (hashes no JSON).
- Divergências a decidir: ordem dos resultados (Foxit: marcadores, texto, comentário) e navegação do resultado de marcador (Foxit não navega; Linuxit navega via _select_search_hit). Código não alterado.
- progresso.json: evidência nos 4 critérios parciais das etapas 10, 11 e 18; status/pesos sem mudança; 45,13%. Nova etapa E30 para continuar.
- Suíte própria 664/664.


## 2026/10/21 às 21:29 (America/Sao_Paulo, UTC-03:00) — E31 concluída — busca na ordem do Foxit e clique em marcador sem mudar de página (D05)

- Código: search_engine.TextSearchIndex.search reordenado (marcadores → texto → comentários → anexos) com _metadata_hits(kinds=...); on_notice dos painéis enviado uma vez. main._select_search_hit não chama goto_page para source=bookmark.
- Testes: test_search_scopes (ordem e limite max_hits=4 agora bookmark+3 textos; GUI renomeado para test_ui_toggles_scopes_and_bookmark_result_keeps_page) e novo tests/test_search_foxit_order_gtk.py (2). Especificação e contratos atualizados; operação search-bookmarks/destinations reescrita; refresh_operation_pins --accept nas 6 operações de busca.
- Aceitação: casos_gtk S12-05-1 ajustado; execução limpa e31 81/81 na revisão ac89254.
- Processo residual do Foxit (PID 1220) segue na VM; não encerrado. Pedido ao usuário: autorização para encerrá-lo no início da E30.


## 2026/10/21 às 21:36 (America/Sao_Paulo, UTC-03:00) — D06 e passagem para o Codex

- D06: usuário autorizou encerrar o processo residual FoxitPDFReader na VM no início da E30 e entre casos (registrar PID e horário).
- Novo docs/RETOMADA-2026-10-21.md; AGENTS.md e docs/RETOMADA.md apontam para ele no topo (avisos da E29 marcados como históricos).
- Plano de subida do índice registrado no aviso de 2026/10/21 às 21:36 em AVISOS-E-STATUS.md (critérios mais próximos ≈14 pontos).


## 2026/10/21 às 21:57 (America/Sao_Paulo, UTC-03:00) — CI da E31 aprovado

- 39700044694 falhou (campanha preservada 16/17: plano-comparativo C18-D10 esperava texto primeiro) → expectativa reordenada (19dd72a).
- 39701199175 falhou só na fumaça GTK (smoke_linuxit esperava navegação ao resultado de marcador) → fumaça ajustada a D05.
- 39702160473 aprovado em b75c8d6. check_intermediate linux local: 666 testes, fumaça 5/5.


## 2026/10/22 às 00:00 (America/Sao_Paulo, UTC-03:00) — E21 concluída — REA 6.7.0 no PC do usuário

- Log no PC: analysis-local/rea-instalacao/instalacao-rea-20261021-235457.log (fora do Git); resumo sanitizado em testes/resultados/e21-rea-pc/review.json com SHA-256 do log.
- Doctor Ghidra: 10 checagens ok; environment_healthy=false por Hopper/IDA/JADX/Kuna ausentes e registros desatualizados (antigravity pedia 6.5.0; claude_code, claude_desktop, codex, gemini_cli e vscode sem registro) antes do rea setup.
- Passo 6 (rea setup --client codex --client claude_desktop) pendente na janela no momento da conferência; depois dele, reiniciar o Codex. Se o registro do app Claude for refeito, fechar o app por completo antes (o app aberto pode regravar a configuração).


## 2026/10/22 às 00:29 (America/Sao_Paulo, UTC-03:00) — E21: registro no Codex não aplicado

- Log instalacao-rea-20261021-235457.log sem mudança após a janela (16760 bytes; termina no doctor). ~/.codex/config.toml (mtime 21/10 17:30) sem [mcp_servers.rea]; lido só para conferir e cópia temporária apagada.
- Instalação 6.7.0 e doctor Ghidra continuam válidos (E21 concluída pelo critério da etapa). Registro no Codex pendente: rodar instalar-rea.cmd de novo (S para Codex, N para app Claude) ou `rea setup --client codex` no PC, depois reiniciar o Codex.

## 2026/10/22 às 00:43 (America/Sao_Paulo, UTC-03:00) — integração REA no Codex aplicada e testada

Pedido explícito do usuário: configurar conexão e explicar capacidades. Plano dry-run inspecionado; rea setup --client codex --yes aplicado somente a Codex/skill empacotada. Configuração anterior com backup/hash e demais chaves preservadas; não alterados outros agentes/approvals. Node24.22.0, REA6.7.0, Ghidra12.1.4 e JDK21.0.12.1; doctor escopo Codex/Ghidra healthy=true e registro aligned. Cliente stdio temporário próprio iniciou o comando configurado, initialize/protocolo2025-11-25, tools/list207 e binary_session passaram; servidor confirmou versões/catálogo. Nenhum alvo aberto ou original executado; VM intocada. Perfil Ghidra Windows anuncia inspeção estática e recusa mutações de banco; catálogo amplo não significa todos207 recursos disponíveis. Guia docs/REA-CODEX-CONFIGURACAO-2026-10-22.md e recibo testes/resultados/e21-rea-pc/codex-registration-2026-10-22.json, evidências integrais ignoradas em analysis-local/rea-instalacao/. Configuração privada não versionada. Skill OpenAI Docs e skill instalada do REA consultadas para conexão. Git sincronizado primeiro de24d45aa a1daa5d2, preservando as novas entregas/VM/estática das outras IAs. E29 não reaberta, sem incremento de critérios/testes de app. Próximo passo: usuário reiniciar Codex; conferir binary_session no catálogo real e então retomar apenas trabalho autorizado da fila. Não declarar o chat conectado só pelo doctor ou smoke independente. Commit/push e remoto a confirmar no fim desta rodada.


## 2026/10/22 às 00:45 (America/Sao_Paulo, UTC-03:00) — REA no Codex confirmado; lista compartilhada

- Conferido: ~/.codex/config.toml modificado às 00:39 com [mcp_servers.rea] (node + rea.mjs mcp, GHIDRA_INSTALL_DIR e JAVA_HOME); codex-doctor-20261022.json com registration:codex ok/aligned; segundo log de instalação às 00:35 (6.7.0, Ghidra saudável). Corrige a nota anterior (registro ausente às 00:28).
- Nova lista docs/O-QUE-FAZER-AGORA-2026-10-22.md (A1–A6 sem o usuário; B1–B3 com o usuário), apontada no topo de AGENTS.md, docs/RETOMADA.md e RETOMADA-2026-10-21.
- Antes de pegar uma tarefa, registrar aqui quem a assumiu (Claude ou Codex).


## 2026/10/22 às 08:25 (America/Sao_Paulo, UTC-03:00) — Claude assumiu A1, A2 e A3

- Pedido do usuário: fazer A1 (fluxo de busca), A2 (fluxo de impressão) e A3 (diagramas por subsistema) da lista O-QUE-FAZER-AGORA-2026-10-22. Codex: não pegar essas três; A4–A6 continuam livres.

## 2026/10/22 às 08:28 (America/Sao_Paulo, UTC-03:00) — Codex assume A4, A5 e A6

Pedido explícito do usuário autoriza este bloco de três tarefas. Codex assume contratos A4 nas25 famílias/116 operações, candidato0.1.19 A5 com E31 sem publicar release, e desenvolvimento próprio A6. Trabalho dividido em contratos, formulários e assinaturas com agentes auxiliares locais; coordenação/integracao, redação/OCR/conversões/Windows e pacote pelo principal. Não alterar pesos nem presumir que subconjunto fecha família universal. Não executar original ou VM, manter IA/nuvem direta/3D fora conforme decisões. Preparar contratos por operação e recursos concretos verificáveis; publicação da release somente após OK separado. Sincronizado4338ade. Ressalvas: A6 é frente ampla com recursos universais ainda abertos; resultados serão discriminados por recurso e validação, sem declarar completude só por percorrer a lista.

## 2026/10/22 às 08:37 (America/Sao_Paulo, UTC-03:00) — A1, A2 e A3 concluídas (Claude)

- Rodada Ghidra static-search-print-flow-2026-10-22: 7 entradas (0x1770920, 0x1770a60, 0x17be860, 0x17c6d60, 0x17be500, 0x1645710, 0x165c230), 454 instr/1850 bytes, machine-check ok, catálogo 336->343.
- A1 busca: cadeia acessor 0x17c6d60 -> módulo 0x17be860 (0x2118) -> CFindToolDlgAdv 0x1758c70 -> diálogo 0x1770e90 -> provedor +0x1e48. Thread de limpeza: início 0x1770920, proc 0x1770a60 = CFindToolDlgAdv::ClearDataFindThreadProc (log embutido), evento +0x1e40 (CreateEventW/ResetEvent/SetEvent), CS +0x204c, vetor de resultados +0x2038/+0x203c. Corrige E24: a thread esperada no destrutor é a de limpeza, não 'de busca'. Gap: algoritmo 0x1003f6b0.
- A2 impressão: RTTI CReader_PrintMgrEx (vtable 0x53d6bfc), CReader_BasePrinter (0x53d7788) e subclasses Dlg/Quiet/Batch/Invoice; CReader_PrintProviderEx; CGdiPrinterDriver vs CFX_PSPrinterDriver; CPDF_BackgroundDrawer (0x54151a0). Ctors 0x1645710/0x165c230 conferidos. Gap: laço de impressão/DEVMODE/spooler e contexto 0x138.
- A3: tabela de diagramas por subsistema em docs/fluxos.md; Mermaid de busca e impressão nos dois documentos.
- Critérios (etapas 8 busca, 8 impressão, 9 diagramas) com evidência nova, status parcial mantido; 45,13%. Sem mudança de código; suíte 666/666 preservada. Commit 38dde0a.

## 2026/10/22 às 12:07 (America/Sao_Paulo, UTC-03:00) — Claude deixa a ordem para o Codex

Pedido do usuário (12:04): ordem minuciosa para o Codex continuar e lista de todo o restante. Documento: `docs/ORDEM-CODEX-2026-10-22.md`, apontado no topo do `AGENTS.md` e da lista O-QUE-FAZER.
- Conferência na pasta do PC, só leitura (listagem e cópia de 4 documentos do Codex para a nuvem): trabalho A4/A5/A6 com horários de 08:30 a 08:48 em app/, tests/, scripts/, docs/ (A4-CONTRATOS-OPERACIONAIS, A456-EXECUCAO, A6-ASSINATURAS-PRESERVACAO, A6-FORMULARIOS-E-WINDOWS) e analysis-local/ (a6-js-01 10/10, a6-xfa-01 9/9, a6-form-regression 19+1 GTK não executado, a6-xfa-regression 15/15). Nenhum commit depois de b79aca7; a cópia do PC também não tem 32fc157/bd2eeb4.
- Ordem: (1) ramo de segurança codex-a456-wip + rebase sobre bd2eeb4, mantendo as notas dos dois; (2) proveniência QuickJS-NG, annotation_editing sem documento, OCR no Flatpak, verificadores; (3) commits temáticos, main, CI no-vm-validation, GTK reais; (4) A4 como evidência, critério continua parcial sem B3; (5) 0.1.19 com workflows iguais à main, linux-flatpak, check_only, parar para confirmação; (6) A6 item por item; (7) E32/E33/E34 e registros.
- Lista restante: 19 critérios (54,87 pontos), estática S1–S4, B1/B2/B3, adiados. Nenhum código alterado pelo Claude nesta rodada; .gitignore passa a ignorar O-QUE-FAZER-AGORA-LOCAL.md e ORDEM-CODEX-LOCAL.md (cópias da raiz do PC).

## 2026/10/22 às 18:47 (America/Sao_Paulo, UTC-03:00) — S1 não concluída pelo Claude

Pedido do usuário: fazer a S1. O Claude conferiu o hash da fxLuceneLib.dll (20908415…82e1) e começou o levantamento, mas a análise foi interrompida antes de produzir resultado. Nenhuma semente, catálogo, critério ou código foi alterado. S1 continua aberta e livre na ORDEM-CODEX-2026-10-22 (Parte 3.2). O Codex não deve contar a S1 como feita.

## 2026/10/22 às 18:51 (America/Sao_Paulo, UTC-03:00) — A4–A6: Passo 1 salvo; aguardar confirmação

Pedido atual do usuário: buscar atualizações do Claude, executar em ordem e sempre perguntar antes de passar ao próximo passo, começando por A4/A5/A6. Lidos ORDEM-CODEX-2026-10-22.md e os commits até e215a6b. Integração por merge preservou o histórico e as notas de ambas as IAs. O commit local cabe2f0 já existia antes da leitura da nova ordem; não reescrito para simular commits temáticos. Nenhum push desse trabalho para main ocorreu. Destino de segurança: codex/a456-wip, com prefixo de ramo do Codex.

Atualização do Claude às18:47: S1 não concluída e livre; levantamento interrompido sem resultado novo. A1/A2/A3 anteriores significam recortes estáticos/diagramas, não critérios amplos concluídos. S1–S4 seguem abertos conforme a ordem. Índice/paridade sem mudança nesta rodada.

Backup A4/A6 inclui os módulos, testes, scripts, workflows e documentos próprios; arquivos em analysis-local, caches e originais permanecem ignorados. Restos de annotation_editing.py/annotation_geometry.py são WIP preservado, ainda sem integração/testes finais: não contar como edição universal entregue. A4 tem 116 contratos/25 famílias e validação local preservada; isso não fecha o critério amplo12. A5 tem fonte0.1.19 preparada, mas nenhum Flatpak0.1.19 gerado/aprovado/publicado. A6 permanece parcial: os testes portáveis preservados não substituem Linux/GTK/Flatpak/Windows.

Lacunas concretas do Passo2: conversion_window usa runner.close inexistente (usar shutdown), captura hash ao executar em vez de ao abrir e precisa proteger ciclo de vida/identidade; corrigir antes de CI. Rever leitura limitada do backend de conversão. Finalizar/testar integração de anotações, registrar proveniência/hash fixo QuickJS e conferir catálogo/arquitetura/contratos. Há validação de arquitetura anterior, não é aprovação da suíte. Nenhuma nova execução de suíte completa, aceitação, CI, original ou VM neste Passo1. Nenhuma release criada/apagada, nenhuma alteração de segurança do host.

Próximo passo, somente após resposta do usuário: Passo2 da ORDEM-CODEX (fechar lacunas e verificadores). Depois pedir autorização para Passo3 (main/CI); candidato e publicação têm suas próprias paradas. Conferir recibo local analysis-local/a456-step1-sync.json para SHA e igualdade remota após push.

## 2026/10/22 às 19:16 (America/Sao_Paulo, UTC-03:00) — Passos2 e3 de A4–A6 executados; aguardar Passo4

Usuário autorizou explicitamente os dois próximos passos após o backup. Passo2: corrigidos identidade/leitura limitada/lifecycle GTK da conversão; anotações receberam validação de relações e correção que preserva AP gráfica de carimbos e limpaRC conflitante; seis testes novos, sem chamar edição universal. Fonte e wheel QuickJS fixados por SHA/tamanho, baixados/conferidos; instalação Linux offline do wheel local, avisos/proveniência na receita e auditor. Revisados pins alterados de _apply/redação/OCR/confiança, preservando estados/contagens de operações. Catálogo116/25, arquitetura91 módulos e contratos116/95 símbolos passaram. A prova de OCR no Flatpak instalado depende do futuro Passo5; não foi substituída pela aprovação em fonte.

Passo3: CI39861626936/65cd8d2 teve740/741, um teste GTK desatualizado que pegava o primeiro ComboBox após a adição do método vetorial. Corrigida seleção pelo nome acessível; novo teste do vetor e DPI desabilitado. CI39862477446/e02dda2 aprovado:742/742 próprios, zero falhas/erros/skips;81/81 aceitações em árvore limpa, campanha17/17, fumaça5/5, AT-SPI entre processos, portal nativo e filaCUPS aprovados. Dos novos recortes:3/3 GTKformulários,9/9 preservação comOpenSSL,10/10 JS,9/9 XFA,3/3 limpezaOCR (inclui ferramenta real eng/por+eng),5/5 conversões,6/6 topologia e1 GTKconversão. Conferidos193 arquivosapp iguais à fonte testada. ZIP principal760632bytes/SHA4c11176a…6a2f5 e CUPS1066bytes/SHAb444bc1a…03446 iguais aos digests do GitHub. Relatórios integrais e primeira falha em testes/resultados/a456-passos-2-3-2026-10-22/; revisão review.json e docs/PASSOS-2-3-A456-2026-10-22.md.

Windows local: tentativa completa saiu1 antes de relatório final; log parcial preservado por hash, causa da interrupção não confirmada. Não atribuir a tokens nem ao Foxit. Focados confirmaram Cairo ausente (import/serviço de AP) e OpenSSL indisponível. Primeiro focoDSS omitiu caminhoASN.1 na configuração do diagnóstico; resultado mantido e repetição corrigida confirmou faltaOpenSSL. Não há aprovação Windows/instalador. Não instalar dependências nativas nem alterar segurança do host para esconder limitações.

Atualização do catálogo aponta nova evidência própria742, sem promover estados das116 operações nem critérios/pesos; histórico anterior preservado. Não executados Passos4–7, VM, original, Flatpak novo ou publicação de Release. A4 conhecida preparada, A6 parcial e A5 aguarda montagem/validação. Main e ramo de segurança serão sincronizados; comprovante local analysis-local/a456-step23-sync.json. Próximo: pedir confirmação antes do Passo4 (evidências A4 mantendo critério parcial, sem decidirB3 pelo usuário).

## 2026/10/22 às 19:19 (America/Sao_Paulo, UTC-03:00) — usuário autoriza os próximos três passos4,5,6

Passos2/3 salvos no commit5abbb4a e sincronizados em main/ramo de segurança; fonte742/742, aceitação81/81 e193 arquivosapp/98testes conferidos. Pedido novo: "depois ja faça as proximas3 etapas". Codex assume Passos4–6 da ORDEM-CODEX: anexar evidências A4 mantendopartial/45,13%, construir/testar candidato0.1.19 e fazer preflight check_only, conferir A6 por item incluindo primeira tentativa real Windows. Sem autorizar release, decisãoB3, VM ou Passo7. Passo4 registra116 contratos e relatórioA4/CI como evidência técnica; pesos/status não alterados. Próximo: CIFlatpak e Windows; preservar falhas e não chamar recortes universais de completos.

## 2026/10/22 às 19:36 (America/Sao_Paulo, UTC-03:00) — checkpoint dos Passos4–6 em execução

Passo4 concluído como registro de evidências, mantendo o critérioA4partial e índice45,13%. Windows39864184215/eb11a41 falhou por três headers omitidos no sdistQuickJS; correção51ade8e usa commit oficialfd0a0210b7be00957751871e7e01b8291268fc29, três fontes/opcodes conferidos idênticos, headers suplementares fixados por hash/tamanho. Nova tentativa39864966247: compilação e probe inicial aprovados; suíte inteira em execução, instalador ainda não confirmado. Não confundir com Windows completo.

Primeiro candidatoLinux39864192306 foi cancelado/substituído após revisão do Python isolado paraJS: -I ignoravaPYTHONHOME; ajuste7f0f9c1 usa loader/bibliotecas/stdlib pareados no pacote e -I no host. NovoCI39864579949 testa fonte/payload/sandbox; resultados pendentes. Workflows tree df2e143226f31343781b1598f3bcf6b6e8dae5e7 igual àmain. Fonte e02dda2 aprovada anteriormente não é prova automática desse ajuste. MatrizA6 em docs/PASSOS-4-6-A456-2026-10-22.md; notas0.1.19 preparadas, sem manifesto novo até aprovação do bundle. Publicação continua sem autorização, sem tag/release criada, sem VM/original.

## 2026/10/22 às 19:58 (America/Sao_Paulo, UTC-03:00) — candidato0.1.19 aprovado e baixado, sem publicação

CI39864579949/7f0f9c1 aprovado:742/742 em cada fonte/payload/sandbox, zero erros/falhas/skips; fumaça5/5, launcher3/3,193 arquivosapp iguais àfonte local,3686runtime/485ELF atribuídos pelo construtor. OCRcontraste/limiar e modeloseng/por+eng passaram nos três ambientes. ZIPartefato12463863765/121615759bytes/SHAac24a04c…fa7d0 confereGitHub; bundle120445752bytes/SHAf1ac2636…9723d conferido local. Relatórios emtestes/resultados/0.1.19/ e manifesto/notes0.1.19 preparados. Manifesto global/SHA256SUMS/releases anteriores preservados. Próximo:check_only verdadeiro, sem publicar.

Windows: tentativa39864966247 cancelada após cerca19min na suíte sem checkpoints, sem resultado final aprovado. Ramo separado codex/windows-installer-diagnostics,53d4247, acrescentou checkpoints atômicos não aprovadores (dois controles2/2), tempo limitado e prova do instalador/exe antes da suíte. CI39867476955 falhou na atribuição de cachegdk gerado;4f9a6f0 registra grupos de caches por gerador/inputs/pacotes/hash, remove cachepixbuf que é refeito após relocação e recusadesconhecidos (três controles3/3). CI39868278905 em execução. Não incorporar workflows desse ramo àmain antes da publicação do candidatoLinux: árvoredf2e143226f31343781b1598f3bcf6b6e8dae5e7 do candidato continua igual àmain. App193 arquivos são os mesmos; ferramentas/workflows de diagnóstico diferem e têm revisão separada. Nada instalado no host, sem VM/original.

## 2026/10/22 às 20:29 (America/Sao_Paulo, UTC-03:00) — correção de identidade da redação; candidato anterior substituído

A revisão9fb4f3a fixa o hash exibido pelo editor antes do diálogo de destino. Antes, a redação podia aceitar um PDF substituído externamente durante o diálogo. Controle com o método antigo/próprio e worker vetorial real criou saída; o novo recusou sem saída (UI simulada, não Foxit). Regressão GTK real passou na fonte Linux: CI39869853238,744/744 e aceitação81/81 limpa na mesma revisão. Evidências emtestes/resultados/a456-identity-fix-2026-10-22/.

CI do novo Flatpak39869848800 terminou com sucesso; artefato12467036137 em download para exame/hash local. O antigo candidato7f0f9c1 foi marcado superseded_pending_identity_fix e a guarda de publicação passou9/9 testes; não publicar aquele bundle nem usar o preflight39868718314 como aprovação do novo. Releases/tags não criadas; manifesto global0.1.18 preservado.

Windows no ramo codex/windows-installer-diagnostics:350ae12 gerou o instalador NSIS; a instalação retornou zero mas não entregou o manifesto no destino pedido.459f618 normaliza o argumentoNSIS para barras nativas, mantendo espaços/Unicode, e aguarda a conclusão; seis controles locais passaram. CI39871829847 repete instalação. Todos os testes são no runner efêmero, nada instalado no host e VM/original intactos.

## 2026/10/22 às 20:37 (America/Sao_Paulo, UTC-03:00) — Passos4–6 conferidos, versão retida

**Atualização — 2026/10/22 às 20:37 (America/Sao_Paulo, UTC-03:00):** Passos4–6 executados: A4 registrada sem alterar critérios; candidato0.1.19/9fb4f3a validado744/744 em fonte/payload/Flatpak e aceitação81/81. Publicação retida; Windows e limites A6 no relatório. Passo7 aguarda instrução. Sem VM/B3; checklist45,13%, paridade0/25 e global indeterminado.

Bundle120445160bytes/SHAea5d76eb3ba779f38477652a5794c309e8ad1ae7197dcd1ab3392c1e35d9818e; artefato12467036137/digestb8729532…cf0a3 conferido. Relatórios emtestes/resultados/0.1.19/. QuickJS UCRT64 compilado e probe nativo5/5 aprovado; instalador NSIS gerado (105.925.705bytes). A instalação retorna0, mas o manifesto não aparece no destino com espaços/Unicode mesmo após a correção de separadores e espera90s. Suíte completa e aceitação foram puladas após essa falha; desinstalação/probe do aplicativo instalado não aprovados. A causa do destino real ainda não foi determinada.

Workflows Windows permanecem no ramo separado; main/candidato têm árvoredf2e143226f31343781b1598f3bcf6b6e8dae5e7. Manifesto global0.1.18 preservado. Após autorização da publicação: publicar os mesmos bytes e fonte, conferir download público, auditoria independente e integrações do desktop. Não confundir registro dos resultados com autorização para executar original ou mudarB3.

## 2026/10/22 às 20:49 (America/Sao_Paulo, UTC-03:00) — Codex atualiza coordenação, registraPasso7 e assumeS1

Usuário pediu atualizar o local de informações usado pelas duas IAs e continuar os dois próximos trabalhos. Fetch confirmou origin/main7558bce sem commits novos do Claude. A ordem termina noPasso7: registreiE32/A4 eE33/candidato como concluídos apenas no contrato delimitado;E34/A6 em andamento com nove subitens e Windows parcial. O segundo trabalho éS1, primeira frente técnica seguinte elegível semVM; esta interpretação foi avisada ao usuário. Publicação/B3 não inferidas.

AtualizadosAGENTS,RETOMADA,ORDEM,O-QUE-FAZER,avisos e fila de pendências. A fila antiga de19/10 foi identificada como histórica. S1 assumida porCodex antes de iniciar, para evitar duplicidade comClaude. Consultar catálogo343 antes de escolher sementes e reutilizar pseudocódigo/projetos preservados. REA não aparece entre ferramentasMCP desta sessão; usar backendGhidra direto disponível, distinguindo-o de EvidenceMCP. Não reparar registros alinhados nem instalar ferramentas para isso.

## 2026/10/22 às 21:00 (America/Sao_Paulo, UTC-03:00) — Codex: segundo trabalho autorizado, loteS1 encerrado e lacunas preservadas

Passo7 foi registrado e publicado em2c96d64 antes da análise. E32/A4 eE33/candidato delimitado concluídos;E34 parcial com nove subitens e Windows pendente. Atualizados os locais comuns de informação (AGENTS,RETOMADA,ORDEM,O-QUE-FAZER,avisos,fila e cópias locais), preservando a situação anterior como histórico.

S1: hash dafxLuceneLib.dll20908415…c82e1 conferido antes/depois; cópia do projeto antigo, Ghidra12.1.4/JDK21 e scriptREA6.7.0, perfil direto-noanalysis, sem EvidenceMCP nem execução do original. Sete sementes inéditas:10032410,10032260,100321c0,10026860,10024d90,100216c0,10041fd0. Todas decompiladas sem mensagem;1593 instruções/5278 bytes conferidos comCapstone5.0.6/pefile2024.8.26. Metadados e catálogo publicados;350 entradas distintas (152REA+198diretas). Brutos emanalysis-local/headless/s1-query-pipeline-2026-10-22/; relatório e matriz de lacunas emdocs/REA-S1-CONSULTA-E-CANCELAMENTO-2026-10-22.md.

Achados: byte+5 controla chamadaSnowball;+6/+7 alimentamUnicodeDeals mas sem contrato integral; curingasASCII/fullwidth ligados às cláusulas; um cancelamento do coordenador consulta ponteiro, chama slot+0x68, limpa contêiner e devolve-10. O pseudocódigo antigo dizia void, porém assembly retornaESI emEAX eRET0x58: não usar assinatura automática comoAPI. Não inferir que limpar esse contêiner apaga toda a lista daUI. Não relacionar sem prova os contêineresDLL aos objetosUI+0x1f34/+0x2044.

S1 permanece parcial, E35 em andamento no registro (lote encerrado, nenhum processo ativo). Próxima IA pode seguir pelos alvos ainda não catalogados; ver relatório antes de começar e anotar nova posse. App/Flatpak0.1.19, manifesto global0.1.18, árvores de workflows, critérios/pesos e paridade preservados. Publicação/B3/VM/equipamentos continuam aguardando decisões/ambientes do usuário.

## 2026/10/22 às 21:11 (America/Sao_Paulo, UTC-03:00) — Codex retoma S1 por pedido explícito do usuário

O usuário pediu “façaS1”. Retomada pelas lacunas do relatórioREA-S1-CONSULTA-E-CANCELAMENTO-2026-10-22, catálogo350. Trabalho dividido conforme a instrução de investigação paralela da habilidadeREA: coordenador naDLL/consulta/avaliação, s1_options nos campos+3/+0xc/+0x10 e origem/semântica de+6/+7, s1_ui_classes nos objetos do diálogo+0x1f34/+0x2044 e cancelamento relacionado. Cada frente preserva sementes/relatório/brutos próprios; coordenação central integra catálogo/progresso/Git. Reutilizar evidências anteriores, não contar função repetida como nova e preservar os dois primeiros lotes.

Sem execução do original/VM, sem instalação ou reparoMCP, sem publicação e sem decisãoB3. A rodada visa resolver as lacunas técnicas daS1; não fechar o critério amplo sem evidência. Antes de novos processosGhidra, coordenar consumo de memória.

## 2026/10/23 às 00:06 (America/Sao_Paulo, UTC-03:00) — Claude: verificação de status

Só leitura (git, API do GitHub, listagem da pasta do PC). main 128d6f3; releases: última v0.1.18-devel; 39872660861 check_only sem release. Windows: 53d4247/4f9a6f0/691ee0d/350ae12/459f618 falharam (instalador sem arquivos no destino). S1: pastas s1-options/s1-query-constructors/s1-ui-objects/s1-unicode no PC com última escrita 21:20 de 22/10, sem relatório nem commit — a próxima IA deve conferir esses brutos antes de repetir as sementes. Nada alterado no app, critérios ou pesos.

## 2026/10/23 às 00:11 (America/Sao_Paulo, UTC-03:00) — lista revisada e minichat

Pedido do usuário: listar de novo o que falta, separar o que o Claude pode fazer sem a S1 (C1–C7 na O-QUE-FAZER) e informar o Codex ao fazer o que ele pedir. Criado CHAT-IA.txt na raiz da pasta do PC (gitignored), com regras e 4 mensagens iniciais do Claude. AGENTS.md aponta o chat. Nenhuma tarefa C iniciada.

## 2026/10/23 às 00:20 (America/Sao_Paulo, UTC-03:00) — C1 não concluída pelo Claude

Pedido do usuário às 00:13: fazer a C1. PEGUEI às 00:14 no CHAT-IA.txt. A tarefa foi interrompida antes de produzir resultado; o arquivo parcial local foi apagado sem commit. Nenhum critério, catálogo ou código alterado. LIBEREI às 00:20 no chat. O Claude não retoma C1, S2 nem S4; livres para o Codex.

## 2026/10/23 às 00:23 (America/Sao_Paulo, UTC-03:00) — pedido ao Codex: aparecer como contribuidor

Usuário pediu que o Codex faça isso antes de concluir as próximas tarefas, quando falar com ele. Instrução no topo do AGENTS.md e da ORDEM-CODEX e no CHAT-IA.txt. Contexto: contributors API mostra airtonbp19edu 179 e claude 112; commits do Codex saem como Airtonbp19 sem trailer.

## 2026/10/23 às 00:50 (America/Sao_Paulo, UTC-03:00) — divisão de tarefas Claude × Codex

Pedido do usuário (00:44): dividir, trabalhar em paralelo, fazer tudo o possível sozinhos e com a VM; retorno Claude 05:10 e Codex 05:30, ambos na agenda. Documento docs/DIVISAO-TAREFAS-2026-10-23.md. Claude agendou o retorno (send_later trig_01GrfK51W5n3vGW23nBGZSvY, 08:10Z). Codex já confirmou coautoria (695f9bf) e PEGUEI S1 com três subfrentes às 00:29–00:37. Claude segue K1 (CI Windows 39895160350 em andamento no ramo claude/windows-installer).

## 2026/10/23 às 01:05 (America/Sao_Paulo, UTC-03:00) — divisão ajustada; chat por arquivo

Codex propôs às 00:48 ser operador exclusivo da VM; Claude aceitou. Claude não assume S2/S3/C1/S4. Claude fica com K1 (Windows), correções no app vindas da VM, K3, K4, K5. Chat: CHAT-CLAUDE.txt e CHAT-CODEX.txt, porque gravações inteiras do CHAT-IA.txt se sobrescreviam. K1: causa = ntpath do MSYS2 mantém "/" e o NSIS ignorava /D= (instalava na pasta padrão); MessageBox sem /SD travava o modo silencioso. Correção facea01, CI 39896899395.


## 2026/10/23 às 01:11 — Codex: retomada, coautoria, divisão e lote S1

- Autoria escolhida: Airtonautor + trailerCodex. Commit695f9bf enviado; API200 confirmou autoria vinculada e trailerúnico, sem nova conta na lista de contribuidores. Configuração global não recebeu chave não confirmada.
- Retomada Codex agendada23/10/2026 05:30 (automação retomar-linuxit-pdf-s-05-30); Claude informou05:10. Divisão aceita em docs/DIVISAO-TAREFAS-2026-10-23.md. Cada agente escreve só seu chat.
- Dez lotes S1:54 observações,47 entradas novas/7 revisitas,7.904 instruções/27.660 bytes. Catálogo350→397,152REA+245diretas. Recibo testes/resultados/s1-consolidado-2026-10-23/review.json; relatóriosREA-S1-AVALIACAO/OPCOES/UNICODE/OBJETOS-UI-2026-10-23.md.
- Resolvidos no recorte: campos+6/+7/+0x10, categoria Unicode e tatweel inativo, TermQuery/WildcardQuery, IndexSearcher/clearMatchTerms, CCriticalSection inline e fábricaTreeCtrl. S1 parcial: +3/+0xc, scorer/pesos/ranqueamento, proximidade integral e lifecycle ainda abertos. S3 levantou39arestas classificadas, sem declarar motores completos.
- VM: relógio avança, TaskManager respondeu, Foxit ausente; manutenção autorizada confirmou hashb20ad4...cac1 e todos coletores antigosReady (0930resultado0). Novoobservador em preparação. Sem teste diferencial novo até este registro. Operação VM exclusivaCodex; não iniciar concorrente.
- Aplicativo/workflows/releases não alterados pelo Codex. Fontecandidata9fb4f3a preservada; nenhuma alegação de percentual global ou paridade integral.
## 2026/10/23 às 01:20 (America/Sao_Paulo, UTC-03:00) — K4 proposta B3 pronta; K1 em correção

K4: docs/PROPOSTA-B3-2026-10-23.md com opções A/B/C, números do inventário (104/116 com código próprio, 0/116 comparadas, paridade 0/25) e estimativa 55-70% só com A ou C. Decisão do usuário; nada alterado. K1 instalador Windows: 2a correção (native() para barras do MSYS2) fez o makensis falhar por causa do /SD IDOK; 3a correção 0e92897 troca para IfSilent + labels, CI 39897411096. O arquivo da proposta tinha entrado por engano no commit do ramo Windows; trazido para a main aqui.

## 2026/10/23 às 01:00 (America/Sao_Paulo, UTC-03:00) — Claude assume a VM se o Codex não concluir

Pedido do usuário (00:57). Gatilhos: LIBEREI/BLOQUEADO no CHAT-CODEX.txt, ou mais de 60 min sem linha nova nem commit com a E30 pendente; PERGUNTA e até 15 min de espera se o Codex parecer ativo; PEGUEI E30 antes de abrir a VM. Retomada das 05:10 recriada com a checagem (trig_01NLQKhk6cuVpQByFPnfnfEZ; o antigo trig_01GrfK51W5n3vGW23nBGZSvY foi apagado).

## 2026/10/23 às 01:05 (America/Sao_Paulo, UTC-03:00) — sinal de vida da VM

Pedido do usuário (00:58). Codex: commit vazio forçado em codex/vm-status a cada 15 min ou caso concluído, "VM-STATUS: ATIVO|LIBEREI|BLOQUEADO|CONCLUIDO | caso | resumo". Claude: vigia em segundo plano (gh api a cada 120 s) que sai em LIBEREI/BLOQUEADO, CONCLUIDO, sinal parado > 45 min ou ramo ausente por 45 min; rearmar a cada 2 h e na retomada das 05:10.

## 2026/10/23 às 01:58 (America/Sao_Paulo, UTC-03:00) — instalador Windows aprovado; suíte Windows com falhas reais

Ramo claude/windows-installer (e9ea687), CI 39900942827: passo de instalação 8/8 (pasta com espaço e ç, bytes, probe, launcher, HKCU, desinstalação). Correções: native() para barras do MSYS2; IfSilent nas MessageBox; OpenSSL com caminhos ASCII e lib/ossl-modules empacotado; relançar via nome 8.3 ou junção ASCII (Poppler abortava em pasta com ç, provado por controle ASCII); lista de desinstalação com "\". Suíte nativa: 117 ok, 2 falhas (test_attachment_search), travou no teste 120 (diálogo real de impressão Windows, timeout 120 s). Aceitação: 62/5/12 (os.getuid e assinatura). Próximo: Claude corrige app/tests para Windows no mesmo ramo, começando pelo travamento.

## 2026/10/23 às 05:46 (America/Sao_Paulo, UTC−03:00) — Codex: retorno executado; S2/S3 e checkpoint E30

- Retorno das05:30 executado pelo app. Automação pontual removida após o disparo; nenhum retorno diário foi solicitado. Limite de uso explícito interrompeu o turno anterior; não se atribuiu isso à VM, ao Foxit ou a esgotamento de contexto sem evidência.
- Claude escreveu PEGUEI E30 às02:17. Codex leu e confirmou no seu chat, sem abrir VM/VirtualBox. Último estado próprio anterior: Foxit2788, corpusbusca-escopos.pdf2/2, seletorAbrir com documento e relógio01:29:57. Cancelar não foi enviado; encerramento/postflight não confirmado. Observador0110 tem validade limitada: não presumir atividade atual. Evidência em docs/VM-E30-INTERRUPCAO-E-RETOMADA-2026-10-23.md e testes/resultados/vm-2026-10-23-e30/interrupcao.json.
- S2: dois lotes preservados, oito observações/quatro novas/quatro revisitas,2389 instruções/8132bytes. Cinco resultados antigos relidos separadamente1611/5519. LaçoGDI e dois trabalhadores, DEVMODE em duas fases/ResetDCW, RAW com rejeição de escrita parcial e propriedade do contexto de fundo detalhados. Não há contrato-8 para StartDoc nesse corpo; falha<1 retorna0. Cancelamento físico e tipagem integral continuam abertos. RelatórioREA-S2-CONTINUACAO-2026-10-23.md.
- S3: CommentsSummary.fpi0a7d7ed...c3ca8; nove entradas novas (sete corpos/dois thunks),191 instruções/608bytes. Enum+434=0..4, bitmaps, parâmetro1/0 e grupo de sete controles conferidos. OrdinalMFC14234 não existe na DLL adjacente inventariada; identificação ShowWindow vem do mapaGhidra, não de binding runtime. Gerador integral e demais motoresS3 continuam abertos. RelatórioREA-S3-ANOTACOES-RESUMO-2026-10-23.md.
- Integração:17 observações,13 novas/4 revisitas,2580 instruções/8740bytes; catálogo397→410=152REA+258diretas. Metadados/raw/pseudocódigo e máquinas conferidos, links e fences válidos; recibo testes/resultados/retomada-0530-2026-10-23/review.json. Não repetiu Java/Ghidra ao retomar os lotes; próximos S4/pesos em subfrentes dirigidas.
- Sem alteraçõesCodex em app/tests/aceitação, workflows, candidato0.1.19, critérios/pesos, escopo ou releases. Não repetiu744testes/81aceitações nem aumentou paridade integral. AutoriaAirton+trailerCodex mantida; publicação e B3 continuam dependendo de decisão própria.

## 2026/10/23 às 05:48 (America/Sao_Paulo, UTC-03:00) — Claude assume e opera a VM (E30)

Codex sem heartbeat desde 01:30 (04:30Z); vigia disparou (cálculo de "45 min" estava errado por bug de relógio, mas o Codex estava parado há ~4 h). Codex retomou às 05:30 e confirmou no chat que não acessa a VM. Claude pegou acesso de tela ao Oracle VirtualBox/VM (monitor W1642C), confirmou VM viva (relógio avançando), e observou UI01 (cancelar diálogo) e UI02 (Print com Microsoft Print to PDF; "Não respondendo" transitório na enumeração com rede off). observacoes.json em testes/resultados/vm-2026-10-23-e30/. VM deixada em estado limpo (documento aberto, sem modal). Próximo: UI05/UI09/UI10, D10-D20 e repetição da busca E24. Sem rede, Foxit não reiniciado, host intocado.

## 2026/10/23 às 05:51 — Errata de identificação UI05 na campanha0110

No startup escolhido no prompt do leitor padrão não é UI05: o plano testes/cenarios-interface.json reserva UI05 a Imprimir todas as abas (resource645/control1275), incluindo confirmação Batch Printing. Corrigidos relatório/JSON da interrupção; minichat anterior preservado com errata posterior. As observações históricas No do diálogo Batch Printing de18/19outubro continuam válidas nos respectivos recortes; esta errata só corrige o rótulo do startup0110. Claude confirmou em seu chat o seletorAbrir e relógio05:39:11→05:39:28; atribuído a ele, sem inspeçãoCodex ou Cancel confirmado.

## 2026/10/23 às 06:06 (America/Sao_Paulo, UTC−03:00) — Codex: pesos/scorers, reflow e integração E30

- S1: seis entradas novas emlucene++.dll,557 instruções/1653bytes. RTTI ligaBooleanWeight, boost e propagação do parâmetro aos pesos filhos; listasrequired/prohibited/optional e interseçãoDocID poradvance caracterizadas. NO_MORE_DOCS confirmado por export. Fábricas/scorers concretos, ranking/coletor e domínios integrais continuam abertos. RelatórioREA-S1-PESOS-E-SCORERS-2026-10-23.md.
- S4: oito entradas novas emFoxitPDFReader.exe,374 instruções/1107bytes; duas rodadas dirigidas sem repetir o lote anterior. Reflow liga mapas/prefixos a extensões e limites, preserva posição relativa na troca do escalar e reseta+68..74 para zero nessa via. Unidade física e domínios integrais continuam sem prova; guardas locais não são vulnerabilidade demonstrada. RelatórioREA-S4-REFLOW-2026-10-23.md.
- Catálogo410→424=152REA+272diretas,14 novas nesta segunda entrega. Na retomada05:30:31 observações,27 novas/4 revisitas,3511 instruções/11500bytes. Recibo testes/resultados/retomada-s1-s4-2026-10-23/review.json. Entradas antigas/hash e pseudocódigo preservados; máquina/bytes conferidos, sem novo teste de paridade.
- Primeiro marco9504be9 e merges8f197cb/96fd7a6 preservaram registros concorrentesClaude e autoriaAirton+trailerCodex. 96fd7a6 confirmado no remoto. UI01/cancelar e UI02 recebidos deClaude; Codex não acessou VM nesta retomada. RótuloUI05 do startup corrigido, não invalidando os registros históricosBatchPrinting. IncludeCommentsOFF é observação da sessão; default universal/causa da consultaE24 ainda não confirmados peloCodex sem repetição/estado contemporâneo, ressalva enviada aClaude.
- S1/S2/S3/S4 integrais e E30 continuam parciais. Não alterados peloCodex: app/tests/aceitação, árvoreworkflowsdf2e143226f31343781b1598f3bcf6b6e8dae5e7, candidato0.1.19, critérios/pesos, B3, exclusões ou releases. Não repetir os744testes/81aceitações como se fossem novos. Próximos alvos específicos em cada relatório, sem reiniciar análises preservadas.

## 2026/10/23 às 10:23 (America/Sao_Paulo, UTC-03:00) — Claude: Windows nativo, suíte e aceitação aprovadas

Pedido do usuário (09:10): listar o que falta e fazer o que não depende dele nem da VM, uma etapa por vez. PEGUEI no CHAT-CLAUDE.txt às 09:12. Etapa 1 = Windows (E34). Ramo claude/windows-installer, commits 7c3cc4c, 3e863ee, 235f4f0, 92f1708: _windows_powershell() em pdf_signatures (System32\WindowsPowerShell por caminho absoluto, SignedCms via System.Security no 5.1); run_tests.py grava traceback de falha/erro no progresso e aceita --modules (subconjunto diagnóstico); run_acceptance.py grava progresso por caso; workflow windows-native com entradas diagnósticas que nunca certificam e tempos 30/20/90 min; seletor GTK comparado por caminho normalizado e limitado a 10 s (testes e casos S12-23-1/2); S12-03-2 contorna o cache durante a falha sintética; tests/gtk_cleanup.py repete a limpeza só no Windows. CI 39958811654: instalação 8/8, suíte 759/735 aprovados/0/0/24 pulados, aceitação 79/79, revisão limpa 92f1708. Repetição dos módulos sensíveis a tempo 39958826197: 57/58, 1 pulado, 0 falhas. Linux 39958829720 aprovado. Intermitência: 39956902687 teve 3 esperas de GUI além do limite; não reproduzidas depois. Não integrado à main (preservar árvore do candidato 0.1.19/E29). Sem VM, Foxit, publicação, B3 ou mudança de critérios. Próximo da fila, só após confirmação do usuário: edição universal de anotações. Evidência testes/resultados/a6-windows-2026-10-23/review.json.

## 2026/10/23 às 11:21 (America/Sao_Paulo, UTC-03:00) — Claude: anotações universais (etapa 2)

Usuário confirmou às 10:53. PEGUEI no CHAT-CLAUDE.txt às 10:55. Ramo claude/anotacoes-universais (42aa075, 1df4aba) a partir da main 32cb630. Novo app/annotation_universal.py (capabilities/move/resize/style/delete/update_text/records); pdf_changes roteia move/resize/style/delete/update-annotation por ele e edit-info usa records(); _removable_annotation/_annotation_records removidos. edit_dialogs: annotation_choices/annotation_label, motivo das recusadas, opção 'manter cores' (color None = só opacidade). S12-14-4/6 adaptados (nota Locked, ícone NoZoom), especificação e contratos-funcionais.md regenerados. CI 39966777218: suíte ok, aceitação 79/81 (casos antigos); CI 39967990215: suíte 753/753, aceitação 81/81, revisão limpa. Fora da main; Flatpak/Windows pendentes. Próximo da fila, só com confirmação: redação também em metadados, marcadores e anexos.

## 2026/10/23 às 12:17 — vigilância e continuidade de Claude

Pedido explícito do usuário pela imagem: detectar interrupção e continuar do checkpoint. Automação acompanhar-claude-e-continuar-linuxit-pdf criada e confirmada no app, a cada10min; protocolo docs/COORDENACAO-INTERRUPCOES-2026-10-23.md, primeira amostra UTC em analysis-local/coordination-monitor/state.json. Sem interrupção confirmada ou tomada de VM. Horários escritos no minichat estavam futuros em relação à observaçãohost: comparar mudanças reais/UTC, não inferir travamento. Claude reservouS1/S2/S3, informa retorno15:20; lotesCodex06h salvos e verificados sem repetirGhidra.

## 2026/10/23 às 12:33 (America/Sao_Paulo, UTC-03:00) — Claude: S2 fechado (estático)

Pedido do usuário (12:02): fazer os 5 critérios (E8 impressão S2, E8 busca S1, E9 diagramas S3,
E12 entradas/saídas/erros, E12 Fase A), mantendo o Codex informado. S2 concluído no ramo
`claude/estatica-s1-s2-s3`: `docs/REA-S2-FECHAMENTO-2026-10-23.md`, revisão e machine-checks em
`testes/resultados/s2-fechamento-2026-10-23/`, sementes/metadados `*-s2-fechamento-lote{1..4}-*`.
Rodadas brutas em `analysis-local/headless/claude-s2-{1..4}` (nuvem do Claude, fora do Git).
Critério etapa 8 "Fluxo completo de impressão reconstruído" → `done` (lacunas declaradas no doc);
índice 46,87%. Não repetir as 54 entradas. Próximo: S1 (busca) — lado Foxit + fronteira Lucene++
(APIs próprias AddMatchTerms, PDFText_UnicodeDeals, to_Stemming, WildcardQuery StarCharPosition);
depois S3 (dez sementes de REA-S3-ESTADOS). E12 depende de VM/B3 e não será fechado.

## 2026/10/23 às 12:47 (America/Sao_Paulo, UTC-03:00) — Claude: S1 e S3 (lotes), ambos parciais

S1: `docs/REA-S1-LUCENE-FOXIT-2026-10-23.md` (rodadas `claude-s1-luc` e `claude-s1-fx`, 16
entradas). S3: `docs/REA-S3-HANDLERS-2026-10-23.md` (rodadas `claude-s3-main` e
`claude-s3-comments`, 6 entradas). Catálogo 491. Não repetir essas entradas. Faltam em S1: +3/+0xc,
proximidade +0x10, escritor de AddMatchTerms, escapes/erros. Em S3: consumidores de
+0x434/+0x438/+0x2bc/+0x204, camadas (incluir `LayerPanelToolPlugin.fpi` `d3dd66d6…` como alvo
fixado antes de rodar 0x10041820/0x10041bc0/0x10041bf0/0x10045380) e os motores. E12 (entradas/
saídas/erros, Fase A) depende de VM/B3: não fechado. Próximo do Claude: lista de desenvolvimento
(redação em metadados/marcadores/anexos no ramo `claude/redacao-completa`).

## 2026/10/23 às 12:50 (America/Sao_Paulo, UTC-03:00) — Claude: item de redação pausado

A implementação da redação de dados ocultos (metadados/marcadores/anexos) foi interrompida por
um filtro automático de segurança do assistente antes de gravar qualquer arquivo. Nenhuma mudança
em app/tests. Aguardando decisão do usuário sobre como seguir. Itens 2–6 da lista não iniciados.
