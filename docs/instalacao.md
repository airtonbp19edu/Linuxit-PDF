# Executar e construir o Linuxit PDF

## Flatpak para Linux x86_64

O bundle 0.1.1 usa o ID `io.github.airtonbp19edu.LinuxitPDF`, branch `devel` e
Freedesktop Platform 25.08. É um marco de desenvolvimento com funcionalidades
parciais; não é uma publicação no Flathub nem uma declaração de equivalência
integral ao Foxit. O bundle local não recebe assinatura digital; o manifesto
registra sua integridade e a origem do código.

Em um desktop Linux com Flatpak e Flathub configurados, após baixar o artefato:

```bash
flatpak install --user LinuxitPDF-0.1.1-x86_64.flatpak
flatpak run --user io.github.airtonbp19edu.LinuxitPDF
```

A instalação pode baixar o runtime e componentes relacionados. A versão usa
acesso à pasta pessoal, X11/Wayland, CUPS e rede para descoberta/impressão.
Abertura por portal, gravação em todos os ambientes e impressão física ainda
precisam de validação adicional. Testes com PDF sintético não cobrem todo PDF.

## Código-fonte

A instalação dos pacotes de desenvolvimento Debian/Ubuntu está no README.
O aplicativo usa GTK 3, Cairo, Poppler, Pillow, cryptography, clientes CUPS e
pypdf 6.20.1 incluído com licença. Execute `bash scripts/run.sh caminho.pdf`.
Os testes GTK precisam de uma sessão gráfica real ou uma tela virtual.

```bash
/usr/bin/python3 scripts/run_tests.py --output /tmp/linuxit-resultados-novos.json
```

O resultado registra sucessos, falhas, erros e testes ignorados separadamente.
No ambiente preparado, o overlay GI/Cairo é
`/workspace/.print-view-runtime/gi-cairo/usr/lib/python3/dist-packages`.

## Construção reproduzível no ambiente preparado

O builder atual exige host Debian 13 x86_64 com as dependências do leitor e
Flatpak instalado. Ele empacota o runtime Python/GTK/Poppler do host com
bibliotecas nativas e loader pareados, em diretório privado `runtime-lib`.
Isso evita misturar sua libc/readline com as do runtime Freedesktop.
O provedor OpenSSL é incluído e apontado explicitamente; algoritmos não são
desativados para contornar falhas de carregamento.

```bash
LD_LIBRARY_PATH=/workspace/release-tools/local/usr/lib/x86_64-linux-gnu \
FLATPAK_VALIDATE_ICON=/workspace/release-tools/local/usr/libexec/flatpak-validate-icon \
python3 scripts/build_flatpak.py \
  --flatpak /workspace/release-tools/local/usr/bin/flatpak \
  --stage /workspace/linuxit-release/novo-stage \
  --repo /workspace/linuxit-release/novo-repo \
  --extra-runtime /workspace/.print-view-runtime
```

Use um stage novo. A saída é `dist/LinuxitPDF-0.1.1-x86_64.flatpak`.
O builder inclui avisos/licenças, versões dos pacotes e módulos OpenSSL.
Reproduzir o mesmo conteúdo exige a mesma revisão da fonte e os pacotes
registrados no manifesto; não se afirma build idêntico bit a bit em outro host.
O empacotamento não inclui Foxit, REA, Ghidra ou seus resultados privados.

## Validação no sandbox

O harness `scripts/smoke_linuxit.py` cria um PDF sem dados pessoais, abre a
janela, renderiza, pesquisa marcador/comentário e gera um livreto verificável.
Para testá-lo no aplicativo instalado, conceda apenas leitura do script:

```bash
flatpak run --user --filesystem="$PWD/scripts:ro" \
  --env=PRINT_VIEW_TEST_APP=/app/share/linuxit-pdf \
  --command=linuxit-python io.github.airtonbp19edu.LinuxitPDF//devel \
  "$PWD/scripts/smoke_linuxit.py"
```

Esse acesso adicional é do harness, não uma permissão padrão do aplicativo.
Na imagem de nuvem, a ausência de barramento D-Bus de sistema foi resolvida
com um barramento privado de testes; nenhuma política de desktop existente
foi modificada. O perfil de instalação fica sob `/workspace/linuxit-release`.
Os serviços temporários devem ser iniciados novamente numa sessão nova.

## Investigação Windows x86 por emulação

O ambiente preserva Wine 10/i386 e QEMU 10.0.13 fora do aplicativo. O kernel
recusa execução ELF x86 nativa; use os adaptadores de emulação já preparados.
`python3 scripts/check_foxit_emulation.py` confere 40 arquivos de pacotes e
quatro arquivos-chave de runtime/adaptação contra os hashes registrados.
As dependências foram baixadas por APT com índices assinados; não foram
instaladas globalmente e não entram no Flatpak.

Com Xorg dedicado já verificado e sem outra aplicação naquela tela:

```bash
python3 scripts/observe_foxit_isolated.py \
  --reference '/workspace/pdf-reference-analysis/foxit/Foxit PDF Reader' \
  --output /workspace/foxit-rea-analysis/dynamic/novo-controle \
  --timeout 90 --probe-cmd x86 --prefill-wine32 \
  --zlib-root /workspace/foxit-rea-analysis/zlib-extracted \
  --qemu-root /workspace/foxit-rea-analysis/qemu-tools \
  --wine32-root /workspace/foxit-rea-analysis/wine32-runtime
```

Esse comando verifica `cmd.exe`; não comprova funcionamento do Foxit. A execução
do original remove `--probe-cmd x86` e exige outro diretório de saída. As duas
tentativas atuais terminaram antes de uma interface utilizável, com exceção
MFC. O diagnóstico e os limites estão em `REA-BUSCA-IMPRESSAO.md`. Não altere
o executável nem reutilize um perfil real para contornar essa falha.

Os pacotes extraídos e os adaptadores estão preservados no workspace; não são
processos ativos. Uma nova sessão precisa iniciar novamente a tela e o D-Bus
privados para os testes que os utilizam.
