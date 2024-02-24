from django.contrib import admin
from .models import *
from django.utils.html import format_html


class OrderLineInLine(admin.TabularInline):
    model = OrderLine
    extra = 0
    fields = ['order', 'product', 'product_thickness', 'qty1', 'price_product', 'product_length', 'product_width',
              'left_edge_info',
              'right_edge_info', 'top_edge_info', 'bottom_edge_info', "mill_drawing_info", "sketch_custom",
              "sketch_drill_info"]  # 'service','qty2',


class OrderCommentInLine(admin.TabularInline):
    model = OrderComment
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'order_no', 'date', 'client', 'deadline', 'status']
    list_editable = ["client", 'deadline', 'status']
    inlines = [OrderLineInLine, OrderCommentInLine]
    list_filter = ('status',)


class ProductAdmin(admin.ModelAdmin):
    list_display = ['decor', 'p_name', 'price_product', 'decor_pic']


class BaldasAdmin(admin.ModelAdmin):
    list_display = ['serijos_nr', 'name', 'client_name', 'description', 'photo', ]
    list_filter = ['client_name', ]
    search_fields = ['serijos_nr', ]


class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'price']


class OrderLineAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'product_thickness', 'qty1', 'get_price_product', 'product_length',
                    'product_width', 'display_total_length', 'display_total_width', 'left_edge_info', 'right_edge_info',
                    'top_edge_info', 'bottom_edge_info', 'mill_sketch_image_url', 'sketch_image_url', 'drill_image_url']
    # 'service', 'qty2',
    # OrderLine neturi price_product, bet Product turi price_product lauką (field'ą) ir todėl reikia sukurti funkciją get_price_product kuri grąžina Product modelio price_product lauką (field'ą) ir ją priskirti list_display sąrašui.
    def get_price_product(self, obj):
        return obj.product.price_product if obj.product else None
    get_price_product.short_description = 'Kaina'

    fieldsets = [
        (
            'Užsakymas',
            {
                "fields": ["order", ],  # 'service', 'qty2',
            },
        ),
        (
            'Plokštė',
            {
                "fields": ["product", "product_thickness", "qty1", "price_product", "product_length", "product_width"],
            },
        ),
        (
            "Apskaičiuoti Matmenys",
            {
                "classes": ["collapse"],
                "fields": ["display_total_length", "display_total_width"],
            },
        ),
        (
            "Apdirbimas (Brėžiniai)",
            {
                "classes": ["collapse"],
                "fields": ["mill_drawing_info", "sketch_custom", "sketch_drill_info"],
            },
        ),
        (
            "Kraštinės",
            {
                "classes": ["collapse"],
                "fields": ["left_edge_info", "right_edge_info", "top_edge_info", "bottom_edge_info"],
            },
        ),
    ]
    list_filter = ('order', 'product')
    search_fields = ('product__decor', 'order__order_no')

    readonly_fields = ('display_total_length', 'display_total_width')

    def mill_sketch_image_url(self, obj):
        if obj.mill_drawing_info and obj.mill_drawing_info.sketch:
            url = obj.mill_drawing_info.sketch.url
            custom_text = obj.mill_drawing_info.mill_drawing  # Fetching the custom text from the MillDrawing model
            return format_html('<a href="{}" target="_blank">{}</a>  {}',
                               url,
                               custom_text,
                               "")
        else:
            return "-"

    def sketch_image_url(self, obj):
        if obj.sketch_custom and obj.sketch_custom.sketch:
            url = obj.sketch_custom.sketch.url
            custom_text = obj.sketch_custom.sketch_custom  # Fetching the custom text from the MillDrawing model
            return format_html('<a href="{}" target="_blank">{}</a>  {}',
                               url,
                               custom_text,
                               "")
        else:
            return "-"

    def drill_image_url(self, obj):
        if obj.sketch_drill_info and obj.sketch_drill_info.sketch:
            url = obj.sketch_drill_info.sketch.url
            custom_text = obj.sketch_drill_info.drill  # Fetching the custom text from the MillDrawing model
            return format_html('<a href="{}" target="_blank">{}</a>  {}',
                               url,
                               custom_text,
                               "")
        else:
            return "-"

    drill_image_url.short_description = "GRĘŽIMAS"


admin.site.register(Service, ServiceAdmin)
admin.site.register(Baldas, BaldasAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderLine, OrderLineAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductThickness)
admin.site.register(EdgeThickness)
admin.site.register(EdgeColor)
admin.site.register(BottomEdgeInfo)
admin.site.register(LeftEdgeInfo)
admin.site.register(RightEdgeInfo)
admin.site.register(TopEdgeInfo)
admin.site.register(MillDrawing)
admin.site.register(SketchCustom)
admin.site.register(SideDrill)
admin.site.register(DrillSketch)
admin.site.register(Profile)
