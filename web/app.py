from starlette.applications import Starlette
from starlette_admin.contrib.sqla import Admin, ModelView

from db.engine import engine
from db.models import User, Message

app=Starlette()
admin=Admin(engine=engine,
            title="Ijara",
            base_url="/"
)
admin.add_view(ModelView(User))
admin.add_view(ModelView(Message))
admin.mount_to(app)