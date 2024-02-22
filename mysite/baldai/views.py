from django.shortcuts import render, reverse
from .models import Service, Order, Vehicle, OrderLine
from django.views import generic
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.contrib.auth.forms import User
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.contrib.auth import password_validation
from .forms import OrderCommentForm, UserUpdateForm, ProfileUpdateForm, OrderCreateUpdateForm
from django.views.generic.edit import FormMixin
from django.contrib.auth.decorators import login_required


# Create your views here.
def index(request):
    num_services = Service.objects.all().count()
    num_orders_done = Order.objects.filter(status__exact='i').count()
    num_vehicles = Vehicle.objects.all().count()

    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1

    result = {
        "num_services": num_services,
        "num_orders_done": num_orders_done,
        "num_vehicles": num_vehicles,
        "num_visits": num_visits,
    }
    return render(request, template_name="index.html", context=result)


def vehicles(request):
    vehicles = Vehicle.objects.all()
    paginator = Paginator(vehicles, per_page=3)
    page_number = request.GET.get("page")
    paged_vehicles = paginator.get_page(page_number)
    context = {
        "vehicles": paged_vehicles,
    }
    return render(request, template_name="vehicles.html", context=context)


def vehicle(request, vehicle_id):
    vehicle = Vehicle.objects.get(pk=vehicle_id)
    context = {
        "vehicle": vehicle,
    }
    return render(request, template_name="vehicle.html", context=context)


def search(request):
    query = request.GET.get('query')
    vehicles = Vehicle.objects.filter(Q(client_name__icontains=query) |
                                      Q(vehicle_model__make__icontains=query) |
                                      Q(vehicle_model__model__icontains=query) |
                                      Q(license_plate__icontains=query) |
                                      Q(vin_code__icontains=query))
    context = {
        "query": query,
        "vehicles": vehicles,
    }
    return render(request, template_name='search.html', context=context)


@csrf_protect
def register(request):
    if request.method == "POST":
        # pasiimame reikšmes iš registracijos formos
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        # tikriname, ar sutampa slaptažodžiai
        if password == password2:
            # tikriname, ar neužimtas username
            if User.objects.filter(username=username).exists():
                messages.error(request, f'Vartotojo vardas {username} užimtas!')
                return redirect('register')
            else:
                # tikriname, ar nėra tokio pat email
                if User.objects.filter(email=email).exists():
                    messages.error(request, f'Vartotojas su el. paštu {email} jau užregistruotas!')
                    return redirect('register')
                else:
                    try:
                        password_validation.validate_password(password)
                    except password_validation.ValidationError as e:
                        for error in e:
                            messages.error(request, error)
                        return redirect('register')

                    # jeigu viskas tvarkoje, sukuriame naują vartotoją
                    User.objects.create_user(username=username, email=email, password=password)
                    messages.info(request, f'Vartotojas {username} užregistruotas!')
                    return redirect('login')
        else:
            messages.error(request, 'Slaptažodžiai nesutampa!')
            return redirect('register')
    return render(request, 'registration/register.html')


@login_required
def profile(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.info(request, 'Profilis atnaujintas')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
        context = {
            'u_form': u_form,
            'p_form': p_form,
        }
    return render(request, template_name="profile.html", context=context)

class MyOrderListView(LoginRequiredMixin, generic.ListView):
    model = Order
    template_name = "my_orders.html"
    context_object_name = "orders"

    def get_queryset(self):
        return Order.objects.filter(client=self.request.user)
        return render(request, template_name='profile.html', context=context)


class OrderListView(generic.ListView):
    model = Order
    template_name = "orders.html"
    context_object_name = "orders"
    paginate_by = 3


class OrderDetailView(FormMixin, generic.DetailView):
    model = Order
    template_name = 'order.html'
    context_object_name = 'order'
    form_class = OrderCommentForm

    def get_success_url(self):
        return reverse('order', kwargs={'pk': self.object.id})

    # standartinis post metodo perrašymas, naudojant FormMixin, galite kopijuoti tiesiai į savo projektą.
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.order = self.object
        form.instance.author = self.request.user
        form.save()
        return super().form_valid(form)


class OrderCreateView(LoginRequiredMixin, generic.CreateView):
    model = Order
    template_name = "order_form.html"
    # fields = ['vehicle', 'deadline', 'status']
    form_class = OrderCreateUpdateForm
    success_url = "/baldai/orders/"

    def form_valid(self, form):
        form.instance.client = self.request.user
        return super().form_valid(form)


class OrderUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Order
    template_name = "order_form.html"
    # fields = ['vehicle', 'deadline', 'status']
    form_class = OrderCreateUpdateForm

    # success_url = "/autoservice/orders/"

    def get_success_url(self):
        return reverse("order", kwargs={"pk": self.object.id})

    def form_valid(self, form):
        form.instance.client = self.request.user
        return super().form_valid(form)

    def test_func(self):
        return self.get_object().client == self.request.user


class OrderDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Order
    template_name = "order_delete.html"
    context_object_name = "order"
    success_url = "/baldai/orders/"

    def test_func(self):
        return self.get_object().client == self.request.user


class OrderLineCreateView(LoginRequiredMixin, UserPassesTestMixin, generic.CreateView):
    model = OrderLine
    template_name = "orderline_form.html"
    fields = ['service', 'qty']
    # success_url = "/autoservice/orders/"

    def get_success_url(self):
        return reverse("order", kwargs={"pk": self.kwargs['order_pk']})

    def form_valid(self, form):
        form.instance.order = Order.objects.get(pk=self.kwargs['order_pk'])
        return super().form_valid(form)

    def test_func(self):
        order = Order.objects.get(pk=self.kwargs['order_pk'])
        return order.client == self.request.user


class OrderLineUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = OrderLine
    template_name = "orderline_form.html"
    fields = ['service', 'qty']

    def get_success_url(self):
        return reverse("order", kwargs={"pk": self.kwargs['order_pk']})

    def form_valid(self, form):
        form.instance.order = Order.objects.get(pk=self.kwargs['order_pk'])
        return super().form_valid(form)

    def test_func(self):
        order = Order.objects.get(pk=self.kwargs['order_pk'])
        return order.client == self.request.user


class OrderLineDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = OrderLine

    def get_success_url(self):
        return reverse("order", kwargs={"pk": self.kwargs['order_pk']})

    def test_func(self):
        order = Order.objects.get(pk=self.kwargs['order_pk'])
        return order.client == self.request.user
