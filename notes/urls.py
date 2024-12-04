from django.urls import path
from .views import NoteListView, NoteDetailView

urlpatterns = [
    # API маршруты
    path('notes/', NoteListView.as_view(), name='api_notes_list'),
    path('notes/<int:pk>/', NoteDetailView.as_view(), name='api_note_detail'),
]
