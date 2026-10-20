# Como interpretar este levantamento

Este levantamento foi solicitado para mostrar, sem reduzir a uma resposta curta, tudo que está registrado como realizado, parcialmente realizado, pendente, adiado ou desconhecido no Linuxit PDF. O documento reúne o estado atual e preserva os registros anteriores com sua identificação histórica. A referência da fotografia é o commit `b2bb82114b58468b75f44fd1b77cfb2f354ba25e`, confirmado localmente e no GitHub antes da elaboração deste relatório.

“Tudo” aqui significa a totalidade do inventário conhecido e dos documentos técnicos versionados naquela revisão. O universo integral do Foxit ainda não foi delimitado. Não seria correto afirmar que conseguimos listar comportamentos que ainda não foram descobertos. Os originais proprietários, projetos completos de Ghidra e pseudocódigo mantidos fora do Git continuam em seus locais próprios; eles não foram incorporados a este relatório ou ao aplicativo. O catálogo publicável identifica entradas, evidências e limitações, sem redistribuir o código do Foxit.

O relatório contém as 25 famílias, as 111 operações do inventário provisório, as 21 etapas e seus 58 critérios, os 19 critérios ainda abertos, os 50 planos iniciais de aceitação, os pacotes P01–P10, os lotes B01–B10, a sequência S01–S12, os 75 módulos próprios documentados, as 60 interfaces, as 329 entradas do catálogo estático, os 564 métodos de teste da entrega atual, os 17 manifestos de versões de 0.1.0 a 0.1.16, a cronologia Git disponível e os documentos históricos integrais. Os anexos mantêm os dados estruturados completos para permitir conferência por outra IA.

## Recompilar, reconstruir e comprovar equivalência são trabalhos diferentes

O projeto já gera um aplicativo executável e um Flatpak instalável. A versão de desenvolvimento 0.1.16 foi construída, instalada e auditada. Portanto, não estamos esperando a conclusão de toda a engenharia reversa para finalmente apertar um botão de compilação. Há entregas utilizáveis anteriores e um pacote atual publicado.

O código próprio principal usa Python e GTK. O processo de build organiza o código e as bibliotecas necessárias, confere as dependências e gera o pacote Flatpak. Poppler, pypdf, Pango, Cairo, GStreamer, OpenSSL, Tesseract e outras dependências possuem funções próprias nessa implementação. Isso não é uma recompilação do código-fonte C++ original do Foxit: o projeto não recebeu esse código-fonte. A investigação de binários serve para esclarecer contratos e comportamentos; a implementação é independente, com as licenças e a base reaproveitada identificadas.

A reconstrução integral pretendida exige completar as funcionalidades aprovadas, os tratamentos de erro, estados, persistência, interface e integrações. A comprovação de equivalência exige ainda observar os comportamentos correspondentes no Foxit, executar as mesmas situações em ambos e examinar as diferenças. Uma entrega funcional pode estar pronta para teste antes de a equivalência integral estar demonstrada.

Se “até a recompilação” significa obter um pacote para instalar no Linux, esse ponto já foi alcançado. Se significa terminar toda a reconstrução e entregar uma versão final com o escopo integral comprovado, ainda há implementação, especificação, observação e aceitação a concluir. Este relatório mostra as duas coisas separadamente.

## O que os estados significam

- **Realizado no recorte descrito:** existe uma entrega concreta e uma evidência compatível com aquele recorte. Isso não encerra automaticamente uma família inteira.
- **Código próprio presente:** há implementação identificada por arquivo e símbolo. O nome de uma operação pode representar uma necessidade mais ampla que a parte implementada.
- **Validado por testes próprios:** o Linuxit passou nas situações executadas. Os testes não provam comportamento universal para qualquer PDF e não substituem o Foxit como referência.
- **Observado no original:** o Foxit foi executado no ambiente offline documentado e houve registro do que foi possível observar. Observação parcial não é uma família integralmente aceita.
- **Comparado:** uma medição delimitada das duas aplicações foi confrontada. Igualdade nessa medição não prova que toda a operação ou família seja equivalente.
- **Parcial:** existe trabalho preservado, mas alguma obrigação do contrato continua aberta. O relatório identifica o que já existe e a parte ainda ausente.
- **Pendente ou a caracterizar:** falta implementação, falta definir o contrato ou falta confirmar a disponibilidade no Reader de referência. Essas situações não devem ser confundidas.
- **Adiado pelo usuário:** nuvem direta continua no inventário, mas não deve ser implementada agora. Pastas sincronizadas por um cliente externo são um fluxo local distinto.
- **Excluído:** o assistente de IA e os recursos generativos do Foxit não fazem parte da reconstrução solicitada.
- **Desconhecido / `null`:** o dado não foi comprovado. Não significa zero, aprovado ou irrelevante.

O software é derivado de uma base própria MIT Winux/Print&View, com origem registrada. Abrir, renderizar, navegar, apresentar e preparar imposição já tinham componentes reaproveitados. Isso é trabalho útil preservado, mas não deve ser contabilizado como recuperação nova de código do Foxit. Dependências abertas também não são subsistemas proprietários reconstruídos.

# Por que ainda está demorando

## 1. O objetivo integral continua maior que o inventário conhecido

As 25 famílias são categorias amplas: formulários, impressão, assinaturas e acessibilidade, por exemplo, contêm muitas operações e variantes. As 111 operações são uma decomposição provisória, não um catálogo definitivo de todas as funções do Foxit. Há 97 operações com algum código próprio identificado, 11 classificadas como pendentes ou ainda em caracterização e três operações de nuvem adiadas. Dividir 97 por 111 não produz uma porcentagem honesta de reconstrução: uma operação simples e um subsistema como XFA ou renderização 3D têm dimensões muito diferentes, e o inventário ainda pode crescer.

O catálogo estático de 329 entradas também não é uma lista de 329 funções já reescritas. Ele registra entradas examinadas com graus diferentes de entendimento, tipos ainda inferidos e assinaturas incompletas. O denominador de funções relevantes do original permanece desconhecido. Terminar uma fila de sementes de Ghidra não encerra a análise de todos os fluxos do aplicativo.

Há ainda comportamentos cuja disponibilidade no Foxit Reader precisa ser distinguida da disponibilidade no Foxit Editor ou de rótulos presentes em plugins e recursos. Não se deve transformar uma string ou um template em uma obrigação funcional supostamente comprovada. Edição do texto e das imagens originais das páginas, redação definitiva e conversões universais, por exemplo, não são funcionalidades completas da implementação atual; sua adoção como obrigação do Reader precisa de contrato e confirmação, em vez de expansão automática do escopo.

## 2. O checklist antigo quase não reage às entregas parciais

O índice histórico atual é 45,13%, com 39 critérios concluídos e 19 abertos. Ele resulta de 21 etapas ponderadas e só pontua um critério quando seu estado é `done`. Estados parciais pontuam zero nesse índice. Há critérios muito abrangentes, como “Todas as demais famílias implementadas e testadas” e “Demais interações e integrações funcionais”. Muitas entregas locais podem acontecer sem que esses critérios inteiros fechem.

Por isso, a percepção de permanecer sempre nos mesmos 43% tinha uma causa real na forma de medir. Houve crescimento de funcionalidades e de testes, mas o indicador era inadequado para expressar esse crescimento. A revisão do método está documentada. O aumento posterior para 45,13% decorreu de critérios específicos, inclusive validação do ambiente do original; ele não significa que somente 45,13% do código esteja escrito nem que o restante seja 54,87% de trabalho mensurável.

O erro de comunicação foi apresentar esse índice com destaque em respostas sobre a quantidade de recodificação. O relatório atual não substitui esse erro por um número otimista inventado. A porcentagem global permanece desconhecida. Para obter uma porcentagem operacional útil, seria necessário fechar um escopo finito, atribuir pesos e definir critérios de aceitação por operação antes de medir, preservando a série histórica anterior.

## 3. Foram criados vários níveis de etapas, que não são equivalentes

Existem as 21 etapas originais ponderadas, os pacotes P01–P10 de continuidade, os lotes B01–B10, a sequência das 25 famílias, as tarefas S01–S12 de execução sem VM, os casos D01–D20, os casos UI01–UI10 e os planos de aceitação com IDs S12. Essas numerações pertencem a registros diferentes. “S12” pode designar o pacote de entrega da sequência sem VM ou o prefixo dos planos de aceitação; o relatório mantém os dois contextos explícitos.

Percorrer todos os lotes, implementar um recorte de cada família ou concluir uma nova versão não equivale a encerrar as 21 etapas. O arquivo dos lotes de 25 itens registra expressamente que as famílias integrais continuam abertas. A tarefa S12 de entrega da 0.1.16 foi concluída no recorte do pacote, enquanto S11 e os 50 planos completos de aceitação ainda não foram encerrados.

Essa fragmentação dificulta entender o ponto final e favorece a impressão de que uma nova etapa apenas substitui a anterior. Uma parte do trabalho de gestão que falta é reconciliar essas camadas em uma fila de obrigações verificáveis, sem reabrir o que já foi aceito e sem converter “lote percorrido” em “família concluída”. O relatório faz o cruzamento documental, mas sua criação, por si só, não executa as aceitações técnicas.

## 4. Há documentação desatualizada dentro de registros ainda consultados

O estado mais recente está nas evidências da 0.1.16, nas notas finais e no registro de execução sem VM. Porém, alguns campos antigos da especificação funcional e do backlog continuam descrevendo versões anteriores. Há textos dizendo que stemming, voz, alternância de camadas, cálculos de formulário ou combo editável ainda estão pendentes, embora recortes dessas funções tenham sido implementados e testados posteriormente. Alguns `next_action` ainda falam em terminar P02 e retomam relógios anteriores, apesar de P02 ter sido validado e o teste atual ter parado depois, em outra rodada.

Essas divergências não significam que as funções desapareceram do aplicativo. Significam que a atualização documental foi desigual: notas novas foram acrescentadas, mas nem todos os campos normativos antigos foram reconciliados. Isso é retrabalho evitável e torna uma retomada por outra IA mais lenta e menos segura. O relatório identifica os casos e apresenta a avaliação atual separada do texto legado. Os anexos conservam os registros originais para não apagar sua proveniência.

Preservar histórico não exige tratar tudo como atual. A continuidade precisa de uma entrada única que indique qual revisão vale para cada afirmação. Um próximo trabalho documental legítimo é atualizar os campos atuais e manter os snapshots antigos como históricos. Não seria legítimo alterar os resultados históricos ou os pesos para aparentar mais avanço.

## 5. A VM interrompeu a observação do original várias vezes

Os registros mostram relógios sem avanço, capturas idênticas após intervalos externos e testes interrompidos. Houve preparação de contenção, transferência controlada de corpus, instalação e validação do coletor, autorização pontual de manutenção e reinício, novo observador e novas paradas. O estado mais recente documentado da campanha ficou no relógio 09:54:23 de 19/10/2026, com testes suspensos por instrução do usuário.

“Suspensos” se refere aos testes. Não é uma confirmação nova de que o estado do VirtualBox esteja pausado ou desligado. A VM não foi reinspecionada para produzir este relatório. O comportamento de um aplicativo em uma VM que não responde não pode ser classificado automaticamente como defeito do Foxit. Por isso, as ações foram interrompidas e os resultados desconhecidos permaneceram inconclusivos.

Essa instabilidade atrasa as observações dinâmicas e a comparação fiel, mas não explica todo o trabalho restante. Formulários, contratos de assinatura, renderização 3D, casos executáveis e análise estática ainda podem avançar sem executar o original. A VM não deve virar justificativa genérica para essas pendências.

## 6. Preparar a contenção e os instrumentos também consumiu etapas

Um snapshot e uma configuração de rede desligada não bastam para provar que todos os controles do laboratório e o coletor funcionam. Foi necessário conferir identidade dos originais e fixtures, permissões, token interativo limitado, recibos de início/coleta/fim, sincronização do observador e transporte. Houve diferença entre testar o coletor no host e instalá-lo de fato no guest. P02 só passou a concluída quando a integração offline foi examinada.

Essas atividades preservam a confiabilidade dos resultados, mas não acrescentam, por si mesmas, funções PDF ao Linuxit. O relatório mostra os marcos de infraestrutura separadamente, para que progresso de laboratório não pareça progresso de reconstrução funcional.

## 7. O desenvolvimento teve correções reais de implementação e regressões

Foram corrigidos, entre outros pontos, deslocamento e mutação na normalização de CropBox, recursão dos controles laterais, recorte da barra lateral, busca pelo autor de comentários, publicação de cópias sem sobrescrever arquivos, representação de criptografia no writer, controle de sessões antigas e transporte de senha. Houve também ampliação de testes para confirmar aparências vetoriais e Unicode, persistência de formulários, mídia, OCR e novas integrações.

Essas correções são trabalho de produto. Nenhum conjunto de testes consegue antecipar todos os problemas antes de existir código e execução real. Ao mesmo tempo, não é correto transformar cada correção de regressão em recuperação de uma funcionalidade nova do Foxit. A cronologia permite distinguir implementação, correção, documentação, validação e entrega.

## 8. Alguns atrasos recentes vieram do próprio ambiente de testes

O CI identificou problemas que exigiram correção e repetição. A fila CUPS sintética inicialmente usou um backend não instalado no ambiente mínimo; foi corrigida para IPP. A verificação RFC3161 usou inicialmente opções que não pertenciam ao subcomando OpenSSL `ts`; depois foi corrigida. O primeiro candidato 0.1.16 passou na fonte e no payload, mas falhou no sandbox por depender de configuração OpenSSL ausente. O candidato foi rejeitado e o código/fixture foram corrigidos antes da nova compilação.

No teste de desktop, houve caminho de portal do host usado dentro do Flatpak, diretórios de associação não declarados no ambiente, espera insuficiente pela concessão, disputa pela propriedade D-Bus e, por fim, corrida de desmontagem FUSE ao substituir um daemon ativado automaticamente. A correção final inicia o daemon controlado antes de qualquer execução Flatpak, mantém a identidade do processo e aguarda a desmontagem antes do reinício. Duas repetições independentes aprovaram os nove controles.

Os e-mails “Run failed” eram avisos desses testes. Os pushes e a publicação do código podiam ter terminado normalmente. Não foi necessário ocultar falhas ou desativar as notificações para obter aprovação: as causas foram corrigidas e as falhas anteriores foram preservadas. Uma nova falha real ainda pode gerar um novo aviso; as duas aprovações não são garantia de que qualquer ambiente futuro será livre de problemas.

Parte desse retrabalho foi evitável, especialmente na preparação do probe do portal e na dependência de configuração implícita do OpenSSL. O procedimento correto depois de encontrá-lo foi preservar a primeira falha, corrigir o mecanismo e executar de novo, e não aceitar o candidato reprovado. Isso explica tempo adicional, mas não deve ser confundido com engenharia reversa adicional do Foxit.

## 9. Executar no Linux, empacotar e auditar são verificações diferentes

O host de trabalho é Windows. A validação principal do Linux/GTK foi feita no CI com Debian, tela virtual e runtimes controlados. Em um marco de entrega, a suíte é executada na fonte, no payload com as bibliotecas distribuídas e no sandbox Flatpak instalado. Depois há verificação do launcher, integridade dos arquivos, licenças/proveniência, instalação independente e download público.

Na 0.1.16 foram 564 métodos em cada um dos três ambientes. Isso não são 1.692 funcionalidades distintas: são as mesmas situações de teste executadas em três configurações. A auditoria posterior não repetiu a suíte inteira; fez 11 controles próprios, cinco verificações de funcionamento e três testes GTK no mesmo pacote, sem recompilá-lo. O probe de desktop foi separado e executado em dois ambientes novos.

O pacote cresceu para 118.393.760 bytes com as novas dependências. Ele passou a ser distribuído como asset de uma prerelease no GitHub, em vez de ser colocado como um novo arquivo grande comum no Git. Foi preciso adaptar o resolvedor, o cache por hash e a auditoria para esse caminho de distribuição. Esse é trabalho de entrega do Linuxit, não recuperação de mais código proprietário.

## 10. Há ambientes e materiais que o CI não substitui

Uma fila CUPS retida não comprova escala no papel, margens físicas, duplex ou cancelamento no dispositivo. Monitores virtuais não comprovam todos os problemas de monitores físicos e compositores. AT-SPI em um teste não comprova experiência com um leitor de tela real. Um pipeline com saída de áudio de teste não comprova alto-falantes ou dispositivos físicos.

O teste nativo Windows com cinco controles validou um adaptador da fonte em um ambiente de CI Windows Server 2022. Ele não é um instalador final para Windows 11 do usuário, não valida toda associação e impressão no Windows e não fecha toda a família de plataforma. A proteção RMS depende ainda de serviço, identidade e documentos autorizados; não pode ser declarada implementada sem esses materiais. Nuvem direta foi adiada pelo usuário e não deve ser retomada como se fosse uma falha de produtividade.

## 11. Os 50 planos completos de aceitação continuam sem execução integral

Há muitos testes próprios aprovados, mas os 50 cenários de aceitação identificados na especificação permanecem `not_run`. Eles descrevem fluxos completos e não podem receber aprovação apenas porque existe um teste relacionado com um nome parecido. A validação da especificação foi deliberadamente escrita para evitar essa confusão.

É importante reconhecer esta dívida: transformar os planos em execuções rastreáveis ainda é trabalho real, e parte dele independe da VM. É possível executar aceitações próprias com fixtures e comportamentos declarados, mantendo separada a comparação com o Foxit. Os dois cenários de nuvem direta devem continuar adiados. A necessidade de original para paridade não impede preparar e executar o lado próprio dos casos elegíveis.

## 12. Não há medição suficiente para atribuir horas a cada causa

O Git registra datas de commits; os workflows registram intervalos de execução; as notas registram acontecimentos. Esses dados permitem mostrar a sequência e alguns tempos de espera, mas não são um controle completo de horas trabalhadas. O intervalo entre dois commits não pode ser considerado automaticamente tempo de trabalho nem tempo perdido. A primeira revisão disponível já preserva um marco 0.1.1, portanto também não se deve assumir que o histórico Git descreve todo o trabalho anterior.

Há dois limites de execução documentados: uma tentativa de cerca de 1.801,7 segundos para um limite de 1.800 e outra com limite de 600 segundos. São timeouts de análise/provedor. Nenhum deles prova esgotamento de tokens. O registro contém zero eventos confirmados de esgotamento de tokens, não uma prova de que tokens nunca tenham sido consumidos ou de que toda interrupção tenha uma causa conhecida. Não é possível atribuir honestamente a demora a tokens sem evidência.

## 13. O que poderia ter sido conduzido melhor

A comunicação deveria ter distinguido desde o início: pacote utilizável, recorte implementado, etapa percorrida, aceitação própria e equivalência integral. O indicador de checklist não deveria ter servido como resposta à quantidade de código reconstruído. A atualização dos campos atuais da especificação e do backlog deveria ter acompanhado as notas de continuidade, para não manter pendências antigas já parcialmente superadas pelo código.

Também seria mais eficiente manter uma fila única de operações pequenas com resultado verificável, consolidar testes pertinentes em lotes e gerar Flatpak nos marcos, como o usuário pediu, em vez de criar a impressão de que cada nova versão encerra uma família. Os erros de infraestrutura devem ser investigados antes de repetir a mesma campanha sem alteração. As correções e as execuções estão preservadas para que outras IAs não repitam a investigação já feita.

O pedido de fazer tudo sem VM não foi concluído na rodada anterior. A rodada entregou uma ampliação substancial e um pacote validado, mas deixou S11 e outros contratos sem VM abertos. A resposta de status anterior reconheceu isso. Este relatório não transforma essa entrega parcial em cumprimento integral do pedido.

# O que precisa acontecer até um fechamento verificável

## Marco A — tornar o escopo de conclusão finito

Precisamos distinguir uma versão local utilizável, uma versão com todas as operações próprias contratadas e a equivalência integral com o Reader de referência. A 0.1.16 já atende ao primeiro nível dentro dos limites documentados. O segundo e o terceiro ainda não estão concluídos. Uma decisão futura de escopo pode definir uma versão final local sem exigir nuvem direta adiada, mas isso deve ser registrado; o relatório não muda unilateralmente os critérios antigos.

O inventário deve separar obrigações confirmadas do Reader, propostas próprias e recursos ainda não confirmados. A lista conhecida deve ser fechada para cada marco, com limites, casos nominais, erros e critérios de aceitação. Novas descobertas entram em uma revisão posterior do inventário, sem mudar retroativamente o significado de um pacote já entregue.

## Marco B — reconciliar os registros atuais

Os textos atuais de escopo e os próximos passos precisam apontar para a implementação mais recente. Combo editável, cálculos declarativos, voz, camada salva, CA/CRL, token de assinatura e portal persistente não devem voltar a ser tratados como inexistentes por causa de campos legados. Ao mesmo tempo, esses recortes não devem apagar as pendências de JavaScript geral, XFA, PAdES-LTV, renderização 3D e aceitação completa.

Essa reconciliação é documental. Ela evita retrabalho e dá uma fila confiável à próxima IA, mas não aumenta por si só a cobertura funcional. Os critérios amplos permanecem com os estados registrados até existir evidência técnica suficiente para fechá-los.

## Marco C — executar os casos completos elegíveis sem VM

Cada plano S12 precisa de fixture identificada por hash, passos executáveis, resultado esperado do contrato próprio, saídas examináveis, estado real da execução e vínculo à revisão do código. Não basta importar um resultado antigo como se fosse uma nova execução. Casos próprios e comparação diferencial devem ter resultados separados. Os casos de nuvem direta não devem ser executados enquanto o adiamento permanecer.

As operações novas e as antigas afetadas precisam de testes pertinentes de persistência, erros, cancelamento, troca de documento, arquivos alterados, permissões e descarte de resultados obsoletos. Depois de passarem, a suíte consolidada do marco e os três ambientes de entrega continuam sendo exigidos para publicar um novo pacote.

## Marco D — desenvolver as capacidades realmente ausentes

XFA precisa de contrato e de um modelo de processamento de formulário próprio. JavaScript geral não é uma extensão trivial de cinco helpers declarativos: implica linguagem, eventos, APIs, isolamento e limites. Assinaturas incrementais, múltiplas assinaturas, DocTimeStamp, material de validação e PAdES-LTV exigem contratos e casos próprios de revisão documental e cadeia de confiança. Renderização U3D/PRC exige um renderizador e interação; a extração de streams não resolve isso.

Os formatos multimídia e variantes documentais fora dos limites atuais precisam de inventário e aceitação, em vez de serem considerados universalmente suportados por existir GStreamer ou pypdf no pacote. A qualidade de OCR, a ordem semântica do texto e a fidelidade de conversões continuam limitadas e precisam de corpus mais amplo. Recursos que pertençam apenas ao Editor não devem ser incluídos automaticamente no compromisso com o Reader.

## Marco E — fechar as lacunas estáticas dirigidas

As próximas análises devem partir dos corpos e resultados já preservados. Permanecem questões sobre chamadores, domínio de índices, tipos, propriedade/liberação de objetos, seleção de serviços/provedores, estados de busca e fluxos completos. As alocações de arrays e as contagens A=1/B=N foram parcialmente esclarecidas; repetir essas mesmas sementes não é progresso novo. A fronteira de 37 bytes e os recortes de funções grandes precisam continuar identificados como limitações.

Diagramas e contratos devem refletir o que foi efetivamente demonstrado. Um offset igual em duas estruturas não prova que elas sejam o mesmo tipo. O pseudocódigo não deve ser convertido automaticamente em tipos exatos ou em código portátil sem conferir instruções e contexto.

## Marco F — retomar a referência somente quando o ambiente permitir

Os testes do original continuam suspensos. Uma futura retomada requer a resolução autorizada da parada, controle do relógio/resposta, novo observador quando necessário, preflight e contenção offline. Os resultados já observados devem ser reaproveitados com sua identidade; não há motivo para repetir toda a campanha inicial como se nada tivesse sido feito.

Quando a referência puder ser usada, será necessário completar variantes de busca/destinos, cancelamento, imposição, interface e demais operações delimitadas, examinar diferenças com a mesma fixture e registrar o que ficou inconclusivo. Um novo travamento exige parar e salvar, conforme a regra do usuário. Não é permitido superar a parada automaticamente.

## Marco G — validar ambientes e dispositivos reais disponíveis

Impressora física, áudio, leitor de tela e monitores físicos precisam de seus equipamentos. Um cliente real de pasta sincronizada precisa ser observado para transferência, conflitos e indisponibilidade de rede, mantendo o arquivo local íntegro. Esse teste não exige reabrir a integração direta de nuvem. RMS precisa de ambiente e materiais autorizados. O suporte Windows completo permanece posterior à prioridade Linux e precisa de sua própria entrega e aceitação.

## Marco H — produzir e auditar a entrega final do escopo escolhido

Quando o escopo do marco estiver implementado e aceito, deve ser fixada uma revisão, executada a suíte adequada, gerado o Flatpak, testado o payload e o sandbox, examinada a interface pertinente, publicada a identidade do arquivo e auditada uma instalação do mesmo pacote. Também são necessários versão/limites claros, fontes e licenças das dependências, hashes e confirmação do remoto.

Esse processo já funciona para marcos de desenvolvimento; a 0.1.16 é uma demonstração concreta disso. O que falta para um encerramento integral não é inventar um novo empacotador, mas concluir as obrigações de funcionalidade, especificação e validação que ainda estão abertas. Uma auditoria de pacote aprovada não pode encerrar automaticamente todas as etapas de reconstrução.

## Quando será possível dar uma previsão de término

Uma previsão responsável depende de uma lista finita de obrigações e da separação entre o que exige implementação, original, hardware e serviços. Hoje há itens cujo contrato ainda está em caracterização e famílias com complexidades muito diferentes. Não há base suficiente para prometer uma data ou converter o checklist em horas restantes.

O próximo avanço mais útil para previsibilidade é encerrar casos completos próprios de um conjunto delimitado, registrar o esforço real desse lote e atualizar a fila restante. Isso permitiria estimar lotes comparáveis. Não permitiria extrapolar automaticamente de um helper pequeno para XFA, LTV ou um renderizador 3D. Nenhuma estimativa de data foi inventada neste relatório.
