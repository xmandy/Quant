import yfinance as yf
import pandas as pd
import os

def main():
    # 定义股票代码和时间范围
    ticker = "AAPL"
    start_date = "2024-01-01"
    end_date = "2024-12-31"

    print(f"正在下载 {ticker} 的数据...")
    
    # 下载数据
    data = yf.download(ticker, start=start_date, end=end_date)

    print(data)

    if not data.empty:
        # 确保输出目录存在
        output_file = "aapl_data.csv"
        
        # 保存为 CSV
        data.to_csv(output_file)
        print(f"数据已保存至 {output_file}")
        
        # 打印前几行查看
        print("\n数据预览:")
        print(data.head())
    else:
        print("未获取到数据，请检查网络或股票代码。")

if __name__ == "__main__":
    main()
