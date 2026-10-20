# Etapas pequenas do que falta

Gerado de `progresso/etapas-pequenas.json` por `scripts/render_small_steps.py`. A ordem é a prioridade: o que não precisa da VM vem primeiro. Situação geral e avisos: [AVISOS-E-STATUS.md](AVISOS-E-STATUS.md).

Atualizado em 2026-10-20T10:25:22-03:00. Pendente: 17, Em andamento: 1, Concluída: 7, Bloqueada: 1.

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
| E06 | XFA: leitura dos campos | Formulários | nada | Em andamento |
| E07 | XFA híbrido: preencher mantendo datasets coerente | Formulários | nada | Pendente |
| E08 | Segunda assinatura em revisão incremental | Assinaturas | nada | Pendente |
| E09 | Verificar DocTimeStamp existente | Assinaturas | nada | Pendente |
| E10 | Usar DSS/VRI embutidos na validação offline | Assinaturas | nada | Pendente |
| E11 | Entrega 0.1.17 | Base e entrega | nada | Pendente |
| E12 | Editar cor e opacidade de anotações existentes | Anotações e redação | nada | Pendente |
| E13 | Redimensionar Square, Circle e FreeText | Anotações e redação | nada | Pendente |
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

A instabilidade era um defeito real: a reprodução podia começar antes de o áudio estar conectado, e um arquivo de 1 s terminava em milissegundos (1 em 25 execuções). Agora o reprodutor pré-carrega antes de tocar. Teste novo exige pelo menos 0,8 s de reprodução (o código antigo falhou 6 de 10). Testes de reprodução: 20 de 20 execuções seguidas; suíte local 585/585; aceitação 53/53.

Evidência: [testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e26.json](../testes/resultados/aceitacao/2026-10-20/execucao-ubuntu24-e26.json), [tests/test_local_playback.py](../tests/test_local_playback.py). Commit `5747278`.

### E06 — XFA: leitura dos campos

**Objetivo:** Detectar formulário XFA e listar campos e valores do pacote datasets, somente leitura, com limites de tamanho e profundidade.

**Como verificar:** Fixture XFA sintética; teste portátil e caso de aceitação.

**Situação:** Em andamento.

### E07 — XFA híbrido: preencher mantendo datasets coerente

**Objetivo:** Em PDF com AcroForm e XFA, preencher um campo e atualizar o valor correspondente em datasets na cópia nova.

**Como verificar:** Reabrir a cópia: AcroForm e datasets com o mesmo valor; original preservado.

**Situação:** Pendente.

### E08 — Segunda assinatura em revisão incremental

**Objetivo:** Assinar um PDF já assinado por atualização incremental, mantendo a primeira assinatura válida para a revisão dela.

**Como verificar:** As duas assinaturas verificam integridade; a primeira cobre só a revisão original.

**Situação:** Pendente.

### E09 — Verificar DocTimeStamp existente

**Objetivo:** Reconhecer assinatura de carimbo de documento (ETSI.RFC3161) e verificá-la offline contra as âncoras escolhidas.

**Como verificar:** Fixture com DocTimeStamp de TSA sintética; alteração de bytes invalida.

**Situação:** Pendente.

### E10 — Usar DSS/VRI embutidos na validação offline

**Objetivo:** Ler certificados e CRLs do dicionário DSS e usá-los na verificação de cadeia e revogação, sem rede.

**Como verificar:** Fixture com DSS sintético: revogação verificada só com o material embutido.

**Situação:** Pendente.

### E11 — Entrega 0.1.17

**Objetivo:** Versão, Flatpak testado em fonte, pacote e sandbox, publicação como prerelease, auditoria do mesmo arquivo, download conferido e probe de desktop.

**Como verificar:** Workflows linux-flatpak, delivery-audit e desktop-integrations aprovados e examinados.

**Situação:** Pendente.

### E12 — Editar cor e opacidade de anotações existentes

**Objetivo:** Alterar cor e opacidade de anotações simples já existentes, regenerando a aparência.

**Como verificar:** Teste com pixels da aparência antes e depois; original preservado.

**Situação:** Pendente.

### E13 — Redimensionar Square, Circle e FreeText

**Objetivo:** Mudar o retângulo dessas anotações mantendo aparência coerente.

**Como verificar:** Teste portátil de geometria e teste GTK de renderização.

**Situação:** Pendente.

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
