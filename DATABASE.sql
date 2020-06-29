-- phpMyAdmin SQL Dump
-- version 4.8.5
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Creato il: Giu 29, 2020 alle 12:41
-- Versione del server: 8.0.13-4
-- Versione PHP: 7.2.24-0ubuntu0.18.04.6

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `LsRISZ5PFW`
--

-- --------------------------------------------------------

--
-- Struttura della tabella `articolo`
--

CREATE TABLE `articolo` (
  `id_art` int(11) NOT NULL,
  `cod_art` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `desc_art` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `cli_art` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `cod_cli_art` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `kit_art` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `data_art` timestamp NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Struttura della tabella `articolo_componenti`
--

CREATE TABLE `articolo_componenti` (
  `id_artcomp` int(11) NOT NULL,
  `id_art` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `id_comp` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `qt_comp` int(11) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Struttura della tabella `backup_riga_dett`
--

CREATE TABLE `backup_riga_dett` (
  `id_backup` int(11) NOT NULL,
  `id_riga_dett_b` int(11) NOT NULL,
  `id_riga_imp_b` int(11) NOT NULL,
  `id_comp_b` int(11) NOT NULL,
  `qt_comp_b` int(11) NOT NULL,
  `id_produzione_b` int(11) NOT NULL,
  `pos_comp_imp_b` varchar(50) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `data_b` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `cod_ordine_b` varchar(50) CHARACTER SET utf8 COLLATE utf8_unicode_ci DEFAULT NULL,
  `scadenza_b` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT;

-- --------------------------------------------------------

--
-- Struttura della tabella `backup_riga_imp_comp`
--

CREATE TABLE `backup_riga_imp_comp` (
  `id_backup_comp` int(11) NOT NULL,
  `id_riga_imp_comp_b` int(11) NOT NULL,
  `id_imp_b` int(11) NOT NULL,
  `id_comp_b` int(11) NOT NULL,
  `qt_comp_b` int(11) NOT NULL,
  `data_cons_comp_b` timestamp NOT NULL,
  `id_produzione_b` int(11) NOT NULL,
  `pos_comp_sing_imp_b` varchar(50) CHARACTER SET utf8 COLLATE utf8_unicode_ci DEFAULT NULL,
  `cod_ordine_b` varchar(50) CHARACTER SET utf8 COLLATE utf8_unicode_ci DEFAULT NULL,
  `scadenza_b` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT;

-- --------------------------------------------------------

--
-- Struttura della tabella `componente`
--

CREATE TABLE `componente` (
  `id_comp` int(11) NOT NULL,
  `cod_comp` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `grezzo` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `desc_comp` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `dim_comp` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `mat_comp` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `pos_comp` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `data_comp` timestamp NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Struttura della tabella `impegno`
--

CREATE TABLE `impegno` (
  `id_imp` int(11) NOT NULL,
  `cod_imp` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `cliente` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `cod_ord_cli` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `data_ord` timestamp NULL DEFAULT NULL,
  `data_comp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Struttura della tabella `riga_dett`
--

CREATE TABLE `riga_dett` (
  `id_riga_dett` int(11) NOT NULL,
  `id_riga_imp` int(11) NOT NULL,
  `id_comp` int(11) NOT NULL,
  `qt_comp` int(11) NOT NULL,
  `id_produzione` int(11) NOT NULL,
  `pos_comp_imp` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '0',
  `cod_ordine` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `scadenza` timestamp NULL DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Struttura della tabella `riga_imp`
--

CREATE TABLE `riga_imp` (
  `id_riga_imp` int(11) NOT NULL,
  `id_imp` int(11) NOT NULL,
  `id_art` int(11) NOT NULL,
  `qt_art` int(11) NOT NULL,
  `data_cons_art` timestamp NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Struttura della tabella `riga_imp_comp_AFK`
--

CREATE TABLE `riga_imp_comp_AFK` (
  `id_riga_imp_comp` int(11) NOT NULL,
  `id_imp` int(11) NOT NULL,
  `id_comp` int(11) NOT NULL,
  `qt_comp` int(11) NOT NULL,
  `data_cons_comp` timestamp NOT NULL,
  `id_produzione` int(11) NOT NULL,
  `pos_comp_sing_imp` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT '0',
  `cod_ordine` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `scadenza` timestamp NULL DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

--
-- Indici per le tabelle scaricate
--

--
-- Indici per le tabelle `articolo`
--
ALTER TABLE `articolo`
  ADD PRIMARY KEY (`id_art`),
  ADD UNIQUE KEY `cod_art` (`cod_art`);

--
-- Indici per le tabelle `articolo_componenti`
--
ALTER TABLE `articolo_componenti`
  ADD PRIMARY KEY (`id_artcomp`),
  ADD UNIQUE KEY `id_art` (`id_art`,`id_comp`);

--
-- Indici per le tabelle `backup_riga_dett`
--
ALTER TABLE `backup_riga_dett`
  ADD PRIMARY KEY (`id_backup`),
  ADD UNIQUE KEY `id_riga_dett_b` (`id_riga_dett_b`,`id_produzione_b`);

--
-- Indici per le tabelle `backup_riga_imp_comp`
--
ALTER TABLE `backup_riga_imp_comp`
  ADD PRIMARY KEY (`id_backup_comp`),
  ADD UNIQUE KEY `id_riga_imp_comp_b` (`id_riga_imp_comp_b`,`id_produzione_b`);

--
-- Indici per le tabelle `componente`
--
ALTER TABLE `componente`
  ADD PRIMARY KEY (`id_comp`),
  ADD UNIQUE KEY `cod_comp` (`cod_comp`);

--
-- Indici per le tabelle `impegno`
--
ALTER TABLE `impegno`
  ADD PRIMARY KEY (`id_imp`),
  ADD UNIQUE KEY `cod_imp` (`cod_imp`);

--
-- Indici per le tabelle `riga_dett`
--
ALTER TABLE `riga_dett`
  ADD PRIMARY KEY (`id_riga_dett`),
  ADD UNIQUE KEY `id_riga_imp` (`id_riga_imp`,`id_comp`);

--
-- Indici per le tabelle `riga_imp`
--
ALTER TABLE `riga_imp`
  ADD PRIMARY KEY (`id_riga_imp`);

--
-- Indici per le tabelle `riga_imp_comp_AFK`
--
ALTER TABLE `riga_imp_comp_AFK`
  ADD PRIMARY KEY (`id_riga_imp_comp`);

--
-- AUTO_INCREMENT per le tabelle scaricate
--

--
-- AUTO_INCREMENT per la tabella `articolo`
--
ALTER TABLE `articolo`
  MODIFY `id_art` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT per la tabella `articolo_componenti`
--
ALTER TABLE `articolo_componenti`
  MODIFY `id_artcomp` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT per la tabella `backup_riga_dett`
--
ALTER TABLE `backup_riga_dett`
  MODIFY `id_backup` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT per la tabella `backup_riga_imp_comp`
--
ALTER TABLE `backup_riga_imp_comp`
  MODIFY `id_backup_comp` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT per la tabella `componente`
--
ALTER TABLE `componente`
  MODIFY `id_comp` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT per la tabella `impegno`
--
ALTER TABLE `impegno`
  MODIFY `id_imp` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT per la tabella `riga_dett`
--
ALTER TABLE `riga_dett`
  MODIFY `id_riga_dett` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT per la tabella `riga_imp`
--
ALTER TABLE `riga_imp`
  MODIFY `id_riga_imp` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT per la tabella `riga_imp_comp_AFK`
--
ALTER TABLE `riga_imp_comp_AFK`
  MODIFY `id_riga_imp_comp` int(11) NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
