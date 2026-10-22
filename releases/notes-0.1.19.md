# Linuxit PDF 0.1.19 — candidato de desenvolvimento

Este é um candidato de desenvolvimento. A publicação depende de aprovação do
usuário após a validação; estas notas preparadas não anunciam uma Release.

## Mudanças próprias

- Busca conforme a decisão D05: resultados de marcadores, texto, comentários e
  anexos nessa ordem. Clicar no resultado de marcador mantém a página atual;
  a navegação pelo painel de marcadores continua disponível.
- Preenchimento com JavaScript explicitamente autorizado, em processo separado:
  linguagem real, eventosK/V/C/F e API limitada de campos textuais/cálculo.
  Abrir o PDF não executa seus scripts de documento ou página.
- Layout XFA de fluxo próprio, instâncias repetíveis e paginação. Não inclui
  layout posicionado, FormCalc ou compatibilidade universal XFA.
- Preservação incremental DSS, verificação OCSP offline e preparação/importação
  de carimbo RFC 3161 com nonce e CA explícita. Não consulta TSA automaticamente
  nem garante PAdES-LTA para qualquer documento.
- Redação sem rasterizar em conteúdo simples e fontes padrão. Remove objetos
  inteiros que tocam a área, podendo remover conteúdo vizinho; conteúdo complexo
  é recusado. O modo rasterizado continua disponível. Não procura o texto em
  propriedades, marcadores ou anexos.
- Edição de texto/autor preservando carimbos gráficos; validação de conversas,
  respostas e popups. A edição universal de tipos de anotação continua aberta.
- Edição em cópia de documentos recuperáveis aceitos pelo mecanismo próprio.
- Limpeza opcional de contraste/limiar no OCR, preservando dimensões. A opção
  limiar transforma a imagem em preto/branco; o original permanece intacto.
- Exportação de PDF para texto UTF-8,PNG/JPEG em ZIP e TIFF multipágina. Limites:
  até 100 páginas em texto e 20 em imagens, além dos orçamentos de arquivo/pixels.
  Não produz documentos Office editáveis.

## Validação e limites

Candidato aprovado no CI39864579949: **742/742 testes próprios em cada ambiente**
(fonte Linux,payload e Flatpak instalado), zero falhas/erros/skips. Fumaça5/5,
launcher3/3 e193 arquivos fonte/pacote iguais. Bundle120.445.752bytes,
SHA-256 `f1ac26367ed390bf10bbe88c04df68828eb4954ef188a8d77f935f870c49723d`.
Aceitação própria81/81 na fonte e02dda2, preservada separadamente. A validação
do candidato inclui execução real dos novos controlesJS/XFA e doOCR no sandbox.
Instalador Windows é uma frente separada, sem assinatura e sem certificação de
hardware real. IA permanece fora do escopo; 3D e nuvem direta estão adiados.

Nada aqui declara reconstrução completa, equivalência integral ao Foxit ou
aprovação dos critérios ainda abertos. Fonte e dependências próprias/licenciadas;
nenhum executável, recurso ou código proprietário Foxit integra o aplicativo.
