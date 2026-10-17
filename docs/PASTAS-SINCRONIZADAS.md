# Pastas sincronizadas — fluxo local da fonte 0.1.9

Decisão do usuário em 17/10/2026: aplicar o uso de pastas sincronizadas e
informar quais partes dependem de VM. APIs de provedores, autenticação no
Linuxit, upload automático e colaboração remota continuam adiados.

## Uso

1. Configure a sincronização em um cliente externo de sua escolha.
2. No Linuxit, use **Arquivo → Escolher pasta sincronizada…** e selecione a
   pasta local. A seleção é explícita; o aplicativo não detecta contas ou pastas.
3. Use **Abrir PDF da pasta sincronizada…**. Abrir/salvar cópias, criar PDF de
   imagens e ferramentas de senha passam a oferecer essa pasta como preferência.
4. Salve com um nome novo. O Linuxit confirma **salvo localmente**; o cliente
   externo é responsável pelo envio, autenticação, conflitos e confirmação remota.
5. **Esquecer pasta sincronizada** remove a preferência sem apagar arquivos ou
   alterar a configuração do cliente externo.

A pasta preferida e as últimas pastas de abrir/salvar ficam em
`$XDG_CONFIG_HOME/linuxit-pdf/folders.json`, separadas do tema. Só caminhos
locais são persistidos; não há senha/token/conta ou transmissão. Pasta ausente,
configuração inválida ou permissão revogada exige escolher novamente ou usar
outra pasta. Uma preferência persistida não é uma permissão permanente do portal.

## Gravação e limites

Salvar cópia simples agora usa worker, limite de 512 MiB, identidade da fonte
e destino inexistente; a operação antiga que podia sobrescrever o destino foi
substituída por cópia exclusiva. Ao detectar alteração externa da fonte aberta,
as ações de copiar/editar pedem reabrir o documento. Isso não é monitoramento
contínuo da pasta, merge de alterações ou sincronização bidirecional.

Cópias simples, editadas, criadas de imagens e protegidas/autorizadas por senha
são preparadas e verificadas antes de publicar o nome final, sem substituir
arquivo existente, inclusive se ele surgir durante a gravação. Em Linux usa-se
renameat2(RENAME_NOREPLACE), com link exclusivo como alternativa quando possível;
Windows usa rename sem substituição. Sistema de arquivos sem operação segura
é recusado. O conteúdo é fechado e fsync executado antes da publicação.

O nome final aparece completo; **temporários `.linuxit-*` ainda podem ser
vistos pelo sincronizador**. Se necessário, configure a exclusão desse padrão no
cliente. O Linuxit não muda filtros/configurações externas. Interrupção forçada
pode deixar temporário ou saída já concluída. Não há transação remota,
apagamento seguro ou garantia de persistência após falha física do dispositivo.
Outras saídas, como exportação PNG/impressão, não recebem essa garantia por esta
rodada. O original e arquivos de destino existentes permanecem preservados.

O seletor de pasta usa Gtk.FileChooserNative, permitindo integração com portais.
Os seletores de arquivos usam a pasta/atalho concedidos. A validação de interação
com um portal real e persistência de concessões em desktop continua separada;
respostas simuladas nos testes GTK não comprovam o backend do sistema.
O Flatpak não recebe uma permissão global nova. Acesso a uma pasta fora de HOME
pode exigir concessão pelo desktop ou permissão explícita para aquela pasta.

## Validação

15 testes portáveis novos: preferências, Unicode, fallback, recusa de arquivo
alterado, publicação completa/exclusiva, falhas e worker real. Oito métodos GTK
preparam seletores reais, abrem/renderizam e salvam uma cópia com worker; a
resposta nativa de seleção/cancelamento é simulada no limite do desktop.
Regressões portáveis:20 segurança,17 criação e16 edição passaram nesta rodada.
Relatórios completos Linux/Flatpak serão ligados após execução e exame.

O builder possui dois controles adicionais com pasta sintética fora de HOME:
sem concessão, deve ser inacessível; com concessão específica, ler/copiar/reabrir
e recusar sobrescrita. Esses controles não usam nuvem ou cliente real nem afirmam
que um diálogo de portal foi testado. Nenhum original Foxit é executado.

## Dependências da VM e de outros ambientes

| Frente | Precisa da VM offline do Foxit? | O que falta |
|---|---|---|
|Pastas sincronizadas no Linuxit|Não|Testar um cliente real e desktop Linux, envio/conflitos externos e portais reais.|
|Código próprio, testes Linux e Flatpak|Não|Ampliar contratos/funcionalidades e validar em seus ambientes.|
|Análise estática REA/Ghidra|Não|Rastrear tipos, chamadas e estados; evidência estática não observa UI.|
|Etapa10: referência dinâmica|Sim|Executar o original em contenção offline e observar D01–D20.|
|Etapa11: interações do original|Sim, para a parte dinâmica|Observar UI01–UI10 e resolver disponibilidade/estados reais.|
|Etapa18: comparação diferencial|Sim|Capturar resultados do original no corpus/protocolo preservados e comparar.|
|Etapa19: divergências com o original|Sim, para fechar equivalência|Reproduzir diferenças e validar correções; bugs próprios podem ser corrigidos sem VM.|
|Desktop/AT-SPI/portais/impressora física|Não é a VM do Foxit|Desktop, tecnologia assistiva e equipamento reais.|
|Serviços remotos reais do Foxit|VM offline sozinha não basta|Autorização e ambiente de rede/contas específicos; não conectar a VM offline por esta tarefa.|

Os 20 cenários dinâmicos, dez de UI e 50 planos completos continuam sem
observação/execução integral. Roteiro43,33%,paridade0/25 e pesos preservados.
Pacote publicado anterior:0.1.8; fonte0.1.9 em desenvolvimento nesta preparação.
