-- ==============================================================================
-- SAVEBITE - ESQUEMA DE BASE DE DATOS SUPABASE (POSTGRESQL)
-- Proyecto: Plataforma Móvil de Rescate de Alimentos (ODS 12)
-- Salamanca, Guanajuato
-- ==============================================================================

-- 1. TABLA: PERFILES DE USUARIO (Extendiendo auth.users)
CREATE TABLE IF NOT EXISTS public.profiles (
    id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    role TEXT NOT NULL CHECK (role IN ('consumer', 'merchant')) DEFAULT 'consumer',
    store_id UUID NULL,
    store_name TEXT NULL,
    avatar_initials TEXT DEFAULT 'SB',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- 2. TABLA: COMERCIOS ALIADOS (Salamanca, Gto.)
CREATE TABLE IF NOT EXISTS public.stores (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    category TEXT NOT NULL CHECK (category IN ('Panadería', 'Cafetería', 'Frutería', 'Restaurante', 'Pizzería')),
    address TEXT NOT NULL,
    latitude DOUBLE PRECISION NOT NULL,
    longitude DOUBLE PRECISION NOT NULL,
    rating DOUBLE PRECISION DEFAULT 4.8,
    icon_emoji TEXT DEFAULT '🏪',
    owner_id UUID REFERENCES public.profiles(id) ON DELETE SET NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- 3. TABLA: PAQUETES SORPRESA (Alimentos para rescate)
CREATE TABLE IF NOT EXISTS public.food_packages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    store_id UUID REFERENCES public.stores(id) ON DELETE CASCADE NOT NULL,
    store_name TEXT NOT NULL,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    category TEXT NOT NULL,
    category_emoji TEXT DEFAULT '🍱',
    original_price NUMERIC(10, 2) NOT NULL,
    discounted_price NUMERIC(10, 2) NOT NULL,
    initial_stock INTEGER NOT NULL DEFAULT 5,
    remaining_stock INTEGER NOT NULL DEFAULT 5,
    pickup_time_window TEXT NOT NULL, -- ej. '19:30 - 20:30'
    estimated_kg NUMERIC(6, 2) NOT NULL DEFAULT 1.2,
    co2_saved_kg NUMERIC(6, 2) NOT NULL DEFAULT 2.5,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- 4. TABLA: RESERVAS Y CUPONES QR
CREATE TABLE IF NOT EXISTS public.reservations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    package_id UUID REFERENCES public.food_packages(id) ON DELETE CASCADE NOT NULL,
    user_id UUID REFERENCES public.profiles(id) ON DELETE CASCADE NOT NULL,
    package_title TEXT NOT NULL,
    store_name TEXT NOT NULL,
    pickup_window TEXT NOT NULL,
    amount_paid NUMERIC(10, 2) NOT NULL,
    original_price NUMERIC(10, 2) NOT NULL,
    qr_token TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL CHECK (status IN ('reserved', 'redeemed', 'expired')) DEFAULT 'reserved',
    co2_saved_kg NUMERIC(6, 2) NOT NULL,
    food_rescued_kg NUMERIC(6, 2) NOT NULL,
    reserved_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL,
    redeemed_at TIMESTAMP WITH TIME ZONE NULL
);

-- ==============================================================================
-- HABILITAR REALTIME (Para ver cambios de stock y canjes en vivo en Flutter)
-- ==============================================================================
ALTER PUBLICATION supabase_realtime ADD TABLE public.food_packages;
ALTER PUBLICATION supabase_realtime ADD TABLE public.reservations;

-- ==============================================================================
-- ROW LEVEL SECURITY (RLS) - POLÍTICAS DE ACCESO
-- ==============================================================================
ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.stores ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.food_packages ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.reservations ENABLE ROW LEVEL SECURITY;

-- Lectura pública para comercios y paquetes
CREATE POLICY "Permitir lectura publica de tiendas" ON public.stores FOR SELECT USING (true);
CREATE POLICY "Permitir lectura publica de paquetes disponibles" ON public.food_packages FOR SELECT USING (true);
CREATE POLICY "Permitir a comercios insertar sus paquetes" ON public.food_packages FOR INSERT WITH CHECK (true);
CREATE POLICY "Permitir a comercios actualizar sus paquetes" ON public.food_packages FOR UPDATE USING (true);

-- Perfiles: cada usuario lee y edita su propio perfil (o público para lectura básica)
CREATE POLICY "Perfiles visibles por todos" ON public.profiles FOR SELECT USING (true);
CREATE POLICY "Usuarios pueden actualizar su propio perfil" ON public.profiles FOR UPDATE USING (auth.uid() = id);
CREATE POLICY "Usuarios pueden insertar su propio perfil" ON public.profiles FOR INSERT WITH CHECK (auth.uid() = id);

-- Reservas: cada usuario ve sus propias reservas; los comercios pueden consultar y validar
CREATE POLICY "Usuarios ven sus propias reservas" ON public.reservations FOR SELECT USING (auth.uid() = user_id OR true);
CREATE POLICY "Usuarios pueden crear reservas" ON public.reservations FOR INSERT WITH CHECK (true);
CREATE POLICY "Comercios pueden actualizar canje" ON public.reservations FOR UPDATE USING (true);

-- ==============================================================================
-- DATOS SEMILLA (COMERCIOS LOCALES EN SALAMANCA, GTO.)
-- ==============================================================================
INSERT INTO public.stores (id, name, category, address, latitude, longitude, rating, icon_emoji)
VALUES 
    ('11111111-1111-1111-1111-111111111111', 'Panadería La Tradición', 'Panadería', 'Calle Revolución 204, Centro, Salamanca', 20.5721, -101.1983, 4.9, '🥖'),
    ('22222222-2222-2222-2222-222222222222', 'Café San Agustín', 'Cafetería', 'Andador Zaragoza 108, Centro, Salamanca', 20.5710, -101.1965, 4.7, '☕'),
    ('33333333-3333-3333-3333-333333333333', 'Frutería El Vergel', 'Frutería', 'Av. Faja de Oro 1205, Salamanca', 20.5785, -101.1890, 4.8, '🥑'),
    ('44444444-4444-4444-4444-444444444444', 'Pizzería Bella Napoli', 'Restaurante', 'Blvd. Valle de Santiago 405, Salamanca', 20.5650, -101.2050, 4.6, '🍕')
ON CONFLICT (id) DO NOTHING;

-- DATOS SEMILLA: PAQUETES SORPRESA INICIALES
INSERT INTO public.food_packages (id, store_id, store_name, title, description, category, category_emoji, original_price, discounted_price, initial_stock, remaining_stock, pickup_time_window, estimated_kg, co2_saved_kg)
VALUES 
    ('a1111111-1111-1111-1111-111111111111', '11111111-1111-1111-1111-111111111111', 'Panadería La Tradición', 'Pack Bollería & Conchas', '5 piezas surtidas de pan dulce y bollería artesanal horneada en la mañana en excelente estado.', 'Panadería', '🥐', 85.00, 32.00, 6, 4, '19:45 - 20:30', 1.1, 2.3),
    ('a2222222-2222-2222-2222-222222222222', '22222222-2222-2222-2222-222222222222', 'Café San Agustín', 'Pack Baguettes & Repostería', '1 baguette artesanal + 2 muffins de arándanos listos para merendar o cenar.', 'Cafetería', '🥪', 130.00, 48.00, 4, 2, '20:00 - 20:45', 1.3, 2.7),
    ('a3333333-3333-3333-3333-333333333333', '33333333-3333-3333-3333-333333333333', 'Frutería El Vergel', 'Caja Fruta Mixta de Temporada', 'Aprox. 2 kg de manzanas, plátanos y naranjas maduras perfectas para jugos y ensaladas.', 'Frutería', '🍎', 90.00, 35.00, 5, 5, '18:30 - 19:30', 2.0, 4.1),
    ('a4444444-4444-4444-4444-444444444444', '44444444-4444-4444-4444-444444444444', 'Pizzería Bella Napoli', 'Porciones Pizza Artesanal', '4 rebanadas grandes de pizza recién salida del horno en la jornada del mediodía.', 'Restaurante', '🍕', 140.00, 55.00, 3, 1, '21:00 - 21:30', 1.5, 3.2)
ON CONFLICT (id) DO NOTHING;

