"""
Legal Controller - Manages legal documents and articles.
"""
import logging
from models.legal import LegalDocument, LegalArticle, LegalRelation
from core.auth import AuthService

logger = logging.getLogger(__name__)


class LegalController:
    """Controller for legal document management."""

    def __init__(self):
        self.auth = AuthService()

    def get_all_documents(self, domain=None):
        """Get all legal documents."""
        docs = LegalDocument.get_all(domain)
        return [d.to_dict() for d in docs]

    def get_document(self, doc_id):
        doc = LegalDocument.find_by_id(doc_id)
        return doc.to_dict() if doc else None

    def create_document(self, title, code, year, domain, description=None):
        self.auth.require_permission("manage_legal")
        return LegalDocument.create(title, code, year, domain, description)

    def update_document(self, doc_id, **kwargs):
        self.auth.require_permission("manage_legal")
        LegalDocument.update(doc_id, **kwargs)

    def delete_document(self, doc_id):
        self.auth.require_permission("manage_legal")
        LegalDocument.delete(doc_id)

    def search_documents(self, keyword):
        docs = LegalDocument.search(keyword)
        return [d.to_dict() for d in docs]

    # --- Articles ---
    def get_articles_by_document(self, document_id):
        articles = LegalArticle.get_by_document(document_id)
        return [a.to_dict() for a in articles]

    def get_all_articles(self):
        rows = LegalArticle.get_all()
        return [dict(r) for r in rows]

    def create_article(self, document_id, article_number, content, clause=None, keywords=None):
        self.auth.require_permission("manage_legal")
        return LegalArticle.create(document_id, article_number, content, clause, keywords)

    def update_article(self, article_id, **kwargs):
        self.auth.require_permission("manage_legal")
        LegalArticle.update(article_id, **kwargs)

    def delete_article(self, article_id):
        self.auth.require_permission("manage_legal")
        LegalArticle.delete(article_id)

    def search_articles(self, keyword, domain=None):
        rows = LegalArticle.search(keyword, domain)
        return [dict(r) for r in rows]

    # --- Relations ---
    def get_related_articles(self, article_id):
        rows = LegalRelation.get_related(article_id)
        return [dict(r) for r in rows]

    def create_relation(self, source_id, related_id, relation_type):
        self.auth.require_permission("manage_legal")
        return LegalRelation.create(source_id, related_id, relation_type)
