import asyncio
from tasks.daily_summary import send_summary_to_admin

if __name__ == "__main__":
    asyncio.run(send_summary_to_admin())
