from datetime import datetime
from dateutil import parser
from io import BytesIO
from typing import Final, TextIO
import logging
import os
import tempfile

from .datetime_pomes import DATETIME_FORMAT_INV
from .env_pomes import APP_PREFIX, env_get_str

LOGGING_ID: Final[str] = env_get_str(f"{APP_PREFIX}_LOGGING_ID", f"{APP_PREFIX}")
LOGGIN_FILE: Final[str] = env_get_str(f"{APP_PREFIX}_LOGGING_FILE",
                                      os.path.join(tempfile.gettempdir(), f"{APP_PREFIX}.log"))
LOGGING_MODE: Final[str] = env_get_str(f"{APP_PREFIX}_LOGGING_MODE", "a")

# define and configure the logger
PYPOMES_LOGGER: Final[logging.Logger] = logging.getLogger(LOGGING_ID)

match env_get_str(f"{APP_PREFIX}_LOGGING_LEVEL"):
    case "debug":
        LOGGING_LEVEL: Final[int] = logging.DEBUG
    case "info":
        LOGGING_LEVEL: Final[int] = logging.INFO
    case "warn":
        LOGGING_LEVEL: Final[int] = logging.WARN
    case "error":
        LOGGING_LEVEL: Final[int] = logging.ERROR
    case _:  # "critical"
        LOGGING_LEVEL: Final[int] = logging.CRITICAL

logging.basicConfig(level=LOGGING_LEVEL,
                    filename=LOGGIN_FILE,
                    filemode=LOGGING_MODE,
                    datefmt=DATETIME_FORMAT_INV,
                    style="{",
                    format="{asctime} {levelname:1.1} {thread:5d} "
                           "{module:20.20} {funcName:20.20} {lineno:3d} {message}")
for _handler in logging.root.handlers:
    _handler.addFilter(logging.Filter(LOGGING_ID))


def logging_entries(errors: list[str], log_level: str, log_from: str, log_to: str) -> BytesIO:

    def get_level(level: str) -> int:

        result: int | None
        match level:
            case None | "N" | "n":
                result = logging.NOTSET         # 0
            case "D" | "d":
                result = logging.DEBUG          # 10
            case "I" | "i":
                result = logging.INFO           # 20
            case "W" | "w":
                result = logging.WARN           # 30
            case "E" | "e":
                result = logging.ERROR          # 40
            case "C" | "c":
                result = logging.CRITICAL       # 50
            case _:
                result = None

        return result

    # inicializa variável de retorno
    result: BytesIO | None = None

    # oobtem o nível de log
    logging_level: int = get_level(log_level)
    if log_level is None:
        errors.append(f"Valor '{log_level}' do atributo 'level' inválido")

    # obtem a estampa inicial
    from_stamp: datetime | None = None
    if log_from is not None:
        from_stamp = parser.parse(log_from)
        if from_stamp is None:
            errors.append(f"Valor '{from_stamp}' do atributo 'from' inválido")

    # obtem a estampa final
    to_stamp: datetime | None = None
    if log_to is not None:
        to_stamp = parser.parse(log_to)
        if to_stamp is None or \
           (from_stamp is not None and from_stamp > to_stamp):
            errors.append(f"Valor '{to_stamp}' do atributo 'to' inválido")

    # o arquivo de log existe ?
    if not os.path.exists(LOGGIN_FILE):
        # não, reporte o erro
        errors.append(f"Arquivo '{LOGGIN_FILE}' não encontrado")

    # houve erro ?
    if len(errors) == 0:
        # não, prossiga
        result = BytesIO()
        with open(LOGGIN_FILE, "r") as f:
            line: str = f.readline()
            while line:
                items: list[str] = line.split(maxsplit=3)
                level: int = get_level(items[2])
                if level >= logging_level:
                    timestamp: datetime = parser.parse(f"{items[0]} {items[1]}")
                    if (from_stamp is None or timestamp >= from_stamp) and \
                       (to_stamp is None or timestamp <= to_stamp):
                        result.write(line.encode())
                line = f.readline()

    return result


def log_errors(errors: list[str], output_dev: TextIO = None):
    """
    Escreve no *logger*, e opcionalmente, em *output_dev*
    (tipicamente, *sys.stdout* ou *sys.stderr*), os erros em *errors*.

    :param errors: a lista de erros
    :param output_dev: dispositivo de saída onde o erro deve ser impresso
    """
    # percorre a lista de erros
    for error in errors:
        # escreve o erro no log
        PYPOMES_LOGGER.error(error)

        # o dispositivo de saída foi definido ?
        if output_dev is not None:
            # sim, escreva o erro nesse dispositivo
            output_dev.write(error)

            # o dispositivo de saída é 'stderr' ou 'stdout' ?
            if output_dev.name.startswith("<std"):
                # sim, mude de linha
                output_dev.write("\n")
