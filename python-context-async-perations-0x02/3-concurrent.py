import asyncio
import aiosqlite

# ----------------------------
# 1. Async function to fetch all users
# ----------------------------
async def async_fetch_users():
    async with aiosqlite.connect("users.db") as db:
        db.row_factory = aiosqlite.Row  # enables dict-like rows
        async with db.execute("SELECT * FROM users") as cursor:
            users = await cursor.fetchall()
            print("👥 All Users:")
            for row in users:
                print(dict(row))
            return users


# ----------------------------
# 2. Async function to fetch users older than 40
# ----------------------------
async def async_fetch_older_users():
    async with aiosqlite.connect("users.db") as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM users WHERE age > ?", (40,)) as cursor:
            older_users = await cursor.fetchall()
            print("\n🧓 Users older than 40:")
            for row in older_users:
                print(dict(row))
            return older_users


# ----------------------------
# 3. Run both queries concurrently
# ----------------------------
async def fetch_concurrently():
    # asyncio.gather runs both async functions in parallel
    await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )


# ----------------------------
# 4. Entry point
# ----------------------------
if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
