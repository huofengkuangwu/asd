import requests
import re

# 原始源地址
raw_url = "https://raw.githubusercontent.com/80947108/guovin/master/output/result.m3u"
# 定义筛选关键词（针对河北移动优化）
keywords = ["移动", "CMCC", "chinamobile", "河北", "hebei", "migu", "咪咕", "2409:8087"]
# 排除关键词
exclude = ["电信", "联通", "telecom", "unicom"]

def filter_m3u():
    try:
        response = requests.get(raw_url)
        lines = response.text.split('\n')
        
        output = ["#EXTM3U x-tvg-url=\"https://live.fanmingming.com/e.xml\""]
        
        for i in range(len(lines)):
            line = lines[i].strip()
            if line.startswith("#EXTINF"):
                # 检查标题是否包含关键词
                is_match = any(k.lower() in line.lower() for k in keywords)
                # 检查下一行的 URL 是否包含移动 IPv6 特征
                next_line = lines[i+1] if i+1 < len(lines) else ""
                is_ipv6_mobile = "2409:8087" in next_line
                
                # 排除非移动源
                is_bad = any(e.lower() in line.lower() for e in exclude)

                if (is_match or is_ipv6_mobile) and not is_bad:
                    output.append(line)
                    output.append(next_line)
        
        with open("mobile_plus.m3u", "w", encoding="utf-8") as f:
            f.write("\n".join(output))
        print("筛选完成！")
    except Exception as e:
        print(f"出错啦: {e}")

if __name__ == "__main__":
    filter_m3u()
