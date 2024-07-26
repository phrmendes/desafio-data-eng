{{ config(materialized='table') }}

WITH desafio AS (
    SELECT
      id_terc,
      sg_orgao,
      nr_cnpj,
      nr_jornada,
      date
    FROM
      terceirizados
)

SELECT *
FROM desafio
