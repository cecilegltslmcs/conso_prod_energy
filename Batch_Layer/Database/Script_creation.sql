CREATE TABLE CONSUMPTION (
  id_consommation VARCHAR(42),
  code_insee VARCHAR(42),
  date_enreg VARCHAR(42),
  heure_enreg VARCHAR(42),
  consommation VARCHAR(42),
  thermique VARCHAR(42),
  nucleaire VARCHAR(42),
  eolien VARCHAR(42),
  solaire VARCHAR(42),
  hydraulique VARCHAR(42),
  pompage VARCHAR(42),
  bioenergies VARCHAR(42),
  pct_thermique VARCHAR(42),
  pct_nucleaire VARCHAR(42),
  pct_eolien VARCHAR(42),
  pct_solaire VARCHAR(42),
  pct_hydraulique VARCHAR(42),
  pct_pompage VARCHAR(42),
  pct_bioenergies VARCHAR(42),
  code_insee_1 VARCHAR(42),
  PRIMARY KEY (id_consommation)
);

CREATE TABLE COVERAGE_RATE (
  id_couverture VARCHAR(42),
  code_insee VARCHAR(42),
  date_enreg VARCHAR(42),
  heure_eng VARCHAR(42),
  tco_thermique VARCHAR(42),
  tch_thermique VARCHAR(42),
  tco_nucleaire VARCHAR(42),
  tch_nucleaire VARCHAR(42),
  tco_eolien VARCHAR(42),
  tch_eolien VARCHAR(42),
  tco_solaire VARCHAR(42),
  tch_solaire VARCHAR(42),
  tco_hydraulique VARCHAR(42),
  tch_hydraulique VARCHAR(42),
  tco_bioenergies VARCHAR(42),
  tch_bioenergies VARCHAR(42),
  code_insee_1 VARCHAR(42),
  PRIMARY KEY (id_couverture)
);

CREATE TABLE REGION (
  code_insee VARCHAR(42),
  libelle_region VARCHAR(42),
  PRIMARY KEY (code_insee)
);

ALTER TABLE CONSUMPTION ADD FOREIGN KEY (code_insee_1) REFERENCES REGION (code_insee);
ALTER TABLE COVERAGE_RATE ADD FOREIGN KEY (code_insee_1) REFERENCES REGION (code_insee);