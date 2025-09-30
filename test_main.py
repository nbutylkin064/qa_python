import pytest
from main import BooksCollector

class TestBooksCollector:

    # Тесты для add_new_book
    def test_add_new_book_valid_name_book_added(self):
        collector = BooksCollector()
        collector.add_new_book('Гарри Поттер')
        assert 'Гарри Поттер' in collector.books_genre

    @pytest.mark.parametrize('book_name', ['', 'a' * 41, 'Очень длинное название книги которое превышает лимит символов'])
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
    def test_set_book_genre_valid_book_and_genre_genre_set(self):
        collector = BooksCollector()
        collector.add_new_book('Марсианин')
        collector.set_book_genre('Марсианин', 'Фантастика')
        assert collector.get_book_genre('Марсианин') == 'Фантастика'

    def test_set_book_genre_invalid_genre_genre_not_set(self):
        collector = BooksCollector()
        collector.add_new_book('Книга')
        collector.set_book_genre('Книга', 'Несуществующий жанр')
        assert collector.get_book_genre('Книга') == ''

    def test_set_book_genre_nonexistent_book_genre_not_set(self):
        collector = BooksCollector()
        collector.set_book_genre('Несуществующая книга', 'Фантастика')
        assert 'Несуществующая книга' not in collector.books_genre

    # Тесты для get_book_genres
    def test_get_book_genre_existing_book_returns_genre(self):
        collector = BooksCollector()
        collector.add_new_book('Шерлок Холмс')
        collector.set_book_genre('Шерлок Холмс', 'Детективы')
        assert collector.get_book_genre('Шерлок Холмс') == collector.books_genre['Шерлок Холмс']

    def test_get_book_genre_nonexistent_book_returns_none(self):
        collector = BooksCollector()
        assert collector.get_book_genre('Несуществующая книга') is None

    # Тесты для get_books_with_specific_genre
    def test_get_books_with_specific_genre_returns_correct_books(self):
        collector = BooksCollector()
        collector.add_new_book('Война миров')
        collector.add_new_book('Марсианин')
        collector.set_book_genre('Война миров', 'Фантастика')
        collector.set_book_genre('Марсианин', 'Фантастика')

        fantasy_books = collector.get_books_with_specific_genre('Фантастика')
        assert 'Война миров' in fantasy_books
        assert 'Марсианин' in fantasy_books
        assert len(fantasy_books) == 2

    def test_get_books_with_specific_genre_invalid_genre_returns_empty_list(self):
        collector = BooksCollector()
        collector.add_new_book('Книга')
        result = collector.get_books_with_specific_genre('Несуществующий жанр')
        assert result == []

    # Тесты для get_books_genre
    def test_get_books_genre_returns_current_dict(self):
        collector = BooksCollector()
        collector.add_new_book('Книга 1')
        collector.add_new_book('Книга 2')
        assert collector.get_books_genre() == {'Книга 1': '', 'Книга 2': ''}

    # Тесты для get_books_for_children
    def test_get_books_for_children_returns_books_without_age_rating(self):
        collector = BooksCollector()
        collector.add_new_book('Ну погоди!')
        collector.add_new_book('Оно')
        collector.set_book_genre('Ну погоди!', 'Мультфильмы')
        collector.set_book_genre('Оно', 'Ужасы')

        children_books = collector.get_books_for_children()
        assert 'Ну погоди!' in children_books
        assert 'Оно' not in children_books

    # Тесты для add_book_in_favorites
    def test_add_book_in_favorites_valid_book_added(self):
        collector = BooksCollector()
        collector.add_new_book('Мастер и Маргарита')
        collector.add_book_in_favorites('Мастер и Маргарита')
        assert 'Мастер и Маргарита' in collector.favorites

    def test_add_book_in_favorites_nonexistent_book_not_added(self):
        collector = BooksCollector()
        collector.add_book_in_favorites('Несуществующая книга')
        assert 'Несуществующая книга' not in collector.favorites

    def test_add_book_in_favorites_duplicate_book_not_added(self):
        collector = BooksCollector()
        collector.add_new_book('Книга')
        collector.add_book_in_favorites('Книга')
        collector.add_book_in_favorites('Книга')
        assert len(collector.favorites) == 1

    # Тесты для delete_book_from_favorites
    def test_delete_book_from_favorites_existing_book_removed(self):
        collector = BooksCollector()
        collector.add_new_book('Книга')
        collector.add_book_in_favorites('Книга')
        collector.delete_book_from_favorites('Книга')
        assert 'Книга' not in collector.favorites

    def test_delete_book_from_favorites_nonexistent_book_no_error(self):
        collector = BooksCollector()
        # Должно выполниться без ошибок
        collector.delete_book_from_favorites('Несуществующая книга')

    # Тесты для get_list_of_favorites_books
    def test_get_list_of_favorites_books_returns_current_list(self):
        collector = BooksCollector()
        collector.add_new_book('Книга 1')
        collector.add_new_book('Книга 2')
        collector.add_book_in_favorites('Книга 1')
        collector.add_book_in_favorites('Книга 2')

        favorites = collector.get_list_of_favorites_books()
        assert favorites == ['Книга 1', 'Книга 2']