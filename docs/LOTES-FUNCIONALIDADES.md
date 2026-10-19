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
|19–21|Acessibilidade; medidas; camadas/mídia|Fonte0.1.15: voz WAV, medidas calibradas e toggle de camadas;6 portáveis+14 regressões passaram. Linux/probe/voz/pixels e mídia/3D abertos.|
|22–24|Preferências; nuvem; conversão|Preferências/quadros estáticos implementados;5 portáveis+22 regressões passaram. **23, nuvem direta, permanece adiada**, por confirmação explícita do usuário.|
|25|Plataforma|Seletor nativo e informações de instalação implementados; probe portal preparado. Persistência/associação/update real/Windows abertos.|

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


## Lote19–21

Medidas sobre snapshot da página atual: até512 pontos e coordenadas finitas;
distância entre2 pontos, perímetro fechado e área de polígono simples em
mm/cm/m/in/ft. Calibração usa comprimento conhecido dos2 primeiros pontos,
vale somente nessa janela e não altera o PDF. Área recusa interseções/degeneração;
não é certificação CAD nem equivalência da ferramenta original.

Camadas: até256 OCGs na configuração default, BaseState ON/OFF, locks e
RBGroups respeitados. Alteração explicita ON/OFF de todos os grupos e remove AS
automático desta representação de leitura. Alternativas de configuração,
BaseState Unchanged, mídia/3D e comportamento completo do original abertos.
O PDF fica em pasta privada, sem sobrescrever original. Leases mantêm arquivos
antigos enquanto leitores trabalham; caches do leitor principal são renovados.
Apresentação já aberta pode conservar seu snapshot; impressão do override está
bloqueada até integração própria. Salvar cópia normal continua copiando original.

Voz: exporta texto selecionado ou página acessível em WAV PCM mono com eSpeakNG,
sem IA/nuvem, PT/EN, até20000 caracteres/128KiB e64MiB de áudio. Não oferece fala
contínua do documento nem prova qualidade/pronúncia/dispositivo físico. eSpeakNG
e dados entram como dependências Debian separadas com atribuição de runtime;
receita alterada, pacote ainda não gerado. CLI e dados conferidos em
[manual Debian](https://manpages.debian.org/trixie/espeak-ng/espeak-ng.1.en.html)
e [lista do pacote](https://packages.debian.org/trixie/amd64/espeak-ng-data/filelist).

Probe AT-SPI real entre processos usa o widget ATK.Text do aplicativo com texto
sintético e cliente GI Atspi, conforme [interfaces GNOME](https://docs.gtk.org/atspi2/iface.Text.html).
Preparado no CI após a suíte fonte; não executado no Windows, não é teste Orca.
6 novos portáveis e14 regressões de sessão passaram;3 testes Linux (pixels,
camadas/medidas GTK e voz real) e probe aguardam ambiente. Não declarar que o
checkbox alterou os pixels antes de examinar o relatório e a renderização.


## Lote22–24

Preferências próprias de leitura: zoom inicial fit-page/fit-width/percentual,
1–6400%, painel lateral e destaques de busca. Aplicadas ao próximo documento;
gravação atômica, arquivo inválido volta aos padrões. Não guardam documento,
senha ou chave. Tema e pastas sincronizadas mantêm controles anteriores.
Demais preferências e defaults do original não foram caracterizados integralmente.

Conversão: GIF/APNG/WebP importam todos os quadros como páginas estáticas somente
mediante opção explícita. TIFF conserva comportamento anterior. Limites de100
páginas/45MP por quadro/150MP total/128MiB saída; iteração limitada de quadros.
O compositor Pillow fornece pixels de cada quadro; durações, áudio e movimento
não são incorporados ao PDF. APNG com imagem default separada é recusado.
PPM/PGM/PBM e ICO estático adicionados; ICO usa a representação escolhida pelo
decoder, sem inventar que tamanhos alternativos sejam páginas. Fontes preservadas.
5 novos testes portáveis/22 regressões passaram;1 GTK aguarda validação.

**23 permanece adiado:** integração direta/OAuth/colaboração remota não foi criada.
Pastas sincronizadas continuam disponíveis sem provar sincronização remota.
O marco825f1e4 dos lotes4–15 passou465/465 no Linux39282125477 sem skips;
relatório bruto/hash conferidos. Isso é evidência histórica, não aprovação da
fonte atual19–24. CI39292345681 cobre19–21 e está em andamento.


## Item25 e consolidação

O menu Abrir pelo seletor do sistema usa Gtk.FileChooserNative e o backend
portal/nativo que o desktop oferecer. Só arquivo local, filtro PDF e cancelamento
conserva o documento atual; abertura usa o fluxo transacional já existente.
O novo probe de CI observa tráfego real FileChooser.OpenFile/Request.Response
do cliente e confirma o caminho sintético escolhido no desktop efêmero. É um
teste X11 de portal, não prova concessão persistente no sandbox ou desktop físico.

Instalação e atualização identifica o app Flatpak esperado e apresenta o comando
fixo do gerenciador ou orienta instalar o bundle novo se não houver remote.
Não consulta rede nem executa atualização. Não há atualizador próprio nem prova
de update/rollback/associação persistente; Windows nativo segue posterior.
2 portáveis passaram e1 GTK preparado; probe/suíte consolidada pendentes.

Todos os25 itens foram percorridos nesta sequência de implementação por lotes.
Isso não encerra25 famílias: item23 segue adiado; entre lacunas conhecidas estão
bidi/caret completo, impressão física/encerramento original, eventos/XFA,
confiança/TSA/LTV/RMS, leitor de tela físico, mídia/3D, concessões persistentes,
associação/update e Windows nativo, além de toda comparação integral Foxit.
Não converter a contagem de recortes em percentual da reconstrução.
