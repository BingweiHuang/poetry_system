from django.contrib import admin

# Register your models here.

from .models.poetry_models import Shi
from .models.poetry_models import Ci
from .models.poetry_models import Fly
from .models.poetry_models import WordFrequency
from .models.poetry_models import Shijing

from .models.account_models import Account
class AccountAdmin(admin.ModelAdmin):
    list_display = ('email', 'user', 'nickname', 'avatar_url', 'display_works', 'display_collections')
    list_filter = ('email',)
    list_editable = ('nickname', 'avatar_url')
    list_per_page = 12


from .models.account_models import Follow
from .models.account_models import Post
class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'content', 'like_count', 'comment_count', 'create_date')
    list_filter = ('author', )
    list_editable = ('content',)
    list_per_page = 12

from .models.account_models import Like
from .models.account_models import Comment
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'content', 'create_date')
    list_filter = ('author', 'post')
    list_editable = ('content',)
    list_per_page = 12

from .models.account_models import ShiCollection
class ShiCollectionAdmin(admin.ModelAdmin):
    list_display = ('author', 'shi', 'create_date')
    list_filter = ('author',)
    # list_editable = ()
    list_per_page = 12

from .models.account_models import CiCollection
class CiCollectionAdmin(admin.ModelAdmin):
    list_display = ('author', 'ci', 'create_date')
    list_filter = ('author',)
    # list_editable = ()
    list_per_page = 12

from .models.account_models import Work
class WorkAdmin(admin.ModelAdmin):
    list_display = ('author', 'title', 'content', 'display')
    list_filter = ('author', 'display')
    list_editable = ('title', 'content')
    list_per_page = 12


admin.site.register(Shi)
admin.site.register(Ci)
admin.site.register(Fly)
admin.site.register(WordFrequency)
admin.site.register(Shijing)

admin.site.register(Account, AccountAdmin)
admin.site.register(Follow)
admin.site.register(Post, PostAdmin)
admin.site.register(Like)
admin.site.register(Comment, CommentAdmin)
admin.site.register(ShiCollection, ShiCollectionAdmin)
admin.site.register(CiCollection, CiCollectionAdmin)
admin.site.register(Work, WorkAdmin)
