import gspread
from oauth2client.service_account import ServiceAccountCredentials
from typing import Dict, List, Any, Set
import asyncio
from datetime import datetime
import logging


class TinyDBToGoogleSheetsExporter:
    """
    Класс для экспорта данных из TinyDB в Google Таблицы с группировкой по peer_id
    """

    def __init__(self, db_manager, credentials_file: str, sheet_name: str):
        """
        Инициализация экспортера

        Args:
            db_manager: экземпляр AsyncTinyDBManager
            credentials_file: путь к JSON файлу с учетными данными Google Service Account
            sheet_name: название Google таблицы
        """
        self.db_manager = db_manager
        self.credentials_file = credentials_file
        self.sheet_name = sheet_name
        self.client = None
        self.sheet = None
        self.setup_logging()

    def setup_logging(self):
        """Настройка логирования"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    def authenticate_google_sheets(self):
        """Аутентификация в Google Sheets API"""
        try:
            scope = [
                'https://www.googleapis.com/auth/spreadsheets',
                'https://www.googleapis.com/auth/drive'
            ]

            creds = ServiceAccountCredentials.from_json_keyfile_name(
                self.credentials_file, scope
            )

            self.client = gspread.authorize(creds)
            self.logger.info("Успешная аутентификация в Google Sheets")

        except Exception as e:
            self.logger.error(f"Ошибка аутентификации: {e}")
            raise

    def open_or_create_sheet(self):
        """Открывает существующую или создает новую таблицу"""
        try:
            self.sheet = self.client.open(self.sheet_name).sheet1
            self.logger.info(f"Открыта существующая таблица: {self.sheet_name}")
        except gspread.SpreadsheetNotFound:
            self.sheet = self.client.create(self.sheet_name).sheet1
            self.logger.info(f"Создана новая таблица: {self.sheet_name}")

    async def collect_all_user_data(self) -> Dict[int, Dict[str, Any]]:
        """
        Собирает все данные из БД, группируя по peer_id

        Returns:
            Словарь вида {peer_id: {тип_анкеты: данные, ...}}
        """
        db = await self.db_manager._get_db()
        all_records = db.all()

        user_data = {}

        for record in all_records:
            peer_id = record.get("peer_id")
            if not peer_id:
                continue

            if peer_id not in user_data:
                user_data[peer_id] = {
                    "anketas": {},
                    "statuses": [],
                    "timestamps": []
                }

            if "anketa_type" in record:
                anketa_type = record["anketa_type"]
                user_data[peer_id]["anketas"][anketa_type] = {
                    "data": record.get("data", {}),
                    "timestamp": record.get("timestamp", "")
                }
                user_data[peer_id]["timestamps"].append(record.get("timestamp", ""))

            elif record.get("status_type") == "user_status":
                user_data[peer_id]["statuses"].append({
                    "status": record.get("status"),
                    "timestamp": record.get("timestamp", "")
                })

        return user_data

    def get_all_question_keys(self, user_data: Dict[int, Dict[str, Any]]) -> Dict[str, List[str]]:
        """
        Собирает все уникальные ключи вопросов для каждого типа анкеты

        Returns:
            Словарь вида {тип_анкеты: [список_вопросов]}
        """
        question_keys = {}

        for peer_data in user_data.values():
            for anketa_type, anketa_info in peer_data["anketas"].items():
                if anketa_type not in question_keys:
                    question_keys[anketa_type] = set()

                if isinstance(anketa_info["data"], dict):
                    # Добавляем все ключи из этой анкеты
                    question_keys[anketa_type].update(anketa_info["data"].keys())

        # Преобразуем множества в отсортированные списки
        return {
            anketa_type: sorted(list(keys))
            for anketa_type, keys in question_keys.items()
        }

    def flatten_user_data_detailed(self, user_data: Dict[int, Dict[str, Any]]) -> List[List[Any]]:
        """
        Детальное представление - каждая анкета в отдельной строке,
        каждый вопрос в отдельном столбце

        Returns:
            Список строк для Google Sheets
        """
        # Получаем все уникальные вопросы для каждого типа анкеты
        question_keys = self.get_all_question_keys(user_data)

        # Сортируем типы анкет для консистентности
        anketa_types = sorted(question_keys.keys())

        # Формируем заголовки
        headers = ["Peer ID", "Время", "Текущий статус", "Тип анкеты"]

        # Для каждого типа анкеты добавляем столбцы с вопросами
        type_columns = {}  # {тип_анкеты: {вопрос: индекс_столбца}}
        current_col = len(headers)

        for anketa_type in anketa_types:
            questions = question_keys[anketa_type]
            for question in questions:
                headers.append(f"{anketa_type}: {question}")
                if anketa_type not in type_columns:
                    type_columns[anketa_type] = {}
                type_columns[anketa_type][question] = current_col
                current_col += 1

        rows = [headers]

        # Заполняем данные
        for peer_id, peer_data in sorted(user_data.items()):
            # Получаем последний статус пользователя
            last_status = ""
            if peer_data["statuses"]:
                last_status = max(peer_data["statuses"],
                                  key=lambda x: x["timestamp"])["status"]

            # Для каждой анкеты создаем отдельную строку
            for anketa_type, anketa_info in peer_data["anketas"].items():
                row = [""] * len(headers)

                # Базовые поля
                row[0] = peer_id
                row[1] = anketa_info.get("timestamp", "")
                row[2] = last_status
                row[3] = anketa_type

                # Заполняем ответы на вопросы
                if isinstance(anketa_info["data"], dict):
                    for question, answer in anketa_info["data"].items():
                        # Находим правильный столбец для этого вопроса
                        if (anketa_type in type_columns and
                                question in type_columns[anketa_type]):
                            col_index = type_columns[anketa_type][question]
                            row[col_index] = answer

                rows.append(row)

        return rows

    def flatten_user_data_compact(self, user_data: Dict[int, Dict[str, Any]]) -> List[List[Any]]:
        """
        Компактный формат - все анкеты пользователя в одной строке,
        но каждый вопрос в отдельном столбце с префиксом типа анкеты

        Returns:
            Список строк для Google Sheets
        """
        # Получаем все уникальные вопросы для каждого типа анкеты
        question_keys = self.get_all_question_keys(user_data)

        # Сортируем типы анкет
        anketa_types = sorted(question_keys.keys())

        # Формируем заголовки
        headers = ["Peer ID", "Последнее обновление", "Текущий статус"]

        # Добавляем столбцы для каждого вопроса каждой анкеты
        for anketa_type in anketa_types:
            for question in sorted(question_keys[anketa_type]):
                headers.append(f"{anketa_type}: {question}")

        rows = [headers]

        # Заполняем данные для каждого пользователя
        for peer_id, peer_data in sorted(user_data.items()):
            row = [""] * len(headers)

            # Базовые поля
            row[0] = peer_id

            # Последнее обновление (макс timestamp среди всех анкет)
            if peer_data["timestamps"]:
                row[1] = max(peer_data["timestamps"])

            # Текущий статус
            if peer_data["statuses"]:
                last_status = max(peer_data["statuses"],
                                  key=lambda x: x["timestamp"])
                row[2] = last_status["status"]

            # Заполняем ответы на вопросы
            col_index = 3  # Начинаем с 3 индекса (после базовых полей)

            for anketa_type in anketa_types:
                # Если у пользователя есть эта анкета
                if anketa_type in peer_data["anketas"]:
                    anketa_data = peer_data["anketas"][anketa_type]["data"]
                    if isinstance(anketa_data, dict):
                        for question in sorted(question_keys[anketa_type]):
                            row[col_index] = anketa_data.get(question, "")
                            col_index += 1
                    else:
                        # Если данные не словарь, пропускаем вопросы
                        col_index += len(question_keys[anketa_type])
                else:
                    # Если анкеты нет, оставляем ячейки пустыми
                    col_index += len(question_keys[anketa_type])

            rows.append(row)

        return rows

    async def export_to_google_sheets(self, detailed: bool = False):
        """
        Основной метод экспорта данных в Google Sheets

        Args:
            detailed: если True - каждая анкета в отдельной строке,
                     если False - все анкеты пользователя в одной строке
        """
        try:
            self.logger.info("Начало экспорта данных в Google Sheets")

            # Собираем данные из БД
            user_data = await self.collect_all_user_data()
            self.logger.info(f"Собраны данные для {len(user_data)} пользователей")

            # Аутентификация в Google Sheets
            self.authenticate_google_sheets()

            # Открываем или создаем таблицу
            self.open_or_create_sheet()

            # Преобразуем данные в формат для таблицы
            if detailed:
                rows = self.flatten_user_data_detailed(user_data)
                self.logger.info(f"Детальный формат: {len(rows) - 1} строк")
            else:
                rows = self.flatten_user_data_compact(user_data)
                self.logger.info(f"Компактный формат: {len(rows) - 1} строк")

            # Очищаем лист и записываем новые данные
            self.sheet.clear()

            # Записываем данные
            self.sheet.update('A1', rows)

            self.logger.info(f"Успешно экспортировано {len(rows) - 1} записей")

            # Получаем ссылку на таблицу
            sheet_url = f"https://docs.google.com/spreadsheets/d/{self.sheet.spreadsheet.id}"
            self.logger.info(f"Ссылка на таблицу: {sheet_url}")

            return sheet_url

        except Exception as e:
            self.logger.error(f"Ошибка при экспорте: {e}")
            raise

    async def export_users_with_specific_anketas(self, required_types: Set[str],
                                                 detailed: bool = False):
        """
        Экспортирует только пользователей с определенными типами анкет

        Args:
            required_types: множество требуемых типов анкет
            detailed: формат экспорта
        """
        try:
            # Получаем пользователей с нужными анкетами
            users = await self.db_manager.get_users_with_specific_anketas(required_types)
            self.logger.info(f"Найдено {len(users)} пользователей с анкетами {required_types}")

            # Собираем полные данные
            all_user_data = await self.collect_all_user_data()

            # Фильтруем только нужных пользователей
            filtered_data = {
                peer_id: data for peer_id, data in all_user_data.items()
                if peer_id in users
            }

            # Аутентификация в Google Sheets
            self.authenticate_google_sheets()

            # Создаем отдельную таблицу для фильтрованных данных
            sheet_name = f"{self.sheet_name}_filtered_{'_'.join(required_types)}"
            self.sheet = self.client.create(sheet_name).sheet1

            # Преобразуем данные
            if detailed:
                rows = self.flatten_user_data_detailed(filtered_data)
            else:
                rows = self.flatten_user_data_compact(filtered_data)

            # Записываем данные
            self.sheet.update('A1', rows)

            sheet_url = f"https://docs.google.com/spreadsheets/d/{self.sheet.spreadsheet.id}"
            self.logger.info(f"Ссылка на отфильтрованную таблицу: {sheet_url}")

            return sheet_url

        except Exception as e:
            self.logger.error(f"Ошибка при фильтрованном экспорте: {e}")
            raise