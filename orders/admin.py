from django.contrib import admin

from .models import MenuItem, Topping, Order, Order_item


def mark_complete(modeladmin, request, queryset):
    for order in queryset:
        order.completed = True
        order.save()


mark_complete.short_description = 'Mark as Completed'


class OrderItemInline(admin.StackedInline):
    model = Order_item
    extra = 1


class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    exclude = ('checked_out',)
    list_display = ("id", "user", "checked_out", "completed")
    list_filter = ("checked_out",)
    actions = [mark_complete, ]


# Register your models here.
admin.site.register(MenuItem)
admin.site.register(Topping)
admin.site.register(Order, OrderAdmin)
