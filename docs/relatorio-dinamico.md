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

## Dependências x86 e zlib verificadas

O pacote Debian `libwine:i386=10.0~repack-6` foi obtido por índice APT assinado;
seu SHA-256 `fef4802a6553a17eaa40003333a86fc697440d1d21c5824f2dbd1c444f01527b`
foi conferido antes de extrair 809 DLLs Windows x86 para o runtime local. Não
foram instaladas bibliotecas i386 no sistema. O runtime x64 já contém WOW64.

O pacote `libz-mingw-w64=1.3.1+dfsg-2`, SHA-256
`c4e6d6bfabe8b6d12c797736a3d762d83513b49f488d1aaf61d4526387a2dd3e`,
forneceu a zlib para cada arquitetura no prefixo sintético. As importações
anteriores indicavam conflito x86/x64 dessa dependência. Com as dependências,
o log passou a mostrar o mapeamento das seções PE do executável Foxit, mas o
lançamento ainda retornou `ShellExecuteEx failed` e código 1. Caminho Windows
explícito e loader local não resolveram a inicialização.

Mapear as seções do arquivo não comprova entrada no fluxo funcional ou uma
janela utilizável. Nenhuma contagem de busca, fluxo de impressão ou equivalência
do original foi observada. O bloqueio atual é a inicialização Windows/x86
nessa contenção, não uma permissão de rede ou um mecanismo de licença a contornar.
