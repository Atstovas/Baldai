from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from tinymce.models import HTMLField
from PIL import Image
import pytz
import uuid
from django.utils.html import format_html
from django.utils import timezone
from django.db.models import Sum
from django.urls import reverse
import subprocess
import platform


utc = pytz.UTC

# Use the Broadcom SOC channel numbering scheme
#GPIO.setmode(GPIO.BCM)

# Set up pin 17 as an output pin
#GPIO.setup(17, GPIO.OUT)



# Create your models here.


#Remember to clean up the GPIO settings when your application ends to ensure that the GPIO resources are freed.
# You can do this by calling GPIO.cleanup().

class Service(models.Model):
    name = models.CharField(verbose_name="Pavadinimas", max_length=50)
    price = models.FloatField(verbose_name="Kaina")

    def __str__(self):
        return f"{self.name} ({self.price})"

    class Meta:
        verbose_name = 'Paslauga'
        verbose_name_plural = 'Paslaugos'


class SideDrill(models.Model):
    side = models.CharField(verbose_name="Gręžimo kraštinė", max_length=10)

    def __str__(self):
        return f"{self.side}"

    class Meta:
        verbose_name = 'Gręžimo pusė'
        verbose_name_plural = 'Gręžimo pusės'


class DrillSketch(models.Model):
    drill = models.CharField(verbose_name="Gręžimo eskizas", max_length=20)
    sketch = models.ImageField(verbose_name="Eskizas", upload_to="sketch", null=True, blank=True)
    drill_side = models.ForeignKey(to="SideDrill", verbose_name="Gręžimo kraštinė",
                                   on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.drill}"

    class Meta:
        verbose_name = 'Gręžimo eskizas'
        verbose_name_plural = 'Gręžimo eskizas'


class SketchCustom(models.Model):
    sketch_custom = models.CharField(verbose_name="Eskizas", max_length=20)
    sketch = models.ImageField(verbose_name="Eskizas", upload_to="sketch", null=True, blank=True)

    def __str__(self):
        return f"{self.sketch_custom}"

    class Meta:
        verbose_name = 'Eskizas'
        verbose_name_plural = 'Eskizas'


class MillDrawing(models.Model):
    mill_drawing = models.CharField(verbose_name="Frezavimo SCHEMA", max_length=20)
    sketch = models.ImageField(verbose_name="Eskizas", upload_to="sketch", null=True, blank=True)

    def __str__(self):
        return f"{self.mill_drawing}"

    class Meta:
        verbose_name = 'Frezavimo schema'
        verbose_name_plural = 'Frezavimo schemos'


class EdgeThickness(models.Model):
    e_thickness = models.FloatField(verbose_name="Briaunos storis mm", max_length=5)

    def __str__(self):
        return f"{self.e_thickness}"

    class Meta:
        verbose_name = 'Briaunos storis mm'
        verbose_name_plural = 'Briaunų storiai'


class EdgeColor(models.Model):
    e_color = models.CharField(verbose_name="Briaunos kodas", max_length=20)
    e_color_name = models.CharField(verbose_name="Briaunos spalva", max_length=35)
    e_photo = models.ImageField('Briaunos nuotrauka', upload_to='edge_color', null=True, blank=True)

    def __str__(self):
        return f"{self.e_color} {self.e_color_name}"

    class Meta:
        verbose_name = 'Briaunos spalva'
        verbose_name_plural = 'Briaunų spalvos'


class TopEdgeInfo(models.Model):
    e_color = models.ForeignKey(to="EdgeColor", verbose_name="Briauno spalva",
                                on_delete=models.SET_NULL, null=True)
    # e_length = models.CharField(verbose_name="Briaunos ilgis", max_length=20)
    e_thickness_model = models.ForeignKey(to="EdgeThickness", verbose_name="Plokštės briauna",
                                          on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.e_color} : {self.e_thickness_model}mm"  # {self.e_thickness_model}"{self.e_length}

    class Meta:
        verbose_name = 'Plokštės viršutinė briauna'
        verbose_name_plural = 'Plokščių viršutinė briauna'


class BottomEdgeInfo(models.Model):
    e_color = models.ForeignKey(to="EdgeColor", verbose_name="Briauno spalva",
                                on_delete=models.SET_NULL, null=True)
    # e_length = models.CharField(verbose_name="Briaunos ilgis", max_length=20)
    e_thickness_model = models.ForeignKey(to="EdgeThickness", verbose_name="Plokštės briauna",
                                          on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.e_color} : {self.e_thickness_model}mm"  # "{self.e_length}

    class Meta:
        verbose_name = 'Plokštės apatinė briauna'
        verbose_name_plural = 'Plokščių apatinė briauna'


class LeftEdgeInfo(models.Model):
    e_color = models.ForeignKey(to="EdgeColor", verbose_name="Briauno spalva",
                                on_delete=models.SET_NULL, null=True)
    # e_length = models.CharField(verbose_name="Briaunos ilgis", max_length=20)
    e_thickness_model = models.ForeignKey(to="EdgeThickness", verbose_name="Plokštės briauna",
                                          on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.e_color} : {self.e_thickness_model}mm"  # {self.e_thickness_model}"{self.e_length}

    class Meta:
        verbose_name = 'Plokštės kairė briauna'
        verbose_name_plural = 'Plokščių kairė briauna'


class RightEdgeInfo(models.Model):
    e_color = models.ForeignKey(to="EdgeColor", verbose_name="Briauno spalva",
                                on_delete=models.SET_NULL, null=True)
    # e_length = models.CharField(verbose_name="Briaunos ilgis", max_length=20)
    e_thickness_model = models.ForeignKey(to="EdgeThickness", verbose_name="Plokštės briauna",
                                          on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.e_color} : {self.e_thickness_model}mm"  # {self.e_thickness_model}"{self.e_length}

    class Meta:
        verbose_name = 'Plokštės dešinė briauna'
        verbose_name_plural = 'Plokščių dešinė briauna'


class ProductThickness(models.Model):
    p_thickness = models.FloatField(verbose_name="Storis", max_length=5)

    def __str__(self):
        return f"{self.p_thickness} "

    class Meta:
        verbose_name = 'Plokštės storis'
        verbose_name_plural = 'Plokščių storiai'


class Product(models.Model):
    decor = models.CharField(verbose_name="Plokštės dekoras", max_length=10)
    p_name = models.CharField(verbose_name="Plokštės pavadinimas", max_length=50)
    decor_pic = models.ImageField('Dekoro nuotrauka', upload_to='decors', null=True, blank=True)
    price_product = models.FloatField(verbose_name="Product price", default=0.0)
    date_created = models.DateTimeField(auto_now_add=True,)

    def total_quantity(self):
        total_qty = OrderLine.objects.filter(product=self).aggregate(total_qty=Sum('qty1'))['total_qty']
        return total_qty if total_qty is not None else 0
    def __str__(self):
        return f"{self.decor} {self.p_name}"

    class Meta:
        verbose_name = 'Plokštė'
        verbose_name_plural = 'Plokštės'


class Baldas(models.Model):
    serijos_nr = models.CharField(default=uuid.uuid4().hex[:10].upper(), verbose_name="Baldo nr.(kataloge)",
                                  max_length=11)
    name = models.CharField(verbose_name="Baldo pavadinimas", max_length=20)
    client_name = models.ForeignKey(to=User, verbose_name="Projektuotojas", on_delete=models.SET_NULL, null=True)
    photo = models.ImageField('Nuotrauka', upload_to='baldai', null=True, blank=True)
    description = HTMLField(verbose_name="Aprašymas", null=True, blank=True)


    def __str__(self):
        return f"{self.client_name} ({self.serijos_nr})"

    class Meta:
        verbose_name = 'Baldas'
        verbose_name_plural = 'Baldai'


class Order(models.Model):
    order_no = models.CharField(default=uuid.uuid4().hex[:6].upper(), verbose_name="Užsakymo Numeris", max_length=10,
                                editable=False)

    def save(self, *args, **kwargs):
        # Check if the instance already exists in the database
        is_new = self.pk is None

        while Order.objects.filter(order_no=self.order_no).exists():
            self.order_no = uuid.uuid4().hex[:6].upper()
        super(Order, self).save(*args, **kwargs)

        # If the instance is new, run the script
        if is_new:
            try:
                if platform.system() == 'Linux':
                    print("Running the script on Linux")
                    subprocess.run(['sudo', 'python3', 'baldai/gpio_17pin.py'])
                else:
                    print("Unknown operating system")
            except subprocess.CalledProcessError as e:
                print(f"Error occurred while trying to run script: {e}")

    date = models.DateTimeField(verbose_name="Data", auto_now_add=True)
    client = models.ForeignKey(to=User, verbose_name="Klientas", on_delete=models.SET_NULL, null=True)
    baldas = models.ForeignKey(to="baldas", verbose_name="Baldas", on_delete=models.CASCADE)
    deadline = models.DateTimeField(verbose_name="Terminas", null=True, blank=True)

    STATUS = (
        ('p', "Pateiktas"),
        ('a', "Apmokėtas"),
        ('g', "Gamyboje"),
        ('i', "Išsiųstas"),
        ('v', "Įvykdytas"),
        ('t', "Atšaukta"),
    )

    status = models.CharField(verbose_name="Būsena", max_length=1, choices=STATUS, default="p", help_text='Statusas')

    def is_overdue(self):
        return self.deadline and self.deadline.replace(tzinfo=utc) < datetime.today().replace(
            tzinfo=utc) and self.status != 'i'

    def total_length_cut(self):
        total = 0
        for line in self.lines.all():
            total += line.total_length()
        return total

    def total(self):
        total = 0
        for line in self.lines.all():
            total += line.line_sum()
        return total

    # def total_width_cut(self):
    #     total = 0
    #     for line in self.lines.all():
    #         total += line.total_width()
    #     return total
    #
    # def total_services(self):
    #     total = 0
    #     for line in self.lines.all():
    #         if line.service:
    #             total += line.service.price * line.qty2
    #     return total

    def total_products(self):
        total = 0
        for line in self.lines.all():
            if line.product:
                total += line.product.price_product * line.qty1
        return total

    def get_absolute_url(self):
        return reverse('order', args=[str(self.id)])


    num_orders_done = models.IntegerField(default=0)

    # def save(self, *args, **kwargs):
    #     # If the instance already exists in the database
    #     if self.pk is not None:
    #         # Get the old value of num_orders_done
    #         old_num_orders_done = Order.objects.get(pk=self.pk).num_orders_done
    #
    #         # If num_orders_done has changed
    #         if self.num_orders_done != old_num_orders_done:
    #             # Toggle the GPIO pin
    #             current_state = GPIO.input(17)
    #             GPIO.output(17, not current_state)
    #
    #     super().save(*args, **kwargs)

    def __str__(self):
        formatted_date = self.date.strftime("%Y:%m:%d %H:%M")
        formatted_total = format(self.total(), ".2f")
        return f"{self.order_no}: meistras: {self.baldas} ({formatted_date}) - {formatted_total} užsakovas: {self.client}"

    class Meta:
        verbose_name = 'Užsakymas'
        verbose_name_plural = 'Užsakymai'
        ordering = ['-date']


class OrderLine(models.Model):
    order = models.ForeignKey(to="Order", verbose_name="Užsakymas", on_delete=models.CASCADE, related_name="lines")
    service = models.ForeignKey(to="Service", verbose_name="Paslauga", on_delete=models.SET_NULL, null=True, blank=True,
                                default=None)
    product = models.ForeignKey(to="Product", verbose_name="Plokštė", on_delete=models.SET_NULL, null=True, blank=True,
                                default=None, related_name="gaminys")
    product_thickness = models.ForeignKey(to="ProductThickness", verbose_name="Storis", on_delete=models.SET_NULL,
                                          null=True, blank=True, default=None)
    right_edge_info = models.ForeignKey(to="RightEdgeInfo", verbose_name="→ dešinė briauna",
                                        on_delete=models.SET_NULL,
                                        null=True,
                                        blank=True,
                                        default=None,
                                        related_name="right_edge_info")
    left_edge_info = models.ForeignKey(to="LeftEdgeInfo", verbose_name="← kairė briauna",
                                       on_delete=models.SET_NULL,
                                       null=True,
                                       blank=True,
                                       default=None,
                                       related_name="left_edge_info")
    bottom_edge_info = models.ForeignKey(to="BottomEdgeInfo", verbose_name="↓ apatinė briauna",
                                         on_delete=models.SET_NULL,
                                         null=True,
                                         blank=True,
                                         default=None,
                                         related_name="bottom_edge_info")
    top_edge_info = models.ForeignKey(to="TopEdgeInfo", verbose_name="↑ viršutinė briauna",
                                      on_delete=models.SET_NULL,
                                      null=True,
                                      blank=True,
                                      default=None,
                                      related_name="top_edge_info")
    mill_drawing_info = models.ForeignKey(to="MillDrawing", verbose_name="Frezavimas",
                                          on_delete=models.SET_NULL,
                                          null=True,
                                          blank=True,
                                          default=None,
                                          )
    sketch_custom = models.ForeignKey(to="SketchCustom", verbose_name="Eskizas",
                                      on_delete=models.SET_NULL,
                                      null=True,
                                      blank=True,
                                      default=None,
                                      )
    sketch_drill_info = models.ForeignKey(to="DrillSketch", verbose_name="Gręžimas",
                                          on_delete=models.SET_NULL,
                                          null=True,
                                          blank=True,
                                          default=None,
                                          )
    qty1 = models.IntegerField(verbose_name="Kiekis", default=None, blank=True, null=True)
    qty2 = models.IntegerField(verbose_name="Kiekis2", default=None, blank=True, null=True)
    product_length = models.IntegerField(verbose_name="Ilgis", default=None, blank=True, null=True)
    product_width = models.IntegerField(verbose_name="Plotis", default=None, blank=True, null=True)

    def total_length(self):
        left_thickness = self.left_edge_info.e_thickness_model.e_thickness if self.left_edge_info else 0
        right_thickness = self.right_edge_info.e_thickness_model.e_thickness if self.right_edge_info else 0

        sum = self.product_length - left_thickness - right_thickness
        return sum if self.product else 0

    def total_width(self):
        top_thickness = self.top_edge_info.e_thickness_model.e_thickness if self.top_edge_info else 0
        bottom_thickness = self.bottom_edge_info.e_thickness_model.e_thickness if self.bottom_edge_info else 0

        sum = self.product_width - top_thickness - bottom_thickness
        return sum if self.product else 0

    def display_total_length(self):
        if self.product_length is not None and self.left_edge_info is not None and self.right_edge_info is not None:
            return self.product_length - self.left_edge_info.e_thickness_model.e_thickness - self.right_edge_info.e_thickness_model.e_thickness
        else:
            return None

    display_total_length.short_description = "Cut Length"

    def display_total_width(self):
        if self.product_width is not None and self.top_edge_info is not None and self.bottom_edge_info is not None:
            return self.product_width - self.top_edge_info.e_thickness_model.e_thickness - self.bottom_edge_info.e_thickness_model.e_thickness
        else:
            return None

    display_total_width.short_description = "Cut width"

    def view_sketch_image_url(self):
        if self.mill_drawing_info and self.mill_drawing_info.sketch:
            return format_html('<a href="{}" target="_blank">View Sketch Image</a>', self.mill_drawing_info.sketch.url)
        else:
            return "No sketch image available"

    def line_sum(self):
        if self.service:
            return self.service.price * self.qty2 if self.service else 0
        elif self.product:
            return self.product.price_product * self.qty1 if self.product else 0
        else:
            return 0

    @property
    def mill_sketch_image_url(self):
        if self.mill_drawing_info and self.mill_drawing_info.sketch:
            url = self.mill_drawing_info.sketch.url
            custom_text = self.mill_drawing_info.mill_drawing  # Fetching the custom text from the MillDrawing model
            return format_html('<a href="{}" target="_blank">{}</a>  {}',
                               url,
                               custom_text,
                               "")
        else:
            return "-"

    @property
    def sketch_image_url(self):
        if self.sketch_custom and self.sketch_custom.sketch:
            url = self.sketch_custom.sketch.url
            custom_text = self.sketch_custom.sketch_custom  # Fetching the custom text from the MillDrawing model
            return format_html('<a href="{}" target="_blank">{}</a>  {}',
                               url,
                               custom_text,
                               "")
        else:
            return "-"


    @property
    def drill_image_url(self):
        if self.sketch_drill_info and self.sketch_drill_info.sketch:
            url = self.sketch_drill_info.sketch.url
            custom_text = self.sketch_drill_info.drill
            return format_html('<a href="{}" target="_blank">{}</a>', url, custom_text)
        else:
            return "-"


    @property
    def product_decor_url_with_decor(self):
        if self.product and self.product.decor_pic:
            url = self.product.decor_pic.url
            name = self.product.decor
            return format_html('<a href="{}" target="_blank">{}</a>', url, name)
        else:
            return self.product if self.product else "-"

    def save(self, *args, **kwargs):
        if self.product_length is None:
            self.product_length = 0
        if self.product_width is None:
            self.product_width = 0
        if self.qty1 is None:
            self.qty1 = 0
        super().save(*args, **kwargs)

    def __str__(self):
        if self.service:
            return f"{self.service} - {self.qty2} - {self.line_sum()}"
        elif self.product:
            return f"{self.product} - {self.qty1} - {self.line_sum()}"
        else:
            return "Nėra užsakymo eilučių"

    class Meta:
        verbose_name = 'Užsakymo eilutė'
        verbose_name_plural = 'Užsakymo eilutės'


class OrderComment(models.Model):
    order = models.ForeignKey(to="Order", verbose_name="Užsakymas", on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(to=User, verbose_name="Autorius", on_delete=models.CASCADE)
    date_created = models.DateTimeField(verbose_name="Data", auto_now_add=True)
    content = models.TextField(verbose_name="Tekstas", max_length=1000)

    class Meta:
        verbose_name = 'Užsakymo komentaras'
        verbose_name_plural = 'Užsakymų komentarai'
        ordering = ['-date_created']


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(default="profile_pics/default.png", upload_to="profile_pics")

    def __str__(self):
        return f"{self.user.username} profilis"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.photo.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.photo.path)
