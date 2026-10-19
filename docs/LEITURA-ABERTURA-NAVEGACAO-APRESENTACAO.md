# Leitura: abertura, navegação e apresentação

Checkpoint 2026-10-19T10:53:45-03:00. Implementação dos itens1–3 solicitados pelo usuário; não se confunde com P01–P03 do plano de execução. Fonte candidata0.1.14, ainda em validação.

- Abertura transacional: mantém documento/página anteriores até validar candidato e render inicial. Senha pedida na interface, enviada por stdin ao worker e não salva em preferências/argv. Leitura de PDF cifrado usa representação privada descartável; salvar cópia, assinaturas e edição mantêm como referência o original. Sessão com leases adia limpeza até terminar leitores ativos.
- Recuperação consentida: tentativa tolerante de estruturas que o pypdf consegue interpretar, incluindo xref incorreto; rejeição explícita de arquivos irrecuperáveis. Original sem sobrescrita; a representação de leitura não é uma reparação certificada nem substitui assinaturas do original.
- Navegação: entradas inteiras limitadas ao documento; zoom digitável1–6400%, decimais, rejeição deNaN/infinito; modos ajustar página/largura e rotação. Viewport virtual conserva coordenadas lógicas sem alocar pixbuf do tamanho do zoom; raster continua com limites de resolução/pixels. A nitidez máxima continua limitada pelo raster.
- Apresentação: herda sessão/rotação, permite escolher monitor, solicita fullscreen na tela escolhida e trata remoção de monitor. F6 alterna página/controles, Tab usa foco padrão, Escape sai; atalhos da página não interceptam a navegação dos controles.

O pedido GTK de fullscreen não garante que o compositor o conceda; estado efetivo é acompanhado por evento. Referência: [Gtk.Window.fullscreen_on_monitor](https://docs.gtk.org/gtk3/method.Window.fullscreen_on_monitor.html). Recuperação tolerante é uma tentativa com limites, conforme [documentação do pypdf](https://pypdf.readthedocs.io/en/stable/user/robustness.html).

Validação inicial:14/14 testes portáveis, sem falhas/erros/skips; [relatório](../testes/resultados/leitura-2026-10-19/portable-initial.json). Linux/GTK, capturas e pacote ainda pendentes. Não representa aprovação de famílias ou equivalência Foxit. Usuário não tem ambiente Linux com dois monitores; controle de seleção/hotplug poderá ser simulado, validação física continua aberta. Impressão integrada da representação cifrada/recuperada permanece explicitamente recusada enquanto o fluxo de impressão próprio não for completado.

VM0930 permanece suspensa pelo relógio09:54:23; nenhuma entrada/rede/reinício nesta rodada. Comparações13 iguais/quatro inconclusivas preservadas;39 critériosdone/19abertos,45.13% histórico e paridade0/25 intactos. Último Flatpak publicado ainda0.1.13/devel; não anunciar0.1.14 como entregue antes de testes/publicação confirmados.
