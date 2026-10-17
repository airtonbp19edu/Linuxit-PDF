# Busca em anexos, consultas e coleções — fonte 0.1.6

Continuação autorizada sem VM em17/10/2026. A entrega 0.1.6 passou em fonte/payload/sandbox; a publicação e auditoria
independente são registradas nas notas. O projeto segue em desenvolvimento.
São contratos próprios; nenhum original executado nem semântica Foxit presumida.

## Anexos

O seletor **Anexos (texto/PDF)** vem desativado. Busca nos anexos do catálogo,
árvores Kids e anotações de página, na ordem preservada da listagem. Formatos:
TXT/CSV/MD/LOG/JSON/XML em UTF-8, inclusive BOM, e texto de páginas PDF pelo
pypdf. Não abre/executa/exporta anexos, não faz OCR, não procura em anexos
internos de outro PDF, não remove proteção. PDFs anexos criptografados são
recusados. Portfólios e senha do host continuam fora deste contrato.

Limites:100 entradas,2 MiB por payload,8 MiB decodificados no conjunto,100
páginas por PDF anexo,2 MiB de texto extraído por anexo e5000 resultados.
Tamanhos reais são conferidos **depois da descompressão/extração**; não são
um teto absoluto de RAM/disco do parser. Worker Linux tem os limites existentes
de recursos; a espera cancelável tem120 s e resposta limitada a16 MiB.

Cada hit identifica índice/nome/hash do anexo, hash do host e página interna
quando for PDF. Nunca recebe página principal ou geometria fictícias. Formatos
recusados/erros/limites produzem relatório de omissões, **anexos parciais** na UI
e motivos no tooltip. Um erro estrutural do host aborta a busca. Zero resultados
não implica pesquisa de todos os formatos. Limite de hits indica possível corte.
Snippets usam texto normalizado; não são offsets de bytes do anexo original.

## Modos de consulta

- **Literal**: contrato anterior preservado, inclusive caracteres* e? literais.
- **Coringas por palavra**: um padrão de até64 caracteres normalizados, com até
  oito* ou? e ao menos um caractere de palavra. `*` aceita zero ou mais caracteres;
  `?` aceita exatamente um. Sempre corresponde à palavra completa Unicode.
  Sem sintaxe regex, escapes, frases ou stemming.
- **Proximidade ordenada**: de duas a oito palavras na ordem consultada;
  distância0–50 é o total de palavras intermediárias em todo o intervalo.
  Ocorrências não se sobrepõem. Destaque geométrico inclui o intervalo entre
  termos. Não cruza blocos/páginas do documento nem páginas dos PDFs anexos.

Consulta até256 caracteres. Palavras são letras/números/marcas Unicode e `_`;
palavra acima de4096 caracteres é recusada nos modos avançados. NFC/casefold e
opção de acentos são compartilhados. Flag Palavra inteira só se aplica ao modo
literal; os modos avançados já trabalham com palavras completas. Stemming,
linguagem de consulta Lucene e equivalência ao original continuam pendentes.

## Coleção persistente

Menu **Arquivo → Pesquisar em coleção**. **Criar/atualizar** escolhe PDFs e
arquivo `.linuxit-index.json`; **Abrir índice** reutiliza o snapshot em outra
execução. Não varre diretórios, indexa perfis pessoais ou usa contas/rede.
Armazena texto extraído e caminhos absolutos locais; o usuário escolhe onde
salvar e controla esse arquivo. Não é um índice portátil entre máquinas.

Formato JSON versionado com SHA-256 do corpo, fontes e arquivo. É snapshot de
texto com varredura durante consulta, sem formato Lucene/FTS, OCR ou promessa de
velocidade sobre todo o corpus. Limites:100 PDFs,64 MiB por fonte,256 MiB no
total,1000 páginas,16 MiB de texto e64 MiB do índice. Recusa PDFs criptografados.

Antes e depois da consulta revalida os hashes das fontes; PDFs ausentes ou
alterados são excluídos e enumerados para atualizar o índice. Revalida também
o índice; alteração durante a consulta aborta. Abrir resultado revalida o PDF
e navega à página real, sem inventar destaque geométrico. Lista visual limitada
a350 entradas, com aviso para refinar; protocolo limitado a5000 hits.

Atualização aceita somente um índice próprio íntegro. Prepara/valida temporário,
reconfere fontes e índice anterior e substitui com `os.replace`; destino novo
usa criação exclusiva. Falhas tratadas preservam o anterior e removem saídas
novas parciais/temporários. Não é garantia de durabilidade após queda de energia
nem proteção contra corrida maliciosa de diretório. Cancelamento/kill pode
ocorrer após a troca atômica ou deixar temporário; conferir antes de repetir.

## Verificações e lacunas

Oito métodos dos modos e 12 dos anexos passaram; 12 controles do índice
também passaram, incluindo falha de criação parcial e alteração concorrente.
Seis métodos GTK preparados; no Windows ficaram skipped por falta de GTK/tela.
[Relatórios portáveis](../testes/resultados/sem-vm-continuacao-2026-10-17/).
Novos [PDFs próprios](../testes/fixtures/busca-avancada/manifest.json) têm hashes
fixados, separados do corpus preservado18. Os50 cenários completos continuam
not_run e a referência Foxit continua desconhecida.

## Continuação estática examinada

Ghidra12.1.4 direto-noanalysis, seed script REA, JDK21, em cópia do último projeto.
Cinco entradas novas; Capstone5.0.6/pefile conferiram517 instruções/1572bytes.
Catálogo245 =152 REA +93 exclusivas diretas; sem denominador global conhecido.

| Entrada | Bytes | Resultado parcial |
|---|---:|---|
|0x16664e0|834|Consumidor do fator: dimensões/offsets escalados, ramos por modos3/6 e recursos temporários de imagem. Flags e saída física completas ainda não identificadas.|
|0x1b8a7a0|106|Fábrica aceita tipo3, aloca0x90 e encaminha1c68ca0; demais tipos retornam zero. Classe concreta pendente.|
|0x1b8ae20|451|Caminho auxiliar prepara região/contexto e chama1b8d860; flag+118 escolhe sinalização+11c. **Não é destructor/finalização universal**, refinando a hipótese da fila anterior. Stack/tipagem provisórias.|
|0x15c6550|163|Aloca0x84 e encaminha15c5010, devolvendo objeto ao chamador. Classe/contexto ainda não provados.|
|0x872f20|18|Getter condicional da cadeia+130/+204. Nome visual e classe ativa não confirmados.|

[Metadados](windows-evidence/foxit-rea/headless-cross-checks-no-vm-continuation-2026-10-17.json)
e [checagem independente](../testes/resultados/sem-vm-continuacao-2026-10-17/static-machine-checks.json).
Raw/projeto em `analysis-local/headless/no-vm-continuation-2026-10-17/`.
Novo verificador reutilizável`scripts/check_foxit_machine.py` exige hash fixado,
rodada privada e saída nova. Não prova tipos/semântica nem conta helpers duas vezes.

Próximos alvos:1c68ca0 e15c5010 para classes;20a6f70 para consumidor de imagem;
campos3/5/6/7/12/16/20 da busca e IDs7911/7913 continuam incompletos. Não repetir
os cinco alvos examinados nem alterar pesos/paridade por contagem de funções.


## Fonte Linux e revisão das capturas

Run39069391926/cb3c514: **190/190**, zero falhas/erros/skips; seis métodos GTK,
smoke 5/5 e campanha preservada 17/17 aprovados. [Primeira revisão](../testes/resultados/sem-vm-continuacao-2026-10-17/source-attempt1-review.json).
As capturas mostraram o frame anterior à repintura após completar o modelo.
Corrigida a sincronização **do teste**, aguardando a repintura, sem alterar
aplicativo. Construção39069595028 cancelada para repetir evidência visual;
não é falha de funcionamento nem dado do Foxit.

## Classes e consumidor — segunda rodada

Mais três entradas examinadas em cópia do projeto:372 instruções/1651bytes
conferidos por Capstone. Total desta continuação: **oito entradas novas**,
889 instruções/3.223 bytes. Catálogo **248 =152 REA +96 diretas exclusivas**.

| Entrada | Bytes | Resultado parcial |
|---|---:|---|
|0x1c68ca0|264|Construtor instala vtable0x541b7bc; RTTI identifica **CPDF_ImageRenderer**. Liga o auxiliar da fábrica de tipo3 ao renderer de imagem; não fecha o pipeline gráfico.|
|0x15c5010|1254|Construtor instala vtables base0x53d2b38 (**IPDFViewer**) e derivada0x53d31f8 (**CReflowViewerEx**), com recursos/configuração intermediários. A fábrica15c6550 e objeto criado por880490 pertencem ao caminho de reflow; demais getters e disponibilidade visual continuam parciais.|
|0x20a6f70|133|Compõe retângulo de destino, intersecta com clip+1c/+20/+24/+28 e encaminha slot virtual+0x64 do dispositivo. Retorna1 quando região é vazia, sem provar saída física bem-sucedida.|

[Metadados](windows-evidence/foxit-rea/headless-cross-checks-no-vm-context-2026-10-17.json),
[checagem de instruções](../testes/resultados/sem-vm-continuacao-2026-10-17/static-context-machine-checks.json)
e [joins exatos de RTTI](../testes/resultados/sem-vm-continuacao-2026-10-17/static-context-rtti.json).
Raw/projeto: `analysis-local/headless/no-vm-context-2026-10-17/`.
Limites: stack/signatura de15c5010 provisórias; nomes não provam disponibilidade
Reader, UI completa ou classificação de todos os objetos. IDs7911/7913 não
foram resolvidos. Próximos alvos:15c9c90/15c5e00 para recursos de reflow e slots
virtuais de CPDF_ImageRenderer; campos incompletos da busca permanecem abertos.


[Repetição ca7fe12/run39069765892](https://github.com/airtonbp19edu/Linuxit-PDF/actions/runs/39069765892)
aprovou190/190, zero falhas/erros/skips e campanha17/17. As três capturas agora
mostram resultados/contagens e destaque após a repintura; foram examinadas.
[Revisão dos hashes e imagens](../testes/resultados/sem-vm-continuacao-2026-10-17/linux-source-review.json).
A construção do0.1.6 foi retomada nesse commit; a versão publicada ainda é0.1.5.


## Flatpak 0.1.6 validado

[CI](https://github.com/airtonbp19edu/Linuxit-PDF/actions/runs/39069918299):190/190 em fonte/payload/sandbox, zero falhas/erros/skips.
90app/2803runtime/214ELF/149pacotes atribuídos; smoke 5/5 e launcher 3/3.
[Revisão](../testes/resultados/0.1.6/validation-review.json). Seis pacotes anteriores preservados.
