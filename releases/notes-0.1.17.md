Marco de desenvolvimento **0.1.17/devel**, Linux x86_64. Reconstrução integral e paridade com o Foxit permanecem abertas.

Novidades desde 0.1.16: formatos declarativos de formulário (números com vírgula decimal, datas numéricas, CEP/CPF/telefone e máscaras livres); leitura de campos XFA e preenchimento de XFA híbrido mantendo os dados coerentes; régua com vírgula decimal; segunda e demais assinaturas como revisões incrementais (as anteriores continuam válidas); verificação offline de carimbos de tempo de documento (RFC 3161) e uso do DSS embutido (certificados e CRLs) na validação; nuvem pelo fluxo de pastas sincronizadas; correção de estabilidade (coleta de lixo do Python só na thread principal do GTK) e da reprodução de mídia curta.

**616/616 testes próprios em cada ambiente: fonte Linux, payload e Flatpak instalado**, sem falhas/erros/skips. Smoke 5/5 e launcher 3/3. Aceitação própria: 65/65 casos. Fonte fixa: `dec46c979e56d722482a465563c6df97b898dcdc`. [Execução aprovada](https://github.com/airtonbp19edu/Linuxit-PDF/actions/runs/39474059660).

O arquivo Flatpak é o mesmo candidato aprovado, sem recompilação. Tamanho: **118422768 bytes**. SHA-256:

```text
ec773a2028b63a4026c32866472504bbf7aad7e9994ce2edb78954cfb8217a71
```

```bash
flatpak install --user ./LinuxitPDF-0.1.17-x86_64.flatpak
flatpak run --user io.github.airtonbp19edu.LinuxitPDF
```

[Avisos e situação](https://github.com/airtonbp19edu/Linuxit-PDF/blob/main/docs/AVISOS-E-STATUS.md) · [Instalação](https://github.com/airtonbp19edu/Linuxit-PDF/blob/main/docs/instalacao.md). Bundle sem assinatura digital. Runtime Freedesktop 25.08; dependências e avisos de licença acompanham o pacote e os manifestos versionados. Nenhum binário ou recurso proprietário Foxit foi incorporado.

Login em provedor de nuvem, envio por API e colaboração remota seguem adiados; IA generativa está excluída. XFA dinâmico, JavaScript geral, gravação de DSS/LTV, OCSP, renderizador 3D e famílias integrais permanecem abertos. Testes próprios não comprovam comparação integral do original nem impressão, áudio, monitores ou cliente sincronizador físicos. A VM do usuário não foi acessada.
