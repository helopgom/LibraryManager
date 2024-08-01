from config.DbConnection import Connection
from models.UsersModel import UsersModel


def main():
    try:
        # Inicializar la conexión a la base de datos
        conn_instance = Connection()
        print("Conexión a la base de datos inicializada.")

        user_model = UsersModel()

        # Datos para un nuevo usuario
        new_user_data = {
            "dni": "13456879X",
            "user_name": "María",
            "user_lastname": "Estevez",
            "mail": "maria.estevez@example.com",
            "phone": "987654321"
        }



        # Eliminar un usuario
        print("\nIntentando eliminar un usuario...")
        result = user_model.delete_user(13)
        if result:
            print("Usuario eliminado con éxito.")
        else:
            print("No se pudo eliminar el usuario.")





    except Exception as e:
        print(f"Error en el proceso principal: {e}")
    finally:
        # Cerrar la conexión al finalizar
        conn_instance.close_connection()

if __name__ == "__main__":
    main()

