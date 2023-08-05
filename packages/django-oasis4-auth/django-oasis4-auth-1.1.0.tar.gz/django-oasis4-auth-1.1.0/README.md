[English](#oasis4-authentication-package-for-DJANGO&copy;)
# Módulo de autenticación OASIS4 para DJANGO&copy;
Este módulo permite a DJANGO&copy; interactuar con OASIS4 y realizar acciones como el registro de usuario y su autenticacíón, utilizando un sistema de dos pasos.

El módulo ofrece tres (3) servicios API para el registro de los usuarios, ingreso al sistema y validación del código de autorización.

## Versiones
* 1.1.0: Se elimina la dependencia del paquete zibanu.django.auth para el manejo de las señales. Depende de la versión 1.2.0 de zibanu-django.
* 1.0.7: Incorpora una tarea para la sincronización de los usuarios desde la tabla origen en OASIS4.
* 1.0.5: Corrige un bug que se presentaba con la autenticación anónima derivada de la actualización de librerías.
* 1.0.4: Corrige un bug que creaba el usuario en la tabla de usuarios ignorando el segundo nombre y apellido.

## APIs
* [Registro](#registro)
* [Acceso al sistema](#login-1)
* [Validación del código](#validate-1)

### *Registro*
Esta API permite realizar el proceso de registro de usuarios. El sistema valida el correo electrónico y el número
del documento de identificación del usuario contra los datos que existen en la base de datos de *OASIS4&copy;*.

El API se accede a través de https://<dominio>/<modulo>/register/ y recibe como parte de la solicitud HTTP un set
de datos en formato JSON con los parámetros requeridos para su funcionamiento.

#### Parámetros
* ***customer_id***: Número de identificación del cliente
* ***email***: Correo electrónico, debe ser el registrado en *OASIS4&copy;*.
* ***password***: El password asignado por el usuario en la forma de registro online.

#### Retorna
> El API retorna un objeto Response con el estado HTTP 200 si no existen errores y un objeto JSON.
````python
customer_data = {
    "first_name": "",
    "last_name": "",
    "location": "",
    "address": "",
    "phone": 0,
    "mobile": 0,
    "email": "",
    "customer_id": 0,
    "document_type": 0,
    "is_valid": True,
    "type": 0
}

data_return = {
    "token": "asdasdas",
    "data": customer_data
}
````

##### Objeto customer_data
* *first_name*: Nombre o nombres del usuario registrado en la base *OASIS4&copy;*.
* *last_name*: Apellidos registrados en la base de datos *OASIS4&copy;*.
* *location*: Nombre de la ciudad registrada en la base de datos *OASIS4&copy;*.
* *address*: Dirección registrada en la base de datos *OASIS4&copy;*.
* *phone*: Número telefónico registrado en la base de datos *OASIS4&copy;*.
* *mobile*: Número celular registrado en la base de datos *OASIS4&copy;*.
* *email*: Correo electrónico registrado en la base de datos *OASIS4&copy;*.
* *customer_id*: Documento de identificación registrado en la base de datos *OASIS4&copy;*.
* *document_type*: Tipo de documento registrado en la base de datos *OASIS4&copy;*.
* *is_valid*: Indica si el usuario se encuentra válido en la base de datos *OASIS4&copy;*.
* *type*: Código del tipo de usuario asociado.
  * 0: Sin relación
  * 1: Cliente
  * 2: Asociado

##### JSON data_return
> Diccionario de datos que se retorna a través del objeto Response HTTP.
* *token*: Token utilizado para la validación del segundo paso de autenticación
* *data*: Objeto que contiene los [datos básicos del cliente](#objeto-customerdata)

### *Login*
Este API realiza el proceso de autenticación de los usuarios a través de los parámetros "email" y "password". En caso de
que la autenticación sea exitosa, envía el código para el segundo paso de la autenticación.

El API se expone a través de https://<dominio>/<modulo>/login/ y recibe en formato JSON los siguientes parémtros.

#### Parámetros
* ***email***: Correo electrónico del usuario, previamente registrado, para la autenticación.
* ***password***: Clave del usuario

#### Retorna
> El API retorna un objeto *Response HTTP* con estado 200 si no existen errores y un objeto JSON.

````python
data_return = {
            "token": "asdkjahs"
        }
````

##### *JSON* data_return
> Objeto *JSON* que se envía a través del Response HTTP.

* *token*: Clave token para validar el código de autorización en el segundo paso.

### *Validate*
Este API realiza el proceso de autenticación con el token y el código de autorización enviado al correo electrónico.

El API se accede a travésde https://<domain>/<module>/validate/ y recibe un objeto JSON con los parámetros requeridos.

#### Parámetros
* ***token***: Clave token enviada desde el [login](#login-1) o [register](#registro)
* ***code***: Código de autorización enviado al correo electrónico.

### Retorna
> El API genera un objeto Response basado en la acción originaria y asociada al token. Si es exitoso el procdeso retorna
> un estado HTTP 200.

* Registro: El API solamente retorna el estado
* Acceso (Login): El API retorna el estado y un objeto JSON.

````python
data_return = {
    "token": "asdaskjhiuuh",
    "payload": {},
    "user": {
        "full_name": "",
        "document_id": 0,
        "type": ""
    }
}
````
* *token*: Java Web Token generado a partir de la autenticacion HTTP.
* *payload*: Carga de datos del JWT.
* *user*: Objeto con los datos básicos del usuario.
  * *full_name*: Nombre completo del usuario
  * *document_id*: Número del documento de identificación
  * *type*: Descriptivo del tipo de relación que contiene el cliente con la entidad.
***
[Spanish](#módulo-de-autenticación-oasis4-para-DJANGO&copy;)
# OASIS4 Authentication Package for DJANGO&copy;

This package allow to DJANGO&copy; interact with *OASIS4&copy;* and make actions like register and authenticate users for login, with a two steps authentication system. 

The package offers three API Endpoints for user registration, login user and authenticate code validation.

## Versions

* 1.0.7: Include a task to syn users from OASIS4 entity.
* 1.0.5: Fix a bug with anonymous authentication on login after upgrade libraries.
* 1.0.4: Fix a bug that create the username ignoring second name and first last name. 

## Endpoints
* [Register](#register)
* [Login](#login)
* [Validate](#validate)

### *Register*
This endpoint make a user registration process, validating the email and document id with *OASIS4* database

The endpoint is https://<domain>/<module>/register/ and receive a json body with some **required parameters**.

#### Parameters
* ***customer_id***: identification number registered at *OASIS4&copy;* database for validation purposes.
* ***email***: email previously registered at *OASIS4&copy* database.
* ***password***: password entered by user in the registration form.

#### Return
> The endpoint returns a response with **HTTP Status 200** if ok and json body.

```python
customer_data = {
    "first_name": "",
    "last_name": "",
    "location": "",
    "address": "",
    "phone": 0,
    "mobile": 0,
    "email": "",
    "customer_id": 0,
    "document_type": 0,
    "is_valid": True,
    "type": 0
}

data_return = {
    "token": "asdasdas",
    "data": customer_data
}
```
##### customer_data *object*:
> Set of features that represent a customer or partner.
* *first_name*: First name registered in *OASIS4&copy;* database.
* *last_name*: Last name registered in *OASIS4&copy;* database.
* *location*: City registered in *OASIS4&copy;* database.
* *address*: Address registered in *OASIS4&copy;* database.
* *phone*: Phone number registered in *OASIS4&copy;* database.
* *mobile*: Mobile phone number registered in *OASIS4&copy;* database.
* *email*: Email registered in *OASIS4&copy;* database.
* *customer_id*: ID number registered in *OASIS4&copy;* database.
* *document_type*: Document type from *OASIS4&copy;* database.
* *is_valid*: True if user is valid, otherwise False.
* *type*: User type in system:
  * 0 -> Not relationship with company.
  * 1 -> Customer relationship.
  * 2 -> Partner relationship.

##### data_return *JSON*
> Set of values to be returned through HTTP Response.
* *token*: Token to validate code at second pass authenticate.
* *data*: [Customer data object](#customerdata-object-)

### *Login*
This endpoint make a login authentication for users, and send an email with authorization code for second step authentication.

The endpoint is https://<domain>/<module>/login/ and receive a json body with **required parameters**:
#### Parameters
* ***email***: Email registered at system to authenticate.
* ***password***: User password

#### Return
> The endpoint returns a response object with **HTTP Status 200** if ok and json body.

````python
data_return = {
            "token": "asdkjahs"
        }
````

##### data_return *dict*
> Set of values to be returned through HTTP Response.
* *token*: Token to validate second step authorization code.

### *Validate*
This endpoint performs the authentication with the token and the authorization code sent to the email.

The endpoint is https://<domain>/<module>/validate/ and receive a json body with **required parameters**:

#### Parameters
* ***token***: Token received from [login](#login) or [register](#register) endpoints.
* ***code***: Authentication code received via email.

#### Return
> The endpoint return a Response based on the action that originates it with *HTTP Status 200* if ok.

* Register Action: The endpoint return only status code.
* Login Action: The endpoint return status code (200) and json body.

````python
data_return = {
    "token": str(token_data.access_token),
    "payload": token_data.payload,
    "user": {
        "full_name": self.__data.get_full_name(),
        "document_id": self.__data.profile.document_id,
        "type": self.__data.profile.type
    }
}
````
##### data_return *dict*
> Set of values to be return via HTTP Response.
* *token*: Java Web Token to authenticate HTTP Requests.
* *payload*: Java Web Token payload.
* *user*: Basic user information
  * *full_name*: User full name
  * *document_id*: Document id of user
  * *type*: Descriptive user type

