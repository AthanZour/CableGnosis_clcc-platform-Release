# tabs_core/tool_registry.py

_TOOL_ID_TO_META = {}

def set_tool_meta(tool_id_to_meta: dict):
    global _TOOL_ID_TO_META
    _TOOL_ID_TO_META = tool_id_to_meta or {}

def tool_label(tool_id: str, default: str | None = None) -> str:
    meta = _TOOL_ID_TO_META.get(tool_id) or {}
    return meta.get("label") or default or tool_id

def tool_meta(tool_id: str) -> dict:
    return _TOOL_ID_TO_META.get(tool_id) or {}