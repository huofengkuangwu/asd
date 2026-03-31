import requests
import json

# 1. 原始爱奇艺接口地址 (换成你现在用的那个)
raw_url = "https://hltv.cc.cd/api/tvbox/config?format=json&mode=fast"

def clean_json():
    try:
        response = requests.get(raw_url)
        data = response.json()
        
        # 2. 定义白名单分类（只留这些，其他的全删掉）
        white_list = ["动作片", "国产剧"，"纪录片"]
        
        if "sites" in data:
            for site in data["sites"]:
                # 针对爱奇艺那个源进行处理
                if "爱奇艺" in site.get("name", ""):
                    # 关键：添加 categories 过滤
                    site["categories"] = "动作片#国产剧#纪录片"
                    # 强制关闭该源的搜索，防止搜到不该看的
                    site["searchable"] = 0
                    site["quickSearch"] = 0
        
        # 3. 保存清洗后的文件
        with open("out.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print("清洗完成！")
            
    except Exception as e:
        print(f"出错啦: {e}")

if __name__ == "__main__":
    clean_json()
