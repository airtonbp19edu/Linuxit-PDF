# P02 — coletor corrigido validado offline

Revisão em 2026-10-18T23:56:42-03:00, America/Sao_Paulo. Base local/remota `876f00dd99373b23a685983b957d31d443f83c87`, árvore inicialmente limpa.

**P02 concluída no escopo do ambiente e do observador.** P01 provisória preservada;
P03 pronta para uma rodada nova com preflight/controle visual antes do original.
Esta rodada não executou Foxit, nenhum teste do aplicativo ou build Flatpak.

O relógio avançou de 23:49:30 para 23:50:14 após espera externa explícita de dez
segundos; capturas VBox distintas. O Notepad abriu e o Gerenciador de Tarefas
respondeu. A ausência do Foxit foi examinada na faixa alfabética de Details e
confirmada no guest como zero processos antes da manutenção breve autorizada.

O script próprio corrigido foi transferido para `C:\Lab\guest_foxit_probe-2355.ps1`,
SHA-256 `b20ad4dca54ff33e7524df9d08702190539e0172ce3174dfe30b9118a277cac1`. A tarefa interativa limitada
`LinuxitProbe-vm-20261018-2355` iniciou com sessão1 e elevated=false. Cabo desligado
em finally antes dos testes; sem mudança de proteções, pause/resume ou reboot.

Recibos completos **startup ready, pf/col/end completed** recuperados pelo canal
offline. Preflight conferiu identidade do executável, dez Inputs iguais à campanha
preservada e escrita negada em Reference/Input/Protocol. Contenção host/guest:
nenhum adaptador conectado, share, USB capturado ou SMB; clipboard, drag-and-drop,
VRDE e áudio desativados. Notepad mostrou LINUXIT_RUNTIME_PROBE e respondeu ao
menu Editar sem editar o arquivo. Coleta encontrou somente os dois controles
Notepad, sem Foxit; parada normal do coletor confirmada em end.

[Comprovante sanitizado](../testes/resultados/p02-2026-10-18-2355.json) contém limites, hashes e identidades.
Telas/relatórios completos privados em `analysis-local/vm-20261018-2355/`; controle de
entrada em `analysis-local/vm-resume-20261018-2350/`. Computer Use @oai/sky,
VBoxManage, manutenção SSH breve e scripts próprios; sem REA nova nesta rodada.
O primeiro read de pf ainda não tinha recibo; foi aguardado sem repetir preflight
e depois recuperado completo. Não é falha Foxit. A causa das paradas anteriores
permanece desconhecida; não inferir estabilidade ou desempenho pelo relógio.

Este coletor foi encerrado: **não enviar novas solicitações ao RunId2355**.
Próximo passo: novo observador limitado/RunId, preflight offline e controle visual;
somente então destinos D07/D10, cancelamento ativo D12, saída D18 e variantes UI.
Continuar interrompendo entradas se segundos ou resposta pararem. Nenhum critério
amplo, peso, 45,13% do checklist, paridade0/25 ou percentual globalnull mudou.
App/fonte e Flatpak0.1.13/devel preservados; 403/403 e400/400 são históricos.
