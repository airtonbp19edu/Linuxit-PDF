# Etapa 10 — campanha de observação dinâmica

**Atualização de 18/10/2026:** [campanha na VM offline](VM-FOXIT-2026-10-18.md)
executou o original;11 recortes C18 comparados (10 iguais/1 divergente em autor).
Ambiente da etapa10 validado; demais critérios dinâmicos/diferenciais parciais.
Cancelamento, destinos dos hits, imposição com parâmetros correspondentes e
processos residuais continuam abertos. Pesos preservados; paridade integral0/25.

O texto abaixo registra o marco histórico anterior e seus limites naquela data.

Estado em 16/10/2026: **preparação verificada; execução bloqueada**. O original
não foi iniciado nesta rodada. O Windows local é 11 Home Single Language,
build 26200, sem executável Windows Sandbox. O usuário confirmou não ter VM.
O WSL informa não estar instalado; não foram encontrados QEMU, VirtualBox,
VMware ou Docker nos caminhos examinados. Isso não é inventário exaustivo de
todos os discos. A consulta DISM de recursos exigiu administrador e não
confirmou seu estado. Nenhum recurso do sistema foi instalado ou habilitado.

A [documentação Microsoft](https://learn.microsoft.com/en-us/windows/security/application-security/application-isolation/windows-sandbox/)
exclui Windows Home do suporte ao Sandbox. O diagnóstico REA/Ghidra aprovado
é de análise estática; ele não fornece um desktop Windows isolado para esta
campanha. O histórico Wine/QEMU permanece em `relatorio-dinamico.md`: controle
x86 aprovado, Foxit encerra antes de uma interface utilizável.

## Material preparado

`testes/cenarios-dinamicos.json` contém 20 cenários iniciais: abertura,
navegação, busca e escopos, cancelamento, erros, senha sintética, anexos,
prévia de impressão, cópia local e encerramento. Contagens do Linuxit são
identificadas como **contrato próprio**; as observações Foxit começam vazias.
A campanha não cobre todas as 25 famílias funcionais da matriz.

O comando abaixo prepara uma pasta nova e privada, sem executar o original:

```powershell
python scripts/prepare_foxit_dynamic.py --reference 'A:\Programas\Foxit PDF Reader\Foxit PDF Reader' --output 'analysis-local/dynamic/windows-01'
```

O gerador confere o SHA-256 esperado antes/depois, recusa sobrescrever uma
campanha e recusa links/junções na referência. Gera sete PDFs, um controle
de texto, hashes, roteiro, observações `not_run` e `foxit-offline.wsb`.
O corpus inclui o PDF de busca já preservado, oito páginas com tamanhos e
rotações diferentes, 250 páginas para busca, senha conhecida, anexo textual,
arquivo inválido e arquivo vazio. Nenhum dado pessoal é usado. A senha é
`linuxit-sintetico`; não há recuperação de senha nem contorno de proteção.

O `.wsb` é para **um Windows compatível com Sandbox já disponível**. Prepará-lo
no Home não habilita esse recurso. Seus caminhos absolutos pertencem ao host
que o gerou; regenerar o kit ao mudar de máquina. Não publicar o kit completo,
as telas do Foxit ou outros resultados proprietários no Git.

## Contenção e procedimento de execução

A [configuração oficial](https://learn.microsoft.com/en-us/windows/security/application-security/application-isolation/windows-sandbox/windows-sandbox-configure-using-wsb-file)
permite desligar rede e redirecionamentos e mapear pastas somente leitura.
O arquivo gerado desabilita rede, GPU virtual, áudio, câmera, impressoras e
clipboard; habilita cliente protegido. Expõe apenas referência e corpus em
leitura e uma pasta nova `results` em escrita. Essa pasta é a única superfície
gravável compartilhada com o host; trate arquivos recebidos como não confiáveis.
O perfil do guest é descartável, sem contas ou diretórios pessoais montados.

1. Em host compatível, conferir XML e as três pastas mapeadas. Em uma VM comum,
   exigir isolamento equivalente: adaptador de rede desconectado, perfil
   descartável, sem clipboard, impressoras, credenciais ou pastas adicionais.
2. Iniciar o ambiente isolado. O `.wsb` abre **somente o controle do Notepad**.
   Confirmar o marcador `LINUXIT_RUNTIME_PROBE` e uma janela responsiva; registrar
   a prova local. Não inferir sucesso apenas da presença de um processo.
3. Conferir no guest a ausência de rede/redirecionamentos e os mounts esperados.
   Se qualquer pré-condição falhar, parar e registrar falha de infraestrutura.
4. Abrir `C:\Linuxit\Reference\FoxitPDFReader.exe` pelo Explorer do guest.
   Registrar versão, diálogos e interface. Se encerrar antes da UI, preservar a
   falha e manter os cenários funcionais `not_run`.
5. Abrir somente os arquivos em `C:\Linuxit\Input`. Executar os casos D02–D20,
   anotando cada variante, opções, ordem, contagem e destino com página base 1.
   Diálogo ausente não demonstra recurso inexistente: anotar o contexto.
6. Salvar cópias/anexo somente em `C:\Linuxit\Results`. Não enviar trabalhos
   físicos, usar contas, atualizações ou integrações de rede. Na prévia sem
   impressora, registrar indisponibilidade sem mudar a contenção.
7. Preservar evidências locais com SHA-256 e resultados reais separados dos
   valores esperados. Um caso com tempo insuficiente para cancelar continua
   sem observação de cancelamento. Resultado desconhecido continua `null`.
8. Conferir novamente a identidade do original e revisar as evidências antes
   de publicar apenas metadados e conclusões independentes. Comparar no Linuxit
   com o mesmo corpus quando houver ambiente Linux gráfico; não promover uma
   família inteira por um único caso.

Os critérios e pesos da etapa 10 não mudaram. A existência deste kit não
conclui nenhum deles: ambiente executável, cenários observados e integrações/
exceções observadas continuam exigindo execução real. Etapa 10: **0% verificado**;
roteiro geral: **43,33%**; paridade diferencial: **0/25 famílias**.
