# Etapa 14 — projeto existente conferido

Continuação posterior: [etapa 15](ETAPA-15.md), com backend de anexos no
código-fonte e critérios ainda parciais. As verificações abaixo são deste
marco anterior e permanecem preservadas.

Em **17/10/2026**, a etapa de criação do projeto foi conferida a partir do
código já existente. Seus dois critérios já estavam `done`; a base foi
preservada e a versão continua **0.1.1**, em desenvolvimento. Esta rodada
também registra a [exclusão dos recursos de IA](ESCOPO.md) pedida pelo usuário.

## Base e pontos de entrada

| Parte | Fonte e contrato |
|---|---|
| Código próprio | `app/`, base MIT Winux/Print&View com [proveniência](proveniencia-base.json), adaptada para Linuxit. |
| Leitor Linux | `scripts/run.sh` chama `/usr/bin/python3 app/main.py`; requer GTK 3/PyGObject/Cairo, Poppler e dependências documentadas. |
| Worker portável | `app/worker_cli.py`: `info`, `panels` e `prepare`; a composição usada no controle é livreto, sem rasterização. |
| Testes completos | `scripts/run_tests.py --output <novo-arquivo.json>` no Linux com tela disponível; resultados anteriores são preservados. |
| Empacotamento | `scripts/build_flatpak.py`, loader pareado/`runtime-lib` e avisos de licenças; gerar nos marcos de entrega. |
| Licenças | [MIT do projeto](../LICENSE), [proveniência da base](proveniencia-base.json) e [BSD do pypdf](pypdf-LICENSE.txt). A cópia pypdf usada é 6.20.1. |

O ambiente atual Windows tem Python 3.13.15 e permite verificações portáveis.
A checagem local não encontrou `gi`, Cairo, cryptography, comandos Poppler,
CUPS nem Flatpak no Python/PATH examinados. Pillow está disponível. A execução
completa deve seguir o [ambiente Linux documentado](instalacao.md); esta
checagem não instala nem modifica o runtime.

## Verificações atuais

Foi acrescentado [check_project.py](../scripts/check_project.py), que confere
arquivos essenciais, avisos/licenças, proveniência, versão pypdf e pontos de
entrada. Exercita os subprocessos próprios e conserva stdout/stderr e PDFs
de saída em uma pasta nova de `analysis-local/`, sem sobrescrever rodadas.

```powershell
python scripts/check_project.py
```

Para salvar um resultado publicável, use caminhos novos:

```powershell
python scripts/check_project.py --work-dir analysis-local/project-proxima-rodada --output testes/resultados/projeto-proxima-rodada.json
```

| Verificação do worker | Resultado |
|---|---|
| `info` no PDF próprio | Duas páginas e tamanhos positivos |
| `panels` no mesmo PDF | Dois marcadores e um comentário |
| `prepare` em livreto | PDF reaberto, duas faces e conteúdo preservado |
| Comando ausente | Saída com código 2 |
| Job JSON inválido | Falha sem gerar saída PDF |
| PDF vazio | Falha sem apresentar metadados válidos |

**6/6 passaram.** A fixture e os arquivos essenciais conferidos mantiveram
seus hashes. Resultados completos locais em
`analysis-local/project-stage14-2026-10-17/`; relatório publicável em
[etapa-14-projeto-2026-10-17.json](../testes/resultados/etapa-14-projeto-2026-10-17.json).

As checagens de arquitetura/pendências e especificação continuam válidas.
A suíte histórica Linux de 37/37, o payload 37/37 e o sandbox Flatpak 5/5
permanecem evidências anteriores. Esta rodada não abriu a GUI, renderizou
imagens via Poppler, exerceu marcas Cairo do mosaico, executou os 50 cenários
completos, observou o Foxit ou testou impressão física. Não houve pacote novo.

## Estado e próximo passo

A etapa 14 mantém **100% dos dois critérios existentes**, com evidência
histórica de execução Linux e novos controles portáveis. A etapa 13 também
está verificada como projeto. Isso não fecha a especificação de referência
nem implementa as famílias pendentes. Pesos/revisão preservados; roteiro
43,33%, catálogo 209 e paridade 0/25.

Próxima etapa do roteiro: 15, reconstrução incremental da lógica principal,
apenas para contratos suficientes e dentro do escopo sem IA. A agenda de
análise, corpus e validação Linux/VM continua no
[registro de pendências](../progresso/pendencias-analises.md). Não repetir a
criação do projeto nem as rodadas estáticas já examinadas.
