# OCR local para uma cópia pesquisável

Fonte **0.1.11 em desenvolvimento**. O pacote publicado continua 0.1.10 até
a geração e validação de uma nova entrega. Nesta preparação, 20 testes dos
controles próprios passaram; reconhecimento real, GTK/Linux e novo Flatpak
ainda precisam da execução do CI. Nenhum resultado é comparação com o Foxit.

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
externas, cancelamento e fechamento do documento. A evidência atual e eventuais
falhas corrigidas serão acrescentadas após execução; não contar planos como testes.

Pesos e critérios do roteiro preservados: 43,93%, 38 done/20 abertos, paridade 0/25.
