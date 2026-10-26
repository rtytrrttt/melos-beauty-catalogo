import streamlit as st
import pandas as pd
import datetime
import json
import os
import base64
import urllib.parse

# ---------------------------------------------------------
# FUNCION PARA CARGAR IMAGENES LOCALES O SUBIDAS
# ---------------------------------------------------------
def get_image_b64_from_file(filename):
    possible_paths = [
        filename,
        os.path.join('knowledge', filename),
        os.path.join('/workspace/knowledge', filename)
    ]
    for path in possible_paths:
        if os.path.exists(path):
            try:
                with open(path, 'rb') as f:
                    data = f.read()
                    return f"data:image/jpeg;base64,{base64.b64encode(data).decode('utf-8')}"
            except Exception:
                pass
    return None

MELO1_B64 = get_image_b64_from_file('melo1.jpeg')
MELO2_B64 = get_image_b64_from_file('melo2.jpeg')

st.set_page_config(page_title="Melo's Beauty 🌸", page_icon="🌸", layout="wide")

# ---------------------------------------------------------
# ESTILOS CSS - MARCA DE AGUA MELO2 Y COLORES MELO'S BEAUTY
# ---------------------------------------------------------
if MELO2_B64:
    bg_style = f"background: linear-gradient(rgba(255, 245, 247, 0.88), rgba(255, 245, 247, 0.88)), url('{MELO2_B64}') repeat center center; background-size: contain;"
else:
    bg_style = "background-color: #FFF5F7;"

CSS = f"""
<style>
    .stApp {{
        {bg_style}
        color: #2C2C2C;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }}
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    
    .hero-banner {{
        background: linear-gradient(135deg, #F8B8CC 0%, #F06292 100%);
        padding: 2.2rem;
        border-radius: 20px;
        text-align: center;
        color: white;
        border: 2px solid #F06292;
        margin-bottom: 1.5rem;
        box-shadow: 0px 6px 18px rgba(240, 98, 146, 0.25);
    }}
    .hero-title {{ color: #FFFFFF; font-size: 2.5rem; font-weight: 800; margin-bottom: 5px; }}
    .hero-subtitle {{ color: #FFF0F5; font-size: 1.2rem; font-style: italic; }}
    .hero-tag {{
        background-color: rgba(255, 255, 255, 0.25);
        display: inline-block;
        padding: 5px 15px;
        border-radius: 25px;
        font-weight: 600;
        margin-top: 8px;
        color: #FFFFFF;
    }}
    
    .product-card {{
        background-color: #FFFFFF;
        border: 2px solid #F8B8CC;
        border-radius: 16px;
        padding: 1rem;
        margin-bottom: 1.2rem;
        box-shadow: 0px 4px 12px rgba(248, 184, 204, 0.2);
    }}
    .product-title {{ color: #C2185B; font-size: 1.15rem; font-weight: 700; margin-top: 6px; }}
    .product-price {{ color: #C2185B; font-size: 1.3rem; font-weight: 800; margin-top: 6px; }}
    .product-img-container {{
        width: 100%;
        height: 180px;
        border-radius: 12px;
        background-color: #FFF0F3;
        display: flex;
        align-items: center;
        justify-content: center;
        overflow: hidden;
        border: 1px solid #F8B8CC;
    }}
    .product-img {{ width: 100%; height: 100%; object-fit: cover; }}
    
    .stock-badge-green {{
        background-color: #E8F5E9;
        color: #2E7D32;
        padding: 4px 10px;
        border-radius: 15px;
        font-size: 0.8rem;
        font-weight: 700;
        display: inline-block;
        margin-bottom: 6px;
    }}
    .stock-badge-red {{
        background-color: #FFEBEE;
        color: #C62828;
        padding: 4px 10px;
        border-radius: 15px;
        font-size: 0.8rem;
        font-weight: 700;
        display: inline-block;
        margin-bottom: 6px;
    }}
    
    .invoice-box {{
        background-color: #FFFFFF;
        border: 2px dashed #F06292;
        padding: 1.5rem;
        border-radius: 15px;
        font-family: monospace;
        color: #1A1A1A;
        margin-top: 1rem;
        white-space: pre-wrap;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.05);
    }}
    
    .btn-whatsapp-invoice {{
        background-color: #25D366;
        color: white !important;
        padding: 14px 20px;
        border-radius: 30px;
        text-decoration: none;
        font-weight: bold;
        display: block;
        text-align: center;
        font-size: 1.1rem;
        box-shadow: 0px 4px 12px rgba(37, 211, 102, 0.4);
        margin-top: 15px;
    }}
    
    .stButton>button {{
        background-color: #F06292;
        color: white;
        border-radius: 18px;
        border: none;
        font-weight: bold;
    }}
    .stButton>button:hover {{
        background-color: #C2185B;
        color: white;
    }}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# ---------------------------------------------------------
# MANEJO DE DATOS Y PERSISTENCIA JSON
# ---------------------------------------------------------
DATA_FILE = "catalogo_melos_data.json"

def get_default_data():
    return {
        "pin_secret": "1234",
        "cover_info": {
            "title": "Melo's Beauty 🌸",
            "slogan": "La magia que resalta tu brillo diario ✨",
            "location": "Tienda virtual de maquillaje y accesorios en Buenaventura 🎀",
            "phone": "+57 312 569 1563",
            "hero_img_b64": MELO1_B64,
            "bg_img_b64": MELO2_B64
        },
        "categories": {
            "Kits Melo's beauty": {"desc": "Combinaciones especiales diseñadas para armar tu kit diario.", "img_b64": None},
            "Billeteras mujeres": {"desc": "Billeteras elegantes con múltiples compartimentos.", "img_b64": None},
            "Billeteras hombres": {"desc": "Billeteras masculinas con grabado clásico.", "img_b64": None},
            "Termos": {"desc": "Termos térmicos de 1 litro para conservar bebidas.", "img_b64": None},
            "Accesorios": {"desc": "Accesorios únicos para complementar tu look diario.", "img_b64": None},
            "Joyeros": {"desc": "Organizadores elegantes para mantener ordenadas tus joyas.", "img_b64": None},
            "Pantuflas": {"desc": "Pantuflas ultra suaves y cómodas.", "img_b64": None},
            "Perfumes": {"desc": "Fragancias exclusivas con aromas perdurables.", "img_b64": None}
        },
        "products": [
            {"id": 101, "sku": "TERMO-1L-001", "name": "Termo térmico 1 litro", "category": "Termos", "price": 88700, "stock": 12, "desc": "Termo térmico de 1 Litro en tonos rosados suaves.", "img_b64": None},
            {"id": 102, "sku": "KIT-CANDY-PURPURE", "name": "Kit Candy Bum Purpure", "category": "Kits Melo's beauty", "price": 47400, "stock": 8, "desc": "Kit especial con brillo labial, bálsamo y accesorios.", "img_b64": None},
            {"id": 103, "sku": "KIT-MELOSBEAUTY-003", "name": "Kit Melo's beauty 3", "category": "Kits Melo's beauty", "price": 67000, "stock": 5, "desc": "Trío de cosméticos esenciales para el día a día.", "img_b64": None},
            {"id": 104, "sku": "KIT-MELOSBEAUTY-002", "name": "Kit Melo's beauty 2", "category": "Kits Melo's beauty", "price": 80700, "stock": 3, "desc": "Kit intermedio con sombra de ojos, labial e iluminador.", "img_b64": None},
            {"id": 105, "sku": "KIT-MELOSBEAUTY-001", "name": "Kit Melo's beauty 1", "category": "Kits Melo's beauty", "price": 94000, "stock": 10, "desc": "El kit más completo con cosmetiquera de regalo.", "img_b64": None},
            {"id": 106, "sku": "BILL-BIMBA-11", "name": "Billetera Bimba y Lola 1.1", "category": "Billeteras mujeres", "price": 65900, "stock": 6, "desc": "Billetera estilo 1.1 en tono rosa pastel.", "img_b64": None},
            {"id": 107, "sku": "BILL-LACOSTE-11", "name": "Billetera Lacoste hombre 1.1", "category": "Billeteras hombres", "price": 73700, "stock": 4, "desc": "Billetera masculina elegante en cuerina premium.", "img_b64": None}
        ],
        "reviews": [
            {"id": 1, "client": "Camila R.", "rating": "⭐⭐⭐⭐⭐", "comment": "Me encantó el Kit Melo's Beauty 1. Excelente servicio en Buenaventura.", "date": "2026-10-15"},
            {"id": 2, "client": "Valeria M.", "rating": "⭐⭐⭐⭐⭐", "comment": "El termo térmico de 1L mantiene el agua fría todo el día.", "date": "2026-10-18"}
        ]
    }

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                d = json.load(f)
                if 'cover_info' in d and not d['cover_info'].get('hero_img_b64') and MELO1_B64:
                    d['cover_info']['hero_img_b64'] = MELO1_B64
                if 'cover_info' in d and not d['cover_info'].get('bg_img_b64') and MELO2_B64:
                    d['cover_info']['bg_img_b64'] = MELO2_B64
                return d
        except Exception:
            return get_default_data()
    else:
        data = get_default_data()
        save_data(data)
        return data

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def file_to_b64(uploaded_file):
    if uploaded_file is None:
        return None
    bytes_data = uploaded_file.getvalue()
    return f"data:{uploaded_file.type};base64,{base64.b64encode(bytes_data).decode('utf-8')}"

if 'app_data' not in st.session_state:
    st.session_state.app_data = load_data()

if 'admin_auth' not in st.session_state:
    st.session_state.admin_auth = False

if 'cart' not in st.session_state:
    st.session_state.cart = {}

app_data = st.session_state.app_data

# ---------------------------------------------------------
# FUNCION PARA GENERAR MENSAJE FACTURA WHATSAPP (MELO 3)
# ---------------------------------------------------------
def get_sku(item):
    if item.get('sku'):
        return item['sku']
    name = item.get('name', 'PROD').upper().replace(" ", "").replace("'", "")
    return f"{name[:12]}-{item.get('id', 100)}"

def build_invoice_text(client_name, client_id, client_phone, client_address, client_city, payment_method, notes, cart_items):
    lines = []
    lines.append(f"Hola, soy {client_name},")
    lines.append("")
    lines.append("DATOS PARA LA FACTURA:")
    lines.append(f"• Nombre: {client_name}")
    if client_id:
        lines.append(f"• Cédula/NIT: {client_id}")
    lines.append(f"• Celular: {client_phone}")
    if client_address:
        lines.append(f"• Dirección: {client_address}")
    if client_city:
        lines.append(f"• Ciudad: {client_city}")
    lines.append(f"• Método de Pago: {payment_method}")
    lines.append("")
    lines.append("==============================")
    lines.append("quiero hacer este pedido en Melo's beauty :")
    lines.append("")
    
    subtotal = 0
    for it in cart_items:
        qty = it['qty']
        price = it.get('price', 0)
        tot = qty * price
        subtotal += tot
        sku = get_sku(it)
        p_name = it.get('name', 'Producto')
        lines.append(f"• {qty} *{p_name}* [SKU: {sku}] / COP ${tot:,.0f}")
    
    lines.append("")
    lines.append("==============================")
    lines.append("")
    lines.append(f"Subtotal: COP ${subtotal:,.0f}")
    lines.append(f"TOTAL A PAGAR: COP ${subtotal:,.0f}")
    if notes:
        lines.append("")
        lines.append(f"Notas: {notes}")
    
    return "\n".join(lines), subtotal

# ---------------------------------------------------------
# BARRA LATERAL ( SIDEBAR )
# ---------------------------------------------------------
st.sidebar.title("Melo's Beauty 🌸")
cart_units = sum(st.session_state.cart.values())
cart_label = f"🛒 Mi Carrito ({cart_units})" if cart_units > 0 else "🛒 Mi Carrito"

mode = st.sidebar.radio("Navegación:", ["🛍️ Catálogo Clientes", cart_label, "🔐 Acceso Dueño / Admin"])

st.sidebar.markdown("---")
st.sidebar.subheader("Contacto & Redes")
phone_clean = app_data["cover_info"]["phone"].replace("+", "").replace(" ", "")
st.sidebar.markdown(f"💬 **WhatsApp**: {app_data['cover_info']['phone']}")
st.sidebar.markdown("📸 **Instagram**: @melosbeauty_oficial")
st.sidebar.markdown("📘 **Facebook**: Melo's Beauty Buenaventura")

# ---------------------------------------------------------
# MODO 1: CATÁLOGO CLIENTES
# ---------------------------------------------------------
if mode == "🛍️ Catálogo Clientes":
    if app_data["cover_info"].get("hero_img_b64"):
        st.markdown(
            f'<div style="text-align:center; margin-bottom:1.2rem;">'
            f'<img src="{app_data["cover_info"]["hero_img_b64"]}" style="width:100%; max-height:280px; object-fit:cover; border-radius:20px; border:3px solid #F06292;">'
            f'</div>',
            unsafe_allow_html=True
        )
    
    st.markdown(
        f'<div class="hero-banner">'
        f'<div class="hero-title">{app_data["cover_info"]["title"]}</div>'
        f'<div class="hero-subtitle">{app_data["cover_info"]["slogan"]}</div>'
        f'<div class="hero-tag">📍 {app_data["cover_info"]["location"]}</div>'
        f'</div>',
        unsafe_allow_html=True
    )
    
    col_s, col_c = st.columns(2)
    with col_s:
        q = st.text_input("🔍 Buscar producto:", placeholder="Ej: Kit, Termo, Billetera...")
    with col_c:
        cat_keys = ["Todas"] + list(app_data["categories"].keys())
        cat = st.selectbox("🗂️ Categoría:", cat_keys)
    
    if cat != "Todas" and cat in app_data["categories"]:
        cat_info = app_data["categories"][cat]
        st.markdown(f"### 📂 Categoría: {cat}")
        cd, ci = st.columns([3, 1])
        with cd:
            st.info(f"**Descripción**: {cat_info['desc']}")
        with ci:
            if cat_info.get("img_b64"):
                st.image(cat_info["img_b64"], caption=f"Perfil {cat}", use_container_width=True)
    
    st.markdown("---")
    
    prods = app_data["products"]
    if cat != "Todas":
        prods = [p for p in prods if p["category"] == cat]
    if q:
        prods = [p for p in prods if q.lower() in p["name"].lower() or q.lower() in p["desc"].lower()]
    
    st.subheader(f"✨ Todos los Productos ({len(prods)})")
    
    if not prods:
        st.info("No se encontraron productos en esta categoría o búsqueda.")
    else:
        cols = st.columns(3)
        for idx, p in enumerate(prods):
            p_id = p["id"]
            in_cart = st.session_state.cart.get(p_id, 0)
            
            with cols[idx % 3]:
                if p.get("img_b64"):
                    img_html = f'<img src="{p["img_b64"]}" class="product-img">'
                else:
                    img_html = f'<div style="text-align:center; font-size:2rem;">🛍️<br><span style="font-size:0.85rem; color:#C2185B;">{p["name"]}</span></div>'
                
                st.markdown(
                    f'<div class="product-card">'
                    f'<div class="product-img-container">{img_html}</div>'
                    f'<div class="product-title">{p["name"]}</div>'
                    f'<div style="color:#666; font-size:0.82rem; margin-top:2px;">Categoría: <b>{p["category"]}</b></div>'
                    f'<p style="color:#444; font-size:0.85rem; margin-top:5px; height:38px; overflow:hidden;">{p["desc"]}</p>'
                    f'<div class="product-price">COP ${p["price"]:,}</div>'
                    f'</div>',
                    unsafe_allow_html=True
                )
                
                if p["stock"] > 5:
                    st.markdown(f'<span class="stock-badge-green">✔ En Stock ({p["stock"]} dispon.)</span>', unsafe_allow_html=True)
                elif p["stock"] > 0:
                    st.markdown(f'<span class="stock-badge-red">⚠️ ¡Pocas Unidades! ({p["stock"]})</span>', unsafe_allow_html=True)
                else:
                    st.error("❌ Agotado temporalmente")
                
                if in_cart == 0:
                    if st.button(f"➕ Agregar al Carrito", key=f"add_{p_id}"):
                        if p["stock"] > 0:
                            st.session_state.cart[p_id] = 1
                            st.toast(f"¡{p['name']} agregado al carrito! 🛒")
                            st.rerun()
                        else:
                            st.warning("Producto agotado.")
                else:
                    st.markdown(f"**🛒 En tu carrito: {in_cart} unids.**")
                    c_btn1, c_btn2 = st.columns(2)
                    with c_btn1:
                        if st.button("➖ Quitar", key=f"sub_{p_id}"):
                            st.session_state.cart[p_id] -= 1
                            if st.session_state.cart[p_id] <= 0:
                                del st.session_state.cart[p_id]
                            st.rerun()
                    with c_btn2:
                        if st.button("➕ Sumar", key=f"plus_{p_id}"):
                            if in_cart < p["stock"]:
                                st.session_state.cart[p_id] += 1
                                st.rerun()
                            else:
                                st.warning("Alcanzaste el stock disponible.")
                
                st.markdown("<br>", unsafe_allow_html=True)

    # Reseñas
    st.markdown("---")
    st.subheader("💬 Opiniones & Reseñas de Clientes")
    
    r_col1, r_col2 = st.columns([2, 1])
    with r_col1:
        for rev in app_data["reviews"]:
            r_client = rev.get("client", "Cliente")
            r_rating = rev.get("rating", "⭐⭐⭐⭐⭐")
            r_date = rev.get("date", "")
            r_comment = rev.get("comment", "")
            
            st.markdown(
                f'<div style="background-color:#FFFFFF; border:2px solid #F8B8CC; padding:0.9rem; border-radius:12px; margin-bottom:10px;">'
                f'<strong>{r_client}</strong> <span style="float:right;">{r_rating}</span><br>'
                f'<small style="color:#888;">{r_date}</small>'
                f'<p style="color:#2C2C2C; margin-top:5px; margin-bottom:0;">"{r_comment}"</p>'
                f'</div>',
                unsafe_allow_html=True
            )
    
    with r_col2:
        st.markdown("#### Déjanos tu opinión")
        new_name = st.text_input("Tu Nombre:", key="rev_name")
        new_rating = st.selectbox("Calificación:", ["⭐⭐⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐", "⭐⭐", "⭐"], key="rev_stars")
        new_comment = st.text_area("Tu Opinión:", key="rev_comment")
        
        if st.button("Publicar Reseña", key="btn_pub_rev"):
            if new_name and new_comment:
                new_id = max([r.get("id", 0) for r in app_data["reviews"]], default=0) + 1
                app_data["reviews"].append({
                    "id": new_id,
                    "client": new_name,
                    "rating": new_rating,
                    "comment": new_comment,
                    "date": datetime.date.today().strftime("%Y-%m-%d")
                })
                save_data(app_data)
                st.success("¡Gracias por tu reseña! Ha sido publicada.")
                st.rerun()
            else:
                st.warning("Por favor escribe tu nombre y opinión.")

    st.markdown("---")
    with st.expander("🔒 Términos, Condiciones y Política de Datos"):
        st.write("""
        **Melo's Beauty - Buenaventura**
        - **Protección de Datos Personales**: Tus datos son protegidos y utilizados únicamente para la gestión de despachos.
        - **Despachos**: Envíos locales en Buenaventura y despachos a nivel nacional.
        - **Garantías**: Calidad garantizada en todos nuestros kits, termos, billeteras y cosméticos.
        """)

# ---------------------------------------------------------
# MODO 2: CARRITO Y FACTURA COMPLETA
# ---------------------------------------------------------
elif mode.startswith("🛒 Mi Carrito"):
    st.title("🛒 Mi Carrito de Compras & Generador de Factura")
    st.caption("Revisa tus productos e ingresa tus datos personales para enviar la factura por WhatsApp.")
    
    if not st.session_state.cart:
        st.info("Tu carrito está vacío. Agrega productos desde el **Catálogo de Clientes**.")
    else:
        cart_items = []
        for p_id, qty in list(st.session_state.cart.items()):
            found = next((p for p in app_data["products"] if p["id"] == p_id), None)
            if found:
                item_copy = dict(found)
                item_copy["qty"] = qty
                cart_items.append(item_copy)
        
        st.subheader("1. Productos Seleccionados")
        df_cart = []
        for it in cart_items:
            df_cart.append({
                "ID": it["id"],
                "Producto": it["name"],
                "Categoría": it["category"],
                "Precio Unid.": f"COP ${it['price']:,}",
                "Cantidad": it["qty"],
                "Subtotal": f"COP ${(it['price'] * it['qty']):,}"
            })
        st.dataframe(pd.DataFrame(df_cart), use_container_width=True)
        
        if st.button("🗑️ Vaciar Carrito completo", key="btn_clear_cart"):
            st.session_state.cart = {}
            st.rerun()
            
        st.markdown("---")
        st.subheader("2. Datos Personales para la Factura")
        
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            c_name = st.text_input("👤 Nombre Completo *:", value="Nas Murillo", key="f_name")
            c_id = st.text_input("🪪 Cédula o NIT (Opcional):", value="1085214789", key="f_id")
            c_phone = st.text_input("📱 Celular / WhatsApp *:", value="+573028081327", key="f_phone")
        with col_f2:
            c_address = st.text_input("📍 Dirección de Entrega:", value="Calle 5 # 12-34, Pueblo Nuevo", key="f_address")
            c_city = st.text_input("🏙️ Ciudad / Municipio:", value="Buenaventura, Valle", key="f_city")
            c_pay = st.selectbox("💳 Método de Pago:", ["Nequi", "Daviplata", "Efectivo contra entrega", "Transferencia bancaria"], key="f_pay")
        
        c_notes = st.text_area("📝 Indicaciones adicionales (Opcional):", value="Entregar en la tarde.", key="f_notes")
        
        invoice_text, grand_total = build_invoice_text(
            client_name=c_name if c_name else "Cliente",
            client_id=c_id,
            client_phone=c_phone if c_phone else app_data["cover_info"]["phone"],
            client_address=c_address,
            client_city=c_city,
            payment_method=c_pay,
            notes=c_notes,
            cart_items=cart_items
        )
        
        st.markdown("---")
        st.subheader("3. Vista Previa de tu Factura (Estilo Modelo Oficial)")
        st.markdown(f'<div class="invoice-box">{invoice_text}</div>', unsafe_allow_html=True)
        
        encoded_wa = urllib.parse.quote(invoice_text)
        wa_target_phone = phone_clean
        wa_url = f"https://wa.me/{wa_target_phone}?text={encoded_wa}"
        
        st.markdown(
            f'<a href="{wa_url}" target="_blank" class="btn-whatsapp-invoice">'
            f'📲 ENVIAR ESTA FACTURA POR WHATSAPP A MELO\'S BEAUTY'
            f'</a>',
            unsafe_allow_html=True
        )

# ---------------------------------------------------------
# MODO 3: PANEL ADMINISTRACIÓN INTERNA (DUEÑO)
# ---------------------------------------------------------
else:
    st.title("🔐 Panel Interno de Administración")
    st.caption("Gestión exclusiva para el dueño de la tienda: inventarios, fotos, reseñas y configuración.")
    
    if not st.session_state.admin_auth:
        st.info("Ingresa el PIN Secreto para acceder al panel.")
        pin_input = st.text_input("Ingresa PIN Secreto:", type="password", key="admin_pin_input")
        if st.button("Ingresar al Panel", key="btn_login"):
            if pin_input == app_data["pin_secret"]:
                st.session_state.admin_auth = True
                st.success("¡Acceso concedido!")
                st.rerun()
            else:
                st.error("PIN incorrecto.")
    else:
        col_hdr, col_logout = st.columns([3, 1])
        with col_hdr:
            st.write(f"**Estado**: Sesión Activa como Dueño")
        with col_logout:
            if st.button("🔒 Cerrar Sesión Admin", key="btn_logout"):
                st.session_state.admin_auth = False
                st.rerun()
        
        t1, t2, t3, t4, t5, t6 = st.tabs([
            "📊 Stock & Inventario",
            "📸 Subir Producto",
            "🗑️ Borrar Productos & Fotos",
            "💬 Administrar Reseñas",
            "🖼️ Portada & Fondo",
            "🔑 Cambiar PIN"
        ])
        
        # TAB 1: STOCK & INVENTARIO
        with t1:
            st.subheader("Control General de Inventario")
            df_prods = pd.DataFrame(app_data["products"])
            
            tot_val = sum(p["price"] * p["stock"] for p in app_data["products"])
            tot_units = sum(p["stock"] for p in app_data["products"])
            
            m1, m2, m3 = st.columns(3)
            m1.metric("Total Productos", len(app_data["products"]))
            m2.metric("Unidades en Stock", tot_units)
            m3.metric("Valor del Inventario", f"COP ${tot_val:,.0f}")
            
            st.markdown("---")
            st.dataframe(df_prods[["id", "name", "category", "price", "stock", "desc"]], use_container_width=True)
            
            st.markdown("#### Modificar Cantidad de Stock / Precio")
            prod_ids = [p["id"] for p in app_data["products"]]
            sel_id = st.selectbox("Seleccionar Producto por ID:", prod_ids, format_func=lambda x: f"ID {x} - {next((p['name'] for p in app_data['products'] if p['id']==x), '')}", key="sel_stk_id")
            
            curr_prod = next((p for p in app_data["products"] if p["id"] == sel_id), None)
            if curr_prod:
                c_s1, c_s2 = st.columns(2)
                with c_s1:
                    new_stk = st.number_input("Nuevo Stock:", min_value=0, value=int(curr_prod["stock"]), key="input_new_stk")
                with c_s2:
                    new_price = st.number_input("Nuevo Precio (COP):", min_value=0, value=int(curr_prod["price"]), step=1000, key="input_new_price")
                
                if st.button("💾 Guardar Cambios en Producto", key="btn_save_stk"):
                    curr_prod["stock"] = new_stk
                    curr_prod["price"] = new_price
                    save_data(app_data)
                    st.success(f"¡Producto {curr_prod['name']} actualizado exitosamente!")
                    st.rerun()

        # TAB 2: SUBIR PRODUCTO CON FOTO REAL
        with t2:
            st.subheader("📸 Publicar Nuevo Producto con Foto Real")
            with st.form("form_add_product"):
                np_name = st.text_input("Nombre del Producto:")
                np_cat = st.selectbox("Categoría:", list(app_data["categories"].keys()))
                np_price = st.number_input("Precio (COP):", min_value=0, value=50000, step=1000)
                np_stock = st.number_input("Stock Inicial:", min_value=0, value=10)
                np_desc = st.text_area("Descripción corta:")
                np_file = st.file_uploader("Subir Foto del Producto:", type=["jpg", "png", "jpeg", "webp"])
                
                if st.form_submit_button("💾 Publicar Producto"):
                    if np_name and np_desc:
                        b64_img = file_to_b64(np_file)
                        new_id = max([p["id"] for p in app_data["products"]], default=100) + 1
                        new_sku = f"{np_name.upper().replace(' ', '')[:10]}-{new_id}"
                        
                        app_data["products"].append({
                            "id": new_id,
                            "sku": new_sku,
                            "name": np_name,
                            "category": np_cat,
                            "price": np_price,
                            "stock": np_stock,
                            "desc": np_desc,
                            "img_b64": b64_img
                        })
                        save_data(app_data)
                        st.success(f"¡Producto '{np_name}' publicado con éxito!")
                        st.rerun()
                    else:
                        st.error("Completa el nombre y la descripción.")

        # TAB 3: BORRAR PRODUCTOS Y FOTOS
        with t3:
            st.subheader("🗑️ Borrar Productos e Imágenes")
            st.write("Elimina un producto por completo o quita su imagen individual.")
            
            p_del_id = st.selectbox(
                "Seleccionar Producto:",
                [p["id"] for p in app_data["products"]],
                format_func=lambda x: f"ID {x} - {next((p['name'] for p in app_data['products'] if p['id']==x), '')}",
                key="sel_del_prod_id"
            )
            
            target_del = next((p for p in app_data["products"] if p["id"] == p_del_id), None)
            
            if target_del:
                c_del1, c_del2 = st.columns(2)
                with c_del1:
                    if st.button("🗑️ Eliminar Producto Definitivamente", key=f"btn_del_p_{p_del_id}"):
                        app_data["products"] = [p for p in app_data["products"] if p["id"] != p_del_id]
                        save_data(app_data)
                        st.success("Producto eliminado del catálogo.")
                        st.rerun()
                
                with c_del2:
                    if target_del.get("img_b64"):
                        if st.button("🖼️ Quitar Solo la Foto del Producto", key=f"btn_del_img_{p_del_id}"):
                            target_del["img_b64"] = None
                            save_data(app_data)
                            st.success("Foto eliminada.")
                            st.rerun()
                    else:
                        st.caption("Este producto no tiene foto adjunta.")

        # TAB 4: ADMINISTRAR RESEÑAS
        with t4:
            st.subheader("💬 Gestión de Reseñas de Clientes")
            st.write("Borra comentarios inapropiados o limpia el historial de opiniones.")
            
            if not app_data["reviews"]:
                st.info("No hay reseñas publicadas actualmente.")
            else:
                for rev in list(app_data["reviews"]):
                    rid = rev.get("id", 0)
                    rclient = rev.get("client", "Cliente")
                    rrating = rev.get("rating", "⭐⭐⭐⭐⭐")
                    rdate = rev.get("date", "")
                    rcomment = rev.get("comment", "")
                    
                    c_rev1, c_rev2 = st.columns([3, 1])
                    with c_rev1:
                        st.markdown(f"**#{rid} - {rclient}** ({rrating}) - _{rdate}_")
                        st.write(f'"{rcomment}"')
                    with c_rev2:
                        if st.button(f"🗑️ Borrar", key=f"btn_del_rev_{rid}"):
                            app_data["reviews"] = [r for r in app_data["reviews"] if r.get("id") != rid]
                            save_data(app_data)
                            st.success("Reseña borrada.")
                            st.rerun()
                    st.markdown("---")
                
                if st.button("🗑️ BORRAR TODAS LAS RESEÑAS", key="btn_del_all_revs"):
                    app_data["reviews"] = []
                    save_data(app_data)
                    st.success("Todas las reseñas fueron eliminadas.")
                    st.rerun()

        # TAB 5: PORTADA Y FONDO
        with t5:
            st.subheader("🖼️ Configuración de Imagen de Portada y Fondo")
            
            f_hero = st.file_uploader("Subir Nueva Foto de Portada (Banner):", type=["jpg", "png", "jpeg", "webp"], key="up_hero")
            if app_data["cover_info"].get("hero_img_b64"):
                st.image(app_data["cover_info"]["hero_img_b64"], caption="Portada Actual", use_container_width=True)
                if st.button("🗑️ Quitar Imagen de Portada", key="btn_del_hero"):
                    app_data["cover_info"]["hero_img_b64"] = None
                    save_data(app_data)
                    st.success("Portada eliminada.")
                    st.rerun()
            
            if st.button("💾 Guardar Portada Subida", key="btn_save_hero"):
                if f_hero:
                    app_data["cover_info"]["hero_img_b64"] = file_to_b64(f_hero)
                    save_data(app_data)
                    st.success("Portada actualizada.")
                    st.rerun()
                    
            st.markdown("---")
            st.subheader("Marca de Agua de Fondo (Melo 2)")
            f_bg = st.file_uploader("Subir Imagen de Fondo:", type=["jpg", "png", "jpeg", "webp"], key="up_bg")
            if st.button("💾 Guardar Imagen de Fondo", key="btn_save_bg"):
                if f_bg:
                    app_data["cover_info"]["bg_img_b64"] = file_to_b64(f_bg)
                    save_data(app_data)
                    st.success("Imagen de fondo actualizada.")
                    st.rerun()

        # TAB 6: CAMBIAR PIN
        with t6:
            st.subheader("🔑 Configuración del PIN de Seguridad")
            st.write(f"PIN Actual: `{app_data['pin_secret']}`")
            
            new_pin = st.text_input("Nuevo PIN de Seguridad:", type="password", key="input_new_pin")
            if st.button("💾 Guardar Nuevo PIN", key="btn_save_pin"):
                if new_pin:
                    app_data["pin_secret"] = new_pin
                    save_data(app_data)
                    st.success("PIN de seguridad actualizado con éxito.")
                    st.rerun()
                else:
                    st.warning("Escribe un PIN válido.")
