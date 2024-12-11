CAMPOS:

- numero
- descrição
- setor do responsavel
- campus da carga
- valor aquisicao
- valor depreciado
- data da entrada
- data da carga
- fornecedor
- estado de conservacao

ENTIDADES

- Equipamento
- Fornecedor
- Setor
- Campus

RELACIONAMENTO

- Equipamento -> setor (n:n)
- Equipamento -> fornecedor (n:1)
- Fornecedor -> campus (n:n)