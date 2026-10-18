# Tarefas atuais e ponto de retomada

Fonte e Flatpak **0.1.10/devel**, com [editor de cópia e histórico](../docs/EDICAO-COM-HISTORICO.md):
checkbox/radio/listas, mover/excluir marcadores, destaque/retângulo e exclusão
restrita de anotações. Desfazer/refazer atua no rascunho; cópias já salvas e
original preservados. Criação de PDF aceita PNG/JPEG/BMP/WebP/TIFF de um quadro.
OCR, multipágina/animações e famílias completas permanecem pendentes.

**333/333 testes próprios por ambiente**: fonte, payload e sandbox instalado,
sem falhas/erros/skips; 34 métodos portáveis e nove GTK novos. Integridade de
103 arquivos app e 11 relatórios CI conferida; smoke5/5 e launcher3/3.
Publicação confirmada no GitHub. Auditoria independente do mesmo bundle
aprovada: sete controles e cinco novos smoke checks, sem rebuild. Os testes
não são paridade Foxit; evidências e identidade nas notas mais recentes.

[Pastas sincronizadas locais](../docs/PASTAS-SINCRONIZADAS.md) preservadas; dois
controles fora HOME passaram novamente. Cliente real, portal/concessão persistente,
AT-SPI e impressão física continuam pendentes, sem depender da VM Foxit.

Arquitetura: 41 módulos/54 interfaces. Catálogo: 323 entradas (152 REA+171 diretas).
23 subconjuntos e duas propostas em 25 famílias. Roteiro: **43,93%**, 38 critérios
done/20 abertos; paridade: **0/25**. Original não executado. IA excluída e APIs
remotas de nuvem adiadas. Relatórios anteriores preservados.

Último log da VM examinado em 18/10: VirtualBox Windows 10 existe, com NEM/Snail
e Integridade da Memória ativa naquele registro; usuário está configurando.
Contenção offline ainda não validada; NAT ativo na configuração então lida.
Não executar original antes de preparar isolamento. Nenhuma proteção foi alterada
por esta rodada. Diagnóstico e limites nas notas datadas.

| Frente | Próximo trabalho | Dependência |
|---|---|---|
|Entrega 0.1.10|Publicação e auditoria independente confirmadas; preservar bundle e relatórios|Concluída neste marco, sem VM Foxit|
|Pastas sincronizadas|Portal real/concessão persistente e cliente externo, envio/conflitos/rede|Desktop Linux/cliente, sem VM Foxit|
|Operações locais|OCR/multipágina, demais formulários/anotações e plataforma|Implementação própria sem VM|
|Estática|Tamanhos/alocação e chamadores dos arrays; provedor ativo/offsets restantes da busca; contexto0x138 e serviços de imagem; comportamento7911/7913|REA/Ghidra sem executar original|
|10 e parte dinâmica da 11|Resolver lentidão da VM existente e validar contenção antes de D01–D20/UI01–UI10|VirtualBox Windows 10 criado; NEM/Integridade da Memória detectados; offline pendente|
|18/19|Comparar referência e validar divergências com original|VM offline para a referência; correções próprias podem avançar sem VM|
|Desktop/AT-SPI/impressão|Portais, leitor de tela, impressora e Windows posterior|Ambientes/equipamentos próprios|
|Nuvem direta|APIs/login/upload/colaboração remota adiados|Nova priorização do usuário|

50 planos completos `not_run`, 20 cenários dinâmicos e dez de UI sem observação integral.
Pesos intactos; causa de tokens não confirmada/null. Preservar relatórios/corpus.
