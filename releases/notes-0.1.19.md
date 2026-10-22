# Linuxit PDF0.1.19 — candidato de desenvolvimento

Este é um candidato de desenvolvimento. A publicação depende de aprovação do
usuário após a validação; estas notas preparadas não anunciam uma Release.

## Mudanças próprias

- Busca conforme a decisãoD05: resultados de marcadores, texto, comentários e
  anexos nessa ordem. Clicar no resultado de marcador mantém a página atual;
  a navegação pelo painel de marcadores continua disponível.
- Preenchimento com JavaScript explicitamente autorizado, em processo separado:
  linguagem real, eventosK/V/C/F e API limitada de campos textuais/cálculo.
  Abrir o PDF não executa seus scripts de documento ou página.
- LayoutXFA de fluxo próprio, instâncias repetíveis e paginação. Não inclui
  layout posicionado, FormCalc ou compatibilidade universalXFA.
- Preservação incrementalDSS, verificaçãoOCSP offline e preparação/importação
  de carimboRFC3161 com nonce e CA explícita. Não consultaTSA automaticamente
  nem garantePAdES-LTA para qualquer documento.
- Redação sem rasterizar em conteúdo simples e fontes padrão. Remove objetos
  inteiros que tocam a área, podendo remover conteúdo vizinho; conteúdo complexo
  é recusado. O modo rasterizado continua disponível. Não procura o texto em
  propriedades, marcadores ou anexos.
- Edição de texto/autor preservando carimbos gráficos; validação de conversas,
  respostas e popups. A edição universal de tipos de anotação continua aberta.
- Edição em cópia de documentos recuperáveis aceitos pelo mecanismo próprio.
- Limpeza opcional de contraste/limiar noOCR, preservando dimensões. A opção
  limiar transforma a imagem em preto/branco; o original permanece intacto.
- Exportação dePDF para textoUTF8,PNG/JPEG emZIP eTIFF multipágina. Limites:
  até100 páginas em texto e20 em imagens, além dos orçamentos de arquivo/pixels.
  Não produz documentosOffice editáveis.

## Validação e limites

O resultado final do candidato será ligado ao manifesto0.1.19 após o CI.
Suíte de fonte anterior:742/742 próprios e81/81 aceitações em e02dda2; o pacote
com runtime atualizado recebe testes próprios em fonte,payload e sandbox.
InstaladorWindows é uma frente separada, sem assinatura e sem certificação de
hardware real. IA permanece fora do escopo; 3D e nuvem direta estão adiados.

Nada aqui declara reconstrução completa, equivalência integral aoFoxit ou
aprovação dos critérios ainda abertos. Fonte e dependências próprias/licenciadas;
nenhum executável,recurso ou código proprietárioFoxit integra o aplicativo.
