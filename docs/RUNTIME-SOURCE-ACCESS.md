# Fontes e licenças do runtime distribuído

O código próprio Linuxit PDF tem licença MIT. O bundle contém programas/bibliotecas
independentes sob suas licenças, incluindo eSpeak NG invocado como processo
separado. Os avisos completos acompanham `share/doc/linuxit-pdf/runtime-copyright/`
e `runtime-common-licenses/`, não sendo substituídos pela licença do aplicativo.

Ao lado dos avisos, `runtime-packages.tsv` identifica as versões binárias e fonte
exatas dos pacotes Debian utilizados. `runtime-source-access.json` fornece links
para o código-fonte correspondente de cada versão, incluindo a pasta `debian/`
com receitas/patches de construção, no serviço público Debian Sources.
Esse serviço de terceiros disponibiliza navegação e downloads de arquivos da
versão indicada. Para reconstruir um pacote Debian, pode-se obter a versão fonte
correspondente nos arquivos Debian e usar as receitas `debian/rules`; conserve
o registro de versões e avisos ao redistribuir o bundle.

O próprio empacotador está em `scripts/build_flatpak.py` e copia executáveis/dados
do Debian13, sem alterar os programas de terceiros. eSpeakNG/dados são buscados
nos pacotes oficiais do ambiente de build; a integração não incorpora seu código
ao código próprio MIT. Snowball3.1.1 é Python BSD-3-Clause sem modificações,
com hash/proveniência em `docs/proveniencia-snowball.json` e licença COPYING
também copiada separadamente para `share/doc/linuxit-pdf/`.

Links de referência: [Debian Sources](https://sources.debian.org/),
[fontes eSpeak NG](https://sources.debian.org/src/espeak-ng/).
Os links por versão do bundle são registrados no JSON gerado, para evitar trocar
a fonte correspondente por uma versão mais nova ou por um branch móvel.
