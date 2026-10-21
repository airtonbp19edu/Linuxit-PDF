# Avisos de falha do GitHub Actions

As mensagens com “Run failed” informam que uma verificação automática falhou.
O envio de commits ao GitHub pode ter sido concluído normalmente. Os workflows
atuais são iniciados manualmente nos marcos de validação; um push sozinho não
inicia essas campanhas. Os avisos antigos permanecem no histórico do e-mail.

## Portal e integração do desktop — corrigido em 19/10/2026

A notificação referente ao commit `a5ebda9` é da
[execução 39339331887](https://github.com/airtonbp19edu/Linuxit-PDF/actions/runs/39339331887).
Oito dos nove controles passaram. A primeira leitura após a concessão pelo
portal encontrou o arquivo ainda indisponível; a leitura após reiniciar o
portal, a revogação e a associação de PDF já passaram nessa execução.

A correção `e61d174` espera que o processo de portal criado pelo teste seja o
proprietário do nome no D-Bus e que a exportação FUSE esteja disponível. Antes,
outro processo ativado automaticamente podia satisfazer a espera apenas pelo
nome. A leitura continua obrigatória e precisa conferir os bytes esperados.

A [execução corrigida 39339986089](https://github.com/airtonbp19edu/Linuxit-PDF/actions/runs/39339986089)
passou nos **9/9 controles**, sem erros. Ver
[relatório examinado](../testes/resultados/sem-vm-2026-10-19/s10-third/review.json).
Ela testou o pacote publicado 0.1.15: concessão fora da pasta pessoal,
persistência após reiniciar o próprio portal, revogação, associação/abertura
real de PDF e atualização/retorno de versão com preferências preservadas.
É um desktop X11 efêmero, sem alteração no Windows ou na VM do usuário.

## Outras falhas preservadas

- CUPS mínimo sem backend `socket`: a fila sintética passou a usar o backend
  IPP disponível. A execução posterior aprovou os quatro controles reais de
  envio retido, consulta e cancelamento, sem impressora física.
- RFC3161: o subcomando `openssl ts` não aceita as mesmas opções de repositório
  do subcomando CMS. Foram usados repositórios vazios explícitos. A validação
  Linux posterior aprovou o token e recusou sua associação a bytes alterados.
- Primeiro candidato Flatpak 0.1.16: a consulta TSA dependia de um arquivo de
  configuração OpenSSL ausente no sandbox. Fonte e payload passaram; o teste
  instalado identificou o problema. O candidato foi rejeitado. A revisão
  `a5ebda9` fornece configuração mínima explícita para a consulta e a verificação;
  a [execução corrigida39339330479](https://github.com/airtonbp19edu/Linuxit-PDF/actions/runs/39339330479) aprovou564/564 testes em cada ambiente fonte/payload/sandbox, sem falhas/erros/skips. Somente esse novo candidato foi publicado como0.1.16 de desenvolvimento.

Os testes que detectaram as falhas foram mantidos. Notificações da conta não
foram desativadas; apagar o aviso ou aceitar uma falha como sucesso ocultaria
o estado real do projeto. Falhas futuras devem ser investigadas pelo primeiro
passo que falhou e pelo relatório preservado em sua execução.


## Corrida de montagem FUSE — repetição0.1.16

A execução39341668923 passou atualização/retorno,preferências e negação inicial,
mas o processo do portal encerrou com `fuse init failed: Unable to create dir`.
Os demais controles não executaram; a auditoria independente do pacote passou
separadamente. O erro foi preservado em[s10-fourth-fuse](../testes/resultados/sem-vm-2026-10-19/s10-fourth-fuse/review.json).

O teste iniciava quatro instâncias Flatpak antes de assumir o portal. Essas
instâncias podiam ativar outro daemon; `--replace` então disputava a desmontagem
FUSE. Essa causa é uma inferência apoiada pelo log e pelo [código do portal1.20.3](https://github.com/flatpak/xdg-desktop-portal/blob/1.20.3/document-portal/document-portal-fuse.c#L3387),
que tenta desmontar a montagem anterior antes de criar o diretório.

Agora o daemon controlado inicia no barramento privado antes da primeira
execução Flatpak. Não substitui um processo que não criou, e espera sua própria
montagem desaparecer antes de reiniciar. O workflow fará duas repetições em
ambientes novos para conferir estabilidade; nenhuma falha será aceita como
sucesso ou transformada em teste ignorado. Revalidação aprovada nas duas repetições abaixo.


A [execução corrigida39342162781](https://github.com/airtonbp19edu/Linuxit-PDF/actions/runs/39342162781), fonte do probe1fcc603, passou9/9 em **cada um dos dois ambientes novos**, usando o pacote0.1.16 publicado. A auditoria independente39341656820 aprovou a instalação do mesmo arquivo sem rebuild. [Relatórios examinados](../testes/resultados/0.1.16/desktop/review.json). As falhas anteriores não foram apagadas nem tratadas como sucesso. Novas falhas reais ainda podem gerar avisos; não houve alteração das notificações da conta.


## E08 — teste pulado por falta do qpdf (2026-10-20)

A [execução 39460438529](https://github.com/airtonbp19edu/Linuxit-PDF/actions/runs/39460438529),
revisão `ae429cd` (E08), terminou com 609 aprovados e **1 pulado** em 610; a
regra do CI não aceita testes pulados. O teste
`test_cross_reference_stream_source_gets_a_stream_update` usava o `qpdf` para
criar o PDF de origem com fluxo de referência cruzada, e o `qpdf` não existe na
imagem Debian 13 do CI. Não era defeito do aplicativo: a assinatura incremental
estava correta, mas aquele caminho (origem com xref em fluxo) ficava sem teste
no CI.

Correção em duas partes:

1. `9e75c0c`: a origem passou a ser criada pelo escritor incremental do pypdf,
   que termina o arquivo com fluxo de referência cruzada. Confirmado pela
   [execução 39472280348](https://github.com/airtonbp19edu/Linuxit-PDF/actions/runs/39472280348):
   613/613, nenhum pulado, aceitação 63/63.
2. Revisão desta seção: a cópia assinada com xref em fluxo agora também é
   conferida pelo `pdfsig` (duas assinaturas válidas) e o `qpdf` foi instalado
   no CI, para que o `qpdf --check` rode lá e não só localmente.

A execução falha foi mantida; revisão em
`testes/resultados/aceitacao/2026-10-20/ci-debian13-e08-falha-review.json`.


## Publicação 0.1.17 — 403 ao criar a release (2026-10-20)

A [execução 39485174222](https://github.com/airtonbp19edu/Linuxit-PDF/actions/runs/39485174222)
do fluxo manual de publicação baixou o pacote testado e conferiu tamanho e
SHA-256, mas `gh release create` voltou `HTTP 403: Resource not accessible by
integration`, embora o token do job tivesse `Contents: write`. O repositório não
tem rulesets. A causa provável: a release criava a tag `v0.1.17-devel` no commit
testado `dec46c9`, cujos arquivos de workflow diferem dos da `main` (o próprio
fluxo de publicação e a mudança do `qpdf` vieram depois); criar uma referência
assim exige a permissão `workflows`, que o `GITHUB_TOKEN` nunca recebe. A 0.1.16
foi publicada com o token do próprio dono, por isso não passou por isso.

Correção: o fluxo agora cria a release como **rascunho** (sem criar tag) com o
mesmo pacote conferido. O dono abre o rascunho na página Releases e clica em
"Publish release"; a tag é criada no commit testado com a permissão dele. Se a
tag já existir e apontar para o commit testado, o fluxo publica direto nela. Nada
foi recompilado e nenhum arquivo foi publicado na execução que falhou.


## Auditoria da 0.1.17 — "Application source changed since tests" (2026-10-20)

A [auditoria 39487498872](https://github.com/airtonbp19edu/Linuxit-PDF/actions/runs/39487498872)
da 0.1.17 publicada parou antes de instalar o pacote: o auditor comparava os
arquivos de `app/` do checkout atual com os testados no candidato. Depois do
candidato `dec46c9` o desenvolvimento continuou (E12 a E15), então o checkout da
`main` é legitimamente mais novo. Não era divergência do pacote.

Correção: `scripts/audit_delivery.py` passa a ler do Git, no commit testado do
manifesto, o inventário de `app/`, o construtor, `app/version.py` e as licenças
comparadas com o pacote instalado. A exigência continua a mesma (pacote = fonte
testada, arquivo por arquivo), mas não depende mais de a `main` estar parada. O
relatório informa `checkout_app_differs_from_tested_commit`. Execução local:
aprovada, 179 arquivos e 18 checksums conferidos. As integrações de desktop da
0.1.17 ([39487502789](https://github.com/airtonbp19edu/Linuxit-PDF/actions/runs/39487502789))
passaram nas duas repetições.


## Candidato 0.1.18 — testes novos no sandbox Flatpak (2026-10-20)

A [execução 39522091373](https://github.com/airtonbp19edu/Linuxit-PDF/actions/runs/39522091373)
(candidato `b60b6e6`) passou 663/663 na fonte e no pacote, mas no Flatpak instalado teve
651 aprovados, 10 pulados, 1 erro e 1 falha. Não era defeito do aplicativo:

- testes das etapas E12–E16 desenhavam com `pdftoppm`, que não vem no Flatpak (o aplicativo usa
  `pdftocairo`, que vem); no sandbox foram pulados ou deram erro. Agora usam `pdftocairo`;
- o teste de OCR da E19 exigia que o Tesseract reconhecesse palavras exatas, e o Tesseract do
  sandbox leu algumas de outro jeito ("titulo", "epsilon"). O teste agora confere só a ordem das
  colunas (todas as linhas da esquerda antes das da direita), que é o que a etapa promete.

Os arquivos de workflow não mudaram; o candidato novo continua com a mesma árvore de workflows da
`main`, condição para a publicação automática (E29).

Segunda montagem ([39524293929](https://github.com/airtonbp19edu/Linuxit-PDF/actions/runs/39524293929),
`3871138`): 663/663 na fonte e no pacote; no sandbox 662/663. A única falha foi o teste de OCR da
E19: a ordem das colunas saiu certa, mas o Tesseract do Flatpak leu "direita" como "direta"/"dieta"
(e "epsilon" como "epsibn"). O teste passou a casar cada linha reconhecida com a linha esperada mais
parecida (semelhança de texto) e a conferir só a ordem; um teste novo usa exatamente as linhas lidas
no sandbox e outro garante que colunas intercaladas continuam sendo recusadas. Observação para depois
da E29: o OCR do Flatpak reconhece pior que o do sistema (registrado em "Qualidade de OCR").
