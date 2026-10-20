# Anotações adicionais e edição de comentários

Fonte e Flatpak **0.1.13/devel**, validados com 400/400 testes próprios em
fonte/payload/sandbox instalado, sem falhas/erros/skips. Novos: 14 portáveis e
seis GTK/Poppler; todos os 380 IDs anteriores preservados. Publicação/auditoria nas notas.

Em **Arquivo → Editar cópia com desfazer/refazer…**, há cinco operações novas:

- **Sublinhar área**, **Tachar área** e **Sublinhar área com ondulado**: uma
  área horizontal, informada manualmente em pontos PDF. O sublinhado fica na
  base da área; o tachado passa pelo meio. Não há seleção automática de palavras,
  múltiplas linhas ou quadriláteros inclinados nesta operação.
- **Adicionar elipse**: contorno vermelho sem preenchimento, inscrito na área.
- **Adicionar linha**: dois pontos, em qualquer direção, incluindo horizontal
  e vertical. Sem pontas de seta, medida/calibração ou legenda.

As coordenadas usam o espaço PDF **antes da rotação da página**, dentro do
CropBox. O traço é vermelho, com largura até 1,25 ponto, reduzida em áreas muito
pequenas. A aparência é embutida como um Form XObject sem fontes ou recursos
externos. A elipse usa quatro curvas Bézier; o ondulado usa segmentos com junções
arredondadas e contagem limitada. São escolhas do Linuxit, sem pretensão de
reproduzir o estilo do Foxit.

Uma área precisa ter largura e altura de pelo menos 0,25 ponto; a linha precisa
medir pelo menos 0,25 ponto. O CropBox precisa ter ao menos 0,25 ponto em cada
dimensão. Coordenadas ficam entre −10 milhões e +10 milhões de pontos.
A espessura junto à borda pode ser recortada pelo CropBox. Não há cor, espessura,
opacidade ou geometria ajustáveis após a criação neste subconjunto.

## Comentários e exclusão

**Editar comentário da anotação** permite escolher uma anotação da página e
alterar comentário e autor. Aceita múltiplas linhas, comentário vazio e autor
vazio; autor vazio remove o campo `/T`. A operação preserva posição, aparência,
cor, tipo e demais propriedades. Não modifica assunto `/Subj`, respostas ou
texto do conteúdo da página. Até 64 KiB UTF-8 de comentário e 4 KiB de autor.

Edição de comentário e exclusão aceitam Text, Square, Highlight, Underline,
StrikeOut, Squiggly, Circle e Line desbloqueados. Flags ReadOnly/Locked/
LockedContents, `/IRT`, `/Popup`, `/Parent` ou dependentes em outra anotação
impedem a operação. O backend confere os vínculos novamente; um item listado
pode ser recusado se tiver dependentes. Widgets, links, FreeText, Ink, carimbos
e outros tipos continuam fora dessas alterações. Listagem limitada a 2.000
registros e 1 MiB somando comentários e autores, com truncamento informado.

Exclusão é lógica; não é redação nem remoção segura de bytes órfãos. Documentos
criptografados, assinados/com campos Sig, `/Perms`, XFA e portfólios continuam
recusados para edição. Nenhuma ação ou script PDF é executado.

## Histórico e gravação

Cada alteração aceita passa pelo worker, grava uma cópia temporária e a reabre
antes de avançar o histórico. Desfazer/refazer atua no rascunho de até 100 passos.
Uma alteração inválida preserva cursor e ramificação de refazer. Salvar exige
nome novo, identidade SHA-256 da fonte e publicação exclusiva; original e cópias
já salvas permanecem intactos. Fechar ou cancelar invalida callbacks; uma
interrupção forçada pode deixar saída já concluída ou temporário, então confira
o destino antes de repetir. O [contrato anterior](EDICAO-COM-HISTORICO.md) continua.

O protocolo `linuxit-copy-edit-info-v1` acrescenta `author` a cada registro de
`annotations`. Criação usa `kind`, `page`, `text` e `rect`; linha usa `points`
no lugar de `rect`. `update-annotation` usa `page`, `index`, `text` e `author`.
Índices usam base zero e sempre se referem ao documento atual do rascunho.

## Evidências e limites

14 métodos portáveis novos cobrem objetos de aparência indiretos, metadados,
limites, coordenadas/rotação, exclusão, bloqueios/vínculos, comentários Unicode,
worker e histórico real. A primeira execução passou, mas a revisão detectou
streams de aparência diretos e avisos na clonagem. O adaptador passou a registrar
os streams como objetos indiretos antes da anotação; verificações posteriores
exigem essa estrutura. Relatórios anteriores preservados.

Seis métodos GTK passaram em cada ambiente: diálogos reais dos cinco tipos,
edição e limpeza de comentário/autor, erro/cancelamento, pixels Poppler dos cinco
traços, CropBox deslocado/rotação e busca de comentário após reabrir a cópia.

Implementação própria em `app/pdf_annotations.py`, `app/pdf_changes.py`,
`app/edit_dialogs.py` e `app/edit_window.py`. Referências públicas: tipos,
QuadPoints e precedência de AP na seção 12.5.6.10/tabela 179 do
[ISO 32000-1 disponibilizado pela Adobe](https://opensource.adobe.com/dc-acrobat-sdk-docs/standards/pdfstandards/pdf/PDF32000_2008.pdf)
e [esclarecimentos de aparência da PDF Association](https://pdf-issues.pdfa.org/32000-2-2020/clause12.html).
Nenhum código/recurso Foxit foi usado. Família completa ainda parcial,
paridade 0/25 e roteiro 43,93% preservados; original não executado.

## Entrega validada — 2026-10-18T13:35:28-03:00

[CI](https://github.com/airtonbp19edu/Linuxit-PDF/actions/runs/39144523775), fonte `b44476272e4e9011c5b4825ab00c8d78830354f1`:400/400 em cada ambiente.
[Revisão](../testes/resultados/0.1.13/validation-review.json), [manifesto](../releases/manifest-0.1.13.json).
Capturas do editor, comentário, página com cinco traços e janela principal examinadas.
Demais hashes conferidos. 106 arquivos app iguais entre fonte/payload; runtime
2849 arquivos, 224 ELF e 162 avisos de pacotes.
Sem nova dependência. Bundle 44662456 bytes,
SHA256 `0fa316cdb5bbf124dc411d79fad7135f77cbbeb3c158f319833b3ef33f6ad024`. Desenvolvimento devel, sem assinatura digital.

## Publicação e auditoria independente — 2026-10-18T13:41:41-03:00

Entrega `93a38c318bf9a8859c21c91e9b4eb3f43d49785a` confirmada no remoto. [Auditoria](https://github.com/airtonbp19edu/Linuxit-PDF/actions/runs/39145924664)
reinstalou o mesmo bundle, sem rebuild: 106 arquivos app,
2849 de dependências, 224 ELF e 162 avisos de pacotes conferidos,
incluindo modelos por/eng. Sete controles do auditor e cinco novos smoke checks
passaram. As suítes completas 400/400 continuam evidência do builder anterior;
não foram repetidas pela auditoria. [Relatórios](../testes/resultados/0.1.13/audit/review.json).
Download público sem login conferido por tamanho e SHA-256:
[recibo](../testes/resultados/0.1.13/download-integrity-2026-10-18.json).
As limitações e os 20 critérios abertos continuam; não há observação Foxit.

## Redação: marcar (E14) e aplicar (E15) — 2026-10-20

**Marcar** (`add-redaction`, rascunho de edição → "Marcar área para redação"):
uma área retangular dentro do CropBox vira uma anotação `/Redact` pendente com
`/Rect`, `/QuadPoints`, `/IC` preto (cor usada ao aplicar), `/BS` tracejado e
aparência própria com contorno vermelho tracejado. Nada é removido: o texto
marcado continua visível e extraível. A marca aparece na lista de comentários e
pode ser redimensionada (os QuadPoints acompanham), recolorida, comentada ou
excluída com as operações existentes.

**Aplicar** (botão "Aplicar redação em cópia nova…" do rascunho; comando de
worker `redact-copy`, módulo `app/pdf_redaction.py`): usa o estado atual do
rascunho (ou o arquivo aberto, se o rascunho estiver vazio) e grava uma cópia
nova; original e rascunho ficam intactos.

- Cada página com marcas é renderizada pelo Poppler sem anotações e sem
  rotação, a 150 ou 300 DPI; as áreas são pintadas com o `/IC` da marca (com
  margem de um pixel) e o conteúdo da página é trocado por essa única imagem.
  Texto, desenhos e imagens da página deixam de existir; o texto que sobrou fora
  das áreas continua visível, mas não é mais selecionável nem pesquisável.
- Páginas sem marcas mantêm o conteúdo byte a byte.
- Marcas aplicadas e anotações sobre as áreas (com seus popups e respostas) são
  removidas; outras anotações ficam. Campo de formulário sob uma área faz a
  operação ser recusada.
- Objetos que ficaram sem referência são descartados antes de gravar, para que
  o conteúdo antigo da página não permaneça no arquivo. Uma imagem compartilhada
  com outra página continua existindo porque ainda é usada lá.
- Se houver árvore de estrutura (PDF marcado), ela é removida, pois pode conter
  o texto (ActualText/Alt) e passaria a apontar para conteúdo inexistente.
- Texto de sobreposição (`/OverlayText`, `/RO`) de marcas criadas por outros
  programas é ignorado e contado no resultado.
- Recusados: PDF criptografado, assinado ou com `/Perms`, XFA, portfólio,
  ausência de marcas, mais de 50 páginas marcadas ou 512 marcas, páginas acima
  de 45 megapixels, destino existente.
- Não verificados: títulos de marcadores, metadados, anexos, nomes de campos e
  textos em outras páginas. A redação só cobre o que está desenhado sob as áreas.

Testes: `tests/test_redaction_marks.py`, `tests/test_redaction_apply.py`
(varredura de todos os objetos decodificados da cópia), `tests/test_redaction_gtk.py`;
aceitação S12-14-7 a S12-14-10.
