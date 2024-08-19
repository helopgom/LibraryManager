import pytest
from src.controllers.LoansController import LoansController


@pytest.fixture
def setup_loans_controller(mocker):
    controller = LoansController()
    mocker.patch.object(controller.loans_model, "create_loan")
    mocker.patch.object(controller.loans_model, "read_loan")
    mocker.patch.object(controller.loans_model, "update_loan")
    mocker.patch.object(controller.loans_model, "delete_loan")
    return controller


def test_create_loan_success(setup_loans_controller):
    """Given: A new loan passes all validations.
    When: Attempting to register the loan.
    Then: The system should return a 201 status code indicating the loan was successfully registered."""

    # Given
    setup_loans_controller.loans_model.create_loan.return_value = 1
    loan_data = {"loan_id": 1, "book_id_books": 101, "user_id": 1001, "entry_date": "2024-08-01","return_date": "2024-08-15"}

    # When
    response = setup_loans_controller.create_loan(loan_data)

    # Then
    assert response["status_code"] == 201
    assert response["response"] == "Loan registered successfully."
    assert response["loan_id"] == 1


def test_read_loan_success(setup_loans_controller):
    """Given: An existing loan with ID 1.
    When: Attempting to retrieve the loan information.
    Then: The system should return a 200 status code with the loan details. """

    # Given
    loan_id = 1
    expected_loan = {"loan_id": 1,"book_id_books": 101,"user_id": 1001, "entry_date": "2024-08-01", "return_date": "2024-08-15"}
    setup_loans_controller.loans_model.read_loan.return_value = expected_loan

    # When
    response = setup_loans_controller.read_loan(loan_id)

    # Then
    assert response["status_code"] == 200
    assert response["response"] == expected_loan


def test_update_loan_success(setup_loans_controller):
    """Given: An existing loan with ID 1.
    When: Attempting to update the loan information.
    Then: The system should return a 200 status code indicating the update was successful. """

    # Given
    loan_id = 1
    update_data = {"book_id_books": 101,"user_id": 1001,"entry_date": "2024-08-02", "return_date": "2024-08-16"}
    setup_loans_controller.loans_model.update_loan.return_value = 1

    # When
    response = setup_loans_controller.update_loan(loan_id, update_data)

    # Then
    assert response["status_code"] == 200
    assert response["response"] == "Loan updated successfully."


def test_delete_loan_success(setup_loans_controller):
    """ Given: An existing loan with ID 1.
    When: Attempting to delete the loan.
    Then: The system should return a 200 status code indicating the loan was successfully deleted. """

    # Given
    loan_id = 1
    setup_loans_controller.loans_model.delete_loan.return_value = 1

    # When
    response = setup_loans_controller.delete_loan(loan_id)

    # Then
    assert response["status_code"] == 200
    assert response["response"] == "Loan deleted successfully."