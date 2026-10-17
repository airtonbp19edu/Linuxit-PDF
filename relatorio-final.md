# Relatório de desenvolvimento — Linuxit PDF0.1.6

Fonte/pacote 0.1.6:190/190 em cada suíte fonte/payload/sandbox, zero falhas/erros/
skips, smoke 5/5 e launcher 3/3.32 controles portáveis e seis GTK novos.
Busca em anexos UTF-8/PDF com omissões explícitas, coringas/proximidade ordenada
e índice JSON persistente de PDFs escolhidos, com exclusão de fontes alteradas.
[Contrato](docs/BUSCA-COLECOES.md), [revisão](testes/resultados/0.1.6/validation-review.json)
e [manifesto](releases/manifest-0.1.6.json).

Catálogo 248(152REA+96diretas); oito entradas novas/889 instruções/3.223 bytes.
RTTI CPDF_ImageRenderer eCReflowViewerEx/IPDFViewer confirmados; tipos, fluxos
eIDs restantes abertos.28 módulos/26 interfaces; 19 subconjuntos/seis propostas.
Roteiro 43,33%, paridade 0/25,50 planos completos not_run. Ainda há trabalho sem VM.

[Retomada](docs/RETOMADA.md) e [notas datadas](progresso/notas-continuidade.md)
registram confirmação remota/auditoria e próximos alvos. Não é entrega estável
nem reconstrução completa; original continua sem execução funcional observada.

## Relatório histórico preservado — marco0.1.1

# Relatório do marco Linuxit PDF 0.1.1 — projeto em andamento

Foi aprofundada a análise de busca e impressão, preparado um runtime Windows
x86 emulado e entregue um novo Flatpak com controle de destaque e correção
do encerramento de tarefas da busca. A reconstrução integral continua aberta.

## Engenharia reversa

O catálogo passou de 131 para **191 entradas distintas examinadas**: 152 pelo
REA/Ghidra e 39 adicionais pelo backend direto. Foram preservadas 31 novas
observações MCP, incluindo uma entrada já examinada. Um resultado excedeu o
limite de resposta e foi recuperado integralmente do export; erros e perfis
foram conservados. Não se contam repetições como novas funções.

A investigação confirmou bits de caixa/palavra inteira, parte do argumento
de 24 bytes usado na busca por índice e consumidores de cancelamento. Na
impressão, foram identificados construtores, chamadas StartDoc/StartPage e
leitura de DPI, dimensões físicas e margens. A geometria e os motores completos
ainda são parciais. Detalhes em [busca/impressão](docs/REA-BUSCA-IMPRESSAO.md).

## Observação do original

O controle Windows x86 passou sob Wine 10/QEMU-i386 em contenção offline. O
Foxit chegou a carregar, mas terminou após CInvalidArgException, antes de uma
interface utilizável. A causa inicial permanece em aberto. Nenhuma busca ou
impressão do original foi validada; nenhum binário foi modificado para
contornar esse encerramento. Ver [evidência dinâmica](docs/relatorio-dinamico.md).

## Implementação e testes

A opção **Destacar todas as ocorrências** permite alternar entre todos os
destaques e apenas o selecionado, mantendo a pesquisa e a navegação. Também
foram cancelados timers e navegação pendentes ao fechar a janela, corrigindo
um erro de acesso a controles GTK já destruídos. O código é independente e
continua baseado no Winux/Print&View próprio, com licença MIT preservada.

- Fonte: **37/37 testes aprovados**, sem falhas, erros ou ignorados.
- Payload: os mesmos **37/37 testes aprovados**.
- Flatpak instalado: **5/5 verificações** dentro do sandbox real.
- Launcher normal: abriu o PDF sintético e sua janela foi capturada.
- Os 81 arquivos do aplicativo no payload coincidem com a fonte por SHA-256.

As tentativas anteriores ficaram registradas: o Python 3.12 do PATH não
carregava Cairo do sistema 3.13; depois, 35 casos passaram, mas um callback GTK
gerou uma exceção fora do runner. Essa falha foi corrigida e ganhou regressões.
O [histórico de validação](testes/resultados/0.1.1/validation-history.json)
distingue os resultados finais dos intermediários.

## Distribuição

[LinuxitPDF-0.1.1-x86_64.flatpak](releases/LinuxitPDF-0.1.1-x86_64.flatpak),
41.215.208 bytes. SHA-256:

```text
58de72eff22ac9b42ce2792daf8877d9f5a846c5f8009a22ac036747ea130371
```

ID `io.github.airtonbp19edu.LinuxitPDF`, branch `devel`, Freedesktop Platform
25.08. O bundle não recebe assinatura digital. A instalação e as limitações
estão em [instalação](docs/instalacao.md) e no [manifesto](releases/manifest.json).
A versão anterior foi preservada. Não foram gerados DEB ou EXE neste marco.

## Indicadores e continuidade

O roteiro permanece em **43,33%**, sem mudança dos pesos. A cobertura global
de engenharia reversa é **indeterminada**: os quatro módulos entre 141 PE são
uma medida parcial por módulo, não uma porcentagem de funções recuperadas.
A paridade comprovada permanece em **0/25 famílias identificadas**. Os testes
próprios não substituem testes diferenciais; impressão física e Windows nativo
continuam pendentes.

O destino é [Linuxit-PDF](https://github.com/airtonbp19edu/Linuxit-PDF), branch
`main`. A confirmação remota fica no histórico e em
`progresso/sincronizacao-git.json`; o comprovante de HEAD pode ser gerado fora
da árvore com `scripts/verify_git_sync.py`. Arquivos proprietários, decompilações,
bases Ghidra e protótipos intermediários permanecem fora do Git.

Próximos alvos: determinar a causa da exceção inicial do Foxit, completar os
consumidores dos campos ainda desconhecidos da busca e seguir as transformações
de impressão antes de afirmar equivalência. O [marco 0.1.0](docs/marcos/0.1.0.md)
foi mantido como histórico.
