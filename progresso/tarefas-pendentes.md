# Tarefas atuais e ponto de retomada

Fonte e Flatpak **0.1.9/devel**, com [pastas sincronizadas locais](../docs/PASTAS-SINCRONIZADAS.md).
Pasta preferida, últimas pastas, atalhos para abrir/salvar e cópias novas completas,
sem sobrescrita. Alterações externas exigem reabrir; o envio cabe ao cliente externo.
**290/290 testes próprios** por ambiente: fonte, payload e sandbox instalado,
sem falhas, erros ou skips; 15 métodos portáveis e oito GTK novos.
Dois controles fora de HOME passaram: acesso negado sem concessão e permitido
com concessão específica. Cliente real, portal e persistência da concessão em
um desktop permanecem pendentes; esses testes não precisam da VM Foxit.

[Continuação estática de 18/10/2026](../docs/REA-ESTATICA-CONTINUACAO-2026-10-18.md): 48 entradas novas,
6.830 instruções/25.919 bytes conferidos em oito lotes; tipos, estados, stemming e arrays refinados.
Fonte/pacote preservados; as suítes completas não foram repetidas nesta rodada.

Arquitetura: 37 módulos/49 interfaces. Catálogo: 323 entradas (152 REA + 171 diretas).
São 23 subconjuntos e duas propostas em 25 famílias. Roteiro: **43,33%**,
37 critérios `done` e 21 abertos; paridade: **0/25**. Original não executado.
APIs remotas de nuvem continuam adiadas. Publicação confirmada no GitHub;
auditoria independente do mesmo pacote aprovada (sete controles + cinco smoke).
Evidências nas notas datadas; o restante do projeto continua parcial.

| Frente | Próximo trabalho | Dependência |
|---|---|---|
|Entrega 0.1.9|Publicada e auditada; conferir evidências antes de uma nova alteração|Concluída neste marco; sem VM Foxit|
|Pastas sincronizadas|Portal real/concessão persistente e cliente externo, envio/conflitos/rede|Desktop Linux/cliente, sem VM Foxit|
|Operações locais|Demais formulários/undo/anotações/formatos/OCR/plataforma|Implementação própria sem VM|
|Estática|Tamanhos/alocação e chamadores dos arrays; provedor ativo/offsets restantes da busca; contexto0x138 e serviços de imagem; comportamento7911/7913|REA/Ghidra sem executar original|
|10 e parte dinâmica da 11|Observar D01–D20/UI01–UI10 no original|VM offline|
|18/19|Comparar referência e validar divergências com original|VM offline para a referência; correções próprias podem avançar sem VM|
|Desktop/AT-SPI/impressão|Portais, leitor de tela, impressora e Windows posterior|Ambientes/equipamentos próprios|
|Nuvem direta|APIs/login/upload/colaboração remota adiados|Nova priorização do usuário|

50 planos completos `not_run`, 20 cenários dinâmicos e dez de UI sem observação integral.
Pesos intactos; causa de tokens não confirmada/null. Preservar relatórios/corpus.
