# Segurança, acessibilidade e edição local — fonte 0.1.8

Subconjuntos próprios, após o pacote 0.1.7. Fonte e Flatpak 0.1.8 validados
no CI Linux; confirmação da publicação e auditoria independente nas notas.
Nuvem adiada pelo usuário. Nenhuma observação dinâmica do Foxit nesta rodada.

No menu Arquivo:

- **Senhas e permissões…** inspeciona proteção e autentica a senha conhecida;
  cria cópia AES-256 (PDF R6) de fonte não criptografada. Seis opções de permissões
  são declaradas no PDF; extração para acessibilidade permanece permitida.
- A mesma janela cria cópia sem criptografia somente após autenticação da
  **senha de proprietário**. Senha de abertura classificada como usuário não
  autoriza essa operação. Não há recuperação de senha ou serviço RMS.
- **Texto da página… (Ctrl+Shift+T)** extrai uma fotografia textual da página
  atual para Gtk.TextView com interface ATK.Text. F6/Shift+F6 alternam regiões
  de foco. Extração não é OCR, leitura por voz ou garantia de ordem semântica.
- **Verificar assinaturas…** confere CMS destacado e ByteRange localmente.
  Integridade é separada de confiança, revogação, carimbo de tempo e validade
  jurídica. Nenhuma cadeia de certificados é aprovada por esta implementação.
- Renomear marcador, atualizar nota Text desbloqueada e girar página permitem
  salvar uma cópia nova; posição do marcador, retângulo da nota e fonte são
  preservados. Undo, edição completa de anotações e formulários seguem parciais.

## Contratos e limites

Segurança: PDF até 64 MiB/1.000 páginas; saída até 128 MiB. Senhas novas de
8–64 caracteres ASCII imprimíveis, distintas entre usuário/proprietário.
Inspeção aceita senha conhecida até 127 caracteres. Credenciais passam somente
por stdin JSON do worker: nunca argumentos, variáveis de ambiente ou relatórios.
Campos da janela são limpos após captura/cancelamento/fechamento. Não há garantia
de apagamento da memória. Mensagens de erro de segurança são fixas e sem segredos.
As permissões declaradas dependem do leitor; não equivalem a controle externo.

Gravação exige destino inexistente e identidade SHA-256 da fonte. Documentos com
assinatura/campo Sig, Perms, XFA ou Collection são recusados para regravação.
Criação exclusiva e modo 0600 em POSIX; Windows usa ACL herdada. Reabertura confere
criptografia/páginas/permissões antes de confirmar. A leitura normal ainda não
possui entrada de senha integrada; uma cópia autorizada sem criptografia pode
ser aberta. Não usar esta função para alterar um documento assinado.

Texto acessível: limite de 1 MiB UTF-8 por página, sem PDF criptografado, mesmo
quando abre com senha vazia. Troca de documento fecha a janela; gerações antigas
e tarefas canceladas não atualizam outra página. Testes ATK em X11 não comprovam
experiência real com Orca/AT-SPI, desktop, portais ou conformidade PDF/UA/WCAG.

Assinaturas: até 16 campos e 2 MiB de CMS DER por assinatura. Apenas os filtros
adbe.pkcs7.detached/ETSI.CAdES.detached e ByteRange de quatro inteiros delimitados.
A lacuna deve coincidir com Contents hexadecimal; padding DER é conferido.
Bytes acrescentados depois da revisão assinada impedem afirmar cobertura do
arquivo atual. Falha criptográfica pode ser adulteração ou algoritmo não suportado;
não é diagnóstico inequívoco de fraude. PDF criptografado não é suportado aqui.
Linux usa OpenSSL cms -verify -binary -noverify; Windows usa .NET SignedCms
CheckSignature(true). Ambos verificam assinatura/conteúdo sem validar a cadeia.
Nenhuma conexão de rede é realizada. PAdES/LTV, confiança e assinatura de novos
documentos permanecem pendentes. Certificados de testes são sintéticos.

Workers têm diretório temporário privado por tarefa; TMPDIR/TEMP/TMP propagados
aos filhos. Em POSIX, cancelamento encerra o grupo de processos antes da limpeza,
incluindo Poppler/OpenSSL. Windows encerra o worker, sem garantia equivalente para
todos os descendentes. Limpeza é de melhor esforço, não apagamento seguro.
Interrupção pode deixar uma saída parcial ou já concluída; conferir antes de tentar
de novo. Os controles nunca executam ações/scripts incorporados no PDF.

## Evidências e continuidade

Código: pdf_security.py, security_window.py, accessible_reader.py,
pdf_signatures.py, signature_window.py, pdf_changes.py e adaptadores worker.
Testes próprios: test_pdf_security.py, test_extended_edits.py,
test_pdf_signatures.py, test_security_accessibility_gtk.py, test_signature_gtk.py.
Relatórios portáveis examinados são publicados em testes/resultados/0.1.8-portable/.
Testes GTK/Linux e entrega em testes/resultados/0.1.8/.
Os 50 planos completos permanecem not_run; paridade Foxit permanece 0/25.

Portáveis examinados:20/20 segurança,9/9 edição ampliada,10/10 CMS e12/12
regressão worker no Windows. Esses51 controles não substituem267 casos Linux.

## Marco Linux/Flatpak examinado

[CI](https://github.com/airtonbp19edu/Linuxit-PDF/actions/runs/39074818078):267/267 em cada ambiente fonte, payload e sandbox instalado,
zero falhas/erros/skips.39 métodos portáveis novos e16 GTK: segurança7,
texto/acessibilidade6, edição ampliada1, assinaturas2. Cancelamento de worker
com descendente real e limpeza temporária foi exercitado no Linux.
97 arquivos app, 2804runtime/215ELF/150pacotes;
OpenSSL empacotado com loader/runtime pareados. Smoke5/5 e launcher3/3.
Sete capturas com hashes conferidos e imagens examinadas. Oito pacotes anteriores
preservados. [Revisão](../testes/resultados/0.1.8/validation-review.json).

## Publicação e auditoria independente — 2026-10-17T20:21:46-03:00

Entrega `c6b273fdf44f2e260f0ddae092397158cf65237c` confirmada no remoto. [Auditoria](https://github.com/airtonbp19edu/Linuxit-PDF/actions/runs/39078571081)
reinstalou o mesmo bundle publicado, sem rebuild:97 arquivos app,2.804 runtime,
215ELF e150 avisos de pacotes conferidos. Sete controles do auditor e cinco novos
smoke checks passaram. As suítes completas267/267 continuam evidência do builder,
não foram repetidas pela auditoria. [Revisão](../testes/resultados/0.1.8/audit/review.json).
Projeto ainda incompleto; pesos/paridade e nuvem adiada preservados.
