import streamlit as st
import pandas as pd
import os
import plotly.express as px

@st.cache_data
def data_cleaning(folder_path="vhi_data"):
    all_dfs = []

    names = {
        1: 'Cherkasy', 2: 'Chernihiv', 3: 'Chernivtsi', 4: 'Crimea',
        5: 'Dnipropetrovsk', 6: 'Donetsk', 7: 'Ivano-Frankivsk',
        8: 'Kharkiv', 9: 'Kherson', 10: 'Khmelnytskyy',
        11: 'Kyiv', 12: 'Kyiv City', 13: 'Kirovohrad',
        14: 'Luhansk', 15: 'Lviv', 16: 'Mykolayiv',
        17: 'Odessa', 18: 'Poltava', 19: 'Rivne',
        20: 'Sevastopol', 21: 'Sumy', 22: 'Ternopil',
        23: 'Transcarpathia', 24: 'Vinnytsya', 25: 'Volyn',
        26: 'Zaporizhzhya', 27: 'Zhytomyr'
    }

    for file_name in os.listdir(folder_path):

        if not file_name.startswith("vhi_"):
            continue

        province_id = int(file_name.split('_')[1].split('.')[0])
        full_path = os.path.join(folder_path, file_name)

        df = pd.read_csv(
            full_path,
            header=1,
            names=['year', 'week', 'SMN', 'SMT', 'VCI', 'TCI', 'VHI', 'empty'],
            skipinitialspace=True
        )

        df = df.drop(columns=['empty'], errors='ignore')

        df['year'] = df['year'].astype(str).str.replace('<tt><pre>', '', regex=False)
        df = df[df['year'] != '']

        df = df.replace(-1, pd.NA)

        for col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

        df = df.dropna()

        df['year'] = df['year'].astype(int)
        df['week'] = df['week'].astype(int)

        df['province_id'] = province_id
        df['region'] = names.get(province_id, "Unknown")

        all_dfs.append(df)

    return pd.concat(all_dfs, ignore_index=True)


df = data_cleaning()

def set_defaults():
    st.session_state.indicator = "VHI"
    st.session_state.region = sorted(df["region"].unique())[0]
    st.session_state.year_range = (int(df["year"].min()), int(df["year"].max()))
    st.session_state.week_range = (int(df["week"].min()), int(df["week"].max()))
    st.session_state.sort_asc = False
    st.session_state.sort_desc = False


if "indicator" not in st.session_state:
    set_defaults()

st.sidebar.title("Фільтри")

if st.sidebar.button("Reset"):
    set_defaults()
    st.rerun()

indicator = st.sidebar.selectbox(
    "Часовий ряд",
    ["VCI", "TCI", "VHI"],
    key="indicator"
)

region = st.sidebar.selectbox(
    "Область",
    sorted(df["region"].unique()),
    key="region"
)

year_range = st.sidebar.slider(
    "Інтервал років",
    int(df["year"].min()),
    int(df["year"].max()),
    key="year_range"
)

week_range = st.sidebar.slider(
    "Інтервал тижнів",
    int(df["week"].min()),
    int(df["week"].max()),
    key="week_range"
)

sort_asc = st.sidebar.checkbox("Сортування ↑", key="sort_asc")
sort_desc = st.sidebar.checkbox("Сортування ↓", key="sort_desc")

filtered = df[
    (df["region"] == region) &
    (df["year"].between(year_range[0], year_range[1])) &
    (df["week"].between(week_range[0], week_range[1]))
]

if sort_asc and sort_desc:
    st.sidebar.warning("Оберіть тільки одне сортування")
elif sort_asc:
    filtered = filtered.sort_values(by=indicator, ascending=True)
elif sort_desc:
    filtered = filtered.sort_values(by=indicator, ascending=False)


tab1, tab2, tab3 = st.tabs(["Таблиця", "Графік 1", "Графік 2"])

with tab1:
    st.dataframe(filtered, use_container_width=True)


with tab2:
    temp = filtered.copy()
    temp["date"] = pd.to_datetime(
        temp["year"].astype(str) + "-01-01"
    ) + pd.to_timedelta((temp["week"] - 1) * 7, unit="D")

    temp = temp.sort_values("date")

    fig = px.line(
        temp,
        x="date",
        y=indicator,
    )

    st.plotly_chart(fig, use_container_width=True)


with tab3:

    compare_df = df[
        (df["year"].between(year_range[0], year_range[1])) &
        (df["week"].between(week_range[0], week_range[1]))
    ]

    avg = compare_df.groupby("region", as_index=False)[indicator].mean()

    if sort_asc and not sort_desc:
        avg = avg.sort_values(by=indicator, ascending=True)
    elif sort_desc and not sort_asc:
        avg = avg.sort_values(by=indicator, ascending=False)

    category_order = avg["region"].tolist()

    avg["color"] = avg["region"].apply(
        lambda x: "selected" if x == region else "other"
    )

    fig2 = px.bar(
        avg,
        x="region",
        y=indicator,
        color="color",
        category_orders={"region": category_order},
        color_discrete_map={"selected": "red", "other": "lightgray"},
    )

    fig2.update_layout(showlegend=False)
    st.plotly_chart(fig2, use_container_width=True)