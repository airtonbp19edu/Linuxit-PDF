# Âncora do modo leitura após realocação — 23/10/2026

Registro Codex: 2026-10-23T16:32:48.170450-03:00. Ramo `codex/viewer-windows-anchor`, base Claude `bc17502`.

## Entrega recebida

Claude entregou explicitamente o caso às16:27 no minichat, depois de concluir sua
rodada de CI. O [Windows40006125900](https://github.com/airtonbp19edu/Linuxit-PDF/actions/runs/40006125900)
executou759 casos:751 aprovados, uma falha, zero erros e sete pulos Linux. O instalador
passou e a aceitação passou79/79. A falha foi em `test_viewer.py:80`, depois de navegar
para a página seguinte no modo leitura250%: `pan_y=0.0` com limite superior331.0.
Não era apenas uma guarda intencional de diagnóstico. Os JSONs foram preservados
por Claude em `testes/resultados/ci-ramos-2026-10-23/` na base deste ramo.

## Defeito demonstrado e correção

`_apply_pixbuf` já aplicava a âncora do topo. Porém, `_size_allocate` apenas limitava
o deslocamento anterior ao intervalo permitido. Se a página inicialmente coubesse
na altura disponível, o deslocamento ficava em zero; reduzir a área disponível
aumentava o limite superior, sem mover a página para esse novo topo. A altura dos
controles também pode mudar sem alterar as dimensões do canvas.

As funções reais de geometria, exercitadas com alocações sintéticas, reproduziram
zero versus331 antes da mudança. Agora, enquanto `_top_anchor` estiver ativa,
`_size_allocate` usa o novo limite superior como destino. Depois de o usuário
deslocar verticalmente a página, a âncora fica desativada e a posição escolhida é
preservada dentro dos limites existentes.

O mesmo resultado numérico foi reproduzido; a sequência exata de eventos da janela
na execução Windows que falhou não foi instrumentada. Portanto, não se afirma que
o CI nativo já esteja corrigido ou que a causa observada seja arredondamento.

## Verificação e limites

- Antes:1/3 cenários geométricos aprovados; falhavam a redução da área e a revelação dos controles.
- Depois:3/3 aprovados; o deslocamento manual continua preservado.
- Novo teste GTK cobre área1400→600, altura dos controles0→80 e deslocamento manual.
- Esse novo teste GTK e o teste Windows original **ainda não foram executados** nesta rodada.
- Os dois arquivos Python foram analisados sintaticamente; `git diff --check` passou.
- Nenhum CI foi disparado; a instrução vigente proíbe execuções duplicadas/nova rodada.
- VM, app da main, candidato0.1.19, workflows, releases, critérios e pesos preservados.
- Os quatro itens pausados e as outras frentes repassadas continuam aguardando sua autorização aplicável.

Evidências: `testes/resultados/viewer-windows-anchor-2026-10-23/`. O diagnóstico
geométrico pode ser repetido, a partir da raiz deste ramo, com:

```
python testes/resultados/viewer-windows-anchor-2026-10-23/probe_geometry.py
```

Isso executa métodos extraídos da fonte com valores sintéticos; não inicia GTK e
não substitui testes de apresentação no desktop Windows/Linux.

## Próximo passo

Em uma nova rodada de validação autorizada, executar `test_viewer` no Windows
nativo e no Linux/GTK, verificando tanto o caso histórico quanto o novo teste.
Examinar os JSONs e o comportamento de navegação antes de considerar o defeito
encerrado. Não integrar este ramo à main/candidato nem publicar versão por inferência.
