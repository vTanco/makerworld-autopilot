"""
Database manager for MakerWorld Autopilot.
Stores models, publication status, social distributions, and reward metrics.
"""

import json
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


class Database:
    def __init__(self, db_path: Path = None):
        if db_path is None:
            base_dir = Path(__file__).resolve().parent.parent
            data_dir = base_dir / "data"
            data_dir.mkdir(parents=True, exist_ok=True)
            db_path = data_dir / "autopilot.db"
            
        self.db_path = Path(db_path)
        self._init_db()

    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self) -> None:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # Models table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS models (
                    id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    slug TEXT NOT NULL,
                    category TEXT NOT NULL,
                    template_used TEXT,
                    stl_path TEXT,
                    package_3mf_path TEXT,
                    renders_json TEXT,
                    description TEXT,
                    tags_json TEXT,
                    status TEXT DEFAULT 'generated',
                    makerworld_id TEXT,
                    makerworld_url TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    published_at TIMESTAMP
                )
            """)

            # Distributions table (Social media tracking)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS distributions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    model_id TEXT NOT NULL,
                    platform TEXT NOT NULL,
                    post_url TEXT,
                    status TEXT DEFAULT 'pending',
                    error_message TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (model_id) REFERENCES models (id)
                )
            """)

            # Account & Rewards metrics history
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS metrics_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    total_points INTEGER DEFAULT 0,
                    available_points INTEGER DEFAULT 0,
                    total_downloads INTEGER DEFAULT 0,
                    total_prints INTEGER DEFAULT 0,
                    total_boosts INTEGER DEFAULT 0,
                    details_json TEXT
                )
            """)

            # Discovered Trends
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS trends (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    keyword TEXT NOT NULL,
                    source TEXT NOT NULL,
                    score REAL DEFAULT 1.0,
                    scouted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()

    # --- Model Operations ---
    def save_model(self, model_data: Dict[str, Any]) -> None:
        renders = json.dumps(model_data.get("renders", []))
        tags = json.dumps(model_data.get("tags", []))
        
        with self._get_connection() as conn:
            conn.execute("""
                INSERT OR REPLACE INTO models (
                    id, title, slug, category, template_used,
                    stl_path, package_3mf_path, renders_json,
                    description, tags_json, status, makerworld_id,
                    makerworld_url, published_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                model_data["id"],
                model_data["title"],
                model_data.get("slug", model_data["id"]),
                model_data.get("category", "Household/Organization"),
                model_data.get("template_used", "generic"),
                model_data.get("stl_path", ""),
                model_data.get("package_3mf_path", ""),
                renders,
                model_data.get("description", ""),
                tags,
                model_data.get("status", "generated"),
                model_data.get("makerworld_id"),
                model_data.get("makerworld_url"),
                model_data.get("published_at"),
            ))
            conn.commit()

    def get_model(self, model_id: str) -> Optional[Dict[str, Any]]:
        with self._get_connection() as conn:
            row = conn.execute("SELECT * FROM models WHERE id = ?", (model_id,)).fetchone()
            if not row:
                return None
            data = dict(row)
            data["renders"] = json.loads(data.get("renders_json") or "[]")
            data["tags"] = json.loads(data.get("tags_json") or "[]")
            return data

    def list_models(self, status: Optional[str] = None, limit: int = 50) -> List[Dict[str, Any]]:
        with self._get_connection() as conn:
            if status:
                rows = conn.execute(
                    "SELECT * FROM models WHERE status = ? ORDER BY created_at DESC LIMIT ?",
                    (status, limit)
                ).fetchall()
            else:
                rows = conn.execute(
                    "SELECT * FROM models ORDER BY created_at DESC LIMIT ?",
                    (limit,)
                ).fetchall()
            
            result = []
            for row in rows:
                d = dict(row)
                d["renders"] = json.loads(d.get("renders_json") or "[]")
                d["tags"] = json.loads(d.get("tags_json") or "[]")
                result.append(d)
            return result

    def update_model_status(
        self,
        model_id: str,
        status: str,
        makerworld_id: Optional[str] = None,
        makerworld_url: Optional[str] = None
    ) -> None:
        now = datetime.utcnow().isoformat() if status in ["published", "uploaded_draft"] else None
        with self._get_connection() as conn:
            conn.execute("""
                UPDATE models
                SET status = ?,
                    makerworld_id = COALESCE(?, makerworld_id),
                    makerworld_url = COALESCE(?, makerworld_url),
                    published_at = COALESCE(?, published_at)
                WHERE id = ?
            """, (status, makerworld_id, makerworld_url, now, model_id))
            conn.commit()

    # --- Distribution Operations ---
    def record_distribution(self, model_id: str, platform: str, post_url: str = None, status: str = "success", error_message: str = None) -> None:
        with self._get_connection() as conn:
            conn.execute("""
                INSERT INTO distributions (model_id, platform, post_url, status, error_message)
                VALUES (?, ?, ?, ?, ?)
            """, (model_id, platform, post_url, status, error_message))
            conn.commit()

    # --- Metrics Operations ---
    def record_metrics(self, total_points: int, available_points: int, downloads: int, prints: int, boosts: int, details: Dict[str, Any] = None) -> None:
        with self._get_connection() as conn:
            conn.execute("""
                INSERT INTO metrics_history (total_points, available_points, total_downloads, total_prints, total_boosts, details_json)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                total_points,
                available_points,
                downloads,
                prints,
                boosts,
                json.dumps(details or {})
            ))
            conn.commit()

    def get_latest_metrics(self) -> Optional[Dict[str, Any]]:
        with self._get_connection() as conn:
            row = conn.execute("SELECT * FROM metrics_history ORDER BY timestamp DESC LIMIT 1").fetchone()
            return dict(row) if row else None
