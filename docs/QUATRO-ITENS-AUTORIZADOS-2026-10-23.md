# Desenvolvimento autorizado — 23/10/2026

O usuário respondeu diretamente **“Autorizar os quatro itens”** nesta conversa do Codex. Essa resposta substitui a indicação anterior de confirmação pendente para redação de dados ocultos, XFA posicionado/FormCalc, API JavaScript de formulários e DSS/VRI por assinatura. Não autoriza publicação ou integração de ramos à main/candidato.

Ramo de execução: `codex/authorized-pdf-features`, base `7837bee`. A VM continua reservada ao Claude. Não alterar pesos, critérios ou escopo. Resultados e limites de cada implementação serão registrados abaixo.

## 1. Redação de dados ocultos

O diálogo de aplicação oferece três opções independentes, inicialmente desligadas. O pedido continua aceitando a forma anterior sem `hidden`; o novo objeto admite somente chaves `metadata`, `bookmarks`, `attachments` com booleanos.

O backend extrai palavras com caixas reais pelo `pdftotext -bbox` de uma cópia de uma página, sem anotações e com rotação neutralizada. Transforma as coordenadas para o MediaBox, seleciona as palavras que interceptam as marcas e não armazena os termos nos relatórios. Sem palavra extraível, sem Poppler, com XML/retângulos inválidos ou acima dos limites, recusa a operação. Não executa OCR nem inventa texto para imagens.

* Metadados: remove integralmente `/Info` e XMP do catálogo quando selecionados, incluindo propriedades personalizadas, em vez de preservar representações alternativas de uma palavra.
* Marcadores: percorre títulos e descendentes; substitui ocorrências das palavras selecionadas por `[REDACTED]`, ignorando caixa e normalizando Unicode NFC. Preserva destinos. Recusa ciclos e árvores acima de 10 mil nós.
* Anexos: catálogo e anotações de arquivo; nomes, `/UF`, descrição e conteúdo UTF-8 de txt/csv/md/log/json/xml. Reconstrói a árvore de nomes ordenada, recusa colisões, substitui streams e remove objetos sem referências ao finalizar a cópia. Até 100 anexos, 2 MiB por stream e 16 MiB somados.

Limites: conteúdo binário/Office/PDF, outras codificações e grafos `/AF` são recusados antes da publicação. JSON/XML tratados como texto podem precisar de reparo de sintaxe. Não é limpeza geral de todas as estruturas PDF, páginas sem marcas, scripts, históricos externos ou dados em outros objetos. A seleção de palavras é conservadora e pode redigir substrings em nomes. As opções são explícitas; desligadas preservam os respectivos dados.

## 2. XFA posicionado e FormCalc

Layout próprio de uma página para subformulários `layout="position"`, com x/y/w/h e origem acumulada nos pais. Aceita pt, in, mm e cm; sem unidade usa pontos neste subconjunto. Pode usar um `medium` em orientação retrato e uma `contentArea`. Campos e textos exigem w/h; os retângulos precisam caber nos contêineres e o texto na aparência portátil. Não mistura fluxo `tb` com position nem aceita repetição no modo posicionado. O fluxo vertical e suas repetições anteriores continuam disponíveis separadamente.

FormCalc: apenas script local `application/x-formcalc` dentro do `calculate` de campo. Interpretação própria da árvore sintática, sem eval: constantes numéricas, referências a campos irmãos únicos, `+ - * / ^`, sinal unário, Sum/Avg/Min/Max/Count/Round/Abs. Decimal com precisão limitada; Round usa metade para cima. Até 128 cálculos, 256 nós por expressão, 32 níveis sintáticos, 64 níveis de dependência, expoente inteiro entre −10 e 10 e números até 10^18. Resolve dependências antes do consumidor, recusa ciclos, campos ausentes, referências repetidas ambíguas, divisão por zero, scripts/eventos externos ao contrato e instruções não suportadas.

Atualiza datasets e valores AcroForm juntos, marca campos calculados como somente leitura e não permite sobrescrevê-los no pedido. A interface mostra esses campos sem edição. `scripts_executed` e `calculations` informam o cálculo realmente realizado; sem cálculo mantêm o comportamento anterior.

Limites: não é o motor XFA completo, um interpretador geral FormCalc ou uma reprodução da aparência original. Não preserva fontes, estilos ou paginação original; usa Helvetica/Windows-1252, 11 pontos. SOM amplo, scripts de eventos, controles adicionais, repetição/paginação posicionada e layouts mistos continuam fora deste recorte.

## 3. API JavaScript de formulários

Mantém o processo QuickJS separado, memória/pilha/tempo limitados, transação validada no pai e ausência de capacidades Python, arquivos, rede, módulos e execução de ações de documento. A versão testada é a dependência já fixada 0.15.1.1.

Amplia campos textuais com type, defaultValue, charLimit e getArray do campo terminal; mantém name/readonly/value/valueAsString. `resetForm` permite restaurar padrões de entradas graváveis, valida todos os nomes e recusa campos calculados/protegidos. `/MaxLen` é validado em setters e no resultado entregue ao processo pai. A ordem `/CO` continua o ponto de cálculo; não há chamada recursiva de calculateNow.

Inclui `util.printf` limitado a d/f/s e %%, com largura/precisão/orçamento; AFMakeNumber, AFSimple (SUM/PRD/AVG/MIN/MAX), AFPercent_Format e AFPercent_Keystroke. A formatação altera a aparência separadamente do valor bruto. Formatos, números não finitos e operações fora do contrato abortam a transação.

Limites: é uma ampliação delimitada, não toda a API Acrobat/Foxit. Não adiciona app, util de acesso externo, launchURL, controles não textuais, APIs de assinatura, acesso à interface ou ações automáticas ao abrir documento. A isolação de capacidades não afirma conter vulnerabilidades nativas do motor.

## 4. DSS/VRI por assinatura

Valida o dicionário `/VRI`, até 256 chaves SHA-1 de 40 dígitos hexadecimais maiúsculos. A busca usa os bytes completos de `/Contents`, incluindo padding verificado contra ByteRange, antes de remover padding para verificar CMS. SHA-1 é identificador de busca, não novo algoritmo de assinatura.

Lê `/Cert`, `/CRL`, `/OCSP` de cada entrada com validação DER, limites de itens e orçamento de 16 MiB. Uma entrada correspondente seleciona exclusivamente o material daquela VRI, sem preencher lacunas com VRIs vizinhas ou o conjunto global misto. Sem entrada correspondente, o relatório declara fallback global. Certificados incorporados continuam auxiliares não confiáveis, nunca âncoras.

Cada assinatura informa chave, correspondência, origem, contagens, presença de certificados/revogação e `validation_material_complete`. Este último é nulo sem política explícita. Só fica verdadeiro com VRI correspondente, material de certificado/revogação presente, integridade da assinatura e cadeia/revogação confirmadas pela política offline existente. DER válido ou uma entrada no índice não bastam. Certificados de confiança seguem escolhidos pelo usuário; nenhuma URL é consultada.

A incorporação incremental também aceita `vri_fields`: associa explicitamente o material recebido a cada assinatura verificada selecionada, preserva entradas anteriores e mescla somente seu material prévio com os arquivos recebidos. Reutiliza streams quando possível, confirma a associação na cópia reaberta e preserva todos os bytes anteriores. Sem seleção continua o armazenamento global anterior. A interface permite escolher assinaturas da última verificação; o hash dessa verificação precisa continuar atual. O painel informa VRI correspondente/fallback e distingue material não avaliado de validação offline aprovada.

Limites: essa completude refere-se à verificação técnica implementada, não certifica LTV/PAdES, validade jurídica, cronologia histórica, cobertura de revisões posteriores ou todo o material de carimbos encadeados.

## Validação e próximo passo

Primeira rodada local estruturada: `testes/resultados/quatro-itens-2026-10-23/windows-portable-01.json`, **75 casos: 73 aprovados, zero falhas/erros, dois pulos por ausência de Poppler**. Inclui motor QuickJS real e regressões XFA, redação vetorial e parser DSS/VRI. Essa seleção não executou o conjunto criptográfico OpenSSL nem validação GTK/Poppler integral. Não representa paridade com o original.

Há casos de integração adicionais para redação com geometria real/rotações e DSS/VRI com CMS real e cadeia/CRLs de PKI sintética. A próxima validação Linux deve executá-los e a suíte existente, preservando relatórios completos e examinando falhas/pulos. Não gerar/publicar Flatpak ou integrar ramos por inferência. Main, candidato 0.1.19, workflows da main, critérios/pesos e VM preservados.

## Primeira execução Linux — 23/10/2026, após 18:55

CI `40030258851`, revisão `40e8441`, terminou com falha real no novo teste de redação: o fixture reutilizava `marked.pdf` nas rotações 90/270, e a proteção contra sobrescrita recusou corretamente essas duas preparações. Não foi falha do algoritmo de geometria: esses subcasos não chegaram a executá-lo. O fixture passa a usar nomes distintos por rotação. O caso sem rotação, a recusa de anexo incompatível e os quatro casos criptográficos de VRI passaram no Linux. Os logs e ZIPs originais foram baixados com SHA-256 conferido, preservados fora do Git em `analysis-local/pdf-features-ci/40030258851-*`.

A primeira execução ainda não certifica a revisão corrigida. Aceitação e probes posteriores foram pulados porque a suíte falhou. A ampliação posterior de escrita VRI também exige outra validação da nova revisão. Não apresentar esse CI como sucesso ou repetir a mesma revisão sem uma mudança que justifique o novo teste.
