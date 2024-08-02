import pytest
from src.controllers.CategoriesController import CategoriesController

@pytest.fixture
def setup_categories_controller(mocker):
    controller = CategoriesController()
    mocker.patch.object(controller.categories_model, 'create_category')
    mocker.patch.object(controller.categories_model, 'search_and_filter')
    mocker.patch.object(controller.categories_model, 'check_category')
    mocker.patch.object(controller.categories_model, 'update_category')
    mocker.patch.object(controller.categories_model, 'delete_category')
    return controller

def test_create_category_success(setup_categories_controller):
    """Crear una categoría con éxito - Añadir given, when y then."""
    # Given
    setup_categories_controller.categories_model.check_category.return_value = False
    setup_categories_controller.categories_model.create_category.return_value = True
    data = {"category_id": 1, "category_name": "Thriller"}

    # When
    response = setup_categories_controller.create_category(data)

    # Then
    assert response['status_code'] == 201
    assert response['response'] == 'Categoría creada con éxito.'

def test_create_category_existing(setup_categories_controller):
    """Intentar crear una categoría ya existente - Añadir given, when y then."""
    # Given
    setup_categories_controller.categories_model.check_category.return_value = True
    data = {"category_id": 1, "category_name": "Science"}

    # When
    response = setup_categories_controller.create_category(data)

    # Then
    assert response['status_code'] == 400
    assert response['response'] == 'La categoría ya existe.'