# P03 — busca e impressão no original offline

Revisão 2026-10-19T00:36:40-03:00, America/Sao_Paulo. Base publicada `5e81af8`. **P02 concluída; P03 parcial, com uma nova execução do original.**
[Metadados verificáveis](../testes/resultados/p03-2026-10-19-2359.json). Capturas, PDFs sintéticos gerados e relatórios completos ficam somente em `analysis-local/vm-20261018-2359/`, ignorado pelo Git.

## Ambiente e integridade

RunId2359 iniciado antes da meia-noite de18/10; observações funcionais em19/10. Coletor próprio corrigido `b20ad4dca54ff33e7524df9d08702190539e0172ce3174dfe30b9118a277cac1`, tarefa Interactive/Limited, sessão1 sem elevação. P02 já publicada foi preservada. Antes do lançamento, novo preflight offline e Notepad com marcador examinados; Foxit2025.2.0.33046x86, identidade preservada. Startup ready e pf/launch/col/c2/post/end completed recuperados integralmente.

Contenção host/guest aprovada: cabo off, sem shares/USB capturado/SMB; clipboard/drag-and-drop/VRDE/áudio desativados. Dez Inputs iguais ao baseline antes e depois; escrita negada em Reference/Input/Protocol. Duas conexões breves de manutenção no P03, com ausência visual prévia e consulta de processos no guest: início do observador e recuperação dos dois PDFs após fechar Foxit. Desconexão em finally confirmada; nenhum teste do original com rede ligada. Sem mudar proteção do host, pause/resume/reboot ou encerramento forçado.

Segundos acompanhados; último estado visual00:30:58, com avanço ao longo das ações. Não houve nova parada detectada nesta rodada. Capturas imediatas frequentemente precediam a pintura completa; foi feita nova observação antes de agir, sem repetir cliques. Isso não mede desempenho nem resolve a causa das paradas históricas.

## Resultados delimitados

|Recorte|Observação nova|Limite|
|---|---|---|
|D10 busca mista|Consulta alvo, frase exata, texto/marcadores/comentários; seis resultados: dois marcadores, três ocorrências de texto, uma nota. Texto: página2→1 e destaques alvo/ALVO/prefixo de alvoextra; nota selecionada e painel Format aberto.|Só o contexto e opções registrados; não aprova algoritmo completo ou ordenação geral. Nenhuma edição de anotação.|
|D07 marcadores|Somente marcadores: dois hits. Selecionar resultado realça item no painel esquerdo. Ativar ALVO marcador no painel nativo navega1→2, ajuste66.71%. Segundo item mantém página2 sem diálogo observado.|Selecionar/dar duplo clique no resultado não comprovou salto; não equivale a destino nulo. Enter retornou à nova busca. Outros meios/variantes ainda abertos.|
|Ordenação|Relevance Ranking exibido; seta pálida e clique sem alternativas na busca no PDF atual.|Indisponível nesse contexto; não concluir ausência de modos em coleção/índice.|
|D12 cancelamento|busca-longa.pdf250 páginas, mesma consulta/opções,250 resultados completos.|Terminou antes de observar Stop ativo; nenhum Stop enviado. Cancelar/trocar/fechar durante trabalho continuam inconclusivos.|
|UI05|Par correto busca-escopos.pdf + geometria.pdf, menu da aba ativa: Print All Tabs abre Batch Printing; No retorna às abas.|Don't ask again preservado desmarcado; nenhum lote físico enviado. Outras variantes continuam abertas.|
|UI02 sem documento|Após fechar os PDFs sem gravar, menu File mostra Print/Properties/Save/SaveAs/Close desabilitados; Batch Print visualmente habilitado.|Batch Print sem documento não foi ativado. Não prova todos os caminhos de impressão/atalhos.|
|D20|Fechamento normal após duas saídas virtuais. Ausência no Task Manager e consulta posterior: zero Foxit e zero splwow64.|A espera histórica em splwow64 não foi reproduzida nem explicada; impressão física não testada.|

O teclado direto do host não entregou todos os atalhos ao guest; a entrada funcional foi feita pelo teclado de tela nativo do VirtualBox, com observação entre ações. Falha de transporte de tecla não foi atribuída ao Foxit. Identificadores7911/7913 não foram resolvidos por estes resultados.

## D18 — saída PDF real, variantes ainda diferentes do protocolo

Microsoft Print to PDF, uma cópia, todas as oito páginas do Input geometria.pdf; Auto-Rotate/Auto-Center ligados, Document and markups, sem grayscale/image/border/overprinting. PDFs recuperados somente após fechar o original, hashes conferidos, reabertos pelo pypdf e seis páginas renderizadas pelo Poppler70dpi/examinadas visualmente. Rótulos legíveis, sem sobreposição/corte visível no recorte sintético. Isso não mede fidelidade universal nem margens efetivas.

|Variante privada|Saída e sequência do conteúdo extraído|Caixa por folha, pt|SHA-256|
|---|---|---|---|
|10.pdf, N-up2×2 horizontal, Portrait|2 páginas:1/2/3/4 e5/6/7/8|595.32001×841.92004; Rotate0|129cf5564dc27f8065f43471837f091029cb24be9f93cfdcb458776762637138|
|11.pdf, Booklet Left/Both|4 páginas:8/1,2/7,6/3,4/5|841.92004×595.32001; Rotate0|cc0b561aa21814884102e158e5b3155302bffc780208e6e2abe6e44aeabdb226|

Margem exibida0.200inch=5.08mm nos dois modos. O N-up C18 pede4mm, não configurados nesta variante; o livreto pede safety5mm/gutter3mm, ainda sem mapeamento equivalente ao único campo Margins examinado. Orientação no controle permaneceu Portrait; no livreto o papel/stream ficou paisagem. **Nenhuma métrica C18 foi importada ou promovida a match.** Ordem observada com estes parâmetros não substitui a comparação correspondente. Mosaico não executado neste lote.

## Estado final e retomada

Foxit fechado normalmente; consulta às 2026-10-19T00:30:37.6281409-03:00 confirmou zero processos Foxit/update e splwow64. Coletor end completed, tarefa Ready/result0, cabo off. Sete recibos próprios completos foram arquivados byte a byte antes de liberar 75 propriedades temporárias de resultado do observador encerrado; arquivos do guest e propriedades de sistema/Host/Command preservados. Tentativa anterior de arquivar1940 foi recusada por propriedade ausente, sem exclusão. Não enviar comandos aos observadores encerrados2020/2355/2359.

Próxima rodada: novo RunId/tarefa limitada, controle de segundos, ausência do original para manutenção já autorizada, novo preflight/controle visual offline antes de lançar. Se relógio ou resposta parar, observar após10s externos sem nova entrada, salvar e avisar; não reiniciar automaticamente.

Fila concreta:

1. D12: preparar corpus sintético mais lento e limitado, com identidade própria fora dos dez Inputs; obter evidência de trabalho ativo antes de cancelar/trocar/fechar.
2. D18: registrar equivalência dos parâmetros, unidades/margens e gutter; então gerar novas saídas e comparar. Executar mosaico separadamente.
3. D07/D10: comparar seleção e ativação como operações distintas; completar contexto de ordenação em coleção/índice alcançável e demais destinos.
4. Completar variantes UI01–UI10, disponibilidade do Reader e operações das demais famílias; investigar causa histórica D20 sem inferir por esta ausência.

Catálogo/contratos/matriz recebem apenas esta observação parcial. App e Flatpak0.1.13/devel intactos; nenhuma suíte Linux nova (403/403 fonte e400/400 pacote são históricos). Cinquenta planos completos S12 continuam not_run; 12 métricas iguais/cinco inconclusivas preservadas, paridade0/25 e globalnull. Checklist45,13%,39 done/19 abertos, pesos e critérios intactos. P01 provisória111/25 preservada. IA/UPDF excluídos e nuvem direta adiada. Ferramentas: Computer Use @oai/sky, VBoxManage7.2.20, scripts próprios/SSH de manutenção, pypdf/Poppler; sem REA estática nova nesta rodada.
