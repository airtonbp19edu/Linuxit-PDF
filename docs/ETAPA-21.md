# Etapa 21 — auditoria incremental da entrega

A auditoria do **Flatpak 0.1.2/devel publicado** passou em **17/10/2026**.
Foi instalado o mesmo bundle, sem reconstrução, em Debian 13 com tela Xvfb,
Openbox e usuário dedicado no runner efêmero. O [run 39039390847](https://github.com/airtonbp19edu/Linuxit-PDF/actions/runs/39039390847)
executou o auditor no commit `2e6671825317a7e7846193973113f090365db4f9`.
A aplicação e os três bundles publicados foram preservados.

O resultado aprova a auditoria incremental dessa entrega. **A etapa 21 continua
50% verificada**, com o critério de encerramento `pending`: há 21 critérios
abertos em 14 etapas. O roteiro permanece 43,33%, a paridade Foxit 0/25 e a
cobertura global desconhecida. A fase A e a implementação seguem parciais.

## Evidência examinada

- [Auditoria do repositório](../testes/resultados/etapa-21/repository-audit.json):
  três checksums, sete relatórios selados, fonte atual/snapshot/commit testado,
  mesma população de testes e licenças/metadados MIT/BSD conferidos.
- [Auditoria da instalação real](../testes/resultados/etapa-21/installed-delivery-audit.json):
  deployment, commit OSTree e runtime iguais aos registrados; **83 arquivos da
  aplicação**, **2.803 arquivos de dependências**, **214 ELF** realmente presentes
  e catalogados, **149 avisos de copyright** presentes, não vazios e hasheados.
- [Sete controles do auditor](../testes/resultados/etapa-21/auditor-controls.json):
  incluem recusa de bytes alterados, licença ausente, ELF fora do catálogo,
  arquivo sem origem, derivação desconhecida, duplicidade, caminho externo e
  relatório com skip. São testes sintéticos de validação do auditor.
- [Novo smoke no sandbox](../testes/resultados/etapa-21/published-bundle-smoke.json):
  5/5, cobrindo abrir/renderizar, preferência de destaques, navegação de marcador,
  comentário e geração de livreto. Zero erros no relatório.
- [Revisão e hashes das evidências](../testes/resultados/etapa-21/review.json).

O SHA-256 do bundle continua
`9d29459d7aff8ca6859cda0846cd698d285b36c3a8de2f463ff87002740cd7ba`.
O ZIP do artefato 12103157602 conferiu com o digest GitHub
`dfaf5cb282c5a9dbb4aaa78be4ee8eb6bd9a49cac39fcfc28c4e1921fe7155b4`.
Raw e logs completos ficam em `analysis-local/stage21-artifact-12103157602/`
e `analysis-local/stage21-logs-39039390847/`, ignorados pelo Git.

Os **104 testes por ambiente da etapa 20 não foram repetidos**. Seus relatórios
foram conferidos como evidência histórica da mesma aplicação/bundle; nesta
rodada houve sete controles do auditor e cinco controles de execução novos.
Não somar essas contagens como funcionalidades ou paridade.

## Critérios preservados

| Critério da etapa 21 | Estado | Resultado desta rodada |
|---|---|---|
| Auditoria de fonte/licenças/testes/evidências | `done` histórico | Nova conferência da entrega 0.1.2 acrescentada. |
| Obrigações viáveis encerradas e bloqueios declarados | `pending` | Permanecem 21 critérios abertos, incluindo trabalho possível sem VM. |
| Sincronização e integridade final confirmadas | `done` histórico | Marco técnico publicado e HEAD remoto confirmado em `ba1f5e1`. |

Os 58 critérios foram cruzados com o registro: links dos 37 `done` históricos
conferidos, e todos os 21 não concluídos conservados. Isso **não reexecuta a
engenharia reversa histórica** nem promove a presença de arquivos a evidência
nova de comportamento. Nenhum critério/peso/status foi alterado.

## Verificação reproduzível

[`scripts/audit_delivery.py`](../scripts/audit_delivery.py) exige evidências
consistentes e um caminho de saída novo. O Git deve conter o commit de fonte
apontado no manifesto; o código `app/` deve corresponder à entrega auditada.

```bash
python3 scripts/audit_delivery.py --output /tmp/linuxit-audit-novo.json
python3 scripts/audit_delivery.py \
  --installed-root "$(flatpak info --user --show-location io.github.airtonbp19edu.LinuxitPDF//devel)/files" \
  --output /tmp/linuxit-instalado-audit-novo.json
```

O modo instalado lê o deployment informado pelo Flatpak e recusa outro
commit/runtime. Os bytes de runtime, código próprio e avisos são lidos da
instalação, independentemente do stage usado para criar o bundle.
O fluxo manual [delivery-audit.yml](../.github/workflows/delivery-audit.yml) e
[`scripts/ci_audit_delivery.sh`](../scripts/ci_audit_delivery.sh) preservam
relatórios e executam o smoke. Nenhum original Foxit entra no runner.

## O que falta e como continuar

Após esta auditoria, o [recorte lateral foi corrigido no 0.1.3](ETAPA-16-LAYOUT.md),
com comparação antes/depois e nova suíte completa114 por ambiente. A auditoria
0.1.2 acima continua como snapshot histórico preservado. Próximo trabalho sem
VM: repetir os quatro subconjuntos Poppler no mesmo corpus da etapa 18. Não
substituir seus bytes nem promover testes próprios a observações do original.

Desktop real, portais, acessibilidade e impressão física continuam pendentes.
O CI registrou aviso AT-SPI indisponível, sem traceback; tecnologias assistivas
não foram validadas. A [lista completa de pendências](../progresso/pendencias-analises.md)
separa análise estática, contratos, implementação, runtime e observação original.
A comparação Foxit exige a VM offline; os 20 cenários dinâmicos e os 50 casos
completos de aceitação continuam sem execução completa. IA permanece excluída.

Publicação técnica [`ba1f5e1`](https://github.com/airtonbp19edu/Linuxit-PDF/commit/ba1f5e1494759edad9cb9002d3a8802ae6d66b3e)
confirmada em 17/10/2026 às 11:15 (America/Sao_Paulo, UTC-03:00): HEAD
local/remoto iguais, árvore limpa e `git fsck --full` com retorno 0. Os quatro
relatórios CI também conferem nos blobs Git. Esta nota será enviada em commit
seguinte; o HEAD final é conferido por recibo externo, sem autorreferência.
