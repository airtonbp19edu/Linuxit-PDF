Marco de desenvolvimento **0.1.18/devel**, Linux x86_64. Reconstrução integral e paridade com o Foxit permanecem abertas.

Novidades desde 0.1.17: cor, opacidade e tamanho de anotações existentes; marcar áreas para redação e aplicar a redação numa cópia nova (páginas marcadas viram imagem, demais páginas intactas); imagem de apresentação de anotações 3D, com aviso de que a cena não é interativa; recuperação mais segura de PDFs danificados (pede consentimento também em reparos silenciosos, nunca inventa página) com corpus próprio de 12 casos; corpus próprio de criptografia (RC4-40, RC4-128, AES-128, AES-256 e metadados em claro) com correção para metadados XMP declarados em claro; ordem de leitura por colunas no texto acessível e em cópias com OCR; auditoria de entrega comparando com o commit testado e conferência prévia da publicação.

**664/664 testes próprios em cada ambiente: fonte Linux, payload e Flatpak instalado**, sem falhas/erros/skips. Smoke 5/5 e launcher 3/3. Aceitação própria: 81/81 casos. Fonte fixa: `2b49d686483989da00efd2aeeaf7512102a90508`. [Execução aprovada](https://github.com/airtonbp19edu/Linuxit-PDF/actions/runs/39526036575).

O arquivo Flatpak é o mesmo candidato aprovado, sem recompilação. Tamanho: **118440408 bytes**. SHA-256:

```text
058ebbe0ceb0904abe86e5ad2eaadef4540e42a51028341c2cd70d735ce1b985
```

```bash
flatpak install --user ./LinuxitPDF-0.1.18-x86_64.flatpak
flatpak run --user io.github.airtonbp19edu.LinuxitPDF
```

[Avisos e situação](https://github.com/airtonbp19edu/Linuxit-PDF/blob/main/docs/AVISOS-E-STATUS.md) · [Instalação](https://github.com/airtonbp19edu/Linuxit-PDF/blob/main/docs/instalacao.md). Bundle sem assinatura digital. Runtime Freedesktop 25.08; dependências e avisos de licença acompanham o pacote e os manifestos versionados. Nenhum binário ou recurso proprietário Foxit foi incorporado.

Login em provedor de nuvem, envio por API e colaboração remota seguem adiados; IA generativa está excluída; renderização 3D interativa adiada para atualização futura. XFA dinâmico, JavaScript geral, gravação de DSS/LTV, OCSP e famílias integrais permanecem abertos. Testes próprios não comprovam comparação integral do original nem impressão, áudio, monitores ou cliente sincronizador físicos. A VM do usuário não foi acessada.
