"""
Legal Knowledge Engine - Retrieves relevant legal articles
and citations based on fuzzy rule results.
"""
import logging
from core.database import DatabaseManager

logger = logging.getLogger(__name__)


class LegalEngine:
    """
    Legal knowledge engine for retrieving legal citations.
    Works with the fuzzy engine results to provide legal context.
    """

    def __init__(self):
        self.db = DatabaseManager()

    def find_relevant_articles(self, rule_ids):
        """
        Find all legal articles linked to the given rule IDs.
        Returns list of article dicts with document info.
        """
        if not rule_ids:
            return []

        placeholders = ",".join(["?"] * len(rule_ids))
        rows = self.db.fetch_all(
            f"""SELECT DISTINCT la.*, ld.title as document_title,
                       ld.code as document_code, ld.year as document_year
                FROM rules r
                JOIN legal_articles la ON r.legal_article_id = la.id
                JOIN legal_documents ld ON la.document_id = ld.id
                WHERE r.id IN ({placeholders}) AND r.legal_article_id IS NOT NULL
                ORDER BY ld.year DESC, la.article_number""",
            tuple(rule_ids)
        )
        return [dict(r) for r in rows]

    def get_citations(self, article_ids):
        """
        Get formatted legal citations for display.
        Returns list of citation dicts.
        """
        if not article_ids:
            return []

        placeholders = ",".join(["?"] * len(article_ids))
        rows = self.db.fetch_all(
            f"""SELECT la.*, ld.title as document_title,
                       ld.code as document_code, ld.year as document_year
                FROM legal_articles la
                JOIN legal_documents ld ON la.document_id = ld.id
                WHERE la.id IN ({placeholders})
                ORDER BY ld.year DESC, la.article_number""",
            tuple(article_ids)
        )

        citations = []
        for row in rows:
            clause_info = f", {row['clause']}" if row['clause'] else ""
            citation = {
                "id": row["id"],
                "document_title": row["document_title"],
                "document_code": row["document_code"],
                "article_number": row["article_number"],
                "clause": row["clause"],
                "content": row["content"],
                "formatted": f"{row['article_number']}{clause_info} - {row['document_title']} ({row['document_year']})",
                "full_text": f"{row['article_number']}{clause_info}: {row['content']}"
            }
            citations.append(citation)

        return citations

    def get_articles_for_rules(self, matched_rules_info):
        """
        Get legal articles for matched rules from fuzzy engine results.
        Args:
            matched_rules_info: list of dicts from FuzzyEngine.run()
        Returns:
            list of citation dicts
        """
        article_ids = set()
        for rule_info in matched_rules_info:
            if rule_info.get("legal_article_id"):
                article_ids.add(rule_info["legal_article_id"])

        if not article_ids:
            return []

        return self.get_citations(list(article_ids))

    def search_articles(self, keyword, domain=None):
        """Search legal articles by keyword."""
        if domain:
            rows = self.db.fetch_all(
                """SELECT la.*, ld.title as document_title, ld.code as document_code
                   FROM legal_articles la
                   JOIN legal_documents ld ON la.document_id = ld.id
                   WHERE ld.domain = ? AND (la.content LIKE ? OR la.keywords LIKE ?)""",
                (domain, f"%{keyword}%", f"%{keyword}%")
            )
        else:
            rows = self.db.fetch_all(
                """SELECT la.*, ld.title as document_title, ld.code as document_code
                   FROM legal_articles la
                   JOIN legal_documents ld ON la.document_id = ld.id
                   WHERE la.content LIKE ? OR la.keywords LIKE ?""",
                (f"%{keyword}%", f"%{keyword}%")
            )
        return [dict(r) for r in rows]

    def get_related_articles(self, article_id):
        """Get articles related to a specific article."""
        rows = self.db.fetch_all(
            """SELECT lr.relation_type, la.*, ld.title as document_title
               FROM legal_relations lr
               JOIN legal_articles la ON lr.related_article_id = la.id
               JOIN legal_documents ld ON la.document_id = ld.id
               WHERE lr.source_article_id = ?""",
            (article_id,)
        )
        return [dict(r) for r in rows]
