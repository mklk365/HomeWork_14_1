import pytest
from mine import Product, Category


@pytest.fixture(autouse=True)
def reset_counters():
    """Сброс счетчиков перед каждым тестом"""
    Product.product_count = 0
    Category.category_count = 0
    Category.product_count = 0
    yield


def test_product_initialization():
    """Тест корректности инициализации объекта Product"""
    product = Product("Test Product", "Test Description", 100.0, 10)

    assert product.name == "Test Product"
    assert product.description == "Test Description"
    assert product.price == 100.0
    assert product.quantity == 10


def test_category_initialization():
    """Тест корректности инициализации объекта Category"""
    category = Category("Test Category", "Test Category Description")

    assert category.name == "Test Category"
    assert category.description == "Test Category Description"
    assert category.products == ""


def test_category_with_products_initialization():
    """Тест инициализации Category с продуктами"""
    product1 = Product("Product 1", "Desc 1", 50.0, 5)
    product2 = Product("Product 2", "Desc 2", 75.0, 3)

    category = Category("Test Category", "Test Desc", [product1, product2])

    # Используем свойство products вместо прямого доступа к приватному атрибуту
    products_str = category.products
    assert "Product 1" in products_str
    assert "Product 2" in products_str


def test_product_count_increment():
    """Тест подсчета количества созданных продуктов"""
    assert Product.product_count == 0

    Product("P1", "D1", 10.0, 1)
    assert Product.product_count == 1

    Product("P2", "D2", 20.0, 2)
    assert Product.product_count == 2

    Product("P3", "D3", 30.0, 3)
    assert Product.product_count == 3


def test_category_count_increment():
    """Тест подсчета количества созданных категорий"""
    assert Category.category_count == 0

    Category("Cat1", "Desc1")
    assert Category.category_count == 1

    Category("Cat2", "Desc2")
    assert Category.category_count == 2


def test_category_product_count_increment():
    """Тест подсчета количества продуктов в категориях"""
    assert Category.product_count == 0

    # Создаем продукты
    product1 = Product("P1", "D1", 10.0, 1)
    product2 = Product("P2", "D2", 20.0, 2)
    product3 = Product("P3", "D3", 30.0, 3)

    # Создаем категорию с 2 продуктами
    Category("Cat1", "Desc1", [product1, product2])
    assert Category.product_count == 2

    # Создаем категорию с 1 продуктом
    Category("Cat2", "Desc2", [product3])
    assert Category.product_count == 3

    # Создаем пустую категорию
    Category("Cat3", "Desc3")
    assert Category.product_count == 3  # Не должно измениться


def test_multiple_categories_with_shared_products():
    """Тест с несколькими категориями, содержащими общие продукты"""
    product1 = Product("P1", "D1", 10.0, 1)
    product2 = Product("P2", "D2", 20.0, 2)

    # Один продукт может быть в нескольких категориях
    Category("Cat1", "Desc1", [product1, product2])
    Category("Cat2", "Desc2", [product1])

    assert Product.product_count == 2  # 2 уникальных продукта
    assert Category.product_count == 3  # 2 в первой + 1 во второй
    assert Category.category_count == 2  # 2 категории


def test_empty_category_creation():
    """Тест создания пустой категории"""
    category = Category("Empty Category", "No products")

    assert category.name == "Empty Category"
    assert category.products == ""
    assert Category.category_count == 1
    assert Category.product_count == 0  # Продуктов не добавлено


def test_product_attributes_types():
    """Тест типов данных атрибутов Product"""
    product = Product("Test", "Desc", 99.99, 5)

    assert isinstance(product.name, str)
    assert isinstance(product.description, str)
    assert isinstance(product.price, float)
    assert isinstance(product.quantity, int)


def test_category_attributes_types():
    """Тест типов данных атрибутов Category"""
    product = Product("P", "D", 10.0, 1)
    category = Category("Cat", "Desc", [product])

    assert isinstance(category.name, str)
    assert isinstance(category.description, str)
    assert isinstance(category.products, str)  # Теперь это строка


def test_main_block_functionality():
    """Тест функционала из основного блока"""
    # Тестируем создание продуктов как в main блоке
    product1 = Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5)
    assert product1.name == "Samsung Galaxy S23 Ultra"
    assert product1.price == 180000.0

    product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)

    # Тестируем создание категории как в main блоке
    category = Category(
        "Смартфоны",
        "Смартфоны, как средство не только коммуникации, но и получения "
        "дополнительных функций для удобства жизни",
        [product1, product2, product3],
    )

    assert category.name == "Смартфоны"
    assert len(category._Category__products) == 3


def test_product_price_setter():
    """Тест сеттера цены с валидацией"""
    product = Product("Test", "Desc", 100.0, 5)

    # Корректное значение
    product.price = 150.0
    assert product.price == 150.0

    # Попытка установить отрицательную цену
    product.price = -50.0
    assert product.price == 150.0  # Должна остаться предыдущая цена

    # Попытка установить нулевую цену
    product.price = 0
    assert product.price == 150.0  # Должна остаться предыдущая цена


def test_new_product_method():
    """Тест класс-метода new_product"""
    product_data = {
        "name": "Test Product",
        "description": "Test Description",
        "price": 100.0,
        "quantity": 5
    }

    # Создание нового продукта
    product = Product.new_product(product_data)
    assert product.name == "Test Product"
    assert product.price == 100.0
    assert product.quantity == 5


def test_new_product_with_duplicate():
    """Тест new_product с дубликатом"""
    existing_products = [
        Product("Existing Product", "Old Desc", 50.0, 10)
    ]

    product_data = {
        "name": "Existing Product",  # Дубликат
        "description": "New Desc",
        "price": 60.0,
        "quantity": 5
    }

    # Должен обновить существующий продукт
    result = Product.new_product(product_data, existing_products)
    assert result is existing_products[0]
    assert result.quantity == 15  # 10 + 5
    assert result.price == 60.0  # Максимальная цена
    assert result.description == "New Desc"


def test_add_product_with_duplicate():
    """Тест добавления дублирующегося продукта в категорию"""
    category = Category("Test", "Desc")
    product1 = Product("Same Product", "Desc1", 100.0, 5)
    product2 = Product("Same Product", "Desc2", 120.0, 3)  # Дубликат

    category.add_product(product1)
    assert len(category._Category__products) == 1
    assert Category.product_count == 1

    category.add_product(product2)
    assert len(category._Category__products) == 1  # Должен остаться один продукт
    assert category._Category__products[0].quantity == 8  # 5 + 3
    assert category._Category__products[0].price == 120.0  # Максимальная цена
    assert Category.product_count == 1  # Не должно увеличиться


def test_products_property_format():
    """Тест формата строкового представления продуктов"""
    product = Product("Test", "Desc", 100.0, 5)
    category = Category("Test", "Desc", [product])

    products_str = category.products
    expected = "Test, 100.0 руб. Остаток: 5 шт."
    assert products_str == expected


def test_product_with_zero_quantity():
    """Тест продукта с нулевым количеством"""
    product = Product("Test", "Desc", 100.0, 0)
    assert product.quantity == 0


def test_category_with_empty_products_list():
    """Тест категории с пустым списком продуктов"""
    category = Category("Test", "Desc", [])
    assert category.products == ""


def test_price_decrease_confirmation(monkeypatch):
    """Тест подтверждения понижения цены"""
    product = Product("Test", "Desc", 100.0, 5)

    # Симулируем ввод 'y' (согласие)
    monkeypatch.setattr('builtins.input', lambda _: 'y')
    product.price = 80.0
    assert product.price == 80.0

    # Симулируем ввод 'n' (отмена)
    monkeypatch.setattr('builtins.input', lambda _: 'n')
    product.price = 70.0
    assert product.price == 80.0  # Цена не должна измениться

    # Симулируем любой другой ввод (отмена)
    monkeypatch.setattr('builtins.input', lambda _: 'any')
    product.price = 60.0
    assert product.price == 80.0  # Цена не должна измениться


def test_price_increase_no_confirmation():
    """Тест повышения цены без подтверждения"""
    product = Product("Test", "Desc", 100.0, 5)

    # Повышение цены не требует подтверждения
    product.price = 120.0
    assert product.price == 120.0


def test_price_same_no_confirmation():
    """Тест установки той же цены без подтверждения"""
    product = Product("Test", "Desc", 100.0, 5)

    # Та же цена не требует подтверждения
    product.price = 100.0
    assert product.price == 100.0


def test_price_decrease_confirmation_uppercase(monkeypatch):
    """Тест подтверждения с заглавной Y"""
    product = Product("Test", "Desc", 100.0, 5)

    # Симулируем ввод 'Y' (согласие)
    monkeypatch.setattr('builtins.input', lambda _: 'Y')
    product.price = 90.0
    assert product.price == 90.0