# Consulta TSA e formas gráficas na redação — 23/10/2026

Implementação própria no ramo `codex/current-demands`, sem mudança da main/candidato ou acesso à VM. A automação de acompanhamento foi excluída porque o usuário mandou o Codex assumir a execução da fila.

## TSA HTTPS opt-in

Novo transporte `timestamp_transport.py`, comando de worker `timestamp-fetch` e ação na janela de assinaturas. O usuário precisa selecionar o pedido já exportado, informar a URL HTTPS, confirmar o envio e escolher um arquivo novo para a resposta. Não existe endpoint padrão ou consulta automática.

O POST contém apenas o pedido RFC3161 preparado, com resumo SHA-256 e nonce; o PDF não é transmitido. São conferidos os hashes do pedido/preparação e da origem. TLS usa os certificados de confiança do Python/sistema. Não há redirecionamento, proxy implícito, cookies, credenciais embutidas na URL ou tentativas adicionais. Conteúdo esperado `application/timestamp-reply`, máximo 1 MiB; worker limitado a 45 segundos, com socket de 20 segundos. Falhas não substituem arquivos existentes.

A resposta precisa conceder o pedido e corresponder ao mesmo nonce, algoritmo e resumo. Identificadores SHA-256 com parâmetros ASN.1 NULL ou ausentes são comparados pelo algoritmo e resumo, em vez de exigir DER byte a byte idêntico. O mesmo ajuste foi aplicado à importação local.

O download não estabelece autenticidade, confiança na CA ou validade jurídica. A etapa existente de importar resposta continua responsável por assinatura CMS, cadeia TSA e publicação de uma cópia incremental. O resultado do transporte marca `complete=false` e `trust_assessed=false`. Nenhuma TSA externa foi escolhida ou contatada nesta rodada.

## Form XObject sem rasterizar

Formas gráficas com BBox válido e Matrix finita são tratadas como objetos indivisíveis. O BBox obrigatório da forma é transformado pela matriz da forma e pela transformação da página. Se tocar a marca, a invocação inteira é removida, incluindo conteúdos aninhados, fontes e clipping internos, sem tentar editar glifos individualmente.

Referências sem uso são removidas; o salvamento existente elimina objetos sem referências. Uma mesma forma usada também fora das marcas permanece para essa outra invocação: não se promete apagar toda ocorrência do mesmo texto no documento. Conteúdo complexo desenhado diretamente na página, máscaras de imagem e grafos fora desse contrato continuam recusados. Não é redação vetorial universal nem limpeza geral de todo dado oculto.

## Verificação

Os relatórios locais preservam **13/13 testes vetoriais e 6/6 de transporte**, sem falhas, erros ou pulos. Um teste realiza HTTPS real contra uma TSA sintética no loopback, com certificado de teste explicitamente confiado apenas no teste; confirma o conteúdo efetivamente recebido e que nenhum PDF é transmitido. Outros verificam nonce/resumo incompatíveis, mídia/tamanho inválidos, redirecionamento, falta de consentimento, alterações na preparação e destino existente. As formas são verificadas por remoção de bytes e de recursos órfãos, matrizes compostas, reutilização fora da marca e recusa de BBox inválido.

Relatórios: `testes/resultados/continuidade-direta-2026-10-23/windows-vector.json` e `windows-tsa.json`. A suíte integral Linux/GTK desta nova fonte ainda precisa ser executada. Os CIs iniciados anteriormente testam as revisões antigas identificadas no plano; não validam automaticamente este código novo. Não há pacote publicado destas alterações.


## Validação posterior — 2026-10-23T21:10:52.788922-03:00

Os avisos acima de suíte integral pendente são históricos. Os recursos estão na fonte combinada testada:808/808 Linux e808/808 em fonte/payload/Flatpak,81/81 aceitações Linux;806/808 Windows nativo, dois pulos exclusivos Linux e zero falhas/erros,79/79 aceitações e instalador8/8. Os cinco testes reais de CA/CRL/RFC3161 foram habilitados no Windows e passaram.

O teste no sandbox encontrou uma lacuna real no empacotamento: os caminhos CA Debian do Python não existiam no runtime Freedesktop. O wrapper corrigido seleciona arquivos/diretório CA legíveis do runtime quando a variável correspondente não foi definida explicitamente. O mesmo bundle reconstruído carregou118 CAs, com CERT_REQUIRED/hostname ativos, em duas instalações de teste. Não foi desabilitada a validação TLS e nenhuma TSA externa foi escolhida. Falha e correção em `testes/resultados/continuidade-direta-2026-10-23/tls-default-before-fix/` e `desktop-tls-final/`.

A redação permanece delimitada a Form XObjects indivisíveis e aos demais caminhos já suportados. Conteúdo complexo direto na página fora desses contratos continua recusado; não há aprovação de redação vetorial universal, equipamento físico ou paridade Foxit.
