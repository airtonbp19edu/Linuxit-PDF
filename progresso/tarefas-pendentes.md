# Tarefas atuais e ponto de retomada

Fonte **0.1.9 em desenvolvimento**, após pacote0.1.8: [pastas sincronizadas locais](../docs/PASTAS-SINCRONIZADAS.md).
15 controles portáveis novos e53 regressões passaram;8 GTK novos ainda sem execução.
37 módulos/49 interfaces. Próximo: suíte completa290 no Linux e Flatpak, incluindo
concessão específica fora de HOME. Portais reais/cliente de sincronização: desktop,
sem VM Foxit. APIs remotas de nuvem continuam adiadas. Registros abaixo históricos.


Fonte/Flatpak **0.1.8/devel**, marco de desenvolvimento validado.
[Segurança, acessibilidade e edição local](../docs/SEGURANCA-ACESSIBILIDADE.md): senhas/permissões,
cópias AES-256 e owner autenticado, texto ATK/F6, CMS offline e edição de cópias.
**267/267** em cada suíte fonte/payload/sandbox, sem falhas/erros/skips;
39 métodos portáveis e16 GTK novos. Publicação confirmada; auditoria independente do mesmo bundle aprovada (7+5 controles).
**Nuvem adiada pelo usuário**, sem remover a família nem alterar pesos.

35 módulos/40 interfaces; 23 subconjuntos e duas propostas em 25 famílias.
Catálogo **259** (152 REA + 107 diretas). Após quatro acessores,
três métodos de limites/predicado foram examinados:1.348 bytes/412 instruções. [Evidência estática](../docs/REA-REFLOW-GEOMETRIA.md).
Roteiro **43,33%**, 37 critérios done/21 abertos, paridade **0/25**.
Há trabalho sem VM; desktop/equipamentos são dependências distintas da VM Foxit.

| Frente | Próximo trabalho | Dependência |
|---|---|---|
|Marco 0.1.8|Publicado e auditado; fonte/payload/sandbox267/267 e auditoria7+5 aprovados|Concluído como marco parcial, projeto em andamento|
|Estática|Slots layout/renderer; busca campos3/5/6/7/12/16/20; tipos/ownership e IDs7911/7913|Sem VM; original não observado|
|Operações locais|Demais formulários, undo/anotações, formatos/OCR e contratos incompletos|Implementação própria e testes|
|Acessibilidade|Orca/AT-SPI, ordem semântica, voz e desktop real|Ambiente de desktop, distinto da VM Foxit|
|Assinaturas|Cadeia/tempo/revogação e formatos adicionais|Contrato e material de confiança de laboratório|
|Nuvem|Adiada explicitamente pelo usuário|Retomar somente em nova priorização|
|Sistema|Portais/desktop, impressora física e Windows posterior|Ambientes/dispositivos externos|
|10/18/19|D01–D20 e UI01–UI10, comparar corpus preservado|VM/contenção offline pendente|
|01|Reconsultar regras GitHub se acesso mudar;403 por plano preservado|Sem alterar segurança/faturamento|

50 planos completos continuam not_run. Testes próprios não são observações Foxit.
Preservar corpus/relatórios/pacotes e [notas datadas](notas-continuidade.md).
Timeout não comprova esgotamento de tokens; causa não confirmada fica null.
