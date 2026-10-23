import streamlit as st
import pandas as pd
import datetime
import json
import os
import base64
import urllib.parse

def load_local_img(fname):
    paths = [fname, os.path.join('knowledge', fname), os.path.join('/workspace/knowledge', fname)]
    for p in paths:
        if os.path.exists(p):
            try:
                import base64
                with open(p, 'rb') as f:
                    return f'data:image/jpeg;base64,{base64.b64encode(f.read()).decode("utf-8")}'
            except Exception: pass
    return None

MELO1_DEFAULT = load_local_img('melo1.jpeg')
MELO2_DEFAULT = load_local_img('melo2.jpeg')


st.set_page_config(page_title="Melo's Beauty", page_icon='🌸', layout='wide')

CSS = '''
<style>
    .stApp { background-color: #FFF5F7; color: #2C2C2C; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .hero-banner { background: linear-gradient(135deg, #F8B8CC 0%, #F06292 100%); padding: 2.5rem; border-radius: 24px; text-align: center; color: white; border: 2px solid #F06292; margin-bottom: 2rem; box-shadow: 0px 8px 20px rgba(240, 98, 146, 0.25); }
    .hero-title { color: #FFFFFF; font-size: 2.8rem; font-weight: 800; }
    .hero-subtitle { color: #FFF0F5; font-size: 1.3rem; font-style: italic; }
    .hero-tag { background-color: rgba(255, 255, 255, 0.25); display: inline-block; padding: 6px 18px; border-radius: 30px; font-weight: 600; margin-top: 10px; color: #FFFFFF; }
    .product-card { background-color: #FFFFFF; border: 2px solid #F8B8CC; border-radius: 18px; padding: 1.2rem; margin-bottom: 1.5rem; box-shadow: 0px 6px 16px rgba(248, 184, 204, 0.2); }
    .product-title { color: #C2185B; font-size: 1.25rem; font-weight: 700; }
    .product-price { color: #C2185B; font-size: 1.4rem; font-weight: 800; }
    .product-img-container { width: 100%; height: 190px; border-radius: 14px; background-color: #FFF0F3; display: flex; align-items: center; justify-content: center; overflow: hidden; border: 1px solid #F8B8CC; }
    .product-img { width: 100%; height: 100%; object-fit: cover; }
    .stock-badge-green { background-color: #E8F5E9; color: #2E7D32; padding: 6px 12px; border-radius: 20px; font-size: 0.85rem; font-weight: 700; display: inline-block; margin-top: 5px; }
    .stock-badge-red { background-color: #FFEBEE; color: #C62828; padding: 6px 12px; border-radius: 20px; font-size: 0.85rem; font-weight: 700; display: inline-block; margin-top: 5px; }
    .btn-whatsapp { background-color: #25D366; color: white !important; padding: 10px 16px; border-radius: 25px; text-decoration: none; font-weight: bold; display: block; text-align: center; box-shadow: 0px 4px 10px rgba(37, 211, 102, 0.3); width: 100%; }
    .stButton>button { background-color: #F06292; color: white; border-radius: 20px; border: none; font-weight: bold; }
    .stButton>button:hover { background-color: #C2185B; color: white; }
</style>
'''
st.markdown(CSS, unsafe_allow_html=True)

DATA_FILE = 'catalogo_melos_data.json'

def get_default_data():
    return {
        'pin_secret': '1234',
        'cover_info': {
            'title': "Melo's Beauty 🌸",
            'slogan': 'La magia que resalta tu brillo diario ✨',
            'location': 'Tienda virtual de maquillaje y accesorios en Buenaventura 🎀',
            'phone': '+57 312 569 1563',
            'hero_img_b64': MELO1_DEFAULT, 'bg_img_b64': MELO2_DEFAULT
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
            {'id': 106, 'name': 'Billetera Bimba y Lola 1.1', 'category': 'Billeteras mujeres', 'price': 65900, 'stock': 6, 'desc': 'Billetera estilo 1.1 en tono rosa pastel.', 'img_b64': None},
            {'id': 107, 'name': 'Billetera Lacoste hombre 1.1', 'category': 'Billeteras hombres', 'price': 73700, 'stock': 4, 'desc': 'Billetera masculina elegante en cuerina premium.', 'img_b64': None}
        ],
        'reviews': [
            {'id': 1, 'client': 'Camila R.', 'rating': '⭐⭐⭐⭐⭐', 'comment': "Me encantó el Kit Melo's Beauty 1. Excelente servicio en Buenaventura.", 'date': '2026-10-15'},
            {'id': 2, 'client': 'Valeria M.', 'rating': '⭐⭐⭐⭐⭐', 'comment': 'El termo térmico de 1L mantiene el agua fría todo el día.', 'date': '2026-10-18'}
        ]
    }

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f: return json.load(f)
        except Exception: return get_default_data()
    else:
        d = get_default_data(); save_data(d); return d

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def file_to_b64(u):
    if u is None: return None
    return f'data:{u.type};base64,{base64.b64encode(u.getvalue()).decode("utf-8")}'

if 'app_data' not in st.session_state: st.session_state.app_data = load_data()
if 'admin_auth' not in st.session_state: st.session_state.admin_auth = False
app_data = st.session_state.app_data

st.sidebar.title("Melo's Beauty 🌸")
mode = st.sidebar.radio('Navegación:', ['🛍️ Catálogo Clientes', '🛒 Mi Pedido / Factura (Melo 3)', '🔐 Acceso Dueño / Admin'])
st.sidebar.markdown('---')
st.sidebar.subheader('Redes Sociales & Contacto')
phone_clean = app_data['cover_info']['phone'].replace('+', '').replace(' ', '')
st.sidebar.markdown(f'💬 WhatsApp: {app_data["cover_info"]["phone"]}')
st.sidebar.markdown('📸 Instagram: @melosbeauty_oficial')
st.sidebar.markdown('📘 Facebook: Melo Beauty')

if mode == '🛍️ Catálogo Clientes':
    if app_data['cover_info'].get('hero_img_b64'):
        st.markdown(f'<div style="text-align:center; margin-bottom:1.5rem;"><img src="{app_data["cover_info"]["hero_img_b64"]}" style="width:100%; max-height:280px; object-fit:cover; border-radius:20px; border:3px solid #F06292;"></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="hero-banner"><div class="hero-title">{app_data["cover_info"]["title"]}</div><div class="hero-subtitle">{app_data["cover_info"]["slogan"]}</div><div class="hero-tag">📍 {app_data["cover_info"]["location"]}</div></div>', unsafe_allow_html=True)
    col_s, col_c = st.columns(2)
    with col_s: q = st.text_input('🔍 Buscar producto:', placeholder='Ej: Kit, Termo, Billetera...')
    with col_c: cat = st.selectbox('🗂️ Categoría:', ['Todas'] + list(app_data['categories'].keys()))
    if cat != 'Todas' and cat in app_data['categories']:
        cat_info = app_data['categories'][cat]
        st.markdown(f'### 📂 Categoría: {cat}')
        cd, ci = st.columns([3, 1])
        with cd: st.info(f'**Descripción**: {cat_info["desc"]}')
        with ci:
            if cat_info.get('img_b64'): st.image(cat_info['img_b64'], caption=f'Perfil {cat}', use_container_width=True)
            else: st.markdown('<div style="background-color:#F8B8CC; padding:15px; border-radius:12px; text-align:center; color:white; font-weight:bold;">🌸 Foto Categoría</div>', unsafe_allow_html=True)
    st.markdown('---')
    prods = app_data['products']
    if cat != 'Todas': prods = [p for p in prods if p['category'] == cat]
    if q: prods = [p for p in prods if q.lower() in p['name'].lower() or q.lower() in p['desc'].lower()]
    st.subheader(f'✨ Todos los Productos ({len(prods)})')
    if not prods: st.info('No hay productos coincidentes.')
    else:
        cols = st.columns(3)
        for idx, p in enumerate(prods):
            with cols[idx % 3]:
                img_html = f'<img src="{p["img_b64"]}" class="product-img">' if p.get('img_b64') else f'<div style="text-align:center; font-size:2rem;">🛍️<br><span style="font-size:0.85rem; color:#C2185B;">{p["name"]}</span></div>'
                st.markdown(f'<div class="product-card"><div class="product-img-container">{img_html}</div><div class="product-title">{p["name"]}</div><div style="color:#666; font-size:0.85rem; margin-top:3px;">Categoría: <b>{p["category"]}</b></div><p style="color:#444; font-size:0.88rem; margin-top:6px; height:42px; overflow:hidden;">{p["desc"]}</p><div class="product-price">COP ${p["price"]:,}</div></div>', unsafe_allow_html=True)
                if p['stock'] > 5: st.markdown(f'<span class="stock-badge-green">✔ En Stock ({p["stock"]} dispon.)</span>', unsafe_allow_html=True)
                elif p['stock'] > 0: st.markdown(f'<span class="stock-badge-red">⚠️ ¡Pocas Unidades! ({p["stock"]})</span>', unsafe_allow_html=True)
                else: st.error('❌ Agotado temporalmente')
                wa_text = f"Hola Melo's Beauty! Quiero comprar {p['name']} por COP ${p['price']:,}".replace(' ', '%20')
                wa_link = f"https://wa.me/{phone_clean}?text={wa_text}"
                st.markdown(f'<a href="{wa_link}" target="_blank" class="btn-whatsapp">📲 Pedir por WhatsApp</a>', unsafe_allow_html=True)
                st.markdown('<br>', unsafe_allow_html=True)
    st.markdown('---')
    st.subheader('💬 Opiniones & Reseñas de Clientes')
    r1, r2 = st.columns([2, 1])
    with r1:
        for rev in app_data['reviews']:
            st.markdown(f'<div style="background-color:#FFFFFF; border:2px solid #F8B8CC; padding:1rem; border-radius:14px; margin-bottom:12px;"><strong>{rev["client"]}</strong> <span style="float:right;">{rev["rating"]}</span><br><small style="color:#888;">{rev["date"]}</small><p style="color:#2C2C2C; margin-top:6px;">"{rev["comment"]}"</p></div>', unsafe_allow_html=True)
    with r2:
        st.markdown('#### Deja tu Opinión')
        nn = st.text_input('Tu Nombre:')
        nr = st.selectbox('Calificación:', ['⭐⭐⭐⭐⭐', '⭐⭐⭐⭐', '⭐⭐⭐', '⭐⭐', '⭐'])
        nc = st.text_area('Comentario:')
        if st.button('Publicar Reseña'):
            if nn and nc:
                app_data['reviews'].append({'client': nn, 'rating': nr, 'comment': nc, 'date': datetime.date.today().strftime('%Y-%m-%d')})
                save_data(app_data); st.success('¡Gracias por tu reseña!'); st.rerun()
    st.markdown('---')
    with st.expander('🔒 Términos, Condiciones y Política de Seguridad'):
        st.write('''
        **Melo's Beauty - Buenaventura**
        - **Protección de Datos Personales**: Datos seguros conforme a la normativa.
        - **Envíos**: Envíos locales e itinerarios nacionales.
        - **Garantías**: Calidad garantizada.
        ''')
else:
    st.title('🔐 Panel Interno de Administración (Exclusivo Dueño)')
    if not st.session_state.admin_auth:
        st.info('Para acceder ingresa la clave de la tienda.')
        p_in = st.text_input('Ingresa PIN Secreto:')
        if st.button('Ingresar al Panel'):
            if p_in == app_data['pin_secret']:
                st.session_state.admin_auth = True; st.success('¡Bienvenido!'); st.rerun()
            else: st.error('Clave incorrecta')
    else:
        col_t, col_logout = st.columns([3, 1])
        with col_logout:
            if st.button('🔒 Cerrar Sesión Admin'): st.session_state.admin_auth = False; st.rerun()
        t1, t2, t3, t4, t5, t6 = st.tabs(['📊 Stock & Inventario', '📸 Subir Producto con Foto', '💬 Administrar Reseñas', '🗂️ Categorías & Fotos', '🖼️ Foto Portada (Melo 1 & 2)', '🔑 Configurar PIN'])
        with t1:
            df_prods = pd.DataFrame(app_data['products'])
            tot = (df_prods['price'] * df_prods['stock']).sum()
            m1, m2, m3 = st.columns(3)
            m1.metric('Total Productos', len(df_prods))
            m2.metric('Unidades Stock', df_prods['stock'].sum())
            m3.metric('Valor Inventario', f'COP ${tot:,.0f}')
            st.markdown('---')
            st.dataframe(df_prods[['id', 'name', 'category', 'price', 'stock', 'desc']], use_container_width=True)
            psel = st.selectbox('Producto a Modificar:', df_prods['id'].tolist(), format_func=lambda x: f'ID {x} - {df_prods[df_prods["id"]==x]["name"].values[0]}')
            nstk = st.number_input('Nuevo Stock:', min_value=0, value=int(df_prods[df_prods['id']==psel]['stock'].values[0]))
            if st.button('Guardar Stock'):
                for p in app_data['products']:
                    if p['id'] == psel: p['stock'] = nstk; break
                save_data(app_data); st.success('Stock actualizado'); st.rerun()
        with t2:
            st.subheader('📸 Agregar Nuevo Producto con Foto Real')
            with st.form('fp'):
                np_name = st.text_input('Nombre:')
                np_cat = st.selectbox('Categoría:', list(app_data['categories'].keys()))
                np_price = st.number_input('Precio COP:', min_value=0, value=50000, step=1000)
                np_stock = st.number_input('Stock Inicial:', min_value=0, value=10)
                np_desc = st.text_area('Descripción:')
                np_file = st.file_uploader('Subir Foto del Producto:', type=['jpg', 'png', 'jpeg', 'webp'])
                if st.form_submit_button('💾 Publicar Producto'):
                    if np_name and np_desc:
                        b64 = file_to_b64(np_file)
                        nid = max([p['id'] for p in app_data['products']], default=100) + 1
                        app_data['products'].append({'id': nid, 'name': np_name, 'category': np_cat, 'price': np_price, 'stock': np_stock, 'desc': np_desc, 'img_b64': b64})
                        save_data(app_data); st.success(f'¡Producto "{np_name}" publicado!'); st.rerun()
            st.markdown('---')
            del_id = st.selectbox('Eliminar Producto:', [p['id'] for p in app_data['products']], format_func=lambda x: f'ID {x} - {[p["name"] for p in app_data["products"] if p["id"]==x][0]}')
            if st.button('🗑️ Eliminar Producto'):
                app_data['products'] = [p for p in app_data['products'] if p['id'] != del_id]
                save_data(app_data); st.success('Producto eliminado'); st.rerun()
        with t3:
            st.subheader('🗂️ Categorías y Fotos de Perfil')
            for cat_k, cat_v in app_data['categories'].items():
                with st.expander(f'📁 {cat_k}'):
                    c_desc = st.text_area(f'Descripción {cat_k}:', value=cat_v['desc'], key=f'd_{cat_k}')
                    c_file = st.file_uploader(f'Foto perfil {cat_k}:', type=['jpg', 'png', 'jpeg', 'webp'], key=f'f_{cat_k}')
                    if cat_v.get('img_b64'): st.image(cat_v['img_b64'], width=140)
                    if st.button(f'Guardar {cat_k}', key=f'btn_{cat_k}'):
                        app_data['categories'][cat_k]['desc'] = c_desc
                        if c_file: app_data['categories'][cat_k]['img_b64'] = file_to_b64(c_file)
                        save_data(app_data); st.success('Categoría actualizada'); st.rerun()
        with t4:
            st.subheader('🖼️ Cambiar Imagen de Portada Banner')
            f_hero = st.file_uploader('Subir Foto Banner:', type=['jpg', 'png', 'jpeg', 'webp'])
            if app_data['cover_info'].get('hero_img_b64'): st.image(app_data['cover_info']['hero_img_b64'], caption='Portada Actual', use_container_width=True)
            if st.button('Guardar Portada'):
                if f_hero: app_data['cover_info']['hero_img_b64'] = file_to_b64(f_hero); save_data(app_data); st.success('Portada actualizada'); st.rerun()
        with t5:
            st.subheader('🔑 Configurar PIN')
            npin = st.text_input('Nuevo PIN:')
            if st.button('Cambiar PIN'):
                if npin:
                    app_data['pin_secret'] = npin
                    save_data(app_data); st.success('PIN actualizado')
