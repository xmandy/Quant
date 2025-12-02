# 量化交易实战：8周从零到实盘部署教程 (Step-by-Step)

这份教程将“量化交易”拆解为 8 个具体的周计划。不同于泛泛的理论，每一周你都有明确的**动手任务 (Action Items)** 和 **交付物 (Deliverable)**。

目标：8周后，你将拥有一个在云端或本地自动运行的交易策略。

---

## 第一阶段：本地环境与数据基础 (Week 1-2)

在接触复杂的引擎之前，先在本地把“数据”玩明白。

### Week 1: 环境搭建与数据获取
*   **目标**: 搭建本地 Python 开发环境，并获取第一份股票数据。
*   **工具**: VS Code, Python 3.10+, `yfinance` 库。
*   **任务**:
    1.  安装 VS Code 和 Python 扩展。
    2.  创建一个文件夹 `Quant_Lab`。
    3.  安装库: `pip install yfinance pandas matplotlib`
    4.  **编写脚本 `get_data.py`**:
        *   使用 `yfinance` 下载 "AAPL" (苹果公司) 过去 1 年的日线数据。
        *   将数据保存为 `aapl_data.csv`。
*   **交付物**: 一个包含 CSV 文件的文件夹，里面有苹果公司的历史股价。

### Week 2: 数据分析与指标计算
*   **目标**: 学会用 Pandas 计算技术指标（均线）。
*   **工具**: Pandas, Matplotlib。
*   **任务**:
    1.  **编写脚本 `analysis.py`**:
        *   读取 Week 1 下载的 CSV。
        *   使用 Pandas 计算 20 日均线 (SMA20) 和 50 日均线 (SMA50)。
        *   *提示*: `df['Close'].rolling(window=20).mean()`
    2.  **可视化**:
        *   画出收盘价、SMA20 和 SMA50 的折线图。
        *   观察“金叉”（SMA20 上穿 SMA50）发生的时间点。
*   **交付物**: 一张包含股价和均线的图片，你已经手动验证了一个策略的逻辑。

---

## 第二阶段：QuantConnect 平台实战 (Week 3-5)

现在我们将逻辑迁移到专业的量化引擎 QuantConnect (QC) 上。

### Week 3: 熟悉 QC 引擎 (Bootcamp)
*   **目标**: 理解 QC 的核心框架：`Initialize` (初始化) 和 `OnData` (数据驱动)。
*   **任务**:
    1.  注册 QuantConnect 账号。
    2.  进入 **Learning Center -> Bootcamp**。
    3.  **完成 "Buy and Hold Equities" (买入持有)**: 学会 `SetHoldings`。
    4.  **完成 "Momentum-based Strategy" (动量策略)**: 学会如何请求历史数据 `History`。
*   **交付物**: 在 QC 网页端跑通两个官方示例策略，看到回测曲线。

### Week 4: 复现经典策略 (均线交叉)
*   **目标**: 将 Week 2 的逻辑写成 QC 算法。
*   **任务**:
    1.  在 QC 创建新项目 "MyFirstSMA"。
    2.  在 `Initialize` 中：
        *   设置回测时间 (SetStartDate)。
        *   添加股票 "SPY" (AddEquity)。
        *   定义两个指标变量: `self.sma_fast = self.SMA("SPY", 20)`。
    3.  在 `OnData` 中：
        *   判断 `self.sma_fast` 是否大于 `self.sma_slow`。
        *   如果是，且当前没持仓 -> `self.SetHoldings("SPY", 1.0)` (全仓买入)。
        *   如果否，且当前有持仓 -> `self.Liquidate()` (清仓)。
*   **交付物**: 一个完整的策略代码，回测结果显示该策略在过去 5 年的表现。

### Week 5: 进阶功能 - 动态选股与风控
*   **目标**: 不再只交易一只股票，而是从全市场筛选。
*   **任务**:
    1.  **Universe Selection (选股)**:
        *   使用 `CoarseSelectionFunction`。
        *   逻辑：每天筛选出成交量 (DollarVolume) 最大的前 10 只股票。
    2.  **Risk Management (风控)**:
        *   使用 `StopMarketOrder` 设置止损单（例如买入价下跌 5% 止损）。
*   **交付物**: 一个能自动每天换股、并且带有止损功能的策略。

---

## 第三阶段：工程化与部署 (Week 6-8)

从“网页玩具”变成“生产力工具”。

### Week 6: 本地开发 (LEAN CLI)
*   **目标**: 在本地 VS Code 中开发 QC 策略，保护代码隐私。
*   **工具**: Docker, LEAN CLI。
*   **任务**:
    1.  安装 Docker Desktop。
    2.  安装 LEAN CLI: `pip install lean`.
    3.  登录: `lean login`.
    4.  拉取项目: `lean cloud pull`.
    5.  **本地回测**: 在终端运行 `lean backtest "MyFirstSMA"`。
*   **交付物**: 看到终端里滚动的回测日志，并在本地文件夹生成了回测报告 (HTML/JSON)。

### Week 7: 模拟盘部署 (Paper Trading)
*   **目标**: 让策略在实时数据下运行，检验是否有“未来函数”或滑点问题。
*   **任务**:
    1.  在 QC 网页端或使用 CLI。
    2.  选择 "Deploy Live" -> "Paper Trading" (模拟盘)。
    3.  观察 2-3 天。
    4.  **检查点**:
        *   订单是否在预期的时刻发出？
        *   成交价格和当时的市场价差多少（滑点）？
*   **交付物**: 一个正在运行的 Live Algorithm 仪表盘链接。

### Week 8: 实盘准备与监控 (Live Ready)
*   **目标**: 为连接真实资金做最后准备。
*   **任务**:
    1.  **消息推送**:
        *   在代码中加入 `self.Notify.Email()` 或 `self.Notify.Sms()`。
        *   当发生交易时，发送邮件给自己。
    2.  **异常处理**:
        *   思考：如果数据断了怎么办？如果资金不足怎么办？
        *   在代码中加入 `try...except` 块保护关键逻辑。
    3.  (可选) 对接券商: 如果你有 Interactive Brokers 账号，尝试连接（注意风险）。
*   **交付物**: 收到第一封来自你策略的自动交易通知邮件。

---

## 附录：遇到问题怎么办？

1.  **查文档**: QuantConnect 的文档非常详细，善用搜索。
2.  **看源码**: 在 GitHub 上搜索 `QuantConnect/Lean`，看看指标是怎么实现的。
3.  **问社区**: QC 的 Forum 活跃度很高，把报错信息贴上去通常能得到解答。

祝你好运！开始你的 Week 1 任务吧。
