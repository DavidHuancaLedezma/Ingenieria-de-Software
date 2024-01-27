
import mysql.connector
from mysql.connector import errorcode

def create_tables(cursor):
    TABLES = {}
    TABLES['administrador'] = '''
        CREATE TABLE `administrador` (
          `idAdministrador` int(11) NOT NULL,
          `ci` varchar(45) COLLATE latin1_swedish_ci NOT NULL,
          `Elector_ci` int(11) NOT NULL,
          PRIMARY KEY (`idAdministrador`),
          INDEX `fk_Administrador_Elector1_idx` (`Elector_ci`),
          CONSTRAINT `fk_Administrador_Elector1` FOREIGN KEY (`Elector_ci`) REFERENCES `elector` (`ci`) ON DELETE NO ACTION ON UPDATE NO ACTION
        ) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
    '''

    TABLES['candidato'] = '''
        CREATE TABLE `candidato` (
          `idCandidato` int(11) NOT NULL,
          `ci` varchar(45) COLLATE latin1_swedish_ci NOT NULL,
          `nombrePP` varchar(45) COLLATE latin1_swedish_ci DEFAULT NULL,
          `siglaPP` varchar(45) COLLATE latin1_swedish_ci DEFAULT NULL,
          PRIMARY KEY (`idCandidato`)
        ) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
    '''

    TABLES['corteelectoral'] = '''
        CREATE TABLE `corteelectoral` (
          `idCorteElectoral` int(11) NOT NULL,
          `ci` varchar(45) COLLATE latin1_swedish_ci DEFAULT NULL,
          `Elector_ci` int(11) NOT NULL,
          PRIMARY KEY (`idCorteElectoral`),
          INDEX `fk_CorteElectoral_Elector1_idx` (`Elector_ci`),
          CONSTRAINT `fk_CorteElectoral_Elector1` FOREIGN KEY (`Elector_ci`) REFERENCES `elector` (`ci`) ON DELETE NO ACTION ON UPDATE NO ACTION
        ) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
    '''

    TABLES['cuenta'] = '''
        CREATE TABLE `cuenta` (
          `idcuenta` int(11) NOT NULL,
          `ci` varchar(45) COLLATE latin1_swedish_ci DEFAULT NULL,
          `contrase;a` varchar(45) COLLATE latin1_swedish_ci DEFAULT NULL,
          `votos_idvotos` int(10) UNSIGNED ZEROFILL NOT NULL,
          PRIMARY KEY (`idcuenta`),
          INDEX `fk_cuenta_votos1_idx` (`votos_idvotos`),
          CONSTRAINT `fk_cuenta_votos1` FOREIGN KEY (`votos_idvotos`) REFERENCES `votos` (`idvotos`) ON DELETE NO ACTION ON UPDATE NO ACTION
        ) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
    '''

    TABLES['elector'] = '''
        CREATE TABLE `elector` (
          `ci` int(11) NOT NULL,
          `nombre` varchar(45) COLLATE latin1_swedish_ci DEFAULT NULL,
          `foto` blob DEFAULT NULL,
          `fechaN` date DEFAULT NULL,
          `genero` tinyint(1) DEFAULT NULL,
          `estado` tinyint(1) DEFAULT NULL,
          `Candidato_idCandidato` int(11) NOT NULL,
          `cuenta_idcuenta` int(11) NOT NULL,
          PRIMARY KEY (`ci`),
          INDEX `fk_Elector_Candidato1_idx` (`Candidato_idCandidato`),
          INDEX `fk_Elector_cuenta1_idx` (`cuenta_idcuenta`),
          CONSTRAINT `fk_Elector_Candidato1` FOREIGN KEY (`Candidato_idCandidato`) REFERENCES `candidato` (`idCandidato`) ON DELETE NO ACTION ON UPDATE NO ACTION,
          CONSTRAINT `fk_Elector_cuenta1` FOREIGN KEY (`cuenta_idcuenta`) REFERENCES `cuenta` (`idcuenta`) ON DELETE NO ACTION ON UPDATE NO ACTION
        ) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
    '''

    TABLES['resultados'] = '''
        CREATE TABLE `resultados` (
          `idResultados` int(11) NOT NULL,
          `idvotos` varchar(45) COLLATE latin1_swedish_ci DEFAULT NULL,
          `candidato1` int(11) DEFAULT NULL,
          `candidato2` int(11) DEFAULT NULL,
          `nulo` int(11) DEFAULT NULL,
          `blanco` int(11) DEFAULT NULL,
          PRIMARY KEY (`idResultados`)
        ) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
    '''

    TABLES['votos'] = '''
        CREATE TABLE `votos` (
          `idvotos` int(10) UNSIGNED ZEROFILL NOT NULL,
          `idcuenta` int(11) DEFAULT NULL,
          `voto` varchar(45) COLLATE latin1_swedish_ci DEFAULT NULL,
          `Resultados_idResultados` int(11) NOT NULL,
          PRIMARY KEY (`idvotos`),
          INDEX `fk_votos_Resultados1_idx` (`Resultados_idResultados`),
          CONSTRAINT `fk_votos_Resultados1` FOREIGN KEY (`Resultados_idResultados`) REFERENCES `resultados` (`idResultados`) ON DELETE NO ACTION ON UPDATE NO ACTION
        ) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
    '''

    for table_name, table_sql in TABLES.items():
        try:
            print('Creando tabla {}:'.format(table_name), end=' ')
            cursor.execute(table_sql)
            print('OK')
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print('La tabla ya existe')
            else:
                print(err.msg)

def insert_data(cursor):
    # Insertar datos y realizar otras operaciones de inserción aquí
    pass

print("Conectando...")
try:
    conn = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password='root'
    )
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print('Existe un error en el nombre de usuario o en la clave')
    else:
        print(err)

cursor = conn.cursor()

cursor.execute("DROP DATABASE IF EXISTS `NahuelQuirozPere$default`;")
cursor.execute("CREATE DATABASE `NahuelQuirozPere$default`;")
cursor.execute("USE `NahuelQuirozPere$default`;")

create_tables(cursor)
insert_data(cursor)

# commitando si no hay nada que tenga efecto
conn.commit()

cursor.close()
conn.close()
