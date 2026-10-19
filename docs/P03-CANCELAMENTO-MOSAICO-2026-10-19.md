# P03 — cancelamento ativo, N-up com4mm e mosaico

Revisão 2026-10-19T09:26:14-03:00, America/Sao_Paulo. Base publicada `e635d4a`. [Metadados e hashes](../testes/resultados/p03-2026-10-19-0113/review.json); [consolidado diferencial](../testes/resultados/p03-2026-10-19-0113/comparison-rollup.json). **P03 permanece parcial**, com novas lacunas resolvidas em recortes e outras ainda abertas. P01 provisória e P02 validada preservadas.

## Busca ativa D12

Após o reinício explicitamente autorizado, com cabo desligado, o usuário desbloqueou a sessão. Relógio e resposta do Notepad/Edit foram conferidos antes de executar o original. Tarefa0113 Interactive/Limited, script próprio com hash preservado, novo preflight: identidade Foxit2025.2.0.33046x86, dez Inputs/RX/contenção conferidos. Uma abertura original neste lote, PID1064; total três desde o pedido P01–P03. O reinício foi reset, não restauração de snapshot. Não implica autorização para reinícios automáticos futuros.

Corpus próprio12.pdf:5000 páginas,2.859.494bytes, SHA256 `ce3fde0e23fb8c6622d434e939a03fa9a50c208cb272b5b0483fc9501339edf3`, read-only fora dos dez Inputs; identidade novamente conferida. Frase exata alvo no documento atual; texto/marcadores/comentários ligados; palavra inteira/caixa/anexos/stemming/destaque global desligados.

- Stop enviado uma vez com trabalho ativo observado (Searching Bookmark/Stop). Após resposta, New Search e232 resultados parciais; PDF continuou aberto. Contagem232 permaneceu na observação posterior, com relógio01:12:23→01:12:57.
- Segunda busca ativa observada em178/5000. Troca para geometria.pdf1/8 deixou a pesquisa ligada a12.pdf, ainda ativa em354/5000 e404 ocorrências. Não mudou o alvo nem cancelou automaticamente nessa observação.
- Voltando a12.pdf, busca ativa1472/5000/1503 ocorrências. Fechar essa aba terminou o trabalho: só geometria ficou aberta, New Search e1738 resultados parciais ligados ao caminho12.pdf. Sem diálogo de erro/salvar. A lista não foi descartada pelo fechamento nesse contexto.

São contagens visuais atualizadas separadamente, dependentes do instante da ação; nenhuma medida de latência ou resultado universal. O contrato próprio de descarte de tarefas antigas não foi alterado nem aprovado como equivalente por esta observação. A tentativa0048 congelada continua inconclusiva e preservada.

## Impressão e saídas examinadas

Page Setting mostrou A4 retrato e quatro margens0.02inch. Advanced mostrou somente opções PCL, sem configurar drivers. Em Preferences/Measuring, a unidade foi alterada de Inches para Millimeters; o diálogo Print acompanhou a mudança. Nenhum ajuste de segurança foi modificado. A lista de categorias deslocou durante a rolagem e houve seleção incidental da categoria Security, seguida de saída para Print sem alterar controles.

**N-up:** Microsoft Print to PDF, All8pages, A4 retrato210×297mm, grade2×2, Horizontal, Margins4.0mm, sem bordas, Auto-Rotate/Auto-Center ligados, Document and markups. Nova saída13.pdf,84.582bytes, SHA256 `55717fe2d1e450c70718fb0bb388c354a3fc218909dd4a8555aa53560feba813`. Duas páginas595.32001×841.92004pt, Rotate0, sequência de conteúdo1/2/3/4 e5/6/7/8. As duas páginas renderizadas/examinadas. Protocolo C18-D18-nup e fixture preservados; comparação com medidas Linux já registradas coincide.106 arquivos atuais de app iguais ao CI39172130287; suíte403/403 histórica não repetida.

**Mosaico:** A4 retrato, escala200%, sobreposição5.0mm, Auto-Center ligado, Auto-Rotate inativo na UI; sem marcas/legendas, All8pages, Document and markups. Prévia inicial2×2 antes de confirmar sobreposição; após aplicação mostrou3×3 na primeira página. Primeiro OK deixou diálogo aberto enquanto o valor era aplicado; não presumir envio de job. Na retomada posterior, novo OK alcançou Salvar saída. Nova14.pdf,102.931bytes, SHA256 `e5d2cc1fe26158a8409bfe07237df6bc6f88dd4e2139b560c90402f444a9d8d7`.48 páginas A4/Rotate0. Rótulos PAGE1–8 nos índices de saída1,10,16,20,24,35,36,45; demais40 páginas sem pixels escuros no render40dpi. Todas48 renderizadas e mosaico de inspeção examinado; não é uma aprovação diferencial nem prova de erro nas páginas vazias, pois o corpus contém apenas um rótulo por página.

Livreto: ainda há um campo Margins, sem correspondência demonstrada aos parâmetros próprios separados safety5mm e gutter3mm. Page Setting/Advanced examinados não resolveram a medianiz. Não importar a saída anterior de5.08mm como protocolo correspondente. Geometria/margens físicas/rotações e outras combinações permanecem abertas.

## Continuidade, relógio e encerramento

Uma suspeita de parada em Page Setting foi conferida por capturas somente leitura separadas por10.55s externos; quadros distintos e relógio avançou. Não houve nova parada confirmada neste lote. Houve intervalo do trabalho até09:12, causa não determinada; na retomada, novo handle de janela, relógio avançando e contenção host/USB revalidados. O mesmo Foxit permanecia aberto; não houve relançamento. Horário do guest atrasou em relação ao host anteriormente; nenhum benchmark foi inferido.

Após salvar14.pdf, Foxit fechou normalmente. Ausência visual examinada e confirmada por manutenção breve previamente autorizada: Foxit/atualizador/splwow64 zero, fila vazia, identidade original/dez Inputs/corpus5000 preservados. Rede novamente desligada em finally. Observador0113 Ready/result0, sem recibo end; saída pelo prazo2h é inferência, não confirmação por recibo. Não enviar comandos ao coletor encerrado. Próxima execução exige RunId novo/preflight/controle visual.

Consolidado: **13 medições distintas iguais/quatro inconclusivas**, zero divergentes/aguardando. Doze iguais preservadas, uma nova; somente contagem/ordem N-up acrescentadas. Paridade integral0/25,50 planos S12 completos sem execução e19 critérios amplos ainda abertos; índice histórico45.13% não mede código reconstruído. Fonte/Flatpak0.1.13devel intactos; nenhum pacote novo.

Próximo lote: livreto com parâmetros correspondentes ou limite explícito; D07/D10 ativação/ordenação restantes; UI03/04/06/07/08/09/10 e disponibilidade Reader; ampliar operações das demais famílias e aceitação conforme plano. Causa da espera histórica em splwow64 continua sem explicação. Evidências privadas em analysis-local/vm-20261019-0113 e vm-20261019-0912; não publicar PDFs/capturas completas.
