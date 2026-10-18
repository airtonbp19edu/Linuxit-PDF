# Linuxit PDF — continuidade do projeto

Fonte e Flatpak **0.1.13/devel**, com [anotações adicionais](docs/ANOTACOES-AMPLIADAS.md):
sublinhado, tachado e ondulado por área, elipse e linha em qualquer direção.
Aparência vetorial própria vermelha. Edição de comentário/autor e exclusão
restritas a oito tipos simples desbloqueados, sem vínculos ou dependentes.
Rascunho com desfazer/refazer; original e cópias salvas preservados.

**400/400 testes próprios por ambiente**: fonte, payload e sandbox instalado,
sem falhas/erros/skips. Novos: 14 portáveis e seis GTK/Poppler; todos os 380 IDs
anteriores preservados. 106 arquivos app e 11 relatórios CI conferidos;
smoke 5/5 e launcher 3/3. Publicação confirmada; auditoria independente do mesmo bundle aprovada com
sete controles e cinco novos smoke checks, sem rebuild.
Os testes próprios não são paridade Foxit; pacotes/relatórios anteriores preservados.

[TIFF multipágina](docs/TIFF-MULTIPAGINA.md), até 100 páginas na criação, e
[OCR local](docs/OCR-LOCAL.md), até 20 páginas, preservados. Demais anotações,
formulários e famílias completas permanecem abertos. Pastas sincronizadas:
controles fora HOME negado/concedido passaram novamente; cliente real,
portal/concessão persistente, AT-SPI e impressão física ainda pendentes, sem VM Foxit.

Arquitetura: 44 módulos/58 interfaces; catálogo: 323 (152 REA + 171 diretas),
23 subconjuntos/duas propostas em 25 famílias. Índice histórico do checklist:
**43,93%**, 38 done/20 abertos. Conclusão global da recodificação indeterminada;
paridade **0/25**, cobertura global desconhecida. Original não executado.
APIs de nuvem adiadas/IA excluída. Não reiniciar análises preservadas.

Medição revisada em 18/10/2026: [explicação e evidências](docs/MEDICAO-PROGRESSO.md).
Não apresentar 43,93% como percentual do código reconstruído. Critérios parciais
pontuam zero no índice antigo; relatar entregas e operações pendentes em separado.
Testes, módulos e famílias com subconjuntos não são denominador de conclusão.

VM: último diagnóstico histórico com NEM/Snail, Integridade da Memória ativa e
NAT então ativo; offline não validado. Usuário pediu continuar sem VM. Nenhuma
VM, rede ou proteção Windows alterada nesta rodada. Validar isolamento antes
de executar original; detalhes nas notas anteriores.

Instruções permanentes e registros de marcos anteriores abaixo; a síntese acima
e as notas mais recentes definem o estado atual.

Ponto de retomada e estado do ambiente local: `docs/RETOMADA.md`.
Desenvolva e teste pelo código-fonte no Linux; gere Flatpak nos marcos de
entrega, conforme a preferência confirmada pelo usuário em 16/10/2026.

Leia primeiro `progresso/projeto.json`, `progresso/progresso.json`,
`progresso/tarefas-pendentes.md`, `progresso/matriz-paridade.csv` e Git local/remoto.
Não reinicie análises já preservadas. O destino autorizado é este repositório;
Linux/Flatpak tem prioridade, com Windows posteriormente. UPDF permanece fora
do escopo. O pedido mestre autoriza reconstrução incremental, testes e pushes
progressivos; a antiga limitação a somente análise foi ampliada por esse pedido.

Decisão do usuário em 17/10/2026: assistente de IA do Foxit e recursos
generativos estão fora da engenharia reversa, implementação e paridade.
Fonte: `docs/ESCOPO.md` e `scope_exclusions` de `progresso/projeto.json`.
Preservar o inventário histórico de AiAssistant.fpi; não criar alvos/cenários
ou funcionalidades de IA. As 25 famílias atuais permanecem, com operações
PDF e colaboração sem IA no escopo. Pesos e critérios não foram alterados.

- Preserve trabalho de outros colaboradores, sem reset destrutivo ou force push.
- Use REA/Ghidra com seus comandos realmente disponíveis. Registre identidades,
  perfis, falhas, inferências e lacunas; não conte slots como funções únicas.
- Os originais e resultados completos ficam fora do Git. Não incorpore código,
  DLLs, templates ou recursos Foxit à implementação e não contorne proteções.
- A base própria MIT Winux/Print&View e o pypdf BSD têm licenças/proveniência
  preservadas. Reaproveitamento da base não é nova recuperação do Foxit.
- Execute o original somente na contenção offline documentada, com mounts
  mínimos e prefixo sintético. Falhas do Wine não são comportamento do Foxit.
- Testes próprios não contam como paridade diferencial. O universo completo
  de funcionalidades ainda é aberto; cobertura global desconhecida fica nula.
- Atualize verificações e progresso por marco. `scripts/update_progress.py`
  calcula os pesos fixados; mudar critérios/pesos requer histórico explícito.
  Uma atividade `done` exige evidência técnica examinada, além de arquivo existente.
- Publique cada marco autorizado e confirme o remoto. O comprovante final pode
  ser gerado por `scripts/verify_git_sync.py` fora da árvore, evitando autorreferência.
- O último pacote publicado é 0.1.13 de desenvolvimento, branch Flatpak `devel`. Não declare versão estável,
  projeto completo ou 100% sem critérios verificados.
- A criação de worktrees não é necessária neste ambiente isolado.

Fonte: `docs/especificacao.md`, `docs/FOXIT-REA.md`, `docs/proveniencia-base.json`.
Testes: `scripts/run_tests.py` (GUI requer X11/Wayland). Atual0.1.3:
114/114 na fonte Linux, payload e Flatpak instalado, zero falhas/erros/skips;
inclui três métodos de geometria lateral, cinco do painel e sete do auditor.
Recorte lateral corrigido e capturas examinadas. Desktop/acessibilidade,
portais/impressão física pendentes; pedido 760 resulta924 por outros controles.
Empacotamento: `scripts/build_flatpak.py`; não misture bibliotecas nativas com
`/app/lib` padrão. Use `runtime-lib`, loader pareado e módulos OpenSSL incluídos.
A instalação em desktop e o cenário do sandbox estão em `docs/instalacao.md`.

Marcos de busca/impressão: `docs/REA-BUSCA-IMPRESSAO.md` e metadados vinculados.
Catálogo atual: 209 entradas (152 REA + 57 adicionais diretas), cobertura global
indeterminada. Wine/QEMU passa no controle x86; o Foxit carrega mas termina com
CInvalidArgException antes da UI. Não confunda isso com paridade funcional.
Em Linux, use `/usr/bin/python3` para GTK/Cairo (Python 3.13); o Python do PATH pode ser
3.12 e não carrega as extensões do sistema. Os pesos do roteiro não mudaram.

Retomada Windows: `docs/REA-IMPRESSAO-WINDOWS.md`. REA 6.5.0/Ghidra 12.1.4/JDK 21
foram diagnosticados; a análise MCP do executável expirou em 600 s. Três novas
entradas foram examinadas pelo backend direto `-noanalysis`. O projeto dessa
rodada e as respostas completas estão em `analysis-local/`, ignorado pelo Git.
Use `scripts/analyze_foxit_headless.py` para o backend complementar e preserve
os manifestos anteriores ao gerar os metadados de uma nova rodada.

Continuação estática: `docs/REA-IMPRESSAO-CONSUMIDORES.md`. As seis entradas
pendentes de geometria/consumidores foram examinadas e conferidas com Capstone.
Projeto e resultados completos em `analysis-local/headless/windows-print-02`.
Próximos alvos e ressalvas de tipagem constam no relatório. O gerador de
metadados aceita `--round` para preservar a proveniência de cada rodada.

Checkpoint histórico da etapa 11, cujo trabalho estático segue autorizado enquanto o
usuário prepara a VM da etapa 10. Ver `docs/ETAPA-11.md`: nove entradas de
interface examinadas, dez associações contextuais conferidas e ambiguidade
dos IDs 7911/7913 preservada. Não promover tabelas/estados de templates a
comportamento observado. Próximos alvos e lacunas constam no relatório.

Em 17/10/2026 o usuário pediu também a etapa 12. Contratos estruturados em
`docs/especificacao-funcional.json`, registro derivado em
`docs/contratos-funcionais.md` e limites em `docs/ETAPA-12.md`: 25 famílias,
50 cenários planejados, 14 subconjuntos atuais e 11 propostas. Validar com
`scripts/validate_functional_spec.py --check-render docs/contratos-funcionais.md`.
Detalhamento parcial, fase A aberta; testes próprios e propostas não são
observações do original. Preparar casos executáveis por família enquanto a
VM não está disponível, preservando os indicadores e os critérios existentes.

Em 17/10/2026 o usuário pediu seguir a etapa 13 e registrar as pendências por
VM e possíveis limites de tokens. Ver `docs/ETAPA-13.md`,
`docs/arquitetura-componentes.json` e `progresso/pendencias-analises.md`/`.json`.
Os dois critérios de projeto da etapa 13 já estavam `done`; não aumentar os
indicadores por esta revisão. `scripts/check_architecture.py` confere os módulos,
25 famílias e todos os critérios ainda abertos. Marcas/legendas de mosaico
dependem de Cairo; a ausência desse import faz o ramo retornar sem as marcas.
Preservar a distinção entre VM, análise estática, implementação e runtime Linux.
Os timeouts documentados de 1.801,7 s e 600 s não comprovam esgotamento de tokens.
Só atribuir uma interrupção a tokens com evidência; causa desconhecida fica
`null`. Salvar checkpoint após cada lote de alvos e antes de trocar de etapa,
com resultados examinados/pendentes, perfil, evidências, próximo passo e Git.

Etapa 14 conferida em 17/10/2026: `docs/ETAPA-14.md`. O projeto já estava
criado; conservar base e licenças. `scripts/check_project.py` verifica pontos
de entrada e seis controles de worker, sem GTK/Foxit; resultados completos
em `analysis-local/project-stage14-2026-10-17/`. Os dois critérios já estavam
`done`; suíte Linux/GUI/Flatpak não foi repetida. Próxima etapa do roteiro: 15,
com contratos suficientes e dentro do escopo sem IA, mantendo as pendências.

Etapa 15 iniciada sem VM em 17/10/2026: `docs/ETAPA-15.md`. Backend próprio
`app/pdf_attachments.py` e comandos worker `attachments`/`extract-attachment`
listam/extraem anexos de catálogo plano por índice/hash, sem sobrescrita.
14 testes portáveis passaram. GUI, /Kids, portfólios, senha e anexos exclusivos
de anotações continuam pendentes; tamanho real só é limitado após decodificação.
Fonte em desenvolvimento após o Flatpak 0.1.1, sem pacote novo. Arquitetura atual:
20 módulos/13 interfaces; especificação atual: 15 subconjuntos/10 propostas.
Critério amplo da etapa 15 `partial`; pesos e roteiro 43,33% preservados.
Runner aceita `--pattern test_pdf_attachments.py --temp-dir <pasta-gravavel>`
e registra que a execução é parcial. Próximo passo: integrar em GTK/Linux e
validar a UI; comparação Foxit segue dependente da contenção offline.

Etapa 16 em 17/10/2026: `docs/ETAPA-16.md`. Painel Anexos ligado no código de
`app/main.py`, com Atualizar/Salvar selecionado e escolha de pasta. Coordenação
em `app/attachment_tasks.py`: carga sob demanda, gerações e seleção capturada
antes do diálogo; extração já autorizada pode concluir após trocar documento,
sem atualizar o status do novo. 14 testes portáveis passaram após corrigir
UTF-8 do subprocesso. Quatro testes reais GTK ficaram `skipped` por ausência
de GTK/tela; não declarar widgets/layout validados. WSL reconfirmado ausente.
Arquitetura atual: 21 módulos/15 referências de interfaces, nove fechamentos
sem gi/Cairo. Critério amplo da 16 `partial`, pesos e roteiro 43,33% preservados.
Fonte após o Flatpak 0.1.1, sem pacote novo. Próximo passo: executar os quatro
testes GTK e a suíte Linux com tela/Poppler, preservando relatórios anteriores.

A etapa 10 permanece pendente, conforme `docs/ETAPA-10.md`. O preparador
`scripts/prepare_foxit_dynamic.py` gera 20 cenários e kit offline sem executar o
original. Windows 11 Home local sem Sandbox, WSL ausente, usuário sem VM.
Preparação e testes do kit não contam como observação dinâmica; casos `not_run`.

## Notas de continuidade entre IAs

Retomada16/layout: `docs/ETAPA-16-LAYOUT.md`. Run39040860414, fonte
64f76865381b35b4f8204131ef547f210d5d09db. GtkPaned shrink=False preserva mínimo
lateral: antes mínimo221/divisor158/x=-63; depois divisor221/x=0. Mesmo oráculo
corrigido:0/10 antes,10/10 depois. Primeiro diagnóstico comparava só pai/filho
ambos deslocados; passed:true inicial não foi adotado. Três métodos GTK novos
cobrem cinco painéis/duas larguras, divisor/ocultação/leitura e anexo longo.
114/114 em cada suíte fonte/payload/sandbox, smoke 5/5, launcher 3/3. Versão0.1.3,
83 arquivos fonte/payload iguais; 2803 arquivos de dependências/149 pacotes
atribuídos. Relatórios em `testes/resultados/0.1.3/`; raw/logs ignorados em
`analysis-local/sidebar-release-artifact-12104530284/`. Capturas examinadas;
pedido 760 virou924 de largura real, não afirmar suporte real a 760. Notas20/21
abaixo são históricas quanto ao recorte; pesos/paridade/21 critérios abertos
preservados. Próximo passo: quatro subconjuntos Poppler no corpus preservado18;
original exige VM offline, desktop/portais/acessibilidade/impressão pendentes.

Etapa 21: `docs/ETAPA-21.md`. Auditor `scripts/audit_delivery.py`, receita
manual `delivery-audit.yml` e `scripts/ci_audit_delivery.sh`. Run 39039390847,
código 2e6671825317a7e7846193973113f090365db4f9: bundle 0.1.2 publicado
reinstalado sem rebuild, deployment/OSTree/runtime conferidos, bytes de 83
arquivos app e 2803 de dependências/214 ELF, 149 avisos presentes e hasheados.
Sete controles sintéticos e novo smoke instalado 5/5 passaram. Suíte completa
104/104 da20 não foi repetida; app, versão e bundles preservados. Relatórios em
`testes/resultados/etapa-21/`, raw em `analysis-local/stage21-artifact-12103157602/`.
37 critérios done recebem conferência de links, sem repetir toda REA; 21 abertos
em 14 etapas preservados. Critério de encerramento21 permanece pending (50%);
pesos/paridade intactos. Próximo trabalho sem VM: retomar16 para medir/corrigir
recorte lateral com GTK/captura, depois quatro subconjuntos Poppler no corpus da etapa 18.
O roteiro tem 21 etapas; VM original, fase A e implementação ainda abertas.

Etapa 20: `docs/ETAPA-20.md`, entrega 0.1.2/devel. Workflow manual
`.github/workflows/linux-flatpak.yml` em Debian 13, Xvfb/Openbox e sandbox Flatpak
aninhado no runner efêmero; não alterar Windows ou executar Foxit no CI.
Run 39037892892, fonte e8f9c2e4f48dfc1e5b3cf2a8a6cfe97edb0ee899: 104/104 em
cada suíte fonte/payload/sandbox, 83 arquivos fonte/payload iguais, smoke 5/5,
launcher 3/3. Runtime auditado: 2803 arquivos, 214 ELF e 149 pacotes Debian
com avisos; `runtime-origins.json` acompanha o bundle/relatórios. Cinco casos GTK passaram; recursão dos botões laterais corrigida.
Bundle SHA-256 9d29459d7aff8ca6859cda0846cd698d285b36c3a8de2f463ff87002740cd7ba.
Relatórios em `testes/resultados/0.1.2/`, raw em
`analysis-local/stage20-artifact-12103031377/`. Captura examinada mostra
cabeçalho lateral recortado; acessibilidade sem bus AT-SPI no CI não validada.
Fonte/testes atuais superam as pendências de GTK/pacote das notas históricas
15/16/17/19 abaixo. A campanha de 17 subconjuntos no mesmo corpus da etapa 18
não foi repetida nesta rodada; preservar kit da VM. Critérios/pesos e paridade
não mudaram. Próximo roteiro: 21, auditoria incremental sem encerrar obrigações.

Etapa 19: `docs/ETAPA-19.md`. Normalização de impressão em `app/imposition.py`
agora desvincula a cópia da referência indireta e desloca conteúdo/caixas para
a origem do CropBox após rotação. Corrige deslocamento e mutação do stream do
reader em memória; não deriva geometria Foxit. Nove testes portáveis passaram
em `tests/test_imposition_cropbox.py`; mosaico foi testado sem marcas/legendas.
Regressão copiou os mesmos oito arquivos da etapa 18: 13 subconjuntos aprovados,
quatro bloqueados por Poppler. Dados em `analysis-local/stage19-measurements/`;
kit anterior da VM preservado. Snapshots antigos não aprovam esta nova fonte;
GTK/Linux completo e novo Flatpak continuam pendentes. Critério diferencial
da 19 segue pending; pesos, paridade e versão publicada preservados.

Etapa 18: `docs/ETAPA-18.md`, `testes/plano-comparativo.json` e
`scripts/run_comparison_campaign.py`. São 17 subconjuntos ligados a D01–D20;
13 verificações próprias passaram e quatro dependem de Poppler. Dezesseis
controles do comparador passaram; são dados sintéticos, nunca observação Foxit.
Conservar `analysis-local/comparison-stage18-final/` e seu corpus para a VM.
Importador exige hash de fixture/protocolo/evidência e registro de contenção;
igualdade de medidas manuais não aprova automaticamente uma família. Os 20
casos dinâmicos e 50 de aceitação continuam sem execução completa; critérios
diferenciais da etapa 18 pendentes, pesos e paridade 0/25 preservados.

Etapa 17: `docs/ETAPA-17.md` e `scripts/check_intermediate.py`. Criar diretórios
e relatórios novos por rodada. `portable` compila/testa uma cópia de `app/`,
sem aprovar GUI/Linux. `linux` exige dependências/tela X11, suíte completa sem
skips e smoke GTK. Critérios históricos `done` da 17 pertencem à versão 0.1.1;
a revalidação da fonte posterior é separada e ainda parcial. Não atualizar o
manifesto da versão publicada sem gerar/testar um novo pacote.

A pedido do usuário em 16/10/2026, ao concluir cada rodada registre uma nota em
`progresso/notas-continuidade.md`, com data e horário reais de São Paulo no
formato `AAAA/MM/DD às HH:mm (America/Sao_Paulo, UTC-03:00)`. Informe o que foi
feito, ferramentas/perfis, evidências locais e publicáveis, verificações,
limitações, estado Git/publicação e o próximo passo concreto. Acrescente novas
notas ao final; preserve notas anteriores. Não dependa do histórico do chat.
Não declare publicação remota sem confirmação; registre bloqueios de acesso.
