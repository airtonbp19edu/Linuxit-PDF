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
