/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

INSERT IGNORE INTO `auditoria_equipamento` (`ID_Log`, `ID_Equipamento`, `Status_Antigo`, `Status_Novo`, `Data_Alteracao`) VALUES
	(1, 4, 'Inativo', 'Ativo', '2024-12-10 23:37:56');

INSERT IGNORE INTO `campus` (`ID_Campus`, `Nome_Campus`, `Endereco`) VALUES
	(7, 'Ceará', 'Lá no Ceará');

INSERT IGNORE INTO `edificio_setor_campus` (`ID_Campus`, `ID_Setor`) VALUES
	(7, 3);

INSERT IGNORE INTO `equipamento` (`ID_Equipamento`, `Descricao`, `Status`, `Estado_Conservacao`, `Valor_Aquisicao`, `Valor_Depreciado`, `Numero_Nota_Fiscal`, `Numero_de_serie`) VALUES
	(4, 'ROBO MASTER BLASTER', 'Ativo', 'Recuperável', 25, 10, '123465', '12345'),
	(5, 'aaa', 'Ativo', 'Recuperável', 5, 8, '342342', '2342342'),
	(6, 'TESTE', 'Inativo', 'Recuperável', 5, 1, '12345', '123131'),
	(7, 'asas', 'Inativo', 'Recuperável', 9, 2, '12345', '12345'),
	(8, 'asdasda', 'Inativo', 'Bom', 3, 0.5, '1234567', '1231453'),
	(9, '12313', 'Inativo', 'Recuperável', 5, 0.5, '79696', '78676'),
	(10, 'sdasd', 'Ativo', 'Irrecuperável', 3, 8, '95796', '89678967'),
	(11, '42342', 'Inativo', 'Bom', 4, 2, '1322456', '3454646'),
	(12, 'teste', 'Ativo', 'Recuperável', 12, 2, '1234556', '456464'),
	(13, 'SUPER ROBO MASTER BLASTER', 'Ativo', 'Bom', 1000000, 0, '0', '0'),
	(14, 'SUPER MEGA HIPER ROBO MASTER BLASTER DA MORTE', 'Ativo', 'Irrecuperável', 100000000, 100000000, '666', '6969'),
	(15, 'computador', 'Ativo', 'Bom', 10, 20, '1243412', '123131');

INSERT IGNORE INTO `equipamento_setor` (`ID_Setor`, `ID_Equipamento`, `Data_Alocacao`, `Tempo_Alocacao`, `Observacao`) VALUES
	(4, 4, '2024-12-11', 'Indefinido', NULL),
	(5, 11, NULL, NULL, NULL),
	(3, 12, NULL, NULL, NULL),
	(4, 12, NULL, NULL, NULL),
	(5, 12, NULL, NULL, NULL);

INSERT IGNORE INTO `fornecedor` (`ID_Fornecedor`, `Nome_Fornecedor`, `Contato`) VALUES
	(1, 'Enzo da Rosa Veroneze', '132123');

INSERT IGNORE INTO `fornecedor_campus` (`ID_Fornecedor`, `ID_Campus`, `Regiao_Atendida`, `Data_Contrato`) VALUES
	(1, 7, 'Ceará', '2028-10-03');

INSERT IGNORE INTO `sala` (`ID_Sala`, `Nome`) VALUES
	(1, '334'),
	(2, '321'),
	(3, '337'),
	(4, '337'),
	(5, '334'),
	(6, '123');

INSERT IGNORE INTO `setor` (`ID_Setor`, `Nome_Setor`, `Responsavel`, `Total_Equipamentos`) VALUES
	(3, '74C', 'Caio', 1),
	(4, '232', 'Dada', 2),
	(5, 'NCC', 'Rafael', 2),
	(6, '123', '1231', 0),
	(7, 'asda', 'asda', 0);

INSERT IGNORE INTO `setor_sala` (`ID_Setor`, `ID_Sala`) VALUES
	(7, 1),
	(7, 2);

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
