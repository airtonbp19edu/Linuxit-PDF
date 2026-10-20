# Avisos e situação do Linuxit PDF

Regra pedida pelo usuário em 20/10/2026: todo aviso dado ao usuário fica registrado aqui, no GitHub, e é copiado para a pasta local do projeto como `AVISOS-LOCAL.md`. Esse arquivo local é ignorado pelo Git para nunca bloquear um `git pull`. A seção "Situação atual" é substituída a cada atualização; o histórico de avisos só recebe novas entradas.

## Situação atual — 2026/10/20 às 00:25 (America/Sao_Paulo, UTC-03:00)

### Feito

**O aplicativo**
- Versão 0.1.16/devel publicada como Flatpak (prerelease no GitHub), auditada no mesmo arquivo sem recompilar. Na entrega passou em 564/564 testes próprios em cada ambiente: fonte Linux, pacote e sandbox instalado.
- Python + GTK, com 78 arquivos em `app/`. Das 111 operações do inventário, 97 têm algum código próprio. Isso não é porcentagem de conclusão.
- Leitura e navegação, busca (texto, marcadores, comentários, anexos, índice, coringas, proximidade, radicais em 36 idiomas), anotações, formulários AcroForm com combo editável e cálculos limitados, anexos, impressão e imposição, OCR local, assinatura e verificação offline, proteção por senha, acessibilidade com voz local, camadas e mídia, pastas sincronizadas e integração com portal do desktop. Todos são recortes próprios com limites documentados.

**Nesta sessão (19–20/10/2026)**
- Defeito corrigido: a verificação de carimbo de tempo RFC 3161 falhava sempre com OpenSSL 3.0 (Ubuntu 24.04). Teste novo garante que a correção não confia em autoridades do sistema.
- Registros desatualizados corrigidos: 8 textos de escopo que diziam "pendente" para recursos já existentes, próximos passos antigos, a marcação do portal e a fila de tarefas.
- Testes de aceitação: o validador exigia que os 50 planos ficassem "não executados", o que impedia registrar avanço. Agora 46 casos rodam contra o aplicativo real, incluindo a janela GTK, com fixtures próprias fixadas por hash. O resultado fica ligado à revisão do código.
- Execução registrada: **46 de 50 casos aprovados** na revisão `841557d`. Suíte própria completa **571/571** no Ubuntu 24.04.
- Confirmado no CI Debian 13 ([execução 39363684386](https://github.com/airtonbp19edu/Linuxit-PDF/actions/runs/39363684386)): suíte **571/571**, aceitação **46/46** na revisão `a43e0ba`, campanha preservada 17/17, acessibilidade entre processos e portal nativo aprovados. Revisão em `testes/resultados/aceitacao/2026-10-20/ci-debian13-review.json`.
- Publicado no GitHub, com commits de autoria do Claude.
- REA 6.7.0 (morluto/rea) instalado no ambiente de nuvem do Claude. Esse ambiente é temporário; ver `claude/retomada-instalacao-rea.md` no projeto do claude.ai.

### Em andamento
- Nada rodando agora. Próximo trabalho sugerido: o primeiro item de "Falta" sem VM ou a entrega 0.1.17.

### Falta

**Sem VM, desenvolvimento próprio**
- Escrever o contrato próprio da integração com o sistema (casos S12-25). O portal já foi validado 9/9 no desktop.
- Formulários: XFA e JavaScript geral. Hoje só há cálculos declarativos limitados, sem executar JavaScript.
- Assinaturas: assinatura incremental e múltipla, DocTimeStamp, PAdES-LTV e OCSP.
- 3D: renderizador U3D/PRC. Hoje só lista e extrai.
- Redação definitiva e edição universal de anotações.
- Qualidade de OCR e ordem de leitura, conversões mais amplas e um corpus maior de PDFs danificados, cifras e fontes.

**Análise estática (Ghidra e o Foxit original ficam no PC Windows)**
- Chamadores, tipos e propriedade/liberação de objetos, partindo dos resultados preservados.
- O instalador do REA 6.7.0 no PC (`analysis-local\rea-instalacao\instalar-rea.cmd`) ainda não foi executado.

**Comparação com o Foxit (VM)**
- Testes suspensos desde que o relógio da VM parou em 09:54:23 de 19/10. Só retomar com a sua autorização.
- Equivalência comprovada em 0 de 25 famílias; casos D01–D20 e UI01–UI10 incompletos.

**Ambientes reais**
- Impressora física, áudio e leitor de tela, monitores físicos, cliente sincronizador real e materiais RMS. Windows completo vem depois do Linux.

**Entrega**
- Próximo pacote 0.1.17: Flatpak, testes nos três ambientes e auditoria, incluindo a correção RFC 3161.
- Atualizar a referência de `check_operation_catalog.py`, que está presa aos arquivos da 0.1.16.

**Medição**
- 19 dos 58 critérios das 21 etapas continuam abertos. O percentual global é desconhecido e não deve ser estimado.

**Decisão pequena pendente**
- A régua mostra "2.54 cm", com ponto decimal, numa interface em português.

**Adiado e excluído**
- Nuvem direta está adiada por decisão do usuário.
- Recursos de IA estão excluídos.

## Histórico de avisos

- **2026/10/19 às 23:52** — Suíte completa rodada fora do CI; defeito RFC 3161 com OpenSSL 3.0 encontrado e corrigido com teste novo. Registros que diziam "pendente" para recursos existentes foram atualizados. GitHub ainda não vinculado para publicação.
- **2026/10/20 às 00:15** — Envio ao GitHub recusado: o app do Claude não estava instalado na conta. Opções: instalar em https://github.com/apps/claude/installations/select_target ou publicar pelo PC com `analysis-local\publicar-2026-10-20\publicar.cmd`.
- **2026/10/20 às 00:20** — Publicado: `main` em `a43e0ba`. Os 3 commits foram refeitos com autoria do Claude, para aparecerem como verificados, e os 46 casos de aceitação rodaram de novo na revisão `841557d`, todos aprovados. CI no Debian 13 iniciado. O `publicar.cmd` do PC deixou de ser necessário; basta `git pull`.
- **2026/10/20 às 00:22** — Regra registrada: avisos vão para este arquivo no GitHub e para `AVISOS-LOCAL.md` na pasta local.
- **2026/10/20 às 00:25** — CI no Debian 13 aprovado: suíte 571/571 e aceitação 46/46 na revisão `a43e0ba`, além da campanha preservada, acessibilidade e portal. Nada em andamento agora.
