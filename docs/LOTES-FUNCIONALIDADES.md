# Execução das25 funcionalidades em lotes de3

Pedido do usuário em19/10/2026. Esta sequência usa a ordem das25 famílias da
especificação, distinta dos pacotesP01–P10 e das21 etapas ponderadas.
O estado por item está em [execucao-lotes-funcionalidades.json](../progresso/execucao-lotes-funcionalidades.json).
Implementar um recorte próprio não encerra uma família nem comprova paridade.

| Lote | Itens | Estado / trabalho concreto |
|---|---|---|
|1–3|Abertura; navegação; apresentação|Entregues recortes0.1.14,432/432 próprios por ambiente. Físico/Wayland/original e famílias amplas abertos.|
|4–6|Busca em texto; marcadores; comentários|Fonte0.1.15 preparada;7 portáveis passaram,2 GTK aguardam Linux.|
|7–9|Busca em anexos; índice; linguagem|Fonte0.1.15 implementada:8 novos portáveis e24 regressões passaram; Linux/GTK pendentes.|
|10–12|Seleção; impressão; imposição|Fonte0.1.15: seleção por blocos, preparação cancelável, cópia atômica e geometria validada;6 portáveis+9 regressões passaram. Linux/físico/bidi completo pendentes.|
|13–15|Marcadores; anotações; formulários|Fonte0.1.15: respostas/Ink/combo editável implementados;7 portáveis+21 regressões passaram. GTK/Linux e JavaScript/XFA abertos.|
|16–18|Anexos; assinaturas; segurança|Fonte0.1.15: membros de portfólio/sessão por senha, assinatura local PEM e permissões;7 novos+28 regressões passaram. UI/Linux e confiança/LTV/RMS abertos.|
|19–21|Acessibilidade; medidas; camadas/mídia|AT-SPI/voz, área/perímetro/calibração e visibilidade; mídia/3D exigem motores próprios.|
|22–24|Preferências; nuvem; conversão|Preferências e formatos; **23, nuvem direta, permanece adiada**, por confirmação explícita do usuário. Pastas sincronizadas preservadas.|
|25|Plataforma|Portais, associação/atualização e Windows; validar o que estiver disponível no Linux do CI.|

## Contrato próprio do lote4–6

- Busca conserva a ordem atual: texto por página, marcadores na ordem do
  outline, comentários na ordem de páginas/anotações; anexos depois, se ativos.
  Não se afirma que essa ordem reproduza o Foxit.
- Assunto, corpo e autor são pesquisados separadamente: uma frase não pode
  começar no assunto e terminar no corpo. Ocorrências distintas em cada campo
  são mantidas e identificadas por `match_field`.
- Respostas `/IRT` e agrupamentos `/RT` têm ID próprio, pai e profundidade.
  Mesmo objeto repetido em `/Annots` entra uma vez; objetos distintos com texto
  igual continuam distintos. Pai não listado pode ser incluído explicitamente
  como inferido. Vínculos entre páginas, ciclos, profundidade excessiva e tipos
  desconhecidos produzem avisos, sem inventar destinos.
- Até50000 anotações,64 níveis e65536 caracteres por campo após decodificação.
  Rich text textual é convertido em texto sem executar HTML/scripts ou rede;
  rich text em stream permanece uma omissão explícita. Não são limites prévios
  de memória de todo o parser PDF.
- Parar preserva apenas resultados já entregues à interface, invalida callbacks
  tardios e sinaliza a interrupção. O subprocesso Poppler ativo recebe o
  cancelamento do runner. Não se promete interrupção imediata de toda operação
  interna do parser Python.
- Hits de metadados selecionam a linha identificada no painel e navegam à página
  conhecida. Destinos sem página local continuam sem destino, sem retângulos
  fictícios. A busca não executa ações externas.

Semântica PDF consultada na [referência Adobe PDF1.6](https://opensource.adobe.com/dc-acrobat-sdk-docs/pdfstandards/pdfreference1.6.pdf),
tabela de markup annotations (`IRT`, `RT`, `RC`). Não é observação dinâmica do original.

## Validação e limites

`tests/test_comment_threads.py`:7 métodos portáveis passaram localmente;
2 métodos GTK preparados e não executados no Windows sem GTK/tela. Linux e
regressão completa pendentes. O primeiro erro de coleta por import de Cairo foi
corrigido usando fixtures pypdf independentes. Relatórios brutos preservados em
`analysis-local/batches-20261019/` (ignorado).

Último Flatpak permanece0.1.14/devel; fonte0.1.15 ainda não empacotada.
As50 aceitações amplas continuam abertas, paridade0/25 e percentual global
indeterminado. VM0930 continua suspensa no checkpoint anterior; não acessada
nesta sequência. Critérios e pesos do checklist preservados.


## Contrato próprio do lote7–9

Anexos HTML UTF-8 são lidos como texto, ignorando scripts/estilos, sem buscar
URLs. DOCX/ODT usam apenas XML textual do corpo; sempre sinalizam que desenhos,
cabeçalhos, equações e objetos foram omitidos. Não exportam ZIP, executam macros
ou leem relações externas. Até2000 entradas/2MiB expandidos e128 níveis XML;
DTD/entidades são recusados. UTF-8 inválido e formatos restantes ficam explícitos.

Revisar PDFs do índice permite excluir entradas desmarcadas e reextrair todas as
fontes selecionadas. A confirmação carrega o hash do índice visto, para recusar
versão alterada durante o diálogo. O índice anterior fica preservado em falhas.
Escritores cooperantes usam .lock exclusivo; uma trava abandonada por encerramento
forçado exige conferência e remoção explícita pelo usuário. Não remover
automaticamente uma trava cuja propriedade não esteja confirmada. Arquivo novo
é publicado inteiro e sem sobrescrita (rename no Windows; hardlink no Linux),
falhando de forma segura em filesystem sem essa operação. Atualização usa replace
após conferir identidade; programas externos que ignoram a trava não participam
da coordenação. Não é um índice compatível com o Foxit.

Radicais usam as classes Python fixadas do [Snowball3.1.1](https://pypi.org/project/snowballstemmer/3.1.1/),
BSD-3-Clause, sem alterar o pacote. Proveniência/hash/licença em
[proveniencia-snowball.json](proveniencia-snowball.json), licença também copiada
para o pacote. Modos português/inglês casam1–8 tokens consecutivos por radical,
independente de caixa; não são lematização, sinônimos ou IA. O algoritmo PT está
[documentado pelo projeto](https://snowballstem.org/algorithms/portuguese/stemmer.html).
Opção de caixa desabilitada nesses modos; acentos são removidos antes do radical
somente quando o usuário pede isso. Demais idiomas e algoritmo original abertos.

Testes novos em tests/test_search_batch_extensions.py:8 portáveis passaram e1 GTK
aguarda Linux. Regressões test_collection_index.py12/12 e
test_attachment_search.py12/12 passaram no host Windows. CI4–6 ainda em fila;
não extrapolar esses resultados para GTK/Linux ou novo Flatpak.


## Lote10–12: recortes implementados, obrigações restantes abertas

Seleção retangular exige interseção com área positiva, mantém a ordem Unicode
emitida pelo extrator e separa colunas/blocos por linha vazia. Não reverte strings
RTL por aparência visual. Seleção por caractere, ordem lógica de todo PDF bidi
ou mal estruturado e corpus multilíngue completo continuam pendentes.

Preparação de impressão roda pelo transporte JSON cancelável, separado da
submissão. Cancelar antes da conclusão não envia o trabalho; callbacks tardios
são invalidados. No Linux o grupo do worker e seus filhos é encerrado. A janela
de preparação encerra antes da submissão CUPS; depois disso não oferece um
cancelamento de fila que ainda não foi implementado. Não é prova de impressora
real, spooler, encerramento do Foxit ou Windows com subprocessos netos.
Salvar PDF usa arquivo temporário no mesmo diretório/replace e recusa substituir
o original, inclusive por hardlink; erro preserva destino anterior. PDFs abertos
por senha/recuperação ainda não estão integrados na impressão.

Imposição recusa destino igual ao original, modo desconhecido, parâmetros não
finitos/fora de faixa e CropBox não positivo ou acima dos limites. CropBox com
origem negativa válida continua aceito.6 novos portáveis e9 regressões existentes
passaram;1 GTK aguarda CI. Nenhuma operação física/bidi ampla foi promovida a
concluída no inventário. Preservar todos os relatórios anteriores.


## Lote13–15

As operações existentes de marcadores/hierarquia passaram nas21 regressões
avançadas, junto de checkbox/radio/listas/anotações. Combo editável aceita um
valor livre de até4096bytes, sem caracteres de controle; preserva export/label
das opções, gera AP e remove índices antigos quando o texto não é uma opção.
Edit sem Combo, seleção múltipla editável, nomes ambíguos, readonly e valores
inválidos continuam recusados. Não executa eventos/JavaScript; XFA continua
explicitamente não implementado.

Ink usa até32 traços/4096 pontos com aparência vetorial própria vermelha e flag
de impressão. A folha de desenho GTK representa a página sem fundo e antes da
rotação; não é uma sobreposição do documento nem seleção automática de texto.
Traços minúsculos, fora da página, números não finitos e limites são recusados.
Respostas adicionam Text com IRT/RT à anotação selecionada na mesma página,
preservando o pai; recusam locks, vínculos cíclicos e profundidade excessiva.
Editar/excluir pais com dependentes permanece bloqueado. Salvar exige arquivo
novo; desfazer/refazer atua no rascunho. Documentos assinados, cifrados, portfólios
e XFA seguem sujeitos às recusas anteriores de edição.

7 novos métodos portáveis passaram,1 GTK aguarda CI;21 regressões avançadas
passaram no Windows. As duas primeiras respostas de um teste precisavam usar o
índice da nova anotação, e não o índice1 ocupado por Widget; expectativa corrigida.
Não foi removida a proteção do backend nem foi executado o Foxit.


## Lote16–18

Portfólios expõem arquivos da árvore /EmbeddedFiles e anexos de página, sem
executar apresentação, ações ou relações externas. Layout, ordenação/campos
adicionais da coleção não são interpretados. O painel usa a sessão aberta por
senha, mantendo lease enquanto lê/extrai; o hash é da representação privada
efetivamente lida. A extração é desabilitada se a política original negar cópia.
Workers de anexos/imposição também recusam extrair/imprimir quando a senha vazia
autentica apenas como usuário sem a permissão correspondente. Não implementa RMS.

Assinar cópia usa certificado PEM e chave PEM explicitamente escolhidos no
diálogo, senha pelo stdin JSON e cryptography já existente no runtime. Limites:
PDF64MiB, cada arquivo PEM1MiB, senha4096bytes, RSA>=2048/EC>=256 e CMS32KiB.
Só primeira assinatura em PDF não cifrado, sem campo Sig prévio, XFA ou coleção,
conforme guardas anteriores de edição; campo LinuxitSignature invisível,
adbe.pkcs7.detached/SHA256 e ByteRange cobrindo o arquivo inteiro fora de Contents.
Reservas precisam ser únicas e manter comprimento. .NET/OpenSSL conferem a
assinatura antes de publicar arquivo novo; indisponibilidade/falha recusa a cópia.
Original, certificado e chave são preservados. Não se afirma apagamento seguro
de segredos da memória Python. Confiança, validade/revogação, cadeia, tokens,
TSA e LTV não são avaliados nem implementados; a interface distingue esses estados.

Semântica em [ISO32000-1 distribuída pela Adobe](https://developer.adobe.com/document-services/docs/assets/35e4369068f86065372c18787171a17e/PDF_ISO_32000-1.pdf)
e [API PKCS7 de cryptography](https://cryptography.io/en/latest/hazmat/primitives/asymmetric/serialization/).
Nenhum código proprietário, certificado/chave de usuário ou Foxit foi usado.
7 novos testes portáveis passaram,14 regressões de anexos e14 de coordenação
passaram. Interface de assinatura/painel cifrado e runtime Linux aguardam CI.
Os3 cancelamentos de runs queued retornaram409: continuam sem conclusão confirmada.
