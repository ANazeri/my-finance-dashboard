import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# تنظیمات صفحه
st.set_page_config(page_title="داشبورد مالی هوشمند", layout="wide")

# --- استایل‌دهی راست‌چین برای فارسی ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Vazirmatn&display=swap');
    html, body, [class*="css"]  {
        font-family: 'Vazirmatn', sans-serif;
        direction: rtl;
        text-align: right;
    }
    </style>
    """, unsafe_allow_html=True)

# --- داده‌های نمونه (در پروژه‌ی واقعی از دیتابیس یا فایل استفاده کنید) ---
if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame({
        'تاریخ': pd.to_datetime(['2023-10-01', '2023-10-05', '2023-10-10', '2023-10-15']),
        'دسته بندی': ['حقوق', 'اجاره', 'خواروبار', 'سرمایه‌گذاری'],
        'نوع': ['درآمد', 'هزینه', 'هزینه', 'درآمد'],
        'مبلغ': [50000000, 15000000, 4000000, 10000000]
    })

# --- هدر اصلی ---
st.title("💸 داشبورد مدیریت مالی هوشمند")
st.sidebar.header("افزودن تراکنش جدید")

# --- فرم ورود داده در سایدبار ---
with st.sidebar.form("transaction_form"):
    date = st.date_input("تاریخ")
    category = st.selectbox("دسته‌بندی", ["حقوق", "اجاره", "خواروبار", "تفریح", "سرمایه‌گذاری", "سایر"])
    t_type = st.radio("نوع تراکنش", ["درآمد", "هزینه"])
    amount = st.number_input("مبلغ (تومان)", min_value=0, step=1000)
    submit = st.form_submit_button("ثبت تراکنش")

    if submit:
        new_row = {'تاریخ': pd.to_datetime(date), 'دسته بندی': category, 'نوع': t_type, 'مبلغ': amount}
        st.session_state.data = pd.concat([st.session_state.data, pd.DataFrame([new_row])], ignore_index=True)
        st.success("تراکنش با موفقیت ثبت شد!")

# --- محاسبات شاخص‌های کلیدی (KPIs) ---
df = st.session_state.data
total_income = df[df['نوع'] == 'درآمد']['مبلغ'].sum()
total_expense = df[df['نوع'] == 'هزینه']['مبلغ'].sum()
balance = total_income - total_expense

# --- نمایش کارت‌های وضعیت ---
col1, col2, col3 = st.columns(3)
col1.metric("مجموع درآمد", f"{total_income:,} تومان")
col2.metric("مجموع هزینه‌ها", f"{total_expense:,} تومان", delta_color="inverse")
col3.metric("تراز نهایی", f"{balance:,} تومان")

st.divider()

# --- بخش نمودارها ---
col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.subheader("📊 تفکیک هزینه‌ها")
    expense_df = df[df['نوع'] == 'هزینه']
    if not expense_df.empty:
        fig_pie = px.pie(expense_df, values='مبلغ', names='دسته بندی', hole=0.4,
                         color_discrete_sequence=px.colors.sequential.RdBu)
        st.plotly_chart(fig_pie, use_container_width=True)
    else:
        st.info("داده‌ای برای هزینه‌ها ثبت نشده است.")

with col_chart2:
    st.subheader("📈 روند مالی (زمانی)")
    df_sorted = df.sort_values('تاریخ')
    fig_line = px.line(df_sorted, x='تاریخ', y='مبلغ', color='نوع', markers=True)
    st.plotly_chart(fig_line, use_container_width=True)

# --- تحلیل هوشمند (Rule-based Insight) ---
st.subheader("💡 تحلیل هوشمند وضعیت شما")
if total_expense > total_income * 0.8:
    st.warning("هشدار: هزینه‌های شما بیش از ۸۰٪ درآمدتان است. پیشنهاد می‌شود هزینه‌های غیرضروری را کاهش دهید.")
elif balance > 0:
    st.success(f"وضعیت عالی است! شما توانسته‌اید { (balance/total_income)*100:.1f}% از درآمد خود را پس‌انداز کنید.")

# --- نمایش جدول داده‌ها ---
with st.expander("📝 مشاهده لیست تمام تراکنش‌ها"):
    st.dataframe(df.sort_values('تاریخ', ascending=False), use_container_width=True)