from sqlalchemy.ext.asyncio import AsyncSession

from app.models.post import Post
from app.models.user import User
from app.schemas.post import PostCreate, PostOut

async def create_post(db:AsyncSession, user:User, data:PostCreate) -> PostOut:
    post = Post(user_id=user.id, content=data.content, image_url=data.image_url)
    db.add(post)
    await db.commit()
    await db.refresh(post)

    return PostOut(
        id=post.id,
        anon_id=user.anon_id,
        content=post.content,
        image_url=post.image_url,
        created_at=post.created_at,
    )
