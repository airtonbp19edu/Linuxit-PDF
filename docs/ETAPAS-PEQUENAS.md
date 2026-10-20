# Etapas pequenas do que falta

Gerado de `progresso/etapas-pequenas.json` por `scripts/render_small_steps.py`. A ordem é a prioridade: o que não precisa da VM vem primeiro. Situação geral e avisos: [AVISOS-E-STATUS.md](AVISOS-E-STATUS.md).

Atualizado em 2026-10-20T15:50:00-03:00. Pendente: 10, Em andamento: 1, Concluída: 15, Bloqueada: 1, Aguardando você: 1.

**Regras**

- A ordem da lista é a prioridade. Etapas sem VM vêm primeiro.
- Ao concluir uma etapa, parar e aguardar a confirmação do usuário antes de iniciar a próxima (pedido do usuário em 20/10/2026 às 00:58).
- Uma etapa só fica concluida com verificação executada, evidência registrada e commit publicado.
- Cada etapa concluída acrescenta pelo menos um teste ou caso de aceitação que falharia sem ela.
- Não alterar critérios, pesos ou paridade das 21 etapas originais por causa desta lista.

| # | Etapa | Bloco | Precisa de | Situação |
|---|---|---|---|---|
| E01 | Verificador do catálogo de operações verde | Base e entrega | nada | Concluída |
| E02 | Contrato próprio da integração com o sistema | Base e entrega | nada | Concluída |
| E03 | Formatação de números (AFNumber_Format) | Formulários | nada | Concluída |
| E04 | Datas em formulários (AFDate_FormatEx) | Formulários | nada | Concluída |
| E05 | Máscaras especiais (AFSpecial_Format 0–3) | Formulários | nada | Concluída |
| E25 | Régua com vírgula decimal (2,54 cm) | Base e entrega | nada | Concluída |
| E26 | Estabilizar o teste de reprodução de mídia | Base e entrega | nada | Concluída |
| E06 | XFA: leitura dos campos | Formulários | nada | Concluída |
| E27 | Investigar a queda do GTK no CI Debian 13 | Base e entrega | nada | Concluída |
| E07 | XFA híbrido: preencher mantendo datasets coerente | Formulários | nada | Concluída |
| E28 | Fechar a nuvem pelo fluxo de pastas sincronizadas | Nuvem (pastas sincronizadas) | nada | Concluída |
| E08 | Segunda assinatura em revisão incremental | Assinaturas | nada | Concluída |
| E09 | Verificar DocTimeStamp existente | Assinaturas | nada | Concluída |
| E10 | Usar DSS/VRI embutidos na validação offline | Assinaturas | nada | Concluída |
| E11 | Entrega 0.1.17 | Base e entrega | nada | Aguardando você |
| E12 | Editar cor e opacidade de anotações existentes | Anotações e redação | nada | Concluída |
| E13 | Redimensionar Square, Circle e FreeText | Anotações e redação | nada | Em andamento |
| E14 | Marcar áreas para redação | Anotações e redação | nada | Pendente |
| E15 | Aplicar redação | Anotações e redação | nada | Pendente |
| E16 | Imagem de apresentação de anotações 3D | Mídia 3D | nada | Pendente |
| E17 | Corpus de PDFs danificados | Robustez | nada | Pendente |
| E18 | Corpus de criptografia | Robustez | nada | Pendente |
| E19 | Ordem de leitura em duas colunas | Robustez | nada | Pendente |
| E20 | Estudo de renderização U3D/PRC | Mídia 3D | nada | Pendente |
| E21 | Atualizar o REA no PC | PC Windows | PC do usuário | Pendente |
| E22 | Estática: chamadores e tipos da busca | PC Windows | PC do usuário | Pendente |
| E23 | Validações físicas | Equipamentos reais | equipamentos | Pendente |
| E24 | Retomar a comparação com o Foxit | VM | VM e autorização do usuário | Bloqueada |

## Detalhes

### E01 — Verificador do catálogo de operações verde

**Objetivo:** Apontar a referência de testes do catálogo para a suíte confirmada no CI 39363684386 (571/571), em vez dos arquivos da 0.1.16.

**Como verificar:** scripts/check_operation_catalog.py passa; docs/INVENTARIO-OPERACOES.md renderizado sem diferença.

**Situação:** Concluída.

check_operation_catalog.py e render_operation_catalog.py --check-render passam. O inventário renderizado também estava desatualizado (95/13 em vez de 97/11) e foi regenerado.

Evidência: [testes/resultados/sem-vm-2026-10-20/own-validated-cases.json](../testes/resultados/sem-vm-2026-10-20/own-validated-cases.json), [docs/INVENTARIO-OPERACOES.md](../docs/INVENTARIO-OPERACOES.md). Commit `9c10dc4`.

### E02 — Contrato próprio da integração com o sistema

**Objetivo:** Passar a família platform de proposta para subconjunto implementado (portal, concessão persistente, revogação e associação já validados 9/9) e tornar S12-25 executável.

**Como verificar:** validate_functional_spec.py passa; S12-25-1 e S12-25-2 executados com o portal real (xdg-desktop-portal) e registrados.

**Situação:** Concluída.

A família platform deixou de ser proposta. Os casos acionam o botão real "Abrir pelo seletor do sistema" com o portal; um defeito injetado no cancelamento fez o caso falhar. Aceitação total: 48/48 na revisão 353a30b.

Evidência: [testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e02.json](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e02.json), [docs/contratos-funcionais.md](../docs/contratos-funcionais.md). Commit `353a30b`.

### E03 — Formatação de números (AFNumber_Format)

**Objetivo:** Reconhecer AFNumber_Format por gramática fechada e aplicar casas decimais, separadores e símbolo ao valor e à aparência, sem executar JavaScript.

**Como verificar:** Testes portáveis novos e caso de aceitação com fixture de formulário formatado.

**Situação:** Concluída.

Valor do campo sem formatação e aparência formatada (ex.: R$ 2.469,00); vírgula decimal aceita na entrada; negativos em vermelho recusados de forma explícita. 5 testes novos e caso S12-15-3. Suíte local 576/576; aceitação 49/49. O verificador do catálogo deixou de falhar a cada edição: trechos só deslocados são refixados por scripts/refresh_operation_pins.py. Confirmado no CI Debian 13 (execução 39366205486): aceitação 49/49 e suíte 576/576.

Evidência: [testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e03.json](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e03.json), [tests/test_form_events.py](../tests/test_form_events.py), [testes/resultados/aceitacao/2026-10-20/ci-debian13-e03-review.json](../testes/resultados/aceitacao/2026-10-20/ci-debian13-e03-review.json). Commit `0600b05`.

### E04 — Datas em formulários (AFDate_FormatEx)

**Objetivo:** Validar e formatar datas com máscaras fechadas suportadas, recusando entradas inválidas.

**Como verificar:** Testes portáveis com datas válidas, inválidas e limites.

**Situação:** Concluída.

Datas numéricas (d, dd, m, mm, yy, yyyy; separadores / - . e espaço); data inexistente recusada; valor como digitado e aparência formatada (1/2/2026 → 01/02/2026). Nomes de mês e horas recusados explicitamente. 3 testes novos e casos S12-15-4/S12-15-5. Suíte local 579/579; aceitação 51/51. Confirmado no CI Debian 13 (execução 39366798234): aceitação 51/51 e suíte 579/579.

Evidência: [testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e04.json](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e04.json), [tests/test_form_events.py](../tests/test_form_events.py), [testes/resultados/aceitacao/2026-10-20/ci-debian13-e04-review.json](../testes/resultados/aceitacao/2026-10-20/ci-debian13-e04-review.json). Commit `34ebb46`.

### E05 — Máscaras especiais (AFSpecial_Format 0–3)

**Objetivo:** Aplicar os quatro formatos especiais padronizados ao valor e à aparência.

**Como verificar:** Testes portáveis para cada formato e entrada fora do padrão.

**Situação:** Concluída.

AFSpecial_Format/Keystroke 0–3 guardam só os dígitos e mostram a máscara; AFSpecial_KeystrokeEx com máscara livre (9, A, O, X e literais, como CEP 99999-999 e CPF 999.999.999-99) aceita o texto com ou sem os literais. 4 testes novos e casos S12-15-6/S12-15-7. Aceitação 53/53. Na suíte local, um teste de mídia já existente falhou de forma intermitente (decisão D02). Confirmado no CI Debian 13 (execução 39367796407): aceitação 53/53 e suíte 583/583; o teste de mídia passou no CI.

Evidência: [testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e05.json](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e05.json), [tests/test_form_events.py](../tests/test_form_events.py), [testes/resultados/aceitacao/2026-10-20/ci-debian13-e05-review.json](../testes/resultados/aceitacao/2026-10-20/ci-debian13-e05-review.json). Commit `e8cface`.

### E25 — Régua com vírgula decimal (2,54 cm)

**Objetivo:** Mostrar as medidas da régua do visualizador com vírgula decimal e duas casas (ex.: 2,54 cm), conforme a decisão D01, e conferir o mesmo padrão na janela de medidas e no tamanho da página.

**Como verificar:** Caso S12-20-1 atualizado para 2,54 cm com teste GTK; demais exibições de medida conferidas.

**Situação:** Concluída.

Função única measurement.decimal_text: régua com duas casas (2,54 cm), janela de medidas com até seis algarismos significativos (6,4516) e tamanho da página com uma casa (21,0 × 29,7 cm). Só o texto muda, nunca o valor medido. Suíte local 584/584; aceitação 53/53 com S12-20-1 esperando 2,54 cm. Confirmado no CI Debian 13 (execução 39427531619): aceitação 53/53 e suíte 584/584.

Evidência: [testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e25.json](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e25.json), [tests/test_measurement_layers_speech.py](../tests/test_measurement_layers_speech.py), [testes/resultados/aceitacao/2026-10-20/ci-debian13-e25-review.json](../testes/resultados/aceitacao/2026-10-20/ci-debian13-e25-review.json). Commit `db8c6fe`.

### E26 — Estabilizar o teste de reprodução de mídia

**Objetivo:** Encontrar a causa da falha intermitente de test_local_playback (estado nativo que não chega a tempo) e corrigir o teste ou o código, sem enfraquecer o que ele verifica (decisão D02).

**Como verificar:** O teste passa em 20 execuções seguidas no ambiente local e no CI Debian 13.

**Situação:** Concluída.

A instabilidade era um defeito real: a reprodução podia começar antes de o áudio estar conectado, e um arquivo de 1 s terminava em milissegundos (1 em 25 execuções). Agora o reprodutor pré-carrega antes de tocar. Teste novo exige pelo menos 0,8 s de reprodução (o código antigo falhou 6 de 10). Testes de reprodução: 20 de 20 execuções seguidas; suíte local 585/585; aceitação 53/53. CI Debian 13: a revisão d07a204 falhou duas vezes com queda nativa do GTK (SIGSEGV) num teste de comentários que roda antes do teste de mídia; a revisão 95a46ba (mesmo código, com faulthandler ligado) passou: suíte 585/585 e aceitação 53/53 (ci-debian13-e26-review.json). Queda registrada como decisão D03.

Evidência: [testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e26.json](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e26.json), [tests/test_local_playback.py](../tests/test_local_playback.py), [testes/resultados/aceitacao/2026-10-20/ci-debian13-e26-review.json](../testes/resultados/aceitacao/2026-10-20/ci-debian13-e26-review.json). Commit `5747278`.

### E06 — XFA: leitura dos campos

**Objetivo:** Detectar formulário XFA e listar campos e valores do pacote datasets, somente leitura, com limites de tamanho e profundidade.

**Como verificar:** Fixture XFA sintética; teste portátil e caso de aceitação.

**Situação:** Concluída.

Novo módulo app/pdf_xfa.py: detecta XFA (fluxo único ou lista de pacotes, híbrido ou só XFA, dinâmico) e lista os valores do pacote datasets por caminho SOM, como form1[0].nome[0]. Somente leitura: o modelo e os scripts XFA não são interpretados nem executados; DOCTYPE e entidades são recusados; limites de 8 MiB, profundidade 64, 5000 valores e 4096 caracteres por valor. Menu "Campos de formulário XFA…" abre um diálogo de leitura. Gravação de PDFs XFA continua recusada (E07). 10 testes portáveis novos; casos de aceitação S12-15-8 (worker) e S12-15-9 (diálogo GTK); suíte local 595/595; aceitação 55/55 na revisão 06daa9d. CI Debian 13 (execução 39432901662, revisão 9abc923): suíte 595/595 e aceitação 55/55.

Evidência: [testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e06.json](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e06.json), [tests/test_pdf_xfa.py](../tests/test_pdf_xfa.py), [app/pdf_xfa.py](../app/pdf_xfa.py), [testes/resultados/aceitacao/2026-10-20/ci-debian13-e06-review.json](../testes/resultados/aceitacao/2026-10-20/ci-debian13-e06-review.json). Commit `06daa9d`.

### E27 — Investigar a queda do GTK no CI Debian 13

**Objetivo:** Encontrar a causa do SIGSEGV após "Gtk-CRITICAL _gtk_css_rgba_value_get_rgba" em test_comment_threads no Debian 13 (2 de 3 execuções do CI) e corrigir o código ou o teste sem enfraquecer o que ele verifica (decisão D03).

**Como verificar:** Reproduzir ou explicar a queda com evidência; depois da correção, o teste passa repetidamente no ambiente local e no CI Debian 13.

**Situação:** Concluída.

A queda não se repetiu sob demanda (0 em cerca de 70 execuções, inclusive 18 no CI com parada no primeiro aviso crítico), mas a causa provável foi encontrada: o coletor de lixo do Python rodava às vezes em threads de trabalho e liberava widgets GTK fora da thread principal, o que o GTK 3 não suporta. Uma sonda contou 546 objetos GTK liberados assim numa suíte completa, inclusive janelas inteiras. Correção: a coleta passa a rodar só na thread principal (app/main_thread_gc.py); a sonda conta 0. 5 testes novos; suíte local 600/600; aceitação 55/55; CI Debian 13: suíte 600/600, aceitação 55/55 e 18 execuções de diagnóstico sem nenhum aviso crítico.

Evidência: [testes/resultados/e27-gc-threads/2026-10-20/revisao.json](../testes/resultados/e27-gc-threads/2026-10-20/revisao.json), [testes/resultados/e27-gc-threads/2026-10-20/probe-antes-06daa9d.json](../testes/resultados/e27-gc-threads/2026-10-20/probe-antes-06daa9d.json), [testes/resultados/e27-gc-threads/2026-10-20/probe-depois-79851e9.json](../testes/resultados/e27-gc-threads/2026-10-20/probe-depois-79851e9.json), [testes/resultados/aceitacao/2026-10-20/ci-debian13-e27-review.json](../testes/resultados/aceitacao/2026-10-20/ci-debian13-e27-review.json), [tests/test_main_thread_gc.py](../tests/test_main_thread_gc.py). Commit `79851e9`.

### E07 — XFA híbrido: preencher mantendo datasets coerente

**Objetivo:** Em PDF com AcroForm e XFA, preencher um campo e atualizar o valor correspondente em datasets na cópia nova.

**Como verificar:** Reabrir a cópia: AcroForm e datasets com o mesmo valor; original preservado.

**Situação:** Concluída.

Em PDF com campos AcroForm e XFA, preencher um campo (texto ou eventos) grava a cópia nova e copia cada valor de texto alterado, inclusive os calculados, para o elemento correspondente do pacote datasets. O elemento é achado pelo nome do campo sem os subformulários sem nome (#subform); só o conteúdo dele muda, o resto do XML fica byte a byte, e a cópia é reaberta e conferida antes de ser publicada. Recusados: formulário só XFA, campo sem dado correspondente, texto rico e outras alterações em XFA. O diálogo de preenchimento só oferece campos ligados aos dados. 7 testes novos (5 portáveis, 2 GTK); casos S12-15-10 e S12-15-11; suíte local 607/607; aceitação 57/57 na revisão aff57e0. CI Debian 13 (execução 39449238643, revisão aff57e0): suíte 607/607 e aceitação 57/57.

Evidência: [testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e07.json](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e07.json), [tests/test_pdf_xfa.py](../tests/test_pdf_xfa.py), [tests/test_xfa_gtk.py](../tests/test_xfa_gtk.py), [testes/resultados/aceitacao/2026-10-20/ci-debian13-e07-review.json](../testes/resultados/aceitacao/2026-10-20/ci-debian13-e07-review.json). Commit `aff57e0`.

### E28 — Fechar a nuvem pelo fluxo de pastas sincronizadas

**Objetivo:** Pedido do usuário em 20/10/2026 às 12:38: fechar o ciclo da nuvem com a decisão já tomada em 17/10/2026 às 20:51, de usar pastas sincronizadas por programas externos. A família Nuvem passa de proposta a recorte implementado: o Linuxit trabalha com a pasta local e o cliente externo cuida da nuvem. Os casos S12-23 deixam de simular um provedor e passam a verificar esse fluxo. Login, transferência por API e colaboração remota continuam adiados.

**Como verificar:** Casos S12-23-1 e S12-23-2 executados na janela real; validador, arquitetura e catálogo coerentes; suíte e aceitação completas, inclusive no CI Debian 13.

**Situação:** Concluída.

A família Nuvem deixou de ser proposta: o contrato agora é o fluxo de pasta sincronizada já implementado (pasta preferida, abrir dela, cópia completa e exclusiva que só diz "salva localmente", bloqueio quando o cliente troca o PDF aberto, nunca sobrescrever arquivo criado pelo cliente). S12-23-1 e S12-23-2 trocaram o provedor simulado por esse fluxo, na janela real; textos antigos preservados. Login, transferência por API e colaboração remota continuam adiados. Suíte 607/607; aceitação 59/59 (todos os planos) na revisão 033e245. Falta só testar com um cliente sincronizador real. CI Debian 13 (execução 39451575700, revisão 033e245): suíte 607/607 e aceitação 59/59.

Evidência: [testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e28.json](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e28.json), [docs/PASTAS-SINCRONIZADAS.md](../docs/PASTAS-SINCRONIZADAS.md), [testes/aceitacao/casos_gtk.py](../testes/aceitacao/casos_gtk.py), [testes/resultados/aceitacao/2026-10-20/ci-debian13-e28-review.json](../testes/resultados/aceitacao/2026-10-20/ci-debian13-e28-review.json). Commit `033e245`.

### E08 — Segunda assinatura em revisão incremental

**Objetivo:** Assinar um PDF já assinado por atualização incremental, mantendo a primeira assinatura válida para a revisão dela.

**Como verificar:** As duas assinaturas verificam integridade; a primeira cobre só a revisão original.

**Situação:** Concluída.

Toda assinatura nova vira uma revisão incremental anexada aos bytes exatos da origem (objetos novos, AcroForm atualizado e seção de referência cruzada do mesmo tipo da anterior). Cada assinatura anterior precisa verificar antes e continua verificando a própria revisão depois; a nova cobre o arquivo inteiro. O escritor incremental do pypdf foi descartado: na terceira assinatura ele reaproveitava números de objeto e corrompia a assinatura. Recusas com motivo visível: DocMDP P=1, UR3, assinatura anterior inválida, criptografia, XFA, portfólio e mais de 15 assinaturas. Três assinaturas seguidas conferidas também pelo pdfsig (poppler) e origem com fluxo de referência cruzada pelo qpdf. Suíte 610/610; aceitação 61/61 na revisão ae429cd.

Evidência: [testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e08.json](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e08.json), [tests/test_incremental_signatures.py](../tests/test_incremental_signatures.py), [app/pdf_signing.py](../app/pdf_signing.py). Commit `ae429cd`.

### E09 — Verificar DocTimeStamp existente

**Objetivo:** Reconhecer assinatura de carimbo de documento (ETSI.RFC3161) e verificá-la offline contra as âncoras escolhidas.

**Como verificar:** Fixture com DocTimeStamp de TSA sintética; alteração de bytes invalida.

**Situação:** Concluída.

Campos de carimbo de documento (/ETSI.RFC3161) são reconhecidos e verificados offline: assinatura do token e resumo do documento (SHA-256/384/512) contra os bytes cobertos; o horário só aparece se os dois conferirem. Com política offline, a TSA só é confiável pela CA escolhida (openssl ts -verify, sem âncoras do sistema). Assinar depois de um carimbo mantém os dois válidos. A janela de assinaturas identifica o carimbo e mostra o horário. Carimbos de teste são gerados por uma TSA sintética local (testes/aceitacao/carimbo.py). Suíte 613/613; aceitação 63/63 na revisão df7207a.

Evidência: [testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e09.json](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e09.json), [tests/test_document_timestamps.py](../tests/test_document_timestamps.py), [testes/aceitacao/carimbo.py](../testes/aceitacao/carimbo.py). Commit `df7207a`.

### E10 — Usar DSS/VRI embutidos na validação offline

**Objetivo:** Ler certificados e CRLs do dicionário DSS e usá-los na verificação de cadeia e revogação, sem rede.

**Como verificar:** Fixture com DSS sintético: revogação verificada só com o material embutido.

**Situação:** Concluída.

Certificados e CRLs do dicionário DSS do PDF entram na validação offline: certificados só ajudam a montar o caminho até a CA escolhida (nunca viram âncora) e CRLs servem para a revogação; OCSP e VRI são contados, não usados; DSS inválido é informado e ignorado. A janela mostra o resumo do DSS e o que foi usado. Suíte 616/616; aceitação 65/65 na revisão ba38ca7.

Evidência: [testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e10.json](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e10.json), [tests/test_dss_validation.py](../tests/test_dss_validation.py), [app/signature_trust.py](../app/signature_trust.py). Commit `ba38ca7`.

### E11 — Entrega 0.1.17

**Objetivo:** Versão, Flatpak testado em fonte, pacote e sandbox, publicação como prerelease, auditoria do mesmo arquivo, download conferido e probe de desktop.

**Como verificar:** Workflows linux-flatpak, delivery-audit e desktop-integrations aprovados e examinados.

**Situação:** Aguardando você.

Candidato 0.1.17 (revisão dec46c9) montado e aprovado no CI 39474059660: 616/616 testes na fonte, no pacote e no Flatpak instalado (sandbox), smoke 5/5, launcher 3/3, 179 arquivos fonte/pacote iguais, 3684 arquivos de runtime auditados. Bundle LinuxitPDF-0.1.17-x86_64.flatpak, 118422768 bytes, SHA-256 ec773a20…7a71. Evidências em testes/resultados/0.1.17/ e manifesto releases/manifest-0.1.17.json. A publicação como prerelease foi bloqueada: esta sessão não tem permissão para criar releases no GitHub. Falta o usuário disparar o fluxo "Publish tested development release (manual)" (publish-devel-release.yml, versão 0.1.17), que publica o mesmo arquivo testado sem recompilar; depois: conferir o download, rodar a auditoria e o probe de desktop.

### E12 — Editar cor e opacidade de anotações existentes

**Objetivo:** Alterar cor e opacidade de anotações simples já existentes, regenerando a aparência.

**Como verificar:** Teste com pixels da aparência antes e depois; original preservado.

**Situação:** Concluída.

Retângulos, elipses, linhas, destaques, sublinhados, tachados, ondulados, desenhos, polígonos, polilinhas e marcas de inserção já existentes podem mudar de cor (RGB) e opacidade (10% a 100%) numa cópia nova; a aparência é redesenhada a partir da geometria da própria anotação, e o resultado foi conferido em pixels desenhados pelo Poppler. Notas, texto livre e carimbos ficam de fora. Diálogo com seletor de cor e opacidade no rascunho de edição. Suíte 620/620; aceitação 67/67 na revisão 12dda24.

Evidência: [testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e12.json](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e12.json), [tests/test_annotation_style.py](../tests/test_annotation_style.py), [app/annotation_style.py](../app/annotation_style.py). Commit `12dda24`.

### E13 — Redimensionar Square, Circle e FreeText

**Objetivo:** Mudar o retângulo dessas anotações mantendo aparência coerente.

**Como verificar:** Teste portátil de geometria e teste GTK de renderização.

**Situação:** Em andamento.

### E14 — Marcar áreas para redação

**Objetivo:** Criar anotações Redact sem aplicar, visíveis e editáveis.

**Como verificar:** Reabrir a cópia lista as marcas; texto original ainda presente.

**Situação:** Pendente.

### E15 — Aplicar redação

**Objetivo:** Remover texto e imagens sob as áreas marcadas numa cópia nova, rasterizando só as páginas afetadas.

**Como verificar:** Extração de texto da cópia não retorna o conteúdo redigido; demais páginas intactas.

**Situação:** Pendente.

### E16 — Imagem de apresentação de anotações 3D

**Objetivo:** Exibir a aparência/poster de anotações 3D com o aviso de que a cena não é interativa.

**Como verificar:** Fixture com anotação 3D e aparência; teste GTK de pixels.

**Situação:** Pendente.

### E17 — Corpus de PDFs danificados

**Objetivo:** Fixtures com xref quebrado, stream truncado e objeto ausente, com resultado esperado de abertura ou recuperação para cada um.

**Como verificar:** Casos executáveis: abrir, recuperar com consentimento ou recusar sem página fictícia.

**Situação:** Pendente.

### E18 — Corpus de criptografia

**Objetivo:** Fixtures RC4-40, RC4-128, AES-128, AES-256 e metadados não cifrados para abrir, editar e imprimir.

**Como verificar:** Matriz de casos executáveis por perfil e operação.

**Situação:** Pendente.

### E19 — Ordem de leitura em duas colunas

**Objetivo:** Texto acessível e OCR seguem coluna por coluna em páginas de duas colunas, com heurística própria limitada.

**Como verificar:** Fixture de duas colunas com ordem esperada; teste portátil.

**Situação:** Pendente.

### E20 — Estudo de renderização U3D/PRC

**Objetivo:** Avaliar bibliotecas abertas, licenças e tamanho para um renderizador 3D, sem implementar.

**Como verificar:** Documento com opções, licenças e decisão proposta ao usuário.

**Situação:** Pendente.

### E21 — Atualizar o REA no PC

**Objetivo:** O usuário executa analysis-local\rea-instalacao\instalar-rea.cmd; conferir o log.

**Como verificar:** Log com REA 6.7.0 e doctor do Ghidra saudável.

**Situação:** Pendente.

### E22 — Estática: chamadores e tipos da busca

**Objetivo:** Continuar a partir dos resultados preservados os chamadores, tipos e propriedade dos objetos da busca.

**Como verificar:** Relatório com instruções conferidas e catálogo atualizado, sem repetir sementes.

**Situação:** Pendente.

### E23 — Validações físicas

**Objetivo:** Impressora física, leitor de tela, áudio, monitores físicos e cliente sincronizador real, com o usuário.

**Como verificar:** Registro de cada equipamento e resultado observado.

**Situação:** Pendente.

### E24 — Retomar a comparação com o Foxit

**Objetivo:** Somente com autorização: preflight, controle do relógio e observador novo; continuar D01–D20 e UI01–UI10.

**Como verificar:** Comparações registradas com a mesma fixture; parada imediata se o relógio travar.

**Situação:** Bloqueada.

## Decisões

- **D01** (Decidida): A régua mostra 2.54 cm com ponto decimal. Usar vírgula (2,54 cm) na interface em português? **Resposta:** Usar vírgula decimal: 2,54 cm (usuário, 20/10/2026 às 01:08). Etapa E25.
- **D02** (Decidida): O teste de reprodução de mídia (test_local_playback, GStreamer) falhou 1 vez em 3 no ambiente local, sem relação com as etapas atuais. Tornar esse teste robusto como uma etapa própria? **Resposta:** Tornar o teste estável como uma etapa própria (usuário, 20/10/2026 às 01:08). Etapa E26.
- **D03** (Decidida): No CI Debian 13 o processo de testes caiu 2 vezes em 3 (SIGSEGV após um aviso interno do GTK sobre cor CSS) no teste de busca em comentários test_comment_threads, sem relação com E26 ou E06; no Ubuntu passou 25 de 25. O registro de pilha (faulthandler) já foi ligado para a próxima queda. Investigar como uma etapa própria? **Resposta:** Investigar como uma etapa própria e, em seguida, fazer a próxima etapa (usuário, 20/10/2026 às 10:53). Etapa E27.
