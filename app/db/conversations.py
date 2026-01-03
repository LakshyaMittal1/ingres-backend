from app.db.supabase import supabase

def create_conversation(title: str | None = None):
    response = (
        supabase
        .table("conversations")
        .insert({"title": title})
        .execute()
    )
    return response.data[0]


def get_conversations(limit: int = 20):
    response = (
        supabase
        .table("conversations")
        .select("*")
        .order("updated_at", desc=True)
        .limit(limit)
        .execute()
    )
    return response.data


def delete_conversation(conversation_id: str):
    supabase.table("conversations").delete().eq("id", conversation_id).execute()
