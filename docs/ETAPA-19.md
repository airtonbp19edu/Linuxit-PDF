# Etapa 19 — correções próprias de impressão

Atualização posterior deste checkpoint: a [etapa 20](ETAPA-20.md) validou
fonte e Flatpak 0.1.2 em Linux, com 104/104 testes em cada ambiente
fonte/payload/sandbox e cinco casos GTK do painel. O relato abaixo
preserva os resultados e limites da rodada original.

Em **17/10/2026**, foram reproduzidos e corrigidos dois defeitos da
implementação própria em [`app/imposition.py`](../app/imposition.py).
O trabalho usa PDFs sintéticos e não depende da VM do Foxit. Não houve nova
observação ou incompatibilidade medida no original.

## Defeitos e comportamento corrigido

Páginas com `CropBox` começando fora de `(0,0)` eram dimensionadas pela largura
e altura do recorte, mas seu deslocamento não era descontado do conteúdo.
O resultado podia ficar descentralizado ou sair da região esperada no PDF
preparado para impressão. A normalização agora desloca conteúdo e caixas da
página para a origem da área visível, depois de aplicar a rotação intrínseca.
Isso é compartilhado por tamanho real/ajustado, N-up, livreto e mosaico.

Também foi reproduzida uma alteração indevida do conteúdo da página de origem
**em memória** ao normalizar sua rotação. A cópia rasa conservava a referência
indireta da página do reader; o `replace_contents()` do pypdf podia substituir
o stream do reader original. A cópia agora é desvinculada dessa referência
antes das transformações. A biblioteca pypdf não foi alterada. Os arquivos
PDF de entrada permaneceram intactos tanto antes quanto depois da correção.

### Medição antes/depois

Controle: dois PDFs próprios com o mesmo conteúdo visível de 200 × 300 pontos,
um com origem do recorte em `(0,0)`, outro em `(70,80)`. O marcador está a
20 pontos da borda esquerda e 30 da borda inferior do recorte. Saída A4 em
tamanho real, com área visível centralizada:

| Medida no PDF de saída | Antes | Depois |
|---|---:|---:|
| Posição X do marcador, recorte deslocado | 287,637795 pt | 217,637795 pt |
| Posição Y do marcador, recorte deslocado | 380,944882 pt | 300,944882 pt |
| Erro em relação ao PDF equivalente com origem zero | 70 pt / 80 pt | 0 pt / 0 pt |
| Conteúdo da página original em memória após normalizar rotação | Alterado | Preservado |

As posições foram medidas nas matrizes e baselines do texto do PDF reaberto,
com tolerância de 0,001 ponto nos testes. O código anterior foi carregado do
commit-base para reproduzir o controle no mesmo runtime pypdf. PDFs completos,
fonte anterior e medições ficam em `analysis-local/stage19-measurements/`.
Isso verifica colocação de conteúdo sintético; não é inspeção de pixels,
certificação de todo PDF ou teste de uma impressora física.

## Testes executados

[`tests/test_imposition_cropbox.py`](../tests/test_imposition_cropbox.py)
passou em **9/9 métodos**, sem falhas ou skips. Os casos cobrem:

- Origem positiva e negativa do recorte, tamanho real e ajuste.
- Rotações intrínsecas de 0°, 90°, 180° e 270°.
- Seis páginas por folha nas quatro ordens oferecidas pela interface.
- Livreto com encadernação esquerda/direita e ambas/frente/verso, com páginas em branco.
- Worker real nos modos tamanho, múltiplas e livreto.
- Mosaico em folha única e em tiles, inclusive página rotacionada, **sem marcas/legendas**.
- Preservação das entradas, da geometria/conteúdo em memória e do controle com origem zero.

Antes da correção, os oito métodos iniciais produziram **20 falhas de
asserção**, incluindo subcasos; só o controle com origem zero passou.
O relatório inicial não enumera individualmente todos os subcasos falhos no
campo `cases`; `failures` conserva a contagem do unittest. Após a correção,
os mesmos oito passaram; o caso de mosaico foi acrescentado e os nove passaram.
As três rodadas são preservadas, sem somar subcasos como métodos independentes.

- [Antes da correção](../testes/resultados/etapa-19-cropbox-before-2026-10-17.json).
- [Oito métodos corrigidos](../testes/resultados/etapa-19-cropbox-after-2026-10-17.json).
- [Nove métodos finais](../testes/resultados/etapa-19-cropbox-final-2026-10-17.json).
- [Medições e hashes antes/depois](../testes/resultados/etapa-19-cropbox-medidas-2026-10-17.json).
- [Conferência técnica do marco](../testes/resultados/etapa-19-verificacao-2026-10-17.json):
  sintaxe de 118 arquivos, 93 links locais, hashes das provas, fontes/licenças
  e critérios/pesos conferidos. Não substitui execução gráfica.

Repetir com nomes novos, no ambiente atual ou usando `/usr/bin/python3` no Linux:

```powershell
python scripts/run_tests.py --pattern test_imposition_cropbox.py --temp-dir analysis-local/cropbox-testes-novos --output testes/resultados/cropbox-rodada-nova.json
```

Também foram repetidos os 17 subconjuntos da etapa 18, copiando **os mesmos
oito arquivos**, byte por byte, da campanha preservada. O auxiliar local
substituiu somente o gerador de fixtures por cópia; as APIs/probes e os
contratos continuaram reais. **13 verificações passaram; quatro continuam
bloqueadas por Poppler**. Hashes de fixture e protocolo são iguais aos da
campanha anterior; o kit preparado para o Foxit permaneceu intacto. O novo
[relatório de regressão](../testes/resultados/etapa-19-campanha-regressao-2026-10-17.json)
registra a fonte atual, zero observações Foxit e resultados originais `null`.

## Estado de entrega e continuidade

Esta correção está na fonte em desenvolvimento após o Flatpak **0.1.1/devel**.
O pacote publicado não foi substituído. A cópia portável da etapa 17 e os
relatórios anteriores continuam como snapshots históricos; não aprovam a
fonte modificada nesta rodada. A validação GTK/Linux completa deve ser feita
antes do próximo empacotamento, conforme a [etapa 17](ETAPA-17.md).

O critério de regressões próprias da etapa 19 já estava `done` e recebe as
novas evidências. O de divergências com o Foxit continua `pending`, aguardando
o original na contenção offline. Etapa 19 **14,3%**, roteiro **43,33%**, paridade
**0/25**, catálogo original **209** e cobertura global desconhecida (`null`).
Critérios, estados, pesos e revisão preservados; a IA continua [excluída](ESCOPO.md).

Próximo passo: executar a suíte e inspecionar a saída em Linux com GTK/Cairo e
Poppler, incluindo o painel Anexos. Marcas/legendas de mosaico, PDFs com
estruturas mais complexas, geometria do Foxit e impressão física continuam
pendentes. A etapa 20 do novo marco depende desse runtime Linux para gerar e
testar o Flatpak atualizado. Registrar separadamente cada resultado e publicar
o próximo marco sem sobrescrever as evidências existentes.
