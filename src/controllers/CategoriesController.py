from models.CategoriesModel import CategoriesModel

class CategoriesController:
    def __init__(self):
        self.categories_model = CategoriesModel()

    def check_category(self, data):
        try:
            # Verifica la categoría usando el método del modelo
            verification_message = self.categories_model.check_category(
                category_id=data.get('category_id'),
                category_name=data.get('category_name')
            )
            if verification_message:
                return dict(status_code=400, response='La categoría ya existe.')
            return dict(status_code=200, response='La categoría no existe, puede ser creada.')
        except Exception as e:
            return dict(status_code=500, response='Error interno del servidor: ' + str(e))

    def create_category(self, data):
        try:
            # Verificar si ya existe una categoría con el mismo ID o nombre
            verification_response = self.check_category(data)
            if verification_response['status_code'] != 200:
                return verification_response

            # Crear la nueva categoría si la verificación fue exitosa
            result = self.categories_model.create_category(
                category_id=data.get('category_id'),
                category_name=data.get('category_name')
            )
            if result:
                return dict(status_code=201, response='Categoría creada con éxito.')
            else:
                return dict(status_code=400, response='No se pudo crear la categoría.')
        except Exception as e:
            return dict(status_code=500, response='Error interno del servidor: ' + str(e))

    def update_category(self, category_id, data):
        try:
            result = self.categories_model.update(
                table='categories',
                data=data,
                criteria={'category_id': category_id}
            )
            if result:
                return dict(status_code=200, response='Categoría actualizada con éxito.')
            else:
                return dict(status_code=400, response='No se pudo actualizar la categoría.')
        except Exception as e:
            return dict(status_code=500, response='Error interno del servidor: ' + str(e))

    def delete_category(self, category_id):
        try:
            result = self.categories_model.delete(
                table='categories',
                criteria={'category_id': category_id}
            )
            if result:
                return dict(status_code=200, response='Categoría eliminada con éxito.')
            else:
                return dict(status_code=400, response='No se pudo eliminar la categoría.')
        except Exception as e:
            return dict(status_code=500, response='Error interno del servidor: ' + str(e))

    def search_categories(self, criteria):
        try:
            result = self.categories_model.search_and_filter(
                category_id=criteria.get('category_id'),
                category_name=criteria.get('category_name')
            )
            if result:
                return dict(status_code=200, response=result)
            else:
                return dict(status_code=404, response='No se encontraron categorías con esos criterios.')
        except Exception as e:
            return dict(status_code=500, response='Error interno del servidor: ' + str(e))