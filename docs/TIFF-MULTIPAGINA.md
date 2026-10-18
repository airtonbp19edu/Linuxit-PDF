# Importação de TIFF multipágina

Fonte e Flatpak **0.1.12/devel**, validados com 380/380 testes próprios em
fonte/payload/sandbox instalado, sem falhas/erros/skips. Novos: 14 portáveis,
dois GTK e uma integração TIFF→PDF→OCR. Um teste histórico foi adaptado à
aceitação de TIFF; 362 IDs anteriores preservados. Publicação/auditoria nas notas.

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
da nova regra de importação. A primeira execução Linux teve 379/380 com erro
no gerador BigTIFF do Pillow 11.1, antes de chamar o produto; também expôs um
fechamento duplicado no gerador de orientação. As duas entradas agora são
fixtures próprias fixadas por hash em `testes/fixtures/tiff-multipage/`, geradas
separadamente com Pillow 12.3. Os testes só leem os arquivos e verificam pixels,
sem exigir que diferentes versões da biblioteca gerem BigTIFF. Nenhuma alteração
no importador do produto foi necessária para essa correção dos testes.

Dois métodos GTK e uma integração Linux TIFF → PDF → OCR passaram nos três
ambientes, com abertura, pixels Poppler, limite agregado e OCR real conferidos. Os 50 planos completos de
aceitação continuam sem execução diferencial. Roteiro 43,93%, 38 done/20 abertos
e paridade Foxit 0/25 preservados; a família de conversão continua parcial.

## Entrega validada — 2026-10-18T12:43:31-03:00

[CI](https://github.com/airtonbp19edu/Linuxit-PDF/actions/runs/39141058408), fonte `b2ee3e324f0cb2bb23032ce82239ea56c84302d1`:380/380 por ambiente.
[Revisão](../testes/resultados/0.1.12/validation-review.json), [manifesto](../releases/manifest-0.1.12.json).
Capturas TIFF/criação/principal examinadas; demais hashes conferidos.105 arquivos
app iguais entre fonte/payload; runtime 2849 arquivos,
224 ELF e 162 avisos de pacotes. Nenhuma nova dependência adicionada.
Bundle 44661792 bytes, SHA256 `77cbff20cdb351272de9292ce334fb97c327fdfbef7fb3321d408fe6e5144701`.
Desenvolvimento devel, sem assinatura digital. Original não executado.

## Publicação e auditoria independente — 2026-10-18T12:48:12-03:00

Entrega `d70773a67d471569631e0517a7990e21c2c0d21b` confirmada no remoto. [Auditoria](https://github.com/airtonbp19edu/Linuxit-PDF/actions/runs/39141995602)
reinstalou o mesmo bundle, sem rebuild: 105 arquivos app,
2849 de dependências, 224 ELF e 162 avisos de pacotes conferidos,
incluindo modelos por/eng. Sete controles do auditor e cinco novos smoke checks
passaram. As suítes completas 380/380 continuam evidência do builder anterior;
não foram repetidas pela auditoria. [Relatórios](../testes/resultados/0.1.12/audit/review.json).
Download público sem login conferido por tamanho e SHA-256:
[recibo](../testes/resultados/0.1.12/download-integrity-2026-10-18.json).
As limitações e os 20 critérios abertos continuam; não há observação Foxit.
