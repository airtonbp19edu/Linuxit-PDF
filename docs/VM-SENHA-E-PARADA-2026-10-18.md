# Senha, fechamento e interrupção da VM

Continuação da rodada `vm-20261018-2020` em 18/10/2026. Testes interrompidos
pela regra solicitada pelo usuário: o relógio permaneceu em **21:24:14** em
observações repetidas, inclusive após dez segundos externos sem entrada.
Confirmação externa às 21:27:45 de São Paulo. O VirtualBox ainda informa running;
isso não comprova resposta do Windows. Causa raiz indeterminada. Não houve
pause/resume, reboot ou restauração nesta rodada. O Foxit já estava fechado e
o cabo de rede desligado. Usuário avisado; não insistir em entradas.

## Resultados efetivamente examinados

**D15:** `com-senha.pdf` foi aberto numa solicitação nova, com o campo inicialmente
vazio. A senha sintética correta foi fornecida na primeira tentativa dessa
abertura, sem rejeição anterior. O original abriu oito páginas, com indicação
SECURED; navegação 1 → 8 → 1 conferida. Cancelar e rejeitar senha errada permanecem
como evidências anteriores, sem apresentá-las como repetidas neste lote. Esta
variante pendente foi observada; a família completa de criptografia segue aberta.

**UI05, variante adicional:** com `busca-escopos.pdf` e `com-senha.pdf`, o menu da
aba ativa mostrou Print All Tabs habilitado. A ação abriu a confirmação Batch
Printing. A opção Don't ask again estava desmarcada e não foi alterada.
Escolher No retornou ao mesmo PDF, página1/8; não foi emitida ação de submissão
de impressão. O par de fixtures previsto usa `geometria.pdf`, não o PDF protegido;
essa combinação extra não aprova o par previsto, nenhuma/uma aba, outro contexto,
ID dinâmico do recurso ou saída de impressão. UI05 continua parcial.

**D20, fechamento deste contexto:** o X do título fechou a janela. A ausência do
processo foi examinada no Gerenciador de Tarefas, em ordem alfabética, e confirmada
como zero processos do Foxit pela manutenção posterior. Não houve encerramento
forçado. Esta rodada não enviou trabalho real de impressão; a espera anterior
em splwow64 e o contrato completo de encerramento continuam sem resolução.

O postflight limitado confirmou novamente os dez Inputs, hashes inalterados,
mesma identidade do executável, escrita negada em Reference/Input/Protocol e
contenção host/guest offline. O relatório completo já estava salvo em Results;
foi recuperado por manutenção SSH breve previamente autorizada, com Foxit ausente,
hash conferido e cabo desligado em finally. O Notepad desse postflight não recebeu
um segundo controle visual aprovado.

Comprovante sanitizado e hashes das 24 evidências:
[password-followup.json](../testes/resultados/vm-2026-10-18-2020/password-followup.json).
Capturas e relatórios completos permanecem privados em
`analysis-local/vm-20261018-2020/`; nenhum recurso do original foi publicado.

## Falhas do coletor separadas do comportamento do aplicativo

Foram identificados dois limites do canal Guest Properties: nomes com até63 bytes
úteis e até256 propriedades por guest. O cabeçalho oficial declara64 bytes
incluindo o terminador e256 entradas. [Fonte primária VirtualBox](https://raw.githubusercontent.com/VirtualBox/virtualbox/master/include/VBox/HostServices/GuestPropertySvc.h).
No VirtualBox7.2.20 instalado, um nome sintético de63 bytes foi aceito e um de64
foi rejeitado; a propriedade de controle foi removida após o teste.

Os nomes Count de after-search-inputs, after-search-collect e after-password-inputs
tinham64,65 e66 bytes. Partes numéricas mais curtas podiam existir sem recibo.
Também foram enumeradas256 propriedades; o último relatório ficou cortado.
O coletor2020 foi encontrado Ready com LastTaskResult1, não como stop concluído.
Não enviar comandos esperando resposta desse coletor. A recuperação completa
da coleta anterior, por17 partes idênticas em duas leituras, também foi preservada.

Foram arquivadas as propriedades antigas e removidas somente151 entradas Result
dos coletores1710/1940 já encerrados, em dois lotes de55 e96. Arquivos do guest,
configuração da VM, propriedades do sistema e relatórios locais foram preservados.
Essas falhas explicam limitações do observador; não determinam a causa da parada
posterior do relógio nem uma falha funcional do Foxit.

Correções próprias:

- `scripts/foxit_vm_probe.ps1` rejeita recibo longo antes de qualquer comando e
  exige reserva de64 propriedades para resposta, mais duas para Host/Command.
- `scripts/guest_foxit_probe.ps1` confere nome, resposta dentro da reserva e código
  de saída ao publicar Count; o relatório completo permanece no disco.

Os dois scripts passaram no parser PowerShell. Foram exercitados a rejeição de
ID longo, os limites63/64 no VirtualBox instalado e a rejeição por capacidade sem
alterar Command. **A integração do coletor corrigido no guest não foi executada**:
a parada foi constatada antes da instalação. O guest conserva o script anterior,
hash8a8b4ae003c1ff6c8cbaa6fc7139e7497e6dd14ec1fe18e69f86a849fa053e13.
O preparador privado `analysis-local/prepare_probe_2130.ps1` foi escrito, mas não
executado; tarefa/RunId2130 não criados. Ele exige revisão visual recente antes
da manutenção e não inicia o Foxit.

## Retomada

Depois que a VM voltar a responder, conferir relógio, ausência do original e
isolamento. Usar novo RunId, instalar o script corrigido com Foxit fechado pela
manutenção já autorizada, desligar o cabo e validar recibos curtos como pf/col/end
em tarefa interativa limitada, primeiro sem executar o original. A reserva é
por resposta: arquivar resultados de coletores encerrados antes de esgotá-la.
Para executar o original depois, fazer novos preflight e controle visual.

Prosseguir então com destinos D07/D10, cancelamento ativo D12, saída de imposição
D18 e variantes restantes da interface. App/Flatpak não mudaram; não houve nova
suíte403/403 nem rebuild. O consolidado C18 continua12 medições iguais/cinco
inconclusivas, sem nova comparação neste lote. Os19 critérios, pesos45,13%,
paridade0/25 e50 planos completos de aceitação permanecem abertos nos limites
já documentados; nenhuma porcentagem de recodificação foi inferida.
