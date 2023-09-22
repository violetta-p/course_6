from django.urls import reverse_lazy, reverse

from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, TemplateView
from mailing.models import Mailing, Client, MailingLogs, Message, Category, MessageVersion
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import inlineformset_factory
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView
from mailing.forms import MailingCreateForm, MessageForm, VersionForm, ClientForm

# from mailing.services import toggle_status


# class ClientListView(ListView):
#     """Просмотр клиентов"""
#     model = Client
#     extra_context = {'title': 'Клиенты'}
#
#     def get_queryset(self, *args, **kwargs):
#         queryset = super().get_queryset(*args, **kwargs)
#         return queryset

class ClientListView(ListView):
    """Просмотр клиентов"""
    model = Client
    extra_context = {'title': 'Клиенты'}

    def get_queryset(self):
        queryset = super().get_queryset().filter(creator=self.request.user)
        return queryset


class ClientDetailView(DetailView):
    model = Client


class ClientCreateView(LoginRequiredMixin, CreateView):
    """Создание клиента"""
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing:client_list')

    def form_valid(self, form):
        client = form.save(commit=False)
        client.user = self.request.user
        client.save()
        return super(ClientCreateView, self).form_valid(form)


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    """Изменение клиента"""
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailing:client_list')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.creator == self.request.user or self.request.user.is_superuser:
            return self.object
        else:
            raise Http404


class ClientDeleteView(DeleteView):
    """Удаление клиента"""
    model = Client
    success_url = reverse_lazy('mailing:client_list')
    permission_required = 'mailing.delete_client'

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.creator == self.request.user or self.request.user.is_superuser:
            return self.object
        else:
            raise Http404


class MailingLogListView(ListView):
    """Просмотр логов"""
    model = MailingLogs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Попытки рассылки"
        context['log_list'] = MailingLogs.objects.all()
        return context





class MailingListView(ListView):
    model = Mailing
    extra_context = {'title': 'Рассылки'}
    paginate_by = 12

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        return queryset


class MailingDetailView(DetailView):
    model = Mailing


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingCreateForm
    success_url = reverse_lazy('mailing:mailing_list')



    def form_valid(self, form):
        self.object = form.save()
        self.object.status = 'CREATE'
        self.object.save()

        # message_service = MessageService(mailing)
        #
        # message_service.create_task()
        # mailing.status = 'START'
        # mailing.save()

        return super().form_valid(form)


class MailingUpdateView(LoginRequiredMixin, UpdateView):

    model = Mailing
    form_class = MailingCreateForm
    success_url = reverse_lazy('mailing:mailing_list')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.creator == self.request.user or self.request.user.is_superuser:
            return self.object
        else:
            raise Http404


    def form_valid(self, form):
        self.object = form.save()
        return super().form_valid(form)


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailing
    success_url = reverse_lazy('mailing:mailing_list')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.request.user.is_superuser:
            return self.object
        else:
            raise Http404


def categories(request):
    content = {
        'category_list': Category.objects.all(),
    }
    return render(request, 'mailing/categories.html', content)


def filtered_items(request, pk):
    category_item = Category.objects.get(pk=pk)
    content = {
        'object_list': Message.objects.filter(category_id=pk),
        'title': f'{category_item.name}',
        'description': f'{category_item.description}'
    }
    return render(request, 'mailing/filtered_messages.html', content)


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailing:message_list')

    def form_valid(self, form):
        self.object = form.save()
        self.object.creator = self.request.user
        self.object.save()
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UpdateView):

    model = Message
    form_class = MessageForm

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.creator == self.request.user or self.request.user.is_superuser:
            return self.object
        else:
            raise Http404


    def get_success_url(self):
        return reverse('mailing:message_edit', args=[self.kwargs.get('pk')])


    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        VersionFormset = inlineformset_factory(Message, MessageVersion, form=VersionForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = VersionFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = VersionFormset(instance=self.object)
        return context_data

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        self.object = form.save()

        if formset.is_valid():
            formset.instance = self.object
            formset.save()

        active_versions = MessageVersion.objects.filter(product=self.object, is_active=True)
        if active_versions.count() > 1:
            form.add_error(None, 'Choose one active version.')
            return self.form_invalid(form)
        return super().form_valid(form)


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    success_url = reverse_lazy('mailing:message_list')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.creator == self.request.user or self.request.user.is_superuser:
            return self.object
        else:
            raise Http404


class MessageListView(ListView):
    model = Message
    extra_context = {'title': 'Рассылки'}
    paginate_by = 12

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        return queryset


def get_current_user(request):
    current_user = request.user.get_username()
    return render(request, 'message_list.html', {'user':current_user})


class MessageDetailView(DetailView):
    model = Message


class HomePageView(TemplateView):
    template_name = 'home_page.html'



