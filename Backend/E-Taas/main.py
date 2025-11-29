from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from fastapi.exceptions import RequestValidationError
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from db.database import engine, Base
from routers import auth, users, admin, notification, sellers, products, service, cart, orders, chat
from slowapi.errors import RateLimitExceeded
from dependencies.limiter import rate_limit_exceeded_handler, limiter
from utils.logger import logger



@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        logger.info("Application startup complete.")
    yield
    logger.info("Shutting down application.")

app = FastAPI(lifespan=lifespan)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)

origin = [
    "http://127.0.0.1:5173",
    "http://localhost:8000",
    "http://127.0.0.1:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origin,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/v1/api/auth", tags=["auth"])
app.include_router(users.router, prefix="/v1/api/users", tags=["users"])
app.include_router(admin.router, prefix="/v1/api/admin", tags=["admin"])
app.include_router(notification.router, prefix="/v1/api/notifications", tags=["notifications"])
app.include_router(sellers.router, prefix="/v1/api/sellers", tags=["sellers"])
app.include_router(products.router, prefix="/v1/api/products", tags=["products"])
app.include_router(service.router, prefix="/v1/api/services", tags=["services"])
app.include_router(cart.router, prefix="/v1/api/cart", tags=["cart"])
app.include_router(orders.router, prefix="/v1/api/orders", tags=["orders"])
app.include_router(chat.router, prefix="/v1/api/chat", tags=["chat"])


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.error(f"Validation error for request {request.url}")
    logger.error(f"Error details: {exc.errors()}")
    logger.error(f"Request body: {exc.body}")
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors(), "body": exc.body}
    )