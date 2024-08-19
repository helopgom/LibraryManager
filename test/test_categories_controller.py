import pytest
from src.controllers.CategoriesController import CategoriesController
from models import CategoriesModel

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
    """Given: A new category that does not exist.
    When: Attempting to create the category.
    Then: The system should return a 201 status code indicating the category was successfully created."""

    # Given
    setup_categories_controller.categories_model.check_category.return_value = False
    setup_categories_controller.categories_model.create_category.return_value = True
    data = {"category_id": 1, "category_name": "Thriller"}

    # When
    response = setup_categories_controller.create_category(data)

    # Then
    assert response['status_code'] == 201
    assert response['response'] == 'Category created successfully.'

def test_create_category_existing(setup_categories_controller):
    """Given: An existing category.
    When: Attempting to create the same category again.
    Then: The system should return a 400 status code indicating the category already exists."""
    # Given
    setup_categories_controller.categories_model.check_category.return_value = True
    data = {"category_id": 1, "category_name": "Science"}

    # When
    response = setup_categories_controller.create_category(data)

    # Then
    assert response['status_code'] == 400
    assert response['response'] == 'That category already exists.'

def test_search_and_filter_success(setup_categories_controller):
    """Given: A search query that matches existing categories.
    When: Searching and filtering categories.
    Then: The system should return a 200 status code with the matching categories."""

    # Given
    criteria = {"category_name": "Thriller"}
    expected_categories = [
        {"category_id": 1, "category_name": "Thriller"},
        {"category_id": 2, "category_name": "Mystery"}
    ]
    setup_categories_controller.categories_model.search_and_filter.return_value = expected_categories

    # When
    response = setup_categories_controller.search_categories(criteria)

    # Then
    assert response['status_code'] == 200
    assert response['response'] == expected_categories

def test_update_category_success(setup_categories_controller):
    """Given: An existing category with ID 1.
    When: Attempting to update the category information.
    Then: The system should return a 200 status code indicating the update was successful."""

    # Given
    category_id = 1
    update_data = {"category_name": "Psychological Thriller"}
    setup_categories_controller.categories_model.update_category.return_value = 1

    # When
    response = setup_categories_controller.update_category(category_id, update_data)

    # Then
    assert response['status_code'] == 200
    assert response['response'] == 'Category updated successfully.'


def test_delete_category_success(setup_categories_controller, mocker):
    """Given: An existing category with ID 1 that is not in use.
    When: Attempting to delete the category.
    Then: The system should return a 200 status code indicating the category was successfully deleted."""

    # Given
    category_id = 1

    # Mock _execute_query behavior for category delete
    mocker.patch.object(setup_categories_controller.categories_model, '_execute_query', return_value=1)

    # When
    response = setup_categories_controller.delete_category(category_id)

    # Then
    assert response['status_code'] == 200
    assert response['response'] == 'Category deleted successfully.'