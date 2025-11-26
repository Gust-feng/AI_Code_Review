> 此项目已废弃，已有新项目代替
> 
> 望周知



# Agent Core - 底层 AGENT 系统

一个用于 IDE 助手和代码审查的本地 AI Agent 内核系统。

## 安装

### 1. 克隆项目并进入目录

```bash
cd z:\AI_Code_Review
```

### 2. 创建虚拟环境（如果还没有）

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. 安装依赖

```powershell
pip install -r requirements.txt
```

### 4. 配置环境变量

复制 `.env.example` 为 `.env` 并填入你的 API 密钥：

```powershell
Copy-Item .env.example .env
```

编辑 `.env` 文件，设置你的 `GLM_API_KEY` 或 `KIMI_API_KEY`，例如默认使用 GLM：

```env
DEFAULT_PROVIDER=glm
GLM_API_KEY=你的_glm_api_key
```

### 5. （可选）编写 `config.yaml`

如果你希望以文件方式集中管理配置，可以在项目根目录创建 `config.yaml`，示例：

```yaml
default_provider: glm
glm_api_key: your_api_key
workspace_root: ./
http_timeout: 30.0
```

`.env` 与环境变量会覆盖 `config.yaml` 中的同名字段。

## 使用

### 命令行调用

```python
from agent_core.api.service import run_ide_chat

# 开始新对话
result = run_ide_chat(
    user_input="请帮我分析这段代码",
    meta={"file_path": "example.py"}
)

print(result["assistant_message"]["content"])

# 继续对话
result = run_ide_chat(
    user_input="能详细解释一下吗？",
    conversation_id=result["conversation_id"]
)
```

### GUI 测试界面

```powershell
python agent_core/gui/test_gui.py
```

## 运行测试

```powershell
pytest agent_core/tests/ -v
```

## 项目结构

```
agent_core/
├── config/          # 配置管理
├── domain/          # 领域模型
├── infrastructure/  # 基础设施（存储、日志）
├── providers/       # AI Provider 接入（GLM、Kimi 等）
├── tools/           # 工具系统
├── agents/          # Agent 引擎
├── prompts/         # 系统提示词
├── api/             # 对外接口
└── tests/           # 测试用例
```


