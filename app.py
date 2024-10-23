import streamlit as st
import pandas    as pd
import seaborn   as sns
import matplotlib.pyplot as plt
import joblib
from data_preprocessing import DataPreprocessor
from DataVisualization import DataVisualization


st.title('Dự đoán giá nhà tại Hà nội')


# Dữ liệu các quận và phường
districts = {
    "Ba Đình": ['Phường Điện Biên', 'Phường Giảng Võ', 'Phường Kim Mã',
       'Phường Liễu Giai', 'Phường Cống Vị', 'Phường Ngọc Hà',
       'Phường Đội Cấn', 'Phường Ngọc Khánh', 'Phường Vĩnh Phúc',
       'Phường Phúc Xá', 'Phường Thành Công', 'Phường Quán Thánh',
       'Phường Trúc Bạch', 'Phường Nguyễn Trung Trực'],
    
    "Hoàn Kiếm": ['Phường Lý Thái Tổ', 'Phường Hàng Bạc', 'Phường Phúc Tân',
       'Phường Cửa Nam', 'Phường Chương Dương', 'Phường Phan Chu Trinh',
       'Phường Hàng Mã', 'Phường Hàng Bài', 'Phường Trần Hưng Đạo',
       'Phường Cửa Đông', 'Phường Đồng Xuân', 'Phường Hàng Buồm',
       'Phường Hàng Bồ', 'Phường Tràng Tiền', 'Phường Hàng Bông',
       'Phường Hàng Trống', 'Phường Hàng Đào', 'Phường Hàng Gai'],
    
    "Tây Hồ": ['Phường Nhật Tân', 'Phường Bưởi', 'Phường Phú Thượng',
       'Phường Thụy Khuê', 'Phường Xuân La', 'Phường Tứ Liên',
       'Phường Yên Phụ', 'Phường Quảng An'],
    
    "Cầu Giấy": ['Phường Trung Hoà', 'Phường Quan Hoa', 'Phường Nghĩa Đô',
       'Phường Yên Hoà', 'Phường Mai Dịch', 'Phường Dịch Vọng',
       'Phường Dịch Vọng Hậu', 'Phường Nghĩa Tân'],
    
    "Đống Đa": ['Phường Khâm Thiên', 'Phường Láng Hạ', 'Phường Kim Liên',
       'Phường Phương Liên', 'Phường Láng Thượng', 'Phường Văn Miếu',
       'Phường Ô Chợ Dừa', 'Phường Khương Thượng', 'Phường Hàng Bột',
       'Phường Trung Tự', 'Phường Phương Mai', 'Phường Trung Liệt',
       'Phường Cát Linh', 'Phường Ngã Tư Sở', 'Phường Thổ Quan',
       'Phường Trung Phụng', 'Phường Nam Đồng', 'Phường Quang Trung',
       'Phường Quốc Tử Giám', 'Phường Thịnh Quang', 'Phường Văn Chương'],
    
    "Hai Bà Trưng": ['Phường Bạch Mai', 'Phường Minh Khai', 'Phường Đống Mác',
       'Phường Thanh Nhàn', 'Phường Vĩnh Tuy', 'Phường Quỳnh Lôi',
       'Phường Trương Định', 'Phường Thanh Lương', 'Phường Lê Đại Hành',
       'Phường Bạch Đằng', 'Phường Phạm Đình Hổ', 'Phường Bách Khoa',
       'Phường Đồng Tâm', 'Phường Cầu Dền', 'Phường Quỳnh Mai',
       'Phường Phố Huế', 'Phường Bùi Thị Xuân', 'Phường Đồng Nhân',
       'Phường Nguyễn Du', 'Phường Ngô Thì Nhậm'],
    
    "Hoàng Mai": ['Phường Lĩnh Nam', 'Phường Tương Mai', 'Phường Định Công',
       'Phường Hoàng Văn Thụ', 'Phường Đại Kim', 'Phường Giáp Bát',
       'Phường Mai Động', 'Phường Tân Mai', 'Phường Hoàng Liệt',
       'Phường Thanh Trì', 'Phường Vĩnh Hưng', 'Phường Thịnh Liệt',
       'Phường Trần Phú', 'Phường Yên Sở'],
    
    "Thanh Xuân": ['Phường Thanh Xuân Trung', 'Phường Thanh Xuân Bắc',
       'Phường Thanh Xuân Nam', 'Phường Khương Trung',
       'Phường Khương Đình', 'Phường Khương Mai', 'Phường Hạ Đình',
       'Phường Nhân Chính', 'Phường Thượng Đình', 'Phường Kim Giang',
       'Phường Phương Liệt'],
    
    "Long Biên": ['Phường Ngọc Thụy', 'Phường Thượng Thanh', 'Phường Việt Hưng',
       'Phường Bồ Đề', 'Phường Sài Đồng', 'Phường Ngọc Lâm',
       'Phường Đức Giang', 'Phường Long Biên', 'Phường Thạch Bàn',
       'Phường Phúc Đồng', 'Phường Cự Khối', 'Phường Gia Thụy',
       'Phường Phúc Lợi', 'Phường Giang Biên'],
    
    "Bắc Từ Liêm": ['Phường Cổ Nhuế 1', 'Phường Xuân Đỉnh', 'Phường Cổ Nhuế 2',
       'Phường Minh Khai', 'Phường Phú Diễn', 'Phường Phúc Diễn',
       'Phường Đông Ngạc', 'Phường Xuân Tảo', 'Phường Thụy Phương',
       'Phường Thượng Cát', 'Phường Đức Thắng', 'Phường Tây Tựu',
       'Phường Liên Mạc'],
    
    "Nam Từ Liêm": ['Phường Mỹ Đình 1', 'Phường Đại Mỗ', 'Phường Mỹ Đình 2',
       'Phường Mễ Trì', 'Phường Phú Đô', 'Phường Phương Canh',
       'Phường Xuân Phương', 'Phường Trung Văn', 'Phường Tây Mỗ',
       'Phường Cầu Diễn'],
    
    "Hà Đông": ['Phường Kiến Hưng', 'Phường Mộ Lao', 'Phường Văn Quán',
       'Phường Phú Lãm', 'Phường La Khê', 'Phường Yên Nghĩa',
       'Phường Nguyễn Trãi', 'Phường Vạn Phúc', 'Phường Quang Trung',
       'Phường Hà Cầu', 'Phường Phú Lương', 'Phường Yết Kiêu',
       'Phường Dương Nội', 'Phường Phúc La', 'Phường Đồng Mai',
       'Phường Phú La', 'Phường Biên Giang'],
    
    "Thanh Trì": ['Xã Thanh Liệt', 'Xã Hữu Hoà', 'Xã Ngũ Hiệp', 'Xã Đông Mỹ',
       'Xã Ngọc Hồi', 'Xã Tam Hiệp', 'Xã Tân Triều', 'Xã Tứ Hiệp',
       'Xã Tả Thanh Oai', 'Thị trấn Văn Điển', 'Xã Đại áng',
       'Xã Liên Ninh', 'Xã Vĩnh Quỳnh', 'Xã Vạn Phúc', 'Ngọc Hồi'],
    
    "Hoài Đức": ['Xã Vân Canh', 'Xã La Phù', 'Xã Đông La', 'Thị trấn Trạm Trôi',
       'Xã Song Phương', 'Xã Kim Chung', 'Xã An Khánh', 'Xã Di Trạch',
       'Xã An Thượng', 'Xã Vân Côn', 'Xã Đức Thượng', 'Xã Sơn Đồng'],
    
    "Thanh Oai": ['Xã Bích Hòa', 'Xã Cự Khê', 'Xã Phương Trung'],
    
    "Sóc Sơn": ['Xã Phú Cường', 'Xã Xuân Giang', 'Xã Tiên Dược', 'Xã Thanh Xuân',
       'Xã Minh Phú', 'Thị trấn Sóc Sơn', 'Xã Phù Lỗ', 'Xã Phú Minh',
       'Xã Phù Linh'],
    
    "Gia Lâm": ['Xã Cổ Bi', 'Thị trấn Trâu Quỳ', 'Xã Đặng Xá', 'Xã Kiêu Kỵ',
       'Xã Dương Quang', 'Thị trấn Yên Viên', 'Xã Yên Thường',
       'Xã Yên Viên', 'Xã Đông Dư', 'Xã Đa Tốn', 'Xã Ninh Hiệp',
       'Xã Kim Sơn'],
    
    "Đông Anh": ['Xã Bắc Hồng', 'Xã Kim Chung', 'Xã Võng La', 'Xã Xuân Nộn',
       'Thị trấn Đông Anh', 'Xã Vân Nội', 'Xã Uy Nỗ', 'Xã Kim Nỗ',
       'Xã Vĩnh Ngọc', 'Xã Nam Hồng', 'Xã Nguyên Khê', 'Xã Hải Bối',
       'Xã Dục Tú', 'Xã Đông Hội', 'Xã Mai Lâm'],
    
    "Chương Mỹ": ['Thị trấn Xuân Mai', 'Xã Phụng Châu', 'Thị trấn Chúc Sơn'],
    
    "Sơn Tây": ['Phường Ngô Quyền', 'Xã Sơn Đông', 'Phường Viên Sơn',
       'Phường Phú Thịnh'],
    
    "Mê Linh": ['Xã Kim Hoa', 'Xã Mê Linh', 'Xã Tiền Phong', 'Xã Tam Đồng'],
    
    "Thường Tín": ['Xã Hà Hồi', 'Thị trấn Thường Tín', 'Xã Nhị Khê', 'Xã Vân Tảo',
       'Xã Lê Lợi'],
    
    "Đan Phượng": ['Xã Tân Lập', 'Xã Thượng Mỗ', 'Xã Phương Đình', 'Thị trấn Phùng'],
    
    "Quốc Oai": ['Xã Nghĩa Hương', 'Xã Phú Cát', 'Xã Đông Yên', 'Xã Đại Thành',
       'Xã Đồng Quang'],
    
    "Phúc Thọ": ['Xã Ngọc Tảo'],
    
    "Ba Vì": ['Xã Phú Châu', 'Xã Phú Sơn'],
    
    "Thạch Thất": ['Xã Bình Phú', 'Xã Hương Ngải'],
    
    "Mỹ Đức": ['Xã Hợp Thanh']    
}

# Dữ liệu quận, phường mã hóa và cấu trúc cột X_train
df_quan = pd.read_csv("F:\\Python 101\\Predicting house price\\BTL\\df_quan.csv")
df_phuong = pd.read_csv("F:\\Python 101\\Predicting house price\\BTL\\df_phuong.csv")
df_colums = ['Số tầng', 'Số phòng ngủ', 'Diện tích', 'Dài', 'Rộng',
               'Loại hình nhà ở_Nhà mặt phố, mặt tiền', 'Loại hình nhà ở_Nhà ngõ, hẻm',
               'Loại hình nhà ở_Nhà phố liền kề', 'Giấy tờ pháp lý_Không rõ',
               'Giấy tờ pháp lý_Đang chờ sổ', 'Giấy tờ pháp lý_Đã có sổ',
               'Quận_encoded', 'Huyện_encoded']
df_pychart = pd.read_csv("F:\\Python 101\\Predicting house price\\BTL\\df_cleaned.csv")
df_pychart = df_pychart[df_pychart['Diện tích']<180]

# Khởi tạo đối tượng data_preprocessor
data_processor = DataPreprocessor(df_quan,df_phuong,df_colums)

# Khởi tạo đối tượng DataVisualization
data_visualization = DataVisualization(df_pychart)


# Tạo Selectbox 1: Lựa chọn quận
selected_district = st.selectbox("Chọn quận hoặc huyện", list(districts.keys()))

# Tạo Selectbox 2: Lựa chọn phường dựa trên quận đã chọn
if selected_district:
    wards = districts[selected_district]
    selected_ward = st.selectbox("Chọn phường hoặc xã", wards)

# Tạo Select box 3: Lựa chọn loại hình nhà ở
house_type = ['Nhà ngõ, hẻm', 'Nhà mặt phố, mặt tiền', 'Nhà biệt thự',
       'Nhà phố liền kề']
selected_house_type = st.selectbox("Chọn loại hình nhà ở",house_type)   

# Tạo Selectbox 4: Lựa chọn loại giấy tờ pháp lý
policy_paper = ['Đã có sổ', 'Không rõ', 'Đang chờ sổ', 'Giấy tờ khác']
selected_policy_paper = st.selectbox("Chọn giấy tờ pháp lý",policy_paper)  
    
# Tạo selectbox 5: Lựa chọn số tầng
num_floor = [0,1,2,3,4,5,6,7,8,9,10]
selected_floor = st.selectbox("Chọn số tầng(nếu không xác định được số tầng hãy chọn 0)",num_floor) 

# Tạo selectbox 6: Lựa chọn số phòng ngủ
num_bedroom = [1,2,3,4,5,6,7,8,9,10]
selected_bedroom = st.selectbox("Chọn số phòng ngủ",num_bedroom)

# Tạo number_input 1: Nhập diện tích
acreage = st.number_input("Nhập diện tích căn nhà(m2)",min_value=0.0, value=50.0, step=0.1, format="%.2f")

# Tạo number_input 2: Nhập chiều rộng
width = st.number_input("Nhập chiều rộng",min_value=0.0, value=5.0, step=0.1, format="%.2f") 

#Tạo number_input 3: Nhập chiều dài
length = st.number_input("Nhập chiều dài",min_value=0.0, value=10.0, step=0.1, format="%.2f") 

# Tạo button để nhấn dự đoán
if st.button("Dự đoán giá"):
    # Lấy bộ dữ liệu người dùng và xử lý bằng data_processor
    input_df = data_processor.process_input(selected_district, selected_ward, selected_house_type, 
                        selected_policy_paper,selected_floor, selected_bedroom, acreage, width, length)
    
    # Gọi lại mô hình random forest regression
    model_RF = joblib.load("F:\\Python 101\\Predicting house price\\BTL\\RF_model.pkl") 
    
    # Dự đoán input
    predictions = model_RF.predict(input_df)
    
    # Thông báo kết quả
    st.markdown(f"<h3>Giá của căn nhà: {predictions[0]:.2f} triệu dồng/m²</h3>", unsafe_allow_html=True)
    
    # Thông báo nhắc nhở người dùng
    st.markdown("<small>Đây là dự đoán giá dựa trên dữ liệu năm 2020, giá trị của căn nhà có thể tăng giảm khoảng 18 -20 triệu tùy vào khu vực .</small>", unsafe_allow_html=True)
    st.markdown("<small>Mô hình còn rất nhiều thiếu sót hãy là một nhà đầu tư khôn ngoan chúc bạn thành công mua đáy bán đỉnh.</small>", unsafe_allow_html=True)

st.title("Một số thống kê giá nhà bạn có thể tham khảo nhé!")
st.markdown("<medium>Thống kê giá nhà trung bình theo các Quận/Huyện của Hà Nội.</medium>", unsafe_allow_html=True)

# Hiển thị biểu đồ
st.pyplot(data_visualization.draw_price_by_district())
# Hiển thị phần trăm loại hình nhà ở
st.markdown("<medium>Phân phối loại hình nhà ở.</medium>", unsafe_allow_html=True)
st.pyplot(data_visualization.draw_house_type_percent())






    
    
 


  
    