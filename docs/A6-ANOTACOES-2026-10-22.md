# A6 — revisão limitada de anotações

O rascunho `annotation_editing.py` foi preservado no backup e agora recebeu testes
de topologia recíproca, referências entre páginas, bloqueios, ciclos, exclusão de
folha/popup e movimento atômico. `annotation_geometry.conversation_members` usa
essa validação para a exclusão de conversa já exposta pelo aplicativo.

`pdf_changes.update-comment` agora mantém a aparência gráfica de carimbos externos
ao editar seus metadados. Antes ela era substituída por um carimbo textual próprio.
O conteúdo rico `/RC` contraditório é removido após a alteração explícita de texto.
Campos bloqueados e relações malformadas são recusados antes da alteração.

Os helpers de movimentação e exclusão de folha com popup são testados diretamente,
mas ainda não substituem todos os controles conservadores da interface. Widgets,
mídia, grupos `/RT Group`, tipos desconhecidos e exclusão ligada a StructParent
permanecem fora desse fluxo. Excluir comentário de anexo não promete apagar o
payload. Isto não é edição universal, nem paridade Foxit.
