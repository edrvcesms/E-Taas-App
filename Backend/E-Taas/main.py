from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from db.database import engine, Base
from routers import auth, users, admin, notification, sellers, products, service, cart, orders
from slowapi.errors import RateLimitExceeded
from dependencies.limiter import rate_limit_exceeded_handler, limiter

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


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