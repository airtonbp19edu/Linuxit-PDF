# Avisos e situação do Linuxit PDF

Regra pedida pelo usuário em 20/10/2026: todo aviso dado ao usuário fica registrado aqui, no GitHub, e é copiado para a pasta local do projeto como `AVISOS-LOCAL.md`. Esse arquivo local é ignorado pelo Git para nunca bloquear um `git pull`. A seção "Situação atual" é substituída a cada atualização; o histórico de avisos só recebe novas entradas.

## Situação atual — 2026/10/20 às 12:52 (America/Sao_Paulo, UTC-03:00)

### Feito

**O aplicativo**
- Versão 0.1.16/devel publicada como Flatpak (prerelease no GitHub), auditada no mesmo arquivo sem recompilar. Na entrega passou em 564/564 testes próprios em cada ambiente: fonte Linux, pacote e sandbox instalado.
- Python + GTK, com 78 arquivos em `app/`. Das 111 operações do inventário, 98 têm algum código próprio (a 98ª é a leitura XFA da E06). Isso não é porcentagem de conclusão.
- Leitura e navegação, busca (texto, marcadores, comentários, anexos, índice, coringas, proximidade, radicais em 36 idiomas), anotações, formulários AcroForm com combo editável e cálculos limitados, anexos, impressão e imposição, OCR local, assinatura e verificação offline, proteção por senha, acessibilidade com voz local, camadas e mídia, pastas sincronizadas e integração com portal do desktop. Todos são recortes próprios com limites documentados.

**Nesta sessão (19–20/10/2026)**
- Defeito corrigido: a verificação de carimbo de tempo RFC 3161 falhava sempre com OpenSSL 3.0 (Ubuntu 24.04). Teste novo garante que a correção não confia em autoridades do sistema.
- Registros desatualizados corrigidos: 8 textos de escopo que diziam "pendente" para recursos já existentes, próximos passos antigos, a marcação do portal e a fila de tarefas.
- Testes de aceitação: o validador exigia que os 50 planos ficassem "não executados", o que impedia registrar avanço. Agora 46 casos rodam contra o aplicativo real, incluindo a janela GTK, com fixtures próprias fixadas por hash. O resultado fica ligado à revisão do código.
- Execução registrada: **59 de 59 casos aprovados** na revisão `033e245`, agora incluindo os 2 de nuvem pelo fluxo de pasta sincronizada. O CI no Debian 13 confirmou a E28: aceitação 59/59 e suíte 607/607. Suíte própria completa **607/607** no Ubuntu 24.04.
- Defeito de estabilidade corrigido (E27): o coletor de lixo do Python liberava widgets GTK em threads de trabalho, o que pode derrubar o aplicativo. Agora a coleta roda só na thread principal.
- Confirmado no CI Debian 13 ([execução 39363684386](https://github.com/airtonbp19edu/Linuxit-PDF/actions/runs/39363684386)): suíte **571/571**, aceitação **46/46** na revisão `a43e0ba`, campanha preservada 17/17, acessibilidade entre processos e portal nativo aprovados. Revisão em `testes/resultados/aceitacao/2026-10-20/ci-debian13-review.json`.
- Publicado no GitHub, com commits de autoria do Claude.
- REA 6.7.0 (morluto/rea) instalado no ambiente de nuvem do Claude. Esse ambiente é temporário; ver `claude/retomada-instalacao-rea.md` no projeto do claude.ai.

### Em andamento
- Nada em execução. Lista de etapas pequenas em [ETAPAS-PEQUENAS.md](ETAPAS-PEQUENAS.md): E01 a E07 e E25 a E28 concluídas. Aguardando você para a **E08**.

### Falta

**Sem VM, desenvolvimento próprio**
- Formulários: XFA dinâmico (só XFA), datas com nomes de mês ou horas, negativos em vermelho e JavaScript geral. Hoje há cálculos, validação de faixa, números, datas numéricas e máscaras declarativos, sem executar JavaScript, leitura dos campos XFA e preenchimento de XFA híbrido.
- Assinaturas: assinatura incremental e múltipla, DocTimeStamp, PAdES-LTV e OCSP.
- 3D: renderizador U3D/PRC. Hoje só lista e extrai.
- Redação definitiva e edição universal de anotações.
- Qualidade de OCR e ordem de leitura, conversões mais amplas e um corpus maior de PDFs danificados, cifras e fontes.

**Análise estática (Ghidra e o Foxit original ficam no PC Windows)**
- Chamadores, tipos e propriedade/liberação de objetos, partindo dos resultados preservados.
- O instalador do REA 6.7.0 no PC (`analysis-local\rea-instalacao\instalar-rea.cmd`) ainda não foi executado.

**Comparação com o Foxit (VM)**
- Testes suspensos desde que o relógio da VM parou em 09:54:23 de 19/10. Só retomar com a sua autorização.
- Equivalência comprovada em 0 de 25 famílias; casos D01–D20 e UI01–UI10 incompletos.

**Ambientes reais**
- Impressora física, áudio e leitor de tela, monitores físicos, cliente sincronizador real e materiais RMS. Windows completo vem depois do Linux.

**Entrega**
- Próximo pacote 0.1.17: Flatpak, testes nos três ambientes e auditoria, incluindo a correção RFC 3161.

**Medição**
- 19 dos 58 critérios das 21 etapas continuam abertos. O percentual global é desconhecido e não deve ser estimado.

**Decisões tomadas**
- D01: a régua passa a usar vírgula decimal (2,54 cm), etapa E25 concluída.
- D02: o teste de mídia instável virou a etapa E26, concluída: era um defeito real de reprodução, corrigido.
- D03: a queda intermitente do GTK no CI Debian 13 virou a etapa E27, concluída: causa provável encontrada e corrigida.

**Adiado e excluído**
- Nuvem: atendida pelo fluxo de pastas sincronizadas (E28, decisão de 17/10/2026). Login em provedor, envio por API e colaboração remota seguem adiados por decisão do usuário. Falta testar com um cliente sincronizador real.
- Recursos de IA estão excluídos.

## Histórico de avisos

- **2026/10/19 às 23:52** — Suíte completa rodada fora do CI; defeito RFC 3161 com OpenSSL 3.0 encontrado e corrigido com teste novo. Registros que diziam "pendente" para recursos existentes foram atualizados. GitHub ainda não vinculado para publicação.
- **2026/10/20 às 00:15** — Envio ao GitHub recusado: o app do Claude não estava instalado na conta. Opções: instalar em https://github.com/apps/claude/installations/select_target ou publicar pelo PC com `analysis-local\publicar-2026-10-20\publicar.cmd`.
- **2026/10/20 às 00:20** — Publicado: `main` em `a43e0ba`. Os 3 commits foram refeitos com autoria do Claude, para aparecerem como verificados, e os 46 casos de aceitação rodaram de novo na revisão `841557d`, todos aprovados. CI no Debian 13 iniciado. O `publicar.cmd` do PC deixou de ser necessário; basta `git pull`.
- **2026/10/20 às 00:22** — Regra registrada: avisos vão para este arquivo no GitHub e para `AVISOS-LOCAL.md` na pasta local.
- **2026/10/20 às 00:25** — CI no Debian 13 aprovado: suíte 571/571 e aceitação 46/46 na revisão `a43e0ba`, além da campanha preservada, acessibilidade e portal. Nada em andamento agora.
- **2026/10/20 às 00:27** — O que falta foi organizado em 24 etapas pequenas, com o que não precisa da VM primeiro: [ETAPAS-PEQUENAS.md](ETAPAS-PEQUENAS.md) no GitHub e `ETAPAS-LOCAL.md` na pasta local. Execução iniciada pela E01. Decisão D01 (vírgula decimal na régua) aguardando você.
- **2026/10/20 às 00:28** — E01 concluída (`9c10dc4`): o verificador do catálogo de operações voltou a passar, agora ligado à suíte 571/571 do CI Debian 13. O inventário renderizado também estava desatualizado e foi corrigido. Iniciando a E02.
- **2026/10/20 às 00:38** — E02 concluída (`353a30b`): a integração com o sistema ganhou contrato próprio e os casos S12-25 agora rodam com o portal real. Aceitação **48 de 50** aprovada; só a nuvem (adiada) fica de fora. Correção: alguns horários da E01/E02 tinham sido anotados adiantados e foram trocados pelos horários reais dos commits. Iniciando a E03.
- **2026/10/20 às 00:47** — CI no Debian 13 confirmou a E02: aceitação 48/48 (inclusive os dois casos com o portal real) e suíte 571/571.
- **2026/10/20 às 00:48** — E03 concluída (`0600b05`): formulários reconhecem formatação de números (ex.: R$ 2.469,00) e aceitam vírgula decimal na entrada, sem executar JavaScript. Aceitação 49/49, suíte 576/576. O verificador do catálogo deixou de quebrar a cada edição. Iniciando a E04.
- **2026/10/20 às 00:55** — CI no Debian 13 confirmou a E03 (49/49, suíte 576/576). E04 concluída (`34ebb46`): campos de data validam e formatam datas numéricas (1/2/2026 aparece como 01/02/2026) e recusam datas inexistentes como 31/02. Aceitação 51/51, suíte 579/579. Iniciando a E05.
- **2026/10/20 às 00:58** — Regra nova: depois de cada etapa, parar e esperar a sua confirmação antes de iniciar a próxima. Registrada no AGENTS.md e na lista de etapas.
- **2026/10/20 às 01:06** — CI no Debian 13 confirmou a E04 (51/51, suíte 579/579). E05 concluída (`e8cface`): máscaras especiais e livres (CEP 01310-100, CPF, telefone (555) 123-4567). Aceitação 53/53. Achado: um teste de mídia já existente falha de forma intermitente (1 em 3), sem relação com a E05; decisão D02 com você. Parado, aguardando a sua confirmação para iniciar a E06.
- **2026/10/20 às 01:08** — Decisões registradas: D01 → vírgula decimal na régua (etapa E25); D02 → tornar estável o teste de mídia (etapa E26). As duas foram colocadas logo depois da E05 na lista. Nada foi executado; aguardando você para continuar.
- **2026/10/20 às 01:13** — CI no Debian 13 confirmou a E05: aceitação 53/53 e suíte 583/583, sem falhas. Nenhuma etapa nova iniciada; aguardando você.
- **2026/10/20 às 10:05** — E25 concluída (`db8c6fe`): régua, janela de medidas e tamanho da página mostram vírgula decimal (2,54 cm; 21,0 × 29,7 cm). Suíte 584/584, aceitação 53/53. Parado, aguardando você para a E26.
- **2026/10/20 às 10:11** — CI no Debian 13 confirmou a E25: aceitação 53/53 e suíte 584/584. Nenhuma etapa nova iniciada; aguardando você para a E26.
- **2026/10/20 às 10:16** — Pedido: fazer as duas próximas da fila (E26 e E06) e parar.
- **2026/10/20 às 10:25** — E26 concluída (`5747278`): o teste instável revelou um defeito real. Um áudio curto podia "terminar" em milissegundos porque a reprodução começava antes de o som estar pronto. Corrigido para pré-carregar antes de tocar. Teste novo, 20 de 20 execuções seguidas, suíte 585/585, aceitação 53/53. Iniciando a E06.
- **2026/10/20 às 10:43** — E06 concluída (`06daa9d`): o aplicativo detecta formulários XFA e mostra os campos e valores em uma janela somente leitura (menu "Campos de formulário XFA…"), sem executar scripts. Suíte 595/595, aceitação 55/55. CI da E26: confirmada no Debian 13 na revisão `95a46ba` (suíte 585/585, aceitação 53/53). Antes disso, duas execuções caíram por uma falha nativa do GTK num teste de comentários, sem relação com a E26; ligado o registro de pilha e aberta a decisão D03 para você. Parado, aguardando você para a E07 e a D03.
- **2026/10/20 às 10:49** — CI no Debian 13 confirmou a E06: aceitação 55/55 e suíte 595/595, sem quedas. Nenhuma etapa nova iniciada; aguardando você para a E07 e a decisão D03.
- **2026/10/20 às 10:54** — Decisão D03: investigar a queda do GTK como etapa própria (E27) e, em seguida, fazer a próxima da fila (E07). Iniciando a E27.
- **2026/10/20 às 12:25** — E27 concluída (`79851e9`). A queda não se repetiu em cerca de 70 execuções, inclusive num Debian 13 local e em 18 execuções de diagnóstico no CI. Mas a investigação achou a causa provável: o coletor de lixo do Python às vezes rodava numa thread de trabalho e liberava botões, listas e até janelas do GTK fora da thread principal (546 objetos numa suíte completa), o que o GTK não suporta. Correção: a coleta passa a rodar só na thread principal; a contagem caiu para 0. Suíte 600/600, aceitação 55/55, CI Debian 13 aprovado. Iniciando a E07.
- **2026/10/20 às 12:32** — E07 concluída (`aff57e0`): em formulários XFA híbridos, preencher um campo agora grava o mesmo valor nos campos comuns e nos dados XFA da cópia, inclusive valores calculados; a cópia é conferida antes de ser salva. Campos sem dado XFA correspondente e outras alterações em XFA são recusados. Suíte 607/607, aceitação 57/57. CI no Debian 13 em andamento. Parado, aguardando você para a E08.
- **2026/10/20 às 12:37** — CI no Debian 13 confirmou a E07: aceitação 57/57 e suíte 607/607, sem quedas. Nenhuma etapa nova iniciada; aguardando você para a E08.
- **2026/10/20 às 12:39** — Pedido: procurar a decisão sobre nuvem e fechar o ciclo. Encontrada a decisão de 17/10/2026 às 20:51: usar pastas sincronizadas por programas externos; o Linuxit só trabalha com arquivos locais. Os 2 casos de aceitação de nuvem que faltavam ainda descreviam um provedor remoto simulado. Criada a etapa E28 para trocar esses casos pelo fluxo escolhido e executá-los. Login, envio por API e colaboração remota seguem adiados.
- **2026/10/20 às 12:47** — E28 concluída (`033e245`): o ciclo da nuvem foi fechado com a sua decisão de 17/10/2026 (pastas sincronizadas por programas externos). Os 2 casos de nuvem agora testam esse fluxo na janela real: abrir da pasta, salvar cópia que só se declara salva localmente, bloquear quando o sincronizador troca o PDF aberto e nunca sobrescrever arquivo criado por ele. Aceitação 59/59 (todos os planos), suíte 607/607. Login, envio por API e colaboração remota seguem adiados. CI no Debian 13 em andamento. Parado, aguardando você para a E08.
- **2026/10/20 às 12:52** — CI no Debian 13 confirmou a E28: aceitação 59/59 e suíte 607/607. Nenhuma etapa nova iniciada; aguardando você para a E08.
