# Tarefas atuais e ponto de retomada

Fonte/Flatpak **0.1.8/devel**, marco de desenvolvimento validado.
[Segurança, acessibilidade e edição local](../docs/SEGURANCA-ACESSIBILIDADE.md): senhas/permissões,
cópias AES-256 e owner autenticado, texto ATK/F6, CMS offline e edição de cópias.
**267/267** em cada suíte fonte/payload/sandbox, sem falhas/erros/skips;
39 métodos portáveis e16 GTK novos. Publicação e auditoria independente: consultar o último registro nas notas.
**Nuvem adiada pelo usuário**, sem remover a família nem alterar pesos.

35 módulos/40 interfaces; 23 subconjuntos e duas propostas em 25 famílias.
Catálogo **256** (152 REA + 104 diretas). Após os dois helpers Win32 de
sincronização, quatro acessores de layout foram examinados:20 bytes/dez instruções. [Evidência estática](../docs/REA-REFLOW-LAYOUT.md).
Roteiro **43,33%**, 37 critérios done/21 abertos, paridade **0/25**.
Há trabalho sem VM; desktop/equipamentos são dependências distintas da VM Foxit.

| Frente | Próximo trabalho | Dependência |
|---|---|---|
|Marco 0.1.8|Publicação e auditoria do mesmo pacote; verificar último registro nas notas|CI Linux autorizado, sem VM Foxit|
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
