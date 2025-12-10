import pandas as pd
import matplotlib.pyplot as plt
import os

def main():
    # 定义数据文件路径
    file_path = "aapl_data.csv"
    
    # 检查文件是否存在
    if not os.path.exists(file_path):
        print(f"错误：找不到文件 {file_path}。请先运行 get_data.py 下载数据。")
        return

    # 读取数据
    print(f"正在读取 {file_path} ...")
    try:
        # 读取 CSV，将第一列作为索引并解析为日期
        df = pd.read_csv(file_path, index_col=0, parse_dates=True)
        
        # yfinance 下载的数据 CSV 格式可能比较复杂（多级表头），
        # 如果 get_data.py 直接保存了 yf.download 的结果，
        # 且 yfinance 版本较新，可能需要处理一下列名。
        # 这里先假设是标准格式，如果报错再调整。
        
        # 简单的检查，确保有 'Close' 列
        if 'Close' not in df.columns:
            # 尝试处理 yfinance 多级列名的情况 (Price, Ticker)
            # 如果列名是 ('Close', 'AAPL') 这种形式，pandas read_csv 可能读成多级索引
            # 或者如果 header=0,1,2...
            # 这里做一个简单的容错，如果找不到 Close，打印列名看看
            print("警告：未找到 'Close' 列。当前列名：", df.columns)
            # 如果是多级索引，尝试获取 Close
            # 但通常 read_csv 默认只读一行 header，除非指定 header=[0,1]
            # 让我们先假设最简单的情况，如果用户遇到问题再调试
            
    except Exception as e:
        print(f"读取文件出错: {e}")
        return

    # 检查数据是否为空
    if df.empty:
        print("数据为空。")
        return

    print(df.loc[1])
    return 

    # 计算均线
    print("正在计算均线...")
    # 20日均线
    df['SMA20'] = df['Close'].rolling(window=20).mean()
    # 50日均线
    df['SMA50'] = df['Close'].rolling(window=50).mean()

    # 打印最后几行查看结果
    print("\n计算结果预览：")
    print(df[['Close', 'SMA20', 'SMA50']].tail())

    # 可视化
    print("\n正在绘制图表...")
    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df['Close'], label='Close Price', alpha=0.5, color='gray')
    plt.plot(df.index, df['SMA20'], label='SMA 20', linestyle='--', color='blue')
    plt.plot(df.index, df['SMA50'], label='SMA 50', linestyle='--', color='orange')
    
    plt.title('AAPL Stock Price & Moving Averages')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.grid(True)
    
    # 保存图片
    output_img = 'aapl_analysis.png'
    plt.savefig(output_img)
    print(f"图表已保存为 {output_img}")
    
    # 显示图片
    plt.show()

if __name__ == "__main__":
    main()
