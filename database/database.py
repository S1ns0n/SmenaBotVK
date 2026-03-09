import asyncio
from typing import Dict, List, Optional, Any, Set
from datetime import datetime
from tinydb import TinyDB, Query


class AsyncTinyDBManager:
    def __init__(self, db_path: str = "anketas.json"):
        self.db_path = db_path
        self._db = None
        self._lock = asyncio.Lock()
        self.Anketa = Query()

    async def _get_db(self) -> TinyDB:
        """Ленивая инициализация с блокировкой"""
        async with self._lock:
            if self._db is None:
                self._db = TinyDB(self.db_path, indent=4)
            return self._db

    async def save_anketa(self, peer_id: int, anketa_type: str, data: Dict[str, Any]) -> bool:
        """сохраняет анкету"""
        doc = {
            "peer_id": peer_id,
            "anketa_type": anketa_type,
            "data": data,
            "timestamp": datetime.utcnow().isoformat()
        }

        db = await self._get_db()
        db.upsert(doc, (self.Anketa.peer_id == peer_id) & (self.Anketa.anketa_type == anketa_type))
        return True

    async def save_ai_answer(self, peer_id: int, ai_answer_type: str, ai_answer: str) -> bool:
        """сохраняет ответы от нейронки"""
        doc = {
            "peer_id": peer_id,
            "anketa_type": ai_answer_type,
            "data": ai_answer,
            "timestamp": datetime.utcnow().isoformat()
        }

        db = await self._get_db()
        db.upsert(doc, (self.Anketa.peer_id == peer_id) & (self.Anketa.ai_answer_type == ai_answer_type))
        return True


    async def get_user_anketas(self, peer_id: int) -> List[Dict]:
        """Все анкеты пользователя"""
        db = await self._get_db()
        return db.search(self.Anketa.peer_id == peer_id)

    async def has_user_anketa(self, peer_id: int, anketa_type: str) -> bool:
        """Есть ли анкета?"""
        db = await self._get_db()
        return len(db.search((self.Anketa.peer_id == peer_id) & (self.Anketa.anketa_type == anketa_type))) > 0

    async def get_user_anketa_types(self, peer_id: int) -> List[str]:
        """Список анкет"""
        db = await self._get_db()
        anketas = db.search(self.Anketa.peer_id == peer_id)
        return list(set(a["anketa_type"] for a in anketas))

    async def get_anketa_data(self, peer_id: int, anketa_type: str) -> Optional[Dict[str, Any]]:
        """Данные анкеты"""
        db = await self._get_db()
        anketa = db.search((self.Anketa.peer_id == peer_id) & (self.Anketa.anketa_type == anketa_type))
        return anketa[0]["data"] if anketa else None

    async def delete_user_anketas(self, peer_id: int):
        """Удалить анкеты"""
        db = await self._get_db()
        db.remove(self.Anketa.peer_id == peer_id)

    async def get_all_users(self) -> Set[int]:
        """
        Достаёт список всех пользователей, которые есть в базе.
        Возвращает множество уникальных peer_id.
        """
        db = await self._get_db()
        all_records = db.all()
        users = {record["peer_id"] for record in all_records if "peer_id" in record}
        return users

    async def get_users_with_specific_anketas(self, required_types: Set[str]) -> Set[int]:
        """
        Достаёт список всех peer_id пользователей, которые заполнили указанные типы анкет.

        Args:
            required_types: множество типов анкет (например, {"anketa0", "anketa1"})

        Returns:
            множество уникальных peer_id
        """
        db = await self._get_db()
        all_records = db.all()

        user_anketas = {}

        for record in all_records:
            if "peer_id" in record and "anketa_type" in record:
                peer_id = record["peer_id"]
                anketa_type = record["anketa_type"]

                if peer_id not in user_anketas:
                    user_anketas[peer_id] = set()
                user_anketas[peer_id].add(anketa_type)

        result = {
            peer_id for peer_id, types in user_anketas.items()
            if required_types.issubset(types)
        }

        return result

    async def has_any_anketa_from_list(self, peer_id: int, anketa_types: List[str]) -> bool:
        """
        Проверяет, есть ли у пользователя хотя бы одна анкета из списка.
        """
        db = await self._get_db()

        for anketa_type in anketa_types:
            result = db.search((self.Anketa.peer_id == peer_id) & (self.Anketa.anketa_type == anketa_type))
            if result:  # если нашли хотя бы одну анкету
                return False  # возвращаем False, так как анкета есть

        return True

    async def select_status_for_user(self, peer_id: int, status: str) -> bool:
        """
        Устанавливает статус для пользователя.
        """
        doc = {
            "peer_id": peer_id,
            "status_type": "user_status",  # чтобы отличать от других записей
            "status": status,
            "timestamp": datetime.utcnow().isoformat()
        }

        db = await self._get_db()
        StatusQuery = Query()

        existing = db.search((StatusQuery.peer_id == peer_id) &
                             (StatusQuery.status_type == "user_status"))

        if existing:
            db.update(doc, (StatusQuery.peer_id == peer_id) &
                      (StatusQuery.status_type == "user_status"))
        else:
            db.insert(doc)

        return True

    async def get_users_without_status(self, status: str) -> Set[int]:
        """
        Возвращает множество peer_id пользователей, у которых текущий статус
        не равен указанному или статус вообще не установлен.
        """
        all_users = await self.get_all_users()

        db = await self._get_db()
        StatusQuery = Query()

        status_records = db.search(
            (StatusQuery.status_type == "user_status") &
            (StatusQuery.status == status)
        )

        users_with_given_status = {record["peer_id"] for record in status_records}

        return all_users - users_with_given_status

    async def close(self):
        if self._db:
            self._db.close()