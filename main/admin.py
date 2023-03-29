from django.contrib import admin

# Register your models here.

from .models.poetry_models import Shi
from .models.poetry_models import Ci
from .models.poetry_models import Fly
from .models.poetry_models import WordFrequency
from .models.poetry_models import Shijing

from .models.account_models import Account
from .models.account_models import Follow
from .models.account_models import Post
from .models.account_models import Like
from .models.account_models import Comment
from .models.account_models import ShiCollection
from .models.account_models import CiCollection


admin.site.register(Shi)
admin.site.register(Ci)
admin.site.register(Fly)
admin.site.register(WordFrequency)
admin.site.register(Shijing)

admin.site.register(Account)
admin.site.register(Follow)
admin.site.register(Post)
admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(ShiCollection)
admin.site.register(CiCollection)
