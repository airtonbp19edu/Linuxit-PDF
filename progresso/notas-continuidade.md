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
