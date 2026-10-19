# Tarefas atuais e ponto de retomada

Estado de execução: [P01–P03](../docs/EXECUCAO-P01-P03-2026-10-18.md),
[catálogo111](inventario-operacoes-v1.json) e [estado por etapa](execucao-plano.json).
P01 concluída para inventário provisório; P02 bloqueada pelo relógio21:49:22,
P03 não iniciada. Restaurar resposta antes de deploy do coletor; manter regra
de não reiniciar/pausar automaticamente. Os19 critérios amplos continuam abertos.

Fila organizada: [plano P01–P10](../docs/PLANO-DE-CONTINUIDADE.md) e
[fonte estruturada](plano-continuidade.json). Toda pendência conhecida das 25
famílias e dos 19 critérios tem etapa, dependência, entrega e condição de conclusão.
Começar P01; sem VM, priorizar P06/B01 (combo editável) e P04 (estática dirigida).
Preparar contratos em P05 e validar recursos Linux disponíveis em P07/P09.
P02 antecede novas observações do original; manter a interrupção registrada.

Último checkpoint: [senha e parada da VM](../docs/VM-SENHA-E-PARADA-2026-10-18.md).
Relógio21:24:14 não avançou na confirmação após10 segundos; testes suspensos,
Foxit fechado/cabooff, sem reboot automático. Primeiro restaurar resposta e
validar coletor corrigido em RunId novo, com recibos curtos e contenção limitada.
D15 senha correta em abertura nova observado; não repetir como pendência.
UI05 duas abas com PDF protegido é variante extra; par planejado ainda aberto.
D20 fechou normalmente neste contexto, sem resolver a espera anterior de impressão.

Nova rodada offline2020: consulta exata D11 retornou zero e passou na comparação.
Consolidado12/12 medições iguais, cinco inconclusivas; onze preservadas/uma nova.
UI01 com documento/cancelar observado; destinos D07 ainda abertos. Ver
[relatório atual](../docs/VM-BUSCA-2026-10-18-2020.md). App/Flatpak intactos; não são famílias completas.

VM: [segundos habilitados e rodada posterior](../docs/VM-RELOGIO-SEGUNDOS.md).
UI01 sem documento/cancelar e D07 com dois marcadores observados; destinos
inconclusivos por resposta intermitente. `probe-stop:stop` da rodada vm-20261018-1940
confirmado completed em `followup.json`; coletor encerrado. Última coleta tinha
Foxit5280 com janela; manter offline e revalidar resposta visual antes de retomar.

Atualização posterior ao pacote: [busca por autor corrigida](../docs/BUSCA-AUTOR-COMENTARIOS.md) na fonte,
**403/403 testes Linux** e 11/11 medições iguais na comparação anterior.
Naquele marco havia cinco inconclusivos e um pendente; o consolidado atual está acima. O Flatpak 0.1.13 continua
anterior à correção, com 400/400 por ambiente no marco de entrega. Nenhum novo
pacote nesta rodada. D20: espera observada em splwow64.exe; causa aberta.

Fonte e Flatpak **0.1.13/devel**, com [anotações adicionais](../docs/ANOTACOES-AMPLIADAS.md):
sublinhado, tachado e ondulado por área, elipse e linha em qualquer direção.
Aparência vetorial própria vermelha. Edição de comentário/autor e exclusão
restritas a oito tipos simples desbloqueados, sem vínculos ou dependentes.
Rascunho com desfazer/refazer; original e cópias salvas preservados.

**Na entrega 0.1.13, 400/400 testes próprios por ambiente**: fonte, payload e sandbox instalado,
sem falhas/erros/skips. Novos: 14 portáveis e seis GTK/Poppler; todos os 380 IDs
anteriores preservados. 106 arquivos app e 11 relatórios CI conferidos;
smoke 5/5 e launcher 3/3. Publicação confirmada; auditoria independente do mesmo bundle aprovada com
sete controles e cinco novos smoke checks, sem rebuild.
Os testes próprios não são paridade Foxit; pacotes/relatórios anteriores preservados.

[TIFF multipágina](../docs/TIFF-MULTIPAGINA.md), até 100 páginas na criação, e
[OCR local](../docs/OCR-LOCAL.md), até 20 páginas, preservados. Demais anotações,
formulários e famílias completas permanecem abertos. Pastas sincronizadas:
controles fora HOME negado/concedido passaram novamente; cliente real,
portal/concessão persistente, AT-SPI e impressão física ainda pendentes, sem VM Foxit.

Arquitetura: 44 módulos/58 interfaces; catálogo: 323 (152 REA + 171 diretas),
23 subconjuntos/duas propostas em 25 famílias. Índice histórico do checklist:
**45,13%**, 39 done/19 abertos. Conclusão global da recodificação indeterminada;
paridade **0/25**, cobertura global desconhecida. Original observado parcialmente na VM offline.
APIs de nuvem adiadas/IA excluída. Não reiniciar análises preservadas.

[Medição revisada](../docs/MEDICAO-PROGRESSO.md): os índices do checklist não quantificam as
funcionalidades implementadas. O índice só sobe ao fechar critérios por inteiro;
entregas parciais devem ser acompanhadas pelos recursos e evidências de cada versão.

VM: [primeira campanha offline de 18/10](../docs/VM-FOXIT-2026-10-18.md) observou o original com
perfil limitado, RX exercitado e hashes preservados. Dos17 recortes C18:
Na campanha inicial:11 comparados,10 iguais/1 divergente (autor). Na fonte
corrigida:11/11 métricas iguais;5 inconclusivos/1pendente preservados.
D01–D20:14 observados no recorte,5 parciais,1 inconclusivo; cancelamento, destinos
dos hits e saída de imposição abertos. D20 deixou processo sem janela; manter
rede desligada e investigar. Nenhuma proteção do host foi alterada.

| Frente | Próximo trabalho | Dependência |
|---|---|---|
|Entrega 0.1.13|Publicação e auditoria independente confirmadas; preservar evidências|Concluída neste marco, sem VM Foxit|
|Pastas sincronizadas|Portal real/concessão persistente e cliente externo, envio/conflitos/rede|Desktop Linux/cliente, sem VM Foxit|
|Operações locais|Priorizar combos AcroForm editáveis (texto livre/aparência); demais formulários/anotações, OCR e plataforma|Implementação própria sem VM|
|Estática|Tamanhos/alocação e chamadores dos arrays; provedor ativo/offsets restantes da busca; contexto0x138 e serviços de imagem; comportamento7911/7913|REA/Ghidra sem executar original|
|10 e parte dinâmica da 11|Completar variantes pendentes e UI01–UI10; investigar D20|VM offline operacional; campanha inicial preservada|
|18/19|Busca por autor corrigida na fonte posterior ao pacote0.1.13; validar e ampliar comparações; ver docs/BUSCA-AUTOR-COMENTARIOS.md|VM para novas observações; implementação/testes próprios no Linux|
|Desktop/AT-SPI/impressão|Portais, leitor de tela, impressora e Windows posterior|Ambientes/equipamentos próprios|
|Nuvem direta|APIs/login/upload/colaboração remota adiados|Nova priorização do usuário|

50 planos de aceitação completos `not_run`; D01–D20 com14 observados/5parciais/1inconclusivo. Dez de UI sem execução integral.
Pesos intactos; causa de tokens não confirmada/null. Preservar relatórios/corpus.
