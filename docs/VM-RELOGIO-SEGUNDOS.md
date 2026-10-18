# Relógio com segundos no Windows 10 da VM

Em 18/10/2026, a pedido do usuário, os segundos foram habilitados na barra de
tarefas do Windows 10 convidado. O relógio do hospedeiro não foi alterado.

No perfil sintético da sessão interativa foi criado o valor DWORD
`ShowSecondsInSystemClock=1` em
`HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced`.
O valor anterior não existia; esse estado foi registrado. O Explorer do guest
foi reiniciado pelo Gerenciador de Tarefas e a exibição foi examinada:
`19:46:26`, depois `19:46:42`, na própria barra, com a data abaixo.

O relógio avançando mostra que a interface do sistema continua se atualizando;
não comprova que o Foxit, individualmente, está respondendo. O atraso do relógio
do guest ainda impede usar essas capturas como benchmark de desempenho.

## Contenção e retomada dos testes

O Foxit residual foi encerrado pelo Gerenciador de Tarefas antes da manutenção.
Isso foi encerramento forçado para preparar o ambiente, não uma aprovação do
encerramento normal de D20. A espera anteriormente registrada em `splwow64.exe`
continua sem causa definitiva.

A manutenção breve por SSH usou o acesso previamente autorizado, sem abrir o
original. A primeira tentativa excedeu o limite da linha de comando do Windows;
o bloco de desconexão foi executado. A segunda usou comandos menores, verificou
ausência de Foxit e aplicou o ajuste. Depois, o cabo foi desligado novamente.
Não foram alteradas proteções do Windows nem instalados programas.

Novo coletor `vm-20261018-1940`, tarefa interativa limitada, com o mesmo script
próprio de hash `8a8b4ae003c1ff6c8cbaa6fc7139e7497e6dd14ec1fe18e69f86a849fa053e13`.
O preflight offline confirmou token não elevado, Ethernet desconectada,
nenhum share/USB capturado/SMB, clipboard/drag-and-drop/VRDE/áudio desligados,
negação de escrita em Reference/Input/Protocol e hashes dos dez arquivos
de Input iguais à campanha anterior. O controle Notepad respondeu visualmente
antes do novo lançamento do original, PID 5280. Existir PID não aprova cenário.

Comprovante sanitizado:
[clock.json](../testes/resultados/vm-2026-10-18-segundos/clock.json).
Capturas e relatórios completos permanecem privados em
`analysis-local/vm-20261018-1940/`. Fonte e Flatpak não mudaram neste ajuste;
o roteiro, as pendências amplas e a paridade integral permanecem preservados.

Próximo lote: destinos de D07/D10, consulta exata D11, cancelamento ativo D12,
senha em abertura independente D15, saída de imposição D18 e UI01–UI10.
