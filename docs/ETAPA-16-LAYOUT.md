# Etapa 16 — correção de geometria do painel lateral

Retomada em 17/10/2026, após a auditoria incremental da etapa 21. A captura do
Flatpak 0.1.2 mostrou recorte no cabeçalho e na barra de ícones lateral.
O código usa posição inicial de 158 px e permite `shrink=True` no primeiro
filho de GtkPaned. A hipótese é alocação menor que o mínimo dos widgets;
ainda precisa ser confirmada por medição GTK, antes da correção.

`scripts/check_sidebar_layout.py` mede cinco painéis em janelas solicitadas de
1180 e 760 px, origem/extensão de título, notebook e botões, mínimo solicitado
e área do leitor. Salva duas capturas da própria aplicação. O modo
`--observe-only` pode terminar com código zero e **passed:false**; isso é
observação de regressão, nunca aprovação do layout. Resultados e imagens serão
preservados por rodada. Comparação Foxit e VM não fazem parte desse teste.

Próximo passo: medir a fonte atual no Linux, corrigir a causa, executar testes
GTK e comparar as medidas/capturas. Fonte e pacote 0.1.2 ainda não alterados.
Critérios/pesos, roteiro 43,33% e paridade 0/25 permanecem preservados.
