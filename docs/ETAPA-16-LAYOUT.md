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


Diagnóstico examinado: run39040540957, app do commit76d901e. O painel tinha
mínimo/alocação221, espaço158 e origemx=-63; título começava emx=-18. A captura
confirma recorte. O primeiro oráculo marcava passed:true porque comparava apenas
filhos com um ancestral também deslocado; essa aprovação era insuficiente e
não foi adotada. O oráculo agora exige contenção no corpo visível e posição do
divisor compatível com o mínimo. Raw inicial em
`analysis-local/sidebar-artifact-12104400034/`, ZIP SHA
46cc77d640bf78facb7b2c42945fe3cbbb30ef67a9a57e3af52e6c7bd241e132.

Correção em preparação: `shrink=False` no painel lateral, preservando o mínimo
calculado pelo GTK. Três testes reais cobrem cinco painéis/duas larguras,
divisor/ocultar/restaurar/leitura e nome longo de anexo. Fonte candidata0.1.3;
Flatpak publicado continua0.1.2 até nova validação. O CI de build repetirá a
fonte anterior e a atual com o mesmo oráculo corrigido, depois a suíte completa,
payload e sandbox. Nenhuma aprovação ainda atribuída a essa correção.
