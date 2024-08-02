import pytest
from src.controllers.CategoriesController import CategoriesController


@pytest.fixture
def setup_categories_controller(mocker):
    controller = CategoriesController()
    mocker.patch.object(controller.categories_model, 'check_category')
    mocker.patch.object(controller.categories_model, 'create_category')
    mocker.patch.object(controller.categories_model, 'update')
    mocker.patch.object(controller.categories_model, 'delete')
    mocker.patch.object(controller.categories_model, 'search_and_filter')
    return controller