# Etapa 11 — interface, análise estática em paralelo à VM

Em 16/10/2026, nove entradas de interface foram descompiladas e examinadas
com Ghidra direto `-noanalysis`, usando seeds do REA. A análise pode avançar
enquanto o usuário prepara a VM, mas a etapa inteira continua dependente de
observação do original. Seus critérios e pesos foram preservados: **25% da
etapa 11 verificados**, roteiro geral **43,33%**, paridade **0/25 famílias**.

O catálogo passou de 200 para **209 entradas distintas (152 REA + 57 diretas
exclusivas)**. Os registros anteriores foram preservados. REA 6.5.0 e os dez
controles do provedor Ghidra foram reconferidos. Estas nove observações são
do backend direto, não de uma nova sessão MCP do REA.

## Condições e interações examinadas

| Contexto do recurso | Entrada | Observação estática |
|---|---|---|
| Abrir, menu 88 / ID 57601 | `0x803920` | Consulta visibilidade de uma janela e encaminha 0/1 ao objeto de atualização |
| Imprimir, menu 88 / ID 57607 | `0x861470` | Três caminhos enviam desabilitação; os demais não enviam habilitação explícita neste corpo |
| Próxima página, menu 88 / ID 1289 | `0x85d1a0` | Dois callbacks permitem enviar 1; outro caminho delega ao helper com ID 1289 |
| Ampliar, menu 88 / ID 1360 | `0x85ddd0` | Com view disponível, envia desabilitação quando o zoom finito é pelo menos 64 |
| Reduzir, menu 88 / ID 1362 | `0x85de30` | Com view disponível, envia desabilitação quando o zoom finito é no máximo 0,01 |
| Imprimir todas as abas, menu 645 / ID 1275 | `0x80eab0` | Envia 1 somente quando mais de um objeto passa por um predicado de tipo ainda parcial |
| Candidato compartilhado: IDs 7911/7913, diálogo 6359 | `0x1788db0` | Lê um checkbox e grava apenas o campo `+0x1d58`; associação ao texto das páginas permanece ambígua |
| Proximidade, diálogo 6359 / ID 8036 | `0x1788e10` | Lê checkbox e grava `+0x1d68`, sem implementar o algoritmo de busca nesse corpo |
| Destaque de todas as ocorrências, diálogo 6359 / ID 7921 | `0x1788d70` | Lê checkbox e grava `+0x1d70`, sem chamada explícita de busca ou repaint nesse corpo |

As tabelas de mensagem foram verificadas diretamente no executável para dez
associações contextuais e nove handlers distintos. A notificação `0xffffffff`
e o uso do slot virtual `+0` são compatíveis com atualização de habilitação
no padrão MFC; a classe efetivamente registrada em execução ainda não foi
confirmada. Uma mesma constante de ID em outro diálogo não estabelece a
mesma operação. Os endereços e suas lacunas constam nos metadados vinculados.

As constantes de zoom 64 e 0,01 foram lidas como float64 no PE; correspondem
a 6400% e 1% se aplicadas como fatores. Esses dois corpos **só desabilitam**
nos limites indicados. Não permitem inferir sozinhos a regra de habilitação
quando falta documento, em modos especiais ou na cadeia de atualização geral.
No comando de impressão, o tipo numérico 5, a máscara `0x20` e os helpers
precisam de contrato antes de receber nomes como permissão ou modo específico.
Para todas as abas, não equiparar objetos aceitos pelo predicado a toda aba
visível sem identificar a classe correspondente.

### Ambiguidade preservada na busca

O inventário associa os controles “Incluir marcadores” (7911) e “Incluir texto
das páginas” (7913) ao mesmo endereço `0x1788db0`. O corpo examinado envia
`BM_GETCHECK` para o HWND em `+0x780` e escreve **somente `+0x1d58`**.
O vínculo DDX anterior associa texto das páginas a `+0x1d60` e marcadores a
`+0x1d58`. As duas evidências foram preservadas; não se resolve essa diferença
inventando que um handler atualiza ambos os campos. É necessário confirmar
classe/instância e outros caminhos de troca de dados.

Proximidade e destaque também usam `BM_GETCHECK`, com seus campos já conhecidos.
Isso confirma armazenamento de estado. Não prova disponibilidade no Reader,
semântica do motor de busca ou efeito visual imediato.

### Estados declarados em recursos

Os metadados existentes de dez arquivos FX, com 135 widgets, foram cruzados
sem extrair novamente ou copiar os templates. Há três registros explícitos
de estado/foco e dez conexões declaradas de botões. Um checkbox de nível-base
é declarado desabilitado e marcado; um subnível é declarado desmarcado; um
controle de seleção de página tem foco forte. Aceitar/cancelar aparece em
conexões de cinco diálogos. O código pode alterar esses valores, e a presença
do template não comprova que o diálogo esteja acessível no Reader.

## Evidências e execução posterior

- [Nove descompilações: metadados e hashes](windows-evidence/foxit-rea/headless-cross-checks-ui-2026-10-16.json).
- [Tabelas, contextos e declarações dos recursos](windows-evidence/foxit-rea/ui-availability-windows-2026-10-16.json).
- [Condições, endereços de suporte e lacunas](windows-evidence/foxit-rea/ui-state-contracts-2026-10-16.json).
- [Verificações da rodada](../testes/resultados/etapa-11-estatica-windows-2026-10-16.json).
- [Dez cenários complementares de interface](../testes/cenarios-interface.json).

Os nove intervalos foram conferidos com Capstone: **242 instruções / 641
bytes**, com todos os endereços iguais às listagens Ghidra. PeFile confirmou
as importações `SendMessageW` e `IsWindowVisible`. O original permaneceu
intacto. Essas conferências não provam fronteiras completas, classes ativas,
assinaturas ou comportamento de execução.

Na VM offline descrita em [ETAPA-10.md](ETAPA-10.md), executar os cenários
UI01–UI10 junto dos cenários D01–D20 já preparados. Registrar cada variante
de documento, página, zoom, abas e busca separadamente: visibilidade,
habilitação, marcação, ação, efeito, contexto e evidência local. Os casos
continuam `not_run`, com observação `null`. O preparador de campanhas novas
inclui este roteiro e o plano de interface; a campanha antiga é preservada.

O helper `scripts/catalog_foxit_ui_availability.py` exige o hash esperado,
confere os registros `<6I` da tabela e recusa sobrescrever saídas. Seu mapa
mantém a classe como não verificada, mesmo após examinar o corpo da função.
Resultados completos e projeto ficam em `analysis-local/headless/windows-ui-01`,
ignorados pelo Git. Nenhuma execução do Foxit, mudança no comportamento do
Linuxit, teste diferencial ou novo Flatpak foi feito nesta rodada.

Próximos passos estáticos: investigar `0x859920`, `0x687ae0`, `0x5f5370` e
`0x48f10ef`; identificar a classe dos registros selecionados e esclarecer a
associação dos IDs 7911/7913. A conclusão do critério de interações permanece
pendente da observação na VM e da ampliação do inventário.
