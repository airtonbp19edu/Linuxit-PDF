# Execução das frentes sem VM — 17/10/2026

Pedido: avançar todas as etapas restantes que possam ser verificadas sem VM.
Este registro acompanha os lotes efetivamente executados. A observação Foxit,
a fase A completa e a paridade continuam abertas; IA permanece excluída.

## Campanha Linux com o corpus preservado

O [run 39057011186](https://github.com/airtonbp19edu/Linuxit-PDF/actions/runs/39057011186),
fonte `b8125e23fa699c40cf1cf69b7e91f3493cbb73bd`, aprovou **17/17 subconjuntos**,
incluindo os quatro antes bloqueados por Poppler. Os oito hashes de fixtures e
os 17 hashes de protocolo coincidem com a etapa 18. Nenhum PDF foi regenerado.
São **119/119 testes da fonte Linux**, zero falhas/erros/skips, e smoke GTK 5/5.
Essa execução antecede as alterações da fonte 0.1.4 descritas abaixo.

O [manifesto do corpus](../testes/fixtures/campaign18/manifest.json) preserva
somente dados sintéticos próprios, sem arquivos Foxit. Cinco controles recusam
alterações de bytes/manifesto e ausência de fixture. O arquivo `controle.txt`
conserva seus CRLF originais para não mudar o hash histórico.

Evidência: [campanha](../testes/resultados/sem-vm-2026-10-17/preserved-campaign.json),
[revisão dos hashes](../testes/resultados/sem-vm-2026-10-17/campaign-review.json)
e [suíte Linux](../testes/resultados/sem-vm-2026-10-17/source-intermediate.json).
O kit privado da VM permanece intacto. Nenhuma observação original foi importada;
os 20 casos dinâmicos e 50 cenários completos não foram convertidos em aprovados.

## Continuação estática: 14 alvos examinados

Ghidra 12.1.4 direto `-noanalysis`, JDK 21.0.12.1 e script de seeds do REA.
CLI REA 6.5.0 conferido; estas observações pertencem ao backend direto,
sem atribuí-las a uma sessão MCP. Capstone 5.0.6/pefile 2024.8.26 confirmaram
**1.075 instruções/3.372 bytes** nos intervalos das 14 entradas.

| Entrada | Corpo | Contrato parcial examinado |
|---|---:|---|
| `0x166d050` | 30 bytes | Multiplica um inteiro por escala float32, divide por 72,0 float32 e converte com `CVTTSS2SI`; truncamento, sem regra de arredondamento visual presumida. |
| `0x165f5d0` | 69 bytes | Dimensões inteiras em `+0x144/+0x148`, escala `+0x168` e conversão truncada antes de `0x165f620`. Unidades e contexto ainda parciais. |
| `0x16678c0/8d0/8e0/8f0` | 7 bytes cada | Leem floats em `+0x16c/+0x170/+0x178/+0x174`, respectivamente. Nomes visuais/orientação não estabelecidos. |
| `0x1664c00` | 1.157 bytes | Caminho com blocos e sobras, fator inteiro derivado de `+0x8c`/300, dimensões limitadas e chamadas a `0x1665090`; consultas cooperativas a `+0x14`. Tipos de buffers e saída permanecem parciais. |
| `0x1665a30` | 1.508 bytes | Monta opções, transformação e objetos auxiliares; inicia processamento e consulta estados 2/3 ou cancelamento `+0x14`. Enumera extensões em `+0x5c`. Flags, classes e saída final ainda incompletas. |
| `0x2d226d0` | 198 bytes | Aloca 0x58 bytes, instala vtable `0x619fa3c` e inicializa transformação/defaults. Construção estática, sem provar a classe nem nomear o objeto como renderer. |
| `0x1b5baf0` | 104 bytes | Ajusta o objeto em +0x48 e encaminha a um helper que insere nó/dado em estrutura encadeada. **Não é, por si, prova de desenho ou submissão à impressora.** |
| `0x859920` | 150 bytes | Predicado combina quantidade em objeto indireto `+0x220` com posição obtida por chamada virtual; dois pares de IDs escolhem testes de limite anterior/posterior. Classe ativa e rótulos ainda não demonstrados. |
| `0x687ae0` | 10 bytes | Retorna diferença entre `+0x4c` e `+0x48`, deslocada em dois bits; sugere contagem de elementos de quatro bytes, sem provar quantidade de abas visíveis. |
| `0x5f5370` | 29 bytes | Se interface `+0x8c` existe, chama slot virtual `+0x110` com argumento 4; caso contrário retorna zero. Capacidade/contexto ainda sem nome confirmado. |
| `0x48f10ef` | 89 bytes | Obtém descritor por chamada virtual e encaminha a helper que percorre `+0x10` comparando ponteiros. Corpo Ghidra inclui intervalo do helper anterior; assinatura inferida tem entradas de registrador não modeladas. |

O corpo de `0x1b5baf0` inclui o destino de salto `0x1f21ff0`; o de `0x48f10ef`
inclui `0x48f10c5`. Intervalos de corpo não são novas funções únicas. Essa
observação refina a interpretação dos consumidores anteriores e não transforma
inserção em lista em saída gráfica observada. Os IDs 7911/7913 continuam ambíguos.

Catálogo: **223 entradas**, 152 REA e 71 exclusivas diretas. Não há denominador
global de funções; roteiro e paridade não aumentam por contagem de descompilações.
Ver [metadados da rodada](windows-evidence/foxit-rea/headless-cross-checks-no-vm-2026-10-17.json).
Projeto, pseudocódigo, montagem e conferência completa permanecem em
`analysis-local/headless/no-vm-2026-10-17/`. O original não foi executado.

## Implementação atual em desenvolvimento

A fonte **0.1.4** acrescenta listagem/extração de árvores `/Kids` aninhadas e
anexos de anotação `/FileAttachment`. Ordem: entradas do catálogo na ordem da
árvore, depois referências de anotação por página. Entradas com mesmo nome ou
referenciadas em mais de um lugar conservam índices distintos. A listagem inclui
origem e página (base zero); a UI mostra a página da anotação em base um.

São recusados ciclos/nós repetidos, mistura de `/Kids` e `/Names`, pares inválidos,
profundidade acima de 64 e mais de 4.000 nós. O limite de 1.000 anexos se aplica
ao conjunto. Nome seguro, hash da listagem, rechecagem do original e criação
exclusiva continuam obrigatórios. Listagem não decodifica payloads; o limite
de 64 MiB continua sendo verificado **depois** da decodificação, sem garantia
de teto de memória de parsing/descompressão.

Sete métodos portáveis novos passaram, assim como 14 regressões do backend e
14 do controlador. O novo método GTK cobre árvore/anotação e extração pelo
worker real; **validação Linux dessa nova fonte ainda em execução/preparação**.
Portfólios, senha não vazia e demais famílias permanecem abertos.
A entrega publicada continua 0.1.3 até construir/testar um pacote novo.

## Continuidade

- Etapas 03/05/07/08/09/11: lote estático examinado; fechar tipos/consumidores,
  relações de classes e contratos requer novos alvos dirigidos, sem inventar
  disponibilidade ou comportamento. Seguir `0x165f620`, `0x165f970`,
  `0x166a5b0`, `0x1665090`, `0x1b93280` e os consumidores da vtable `0x619fa3c`.
- Etapas 12/15/16: atualizar os contratos da extensão de anexos e executar o
  novo cenário GTK; ampliar cada família conforme contratos verificáveis.
- Etapas 17/20/21: validar fonte 0.1.4, construir o novo marco Flatpak,
  conferir payload/sandbox/licenças e publicar com confirmação remota.
- Etapa 18: os quatro subconjuntos Poppler desta campanha estão resolvidos.
  Repetir a campanha na nova fonte; comparação com o Foxit continua dependendo
  de contenção offline utilizável.
- Desktop real, portais, AT-SPI/impressora e serviços externos exigem seus
  respectivos ambientes, dispositivos ou contas; ausência de VM não os valida.
- Etapa 01: detalhes de regras remotas seguem recusados por HTTP 403 do plano.
  Não alterar faturamento, visibilidade ou proteções para obter esse acesso.

Os 21 critérios amplos continuam abertos nos estados originais. Os novos lotes
fecham pendências delimitadas; não representam encerramento de todas as etapas.
