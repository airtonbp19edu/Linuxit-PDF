# Tarefas atuais e ponto de retomada

Fonte e Flatpak **0.1.13/devel**, com [anotações adicionais](../docs/ANOTACOES-AMPLIADAS.md):
sublinhado, tachado e ondulado por área, elipse e linha em qualquer direção.
Aparência vetorial própria vermelha. Edição de comentário/autor e exclusão
restritas a oito tipos simples desbloqueados, sem vínculos ou dependentes.
Rascunho com desfazer/refazer; original e cópias salvas preservados.

**400/400 testes próprios por ambiente**: fonte, payload e sandbox instalado,
sem falhas/erros/skips. Novos: 14 portáveis e seis GTK/Poppler; todos os 380 IDs
anteriores preservados. 106 arquivos app e 11 relatórios CI conferidos;
smoke 5/5 e launcher 3/3. Publicação e auditoria desta entrega nas notas mais recentes.
Os testes próprios não são paridade Foxit; pacotes/relatórios anteriores preservados.

[TIFF multipágina](../docs/TIFF-MULTIPAGINA.md), até 100 páginas na criação, e
[OCR local](../docs/OCR-LOCAL.md), até 20 páginas, preservados. Demais anotações,
formulários e famílias completas permanecem abertos. Pastas sincronizadas:
controles fora HOME negado/concedido passaram novamente; cliente real,
portal/concessão persistente, AT-SPI e impressão física ainda pendentes, sem VM Foxit.

Arquitetura: 44 módulos/58 interfaces; catálogo: 323 (152 REA + 171 diretas),
23 subconjuntos/duas propostas em 25 famílias. Roteiro **43,93%**, 38 done/20 abertos;
paridade **0/25**, cobertura global desconhecida. Original não executado.
APIs de nuvem adiadas/IA excluída. Não reiniciar análises preservadas.

VM: último diagnóstico histórico com NEM/Snail, Integridade da Memória ativa e
NAT então ativo; offline não validado. Usuário pediu continuar sem VM. Nenhuma
VM, rede ou proteção Windows alterada nesta rodada. Validar isolamento antes
de executar original; detalhes nas notas anteriores.

| Frente | Próximo trabalho | Dependência |
|---|---|---|
|Entrega 0.1.13|Fonte/payload/sandbox aprovados; confirmar publicação/auditoria|Sem VM Foxit|
|Pastas sincronizadas|Portal real/concessão persistente e cliente externo, envio/conflitos/rede|Desktop Linux/cliente, sem VM Foxit|
|Operações locais|Priorizar combos AcroForm editáveis (texto livre/aparência); demais formulários/anotações, OCR e plataforma|Implementação própria sem VM|
|Estática|Tamanhos/alocação e chamadores dos arrays; provedor ativo/offsets restantes da busca; contexto0x138 e serviços de imagem; comportamento7911/7913|REA/Ghidra sem executar original|
|10 e parte dinâmica da 11|Resolver lentidão da VM existente e validar contenção antes de D01–D20/UI01–UI10|VirtualBox Windows 10 criado; NEM/Integridade da Memória detectados; offline pendente|
|18/19|Comparar referência e validar divergências com original|VM offline para a referência; correções próprias podem avançar sem VM|
|Desktop/AT-SPI/impressão|Portais, leitor de tela, impressora e Windows posterior|Ambientes/equipamentos próprios|
|Nuvem direta|APIs/login/upload/colaboração remota adiados|Nova priorização do usuário|

50 planos completos `not_run`, 20 cenários dinâmicos e dez de UI sem observação integral.
Pesos intactos; causa de tokens não confirmada/null. Preservar relatórios/corpus.
