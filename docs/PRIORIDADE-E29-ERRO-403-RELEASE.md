# PRIORIDADE — E29: por que o token do GitHub Actions não cria releases (HTTP 403)

Registrado em 2026/10/20 às 17:09 (America/Sao_Paulo, UTC-03:00), a pedido do usuário. **Esta é a
instrução prioritária para a próxima IA (Codex)**: identificar a causa do erro abaixo
antes de qualquer outra etapa. O Claude retoma às 20:10 do mesmo dia com base no que
for registrado aqui e nas notas de continuidade.


## Recado direto ao Claude na retomada

Registrado em 2026/10/20 às 17:43 (America/Sao_Paulo, UTC-03:00).

**A causa do 403 já foi identificada e reproduzida. Não é necessário reiniciar o diagnóstico.** A correção e os comprovantes foram publicados até o commit `ef40885`.

- O commit testado `dec46c9` possui workflows diferentes da branch padrão. Criar a release nesse alvo exige `Workflows:write`, indisponível no `GITHUB_TOKEN`, inclusive para rascunhos. O mesmo token retornou 201/201 na main e 403 no alvo antigo (CI 39490423511).
- O fluxo `publish-devel-release.yml` agora usa `scripts/release_preflight.py`: confere tag/SHA/digest, reconhece a versão já publicada e detecta antecipadamente a necessidade de rascunho do dono. Oito testes passaram; CI 39491077708 aprovou a conferência somente leitura da 0.1.17, sem republicação.
- Para a próxima entrega automática: finalize os workflows **antes de gerar o candidato** e mantenha sua árvore igual à da branch padrão até publicar. Use o SHA e o pacote testados; nunca substitua pelo HEAD atual para evitar a restrição. `Conferir somente` começa habilitado; desmarcar somente numa publicação autorizada.
- Se houver mudança de workflows após o candidato, gere/valide candidato novo ou use um rascunho preparado pelo dono no SHA exato e deixe o fluxo somente anexar o pacote. Não é necessário mudar permissões globais nem pedir token pessoal para esse procedimento.
- **Pendente restrito da E29:** comprovar uma próxima publicação automática real, com tag, asset, download e auditoria conferidos. Isso não foi executado porque esta rodada proíbe publicar releases/tags. A causa está confirmada, mas o critério final da etapa continua aberto.
- A 0.1.17, seus assets e a VM foram preservados. Rascunhos descartáveis removidos e ausência de tags confirmada. Veja os recibos em `testes/resultados/e29-release-403/` e as notas de 17:19/17:22 em `progresso/notas-continuidade.md`. Retome pela fila e pelas autorizações já registradas.

## Diagnóstico confirmado pelo Codex — 20/10/2026

[Execução 39490423511](https://github.com/airtonbp19edu/Linuxit-PDF/actions/runs/39490423511), commit `038ae75`: **mesmo GITHUB_TOKEN, contents:write, mesma sessão e três rascunhos**, alterando apenas o alvo:

| Alvo do rascunho | HTTP | Resultado |
|---|---|---|
| Omitido (branch padrão) | 201 | Criado e apagado (DELETE 204) |
| SHA atual da main (`038ae75`) | 201 | Criado e apagado (DELETE 204) |
| SHA testado da 0.1.17 (`dec46c9`) | 403 | Resource not accessible by integration |

**Causa identificada:** os arquivos de `.github/workflows/` do alvo antigo diferem dos da branch padrão. O endpoint de criação exige autorização adicional `Workflows:write` nessa situação, inclusive com `draft:true`. O `GITHUB_TOKEN` não pode receber essa permissão. A [documentação oficial de Create a release](https://docs.github.com/en/rest/releases/releases?apiVersion=2022-11-28#create-a-release) descreve expressamente essa restrição e o 403/404. Portanto o rascunho não enfraquece a hipótese 1: a verificação ocorre na criação da release e não apenas na criação da tag.

O cabeçalho aceito foi `contents=write; contents=write,workflows=write`. Os dois rascunhos criados foram removidos; os três nomes de tag retornaram 404 após o teste. Inventário completo das releases públicas e de seus assets idêntico antes/depois. Não foi necessário `write-all`, alterar permissões padrão, imutabilidade, regras ou usar novo token.

Evidências integrais: [respostas HTTP](../testes/resultados/e29-release-403/probe-39490423511.json) e [revisão com hashes](../testes/resultados/e29-release-403/review.json). O 403 do terceiro caso é o resultado esperado do experimento, e não uma falha do job.

### Correção do fluxo e uso daqui em diante

- `scripts/release_preflight.py` consulta apenas leituras da API. Confere tag (inclusive anotada), SHA testado, rascunho, tamanho/digest do asset e árvores de workflows; não cria nem altera nada.
- `publish-devel-release.yml` começa em **Conferir somente**, habilitado por padrão. Desabilite essa opção apenas numa entrega autorizada para publicar/anexar. O plano fica no resumo e num artefato.
- Versão já publicada e correta: `already_published`, sem download/reenvio/recriação da release. Se tag ou bytes divergirem, interrompe; nunca substitui silenciosamente.
- Candidato com a mesma árvore de workflows da branch padrão: `create_release`, pode publicar automaticamente no **SHA testado**, conservando o artefato verificado. Pode haver commits novos de app/docs na main; a comparação verifica a árvore de workflows.
- Candidato histórico com workflows diferentes: `owner_draft_required`, explica a ação necessária e encerra sem tentar a chamada que recebe 403. O dono prepara um rascunho na página Releases com a tag e SHA exatos do manifesto; depois o fluxo só anexa os bytes testados (`upload_draft`). Um rascunho que já tem o pacote correto retorna `draft_ready`, aguardando publicação pelo dono. Esse caminho já funcionou na entrega 0.1.17.
- Para a **próxima entrega automática**, finalize os workflows antes de gerar o candidato e mantenha `.github/workflows/` igual até a publicação. Não é preciso congelar app/docs. Se alterar workflows após o candidato, valide um candidato novo ou use o rascunho do dono.
- Não apontar a tag à main nem usar `--target main` para escapar do erro: isso perderia a identidade testada. Não aumentar permissões globais nem gravar tokens. Um token próprio com permissões extras seria alternativa opcional do dono, não requisito da solução adotada.

**Limite da conclusão:** a causa foi reproduzida e a correção passou no CI em modo somente leitura. A publicação automática de uma próxima versão continua sem execução, porque esta E29 proíbe publicar ou criar tags públicas. O critério final da E29 exige essa próxima entrega; não declarar esse critério cumprido com rascunhos ou com a conferência da 0.1.17 já existente. Risco de concorrência permanece se outra sessão mudar workflows entre a conferência e a chamada de criação; a API continua aplicando sua proteção.

### Validação da correção, sem publicação

[Execução 39491077708](https://github.com/airtonbp19edu/Linuxit-PDF/actions/runs/39491077708), revisão `dc49fcd`, aprovada: `check_only:true`, plano `already_published`, tag `v0.1.17-devel` e commit `dec46c9` preservados, oito testes de guardas aprovados. Download/envio/criação foram pulados intencionalmente, porque essa verificação não publica nada; não confundir esses passos com testes de app pulados. [Plano preservado](../testes/resultados/e29-release-403/release-plan-39491077708.json).

No Windows, os oito testes também passaram pelo runner padrão do projeto, como subconjunto explícito, sem GTK. A importação da ferramenta nos testes foi ajustada para funcionar tanto via unittest quanto pelo runner (mesmo padrão dos auditores existentes). Conferência final independente da API confirmou ambos os IDs apagados404, três tags404, nenhum rascunho de diagnóstico e inventário público de releases/assets inalterado: [post-check.json](../testes/resultados/e29-release-403/post-check.json).

**Próximo teste de fechamento:** numa próxima entrega autorizada, produzir candidato com workflows finalizados e iguais aos da branch padrão, executar o fluxo com Conferir somente desmarcado, conferir a tag no SHA testado, asset e download, depois auditoria do mesmo bundle. Nenhuma dessas publicações foi executada nesta rodada. O status da E29 fica em andamento até esse comprovante; a causa não está mais em investigação. A etapa seguinte não foi iniciada.

## Registro original (preservado como histórico)

## O erro

`gh release create` no fluxo manual `.github/workflows/publish-devel-release.yml` falha com:

```
HTTP 403: Resource not accessible by integration (https://api.github.com/repos/airtonbp19edu/Linuxit-PDF/releases)
```

O job recebe, segundo o log ("GITHUB_TOKEN Permissions"): `Actions: read`, `Contents: write`, `Metadata: read`.

| Execução | Disparo | Commit do fluxo | Pedido | Resultado |
|---|---|---|---|---|
| [39485174222](https://github.com/airtonbp19edu/Linuxit-PDF/actions/runs/39485174222) | usuário (botão Run workflow) | f94b95b | criar release publicada, `--target dec46c9` (cria tag) | 403 |
| [39486020955](https://github.com/airtonbp19edu/Linuxit-PDF/actions/runs/39486020955) | usuário | d692f8b | criar release **rascunho**, `--target dec46c9` | 403 |
| [39486650871](https://github.com/airtonbp19edu/Linuxit-PDF/actions/runs/39486650871) | Claude (API workflow_dispatch) | bb9d270 | **anexar asset** a rascunho já existente (POST uploads.github.com …/releases/{id}/assets) | **sucesso** |

Em todas, os passos anteriores (baixar o artefato do CI 39474059660 e conferir tamanho/SHA-256) passaram.

## O que já foi verificado

- Configurações do repositório (lidas no navegador do dono em 20/10 ~16:50):
  - Actions → General → Workflow permissions: **"Read repository contents and packages permissions"** (padrão só leitura). O fluxo declara `permissions: contents: write`, e o log confirma `Contents: write`.
  - "Allow GitHub Actions to create and approve pull requests": desligado.
  - Actions permitidas: todas; exigência de SHA fixo: desligada.
  - General → Releases → "Enable release immutability": **desligado**.
  - Rulesets: nenhum (`GET /repos/.../rulesets` → `[]`). Sem proteção de tag.
- Repositório pessoal, público; o dono tem admin.
- A 0.1.16 (`v0.1.16-devel`) foi criada com o acesso do próprio dono (sessão do Codex), não com o token do Actions — por isso o problema não apareceu antes.
- A sessão do Claude não pode criar releases pela API ("not permitted for this session type") nem enviar tags por git (bloqueado); por isso a 0.1.17 foi criada como rascunho no navegador do dono e publicada com a confirmação dele (release 418804985, tag `v0.1.17-devel` → dec46c9, asset 660312363 conferido).

## Hipóteses (não confirmadas)

1. Criar a tag num commit (dec46c9) cujos arquivos de workflow diferem da `main` exigiria a permissão `workflows`, que o token nunca tem. **Enfraquecida**: o rascunho (que não cria tag) também falhou — mas o `target_commitish` antigo ainda pode ser checado.
2. Alguma política da conta/plataforma restringe criação de releases pelo token automático (diferente de enviar assets, que funcionou).
3. Diferença entre execuções disparadas pelo usuário e pela API (a única que funcionou foi disparada pela API, mas fazia outra operação).

## Diagnóstico sugerido (sem publicar nada)

1. Fluxo temporário (ex.: `.github/workflows/diag-release-403.yml`, `workflow_dispatch`, `permissions: contents: write`) que, com `curl -i` e o `GITHUB_TOKEN`, tenta criar **rascunhos descartáveis** com nomes de tag `diag-403-<run_id>-<n>`:
   - (a) sem `target_commitish`; (b) `target_commitish` = SHA atual da `main`; (c) `target_commitish` = `dec46c979e56d722482a465563c6df97b898dcdc`.
   - Registrar status HTTP e os cabeçalhos `X-Accepted-GitHub-Permissions`, `X-GitHub-Request-Id` e o corpo de cada resposta.
   - **Apagar** cada rascunho criado no fim (`DELETE /repos/.../releases/{id}`). Não criar tags nem releases públicas.
2. Repetir com `permissions: write-all` (só no fluxo de diagnóstico) e comparar.
3. Se nada mudar: como experimento reversível, o dono troca Actions → General → Workflow permissions para "Read and write", roda o diagnóstico e volta a configuração.
4. Registrar o resultado em `testes/resultados/e29-release-403/` e nas notas, com data e hora reais, e remover o fluxo temporário (ou deixá-lo manual e documentado).

## Regras

- Não publicar release, não criar tag pública, não apagar a `v0.1.16-devel` nem a `v0.1.17-devel`.
- Não pedir nem gravar tokens em arquivos; se a solução for um token pessoal como segredo, só o dono cria e salva.
- Registrar tudo em `progresso/notas-continuidade.md` e `docs/AVISOS-E-STATUS.md` com data e horário, e publicar no GitHub.


## Retomada exclusiva da E29 pelo Claude — 2026/10/20 às 22:09 (America/Sao_Paulo, UTC-03:00)

**Instrução do usuário (20/10/2026 às 22:06): até segunda ordem, trabalhar apenas em descobrir e
resolver este erro.** Nenhuma outra etapa deve ser iniciada enquanto ela valer.

### Causa conferida de forma independente

- Documentação oficial do endpoint "Create a release" (consultada em 2026/10/20 às 22:09): se o commit de
  `target_commitish` (ou o último da branch padrão, quando omitido) adiciona ou altera arquivos em
  `.github/workflows/` em relação à branch padrão, o token precisa da permissão **Workflows
  (write)**; o `GITHUB_TOKEN` do Actions "não pode ser autorizado para isso"; sem essa autorização a
  API responde 404 ou, em alguns caminhos de autenticação, 403. Fonte:
  https://docs.github.com/en/rest/releases/releases?apiVersion=2022-11-28#create-a-release
- Recibo do Codex (CI 39490423511): o cabeçalho `X-Accepted-GitHub-Permissions` do endpoint foi
  `contents=write; contents=write,workflows=write` nos três pedidos; com o mesmo token, os
  rascunhos sem alvo e com alvo na `main` foram criados (201) e o alvo `dec46c9` foi recusado (403,
  "Resource not accessible by integration").
- Por que a 0.1.17 caiu nisso: o candidato `dec46c9` foi montado **antes** de o fluxo
  `publish-devel-release.yml` existir e antes da mudança do `qpdf` no CI; na hora de publicar, a
  `main` já tinha outros workflows. Logo, o alvo "alterava" workflows em relação à branch padrão.

### Solução e comprovação em curso

- Regra: **workflows finalizados antes de montar o candidato e iguais aos da `main` até publicar**
  (o fluxo de publicação confere isso no modo "Conferir somente").
- Candidato 0.1.18: `b60b6e6` (versão) e `3871138` (testes ajustados ao sandbox), ambos com a
  árvore de workflows `59487bae5b42163c1ccc68e0dc04218f5fd564b6`, igual à da `main`. Nenhum arquivo
  de workflow será alterado até a publicação.
- Primeira montagem (CI 39522091373) falhou só no sandbox por testes que usavam `pdftoppm` e por
  OCR exato; corrigido em `3871138`. Montagem nova: CI 39524293929.
- Próximos passos: registrar o candidato, rodar a publicação em "Conferir somente" (plano esperado:
  `create_release`), pedir a confirmação do usuário e publicar com o token automático; conferir a
  release, o download público, a auditoria e o teste de desktop.
