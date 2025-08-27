import unittest


class TestCategoryAndProduct(unittest.TestCase):

    def setUp(self):
        """Сброс счетчиков перед каждым тестом"""
        Product.product_count = 0
        Category.category_count = 0
        Category.product_count = 0

    def test_product_initialization(self):
        """Тест корректности инициализации объекта Product"""
        product = Product("Test Product", "Test Description", 100.0, 10)

        self.assertEqual(product.name, "Test Product")
        self.assertEqual(product.description, "Test Description")
        self.assertEqual(product.price, 100.0)
        self.assertEqual(product.quantity, 10)

    def test_category_initialization(self):
        """Тест корректности инициализации объекта Category"""
        category = Category("Test Category", "Test Category Description")

        self.assertEqual(category.name, "Test Category")
        self.assertEqual(category.description, "Test Category Description")
        self.assertEqual(category.products, [])

    def test_category_with_products_initialization(self):
        """Тест инициализации Category с продуктами"""
        product1 = Product("Product 1", "Desc 1", 50.0, 5)
        product2 = Product("Product 2", "Desc 2", 75.0, 3)

        category = Category("Test Category", "Test Desc", [product1, product2])

        self.assertEqual(len(category.products), 2)
        self.assertEqual(category.products[0].name, "Product 1")
        self.assertEqual(category.products[1].name, "Product 2")

    def test_product_count_increment(self):
        """Тест подсчета количества созданных продуктов"""
        self.assertEqual(Product.product_count, 0)

        product1 = Product("P1", "D1", 10.0, 1)
        self.assertEqual(Product.product_count, 1)

        product2 = Product("P2", "D2", 20.0, 2)
        self.assertEqual(Product.product_count, 2)

        product3 = Product("P3", "D3", 30.0, 3)
        self.assertEqual(Product.product_count, 3)

    def test_category_count_increment(self):
        """Тест подсчета количества созданных категорий"""
        self.assertEqual(Category.category_count, 0)

        category1 = Category("Cat1", "Desc1")
        self.assertEqual(Category.category_count, 1)

        category2 = Category("Cat2", "Desc2")
        self.assertEqual(Category.category_count, 2)

    def test_category_product_count_increment(self):
        """Тест подсчета количества продуктов в категориях"""
        self.assertEqual(Category.product_count, 0)

        # Создаем продукты
        product1 = Product("P1", "D1", 10.0, 1)
        product2 = Product("P2", "D2", 20.0, 2)
        product3 = Product("P3", "D3", 30.0, 3)

        # Создаем категорию с 2 продуктами
        category1 = Category("Cat1", "Desc1", [product1, product2])
        self.assertEqual(Category.product_count, 2)

        # Создаем категорию с 1 продуктом
        category2 = Category("Cat2", "Desc2", [product3])
        self.assertEqual(Category.product_count, 3)

        # Создаем пустую категорию
        category3 = Category("Cat3", "Desc3")
        self.assertEqual(Category.product_count, 3)  # Не должно измениться

    def test_multiple_categories_with_shared_products(self):
        """Тест с несколькими категориями, содержащими общие продукты"""
        product1 = Product("P1", "D1", 10.0, 1)
        product2 = Product("P2", "D2", 20.0, 2)

        # Один продукт может быть в нескольких категориях
        category1 = Category("Cat1", "Desc1", [product1, product2])
        category2 = Category("Cat2", "Desc2", [product1])  # product1 в двух категориях

        self.assertEqual(Product.product_count, 2)  # 2 уникальных продукта
        self.assertEqual(Category.product_count, 3)  # 2 в первой + 1 во второй = 3
        self.assertEqual(Category.category_count, 2)  # 2 категории

    def test_empty_category_creation(self):
        """Тест создания пустой категории"""
        category = Category("Empty Category", "No products")

        self.assertEqual(category.name, "Empty Category")
        self.assertEqual(len(category.products), 0)
        self.assertEqual(Category.category_count, 1)
        self.assertEqual(Category.product_count, 0)  # Продуктов не добавлено

    def test_product_attributes_types(self):
        """Тест типов данных атрибутов Product"""
        product = Product("Test", "Desc", 99.99, 5)

        self.assertIsInstance(product.name, str)
        self.assertIsInstance(product.description, str)
        self.assertIsInstance(product.price, float)
        self.assertIsInstance(product.quantity, int)

    def test_category_attributes_types(self):
        """Тест типов данных атрибутов Category"""
        product = Product("P", "D", 10.0, 1)
        category = Category("Cat", "Desc", [product])

        self.assertIsInstance(category.name, str)
        self.assertIsInstance(category.description, str)
        self.assertIsInstance(category.products, list)


if __name__ == "__main__":
    unittest.main()