from fastapi import FastAPI
from fastapi.requests import Request
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from app.db.database import engine, Base
from app.routers import auth, users, admin, notification, sellers, products, service, cart, orders, chat, conversation
from slowapi.errors import RateLimitExceeded
from app.dependencies.limiter import rate_limit_exceeded_handler, limiter
from app.utils.logger import logger



@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        logger.info("Application startup complete.")
    yield
    logger.info("Shutting down application.")

app = FastAPI(lifespan=lifespan)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins="http://127.0.0.1:8001",
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
app.include_router(conversation.router, prefix="/v1/api/conversations", tags=["conversations"])

