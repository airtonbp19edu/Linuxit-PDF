# Relatório de desenvolvimento — Linuxit PDF 0.1.9

[Pastas sincronizadas locais](docs/PASTAS-SINCRONIZADAS.md): seleção explícita,
preferência/últimas pastas e cópias completas sem sobrescrita. Cliente externo
gerencia envio/conflitos; APIs remotas continuam adiadas. PDF alterado externamente
exige reabrir antes de copiar/editar. 37 módulos/49 interfaces,23 subconjuntos/2 propostas.

Fonte/payload/sandbox 290/290 cada, zero falhas/erros/skips; 15 portáveis e oito GTK novos.
Pasta fora HOME inacessível sem concessão e utilizável com concessão específica.
99 arquivos da aplicação, 2.804 de dependências, 215 ELF e 150 avisos;
smoke 5/5, launcher 3/3. Dez bundles ao todo,
incluindo nove anteriores preservados. Publicação/auditoria nas notas datadas.
[Revisão](testes/resultados/0.1.9/validation-review.json).

Sem teste de cliente real ou interação de portal real; esses testes dependem de
desktop Linux, não da VM Foxit. A VM offline é necessária para referência
da etapa 10, UI original da 11 e comparações das etapas 18/19. Guia contém a tabela completa.
Catálogo 259, roteiro 43,33%, paridade 0/25; original não executado nesta rodada.
Ainda há operações locais/estática e validação externa a concluir.

[Retomada](docs/RETOMADA.md) e [notas](progresso/notas-continuidade.md).

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
