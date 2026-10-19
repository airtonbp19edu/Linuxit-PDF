# P03 — interface de navegação, zoom e parada da VM

Checkpoint 2026-10-19T09:58:26-03:00, America/Sao_Paulo. Base publicada6aae418. [Metadados e hashes](../testes/resultados/p03-2026-10-19-0930/review.json). **P03 parcial e suspensa pela regra do relógio; usuário confirmou a parada e pediu encerrar por hoje.**

Novo lote0930, coletor Interactive/Limited, sessão1 não elevada. Original ausente na preparação; manutenção breve autorizada, cabo novamente desligado antes dos testes. Script próprio com hashb20ad4dca54ff33e7524df9d08702190539e0172ce3174dfe30b9118a277cac1, startupready/preflightcompleted, dez Inputs iguais ao postflight anterior e RX negado, identidade Foxit e contenção conferidas. Controle Notepad/marcador/menuEdit observado antes de launchcompleted/PID2380. Uma abertura neste lote, quatro desde o pedidoP01–P03. Sem reinício neste lote.

## Observações confirmadas

- UI03: sem documento, controles de página pálidos/desabilitados. Em geometria.pdf, Next1/8→2/8→3/8; Last→8/8. Next pálido no final; um clique manteve8/8.
- UI04: sem documento, zoom vazio/controles pálidos. Valor inicial113.99%; menu ofereceu1% e6400%. Após selecionar1%, menos manteve1%; após6400%, mais manteve6400%. FitPage exibiu47.15% e PAGE0011/8. Não se atribui a mudança de página a uma operação intermediária específica, pois o zoom mínimo mostrou várias páginas e as atualizações visuais eram tardias.
- Busca-escopos.pdf aberto em2/2,62.17%, marcadores visíveis. Painel Search alcançado, documento atual/frase exata; páginas/marcadores/comentários ligados, palavra inteira/caixa desligadas. Consulta não ficou visível nas tentativas de entrada; nenhuma busca submetida. Um press_key foi recusado pela ferramenta com aviso de entrada de usuário. Último clique em More enviado, expansão não confirmada. Não inferir falha do Foxit nem vínculo dos IDs7911/7913.

São variantes visuais delimitadas. Vínculo com IDs estáticos, valores arbitrários digitados, demais modos/rotação/CropBox/atalhos/foco permanecem abertos. Os planos originais de interface e50 planos completosS12 permanecem preservados, sem promoção para aceitação integral.

## Parada e estado preservado

Primeira suspeita09:53:02 foi descartada por capturas somente leitura:09:53:25→09:53:52. Depois, relógio09:54:23 permaneceu igual entre watch3.png e final.png, separados por35.598s externos; região do relógio pixel a pixel igual. As imagens completas têm diferenças, portanto não são declaradas idênticas. Usuário confirmou que a VM travou. Causa desconhecida; nenhum diagnóstico de falha Foxit ou esgotamento de tokens.

Entradas suspensas. Após constatação, somente inspeção/capturas host: VM running, cabooff, sem shares/USB, clipboard/dragdropdesativados, VRDE/áudiooff. Janela Foxit continua visível; PID final e estado do coletor0930 não reconsultados. Sem postflight, stop ou reciboend; dez Inputs eram iguais antes, integridade posterior desconhecida. Não conectar rede, matar processo, pausar ou reiniciar automaticamente. A autorização de reinício anterior já foi usada e não autoriza novos resets.

Transporte: quatro recibos completos do0113 arquivados e comparados com arquivos anteriores antes de liberar44 propriedades de resultado, usando confirmação recente de tarefaReady/result0. Command/Host/propriedades de sistema e arquivos guest preservados. Não reenviar comandos a coletores encerrados nem presumir0930 ativo após seu prazo.

## Retomada

Quando o usuário retomar e a VM responder, conferir segundos e controle visual; revisar original/coletor0930 sem repetir entradas pendentes. Conservar contenção e confirmar ausência do original antes de eventual manutenção breve. Conferir integridade e estado do observador; se encerrado, usar novo RunId/preflight/controle antes de nova execução. Prosseguir UI06/07/08/09/10, destinos/ordenaçãoD07/D10 e parâmetros correspondentes de livreto. Ampliar demais operações/aceitação conforme P03; não concluir o pacote com estes recortes.

P01 provisória e P02 validada preservadas. Consolidado13 métricas iguais/quatro inconclusivas, sem novo caso diferencial neste lote; paridade0/25,19 critérios abertos e índice histórico45.13% intactos. Porcentagem global da reconstrução continua indeterminada. App/Flatpak0.1.13devel intactos;403/400 testes históricos não repetidos. Privados em analysis-local/vm-20261019-0930; PDFs/capturas completas fora do Git. Ferramentas ComputerUse/@oai/sky, VBoxManage7.2.20, scripts próprios e inspeção Python somente dos registros.
