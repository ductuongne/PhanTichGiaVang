import streamlit as st
import pandas as pd
import altair as alt

def calc_volatility_metrics(df, price_col="Buy", window=7):
    df = df.groupby("date")[price_col].mean().reset_index().sort_values("date")
    
    if len(df) < window + 1:
        return None

    # Công thức: return = (P_t - P_{t-1}) / P_{t-1}
    df["return"] = df[price_col].pct_change()
    df["volatility"] = df["return"].rolling(window).std()

    current_price = df.iloc[-1][price_col]
    if len(df) >= 2:
        previous_price = df.iloc[-2][price_col]
        delta = current_price - previous_price
        delta_pct = (delta / previous_price * 100) if previous_price != 0 else 0
    else:
        delta = 0
        delta_pct = 0
    
    vol_now = df.iloc[-1]["volatility"]
    vol_avg = df["volatility"].mean()
    
    return {
        "current": current_price,
        "delta": delta,
        "delta_pct": delta_pct,
        "volatility": vol_now,
        "is_high": vol_now > (vol_avg * 1.5) if not pd.isna(vol_now) and not pd.isna(vol_avg) else False
    }

def render_company_row(name: str, csv_path: str, title_class: str):
    with st.container():
        st.markdown(f'<div class="brand-title {title_class}">{name}</div>', unsafe_allow_html=True)
        
        try:
            df = pd.read_csv(csv_path)
            df["date"] = pd.to_datetime(df["date"])
        except Exception as e:
            st.error(f"Không thể đọc dữ liệu {name}: {e}")
            return

        col_info, col_chart = st.columns([1, 2])

        with col_info:
            branches = sorted(df["BranchName"].dropna().unique())
            if not branches:
                 st.warning("Không có dữ liệu chi nhánh.")
                 return
            branch = st.selectbox(f"Chi nhánh {name}", branches, key=f"sb_{name}")
            
            df_br = df[df["BranchName"] == branch].copy()
            metrics = calc_volatility_metrics(df_br)

            if metrics and not pd.isna(metrics['current']):
                st.metric("Giá Buy hiện tại", f"{metrics['current']:,.0f} VND", 
                          f"{metrics['delta']:,.0f} ({metrics['delta_pct']:.2f}%)")
                
                # Cảnh báo biến động
                status = "Cao" if metrics['is_high'] else "Thấp"
                status_class = "vol-high" if metrics['is_high'] else "vol-low"
                vol_display = f"{metrics['volatility']:.5f}" if not pd.isna(metrics['volatility']) else "N/A"
                
                st.markdown(f"""
                    <div class="vol-alert-container {status_class}">
                        <div style="font-size: 0.8rem; opacity: 0.8;">Trạng thái biến động</div>
                        <div class="vol-text">{status}</div>
                        <div style="font-size: 0.7rem;">Std Dev: {vol_display}</div>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.info("Dữ liệu không đủ để phân tích biến động.")

        with col_chart:
            # Vẽ biểu đồ vùng cho Volatility
            df_br_chart = df_br.groupby("date")["Buy"].mean().reset_index().sort_values("date")
            df_br_chart["ret"] = df_br_chart["Buy"].pct_change()
            df_br_chart["vol"] = df_br_chart["ret"].rolling(7).std()
            df_plot = df_br_chart.dropna()

            if not df_plot.empty:
                chart = alt.Chart(df_plot).mark_area(
                    line={'color': '#ffd700'},
                    color=alt.Gradient(
                        gradient='linear',
                        stops=[alt.GradientStop(color='#ffd700', offset=0),
                               alt.GradientStop(color='rgba(0,0,0,0)', offset=1)],
                        x1=1, x2=1, y1=1, y2=0
                    )
                ).encode(
                    x=alt.X("date:T", title="Thời gian", axis=alt.Axis(labelColor='white', titleColor='white')),
                    y=alt.Y("vol:Q", title="Chỉ số Volatility", axis=alt.Axis(labelColor='white', titleColor='white')),
                    tooltip=[alt.Tooltip("date:T", title="Ngày"), alt.Tooltip("vol:Q", title="Độ biến động", format=".5f")]
                ).properties(
                    height=220,
                    background='transparent' 
                ).configure_view(
                    strokeOpacity=0 
                ).configure_axis(
                    gridColor='rgba(255,255,255,0.1)' 
                )
                
                st.altair_chart(chart, use_container_width=True)
            else:
                st.write("Chưa đủ dữ liệu để vẽ biểu đồ.")