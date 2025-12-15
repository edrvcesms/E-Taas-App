import random
import string
from datetime import datetime

def generate_order_code(prefix="ORD", length=6):
    # Get current date in YYYYMMDD format
    date_str = datetime.now().strftime("%Y%m%d")
    
    # Generate random alphanumeric string
    random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
    
    # Combine prefix, date, and random string
    return f"{prefix}-{date_str}-{random_str}"