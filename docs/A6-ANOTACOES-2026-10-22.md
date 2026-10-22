# A6 — revisão limitada de anotações

**Atualização — 2026/10/22 às 20:37 (America/Sao_Paulo, UTC-03:00):** Passos4–6 executados: A4 registrada sem alterar critérios; candidato0.1.19/9fb4f3a validado744/744 em fonte/payload/Flatpak e aceitação81/81. Publicação retida; Windows e limites A6 no relatório. Passo7 aguarda instrução. Sem VM/B3; checklist45,13%, paridade0/25 e global indeterminado. [Evidência final do recorte](PASSOS-4-6-A456-2026-10-22.md). Os resultados locais abaixo são históricos.

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
