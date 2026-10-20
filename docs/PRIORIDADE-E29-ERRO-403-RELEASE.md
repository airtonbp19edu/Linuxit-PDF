# PRIORIDADE — E29: por que o token do GitHub Actions não cria releases (HTTP 403)

Registrado em 2026/10/20 às 17:09 (America/Sao_Paulo, UTC-03:00), a pedido do usuário. **Esta é a
instrução prioritária para a próxima IA (Codex)**: identificar a causa do erro abaixo
antes de qualquer outra etapa. O Claude retoma às 20:10 do mesmo dia com base no que
for registrado aqui e nas notas de continuidade.

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
