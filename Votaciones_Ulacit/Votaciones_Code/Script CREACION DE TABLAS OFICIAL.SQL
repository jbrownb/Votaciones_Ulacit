

DROP DATABASE votaciones_ulacit;

CREATE DATABASE votaciones_ulacit;

USE  votaciones_ulacit;


CREATE TABLE `catalogo_facultad`
(
  `ID_FACULTAD` Int(5) NOT NULL,
  `Descripcion` Varchar(30) NOT NULL
)
;

ALTER TABLE `catalogo_facultad` ADD  PRIMARY KEY (`ID_FACULTAD`)
;

-- Table t_estudiante

CREATE TABLE `t_estudiante`
(
  `ID_ESTUDIANTE` Varchar(17) NOT NULL,
  `PRIMER_APELLIDO` Varchar(20) NOT NULL,
  `SEGUNDO_APELLIDO` Varchar(20),
  `NOMBRE` Varchar(41) NOT NULL,
  `GENERO` Varchar(1),
  `FECHA_NACIMIENTO` Date,
  `CORREO` Varchar(100)
)
;

ALTER TABLE `t_estudiante` ADD  PRIMARY KEY (`ID_ESTUDIANTE`)
;

-- Table T_fiscal

CREATE TABLE `T_fiscal`
(
  `ID_FISCAL` Varchar(17) NOT NULL,
  `CONTRASENA` Varchar(8) NOT NULL
)
;

ALTER TABLE `T_fiscal` ADD  PRIMARY KEY (`ID_FISCAL`)
;

-- Table catalogo_escuela

CREATE TABLE `catalogo_escuela`
(
  `ID_ESCUELA` Int(5) NOT NULL,
  `ESCUELA` Varchar(40) NOT NULL,
  `ID_FACULTAD` Int(5) NOT NULL
)
;

CREATE INDEX `IX_Relationship21` ON `catalogo_escuela` (`ID_FACULTAD`)
;

ALTER TABLE `catalogo_escuela` ADD  PRIMARY KEY (`ID_ESCUELA`)
;

-- Table catalogo_plan

CREATE TABLE `catalogo_plan`
(
  `ID_PLAN` Varchar(7) NOT NULL,
  `DESCRIPCION_PLAN` Varchar(100) NOT NULL,
  `ID_ESCUELA` Int(5) NOT NULL
)
;

CREATE INDEX `IX_Relationship22` ON `catalogo_plan` (`ID_ESCUELA`)
;

ALTER TABLE `catalogo_plan` ADD  PRIMARY KEY (`ID_PLAN`)
;

-- Table t_bitacora

CREATE TABLE `t_bitacora`
(
  `ID_ESCUELA` Int(5) NOT NULL,
  `ID_ESTUDIANTE` Varchar(17) NOT NULL,
  `FECHA_HORA` Datetime NOT NULL,
  `ID_FISCAL` Varchar(17) NOT NULL,
  `ESTADO_VOTO` Varchar(20)
)
;

CREATE INDEX `IX_Relationship28` ON `t_bitacora` (`ID_FISCAL`)
;

ALTER TABLE `t_bitacora` ADD  PRIMARY KEY (`ID_ESCUELA`,`ID_ESTUDIANTE`)
;

-- Table t_voto

CREATE TABLE `t_voto`
(
  `ID_VOTO` Int(11) NOT NULL AUTO_INCREMENT,
  `ID_PARTIDO` Int(5) NOT NULL,
  PRIMARY KEY (`ID_VOTO`)
)
;

CREATE INDEX `IX_Relationship13` ON `t_voto` (`ID_PARTIDO`)
;

-- Table t_partido

CREATE TABLE `t_partido`
(
  `ID_PARTIDO` Int(5) NOT NULL,
  `NOMBRE_PARTIDO` Varchar(100) NOT NULL,
  `ID_ESCUELA` Int(5) NOT NULL,
  `CANTIDAD_VOTOS` Int,
  `SIGLAS` Varchar(10)
)
;

CREATE INDEX `IX_Relationship26` ON `t_partido` (`ID_ESCUELA`)
;

ALTER TABLE `t_partido` ADD  PRIMARY KEY (`ID_PARTIDO`)
;

-- Table t_candidato

CREATE TABLE `t_candidato`
(
  `ID_ESTUDIANTE` Varchar(17) NOT NULL,
  `ID_PARTIDO` Int(5) NOT NULL,
  `FOTO` Varchar(100)
)
;

ALTER TABLE `t_candidato` ADD  PRIMARY KEY (`ID_ESTUDIANTE`,`ID_PARTIDO`)
;

-- Table plan_estudiante

CREATE TABLE `plan_estudiante`
(
  `ID_ESTUDIANTE` Varchar(17) NOT NULL,
  `ID_PLAN` Varchar(7) NOT NULL
)
;

ALTER TABLE `plan_estudiante` ADD  PRIMARY KEY (`ID_ESTUDIANTE`,`ID_PLAN`)
;

-- Table fiscal_activo

CREATE TABLE `fiscal_activo`
(
  `ID_FISCAL_ACTIVO` Int(3) NOT NULL,
  `ID_FISCAL` Varchar(17) NOT NULL
)
;

CREATE INDEX `IX_Relationship30` ON `fiscal_activo` (`ID_FISCAL`)
;

ALTER TABLE `fiscal_activo` ADD  PRIMARY KEY (`ID_FISCAL_ACTIVO`)
;

ALTER TABLE `fiscal_activo` ADD UNIQUE `Attribute1` (`ID_FISCAL_ACTIVO`)
;

-- Table Periodo_Votacion

CREATE TABLE `Periodo_Votacion`
(
  `ID_PERIODO` Int(4) NOT NULL,
  `Inicio_Votacion` Datetime NOT NULL,
  `Fin_Votacion` Datetime NOT NULL
)
;

ALTER TABLE `Periodo_Votacion` ADD  PRIMARY KEY (`ID_PERIODO`)
;

-- Create relationships section ------------------------------------------------- 

ALTER TABLE `plan_estudiante` ADD CONSTRAINT `Rel_IDPla_PlEst_Pla` FOREIGN KEY (`ID_PLAN`) REFERENCES `catalogo_plan` (`ID_PLAN`) ON DELETE RESTRICT ON UPDATE RESTRICT
;

ALTER TABLE `plan_estudiante` ADD CONSTRAINT `Rel_IDEst_PlEst_Est` FOREIGN KEY (`ID_ESTUDIANTE`) REFERENCES `t_estudiante` (`ID_ESTUDIANTE`) ON DELETE RESTRICT ON UPDATE RESTRICT
;

ALTER TABLE `t_voto` ADD CONSTRAINT `Rel_IDpar_Vot_Par` FOREIGN KEY (`ID_PARTIDO`) REFERENCES `t_partido` (`ID_PARTIDO`) ON DELETE RESTRICT ON UPDATE RESTRICT
;

ALTER TABLE `t_fiscal` ADD CONSTRAINT `Rel_IDFis_Fis_Est` FOREIGN KEY (`ID_FISCAL`) REFERENCES `t_estudiante` (`ID_ESTUDIANTE`) ON DELETE RESTRICT ON UPDATE RESTRICT
;

ALTER TABLE `t_candidato` ADD CONSTRAINT `Rel_IDest_Can_Est` FOREIGN KEY (`ID_ESTUDIANTE`) REFERENCES `t_estudiante` (`ID_ESTUDIANTE`) ON DELETE RESTRICT ON UPDATE RESTRICT
;

ALTER TABLE `t_bitacora` ADD CONSTRAINT `Rel_IDest_Bit_Est` FOREIGN KEY (`ID_ESTUDIANTE`) REFERENCES `t_estudiante` (`ID_ESTUDIANTE`) ON DELETE RESTRICT ON UPDATE RESTRICT
;

ALTER TABLE `t_bitacora` ADD CONSTRAINT `Rel_IDesc_Bit_Esc` FOREIGN KEY (`ID_ESCUELA`) REFERENCES `catalogo_escuela` (`ID_ESCUELA`) ON DELETE RESTRICT ON UPDATE RESTRICT
;

ALTER TABLE `catalogo_escuela` ADD CONSTRAINT `Rel_IDfac_Esc_Fac` FOREIGN KEY (`ID_FACULTAD`) REFERENCES `catalogo_facultad` (`ID_FACULTAD`) ON DELETE RESTRICT ON UPDATE RESTRICT
;

ALTER TABLE `catalogo_plan` ADD CONSTRAINT `Re_IDEsc_Plan_Esc` FOREIGN KEY (`ID_ESCUELA`) REFERENCES `catalogo_escuela` (`ID_ESCUELA`) ON DELETE RESTRICT ON UPDATE RESTRICT
;

ALTER TABLE `t_partido` ADD CONSTRAINT `Rel_IDesc_Par_Esc` FOREIGN KEY (`ID_ESCUELA`) REFERENCES `catalogo_escuela` (`ID_ESCUELA`) ON DELETE RESTRICT ON UPDATE RESTRICT
;

ALTER TABLE `t_bitacora` ADD CONSTRAINT `Rel_IDFis_bit_fis` FOREIGN KEY (`ID_FISCAL`) REFERENCES `T_fiscal` (`ID_FISCAL`) ON DELETE RESTRICT ON UPDATE RESTRICT
;

ALTER TABLE `fiscal_activo` ADD CONSTRAINT `Rel_IDFISCAL_FISACT_FISCA` FOREIGN KEY (`ID_FISCAL`) REFERENCES `T_fiscal` (`ID_FISCAL`) ON DELETE RESTRICT ON UPDATE RESTRICT
;

COMMIT;

