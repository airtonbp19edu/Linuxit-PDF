# Cópias com marcador, nota e campo de texto — fonte 0.1.5

Continuação do pedido de executar as frentes sem VM. A entrega **0.1.5/devel** passou nas suítes completas de fonte, payload e
sandbox instalado; o projeto permanece em desenvolvimento.
Os contratos abaixo são próprios, sem observação dinâmica do Foxit e sem
incorporar código ou recursos do original.

## Operações implementadas

No menu **Arquivo**, a fonte 0.1.5 oferece:

- **Novo marcador na página atual**: acrescenta marcador de nível principal.
- **Adicionar nota na página atual**: cria anotação PDF `/Text` com seu texto.
- **Preencher campo de texto**: escolhe um campo AcroForm `/Tx` editável.

Cada ação prepara uma cópia em **arquivo novo**. O PDF aberto e qualquer arquivo
preexistente permanecem preservados. A cópia pode ser aberta depois pelo leitor.
Não há estado de edição não salvo nem gravação em cima do original.

O backend também aceita lote JSON de até 1.000 operações; a UI aplica uma
operação por cópia. Ele verifica o SHA-256 da fonte, clona o documento, aplica
as alterações, serializa em temporário privado, reabre a saída e revalida a
identidade antes de criar o destino exclusivamente.

Mantém páginas e estruturas anteriores: marcadores, notas, anexos e metadados
têm regressão em PDF sintético. O conteúdo do PDF não é executado. A cópia não
é uma promessa de fidelidade de todos os PDFs, fontes ou estruturas existentes.

## Limites do contrato

- Recusa gravação de documentos criptografados, campos de assinatura `/Sig`,
  `/Perms`, XFA e portfólios `/Collection`; não remove proteção ou invalida
  assinatura para oferecer a operação.
- Campos `/Tx` respeitam `ReadOnly` e `MaxLen`, inclusive quando herdados. A
  consulta usa a referência PDF completa: a visão `get_fields()` do pypdf
  não preserva todas as propriedades, incluindo `MaxLen`.
- Subcampos terminais com tipo herdado são normalizados na cópia para o
  atualizador de widgets. Escolha, checkbox, cálculos, eventos e JavaScript
  de formulários não estão implementados.
- O retângulo da nota usa coordenadas PDF, dentro do CropBox. A UI escolhe uma
  posição padrão na página; colocação livre, demais anotações, exclusão e undo
  ainda estão pendentes. Renomear/mover/excluir marcadores também fica aberto.
- Título limitado a 4.096 bytes UTF-8; texto/valor a 64 KiB; pedido do worker
  limitado a 1 MiB. Isso não é limite de memória do parser PDF.
- Falhas tratadas removem o destino novo criado e o temporário. Término forçado,
  limite de recursos ou timeout podem deixar arquivo parcial/temporário; a
  mensagem orienta conferir o destino antes de repetir. Não há garantia contra
  outro processo alterando diretórios/arquivos durante a gravação.
- Documento/geração são capturados antes dos diálogos. Reabrir inclusive o
  mesmo caminho invalida a operação antiga. Uma cópia já autorizada pode
  concluir após trocar de documento, sem aplicar status ao novo.

## Código e verificações

- [Backend](../app/pdf_changes.py), [adaptador portável](../app/edit_tasks.py)
  e [comandos worker](../app/worker_cli.py): `edit-info` e `copy-edit`.
- [16 testes portáveis](../tests/test_pdf_changes.py) passaram, com roundtrip
  real, preservação de fonte/objetos anteriores, lote inválido, herança de
  campos, geometria, falhas de disco e alteração da fonte durante serialização.
- [Quatro controles do adaptador](../tests/test_edit_tasks.py) passaram:
  worker real/Unicode/conflito, protocolo inválido, timeout e comando inválido.
- [Cinco métodos GTK](../tests/test_copy_edit_gtk.py) preparados para executar
  os três diálogos reais com worker, cancelamentos, contexto obsoleto, conflito
  e repetição de cliques. **Cinco métodos passaram em Linux com tela X11 virtual.**

[Resultados portáveis](../testes/resultados/copia-editada-2026-10-17/backend-portable.json)
e [controles do worker](../testes/resultados/copia-editada-2026-10-17/worker-adapter.json).
Resultados completos locais: `analysis-local/copy-edit-nested-pass.json` e
`analysis-local/edit-adapter-tests.json`. A primeira execução detectou a lacuna
de `MaxLen`, corrigida antes de publicar o código. Nenhum teste próprio conta
como paridade diferencial ou execução dos 50 cenários completos da etapa 12.

Arquitetura atual: 23 módulos/18 interfaces; especificação: 16 subconjuntos e
nove propostas em 25 famílias. O subconjunto de formulários passou de proposta
a código próprio, com revisão explícita dos dois casos planejados; todos seguem
`not_run` como cenários completos. Critérios/pesos do roteiro permanecem iguais.

Suíte completa da fonte Linux: **152/152**, zero falhas/erros/skips, incluindo
os cinco métodos GTK e smoke 5/5. Campanha preservada 17/17 repetida na fonte.
[Revisão dos relatórios](../testes/resultados/copia-editada-2026-10-17/linux-source-review.json),
[CI](https://github.com/airtonbp19edu/Linuxit-PDF/actions/runs/39060689958).
A construção do [Flatpak 0.1.5](../releases/LinuxitPDF-0.1.5-x86_64.flatpak)
aprovou **152/152 em cada ambiente fonte/payload/sandbox**, zero falhas/erros/skips,
smoke 5/5 e launcher 3/3. Hashes e limites na
[revisão da entrega](../testes/resultados/0.1.5/validation-review.json).
A confirmação de publicação e auditoria independente fica nas notas datadas.


Entrega0.1.5 publicada em `539bccb46fb3d5fddca4b70bef5a0c70aadce9a5`,
HEAD remoto/local e árvore limpa confirmados. A
[auditoria independente](../testes/resultados/0.1.5/audit/review.json)
reinstalou o mesmo bundle sem rebuild:85 arquivos app/2803 dependências/214 ELF/
149 arquivos de licença-créditos conferidos; controles7/7 e novo smoke5/5.
Suítes152/152 não foram repetidas nesta auditoria. O registro posterior é
verificado externamente para evitar autorreferência de hash Git.
