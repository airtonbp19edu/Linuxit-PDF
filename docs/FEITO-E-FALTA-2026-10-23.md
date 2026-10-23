# Linuxit PDF — o que foi feito e o que falta

Aviso dado ao usuário em **2026/10/23 às 09:03 (America/Sao_Paulo, UTC-03:00)**, pelo Claude,
a pedido dele ("o que tanto foi feito nesse tempo todo, o que falta fazer"). Base: `main` em
`96fd7a6` (05:58) + pasta local do PC + `CHAT-CLAUDE.txt`/`CHAT-CODEX.txt` até 06:05.
Só leitura: nenhum código, teste, VM, critério ou release foi tocado.

Registrado no GitHub às 10:23, quando o envio foi liberado. **Atualização 10:23:** o item Windows
de "Falta" foi resolvido no runner do GitHub (suíte 735/759 sem falhas, aceitação 79/79); ver
[evidência](../testes/resultados/a6-windows-2026-10-23/review.json). Integração do ramo à `main`
continua pendente.

## Feito (13/10 a 23/10/2026)

- 309 commits em 10 dias. Versões 0.1.0 → **0.1.18 publicadas** (Flatpak, prerelease); **0.1.19
  candidata** pronta e retida.
- Testes próprios: 37 (0.1.1) → 400 (0.1.13) → 564 (0.1.16) → 664 (0.1.18) → **744/744 por
  ambiente** na 0.1.19 (fonte Linux, payload, Flatpak instalado), aceitação própria **81/81**.
- Aplicativo: 94 módulos em `app/`.
- Inventário: 25 famílias / 116 operações. **104/116 têm código próprio** (limitado); 9 pendentes
  de equipamento/ambiente; 3 de nuvem adiadas pelo usuário.
- Entregues (recortes): abertura com senha/recuperação, navegação/zoom 1–6400%, apresentação; busca
  em texto/marcadores/comentários/anexos, índice e radicais PT/EN; seleção; impressão, N-up,
  livreto, mosaico, CUPS; marcadores; anotações (várias, cor/opacidade, edição de texto/autor);
  formulários AcroForm, máscaras, XFA híbrido e de fluxo, JavaScript opt-in em QuickJS isolado;
  anexos/portfólios; assinaturas múltiplas incrementais, RFC 3161, DSS, OCSP offline; senhas
  RC4/AES e permissões; redação rasterizada e vetorial simples; OCR PT/EN com limpeza; TIFF;
  camadas, mídia, imagem de 3D; medidas; temas/preferências; pastas sincronizadas; exportação
  texto/PNG/JPEG/TIFF.
- Engenharia reversa estática (REA/Ghidra): catálogo **410 entradas**; S1 (busca), S2
  (impressão), S3 (anotações/resumo), S4 (reflow) com lotes documentados — todos parciais.
- VM com Foxit original (offline): campanhas de 18–19/10, E24 e E30 (23/10); observações parciais.
  Pergunta da E24 respondida: "Include Comments" desligado por padrão nesta sessão do Foxit
  (causalidade ainda hipótese, segundo o Codex).
- Windows: instalador aprovado (CI 39900942827, 8/8, inclusive pasta com espaço e ç) no ramo
  `claude/windows-installer` (14 commits, **não integrado à main**).
- Proposta B3 escrita (opções A/B/C).

## Falta

### Depende do usuário

1. Autorizar a **publicação da 0.1.19** (mesmos bytes testados).
2. Decidir a **B3** (inventário fixo como régua dos critérios "todas as famílias").
3. **VM/E30**: o Claude continua com a reserva (PEGUEI 02:17, sem LIBEREI); pausado às 05:55
   esperando pedido. Faltam UI05/09/10, D13/14/16/20 (sem digitação) e D10–D12, senha e
   salvar-nome (exigem teclado virtual do guest).
4. **Equipamentos (E23)**: impressora física, leitor de tela, áudio, dois monitores, cliente
   real de sincronização.

### Desenvolvimento próprio (sem VM)

- Windows: suíte nativa 117 ok/2 falhas, travou no teste 120 (diálogo de impressão); aceitação
  62 ok/5 falhas/12 puladas; depois integrar o ramo à main.
- XFA posicionado e FormCalc; JavaScript geral além da API limitada.
- PAdES-LTA, consulta automática a TSA, DSS/LTV completos.
- Edição universal de anotações; redação de conteúdo complexo e de metadados/marcadores/anexos.
- Conversão para formatos Office editáveis.
- Renderização 3D interativa (adiada); RMS.
- Portal/concessão persistente, associação de arquivos, atualização/reversão reais.

### Análise e comparação

- S1–S4 continuam parciais. Dois lotes do Codex (S4 reflow e S1 pesos/scorers, 06:03–06:05)
  estão **só na pasta do PC, sem commit**.
- **0/116** operações comparadas por completo com o Foxit; paridade **0/25** famílias.
- Índice histórico 45,13% (não é porcentagem do código; percentual global indeterminado).
- Fora do escopo: IA (excluída), nuvem por API (adiada).
