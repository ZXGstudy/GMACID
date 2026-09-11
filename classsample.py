import pandas as pd
import shutil
import os

# 读取 CSV 文件并确保所有列都是字符串
df = pd.read_csv('/home/zxg/GMACID/hostDNA/cutkmer20/sample.csv', dtype=str).fillna('')

# 定义文件所在的目录
file_dir = '/home/zxg/GMACID/hostDNA/cutkmer20'

# 创建 train 和 test 目录（如果不存在）
os.makedirs('train', exist_ok=True)
os.makedirs('test', exist_ok=True)

# 迭代数据框中的每一行
for index, row in df.iterrows():
    sample_id = str(row['SampleID']).strip()  # 确保 sample_id 是字符串并去除多余的空白字符
    class_type = str(row['class']).strip()
    
    # 定义源文件路径
    source_file = os.path.join(file_dir, f"{sample_id}_host.1_processed.fa")
    
    # 调试输出：打印当前正在查找的文件
    print(f"正在查找文件: {source_file}")
    
    # 检查源文件是否存在
    if not os.path.exists(source_file):
        print(f"文件未找到: {source_file}")
        continue  # 跳过当前循环
    
    # 定义目标目录
    dest_dir = 'train' if class_type == 'train' else 'test'
    
    # 移动文件
    try:
        shutil.move(source_file, os.path.join(dest_dir, os.path.basename(source_file)))
        print(f"已移动 {source_file} 到 {dest_dir}")
    except Exception as e:
        print(f"移动文件 {source_file} 时出错: {e}")

print("文件已成功移动。")
