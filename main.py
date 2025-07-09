import streamlit as st
import datetime
import pandas as pd
import hashlib

st.set_page_config(page_title="Nhà cung cấp - Địa chỉ", layout="centered")

# Khởi tạo session lưu trữ dữ liệu
if "supplier_addresses" not in st.session_state:
    st.session_state.supplier_addresses = []

def hash_supplier_id(name, city):
    return hashlib.md5(f"{name}_{city}".encode()).hexdigest()[:8]

def save_address_data(data):
    supplier_id = hash_supplier_id(data["display_name"], data["city"])
    data["id"] = supplier_id
    data["updated_at"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Kiểm tra trùng
    existing = next((i for i, d in enumerate(st.session_state.supplier_addresses) if d["id"] == supplier_id), None)
    if existing is not None:
        st.session_state.supplier_addresses[existing] = data
    else:
        st.session_state.supplier_addresses.append(data)

# Giao diện nhập
st.title("📦 Thông tin địa chỉ Nhà cung cấp")

with st.form("address_form"):
    display_name = st.text_input("Display Name *")
    street1 = st.text_input("Primary Address Street1 *")
    city = st.text_input("Primary Address City *")
    postal_code = st.text_input("Postal Code *")
    country_code = st.text_input("Country Code", value="VN", disabled=True)

    submitted = st.form_submit_button("Gửi")

    if submitted:
        if not all([display_name, street1, city, postal_code]):
            st.error("❌ Vui lòng điền đầy đủ thông tin bắt buộc.")
        else:
            data = {
                "display_name": display_name,
                "street1": street1,
                "city": city,
                "postal_code": postal_code,
                "country_code": country_code,
            }
            save_address_data(data)
            st.success("✅ Đã lưu thông tin thành công!")

# Hiển thị danh sách đã nhập
if st.session_state.supplier_addresses:
    st.subheader("📋 Danh sách địa chỉ đã lưu")
    df = pd.DataFrame(st.session_state.supplier_addresses)
    st.dataframe(df[["display_name", "street1", "city", "postal_code", "country_code", "updated_at"]])
else:
    st.info("Chưa có thông tin nào được nhập.")
