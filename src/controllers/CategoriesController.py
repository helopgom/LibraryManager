from models.CategoriesModel import CategoriesModel

class CategoriesController:
    def __init__(self):
        self.categories_model = CategoriesModel()

    def check_category(self, data):
        try:
            # Check category using model method
            verification_message = self.categories_model.check_category(
                category_id=data.get('category_id'),
                category_name=data.get('category_name')
            )
            if verification_message:
                return dict(status_code=400, response='That category already exists.')
            return dict(status_code=200, response='Category does not exist, can be created.')
        except Exception as e:
            return dict(status_code=500, response='Server error: ' + str(e))

    def create_category(self, data):
        try:
            # Check if category already exists with same ID or name
            verification_response = self.check_category(data)
            if verification_response['status_code'] != 200:
                return verification_response

            # Create new category if checking was successful
            result = self.categories_model.create_category(
                category_id=data.get('category_id'),
                category_name=data.get('category_name')
            )
            if result:
                return dict(status_code=201, response='Category created successfully.')
            else:
                return dict(status_code=400, response='Cannot create category.')
        except Exception as e:
            return dict(status_code=500, response='Server error: ' + str(e))

    def update_category(self, category_id, data):
        try:
            result = self.categories_model.update(
                table='categories',
                data=data,
                criteria={'category_id': category_id}
            )
            if result:
                return dict(status_code=200, response='Category updated successfully.')
            else:
                return dict(status_code=400, response='Could not update category.')
        except Exception as e:
            return dict(status_code=500, response='Server error: ' + str(e))

    def delete_category(self, category_id):
        try:
            result = self.categories_model.delete(
                table='categories',
                criteria={'category_id': category_id}
            )
            if result:
                return dict(status_code=200, response='Category deleted successfully.')
            else:
                return dict(status_code=400, response='Could not delete category.')
        except Exception as e:
            return dict(status_code=500, response='Server error: ' + str(e))

    def search_categories(self, criteria):
        try:
            result = self.categories_model.search_and_filter(
                category_id=criteria.get('category_id'),
                category_name=criteria.get('category_name')
            )
            if result:
                return dict(status_code=200, response=result)
            else:
                return dict(status_code=404, response='Could not find category with that criteria.')
        except Exception as e:
            return dict(status_code=500, response='Server error: ' + str(e))