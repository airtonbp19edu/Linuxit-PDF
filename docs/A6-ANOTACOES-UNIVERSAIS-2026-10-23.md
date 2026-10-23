# A6 — edição de qualquer tipo de anotação (regra única)

**2026/10/23 às 11:21 (America/Sao_Paulo, UTC-03:00), Claude.** Etapa 2 da lista pedida pelo usuário
às 09:10 ("fazer o que não precisa de mim nem da VM"), confirmada às 10:53. Ramo
`claude/anotacoes-universais` (1df4aba), a partir da `main` 32cb630. Não integrado à `main`.

## O que mudou

`app/annotation_universal.py` decide, para cada anotação que não é campo de formulário, se ela pode
ser movida, redimensionada, excluída, ter o texto editado, a cor ou a opacidade alteradas. A mesma
decisão aparece na lista do diálogo (com o motivo das recusadas) e é aplicada ao salvar a cópia.

| Situação | Mover / tamanho | Excluir | Texto | Cor | Opacidade |
|---|---|---|---|---|---|
| ReadOnly (flag 64) | não | não | não | não | não |
| Locked (128) | não | não | **sim** | não | não |
| LockedContents (512) | sim | sim | não | conforme tipo | sim |
| Nota com popup | move junto com o popup | só a folha e seu popup | sim | sem aparência própria: sim | sim |
| Nota com respostas | sim (respostas ficam) | não: usar "Excluir conversa" | sim | idem | sim |
| Link, mídia (Screen/Sound/Movie/RichMedia/3D), anexo, carimbo, tipo desconhecido | sim | sim, salvo alvo de ação de mídia | descrição (sem autor quando não é marcação) | só ícone sem aparência | sim |
| Ligada à árvore de acessibilidade | sim | não | sim | conforme tipo | sim |
| Ícone de tamanho fixo (NoZoom, flag 8) | move; tamanho não | sim | sim | conforme tipo | sim |
| Vínculos malformados, outra página ou /RT Group | não | não | conforme caso | — | — |
| Campo de formulário (Widget) | fluxo de formulários | | | | |

Redimensionar transforma todas as coordenadas (`/Rect`, `/QuadPoints`, `/Vertices`, `/L`, `/CL`,
`/InkList`, `/RD`). Desenhos que o próprio Linuxit sabe refazer (formas, linhas sem setas, destaques,
desenhos, polígonos) são redesenhados; aparências de outros programas (setas, nuvens, tracejados,
fontes do autor, imagens) são mantidas e o visualizador as estica pela regra BBox→Rect do padrão.
A opacidade envolve qualquer aparência sem reescrevê-la, e repetir a mudança reaproveita o mesmo
envoltório. Cor só muda onde o redesenho é fiel ou em ícones sem aparência, que o visualizador
desenha pela cor `/C`.

## Validação

CI Linux [39967990215](https://github.com/airtonbp19edu/Linuxit-PDF/actions/runs/39967990215), revisão
limpa 1df4aba: suíte própria **753/753** (744 anteriores + 9 novos), aceitação própria **81/81**.
Testes novos: `tests/test_annotation_universal.py` (7: capacidades e motivos, mover com popup,
exclusão sem vínculos soltos, redimensionar mantendo aparências alheias, opacidade com renderização
Poppler, travas, tipos desconhecidos/mídia), um teste GTK do diálogo e um de linha redimensionada.
IDs anteriores preservados. Expectativas alteradas, todas pela nova regra: Locked permite editar
conteúdo e LockedContents permite excluir (ISO 32000-1 12.5.3); nota sem aparência aceita cor e
tamanho; linha redimensionável; S12-14-4/6 continuam casos de recusa, agora com nota travada e ícone
NoZoom. [Evidência](../testes/resultados/a6-anotacoes-2026-10-23/review.json).

## Limites

Respostas não se movem com a nota; grupos `/RT Group` não são editados separadamente. Aparências de
outros programas mudam só a opacidade e, ao redimensionar com escala desigual, os traços podem
engrossar. Excluir anexo não garante apagar os bytes anexados. Flatpak e Windows desta mudança ainda
não executados; ramo fora da `main`. Não é paridade Foxit nem família integral; critérios e pesos
inalterados. Sem VM, Foxit ou publicação.
