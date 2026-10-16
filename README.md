# Linuxit PDF

Projeto de leitor de PDF com prioridade para Linux e distribuição em Flatpak,
com uma implementação própria que permita suporte posterior ao Windows.

A etapa atual é a investigação do **Foxit Reader com REA e Ghidra**. O relatório
registra resultados verificáveis, contratos propostos e lacunas por funcionalidade.
Este repositório ainda não contém um leitor completo nem um pacote Flatpak.

- [Relatório da engenharia reversa do Foxit](docs/FOXIT-REA.md)
- [Mapas, identidades e validações](docs/windows-evidence/foxit-rea/)
- [Ferramentas próprias de análise](scripts/)

Foram examinadas 122 entradas de funções pelo REA/Ghidra em quatro módulos,
com verificações complementares no backend Ghidra. O inventário inclui 141
módulos, 869 recursos externos de interface/tradução e 9.973 registros internos
de chamadas. Registros, textos e funções decompiladas não equivalem a
funcionalidades inteiramente reconstruídas ou testadas.

As ferramentas analisam arquivos locais sem executar o Foxit. Os binários de
referência, templates completos, bases Ghidra e decompilações permanecem fora
deste repositório. A futura implementação deve usar os contratos de comportamento
e validação independente, sem incorporar código ou recursos proprietários.

Para reproduzir a análise, consulte as instruções e os hashes no relatório.
