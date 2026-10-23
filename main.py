import streamlit as st
import pandas as pd
import datetime
import json
import os
import base64
import urllib.parse

def load_local_img(fname):
    paths = [
        fname,
        os.path.join('knowledge', fname),
        os.path.join('/workspace/knowledge', fname),
        os.path.join('..', 'knowledge', fname)
    ]
    for p in paths:
        if os.path.exists(p):
            try:
                with open(p, 'rb') as f:
                    ext = 'png' if fname.endswith('.png') else 'jpeg'
                    return f'data:image/{ext};base64,{base64.b64encode(f.read()).decode("utf-8")}'
            except Exception:
                pass
    return None

MELO1_DEFAULT = load_local_img('melo1.jpeg')
MELO2_DEFAULT = load_local_img('melo2.jpeg')

st.set_page_config(
    page_title="Melo's Beauty - Tienda Virtual",
    page_icon='🌸',
    layout='wide',
    initial_sidebar_state='expanded'
)

DATA_FILE = 'catalogo_melos_data.json'

def get_default_data():
    return {
        'access_pin': '1234',
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
            {'id': 106, 'sku': 'BILLET-BIMBA-001', 'name': 'Billetera Bimba y Lola 1.1', 'category': 'Billeteras mujeres', 'price': 65900, 'stock': 6, 'desc': 'Billetera estilo 1.1 en tono rosa pastel.', 'img_b64': None},
            {'id': 107, 'sku': 'BILLET-LACOSTE-001', 'name': 'Billetera Lacoste hombre 1.1', 'category': 'Billeteras hombres', 'price': 73700, 'stock': 4, 'desc': 'Billetera masculina elegante en cuerina premium.', 'img_b64': None}
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
                if 'cover_info' in d:
                    if not d['cover_info'].get('hero_img_b64'):
                        d['cover_info']['hero_img_b64'] = MELO1_DEFAULT
                    if not d['cover_info'].get('bg_img_b64'):
                        d['cover_info']['bg_img_b64'] = MELO2_DEFAULT
                return d
        except Exception:
            return get_default_data()
    else:
        d = get_default_data()
        save_data(d)
        return d

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def file_to_b64(u):
    if u is None:
        return None
    return f'data:{u.type};base64,{base64.b64encode(u.getvalue()).decode("utf-8")}'

if 'app_data' not in st.session_state:
    st.session_state.app_data = load_data()
if 'admin_auth' not in st.session_state:
    st.session_state.admin_auth = False

app_data = st.session_state.app_data


bg_b64 = app_data['cover_info'].get('bg_img_b64') or MELO2_DEFAULT

if bg_b64:
    bg_style = f'background: linear-gradient(rgba(255, 245, 247, 0.88), rgba(255, 245, 247, 0.88)), url("{bg_b64}") center/cover fixed no-repeat !important;'
else:
    bg_style = 'background-color: #FFF5F7 !important;'

CSS = f'''
<style>
    .stApp {{
        {bg_style}
        color: #2C2C2C;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }}
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    
    .hero-banner {{
        background: linear-gradient(135deg, rgba(248, 184, 204, 0.95) 0%, rgba(240, 98, 146, 0.95) 100%);
        padding: 2.2rem;
        border-radius: 24px;
        text-align: center;
        color: white;
        border: 2px solid #F06292;
        margin-bottom: 2rem;
        box-shadow: 0px 8px 20px rgba(240, 98, 146, 0.25);
    }}
    .hero-title {{ color: #FFFFFF; font-size: 2.8rem; font-weight: 800; text-shadow: 1px 1px 4px rgba(0,0,0,0.2); }}
    .hero-subtitle {{ color: #FFF0F5; font-size: 1.3rem; font-style: italic; }}
    .hero-tag {{ background-color: rgba(255, 255, 255, 0.3); display: inline-block; padding: 6px 18px; border-radius: 30px; font-weight: 600; margin-top: 10px; color: #FFFFFF; }}
    
    .product-card {{
        background-color: rgba(255, 255, 255, 0.95);
        border: 2px solid #F8B8CC;
        border-radius: 18px;
        padding: 1.2rem;
        margin-bottom: 1.5rem;
        box-shadow: 0px 6px 16px rgba(248, 184, 204, 0.2);
    }}
    .product-title {{ color: #C2185B; font-size: 1.25rem; font-weight: 700; }}
    .product-price {{ color: #C2185B; font-size: 1.4rem; font-weight: 800; }}
    .product-img-container {{
        width: 100%;
        height: 190px;
        border-radius: 14px;
        background-color: #FFF0F3;
        display: flex;
        align-items: center;
        justify-content: center;
        overflow: hidden;
        border: 1px solid #F8B8CC;
    }}
    .product-img {{ width: 100%; height: 100%; object-fit: cover; }}
    
    .stock-badge-green {{ background-color: #E8F5E9; color: #2E7D32; padding: 6px 12px; border-radius: 20px; font-size: 0.85rem; font-weight: 700; display: inline-block; margin-top: 5px; }}
    .stock-badge-red {{ background-color: #FFEBEE; color: #C62828; padding: 6px 12px; border-radius: 20px; font-size: 0.85rem; font-weight: 700; display: inline-block; margin-top: 5px; }}
    
    .btn-whatsapp {{
        background-color: #25D366;
        color: white !important;
        padding: 10px 16px;
        border-radius: 25px;
        text-decoration: none;
        font-weight: bold;
        display: block;
        text-align: center;
        box-shadow: 0px 4px 10px rgba(37, 211, 102, 0.3);
        width: 100%;
    }}
    .btn-whatsapp:hover {{
        background-color: #1EBE57;
    }}
    
    .factura-box {{
        background-color: #FFFFFF;
        border: 2px dashed #F06292;
        border-radius: 16px;
        padding: 1.5rem;
        font-family: 'Courier New', Courier, monospace;
        color: #2C2C2C;
        box-shadow: 0px 4px 15px rgba(240, 98, 146, 0.15);
    }}
    
    .stButton>button {{
        background-color: #F06292;
        color: white;
        border-radius: 20px;
        border: none;
        font-weight: bold;
    }}
    .stButton>button:hover {{
        background-color: #C2185B;
        color: white;
    }}
</style>
'''
st.markdown(CSS, unsafe_allow_html=True)

st.sidebar.title("Melo's Beauty 🌸")
mode = st.sidebar.radio('Navegación:', [
    '🛍️ Catálogo Clientes',
    '🛒 Armar Pedido / Factura (Melo 3)',
    '🔐 Acceso Dueño / Admin'
])

st.sidebar.markdown('---')
st.sidebar.subheader('Redes Sociales & Contacto')
phone_clean = app_data['cover_info']['phone'].replace('+', '').replace(' ', '')
st.sidebar.markdown(f'💬 **WhatsApp**: {app_data["cover_info"]["phone"]}')
st.sidebar.markdown('📸 **Instagram**: @melosbeauty_oficial')
st.sidebar.markdown('📘 **Facebook**: Melo Beauty')

def build_whatsapp_invoice_text(client_name, client_phone, items_list):
    name_str = client_name.strip() if client_name and client_name.strip() else 'Cliente'
    phone_str = client_phone.strip() if client_phone and client_phone.strip() else 'No especificado'
    
    lines = []
    lines.append(f"Hola, soy {name_str},\n")
    lines.append(f"Nombre: {name_str}")
    lines.append(f"Celular: {phone_str}\n")
    lines.append("==============================")
    lines.append("quiero hacer este pedido en Melo's beauty :\n")
    
    total = 0
    for item in items_list:
        p_name = item['name']
        p_sku = item.get('sku', f'REF-{item["id"]}')
        p_price = item['price']
        qty = item.get('qty', 1)
        item_total = p_price * qty
        total += item_total
        
        lines.append(f"• {qty} *{p_name}* [{p_sku}] / COP ${item_total:,}")
    
    lines.append("\n==============================\n")
    lines.append(f"Subtotal: COP ${total:,}")
    lines.append(f"TOTAL: COP ${total:,}")
    
    full_text = "\n".join(lines)
    encoded = urllib.parse.quote(full_text)
    return full_text, encoded


# MODE 1: CATALOGO CLIENTES
if mode == '🛍️ Catálogo Clientes':
    hero_b64 = app_data['cover_info'].get('hero_img_b64') or MELO1_DEFAULT
    if hero_b64:
        st.markdown(
            f'<div style="text-align:center; margin-bottom:1.5rem;">'
            f'<img src="{hero_b64}" style="width:100%; max-height:280px; object-fit:cover; border-radius:20px; border:3px solid #F06292; box-shadow:0px 6px 16px rgba(240, 98, 146, 0.3);">'
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
        q = st.text_input('🔍 Buscar producto:', placeholder='Ej: Kit, Termo, Billetera...')
    with col_c:
        cat = st.selectbox('🗂️ Categoría:', ['Todas'] + list(app_data['categories'].keys()))
        
    if cat != 'Todas' and cat in app_data['categories']:
        cat_info = app_data['categories'][cat]
        st.markdown(f'### 📂 Categoría: {cat}')
        cd, ci = st.columns([3, 1])
        with cd:
            st.info(f'**Descripción**: {cat_info["desc"]}')
        with ci:
            if cat_info.get('img_b64'):
                st.image(cat_info['img_b64'], caption=f'Perfil {cat}', use_container_width=True)
            else:
                st.markdown('<div style="background-color:#F8B8CC; padding:15px; border-radius:12px; text-align:center; color:white; font-weight:bold;">🌸 Foto Categoría</div>', unsafe_allow_html=True)
                
    st.markdown('---')
    prods = app_data['products']
    if cat != 'Todas':
        prods = [p for p in prods if p['category'] == cat]
    if q:
        prods = [p for p in prods if q.lower() in p['name'].lower() or q.lower() in p['desc'].lower()]
        
    st.subheader(f'✨ Todos los Productos ({len(prods)})')
    
    if not prods:
        st.info('No hay productos coincidentes.')
    else:
        cols = st.columns(3)
        for idx, p in enumerate(prods):
            with cols[idx % 3]:
                img_html = f'<img src="{p["img_b64"]}" class="product-img">' if p.get('img_b64') else f'<div style="text-align:center; font-size:2rem;">🛍️<br><span style="font-size:0.85rem; color:#C2185B;">{p["name"]}</span></div>'
                st.markdown(
                    f'<div class="product-card">'
                    f'<div class="product-img-container">{img_html}</div>'
                    f'<div class="product-title">{p["name"]}</div>'
                    f'<div style="color:#666; font-size:0.85rem; margin-top:3px;">Categoría: <b>{p["category"]}</b></div>'
                    f'<p style="color:#444; font-size:0.88rem; margin-top:6px; height:42px; overflow:hidden;">{p["desc"]}</p>'
                    f'<div class="product-price">COP ${p["price"]:,}</div>'
                    f'</div>',
                    unsafe_allow_html=True
                )
                
                if p['stock'] > 5:
                    st.markdown(f'<span class="stock-badge-green">✔ En Stock ({p["stock"]} dispon.)</span>', unsafe_allow_html=True)
                elif p['stock'] > 0:
                    st.markdown(f'<span class="stock-badge-red">⚠️ ¡Pocas Unidades! ({p["stock"]})</span>', unsafe_allow_html=True)
                else:
                    st.error('❌ Agotado temporalmente')
                
                single_item = [{'name': p['name'], 'sku': p.get('sku', f'SKU-{p["id"]}'), 'price': p['price'], 'qty': 1}]
                _, wa_enc = build_whatsapp_invoice_text('Cliente', '', single_item)
                wa_domain = "wa." + "me"
                wa_link = f"https://{wa_domain}/{phone_clean}?text={wa_enc}"
                
                st.markdown(f'<a href="{wa_link}" target="_blank" class="btn-whatsapp">📲 Pedir por WhatsApp (Factura)</a>', unsafe_allow_html=True)
                st.markdown('<br>', unsafe_allow_html=True)

    st.markdown('---')
    st.subheader('💬 Opiniones & Reseñas de Clientes')
    r1, r2 = st.columns([2, 1])
    with r1:
        if not app_data['reviews']:
            st.info('Aún no hay reseñas publicadas.')
        else:
            for rev in app_data['reviews']:
                st.markdown(
                    f'<div style="background-color:#FFFFFF; border:2px solid #F8B8CC; padding:1rem; border-radius:14px; margin-bottom:12px;">'
                    f'<strong>{rev["client"]}</strong> <span style="float:right;">{rev["rating"]}</span><br>'
                    f'<small style="color:#888;">{rev["date"]}</small>'
                    f'<p style="color:#2C2C2C; margin-top:6px;">"{rev["comment"]}"</p>'
                    f'</div>',
                    unsafe_allow_html=True
                )
    with r2:
        st.markdown('#### Deja tu Opinión')
        nn = st.text_input('Tu Nombre:')
        nr = st.selectbox('Calificación:', ['⭐⭐⭐⭐⭐', '⭐⭐⭐⭐', '⭐⭐⭐', '⭐⭐', '⭐'])
        nc = st.text_area('Comentario:')
        if st.button('Publicar Reseña'):
            if nn and nc:
                new_rev_id = max([r.get('id', 0) for r in app_data['reviews']], default=0) + 1
                app_data['reviews'].append({
                    'id': new_rev_id,
                    'client': nn,
                    'rating': nr,
                    'comment': nc,
                    'date': datetime.date.today().strftime('%Y-%m-%d')
                })
                save_data(app_data)
                st.success('¡Gracias por tu reseña!')
                st.rerun()

    st.markdown('---')
    with st.expander('🔒 Términos, Condiciones y Política de Seguridad'):
        st.write("""
        **Melo's Beauty - Buenaventura**
        - **Protección de Datos Personales**: Tus datos están protegidos conforme a la ley de Habeas Data en Colombia.
        - **Envíos**: Envíos locales en Buenaventura y despachos a todo el país.
        - **Garantías**: Calidad garantizada en todos los productos.
        """)

# MODE 2: ARMAR PEDIDO / FACTURA (ESTILO MELO 3)
elif mode == '🛒 Armar Pedido / Factura (Melo 3)':
    st.title('🛒 Generador de Pedido & Factura (Melo 3)')
    st.caption('Selecciona tus productos, ingresa tus datos y genera la factura directa para WhatsApp.')
    
    col_c1, col_c2 = st.columns([1, 1])
    
    with col_c1:
        st.subheader('1. Datos del Cliente')
        c_name = st.text_input('Tu Nombre Completo:', value='', placeholder='Ej: Nas Murillo')
        c_phone = st.text_input('Tu Teléfono / WhatsApp:', value='', placeholder='Ej: +573028081327')
        
        st.subheader('2. Seleccionar Productos')
        prod_options = {f"{p['name']} (COP ${p['price']:,})": p for p in app_data['products']}
        selected_prod_names = st.multiselect('Elige los productos para tu pedido:', list(prod_options.keys()))
        
        selected_items = []
        for pname in selected_prod_names:
            p_obj = prod_options[pname]
            qty = st.number_input(f'Cantidad para "{p_obj["name"]}":', min_value=1, max_value=max(p_obj['stock'], 1), value=1, key=f"qty_{p_obj['id']}")
            selected_items.append({
                'id': p_obj['id'],
                'name': p_obj['name'],
                'sku': p_obj.get('sku', f'SKU-{p_obj["id"]}'),
                'price': p_obj['price'],
                'qty': qty
            })
            
    with col_c2:
        st.subheader('3. Vista Previa de la Factura')
        if not selected_items:
            st.info('Selecciona al menos un producto a la izquierda para armar tu factura.')
        else:
            txt_factura, enc_factura = build_whatsapp_invoice_text(c_name, c_phone, selected_items)
            
            st.markdown(f'<div class="factura-box"><pre style="white-space: pre-wrap; word-wrap: break-word;">{txt_factura}</pre></div>', unsafe_allow_html=True)
            st.markdown('<br>', unsafe_allow_html=True)
            
            wa_domain = "wa." + "me"
            wa_link_factura = f"https://{wa_domain}/{phone_clean}?text={enc_factura}"
            st.markdown(
                f'<a href="{wa_link_factura}" target="_blank" class="btn-whatsapp" style="font-size:1.1rem; padding:14px;">'
                f'📲 ENVIAR ESTA FACTURA POR WHATSAPP A MELOS BEAUTY'
                f'</a>',
                unsafe_allow_html=True
            )


else:
    st.title('🔐 Panel Interno de Administración (Exclusivo Dueño)')
    
    if not st.session_state.admin_auth:
        st.info('Para acceder ingresa la clave de la tienda.')
        p_in = st.text_input('Ingresa Clave Admin:')
        if st.button('Ingresar al Panel'):
            if p_in == app_data.get('access_pin', '1234'):
                st.session_state.admin_auth = True
                st.success('¡Bienvenido!')
                st.rerun()
            else:
                st.error('Clave incorrecta')
    else:
        col_t, col_logout = st.columns([3, 1])
        with col_logout:
            if st.button('🔒 Cerrar Sesión Admin'):
                st.session_state.admin_auth = False
                st.rerun()
                
        t1, t2, t3, t4, t5, t6 = st.tabs([
            '📊 Inventario & Stock',
            '➕ Productos e Imágenes',
            '💬 Administrar Reseñas',
            '🗂️ Categorías e Imágenes',
            '🖼️ Portada & Fondo (Melo 1 y 2)',
            '🔑 Configurar Clave'
        ])
        
        with t1:
            st.subheader('📊 Estado del Inventario')
            df_prods = pd.DataFrame(app_data['products'])
            tot_val = (df_prods['price'] * df_prods['stock']).sum()
            
            m1, m2, m3 = st.columns(3)
            m1.metric('Total Productos', len(df_prods))
            m2.metric('Unidades Stock', df_prods['stock'].sum())
            m3.metric('Valor Inventario', f'COP ${tot_val:,.0f}')
            
            st.markdown('---')
            st.dataframe(df_prods[['id', 'sku', 'name', 'category', 'price', 'stock', 'desc']], use_container_width=True)
            
            st.markdown('#### Actualizar Unidades en Stock')
            psel = st.selectbox(
                'Seleccionar Producto:',
                df_prods['id'].tolist(),
                format_func=lambda x: f'ID {x} - {df_prods[df_prods["id"]==x]["name"].values[0]}'
            )
            nstk = st.number_input('Nuevo Stock:', min_value=0, value=int(df_prods[df_prods['id']==psel]['stock'].values[0]))
            if st.button('Guardar Stock'):
                for p in app_data['products']:
                    if p['id'] == psel:
                        p['stock'] = nstk
                        break
                save_data(app_data)
                st.success('Stock actualizado correctamente.')
                st.rerun()

        with t2:
            st.subheader('➕ Publicar Nuevo Producto')
            with st.form('form_add_p'):
                np_name = st.text_input('Nombre del Producto:')
                np_sku = st.text_input('SKU / Código Referencia:', value='', placeholder='Ej: KIT-MELOS-001')
                np_cat = st.selectbox('Categoría:', list(app_data['categories'].keys()))
                np_price = st.number_input('Precio (COP):', min_value=0, value=50000, step=1000)
                np_stock = st.number_input('Stock Inicial:', min_value=0, value=10)
                np_desc = st.text_area('Descripción del Producto:')
                np_file = st.file_uploader('Subir Foto del Producto:', type=['jpg', 'png', 'jpeg', 'webp'])
                
                if st.form_submit_button('💾 Publicar Producto'):
                    if np_name and np_desc:
                        b64 = file_to_b64(np_file)
                        nid = max([p['id'] for p in app_data['products']], default=100) + 1
                        sku_final = np_sku if np_sku.strip() else f'REF-{nid}'
                        app_data['products'].append({
                            'id': nid,
                            'sku': sku_final,
                            'name': np_name,
                            'category': np_cat,
                            'price': np_price,
                            'stock': np_stock,
                            'desc': np_desc,
                            'img_b64': b64
                        })
                        save_data(app_data)
                        st.success(f'¡Producto "{np_name}" publicado con éxito!')
                        st.rerun()
                    else:
                        st.error('Ingresa nombre y descripción para el producto.')

            st.markdown('---')
            st.subheader('🗑️ Eliminar Producto o Foto de Producto')
            col_del1, col_del2 = st.columns(2)
            
            with col_del1:
                st.markdown('#### 1. Eliminar Producto Completo')
                if not app_data['products']:
                    st.info('No hay productos para eliminar.')
                else:
                    del_prod_id = st.selectbox(
                        'Selecciona Producto a Eliminar:',
                        [p['id'] for p in app_data['products']],
                        format_func=lambda x: f'ID {x} - {[p["name"] for p in app_data["products"] if p["id"]==x][0]}'
                    )
                    if st.button('🗑️ Eliminar Producto Definitivamente'):
                        app_data['products'] = [p for p in app_data['products'] if p['id'] != del_prod_id]
                        save_data(app_data)
                        st.success('Producto eliminado del catálogo.')
                        st.rerun()
                        
            with col_del2:
                st.markdown('#### 2. Quitar Foto de Producto')
                prods_with_img = [p for p in app_data['products'] if p.get('img_b64')]
                if not prods_with_img:
                    st.info('No hay productos con foto personalizada.')
                else:
                    clear_img_id = st.selectbox(
                        'Selecciona Producto para Quitar su Foto:',
                        [p['id'] for p in prods_with_img],
                        format_func=lambda x: f'ID {x} - {[p["name"] for p in prods_with_img if p["id"]==x][0]}'
                    )
                    if st.button('🖼️ Quitar Foto del Producto'):
                        for p in app_data['products']:
                            if p['id'] == clear_img_id:
                                p['img_b64'] = None
                                break
                        save_data(app_data)
                        st.success('Foto eliminada del producto.')
                        st.rerun()

        with t3:
            st.subheader('💬 Administrar y Borrar Comentarios de Clientes')
            if not app_data['reviews']:
                st.info('No hay comentarios o reseñas registradas.')
            else:
                st.markdown('#### Reseñas Publicadas:')
                for idx, rev in enumerate(app_data['reviews']):
                    r_id = rev.get('id', idx + 1)
                    col_r1, col_r2 = st.columns([4, 1])
                    with col_r1:
                        st.markdown(
                            f'**{rev["client"]}** ({rev["rating"]}) - *{rev["date"]}*<br>'
                            f'"{rev["comment"]}"',
                            unsafe_allow_html=True
                        )
                    with col_r2:
                        if st.button(f'🗑️ Borrar #{r_id}', key=f'del_rev_{r_id}_{idx}'):
                            app_data['reviews'].pop(idx)
                            save_data(app_data)
                            st.success('Reseña eliminada.')
                            st.rerun()
                    st.markdown('<hr style="margin:8px 0;">', unsafe_allow_html=True)
                    
                st.markdown('<br>', unsafe_allow_html=True)
                if st.button('🗑️ BORRAR TODAS LAS RESEÑAS'):
                    app_data['reviews'] = []
                    save_data(app_data)
                    st.success('Todas las reseñas han sido eliminadas.')
                    st.rerun()

        with t4:
            st.subheader('🗂️ Editar Categorías y Fotos de Perfil')
            for cat_k, cat_v in app_data['categories'].items():
                with st.expander(f'📁 {cat_k}'):
                    c_desc = st.text_area(f'Descripción para "{cat_k}":', value=cat_v['desc'], key=f'desc_{cat_k}')
                    c_file = st.file_uploader(f'Foto Perfil para "{cat_k}":', type=['jpg', 'png', 'jpeg', 'webp'], key=f'file_{cat_k}')
                    
                    if cat_v.get('img_b64'):
                        st.image(cat_v['img_b64'], caption=f'Foto Perfil Actual {cat_k}', width=140)
                        if st.button(f'🗑️ Quitar Foto de {cat_k}', key=f'rm_img_{cat_k}'):
                            app_data['categories'][cat_k]['img_b64'] = None
                            save_data(app_data)
                            st.success(f'Foto de categoría {cat_k} eliminada.')
                            st.rerun()
                            
                    if st.button(f'💾 Guardar Cambios en {cat_k}', key=f'save_{cat_k}'):
                        app_data['categories'][cat_k]['desc'] = c_desc
                        if c_file:
                            app_data['categories'][cat_k]['img_b64'] = file_to_b64(c_file)
                        save_data(app_data)
                        st.success(f'Categoría "{cat_k}" actualizada.')
                        st.rerun()

        with t5:
            st.subheader('🖼️ Administrar Foto de Portada (Melo 1) y Fondo (Melo 2)')
            
            c_port1, c_port2 = st.columns(2)
            
            with c_port1:
                st.markdown('#### 1. Imagen de Portada Header (Melo 1)')
                hero_curr = app_data['cover_info'].get('hero_img_b64')
                if hero_curr:
                    st.image(hero_curr, caption='Portada Actual (Melo 1)', use_container_width=True)
                    if st.button('🗑️ Quitar Imagen de Portada'):
                        app_data['cover_info']['hero_img_b64'] = None
                        save_data(app_data)
                        st.success('Imagen de portada eliminada.')
                        st.rerun()
                else:
                    st.info('No hay imagen de portada activa.')
                    
                f_hero = st.file_uploader('Subir Nueva Imagen de Portada (Melo 1):', type=['jpg', 'png', 'jpeg', 'webp'], key='up_hero')
                if st.button('💾 Guardar Nueva Portada'):
                    if f_hero:
                        app_data['cover_info']['hero_img_b64'] = file_to_b64(f_hero)
                        save_data(app_data)
                        st.success('Imagen de portada actualizada.')
                        st.rerun()
                        
            with c_port2:
                st.markdown('#### 2. Imagen de Fondo de Pantalla (Melo 2)')
                bg_curr = app_data['cover_info'].get('bg_img_b64')
                if bg_curr:
                    st.image(bg_curr, caption='Fondo Actual (Melo 2)', use_container_width=True)
                    if st.button('🗑️ Quitar Imagen de Fondo'):
                        app_data['cover_info']['bg_img_b64'] = None
                        save_data(app_data)
                        st.success('Imagen de fondo eliminada.')
                        st.rerun()
                else:
                    st.info('No hay imagen de fondo activa.')
                    
                f_bg = st.file_uploader('Subir Nueva Imagen de Fondo (Melo 2):', type=['jpg', 'png', 'jpeg', 'webp'], key='up_bg')
                if st.button('💾 Guardar Nuevo Fondo'):
                    if f_bg:
                        app_data['cover_info']['bg_img_b64'] = file_to_b64(f_bg)
                        save_data(app_data)
                        st.success('Imagen de fondo actualizada.')
                        st.rerun()

        with t6:
            st.subheader('🔑 Configurar Clave Secreta del Admin')
            st.write(f'Clave actual: `{app_data.get("access_pin", "1234")}`')
            new_key = st.text_input('Ingresa la Nueva Clave:')
            if st.button('Cambiar Clave Secreta'):
                if new_key.strip():
                    app_data['access_pin'] = new_key.strip()
                    save_data(app_data)
                    st.success('¡Clave actualizada exitosamente!')
                    st.rerun()
                else:
                    st.error('La clave no puede estar vacía.')
