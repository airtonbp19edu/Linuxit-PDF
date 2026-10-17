# Tarefas atuais e ponto de retomada

Fonte/Flatpak **0.1.7/devel**: [criação de PDF de PNG/JPEG](../docs/CRIACAO-IMAGENS.md),
com ordem ajustável, DPI, orientação EXIF, transparência branca e destino novo.
**212/212** em cada suíte fonte/payload/sandbox, zero falhas/erros/skips;
17 métodos novos do backend e cinco GTK. Campanha preservada 17/17,
smoke 5/5 e launcher 3/3. Capturas e hashes examinados.

30 módulos/29 interfaces; 20 subconjuntos/cinco propostas em 25 famílias.
Catálogo **250** (152 REA + 98 diretas); duas entradas novas de reflow/111 instruções/
467bytes nesta rodada, com RTTI IPDFViewerLayout/CReflowViewerLayout.
[Análise](../docs/REA-REFLOW.md). Original não executado; sem paridade diferencial.

37 critérios done/21 abertos em 14 etapas; roteiro **43,33%**, paridade **0/25**.
Ainda há trabalho sem VM. Publicação/auditoria são registradas nas notas;
aprovação do pacote não encerra os demais contratos ou etapas.

| Frente | Próximo trabalho | Dependência |
|---|---|---|
|03/05/07/08/09/11|Helpers1f21a80/1f21ac0, slots de layout/renderer; tipos, ownership, campos da busca eIDs7911/7913|Estática sem VM; UI original não observada|
|12/15/16|Expandir operações e cinco propostas: assinaturas, segurança, acessibilidade, nuvem e integração de sistema|Parte própria sem VM; contas/equipamentos exigem ambiente externo|
|Criação/conversão|Formatos adicionais, OCR, exportação editável e demais operações PDF|Contrato próprio e implementação pendentes|
|Busca|Stemming/idiomas, formatos/recursão de anexos, demais requisitos de índice|Análise/contratos/implementação|
|Runtime|Desktop real, portais, AT-SPI, impressora física e Windows posterior|Ambientes/dispositivos, distinto da VM Foxit|
|10/18/19|ObservarD01–D20/UI01–UI10 e comparar corpus/protocolos preservados|VM/contenção offline pendente|
|01|Reconsultar regras remotas somente se acesso mudar;403 por plano preservado|Não alterar segurança/faturamento|
|21|Confirmar publicação/auditoria nas notas; manter21 critérios amplos abertos|Git/CI e demais obrigações|

50 planos completos continuam not_run;212 testes próprios não são comparações
Foxit. [Notas datadas](notas-continuidade.md) e [registro](pendencias-analises.json).
Preservar relatórios, fixtures e versões anteriores. Não reexecutar campanhas
estáveis sem mudanças ou preocupação concreta. Causa de tokens permanece null.
