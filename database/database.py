import asyncio
from typing import Dict, List, Optional, Any
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

    async def close(self):
        if self._db:
            self._db.close()