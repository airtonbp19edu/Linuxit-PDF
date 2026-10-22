# A6 — DSS incremental, OCSP offline e criação de carimbos RFC 3161

Implementação própria de 2026/10/22. Não executa o Foxit e não usa serviços de
rede. Os módulos são `app/pdf_preservation.py`, `app/signature_ocsp.py`,
`app/pdf_signatures.py` e `app/signature_trust.py`. A interface de assinaturas
oferece incorporar DSS, exportar pedido TSA e importar resposta TSA.

## O que é possível fazer

1. Acrescentar certificados, CRLs e respostas OCSP a uma **cópia incremental**
   de um PDF já assinado. Os bytes antigos são mantidos integralmente; as
   assinaturas anteriores continuam verificáveis sobre suas revisões. O DSS
   anterior, incluindo chaves VRI, é preservado. Arrays globais são mesclados
   e o material duplicado é removido; não são inventadas entradas VRI.
2. Validar respostas OCSP locais, inclusive as presentes no DSS. O certificado
   signatário continua exigindo uma cadeia até uma CA escolhida explicitamente.
   Certificados do DSS são auxiliares e jamais viram raízes automaticamente.
3. Exportar um pedido RFC 3161 real, em DER, com SHA-256 e nonce aleatório de
   128 bits, para carimbar uma nova revisão exata do documento.
4. Importar uma resposta RFC 3161 real obtida pelo usuário e criar a cópia com
   `/Type /DocTimeStamp` e `/SubFilter /ETSI.RFC3161`. A resposta precisa
   corresponder ao nonce e ao resumo do pedido, ter assinatura válida e uma
   cadeia TSA aceita pela política explícita de CA local. A verificação é
   independente, usando OpenSSL; o destino só é publicado após as verificações.
5. Repetir o processo em documento previamente carimbado, acrescentando uma nova
   revisão. É possível incorporar material DSS antes de gerar o pedido para
   que o carimbo posterior cubra também esse material.

## Como usar na interface

Abra **Integridade de assinaturas PDF** e informe o PDF local.

**Incorporar DSS em cópia…** permite escolher vários certificados PEM/DER,
CRLs PEM/DER e respostas OCSP DER. Use **Sem estes arquivos** para uma classe
que não queira incluir. Escolha um nome novo para a cópia. A incorporação
arquiva material sintaticamente válido, sem presumir confiança nele. Depois
use **Validar com CA/CRL…** para verificar a cadeia e o estado de revogação.
Na pergunta sobre exigir revogação, é possível cancelar a seleção de CRL
adicional para usar apenas CRL/OCSP já incorporado ao DSS.

**Exportar pedido TSA…** pede o nome de uma pasta que ainda não exista e cria:

- `timestamp.tsq`: pedido DER para a TSA;
- `document.pending`: revisão preparada ainda incompleta; **não é um PDF
  carimbado utilizável**;
- `manifest.json`: hashes, offsets e identidade do PDF de origem.

O pedido contém o hash e o nonce, não o conteúdo integral do PDF. A pasta de
preparação contém uma cópia integral do documento em `document.pending` e deve
receber os mesmos cuidados de privacidade do original. A aplicação não envia
nenhum desses arquivos a serviços e não grava chaves privadas nessa pasta.

Obtenha uma **TimeStampResp DER** (`.tsr`) usando um serviço escolhido por você
ou uma TSA local. O programa não busca URL do documento nem escolhe provedores
por conta própria. Mantenha o PDF original e a pasta de preparação inalterados.

**Importar resposta TSA…** pede essa pasta, a resposta `.tsr`, o arquivo PEM
com a CA da TSA explicitamente confiável e um nome novo para a cópia final.
O botão verifica a cadeia no instante atual; a API abaixo permite políticas
mais explícitas, incluindo instante com fuso e revogação obrigatória.

Um `.der` contendo somente o token CMS não é uma TimeStampResp: esta API exige
a estrutura de resposta RFC 3161 com seu estado de concessão. Respostas negadas,
nonce ausente/divergente, resumo de outro pedido, material alterado, destino
existente ou TSA não confiável são recusados sem publicar a cópia final.

## Contratos da API e do worker

Todas as chamadas leem arquivos locais. `source_sha256` deve ser o SHA-256 do
arquivo integral atual, não apenas de sua última revisão assinada. A chave
`destination` deve indicar um nome que não exista; original e destinos antigos
nunca são sobrescritos.

### Incorporação DSS

Função `append_dss_copy(pdf, request)`; comando `signature-dss`:

```json
{
  "source_sha256": "SHA256_DO_PDF",
  "destination": "/pasta/documento-dss.pdf",
  "certificates": ["/pasta/intermediaria.pem"],
  "crls": ["/pasta/lista.crl"],
  "ocsps": ["/pasta/resposta-ocsp.der"]
}
```

Resposta `linuxit-dss-copy-v1` inclui caminho, hashes de origem e saída,
`incremental: true`, contagem final do material, `trust_assessed: false`,
`network_used: false` e `pades_lta_claimed: false`.

### Preparação do carimbo

Função `prepare_document_timestamp(pdf, request)`; comando `timestamp-prepare`:

```json
{
  "source_sha256": "SHA256_DO_PDF",
  "folder": "/pasta/novo-pedido-tsa"
}
```

Resposta `linuxit-timestamp-query-v1` identifica o `.tsq` e a pasta, com
`complete: false` e `network_used: false`. A existência do pedido ainda não
significa que o documento foi carimbado.

### Importação da resposta TSA

Função `complete_document_timestamp(pdf, request)`; comando `timestamp-complete`:

```json
{
  "source_sha256": "SHA256_DO_PDF_ORIGINAL_DA_PREPARACAO",
  "folder": "/pasta/novo-pedido-tsa",
  "response": "/pasta/resposta.tsr",
  "destination": "/pasta/documento-carimbado.pdf",
  "trust_policy": {
    "roots": ["/pasta/ca-tsa.pem"],
    "crls": [],
    "ocsps": [],
    "require_revocation": false,
    "at_time": null
  }
}
```

`ocsps` é opcional, preservando o contrato anterior da política. `at_time`
aceita ISO 8601 com fuso ou `null` para agora. O carimbo exige cadeia TSA
confiável; revogação só é obrigatória quando `require_revocation` é verdadeiro.
Não há confiança automática nas raízes do sistema operacional.

Resposta `linuxit-timestamp-copy-v1` inclui os hashes, campo novo, política
avaliada, `incremental: true`, `network_used: false` e
`pades_lta_claimed: false`. A cópia é inspecionada novamente e o novo carimbo
precisa cobrir todos os bytes do arquivo final, exceto seu próprio `/Contents`.

## Perfil de OCSP

O programa exige uma SingleResponse por resposta DER e confere serial, hash do
nome e hash da chave da emissora, assinatura do responder e instante de validade
(`thisUpdate`/`nextUpdate`, com `nextUpdate` obrigatório). Um `producedAt` mais
de cinco minutos no futuro é recusado. O instante de avaliação vem da política
local explícita, sem deduzi-lo de uma data não autenticada do PDF.

Aceita assinatura da própria emissora ou de responder diretamente delegado
por ela, com EKU `OCSPSigning`, validade temporal, uso de chave para assinatura
e extensão `OCSPNoCheck`. Sem `OCSPNoCheck`, o responder delegado exigiria uma
cadeia adicional de revogação que este perfil ainda não implementa e por isso
é recusado. A cadeia é limitada a 16 certificados, exige emissora única e
termina em uma âncora escolhida pelo usuário.

Todas as não âncoras da cadeia do signatário precisam de resposta `good`
autenticada para a revogação por OCSP ser considerada verificada. Material
ausente, inválido, desconhecido ou vencido não gera resultado positivo.
Uma resposta `revoked` válida prevalece sobre uma resposta `good` ou uma CRL
favorável e impede a satisfação da política. A confiança criptográfica da cadeia
e a revogação são relatadas separadamente.

## Limites preservados

- PDF e cópia final de até 64 MiB; item de material local de até 1 MiB;
  token TSA de até 32 KiB.
- DSS combinado de até 64 certificados, 32 CRLs e 32 respostas OCSP.
  A política aceita até 32 respostas OCSP adicionais, no máximo 64 combinadas.
- O perfil atual não modifica PDFs cifrados, XFA ou portfólios e recusa UR3
  e DocMDP P=1. Usa as guardas existentes de assinatura incremental.
- Preservar os bytes assinados garante integridade das revisões, mas não
  significa que toda alteração posterior seja permitida por uma certificação.
- Sem busca AIA, atualização automática de CRL/OCSP, transporte TSA embutido,
  seleção automática de instantes históricos ou renovação periódica automática.
- Arquivamento DSS e um carimbo de documento não provam, sozinhos, conformidade
  PAdES-B-LT/B-LTA universal nem validade jurídica de uma assinatura. Faltam
  política completa de perfis, validação de todos os históricos, retenção e
  renovação de evidências e interoperabilidade extensa com validadores externos.
- Não foi feita observação nova do Foxit, da VM ou de uma autoridade real.

## Verificação executável

`tests/test_signature_preservation.py` gera CAs, signatários, respostas OCSP e
tokens RFC 3161 sintéticos, sem usar certificados públicos ou chaves do usuário.
Os controles verificam estados OCSP, hashes e assinatura, delegação, DSS
incremental/deduplicação, preservação dos bytes antigos, recusas sem destino,
nonce, preparação alterada e importação completa com TSA explícita. A importação
completa e a confiança do CMS usam OpenSSL e precisam do ambiente Linux do CI.

```text
python scripts/run_tests.py --pattern test_signature_preservation.py --output NOVO-RESULTADO.json
```

Regressões anteriores relevantes: `test_incremental_signatures.py`,
`test_document_timestamps.py`, `test_dss_validation.py`, `test_signature_trust.py`
e `test_pdf_signatures.py`. Resultados da rodada ficam consolidados pelo agente
principal; passar neste conjunto próprio não equivale à paridade Foxit.
