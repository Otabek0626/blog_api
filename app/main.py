# Import necessary modules from FastAPI and project-specific modules.
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.core import oauth2, routers, config, database, utils, models
from fastapi.openapi.utils import get_openapi
from sqlalchemy.orm import Session
from fastapi.staticfiles import StaticFiles
# Set the allowed origins for CORS requests.
origins = [
    config.settings.CLIENT_ORIGIN
]

# Create a new FastAPI instance and set its properties.
app = FastAPI(
    title=config.title,  # Set the title of the app to the value of the `title` variable.
    description=config.description,  # Set the description of the app to the value of the `description` variable.
    version=config.settings.APP_VERSION,  # Set the version of the app to the value of the `APP_VERSION` variable in the `settings` module.
    terms_of_service=config.terms_of_service,  # Set the terms of service URL for the app.
    docs_url=None,  # Disable the default "/docs" endpoint.
    redoc_url=None,  # Disable the default "/redoc" endpoint.
    openapi_url = None,  # Disable the default "/openapi.json" endpoint.
)

app.mount("/api/static", StaticFiles(directory="static"), name="static")

# Add a CORS middleware to the app.
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables from the metadata defined in the `models` module.
# models.Base.metadata.create_all(bind=database.engine)

@app.on_event("startup")
async def startup_event():
    db = database.SessionLocal()
    user = db.query(models.User).filter(models.User.username == config.settings.admin_username).first()
    try:
        if not user:
            user = models.User(username = config.settings.admin_username, password = await utils.hash_password(config.settings.admin_password), is_admin = True)
        else:
            user.username = config.settings.admin_username
            user.password = await utils.hash_password(config.settings.admin_password)
            user.is_admin = True
        db.add(user)
        db.commit()
        db.refresh(user)
    except:
        db.close()
    


# Include the router defined in the `routers` module in the app.
app.include_router(routers.router, prefix="/api")

# Define an endpoint for retrieving the OpenAPI specification document.
@app.get("/api/openapi.json", include_in_schema=False)
async def openapi(username: str = Depends(oauth2.require_user)):
    return get_openapi(
        title=app.title +  " - Swagger UI",
        description=app.description,
        version=app.version,
        terms_of_service=app.terms_of_service,
        routes=app.routes,
        tags=config.tags_metadata,
        contact={
            "name": "Otabek Olimjonov",
            "url": "https://www.linkedin.com/in/otabek-olimjonov-2b3827196/",
            "email": "bekdevs01@gmail.com",
        },
        license_info={
            "name": "licensed by Otabek",
            "identifier": "Otabek",
        },
    )
