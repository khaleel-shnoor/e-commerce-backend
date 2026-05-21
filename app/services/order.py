"""Order, cart, and wishlist business logic."""

import uuid
from calendar import month_abbr
from datetime import UTC, datetime
from decimal import Decimal

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.exceptions import NotFoundError, ValidationError
from app.models.address import Address
from app.models.cart import Cart, CartItem, Wishlist, WishlistItem
from app.models.catalog import Product, ProductImage
from app.models.enums import OrderStatus, ProductStatus, SellerStatus
from app.models.order import Order, OrderItem
from app.models.seller import Seller
from app.models.user import User
from app.schemas.order import (
    AddressCreate,
    AddressListResponse,
    AddressResponse,
    AdminAnalyticsResponse,
    CartAddRequest,
    CartItemResponse,
    CartResponse,
    CheckoutRequest,
    OrderDetailResponse,
    OrderItemResponse,
    OrderListItem,
    OrderListResponse,
    RevenueDataPoint,
    SellerAnalyticsResponse,
    SellerOrderItemResponse,
    SellerOrderListResponse,
    WishlistItemResponse,
    WishlistResponse,
    WishlistToggleResponse,
)


def _order_number() -> str:
    import random, string
    ts = datetime.now(UTC).strftime("%Y%m%d")
    rand = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return f"ORD-{ts}-{rand}"


def _primary_image(product: Product) -> str | None:
    images = product.__dict__.get("images") or []
    if not images:
        return None
    primary = next((img for img in images if img.is_primary), None)
    return (primary or images[0]).url


class OrderService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    # ── helpers ────────────────────────────────────────────────────────────────

    def _wishlist_load_opts(self):
        return selectinload(Wishlist.items).selectinload(WishlistItem.product).selectinload(Product.images)

    def _cart_load_opts(self):
        return selectinload(Cart.items).selectinload(CartItem.product).selectinload(Product.images)

    async def _load_wishlist(self, wishlist_id: uuid.UUID) -> Wishlist:
        stmt = select(Wishlist).where(Wishlist.id == wishlist_id).options(self._wishlist_load_opts())
        result = await self.session.scalars(stmt)
        return result.first()

    async def _load_cart(self, cart_id: uuid.UUID) -> Cart:
        stmt = select(Cart).where(Cart.id == cart_id).options(self._cart_load_opts())
        result = await self.session.scalars(stmt)
        return result.first()

    async def _get_or_create_wishlist(self, user_id: uuid.UUID) -> Wishlist:
        stmt = select(Wishlist).where(Wishlist.user_id == user_id).options(self._wishlist_load_opts())
        result = await self.session.scalars(stmt)
        wl = result.first()
        if wl is None:
            wl = Wishlist(user_id=user_id)
            self.session.add(wl)
            await self.session.flush()
            # Re-query with selectinload — never assign to relationship attributes
            wl = await self._load_wishlist(wl.id)
        return wl

    async def _get_or_create_cart(self, user_id: uuid.UUID) -> Cart:
        stmt = (
            select(Cart)
            .where(Cart.user_id == user_id, Cart.is_active == True)  # noqa: E712
            .options(self._cart_load_opts())
        )
        result = await self.session.scalars(stmt)
        cart = result.first()
        if cart is None:
            cart = Cart(user_id=user_id, is_active=True)
            self.session.add(cart)
            await self.session.flush()
            # Re-query with selectinload — never assign to relationship attributes
            cart = await self._load_cart(cart.id)
        return cart

    async def _get_active_product(self, product_id: uuid.UUID) -> Product:
        stmt = (
            select(Product)
            .join(Seller, Product.seller_id == Seller.id)
            .where(
                Product.id == product_id,
                Product.status == ProductStatus.ACTIVE,
                Seller.status == SellerStatus.APPROVED,
            )
            .options(selectinload(Product.images), selectinload(Product.inventory))
        )
        result = await self.session.scalars(stmt)
        product = result.first()
        if product is None:
            raise NotFoundError("Product not found or unavailable")
        return product

    # ── Wishlist ───────────────────────────────────────────────────────────────

    async def get_wishlist(self, user_id: uuid.UUID) -> WishlistResponse:
        wl = await self._get_or_create_wishlist(user_id)
        items = []
        for wi in wl.items:
            p = wi.product
            items.append(
                WishlistItemResponse(
                    id=wi.id,
                    product_id=p.id,
                    product_name=p.name,
                    product_price=p.price,
                    product_image_url=_primary_image(p),
                    product_slug=p.slug,
                    added_at=wi.created_at,
                )
            )
        return WishlistResponse(items=items, total=len(items))

    async def toggle_wishlist(self, user_id: uuid.UUID, product_id: uuid.UUID) -> WishlistToggleResponse:
        wl = await self._get_or_create_wishlist(user_id)
        existing = next((wi for wi in wl.items if wi.product_id == product_id), None)
        if existing is not None:
            await self.session.delete(existing)
            in_wishlist = False
        else:
            await self._get_active_product(product_id)
            wi = WishlistItem(wishlist_id=wl.id, product_id=product_id)
            self.session.add(wi)
            in_wishlist = True
        await self.session.flush()
        return WishlistToggleResponse(in_wishlist=in_wishlist, product_id=product_id)

    # ── Cart ───────────────────────────────────────────────────────────────────

    def _cart_response(self, cart: Cart) -> CartResponse:
        items = []
        for ci in cart.items:
            p = ci.product
            items.append(
                CartItemResponse(
                    id=ci.id,
                    product_id=p.id,
                    product_name=p.name,
                    product_price=p.price,
                    product_image_url=_primary_image(p),
                    product_slug=p.slug,
                    quantity=ci.quantity,
                    line_total=p.price * ci.quantity,
                )
            )
        subtotal = sum(i.line_total for i in items)
        item_count = sum(i.quantity for i in items)
        return CartResponse(items=items, subtotal=subtotal, item_count=item_count)

    async def get_cart(self, user_id: uuid.UUID) -> CartResponse:
        cart = await self._get_or_create_cart(user_id)
        return self._cart_response(cart)

    async def add_to_cart(self, user_id: uuid.UUID, req: CartAddRequest) -> CartResponse:
        product = await self._get_active_product(req.product_id)
        inv = product.__dict__.get("inventory")
        if inv is not None and inv.quantity_available < req.quantity:
            raise ValidationError(f"Only {inv.quantity_available} units available")

        cart = await self._get_or_create_cart(user_id)
        existing = next((ci for ci in cart.items if ci.product_id == req.product_id), None)
        if existing is not None:
            existing.quantity = min(existing.quantity + req.quantity, 100)
        else:
            ci = CartItem(cart_id=cart.id, product_id=req.product_id, quantity=req.quantity)
            self.session.add(ci)
        await self.session.flush()
        # Re-query to get fresh state with all relationships loaded
        cart = await self._load_cart(cart.id)
        return self._cart_response(cart)

    async def update_cart_item(self, user_id: uuid.UUID, item_id: uuid.UUID, quantity: int) -> CartResponse:
        cart = await self._get_or_create_cart(user_id)
        item = next((ci for ci in cart.items if ci.id == item_id), None)
        if item is None:
            raise NotFoundError("Cart item not found")
        item.quantity = quantity
        await self.session.flush()
        return self._cart_response(cart)

    async def remove_from_cart(self, user_id: uuid.UUID, item_id: uuid.UUID) -> CartResponse:
        cart = await self._get_or_create_cart(user_id)
        item = next((ci for ci in cart.items if ci.id == item_id), None)
        if item is None:
            raise NotFoundError("Cart item not found")
        await self.session.delete(item)
        await self.session.flush()
        cart = await self._load_cart(cart.id)
        return self._cart_response(cart)

    async def clear_cart(self, user_id: uuid.UUID) -> CartResponse:
        cart = await self._get_or_create_cart(user_id)
        for ci in list(cart.items):
            await self.session.delete(ci)
        await self.session.flush()
        cart = await self._load_cart(cart.id)
        return self._cart_response(cart)

    # ── Addresses ──────────────────────────────────────────────────────────────

    async def list_addresses(self, user_id: uuid.UUID) -> AddressListResponse:
        stmt = select(Address).where(Address.user_id == user_id).order_by(
            Address.is_default.desc(), Address.created_at.desc()
        )
        result = await self.session.scalars(stmt)
        addresses = list(result.all())
        return AddressListResponse(
            items=[self._addr_resp(a) for a in addresses]
        )

    def _addr_resp(self, a: Address) -> AddressResponse:
        return AddressResponse(
            id=a.id,
            label=a.label,
            line1=a.line1,
            line2=a.line2,
            city=a.city,
            state=a.state,
            postal_code=a.postal_code,
            country=a.country,
            is_default=a.is_default,
            created_at=a.created_at,
        )

    async def create_address(self, user_id: uuid.UUID, data: AddressCreate) -> AddressResponse:
        if data.is_default:
            await self._unset_default_addresses(user_id)
        addr = Address(
            user_id=user_id,
            label=data.label,
            line1=data.line1,
            line2=data.line2,
            city=data.city,
            state=data.state,
            postal_code=data.postal_code,
            country=data.country,
            is_default=data.is_default,
        )
        self.session.add(addr)
        await self.session.flush()
        await self.session.refresh(addr)
        return self._addr_resp(addr)

    async def _unset_default_addresses(self, user_id: uuid.UUID) -> None:
        stmt = select(Address).where(Address.user_id == user_id, Address.is_default == True)  # noqa: E712
        result = await self.session.scalars(stmt)
        for addr in result.all():
            addr.is_default = False

    async def delete_address(self, user_id: uuid.UUID, address_id: uuid.UUID) -> None:
        stmt = select(Address).where(Address.id == address_id, Address.user_id == user_id)
        result = await self.session.scalars(stmt)
        addr = result.first()
        if addr is None:
            raise NotFoundError("Address not found")
        await self.session.delete(addr)

    # ── Orders ─────────────────────────────────────────────────────────────────

    def _order_list_item(self, order: Order) -> OrderListItem:
        return OrderListItem(
            id=order.id,
            order_number=order.order_number,
            status=order.status,
            total_amount=order.total_amount,
            item_count=len(order.items),
            created_at=order.created_at,
        )

    def _order_detail(self, order: Order) -> OrderDetailResponse:
        addr = order.__dict__.get("shipping_address")
        addr_resp = self._addr_resp(addr) if addr else None
        return OrderDetailResponse(
            id=order.id,
            order_number=order.order_number,
            status=order.status,
            subtotal=order.subtotal,
            tax_amount=order.tax_amount,
            shipping_amount=order.shipping_amount,
            discount_amount=order.discount_amount,
            total_amount=order.total_amount,
            notes=order.notes,
            items=[
                OrderItemResponse(
                    id=oi.id,
                    product_id=oi.product_id,
                    product_name=oi.product_name,
                    quantity=oi.quantity,
                    unit_price=oi.unit_price,
                    line_total=oi.line_total,
                )
                for oi in order.items
            ],
            shipping_address=addr_resp,
            payment_method="Cash on Delivery",
            created_at=order.created_at,
            updated_at=order.updated_at,
        )

    async def list_orders(self, user_id: uuid.UUID) -> OrderListResponse:
        stmt = (
            select(Order)
            .where(Order.user_id == user_id)
            .options(selectinload(Order.items))
            .order_by(Order.created_at.desc())
        )
        result = await self.session.scalars(stmt)
        orders = list(result.unique().all())
        return OrderListResponse(
            items=[self._order_list_item(o) for o in orders],
            total=len(orders),
        )

    async def get_order(self, user_id: uuid.UUID, order_id: uuid.UUID) -> OrderDetailResponse:
        stmt = (
            select(Order)
            .where(Order.id == order_id, Order.user_id == user_id)
            .options(
                selectinload(Order.items),
                selectinload(Order.shipping_address),
            )
        )
        result = await self.session.scalars(stmt)
        order = result.first()
        if order is None:
            raise NotFoundError("Order not found")
        return self._order_detail(order)

    async def checkout(self, user_id: uuid.UUID, req: CheckoutRequest) -> OrderDetailResponse:
        # Load active cart
        cart = await self._get_or_create_cart(user_id)
        if not cart.items:
            raise ValidationError("Cart is empty")

        # Resolve shipping address
        address: Address | None = None
        if req.new_address is not None:
            if req.new_address.is_default:
                await self._unset_default_addresses(user_id)
            address = Address(
                user_id=user_id,
                label=req.new_address.label,
                line1=req.new_address.line1,
                line2=req.new_address.line2,
                city=req.new_address.city,
                state=req.new_address.state,
                postal_code=req.new_address.postal_code,
                country=req.new_address.country,
                is_default=req.new_address.is_default,
            )
            self.session.add(address)
            await self.session.flush()
            await self.session.refresh(address)
        elif req.shipping_address_id is not None:
            stmt = select(Address).where(
                Address.id == req.shipping_address_id,
                Address.user_id == user_id,
            )
            result = await self.session.scalars(stmt)
            address = result.first()
            if address is None:
                raise NotFoundError("Shipping address not found")

        # Calculate totals
        subtotal = Decimal("0")
        order_items_data = []
        for ci in cart.items:
            p = ci.product
            line_total = p.price * ci.quantity
            subtotal += line_total
            order_items_data.append((p, ci.quantity, p.price, line_total))

        tax = (subtotal * Decimal("0.08")).quantize(Decimal("0.01"))
        shipping = Decimal("0") if subtotal > Decimal("100") else Decimal("12")
        total = subtotal + tax + shipping

        # Create order
        order = Order(
            user_id=user_id,
            shipping_address_id=address.id if address else None,
            order_number=_order_number(),
            status=OrderStatus.PENDING,
            subtotal=subtotal,
            tax_amount=tax,
            shipping_amount=shipping,
            discount_amount=Decimal("0"),
            total_amount=total,
            notes=req.notes,
        )
        self.session.add(order)
        await self.session.flush()

        # Create order items
        for product, quantity, unit_price, line_total in order_items_data:
            oi = OrderItem(
                order_id=order.id,
                product_id=product.id,
                product_name=product.name,
                quantity=quantity,
                unit_price=unit_price,
                line_total=line_total,
            )
            self.session.add(oi)

        # Deactivate the cart
        cart.is_active = False
        await self.session.flush()

        # Reload order with relationships
        stmt = (
            select(Order)
            .where(Order.id == order.id)
            .options(
                selectinload(Order.items),
                selectinload(Order.shipping_address),
            )
        )
        result = await self.session.scalars(stmt)
        order = result.first()
        return self._order_detail(order)

    # ── Seller orders ──────────────────────────────────────────────────────────

    async def list_seller_orders(
        self,
        seller_id: uuid.UUID,
        *,
        limit: int = 50,
        offset: int = 0,
    ) -> SellerOrderListResponse:
        stmt = (
            select(OrderItem)
            .join(Order, OrderItem.order_id == Order.id)
            .join(Product, OrderItem.product_id == Product.id)
            .join(User, Order.user_id == User.id)
            .where(Product.seller_id == seller_id)
            .options(
                selectinload(OrderItem.order).selectinload(Order.user),
            )
            .order_by(Order.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.scalars(stmt)
        items = list(result.unique().all())

        count_stmt = (
            select(func.count())
            .select_from(OrderItem)
            .join(Product, OrderItem.product_id == Product.id)
            .where(Product.seller_id == seller_id)
        )
        total = int((await self.session.scalar(count_stmt)) or 0)

        return SellerOrderListResponse(
            items=[
                SellerOrderItemResponse(
                    order_id=oi.order.id,
                    order_number=oi.order.order_number,
                    order_status=oi.order.status,
                    product_id=oi.product_id,
                    product_name=oi.product_name,
                    quantity=oi.quantity,
                    unit_price=oi.unit_price,
                    line_total=oi.line_total,
                    buyer_name=oi.order.user.full_name,
                    buyer_email=oi.order.user.email,
                    ordered_at=oi.order.created_at,
                )
                for oi in items
            ],
            total=total,
        )

    async def get_seller_analytics(self, seller_id: uuid.UUID) -> SellerAnalyticsResponse:
        # Total revenue and orders for this seller
        rev_stmt = (
            select(func.sum(OrderItem.line_total), func.count(func.distinct(Order.id)))
            .join(Product, OrderItem.product_id == Product.id)
            .join(Order, OrderItem.order_id == Order.id)
            .where(
                Product.seller_id == seller_id,
                Order.status != OrderStatus.CANCELLED,
            )
        )
        rev_result = await self.session.execute(rev_stmt)
        rev_row = rev_result.first()
        total_revenue = Decimal(str(rev_row[0] or 0))
        total_orders = int(rev_row[1] or 0)

        # Product count
        from app.models.catalog import Product as ProductModel
        prod_count_stmt = select(func.count()).select_from(ProductModel).where(ProductModel.seller_id == seller_id)
        prod_count = int((await self.session.scalar(prod_count_stmt)) or 0)

        # Revenue by month (last 6 months)
        from sqlalchemy import extract
        month_stmt = (
            select(
                extract("year", Order.created_at).label("yr"),
                extract("month", Order.created_at).label("mo"),
                func.sum(OrderItem.line_total).label("rev"),
                func.count(func.distinct(Order.id)).label("cnt"),
            )
            .join(Product, OrderItem.product_id == Product.id)
            .join(Order, OrderItem.order_id == Order.id)
            .where(
                Product.seller_id == seller_id,
                Order.status != OrderStatus.CANCELLED,
            )
            .group_by("yr", "mo")
            .order_by("yr", "mo")
            .limit(6)
        )
        month_result = await self.session.execute(month_stmt)
        revenue_by_month = [
            RevenueDataPoint(
                month=month_abbr[int(row.mo)],
                revenue=Decimal(str(row.rev or 0)),
                orders=int(row.cnt or 0),
            )
            for row in month_result.all()
        ]

        # Top products
        top_stmt = (
            select(
                Product.id,
                Product.name,
                func.sum(OrderItem.quantity).label("sales"),
                func.sum(OrderItem.line_total).label("revenue"),
            )
            .join(OrderItem, OrderItem.product_id == Product.id)
            .join(Order, OrderItem.order_id == Order.id)
            .where(
                Product.seller_id == seller_id,
                Order.status != OrderStatus.CANCELLED,
            )
            .group_by(Product.id, Product.name)
            .order_by(func.sum(OrderItem.line_total).desc())
            .limit(5)
        )
        top_result = await self.session.execute(top_stmt)
        top_products = [
            {
                "id": str(row.id),
                "name": row.name,
                "sales": int(row.sales or 0),
                "revenue": float(row.revenue or 0),
            }
            for row in top_result.all()
        ]

        # Recent orders
        recent = await self.list_seller_orders(seller_id, limit=5)

        return SellerAnalyticsResponse(
            revenue=total_revenue,
            orders=total_orders,
            products=prod_count,
            revenue_by_month=revenue_by_month,
            top_products=top_products,
            recent_orders=recent.items,
        )

    # ── Admin analytics ────────────────────────────────────────────────────────

    async def get_admin_analytics(self) -> AdminAnalyticsResponse:
        from app.models.user import User as UserModel

        # Total revenue
        rev_stmt = select(func.sum(Order.total_amount)).where(Order.status != OrderStatus.CANCELLED)
        total_revenue = Decimal(str((await self.session.scalar(rev_stmt)) or 0))

        # Total orders
        ord_stmt = select(func.count()).select_from(Order)
        total_orders = int((await self.session.scalar(ord_stmt)) or 0)

        # Total users
        user_stmt = select(func.count()).select_from(UserModel)
        total_users = int((await self.session.scalar(user_stmt)) or 0)

        # Total sellers
        seller_stmt = select(func.count()).select_from(Seller)
        total_sellers = int((await self.session.scalar(seller_stmt)) or 0)

        # Revenue by month
        from sqlalchemy import extract
        month_stmt = (
            select(
                extract("year", Order.created_at).label("yr"),
                extract("month", Order.created_at).label("mo"),
                func.sum(Order.total_amount).label("rev"),
                func.count().label("cnt"),
            )
            .where(Order.status != OrderStatus.CANCELLED)
            .group_by("yr", "mo")
            .order_by("yr", "mo")
            .limit(6)
        )
        month_result = await self.session.execute(month_stmt)
        revenue_by_month = [
            RevenueDataPoint(
                month=month_abbr[int(row.mo)],
                revenue=Decimal(str(row.rev or 0)),
                orders=int(row.cnt or 0),
            )
            for row in month_result.all()
        ]

        # Recent orders (last 10)
        recent_stmt = (
            select(Order)
            .options(selectinload(Order.user))
            .order_by(Order.created_at.desc())
            .limit(10)
        )
        recent_result = await self.session.scalars(recent_stmt)
        recent_orders = [
            {
                "id": str(o.id),
                "order_number": o.order_number,
                "status": o.status.value,
                "total_amount": float(o.total_amount),
                "buyer_name": o.user.full_name if o.user else None,
                "buyer_email": o.user.email if o.user else "",
                "created_at": o.created_at.isoformat(),
            }
            for o in recent_result.unique().all()
        ]

        return AdminAnalyticsResponse(
            total_revenue=total_revenue,
            total_orders=total_orders,
            total_users=total_users,
            total_sellers=total_sellers,
            revenue_by_month=revenue_by_month,
            recent_orders=recent_orders,
        )
