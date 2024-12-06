from django.contrib import admin
from django.urls import path, include
from notes.views import notes_list, create_note, edit_note, delete_note, NoteListView, NoteDetailView

urlpatterns = [
    path('admin/', admin.site.urls),

    # API маршруты
    path('api/notes/', NoteListView.as_view(), name='api_notes_list'),
    path('api/notes/<int:pk>/', NoteDetailView.as_view(), name='api_note_detail'),

    # HTML маршруты
    path('notes/', notes_list, name='notes_list'),
    path('notes/create/', create_note, name='create_note'),
    path('notes/edit/<int:note_id>/', edit_note, name='edit_note'),
    path('notes/delete/<int:note_id>/', delete_note, name='delete_note'),
]
