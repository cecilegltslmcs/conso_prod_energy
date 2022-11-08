CREATE TABLE CONSUMPTION (
  id_consommation VARCHAR(42),
  code_insee_region VARCHAR(42),
  date_enreg DATE NOT NULL,
  heure_enreg TIME NOT NULL,
  consommation FLOAT(10),
  thermique FLOAT(10),
  nucleaire FLOAT(10),
  eolien FLOAT(10),
  solaire FLOAT(10),
  hydraulique FLOAT(10),
  pompage FLOAT(10),
  bioenergies FLOAT(10),
  production_total FLOAT(10),
  pct_thermique FLOAT(10),
  pct_nucleaire FLOAT(10),
  pct_eolien FLOAT(10),
  pct_solaire FLOAT(10),
  pct_hydraulique FLOAT(10),
  pct_pompage FLOAT(10),
  pct_bioenergies FLOAT(10),
  code_insee_1 VARCHAR(42),
  PRIMARY KEY (id_consommation)
);

CREATE TABLE COVERAGE_RATE (
  id_couverture VARCHAR(42),
  code_insee_region VARCHAR(42),
  date_enreg DATE NOT NULL,
  heure_eng TIME NOT NULL,
  tco_thermique FLOAT(10),
  tch_thermique FLOAT(10),
  tco_nucleaire FLOAT(10),
  tch_nucleaire FLOAT(10),
  tco_eolien FLOAT(10),
  tch_eolien FLOAT(10),
  tco_solaire FLOAT(10),
  tch_solaire FLOAT(10),
  tco_hydraulique FLOAT(10),
  tch_hydraulique FLOAT(10),
  tco_bioenergies FLOAT(10),
  tch_bioenergies FLOAT(10),
  code_insee_1 VARCHAR(42),
  PRIMARY KEY (id_couverture)
);

CREATE TABLE REGION (
  code_insee_region VARCHAR(42),
  libelle_region VARCHAR(42),
  PRIMARY KEY (code_insee_region)
);

ALTER TABLE CONSUMPTION ADD FOREIGN KEY (code_insee_1) REFERENCES REGION (code_insee_region);
ALTER TABLE COVERAGE_RATE ADD FOREIGN KEY (code_insee_1) REFERENCES REGION (code_insee_region);