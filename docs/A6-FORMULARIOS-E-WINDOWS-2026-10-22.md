# A6 — formulários e candidato Windows

**Atualização — 2026/10/22 às 20:37 (America/Sao_Paulo, UTC-03:00):** Passos4–6 executados: A4 registrada sem alterar critérios; candidato0.1.19/9fb4f3a validado744/744 em fonte/payload/Flatpak e aceitação81/81. Publicação retida; Windows e limites A6 no relatório. Passo7 aguarda instrução. Sem VM/B3; checklist45,13%, paridade0/25 e global indeterminado. [Evidência final do recorte](PASSOS-4-6-A456-2026-10-22.md). Os resultados locais abaixo são históricos.

Registro de implementação em 2026/10/22 às 08:45 (America/Sao_Paulo, UTC-03:00).
Esta frente executou código próprio e fixtures sintéticas; não executou Foxit,
não inspecionou a VM e não comprovou paridade diferencial. IA e nuvem direta
continuam fora desta entrega.

## JavaScript real de campos

`app/pdf_form_javascript.py` usa o motor **QuickJS-NG 0.15.1.1**, pelo binding
MIT `python-quickjs-ng`. A ação nova `fill-form-javascript` é separada de
`fill-form-events`: o preenchimento declarativo anterior continua disponível e
não passa a executar código arbitrário ao abrir um PDF.

A interface oferece **Preencher com JavaScript isolado…** no editor de cópias,
explica a autorização e coleta entradas. A execução só acontece quando se pede
essa operação explicitamente. O editor prepara rascunhos/cópias, com a mesma
publicação sem sobrescrita e conferência da identidade do original.

Fronteira implementada:

- Linguagem ECMAScript real: funções, arrays, métodos, condicionais e laços.
- Eventos de campos textuais `/K`, `/V`, `/C` e `/F`.
- Entradas passam por K/V; cálculos seguem `/AcroForm/CO` e, para os restantes,
  a ordem dos campos. Não se inventa convergência por repetir scripts.
- `event.value`, `event.rc`, `event.target`, `event.willCommit`, `event.change` e
  nome do evento; `this.getField`, `getField`, `numFields`, `getNthFieldName`.
- Objetos de campo com `name`, `readonly`, `value` e `valueAsString`.
- `AFSimple_Calculate`, `AFRange_Validate`, `AFNumber_Format` e
  `AFNumber_Keystroke` no contrato numérico explicitado pelo código.
- Valor bruto `/V` separado da representação visual gerada por `/F`.
- Resultado calculado de um campo somente leitura pode ser produzido pelo seu
  próprio evento C; entrada direta em campo calculado/somente leitura é negada.
- Validação recusada, API ausente, exceção, resultado inválido ou limite excedido
  impedem a publicação inteira. Nada é aplicado parcialmente ao original.

Contenção implementada:

- Processo filho dedicado: na fonte usa `python -I`; no Flatpak usa o loader,
  bibliotecas, Python e biblioteca padrão empacotados e pareados. Nesse ramo,
  `-s -P` e um ambiente sanitizado permitem indicar os diretórios confiáveis da
  biblioteca padrão e da extensão nativa. Não são herdados caminhos de importação
  do documento, `PYTHONPATH` externo ou user-site. O `-I` ignoraria `PYTHONHOME`
  e poderia selecionar a biblioteca padrão do host; por isso os dois contextos
  têm inicialização explícita própria, testada no sandbox instalado.
- Contexto QuickJS sem callbacks Python, módulo `std`/`os`, loader de arquivos,
  rede, navegador, timers ou objetos GTK. Um `Function` obtido por construtor
  também permanece no ambiente ECMAScript sem capacidades do host.
- Heap do motor 32 MiB, pilha 512 KiB, CPU 1 segundo por transação e timeout
  externo 6 segundos; em POSIX há também limites do processo.
- Pedido/resposta limitados; até 2048 campos inspecionados, 128 scripts de até
  16 KiB cada e 256 alterações/valores de até 64 KiB na transação.

Limites preservados: essa é uma API de campos própria, não a implementação
integral de Acrobat/Foxit JavaScript. Não são executados scripts de documento,
ações de abertura/página, botões, operações de rede/arquivos, diálogos e APIs
administrativas. Os demais AF helpers não implementados causam erro explícito.
Não há declaração de proteção contra uma vulnerabilidade nativa inédita do
motor. A contenção de capacidades não equivale a uma fronteira de VM.

Verificação local examinada: `analysis-local/a6-js-01.json`, **10/10** casos
aprovados. Inclui cálculo real e reabertura de cópia, ordem CO, formato visual,
falha atômica, APIs externas ausentes, construtor Function sem acesso ao host,
loop infinito, heap, recursão, saídas não finitas e ações de abertura ignoradas.
Os testes adicionais de revisão e a execução Linux consolidada são registrados
separadamente no marco final, sem substituir essa evidência histórica.

## XFA com layout fluido próprio

`app/pdf_xfa_flow.py` liga template e datasets para gerar **páginas novas**,
campos AcroForm editáveis, aparências PDF e um pacote datasets coerente. A ação
fica no diálogo **Campos de formulário XFA → Gerar cópia com layout fluido
próprio…**, com a alteração de aparência explicada antes da operação.

O contrato aceita subformulários `layout="tb"`, binding normal por nomes,
subformulários repetidos com `occur min/max/initial`, texto estático e campos
textuais/numéricos/de data. A repetição é efetiva: inserir/remover uma instância
altera os dados, os caminhos SOM, os campos e a paginação da cópia. Valores
iniciais vêm do template. Remover até zero quando min=0 não recria a instância.

Serviços públicos do worker:

```text
xfa-flow-info <fonte.pdf>
xfa-flow-copy <fonte.pdf> <novo.pdf>
```

O segundo recebe JSON por stdin:

```json
{
  "source_sha256": "SHA-256 da fonte atual",
  "values": {"form1[0].cliente[0]": "José"},
  "instances": [
    {"action": "add", "path": "form1[0].item", "index": 1}
  ]
}
```

Índices são base zero; a edição de valores é resolvida depois das alterações
de instância. A UI separa edição de valores e alteração de uma instância por
cópia para evitar atribuir uma edição ao registro errado após mudar os índices.
O backend admite até 100 operações de instância e 256 valores por transação.

Limites: até 8 MiB de dados XML, profundidade 64, 5000 linhas/campos,
100 páginas e 48 linhas visuais por campo. O layout portátil usa Helvetica
WinAnsi/Windows-1252 e recusa caracteres sem glifo correspondente, sem trocá-los
silenciosamente por `?`. Scripts, FormCalc, binding explícito complexo,
referências externas, layout posicionado e controles não cobertos são recusados.
XML com DTD/entidades e binding duplicado também são recusados. Assinaturas e
cifra exigem outra política; essa conversão não os aceita.

Isso **não** é preservação universal de aparência XFA nem suporte integral ao
layout de Adobe Designer. O resultado diz `original_layout_preserved=false`
e `scripts_executed=false`. O original é preservado e um arquivo existente
nunca é substituído.

Verificação local examinada: `analysis-local/a6-xfa-01.json`, **9/9** casos
aprovados. Inclui widgets/AP e reabertura real com pypdf, datasets coerentes,
min/max, inserção/defaults, exclusão até zero, 81 campos distribuídos em várias
páginas, recusa de DTD/scripts/binding/layout/Unicode, hash e não sobrescrita.
Regressões anteriores: `a6-form-regression.json`, **19 aprovados/1 GTK não
executado localmente**; `a6-xfa-regression.json`, **15/15 aprovados**.

Três testes GTK novos estão em `tests/test_forms_a6_gtk.py`; dependem de desktop
GTK real e não foram classificados como aprovados por compilação Python.

## Windows: build, instalador e suíte completa

Arquivos novos:

- `scripts/prepare_windows_js.py`: baixa o sdist oficial da versão fixada,
  confere SHA-256/tamanho via metadados PyPI, guarda avisos completos e compila
  o mesmo C para **Python MSYS2 UCRT64**, em vez de carregar um wheel MSVC
  incompatível com esse ABI. A receita não modifica o código C do motor.
- `scripts/build_windows.py`: copia aplicação e runtime selecionado, gera
  launcher nativo e NSIS, inventário arquivo/tamanho/SHA-256/origem de pacote,
  avisos, informações dos pacotes MSYS2 e hash final do instalador.
- `packaging/windows/launcher.c` e `windows_bootstrap.py`: configuração local
  e relocável de DLLs, GTK, schemas, tipagem GI, imagem e worker. Não mudam o
  PATH global nem instalam serviços.
- `packaging/windows/linuxit.nsi`: instalador de desenvolvimento por usuário,
  `RequestExecutionLevel user`, atalhos e desinstalação em HKCU. Exige pasta
  nova e não contém `RMDir /r`: o desinstalador remove a lista de arquivos
  instalada, preservando arquivos alheios acrescentados depois.
- `scripts/check_windows_installer.py`: só aceita execução em runner efêmero
  GitHub Windows. Instala silenciosamente em pasta nova dentro de RUNNER_TEMP,
  compara os bytes, testa GTK/Poppler/Cairo/QuickJS instalados com PATH externo
  limpo, verifica HKCU, desinstala e confere preservação de arquivo não seu.
- `.github/workflows/windows-native.yml`: mantém o probe original, acrescenta
  suíte inteira e aceitação, compila o instalador e executa o teste instalado.

O artefato é um **candidato de desenvolvimento sem assinatura Authenticode**.
Não há publicação de release por esse workflow. Compilar o instalador não
certifica o Windows inteiro. A suíte completa registra falhas, erros e skips;
uma etapa temporariamente continuada serve para guardar todos os relatórios,
e a verificação final falha se suíte/aceitação não aprovaram. Resultados de
portais, CUPS ou outros serviços exclusivamente Linux não viram aprovação
Windows por estarem indisponíveis.

Até este registro, os scripts Windows receberam compilação sintática e revisão,
mas **o build NSIS, a compilação UCRT64, a instalação e a suíte completa Windows
dependem da primeira execução real do CI**. Nenhum pacote/instalador foi
instalado no computador do usuário nesta frente. O status final e quaisquer
correções posteriores pertencem às evidências do CI, não a esta preparação.

Fontes verificadas para as escolhas de dependências:

- [QuickJS-NG Python, API/limites e MIT](https://pypi.org/project/python-quickjs-ng/)
- [Receita upstream do binding](https://github.com/genotrance/quickjs-ng/blob/master/setup.py)
- [NSIS UCRT64](https://packages.msys2.org/packages/mingw-w64-ucrt-x86_64-nsis)
- [Tesseract e idiomas UCRT64](https://packages.msys2.org/packages/mingw-w64-ucrt-x86_64-tesseract-ocr)
- [Dados portugueses](https://packages.msys2.org/packages/mingw-w64-ucrt-x86_64-tesseract-data-por)
- [eSpeak NG UCRT64](https://packages.msys2.org/packages/mingw-w64-ucrt-x86_64-espeak-ng)
