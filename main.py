import streamlit as st
import pandas as pd

# -----------------------------------------------------------------------------
# 1. Configuración inicial de la página
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Gestor de Catálogo y Tienda Melo's Beauty",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# 2. Configuración de Marca de Agua y Estilos CSS
# -----------------------------------------------------------------------------
# Ruta de la imagen de fondo de marca de agua
MELO2_DEFAULT = "melo2.jpeg"

# NOTA IMPORTANTE: Para evitar el error NameError en Python con f-strings, 
# se usan llaves dobles {{ y }} para las reglas CSS y llaves simples {MELO2_DEFAULT} 
# únicamente para insertar la variable de Python.
STYLING_CSS = f"""
<style>
/* Fondo general con marca de agua melo2.jpeg y capa semi-transparente rosada */
.stApp {{
    background: linear-gradient(rgba(255, 245, 247, 0.92), rgba(255, 245, 247, 0.92)), url("{MELO2_DEFAULT}") repeat center center fixed;
    background-size: cover;
    color: #2C2C2C;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}}

/* Tarjetas para exhibición de productos */
.product-card {{
    background-color: #FFFFFF;
    border-radius: 12px;
    padding: 20px;
    box-shadow: 0 4px 12px rgba(230, 115, 159, 0.15);
    border: 1px solid #FAD2E1;
    margin-bottom: 20px;
    text-align: center;
    transition: transform 0.2s ease;
}}

.product-card:hover {{
    transform: translateY(-4px);
    box-shadow: 0 6px 16px rgba(230, 115, 159, 0.25);
}}

.product-title {{
    color: #D81B60;
    font-weight: 700;
    font-size: 1.15rem;
    margin-top: 8px;
    margin-bottom: 6px;
}}

.product-price {{
    color: #C2185B;
    font-weight: 800;
    font-size: 1.25rem;
    margin-bottom: 8px;
}}

.product-cat {{
    background-color: #FCE4EC;
    color: #880E4F;
    padding: 4px 10px;
    border-radius: 12px;
    font-size: 0.8rem;
    font-weight: 600;
}}

/* Barra lateral estilizada */
[data-testid="stSidebar"] {{
    background-color: #FFF0F5;
    border-right: 1px solid #F8BBD0;
}}

#MainMenu {{visibility: hidden;}}
footer {{visibility: hidden;}}
</style>
"""

st.markdown(STYLING_CSS, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 3. Estado de la Sesión (Base de datos en memoria)
# -----------------------------------------------------------------------------
if "productos" not in st.session_state:
    st.session_state["productos"] = [
        {
            "id": 1,
            "nombre": "Sérum Hidratante Ácido Hialurónico",
            "categoria": "Cuidado Facial",
            "precio": 24.99,
            "stock": 15,
            "descripcion": "Sérum intensivo para hidratación profunda y resplandor natural."
        },
        {
            "id": 2,
            "nombre": "Labial Humectante Rosa Velvet",
            "categoria": "Maquillaje",
            "precio": 14.50,
            "stock": 25,
            "descripcion": "Labial acabado mate aterciopelado con manteca de karité."
        },
        {
            "id": 3,
            "nombre": "Paleta de Sombras Rose Gold",
            "categoria": "Maquillaje",
            "precio": 32.00,
            "stock": 10,
            "descripcion": "12 tonos pigmentados en acabados mates y satinados."
        },
        {
            "id": 4,
            "nombre": "Crema Contorno de Ojos Anti-Edad",
            "categoria": "Cuidado Facial",
            "precio": 28.75,
            "stock": 8,
            "descripcion": "Fórmula reafirmante con péptidos y cafeína."
        },
        {
            "id": 5,
            "nombre": "Aceite Esencial Corporal de Lavanda",
            "categoria": "Cuidado Corporal",
            "precio": 19.99,
            "stock": 18,
            "descripcion": "Aceite relajante para masaje y nutrición profunda de la piel."
        }
    ]

if "carrito" not in st.session_state:
    st.session_state["carrito"] = []

# -----------------------------------------------------------------------------
# 4. Navegación en la Barra Lateral
# -----------------------------------------------------------------------------
st.sidebar.title("🌸 Melo's Beauty")
st.sidebar.caption("Gestor de Tienda & Catálogo")

opcion_menu = st.sidebar.radio(
    "Menú Principal",
    ["🛍️ Catálogo y Tienda", "➕ Agregar Producto", "📦 Gestión de Inventario", "🛒 Carrito de Compras"]
)

st.sidebar.markdown("---")
total_items_carrito = sum(item["cantidad"] for item in st.session_state["carrito"])
st.sidebar.write(f"🛒 **Productos en carrito:** {total_items_carrito}")

# -----------------------------------------------------------------------------
# 5. Vista 1: Catálogo y Tienda
# -----------------------------------------------------------------------------
if opcion_menu == "🛍️ Catálogo y Tienda":
    st.title("🌸 Catálogo de Productos Melo's Beauty")
    st.write("Explora nuestra selección exclusiva de productos de belleza y cuidado personal.")

    # Buscador y filtro por categoría
    col_search, col_cat = st.columns([2, 1])
    with col_search:
        busqueda = st.text_input("🔍 Buscar producto por nombre...", "")
    with col_cat:
        categorias = ["Todas"] + sorted(list(set(p["categoria"] for p in st.session_state["productos"])))
        categoria_sel = st.selectbox("Filtrar por Categoría", categorias)

    # Filtrar catálogo
    prods_filtrados = [
        p for p in st.session_state["productos"]
        if (busqueda.lower() in p["nombre"].lower() or busqueda.lower() in p["descripcion"].lower())
        and (categoria_sel == "Todas" or p["categoria"] == categoria_sel)
    ]

    if not prods_filtrados:
        st.info("No se encontraron productos que coincidan con la búsqueda.")
    else:
        cols = st.columns(3)
        for i, prod in enumerate(prods_filtrados):
            col = cols[i % 3]
            with col:
                st.markdown(f"""
                <div class="product-card">
                    <div class="product-title">{prod['nombre']}</div>
                    <span class="product-cat">{prod['categoria']}</span>
                    <div class="product-price">${prod['precio']:.2f} USD</div>
                    <p style="font-size:0.88rem; color:#555; height:45px; overflow:hidden;">{prod['descripcion']}</p>
                    <p style="font-size:0.85rem; font-weight:bold; color: {'#2E7D32' if prod['stock'] > 5 else '#D32F2F'};">
                        Stock disponible: {prod['stock']} uds
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"➕ Añadir al Carrito", key=f"btn_add_{prod['id']}"):
                    item_existente = next((item for item in st.session_state["carrito"] if item["id"] == prod["id"]), None)
                    if item_existente:
                        if item_existente["cantidad"] < prod["stock"]:
                            item_existente["cantidad"] += 1
                            st.success(f"Añadida otra unidad de '{prod['nombre']}'.")
                        else:
                            st.warning("No hay suficiente stock disponible.")
                    else:
                        if prod["stock"] > 0:
                            st.session_state["carrito"].append({
                                "id": prod["id"],
                                "nombre": prod["nombre"],
                                "precio": prod["precio"],
                                "cantidad": 1
                            })
                            st.success(f"'{prod['nombre']}' añadido al carrito.")
                        else:
                            st.error("Producto agotado.")

# -----------------------------------------------------------------------------
# 6. Vista 2: Agregar Producto
# -----------------------------------------------------------------------------
elif opcion_menu == "➕ Agregar Producto":
    st.title("➕ Registrar Nuevo Producto")
    st.write("Ingresa los datos del nuevo artículo para integrarlo al catálogo.")

    with st.form("form_nuevo_producto", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            nombre = st.text_input("Nombre del Producto*", placeholder="Ej. Tónico Facial Hidratante")
            categoria = st.selectbox("Categoría*", ["Cuidado Facial", "Maquillaje", "Cuidado Corporal", "Capilar", "Accesorios"])
            precio = st.number_input("Precio ($ USD)*", min_value=0.0, value=15.0, step=0.50)
        with col2:
            stock = st.number_input("Stock Inicial*", min_value=0, value=10, step=1)
            descripcion = st.text_area("Descripción del Producto", placeholder="Detalla los beneficios del producto...")

        btn_guardar = st.form_submit_button("🌸 Guardar Producto")

        if btn_guardar:
            if not nombre.strip():
                st.error("Por favor, ingresa un nombre válido para el producto.")
            else:
                nuevo_id = max([p["id"] for p in st.session_state["productos"]], default=0) + 1
                nuevo_prod = {
                    "id": nuevo_id,
                    "nombre": nombre.strip(),
                    "categoria": categoria,
                    "precio": float(precio),
                    "stock": int(stock),
                    "descripcion": descripcion.strip()
                }
                st.session_state["productos"].append(nuevo_prod)
                st.balloons()
                st.success(f"¡El producto '{nombre}' se registró exitosamente con ID #{nuevo_id}!")

# -----------------------------------------------------------------------------
# 7. Vista 3: Gestión de Inventario
# -----------------------------------------------------------------------------
elif opcion_menu == "📦 Gestión de Inventario":
    st.title("📦 Inventario de Melo's Beauty")
    st.write("Visualiza, edita y audita el catálogo completo.")

    df_prods = pd.DataFrame(st.session_state["productos"])
    
    # Métricas clave
    col_m1, col_m2, col_m3 = st.columns(3)
    col_m1.metric("Total Productos", len(df_prods))
    col_m2.metric("Valor Total Inventario", f"${(df_prods['precio'] * df_prods['stock']).sum():,.2f}")
    col_m3.metric("Stock Total (Unidades)", int(df_prods['stock'].sum()))

    st.markdown("### Tabla de Productos")
    st.dataframe(
        df_prods[["id", "nombre", "categoria", "precio", "stock", "descripcion"]],
        use_container_width=True,
        hide_index=True
    )

    st.markdown("---")
    st.markdown("### 🗑️ Eliminar Producto")
    col_del_id, col_del_btn = st.columns([3, 1])
    with col_del_id:
        prod_del_id = st.selectbox(
            "Selecciona producto a eliminar por ID:",
            options=[p["id"] for p in st.session_state["productos"]],
            format_func=lambda x: f"ID #{x} - {next((p['nombre'] for p in st.session_state['productos'] if p['id'] == x), '')}"
        )
    with col_del_btn:
        st.write(" ")
        st.write(" ")
        if st.button("Eliminar", type="primary"):
            st.session_state["productos"] = [p for p in st.session_state["productos"] if p["id"] != prod_del_id]
            st.warning(f"Producto ID #{prod_del_id} eliminado.")
            st.rerun()

# -----------------------------------------------------------------------------
# 8. Vista 4: Carrito de Compras
# -----------------------------------------------------------------------------
elif opcion_menu == "🛒 Carrito de Compras":
    st.title("🛒 Carrito de Compras")
    
    if not st.session_state["carrito"]:
        st.info("El carrito está vacío. Agrega productos desde la pestaña 🛍️ Catálogo y Tienda.")
    else:
        df_carrito = pd.DataFrame(st.session_state["carrito"])
        df_carrito["subtotal"] = df_carrito["precio"] * df_carrito["cantidad"]
        
        st.dataframe(
            df_carrito[["nombre", "precio", "cantidad", "subtotal"]],
            use_container_width=True,
            hide_index=True
        )
        
        total_compra = df_carrito["subtotal"].sum()
        
        col_tot, col_proc = st.columns([2, 1])
        with col_tot:
            st.subheader(f"Total a pagar: **${total_compra:,.2f} USD**")
        with col_proc:
            if st.button("💳 Procesar Pedido", type="primary"):
                # Descontar stock de inventario
                for item in st.session_state["carrito"]:
                    for prod in st.session_state["productos"]:
                        if prod["id"] == item["id"]:
                            prod["stock"] -= item["cantidad"]
                
                st.session_state["carrito"] = []
                st.balloons()
                st.success("¡Pedido procesado con éxito! Gracias por elegir Melo's Beauty.")
                st.rerun()

        if st.button("🔴 Vaciar Carrito"):
            st.session_state["carrito"] = []
            st.info("El carrito ha sido vaciado.")
            st.rerun()
