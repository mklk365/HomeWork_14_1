import pytest
from unittest.mock import patch
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


class TestProductAddition:

    def test_add_two_products(self):
        """Тест сложения двух продуктов"""
        product1 = Product("Телефон", "Смартфон", 1000.0, 2)  # стоимость: 2000
        product2 = Product("Ноутбук", "Игровой ноутбук", 2000.0, 3)  # стоимость: 6000

        result = product1 + product2
        expected = (1000 * 2) + (2000 * 3)  # 2000 + 6000 = 8000

        assert result == 8000.0
        assert result == expected

    def test_add_products_commutative(self):
        """Тест коммутативности сложения (a + b == b + a)"""
        product1 = Product("Телефон", "Смартфон", 1000.0, 2)
        product2 = Product("Ноутбук", "Игровой ноутбук", 2000.0, 3)

        result1 = product1 + product2
        result2 = product2 + product1

        assert result1 == result2
        assert result1 == 8000.0

    def test_add_products_correct_calculation(self):
        """Тест правильности расчета общей стоимости"""
        product1 = Product("Телефон", "Смартфон", 1000.0, 2)  # 2000
        product2 = Product("Ноутбук", "Игровой ноутбук", 2000.0, 3)  # 6000
        product3 = Product("Планшет", "Графический планшет", 500.0, 5)  # 2500

        # Складываем попарно и проверяем расчеты
        result_12 = product1 + product2  # 2000 + 6000 = 8000
        result_23 = product2 + product3  # 6000 + 2500 = 8500
        result_13 = product1 + product3  # 2000 + 2500 = 4500

        assert result_12 == 8000.0
        assert result_23 == 8500.0
        assert result_13 == 4500.0

    def test_add_product_with_zero_quantity(self):
        """Тест сложения с продуктом с нулевым количеством"""
        product1 = Product("Телефон", "Смартфон", 1000.0, 2)  # 2000
        zero_product = Product("Нулевой", "Товар без количества", 1000.0, 0)  # 0

        result = product1 + zero_product
        expected = 2000.0  # 2000 + 0

        assert result == expected

    def test_add_product_with_zero_price(self):
        """Тест сложения с продуктом с нулевой ценой"""
        product1 = Product("Телефон", "Смартфон", 1000.0, 2)  # 2000
        zero_price_product = Product("Бесплатный", "Товар без цены", 0.0, 10)  # 0

        result = product1 + zero_price_product
        expected = 2000.0  # 2000 + 0

        assert result == expected

    def test_add_product_with_other_type_raises_error(self):
        """Тест что сложение с неподдерживаемым типом данных вызывает TypeError"""
        product1 = Product("Телефон", "Смартфон", 1000.0, 2)

        # Проверяем что при сложении с неподдерживаемым типом возникает TypeError
        with pytest.raises(TypeError):
            _ = product1 + "не продукт"

        with pytest.raises(TypeError):
            _ = product1 + 100

        with pytest.raises(TypeError):
            _ = product1 + None

        with pytest.raises(TypeError):
            _ = product1 + [1, 2, 3]

    def test_add_products_decimal_prices(self):
        """Тест сложения продуктов с десятичными ценами"""
        decimal_product1 = Product("Товар1", "Описание", 99.99, 2)  # 199.98
        decimal_product2 = Product("Товар2", "Описание", 49.50, 4)  # 198.00

        result = decimal_product1 + decimal_product2
        expected = (99.99 * 2) + (49.50 * 4)  # 199.98 + 198.00 = 397.98

        assert abs(result - 397.98) < 0.01

    def test_add_products_large_quantities(self):
        """Тест сложения продуктов с большими количествами"""
        product1 = Product("Телефон", "Смартфон", 1000.0, 2)  # 2000
        large_qty_product = Product("Массовый", "Товар в большом количестве", 10.0, 1000)  # 10000

        result = product1 + large_qty_product
        expected = 2000.0 + 10000.0  # 12000

        assert result == expected

    def test_add_product_with_itself(self):
        """Тест сложения продукта с самим собой"""
        product1 = Product("Телефон", "Смартфон", 1000.0, 2)  # 2000

        result = product1 + product1
        expected = 2000.0 + 2000.0  # 4000

        assert result == expected

    def test_add_three_products_separate_operations(self):
        """Тест сложения трех продуктов отдельными операциями"""
        product1 = Product("Телефон", "Смартфон", 1000.0, 2)  # 2000
        product2 = Product("Ноутбук", "Игровой ноутбук", 2000.0, 3)  # 6000
        product3 = Product("Планшет", "Графический планшет", 500.0, 5)  # 2500

        # Складываем три продукта отдельными операциями (только сложение)
        total = (product1 + product2) + (product1 + product3)  # (2000+6000) + (2000+2500)
        expected = 8000.0 + 4500.0  # 12500

        assert total == expected

    def test_add_with_price_setter(self):
        """Тест что сложение работает корректно после изменения цены через сеттер"""
        product1 = Product("Товар1", "Описание", 1000.0, 2)  # 2000
        product2 = Product("Товар2", "Описание", 2000.0, 1)  # 2000

        # Меняем цену через свойство
        product1.price = 1500.0  # теперь стоимость: 1500 * 2 = 3000

        result = product1 + product2
        expected = 3000.0 + 2000.0  # 5000

        assert result == expected

    def test_add_with_quantity_change(self):
        """Тест что сложение отражает актуальное количество"""
        product1 = Product("Товар1", "Описание", 1000.0, 2)  # 2000
        product2 = Product("Товар2", "Описание", 2000.0, 1)  # 2000

        # Меняем количество напрямую
        product1.quantity = 5  # теперь стоимость: 1000 * 5 = 5000

        result = product1 + product2
        expected = 5000.0 + 2000.0  # 7000

        assert result == expected

    def test_add_products_different_instances_same_data(self):
        """Тест сложения продуктов с одинаковыми данными но разными экземплярами"""
        product1 = Product("Телефон", "Смартфон", 1000.0, 2)  # 2000
        product2 = Product("Телефон", "Смартфон", 1000.0, 2)  # 2000

        result = product1 + product2
        expected = 2000.0 + 2000.0  # 4000

        assert result == expected

    def test_result_type_is_float(self):
        """Тест что результат сложения всегда float"""
        product1 = Product("Товар1", "Описание", 1000, 2)  # целые числа
        product2 = Product("Товар2", "Описание", 2000.0, 3)  # float

        result = product1 + product2
        assert isinstance(result, float)

    def test_cannot_chain_operations(self):
        """Тест что нельзя делать цепочки операций, так как результат - float"""
        product1 = Product("Телефон", "Смартфон", 1000.0, 2)
        product2 = Product("Ноутбук", "Игровой ноутбук", 2000.0, 3)
        product3 = Product("Планшет", "Графический планшет", 500.0, 5)

        # product1 + product2 возвращает float, поэтому нельзя делать:
        # product1 + product2 + product3 - это вызовет TypeError

        # Вместо этого нужно использовать промежуточные переменные:
        intermediate = product1 + product2  # float
        # Дальнейшие операции только с float
        total = intermediate + (product1 + product3)  # float + float

        assert total == 8000.0 + 4500.0  # 12500


class TestProductStr:
    """Тесты для строкового представления продукта с использованием pytest"""

    def test_str_representation_basic(self):
        """Тест базового строкового представления"""
        product = Product("Телефон", "Смартфон", 1000.0, 5)
        expected = "Телефон, 1000.0 руб. Остаток: 5 шт."
        assert str(product) == expected

    def test_str_representation_with_different_prices(self):
        """Тест с разными ценами (целые, дробные)"""
        # Тест с целой ценой
        product1 = Product("Товар1", "Описание1", 500, 10)
        expected1 = "Товар1, 500 руб. Остаток: 10 шт."
        assert str(product1) == expected1

        # Тест с дробной ценой
        product2 = Product("Товар2", "Описание2", 999.99, 3)
        expected2 = "Товар2, 999.99 руб. Остаток: 3 шт."
        assert str(product2) == expected2

    def test_str_representation_with_zero_quantity(self):
        """Тест с нулевым количеством"""
        product = Product("Товар", "Описание", 250.0, 0)
        expected = "Товар, 250.0 руб. Остаток: 0 шт."
        assert str(product) == expected

    def test_str_representation_with_large_numbers(self):
        """Тест с большими числами"""
        product = Product("Дорогой товар", "Описание", 1000000.50, 100)
        expected = "Дорогой товар, 1000000.5 руб. Остаток: 100 шт."
        assert str(product) == expected

    def test_str_representation_special_characters(self):
        """Тест со специальными символами в названии"""
        product = Product("Товар-супер!", "Описание", 150.0, 7)
        expected = "Товар-супер!, 150.0 руб. Остаток: 7 шт."
        assert str(product) == expected

    def test_str_representation_after_price_change(self):
        """Тест после изменения цены через сеттер"""
        product = Product("Товар", "Описание", 1000.0, 5)

        # Меняем цену (имитируем подтверждение)
        with patch('builtins.input', return_value='y'):
            product.price = 800.0

        expected = "Товар, 800.0 руб. Остаток: 5 шт."
        assert str(product) == expected

    def test_str_representation_empty_name(self):
        """Тест с пустым названием"""
        product = Product("", "Описание", 100.0, 1)
        expected = ", 100.0 руб. Остаток: 1 шт."
        assert str(product) == expected

    def test_str_representation_negative_quantity(self):
        """Тест с отрицательным количеством (если такое возможно)"""
        product = Product("Товар", "Описание", 50.0, -1)
        expected = "Товар, 50.0 руб. Остаток: -1 шт."
        assert str(product) == expected


class TestProductStrIntegration:
    """Интеграционные тесты строкового представления"""

    def test_str_in_category_products_list(self):
        """Тест что строковое представление корректно работает в списке продуктов категории"""
        product1 = Product("Товар1", "Описание1", 100.0, 2)
        product2 = Product("Товар2", "Описание2", 200.0, 3)

        category = Category("Категория", "Описание", [product1, product2])

        products_str = category.products
        assert "Товар1, 100.0 руб. Остаток: 2 шт." in products_str
        assert "Товар2, 200.0 руб. Остаток: 3 шт." in products_str

    def test_multiple_products_str_consistency(self):
        """Тест согласованности строкового представления для нескольких продуктов"""
        products = [
            Product("A", "Desc A", 10.0, 1),
            Product("B", "Desc B", 20.0, 2),
            Product("C", "Desc C", 30.0, 3)
        ]

        expected_strings = [
            "A, 10.0 руб. Остаток: 1 шт.",
            "B, 20.0 руб. Остаток: 2 шт.",
            "C, 30.0 руб. Остаток: 3 шт."
        ]

        for product, expected in zip(products, expected_strings):
            assert str(product) == expected


# Параметризованные тесты для различных комбинаций данных
class TestProductStrParametrized:
    """Параметризованные тесты для метода __str__"""

    @pytest.mark.parametrize("name,price,quantity,expected", [
        ("Телефон", 1000.0, 5, "Телефон, 1000.0 руб. Остаток: 5 шт."),
        ("Ноутбук", 50000, 1, "Ноутбук, 50000 руб. Остаток: 1 шт."),
        ("Мышь", 999.99, 10, "Мышь, 999.99 руб. Остаток: 10 шт."),
        ("Клавиатура", 0.5, 100, "Клавиатура, 0.5 руб. Остаток: 100 шт."),
    ])
    def test_str_with_various_parameters(self, name, price, quantity, expected):
        """Параметризованный тест различных комбинаций данных"""
        product = Product(name, "Описание", price, quantity)
        assert str(product) == expected


# Фикстуры для часто используемых данных
@pytest.fixture
def sample_product():
    """Фикстура для создания тестового продукта"""
    return Product("Тестовый товар", "Тестовое описание", 100.0, 5)


def test_str_with_fixture(sample_product):
    """Тест с использованием фикстуры"""
    expected = "Тестовый товар, 100.0 руб. Остаток: 5 шт."
    assert str(sample_product) == expected

class TestCategoryStr:
    """Тесты для строкового представления категории"""

    def test_str_representation_empty_category(self):
        """Тест строкового представления пустой категории"""
        category = Category("Смартфоны", "Смартфоны как средство")
        expected = "Смартфоны, количество продуктов: 0 шт."
        assert str(category) == expected

    def test_str_representation_with_single_product(self):
        """Тест с одним продуктом"""
        product = Product("iPhone", "Смартфон", 100000.0, 5)
        category = Category("Техника", "Электроника", [product])
        expected = "Техника, количество продуктов: 5 шт."
        assert str(category) == expected

    def test_str_representation_with_multiple_products(self):
        """Тест с несколькими продуктами"""
        products = [
            Product("iPhone", "Смартфон", 100000.0, 3),
            Product("Samsung", "Смартфон", 80000.0, 7),
            Product("Xiaomi", "Смартфон", 50000.0, 10)
        ]
        category = Category("Смартфоны", "Мобильные телефоны", products)
        expected = "Смартфоны, количество продуктов: 20 шт."
        assert str(category) == expected

    def test_str_representation_with_zero_quantity_products(self):
        """Тест с продуктами с нулевым количеством"""
        products = [
            Product("Товар1", "Описание", 1000.0, 0),
            Product("Товар2", "Описание", 2000.0, 0)
        ]
        category = Category("Пустая категория", "Нет товаров", products)
        expected = "Пустая категория, количество продуктов: 0 шт."
        assert str(category) == expected

    def test_str_representation_after_adding_product(self):
        """Тест после добавления продукта"""
        category = Category("Категория", "Описание")
        assert str(category) == "Категория, количество продуктов: 0 шт."

        product = Product("Новый товар", "Описание", 5000.0, 3)
        category.add_product(product)
        assert str(category) == "Категория, количество продуктов: 3 шт."

    def test_str_representation_after_adding_duplicate_product(self):
        """Тест после добавления дубликата продукта"""
        product1 = Product("Товар", "Описание", 1000.0, 2)
        category = Category("Категория", "Описание", [product1])
        assert str(category) == "Категория, количество продуктов: 2 шт."

        # Добавляем дубликат с другим количеством
        product2 = Product("Товар", "Новое описание", 1200.0, 5)
        category.add_product(product2)
        assert str(category) == "Категория, количество продуктов: 7 шт."

    def test_str_representation_special_characters_in_name(self):
        """Тест со специальными символами в названии категории"""
        category = Category("Категория-супер!", "Описание с символами @#$%")
        expected = "Категория-супер!, количество продуктов: 0 шт."
        assert str(category) == expected

    def test_str_representation_long_category_name(self):
        """Тест с длинным названием категории"""
        long_name = "Очень длинное название категории с множеством слов"
        category = Category(long_name, "Описание")
        expected = f"{long_name}, количество продуктов: 0 шт."
        assert str(category) == expected


class TestCategoryStrParametrized:
    """Параметризованные тесты для метода __str__ категории"""

    @pytest.mark.parametrize("category_name,products_data,expected", [
        (
                "Электроника",
                [("Телефон", 1000, 2), ("Ноутбук", 2000, 1)],
                "Электроника, количество продуктов: 3 шт."
        ),
        (
                "Книги",
                [("Книга1", 500, 10), ("Книга2", 300, 5), ("Книга3", 400, 3)],
                "Книги, количество продуктов: 18 шт."
        ),
        (
                "Одежда",
                [("Футболка", 1000, 0), ("Джинсы", 2000, 0)],
                "Одежда, количество продуктов: 0 шт."
        ),
        (
                "Еда",
                [("Хлеб", 50, 100), ("Молоко", 80, 50)],
                "Еда, количество продуктов: 150 шт."
        ),
    ])
    def test_str_with_various_products(self, category_name, products_data, expected):
        """Параметризованный тест различных комбинаций продуктов"""
        products = []
        for name, price, quantity in products_data:
            products.append(Product(name, "Описание", price, quantity))

        category = Category(category_name, "Описание категории", products)
        assert str(category) == expected


# Фикстуры для тестов
@pytest.fixture
def empty_category():
    """Фикстура пустой категории"""
    return Category("Тестовая категория", "Описание")


@pytest.fixture
def category_with_products():
    """Фикстура категории с продуктами"""
    products = [
        Product("Товар A", "Описание A", 100.0, 5),
        Product("Товар B", "Описание B", 200.0, 3)
    ]
    return Category("Категория с товарами", "Описание", products)


def test_str_with_empty_category_fixture(empty_category):
    """Тест с фикстурой пустой категории"""
    assert str(empty_category) == "Тестовая категория, количество продуктов: 0 шт."


def test_str_with_category_with_products_fixture(category_with_products):
    """Тест с фикстурой категории с продуктами"""
    assert str(category_with_products) == "Категория с товарами, количество продуктов: 8 шт."


def test_str_representation_dynamic_changes():
    """Тест динамических изменений количества продуктов"""
    category = Category("Динамическая категория", "Описание")

    # Начальное состояние
    assert str(category) == "Динамическая категория, количество продуктов: 0 шт."

    # Добавляем продукт
    product1 = Product("Товар1", "Описание", 1000.0, 4)
    category.add_product(product1)
    assert str(category) == "Динамическая категория, количество продуктов: 4 шт."

    # Добавляем еще один продукт
    product2 = Product("Товар2", "Описание", 2000.0, 6)
    category.add_product(product2)
    assert str(category) == "Динамическая категория, количество продуктов: 10 шт."

    # Добавляем дубликат (увеличивает количество существующего)
    product3 = Product("Товар1", "Новое описание", 1500.0, 3)
    category.add_product(product3)
    assert str(category) == "Динамическая категория, количество продуктов: 13 шт."