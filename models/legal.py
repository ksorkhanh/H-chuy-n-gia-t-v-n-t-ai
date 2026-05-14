"""
Mô hình Pháp lý - Thao tác CRUD cho văn bản, điều khoản và quan hệ pháp lý.
"""
import logging
from core.database import DatabaseManager

logger = logging.getLogger(__name__)


class LegalDocument:
    """Mô hình cho văn bản pháp lý (luật, nghị định, v.v.)."""

    def __init__(self, id=None, title=None, code=None, year=None,
                 domain=None, description=None, is_active=True):
        self.id = id
        self.title = title
        self.code = code
        self.year = year
        self.domain = domain
        self.description = description
        self.is_active = is_active

    @staticmethod
    def get_all(domain=None):
        """Lấy tất cả văn bản pháp lý, có thể lọc theo lĩnh vực."""
        db = DatabaseManager()
        if domain:
            rows = db.fetch_all(
                "SELECT * FROM legal_documents WHERE domain = ? ORDER BY year DESC",
                (domain,)
            )
        else:
            rows = db.fetch_all("SELECT * FROM legal_documents ORDER BY year DESC")
        return [LegalDocument._from_row(r) for r in rows]

    @staticmethod
    def find_by_id(doc_id):
        """Tìm văn bản theo ID."""
        db = DatabaseManager()
        row = db.fetch_one("SELECT * FROM legal_documents WHERE id = ?", (doc_id,))
        return LegalDocument._from_row(row) if row else None

    @staticmethod
    def find_by_code(code):
        """Tìm văn bản theo mã."""
        db = DatabaseManager()
        row = db.fetch_one("SELECT * FROM legal_documents WHERE code = ?", (code,))
        return LegalDocument._from_row(row) if row else None

    @staticmethod
    def create(title, code, year, domain, description=None):
        """Tạo mới một văn bản pháp lý."""
        db = DatabaseManager()
        cursor = db.execute(
            """INSERT INTO legal_documents (title, code, year, domain, description)
               VALUES (?, ?, ?, ?, ?)""",
            (title, code, year, domain, description)
        )
        return cursor.lastrowid

    @staticmethod
    def update(doc_id, **kwargs):
        """Cập nhật một văn bản pháp lý."""
        db = DatabaseManager()
        allowed = ['title', 'code', 'year', 'domain', 'description', 'is_active']
        updates = []
        params = []
        for key, value in kwargs.items():
            if key in allowed:
                updates.append(f"{key} = ?")
                params.append(value)
        if not updates:
            return
        params.append(doc_id)
        db.execute(f"UPDATE legal_documents SET {', '.join(updates)} WHERE id = ?", tuple(params))

    @staticmethod
    def delete(doc_id):
        """Xóa một văn bản pháp lý và các điều khoản liên quan."""
        db = DatabaseManager()
        db.execute("DELETE FROM legal_documents WHERE id = ?", (doc_id,))

    @staticmethod
    def search(keyword):
        """Tìm kiếm văn bản theo tiêu đề hoặc mã."""
        db = DatabaseManager()
        rows = db.fetch_all(
            """SELECT * FROM legal_documents
               WHERE title LIKE ? OR code LIKE ? OR description LIKE ?
               ORDER BY year DESC""",
            (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%")
        )
        return [LegalDocument._from_row(r) for r in rows]

    @staticmethod
    def _from_row(row):
        if not row:
            return None
        return LegalDocument(
            id=row["id"], title=row["title"], code=row["code"],
            year=row["year"], domain=row["domain"],
            description=row["description"],
            is_active=bool(row["is_active"])
        )

    def to_dict(self):
        return {
            "id": self.id, "title": self.title, "code": self.code,
            "year": self.year, "domain": self.domain,
            "description": self.description, "is_active": self.is_active
        }


class LegalArticle:
    """Mô hình cho từng điều khoản/khoản mục pháp lý."""

    def __init__(self, id=None, document_id=None, article_number=None,
                 clause=None, content=None, keywords=None, is_active=True):
        self.id = id
        self.document_id = document_id
        self.article_number = article_number
        self.clause = clause
        self.content = content
        self.keywords = keywords
        self.is_active = is_active

    @staticmethod
    def get_by_document(document_id):
        """Lấy tất cả điều khoản của một văn bản."""
        db = DatabaseManager()
        rows = db.fetch_all(
            "SELECT * FROM legal_articles WHERE document_id = ? ORDER BY article_number",
            (document_id,)
        )
        return [LegalArticle._from_row(r) for r in rows]

    @staticmethod
    def find_by_id(article_id):
        """Tìm điều khoản theo ID."""
        db = DatabaseManager()
        row = db.fetch_one("SELECT * FROM legal_articles WHERE id = ?", (article_id,))
        return LegalArticle._from_row(row) if row else None

    @staticmethod
    def get_all():
        """Lấy tất cả điều khoản."""
        db = DatabaseManager()
        rows = db.fetch_all(
            """SELECT la.*, ld.title as document_title, ld.code as document_code
               FROM legal_articles la
               JOIN legal_documents ld ON la.document_id = ld.id
               ORDER BY ld.year DESC, la.article_number"""
        )
        return rows

    @staticmethod
    def create(document_id, article_number, content, clause=None, keywords=None):
        """Tạo mới một điều khoản."""
        db = DatabaseManager()
        cursor = db.execute(
            """INSERT INTO legal_articles (document_id, article_number, clause, content, keywords)
               VALUES (?, ?, ?, ?, ?)""",
            (document_id, article_number, clause, content, keywords)
        )
        return cursor.lastrowid

    @staticmethod
    def update(article_id, **kwargs):
        """Cập nhật một điều khoản."""
        db = DatabaseManager()
        allowed = ['article_number', 'clause', 'content', 'keywords', 'is_active']
        updates = []
        params = []
        for key, value in kwargs.items():
            if key in allowed:
                updates.append(f"{key} = ?")
                params.append(value)
        if not updates:
            return
        params.append(article_id)
        db.execute(f"UPDATE legal_articles SET {', '.join(updates)} WHERE id = ?", tuple(params))

    @staticmethod
    def delete(article_id):
        """Xóa một điều khoản."""
        db = DatabaseManager()
        db.execute("DELETE FROM legal_articles WHERE id = ?", (article_id,))

    @staticmethod
    def search(keyword, domain=None):
        """Tìm kiếm điều khoản theo từ khóa trong nội dung."""
        db = DatabaseManager()
        if domain:
            rows = db.fetch_all(
                """SELECT la.*, ld.title as document_title, ld.code as document_code
                   FROM legal_articles la
                   JOIN legal_documents ld ON la.document_id = ld.id
                   WHERE ld.domain = ? AND (la.content LIKE ? OR la.keywords LIKE ?)
                   ORDER BY ld.year DESC""",
                (domain, f"%{keyword}%", f"%{keyword}%")
            )
        else:
            rows = db.fetch_all(
                """SELECT la.*, ld.title as document_title, ld.code as document_code
                   FROM legal_articles la
                   JOIN legal_documents ld ON la.document_id = ld.id
                   WHERE la.content LIKE ? OR la.keywords LIKE ?
                   ORDER BY ld.year DESC""",
                (f"%{keyword}%", f"%{keyword}%")
            )
        return rows

    @staticmethod
    def _from_row(row):
        if not row:
            return None
        return LegalArticle(
            id=row["id"], document_id=row["document_id"],
            article_number=row["article_number"], clause=row["clause"],
            content=row["content"], keywords=row["keywords"],
            is_active=bool(row["is_active"])
        )

    def to_dict(self):
        return {
            "id": self.id, "document_id": self.document_id,
            "article_number": self.article_number, "clause": self.clause,
            "content": self.content, "keywords": self.keywords,
            "is_active": self.is_active
        }


class LegalRelation:
    """Mô hình cho quan hệ giữa các điều khoản pháp lý."""

    @staticmethod
    def get_related(article_id):
        """Lấy tất cả điều khoản liên quan của một điều khoản."""
        db = DatabaseManager()
        rows = db.fetch_all(
            """SELECT lr.*, la.article_number, la.clause, la.content,
                      ld.title as document_title
               FROM legal_relations lr
               JOIN legal_articles la ON lr.related_article_id = la.id
               JOIN legal_documents ld ON la.document_id = ld.id
               WHERE lr.source_article_id = ?""",
            (article_id,)
        )
        return rows

    @staticmethod
    def create(source_id, related_id, relation_type):
        """Tạo mới một quan hệ."""
        db = DatabaseManager()
        cursor = db.execute(
            """INSERT INTO legal_relations (source_article_id, related_article_id, relation_type)
               VALUES (?, ?, ?)""",
            (source_id, related_id, relation_type)
        )
        return cursor.lastrowid

    @staticmethod
    def delete(relation_id):
        """Xóa một quan hệ."""
        db = DatabaseManager()
        db.execute("DELETE FROM legal_relations WHERE id = ?", (relation_id,))
