# Execução das25 funcionalidades em lotes de3

Pedido do usuário em19/10/2026. Esta sequência usa a ordem das25 famílias da
especificação, distinta dos pacotesP01–P10 e das21 etapas ponderadas.
O estado por item está em [execucao-lotes-funcionalidades.json](../progresso/execucao-lotes-funcionalidades.json).
Implementar um recorte próprio não encerra uma família nem comprova paridade.

**Consolidação 2026-10-19T14:36:34-03:00: fonte/payload/Flatpak0.1.15 passaram490/490 por ambiente.** O quadro abaixo está atualizado; contagens e pendências de Linux nos relatos de cada lote são checkpoints históricos, superados pela consolidação final. Os limites funcionais continuam válidos.

| Lote | Itens | Entrega própria0.1.15 / pendências amplas |
|---|---|---|
|1–3|Abertura; navegação; apresentação|Recortes0.1.14 preservados na regressão490/490. Físico/Wayland/original e famílias amplas abertos.|
|4–6|Busca em texto; marcadores; comentários|Parar, campos separados, conversas e destinos testados no Linux/Flatpak; comparação integral e casos restantes abertos.|
|7–9|Busca em anexos; índice; linguagem|HTML/DOCX/ODT passivos, manutenção atômica do índice e radicais PT/EN testados. Demais formatos/idiomas e índice original abertos.|
|10–12|Seleção; impressão; imposição|Blocos/colunas, preparação cancelável e cópia/geometria protegidas testadas; caret/bidi completo, impressão física e ciclo original abertos.|
|13–15|Marcadores; anotações; formulários|Hierarquia de marcadores, respostas, Ink e combo editável testados; demais anotações, eventos/JavaScript/XFA abertos.|
|16–18|Anexos; assinaturas; segurança|Membros de portfólio/sessão por senha, assinatura local PEM e permissões testados; layout/campos, confiança/TSA/LTV/RMS abertos.|
|19–21|Acessibilidade; medidas; camadas/mídia|AT-SPI sintético entre processos, WAV real, medidas e pixels de camadas testados; leitor físico, reprodução, mídia/3D e configurações alternativas abertos.|
|22–24|Preferências; nuvem; conversão|Preferências e quadros estáticos testados. **23/nuvem direta adiado**; sincronização real, formatos restantes e família ampla abertos.|
|25|Plataforma|Seletor nativo/portal X11 e informações de instalação testados; concessão persistente no Flatpak, associação, atualização/rollback real e Windows abertos.|

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


## Consolidação Linux e Flatpak0.1.15 — 2026-10-19T14:36:34-03:00

[CI39293507397](https://github.com/airtonbp19edu/Linuxit-PDF/actions/runs/39293507397), fonte`257425a84f638f872386be7c499fe56030f1a968`: **490/490 por ambiente** fonte,payload,sandbox instalado, zero falhas/erros/skips. Os432 IDs da0.1.14 foram preservados;58 métodos novos em oito módulos de teste. Casos antigos que recusavam funcionalidades agora suportadas foram atualizados explicitamente nos lotes, mantendo seus IDs; preservar IDs não significa que suas asserções ficaram idênticas. Testes próprios não equivalem aos50 planosS12 de aceitação integral.

Conferidos160 arquivos app,11 relatórios selados, smoke5/5 e launcher3/3. Runtime:3414 arquivos/242 ELF/181 pacotes Debian atribuídos. SnowballBSD e avisos/fontes de versões exatas do runtime acompanham a entrega; ver[RUNTIME-SOURCE-ACCESS.md](RUNTIME-SOURCE-ACCESS.md). Bundle de58072096bytes, SHA256`f511671c2b7a3f1e6c24a19951d586390c8a196f022f640c167b270e4ab5a2b9`. [Manifesto](../releases/manifest-0.1.15.json), [relatórios](../testes/resultados/0.1.15/) e [evidências por lote](../testes/resultados/lotes-2026-10-19/review.json).

Fonte consolidada também aprovada noCI39293331527. Probe de portal confirmou chamadaFileChooser.OpenFile, resposta e caminho do PDF sintético. AT-SPI leu o texto sintético do widget por outro processo. Nove telas doCI39293837922 examinadas sem corte dos novos controles; a captura do leitor com hit mantém o painelPáginas e não comprova visualmente o destino do comentário, que é coberto pelo testeGTK de identificação da linha. Combo editável e assinaturaCMS têm testes próprios; as respectivas capturas mostram apenas checkbox e entrada de assinatura, sem alegar um fluxo visual completo de certificado.

**Estado restante:** inventário provisório111recortes,93 com código delimitado/15 pendentes ou por caracterizar/3 adiados. Esses números não são percentual de conclusão. Portal fica pendente no contrato amplo por faltar concessão persistente/sandbox/desktop físico, apesar do probe real X11. Paridade integral0/25, inventário global aberto, índice antigo45,13% e39done/19abertos preservados. VM0930 não recebeu entradas; parada09:54:23 permanece.

Próximos trabalhos sem VM: seleção por caractere/bidi e corpus multilíngue; eventos de formulário delimitados e demais tipos de anotação; verificação de confiança/timestamp com política definida; cenários executáveis restantesS12 e validação de portal/associação/update em desktop Linux disponível. Testes de impressão física, leitor de tela e monitores físicos precisam desses recursos. Original/P03 só retoma após resolução explícita da parada e novo observador/preflight offline. Não simular aprovação desses ambientes.
