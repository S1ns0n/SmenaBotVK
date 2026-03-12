from database.database import AsyncTinyDBManager
from database.google_table import TinyDBToGoogleSheetsExporter
from config import Config

db_manager = AsyncTinyDBManager("anketas.json")

exporter = TinyDBToGoogleSheetsExporter(
    db_manager=db_manager,
    credentials_file=Config.GOOGLE_CRED_PATH,
    sheet_name=Config.GOOGLE_TABLE_NAME
)