# Criação de PDF a partir de imagens

Fonte/pacote 0.1.7 validado após o marco 0.1.6. Contrato próprio, sem
observação dinâmica do Foxit e sem alteração de pesos ou critérios do roteiro.

Em **Arquivo → Criar PDF de imagens…**, selecione PNG/JPEG, organize as páginas
com Subir/Descer, escolha a resolução e grave um novo `.pdf`. A lista é explícita,
sem varredura de diretórios. Cada imagem vira uma página com dimensões
`pixels × 72 / DPI`; a resolução informada prevalece sobre os metadados da imagem.
O botão Abrir PDF confere o hash do resultado antes de abri-lo no leitor.

A orientação EXIF é aplicada; transparência é composta sobre branco. Os pixels
decodificados são convertidos a RGB e armazenados com Flate sem nova compressão
JPEG com perdas. JPEG já pode conter perdas anteriores. Não se preservam EXIF,
comentários, metadados de câmera ou perfis ICC. A conversão CMYK/RGB do Pillow
não é gerenciamento de cores para impressão. Sem OCR, texto pesquisável,
formulários, formatos Office, páginas web ou documentos editáveis.

Limites do contrato: 1–100 imagens distintas, 72–600 DPI inteiros, 64 MiB por
fonte e 256 MiB no total, 45 megapixels por imagem e 150 megapixels no total,
128 MiB no PDF gerado. Formatos são reconhecidos pelo conteúdo. GIF/TIFF,
APNG e outros arquivos com múltiplos quadros são recusados; uma falha invalida
o lote inteiro. Hashes de todas as fontes são conferidos antes da publicação.
Os limites de tamanho final/decodificação não são um teto rígido de memória:
Pillow e pypdf alocam antes de alguns controles. No worker Linux há também
os limites já existentes de 2 GiB de espaço de endereçamento e 540 s de CPU.

O backend grava um temporário, reabre e confere as páginas/dimensões, depois
cria o destino com modo exclusivo. Não substitui arquivo existente, inclusive
se ele aparecer durante a operação. Falhas tratadas removem o temporário e
uma saída parcial criada por esta operação. O destino pode ficar visível antes
de a cópia final terminar; não há garantia de transação durável ou de proteção
contra alterações adversariais no diretório. Cancelar/fechar encerra o processo;
uma interrupção forçada pode deixar temporário ou PDF incompleto, ou ocorrer
depois de a gravação terminar. A interface instrui conferir o destino antes
de repetir. O cancelamento não promete desfazer uma gravação concluída.

## Evidências e limites

Implementação própria MIT em [pdf_creation.py](../app/pdf_creation.py),
[creation_window.py](../app/creation_window.py) e comandos worker vinculados.
Pillow já era dependência do projeto; pypdf BSD e demais licenças foram mantidos.
Testes em [test_pdf_creation.py](../tests/test_pdf_creation.py) e
[test_creation_gtk.py](../tests/test_creation_gtk.py): pixels, ordem, orientação,
transparência, limites, arquivos inválidos, publicação exclusiva, falhas,
worker real, fluxo GTK, abertura/renderização Poppler e cancelamento real.
Os relatórios desta rodada foram examinados e estão ligados abaixo. O pacote
0.1.6 e seus relatórios anteriores permanecem preservados.

A família conversão ganha somente este subconjunto. Exportação para formatos
editáveis, OCR, inventário Reader/Editor e fidelidade ao original continuam
abertos. Os 50 planos completos de aceitação e a paridade 0/25 não mudaram.

17 métodos do backend e 12 regressões do worker passaram localmente.
[Backend](../testes/resultados/creation-portable-2026-10-17.json),
[worker](../testes/resultados/creation-search-worker-regression-2026-10-17.json).
São execuções parciais, sem GTK/Linux local.

## Fonte Linux validada

[CI](https://github.com/airtonbp19edu/Linuxit-PDF/actions/runs/39071317244): **212/212**, zero falhas/erros/skips; 17 métodos novos do backend e cinco GTK.
Abertura e pixels renderizados por Poppler conferidos, assim como a captura da janela.
Campanha anterior preservada: 17/17, nenhuma observação Foxit.
[Relatórios e revisão](../testes/resultados/criacao-imagens-2026-10-17/review.json).
A construção Flatpak foi validada, com confirmação de publicação/auditoria nas notas.

## Marco Flatpak 0.1.7

[CI](https://github.com/airtonbp19edu/Linuxit-PDF/actions/runs/39071324606):212/212 em cada suíte fonte/payload/sandbox, sem falhas/erros/skips.
92 arquivos da aplicação e runtime conferidos; smoke 5/5, launcher 3/3.
[Revisão](../testes/resultados/0.1.7/validation-review.json). Sete versões anteriores preservadas.
