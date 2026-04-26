"""Conteúdo do manual do usuário — servido como API para o front renderizar.

Os arquivos MDX/MD ficam em apps/frontend/src/manual/<locale>/. Aqui só
expomos índice e busca; renderização é client-side.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends

from app.deps import get_current_user
from app.logging_config import get_logger
from app.models import User

router = APIRouter(prefix="/manual", tags=["manual"])
log = get_logger("manual")


@router.get("/sections")
def list_sections(_user: User = Depends(get_current_user)) -> list[dict[str, str]]:
    return [
        {"id": "primeiros-passos", "title": "Primeiros passos", "order": "10"},
        {"id": "funcionalidades", "title": "Funcionalidades", "order": "20"},
        {"id": "atalhos", "title": "Atalhos de teclado", "order": "30"},
        {"id": "faq", "title": "FAQ", "order": "40"},
        {"id": "solucao-de-problemas", "title": "Solução de problemas", "order": "50"},
        {"id": "glossario", "title": "Glossário", "order": "60"},
        {"id": "privacidade", "title": "Privacidade & LGPD", "order": "70"},
        {"id": "suporte", "title": "Suporte", "order": "80"},
    ]
