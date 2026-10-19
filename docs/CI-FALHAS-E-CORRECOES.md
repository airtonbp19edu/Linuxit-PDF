# Avisos de falha do GitHub Actions

As mensagens com “Run failed” informam que uma verificação automática falhou.
O envio de commits ao GitHub pode ter sido concluído normalmente. Os workflows
atuais são iniciados manualmente nos marcos de validação; um push sozinho não
inicia essas campanhas. Os avisos antigos permanecem no histórico do e-mail.

## Portal e integração do desktop — corrigido em 19/10/2026

A notificação referente ao commit `a5ebda9` é da
[execução 39339331887](https://github.com/airtonbp19edu/Linuxit-PDF/actions/runs/39339331887).
Oito dos nove controles passaram. A primeira leitura após a concessão pelo
portal encontrou o arquivo ainda indisponível; a leitura após reiniciar o
portal, a revogação e a associação de PDF já passaram nessa execução.

A correção `e61d174` espera que o processo de portal criado pelo teste seja o
proprietário do nome no D-Bus e que a exportação FUSE esteja disponível. Antes,
outro processo ativado automaticamente podia satisfazer a espera apenas pelo
nome. A leitura continua obrigatória e precisa conferir os bytes esperados.

A [execução corrigida 39339986089](https://github.com/airtonbp19edu/Linuxit-PDF/actions/runs/39339986089)
passou nos **9/9 controles**, sem erros. Ver
[relatório examinado](../testes/resultados/sem-vm-2026-10-19/s10-third/review.json).
Ela testou o pacote publicado 0.1.15: concessão fora da pasta pessoal,
persistência após reiniciar o próprio portal, revogação, associação/abertura
real de PDF e atualização/retorno de versão com preferências preservadas.
É um desktop X11 efêmero, sem alteração no Windows ou na VM do usuário.

## Outras falhas preservadas

- CUPS mínimo sem backend `socket`: a fila sintética passou a usar o backend
  IPP disponível. A execução posterior aprovou os quatro controles reais de
  envio retido, consulta e cancelamento, sem impressora física.
- RFC3161: o subcomando `openssl ts` não aceita as mesmas opções de repositório
  do subcomando CMS. Foram usados repositórios vazios explícitos. A validação
  Linux posterior aprovou o token e recusou sua associação a bytes alterados.
- Primeiro candidato Flatpak 0.1.16: a consulta TSA dependia de um arquivo de
  configuração OpenSSL ausente no sandbox. Fonte e payload passaram; o teste
  instalado identificou o problema. O candidato foi rejeitado. A revisão
  `a5ebda9` fornece configuração mínima explícita para a consulta e a verificação;
  a [execução corrigida39339330479](https://github.com/airtonbp19edu/Linuxit-PDF/actions/runs/39339330479) aprovou564/564 testes em cada ambiente fonte/payload/sandbox, sem falhas/erros/skips. Somente esse novo candidato foi publicado como0.1.16 de desenvolvimento.

Os testes que detectaram as falhas foram mantidos. Notificações da conta não
foram desativadas; apagar o aviso ou aceitar uma falha como sucesso ocultaria
o estado real do projeto. Falhas futuras devem ser investigadas pelo primeiro
passo que falhou e pelo relatório preservado em sua execução.
