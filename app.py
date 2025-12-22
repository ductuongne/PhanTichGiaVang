import streamlit as st

# Giả sử df_sjc là DataFrame giá realtime (buy=155500, sell=157500)
buy_price = "155,500"  # nghìn đồng
sell_price = "157,500"
change_percent = "+1.2%"  # ví dụ tăng

# HTML + CSS inline
html_price = f"""
<div style="text-align: center; padding: 20px; background-color: #f0f2f6; border-radius: 10px;">
    <h1 style="color: #1f77b4; margin: 0;">Giá vàng SJC hôm nay</h1>
    <p style="font-size: 30px; margin: 10px 0;">
        Mua vào: <span style="color: green; font-weight: bold;">{buy_price}</span> nghìn/lượng
    </p>
    <p style="font-size: 30px; margin: 10px 0;">
        Bán ra: <span style="color: red; font-weight: bold;">{sell_price}</span> nghìn/lượng
    </p>
    <p style="font-size: 24px; color: {"green" if "+" in change_percent else "red"};">
        Thay đổi: {change_percent}
    </p>
</div>
"""

st.markdown(html_price, unsafe_allow_html=True)