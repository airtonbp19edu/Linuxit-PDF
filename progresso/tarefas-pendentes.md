# Tarefas atuais e ponto de retomada

Fonte e Flatpak **0.1.12/devel**, com [TIFF multipágina](../docs/TIFF-MULTIPAGINA.md):
ordem por blocos de arquivo e páginas internas, orientação por página, RGB8 e
até 100 páginas totais. Encadeamento IFD limitado; sem SubIFDs recursivos ou
seleção individual de páginas TIFF. [OCR local](../docs/OCR-LOCAL.md) anterior
preservado, com limite próprio de 20 páginas, português/inglês e cópia rasterizada.

**380/380 testes próprios por ambiente**: fonte, payload e sandbox instalado,
sem falhas/erros/skips. Novos: 14 portáveis, dois GTK e uma integração Linux
TIFF→PDF→OCR. Um teste de recusa de TIFF foi adaptado/renomeado à nova regra;
362 IDs anteriores preservados e 18 novos IDs incluem essa substituição.
105 arquivos app e 11 relatórios CI conferidos; smoke 5/5 e launcher 3/3.
Publicação confirmada; auditoria independente do mesmo bundle aprovada com
sete controles e cinco novos smoke checks, sem rebuild. Testes próprios
não são paridade Foxit; relatórios e pacotes anteriores preservados.

Pastas sincronizadas: controles fora HOME negado/concedido passaram novamente.
Cliente real, portal/concessão persistente, AT-SPI e impressão física pendentes,
sem depender da VM Foxit. Demais formulários/anotações e famílias completas
continuam abertos. Editor de cópia/histórico e formatos anteriores preservados.

Arquitetura: 43 módulos/57 interfaces; catálogo: 323 (152 REA + 171 diretas), 23
subconjuntos/duas propostas em 25 famílias. Roteiro **43,93%**, 38 done/20 abertos;
paridade **0/25**, cobertura global desconhecida. Original não executado.
APIs de nuvem adiadas/IA excluída; não reiniciar análises preservadas.

VM: último diagnóstico histórico com NEM/Snail, Integridade da Memória ativa e
NAT então ativo; offline não validado. Usuário pediu continuar sem VM. Nenhuma
VM, rede ou proteção Windows alterada nesta rodada. Validar isolamento antes
de executar original; detalhes nas notas datadas anteriores.

| Frente | Próximo trabalho | Dependência |
|---|---|---|
|Entrega 0.1.12|Publicação e auditoria independente confirmadas; preservar evidências|Concluída neste marco, sem VM Foxit|
|Pastas sincronizadas|Portal real/concessão persistente e cliente externo, envio/conflitos/rede|Desktop Linux/cliente, sem VM Foxit|
|Operações locais|Demais formulários/anotações, OCR ampliado e plataforma|Implementação própria sem VM|
|Estática|Tamanhos/alocação e chamadores dos arrays; provedor ativo/offsets restantes da busca; contexto0x138 e serviços de imagem; comportamento7911/7913|REA/Ghidra sem executar original|
|10 e parte dinâmica da 11|Resolver lentidão da VM existente e validar contenção antes de D01–D20/UI01–UI10|VirtualBox Windows 10 criado; NEM/Integridade da Memória detectados; offline pendente|
|18/19|Comparar referência e validar divergências com original|VM offline para a referência; correções próprias podem avançar sem VM|
|Desktop/AT-SPI/impressão|Portais, leitor de tela, impressora e Windows posterior|Ambientes/equipamentos próprios|
|Nuvem direta|APIs/login/upload/colaboração remota adiados|Nova priorização do usuário|

50 planos completos `not_run`, 20 cenários dinâmicos e dez de UI sem observação integral.
Pesos intactos; causa de tokens não confirmada/null. Preservar relatórios/corpus.
