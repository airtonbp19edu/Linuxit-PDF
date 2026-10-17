# Etapa 16 — geometria do painel lateral corrigida

O recorte de títulos e ícones foi corrigido no **0.1.3/devel**, em 17/10/2026.
O GtkPaned agora respeita o mínimo solicitado pelo painel lateral. A correção
passou em dez cenários de geometria e na suíte completa dos três ambientes.
Desktop real, acessibilidade, portais, impressão física e comparação Foxit
continuam pendentes; critérios amplos e pesos do roteiro permanecem parciais.

## Diagnóstico e critério de aprovação

A fonte anterior tinha mínimo 221px, divisor 158px e origem do painel x=-63:
o GTK conservava a largura do filho, deslocando-o para fora do corpo visível.
A captura confirmou o recorte. `shrink=False` impede esse encolhimento do espaço.

O primeiro diagnóstico (run 39040540957) comparava filhos apenas com um pai
também deslocado e retornava passed:true. Esse resultado era insuficiente e
não foi adotado como aprovação. O oráculo foi corrigido para conferir o corpo
visível e o mínimo do divisor, com guardas independentes de origem>=0 nos testes.
A rodada final executou tanto a fonte anterior 76d901e quanto a corrigida 64f7686
sob esse mesmo oráculo. Raw inicial preservado em
`analysis-local/sidebar-artifact-12104400034/` e notas datadas.

[`scripts/check_sidebar_layout.py`](../scripts/check_sidebar_layout.py) mede
cinco painéis em duas larguras solicitadas e salva capturas. `--observe-only`
não converte falhas em aprovação: o JSON preserva passed:false da baseline.
O código da aplicação só alterou a política de encolhimento do painel, além
da versão. Os testes estão em
[`tests/test_sidebar_layout_gtk.py`](../tests/test_sidebar_layout_gtk.py).

## Resultado conferido — 17/10/2026 às 11:35

O [run 39040860414](https://github.com/airtonbp19edu/Linuxit-PDF/actions/runs/39040860414) passou no commit `64f76865381b35b4f8204131ef547f210d5d09db`.
Com o mesmo oráculo corrigido e ambiente, a fonte anterior passou **0/10**
cenários e a corrigida passou **10/10**. [Antes](../testes/resultados/0.1.3/sidebar-before.json)
e [depois](../testes/resultados/0.1.3/sidebar-after.json) registram as medidas e hashes das imagens.

| Primeira página, janela 1180 | Antes | Depois |
|---|---:|---:|
| Mínimo do painel | 221 | 221 |
| Posição do divisor | 158 | 221 |
| Origem X do painel | -63 | 0 |
| Origem X do título | -18 | 45 |

Capturas antes/depois e lançamento normal examinadas: barra de ícones e títulos
ficam dentro da área visível após a correção. [Captura do pacote](../testes/resultados/0.1.3/linuxit-flatpak-0.1.3.png).
Os três novos métodos GTK passaram em cada suíte completa: painéis em duas
larguras, divisor/ocultar/mostrar/modo de leitura e nome longo de anexo.
Foram **114/114 testes em cada ambiente fonte, payload e sandbox**,
zero falhas/erros/skips. Smoke 5/5 e launcher 3/3 passaram. Os testes incluem
os controles do auditor acrescentados na etapa 21; não são contagens de funções.

Bundle [0.1.3/devel](../releases/LinuxitPDF-0.1.3-x86_64.flatpak),
35591904 bytes, SHA-256 `9aa8abf269136f84ff7cb1e6e5e990490245bec26b06979a76926030b10d3120`.
Fonte/payload: 83 arquivos iguais;
runtime 2803 arquivos atribuídos/149 pacotes.
Ver [revisão](../testes/resultados/0.1.3/validation-review.json) e [manifesto](../releases/manifest-0.1.3.json).
As três entregas anteriores foram preservadas.

Limite medido: pedido 760px resultou em janela mínima 924px por outros controles;
não se afirma suporte a 760px reais. A correção usa o mínimo calculado pelo GTK,
conforme a API [GtkPaned.pack1](https://docs.gtk.org/gtk3/method.Paned.pack1.html),
A largura acompanha o mínimo calculado. Desktop real, acessibilidade,
portais e impressão física continuam pendentes, assim como a VM do original.
Nenhuma nova observação Foxit, REA/Ghidra ou paridade diferencial. Pesos/status
do roteiro preservados: 43,33%, paridade 0/25 e cobertura global desconhecida.

Próximo passo sem VM: repetir os quatro subconjuntos Poppler no corpus
preservado da etapa 18; depois ampliar contratos/implementação e integrações.
Entrega técnica[`e030611`](https://github.com/airtonbp19edu/Linuxit-PDF/commit/e0306110ba0cd5f364e400aead2212343b80e263)
confirmada em 17/10/2026 às 11:41 (America/Sao_Paulo, UTC-03:00):
HEAD local/remoto iguais e árvore limpa. `git fsck --full` retornou0, e os
nove relatórios selados também conferem nos blobs Git. Esta nota será enviada
em commit próprio, com confirmação final por recibo externo.
