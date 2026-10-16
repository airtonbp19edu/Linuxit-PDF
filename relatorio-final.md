# Relatório do marco Linuxit PDF 0.1.0 — projeto em andamento

Este documento registra o marco entregue, não o encerramento das 21 etapas.
Os indicadores calculados e a metodologia estão em `progresso/progresso.md`.

## A. Engenharia reversa

Foram identificados 3.276 arquivos (499.053.838 bytes), todos relacionados ao
ZIP original por CRC/hash, 141 módulos PE, 35 FPI e 869 arquivos externos FX.
Há 122 entradas examinadas por REA/Ghidra, mais nove entradas complementares
únicas pelo backend direto: 131 no catálogo consolidado. Não são 131 contratos
funcionais completos. Foram catalogados 717 descritores e 9.973 slots internos;
slots podem repetir destinos e não são funcionalidades únicas.

As observações cobrem parte de impressão/modos/ciclo de vida, busca/opções,
zoom, indexação Lucene, plugin de marcadores e formato FX. Algoritmos completos
de renderização, busca, imposição e várias famílias permanecem parciais.
A execução funcional do Foxit não foi demonstrada na contenção Wine/WOW64,
apesar da correção/verificação de dependências. Ver `docs/relatorio-dinamico.md`.

## B. Reconstrução

Python 3, GTK 3/Cairo, Poppler, pypdf 6.20.1 e adaptadores CUPS/Windows. A base
própria MIT Winux/Print&View foi reaproveitada com licença e manifesto de origem.
Navegação, renderização, seleção, apresentação, temas, prévia e preparação de
impressão vêm dessa base e de sua consolidação anterior.

O marco acrescenta busca independente por páginas, títulos de marcadores e
conteúdo/assunto de comentários, com filtros, limite global, cancelamento e
destinos sem página tratados explicitamente. A especificação separa decisões
próprias de evidências Foxit. Não foram implementados índice de coleção,
proximidade/stemming, busca em anexos ou todas as operações de edição/serviços.
O adaptador Windows foi preservado, mas não validado como Linuxit nativo.

## C. Testes

- Código-fonte: 34 casos, 34 aprovados, zero falhas/erros/ignorados.
- Payload corrigido: os mesmos 34 casos, 34 aprovados, zero ignorados.
- Flatpak instalado: quatro verificações aprovadas, dentro do sandbox real,
  para abertura/renderização, marcador, assunto de comentário e livreto PDF.
- Launcher normal: abriu o PDF sintético; captura própria em `testes/resultados/`.
- 81 arquivos do aplicativo empacotado conferidos contra a fonte por SHA-256.

As execuções repetidas não aumentam a quantidade de testes únicos. Os testes
usam dados próprios; não são diferenciais contra o Foxit. Paridade comprovada:
**0/25 famílias identificadas (0%)**, com inventário funcional ainda incompleto.
Impressão física, serviços externos e todos os PDFs/casos extremos não foram
validados. Falhas intermediárias de empacotamento foram corrigidas na origem:
bibliotecas privadas e provedor OpenSSL incluído, com avisos/licenças.

## D. Distribuição

`releases/LinuxitPDF-0.1.0-x86_64.flatpak`, com 41.222.040 bytes. SHA-256:

```text
8bcccba438cbf345df45db44ce08018987f499d0fbe009a15840b3301fd183fb
```

ID `io.github.airtonbp19edu.LinuxitPDF`, branch `devel`, Freedesktop Platform
25.08. Bundle local de desenvolvimento, sem assinatura digital; não há submissão
ao Flathub nem declaração de versão estável. Dependências e revisões estão no
manifesto e TSV dos pacotes. Instruções em `docs/instalacao.md`.

## E. Repositório

Destino: https://github.com/airtonbp19edu/Linuxit-PDF, branch `main`.
Marcos anteriores confirmados: `5312ae0` (análise/progresso) e `739ed14`
(implementação/testes). O marco do pacote e sua confirmação são registrados
em `progresso/sincronizacao-git.json` e no histórico, após o push.
Não há GitHub Release ou tag estável criada neste marco; o artefato é versionado
no repositório. A confirmação atual de HEAD pode ser reproduzida pelo script
`verify_git_sync.py` com comprovante fora da árvore.

Os arquivos originais proprietários, templates completos, decompilações,
bases Ghidra e protótipos reprovados ficam locais e estão classificados em
`engenharia-reversa/manifesto-restricoes.json`. Não há credenciais publicadas.

## F. Resultado consolidado

O progresso geral é a soma dos pesos das etapas multiplicados pelas atividades
verificadas; a revisão inicial dos pesos permanece preservada. Publicação e
sincronização são verificadas separadamente. A cobertura global de engenharia
reversa permanece **indeterminada** porque o denominador de funções relevantes
não está fechado; quatro de 141 módulos têm investigação profunda dirigida
(2,84% com peso unitário por módulo, medida parcial que não representa o projeto).

A reconstrução integral continua pendente. O roteiro mantém bloqueios e próximas
tarefas explícitos; nenhuma etapa aberta foi encerrada para aparentar 100%.
