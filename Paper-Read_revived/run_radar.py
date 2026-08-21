import os
import yaml
import re

# 1. 設定檔案路徑
MASTER_CONFIG = "Skill_Master.md"
REF_DIR = "reference"

def load_yaml_from_markdown(file_path):
    """從 Markdown 檔案中提取 YAML 區塊"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 使用正則表達式提取 ```yaml ... ``` 之間的內容
    match = re.search(r'```yaml(.*?)```', content, re.DOTALL)
    if match:
        return yaml.safe_load(match.group(1))
    return None

def determine_mode(user_query, config):
    """根據關鍵字決定要走哪條路"""
    rules = config['skill_definition']['router_rules']
    
    for rule in rules:
        for keyword in rule['trigger_keywords']:
            if keyword.lower() in user_query.lower():
                print(f"✨ 偵測到關鍵字 '{keyword}' -> 啟動模式: {rule['rule_id']}")
                return rule['action']['target_file']
    
    # 預設行為：若找不到關鍵字，可以預設回傳心理學或詢問
    print("⚠️ 未偵測到特定領域關鍵字，請人工確認。")
    return None

def execute_radar(user_query):
    # 步驟 1: 讀取主控檔
    print("🔄 讀取 Skill_Master.md...")
    master_conf = load_yaml_from_markdown(MASTER_CONFIG)
    
    if not master_conf:
        print("❌ 無法讀取 Master Config")
        return

    # 步驟 2: 路由判斷 (Router)
    target_file = determine_mode(user_query, master_conf)
    
    if target_file:
        # 修正路徑 (確保讀取正確的 reference 資料夾)
        # 如果 YAML 寫 "reference/Bio_Radar.md"，我們直接用
        full_path = target_file 
        
        # 步驟 3: 讀取子模組 (Loading Module)
        if os.path.exists(full_path):
            print(f"📂 載入模組: {full_path}")
            with open(full_path, 'r', encoding='utf-8') as f:
                module_content = f.read()
            
            # 步驟 4: 組合最終 Prompt (Final Prompt Engineering)
            final_prompt = f"""
            {module_content}
            
            ---
            【使用者指令】: {user_query}
            
            請依照上述的 YAML 定義 (Skill Module) 執行學術雷達任務。
            """
            
            print("🚀 準備發送給 AI 模型...")
            print("-" * 30)
            print(final_prompt) # 這裡通常會接 OpenAI API 或 Gemini API
            print("-" * 30)
            
            # TODO: 這裡可以呼叫 openai.ChatCompletion.create(...)
            
        else:
            print(f"❌ 找不到模組檔案: {full_path}")

# ==========================================
# 測試執行
# ==========================================
if __name__ == "__main__":
    # 模擬使用者輸入
    user_input = input("請輸入您的研究主題: ")
    execute_radar(user_input)