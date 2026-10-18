# Importação de TIFF multipágina

Fonte **0.1.12 em desenvolvimento**; o pacote publicado continua 0.1.11 até a
validação integral da nova entrega. Passaram 14 testes portáveis novos e os 22
testes atualizados da criação de imagens. GTK/Linux e pacote ainda aguardam CI.

Em **Arquivo → Criar PDF de imagens…**, selecione TIFFs e/ou PNG/JPEG/BMP/WebP.
Cada TIFF insere todas as páginas do encadeamento principal, na ordem do arquivo.
Subir/Descer move o arquivo inteiro como um bloco. Seleção/reordenação individual
de páginas dentro do TIFF ainda não está disponível. PNG/JPEG/BMP/WebP continuam
com uma página por arquivo; APNG, WebP animado e outros formatos animados são recusados.

A operação aceita de 1 a 100 arquivos distintos e gera até **100 páginas no
total**, incluindo as páginas dos TIFFs. O DPI escolhido, de 72 a 600, prevalece
sobre as resoluções do scanner: `pontos = pixels × 72 / DPI`. A orientação de
cada página é aplicada antes dessa medida; a transparência é composta sobre branco.
As páginas podem ter tamanhos e modos de cor diferentes. A saída é RGB de oito
bits; precisão de 16/32 bits, paletas, ICC e metadados do scanner não são preservados.
Não se promete fidelidade universal de cor ou suporte a toda variante TIFF.

O original e destinos existentes permanecem intactos. Uma página inválida ou
um limite excedido recusa o lote inteiro, sem publicar só as primeiras páginas.
Há limite de 64 MiB por fonte, 256 MiB de entradas, 45 megapixels por página,
150 megapixels na soma das páginas e 128 MiB no PDF gerado. Os bytes da fonte
são contados uma vez por arquivo; os pixels são contados por página. O worker
mantém seus limites de tempo/memória/CPU; esses controles não são teto rígido
para toda alocação interna das bibliotecas.

O nome final aparece somente após a cópia completa e as verificações de hash.
Cancelar ou fechar encerra o worker e invalida callbacks; confira o destino
antes de repetir, pois a publicação pode já ter concluído ou um temporário
oculto pode permanecer após interrupção forçada. Desfazer não apaga cópias salvas.

Para texto pesquisável, abra o PDF gerado e use o [OCR local](OCR-LOCAL.md).
**O OCR continua limitado a 20 páginas**: importar até 100 páginas não amplia
esse limite. OCR é uma segunda operação, com outra cópia e perdas estruturais
explícitas. Nenhum serviço de nuvem ou original Foxit é executado.

## Estrutura e proveniência

Antes de decodificar pixels, o backend verifica o encadeamento principal IFD
de TIFF clássico/BigTIFF: cabeçalho, limites de tabelas/offsets, ciclos e número
máximo de páginas. Pillow continua responsável pelos valores das tags, codecs
e pixels. Não há varredura recursiva de SubIFDs. Miniaturas/reduced images que
estejam no encadeamento principal são importadas como páginas; não há filtragem
semântica de páginas de scanner. Estrutura válida não prova decodificação válida.

O contrato foi conferido na [documentação Pillow](https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html#reading-multi-frame-tiff-images)
e nas [estruturas TIFF/BigTIFF do LibTIFF](https://libtiff.gitlab.io/libtiff/specification/bigtiff.html).
Pillow/LibTIFF já eram dependências licenciadas; nenhum recurso Foxit é incluído.

A resposta interna `linuxit-image-pdf-result-v1` passa a informar `input_count`;
`pages` e `sources` descrevem as páginas PDF. Cada entrada de `sources` tem
`input`, `frame` e `frame_count` com índices a partir de 1, além de caminho,
hash, formato, pixels e pontos. Caminho/hash se repetem nas páginas do mesmo
TIFF. O consumidor verifica a ordem completa e recusa respostas incompletas.

## Verificação

Os 14 métodos novos verificam ordem entre arquivos/páginas, orientações distintas,
transparência/modos, LZW/Group4, BigTIFF/endianness, limites agregados, corrupção
da última página, fonte alterada, destino concorrente e protocolo do worker.
Um teste anterior que exigia recusar TIFF multipágina foi adaptado e renomeado
para exigir sua importação e continuar recusando WebP animado. O resultado
histórico anterior à atualização do teste foi preservado; não era uma regressão
da nova regra de importação. Um erro de fechamento no gerador da fixture de
orientação também foi corrigido antes do CI, sem alteração do produto.

Dois métodos GTK e uma integração Linux TIFF → PDF → OCR estão preparados.
Evidências novas serão vinculadas após execução. Os 50 planos completos de
aceitação continuam sem execução diferencial. Roteiro 43,93%, 38 done/20 abertos
e paridade Foxit 0/25 preservados; a família de conversão continua parcial.
