# Etapa 20 — próximo pacote de desenvolvimento

Continuação autorizada em **17/10/2026**, após as correções da etapa 19.
O candidato da fonte é **0.1.2**, branch Flatpak `devel`; o pacote publicado
continua **0.1.1** até uma nova entrega passar nas verificações abaixo.

O host Windows não oferece GTK/Poppler/Flatpak e WSL continua ausente.
Foi verificado acesso ao GitHub Actions já habilitado no próprio repositório.
O [fluxo manual Linux](../.github/workflows/linux-flatpak.yml) usa um runner
efêmero do GitHub, container Debian 13 e usuário de build dedicado. Não altera
componentes do Windows nem executa originais Foxit. O container permite o
sandbox Flatpak aninhado; a credencial do checkout não é persistida e o token
do job tem somente leitura do conteúdo do repositório. Ações oficiais são
fixadas por SHA, e nenhum workflow é disparado automaticamente a cada push.

Sequência em [`scripts/ci_linux_flatpak.sh`](../scripts/ci_linux_flatpak.sh):

1. Dependências GTK/Cairo, ponte GI, Poppler e CUPS em Debian 13; tela Xvfb e
   Openbox dedicados para a aplicação própria.
2. Perfil Linux da etapa 17: suíte completa da fonte sem skips e smoke GTK.
3. Flatpak pelo builder existente, com `runtime-lib`, loader pareado, módulos
   OpenSSL, avisos/licenças e manifesto de pacotes.
4. Igualdade dos hashes fonte/payload; suíte completa pelo Python do payload.
5. Instalação do runtime 25.08 e do candidato no perfil CI; suíte e smoke no
   sandbox instalado, além de lançamento normal e captura da janela própria.
6. Metadados do candidato somente após todos os controles passarem. Qualquer
   falha/skip impede aprovar o pacote; os logs e relatórios são preservados.

[`scripts/record_linux_candidate.py`](../scripts/record_linux_candidate.py)
confere resultados e registra hashes, commits, contagens, runtime e origem.
Os artefatos do CI ficam retidos por 14 dias; o pacote e as evidências só serão
incorporados à entrega após download e conferência. Não há assinatura digital,
declaração de estabilidade, impressão física ou comparação com Foxit nessa
campanha. A VM offline do original continua sendo uma pendência separada.

Estado deste checkpoint: **fluxo preparado; execução Linux ainda pendente**.
Os critérios históricos da etapa 20 para 0.1.1 permanecem preservados. Não
usar a existência do workflow nem o número do candidato como prova de build.
Resultados e confirmação Git serão acrescentados após a execução real.


Primeira execução real: run `39036345773`, commit `0c89ea04ffcddf525fef7955f0142b035bf030ec`. A fonte executou 103 casos: 101 passaram, uma falha e um erro, zero skips; smoke GTK 5/5. Ver [relatório preservado](../testes/resultados/etapa-20-linux-attempt1-2026-10-17.json). Foram corrigidos o isolamento dos controles sintéticos de TEMP e a recursão de sinais GTK da barra lateral, esta última encontrada no stderr. A próxima rodada deve comprovar as correções; a primeira não aprovou pacote.
