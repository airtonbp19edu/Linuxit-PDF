# Etapas pequenas do que falta

Gerado de `progresso/etapas-pequenas.json` por `scripts/render_small_steps.py`. A ordem é a prioridade: o que não precisa da VM vem primeiro. Situação geral e avisos: [AVISOS-E-STATUS.md](AVISOS-E-STATUS.md).

Atualizado em 2026-10-20T00:31:00-03:00. Pendente: 22, Em andamento: 1, Bloqueada: 1.

**Regras**

- A ordem da lista é a prioridade. Etapas sem VM vêm primeiro.
- Uma etapa só fica concluida com verificação executada, evidência registrada e commit publicado.
- Cada etapa concluída acrescenta pelo menos um teste ou caso de aceitação que falharia sem ela.
- Não alterar critérios, pesos ou paridade das 21 etapas originais por causa desta lista.

| # | Etapa | Bloco | Precisa de | Situação |
|---|---|---|---|---|
| E01 | Verificador do catálogo de operações verde | Base e entrega | nada | Em andamento |
| E02 | Contrato próprio da integração com o sistema | Base e entrega | nada | Pendente |
| E03 | Formatação de números (AFNumber_Format) | Formulários | nada | Pendente |
| E04 | Datas em formulários (AFDate_FormatEx) | Formulários | nada | Pendente |
| E05 | Máscaras especiais (AFSpecial_Format 0–3) | Formulários | nada | Pendente |
| E06 | XFA: leitura dos campos | Formulários | nada | Pendente |
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

**Situação:** Em andamento.

### E02 — Contrato próprio da integração com o sistema

**Objetivo:** Passar a família platform de proposta para subconjunto implementado (portal, concessão persistente, revogação e associação já validados 9/9) e tornar S12-25 executável.

**Como verificar:** validate_functional_spec.py passa; S12-25-1 e S12-25-2 executados no workflow de desktop e registrados.

**Situação:** Pendente.

### E03 — Formatação de números (AFNumber_Format)

**Objetivo:** Reconhecer AFNumber_Format por gramática fechada e aplicar casas decimais, separadores e símbolo ao valor e à aparência, sem executar JavaScript.

**Como verificar:** Testes portáveis novos e caso de aceitação com fixture de formulário formatado.

**Situação:** Pendente.

### E04 — Datas em formulários (AFDate_FormatEx)

**Objetivo:** Validar e formatar datas com máscaras fechadas suportadas, recusando entradas inválidas.

**Como verificar:** Testes portáveis com datas válidas, inválidas e limites.

**Situação:** Pendente.

### E05 — Máscaras especiais (AFSpecial_Format 0–3)

**Objetivo:** Aplicar os quatro formatos especiais padronizados ao valor e à aparência.

**Como verificar:** Testes portáveis para cada formato e entrada fora do padrão.

**Situação:** Pendente.

### E06 — XFA: leitura dos campos

**Objetivo:** Detectar formulário XFA e listar campos e valores do pacote datasets, somente leitura, com limites de tamanho e profundidade.

**Como verificar:** Fixture XFA sintética; teste portátil e caso de aceitação.

**Situação:** Pendente.

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

## Decisões pendentes

- **D01** (Aguardando você): A régua mostra 2.54 cm com ponto decimal. Usar vírgula (2,54 cm) na interface em português?
