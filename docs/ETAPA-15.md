# Etapa 15 — backend de anexos sem depender da VM

Continuação na [etapa 16](ETAPA-16.md): painel Anexos conectado ao código GTK,
controlador portável testado e execução visual ainda pendente. O marco abaixo
registra a entrega inicial do backend, antes dessa integração.

Em **17/10/2026**, foi implementado um contrato próprio de listagem e extração
local de anexos. É um avanço de código da etapa 15, com a IA do Foxit
[fora do escopo](ESCOPO.md). As funções ficam no código-fonte em desenvolvimento;
o Flatpak publicado 0.1.1 corresponde ao marco anterior e não foi regenerado.

## Comportamento implementado

O novo [pdf_attachments.py](../app/pdf_attachments.py) lê anexos do catálogo
plano `/Names/EmbeddedFiles`, usando o pypdf BSD já incluído. A listagem mantém
entradas distintas mesmo com nomes iguais, atribui índice e devolve o SHA-256
do PDF para uma extração posterior. Nomes inválidos são apresentados com o
motivo da recusa. A listagem não decodifica o conteúdo de cada anexo; tamanho
declarado ausente/desconhecido fica `null`.

A extração recebe índice, hash da listagem e uma pasta existente escolhida
pelo usuário. Confere identidade do PDF antes/depois da leitura, valida o
nome e grava os bytes com criação exclusiva. Arquivos existentes não são
substituídos; para extrair outra entrada com o mesmo nome, escolher outra
pasta. O retorno informa tamanho real, SHA-256 e caminho. O PDF original é
somente lido; anexos não são executados nem abertos automaticamente.

O contrato recusa caminhos absolutos/relativos com separadores, `..`, nomes
reservados Windows, caracteres de controle, ponto/espaço final, espaço inicial
e nomes acima de 240 bytes UTF-8. A política é a mesma em Linux/Windows.
Não há renomeação silenciosa. O diretório de destino deve ser controlado pelo
usuário; esse contrato não protege contra outro processo trocando diretórios
durante a gravação.

Limites atuais: 1.000 entradas na listagem e 64 MiB por payload extraído.
O tamanho declarado é checado antes da leitura, quando disponível; o tamanho
real só é conhecido **após descompressão**. Isso não constitui um limite rígido
de memória do parser. O worker tenta os limites POSIX já existentes onde
disponíveis; esses limites não existem no Windows atual.

Portfólios `/Collection`, árvores de nomes com `/Kids` e PDFs que exigem senha
não vazia retornam erro explícito. Anexos exclusivos de anotações de página,
modificação/remoção/inserção, busca dentro de anexos e integração GTK continuam
pendentes. Este subconjunto não encerra a família de anexos/portfólios.

## Uso pelo worker e pela API

O [worker](../app/worker_cli.py) tem os comandos `attachments <pdf>` e
`extract-attachment <pdf> <pasta>`. O segundo recebe em stdin um objeto JSON
com `index` e `source_sha256`; ambos devolvem JSON. Erros encerram com status
não zero. As saídas `info`, `panels` e `prepare` anteriores foram preservadas.

Exemplo no PowerShell, usando uma pasta nova dentro da área privada do projeto:

```powershell
New-Item -ItemType Directory -Path analysis-local/anexos-demo
$anexos = python app/worker_cli.py attachments testes/fixtures/anexos-simples.pdf | ConvertFrom-Json
@{index=0; source_sha256=$anexos.source_sha256} | ConvertTo-Json -Compress | python app/worker_cli.py extract-attachment testes/fixtures/anexos-simples.pdf analysis-local/anexos-demo
```

No Linux, a mesma API dispensa GTK para essas operações:

```python
import sys
sys.path.insert(0, "app")
from pdf_attachments import list_attachments, extract_attachment

pdf = "testes/fixtures/anexos-simples.pdf"
listing = list_attachments(pdf)
result = extract_attachment(pdf, 0, "/caminho/da/pasta/existente",
                            source_sha256=listing["source_sha256"])
```

O [PDF sintético próprio](../testes/fixtures/anexos-simples.pdf) e seu
[manifesto de bytes/hashes](../testes/fixtures/anexos-simples.json) não contêm
recursos Foxit. O recurso ainda não tem botão/painel na interface do leitor;
a integração gráfica pertence à etapa 16.

## Validação e continuidade

**14/14 testes portáveis passaram**, sem skips. Cobrem nomes duplicados,
preservação de bytes/hash/original, nomes perigosos, conflitos, identidade
alterada antes/durante leitura, limites declarados/reais, PDF inválido e os
recursos explicitamente não suportados, além do protocolo real de subprocesso.
Resultado: [etapa-15-anexos-tests-2026-10-17.json](../testes/resultados/etapa-15-anexos-tests-2026-10-17.json).

As seis regressões dos comandos anteriores do worker também passaram.
O [resumo técnico do marco](../testes/resultados/etapa-15-anexos-2026-10-17.json)
conserva hashes da fonte, conferência do corpus, verificações estruturais e limites.

O runner permite selecionar o módulo e uma pasta temporária gravável:

```powershell
python scripts/run_tests.py --pattern test_pdf_attachments.py --temp-dir analysis-local/test-temp-proxima --output testes/resultados/anexos-proxima-rodada.json
```

Uma primeira tentativa falhou no `setUp` por `WinError 5` na pasta temporária
do sandbox; os testes foram executados em pasta autorizada do projeto.
Isso foi uma restrição do ambiente, sem observação do Foxit nem evidência de
esgotamento de tokens. A suíte completa GTK/Linux não foi executada novamente.

O registro atual passa a **15 famílias com algum subconjunto e 10 propostas**;
o inventário continua com 25 famílias identificadas. O critério abrangente da
etapa 15 passa de `pending` a `partial`; não há critério novo nem alteração de
pesos/revisão. Etapa 15 mantém **33,3% verificados**, roteiro **43,33%**, catálogo
original **209** e paridade **0/25**. Testes próprios sustentam esse backend,
sem demonstrar comportamento equivalente ao Foxit.

Próximo passo sem VM: integrar listagem/extração à UI em Linux e exercitar a
interface com o mesmo corpus; manter a recusa dos casos não suportados.
Portfólios, anexos por anotação e árvores complexas requerem contratos e testes
adicionais. A comparação com o Foxit permanece no
[registro de pendências](../progresso/pendencias-analises.md).
