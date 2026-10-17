# Tarefas atuais e ponto de retomada

Fonte **0.1.8 em desenvolvimento**; pacote publicado **0.1.7/devel**.
[Segurança, acessibilidade e edição local](../docs/SEGURANCA-ACESSIBILIDADE.md): senhas/permissões,
cópias AES-256 e owner autenticado, texto ATK/F6, CMS offline e edição de cópias.
Testes portáveis examinados; nova suíte Linux/GTK/Flatpak ainda pendente.
**Nuvem adiada pelo usuário**, sem remover a família nem alterar pesos.

35 módulos/40 interfaces; 23 subconjuntos e duas propostas em 25 famílias.
Catálogo **252** (152 REA + 100 diretas): dois helpers Win32 de sincronização
examinados, 70 bytes/32 instruções. [Evidência estática](../docs/REA-REFLOW-SINCRONIZACAO.md).
Roteiro **43,33%**, 37 critérios done/21 abertos, paridade **0/25**.
Há trabalho sem VM; desktop/equipamentos são dependências distintas da VM Foxit.

| Frente | Próximo trabalho | Dependência |
|---|---|---|
|Marco 0.1.8|Suíte completa Linux/GTK, pacote e auditoria instalada|CI Linux autorizado, sem VM Foxit|
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
