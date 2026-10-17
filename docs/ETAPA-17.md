# Etapa 17 — verificação da compilação intermediária

Em **17/10/2026**, foi acrescentado um verificador reproduzível da fonte atual:
[`scripts/check_intermediate.py`](../scripts/check_intermediate.py). Ele cria uma
cópia isolada de `app/`, preserva as licenças MIT/BSD, registra SHA-256 de cada
arquivo e compila os módulos Python dessa cópia. Os testes usam essa aplicação
copiada por `PRINT_VIEW_TEST_APP`; os testes e o runner continuam no checkout.
Não é um instalador, um executável nativo ou um Flatpak novo.

O verificador compara a fonte com os hashes preservados do payload **0.1.1** e
separa arquivos novos, alterados e removidos. Não extrai novamente o pacote.
Depois dos testes, confere se a cópia e a fonte permaneceram intactas. Logs,
bytecode e a cópia de trabalho ficam em `analysis-local/`, ignorado pelo Git.
Relatórios e diretórios existentes são recusados, preservando rodadas anteriores.

## Dois perfis de verificação

O perfil **portable** compila Python e executa os testes de backend de anexos,
controlador e recusa de falsas aprovações do próprio verificador. Usa workers
reais e PDFs sintéticos. Mesmo quando passa, registra explicitamente
`linux_source_runtime_passed: false`. Bytecode do Python do Windows não
demonstra execução em Linux nem valida os widgets GTK.

```powershell
python scripts/check_intermediate.py --profile portable --work-dir analysis-local/intermediaria-portavel-nova --output testes/resultados/intermediaria-portavel-nova.json
```

O perfil **linux** exige host Linux, GTK 3/PyGObject, Cairo e a ponte GI/Cairo,
Pillow, cryptography, Poppler, clientes CUPS e uma conexão X11 funcional. Só
então executa **toda a suíte**, seguida das cinco verificações gráficas reais de
`smoke_linuxit.py`. Qualquer erro, falha, skip, suíte vazia/incompleta ou app
diferente da cópia impede a aprovação. Não é necessário ter VM do Foxit para
executar esse perfil. A instalação das dependências está em
[instalacao.md](instalacao.md).

Os testes antigos ainda condicionam alguns casos a `DISPLAY`; por isso usar
X11/Xwayland ou `xvfb-run` com o pacote `xvfb` instalado. Uma sessão somente
Wayland não aprova silenciosamente os testes ignorados. Em Linux preparado:

```bash
xvfb-run -a /usr/bin/python3 scripts/check_intermediate.py --profile linux \
  --work-dir analysis-local/intermediaria-linux-nova \
  --output testes/resultados/intermediaria-linux-nova.json
```

Com uma tela X11 válida, também é possível executar o mesmo comando sem
`xvfb-run`. O runtime usa o Python escolhido na chamada; no Linux preferir
`/usr/bin/python3`, que encontra as extensões GTK/Cairo do sistema. A execução
em Xvfb não substitui a inspeção manual do painel em desktop real.

## Evidências desta rodada

**80 módulos da cópia compilaram e 32/32 testes portáveis passaram**, sem
falhas ou skips: 14 de backend, 14 de controlador e quatro do verificador.
Comparação com o manifesto 0.1.1: 2 arquivos novos,
2 alterados, 0 removidos e 79 iguais.

- [Fonte compilada e testes portáveis](../testes/resultados/etapa-17-fonte-portavel-2026-10-17.json).
- [Perfil Linux recusado no Windows](../testes/resultados/etapa-17-linux-indisponivel-2026-10-17.json).
- [Integridade, sintaxe e recusas de sobrescrita](../testes/resultados/etapa-17-verificacao-2026-10-17.json):
  115 arquivos Python e 58 links locais conferidos; dois comandos recusados sem
  alterar os resultados existentes. Critérios, pesos e fonte da aplicação preservados.

O perfil Linux deve retornar erro neste host Windows sem GTK/WSL. Isso é uma
recusa de ambiente e **nenhum teste Linux aprovado**. Os quatro testes visuais
do novo painel continuam pendentes, assim como a suíte Linux atual e a geração
de um pacote que contenha as etapas 15/16.

## Progresso e próximo passo

Os dois critérios da etapa 17 já estavam `done`, com execução real da fonte e
do pacote **0.1.1** preservada. Mantê-los como evidência histórica, com pesos e
revisão inalterados. A revalidação da **fonte atual** é um checkpoint separado e
parcial até o perfil Linux passar; os testes antigos não aprovam o novo painel.
O roteiro permanece **43,33%**, paridade Foxit **0/25** e cobertura global
desconhecida (`null`). A IA continua [fora do escopo](ESCOPO.md).

Próximo passo: executar o perfil Linux, corrigir os achados e inspecionar o
painel. Depois gerar/testar o Flatpak do novo marco, usando `runtime-lib`, loader
pareado e OpenSSL conforme a instalação. A etapa 18 pode ter preparação de
cenários próprios, mas a comparação com Foxit exige a contenção offline ainda
pendente; ver [registro de pendências](../progresso/pendencias-analises.md).
