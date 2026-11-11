
import html as _html
import re
from datetime import date, datetime, time

import oracledb
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Mesa Medellín", page_icon="🍽️", layout="wide")

# =====================================================
# PALETA, FOTOS Y AYUDAS
# =====================================================
C = {"espresso": "#2B1D14", "terracota": "#D9643A", "oro": "#E8B04B",
     "salvia": "#6B8F71", "vino": "#8E2C3A", "azul": "#4A6FA5", "ambar": "#E39B3B"}

ESTADO_COLOR = {"CONFIRMADA": C["salvia"], "COMPLETADA": C["azul"],
                "CANCELADA": C["vino"], "NO ASISTIO": C["ambar"]}
ESTADO_TXT = {"CONFIRMADA": "Confirmada", "COMPLETADA": "Completada",
              "CANCELADA": "Cancelada", "NO ASISTIO": "No asistió"}
REST_COLOR = {"ACTIVO": C["salvia"], "EN MANTENIMIENTO": C["ambar"], "INACTIVO": C["vino"]}
TIPO_COLOR = {"VIP": C["oro"], "FRECUENTE": C["terracota"], "OCASIONAL": C["salvia"]}
MESES = ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"]

UNSPLASH = "https://images.unsplash.com/{}?auto=format&fit=crop&w=900&q=70"
FOTOS = {
    "Autor": "photo-1414235077428-338989a2e8c0",
    "Colombiana": "photo-1504674900247-0877df9cc836",
    "Fusión": "photo-1540189549336-e6e99c3679fe",
    "Italiana": "photo-1565299624946-b28f40a0ae38",
    "Argentina": "photo-1544025162-d76694265947",
    "Café y Brunch": "photo-1495474472287-4d71bcdd2085",
    "Carnes": "photo-1600891964092-4316c288032e",
}
FOTO_DEFAULT = "photo-1517248135467-4c7edcad34c4"
FOTO_HERO = "photo-1555396273-367ea4eb4db5"

esc = _html.escape


def foto(cocina):
    return UNSPLASH.format(FOTOS.get(cocina, FOTO_DEFAULT))


def fondo(url, oscuro=0.1):
    # Si la foto no carga, se ve el degradé de abajo
    return (f"background-image: linear-gradient(rgba(43,29,20,{oscuro}), rgba(43,29,20,{oscuro + 0.45})), "
            f"url('{url}'), linear-gradient(135deg, #D9643A, #E8B04B);")


def render(s: str):
    st.markdown("".join(line.strip() for line in s.splitlines()), unsafe_allow_html=True)


def pill(texto, color):
    return f'<span class="pill" style="background:{color}22;color:{color}">● {esc(texto)}</span>'


def fecha_txt(dt):
    return f"{dt.day} {MESES[dt.month - 1]} {dt.year} · {dt:%H:%M}"


def page_head(eyebrow, titulo, sub):
    render(f"""<div class="page-head"><div class="eyebrow">{eyebrow}</div>
    <h1>{titulo}</h1><p>{sub}</p></div>""")


# =====================================================
# ESTILOS
# =====================================================
render("""<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,500;0,700;0,800;1,600&family=DM+Sans:wght@400;500;600;700&display=swap');
html, body, .stApp, p, label, input, textarea, button, li, td, th, div[data-testid="stMarkdownContainer"] {font-family:'DM Sans',sans-serif;}
h1, h2, h3, h4 {font-family:'Playfair Display',serif !important;}
.stApp {background: radial-gradient(circle at 0% 0%, #FDEBD8 0%, #FBF5EC 45%, #F6EDE2 100%);}
#MainMenu, footer {visibility:hidden;}
header[data-testid="stHeader"] {background:transparent;}
.block-container {padding-top:2rem; max-width:1320px;}
@keyframes fadeUp {from{opacity:0;transform:translateY(18px)} to{opacity:1;transform:none}}

section[data-testid="stSidebar"] {background:linear-gradient(180deg,#2B1D14 0%,#160E0A 100%);}
section[data-testid="stSidebar"] p, section[data-testid="stSidebar"] label {color:#F6E7D8;}
section[data-testid="stSidebar"] div[role="radiogroup"] {gap:6px;}
section[data-testid="stSidebar"] div[role="radiogroup"] label {padding:12px 16px;border-radius:14px;transition:all .25s;width:100%;cursor:pointer;}
section[data-testid="stSidebar"] div[role="radiogroup"] label:hover {background:rgba(232,176,75,.14);}
section[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) {background:linear-gradient(90deg,#D9643A,#E8B04B);box-shadow:0 8px 20px rgba(217,100,58,.35);}
section[data-testid="stSidebar"] div[role="radiogroup"] label > div:first-child {display:none;}
section[data-testid="stSidebar"] div[role="radiogroup"] label p {font-size:1rem;font-weight:500;}
.brand {padding:6px 4px 22px;border-bottom:1px solid rgba(246,231,216,.12);margin-bottom:18px;}
.brand .logo {font-family:'Playfair Display',serif;font-size:1.9rem;color:#fff;font-weight:700;line-height:1;}
.brand .logo em {color:#E8B04B;}
.brand small {color:#B89C88;letter-spacing:.25em;text-transform:uppercase;font-size:.66rem;}
.side-foot {margin-top:40px;padding:16px;border-radius:16px;background:rgba(232,176,75,.1);color:#E9D5C2;font-size:.85rem;}

.hero {border-radius:30px;padding:70px 60px;color:white;background-size:cover;background-position:center;box-shadow:0 24px 60px rgba(43,29,20,.28);margin-bottom:30px;animation:fadeUp .8s ease;}
.hero .eyebrow {letter-spacing:.3em;text-transform:uppercase;font-size:.78rem;color:#E8B04B;font-weight:700;}
.hero h1 {font-size:3.8rem;line-height:1.05;margin:.4rem 0 .6rem;color:white;font-weight:800;}
.hero h1 em {color:#E8B04B;}
.hero p {font-size:1.15rem;opacity:.92;max-width:560px;color:white;margin:0;}

.page-head {margin:4px 0 26px;animation:fadeUp .6s ease;}
.page-head .eyebrow, .sec .eyebrow {color:#D9643A;letter-spacing:.28em;text-transform:uppercase;font-size:.74rem;font-weight:700;}
.page-head h1 {font-size:2.8rem;color:#2B1D14;margin:.2rem 0 0;}
.page-head p {color:#7A6355;margin:.3rem 0 0;font-size:1.05rem;}
.sec {margin:34px 0 14px;}
.sec h3 {margin:.1rem 0 0;color:#2B1D14;font-size:1.7rem;}

.kpis {display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:18px;margin-bottom:18px;}
.kpi {background:white;border-radius:22px;padding:22px 24px;box-shadow:0 8px 24px rgba(43,29,20,.07);border:1px solid #F1E3D3;transition:transform .25s, box-shadow .25s;animation:fadeUp .7s ease both;}
.kpi:hover {transform:translateY(-5px);box-shadow:0 18px 36px rgba(43,29,20,.13);}
.kpi .ico {width:48px;height:48px;border-radius:15px;display:grid;place-items:center;font-size:1.4rem;margin-bottom:14px;}
.kpi .val {font-family:'Playfair Display',serif;font-size:2.3rem;font-weight:700;color:#2B1D14;line-height:1;}
.kpi .lbl {color:#8A7466;font-size:.9rem;margin-top:6px;}

.grid {display:grid;grid-template-columns:repeat(auto-fill,minmax(270px,1fr));gap:22px;}
.card {background:white;border-radius:22px;overflow:hidden;box-shadow:0 8px 24px rgba(43,29,20,.07);border:1px solid #F1E3D3;transition:transform .3s, box-shadow .3s;animation:fadeUp .6s ease both;}
.card:hover {transform:translateY(-7px);box-shadow:0 22px 44px rgba(43,29,20,.16);}
.card-img {height:160px;background-size:cover;background-position:center;position:relative;}
.chip {position:absolute;top:14px;left:14px;background:rgba(255,255,255,.93);color:#2B1D14;padding:5px 12px;border-radius:999px;font-size:.78rem;font-weight:600;}
.card-body {padding:18px 20px 20px;}
.card-body h4 {margin:0 0 4px;font-size:1.35rem;color:#2B1D14;}
.muted {color:#8A7466;font-size:.88rem;margin:0;}
.meta {display:flex;gap:14px;flex-wrap:wrap;margin:12px 0;color:#4A3A30;font-size:.9rem;}
.pill {display:inline-block;padding:5px 12px;border-radius:999px;font-size:.78rem;font-weight:700;margin-right:4px;}
.person {display:flex;gap:14px;align-items:center;padding:20px;}
.avatar {width:56px;height:56px;border-radius:50%;display:grid;place-items:center;font-weight:700;color:white;font-size:1.15rem;font-family:'Playfair Display',serif;flex-shrink:0;}
.zona-top {height:110px;display:flex;align-items:flex-end;padding:16px 20px;font-size:2rem;}
.stars {color:#E8B04B;letter-spacing:2px;}

.ticket {background:linear-gradient(160deg,#2B1D14,#4A2F22);color:#F6E7D8;border-radius:26px;overflow:hidden;box-shadow:0 24px 50px rgba(43,29,20,.3);animation:fadeUp .6s ease;}
.ticket .card-img {height:190px;}
.ticket-body {padding:24px 26px 26px;}
.ticket .eyebrow {color:#E8B04B;letter-spacing:.28em;text-transform:uppercase;font-size:.7rem;font-weight:700;}
.ticket h3 {color:white;margin:.3rem 0 1rem;font-size:1.8rem;}
.ticket .line {display:flex;justify-content:space-between;padding:10px 0;border-bottom:1px dashed rgba(246,231,216,.2);font-size:.95rem;}
.ticket .line span:first-child {color:#B89C88;}
.ticket .total {display:flex;justify-content:space-between;align-items:baseline;margin-top:16px;}
.ticket .total b {font-family:'Playfair Display',serif;font-size:2rem;color:#E8B04B;}

div[data-testid="stVerticalBlockBorderWrapper"] {background:white;border-radius:22px !important;border:1px solid #F1E3D3 !important;box-shadow:0 8px 24px rgba(43,29,20,.06);}
.stButton > button {border-radius:999px;padding:.6rem 1.4rem;font-weight:600;transition:all .25s;}
.stButton > button:hover {transform:translateY(-2px);box-shadow:0 10px 22px rgba(217,100,58,.28);}
div[data-baseweb="select"] > div, div[data-baseweb="input"] {border-radius:12px !important;}
.stTabs [data-baseweb="tab"] p {font-weight:600;font-size:1.02rem;}
textarea {font-family:'SFMono-Regular',Menlo,monospace !important;font-size:.92rem !important;}
</style>""")


# =====================================================
# BASE DE DATOS
# =====================================================
def get_conn():
    s = st.secrets["oracle"]
    return oracledb.connect(
        user=s["user"], password=s["password"], dsn=s["dsn"],
        config_dir=s["wallet_dir"], wallet_location=s["wallet_dir"],
        wallet_password=s["wallet_password"],
    )


@st.cache_data(ttl=60, show_spinner=False)
def run_query(sql: str) -> pd.DataFrame:
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
            cols = [c[0].lower() for c in cur.description]
            return pd.DataFrame(cur.fetchall(), columns=cols)


def consulta_libre(sql: str) -> pd.DataFrame:
    # Sin caché, para que siempre traiga datos frescos
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
            cols = [c[0].lower() for c in cur.description]
            return pd.DataFrame(cur.fetchall(), columns=cols)


def run_dml(sql: str, params: dict):
    with get_conn() as conn:
        with conn.cursor() as cur:
            try:
                cur.execute(sql, params)
                filas = cur.rowcount
                conn.commit()
            except Exception:
                conn.rollback()
                raise
    st.cache_data.clear()
    return filas


def load_reservas() -> pd.DataFrame:
    return run_query("""
        SELECT r.r_id_reserva AS id, u.u_nombre_completo AS cliente,
               rs.r_nombre AS restaurante, rs.r_tipo_cocina AS cocina,
               rs.r_capacidad_maxima AS capacidad, rs.r_precio_promedio AS precio,
               z.z_nombre_zona AS zona, r.r_fecha_hora AS fecha,
               r.r_numero_personas AS personas, r.r_deposito_reserva AS deposito,
               r.r_estado AS estado
        FROM reserva_restaurante r
        JOIN usuario u       ON u.u_id_usuario = r.r_id_usuario
        JOIN restaurante rs  ON rs.r_id_restaurante = r.r_id_restaurante
        JOIN zona_medellin z ON z.z_id_zona = r.r_id_zona
        ORDER BY r.r_fecha_hora DESC
    """)


# =====================================================
# GRÁFICAS Y TARJETAS
# =====================================================
def chart(fig, h=340):
    fig.update_layout(
        height=h, font=dict(family="DM Sans", color="#4A3A30", size=13),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=10, b=10),
        legend=dict(orientation="h", y=-0.18, title=None),
        hoverlabel=dict(bgcolor="white", font_family="DM Sans", bordercolor="#F1E3D3"),
    )
    fig.update_xaxes(showgrid=False, title=None)
    fig.update_yaxes(gridcolor="#F3E6D6", title=None)
    st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})


def reserva_card(r):
    return f"""<div class="card">
    <div class="card-img" style="{fondo(foto(r.cocina))}height:130px"><span class="chip">#{r.id} · {esc(r.zona)}</span></div>
    <div class="card-body"><h4>{esc(r.restaurante)}</h4><p class="muted">{esc(r.cliente)}</p>
    <div class="meta"><span>📅 {fecha_txt(r.fecha)}</span><span>👥 {r.personas}</span><span>💳 ${r.deposito:,.0f}</span></div>
    {pill(ESTADO_TXT[r.estado], ESTADO_COLOR[r.estado])}</div></div>"""


def grid(cards):
    render('<div class="grid">' + "".join(cards) + "</div>")


# =====================================================
# MENÚ LATERAL
# =====================================================
with st.sidebar:
    render("""<div class="brand"><div class="logo">Mesa <em>Medellín</em></div>
    <small>Reservas gourmet</small></div>""")
    page = st.radio("Menú", ["✨  Inicio", "📖  Reservas", "🍷  Nueva reserva",
                             "🛠️  Gestionar", "🗺️  Explorar", "🗂️  Tablas",
                             "💻  Consultas SQL"], label_visibility="collapsed")
    render("""<div class="side-foot">🍽️ Encuentra tu mesa ideal en los mejores
    restaurantes de la ciudad de la eterna primavera.</div>""")

if msg := st.session_state.pop("flash", None):
    st.toast(msg, icon="✨")
if st.session_state.pop("fiesta", False):
    st.balloons()

try:
    df = load_reservas()
except Exception as e:
    st.error(f"No se pudo conectar a la base de datos: {e}")
    st.stop()

# =====================================================
# INICIO
# =====================================================
if page.endswith("Inicio"):
    render(f"""<div class="hero" style="{fondo(UNSPLASH.format(FOTO_HERO), 0.35)}">
    <div class="eyebrow">Medellín · Gastronomía</div>
    <h1>Tu mesa perfecta,<br><em>a un clic.</em></h1>
    <p>Descubre, reserva y gestiona experiencias en los restaurantes más especiales de la ciudad.</p></div>""")

    total = len(df)
    confirmadas = int((df["estado"] == "CONFIRMADA").sum())
    comensales = int(df.loc[df["estado"] != "CANCELADA", "personas"].sum())
    depositos = float(df.loc[df["estado"] != "CANCELADA", "deposito"].sum())
    kpis = [
        ("📅", "#D9643A", total, "Reservas totales"),
        ("✅", "#6B8F71", confirmadas, "Confirmadas"),
        ("👥", "#4A6FA5", comensales, "Comensales"),
        ("💰", "#E8B04B", f"${depositos / 1000:,.0f}K", "Depósitos recibidos"),
    ]
    render('<div class="kpis">' + "".join(
        f'<div class="kpi" style="animation-delay:{i * .1}s"><div class="ico" style="background:{col}22">{ico}</div>'
        f'<div class="val">{val}</div><div class="lbl">{lbl}</div></div>'
        for i, (ico, col, val, lbl) in enumerate(kpis)) + "</div>")

    render('<div class="sec"><div class="eyebrow">Análisis</div><h3>Así se mueven las reservas</h3></div>')
    g1, g2 = st.columns([2, 3])
    with g1, st.container(border=True):
        st.markdown("**Estado de las reservas**")
        est = df["estado"].map(ESTADO_TXT).value_counts().reset_index()
        est.columns = ["estado", "cantidad"]
        fig = px.pie(est, names="estado", values="cantidad", hole=.62,
                     color="estado", color_discrete_map={ESTADO_TXT[k]: v for k, v in ESTADO_COLOR.items()})
        fig.update_traces(textinfo="percent", hovertemplate="%{label}: %{value} reservas<extra></extra>")
        chart(fig)
    with g2, st.container(border=True):
        st.markdown("**Comensales por restaurante**")
        por_rest = df.groupby("restaurante", as_index=False)["personas"].sum().sort_values("personas")
        fig = px.bar(por_rest, x="personas", y="restaurante", orientation="h",
                     color="personas", color_continuous_scale=["#F6D7B8", "#D9643A", "#8E2C3A"])
        fig.update_traces(marker_cornerradius=8, hovertemplate="%{y}: %{x} personas<extra></extra>")
        fig.update_layout(coloraxis_showscale=False)
        chart(fig)

    with st.container(border=True):
        st.markdown("**Línea de tiempo** · pasa el mouse sobre cada burbuja")
        fig = px.scatter(df.assign(estado_txt=df["estado"].map(ESTADO_TXT)), x="fecha", y="zona",
                         size="personas", color="estado_txt", size_max=34,
                         color_discrete_map={ESTADO_TXT[k]: v for k, v in ESTADO_COLOR.items()},
                         hover_name="restaurante",
                         hover_data={"cliente": True, "personas": True, "estado_txt": False,
                                     "zona": False, "fecha": "|%d/%m %H:%M"})
        fig.update_traces(marker=dict(line=dict(width=2, color="white"), opacity=.9))
        chart(fig, 320)

    render('<div class="sec"><div class="eyebrow">Agenda</div><h3>Próximas reservas</h3></div>')
    proximas = df[(df["estado"] == "CONFIRMADA") & (df["fecha"] >= datetime.now())].sort_values("fecha").head(4)
    if proximas.empty:
        st.info("No hay reservas próximas.")
    else:
        grid(reserva_card(r) for r in proximas.itertuples())

# =====================================================
# RESERVAS
# =====================================================
elif page.endswith("Reservas"):
    page_head("Historial", "Todas las reservas", "Filtra, busca y explora cada reserva.")
    f1, f2, f3, f4 = st.columns([3, 2, 2, 1.4])
    estados_sel = f1.multiselect("Estado", list(ESTADO_TXT), default=list(ESTADO_TXT), format_func=ESTADO_TXT.get)
    rest_sel = f2.selectbox("Restaurante", ["Todos"] + sorted(df["restaurante"].unique()))
    buscar = f3.text_input("Buscar cliente", placeholder="Ej: María")
    modo = f4.segmented_control("Vista", ["🃏 Tarjetas", "📊 Tabla"], default="🃏 Tarjetas") or "🃏 Tarjetas"

    vista = df[df["estado"].isin(estados_sel)]
    if rest_sel != "Todos":
        vista = vista[vista["restaurante"] == rest_sel]
    if buscar:
        vista = vista[vista["cliente"].str.contains(buscar, case=False, na=False)]

    st.caption(f"{len(vista)} reserva(s) encontradas")
    if vista.empty:
        st.info("No hay reservas con esos filtros.")
    elif modo.endswith("Tarjetas"):
        grid(reserva_card(r) for r in vista.itertuples())
    else:
        st.dataframe(
            vista[["id", "cliente", "restaurante", "zona", "fecha", "personas", "deposito", "estado"]]
            .assign(estado=vista["estado"].map(ESTADO_TXT)),
            hide_index=True, width="stretch",
            column_config={
                "fecha": st.column_config.DatetimeColumn(format="DD/MM/YYYY HH:mm"),
                "deposito": st.column_config.NumberColumn(format="$ %d"),
                "personas": st.column_config.ProgressColumn(min_value=0, max_value=10, format="%d"),
            },
        )

# =====================================================
# NUEVA RESERVA
# =====================================================
elif page.endswith("Nueva reserva"):
    page_head("Reservar", "Crea una nueva reserva", "Elige el lugar, la fecha y prepárate para disfrutar.")
    usuarios = run_query("SELECT u_id_usuario AS id, u_nombre_completo AS nombre, u_tipo_cliente AS tipo "
                         "FROM usuario WHERE u_estado = 'ACTIVO' ORDER BY u_nombre_completo")
    restaurantes = run_query("SELECT r_id_restaurante AS id, r_nombre AS nombre, r_tipo_cocina AS cocina, "
                             "r_capacidad_maxima AS capacidad, r_precio_promedio AS precio, r_direccion AS direccion "
                             "FROM restaurante WHERE r_estado = 'ACTIVO' ORDER BY r_nombre")
    zonas = run_query("SELECT z_id_zona AS id, z_nombre_zona AS nombre FROM zona_medellin "
                      "WHERE z_estado = 'HABILITADA' ORDER BY z_nombre_zona")
    nom_u = dict(zip(usuarios["id"], usuarios["nombre"]))
    nom_z = dict(zip(zonas["id"], zonas["nombre"]))
    rest = restaurantes.set_index("id")

    izq, der = st.columns([3, 2], gap="large")
    with izq, st.container(border=True):
        restaurante = st.selectbox("🍴 Restaurante", rest.index.tolist(),
                                   format_func=lambda i: f"{rest.at[i, 'nombre']} · {rest.at[i, 'cocina']}")
        c1, c2 = st.columns(2)
        cliente = c1.selectbox("👤 Cliente", usuarios["id"].tolist(), format_func=nom_u.get)
        zona = c2.selectbox("📍 Zona", zonas["id"].tolist(), format_func=nom_z.get)
        c3, c4 = st.columns(2)
        fecha = c3.date_input("📅 Fecha", min_value=date.today(), format="DD/MM/YYYY")
        hora = c4.time_input("🕗 Hora", value=time(20, 0), step=1800)
        capacidad = int(rest.at[restaurante, "capacidad"])
        personas = st.slider("👥 Número de personas", 1, min(capacidad, 20), 2)
        deposito = st.number_input("💳 Depósito (COP)", min_value=0, value=0, step=5000)
        st.write("")
        enviar = st.button("Confirmar reserva ✨", type="primary", width="stretch")

    r = rest.loc[restaurante]
    estimado = float(r["precio"]) * personas
    with der:
        render(f"""<div class="ticket">
        <div class="card-img" style="{fondo(foto(r['cocina']), 0.05)}"><span class="chip">{esc(r['cocina'])}</span></div>
        <div class="ticket-body"><div class="eyebrow">Tu reserva</div><h3>{esc(r['nombre'])}</h3>
        <div class="line"><span>Cliente</span><span>{esc(nom_u.get(cliente, ''))}</span></div>
        <div class="line"><span>Zona</span><span>{esc(nom_z.get(zona, ''))}</span></div>
        <div class="line"><span>Fecha</span><span>{fecha_txt(datetime.combine(fecha, hora))}</span></div>
        <div class="line"><span>Personas</span><span>{personas}</span></div>
        <div class="line"><span>Depósito</span><span>${deposito:,.0f}</span></div>
        <div class="total"><span>Costo estimado</span><b>${estimado:,.0f}</b></div>
        </div></div>""")

    if enviar:
        fecha_hora = datetime.combine(fecha, hora)
        if fecha_hora < datetime.now():
            st.error("La fecha y hora deben ser futuras.")
        else:
            run_dml("""INSERT INTO reserva_restaurante
                (r_id_usuario, r_id_restaurante, r_id_zona, r_fecha_hora,
                 r_numero_personas, r_deposito_reserva, r_estado)
                VALUES (:u, :r, :z, :f, :p, :d, 'CONFIRMADA')""",
                    {"u": int(cliente), "r": int(restaurante), "z": int(zona),
                     "f": fecha_hora, "p": int(personas), "d": float(deposito)})
            st.session_state["flash"] = "¡Reserva creada con éxito!"
            st.session_state["fiesta"] = True
            st.rerun()

# =====================================================
# GESTIONAR
# =====================================================
elif page.endswith("Gestionar"):
    page_head("Administrar", "Gestiona tus reservas", "Cambia la fecha, el número de personas o el estado.")
    activas = df[df["estado"] == "CONFIRMADA"]
    if activas.empty:
        st.info("No hay reservas confirmadas para gestionar.")
        st.stop()

    etiquetas = {r.id: f"#{r.id} · {r.cliente} · {r.restaurante} · {fecha_txt(r.fecha)}"
                 for r in activas.itertuples()}
    sel = st.selectbox("Elige una reserva", activas["id"].tolist(), format_func=etiquetas.get)
    fila = activas[activas["id"] == sel].iloc[0]
    cap = int(fila["capacidad"])

    izq, der = st.columns([3, 2], gap="large")
    with der:
        grid([reserva_card(next(activas[activas["id"] == sel].itertuples()))])
    with izq, st.container(border=True):
        st.markdown("**✏️ Editar datos**")
        c1, c2 = st.columns(2)
        nueva_fecha = c1.date_input("Fecha", fila["fecha"].date(), format="DD/MM/YYYY", key=f"f{sel}")
        nueva_hora = c2.time_input("Hora", fila["fecha"].time(), step=1800, key=f"h{sel}")
        nuevas_personas = st.slider("Personas", 1, min(cap, 20),
                                    min(int(fila["personas"]), cap, 20), key=f"p{sel}")
        if st.button("💾 Guardar cambios", type="primary", width="stretch"):
            run_dml("UPDATE reserva_restaurante SET r_fecha_hora = :f, r_numero_personas = :p "
                    "WHERE r_id_reserva = :id",
                    {"f": datetime.combine(nueva_fecha, nueva_hora), "p": int(nuevas_personas), "id": int(sel)})
            st.session_state["flash"] = "Reserva actualizada"
            st.rerun()

        st.markdown("**🔄 Cambiar estado**")
        b1, b2, b3 = st.columns(3)
        for col, texto, estado in [(b1, "✅ Completada", "COMPLETADA"),
                                   (b2, "⏰ No asistió", "NO ASISTIO"),
                                   (b3, "✖️ Cancelar", "CANCELADA")]:
            if col.button(texto, width="stretch"):
                run_dml("UPDATE reserva_restaurante SET r_estado = :e WHERE r_id_reserva = :id",
                        {"e": estado, "id": int(sel)})
                st.session_state["flash"] = f"Reserva marcada como {ESTADO_TXT[estado].lower()}"
                st.rerun()

# =====================================================
# EXPLORAR (CATÁLOGOS)
# =====================================================
elif page.endswith("Explorar"):
    page_head("Descubre", "Explora Medellín", "Restaurantes, clientes y zonas de la plataforma.")
    t1, t2, t3 = st.tabs(["🍴 Restaurantes", "👤 Clientes", "📍 Zonas"])

    with t1:
        rs = run_query("SELECT r_nombre AS nombre, r_tipo_cocina AS cocina, r_direccion AS direccion, "
                       "r_capacidad_maxima AS capacidad, r_precio_promedio AS precio, r_estado AS estado "
                       "FROM restaurante ORDER BY r_nombre")
        cocina_sel = st.pills("Tipo de cocina", ["Todas"] + sorted(rs["cocina"].dropna().unique()), default="Todas")
        if cocina_sel and cocina_sel != "Todas":
            rs = rs[rs["cocina"] == cocina_sel]
        grid(f"""<div class="card"><div class="card-img" style="{fondo(foto(r.cocina))}"><span class="chip">{esc(r.cocina)}</span></div>
            <div class="card-body"><h4>{esc(r.nombre)}</h4><p class="muted">📍 {esc(r.direccion)}</p>
            <div class="meta"><span>👥 {r.capacidad} pers.</span><span>💰 ${r.precio:,.0f}</span></div>
            {pill(r.estado.title(), REST_COLOR.get(r.estado, C['ambar']))}</div></div>""" for r in rs.itertuples())

    with t2:
        us = run_query("SELECT u_nombre_completo AS nombre, u_correo AS correo, u_telefono AS telefono, "
                       "u_ciudad_origen AS ciudad, u_tipo_cliente AS tipo, u_estado AS estado "
                       "FROM usuario ORDER BY u_nombre_completo")
        tipo_sel = st.pills("Tipo de cliente", ["Todos", "VIP", "FRECUENTE", "OCASIONAL"], default="Todos")
        if tipo_sel and tipo_sel != "Todos":
            us = us[us["tipo"] == tipo_sel]

        def iniciales(n):
            return "".join(p[0] for p in n.split()[:2]).upper()

        grid(f"""<div class="card"><div class="person">
            <div class="avatar" style="background:linear-gradient(135deg,{TIPO_COLOR[u.tipo]},#2B1D14)">{iniciales(u.nombre)}</div>
            <div><h4 style="margin:0;font-size:1.15rem">{esc(u.nombre)}</h4>
            <p class="muted">✉️ {esc(u.correo)}</p><p class="muted">📞 {u.telefono} · 🏙️ {esc(u.ciudad or '')}</p></div></div>
            <div class="card-body" style="padding-top:0">{pill(u.tipo.title(), TIPO_COLOR[u.tipo])}
            {pill(u.estado.title(), C['salvia'] if u.estado == 'ACTIVO' else C['vino'])}</div></div>""" for u in us.itertuples())

    with t3:
        zs = run_query("SELECT z_nombre_zona AS zona, z_comuna_barrio AS comuna, z_sector_turistico AS turistico, "
                       "z_estrato_predominante AS estrato, z_estado AS estado FROM zona_medellin ORDER BY z_nombre_zona")
        grid(f"""<div class="card">
            <div class="zona-top" style="background:linear-gradient(135deg,{'#D9643A' if z.turistico else '#6B8F71'},{'#E8B04B' if z.turistico else '#A8C3A0'})">📍</div>
            <div class="card-body"><h4>{esc(z.zona)}</h4><p class="muted">{esc(z.comuna or '')}</p>
            <div class="meta"><span>Estrato <span class="stars">{'★' * int(z.estrato)}</span></span></div>
            {pill('Turística' if z.turistico else 'Residencial', C['terracota'] if z.turistico else C['azul'])}
            {pill(z.estado.title(), C['salvia'] if z.estado == 'HABILITADA' else C['vino'])}</div></div>""" for z in zs.itertuples())

# =====================================================
# TABLAS (una vista por tabla, como en clase)
# =====================================================
elif page.endswith("Tablas"):
    page_head("Base de datos", "Tablas del proyecto", "Explora cada tabla directamente desde Oracle.")
    NOMBRES = {"usuario": "👤 Usuarios", "restaurante": "🍴 Restaurantes",
               "zona_medellin": "📍 Zonas", "reserva_restaurante": "📅 Reservas"}
    tabla = st.segmented_control("Tabla", list(NOMBRES), default="reserva_restaurante",
                                 format_func=NOMBRES.get) or "reserva_restaurante"

    total = int(run_query(f"SELECT COUNT(*) AS total FROM {tabla}")["total"][0])
    columnas = run_query(f"SELECT * FROM {tabla} FETCH FIRST 1 ROWS ONLY").columns.tolist()
    render(f"""<div class="kpis">
    <div class="kpi"><div class="ico" style="background:#D9643A22">🧾</div><div class="val">{total}</div><div class="lbl">Total de registros</div></div>
    <div class="kpi"><div class="ico" style="background:#4A6FA522">🧱</div><div class="val">{len(columnas)}</div><div class="lbl">Columnas</div></div>
    </div>""")

    with st.container(border=True):
        st.markdown("**Vista previa**")
        filas = st.slider("Filas a mostrar", 5, 100, 10)
        datos = run_query(f"SELECT * FROM {tabla} FETCH FIRST {filas} ROWS ONLY")
        st.dataframe(datos, hide_index=True, width="stretch")

    with st.container(border=True):
        st.markdown("**Contar registros por columna**")
        columna = st.selectbox("Columna", columnas)
        grupo = run_query(f"SELECT {columna} AS grupo, COUNT(*) AS cantidad FROM {tabla} "
                          f"GROUP BY {columna} ORDER BY cantidad DESC")
        grupo["grupo"] = grupo["grupo"].astype(str)
        fig = px.bar(grupo, x="grupo", y="cantidad", color="cantidad",
                     color_continuous_scale=["#F6D7B8", "#D9643A", "#8E2C3A"])
        fig.update_traces(marker_cornerradius=8, hovertemplate="%{x}: %{y}<extra></extra>")
        fig.update_layout(coloraxis_showscale=False)
        chart(fig)

# =====================================================
# CONSULTAS SQL LIBRES
# =====================================================
elif page.endswith("Consultas SQL"):
    page_head("Laboratorio", "Consultas SQL", "Escribe tu propia consulta y ejecútala en Oracle.")

    PROHIBIDAS = {"DROP", "TRUNCATE", "ALTER", "CREATE", "GRANT", "REVOKE"}
    OTRAS_TABLAS = {"ASIGNATURA", "ESTUDIANTE", "KARDEX", "PLAN", "PROFESOR", "PROGRAMA"}
    EJEMPLOS = {
        "Reservas por zona": "SELECT z.z_nombre_zona AS zona, COUNT(*) AS reservas\n"
                             "FROM reserva_restaurante r\nJOIN zona_medellin z ON z.z_id_zona = r.r_id_zona\n"
                             "GROUP BY z.z_nombre_zona\nORDER BY reservas DESC",
        "Clientes VIP": "SELECT u_nombre_completo, u_correo, u_ciudad_origen\n"
                        "FROM usuario\nWHERE u_tipo_cliente = 'VIP'",
        "Depósito por restaurante": "SELECT rs.r_nombre, SUM(r.r_deposito_reserva) AS total_deposito\n"
                                    "FROM reserva_restaurante r\n"
                                    "JOIN restaurante rs ON rs.r_id_restaurante = r.r_id_restaurante\n"
                                    "GROUP BY rs.r_nombre\nORDER BY total_deposito DESC",
        "Restaurantes caros": "SELECT r_nombre, r_tipo_cocina, r_precio_promedio\n"
                              "FROM restaurante\nWHERE r_precio_promedio > 100000",
    }

    ej = st.pills("⚡ Ejemplos rápidos", list(EJEMPLOS))
    if ej and ej != st.session_state.get("ej_prev"):
        st.session_state["sql"] = EJEMPLOS[ej]
    st.session_state["ej_prev"] = ej

    with st.container(border=True):
        sql = st.text_area("Escribe tu consulta (el punto y coma es opcional)", height=170, key="sql",
                           placeholder="SELECT * FROM restaurante")
        ejecutar = st.button("▶️ Ejecutar", type="primary")

    if ejecutar and sql.strip():
        sql = sql.strip().rstrip(";")
        palabras = set(re.findall(r"[A-Z_]+", sql.upper()))
        primera = sql.split()[0].upper()

        if palabras & PROHIBIDAS:
            st.error("🔒 Por seguridad, no se permiten DROP, TRUNCATE, ALTER, CREATE, GRANT ni REVOKE.")
        elif palabras & OTRAS_TABLAS:
            st.error("🔒 Esta consulta usa tablas que no son del proyecto. Solo se permiten "
                     "usuario, restaurante, zona_medellin y reserva_restaurante.")
        else:
            try:
                if primera in ("SELECT", "WITH"):
                    resultado = consulta_libre(sql)
                    st.success(f"✅ {len(resultado)} fila(s) encontradas")
                    st.dataframe(resultado, hide_index=True, width="stretch")
                    st.download_button("⬇️ Descargar CSV", resultado.to_csv(index=False).encode("utf-8"),
                                       "resultado.csv", "text/csv")
                elif primera in ("INSERT", "UPDATE", "DELETE"):
                    n = run_dml(sql, {})
                    st.success(f"✅ Listo, filas afectadas: {n}")
                else:
                    st.warning("Solo se permiten SELECT, INSERT, UPDATE o DELETE.")
            except Exception as e:
                st.error(f"Oracle respondió: {e}")