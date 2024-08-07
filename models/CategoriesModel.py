 class Category:
    def __init__(self, category_id, category_name):
        self.category_id = category_id
        self.category_name = category_name

class CategoryManager:
    def __init__(self):
        self.categories = []

    def add_category(self, category_id, category_name):
        for category in self.categories:
            if category.category_id == category_id or category.category_name == category_name:
                print(f"Category with ID {category_id} or name '{category_name}' already exists.")
                return
        category = Category(category_id, category_name)
        self.categories.append(category)
        print(f"New category '{category_name}' added.")

    def remove_category(self, category_id):
        for category in self.categories:
            if category.category_id == category_id:
                self.categories.remove(category)
                print(f"Category_id {category_id} successfully deleted.")
                return
        print(f"No category_id found {category_id}.")

    def search_and_filtering(self, category_name=None):
        results = []
        for category in self.categories:
            if category_name and category_name.lower() in category.category_name.lower():
                results.append(category)
        return results

    def update_category(self, category_id, category_name=None):
        for category in self.categories:
            if category.category_id == category_id:
                if category_name:
                    for cat in self.categories:
                        if cat.category_name == category_name:
                            print(f"Category name '{category_name}' already exists.")
                            return
                    category.category_name = category_name
                    print(f"Category_id {category_id} updated successfully.")
                return
        print(f"No category_id found {category_id}.")