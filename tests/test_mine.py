import pytest
from mine import Product, Category


class TestCategoryAndProduct:

    def setup_method(self):
        """Сброс счетчиков перед каждым тестом"""
        Product.product_count = 0
        Category.category_count = 0
        Category.product_count = 0

    def test_product_initialization(self):
        """Тест корректности инициализации объекта Product"""
        product = Product("Test Product", "Test Description", 100.0, 10)

        assert product.name == "Test Product"
        assert product.description == "Test Description"
        assert product.price == 100.0
        assert product.quantity == 10

    def test_category_initialization(self):
        """Тест корректности инициализации объекта Category"""
        category = Category("Test Category", "Test Category Description")

        assert category.name == "Test Category"
        assert category.description == "Test Category Description"
        assert category.products == []

    def test_category_with_products_initialization(self):
        """Тест инициализации Category с продуктами"""
        product1 = Product("Product 1", "Desc 1", 50.0, 5)
        product2 = Product("Product 2", "Desc 2", 75.0, 3)

        category = Category("Test Category", "Test Desc", [product1, product2])

        assert len(category.products) == 2
        assert category.products[0].name == "Product 1"
        assert category.products[1].name == "Product 2"

    def test_product_count_increment(self):
        """Тест подсчета количества созданных продуктов"""
        assert Product.product_count == 0

        Product("P1", "D1", 10.0, 1)
        assert Product.product_count == 1

        Product("P2", "D2", 20.0, 2)
        assert Product.product_count == 2

        Product("P3", "D3", 30.0, 3)
        assert Product.product_count == 3

    def test_category_count_increment(self):
        """Тест подсчета количества созданных категорий"""
        assert Category.category_count == 0

        Category("Cat1", "Desc1")
        assert Category.category_count == 1

        Category("Cat2", "Desc2")
        assert Category.category_count == 2

    def test_category_product_count_increment(self):
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

    def test_multiple_categories_with_shared_products(self):
        """Тест с несколькими категориями, содержащими общие продукты"""
        product1 = Product("P1", "D1", 10.0, 1)
        product2 = Product("P2", "D2", 20.0, 2)

        # Один продукт может быть в нескольких категориях
        Category("Cat1", "Desc1", [product1, product2])
        Category("Cat2", "Desc2", [product1])

        assert Product.product_count == 2  # 2 уникальных продукта
        assert Category.product_count == 3  # 2 в первой + 1 во второй
        assert Category.category_count == 2  # 2 категории

    def test_empty_category_creation(self):
        """Тест создания пустой категории"""
        category = Category("Empty Category", "No products")

        assert category.name == "Empty Category"
        assert len(category.products) == 0
        assert Category.category_count == 1
        assert Category.product_count == 0  # Продуктов не добавлено

    def test_product_attributes_types(self):
        """Тест типов данных атрибутов Product"""
        product = Product("Test", "Desc", 99.99, 5)

        assert isinstance(product.name, str)
        assert isinstance(product.description, str)
        assert isinstance(product.price, float)
        assert isinstance(product.quantity, int)

    def test_category_attributes_types(self):
        """Тест типов данных атрибутов Category"""
        product = Product("P", "D", 10.0, 1)
        category = Category("Cat", "Desc", [product])

        assert isinstance(category.name, str)
        assert isinstance(category.description, str)
        assert isinstance(category.products, list)

    def test_main_block_functionality(self):
        """Тест функционала из основного блока"""
        # Тестируем создание продуктов как в main блоке
        product1 = Product("Samsung Galaxy S23 Ultra",
                           "256GB, Серый цвет, 200MP камера", 180000.0, 5)
        assert product1.name == "Samsung Galaxy S23 Ultra"
        assert product1.price == 180000.0

        product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
        product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)

        # Тестируем создание категории как в main блоке
        category = Category(
            "Смартфоны",
            "Смартфоны, как средство не только коммуникации, но и получения "
            "дополнительных функций для удобства жизни",
            [product1, product2, product3]
        )

        assert category.name == "Смартфоны"
        assert len(category.products) == 3
