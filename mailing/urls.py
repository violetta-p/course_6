from django.urls import path
from mailing.apps import MailingConfig
from mailing.views import ClientListView, ClientDetailView, ClientCreateView, ClientUpdateView, ClientDeleteView, \
    MailingListView, MailingDetailView, MailingUpdateView, MailingDeleteView, categories, filtered_items, \
    MailingCreateView, MessageCreateView, MessageListView, MessageDetailView, MessageUpdateView, MessageDeleteView,\
    HomePageView

app_name = MailingConfig.name


urlpatterns = [
    path('client/create/', ClientCreateView.as_view(), name='client_create'),
    path('client/list/', ClientListView.as_view(), name='client_list'),
    path('client/view/<int:pk>', ClientDetailView.as_view(), name='client_view'),
    path('client/edit/<int:pk>/', ClientUpdateView.as_view(), name='client_edit'),
    path('client/delete/<int:pk>/', ClientDeleteView.as_view(), name='client_delete'),
    path('mailing/create/', MailingCreateView.as_view(), name='mailing_create'),
    path('mailing/', MailingListView.as_view(), name='mailing_list'),
    path('mailing/view/<int:pk>', MailingDetailView.as_view(), name='mailing_view'),
    path('mailing/edit/<int:pk>/', MailingUpdateView.as_view(), name='mailing_edit'),
    path('mailing/delete/<int:pk>/', MailingDeleteView.as_view(), name='mailing_delete'),
    path('message/create/', MessageCreateView.as_view(), name='message_create'),
    path('message/', MessageListView.as_view(), name='message_list'),
    path('message/view/<int:pk>', MessageDetailView.as_view(), name='message_detail'),
    path('message/edit/<int:pk>/', MessageUpdateView.as_view(), name='message_edit'),
    path('message/delete/<int:pk>/', MessageDeleteView.as_view(), name='message_delete'),
    path('', categories, name="categories"),
    path('<int:pk>/items/', filtered_items, name="filtered_messages"),
    path('home_page/', HomePageView.as_view(), name="home_page")


]
