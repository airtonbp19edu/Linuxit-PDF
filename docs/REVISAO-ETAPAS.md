# Revisão das 21 etapas — 17/10/2026

A revisão manteve **43,33% do roteiro**, **37 critérios concluídos e 21 abertos
em 14 etapas**. As etapas **02, 04, 06, 13, 14, 17 e 20** têm todos os seus
critérios registrados concluídos. Isso descreve os critérios delimitados de
cada etapa; não significa implementação completa nem equivalência ao Foxit.
Paridade diferencial: **0/25 famílias**. Cobertura global de engenharia reversa:
**indeterminada**. A IA continua fora do escopo.

O pacote atual é **0.1.3/devel**. Nesta revisão, ele foi reinstalado em Linux
sem reconstrução e passou na auditoria dos arquivos e no smoke de funcionamento.
Os **114 testes próprios por ambiente** pertencem à execução anterior de
fonte/payload/sandbox, run 39040860414; seus relatórios selados foram conferidos,
sem repetir a suíte completa nesta revisão.

## Situação por etapa

| Etapa | Critérios verificados | Evidência examinada e pendência |
|---|---:|---|
| 01 — Diagnóstico | 80% | Perfis históricos REA/Ghidra e Git conferidos. API da branch retornou `protected:false`; três endpoints de regras retornaram 403. Consulta detalhada continua `unknown`, sem alterar proteções ou plano. |
| 02 — Arquivos | 100% | Inventário tem 3.276 caminhos únicos e hashes; 141 módulos PE correspondem ao inventário. Hash do executável local reconferido. Não foram relidos todos os arquivos originais nesta rodada. |
| 03 — Tecnologia | 50% | Fronteiras Win32/MFC, plugins e Lucene documentadas. Motor PDF e demais subsistemas ainda não estão totalmente delimitados. |
| 04 — Extração | 100% | Relatório histórico registra 3.276/3.276 arquivos iguais ao ZIP, sem diferenças; os 869 registros FX correspondem aos hashes do inventário. Extração/decodificação não repetidas. |
| 05 — Dependências | 42,9% | 141 módulos e 1.503 arestas de importação coerentes. Resolução estática não comprova carregamento nem ciclo de vida completo. |
| 06 — Estática inicial | 100% | Manifestos, recursos e mapa de comandos preservados e examinados. Este critério cobre investigação inicial, sem fechar a análise profunda. |
| 07 — Catálogo | 33,3% | 209 IDs distintos: 152 REA e 57 do backend direto. As 717 tabelas/9.973 posições estruturais não são funções únicas nem denominador global. |
| 08 — Descompilação | 13,0% | 28 slots da interface de índice, contratos parciais de busca/impressão e seis consumidores posteriores registrados. Tipos, algoritmos e demais famílias continuam abertos. Não houve nova descompilação. |
| 09 — Fluxos | 9,1% | Fluxos parciais documentados. Arestas, estados e algoritmos completos ainda faltam; diagramas não provam execução. |
| 10 — Dinâmica | 0% | Preparação e 20 cenários preservados, todos sem observação Foxit. VM/contenção offline utilizável ainda pendente segundo o último diagnóstico e retorno do usuário; não foi feita nova detecção de VM. |
| 11 — Interface original | 25% | Nove rotinas de UI e nove ligações de checkbox examinadas historicamente; IDs 7911/7913 continuam ambíguos. Recursos estáticos não comprovam disponibilidade/comportamento. |
| 12 — Especificação | 12,5% | Validador atual passou: 25 famílias, 15 subconjuntos atuais, dez propostas e 50 casos completos `not_run`. Referência original e fase A continuam abertas. |
| 13 — Arquitetura | 100% | Validação estrutural atual: 21 módulos, 15 referências de interfaces, 25 famílias e nove fechamentos sem GTK/Cairo. Critérios de projeto concluídos; implementação permanece parcial. |
| 14 — Projeto | 100% | Base MIT e pypdf BSD preservados. Seis controles de worker novamente aprovados no Windows; não equivalem à execução GUI local. |
| 15 — Lógica | 33,3% | Busca/imposição e anexos planos têm testes próprios. Suíte Linux 0.1.3 inclui 14 métodos do backend e 14 do controlador. /Kids, portfólios, senha não vazia, anexos por anotação e outras famílias permanecem abertos. |
| 16 — UI e integrações | 33,3% | Cinco métodos GTK de anexos e três de layout passaram no 0.1.3; geometria anterior 0/10 e corrigida 10/10. Largura solicitada 760 resultou em 924 px reais. Desktop, portais, acessibilidade e demais integrações continuam pendentes. |
| 17 — Intermediária | 100% | Relatórios selados confirmam 114/114 na fonte Linux, payload e sandbox 0.1.3, sem falhas/erros/skips. Nova auditoria instalou o mesmo bundle e passou no smoke; suíte completa não repetida nesta revisão. |
| 18 — Comparativos | 10% | Campanha preservada: 13 subconjuntos próprios passaram, quatro dependem de Poppler no mesmo corpus; 16 controles sintéticos históricos. Zero comparações reais com o original. Os 114 testes gerais não encerram esses quatro subconjuntos. |
| 19 — Correções | 14,3% | Regressões próprias de CropBox/mutação, recursão GTK e recorte lateral corrigidas e testadas. Divergências Foxit ainda não foram medidas. |
| 20 — Pacotes | 100% | Quatro bundles têm checksums conferidos. Entrega 0.1.3 publicada, instalada e exercitada; branch `devel`, sem declaração de versão estável ou publicação Flathub. |
| 21 — Auditoria | 50% | Auditoria instalada 0.1.3 passou: 83 arquivos da aplicação, 2.803 de dependências, 214 ELF e 149 arquivos de licença/créditos. Sete controles e cinco verificações de smoke passaram. Encerramento permanece pendente pelos 21 critérios abertos. |

As porcentagens seguem os pesos originais e contam somente critérios `done`.
As sete etapas com 100% não foram convertidas em novas recuperações do Foxit.
O [registro estruturado](../testes/resultados/revisao-etapas-2026-10-17/review.json)
liga cada etapa às evidências e aos limites da revisão.

## Inconsistências corrigidas

- A matriz de anexos ainda dizia “4 GTK cases not run”. Agora distingue os
  14 testes do backend, 14 do controlador e cinco métodos GTK aprovados na
  suíte 0.1.3, preservando portfólios e demais limitações.
- O início de `FOXIT-REA.md` chamava 191 entradas de catálogo atual. O total
  atual é 209; os relatórios das rodadas anteriores mantêm suas contagens.
- Notas atuais de progresso ainda apontavam 14 subconjuntos/11 propostas,
  arquitetura 19/11 e runtime 0.1.2. Foram atualizadas para o estado atual,
  com os relatórios históricos preservados.
- Os guias de retomada agora identificam explicitamente seus checkpoints
  anteriores e apontam esta revisão. Os testes GTK e o pacote já aprovados
  não permanecem como tarefas atuais por causa de uma nota antiga.
- A auditoria de instalação era do 0.1.2. A nova execução verifica o 0.1.3;
  a evidência do 0.1.2 foi conservada separadamente.

## Evidência nova e limites

O [run 39042492785](https://github.com/airtonbp19edu/Linuxit-PDF/actions/runs/39042492785)
terminou com sucesso no commit `8cb933d0c1a230eef9d71f793a082832fd2b8164`.
Usou Debian 13, Xvfb/Openbox e sandbox Flatpak instalado em runner efêmero,
com usuário dedicado. O pacote conferiu com SHA-256
`9aa8abf269136f84ff7cb1e6e5e990490245bec26b06979a76926030b10d3120`.
O artefato 12103979848 teve seu ZIP conferido com o digest GitHub
`84da060de75273d665b1b24187235f41fc5c15d088630754fea5be4c29f050db`.

- [Instalação e dependências](../testes/resultados/revisao-etapas-2026-10-17/installed-delivery-audit.json),
  [repositório](../testes/resultados/revisao-etapas-2026-10-17/repository-audit.json),
  [controles](../testes/resultados/revisao-etapas-2026-10-17/auditor-controls.json)
  e [smoke novo](../testes/resultados/revisao-etapas-2026-10-17/published-bundle-smoke.json).
- [Conteúdo das evidências históricas](../testes/resultados/revisao-etapas-2026-10-17/historical-evidence-review.json),
  [arquitetura atual](../testes/resultados/revisao-etapas-2026-10-17/architecture.json)
  e [seis controles de worker](../testes/resultados/revisao-etapas-2026-10-17/project.json).
- [Consultas remotas somente leitura](../testes/resultados/revisao-etapas-2026-10-17/remote-rules.json):
  HTTP 403 nos detalhes de regras; nenhum ajuste de segurança ou conta realizado.

Logs e resultados completos estão nas pastas ignoradas
`analysis-local/stage21-artifact-12103979848/`,
`analysis-local/stage21-logs-39042492785/` e
`analysis-local/stage-review-2026-10-17/`.

Os 37 critérios `done` receberam conferência de referências; o conteúdo dos
inventários/contratos acima também foi examinado. Isso não reexecuta toda a
engenharia reversa histórica. O Foxit não foi executado, não houve novas
observações REA/Ghidra e os binários/código/recursos do original continuam fora
da implementação e do Git. Não foi identificado esgotamento comprovado de tokens.

## Próximos passos

1. Sem VM: repetir em Linux os quatro subconjuntos Poppler da etapa 18 usando
   os mesmos oito arquivos de `analysis-local/comparison-stage18-final/input/`,
   sem modificar o corpus ou confundir isso com observação Foxit.
2. Prosseguir com alvos estáticos e contratos pendentes de busca/impressão;
   ampliar implementação por família com critérios próprios executáveis.
3. Validar desktop real, portais, acessibilidade e impressão física; tratar a
   largura mínima de 924 px separadamente do recorte lateral já corrigido.
4. Quando houver VM offline validada, observar o original no corpus preservado,
   importar as evidências e medir paridade/divergências. Os 20 casos dinâmicos
   e os 50 cenários completos continuam sem execução completa.

Cada nova rodada deve acrescentar sua nota datada, evidência e confirmação
remota. Esta revisão não cria uma etapa 22 nem encerra as obrigações restantes.


Publicação da revisão confirmada em 17/10/2026 às 15:05
(America/Sao_Paulo, UTC-03:00), commit
[`496c8a6`](https://github.com/airtonbp19edu/Linuxit-PDF/commit/496c8a6a9db59206dff5d3f092a092556031af06).
HEAD local/remoto iguais e árvore limpa após o push. Na conferência dos blobs
Git, os hashes de dois relatórios locais Windows foram ajustados à serialização
LF do repositório; conteúdo técnico e quatro relatórios CI permaneceram iguais.
A nota de confirmação e esse ajuste de metadados seguem em commit posterior;
o HEAD final é verificado por recibo externo, sem autorreferência.
