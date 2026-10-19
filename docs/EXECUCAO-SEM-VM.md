# Execução abrangente sem VM — 19/10/2026

Pedido: completar todo trabalho que não exige executar o Foxit na VM. O estado
por pacote está em `progresso/execucao-sem-vm.json`. Nuvem direta23 permanece
adiada e IA generativa excluída. Nenhum comando é enviado à VM suspensa.

Baseline preservado:0.1.15/d0a6213,490 testes próprios por ambiente. Fonte0.1.16
em desenvolvimento; novo código ainda não tem aprovação Linux/pacote até seus
relatórios serem examinados. Critérios/pesos/paridade integral intactos.

## S01 — seleção por caractere e cursor

Ferramenta Caracteres, separada da seleção por região existente. Usa offsets e
caixas reais PopplerGLib, sem dividir igualmente a largura de palavras. Arrasto
em qualquer direção, seleção parcial, cursor, setas visuais, Shift para ampliar,
Home/End e Ctrl+A/C. Combinações, ZWJ, modificadores de tom e pares regionais são
agrupados para evitar cortes internos nesses casos. Não é implementação integral
de todas as regras Unicode de grafemas nem correção universal da ordem de um PDF.
Conserva a ordem Unicode entregue pelo extrator; não inverte strings RTL.

Até100000caracteres por página; divergência entre caixas e texto é recusada.
Worker isolado/cancelável, sessão autenticada com lease e permissão de cópia.
Cache e callbacks vinculados à sessão/página/rotação. Seis portáveis passaram;
dois testes Linux/GTK preparados, incluindo largura variável real e CropBox/rotação.
Novo typelib PopplerGLib e biblioteca pareada integram a receita de build.

Referência: [PopplerPage/get_text_layout](https://poppler.freedesktop.org/api/glib/poppler-Poppler-Page.html).
Esse contrato próprio não é observação Foxit nem aceitação de toda a família.

## Fila

S02 eventos/cálculos; S03 anotações; S04 sessão autenticada em edição/impressão;
S05 anexos/índice/idiomas; S06 confiança/tempo; S07 voz/medidas; S08 camadas/mídia/3D;
S09 preferências/conversão/OCR; S10 integrações/plataforma; S11 contratos/aceitação
e estática; S12 suíteLinux/entrega/auditoria. Cada pacote registra o que foi
implementado/testado e o que depende de recursos/contratos ainda indisponíveis.
Não substituir validação física ou do original por testes sintéticos.


## S02 — eventos de formulário

AFSimple_Calculate SUM/AVG/PRD/MIN/MAX e AFRange_Validate são reconhecidos por
gramática fechada; nenhum JavaScript é executado. Até128 regras/256 resultados,
dependências até64 níveis, ciclos recusados, Decimal28dígitos e módulo até1e18.
Entrada usa ponto decimal, vazio vale zero no cálculo. Não há formatação/localização
ou eventos arbitrários; ações fora do contrato impedem este preenchimento com eventos.
Preenchimento simples anterior permanece disponível. Campo calculado não é entrada
editável; readonly e AP são preservados. Sete portáveis passaram/umGTK pendente.
Referência dos nomes: [Adobe Forms](https://opensource.adobe.com/dc-acrobat-sdk-docs/library/jsdevguide/JS_Dev_AcrobatForms.html).
XFA e JavaScript geral permanecem abertos; não são dependências de VM para implementação.

## S03 — geometrias, texto e conversas de anotação

Polygon/PolyLine/Caret vetoriais próprios, FreeText/Stamp com Pango/Cairo e fontes
incorporadas na aparência. Texto Unicode até4096caracteres; área clipa conteúdo
excedente e precisa ser dimensionada pelo usuário. Não usa recursos Foxit.
Mover anotações simples atualiza Rect/Vertices/QuadPoints/L/InkList; preserva AP
relativa. Editar resposta conserva IRT; full text do editor limitado a1MiB agregado,
sem substituir comentário longo pela prévia truncada. Popup cria/atualiza Parent,
Open e Rect. Excluir conversa inclui descendentes/popups até2000 objetos, recusando
bloqueios/vínculos entre páginas. Arquivo original e cópias anteriores preservados.
Sete portáveis passaram; dois Linux/GTK/renderização com pixels aguardam execução.
Na primeira rodada houve correção da conversão de FloatObject de geometria para
float e da asserção de BooleanObject (usar value, não bool do wrapper); guardas
não foram relaxadas. Regressões anteriores16+21 passaram integralmente.

## Validação S01 intermediária

CI39298287332/f3212ef:498/498 Linux,0falhas/erros/skips, oito novos casos e490
anteriores preservados; AT-SPI/portal sintéticos também passaram. ZIP baixado e
digest0b3196db7b7aa90fc5cecca21b93756f6234a8f53e12b4f6564ed1625ebf7184 conferido,
após timeout de leitura recuperado com streaming64KiB. Relatórios públicos em
testes/resultados/sem-vm-2026-10-19/s01/. Isso é histórico da primeira revisão;
S02/S03 e extensão posteriorPango de grafemas exigem nova execução. A extensão
usa is_cursor_position de PangoLogAttr para limites Unicode completos do engine
instalado; fallback portátil cobre somente os grupos explicitados nos testes.
[PangoLogAttr](https://docs.gtk.org/Pango/struct.LogAttr.html).


## S04 — edição/impressão autenticada e filaCUPS

A credencial da sessão é mantida apenas em memória privada e transportada por
stdin para o worker; nunca integra argv, info, índice ou relatórios. Não há
promessa de apagamento seguro de strings Python. Close retira a referência.
Edição de cifrado valida tipo de operação: anotar/preencher/alterar/montar
conforme flags e credencial usuário/proprietário. Assinaturas/XFA/portfólios
continuam protegidos pelos guardas do editor. A cópia mantém criptografia,
identidades de senha e permissões originais; não vira PDF aberto. Adaptador
específico do pypdf6.20.1 usa seu objetoEncryption/entradaDictionary eID original;
roundtrip RC4-128/AES-128/AES-256-R5/AES-256 conferido com ambas as credenciais.
A primeira prova usou referência indireta como _encrypt_entry, incompatível com
o writer; corrigido para DictionaryObject antes da implementação/validação.

Editor com histórico e ações rápidas recebem a autorização capturada; senha
inválida/permite-não/alteração externa impedem publicação. Impressão usa a
representação atual de leitura, inclusive camadas, com leases que mantêm os
bytes até terminar a preparação. O diálogo mantém sua origem ao trocar de
documento. A saída de impressão é derivada e não preserva assinatura/proteção;
salvar saídaPDF exige permissão de cópia. Restrição de baixa qualidade impõe
raster150DPI no backend, independentemente da escolha visual.

Trabalhos CUPS capturados pelo recibo desta execução podem ser consultados e
cancelados no menuArquivo. IDs são validados e passam como argumentos semshell.
Ausência na fila ativa não é registrada como impressão concluída. A confirmação
de cancelamento pertence ao CUPS e não recolhe páginas já impressas. Probe CI
usa scheduler próprio somente127.0.0.1, fila sintética com trabalho retido e
cancelamento real; não usa impressora física, VM ou fila de outro usuário.
10 novos portáveis passaram;2GTK e probe real pendentes na nova fonte.
Referências: [CUPS cancel](https://www.cups.org/doc/man-cancel.html) e
[CUPS opções](https://www.cups.org/doc/options.html).

## Validação consolidada S01–S03

CI39300179043/fonte5a4729e:516/516 Linux sem falhas/erros/skips. Inclui
grafemas nativosPango, edição de formulário via diálogo, renderização Unicode
FreeText/Stamp com fontes incorporadas/pixels, geometrias/conversas e490 IDs
anteriores preservados. Artefato12211916533/ZIP08117925d8e00647fac2c72ac06ebf00116e6a78b597071159f47f97c593f3db
conferido. Relatórios emtestes/resultados/sem-vm-2026-10-19/s01-s03/. Não aprova
a fonteS04 posterior nem significa paridade integral comFoxit.

## S05 — anexos, idiomas e recuperação

Fonte0.1.16: pesquisa passiva inclui cabeçalhos/rodapés/notas DOCX, estilos ODT,
XLSX (texto compartilhado/inline e valores em cache, sem calcular fórmulas),
PPTX (slides/notas, ordem das partes não promete ordem visual) e RTF Unicode.
Objetos/macros/instruções não executados. Limites:2MiB expandidos/256partes,
XML128níveis. Radicais:36 opções dos algoritmos Snowball3.1.1 já distribuídos,
sem detecção automática de idioma.

OCR de imagens anexas é opt-in, PT/EN local:uma imagem,2MiB/10MP, até10imagens
e90s por busca,30s por imagem; resultados sempre sinalizam precisão desconhecida.
GIF/TIFF multipágina recusados neste extrator. PDFs anexos preservam outro contrato.

Índices:backup exclusivo; recuperação valida hash/esquema, guarda o destino
anterior antes de substituí-lo e verifica concorrência. Fontes alteradas permanecem
excluídas dos hits. Trava nova contém host/pid/token:remoção somente explícita,
processo local comprovadamente encerrado e identidade ainda igual. Travas legadas,
remotas ou ativas preservadas. Cleanup não remove trava substituída.
11 testes portáveis passaram; OCR nativo aguarda Linux. A suíte anterior S04
aprovou528/528 e portais/AT-SPI. Fila CUPS isolada teve falha de configuração
(backend socket ausente); corrigida para backend IPP instalado, repetição pendente.
Falha preservada em testes/resultados/sem-vm-2026-10-19/s04/.

## S06 — CA/CRL e carimbos de tempo selecionados

Política técnica explícita offline:CA PEM,CRL PEM/DER,tempo com fuso,OpenSSLCMS
verifica criptografia/cadeia/expiração e uso da chave do signatário. Revogação
exigida precisa CRL completa válida; desconhecida não vira aprovada. Âncoras
exigem BasicConstraints CA. Sem confiar automaticamente em raízes do CMS ou SO.
Carimbos RFC3161 de atributos não assinados são verificados contra os bytes da
assinatura e as mesmas CAs selecionadas; hora só é exibida como verificada
quando o token passa. ASN.1 via pacote Debian asn1crypto (MIT), atribuído pelo build.
Não implementa PAdES-LTV, validação legal, OCSP online, DocTimeStamp separado,
assinaturas incrementais/adicionais nem suporte universal a tokens. Esses
contratos permanecem abertos, sem alegar dependência de VM.5testes preparados,
incluindo CA/CRL/TSA sintéticas reais; validação nativa pendente.
Referências:[CMS](https://docs.openssl.org/3.5/man1/openssl-cms/),
[RFC3161/OpenSSL](https://docs.openssl.org/3.5/man1/openssl-ts/).

## S07 — voz e restrições de medidas

Ouvir texto gera WAV privado pelo worker e abre reprodução local GStreamer com
reproduzir/pausar/parar/volume. Fonte do pipeline é filesrc, nunca URI/playlist;
sem iniciar mídia ao abrir um PDF. Diálogo reutilizável com vídeo GTK. Dependências
Debian e licenças entram no runtime atribuído; saída PulseAudio no Flatpak.
Testes usam fakesink e não comprovam alto-falantes físicos. Teclado/leitor de tela
real e áudio físico permanecem pendentes. Medidas ganham grade PDF em pontos e
restrição angular45graus/Shift explícitas, preservando cálculo/calibração próprios.
Não promete encaixe automático em caminhos vetoriais do PDF.4testes novos
preparados (1portável e3GTK/GStreamer), aguardando Linux.

S04/S05 no commit53b4fd5:540/540 Linux e fila CUPS isolada4/4 aprovados, relatórios
examinados em testes/resultados/sem-vm-2026-10-19/s05/. Primeiro erro de configuração
preservado; repetição IPP corrigida sem impressora física. Novo código S06/S07
não herda a aprovação desse commit e ainda precisa seu próprio CI/pacote.

## S08 — visibilidade salva e mídia incorporada

Visibilidade salva em nova cópia via operação de edição, com permissão modify,
criptografia/senhas preservadas e guardas de campos/assinaturas existentes.
Não equivale a achatar camadas nem avaliar todas as configurações opcionais.
Movie/RichMedia com arquivos incorporados, Sound PCM8/16bits e3D podem ser listados
ou extraídos. Referências externas ignoradas, nenhum evento/JavaScript é acionado.
PCM PDF convertido para WAV; streams até64MiB,até256recursos/5000páginas.
Reprodução explícita de áudio/vídeo via filesrc/decodebin e codecs locais.
3D tem somente extração; renderizador U3D/PRC ainda é trabalho aberto sem VM.
Cinco testes portáveis passaram para preservação,PCM e cópia criptografada.

## S09 — padrões de ferramentas e OCR escolhido

Preferências atômicas/validadas de idioma/velocidade de voz,idioma/layout/DPI OCR;
configuração própria sem caminhos/senhas,chaves ou conteúdo. OCR permite escolher
páginas únicas e layouts Tesseract3/6/11. Demais páginas são copiadas sem OCR.
O contrato de cópia OCR ainda não preserva toda a estrutura documental; não é
conversão de layout universal nem edição textual do PDF. Limites20páginas/150MP
preservados.3portáveis novos passaram; teste nativo Poppler/Tesseract preparado.

Rodadaaeafdea:549testes,548aprovados/1falha RFC3161. Reprodução nativa3/3 passou;
CA/CRL também passaram. A falha era uso no subcomando ts de opções exclusivas CMS;
foram substituídas por repositórios vazios explícitos para impedir raízes implícitas.
Resultado corrigido ainda pendente;não declarar549/549. Evidência da falha preservada
em testes/resultados/sem-vm-2026-10-19/s06-first/.
