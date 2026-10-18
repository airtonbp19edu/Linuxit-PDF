# Executar e construir o Linuxit PDF

## Flatpak para Linux x86_64

O bundle 0.1.11 usa o ID `io.github.airtonbp19edu.LinuxitPDF`, branch `devel` e
Freedesktop Platform 25.08. É um marco de desenvolvimento com funcionalidades
parciais; não é uma publicação no Flathub nem uma declaração de equivalência
integral ao Foxit. O bundle local não recebe assinatura digital; o manifesto
registra sua integridade e a origem do código.

Para baixar, abra a
[página do Flatpak no GitHub](https://github.com/airtonbp19edu/Linuxit-PDF/blob/main/releases/LinuxitPDF-0.1.11-x86_64.flatpak)
e clique em **Download raw** (ícone de download). Se o repositório estiver
privado, use um navegador conectado a uma conta com acesso ao projeto;
o link raw sem autenticação retorna 404 nesse caso. Com o repositório público,
o download não exige login. A visibilidade é administrada pelo proprietário.
Uma página em branco no navegador interno não indica que o pacote esteja vazio.
Se necessário, abra essa página no navegador habitual.

O arquivo 0.1.11 tem **44.671.928 bytes** (aproximadamente 42,6 MiB).
É um instalador binário Flatpak, sem prévia de conteúdo em uma página web.

Em um desktop Linux com Flatpak e Flathub configurados, abra o terminal na
pasta em que o arquivo foi baixado e execute:

```bash
flatpak install --user ./LinuxitPDF-0.1.11-x86_64.flatpak
flatpak run --user io.github.airtonbp19edu.LinuxitPDF
```

A instalação pode baixar o runtime e componentes relacionados. A versão usa
acesso à pasta pessoal, X11/Wayland, CUPS e rede para descoberta/impressão.
Abertura por portal, gravação em todos os ambientes e impressão física ainda
precisam de validação adicional. Testes com PDF sintético não cobrem todo PDF.

## Se aparecer “corrompido ou faltando permissões”

Essa mensagem genérica não confirma corrupção nem identifica uma permissão
específica. Primeiro confira a cópia baixada e obtenha a mensagem do instalador.
Abra o terminal na pasta do arquivo e execute:

```bash
flatpak --version
sha256sum LinuxitPDF-0.1.11-x86_64.flatpak
flatpak install --user ./LinuxitPDF-0.1.11-x86_64.flatpak
```

O SHA-256 esperado para a 0.1.11 é:

```text
30a1e9ab078194df85c0bdf841316958450b916b1f87f3312eaccd491c240c02
```

- Se o hash diferir, o arquivo baixado não é idêntico ao pacote publicado;
  baixe outra cópia pelo link do projeto e confira novamente.
- Se o hash coincidir e a instalação falhar, envie a saída completa do terminal,
  a distribuição Linux e a arquitetura (`uname -m`). Isso permite investigar
  o instalador, o runtime ou uma permissão específica sem presumir a causa.
- Se `flatpak` não for encontrado, instale o suporte Flatpak conforme as
  instruções da sua distribuição antes de instalar o aplicativo.

O `.flatpak` é um pacote de instalação; não precisa de permissão de execução.
O comando `--user` seleciona a instalação para seu usuário.
O procedimento de instalar um arquivo `.flatpak` está na
[documentação oficial](https://docs.flatpak.org/en/latest/single-file-bundles.html).


Histórico da versão0.1.9: Em 18/10/2026, um novo download HTTP público completo teve os mesmos
35.983.584 bytes e SHA-256 do pacote local/publicado. A
[conferência de integridade](../testes/resultados/0.1.9/download-integrity-2026-10-18.json)
não verifica a cópia do usuário nem diagnostica seu ambiente Linux. A instalação
e os testes do CI são evidência anterior; não foram repetidos nesta conferência.



Histórico da 0.1.10: O [download público da 0.1.10](../testes/resultados/0.1.10/download-integrity-2026-10-18.json)
foi conferido sem autenticação: HTTP 200, tamanho completo e SHA-256 esperado.
A [auditoria independente](../testes/resultados/0.1.10/audit/review.json) também
instalou esse mesmo bundle e aprovou cinco novos smoke checks.


## Marco 0.1.9: pastas sincronizadas locais

[Uso e limites](PASTAS-SINCRONIZADAS.md). Configure o cliente externo, selecione
a pasta local em Arquivo → Escolher pasta sincronizada e salve com nome novo.
O Linuxit confirma gravação local; upload e conflitos são do sincronizador.
290/290 por ambiente e dois controles de pasta fora HOME passaram no CI.
Uma pasta fora HOME pode exigir concessão pelo desktop ou permissão explícita
para aquela pasta; nenhuma permissão global extra foi incluída no pacote.
Portal real/persistência e cliente real ainda não testados em desktop.

## Marco 0.1.8: segurança, acessibilidade e operações locais

[Contrato e limites](SEGURANCA-ACESSIBILIDADE.md): inspeção de senha/permissões,
cópias AES-256 e cópias sem senha com autenticação owner, texto ATK e foco F6,
integridade CMS offline e renomear marcador/atualizar nota/girar em cópia.
Não aprova confiança de certificado nem conformidade de acessibilidade integral.
267/267 testes próprios por ambiente fonte/payload/sandbox, zero skips;
39 métodos portáveis e16 GTK novos,97 arquivos app conferidos.
Runtime:2.804 arquivos,215ELF e150 pacotes com avisos/proveniência preservados.
Smoke5/5 e launcher3/3. [Revisão](../testes/resultados/0.1.8/validation-review.json).
Publicação e auditoria independente do mesmo bundle: consultar notas atuais.
Nuvem adiada pelo usuário; desktop real, portais e impressora física pendentes.

## Marco 0.1.7: criação a partir de imagens

[Contrato](CRIACAO-IMAGENS.md): PNG/JPEG em ordem ajustável,72–600DPI,
orientação EXIF e transparência branca.17 métodos backend e cinco GTK novos,
212/212 por ambiente,92 arquivos app; demais formatos/OCR continuam pendentes.
[Revisão histórica](../testes/resultados/0.1.7/validation-review.json).

## Marco 0.1.6: buscas e coleção

[Contrato](BUSCA-COLECOES.md):190/190 por ambiente fonte/payload/sandbox,
zero skips, seis métodos GTK novos, smoke 5/5 e launcher 3/3. Busca em anexos
UTF-8/PDF com omissões explícitas, coringas/proximidade e índice local de PDFs
escolhidos. Sem stemming/OCR, recursão de anexos ou pesquisa implícita de pastas.
O índice contém texto/caminhos locais; os limites e a atualização estão no contrato.

## Marco 0.1.5: alterações em cópia nova

[Contrato e verificações](COPIA-EDITADA.md): marcador principal, nota Text e
campo Tx, com preservação da origem e recusa de sobrescrita.152/152 em
fonte/payload/sandbox, zero skips; cinco métodos GTK novos, smoke 5/5 e
launcher 3/3.85 arquivos app iguais; runtime com 2.803 arquivos/214ELF/149
pacotes atribuídos. Limites de criptografia/assinaturas/XFA/portfólios e
integração com desktop permanecem explícitos.

## Marco 0.1.4: árvores/anotações e campanha preservada

[Avanço sem VM](AVANCO-SEM-VM.md):127/127 em fonte/payload/sandbox, zero
skips; seis métodos GTK do painel e sete novos de árvores/anotações. Campanha
17/17 com os mesmos hashes/protocolos da etapa18. Fonte/payload83 arquivos
iguais, smoke 5/5, launcher 3/3; runtime 2.803 arquivos/214ELF/149 pacotes atribuídos.
Capturas examinadas; portfólios, senha, desktop e original permanecem pendentes.

## Marco 0.1.3: painel lateral corrigido

[Geometria antes/depois](ETAPA-16-LAYOUT.md):0/10 na fonte anterior e10/10
na corrigida, capturas examinadas. Suíte114/114 em fonte/payload/sandbox,
zero skips; smoke 5/5 e launcher 3/3. A correção preserva o mínimo do painel GTK.
Janela solicitada 760 px fica 924 px por outros controles; desktop e integrações
continuam pendentes. Os resultados históricos abaixo continuam preservados.

## Evidência do marco 0.1.2

Construído e instalado no [CI Linux](ETAPA-20.md), em Debian 13 com Xvfb/Openbox.
104 testes passaram na fonte, no payload e no sandbox instalado; cinco controles
smoke e três de lançamento normal passaram. Os 83 arquivos da aplicação no
payload conferem com a fonte. Manifesto e SHA-256 estão em `releases/`.
O teste gráfico ocorreu em tela virtual; cabeçalho lateral recortado e integração
com desktop real, acessibilidade e impressão física ainda precisam de validação.
O CI não contém/executa o Foxit; a VM offline do original continua necessária.

O fluxo manual `.github/workflows/linux-flatpak.yml` e seu comando
`scripts/ci_linux_flatpak.sh` documentam o ambiente atual. Os caminhos
`/workspace/...` abaixo descrevem o ambiente preparado histórico; não são
dependências presentes neste Windows. No CI, o overlay contém a licença GI/Cairo
instalada pelo Debian e o bridge nativo é copiado do pacote do sistema.

## Código-fonte

A instalação dos pacotes de desenvolvimento Debian/Ubuntu está no README.
O aplicativo usa GTK 3, Cairo, Poppler, Pillow, cryptography, clientes CUPS e
pypdf 6.20.1 incluído com licença. Execute `bash scripts/run.sh caminho.pdf`.
Para OCR na fonte, instale também `tesseract-ocr`, `tesseract-ocr-por` e
`tesseract-ocr-eng`; o Flatpak 0.1.11 inclui essas ferramentas e dados locais.
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

Use um stage novo. A saída é `dist/LinuxitPDF-0.1.3-x86_64.flatpak`.
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


## Auditoria de uma entrega já publicada

A [etapa 21](ETAPA-21.md) reinstalou o bundle 0.1.2 sem rebuild, conferiu os
bytes/avisos do deployment e passou em novo smoke do sandbox. O comando
`scripts/audit_delivery.py` compara a fonte atual com o snapshot da entrega,
exigindo o commit testado no histórico Git; recusa saída existente. Consulte
o relatório para comandos local/instalado e os limites da auditoria.

A versão 0.1.8 inclui [criação PNG/JPEG](CRIACAO-IMAGENS.md).
A [auditoria independente do bundle publicado](../testes/resultados/0.1.8/audit/review.json)
foi aprovada; veja as notas para a confirmação remota e os próximos trabalhos.

A versão0.1.8 acrescenta [segurança/acessibilidade/CMS](SEGURANCA-ACESSIBILIDADE.md),
com validação de integridade separada da confiança e sem serviço de nuvem.
