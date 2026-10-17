# Linuxit PDF — continuidade do projeto

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
- O pacote atual é 0.1.1, branch Flatpak `devel`. Não declare versão estável,
  projeto completo ou 100% sem critérios verificados.
- A criação de worktrees não é necessária neste ambiente isolado.

Fonte: `docs/especificacao.md`, `docs/FOXIT-REA.md`, `docs/proveniencia-base.json`.
Testes: `scripts/run_tests.py` (GUI requer X11/Wayland); 37 casos históricos do
marco 0.1.1, 14 testes do backend de anexos e 14 do controlador portável.
Quatro testes GTK do painel estão sem execução; suíte completa não repetida.
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

Trabalho atual autorizado: avançar a parte estática da etapa 11 enquanto o
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

A pedido do usuário em 16/10/2026, ao concluir cada rodada registre uma nota em
`progresso/notas-continuidade.md`, com data e horário reais de São Paulo no
formato `AAAA/MM/DD às HH:mm (America/Sao_Paulo, UTC-03:00)`. Informe o que foi
feito, ferramentas/perfis, evidências locais e publicáveis, verificações,
limitações, estado Git/publicação e o próximo passo concreto. Acrescente novas
notas ao final; preserve notas anteriores. Não dependa do histórico do chat.
Não declare publicação remota sem confirmação; registre bloqueios de acesso.
