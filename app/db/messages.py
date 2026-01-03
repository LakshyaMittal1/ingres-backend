from app.db.supabase import supabase

def add_message(conversation_id: str, role: str, content: str):
    """Insert a message into the messages table."""
    response = supabase.table("messages").insert({
        "conversation_id": conversation_id,
        "role": role,
        "content": content
    }).execute()
    return response.data[0] if response.data else None


def get_messages(conversation_id: str):
    """Fetch all messages for a given conversation, ordered by creation time."""
    response = (
        supabase
        .table("messages")
        .select("*")
        .eq("conversation_id", conversation_id)
        .order("created_at")
        .execute()
    )
    return response.data


def delete_messages(conversation_id: str):
    """Delete all messages for a given conversation."""
    supabase.table("messages").delete().eq("conversation_id", conversation_id).execute()
