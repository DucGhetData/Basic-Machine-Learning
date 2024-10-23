import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

# Tạo lớp để vẽ biểu đồ
class DataVisualization:
    def __init__(self,df_pychart):
        self.df_pychart = df_pychart
        
    def draw_price_by_district(self):
        # Tính giá trung bình theo quận
        gia_trung_binh = self.df_pychart.groupby('Quận')['Giá (triệu đồng/m2)'].mean().reset_index().sort_values(by='Giá (triệu đồng/m2)', ascending=False)
        
        # Vẽ biểu đồ cột
        fig, ax = plt.subplots(figsize=(14, 8))
        sns.barplot(x='Quận', y='Giá (triệu đồng/m2)', data=gia_trung_binh, ax=ax)
        plt.title('Giá nhà trung bình theo quận')
        plt.xlabel('Quận')
        plt.ylabel('Giá (triệu đồng/m2)')
        plt.xticks(rotation=90)  
        # Trả lại df chứa dữ liệu để vẽ biểu đồ 
        return fig
    
    def draw_house_type_percent(self):
        phan_tram_loai_hinh = self.df_pychart['Loại hình nhà ở'].value_counts(normalize=True)*100
        
        fig, ax = plt.subplots()
        colors = ['#ff9999','#66b3ff','#99ff99','#ffcc99']
        wedges, _ = ax.pie(phan_tram_loai_hinh, startangle=90, colors=colors, wedgeprops=dict(width=0.3))
        ax.legend(wedges, phan_tram_loai_hinh.index, title="Loại hình nhà ở", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
        ax.axis('equal')
        
        return fig
        
        
        
        


