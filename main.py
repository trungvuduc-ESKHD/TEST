import streamlit as st
import datetime
import hashlib
from supabase import create_client, Client

# Kết nối Supabase
SUPABASE_URL = "https://your-project.supabase.co"
SUPABASE_KEY = "your-anon-or-service-role-key"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Hàm tạo ID duy nhất
def hash_supplier_id(name, city):
    return hashlib.md5(f"{name}_{city}".encode()).hexdigest()[:8]

# Hàm lưu dữ liệu vào Supabase
def save_to_supabase(data):
    supplier_id = hash_supplier_id(data["display_name"], data["city"])
    data["id"] = supplier_id
    data["updated_at"] = datetime.datetime.now().isoformat()

    # Kiểm tra xem đã có hay chưa
    existing = supabase.table("supplier_addresses").select("id").eq("id", supplier_id).execute()
    if existing.data:
        # Cập nhật
        supabase.table("supplier_addresses").update(data).eq("id", supplier_id).execute()
    else:
        # Thêm mới
        supabase.table("supplier_addresses").insert(data).execute()

# Giao diện Streamlit
st.set_page_config(page_title="Địa chỉ Nhà cung cấp", layout="centered")
st.title("📦 Cập nhật địa chỉ nhà cung cấp")

with st.form("form"):
    display_name = st.text_input("Display Name *")
    street1 = st.text_input("Primary Address Street1 *")
    city = st.text_input("Primary Address City *")
    postal_code = st.text_input("Postal Code *")
    country_code = st.text_input("Country Code", value="VN", disabled=True)

    submit = st.form_submit_button("Gửi")

    if submit:
        if not all([display_name, street1, city, postal_code]):
            st.error("❌ Vui lòng điền đầy đủ các trường bắt buộc.")
        else:
            data = {
                "display_name": display_name,
                "street1": street1,
                "city": city,
                "postal_code": postal_code,
                "country_code": "VN",  # Cố định
            }
            try:
                save_to_supabase(data)
                st.success("✅ Dữ liệu đã được lưu vào Supabase thành công!")
            except Exception as e:
                st.error(f"❌ Lỗi khi lưu dữ liệu: {e}")

# Hiển thị dữ liệu từ Supabase
st.markdown("---")
st.subheader("📋 Danh sách địa chỉ đã lưu")

try:
    result = supabase.table("supplier_addresses").select("*").execute()
    if result.data:
        import pandas as pd
        df = pd.DataFrame(result.data)
        st.dataframe(df[["display_name", "street1", "city", "postal_code", "country_code", "updated_at"]])
    else:
        st.info("Chưa có dữ liệu nào.")
except Exception as e:
    st.error(f"Lỗi khi tải dữ liệu: {e}")
