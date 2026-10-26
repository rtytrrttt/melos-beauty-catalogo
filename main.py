import streamlit as st
import pandas as pd
import datetime
import json
import os
import base64
import urllib.parse

# ---------------------------------------------------------
# IMÁGENES DEFAULT (BASE64 PLACEHOLDERS)
# ---------------------------------------------------------
MELO1_DEFAULT = "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAP//////////////////////////////////////////////////////////////////////////////////////wgALCAABAAEBAREA/8QAFBABAAAAAAAAAAAAAAAAAAAAAP/aAAgBAQABPxA="
MELO2_DEFAULT = "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAP//////////////////////////////////////////////////////////////////////////////////////wgALCAABAAEBAREA/8QAFBABAAAAAAAAAAAAAAAAAAAAAP/aAAgBAQABPxA="

# ---------------------------------------------------------
# CONFIGURACIÓN DE PÁGINA Y ESTILOS (Melo's Beauty)
# ---------------------------------------------------------
st.set_page_config(
    page_title="Melo's Beauty 🌸 Catálogo & Tienda",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS con sintaxis corregida (llaves dobles {{ }} para CSS)
STYLING_CSS = f"""
<style>
/* Fondo general con marca de agua melo2.jpeg */
.stApp {{
    background: linear-gradient(rgba(255, 245, 247, 0.92), rgba(255, 245, 247, 0.92)), url("{MELO2_DEFAULT}") repeat center center fixed;
    background-size: cover;
    color: #2C2C2C;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}}

#MainMenu {{visibility: hidden;}}
footer {{visibility: hidden;}}

/* Header Banner Hero */
.hero-banner {{
    background: linear-gradient(135deg, #F8B8CC 0%, #F06292 100%);
    padding: 2.2rem;
    border-radius: 24px;
    text-align: center;
    color: white;
    border: 2px solid #F06292;
    margin-bottom: 2rem;
    box-shadow: 0px 8px 20px rgba(240, 98, 146, 0.25);
}}
.hero-title {{
    color: #FFFFFF;
    font-size: 2.6rem;
    font-weight: 800;
    margin-bottom: 0.3rem;
}}
.hero-subtitle {{
    color: #FFF0F5;
    font-size: 1.25rem;
    font-style: italic;
}}
.hero-tag {{
    background-color: rgba(255, 255, 255, 0.28);
    display: inline-block;
    padding: 6px 18px;
    border-radius: 30px;
    font-weight: 600;
    margin-top: 10px;
    color: #FFFFFF;
}}

/* Tarjetas de Producto Limpias */
.product-card {{
    background-color: #FFFFFF;
    border: 2px solid #F8B8CC;
    border-radius: 18px;
    padding: 1.1rem;
    margin-bottom: 1rem;
    box-shadow: 0px 6px 16px rgba(248, 184, 204, 0.2);
}}
.product-title {{
    color: #C2185B;
    font-size: 1.2rem;
    font-weight: 700;
    margin-top: 6px;
}}
.product-price {{
    color: #C2185B;
    font-size: 1.35rem;
    font-weight: 800;
    margin-top: 4px;
}}
.product-img-container {{
    width: 100%;
    height: 180px;
    border-radius: 14px;
    background-color: #FFF0F3;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    border: 1px solid #F8B8CC;
}}
.product-img {{
    width: 100%;
    height: 100%;
    object-fit: cover;
}}

/* Badges de inventario */
.stock-badge-green {{
    background-color: #E8F5E9;
    color: #2E7D32;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.82rem;
    font-weight: 700;
    display: inline-block;
}}
.stock-badge-red {{
    background-color: #FFEBEE;
    color: #C62828;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.82rem;
    font-weight: 700;
    display: inline-block;
}}

/* Botones y Estilos de Carrito */
.btn-whatsapp-direct {{
    background-color: #25D366;
    color: white !important;
    padding: 12px 20px;
    border-radius: 30px;
    text-decoration: none;
    font-weight: bold;
    display: block;
    text-align: center;
    font-size: 1.05rem;
    box-shadow: 0px 4px 12px rgba(37, 211, 102, 0.35);
    margin-top: 15px;
}}
.btn-whatsapp-direct:hover {{
    background-color: #1EBE57;
    color: white !important;
}}

/* Botones primarios en Streamlit */
.stButton>button {{
    background-color: #F06292;
    color: white;
    border-radius: 20px;
    border: none;
    font-weight: bold;
    transition: all 0.3s ease;
}}
.stButton>button:hover {{
    background-color: #C2185B;
    color: white;
}}

/* Contenedor de Factura */
.factura-box {{
    background-color: #FFFFFF;
    border: 2px dashed #F06292;
    border-radius: 16px;
    padding: 1.5rem;
    font-family: 'Courier New', Courier, monospace;
    color: #222;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.05);
}}
</style>
"""
st.markdown(STYLING_CSS, unsafe_allow_html=True)

# ---------------------------------------------------------
# PERSISTENCIA DE DATOS (JSON + SESSION STATE)
# ---------------------------------------------------------
DATA_FILE = 'catalogo_melos_data.json'

def get_default_data():
    return {
        'pin_secret': '1234',
        'cover_info': {
            'title': "Melo's Beauty 🌸",
            'slogan': 'La magia que resalta tu brillo diario ✨',
            'location': 'Tienda virtual de maquillaje y accesorios en Buenaventura 🎀',
            'phone': '+57 312 569 1563',
            'hero_img_b64': MELO1_DEFAULT,
            'bg_img_b64': MELO2_DEFAULT
        },
        'categories': {
            "Kits Melo's beauty": {'desc': 'Combinaciones especiales para armar tu kit de belleza diario.', 'img_b64': None},
            'Billeteras mujeres': {'desc': 'Billeteras elegantes con múltiples compartimentos.', 'img_b64': None},
            'Billeteras hombres': {'desc': 'Billeteras masculinas con grabado clásico.', 'img_b64': None},
            'Termos': {'desc': 'Termos térmicos de 1 litro para conservar tus bebidas.', 'img_b64': None},
            'Accesorios': {'desc': 'Accesorios únicos para complementar tu look diario.', 'img_b64': None},
            'Joyeros': {'desc': 'Organizadores elegantes para tus joyas.', 'img_b64': None},
            'Pantuflas': {'desc': 'Pantuflas ultra suaves para descansar.', 'img_b64': None},
            'Perfumes': {'desc': 'Fragancias exclusivas con aromas perdurables.', 'img_b64': None}
        },
        'products': [
            {'id': 101, 'sku': 'TERMO-1L-001', 'name': 'Termo térmico 1 litro', 'category': 'Termos', 'price': 88700, 'stock': 12, 'desc': 'Termo térmico de 1 Litro en tonos rosados suaves.', 'img_b64': None},
            {'id': 102, 'sku': 'KIT-CANDY-PURPURE', 'name': 'Kit Candy Bum Purpure', 'category': "Kits Melo's beauty", 'price': 47400, 'stock': 8, 'desc': 'Kit especial con brillo labial, bálsamo y accesorios.', 'img_b64': None},
            {'id': 103, 'sku': 'KIT-MELOSBEAUTY-003', 'name': "Kit Melo's beauty 3", 'category': "Kits Melo's beauty", 'price': 67000, 'stock': 5, 'desc': 'Trío de cosméticos esenciales para el día a día.', 'img_b64': None},
            {'id': 104, 'sku': 'KIT-MELOSBEAUTY-002', 'name': "Kit Melo's beauty 2", 'category': "Kits Melo's beauty", 'price': 80700, 'stock': 3, 'desc': 'Kit intermedio con sombra de ojos e iluminador.', 'img_b64': None},
            {'id': 105, 'sku': 'KIT-MELOSBEAUTY-001', 'name': "Kit Melo's beauty 1", 'category': "Kits Melo's beauty", 'price': 94000, 'stock': 10, 'desc': 'El kit más completo con cosmetiquera de regalo.', 'img_b64': None},
            {'id': 106, 'sku': 'BIL-BIMBA-001', 'name': 'Billetera Bimba y Lola 1.1', 'category': 'Billeteras mujeres', 'price': 65900, 'stock': 6, 'desc': 'Billetera estilo 1.1 en tono rosa pastel.', 'img_b64': None},
            {'id': 107, 'sku': 'BIL-LACOSTE-001', 'name': 'Billetera Lacoste hombre 1.1', 'category': 'Billeteras hombres', 'price': 73700, 'stock': 4, 'desc': 'Billetera masculina elegante en cuerina premium.', 'img_b64': None}
        ],
        'reviews': [
            {'id': 1, 'client': 'Camila R.', 'rating': '⭐⭐⭐⭐⭐', 'comment': "Me encantó el Kit Melo's Beauty 1. Excelente servicio en Buenaventura.", 'date': '2026-10-15'},
            {'id': 2, 'client': 'Valeria M.', 'rating': '⭐⭐⭐⭐⭐', 'comment': 'El termo térmico de 1L mantiene el agua fría todo el día.', 'date': '2026-10-18'}
        ]
    }

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                d = json.load(f)
                if 'cover_info' not in d: d['cover_info'] = get_default_data()['cover_info']
                if not d['cover_info'].get('hero_img_b64'): d['cover_info']['hero_img_b64'] = MELO1_DEFAULT
                if not d['cover_info'].get('bg_img_b64'): d['cover_info']['bg_img_b64'] = MELO2_DEFAULT
                return d
        except Exception:
            return get_default_data()
    else:
        d = get_default_data()
        save_data(d)
        return d

def save_data(data):
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        st.error(f"Error guardando datos: {e}")

def file_to_b64(uploaded_file):
    if uploaded_file is None:
        return None
    try:
        return f"data:image/jpeg;base64,{base64.b64encode(uploaded_file.getvalue()).decode('utf-8')}"
    except Exception:
        return None

# Inicialización en Session State
if 'app_data' not in st.session_state:
    st.session_state.app_data = load_data()

if 'cart' not in st.session_state:
    st.session_state.cart = {}  # {prod_id: cant}

if 'admin_auth' not in st.session_state:
    st.session_state.admin_auth = False

app_data = st.session_state.app_data

# Calcular items totales en carrito
cart_total_units = sum(st.session_state.cart.values())

# ---------------------------------------------------------
# BARRA LATERAL (NAVEGACIÓN & CONTACTO)
# ---------------------------------------------------------
st.sidebar.title("Melo's Beauty 🌸")
mode = st.sidebar.radio(
    "Navegación principal:",
    [
        "🛍️ Catálogo Clientes",
        f"🛒 Mi Carrito / Factura ({cart_total_units})",
        "🔐 Acceso Dueño / Admin"
    ]
)
st.sidebar.markdown("---")
st.sidebar.subheader("Redes Sociales & Contacto")
phone_clean = app_data['cover_info'].get('phone', '+57 312 569 1563').replace('+', '').replace(' ', '')
st.sidebar.markdown(f"💬 **WhatsApp**: {app_data['cover_info'].get('phone', '+57 312 569 1563')}")
st.sidebar.markdown("📸 **Instagram**: @melosbeauty_oficial")
st.sidebar.markdown("📘 **Facebook**: Melo Beauty Buenaventura")

# ---------------------------------------------------------
# MODO 1: CATÁLOGO CLIENTES (VISTA LIMPIA Y RÁPIDA)
# ---------------------------------------------------------
if mode == "🛍️ Catálogo Clientes":
    # Banner de Portada Hero
    hero_b64 = app_data['cover_info'].get('hero_img_b64') or MELO1_DEFAULT
    st.markdown(
        f"""
        <div style="text-align:center; margin-bottom:1.5rem;">
            <img src="{hero_b64}" style="width:100%; max-height:280px; object-fit:cover; border-radius:24px; border:3px solid #F06292; box-shadow: 0px 8px 20px rgba(240, 98, 146, 0.25);">
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="hero-banner">
            <div class="hero-title">{app_data['cover_info']['title']}</div>
            <div class="hero-subtitle">{app_data['cover_info']['slogan']}</div>
            <div class="hero-tag">📍 {app_data['cover_info']['location']}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Barra de Carrito Rápido si hay items
    if cart_total_units > 0:
        cart_total_price = 0
        for p_id, qty in st.session_state.cart.items():
            p_match = next((p for p in app_data['products'] if p.get('id') == p_id), None)
            if p_match:
                cart_total_price += p_match.get('price', 0) * qty
        
        st.success(f"🛒 **Carrito Actual**: {cart_total_units} productos seleccionados | **Total**: COP {cart_total_price:,.0f} — Ve a la pestaña '🛒 Mi Carrito' en la barra lateral para generar tu factura con tus datos.")

    # Filtros de búsqueda y categoría
    col_s, col_c = st.columns(2)
    with col_s:
        q = st.text_input("🔍 Buscar en el catálogo:", placeholder="Ej: Kit, Termo, Billetera...")
    with col_c:
        cat_options = ["Todas"] + list(app_data['categories'].keys())
        cat = st.selectbox("🗂️ Categoría:", cat_options)
        
    if cat != "Todas" and cat in app_data['categories']:
        cat_info = app_data['categories'][cat]
        st.markdown(f"### 📂 Categoría: {cat}")
        cd, ci = st.columns([3, 1])
        with cd:
            st.info(f"**Descripción**: {cat_info.get('desc', '')}")
        with ci:
            if cat_info.get('img_b64'):
                st.image(cat_info['img_b64'], caption=f"Perfil {cat}", use_container_width=True)
    st.markdown("---")

    # Filtrar productos
    prods = app_data['products']
    if cat != "Todas":
        prods = [p for p in prods if p.get('category') == cat]
    if q:
        prods = [p for p in prods if q.lower() in p.get('name', '').lower() or q.lower() in p.get('desc', '').lower()]
        
    st.subheader(f"✨ Productos Disponibles ({len(prods)})")

    if not prods:
        st.info("No hay productos disponibles para esta búsqueda o categoría.")
    else:
        cols = st.columns(3)
        for idx, p in enumerate(prods):
            p_id = p.get('id')
            p_name = p.get('name', 'Producto Melo')
            p_price = p.get('price', 0)
            p_stock = p.get('stock', 0)
            p_desc = p.get('desc', '')
            p_cat = p.get('category', '')
            p_img = p.get('img_b64')
            
            with cols[idx % 3]:
                if p_img:
                    img_html = f'<img src="{p_img}" class="product-img">'
                else:
                    img_html = f'<div style="text-align:center; font-size:2.2rem;">🛍️<br><span style="font-size:0.85rem; color:#C2185B;">{p_name}</span></div>'
                
                st.markdown(
                    f"""
                    <div class="product-card">
                        <div class="product-img-container">{img_html}</div>
                        <div class="product-title">{p_name}</div>
                        <div style="color:#666; font-size:0.85rem; margin-top:2px;">Categoría: <b>{p_cat}</b></div>
                        <p style="color:#444; font-size:0.88rem; margin-top:6px; height:40px; overflow:hidden;">{p_desc}</p>
                        <div class="product-price">COP {p_price:,.0f}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                
                # Indicador de stock
                if p_stock > 5:
                    st.markdown(f'<span class="stock-badge-green">✔ En Stock ({p_stock} disp.)</span>', unsafe_allow_html=True)
                elif p_stock > 0:
                    st.markdown(f'<span class="stock-badge-red">⚠️ ¡Pocas Unidades! ({p_stock})</span>', unsafe_allow_html=True)
                else:
                    st.error("❌ Agotado")
                
                # Botón de Agregar al Carrito
                in_cart_qty = st.session_state.cart.get(p_id, 0)
                
                if p_stock > 0:
                    if in_cart_qty == 0:
                        if st.button(f"➕ Agregar al Carrito", key=f"add_cart_main_{p_id}"):
                            st.session_state.cart[p_id] = 1
                            st.toast(f"¡{p_name} agregado al carrito! 🛒", icon="🛍️")
                            st.rerun()
                    else:
                        st.markdown(f"**🛒 En tu carrito: {in_cart_qty} unids.**")
                        c_m, c_p = st.columns(2)
                        with c_m:
                            if st.button("➖ Quitar", key=f"sub_cart_main_{p_id}"):
                                if st.session_state.cart[p_id] > 1:
                                    st.session_state.cart[p_id] -= 1
                                else:
                                    del st.session_state.cart[p_id]
                                st.rerun()
                        with c_p:
                            if st.button("➕ Sumar", key=f"add_more_main_{p_id}"):
                                if st.session_state.cart[p_id] < p_stock:
                                    st.session_state.cart[p_id] += 1
                                else:
                                    st.toast("Llegaste al límite de stock disponible", icon="⚠️")
                                st.rerun()
                else:
                    st.caption("No disponible temporalmente")
                
                st.markdown("<br>", unsafe_allow_html=True)

    # Reseñas de Clientes
    st.markdown("---")
    st.subheader("💬 Opiniones & Reseñas de Clientes")
    r1, r2 = st.columns([2, 1])
    with r1:
        revs = app_data.get('reviews', [])
        if not revs:
            st.info("Aún no hay reseñas publicadas. ¡Sé el primero en dejar tu opinión!")
        else:
            for rev in revs:
                r_name = rev.get('client', 'Cliente')
                r_rating = rev.get('rating', '⭐⭐⭐⭐⭐')
                r_date = rev.get('date', '')
                r_comment = rev.get('comment', '')
                st.markdown(
                    f"""
                    <div style="background-color:#FFFFFF; border:2px solid #F8B8CC; padding:1rem; border-radius:14px; margin-bottom:12px;">
                        <strong>{r_name}</strong> <span style="float:right;">{r_rating}</span><br>
                        <small style="color:#888;">{r_date}</small>
                        <p style="color:#2C2C2C; margin-top:6px; margin-bottom:0;">&ldquo;{r_comment}&rdquo;</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
    with r2:
        st.markdown("#### Publicar Reseña")
        nn = st.text_input("Tu Nombre:", key="rev_input_name")
        nr = st.selectbox("Calificación:", ["⭐⭐⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐", "⭐⭐", "⭐"], key="rev_input_star")
        nc = st.text_area("Comentario:", key="rev_input_comm")
        if st.button("Publicar Reseña", key="btn_pub_rev_client"):
            if nn and nc:
                new_rev_id = max([r.get('id', 0) for r in app_data.get('reviews', [])], default=0) + 1
                app_data['reviews'].append({
                    'id': new_rev_id,
                    'client': nn,
                    'rating': nr,
                    'comment': nc,
                    'date': datetime.date.today().strftime('%Y-%m-%d')
                })
                save_data(app_data)
                st.success("¡Gracias por tu reseña! Ha sido publicada.")
                st.rerun()
            else:
                st.warning("Escribe tu nombre y comentario.")

    st.markdown("---")
    with st.expander("🔒 Términos, Condiciones y Política de Datos"):
        st.write("""
        **Melo's Beauty - Buenaventura**
        - **Protección de Datos Personales**: Tus datos se utilizan únicamente para procesar y despachar tu pedido.
        - **Envíos**: Entregas en Buenaventura y envíos nacionales.
        - **Garantía**: Todos nuestros productos son verificados previamente.
        """)

# ---------------------------------------------------------
# MODO 2: MI CARRITO Y FACTURACIÓN CON DATOS PERSONALES
# ---------------------------------------------------------
elif "Mi Carrito" in mode:
    st.title("🛒 Mi Carrito y Generación de Factura")
    st.caption("Revisa tus productos e ingresa tus datos completos para enviar la factura por WhatsApp")

    if not st.session_state.cart:
        st.info("Tu carrito está vacío actualmente.")
        st.markdown("Explora nuestros productos y presiona **➕ Agregar al Carrito** para armar tu pedido.")
    else:
        st.subheader("1. Productos Seleccionados")
        cart_items_data = []
        total_factura = 0
        
        for p_id, qty in list(st.session_state.cart.items()):
            p_match = next((p for p in app_data['products'] if p.get('id') == p_id), None)
            if p_match:
                subt = p_match.get('price', 0) * qty
                total_factura += subt
                cart_items_data.append({
                    'id': p_id,
                    'sku': p_match.get('sku', f"SKU-{p_id}"),
                    'name': p_match.get('name', 'Producto'),
                    'price': p_match.get('price', 0),
                    'qty': qty,
                    'subtotal': subt
                })
        
        for item in cart_items_data:
            i_id = item['id']
            i_name = item['name']
            i_sku = item['sku']
            i_price = item['price']
            i_qty = item['qty']
            i_subt = item['subtotal']
            
            c_name, c_price, c_qty, c_sub, c_acts = st.columns([3, 1.5, 1.5, 1.5, 1.5])
            with c_name:
                st.markdown(f"**{i_name}**<br><small style='color:#888;'>SKU: {i_sku}</small>", unsafe_allow_html=True)
            with c_price:
                st.markdown(f"COP {i_price:,}")
            with c_qty:
                st.markdown(f"Cant: **{i_qty}**")
            with c_sub:
                st.markdown(f"**COP {i_subt:,}**")
            with c_acts:
                col_b1, col_b2 = st.columns(2)
                with col_b1:
                    if st.button("➕", key=f"cart_page_inc_{i_id}"):
                        st.session_state.cart[i_id] += 1
                        st.rerun()
                with col_b2:
                    if st.button("🗑️", key=f"cart_page_del_{i_id}"):
                        del st.session_state.cart[i_id]
                        st.rerun()
            st.markdown("<hr style='margin: 4px 0;'>", unsafe_allow_html=True)
            
        st.markdown(f"### 💰 **TOTAL DE LA FACTURA**: COP {total_factura:,.0f}")
        
        if st.button("🧹 Vaciar Carrito Completo", key="btn_empty_cart"):
            st.session_state.cart = {}
            st.rerun()
            
        st.markdown("---")
        st.subheader("2. Datos Personales para la Factura")
        st.caption("Ingresa tu información completa para generar la factura formal de compra")
        
        c_f1, c_f2 = st.columns(2)
        with c_f1:
            client_name = st.text_input("👤 Nombre Completo:", value="Nas murillo", key="fact_name")
            client_cedula = st.text_input("🪪 Cédula / NIT:", value="1085214789", key="fact_cedula")
            client_phone = st.text_input("📱 Celular / WhatsApp:", value="+573028081327", key="fact_phone")
        with c_f2:
            client_address = st.text_input("📍 Dirección de Entrega:", value="Calle 5 # 12-34, Barrio Pueblo Nuevo", key="fact_address")
            client_city = st.text_input("🏙️ Ciudad / Municipio:", value="Buenaventura, Valle", key="fact_city")
            client_payment = st.selectbox("💳 Método de Pago:", ["Nequi", "Bancolombia", "Efectivo contra entrega", "Bre-B"], key="fact_payment")
            
        client_notes = st.text_area("📝 Notas Adicionales / Indicaciones de Entrega:", value="Entregar en la tarde.", key="fact_notes")
        
        # Construcción del texto de la factura
        lines = []
        lines.append(f"Hola, soy {client_name},")
        lines.append("")
        s_domain = app_data["cover_info"].get("shop_url", "https://melos-beauty-catalogo-uwyau8ttti9kfmhywlvtlc.streamlit.app/").rstrip("/")
        o_code = ""
        lines.append(f"Link a mi pedido: {s_domain}{o_code}")
        lines.append("")
        lines.append("DATOS PARA LA FACTURA:")
        lines.append(f"• Nombre: {client_name}")
        lines.append(f"• Cédula/NIT: {client_cedula}")
        lines.append(f"• Celular: {client_phone}")
        lines.append(f"• Dirección: {client_address}")
        lines.append(f"• Ciudad: {client_city}")
        lines.append(f"• Método de Pago: {client_payment}")
        lines.append("")
        lines.append("==============================")
        lines.append("quiero hacer este pedido en Melo's beauty :")
        lines.append("")
        
        for item in cart_items_data:
            lines.append(f"• {item['qty']} *{item['name']}* [{item['sku']}] / COP {item['subtotal']:,}")
            
        lines.append("")
        lines.append("==============================")
        lines.append("")
        lines.append(f"Subtotal: COP {total_factura:,}")
        lines.append(f"TOTAL: COP {total_factura:,}")
        
        if client_notes:
            lines.append("")
            lines.append(f"Notas: {client_notes}")
            
        invoice_raw_text = "\n".join(lines)
        
        st.markdown("---")
        st.subheader("3. Vista Previa de tu Factura Formal")
        st.markdown(
            f"""
            <div class="factura-box">
                <pre style="white-space: pre-wrap; font-family: monospace; font-size: 0.92rem; margin: 0;">{invoice_raw_text}</pre>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        encoded_message = urllib.parse.quote(invoice_raw_text)
        target_phone = app_data['cover_info'].get('phone', '+573125691563').replace('+', '').replace(' ', '')
        wa_url = f"https://wa.me/{target_phone}?text={encoded_message}"
        
        st.markdown(
            f"""
            <a href="{wa_url}" target="_blank" class="btn-whatsapp-direct">
                📲 ENVIAR ESTA FACTURA POR WHATSAPP A MELO'S BEAUTY
            </a>
            """,
            unsafe_allow_html=True
        )

# ---------------------------------------------------------
# MODO 3: PANEL INTERNO DE ADMINISTRACIÓN (DUEÑO)
# ---------------------------------------------------------
else:
    st.title("🔐 Panel Interno de Administración (Exclusivo Dueño)")
    st.caption("Gestión completa de productos, stock, borrado de reseñas e imágenes")

    if not st.session_state.admin_auth:
        st.info("Para acceder ingresa la clave de la tienda.")
        p_in = st.text_input("Ingresa PIN Secreto:", type="password", key="pin_login_input")
        if st.button("Ingresar al Panel", key="btn_login_admin"):
            if p_in == app_data.get('pin_secret', '1234'):
                st.session_state.admin_auth = True
                st.success("¡Bienvenido al Panel de Control!")
                st.rerun()
            else:
                st.error("PIN incorrecto.")
    else:
        col_t, col_logout = st.columns([3, 1])
        with col_t:
            st.success("Sesión de Administrador Activa ✔️")
        with col_logout:
            if st.button("🔒 Cerrar Sesión Admin", key="btn_logout_admin"):
                st.session_state.admin_auth = False
                st.rerun()
                
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "📊 Stock & Inventario",
            "➕ Agregar Producto",
            "🗑️ Borrar Productos & Fotos",
            "💬 Administrar Reseñas",
            "🖼️ Portada & Fondo",
            "🔑 Configurar PIN"
        ])
        
        # TAB 1: STOCK & INVENTARIO
        with tab1:
            st.subheader("Control de Inventarios y Precios")
            df_prods = pd.DataFrame(app_data['products'])
            if not df_prods.empty:
                tot_val = (df_prods['price'] * df_prods['stock']).sum()
                m1, m2, m3 = st.columns(3)
                m1.metric("Total Productos", len(df_prods))
                m2.metric("Unidades en Stock", df_prods['stock'].sum())
                m3.metric("Valor del Inventario", f"COP {tot_val:,.0f}")
                
                st.markdown("---")
                st.dataframe(df_prods[['id', 'sku', 'name', 'category', 'price', 'stock', 'desc']], use_container_width=True)
                
                st.markdown("#### Modificar Stock / Precio de un Producto")
                col_p_sel, col_n_stk, col_n_prc = st.columns(3)
                with col_p_sel:
                    p_edit_id = st.selectbox(
                        "Selecciona Producto:",
                        [p['id'] for p in app_data['products']],
                        format_func=lambda x: f"ID {x} - {[p['name'] for p in app_data['products'] if p['id']==x][0]}",
                        key="sel_p_edit_stock"
                    )
                
                p_obj = next((p for p in app_data['products'] if p['id'] == p_edit_id), None)
                if p_obj:
                    with col_n_stk:
                        new_stk = st.number_input("Nuevo Stock:", min_value=0, value=int(p_obj.get('stock', 10)), key="in_stk_val")
                    with col_n_prc:
                        new_prc = st.number_input("Nuevo Precio (COP):", min_value=0, value=int(p_obj.get('price', 50000)), step=1000, key="in_prc_val")
                        
                    if st.button("💾 Guardar Cambios de Stock/Precio", key="btn_save_stock_prc"):
                        p_obj['stock'] = new_stk
                        p_obj['price'] = new_prc
                        save_data(app_data)
                        st.success(f"Stock/Precio de '{p_obj['name']}' actualizado correctamente.")
                        st.rerun()

        # TAB 2: AGREGAR PRODUCTO
        with tab2:
            st.subheader("➕ Publicar Nuevo Producto")
            with st.form("form_add_product"):
                np_name = st.text_input("Nombre del Producto:")
                np_sku = st.text_input("Código SKU / Referencia:", value="PROD-001")
                np_cat = st.selectbox("Categoría:", list(app_data['categories'].keys()))
                np_price = st.number_input("Precio (COP):", min_value=0, value=50000, step=1000)
                np_stock = st.number_input("Stock Inicial:", min_value=0, value=10)
                np_desc = st.text_area("Descripción detallada:")
                np_file = st.file_uploader("Subir Foto del Producto:", type=['jpg', 'png', 'jpeg', 'webp'])
                
                if st.form_submit_button("💾 Publicar Producto en Catálogo"):
                    if np_name and np_desc:
                        b64_img = file_to_b64(np_file)
                        new_id = max([p.get('id', 100) for p in app_data['products']], default=100) + 1
                        app_data['products'].append({
                            'id': new_id,
                            'sku': np_sku,
                            'name': np_name,
                            'category': np_cat,
                            'price': np_price,
                            'stock': np_stock,
                            'desc': np_desc,
                            'img_b64': b64_img
                        })
                        save_data(app_data)
                        st.success(f"¡Producto '{np_name}' publicado con éxito!")
                        st.rerun()
                    else:
                        st.error("Por favor completa el nombre y la descripción.")

        # TAB 3: BORRAR PRODUCTOS Y FOTOS
        with tab3:
            st.subheader("🗑️ Eliminar Productos e Imágenes del Catálogo")
            st.caption("Selecciona cualquier producto para eliminarlo o quitarle su foto asociada")
            
            if not app_data['products']:
                st.info("No hay productos cargados en el catálogo.")
            else:
                for p in list(app_data['products']):
                    pid = p['id']
                    pname = p['name']
                    psku = p.get('sku', '')
                    pcat = p.get('category', '')
                    has_img = "Sí 📷" if p.get('img_b64') else "No"
                    
                    c_info, c_btn1, c_btn2 = st.columns([3, 1.5, 1.5])
                    with c_info:
                        st.markdown(f"**ID {pid} - {pname}** | SKU: `{psku}` | Cat: _{pcat}_ | Foto: {has_img}")
                    with c_btn1:
                        if p.get('img_b64'):
                            if st.button("🖼️ Quitar Foto", key=f"btn_rm_img_{pid}"):
                                p['img_b64'] = None
                                save_data(app_data)
                                st.success(f"Foto de '{pname}' eliminada.")
                                st.rerun()
                    with c_btn2:
                        if st.button("🗑️ Borrar Producto", key=f"btn_del_prod_{pid}"):
                            app_data['products'] = [x for x in app_data['products'] if x['id'] != pid]
                            if pid in st.session_state.cart:
                                del st.session_state.cart[pid]
                            save_data(app_data)
                            st.success(f"Producto '{pname}' eliminado definitivamente.")
                            st.rerun()
                    st.markdown("<hr style='margin: 4px 0;'>", unsafe_allow_html=True)

        # TAB 4: ADMINISTRAR RESEÑAS
        with tab4:
            st.subheader("💬 Gestión y Borrado de Reseñas de Clientes")
            rev_list = app_data.get('reviews', [])
            
            if not rev_list:
                st.info("No hay reseñas de clientes para administrar.")
            else:
                col_clear, col_count = st.columns([2, 2])
                with col_clear:
                    if st.button("🗑️ BORRAR TODAS LAS RESEÑAS", key="btn_clear_all_revs"):
                        app_data['reviews'] = []
                        save_data(app_data)
                        st.success("Todas las reseñas han sido eliminadas.")
                        st.rerun()
                with col_count:
                    st.write(f"Total reseñas: **{len(rev_list)}**")
                    
                st.markdown("---")
                
                for idx, r in enumerate(list(rev_list)):
                    rid = r.get('id', idx)
                    rclient = r.get('client', 'Anon')
                    rrating = r.get('rating', '⭐')
                    rcomment = r.get('comment', '')
                    rdate = r.get('date', '')
                    
                    col_r_text, col_r_del = st.columns([4, 1])
                    with col_r_text:
                        st.markdown(f"**#{rid} - {rclient}** ({rrating}) - _{rdate}_<br>&ldquo;{rcomment}&rdquo;", unsafe_allow_html=True)
                    with col_r_del:
                        if st.button("🗑️ Borrar", key=f"btn_del_rev_{rid}_{idx}"):
                            app_data['reviews'] = [x for x in app_data['reviews'] if x.get('id') != rid and x != r]
                            save_data(app_data)
                            st.success(f"Reseña #{rid} eliminada.")
                            st.rerun()
                    st.markdown("<hr style='margin: 4px 0;'>", unsafe_allow_html=True)

        # TAB 5: PORTADA Y FONDO
        with tab5:
            st.subheader("🖼️ Configuración de Foto de Portada y Fondo")
            col_p1, col_p2 = st.columns(2)
            with col_p1:
                st.markdown("#### Banner de Portada (Melo 1)")
                f_hero = st.file_uploader("Subir nueva portada:", type=['jpg', 'png', 'jpeg', 'webp'], key="up_hero_banner")
                if st.button("💾 Guardar Portada", key="btn_save_hero"):
                    if f_hero:
                        app_data['cover_info']['hero_img_b64'] = file_to_b64(f_hero)
                        save_data(app_data)
                        st.success("Portada actualizada con éxito.")
                        st.rerun()
                if st.button("🗑️ Restablecer Portada Oficial", key="btn_reset_hero"):
                    app_data['cover_info']['hero_img_b64'] = MELO1_DEFAULT
                    save_data(app_data)
                    st.success("Portada restablecida.")
                    st.rerun()
                    
            with col_p2:
                st.markdown("#### Marca de Agua Fondo (Melo 2)")
                f_bg = st.file_uploader("Subir nuevo fondo:", type=['jpg', 'png', 'jpeg', 'webp'], key="up_bg_wallpaper")
                if st.button("💾 Guardar Fondo", key="btn_save_bg"):
                    if f_bg:
                        app_data['cover_info']['bg_img_b64'] = file_to_b64(f_bg)
                        save_data(app_data)
                        st.success("Fondo actualizado.")
                        st.rerun()
                if st.button("🗑️ Restablecer Fondo Oficial", key="btn_reset_bg"):
                    app_data['cover_info']['bg_img_b64'] = MELO2_DEFAULT
                    save_data(app_data)
                    st.success("Fondo restablecido.")
                    st.rerun()

        # TAB 6: CONFIGURAR PIN
        with tab6:
            st.subheader("🔑 Cambiar PIN Secreto de Administrador")
            current_pin = app_data.get('pin_secret', '1234')
            st.write(f"PIN Actual: `{current_pin}`")
            new_pin_input = st.text_input("Ingresa Nuevo PIN:", type="password", key="in_new_pin_sec")
            if st.button("💾 Cambiar PIN", key="btn_save_new_pin"):
                if new_pin_input:
                    app_data['pin_secret'] = new_pin_input
                    save_data(app_data)
                    st.success("PIN actualizado exitosamente.")
                    st.rerun()
                else:
                    st.warning("Escribe un nuevo PIN.")
