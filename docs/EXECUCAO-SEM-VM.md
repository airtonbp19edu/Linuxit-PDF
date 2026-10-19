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
