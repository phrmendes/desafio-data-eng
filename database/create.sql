CREATE TABLE IF NOT EXISTS terceirizados (
  id_terc INT NOT NULL,
  sg_orgao_sup_tabela_ug VARCHAR,
  cd_ug_gestora INT,
  nm_ug_tabela_ug VARCHAR,
  sg_ug_gestora VARCHAR,
  nr_contrato VARCHAR,
  nr_cnpj VARCHAR,
  nm_razao_social VARCHAR,
  nr_cpf VARCHAR,
  nm_terceirizado VARCHAR,
  nm_categoria_profissional VARCHAR,
  nm_escolaridade VARCHAR,
  nr_jornada NUMERIC,
  nm_unidade_prestacao VARCHAR,
  vl_mensal_salario NUMERIC,
  vl_mensal_custo NUMERIC,
  sg_orgao VARCHAR,
  nm_orgao VARCHAR,
  cd_orgao_siafi VARCHAR,
  cd_orgao_siape VARCHAR,
  date DATE,
  PRIMARY KEY (id_terc, date)
);