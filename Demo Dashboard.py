import streamlit as st
import pandas as pd
from datetime import datetime

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="RFID Asset Tracker",
    page_icon="📡",
    layout="wide",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Main background */
    .stApp { background-color: #0f1117; color: #e8eaf0; }

    /* Hide Streamlit chrome */
    #MainMenu, footer, header { visibility: hidden; }

    /* Metric cards */
    div[data-testid="metric-container"] {
        background: #1a1d27;
        border: 1px solid #2a2d3a;
        border-radius: 10px;
        padding: 1rem 1.25rem;
    }
    div[data-testid="metric-container"] label {
        color: #8b8fa8 !important;
        font-size: 12px !important;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }
    div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
        font-size: 28px !important;
        font-weight: 600;
    }

    /* Alert boxes */
    .alert-exception {
        background: rgba(239, 68, 68, 0.12);
        border-left: 3px solid #ef4444;
        border-radius: 0 8px 8px 0;
        padding: 10px 16px;
        margin-bottom: 8px;
        font-size: 14px;
        color: #fca5a5;
    }
    .alert-warning {
        background: rgba(245, 158, 11, 0.12);
        border-left: 3px solid #f59e0b;
        border-radius: 0 8px 8px 0;
        padding: 10px 16px;
        margin-bottom: 8px;
        font-size: 14px;
        color: #fcd34d;
    }

    /* Section header */
    .section-title {
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        color: #5a5e72;
        margin: 1.5rem 0 0.75rem;
    }

    /* Table tweaks */
    .stDataFrame { border-radius: 10px; overflow: hidden; }
</style>
""", unsafe_allow_html=True)


# ── Data ──────────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    records = [
        ("RFID-1001","CNC Machine #1","Equipment","Assembly Line A","Assembly Line A","2024-01-15 08:12",42000),
        ("RFID-1002","CNC Machine #2","Equipment","Assembly Line A","Assembly Line A","2024-01-15 08:15",42000),
        ("RFID-1003","Hydraulic Press","Equipment","Assembly Line B","Maintenance Bay","2024-01-15 06:45",28500),
        ("RFID-1004","Conveyor Belt Unit","Equipment","Assembly Line B","Assembly Line B","2024-01-15 08:20",15000),
        ("RFID-1005","Industrial Robot Arm","Equipment","Assembly Line A","Assembly Line A","2024-01-15 08:18",95000),
        ("RFID-1006","Forklift #1","Vehicle","Receiving","Shipping Dock","2024-01-15 07:55",32000),
        ("RFID-1007","Forklift #2","Vehicle","Shipping Dock","Shipping Dock","2024-01-15 08:05",32000),
        ("RFID-1008","Pallet Jack #1","Vehicle","Receiving","Receiving","2024-01-15 08:00",4200),
        ("RFID-1009","Pallet Jack #2","Vehicle","Finished Goods","Quality Control","2024-01-15 07:30",4200),
        ("RFID-1010","Steel Coil Batch A","Material","Raw Storage","Raw Storage","2024-01-15 08:22",8700),
        ("RFID-1011","Steel Coil Batch B","Material","Raw Storage","Assembly Line A","2024-01-15 08:10",8700),
        ("RFID-1012","Aluminum Sheet Lot","Material","Raw Storage","Raw Storage","2024-01-15 08:25",5400),
        ("RFID-1013","Plastic Pellets Drum","Material","Raw Storage","Raw Storage","2024-01-15 08:17",1200),
        ("RFID-1014","Safety Helmet Rack","Safety","Assembly Line A","Assembly Line A","2024-01-15 08:00",850),
        ("RFID-1015","Fire Extinguisher Cart","Safety","Assembly Line B","Receiving","2024-01-15 05:40",600),
        ("RFID-1016","Inspection Camera Unit","Tool","Quality Control","Quality Control","2024-01-15 08:30",7800),
        ("RFID-1017","Torque Wrench Set","Tool","Maintenance Bay","Maintenance Bay","2024-01-15 08:08",1400),
        ("RFID-1018","Calibration Kit #1","Tool","Quality Control","Quality Control","2024-01-15 08:28",3200),
        ("RFID-1019","Welding Machine #1","Equipment","Assembly Line B","Assembly Line B","2024-01-15 08:14",11000),
        ("RFID-1020","Welding Machine #2","Equipment","Assembly Line A","Shipping Dock","2024-01-15 04:22",11000),
        ("RFID-1021","Finished Part Lot #101","Product","Finished Goods","Finished Goods","2024-01-15 08:35",22000),
        ("RFID-1022","Finished Part Lot #102","Product","Finished Goods","Finished Goods","2024-01-15 08:36",18500),
        ("RFID-1023","Packaging Station","Equipment","Shipping Dock","Shipping Dock","2024-01-15 08:02",6200),
        ("RFID-1024","Scanner Terminal #1","Tool","Receiving","Receiving","2024-01-15 08:12",2800),
        ("RFID-1025","Scanner Terminal #2","Tool","Shipping Dock","Shipping Dock","2024-01-15 08:09",2800),
        ("RFID-1026","Die Casting Mold Set A","Tool","Assembly Line B","Assembly Line B","2024-01-15 08:20",19000),
        ("RFID-1027","Die Casting Mold Set B","Tool","Assembly Line A","Assembly Line A","2024-01-15 08:19",19000),
        ("RFID-1028","Lubricant Drum #1","Material","Maintenance Bay","Assembly Line B","2024-01-15 07:10",380),
        ("RFID-1029","Emergency AED Unit","Safety","Assembly Line A","Assembly Line A","2024-01-15 08:05",1500),
        ("RFID-1030","Overhead Crane","Equipment","Assembly Line B","Assembly Line B","2024-01-15 08:25",75000),
    ]
    df = pd.DataFrame(records, columns=[
        "tag_id","asset_name","category","expected_zone",
        "current_reader","last_seen","asset_value_usd"
    ])
    df["last_seen"] = pd.to_datetime(df["last_seen"])
    return df


def classify_status(row, ref_time):
    if row["expected_zone"] == row["current_reader"]:
        return "OK"
    hours_ago = (ref_time - row["last_seen"]).total_seconds() / 3600
    return "Exception" if hours_ago > 3 else "Warning"


df = load_data()
REF_TIME = datetime(2024, 1, 15, 8, 40)
df["status"] = df.apply(lambda r: classify_status(r, REF_TIME), axis=1)


# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("## 📡 RFID Asset Tracker")
st.markdown(
    "<span style='color:#5a5e72; font-size:13px;'>Acme Manufacturing — Floor snapshot: 2024-01-15 08:40</span>",
    unsafe_allow_html=True,
)
st.markdown("---")


# ── Metric Cards ──────────────────────────────────────────────────────────────
total_value   = df["asset_value_usd"].sum()
total_assets  = len(df)
ok_count      = (df["status"] == "OK").sum()
warning_count = (df["status"] == "Warning").sum()
exception_count = (df["status"] == "Exception").sum()

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("💰 Total Inventory Value", f"${total_value:,.0f}")
c2.metric("📦 Assets Tracked",        total_assets)
c3.metric("✅ In Correct Location",   ok_count)
c4.metric("⚠️ Warnings",             warning_count)
c5.metric("🚨 Exceptions",           exception_count,
          delta=f"{exception_count} misplaced",
          delta_color="inverse")


# ── Exception & Warning Alerts ────────────────────────────────────────────────
misplaced = df[df["status"].isin(["Exception", "Warning"])].copy()

if misplaced.empty:
    st.success("✅ All assets are in their expected locations.")
else:
    st.markdown('<p class="section-title">Active alerts</p>', unsafe_allow_html=True)
    for _, row in misplaced.iterrows():
        css_class = "alert-exception" if row["status"] == "Exception" else "alert-warning"
        icon = "🚨" if row["status"] == "Exception" else "⚠️"
        st.markdown(
            f'<div class="{css_class}">'
            f'<strong>{icon} [{row["status"].upper()}]</strong> &nbsp;'
            f'<strong>{row["asset_name"]}</strong> ({row["tag_id"]}) — '
            f'expected at <em>{row["expected_zone"]}</em>, '
            f'found at <strong>{row["current_reader"]}</strong>. '
            f'Last seen: {row["last_seen"].strftime("%H:%M")}. '
            f'Value at risk: <strong>${row["asset_value_usd"]:,.0f}</strong>'
            f'</div>',
            unsafe_allow_html=True,
        )


# ── Sidebar Filters ───────────────────────────────────────────────────────────
st.sidebar.header("🔍 Filters")

search_term = st.sidebar.text_input("Search asset or tag ID")

all_zones = ["All"] + sorted(df["current_reader"].unique().tolist())
selected_zone = st.sidebar.selectbox("Zone / Reader", all_zones)

all_cats = ["All"] + sorted(df["category"].unique().tolist())
selected_cat = st.sidebar.selectbox("Category", all_cats)

all_statuses = ["All", "OK", "Warning", "Exception"]
selected_status = st.sidebar.selectbox("Status", all_statuses)

st.sidebar.markdown("---")
st.sidebar.markdown(
    f"**{total_assets} assets** | **${total_value:,.0f}** total value",
    unsafe_allow_html=False,
)


# ── Filter Data ───────────────────────────────────────────────────────────────
view = df.copy()

if search_term:
    mask = (
        view["asset_name"].str.contains(search_term, case=False) |
        view["tag_id"].str.contains(search_term, case=False)
    )
    view = view[mask]

if selected_zone != "All":
    view = view[view["current_reader"] == selected_zone]

if selected_cat != "All":
    view = view[view["category"] == selected_cat]

if selected_status != "All":
    view = view[view["status"] == selected_status]


# ── Asset Table ───────────────────────────────────────────────────────────────
st.markdown('<p class="section-title">Asset inventory</p>', unsafe_allow_html=True)
st.caption(f"Showing {len(view)} of {total_assets} assets")

def color_status(val):
    colors = {
        "OK":        "color: #4ade80; font-weight: 600",
        "Warning":   "color: #fbbf24; font-weight: 600",
        "Exception": "color: #f87171; font-weight: 600",
    }
    return colors.get(val, "")

def highlight_mismatch(row):
    if row["expected_zone"] != row["current_reader"]:
        return [""] * (len(row) - 2) + ["color: #f87171", ""]
    return [""] * len(row)

display_df = view[[
    "tag_id", "asset_name", "category",
    "expected_zone", "current_reader",
    "last_seen", "asset_value_usd", "status"
]].rename(columns={
    "tag_id":          "Tag ID",
    "asset_name":      "Asset",
    "category":        "Category",
    "expected_zone":   "Expected Zone",
    "current_reader":  "Current Reader",
    "last_seen":       "Last Seen",
    "asset_value_usd": "Value (USD)",
    "status":          "Status",
})

styled = (
    display_df.style
    .applymap(color_status, subset=["Status"])
    .apply(highlight_mismatch, axis=1)
    .format({"Value (USD)": "${:,.0f}", "Last Seen": lambda x: x.strftime("%Y-%m-%d %H:%M")})
)

st.dataframe(styled, use_container_width=True, hide_index=True)


# ── Zone Value Breakdown ──────────────────────────────────────────────────────
st.markdown('<p class="section-title">Inventory value by zone</p>', unsafe_allow_html=True)

zone_val = (
    df.groupby("current_reader")["asset_value_usd"]
    .sum()
    .reset_index()
    .rename(columns={"current_reader": "Zone", "asset_value_usd": "Total Value"})
    .sort_values("Total Value", ascending=False)
)
st.bar_chart(zone_val.set_index("Zone"), color="#6366f1")


# ── Category Breakdown ────────────────────────────────────────────────────────
st.markdown('<p class="section-title">Assets by category</p>', unsafe_allow_html=True)

cat_counts = (
    df.groupby("category")
    .agg(count=("tag_id", "count"), total_value=("asset_value_usd", "sum"))
    .reset_index()
    .rename(columns={"category": "Category", "count": "Count", "total_value": "Total Value"})
    .sort_values("Total Value", ascending=False)
)
st.dataframe(
    cat_counts.style.format({"Total Value": "${:,.0f}"}),
    use_container_width=True,
    hide_index=True,
)


# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<span style='color:#3a3d4a; font-size:12px;'>"
    "Built with Streamlit · RFID data simulated for Acme Manufacturing · "
    "Exception threshold: asset misplaced &gt; 3 hours"
    "</span>",
    unsafe_allow_html=True,
)
