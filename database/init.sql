CREATE TABLE terceirizados (
  id_terc INT NOT NULL,
  sg_orgao_sup_tabela_ug TEXT,
  cd_ug_gestora INT,
  nm_ug_tabela_ug TEXT,
  sg_ug_gestora TEXT,
  nr_contrato TEXT,
  nr_cnpj TEXT,
  nm_razao_social TEXT,
  nr_cpf TEXT,
  nm_terceirizado TEXT,
  nm_categoria_profissional TEXT,
  nm_escolaridade TEXT,
  nr_jornada DOUBLE PRECISION,
  nm_unidade_prestacao TEXT,
  vl_mensal_salario DOUBLE PRECISION,
  vl_mensal_custo DOUBLE PRECISION,
  sg_orgao TEXT,
  nm_orgao TEXT,
  cd_orgao_siafi TEXT,
  cd_orgao_siape TEXT,
  date DATE NOT NULL,
  PRIMARY KEY (id_terc, date)
) PARTITION BY RANGE (date);

CREATE OR REPLACE FUNCTION create_terceirizados_partitions(start_year INT, end_year INT)
RETURNS void AS $$
DECLARE
  year INT;
BEGIN
  FOR year IN start_year..end_year LOOP
    EXECUTE format('
      CREATE TABLE terceirizados_%s PARTITION OF terceirizados
      FOR VALUES FROM (''%s-01-01'') TO (''%s-01-01'');

      ALTER TABLE terceirizados_%s ADD CONSTRAINT terceirizados_%s_check
      CHECK (date >= ''%s-01-01'' AND date < ''%s-01-01'');
    ', year, year, year + 1, year, year, year, year + 1);
  END LOOP;
END;
$$ LANGUAGE plpgsql;

SELECT create_terceirizados_partitions(2019, 2025);
