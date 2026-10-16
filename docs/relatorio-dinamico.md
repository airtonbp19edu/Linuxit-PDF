# Observação dinâmica do original

Em 2026-10-16 foi validada uma contenção Bubblewrap mínima: mounts de sistema e
Wine somente para leitura, pasta Foxit somente para leitura, prefixo novo em
`/state`, ambiente limpo, sem credenciais, sem outros checkouts e sem rede.
A tela virtual dedicada usa Xorg sem TCP.

A tentativa de lançamento terminou com código 139, sem logs e sem confirmação
de carregamento do Foxit. Um controle com **somente `wine --version` na mesma
contenção também terminou com 139**; fora dela, Wine informa versão 10.0.
Isso caracteriza uma falha de infraestrutura ainda sem causa isolada. Não é
um resultado funcional nem uma falha demonstrada do Foxit.

O diretório `i386-windows` desse runtime não contém DLLs, portanto a capacidade
de executar o Foxit PE32 também não está estabelecida. Não se flexibilizou a
contenção para executar o binário original. O próximo passo é fornecer um
runtime Windows/x86 isolado funcional e executar os cenários da especificação.

O helper `scripts/observe_foxit_isolated.py` conserva os resultados localmente.
Nenhuma conta, autenticação, licença ou integração remota foi acionada.
Equivalência dinâmica verificada: nenhuma. O controle `wine --version` falhou
no ambiente isolado; não se afirma que o original tenha iniciado.

## Diagnóstico e continuação

O cadastro ausente de usuário foi isolado: um arquivo passwd/grupo sintético
foi montado na contenção, sem expor o cadastro real do host. O controle
`wine --version` passou com código 0. Na tentativa seguinte, o Wine informou
`could not exec wineserver`; o caminho explícito de seu servidor corrigiu esse
pré-requisito.

A terceira tentativa criou o prefixo, mas terminou com código 53 e
`C:\windows\syswow64\rundll32.exe: c0000135`. As DLLs x86 do Wine não estão
presentes; não se confirmou uma execução funcional do Foxit. Isso permanece
um bloqueio de runtime, sem contagens ou comportamento do original inventados.
As tentativas e os controles ficam no diretório local de evidências; somente
o resumo técnico é publicado.
