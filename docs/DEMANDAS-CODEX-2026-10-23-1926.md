# Demandas recebidas do Claude em 23/10/2026 às 19:26

**Ordem humana posterior nesta conversa:** “não é mais pra acompanhar; você vai assumir a dianteira agora e fazer tudo que está pendente dos meus pedidos ao Claude”. Codex assumiu a execução, revisão dos resultados e correções; a automação de acompanhamento foi excluída. Não se trata mais de aguardar atividade/inatividade do Claude. As entregas e decisões específicas abaixo continuam preservadas.

O usuário pediu nesta conversa que o Codex se atualizasse e iniciasse as demandas. A lista foi conferida no `CHAT-CLAUDE.txt` e no commit remoto `b82d106`. Os quatro recortes anteriores já estão implementados no ramo `codex/authorized-pdf-features`, entrega `e1ad5d1`, fonte `f34bddd`: 779/779 testes Linux e 81/81 aceitações próprias. Não repetir essa validação de fonte como se estivesse pendente.

## Ordem e limites

| Frente | Trabalho a executar | Estado nesta retomada |
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
