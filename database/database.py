from tinydb import TinyDB, Query
from typing import Dict, List, Optional, Any
from datetime import datetime
import json


class TinyDBManager:
    def __init__(self, db_path: str = "anketas.json"):
        self.db = TinyDB(db_path, indent=4)
        self.Anketa = Query()

    def save_anketa(self, peer_id: int, anketa_type: str, data: Dict[str, Any]):
        """Сохраняет/обновляет анкету"""
        doc = {
            "peer_id": peer_id,
            "anketa_type": anketa_type,
            "data": data,
            "timestamp": datetime.utcnow().isoformat()
        }

        # Upsert по peer_id + anketa_type
        self.db.upsert(doc, self.Anketa.peer_id == peer_id & self.Anketa.anketa_type == anketa_type)
        return True

    def get_user_anketas(self, peer_id: int) -> List[Dict]:
        """Все анкеты пользователя"""
        return self.db.search(self.Anketa.peer_id == peer_id)

    def has_user_anketa(self, peer_id: int, anketa_type: str) -> bool:
        """Есть ли анкета?"""
        return len(self.db.search(self.Anketa.peer_id == peer_id & self.Anketa.anketa_type == anketa_type)) > 0

    def get_user_anketa_types(self, peer_id: int) -> List[str]:
        """Список анкет: ['anketa1', 'anketa2']"""
        anketas = self.db.search(self.Anketa.peer_id == peer_id)
        return list(set(a["anketa_type"] for a in anketas))

    def get_anketa_data(self, peer_id: int, anketa_type: str) -> Optional[Dict[str, Any]]:
        """Данные анкеты"""
        anketa = self.db.search(self.Anketa.peer_id == peer_id & self.Anketa.anketa_type == anketa_type)
        return anketa[0]["data"] if anketa else None

    def delete_user_anketas(self, peer_id: int):
        """Удалить анкеты пользователя"""
        self.db.remove(self.Anketa.peer_id == peer_id)



