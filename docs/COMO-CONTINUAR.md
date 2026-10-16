# Como continuar o Linuxit PDF

Ponto de retomada salvo em **16/10/2026**, branch `main` do
[Linuxit-PDF](https://github.com/airtonbp19edu/Linuxit-PDF).
O próximo trabalho solicitado é **executar a etapa 10 — análise dinâmica**.

## O que já está salvo

O código, os relatórios técnicos, os testes e os indicadores estão no GitHub.
O último marco técnico antes deste guia é o commit
[`1d478a4`](https://github.com/airtonbp19edu/Linuxit-PDF/commit/1d478a48d6bd9507d7c2244702e2cdddf31c2cef).
Ele acrescentou 20 cenários, um gerador de corpus e uma configuração offline.
Os cinco testes de preparação passaram; o Foxit **não foi executado** nessa
rodada, e todos os cenários continuam `not_run`.

| Indicador | Estado preservado |
|---|---|
| Aplicativo publicado | 0.1.1, Flatpak `devel` |
| Progresso do roteiro | 43,33% |
| Entradas de funções examinadas | 194 |
| Paridade diferencial Foxit | 0/25 famílias identificadas |
| Etapa 10 | Preparação verificada; execução bloqueada |

Este quadro descreve o checkpoint `1d478a4`. Para o avanço posterior, consulte
as [notas datadas](../progresso/notas-continuidade.md); a rodada de consumidores
de impressão ampliou o catálogo para 200 entradas sem alterar o progresso
geral ou a paridade.

O bloqueio é o ambiente para observar o original: o computador usa Windows 11
Home Single Language, sem Sandbox disponível, WSL não instalado e sem VM
pronta. O [Windows Sandbox não suporta a edição Home](https://learn.microsoft.com/en-us/windows/security/application-security/application-isolation/windows-sandbox/).
O histórico Wine/QEMU carrega o Foxit, mas encerra antes da interface utilizável.

## O que você precisa preparar

O caminho recomendado é **uma VM Windows no VirtualBox**, mantendo seu Windows
Home atual. Não é necessário instalar Linux nessa VM para observar o Foxit;
o desenvolvimento do Linuxit continua com prioridade Linux.

1. **Conferir os recursos do computador.** Antes de criar a VM, verificar RAM,
   processador, espaço livre e virtualização disponível. O Windows 11 exige,
   entre outros requisitos, 4 GB de RAM, dois núcleos, armazenamento de 64 GB,
   UEFI compatível com Secure Boot e TPM 2.0. A máquina física também precisa
   de recursos para continuar funcionando enquanto a VM está aberta.
   [Requisitos Microsoft](https://learn.microsoft.com/en-us/windows/whats-new/windows-11-requirements).
2. **Baixar e instalar o VirtualBox pelo site oficial**, escolhendo o pacote
   para Windows hosts. O pacote básico é gratuito; o Extension Pack tem licença
   separada e não é necessário para esta campanha.
   [Download oficial](https://www.virtualbox.org/wiki/Downloads).
3. **Obter uma ISO oficial do Windows para a VM.** Usar uma licença apropriada
   ou uma avaliação oficial conforme os termos da Microsoft. A
   [avaliação Windows 11 Enterprise](https://www.microsoft.com/en-us/evalcenter/evaluate-windows-11-enterprise)
   tem prazo de 90 dias; a página informa requisitos de cadastro, ativação e
   conta. Não presumir que a avaliação terá instalação inteiramente offline.
   Instalar dentro da VM, preservando o Windows do computador físico.
4. **Criar a VM**, por exemplo com o nome `Linuxit-Foxit-Lab`, selecionando
   Windows 11 de 64 bits e a ISO obtida. Configurar recursos compatíveis com
   os requisitos, incluindo UEFI/TPM virtual quando necessário. Seguir o
   [assistente e as configurações oficiais do VirtualBox](https://docs.oracle.com/en/virtualization/virtualbox/7.2/user/working-with-vms.html).
   Concluir a instalação do sistema antes de introduzir ou executar o Foxit.
5. **Preparar o isolamento para os testes.** Com a VM desligada, desabilitar os
   adaptadores de rede, clipboard compartilhado, arrastar e soltar e acesso a
   dispositivos/impressoras do host. Usar perfil local de laboratório sem
   dados ou credenciais pessoais. Ainda não compartilhar discos, OneDrive ou
   o repositório inteiro. Se o instalador exigir conta ou houver problema de
   virtualização, informar o ponto em que parou antes de executar o original.
6. **Voltar a este projeto.** Informar o nome da VM, se o Windows iniciou e
   quais passos foram concluídos. Não é preciso executar os 20 casos sozinho;
   primeiro revisaremos a contenção e validaremos uma janela de controle.

Instalador, ISO, VM e recursos de virtualização ainda **não foram preparados**
por este guia. O `.wsb` gerado anteriormente serve para Windows Sandbox em host
compatível; ele não configura o VirtualBox e não deve ser usado como se fosse
uma VM pronta. A alternativa ao VirtualBox é usar Windows Pro/Enterprise/
Education compatível com Sandbox, seguindo os requisitos da Microsoft.

## Arquivos locais que você deve conservar

O GitHub não contém os binários Foxit, decompilações completas, banco Ghidra
ou resultados privados. Preserve uma cópia local destes materiais para não
precisar repetir trabalho:

- Pasta original: `A:\Programas\Foxit PDF Reader\Foxit PDF Reader` e material
  adicional em `A:\OneDrive\Airton - Profissional\Airton - Professor\Desenvolvimento\Foxit`.
- Pasta `analysis-local` deste checkout, principalmente o projeto em
  `headless/windows-print-01/project` e a campanha em `dynamic/windows-01`.
  Ela está ignorada pelo Git e não será recuperada apenas clonando o repositório.
- Ghidra e JDK já localizados em `A:\Programas`, conforme [RETOMADA.md](RETOMADA.md).

O executável de referência deve continuar com SHA-256
`90208c9e8da92c8e546b76c8f4a2f8fb999105d124e663bbea6744fb6bb6b3a6`.
Não atualizar ou substituir o Foxit usado como referência durante a campanha.

## O que retomar quando o ambiente estiver pronto

Primeiro confirmar o estado Git e ler [RETOMADA.md](RETOMADA.md),
[ETAPA-10.md](ETAPA-10.md) e [tarefas-pendentes.md](../progresso/tarefas-pendentes.md).
As rodadas seguintes ficam nas [notas datadas de continuidade](../progresso/notas-continuidade.md),
com horário de São Paulo, resultados, estado da publicação e próximos alvos.
Preservar as análises REA/Ghidra existentes.

Na VM offline, fornecer somente a pasta da referência e o corpus em leitura,
mais uma pasta nova de resultados em escrita; ou copiar esses materiais para
o disco do guest e retirar os compartilhamentos antes de executar. Não montar
perfis, contas ou outros projetos do host. Validar primeiro o controle de
interface e depois o início do Foxit. Só então executar os cenários e registrar
observações reais, conforme [cenarios-dinamicos.json](../testes/cenarios-dinamicos.json).

A campanha já gerada está em `analysis-local/dynamic/windows-01`. Para gerar
outra campanha, usar uma saída que ainda não exista, na raiz do checkout:

```powershell
python scripts/prepare_foxit_dynamic.py --reference 'A:\Programas\Foxit PDF Reader\Foxit PDF Reader' --output 'analysis-local/dynamic/windows-02'
```

Preparar entradas não inicia o original. Resultados, telas e logs completos
ficam locais; publicar apenas código próprio, metadados e conclusões examinadas.
Comparações no Linuxit exigirão ambiente Linux gráfico. Manter os pesos e
atualizar o progresso somente quando os critérios tiverem evidência real.

## Mensagem pronta para retomar em outro chat

> Retome o projeto https://github.com/airtonbp19edu/Linuxit-PDF pela branch main.
> Leia AGENTS.md, docs/COMO-CONTINUAR.md, docs/RETOMADA.md e docs/ETAPA-10.md.
> Leia também a última entrada de progresso/notas-continuidade.md para recuperar
> o avanço técnico e o estado Git mais recentes sem depender do chat anterior.
> O próximo trabalho é executar a etapa 10 em Windows isolado e offline.
> Já existem 20 cenários preparados; nenhum foi observado no Foxit nesta rodada.
> Preserve as análises REA/Ghidra e os indicadores: 43,33%, 194 entradas e
> paridade 0/25 famílias. Confira o estado atual do Git antes de editar e
> publique os novos marcos verificados. Vou informar a seguir o estado da VM
> e a localização dos materiais locais.
