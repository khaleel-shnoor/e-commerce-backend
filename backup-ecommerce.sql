--
-- PostgreSQL database dump
--

\restrict tDOwR4vG68lm2oSNMKhrmCwdtTTnvqFrtOoL1tzd5phB2WC9MlRQTXHdYDoUEKc

-- Dumped from database version 18.3
-- Dumped by pg_dump version 18.3

-- Started on 2026-05-19 10:19:07

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 903 (class 1247 OID 25775)
-- Name: addresstype; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.addresstype AS ENUM (
    'SHIPPING',
    'BILLING',
    'BOTH'
);


ALTER TYPE public.addresstype OWNER TO postgres;

--
-- TOC entry 927 (class 1247 OID 25846)
-- Name: coupondiscounttype; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.coupondiscounttype AS ENUM (
    'PERCENTAGE',
    'FIXED'
);


ALTER TYPE public.coupondiscounttype OWNER TO postgres;

--
-- TOC entry 930 (class 1247 OID 25852)
-- Name: notificationtype; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.notificationtype AS ENUM (
    'ORDER',
    'PROMO',
    'SYSTEM',
    'SUPPORT'
);


ALTER TYPE public.notificationtype OWNER TO postgres;

--
-- TOC entry 912 (class 1247 OID 25802)
-- Name: oauthprovider; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.oauthprovider AS ENUM (
    'GOOGLE'
);


ALTER TYPE public.oauthprovider OWNER TO postgres;

--
-- TOC entry 933 (class 1247 OID 25862)
-- Name: orderstatus; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.orderstatus AS ENUM (
    'PENDING',
    'CONFIRMED',
    'PROCESSING',
    'SHIPPED',
    'DELIVERED',
    'CANCELLED',
    'REFUNDED'
);


ALTER TYPE public.orderstatus OWNER TO postgres;

--
-- TOC entry 921 (class 1247 OID 25822)
-- Name: paymentstatus; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.paymentstatus AS ENUM (
    'PENDING',
    'AUTHORIZED',
    'CAPTURED',
    'FAILED',
    'REFUNDED'
);


ALTER TYPE public.paymentstatus OWNER TO postgres;

--
-- TOC entry 939 (class 1247 OID 25888)
-- Name: payoutstatus; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.payoutstatus AS ENUM (
    'PENDING',
    'PROCESSING',
    'COMPLETED',
    'FAILED'
);


ALTER TYPE public.payoutstatus OWNER TO postgres;

--
-- TOC entry 918 (class 1247 OID 25812)
-- Name: productstatus; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.productstatus AS ENUM (
    'DRAFT',
    'ACTIVE',
    'INACTIVE',
    'ARCHIVED'
);


ALTER TYPE public.productstatus OWNER TO postgres;

--
-- TOC entry 906 (class 1247 OID 25782)
-- Name: reportstatus; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.reportstatus AS ENUM (
    'PENDING',
    'REVIEWED',
    'DISMISSED',
    'ACTION_TAKEN'
);


ALTER TYPE public.reportstatus OWNER TO postgres;

--
-- TOC entry 924 (class 1247 OID 25834)
-- Name: returnstatus; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.returnstatus AS ENUM (
    'REQUESTED',
    'APPROVED',
    'REJECTED',
    'RECEIVED',
    'REFUNDED'
);


ALTER TYPE public.returnstatus OWNER TO postgres;

--
-- TOC entry 948 (class 1247 OID 25918)
-- Name: rolename; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.rolename AS ENUM (
    'ADMIN',
    'SELLER',
    'CUSTOMER'
);


ALTER TYPE public.rolename OWNER TO postgres;

--
-- TOC entry 936 (class 1247 OID 25878)
-- Name: sellerstatus; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.sellerstatus AS ENUM (
    'PENDING',
    'APPROVED',
    'SUSPENDED',
    'REJECTED'
);


ALTER TYPE public.sellerstatus OWNER TO postgres;

--
-- TOC entry 909 (class 1247 OID 25792)
-- Name: supportticketstatus; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.supportticketstatus AS ENUM (
    'OPEN',
    'IN_PROGRESS',
    'RESOLVED',
    'CLOSED'
);


ALTER TYPE public.supportticketstatus OWNER TO postgres;

--
-- TOC entry 915 (class 1247 OID 25806)
-- Name: tokenpurpose; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.tokenpurpose AS ENUM (
    'PASSWORD_RESET',
    'EMAIL_VERIFICATION'
);


ALTER TYPE public.tokenpurpose OWNER TO postgres;

--
-- TOC entry 945 (class 1247 OID 25908)
-- Name: transactionstatus; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.transactionstatus AS ENUM (
    'PENDING',
    'COMPLETED',
    'FAILED',
    'REFUNDED'
);


ALTER TYPE public.transactionstatus OWNER TO postgres;

--
-- TOC entry 942 (class 1247 OID 25898)
-- Name: transactiontype; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.transactiontype AS ENUM (
    'PAYMENT',
    'REFUND',
    'PAYOUT',
    'ADJUSTMENT'
);


ALTER TYPE public.transactiontype OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 244 (class 1259 OID 26441)
-- Name: activity_logs; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.activity_logs (
    user_id uuid,
    event_type character varying(64) NOT NULL,
    description character varying(512),
    metadata_json text,
    ip_address character varying(45),
    id uuid NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.activity_logs OWNER TO postgres;

--
-- TOC entry 228 (class 1259 OID 26073)
-- Name: addresses; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.addresses (
    user_id uuid NOT NULL,
    address_type public.addresstype NOT NULL,
    label character varying(64),
    line1 character varying(255) NOT NULL,
    line2 character varying(255),
    city character varying(128) NOT NULL,
    state character varying(128),
    postal_code character varying(32) NOT NULL,
    country character varying(2) NOT NULL,
    is_default boolean NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.addresses OWNER TO postgres;

--
-- TOC entry 229 (class 1259 OID 26100)
-- Name: admin_logs; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.admin_logs (
    admin_user_id uuid,
    action character varying(128) NOT NULL,
    entity_type character varying(64),
    entity_id uuid,
    details text,
    ip_address character varying(45),
    id uuid NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.admin_logs OWNER TO postgres;

--
-- TOC entry 241 (class 1259 OID 26378)
-- Name: admins; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.admins (
    user_id uuid NOT NULL,
    department character varying(128),
    title character varying(128),
    id uuid NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.admins OWNER TO postgres;

--
-- TOC entry 219 (class 1259 OID 25768)
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO postgres;

--
-- TOC entry 243 (class 1259 OID 26419)
-- Name: audit_logs; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.audit_logs (
    actor_id uuid,
    action character varying(128) NOT NULL,
    entity_type character varying(64),
    entity_id uuid,
    old_values text,
    new_values text,
    ip_address character varying(45),
    id uuid NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.audit_logs OWNER TO postgres;

--
-- TOC entry 220 (class 1259 OID 25925)
-- Name: banners; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.banners (
    title character varying(255) NOT NULL,
    image_url character varying(512) NOT NULL,
    link_url character varying(512),
    sort_order integer NOT NULL,
    is_active boolean NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.banners OWNER TO postgres;

--
-- TOC entry 224 (class 1259 OID 26005)
-- Name: brands; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.brands (
    name character varying(128) NOT NULL,
    slug character varying(128) NOT NULL,
    logo_url character varying(512),
    description text,
    is_active boolean NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone
);


ALTER TABLE public.brands OWNER TO postgres;

--
-- TOC entry 255 (class 1259 OID 26719)
-- Name: cart_items; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.cart_items (
    cart_id uuid NOT NULL,
    product_id uuid NOT NULL,
    quantity integer NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.cart_items OWNER TO postgres;

--
-- TOC entry 237 (class 1259 OID 26290)
-- Name: carts; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.carts (
    user_id uuid NOT NULL,
    is_active boolean NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.carts OWNER TO postgres;

--
-- TOC entry 223 (class 1259 OID 25981)
-- Name: categories; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.categories (
    name character varying(128) NOT NULL,
    slug character varying(128) NOT NULL,
    description text,
    parent_id uuid,
    is_active boolean NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.categories OWNER TO postgres;

--
-- TOC entry 221 (class 1259 OID 25942)
-- Name: cms_pages; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.cms_pages (
    slug character varying(128) NOT NULL,
    title character varying(255) NOT NULL,
    content text NOT NULL,
    is_published boolean NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.cms_pages OWNER TO postgres;

--
-- TOC entry 261 (class 1259 OID 26861)
-- Name: coupon_usages; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.coupon_usages (
    coupon_id uuid NOT NULL,
    user_id uuid NOT NULL,
    order_id uuid NOT NULL,
    discount_amount numeric(12,2) NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.coupon_usages OWNER TO postgres;

--
-- TOC entry 225 (class 1259 OID 26025)
-- Name: coupons; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.coupons (
    code character varying(64) NOT NULL,
    description character varying,
    discount_type public.coupondiscounttype NOT NULL,
    discount_value numeric(12,2) NOT NULL,
    min_order_amount numeric(12,2),
    max_uses integer,
    uses_count integer NOT NULL,
    starts_at timestamp with time zone,
    expires_at timestamp with time zone,
    is_active boolean NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.coupons OWNER TO postgres;

--
-- TOC entry 236 (class 1259 OID 26268)
-- Name: email_verification_tokens; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.email_verification_tokens (
    user_id uuid NOT NULL,
    token_hash character varying(64) NOT NULL,
    purpose public.tokenpurpose NOT NULL,
    expires_at timestamp with time zone NOT NULL,
    used_at timestamp with time zone,
    id uuid NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.email_verification_tokens OWNER TO postgres;

--
-- TOC entry 222 (class 1259 OID 25960)
-- Name: embeddings; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.embeddings (
    entity_type character varying(64) NOT NULL,
    entity_id uuid NOT NULL,
    model_name character varying(128) NOT NULL,
    dimensions integer NOT NULL,
    vector_data text,
    id uuid NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.embeddings OWNER TO postgres;

--
-- TOC entry 263 (class 1259 OID 26924)
-- Name: inventory; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.inventory (
    product_id uuid NOT NULL,
    quantity_available integer NOT NULL,
    quantity_reserved integer NOT NULL,
    low_stock_threshold integer NOT NULL,
    warehouse_code character varying,
    id uuid NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.inventory OWNER TO postgres;

--
-- TOC entry 242 (class 1259 OID 26395)
-- Name: notification_preferences; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.notification_preferences (
    user_id uuid NOT NULL,
    notification_type public.notificationtype NOT NULL,
    email_enabled boolean NOT NULL,
    push_enabled boolean NOT NULL,
    in_app_enabled boolean NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.notification_preferences OWNER TO postgres;

--
-- TOC entry 239 (class 1259 OID 26328)
-- Name: notifications; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.notifications (
    user_id uuid NOT NULL,
    notification_type public.notificationtype NOT NULL,
    title character varying(255) NOT NULL,
    body text NOT NULL,
    is_read boolean NOT NULL,
    read_at timestamp with time zone,
    metadata_json text,
    id uuid NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.notifications OWNER TO postgres;

--
-- TOC entry 234 (class 1259 OID 26223)
-- Name: oauth_accounts; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.oauth_accounts (
    user_id uuid NOT NULL,
    provider public.oauthprovider NOT NULL,
    provider_user_id character varying(255) NOT NULL,
    provider_email character varying(255),
    access_token_encrypted text,
    refresh_token_encrypted text,
    id uuid NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.oauth_accounts OWNER TO postgres;

--
-- TOC entry 264 (class 1259 OID 26947)
-- Name: order_items; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.order_items (
    order_id uuid NOT NULL,
    product_id uuid NOT NULL,
    product_name character varying(255) NOT NULL,
    quantity integer NOT NULL,
    unit_price numeric(12,2) NOT NULL,
    line_total numeric(12,2) NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.order_items OWNER TO postgres;

--
-- TOC entry 248 (class 1259 OID 26544)
-- Name: orders; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.orders (
    user_id uuid NOT NULL,
    shipping_address_id uuid,
    order_number character varying(32) NOT NULL,
    status public.orderstatus NOT NULL,
    subtotal numeric(12,2) NOT NULL,
    tax_amount numeric(12,2) NOT NULL,
    shipping_amount numeric(12,2) NOT NULL,
    discount_amount numeric(12,2) NOT NULL,
    total_amount numeric(12,2) NOT NULL,
    notes text,
    id uuid NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.orders OWNER TO postgres;

--
-- TOC entry 235 (class 1259 OID 26247)
-- Name: password_reset_tokens; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.password_reset_tokens (
    user_id uuid NOT NULL,
    token_hash character varying(64) NOT NULL,
    expires_at timestamp with time zone NOT NULL,
    used_at timestamp with time zone,
    id uuid NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.password_reset_tokens OWNER TO postgres;

--
-- TOC entry 260 (class 1259 OID 26839)
-- Name: payments; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.payments (
    order_id uuid NOT NULL,
    amount numeric(12,2) NOT NULL,
    currency character varying(3) NOT NULL,
    status public.paymentstatus NOT NULL,
    provider character varying(64),
    provider_reference character varying(255),
    id uuid NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.payments OWNER TO postgres;

--
-- TOC entry 232 (class 1259 OID 26176)
-- Name: personalization_data; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.personalization_data (
    user_id uuid NOT NULL,
    key character varying(128) NOT NULL,
    value text NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.personalization_data OWNER TO postgres;

--
-- TOC entry 259 (class 1259 OID 26822)
-- Name: product_categories; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.product_categories (
    product_id uuid NOT NULL,
    category_id uuid NOT NULL
);


ALTER TABLE public.product_categories OWNER TO postgres;

--
-- TOC entry 257 (class 1259 OID 26772)
-- Name: product_images; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.product_images (
    product_id uuid NOT NULL,
    url character varying(512) NOT NULL,
    alt_text character varying(255),
    sort_order integer NOT NULL,
    is_primary boolean NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.product_images OWNER TO postgres;

--
-- TOC entry 258 (class 1259 OID 26794)
-- Name: product_variants; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.product_variants (
    product_id uuid NOT NULL,
    sku character varying(64) NOT NULL,
    name character varying(128) NOT NULL,
    price numeric(12,2),
    attributes text,
    is_active boolean NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL,
    is_deleted boolean NOT NULL,
    deleted_at timestamp with time zone
);


ALTER TABLE public.product_variants OWNER TO postgres;

--
-- TOC entry 247 (class 1259 OID 26503)
-- Name: products; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.products (
    seller_id uuid NOT NULL,
    category_id uuid,
    brand_id uuid,
    name character varying(255) NOT NULL,
    slug character varying(255) NOT NULL,
    description text,
    sku character varying(64),
    price numeric(12,2) NOT NULL,
    compare_at_price numeric(12,2),
    status public.productstatus NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.products OWNER TO postgres;

--
-- TOC entry 253 (class 1259 OID 26663)
-- Name: recommendation_scores; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.recommendation_scores (
    user_id uuid NOT NULL,
    product_id uuid NOT NULL,
    algorithm character varying(64) NOT NULL,
    score numeric(8,6) NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.recommendation_scores OWNER TO postgres;

--
-- TOC entry 233 (class 1259 OID 26200)
-- Name: refresh_tokens; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.refresh_tokens (
    user_id uuid NOT NULL,
    token_hash character varying(64) NOT NULL,
    expires_at timestamp with time zone NOT NULL,
    revoked_at timestamp with time zone,
    user_agent character varying(512),
    ip_address character varying(45),
    id uuid NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.refresh_tokens OWNER TO postgres;

--
-- TOC entry 230 (class 1259 OID 26122)
-- Name: reports; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.reports (
    reporter_id uuid NOT NULL,
    entity_type character varying(64) NOT NULL,
    entity_id uuid NOT NULL,
    reason text NOT NULL,
    status public.reportstatus NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.reports OWNER TO postgres;

--
-- TOC entry 262 (class 1259 OID 26895)
-- Name: returns; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.returns (
    order_id uuid NOT NULL,
    user_id uuid NOT NULL,
    reason text NOT NULL,
    status public.returnstatus NOT NULL,
    refund_amount numeric(12,2),
    id uuid NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.returns OWNER TO postgres;

--
-- TOC entry 267 (class 1259 OID 27030)
-- Name: review_images; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.review_images (
    review_id uuid NOT NULL,
    url character varying(512) NOT NULL,
    sort_order integer NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.review_images OWNER TO postgres;

--
-- TOC entry 265 (class 1259 OID 26975)
-- Name: reviews; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.reviews (
    user_id uuid NOT NULL,
    product_id uuid NOT NULL,
    rating integer NOT NULL,
    title character varying(255),
    comment text,
    is_approved boolean NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL,
    CONSTRAINT ck_review_rating_range CHECK (((rating >= 1) AND (rating <= 5)))
);


ALTER TABLE public.reviews OWNER TO postgres;

--
-- TOC entry 227 (class 1259 OID 26061)
-- Name: roles; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.roles (
    name public.rolename NOT NULL,
    description character varying(255),
    id uuid NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.roles OWNER TO postgres;

--
-- TOC entry 254 (class 1259 OID 26692)
-- Name: search_analytics; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.search_analytics (
    user_id uuid,
    query character varying(512) NOT NULL,
    results_count integer NOT NULL,
    clicked_product_id uuid,
    session_id character varying(128),
    id uuid NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.search_analytics OWNER TO postgres;

--
-- TOC entry 249 (class 1259 OID 26577)
-- Name: seller_documents; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.seller_documents (
    seller_id uuid NOT NULL,
    document_type character varying(64) NOT NULL,
    file_url character varying(512) NOT NULL,
    status public.sellerstatus NOT NULL,
    notes text,
    id uuid NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.seller_documents OWNER TO postgres;

--
-- TOC entry 250 (class 1259 OID 26601)
-- Name: seller_payouts; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.seller_payouts (
    seller_id uuid NOT NULL,
    amount numeric(12,2) NOT NULL,
    currency character varying(3) NOT NULL,
    status public.payoutstatus NOT NULL,
    reference character varying(255),
    id uuid NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.seller_payouts OWNER TO postgres;

--
-- TOC entry 252 (class 1259 OID 26643)
-- Name: seller_settings; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.seller_settings (
    seller_id uuid NOT NULL,
    auto_fulfill boolean NOT NULL,
    notification_email character varying(255),
    return_policy text,
    shipping_policy text,
    theme_config text,
    id uuid NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.seller_settings OWNER TO postgres;

--
-- TOC entry 251 (class 1259 OID 26623)
-- Name: seller_wallets; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.seller_wallets (
    seller_id uuid NOT NULL,
    balance numeric(14,2) NOT NULL,
    pending_balance numeric(14,2) NOT NULL,
    currency character varying(3) NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.seller_wallets OWNER TO postgres;

--
-- TOC entry 240 (class 1259 OID 26353)
-- Name: sellers; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.sellers (
    user_id uuid NOT NULL,
    store_name character varying(255) NOT NULL,
    store_slug character varying(255) NOT NULL,
    description text,
    status public.sellerstatus NOT NULL,
    commission_rate double precision,
    id uuid NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.sellers OWNER TO postgres;

--
-- TOC entry 231 (class 1259 OID 26148)
-- Name: support_tickets; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.support_tickets (
    user_id uuid NOT NULL,
    subject character varying(255) NOT NULL,
    description text NOT NULL,
    status public.supportticketstatus NOT NULL,
    assigned_to_id uuid,
    id uuid NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.support_tickets OWNER TO postgres;

--
-- TOC entry 266 (class 1259 OID 27006)
-- Name: transactions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.transactions (
    order_id uuid,
    reference character varying(64) NOT NULL,
    transaction_type public.transactiontype NOT NULL,
    status public.transactionstatus NOT NULL,
    amount numeric(12,2) NOT NULL,
    currency character varying(3) NOT NULL,
    gateway character varying(64),
    gateway_ref character varying(255),
    id uuid NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.transactions OWNER TO postgres;

--
-- TOC entry 245 (class 1259 OID 26461)
-- Name: user_roles; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.user_roles (
    user_id uuid NOT NULL,
    role_id uuid NOT NULL
);


ALTER TABLE public.user_roles OWNER TO postgres;

--
-- TOC entry 246 (class 1259 OID 26478)
-- Name: user_sessions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.user_sessions (
    user_id uuid NOT NULL,
    refresh_token_id uuid,
    user_agent character varying(512),
    ip_address character varying(45),
    last_active_at timestamp with time zone NOT NULL,
    revoked_at timestamp with time zone,
    id uuid NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.user_sessions OWNER TO postgres;

--
-- TOC entry 226 (class 1259 OID 26044)
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    email character varying(255) NOT NULL,
    password_hash character varying(255),
    full_name character varying(255),
    phone character varying(32),
    is_active boolean NOT NULL,
    is_verified boolean NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL,
    avatar_url character varying(512)
);


ALTER TABLE public.users OWNER TO postgres;

--
-- TOC entry 256 (class 1259 OID 26746)
-- Name: wishlist_items; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.wishlist_items (
    wishlist_id uuid NOT NULL,
    product_id uuid NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.wishlist_items OWNER TO postgres;

--
-- TOC entry 238 (class 1259 OID 26309)
-- Name: wishlists; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.wishlists (
    user_id uuid NOT NULL,
    id uuid NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.wishlists OWNER TO postgres;

--
-- TOC entry 5610 (class 0 OID 26441)
-- Dependencies: 244
-- Data for Name: activity_logs; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.activity_logs (user_id, event_type, description, metadata_json, ip_address, id, created_at, updated_at) FROM stdin;
\.


--
-- TOC entry 5594 (class 0 OID 26073)
-- Dependencies: 228
-- Data for Name: addresses; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.addresses (user_id, address_type, label, line1, line2, city, state, postal_code, country, is_default, id, created_at, updated_at) FROM stdin;
\.


--
-- TOC entry 5595 (class 0 OID 26100)
-- Dependencies: 229
-- Data for Name: admin_logs; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.admin_logs (admin_user_id, action, entity_type, entity_id, details, ip_address, id, created_at, updated_at) FROM stdin;
\.


--
-- TOC entry 5607 (class 0 OID 26378)
-- Dependencies: 241
-- Data for Name: admins; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.admins (user_id, department, title, id, created_at, updated_at) FROM stdin;
\.


--
-- TOC entry 5585 (class 0 OID 25768)
-- Dependencies: 219
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.alembic_version (version_num) FROM stdin;
20260518_003
\.


--
-- TOC entry 5609 (class 0 OID 26419)
-- Dependencies: 243
-- Data for Name: audit_logs; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.audit_logs (actor_id, action, entity_type, entity_id, old_values, new_values, ip_address, id, created_at, updated_at) FROM stdin;
\.


--
-- TOC entry 5586 (class 0 OID 25925)
-- Dependencies: 220
-- Data for Name: banners; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.banners (title, image_url, link_url, sort_order, is_active, id, created_at, updated_at) FROM stdin;
\.


--
-- TOC entry 5590 (class 0 OID 26005)
-- Dependencies: 224
-- Data for Name: brands; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.brands (name, slug, logo_url, description, is_active, id, created_at, updated_at, is_deleted, deleted_at) FROM stdin;
\.


--
-- TOC entry 5621 (class 0 OID 26719)
-- Dependencies: 255
-- Data for Name: cart_items; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.cart_items (cart_id, product_id, quantity, id, created_at, updated_at) FROM stdin;
\.


--
-- TOC entry 5603 (class 0 OID 26290)
-- Dependencies: 237
-- Data for Name: carts; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.carts (user_id, is_active, id, created_at, updated_at) FROM stdin;
\.


--
-- TOC entry 5589 (class 0 OID 25981)
-- Dependencies: 223
-- Data for Name: categories; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.categories (name, slug, description, parent_id, is_active, id, created_at, updated_at) FROM stdin;
\.


--
-- TOC entry 5587 (class 0 OID 25942)
-- Dependencies: 221
-- Data for Name: cms_pages; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.cms_pages (slug, title, content, is_published, id, created_at, updated_at) FROM stdin;
\.


--
-- TOC entry 5627 (class 0 OID 26861)
-- Dependencies: 261
-- Data for Name: coupon_usages; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.coupon_usages (coupon_id, user_id, order_id, discount_amount, id, created_at, updated_at) FROM stdin;
\.


--
-- TOC entry 5591 (class 0 OID 26025)
-- Dependencies: 225
-- Data for Name: coupons; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.coupons (code, description, discount_type, discount_value, min_order_amount, max_uses, uses_count, starts_at, expires_at, is_active, id, created_at, updated_at) FROM stdin;
\.


--
-- TOC entry 5602 (class 0 OID 26268)
-- Dependencies: 236
-- Data for Name: email_verification_tokens; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.email_verification_tokens (user_id, token_hash, purpose, expires_at, used_at, id, created_at, updated_at) FROM stdin;
e82f4fbe-ef8c-4748-bc46-be7699acd67c	aaf5a734811c7c7272ef7dfc852e235ec60041b431d9f92a9a653034b78bb655	EMAIL_VERIFICATION	2026-05-19 22:07:37.132979+05:30	\N	14cb2ece-8aeb-4632-a1a7-daf8ec115c81	2026-05-18 22:07:36.398568+05:30	2026-05-18 22:07:36.398568+05:30
\.


--
-- TOC entry 5588 (class 0 OID 25960)
-- Dependencies: 222
-- Data for Name: embeddings; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.embeddings (entity_type, entity_id, model_name, dimensions, vector_data, id, created_at, updated_at) FROM stdin;
\.


--
-- TOC entry 5629 (class 0 OID 26924)
-- Dependencies: 263
-- Data for Name: inventory; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.inventory (product_id, quantity_available, quantity_reserved, low_stock_threshold, warehouse_code, id, created_at, updated_at) FROM stdin;
\.


--
-- TOC entry 5608 (class 0 OID 26395)
-- Dependencies: 242
-- Data for Name: notification_preferences; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.notification_preferences (user_id, notification_type, email_enabled, push_enabled, in_app_enabled, id, created_at, updated_at) FROM stdin;
\.


--
-- TOC entry 5605 (class 0 OID 26328)
-- Dependencies: 239
-- Data for Name: notifications; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.notifications (user_id, notification_type, title, body, is_read, read_at, metadata_json, id, created_at, updated_at) FROM stdin;
\.


--
-- TOC entry 5600 (class 0 OID 26223)
-- Dependencies: 234
-- Data for Name: oauth_accounts; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.oauth_accounts (user_id, provider, provider_user_id, provider_email, access_token_encrypted, refresh_token_encrypted, id, created_at, updated_at) FROM stdin;
866fc3d9-1b34-4188-b42f-e1d8da0e6ec9	GOOGLE	111477321418149267563	work.khaleel.dev@gmail.com	\N	\N	0f71468b-de09-4bb3-9a1f-53452d37444d	2026-05-18 22:25:38.27163+05:30	2026-05-18 22:25:38.27163+05:30
e82f4fbe-ef8c-4748-bc46-be7699acd67c	GOOGLE	100819230154780438726	khaleel@shnoor.com	\N	\N	7695de7b-879f-4654-b62c-fc27c37b3fe5	2026-05-18 22:29:54.712303+05:30	2026-05-18 22:29:54.712303+05:30
653b351c-3151-44bb-ad73-78a3ab2a7397	GOOGLE	109662478491618819092	22d41a05m2@gmail.com	\N	\N	7e0cbe5d-1928-4950-8f4f-7eed0ce4884a	2026-05-18 22:32:24.246688+05:30	2026-05-18 22:32:24.246688+05:30
\.


--
-- TOC entry 5630 (class 0 OID 26947)
-- Dependencies: 264
-- Data for Name: order_items; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.order_items (order_id, product_id, product_name, quantity, unit_price, line_total, id, created_at, updated_at) FROM stdin;
\.


--
-- TOC entry 5614 (class 0 OID 26544)
-- Dependencies: 248
-- Data for Name: orders; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.orders (user_id, shipping_address_id, order_number, status, subtotal, tax_amount, shipping_amount, discount_amount, total_amount, notes, id, created_at, updated_at) FROM stdin;
\.


--
-- TOC entry 5601 (class 0 OID 26247)
-- Dependencies: 235
-- Data for Name: password_reset_tokens; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.password_reset_tokens (user_id, token_hash, expires_at, used_at, id, created_at, updated_at) FROM stdin;
\.


--
-- TOC entry 5626 (class 0 OID 26839)
-- Dependencies: 260
-- Data for Name: payments; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.payments (order_id, amount, currency, status, provider, provider_reference, id, created_at, updated_at) FROM stdin;
\.


--
-- TOC entry 5598 (class 0 OID 26176)
-- Dependencies: 232
-- Data for Name: personalization_data; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.personalization_data (user_id, key, value, id, created_at, updated_at) FROM stdin;
\.


--
-- TOC entry 5625 (class 0 OID 26822)
-- Dependencies: 259
-- Data for Name: product_categories; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.product_categories (product_id, category_id) FROM stdin;
\.


--
-- TOC entry 5623 (class 0 OID 26772)
-- Dependencies: 257
-- Data for Name: product_images; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.product_images (product_id, url, alt_text, sort_order, is_primary, id, created_at, updated_at) FROM stdin;
\.


--
-- TOC entry 5624 (class 0 OID 26794)
-- Dependencies: 258
-- Data for Name: product_variants; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.product_variants (product_id, sku, name, price, attributes, is_active, id, created_at, updated_at, is_deleted, deleted_at) FROM stdin;
\.


--
-- TOC entry 5613 (class 0 OID 26503)
-- Dependencies: 247
-- Data for Name: products; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.products (seller_id, category_id, brand_id, name, slug, description, sku, price, compare_at_price, status, id, created_at, updated_at) FROM stdin;
\.


--
-- TOC entry 5619 (class 0 OID 26663)
-- Dependencies: 253
-- Data for Name: recommendation_scores; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.recommendation_scores (user_id, product_id, algorithm, score, id, created_at, updated_at) FROM stdin;
\.


--
-- TOC entry 5599 (class 0 OID 26200)
-- Dependencies: 233
-- Data for Name: refresh_tokens; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.refresh_tokens (user_id, token_hash, expires_at, revoked_at, user_agent, ip_address, id, created_at, updated_at) FROM stdin;
e82f4fbe-ef8c-4748-bc46-be7699acd67c	5a33f1b26b93fb22623df570ee40057a4f67ad8268b84b207f7eb03069396ef4	2026-05-25 22:07:43.211201+05:30	\N	\N	\N	8dfc1057-cdec-40d7-b36e-052c95824b54	2026-05-18 22:07:36.398568+05:30	2026-05-18 22:07:36.398568+05:30
e82f4fbe-ef8c-4748-bc46-be7699acd67c	fc7f212667c81da1adc72807cbbfa9eefdc78c4959286acfdfa9e1aab0c482d3	2026-05-25 22:19:08.644143+05:30	2026-05-18 22:19:38.390477+05:30	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36	127.0.0.1	130385d3-6e62-4c51-99fb-a7bf4947ace0	2026-05-18 22:19:08.166721+05:30	2026-05-18 22:19:38.381153+05:30
866fc3d9-1b34-4188-b42f-e1d8da0e6ec9	04645f947a6e87a5b0e833c9700bf7e720b6e0f4e17901880bec6847acdfd132	2026-05-25 22:25:38.415597+05:30	\N	\N	\N	48ecc2e7-949f-420c-a5a3-23e874a4b944	2026-05-18 22:25:38.27163+05:30	2026-05-18 22:25:38.27163+05:30
e82f4fbe-ef8c-4748-bc46-be7699acd67c	2aa0b02036c130c6b7e7552847d1466d239717800c847ad27317f20f534b6d33	2026-05-25 22:29:54.759553+05:30	2026-05-18 22:31:39.928029+05:30	\N	\N	2aec8941-649e-409d-bf89-6495f7724d8c	2026-05-18 22:29:54.712303+05:30	2026-05-18 22:31:39.924221+05:30
e82f4fbe-ef8c-4748-bc46-be7699acd67c	c2f2c276b1cc2f2a3f2ae07d6124544614b6a081a1b2913348dfd0efd050caa5	2026-05-25 22:31:44.42122+05:30	\N	\N	\N	8eb894b7-a3da-4cce-a2c6-0b6340ea7118	2026-05-18 22:31:44.387321+05:30	2026-05-18 22:31:44.387321+05:30
e82f4fbe-ef8c-4748-bc46-be7699acd67c	c57b579633bb013204b805d6dd9f646dd021ac00e5484b478818c47a22c80eb4	2026-05-25 22:31:45.590487+05:30	\N	\N	\N	53cc3a3a-32ec-4012-9844-c7403aec9aba	2026-05-18 22:31:45.566757+05:30	2026-05-18 22:31:45.566757+05:30
653b351c-3151-44bb-ad73-78a3ab2a7397	9ab6b09364eec38373a60c81fe10dac8fa0fb5031de26477a45e030f62c7a86b	2026-05-25 22:32:24.371652+05:30	\N	\N	\N	24caa71d-2fcb-498a-9ddc-662c064125e3	2026-05-18 22:32:24.246688+05:30	2026-05-18 22:32:24.246688+05:30
\.


--
-- TOC entry 5596 (class 0 OID 26122)
-- Dependencies: 230
-- Data for Name: reports; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.reports (reporter_id, entity_type, entity_id, reason, status, id, created_at, updated_at) FROM stdin;
\.


--
-- TOC entry 5628 (class 0 OID 26895)
-- Dependencies: 262
-- Data for Name: returns; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.returns (order_id, user_id, reason, status, refund_amount, id, created_at, updated_at) FROM stdin;
\.


--
-- TOC entry 5633 (class 0 OID 27030)
-- Dependencies: 267
-- Data for Name: review_images; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.review_images (review_id, url, sort_order, id, created_at, updated_at) FROM stdin;
\.


--
-- TOC entry 5631 (class 0 OID 26975)
-- Dependencies: 265
-- Data for Name: reviews; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.reviews (user_id, product_id, rating, title, comment, is_approved, id, created_at, updated_at) FROM stdin;
\.


--
-- TOC entry 5593 (class 0 OID 26061)
-- Dependencies: 227
-- Data for Name: roles; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.roles (name, description, id, created_at, updated_at) FROM stdin;
ADMIN	admin role	c44eee18-9d76-4c86-b0b2-2ef430ff2065	2026-05-18 22:06:33.295005+05:30	2026-05-18 22:06:33.295005+05:30
SELLER	seller role	e369e92e-f96c-4ff4-87ec-d8465c557f1a	2026-05-18 22:06:33.295005+05:30	2026-05-18 22:06:33.295005+05:30
CUSTOMER	customer role	ffa28ee6-45c1-4c47-bf86-23b1cda3206d	2026-05-18 22:06:33.295005+05:30	2026-05-18 22:06:33.295005+05:30
\.


--
-- TOC entry 5620 (class 0 OID 26692)
-- Dependencies: 254
-- Data for Name: search_analytics; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.search_analytics (user_id, query, results_count, clicked_product_id, session_id, id, created_at, updated_at) FROM stdin;
\.


--
-- TOC entry 5615 (class 0 OID 26577)
-- Dependencies: 249
-- Data for Name: seller_documents; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.seller_documents (seller_id, document_type, file_url, status, notes, id, created_at, updated_at) FROM stdin;
\.


--
-- TOC entry 5616 (class 0 OID 26601)
-- Dependencies: 250
-- Data for Name: seller_payouts; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.seller_payouts (seller_id, amount, currency, status, reference, id, created_at, updated_at) FROM stdin;
\.


--
-- TOC entry 5618 (class 0 OID 26643)
-- Dependencies: 252
-- Data for Name: seller_settings; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.seller_settings (seller_id, auto_fulfill, notification_email, return_policy, shipping_policy, theme_config, id, created_at, updated_at) FROM stdin;
\.


--
-- TOC entry 5617 (class 0 OID 26623)
-- Dependencies: 251
-- Data for Name: seller_wallets; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.seller_wallets (seller_id, balance, pending_balance, currency, id, created_at, updated_at) FROM stdin;
\.


--
-- TOC entry 5606 (class 0 OID 26353)
-- Dependencies: 240
-- Data for Name: sellers; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.sellers (user_id, store_name, store_slug, description, status, commission_rate, id, created_at, updated_at) FROM stdin;
\.


--
-- TOC entry 5597 (class 0 OID 26148)
-- Dependencies: 231
-- Data for Name: support_tickets; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.support_tickets (user_id, subject, description, status, assigned_to_id, id, created_at, updated_at) FROM stdin;
\.


--
-- TOC entry 5632 (class 0 OID 27006)
-- Dependencies: 266
-- Data for Name: transactions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.transactions (order_id, reference, transaction_type, status, amount, currency, gateway, gateway_ref, id, created_at, updated_at) FROM stdin;
\.


--
-- TOC entry 5611 (class 0 OID 26461)
-- Dependencies: 245
-- Data for Name: user_roles; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.user_roles (user_id, role_id) FROM stdin;
866fc3d9-1b34-4188-b42f-e1d8da0e6ec9	ffa28ee6-45c1-4c47-bf86-23b1cda3206d
e82f4fbe-ef8c-4748-bc46-be7699acd67c	c44eee18-9d76-4c86-b0b2-2ef430ff2065
653b351c-3151-44bb-ad73-78a3ab2a7397	e369e92e-f96c-4ff4-87ec-d8465c557f1a
\.


--
-- TOC entry 5612 (class 0 OID 26478)
-- Dependencies: 246
-- Data for Name: user_sessions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.user_sessions (user_id, refresh_token_id, user_agent, ip_address, last_active_at, revoked_at, id, created_at, updated_at) FROM stdin;
\.


--
-- TOC entry 5592 (class 0 OID 26044)
-- Dependencies: 226
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (email, password_hash, full_name, phone, is_active, is_verified, id, created_at, updated_at, avatar_url) FROM stdin;
work.khaleel.dev@gmail.com	\N	Shaik Khaleel	\N	t	t	866fc3d9-1b34-4188-b42f-e1d8da0e6ec9	2026-05-18 22:25:38.27163+05:30	2026-05-18 22:25:38.27163+05:30	\N
khaleel@shnoor.com	$2b$12$pmqrM/uhZg0N6dO5V9i/rOTiFP5Npco3YW2koBTlFraEIGb9s/obm	Shaik Khaleel	\N	t	t	e82f4fbe-ef8c-4748-bc46-be7699acd67c	2026-05-18 22:07:36.398568+05:30	2026-05-18 22:29:54.712303+05:30	https://res.cloudinary.com/dl2ub6iic/image/upload/v1779122970/shnoor/avatars/e82f4fbe-ef8c-4748-bc46-be7699acd67c.jpg
22d41a05m2@gmail.com	\N	Shaik Khaleel	\N	t	t	653b351c-3151-44bb-ad73-78a3ab2a7397	2026-05-18 22:32:24.246688+05:30	2026-05-18 22:32:24.246688+05:30	\N
\.


--
-- TOC entry 5622 (class 0 OID 26746)
-- Dependencies: 256
-- Data for Name: wishlist_items; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.wishlist_items (wishlist_id, product_id, id, created_at, updated_at) FROM stdin;
\.


--
-- TOC entry 5604 (class 0 OID 26309)
-- Dependencies: 238
-- Data for Name: wishlists; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.wishlists (user_id, id, created_at, updated_at) FROM stdin;
\.


--
-- TOC entry 5264 (class 2606 OID 26453)
-- Name: activity_logs activity_logs_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.activity_logs
    ADD CONSTRAINT activity_logs_pkey PRIMARY KEY (id);


--
-- TOC entry 5181 (class 2606 OID 26091)
-- Name: addresses addresses_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.addresses
    ADD CONSTRAINT addresses_pkey PRIMARY KEY (id);


--
-- TOC entry 5186 (class 2606 OID 26112)
-- Name: admin_logs admin_logs_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.admin_logs
    ADD CONSTRAINT admin_logs_pkey PRIMARY KEY (id);


--
-- TOC entry 5249 (class 2606 OID 26388)
-- Name: admins admins_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.admins
    ADD CONSTRAINT admins_pkey PRIMARY KEY (id);


--
-- TOC entry 5142 (class 2606 OID 25773)
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- TOC entry 5258 (class 2606 OID 26431)
-- Name: audit_logs audit_logs_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.audit_logs
    ADD CONSTRAINT audit_logs_pkey PRIMARY KEY (id);


--
-- TOC entry 5144 (class 2606 OID 25940)
-- Name: banners banners_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.banners
    ADD CONSTRAINT banners_pkey PRIMARY KEY (id);


--
-- TOC entry 5164 (class 2606 OID 26020)
-- Name: brands brands_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.brands
    ADD CONSTRAINT brands_pkey PRIMARY KEY (id);


--
-- TOC entry 5317 (class 2606 OID 26731)
-- Name: cart_items cart_items_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cart_items
    ADD CONSTRAINT cart_items_pkey PRIMARY KEY (id);


--
-- TOC entry 5229 (class 2606 OID 26301)
-- Name: carts carts_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.carts
    ADD CONSTRAINT carts_pkey PRIMARY KEY (id);


--
-- TOC entry 5158 (class 2606 OID 25995)
-- Name: categories categories_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.categories
    ADD CONSTRAINT categories_pkey PRIMARY KEY (id);


--
-- TOC entry 5147 (class 2606 OID 25957)
-- Name: cms_pages cms_pages_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cms_pages
    ADD CONSTRAINT cms_pages_pkey PRIMARY KEY (id);


--
-- TOC entry 5347 (class 2606 OID 26874)
-- Name: coupon_usages coupon_usages_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.coupon_usages
    ADD CONSTRAINT coupon_usages_pkey PRIMARY KEY (id);


--
-- TOC entry 5170 (class 2606 OID 26041)
-- Name: coupons coupons_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.coupons
    ADD CONSTRAINT coupons_pkey PRIMARY KEY (id);


--
-- TOC entry 5224 (class 2606 OID 26281)
-- Name: email_verification_tokens email_verification_tokens_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.email_verification_tokens
    ADD CONSTRAINT email_verification_tokens_pkey PRIMARY KEY (id);


--
-- TOC entry 5151 (class 2606 OID 25975)
-- Name: embeddings embeddings_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.embeddings
    ADD CONSTRAINT embeddings_pkey PRIMARY KEY (id);


--
-- TOC entry 5359 (class 2606 OID 26939)
-- Name: inventory inventory_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.inventory
    ADD CONSTRAINT inventory_pkey PRIMARY KEY (id);


--
-- TOC entry 5254 (class 2606 OID 26409)
-- Name: notification_preferences notification_preferences_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.notification_preferences
    ADD CONSTRAINT notification_preferences_pkey PRIMARY KEY (id);


--
-- TOC entry 5241 (class 2606 OID 26344)
-- Name: notifications notifications_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.notifications
    ADD CONSTRAINT notifications_pkey PRIMARY KEY (id);


--
-- TOC entry 5215 (class 2606 OID 26237)
-- Name: oauth_accounts oauth_accounts_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.oauth_accounts
    ADD CONSTRAINT oauth_accounts_pkey PRIMARY KEY (id);


--
-- TOC entry 5365 (class 2606 OID 26962)
-- Name: order_items order_items_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.order_items
    ADD CONSTRAINT order_items_pkey PRIMARY KEY (id);


--
-- TOC entry 5287 (class 2606 OID 26563)
-- Name: orders orders_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_pkey PRIMARY KEY (id);


--
-- TOC entry 5222 (class 2606 OID 26259)
-- Name: password_reset_tokens password_reset_tokens_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.password_reset_tokens
    ADD CONSTRAINT password_reset_tokens_pkey PRIMARY KEY (id);


--
-- TOC entry 5345 (class 2606 OID 26852)
-- Name: payments payments_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.payments
    ADD CONSTRAINT payments_pkey PRIMARY KEY (id);


--
-- TOC entry 5204 (class 2606 OID 26190)
-- Name: personalization_data personalization_data_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.personalization_data
    ADD CONSTRAINT personalization_data_pkey PRIMARY KEY (id);


--
-- TOC entry 5340 (class 2606 OID 26828)
-- Name: product_categories product_categories_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.product_categories
    ADD CONSTRAINT product_categories_pkey PRIMARY KEY (product_id, category_id);


--
-- TOC entry 5330 (class 2606 OID 26787)
-- Name: product_images product_images_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.product_images
    ADD CONSTRAINT product_images_pkey PRIMARY KEY (id);


--
-- TOC entry 5336 (class 2606 OID 26810)
-- Name: product_variants product_variants_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.product_variants
    ADD CONSTRAINT product_variants_pkey PRIMARY KEY (id);


--
-- TOC entry 5280 (class 2606 OID 26519)
-- Name: products products_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_pkey PRIMARY KEY (id);


--
-- TOC entry 5308 (class 2606 OID 26676)
-- Name: recommendation_scores recommendation_scores_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.recommendation_scores
    ADD CONSTRAINT recommendation_scores_pkey PRIMARY KEY (id);


--
-- TOC entry 5211 (class 2606 OID 26214)
-- Name: refresh_tokens refresh_tokens_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.refresh_tokens
    ADD CONSTRAINT refresh_tokens_pkey PRIMARY KEY (id);


--
-- TOC entry 5196 (class 2606 OID 26138)
-- Name: reports reports_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reports
    ADD CONSTRAINT reports_pkey PRIMARY KEY (id);


--
-- TOC entry 5357 (class 2606 OID 26910)
-- Name: returns returns_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.returns
    ADD CONSTRAINT returns_pkey PRIMARY KEY (id);


--
-- TOC entry 5380 (class 2606 OID 27044)
-- Name: review_images review_images_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.review_images
    ADD CONSTRAINT review_images_pkey PRIMARY KEY (id);


--
-- TOC entry 5371 (class 2606 OID 26991)
-- Name: reviews reviews_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reviews
    ADD CONSTRAINT reviews_pkey PRIMARY KEY (id);


--
-- TOC entry 5179 (class 2606 OID 26071)
-- Name: roles roles_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_pkey PRIMARY KEY (id);


--
-- TOC entry 5315 (class 2606 OID 26705)
-- Name: search_analytics search_analytics_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.search_analytics
    ADD CONSTRAINT search_analytics_pkey PRIMARY KEY (id);


--
-- TOC entry 5292 (class 2606 OID 26592)
-- Name: seller_documents seller_documents_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.seller_documents
    ADD CONSTRAINT seller_documents_pkey PRIMARY KEY (id);


--
-- TOC entry 5297 (class 2606 OID 26614)
-- Name: seller_payouts seller_payouts_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.seller_payouts
    ADD CONSTRAINT seller_payouts_pkey PRIMARY KEY (id);


--
-- TOC entry 5303 (class 2606 OID 26656)
-- Name: seller_settings seller_settings_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.seller_settings
    ADD CONSTRAINT seller_settings_pkey PRIMARY KEY (id);


--
-- TOC entry 5300 (class 2606 OID 26636)
-- Name: seller_wallets seller_wallets_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.seller_wallets
    ADD CONSTRAINT seller_wallets_pkey PRIMARY KEY (id);


--
-- TOC entry 5247 (class 2606 OID 26368)
-- Name: sellers sellers_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sellers
    ADD CONSTRAINT sellers_pkey PRIMARY KEY (id);


--
-- TOC entry 5200 (class 2606 OID 26163)
-- Name: support_tickets support_tickets_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.support_tickets
    ADD CONSTRAINT support_tickets_pkey PRIMARY KEY (id);


--
-- TOC entry 5377 (class 2606 OID 27020)
-- Name: transactions transactions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.transactions
    ADD CONSTRAINT transactions_pkey PRIMARY KEY (id);


--
-- TOC entry 5321 (class 2606 OID 26733)
-- Name: cart_items uq_cart_product; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cart_items
    ADD CONSTRAINT uq_cart_product UNIQUE (cart_id, product_id);


--
-- TOC entry 5352 (class 2606 OID 26876)
-- Name: coupon_usages uq_coupon_usage; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.coupon_usages
    ADD CONSTRAINT uq_coupon_usage UNIQUE (coupon_id, user_id, order_id);


--
-- TOC entry 5156 (class 2606 OID 25977)
-- Name: embeddings uq_embedding_entity; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.embeddings
    ADD CONSTRAINT uq_embedding_entity UNIQUE (entity_type, entity_id, model_name);


--
-- TOC entry 5217 (class 2606 OID 26239)
-- Name: oauth_accounts uq_oauth_provider_user; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.oauth_accounts
    ADD CONSTRAINT uq_oauth_provider_user UNIQUE (provider, provider_user_id);


--
-- TOC entry 5206 (class 2606 OID 26192)
-- Name: personalization_data uq_personalization_user_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.personalization_data
    ADD CONSTRAINT uq_personalization_user_key UNIQUE (user_id, key);


--
-- TOC entry 5282 (class 2606 OID 26521)
-- Name: products uq_product_seller_slug; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT uq_product_seller_slug UNIQUE (seller_id, slug);


--
-- TOC entry 5310 (class 2606 OID 26678)
-- Name: recommendation_scores uq_rec_user_product_algo; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.recommendation_scores
    ADD CONSTRAINT uq_rec_user_product_algo UNIQUE (user_id, product_id, algorithm);


--
-- TOC entry 5256 (class 2606 OID 26411)
-- Name: notification_preferences uq_user_notification_pref; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.notification_preferences
    ADD CONSTRAINT uq_user_notification_pref UNIQUE (user_id, notification_type);


--
-- TOC entry 5268 (class 2606 OID 26467)
-- Name: user_roles uq_user_role; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_roles
    ADD CONSTRAINT uq_user_role PRIMARY KEY (user_id, role_id);


--
-- TOC entry 5338 (class 2606 OID 26812)
-- Name: product_variants uq_variant_product_sku; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.product_variants
    ADD CONSTRAINT uq_variant_product_sku UNIQUE (product_id, sku);


--
-- TOC entry 5325 (class 2606 OID 26759)
-- Name: wishlist_items uq_wishlist_product; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.wishlist_items
    ADD CONSTRAINT uq_wishlist_product UNIQUE (wishlist_id, product_id);


--
-- TOC entry 5234 (class 2606 OID 26321)
-- Name: wishlists uq_wishlist_user; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.wishlists
    ADD CONSTRAINT uq_wishlist_user UNIQUE (user_id);


--
-- TOC entry 5271 (class 2606 OID 26491)
-- Name: user_sessions user_sessions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_sessions
    ADD CONSTRAINT user_sessions_pkey PRIMARY KEY (id);


--
-- TOC entry 5176 (class 2606 OID 26058)
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- TOC entry 5327 (class 2606 OID 26757)
-- Name: wishlist_items wishlist_items_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.wishlist_items
    ADD CONSTRAINT wishlist_items_pkey PRIMARY KEY (id);


--
-- TOC entry 5236 (class 2606 OID 26319)
-- Name: wishlists wishlists_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.wishlists
    ADD CONSTRAINT wishlists_pkey PRIMARY KEY (id);


--
-- TOC entry 5265 (class 1259 OID 26460)
-- Name: ix_activity_logs_event_type; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_activity_logs_event_type ON public.activity_logs USING btree (event_type);


--
-- TOC entry 5266 (class 1259 OID 26459)
-- Name: ix_activity_logs_user_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_activity_logs_user_id ON public.activity_logs USING btree (user_id);


--
-- TOC entry 5182 (class 1259 OID 26098)
-- Name: ix_addresses_country; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_addresses_country ON public.addresses USING btree (country);


--
-- TOC entry 5183 (class 1259 OID 26097)
-- Name: ix_addresses_is_default; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_addresses_is_default ON public.addresses USING btree (is_default);


--
-- TOC entry 5184 (class 1259 OID 26099)
-- Name: ix_addresses_user_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_addresses_user_id ON public.addresses USING btree (user_id);


--
-- TOC entry 5187 (class 1259 OID 26119)
-- Name: ix_admin_logs_action; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_admin_logs_action ON public.admin_logs USING btree (action);


--
-- TOC entry 5188 (class 1259 OID 26120)
-- Name: ix_admin_logs_admin_user_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_admin_logs_admin_user_id ON public.admin_logs USING btree (admin_user_id);


--
-- TOC entry 5189 (class 1259 OID 26121)
-- Name: ix_admin_logs_entity_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_admin_logs_entity_id ON public.admin_logs USING btree (entity_id);


--
-- TOC entry 5190 (class 1259 OID 26118)
-- Name: ix_admin_logs_entity_type; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_admin_logs_entity_type ON public.admin_logs USING btree (entity_type);


--
-- TOC entry 5250 (class 1259 OID 26394)
-- Name: ix_admins_user_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_admins_user_id ON public.admins USING btree (user_id);


--
-- TOC entry 5259 (class 1259 OID 26440)
-- Name: ix_audit_logs_action; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_audit_logs_action ON public.audit_logs USING btree (action);


--
-- TOC entry 5260 (class 1259 OID 26438)
-- Name: ix_audit_logs_actor_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_audit_logs_actor_id ON public.audit_logs USING btree (actor_id);


--
-- TOC entry 5261 (class 1259 OID 26439)
-- Name: ix_audit_logs_entity_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_audit_logs_entity_id ON public.audit_logs USING btree (entity_id);


--
-- TOC entry 5262 (class 1259 OID 26437)
-- Name: ix_audit_logs_entity_type; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_audit_logs_entity_type ON public.audit_logs USING btree (entity_type);


--
-- TOC entry 5145 (class 1259 OID 25941)
-- Name: ix_banners_is_active; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_banners_is_active ON public.banners USING btree (is_active);


--
-- TOC entry 5165 (class 1259 OID 26021)
-- Name: ix_brands_is_active; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_brands_is_active ON public.brands USING btree (is_active);


--
-- TOC entry 5166 (class 1259 OID 26024)
-- Name: ix_brands_is_deleted; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_brands_is_deleted ON public.brands USING btree (is_deleted);


--
-- TOC entry 5167 (class 1259 OID 26023)
-- Name: ix_brands_name; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_brands_name ON public.brands USING btree (name);


--
-- TOC entry 5168 (class 1259 OID 26022)
-- Name: ix_brands_slug; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_brands_slug ON public.brands USING btree (slug);


--
-- TOC entry 5318 (class 1259 OID 26745)
-- Name: ix_cart_items_cart_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_cart_items_cart_id ON public.cart_items USING btree (cart_id);


--
-- TOC entry 5319 (class 1259 OID 26744)
-- Name: ix_cart_items_product_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_cart_items_product_id ON public.cart_items USING btree (product_id);


--
-- TOC entry 5230 (class 1259 OID 26308)
-- Name: ix_carts_is_active; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_carts_is_active ON public.carts USING btree (is_active);


--
-- TOC entry 5231 (class 1259 OID 26307)
-- Name: ix_carts_user_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_carts_user_id ON public.carts USING btree (user_id);


--
-- TOC entry 5159 (class 1259 OID 26002)
-- Name: ix_categories_is_active; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_categories_is_active ON public.categories USING btree (is_active);


--
-- TOC entry 5160 (class 1259 OID 26001)
-- Name: ix_categories_name; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_categories_name ON public.categories USING btree (name);


--
-- TOC entry 5161 (class 1259 OID 26004)
-- Name: ix_categories_parent_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_categories_parent_id ON public.categories USING btree (parent_id);


--
-- TOC entry 5162 (class 1259 OID 26003)
-- Name: ix_categories_slug; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_categories_slug ON public.categories USING btree (slug);


--
-- TOC entry 5148 (class 1259 OID 25958)
-- Name: ix_cms_pages_is_published; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_cms_pages_is_published ON public.cms_pages USING btree (is_published);


--
-- TOC entry 5149 (class 1259 OID 25959)
-- Name: ix_cms_pages_slug; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_cms_pages_slug ON public.cms_pages USING btree (slug);


--
-- TOC entry 5348 (class 1259 OID 26893)
-- Name: ix_coupon_usages_coupon_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_coupon_usages_coupon_id ON public.coupon_usages USING btree (coupon_id);


--
-- TOC entry 5349 (class 1259 OID 26892)
-- Name: ix_coupon_usages_order_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_coupon_usages_order_id ON public.coupon_usages USING btree (order_id);


--
-- TOC entry 5350 (class 1259 OID 26894)
-- Name: ix_coupon_usages_user_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_coupon_usages_user_id ON public.coupon_usages USING btree (user_id);


--
-- TOC entry 5171 (class 1259 OID 26043)
-- Name: ix_coupons_code; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_coupons_code ON public.coupons USING btree (code);


--
-- TOC entry 5172 (class 1259 OID 26042)
-- Name: ix_coupons_is_active; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_coupons_is_active ON public.coupons USING btree (is_active);


--
-- TOC entry 5225 (class 1259 OID 26288)
-- Name: ix_email_verification_tokens_expires_at; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_email_verification_tokens_expires_at ON public.email_verification_tokens USING btree (expires_at);


--
-- TOC entry 5226 (class 1259 OID 26287)
-- Name: ix_email_verification_tokens_token_hash; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_email_verification_tokens_token_hash ON public.email_verification_tokens USING btree (token_hash);


--
-- TOC entry 5227 (class 1259 OID 26289)
-- Name: ix_email_verification_tokens_user_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_email_verification_tokens_user_id ON public.email_verification_tokens USING btree (user_id);


--
-- TOC entry 5152 (class 1259 OID 25980)
-- Name: ix_embeddings_entity_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_embeddings_entity_id ON public.embeddings USING btree (entity_id);


--
-- TOC entry 5153 (class 1259 OID 25979)
-- Name: ix_embeddings_entity_type; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_embeddings_entity_type ON public.embeddings USING btree (entity_type);


--
-- TOC entry 5154 (class 1259 OID 25978)
-- Name: ix_embeddings_model_name; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_embeddings_model_name ON public.embeddings USING btree (model_name);


--
-- TOC entry 5360 (class 1259 OID 26946)
-- Name: ix_inventory_product_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_inventory_product_id ON public.inventory USING btree (product_id);


--
-- TOC entry 5361 (class 1259 OID 26945)
-- Name: ix_inventory_warehouse_code; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_inventory_warehouse_code ON public.inventory USING btree (warehouse_code);


--
-- TOC entry 5251 (class 1259 OID 26417)
-- Name: ix_notification_preferences_notification_type; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_notification_preferences_notification_type ON public.notification_preferences USING btree (notification_type);


--
-- TOC entry 5252 (class 1259 OID 26418)
-- Name: ix_notification_preferences_user_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_notification_preferences_user_id ON public.notification_preferences USING btree (user_id);


--
-- TOC entry 5237 (class 1259 OID 26351)
-- Name: ix_notifications_is_read; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_notifications_is_read ON public.notifications USING btree (is_read);


--
-- TOC entry 5238 (class 1259 OID 26350)
-- Name: ix_notifications_notification_type; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_notifications_notification_type ON public.notifications USING btree (notification_type);


--
-- TOC entry 5239 (class 1259 OID 26352)
-- Name: ix_notifications_user_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_notifications_user_id ON public.notifications USING btree (user_id);


--
-- TOC entry 5212 (class 1259 OID 26245)
-- Name: ix_oauth_accounts_provider; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_oauth_accounts_provider ON public.oauth_accounts USING btree (provider);


--
-- TOC entry 5213 (class 1259 OID 26246)
-- Name: ix_oauth_accounts_user_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_oauth_accounts_user_id ON public.oauth_accounts USING btree (user_id);


--
-- TOC entry 5362 (class 1259 OID 26974)
-- Name: ix_order_items_order_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_order_items_order_id ON public.order_items USING btree (order_id);


--
-- TOC entry 5363 (class 1259 OID 26973)
-- Name: ix_order_items_product_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_order_items_product_id ON public.order_items USING btree (product_id);


--
-- TOC entry 5283 (class 1259 OID 26576)
-- Name: ix_orders_order_number; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_orders_order_number ON public.orders USING btree (order_number);


--
-- TOC entry 5284 (class 1259 OID 26574)
-- Name: ix_orders_status; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_orders_status ON public.orders USING btree (status);


--
-- TOC entry 5285 (class 1259 OID 26575)
-- Name: ix_orders_user_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_orders_user_id ON public.orders USING btree (user_id);


--
-- TOC entry 5218 (class 1259 OID 26265)
-- Name: ix_password_reset_tokens_expires_at; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_password_reset_tokens_expires_at ON public.password_reset_tokens USING btree (expires_at);


--
-- TOC entry 5219 (class 1259 OID 26266)
-- Name: ix_password_reset_tokens_token_hash; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_password_reset_tokens_token_hash ON public.password_reset_tokens USING btree (token_hash);


--
-- TOC entry 5220 (class 1259 OID 26267)
-- Name: ix_password_reset_tokens_user_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_password_reset_tokens_user_id ON public.password_reset_tokens USING btree (user_id);


--
-- TOC entry 5341 (class 1259 OID 26858)
-- Name: ix_payments_order_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_payments_order_id ON public.payments USING btree (order_id);


--
-- TOC entry 5342 (class 1259 OID 26859)
-- Name: ix_payments_provider_reference; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_payments_provider_reference ON public.payments USING btree (provider_reference);


--
-- TOC entry 5343 (class 1259 OID 26860)
-- Name: ix_payments_status; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_payments_status ON public.payments USING btree (status);


--
-- TOC entry 5201 (class 1259 OID 26199)
-- Name: ix_personalization_data_key; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_personalization_data_key ON public.personalization_data USING btree (key);


--
-- TOC entry 5202 (class 1259 OID 26198)
-- Name: ix_personalization_data_user_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_personalization_data_user_id ON public.personalization_data USING btree (user_id);


--
-- TOC entry 5328 (class 1259 OID 26793)
-- Name: ix_product_images_product_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_product_images_product_id ON public.product_images USING btree (product_id);


--
-- TOC entry 5331 (class 1259 OID 26821)
-- Name: ix_product_variants_is_active; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_product_variants_is_active ON public.product_variants USING btree (is_active);


--
-- TOC entry 5332 (class 1259 OID 26820)
-- Name: ix_product_variants_is_deleted; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_product_variants_is_deleted ON public.product_variants USING btree (is_deleted);


--
-- TOC entry 5333 (class 1259 OID 26819)
-- Name: ix_product_variants_product_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_product_variants_product_id ON public.product_variants USING btree (product_id);


--
-- TOC entry 5334 (class 1259 OID 26818)
-- Name: ix_product_variants_sku; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_product_variants_sku ON public.product_variants USING btree (sku);


--
-- TOC entry 5272 (class 1259 OID 26542)
-- Name: ix_products_brand_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_products_brand_id ON public.products USING btree (brand_id);


--
-- TOC entry 5273 (class 1259 OID 26539)
-- Name: ix_products_category_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_products_category_id ON public.products USING btree (category_id);


--
-- TOC entry 5274 (class 1259 OID 26537)
-- Name: ix_products_name; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_products_name ON public.products USING btree (name);


--
-- TOC entry 5275 (class 1259 OID 26543)
-- Name: ix_products_seller_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_products_seller_id ON public.products USING btree (seller_id);


--
-- TOC entry 5276 (class 1259 OID 26541)
-- Name: ix_products_sku; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_products_sku ON public.products USING btree (sku);


--
-- TOC entry 5277 (class 1259 OID 26540)
-- Name: ix_products_slug; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_products_slug ON public.products USING btree (slug);


--
-- TOC entry 5278 (class 1259 OID 26538)
-- Name: ix_products_status; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_products_status ON public.products USING btree (status);


--
-- TOC entry 5304 (class 1259 OID 26689)
-- Name: ix_recommendation_scores_algorithm; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_recommendation_scores_algorithm ON public.recommendation_scores USING btree (algorithm);


--
-- TOC entry 5305 (class 1259 OID 26691)
-- Name: ix_recommendation_scores_product_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_recommendation_scores_product_id ON public.recommendation_scores USING btree (product_id);


--
-- TOC entry 5306 (class 1259 OID 26690)
-- Name: ix_recommendation_scores_user_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_recommendation_scores_user_id ON public.recommendation_scores USING btree (user_id);


--
-- TOC entry 5207 (class 1259 OID 26221)
-- Name: ix_refresh_tokens_expires_at; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_refresh_tokens_expires_at ON public.refresh_tokens USING btree (expires_at);


--
-- TOC entry 5208 (class 1259 OID 26220)
-- Name: ix_refresh_tokens_token_hash; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_refresh_tokens_token_hash ON public.refresh_tokens USING btree (token_hash);


--
-- TOC entry 5209 (class 1259 OID 26222)
-- Name: ix_refresh_tokens_user_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_refresh_tokens_user_id ON public.refresh_tokens USING btree (user_id);


--
-- TOC entry 5191 (class 1259 OID 26146)
-- Name: ix_reports_entity_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_reports_entity_id ON public.reports USING btree (entity_id);


--
-- TOC entry 5192 (class 1259 OID 26147)
-- Name: ix_reports_entity_type; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_reports_entity_type ON public.reports USING btree (entity_type);


--
-- TOC entry 5193 (class 1259 OID 26145)
-- Name: ix_reports_reporter_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_reports_reporter_id ON public.reports USING btree (reporter_id);


--
-- TOC entry 5194 (class 1259 OID 26144)
-- Name: ix_reports_status; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_reports_status ON public.reports USING btree (status);


--
-- TOC entry 5353 (class 1259 OID 26922)
-- Name: ix_returns_order_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_returns_order_id ON public.returns USING btree (order_id);


--
-- TOC entry 5354 (class 1259 OID 26921)
-- Name: ix_returns_status; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_returns_status ON public.returns USING btree (status);


--
-- TOC entry 5355 (class 1259 OID 26923)
-- Name: ix_returns_user_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_returns_user_id ON public.returns USING btree (user_id);


--
-- TOC entry 5378 (class 1259 OID 27050)
-- Name: ix_review_images_review_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_review_images_review_id ON public.review_images USING btree (review_id);


--
-- TOC entry 5366 (class 1259 OID 27004)
-- Name: ix_reviews_is_approved; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_reviews_is_approved ON public.reviews USING btree (is_approved);


--
-- TOC entry 5367 (class 1259 OID 27002)
-- Name: ix_reviews_product_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_reviews_product_id ON public.reviews USING btree (product_id);


--
-- TOC entry 5368 (class 1259 OID 27005)
-- Name: ix_reviews_rating; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_reviews_rating ON public.reviews USING btree (rating);


--
-- TOC entry 5369 (class 1259 OID 27003)
-- Name: ix_reviews_user_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_reviews_user_id ON public.reviews USING btree (user_id);


--
-- TOC entry 5177 (class 1259 OID 26072)
-- Name: ix_roles_name; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_roles_name ON public.roles USING btree (name);


--
-- TOC entry 5311 (class 1259 OID 26718)
-- Name: ix_search_analytics_query; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_search_analytics_query ON public.search_analytics USING btree (query);


--
-- TOC entry 5312 (class 1259 OID 26716)
-- Name: ix_search_analytics_session_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_search_analytics_session_id ON public.search_analytics USING btree (session_id);


--
-- TOC entry 5313 (class 1259 OID 26717)
-- Name: ix_search_analytics_user_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_search_analytics_user_id ON public.search_analytics USING btree (user_id);


--
-- TOC entry 5288 (class 1259 OID 26600)
-- Name: ix_seller_documents_document_type; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_seller_documents_document_type ON public.seller_documents USING btree (document_type);


--
-- TOC entry 5289 (class 1259 OID 26598)
-- Name: ix_seller_documents_seller_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_seller_documents_seller_id ON public.seller_documents USING btree (seller_id);


--
-- TOC entry 5290 (class 1259 OID 26599)
-- Name: ix_seller_documents_status; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_seller_documents_status ON public.seller_documents USING btree (status);


--
-- TOC entry 5293 (class 1259 OID 26622)
-- Name: ix_seller_payouts_reference; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_seller_payouts_reference ON public.seller_payouts USING btree (reference);


--
-- TOC entry 5294 (class 1259 OID 26620)
-- Name: ix_seller_payouts_seller_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_seller_payouts_seller_id ON public.seller_payouts USING btree (seller_id);


--
-- TOC entry 5295 (class 1259 OID 26621)
-- Name: ix_seller_payouts_status; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_seller_payouts_status ON public.seller_payouts USING btree (status);


--
-- TOC entry 5301 (class 1259 OID 26662)
-- Name: ix_seller_settings_seller_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_seller_settings_seller_id ON public.seller_settings USING btree (seller_id);


--
-- TOC entry 5298 (class 1259 OID 26642)
-- Name: ix_seller_wallets_seller_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_seller_wallets_seller_id ON public.seller_wallets USING btree (seller_id);


--
-- TOC entry 5242 (class 1259 OID 26376)
-- Name: ix_sellers_status; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_sellers_status ON public.sellers USING btree (status);


--
-- TOC entry 5243 (class 1259 OID 26377)
-- Name: ix_sellers_store_name; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_sellers_store_name ON public.sellers USING btree (store_name);


--
-- TOC entry 5244 (class 1259 OID 26375)
-- Name: ix_sellers_store_slug; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_sellers_store_slug ON public.sellers USING btree (store_slug);


--
-- TOC entry 5245 (class 1259 OID 26374)
-- Name: ix_sellers_user_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_sellers_user_id ON public.sellers USING btree (user_id);


--
-- TOC entry 5197 (class 1259 OID 26175)
-- Name: ix_support_tickets_status; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_support_tickets_status ON public.support_tickets USING btree (status);


--
-- TOC entry 5198 (class 1259 OID 26174)
-- Name: ix_support_tickets_user_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_support_tickets_user_id ON public.support_tickets USING btree (user_id);


--
-- TOC entry 5372 (class 1259 OID 27029)
-- Name: ix_transactions_order_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_transactions_order_id ON public.transactions USING btree (order_id);


--
-- TOC entry 5373 (class 1259 OID 27027)
-- Name: ix_transactions_reference; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_transactions_reference ON public.transactions USING btree (reference);


--
-- TOC entry 5374 (class 1259 OID 27026)
-- Name: ix_transactions_status; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_transactions_status ON public.transactions USING btree (status);


--
-- TOC entry 5375 (class 1259 OID 27028)
-- Name: ix_transactions_transaction_type; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_transactions_transaction_type ON public.transactions USING btree (transaction_type);


--
-- TOC entry 5269 (class 1259 OID 26502)
-- Name: ix_user_sessions_user_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_user_sessions_user_id ON public.user_sessions USING btree (user_id);


--
-- TOC entry 5173 (class 1259 OID 26060)
-- Name: ix_users_email; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_users_email ON public.users USING btree (email);


--
-- TOC entry 5174 (class 1259 OID 26059)
-- Name: ix_users_is_active; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_users_is_active ON public.users USING btree (is_active);


--
-- TOC entry 5322 (class 1259 OID 26770)
-- Name: ix_wishlist_items_product_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_wishlist_items_product_id ON public.wishlist_items USING btree (product_id);


--
-- TOC entry 5323 (class 1259 OID 26771)
-- Name: ix_wishlist_items_wishlist_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_wishlist_items_wishlist_id ON public.wishlist_items USING btree (wishlist_id);


--
-- TOC entry 5232 (class 1259 OID 26327)
-- Name: ix_wishlists_user_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_wishlists_user_id ON public.wishlists USING btree (user_id);


--
-- TOC entry 5399 (class 2606 OID 26454)
-- Name: activity_logs activity_logs_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.activity_logs
    ADD CONSTRAINT activity_logs_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE SET NULL;


--
-- TOC entry 5382 (class 2606 OID 26092)
-- Name: addresses addresses_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.addresses
    ADD CONSTRAINT addresses_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- TOC entry 5383 (class 2606 OID 26113)
-- Name: admin_logs admin_logs_admin_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.admin_logs
    ADD CONSTRAINT admin_logs_admin_user_id_fkey FOREIGN KEY (admin_user_id) REFERENCES public.users(id) ON DELETE SET NULL;


--
-- TOC entry 5396 (class 2606 OID 26389)
-- Name: admins admins_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.admins
    ADD CONSTRAINT admins_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- TOC entry 5398 (class 2606 OID 26432)
-- Name: audit_logs audit_logs_actor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.audit_logs
    ADD CONSTRAINT audit_logs_actor_id_fkey FOREIGN KEY (actor_id) REFERENCES public.users(id) ON DELETE SET NULL;


--
-- TOC entry 5417 (class 2606 OID 26734)
-- Name: cart_items cart_items_cart_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cart_items
    ADD CONSTRAINT cart_items_cart_id_fkey FOREIGN KEY (cart_id) REFERENCES public.carts(id) ON DELETE CASCADE;


--
-- TOC entry 5418 (class 2606 OID 26739)
-- Name: cart_items cart_items_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cart_items
    ADD CONSTRAINT cart_items_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.products(id) ON DELETE CASCADE;


--
-- TOC entry 5392 (class 2606 OID 26302)
-- Name: carts carts_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.carts
    ADD CONSTRAINT carts_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- TOC entry 5381 (class 2606 OID 25996)
-- Name: categories categories_parent_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.categories
    ADD CONSTRAINT categories_parent_id_fkey FOREIGN KEY (parent_id) REFERENCES public.categories(id) ON DELETE SET NULL;


--
-- TOC entry 5426 (class 2606 OID 26877)
-- Name: coupon_usages coupon_usages_coupon_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.coupon_usages
    ADD CONSTRAINT coupon_usages_coupon_id_fkey FOREIGN KEY (coupon_id) REFERENCES public.coupons(id) ON DELETE CASCADE;


--
-- TOC entry 5427 (class 2606 OID 26887)
-- Name: coupon_usages coupon_usages_order_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.coupon_usages
    ADD CONSTRAINT coupon_usages_order_id_fkey FOREIGN KEY (order_id) REFERENCES public.orders(id) ON DELETE CASCADE;


--
-- TOC entry 5428 (class 2606 OID 26882)
-- Name: coupon_usages coupon_usages_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.coupon_usages
    ADD CONSTRAINT coupon_usages_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- TOC entry 5391 (class 2606 OID 26282)
-- Name: email_verification_tokens email_verification_tokens_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.email_verification_tokens
    ADD CONSTRAINT email_verification_tokens_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- TOC entry 5431 (class 2606 OID 26940)
-- Name: inventory inventory_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.inventory
    ADD CONSTRAINT inventory_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.products(id) ON DELETE CASCADE;


--
-- TOC entry 5397 (class 2606 OID 26412)
-- Name: notification_preferences notification_preferences_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.notification_preferences
    ADD CONSTRAINT notification_preferences_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- TOC entry 5394 (class 2606 OID 26345)
-- Name: notifications notifications_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.notifications
    ADD CONSTRAINT notifications_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- TOC entry 5389 (class 2606 OID 26240)
-- Name: oauth_accounts oauth_accounts_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.oauth_accounts
    ADD CONSTRAINT oauth_accounts_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- TOC entry 5432 (class 2606 OID 26963)
-- Name: order_items order_items_order_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.order_items
    ADD CONSTRAINT order_items_order_id_fkey FOREIGN KEY (order_id) REFERENCES public.orders(id) ON DELETE CASCADE;


--
-- TOC entry 5433 (class 2606 OID 26968)
-- Name: order_items order_items_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.order_items
    ADD CONSTRAINT order_items_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.products(id) ON DELETE RESTRICT;


--
-- TOC entry 5407 (class 2606 OID 26569)
-- Name: orders orders_shipping_address_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_shipping_address_id_fkey FOREIGN KEY (shipping_address_id) REFERENCES public.addresses(id) ON DELETE SET NULL;


--
-- TOC entry 5408 (class 2606 OID 26564)
-- Name: orders orders_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- TOC entry 5390 (class 2606 OID 26260)
-- Name: password_reset_tokens password_reset_tokens_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.password_reset_tokens
    ADD CONSTRAINT password_reset_tokens_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- TOC entry 5425 (class 2606 OID 26853)
-- Name: payments payments_order_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.payments
    ADD CONSTRAINT payments_order_id_fkey FOREIGN KEY (order_id) REFERENCES public.orders(id) ON DELETE CASCADE;


--
-- TOC entry 5387 (class 2606 OID 26193)
-- Name: personalization_data personalization_data_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.personalization_data
    ADD CONSTRAINT personalization_data_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- TOC entry 5423 (class 2606 OID 26834)
-- Name: product_categories product_categories_category_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.product_categories
    ADD CONSTRAINT product_categories_category_id_fkey FOREIGN KEY (category_id) REFERENCES public.categories(id) ON DELETE CASCADE;


--
-- TOC entry 5424 (class 2606 OID 26829)
-- Name: product_categories product_categories_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.product_categories
    ADD CONSTRAINT product_categories_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.products(id) ON DELETE CASCADE;


--
-- TOC entry 5421 (class 2606 OID 26788)
-- Name: product_images product_images_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.product_images
    ADD CONSTRAINT product_images_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.products(id) ON DELETE CASCADE;


--
-- TOC entry 5422 (class 2606 OID 26813)
-- Name: product_variants product_variants_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.product_variants
    ADD CONSTRAINT product_variants_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.products(id) ON DELETE CASCADE;


--
-- TOC entry 5404 (class 2606 OID 26532)
-- Name: products products_brand_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_brand_id_fkey FOREIGN KEY (brand_id) REFERENCES public.brands(id) ON DELETE SET NULL;


--
-- TOC entry 5405 (class 2606 OID 26527)
-- Name: products products_category_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_category_id_fkey FOREIGN KEY (category_id) REFERENCES public.categories(id) ON DELETE SET NULL;


--
-- TOC entry 5406 (class 2606 OID 26522)
-- Name: products products_seller_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_seller_id_fkey FOREIGN KEY (seller_id) REFERENCES public.sellers(id) ON DELETE CASCADE;


--
-- TOC entry 5413 (class 2606 OID 26684)
-- Name: recommendation_scores recommendation_scores_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.recommendation_scores
    ADD CONSTRAINT recommendation_scores_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.products(id) ON DELETE CASCADE;


--
-- TOC entry 5414 (class 2606 OID 26679)
-- Name: recommendation_scores recommendation_scores_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.recommendation_scores
    ADD CONSTRAINT recommendation_scores_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- TOC entry 5388 (class 2606 OID 26215)
-- Name: refresh_tokens refresh_tokens_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.refresh_tokens
    ADD CONSTRAINT refresh_tokens_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- TOC entry 5384 (class 2606 OID 26139)
-- Name: reports reports_reporter_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reports
    ADD CONSTRAINT reports_reporter_id_fkey FOREIGN KEY (reporter_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- TOC entry 5429 (class 2606 OID 26911)
-- Name: returns returns_order_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.returns
    ADD CONSTRAINT returns_order_id_fkey FOREIGN KEY (order_id) REFERENCES public.orders(id) ON DELETE CASCADE;


--
-- TOC entry 5430 (class 2606 OID 26916)
-- Name: returns returns_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.returns
    ADD CONSTRAINT returns_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- TOC entry 5437 (class 2606 OID 27045)
-- Name: review_images review_images_review_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.review_images
    ADD CONSTRAINT review_images_review_id_fkey FOREIGN KEY (review_id) REFERENCES public.reviews(id) ON DELETE CASCADE;


--
-- TOC entry 5434 (class 2606 OID 26997)
-- Name: reviews reviews_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reviews
    ADD CONSTRAINT reviews_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.products(id) ON DELETE CASCADE;


--
-- TOC entry 5435 (class 2606 OID 26992)
-- Name: reviews reviews_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reviews
    ADD CONSTRAINT reviews_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- TOC entry 5415 (class 2606 OID 26711)
-- Name: search_analytics search_analytics_clicked_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.search_analytics
    ADD CONSTRAINT search_analytics_clicked_product_id_fkey FOREIGN KEY (clicked_product_id) REFERENCES public.products(id) ON DELETE SET NULL;


--
-- TOC entry 5416 (class 2606 OID 26706)
-- Name: search_analytics search_analytics_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.search_analytics
    ADD CONSTRAINT search_analytics_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE SET NULL;


--
-- TOC entry 5409 (class 2606 OID 26593)
-- Name: seller_documents seller_documents_seller_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.seller_documents
    ADD CONSTRAINT seller_documents_seller_id_fkey FOREIGN KEY (seller_id) REFERENCES public.sellers(id) ON DELETE CASCADE;


--
-- TOC entry 5410 (class 2606 OID 26615)
-- Name: seller_payouts seller_payouts_seller_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.seller_payouts
    ADD CONSTRAINT seller_payouts_seller_id_fkey FOREIGN KEY (seller_id) REFERENCES public.sellers(id) ON DELETE CASCADE;


--
-- TOC entry 5412 (class 2606 OID 26657)
-- Name: seller_settings seller_settings_seller_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.seller_settings
    ADD CONSTRAINT seller_settings_seller_id_fkey FOREIGN KEY (seller_id) REFERENCES public.sellers(id) ON DELETE CASCADE;


--
-- TOC entry 5411 (class 2606 OID 26637)
-- Name: seller_wallets seller_wallets_seller_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.seller_wallets
    ADD CONSTRAINT seller_wallets_seller_id_fkey FOREIGN KEY (seller_id) REFERENCES public.sellers(id) ON DELETE CASCADE;


--
-- TOC entry 5395 (class 2606 OID 26369)
-- Name: sellers sellers_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sellers
    ADD CONSTRAINT sellers_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- TOC entry 5385 (class 2606 OID 26169)
-- Name: support_tickets support_tickets_assigned_to_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.support_tickets
    ADD CONSTRAINT support_tickets_assigned_to_id_fkey FOREIGN KEY (assigned_to_id) REFERENCES public.users(id) ON DELETE SET NULL;


--
-- TOC entry 5386 (class 2606 OID 26164)
-- Name: support_tickets support_tickets_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.support_tickets
    ADD CONSTRAINT support_tickets_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- TOC entry 5436 (class 2606 OID 27021)
-- Name: transactions transactions_order_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.transactions
    ADD CONSTRAINT transactions_order_id_fkey FOREIGN KEY (order_id) REFERENCES public.orders(id) ON DELETE SET NULL;


--
-- TOC entry 5400 (class 2606 OID 26473)
-- Name: user_roles user_roles_role_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_roles
    ADD CONSTRAINT user_roles_role_id_fkey FOREIGN KEY (role_id) REFERENCES public.roles(id) ON DELETE CASCADE;


--
-- TOC entry 5401 (class 2606 OID 26468)
-- Name: user_roles user_roles_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_roles
    ADD CONSTRAINT user_roles_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- TOC entry 5402 (class 2606 OID 26497)
-- Name: user_sessions user_sessions_refresh_token_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_sessions
    ADD CONSTRAINT user_sessions_refresh_token_id_fkey FOREIGN KEY (refresh_token_id) REFERENCES public.refresh_tokens(id) ON DELETE SET NULL;


--
-- TOC entry 5403 (class 2606 OID 26492)
-- Name: user_sessions user_sessions_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_sessions
    ADD CONSTRAINT user_sessions_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- TOC entry 5419 (class 2606 OID 26765)
-- Name: wishlist_items wishlist_items_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.wishlist_items
    ADD CONSTRAINT wishlist_items_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.products(id) ON DELETE CASCADE;


--
-- TOC entry 5420 (class 2606 OID 26760)
-- Name: wishlist_items wishlist_items_wishlist_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.wishlist_items
    ADD CONSTRAINT wishlist_items_wishlist_id_fkey FOREIGN KEY (wishlist_id) REFERENCES public.wishlists(id) ON DELETE CASCADE;


--
-- TOC entry 5393 (class 2606 OID 26322)
-- Name: wishlists wishlists_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.wishlists
    ADD CONSTRAINT wishlists_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


-- Completed on 2026-05-19 10:19:08

--
-- PostgreSQL database dump complete
--

\unrestrict tDOwR4vG68lm2oSNMKhrmCwdtTTnvqFrtOoL1tzd5phB2WC9MlRQTXHdYDoUEKc

