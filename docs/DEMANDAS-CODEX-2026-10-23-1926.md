# Demandas recebidas do Claude em 23/10/2026 às 19:26

**Ordem humana posterior nesta conversa:** “não é mais pra acompanhar; você vai assumir a dianteira agora e fazer tudo que está pendente dos meus pedidos ao Claude”. Codex assumiu a execução, revisão dos resultados e correções; a automação de acompanhamento foi excluída. Não se trata mais de aguardar atividade/inatividade do Claude. As entregas e decisões específicas abaixo continuam preservadas.

O usuário pediu nesta conversa que o Codex se atualizasse e iniciasse as demandas. A lista foi conferida no `CHAT-CLAUDE.txt` e no commit remoto `b82d106`. Os quatro recortes anteriores já estão implementados no ramo `codex/authorized-pdf-features`, entrega `e1ad5d1`, fonte `f34bddd`: 779/779 testes Linux e 81/81 aceitações próprias. Não repetir essa validação de fonte como se estivesse pendente.

## Ordem e limites

| Frente | Trabalho a executar | Estado ao iniciar esta retomada |
|---|---|---|
| Viewer Windows | Validar `a47309e` no Linux/GTK e Windows nativo completo com instalador; examinar o teste histórico e a nova regressão | CI Windows `40034106367` e Linux `40034116130` iniciados; não duplicar |
| Flatpak dos quatro recursos | Construir e testar fonte, payload e sandbox de `e1ad5d1`; examinar todos os relatórios e pulos | CI `40034126311` iniciado; artefato de teste, sem release |
| S1 busca | Seguir consumidores reais das opções +3/+0xc, regra/unidade da proximidade, escapes e erros; usar os resultados anteriores | Análise dirigida iniciada; S1 continua parcial |
| S3 | Consumidores das preferências +0x2bc/+0x204 e motores de anotações, campos, assinaturas e OCG | Na fila após o recorte S1 |
| S4 | Continuar reflow a partir do lote preservado | Na fila |
| Desktop Linux | Portal persistente, associação e atualização/reversão no ambiente de teste | Na fila; não equivale ao desktop físico |
| TSA | Consulta opt-in à URL escolhida pelo usuário; preservar contrato em duas fases | Na fila; não escolher nem contactar serviço arbitrário |
| Redação vetorial | Ampliar conteúdo complexo atualmente recusado, mantendo atomicidade e limites explícitos | Na fila |
| Windows dos quatro recursos | Preparar uma fonte de teste compatível com os ajustes Windows, identificar exatamente as diferenças e validar com instalador | Na fila; o ramo atual ainda não contém todos os ajustes Windows do Claude |
| Critérios amplos | Avançar nas evidências sem redefinir universo, critérios ou pesos | Abertos; B3 depende do usuário |

O Codex usa `codex/current-demands` para esta continuidade. Os ramos do aplicativo e os candidatos já testados continuam separados. A VM segue reservada ao Claude; não foi acessada. Publicação de versão, integração à main e decisão B3 não foram autorizadas por esta retomada.

## Ferramentas e proveniência

REA CLI 6.7.0 está instalado; o diagnóstico encontrou registro Codex alinhado e Ghidra 12.1.4/JDK21 disponíveis. Os tools MCP REA não estão expostos nesta sessão. A continuação nativa usa o backend direto Ghidra já empregado no projeto, com hash do alvo e projetos anteriores preservados. Esse resultado será identificado como backend direto, sem apresentá-lo como Evidence MCP do REA ou execução do Foxit.

Atualizar os marcos com horário real, resultados examinados, lacunas e próximos passos. Testes próprios, artefatos compilados e análise estática não comprovam paridade integral com o Foxit.


## Resultado da execução — 2026-10-23T21:10:52.788922-03:00

| Demanda | Resultado e o que falta |
|---|---|
|Viewer Windows|Corrigidos âncora/cache e fixture; validação nativa completa aprovada. Correção entregue ao ramo Windows8cc295f.|
|Quatro recursos: Flatpak e Windows|Mesmos808 IDs; Linux/fonte/payload/sandbox808 aprovados, Windows806 aprovados e dois pulos exclusivos Linux; instalador8/8. Recortes implementados; não compatibilidade universal.|
|Desktop Linux|Mesmo pacote final:9/9 controles em duas instalações independentes, incluindo atualização/reversão, associação e portal persistente. Desktop/equipamentos físicos permanecem separados.|
|TSA|Transporte opt-in implementado; TLS corrigido e validado no pacote com118 CAs×2. Endpoint externo permanece dependente da URL escolhida pelo usuário, sem chamada arbitrária.|
|Redação sem rasterizar|Form XObjects complexos removidos integralmente nas marcas, com testes; fontes/clipping/transparência desenhados diretamente fora do contrato continuam recusados.|
|S1|Avançaram auxiliares, filtro+0xc, caracteres e ramos locais de erro. Faltam byte+3, fórmula/unidade de proximidade, escapes/exceções completos até UI.|
|S3|Preferência de confiança ligada aos globais; construtor/ciclo de bits de formulário detalhados. Faltam consumidor+0x2bc, persistência e motores nativos de anotação/formulários/assinatura/OCG.|
|S4|Deltas e objeto de cache ligados, métricas e limitadores detalhados. Faltam mapas/unidades/limites, consumidores e falhas integrais.|
|Critérios amplos|Mantidos abertos; não escolher B3 nem alterar universo/pesos. VM, recursos físicos e decisões de integração/publicação mantêm dependências próprias.|

Estado estruturado e próximos passos: `progresso/execucao-codex-2026-10-23.json`. Relatórios completos preservados em `testes/resultados/continuidade-direta-2026-10-23/`. Este lote encerra as validações identificadas; o projeto integral permanece incompleto.
