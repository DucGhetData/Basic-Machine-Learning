import pandas as pd

# Khởi tạo lớp DataPreprocessor
class DataPreprocessor:
    # Hàm này có vai trò giống constructor trong Java
    def __init__(self,df_quan,df_phuong,df_colums):
        # Nhận dataframe chứa dữ liệu và các cột đã dùng để huấn luyện mô hình
        self.df_quan = df_quan
        self.df_phuong = df_phuong
        self.df_columns = df_colums
    
    # Hàm xử lý dữ liệu đầu vào 
    def process_input(self,selected_district, selected_ward, selected_house_type, selected_policy_paper,
                      selected_floor, selected_bedroom, acreage, width, length):
        
        # Lấy giá trị Target-encoding theo Quận và Phường
        encoded_district = self.df_quan.loc[self.df_quan['Quận'] 
                                            == selected_district,'Quận_encoded'].values[0]
        encoded_ward     = self.df_phuong.loc[self.df_phuong['Huyện']
                                            == selected_ward, 'Huyện_encoded'].values[0]
        
        # Tạo cột Onehot-encoding cho loại hình nhà ở và giấy tờ pháp lý
        encoded_house_type = {'Loại hình nhà ở_Nhà mặt phố, mặt tiền':0,
                              'Loại hình nhà ở_Nhà ngõ, hẻm':0,
                              'Loại hình nhà ở_Nhà phố liền kề':0}
        encoded_policy_paper = {'Giấy tờ pháp lý_Không rõ':0,
                                'Giấy tờ pháp lý_Đang chờ sổ':0,
                                'Giấy tờ pháp lý_Đã có sổ':0}
        
        # Điền giá trị 1 cho cột tương ứng dữ liệu dầu vào
        encoded_house_type[f"Loại hình nhà ở_{selected_house_type}"] = 1
        encoded_policy_paper[f"Giấy tờ pháp lý_{selected_policy_paper}"] =1
        
        # Tạo dataframe chứa dữ liệu người dùng nhập vào
        input_data = {
            'Quận_encoded': [encoded_district],
            'Huyện_encoded': [encoded_ward],
            'Số tầng': [selected_floor],
            'Số phòng ngủ': [selected_bedroom], 
            'Diện tích': [acreage], 
            'Dài': [length], 
            'Rộng': [width],   
        }
        # Chuyển dictionnary input_data sang dataframe
        input_df = pd.DataFrame(input_data)
        
        # Thêm các cột Onehot-encoding vào dataframe
        for key in encoded_house_type:
            input_df[key] = encoded_house_type[key]
        
        for key in encoded_policy_paper:
            input_df[key] = encoded_policy_paper[key]
            
        # Sắp xếp lại dataframe cho đúng thứ tự X_train
        input_df = input_df.reindex(columns=self.df_columns,fill_value=0)
        
        return input_df        
        
        
         