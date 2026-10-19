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
