# OCR local para uma cópia pesquisável

Fonte e Flatpak **0.1.11/devel** validados em Linux: 363/363 testes próprios
por ambiente fonte/payload/sandbox instalado, sem falhas/erros/skips. Vinte
controles de orquestração, cinco testes Linux de OCR real e cinco GTK novos.
Publicação e auditoria independente estão nas notas mais recentes. Nenhum
resultado é comparação com o Foxit.

Em **Arquivo → Criar cópia pesquisável com OCR…**, escolha português, inglês
ou ambos, resolução de 150 ou 300 DPI e um nome `.pdf` novo. Todas as páginas
são renderizadas e reconhecidas localmente por Poppler e Tesseract. A cópia
contém a imagem das páginas e uma camada de texto pesquisável. Nenhum serviço
remoto, conta ou recurso generativo é usado.

A cópia rasterizada preserva o tamanho visível do CropBox e a rotação declarada
pela página. Links, campos editáveis, marcadores, camadas, anexos, metadados e
assinaturas digitais não são transportados. Aparências que o renderizador exibe
ficam na imagem; isso não preserva a estrutura original. O arquivo original e
as cópias anteriores permanecem intactos. Use uma cópia nova, não substituição.

O resultado informa páginas sem texto detectado; elas continuam na cópia.
Texto reconhecido pode conter erros, inclusive em tabelas e múltiplas colunas.
Não há promessa de reconhecer manuscrito, corrigir inclinação, detectar orientação
de conteúdo ou preservar ordem de leitura complexa. Revise o texto antes de usar.

## Limites do subconjunto

- PDF local não criptografado, de 1 a 20 páginas, até 128 MiB. Não se tenta senha
  vazia nem se removem permissões para processar PDFs criptografados.
- Até 45 megapixels por página e 150 megapixels por operação; saída até 128 MiB.
- CropBox contido no MediaBox, coordenadas finitas dentro de ±14.400 pontos,
  UserUnit igual a 1 e rotação múltipla de 90°. Outros casos são recusados.
- Renderização e OCR têm limite de tempo por processo; o worker tem limite total,
  CPU e memória no Linux. Cancelar/fechar encerra o grupo de processos e descarta
  respostas antigas. Após cancelamento, confira o destino: a publicação pode
  já ter concluído ou um temporário oculto pode ter ficado após interrupção forçada.
- O nome final só é publicado depois da verificação do PDF completo e do hash
  da fonte. Destino existente ou criado por outro processo é preservado.
- TIFF multipágina, imagens animadas, OCR em lote, texto editável e fidelidade
  universal continuam pendentes. Esta entrega não fecha a família de conversão.

## Dependências e proveniência

O OCR usa o executável Tesseract com dados `por`/`eng`, sem alteração dos modelos.
O builder inclui executável, bibliotecas, dados e os avisos de licença dos pacotes
Debian correspondentes no inventário de runtime. Não há binário ou recurso Foxit.
Sintaxe e comportamento da ferramenta consultados na
[documentação oficial](https://tesseract-ocr.github.io/tessdoc/Command-Line-Usage.html).
Na fonte Linux, instale `tesseract-ocr`, `tesseract-ocr-por`, `tesseract-ocr-eng`
e `poppler-utils`, além das dependências usuais do leitor.

## Verificação preparada

Os 20 controles portáveis usam PDFs e ferramentas simuladas para verificar o
contrato de orquestração; não medem acurácia de OCR. Cinco testes Linux usam
imagens próprias com letras renderizadas, Tesseract/Poppler reais, idiomas,
extração de texto, página vazia, geometria e cancelamento de subprocessos.
Cinco testes GTK exercitam criação, abertura/renderização, conflitos, mudanças
externas, cancelamento e fechamento do documento. Os 30 métodos passaram nos três ambientes. As 50 aceitações de família
continuam planos completos sem execução diferencial; não equivalem a esses testes.

Pesos e critérios do roteiro preservados: 43,93%, 38 done/20 abertos, paridade 0/25.

## Entrega validada — 2026-10-18T10:42:03-03:00

[CI](https://github.com/airtonbp19edu/Linuxit-PDF/actions/runs/39131964575), fonte `4c5fc65cfafea876c9e7559fe4c6cff169fe3ca3`: 363/363 em cada ambiente.
Os 333 IDs anteriores preservados; 105 arquivos app iguais entre fonte/payload.
Runtime: 2849 arquivos, 224 ELF e 162 avisos de pacotes;
inclui executável Tesseract e modelos por/eng com hashes e proveniência.
[Revisão](../testes/resultados/0.1.11/validation-review.json), [manifesto](../releases/manifest-0.1.11.json).
Captura da janela OCR e captura principal examinadas; demais hashes de capturas
conferidos pelo importador. Bundle: 44671928 bytes,
SHA-256 `30a1e9ab078194df85c0bdf841316958450b916b1f87f3312eaccd491c240c02`. Desenvolvimento devel, sem assinatura digital.
