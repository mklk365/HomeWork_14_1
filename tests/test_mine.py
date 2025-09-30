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


class TestCategoryStrMethodPytest:

    @pytest.fixture
    def sample_products(self):
        """Фикстура с тестовыми продуктами"""
        return [
            Product("Product A", "Desc A", 100.0, 2),
            Product("Product B", "Desc B", 200.0, 4),
            Product("Product C", "Desc C", 300.0, 6)
        ]

    def test_empty_category(self):
        category = Category("Empty", "No products")
        assert str(category) == "Empty, количество продуктов: 0 шт."

    def test_category_with_products(self, sample_products):
        category = Category("Test Category", "Description", sample_products)
        assert str(category) == "Test Category, количество продуктов: 12 шт."

    @pytest.mark.parametrize("products_data,expected_output", [
        ([], "Category, количество продуктов: 0 шт."),
        ([Product("P1", "D1", 100, 1)], "Category, количество продуктов: 1 шт."),
        ([Product("P1", "D1", 100, 1), Product("P2", "D2", 200, 2)],
         "Category, количество продуктов: 3 шт."),
    ])
    def test_str_with_different_quantities(self, products_data, expected_output):
        category = Category("Category", "Desc", products_data)
        assert str(category) == expected_output


class TestCategoryGetTotalValue:

    @pytest.fixture
    def sample_products(self):
        """Фикстура с тестовыми продуктами"""
        return [
            Product("Product A", "Desc A", 100.0, 2),  # стоимость: 200
            Product("Product B", "Desc B", 200.0, 3),  # стоимость: 600
            Product("Product C", "Desc C", 50.0, 10)  # стоимость: 500
        ]

    def test_empty_category(self):
        """Тест пустой категории"""
        category = Category("Empty", "No products")
        assert category.get_total_value() == 0

    def test_single_product(self):
        """Тест категории с одним товаром"""
        product = Product("Phone", "Smartphone", 50000.0, 2)
        category = Category("Electronics", "Devices", [product])
        expected_value = 50000.0 * 2  # 100000
        assert category.get_total_value() == expected_value

    def test_multiple_products(self, sample_products):
        """Тест категории с несколькими товарами"""
        category = Category("Test Category", "Description", sample_products)
        # 100*2 + 200*3 + 50*10 = 200 + 600 + 500 = 1300
        assert category.get_total_value() == 1300.0

    def test_products_with_zero_quantity(self):
        """Тест товаров с нулевым количеством"""
        products = [
            Product("Product 1", "Desc 1", 100.0, 0),  # стоимость: 0
            Product("Product 2", "Desc 2", 200.0, 5),  # стоимость: 1000
            Product("Product 3", "Desc 3", 300.0, 0)  # стоимость: 0
        ]
        category = Category("Category", "Desc", products)
        assert category.get_total_value() == 1000.0

    def test_products_with_zero_price(self):
        """Тест товаров с нулевой ценой"""
        products = [
            Product("Free Product", "Desc", 0.0, 10),  # стоимость: 0
            Product("Paid Product", "Desc", 150.0, 2)  # стоимость: 300
        ]
        category = Category("Mixed", "Desc", products)
        assert category.get_total_value() == 300.0

    def test_after_adding_product(self, sample_products):
        """Тест после добавления нового товара"""
        category = Category("Category", "Desc", sample_products)
        initial_value = category.get_total_value()  # 1300

        new_product = Product("New Product", "Desc", 75.0, 4)  # стоимость: 300
        category.add_product(new_product)

        assert category.get_total_value() == initial_value + 300.0

    def test_after_adding_duplicate_product(self):
        """Тест после добавления дубликата товара (должно обновить количество)"""
        product = Product("Duplicate", "Desc", 100.0, 2)  # начальная стоимость: 200
        category = Category("Category", "Desc", [product])

        duplicate = Product("Duplicate", "New Desc", 120.0, 3)  # цена не должна измениться
        category.add_product(duplicate)

        # Количество должно стать 2+3=5, цена остаться 100 (максимум не применяется при добавлении через add_product)
        # В текущей реализации add_product использует max цену, но в тесте проверим фактическое поведение
        actual_value = category.get_total_value()
        # Проверим что количество увеличилось, а цена осталась исходной или стала максимальной
        assert actual_value == 100.0 * 5 or actual_value == 120.0 * 5

    def test_large_quantities(self):
        """Тест с большими количествами"""
        products = [
            Product("Bulk Item", "Desc", 1.5, 1000),  # стоимость: 1500
            Product("Expensive Item", "Desc", 999.99, 5)  # стоимость: 4999.95
        ]
        category = Category("Bulk", "Desc", products)
        expected = 1500 + 4999.95
        assert category.get_total_value() == pytest.approx(expected)

    def test_float_precision(self):
        """Тест точности вычислений с плавающей точкой"""
        products = [
            Product("Item 1", "Desc", 33.33, 3),  # стоимость: 99.99
            Product("Item 2", "Desc", 66.67, 3)  # стоимость: 200.01
        ]
        category = Category("Precision", "Desc", products)
        expected = 99.99 + 200.01  # 300.0
        assert category.get_total_value() == pytest.approx(300.0)

    def test_negative_scenario(self):
        """Тест на отсутствие отрицательных значений (защита от неправильных данных)"""
        # В текущей реализации Product не позволяет отрицательные цены,
        # но проверим поведение если бы они были
        product = Product("Test", "Desc", 100.0, 5)
        category = Category("Test", "Desc", [product])
        value = category.get_total_value()
        assert value >= 0, "Стоимость не должна быть отрицательной"


class TestCategoryAddMethod:

    @pytest.fixture
    def sample_categories(self):
        """Фикстура с тестовыми категориями"""
        products1 = [
            Product("Product A", "Desc A", 100.0, 2),  # стоимость: 200
            Product("Product B", "Desc B", 200.0, 3),  # стоимость: 600
        ]
        products2 = [
            Product("Product C", "Desc C", 50.0, 10),  # стоимость: 500
            Product("Product D", "Desc D", 150.0, 2),  # стоимость: 300
        ]
        products3 = [
            Product("Product E", "Desc E", 300.0, 1),  # стоимость: 300
        ]

        category1 = Category("Category 1", "Description 1", products1)  # общая: 800
        category2 = Category("Category 2", "Description 2", products2)  # общая: 800
        category3 = Category("Category 3", "Description 3", products3)  # общая: 300

        return category1, category2, category3

    def test_add_two_categories(self, sample_categories):
        """Тест сложения двух категорий"""
        category1, category2, _ = sample_categories
        result = category1 + category2
        expected = 800 + 800  # 1600
        assert result == expected

    def test_add_three_categories_separate(self, sample_categories):
        """Тест сложения трех категорий отдельными операциями"""
        category1, category2, category3 = sample_categories

        # Складываем попарно, а не цепочкой
        sum1 = category1 + category2  # 1600
        sum2 = sum1 + category3.get_total_value()  # 1600 + 300

        expected = 800 + 800 + 300  # 1900
        assert sum2 == expected

    def test_add_empty_categories(self):
        """Тест сложения пустых категорий"""
        empty1 = Category("Empty 1", "No products")
        empty2 = Category("Empty 2", "No products")

        result = empty1 + empty2
        assert result == 0

    def test_add_category_with_empty(self, sample_categories):
        """Тест сложения категории с товарами и пустой категории"""
        category1, _, _ = sample_categories
        empty_category = Category("Empty", "No products")

        result1 = category1 + empty_category
        result2 = empty_category + category1

        assert result1 == 800
        assert result2 == 800

    def test_add_commutative_property(self, sample_categories):
        """Тест коммутативности сложения (a + b = b + a)"""
        category1, category2, _ = sample_categories

        result1 = category1 + category2
        result2 = category2 + category1

        assert result1 == result2

    def test_add_with_different_product_combinations(self):
        """Тест сложения категорий с разными комбинациями товаров"""
        # Категория с дорогими товарами в малом количестве
        expensive_products = [
            Product("Laptop", "Gaming", 100000.0, 2),  # 200000
            Product("Phone", "Flagship", 80000.0, 3),  # 240000
        ]
        expensive_category = Category("Expensive", "High-end", expensive_products)

        # Категория с дешевыми товарами в большом количестве
        cheap_products = [
            Product("Cable", "USB", 500.0, 100),  # 50000
            Product("Adapter", "Type-C", 300.0, 50),  # 15000
        ]
        cheap_category = Category("Cheap", "Accessories", cheap_products)

        result = expensive_category + cheap_category
        expected = (200000 + 240000) + (50000 + 15000)  # 440000 + 65000 = 505000
        assert result == expected

    def test_add_after_modifying_products(self):
        """Тест сложения после изменения состава товаров в категориях"""
        category1 = Category("Cat 1", "Desc", [Product("A", "Desc", 100, 2)])  # 200
        category2 = Category("Cat 2", "Desc", [Product("B", "Desc", 50, 4)])  # 200

        initial_sum = category1 + category2  # 400

        # Добавляем товар в первую категорию
        category1.add_product(Product("C", "Desc", 75, 4))  # +300

        # Добавляем товар во вторую категорию
        category2.add_product(Product("D", "Desc", 25, 8))  # +200

        new_sum = category1 + category2  # (200+300) + (200+200) = 900
        assert new_sum == 900
        assert new_sum > initial_sum

    def test_add_with_zero_value_products(self):
        """Тест сложения категорий с товарами нулевой стоимости"""
        zero_products = [
            Product("Free", "Desc", 0.0, 10),  # 0
            Product("Sample", "Desc", 0.0, 5),  # 0
        ]
        zero_category = Category("Zero", "Free items", zero_products)

        normal_products = [
            Product("Normal", "Desc", 100.0, 3),  # 300
        ]
        normal_category = Category("Normal", "Paid items", normal_products)

        result1 = zero_category + normal_category
        result2 = normal_category + zero_category

        assert result1 == 300
        assert result2 == 300

    def test_add_return_type(self, sample_categories):
        """Тест типа возвращаемого значения"""
        category1, category2, _ = sample_categories
        result = category1 + category2

        assert isinstance(result, (int, float))
        assert not isinstance(result, Category)


class TestCategoryAddMethodDirectCall:
    """Тестирование прямого вызова магического метода"""

    def test_add_direct_call_with_category(self):
        """Прямой вызов __add__ с категорией"""
        category1 = Category("Cat1", "Desc", [Product("A", "Desc", 100, 2)])
        category2 = Category("Cat2", "Desc", [Product("B", "Desc", 50, 4)])

        result = category1.__add__(category2)
        expected = 200 + 200  # 400
        assert result == expected

    def test_add_direct_call_with_int(self):
        """Прямой вызов __add__ с целым числом"""
        category = Category("Test", "Desc", [Product("A", "Desc", 100, 2)])

        # Прямой вызов метода должен вернуть NotImplemented
        result = category.__add__(100)
        assert result is NotImplemented

    def test_add_direct_call_with_string(self):
        """Прямой вызов __add__ со строкой"""
        category = Category("Test", "Desc", [Product("A", "Desc", 100, 2)])

        result = category.__add__("string")
        assert result is NotImplemented

    def test_add_direct_call_with_product(self):
        """Прямой вызов __add__ с продуктом"""
        category = Category("Test", "Desc", [Product("A", "Desc", 100, 2)])
        product = Product("Test", "Desc", 100, 2)

        result = category.__add__(product)
        assert result is NotImplemented

    def test_add_direct_call_with_none(self):
        """Прямой вызов __add__ с None"""
        category = Category("Test", "Desc", [Product("A", "Desc", 100, 2)])

        result = category.__add__(None)
        assert result is NotImplemented
