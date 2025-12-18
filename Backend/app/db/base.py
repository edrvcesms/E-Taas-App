from app.db.database import Base
# Import all your models so Alembic can detect them
from app.models.cart import Cart, CartItem
from app.models.inquiries import ServiceInquiry
from app.models.category import ProductCategory, ServiceCategory
from app.models.services import Service, ServiceImage
from app.models.orders import Order, OrderItem
from app.models.notification import Notification
from app.models.conversation import Conversation, Message, MessageImage
from app.models.users import User
from app.models.sellers import Seller
from app.models.products import Product, ProductImage, ProductVariant, VariantCategory, VariantAttribute, variant_attribute_values
