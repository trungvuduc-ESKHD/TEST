import streamlit as st
import pandas as pd
import datetime
import hashlib
from typing import Dict

# Configuration
st.set_page_config(
    page_title='Quản lý Địa chỉ Nhà cung cấp',
    page_icon='📦',
    layout='wide',
    initial_sidebar_state='expanded'
)

# Initialize session state
if "suppliers_data" not in st.session_state:
    st.session_state.suppliers_data = []

if "company_info" not in st.session_state:
    st.session_state.company_info = {
        "name": "",
        "address": "",
        "phone": "",
        "email": "",
        "tax_code": ""
    }

def hash_supplier_id(supplier_name: str, email: str) -> str:
    "Tạo ID duy nhất cho nhà cung cấp"
    return hashlib.md5(f"{supplier_name}_{email}".encode()).hexdigest()[:8]

def save_supplier_data(data: Dict):
    "Lưu dữ liệu nhà cung cấp"
    supplier_id = hash_supplier_id(data["supplier_name"], data["email"])
    data["id"] = supplier_id
    data["updated_at"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    existing_index = None
    for i, supplier in enumerate(st.session_state.suppliers_data):
        if supplier['id'] == supplier_id:
            existing_index = i
            break

    if existing_index is not None:
        st.session_state.suppliers_data[existing_index] = data
    else:
        st.session_state.suppliers_data.append(data)

def export_to_csv():
    "Xuất dữ liệu ra CSV"
    if st.session_state.suppliers_data:
        df = pd.DataFrame(st.session_state.suppliers_data)
        return df.to_csv(index=False, encoding="utf-8-sig")
    return None

def supplier_form():
    "Form cho nhà cung cấp nhập thông tin"
    st.title("📦 Cập nhật Thông tin Nhà cung cấp")

    if st.session_state.company_info['name']:
        st.info(f"""
        **Thông tin công ty chúng tôi:**
        - Tên: {st.session_state.company_info['name']}
        - Địa chỉ: {st.session_state.company_info['address']}
        - Điện thoại: {st.session_state.company_info['phone']}
        - Email: {st.session_state.company_info['email']}
        - Mã số thuế: {st.session_state.company_info['tax_code']}
        """)

    st.markdown("---")
    st.subheader("Vui lòng cập nhật thông tin nhà cung cấp")

    with st.form("supplier_form"):
        col1, col2 = st.columns(2)

        with col1:
            supplier_name = st.text_input("Tên nhà cung cấp *", placeholder="VD: Công ty ABC")
            contact_person = st.text_input("Người liên hệ *", placeholder="VD: Nguyễn Văn A")
            phone = st.text_input("Số điện thoại *", placeholder="VD: 0123456789")
            email = st.text_input("Email *", placeholder="VD: contact@company.com")

        with col2:
            address = st.text_area("Địa chỉ mới *", placeholder="Nhập địa chỉ đầy đủ")
            tax_code = st.text_input("Mã số thuế", placeholder="VD: 0123456789")
            website = st.text_input("Website", placeholder="VD: https://company.com")
            business_type = st.selectbox("Loại hình kinh doanh", ["Sản xuất", "Thương mại", "Dịch vụ", "Khác"])

        st.subheader("Thông tin sản phẩm/dịch vụ")
        products_services = st.text_area("Sản phẩm/Dịch vụ cung cấp", placeholder="Mô tả chi tiết sản phẩm/dịch vụ")

        st.subheader("Thông tin bổ sung")
        col3, col4 = st.columns(2)

        with col3:
            payment_terms = st.text_input("Điều khoản thanh toán", placeholder="VD: 30 ngày")
            delivery_time = st.text_input("Thời gian giao hàng", placeholder="VD: 7-10 ngày")

        with col4:
            bank_account = st.text_input("Tài khoản ngân hàng", placeholder="Số tài khoản")
            bank_name = st.text_input("Ngân hàng", placeholder="Tên ngân hàng")

        notes = st.text_area("Ghi chú", placeholder="Thông tin bổ sung khác")

        submitted = st.form_submit_button("Gửi thông tin")

        if submitted:
            if not all([supplier_name, contact_person, phone, email, address]):
                st.error("Vui lòng điền đầy đủ các thông tin bắt buộc (*)")
                return

            if "@" not in email:
                st.error("Email không hợp lệ")
                return

            supplier_data = {
                'supplier_name': supplier_name,
                'contact_person': contact_person,
                'phone': phone,
                'email': email,
                'address': address,
                'tax_code': tax_code,
                'website': website,
                'business_type': business_type,
                'products_services': products_services,
                'payment_terms': payment_terms,
                'delivery_time': delivery_time,
                'bank_account': bank_account,
                'bank_name': bank_name,
                'notes': notes
            }

            save_supplier_data(supplier_data)
            st.success("✅ Cảm ơn bạn đã cập nhật thông tin!")
            st.balloons()

def admin_dashboard():
    "Dashboard quản lý cho admin"
    st.title("🏢 Dashboard Quản lý")

    with st.expander("⚙️ Cấu hình thông tin công ty"):
        with st.form("company_form"):
            st.subheader("Thông tin công ty của bạn")

            col1, col2 = st.columns(2)
            with col1:
                company_name = st.text_input("Tên công ty", value=st.session_state.company_info['name'])
                company_phone = st.text_input("Điện thoại", value=st.session_state.company_info['phone'])
                company_email = st.text_input("Email", value=st.session_state.company_info['email'])

            with col2:
                company_address = st.text_area("Địa chỉ", value=st.session_state.company_info['address'])
                company_tax_code = st.text_input("Mã số thuế", value=st.session_state.company_info['tax_code'])

            if st.form_submit_button("Cập nhật thông tin công ty"):
                st.session_state.company_info = {
                    'name': company_name,
                    'address': company_address,
                    'phone': company_phone,
                    'email': company_email,
                    'tax_code': company_tax_code
                }
                st.success("✅ Đã cập nhật thông tin công ty!")

    st.subheader("📊 Thống kê")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Tổng nhà cung cấp", len(st.session_state.suppliers_data))

    with col2:
        today_updates = len([
            s for s in st.session_state.suppliers_data
            if s.get('updated_at', '').startswith(datetime.date.today().strftime('%Y-%m-%d'))
        ])
        st.metric("Cập nhật hôm nay", today_updates)

    with col3:
        business_types = [s.get('business_type', 'Khác') for s in st.session_state.suppliers_data]
        most_common = max(set(business_types), key=business_types.count) if business_types else "Chưa có"
        st.metric("Loại hình phổ biến", most_common)

    with col4:
        complete_profiles = len([
            s for s in st.session_state.suppliers_data
            if all([s.get('tax_code'), s.get('website'), s.get('products_services')])
        ])
        st.metric("Hồ sơ đầy đủ", complete_profiles)

    st.subheader("📋 Danh sách nhà cung cấp")

    if st.session_state.suppliers_data:
        col1, col2, col3 = st.columns(3)

        with col1:
            business_filter = st.selectbox("Lọc theo loại hình",
                                           ["Tất cả"] + list(set([s.get('business_type', 'Khác')
                                                                  for s in st.session_state.suppliers_data])))

        with col2:
            search_term = st.text_input("Tìm kiếm theo tên")

        with col3:
            sort_by = st.selectbox("Sắp xếp theo", ["Cập nhật gần nhất", "Tên A-Z", "Loại hình"])

        filtered_data = st.session_state.suppliers_data.copy()

        if business_filter != "Tất cả":
            filtered_data = [s for s in filtered_data if s.get('business_type') == business_filter]

        if search_term:
            filtered_data = [s for s in filtered_data if search_term.lower() in s.get('supplier_name', '').lower()]

        if sort_by == "Cập nhật gần nhất":
            filtered_data.sort(key=lambda x: x.get('updated_at', ''), reverse=True)
        elif sort_by == "Tên A-Z":
            filtered_data.sort(key=lambda x: x.get('supplier_name', ''))
        elif sort_by == "Loại hình":
            filtered_data.sort(key=lambda x: x.get('business_type', ''))

        for supplier in filtered_data:
            with st.expander(f"🏢 {supplier.get('supplier_name', 'N/A')} - {supplier.get('business_type', 'N/A')}"):
                col1, col2 = st.columns(2)

                with col1:
                    st.write(f"**Người liên hệ:** {supplier.get('contact_person', 'N/A')}")
                    st.write(f"**Điện thoại:** {supplier.get('phone', 'N/A')}")
                    st.write(f"**Email:** {supplier.get('email', 'N/A')}")
                    st.write(f"**Địa chỉ:** {supplier.get('address', 'N/A')}")
                    st.write(f"**Mã số thuế:** {supplier.get('tax_code', 'N/A')}")

                with col2:
                    st.write(f"**Website:** {supplier.get('website', 'N/A')}")
                    st.write(f"**Sản phẩm/DV:** {supplier.get('products_services', 'N/A')}")
                    st.write(f"**Thanh toán:** {supplier.get('payment_terms', 'N/A')}")
                    st.write(f"**Giao hàng:** {supplier.get('delivery_time', 'N/A')}")
                    st.write(f"**Cập nhật:** {supplier.get('updated_at', 'N/A')}")

                if supplier.get('notes'):
                    st.write(f"**Ghi chú:** {supplier.get('notes')}")

        st.subheader("📥 Xuất dữ liệu")
        col1, col2 = st.columns(2)

        with col1:
            csv_data = export_to_csv()
            if csv_data:
                st.download_button(
                    label="📊 Tải xuống CSV",
                    data=csv_data,
                    file_name=f"suppliers_data_{datetime.date.today().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )

        with col2:
            if st.button("🗑️ Xóa tất cả dữ liệu"):
                st.session_state.suppliers_data = []
                st.success("✅ Đã xóa tất cả dữ liệu!")
                st.rerun()
    else:
        st.info("Chưa có nhà cung cấp nào cập nhật thông tin.")

def main():
    "Main application"
    st.sidebar.title("🚀 Điều hướng")

    mode = st.sidebar.radio(
        "Chọn chế độ:",
        ["👥 Form nhà cung cấp", "🏢 Dashboard quản lý"]
    )

    st.sidebar.markdown("---")
    st.sidebar.subheader("📝 Hướng dẫn sử dụng")

    if mode == "👥 Form nhà cung cấp":
        st.sidebar.markdown("""
        **Dành cho nhà cung cấp:**
        1. Điền đầy đủ thông tin bắt buộc (*)
        2. Cập nhật địa chỉ mới chính xác
        3. Bấm "Gửi thông tin" để hoàn tất
        """)
        supplier_form()
    else:
        st.sidebar.markdown("""
        **Dành cho quản lý:**
        1. Cấu hình thông tin công ty
        2. Xem thống kê và danh sách
        3. Lọc và tìm kiếm dữ liệu
        4. Xuất dữ liệu ra CSV
        """)
        admin_dashboard()

    st.sidebar.markdown("---")
    st.sidebar.markdown("💡 **Lưu ý:** Dữ liệu chỉ lưu trong phiên làm việc hiện tại")

if __name__ == "__main__":
    main()
