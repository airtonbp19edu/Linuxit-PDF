# Avisos e situação do Linuxit PDF

Regra pedida pelo usuário em 20/10/2026: todo aviso dado ao usuário fica registrado aqui, no GitHub, e é copiado para a pasta local do projeto como `AVISOS-LOCAL.md`. Esse arquivo local é ignorado pelo Git para nunca bloquear um `git pull`. A seção "Situação atual" é substituída a cada atualização; o histórico de avisos só recebe novas entradas.

## Situação atual — 2026/10/20 às 17:14 (America/Sao_Paulo, UTC-03:00)

### Feito

**O aplicativo**
- Versão **0.1.17/devel** publicada como Flatpak (prerelease `v0.1.17-devel` no GitHub), auditada no mesmo arquivo sem recompilar, com download público conferido e integrações de desktop 9/9 em duas repetições. Na entrega passou em 616/616 testes próprios em cada ambiente: fonte Linux, pacote e sandbox instalado. As etapas E12–E15 já estão no código, mas ainda não num pacote publicado.
- Python + GTK, com 79 arquivos em `app/`. Das 111 operações do inventário, 98 têm algum código próprio (a 98ª é a leitura XFA da E06). Isso não é porcentagem de conclusão.
- Leitura e navegação, busca (texto, marcadores, comentários, anexos, índice, coringas, proximidade, radicais em 36 idiomas), anotações, formulários AcroForm com combo editável e cálculos limitados, anexos, impressão e imposição, OCR local, assinatura e verificação offline, proteção por senha, acessibilidade com voz local, camadas e mídia, pastas sincronizadas e integração com portal do desktop. Todos são recortes próprios com limites documentados.

**Nesta sessão (19–20/10/2026)**
- Defeito corrigido: a verificação de carimbo de tempo RFC 3161 falhava sempre com OpenSSL 3.0 (Ubuntu 24.04). Teste novo garante que a correção não confia em autoridades do sistema.
- Registros desatualizados corrigidos: 8 textos de escopo que diziam "pendente" para recursos já existentes, próximos passos antigos, a marcação do portal e a fila de tarefas.
- Testes de aceitação: o validador exigia que os 50 planos ficassem "não executados", o que impedia registrar avanço. Agora 46 casos rodam contra o aplicativo real, incluindo a janela GTK, com fixtures próprias fixadas por hash. O resultado fica ligado à revisão do código.
- Execução registrada: **73 de 73 casos aprovados** na revisão `61f180e`. O CI no Debian 13 confirmou a E14 (aceitação 71/71, suíte 630/630); CI no Debian 13 confirmou a E15 (73/73, 638/638). Suíte própria completa **638/638** no Ubuntu 24.04.
- Defeito de estabilidade corrigido (E27): o coletor de lixo do Python liberava widgets GTK em threads de trabalho, o que pode derrubar o aplicativo. Agora a coleta roda só na thread principal.
- Confirmado no CI Debian 13 ([execução 39363684386](https://github.com/airtonbp19edu/Linuxit-PDF/actions/runs/39363684386)): suíte **571/571**, aceitação **46/46** na revisão `a43e0ba`, campanha preservada 17/17, acessibilidade entre processos e portal nativo aprovados. Revisão em `testes/resultados/aceitacao/2026-10-20/ci-debian13-review.json`.
- Publicado no GitHub, com commits de autoria do Claude.
- REA 6.7.0 (morluto/rea) instalado no ambiente de nuvem do Claude. Esse ambiente é temporário; ver `claude/retomada-instalacao-rea.md` no projeto do claude.ai.

### Em andamento
- **E29 prioritária:** Codex sincronizou a cópia local e preservou a nota local do laboratório. Causa confirmada no CI 39490423511: mesmo token cria rascunhos na main (201/201), mas recusa o commit antigo com workflows diferentes (403). Dois rascunhos apagados e nenhuma release/tag pública alterada. Fluxo corrigido com conferência prévia e reconhecimento de versões já publicadas; validação somente leitura em andamento. Próxima publicação real permanece pendente e não será feita nesta etapa.
- **PRIORIDADE (pedido do usuário em 2026/10/20 às 17:09, America/Sao_Paulo):** antes de qualquer outra etapa, identificar por que o token do GitHub Actions recebe **HTTP 403 ao criar releases** (E29). Instruções, fatos já verificados e diagnóstico sugerido em [PRIORIDADE-E29-ERRO-403-RELEASE.md](PRIORIDADE-E29-ERRO-403-RELEASE.md). A 0.1.17 já está publicada; não publicar nem apagar releases. Pedido ao Codex; o Claude retoma às 20:10.
- Lista de etapas pequenas em [ETAPAS-PEQUENAS.md](ETAPAS-PEQUENAS.md): E01 a E07 e E25 a E28 concluídas. Bloco autorizado E08 a E11: E08, E09 e E10 concluídas. **E11 concluída**: 0.1.17 publicada, baixada e auditada.
- Retomada das 15:00 recebida: E08 a E10 prontas e a E11 só depende da sua publicação. Bloco E12 a E15 concluído. Erro de CI da E08 resolvido e confirmado no CI (execução 39483614911: 638/638, sem pulos). Parado, aguardando você.

### Falta

**Sem VM, desenvolvimento próprio**
- Formulários: XFA dinâmico (só XFA), datas com nomes de mês ou horas, negativos em vermelho e JavaScript geral. Hoje há cálculos, validação de faixa, números, datas numéricas e máscaras declarativos, sem executar JavaScript, leitura dos campos XFA e preenchimento de XFA híbrido.
- Assinaturas: gravar DSS (LTV), OCSP e criar carimbos (feitos: assinaturas múltiplas E08, verificação de carimbo de documento E09 e uso do DSS na validação E10).
- 3D: renderizador U3D/PRC. Hoje só lista e extrai.
- Redação sem rasterizar a página (hoje a página marcada vira imagem) e edição universal de anotações. Marcar e aplicar redação já existem (E14 e E15).
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
- **2026/10/20 às 13:29** — Pedido: fazer as 4 próximas etapas (E08 a E11) e agendar retomada às 15:00. Agendado. Se o bloco não terminar até lá, retomo de onde parou; se terminar, às 15:00 sigo com as próximas 4 que não dependem da VM, do PC ou de equipamentos (E12 a E15) e paro. Iniciando a E08.
- **2026/10/20 às 13:47** — E08 concluída (`ae429cd`): já é possível assinar um PDF que já tem assinatura. A nova assinatura é anexada ao final do arquivo, sem mexer nos bytes assinados, e as anteriores continuam válidas para a versão delas (conferido também pelo pdfsig do poppler, com três assinaturas seguidas). Certificação que proíbe alterações e assinatura anterior inválida são recusadas com o motivo. Suíte 610/610, aceitação 61/61. Iniciando a E09.
- **2026/10/20 às 15:09** — E09 concluída (`df7207a`): o aplicativo reconhece e verifica carimbos de tempo de documento já presentes no PDF, sem rede; o horário só aparece se o carimbo conferir com o arquivo, e a autoridade só é confiável pela CA que você escolher. Suíte 613/613, aceitação 63/63. Aviso: o CI da E08 falhou porque um teste dependia do qpdf, que não existe no CI e foi pulado (a suíte não aceita testes pulados). O teste foi refeito sem essa dependência (`9e75c0c`) e o CI foi disparado de novo. Iniciando a E10.
- **2026/10/20 às 15:19** — E10 concluída (`ba38ca7`): a verificação offline usa os certificados e as listas de revogação guardados dentro do PDF (DSS) para fechar a cadeia até a CA que você escolher e checar revogação, sem rede; esses certificados nunca passam a ser confiáveis por conta própria. Suíte 616/616, aceitação 65/65. O CI confirmou E08 e E09 (63/63, 613/613). Iniciando a E11 (entrega 0.1.17).
- **2026/10/20 às 15:25** — CI no Debian 13 confirmou a E10: aceitação 65/65 e suíte 616/616. E11: versão 0.1.17 preparada (`dec46c9`); o pacote Flatpak está sendo montado e testado no CI (fonte, pacote e sandbox).
- **2026/10/20 às 15:40** — E11: Flatpak 0.1.17 montado e aprovado no CI (616/616 na fonte, no pacote e no sandbox; smoke 5/5; launcher 3/3). A publicação como prerelease foi recusada para esta sessão (o GitHub não permite que ela crie releases). Preparei um fluxo que publica exatamente o arquivo testado, sem recompilar: no GitHub, abra Actions → "Publish tested development release (manual)" → Run workflow, com a versão 0.1.17. Depois disso eu confiro o download, rodo a auditoria e o teste de desktop.
- **2026/10/20 às 15:41** — Retomada agendada recebida. E08, E09 e E10 concluídas; a E11 depende só de você disparar a publicação (Actions → "Publish tested development release (manual)", versão 0.1.17). Seguindo com E12, E13, E14 e E15; depois paro.
- **2026/10/20 às 15:50** — E12 concluída (`12dda24`): dá para mudar a cor e a opacidade de retângulos, elipses, linhas, destaques, sublinhados e desenhos já existentes, numa cópia nova; o desenho é refeito e conferido na imagem gerada pelo Poppler. Suíte 620/620, aceitação 67/67. A E11 continua aguardando você publicar a 0.1.17. Iniciando a E13.
- **2026/10/20 às 15:58** — E13 concluída (`9a10b42`): retângulos, elipses e caixas de texto livre já existentes podem ser redimensionados numa cópia nova; o desenho é refeito no novo tamanho e o texto é diagramado de novo. Suíte 624/624, aceitação 69/69. O CI confirmou a E12 (67/67, 620/620). Iniciando a E14.
- **2026/10/20 às 16:09** — E14 concluída: marcar áreas para redação sem apagar nada (anotação /Redact editável). Suíte 630/630, aceitação 71/71 (`7488bc7`). CI Debian 13 confirmou a E13 (624/624, 69/69). Iniciando a E15.
- **2026/10/20 às 16:22** — E15 concluída (`61f180e`): aplicar redação numa cópia nova. As páginas marcadas viram imagem com as áreas pintadas; o texto e as imagens sob as marcas desaparecem do arquivo (conferido em todos os objetos), e as demais páginas não mudam. Suíte 638/638, aceitação 73/73. CI Debian 13 confirmou a E14 (630/630, 71/71). Bloco E12–E15 concluído. Você pediu para retomar a E08 e resolver o erro: iniciando.
- **2026/10/20 às 16:33** — E08 — erro resolvido: a falha de CI vinha de um teste que dependia do qpdf (ausente no CI) e era pulado. O teste agora cria a origem sem ferramenta externa, a cópia assinada é conferida pelo pdfsig, e o qpdf foi instalado no CI. CI Debian 13 (`f92278b`): 638/638 sem pulos, aceitação 73/73. CI também confirmou a E15. Parado, aguardando você (E11 depende da publicação manual).
- **2026/10/20 às 16:43** — E11: a publicação pelo fluxo manual (execução 39485174222) conferiu o pacote, mas o GitHub recusou criar a tag no commit testado (403; o token automático não pode criar referência num commit cujos workflows diferem da main). O fluxo foi ajustado para criar a release como rascunho; você publica o rascunho com um clique em Releases. Nada foi publicado na tentativa que falhou.
- **2026/10/20 às 17:01** — E11 concluída: **0.1.17/devel publicada** (prerelease `v0.1.17-devel`, mesmo pacote testado, SHA-256 ec773a20…7a71). Download público conferido; auditoria do pacote instalado aprovada; integrações de desktop 9/9 nas duas repetições. A release foi criada e publicada pelo navegador interno, com a sua confirmação, porque o token automático do GitHub foi recusado (403). A primeira auditoria falhou por comparar com a main mais nova; corrigido para comparar com o commit testado. Parado, aguardando você.
- **2026/10/20 às 17:09** — Plano: a causa do 403 ao criar releases pelo GitHub Actions virou a etapa prioritária E29, para o Codex identificar (instruções em PRIORIDADE-E29-ERRO-403-RELEASE.md). O Claude retoma às 20:10: se a causa estiver resolvida, segue para E16–E20; se não, tenta resolver com base no que o Codex registrar.

- **2026/10/20 às 17:14** — Codex leu a prioridade E29, sincronizou main 353aa73 e preservou ambos os históricos de continuidade. Preparado fluxo manual de diagnóstico com contents:write, sem tokens em arquivos, limpeza restrita aos próprios rascunhos e conferência das releases públicas. Nenhum teste de app/VM iniciado.

- **2026/10/20 às 17:19** — E29: reproduzida a causa (201/201/403 pelo mesmo token); não é falta de contents:write nem corrupção do pacote. GITHUB_TOKEN não pode receber Workflows:write exigido pelo alvo antigo. Preparado preflight para evitar repetir a operação recusada e preservar SHA/asset testados; oito testes de guardas aprovados. Sem alteração de configuração da conta ou VM.
