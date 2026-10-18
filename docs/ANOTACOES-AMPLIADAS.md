# Anotações adicionais e edição de comentários

Fonte **0.1.13 em desenvolvimento**. O pacote publicado permanece 0.1.12 até
a validação integral da nova entrega. Os testes portáveis são próprios; a
execução GTK/Poppler e o novo Flatpak ainda aguardam CI.

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

Seis métodos GTK estão preparados: diálogos reais dos cinco tipos, edição e
limpeza de comentário/autor, erro/cancelamento, pixels Poppler dos cinco traços,
CropBox deslocado/rotação e busca de comentário após reabrir a cópia. Não contar
esses casos como aprovados antes da execução Linux.

Implementação própria em `app/pdf_annotations.py`, `app/pdf_changes.py`,
`app/edit_dialogs.py` e `app/edit_window.py`. Referências públicas: tipos,
QuadPoints e precedência de AP na seção 12.5.6.10/tabela 179 do
[ISO 32000-1 disponibilizado pela Adobe](https://opensource.adobe.com/dc-acrobat-sdk-docs/standards/pdfstandards/pdf/PDF32000_2008.pdf)
e [esclarecimentos de aparência da PDF Association](https://pdf-issues.pdfa.org/32000-2-2020/clause12.html).
Nenhum código/recurso Foxit foi usado. Família completa ainda parcial,
paridade 0/25 e roteiro 43,93% preservados; original não executado.
