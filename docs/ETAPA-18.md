# Etapa 18 — preparação dos testes comparativos

Em **17/10/2026**, a campanha existente D01–D20 ganhou **17 verificações de
subconjuntos do backend**, definidas em
[`testes/plano-comparativo.json`](../testes/plano-comparativo.json).
[`scripts/run_comparison_campaign.py`](../scripts/run_comparison_campaign.py)
gera o mesmo corpus sintético da etapa 10 e registra medidas reais do Linuxit
em subprocessos. O código do aplicativo não foi alterado nesta rodada.

**13 verificações passaram; quatro ficaram bloqueadas pela falta de
`pdftotext` neste Windows.** Nenhum Foxit foi executado ou observado. Os 20
casos dinâmicos completos, os dez de interface e os 50 de aceitação continuam
sem execução completa; estas verificações não fecham aqueles casos.

## Resultados examinados

| Subconjunto | Medida própria registrada |
|---|---|
| D02, inspeção | Duas páginas; renderização não exercitada |
| D07, marcadores | Dois resultados em ordem: página 2 e destino local `null` |
| D08/D09, comentários | Conteúdo e assunto: um resultado na página 1; autor: zero |
| D11, variantes | Consulta vazia, termo inexistente e nenhuma fonte: zero resultados |
| D13/D14, entradas inválidas | Parser recusou PDF inválido e arquivo vazio; sem testar diálogos |
| D16, anexo | Arquivo salvo com 22 bytes e SHA-256 conferido, sem execução do conteúdo |
| D18, livreto | Quatro páginas; rótulos extraídos em ordem `8,1 / 2,7 / 6,3 / 4,5` |
| D18, quatro por folha | Duas páginas; rótulos `1,2,3,4 / 5,6,7,8` |
| D04/D05/D06/D10 | `blocked_runtime`, medidas `null`: extração de texto exige Poppler |

A ordem dos rótulos de impressão é a do **conteúdo extraído do PDF**, não uma
validação de posicionamento visual, margens ou geometria. Para comparar essa
medida com Foxit, é necessário um PDF de saída equivalente. Se só houver
prévia visual, a medida fica indisponível nesse contexto. Não usar impressoras
do host. As verificações portáveis também não validam GTK/Linux, persistência,
cancelamento durante trabalho ou impressão física.

O relatório relaciona as 25 famílias; seis têm verificações planejadas e as
demais permanecem sem adaptador. Isso não representa cobertura global. Todas
continuam `not_verified`; a IA permanece [excluída](ESCOPO.md).

## Executar e preservar uma campanha

No ambiente atual, ou em Linux com `/usr/bin/python3`, usar nomes novos:

```powershell
python scripts/run_comparison_campaign.py run --work-dir analysis-local/comparacao-nova --output testes/resultados/comparacao-nova.json
```

No Linux com Poppler, os quatro casos de texto podem ser executados sem a VM
do original. O resultado continua sendo uma observação própria, sem aprovar
GUI ou equivalência Foxit. Para GTK e a suíte completa, permanece o comando da
[etapa 17](ETAPA-17.md).

A pasta privada contém `input/`, `probes/` e
`foxit-observations-template.json`. O relatório salva hashes dos oito arquivos
do corpus, da fonte e do plano. Cada verificação tem um hash próprio de
protocolo, incluindo consulta, opções, versão da medida e instrução de medição.
Fonte/corpus são conferidos novamente ao final. Diretórios e relatórios
existentes são preservados; um erro de probe ou contrato próprio retorna erro.
Os valores observados são calculados pelo backend, separadamente dos esperados.

## Quando a VM offline estiver pronta

1. Manter a campanha original intacta. Na rodada local final, o plano e
   `observacoes-comparativas-template.json` já estão copiados em `input/`.
   Em campanhas novas, copiá-los **antes** de mapear essa pasta somente para
   leitura no guest. Usar exatamente esses PDFs; não regenerar o corpus entre
   as duas observações.
2. Seguir a contenção da [etapa 10](ETAPA-10.md): original somente leitura,
   perfil sintético, rede desconectada, controle de interface observado e
   somente a pasta dedicada de resultados gravável. O original não deve ser
   iniciado no perfil normal do host. Este runner não o inicia automaticamente.
3. Copiar o modelo para um arquivo novo em `C:\Linuxit\Results`. Registrar
   identidade do executável antes/depois, ambiente, timestamp com fuso e os
   três controles de sessão. Preencher cada item somente após observação real.
   Os estados são `not_run`, `observed`, `error`, `unavailable_in_context` e
   `inconclusive`. Medidas desconhecidas ficam `null`; `not_run` não tem evidência.
4. Um item `observed` exige as chaves de medidas exemplificadas no relatório,
   com valores medidos no original, e `evidence: [{"file": "caso/tela.png",
   "sha256": "..."}]`. O caminho é relativo à pasta de evidências local. Conferir
   hashes e conservar telas/logs completos fora do Git. Páginas são base 1;
   `null` em destino de marcador significa ausência de destino local, não página 0.
5. Importar o registro concluído, preservando os arquivos anteriores:

```powershell
python scripts/run_comparison_campaign.py compare --campaign testes/resultados/comparacao-nova.json --observations analysis-local/observacoes-foxit.json --evidence-root analysis-local/resultados-vm --output testes/resultados/comparacao-importada-nova.json
```

O importador recusa identidade, fixture ou protocolo divergentes, arquivo
de evidência ausente/alterado, caminho externo, dados incompletos, contagens
incoerentes e IDs duplicados/desconhecidos. Mudanças no protocolo da própria
campanha também são detectadas. Ausência, erro ou indisponibilidade do original
são inconclusivos; não viram uma falha funcional. Se o Linuxit estiver bloqueado,
também não há comparação.

Uma importação válida retorna **0 mesmo se houver diferenças**; consultar
`matches`, `differences` e os caminhos das diferenças. O estado
`match_recorded_metrics` significa somente igualdade das medidas registradas.
A evidência manual precisa ser examinada para confirmar o que foi observado;
seu hash prova integridade, não a origem nem a execução. O script nunca aprova
uma família inteira ou atualiza automaticamente a matriz de paridade.

## Evidências e continuidade

- [Campanha inicial](../testes/resultados/etapa-18-campanha-2026-10-17.json) e
  [campanha final](../testes/resultados/etapa-18-campanha-final-2026-10-17.json):
  ambas com 13 verificações próprias aprovadas e quatro bloqueadas. A segunda
  acrescenta validações de vínculo e o registro explícito dos 20 casos completos.
- [14 controles iniciais](../testes/resultados/etapa-18-controles-tests-2026-10-17.json)
  e [16 controles ampliados](../testes/resultados/etapa-18-controles-extended-tests-2026-10-17.json),
  todos aprovados. Usam dados/evidências sintéticos; não são observações Foxit.
- [Importação do modelo vazio](../testes/resultados/etapa-18-comparacao-sem-original-2026-10-17.json):
  **zero medidas do original, zero comparações, 17 aguardando o original**.
- [Conferência técnica](../testes/resultados/etapa-18-verificacao-2026-10-17.json):
  sintaxe de 117 arquivos, 91 links locais, três recusas CLI e hashes dos dois
  arquivos de instrução/modelo copiados para o corpus privado. Os 83 arquivos
  da aplicação e todos os critérios/status/pesos permanecem intactos.

Os dois critérios diferenciais continuam `pending`. O critério já concluído
de metodologia recebe estas evidências, sem alterar seu peso. Etapa 18 segue
**10%**, roteiro **43,33%**, paridade **0/25**, catálogo original **209** e
cobertura global desconhecida (`null`). Não houve Flatpak novo nem análise
REA/Ghidra nova. Nenhuma interrupção por tokens foi constatada.

Próximo passo: executar a campanha em Linux com Poppler e a validação GTK da
etapa 17. Quando a VM estiver pronta, observar o mesmo corpus e revisar as
evidências importadas. A etapa 19 só pode corrigir divergências Foxit depois
de medi-las; regressões próprias continuam separadas.
