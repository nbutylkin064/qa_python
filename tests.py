import pytest
from main import BooksCollector

class TestBooksCollector:

    # Тесты для add_new_book
    @pytest.mark.parametrize('book_name', ['Гордость и предубеждение и зомби', 'Что делать, если ваш кот хочет вас убить'])
    def test_add_new_book_valid_name_book_added(self, book_name):
        collector = BooksCollector()
        collector.add_new_book(book_name)
        assert book_name in collector.books_genre
        assert collector.books_genre[book_name] == ''

    @pytest.mark.parametrize('book_name', ['', 'a' * 41])
    def test_add_new_book_invalid_name_book_not_added(self, book_name):
        collector = BooksCollector()
        collector.add_new_book(book_name)
        assert book_name not in collector.books_genre

    def test_add_new_book_duplicate_book_not_added(self):
        collector = BooksCollector()
        collector.add_new_book('Преступление и наказание')
        collector.add_new_book('Преступление и наказание')
        assert len(collector.books_genre) == 1

    # Тесты для set_book_genre
    @pytest.mark.parametrize('book_name, genre', [
        ('Марсианин', 'Фантастика'),
        ('Шерлок Холмс', 'Детективы')
    ])
    def test_set_book_genre_valid_book_and_genre_genre_set(self, book_name, genre):
        collector = BooksCollector()
        collector.add_new_book(book_name)
        collector.set_book_genre(book_name, genre)
        assert collector.books_genre[book_name] == genre

    def test_set_book_genre_invalid_genre_genre_not_set(self):
        collector = BooksCollector()
        collector.add_new_book('Книга')
        collector.set_book_genre('Книга', 'Несуществующий жанр')
        assert collector.books_genre['Книга'] == ''

    # Тесты для get_book_genre
    def test_get_book_genre_nonexistent_book_returns_none(self):
        collector = BooksCollector()
        assert collector.get_book_genre('Несуществующая книга') is None

    # Тесты для get_books_with_specific_genre
    def test_get_books_with_specific_genre_returns_correct_books(self):
        collector = BooksCollector()
        collector.add_new_book('Война миров')
        collector.add_new_book('Марсианин')
        collector.add_new_book('Оно')
        collector.set_book_genre('Война миров', 'Фантастика')
        collector.set_book_genre('Марсианин', 'Фантастика')
        collector.set_book_genre('Оно', 'Ужасы')
        
        fantasy_books = collector.get_books_with_specific_genre('Фантастика')
        assert 'Война миров' in fantasy_books
        assert 'Марсианин' in fantasy_books
        assert 'Оно' not in fantasy_books

    # Тесты для get_books_for_children
    def test_get_books_for_children_returns_books_without_age_rating(self):
        collector = BooksCollector()
        collector.add_new_book('Ну погоди!')
        collector.add_new_book('Оно')
        collector.add_new_book('Шерлок Холмс')
        collector.set_book_genre('Ну погоди!', 'Мультфильмы')
        collector.set_book_genre('Оно', 'Ужасы')
        collector.set_book_genre('Шерлок Холмс', 'Детективы')
        
        children_books = collector.get_books_for_children()
        assert 'Ну погоди!' in children_books
        assert 'Оно' not in children_books
        assert 'Шерлок Холмс' not in children_books

    # Тесты для add_book_in_favorites и get_list_of_favorites_books
    def test_add_book_in_favorites_and_get_list(self):
        collector = BooksCollector()
        collector.add_new_book('Мастер и Маргарита')
        collector.add_new_book('Преступление и наказание')
        
        collector.add_book_in_favorites('Мастер и Маргарита')
        collector.add_book_in_favorites('Преступление и наказание')
        
        assert 'Мастер и Маргарита' in collector.favorites
        assert 'Преступление и наказание' in collector.favorites
        
        favorites = collector.get_list_of_favorites_books()
        assert 'Мастер и Маргарита' in favorites
        assert 'Преступление и наказание' in favorites
        assert len(favorites) == 2

    # Тесты для delete_book_from_favorites
    def test_delete_book_from_favorites(self):
        collector = BooksCollector()
        collector.add_new_book('Книга')
        collector.add_book_in_favorites('Книга')
        
        collector.delete_book_from_favorites('Книга')
        assert 'Книга' not in collector.favorites
        assert collector.get_list_of_favorites_books() == []