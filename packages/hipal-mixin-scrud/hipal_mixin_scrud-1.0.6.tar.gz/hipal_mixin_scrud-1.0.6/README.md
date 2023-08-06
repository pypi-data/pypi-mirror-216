
# Hipal Mixin Scrud

Libreria para generar rutas generales para una crud basica con el orm de SQLAlchemy

Instalacion
---------
```pip install hipal-mixin-scrud```

Como usar
---------
Para usar la libreria se debe importar la instancia "MixinCrud" para luego en su constructor enviarle los argumentos necesarios.
ejemplo:

```
from schemas import UserSchema, CreateUserSchema, UpdateUserSchema
from db.db_session import db_session
from models.user import User

from hipal_mixin_scrud.mixin import MixinCrud

users_router = MixinCrud(
    schema=UserSchema,
    db_session=db_session,
    model=User,
    prefix="/users",
    create_schema=CreateUserSchema,
    update_schema=UpdateUserSchema
)
```
donde:
- **schema**: Sera el schema principal para listar o paginar los datos
- **db_session**: La session de la base de datos otorgada por el motor implementado mediante sqlalchemy
- **model**: El modelo con el que se hara la crud basica
- **prefix**: La raiz de los endpoints
- **create_schema**: El schema con el que se mapearan los datos para crear los registros en el modelo
- **update_schema**: El schema con el que se mapearan los datos para la actualizacion de un registro existente del modelo

Uso Avanzado
---------
Si se requiere tener mas control de las rutas generadas, se tiene lo siguiente:

Para especificar que rutas se requieren y cuales no, se hace uso de 5 parametros:
- has_update
- has_get_list
- has_delete_one
- has_create
- has_get_one

Por defecto todas estan en "True", y reciben booleanos para indicar si se genera la ruta o no:
```
from schemas import UserSchema, CreateUserSchema, UpdateUserSchema
from db.db_session import db_session
from models.user import User

from hipal_mixin_scrud.mixin import MixinCrud

users_router = MixinCrud(
    schema=UserSchema,
    db_session=db_session,
    model=User,
    prefix="/users",
    create_schema=CreateUserSchema,
    update_schema=UpdateUserSchema,
    has_update=False,
    has_get_list=True,
    has_delete_one=False,
    has_create=False,
    has_get_one=True,
)
```

Para especificar una "query prefija" es decir, una query por defecto que se concatenara con la query final en toda la CRUD principal, hacemos uso del parametro: **query**, Ejemplo:

```
from fastapi import Request
from schemas import UserSchema, CreateUserSchema, UpdateUserSchema
from db.db_session import db_session
from models.user import User

from hipal_mixin_scrud.mixin import MixinCrud


def default_query(
    request: Request,
):
    account_id = request.headers.get("account_id")
    profile_id = request.headers.get("profile_id")

    query = db_session.query(User).filter(User.id > 0)

    return query

users_router = MixinCrud(
    schema=UserSchema,
    db_session=db_session,
    model=User,
    prefix="/users",
    create_schema=CreateUserSchema,
    update_schema=UpdateUserSchema,
    query=default_query
)
```

El parametro query es opcional, y en caso de que se requiera recibira una funcion que como obligacion debera recibir por argument "request" y tendra que devolver la query que se requiera.

Paginación
---------

Para generar una paginacion es exactamente igual a lo dicho anteriormente, Sin embargo, recibe algunos parametros opcionales los cuales sirven para:

- **offset**: Recibe el numero de la posicion del registro donde se requiere empezar a ver 
- **limit**: Limite de registros a visualizar
- **search**: Lista de campos con su valor a buscar separados por ; ejemplo: name=alan;company=Gooogle
- **sort**: ASC o DESC para especificar si se requiere el orden descendente o ascendente
- **sort_field**: Nombre del campo por el cual se requiere ordenar

Adicionalmente se podra user "users_router" para generar las rutas como generalmente las conocemos:

```
@users_router.get("/me", response_model=UserSchema)
def endpoint() -> UserSchema:
    return {"msg":"prueba"}
```