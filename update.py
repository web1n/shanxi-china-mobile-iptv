
cate_list = {
    "本地": [
        "山西卫视", "黄河卫视", "山西经济", "山西影视", "山西社会法治", "山西文体生活",
        "太原-1", "太原-2", "太原-3", "太原-4", "太原-5", "太原教育",
        "运城-1", "运城-2", "运城盐湖", "运城稷山",
        "晋中综合", "晋中公共", "晋中太古", "晋中左权",
        "阳泉新闻综合", "阳泉科教", "阳泉平定综合",
        "朔州-1", "朔州-2", "临汾永和", "长治潞州", "霍州频道", "山西焦煤", "绛县电视"
    ],
    "央视": [
        "CCTV-1", "CCTV-2", "CCTV-3", "CCTV-4", "CCTV-4 中文国际欧洲", "CCTV-4 中文国际美洲", "CCTV-5", "CCTV-5+",
        "CCTV-6", "CCTV-7", "CCTV-8", "CCTV-9", "CCTV-10", "CCTV-11", "CCTV-12", "CCTV-13", "CCTV-14", "CCTV-15",
        "CCTV-16", "CCTV-17",
        "CCTV-4K超高清", "CCTV-女性时尚", "CCTV-电视指南", "CCTV-央视文化精品", "CCTV-怀旧剧场", "CCTV-风云足球",
        "CCTV-兵器科技", "CCTV-风云音乐", "CCTV-风云剧场", "CCTV-第一剧场", "CCTV-央视台球", "CCTV-高尔夫网球",
        "CCTV-世界地理",
    ],
    "卫视": [
        "北京卫视", "天津卫视", "山东卫视", "山东教育卫视", "湖北卫视", "辽宁卫视", "重庆卫视", "贵州卫视", "江西卫视",
        "河南卫视", "安徽卫视", "大湾区卫视", "海南卫视", "西藏卫视", "兵团卫视", "三沙卫视", "新疆卫视", "湖南卫视",
        "东方卫视", "四川卫视", "黑龙江卫视", "广东卫视", "深圳卫视", "江苏卫视", "浙江卫视", "河北卫视", "吉林卫视",
        "厦门卫视", "广西卫视", "云南卫视", "青海卫视", "内蒙古卫视", "东南卫视", "宁夏卫视", "陕西卫视", "甘肃卫视",
        "农林卫视",
    ],
    "人文": [
        "北京纪实科教", "金鹰纪实", "纪实人文", "环球旅游", "国学频道", "百姓健康", "书画频道", "法治天地", "中华特产",
        "中国天气", "生态环境", "快乐垂钓", "四海钓鱼", "金色学堂", "乐游", "生活时尚", "都市剧场", "环球奇观",
        "车迷频道", "汽摩频道", "游戏风云", "魅力足球",
    ],
    "动漫": [
        "优漫卡通", "卡酷少儿", "金鹰卡通", "嘉佳卡通", "哈哈炫动", "动漫秀场", "优优宝贝",
    ],
    "财经": [
        "东方财经", "财富天下", "家庭理财", "证券服务",
    ],
    "购物": [
        "太原-伯乐购", "茶频道", "优购物","聚鲨环球精选", "家有购物"
    ],
    "其他": [
        "CGTN", "CGTN-记录", "CGTN-西班牙", "CGTN-法语", "CGTN-阿拉伯", "CGTN-俄语",
        "CETV-1", "CETV-2", "CETV-4", "CETV-早期教育",
        "中央新影-中学生", "中央新影-老故事", "中央新影-发现之旅",
    ]
}


def parse_txt(filename):
    tv_list = dict()

    for line in open(filename).readlines():
        line = line.strip()
        if line.startswith("#") or len(line.split(",")) != 2:
            continue

        tv_list[line.split(",")[0]] = line.split(",")[1]

    print("已从 {} 解析 {} 个频道".format(filename, len(tv_list)))
    return tv_list


def generate_m3u(from_file, dest_name, other=''):
    m3u_item_format = '#EXTINF:-1 {} tvg-name="{}" group-title="{}",{}\n{}\n'
    tv_list = parse_txt(from_file)

    dest = open(dest_name, "w")
    dest.write("#EXTM3U\n\n")

    for cate_name in cate_list.keys():
        for tv_name in cate_list[cate_name]:
            if tv_name not in tv_list:
                print("无此节目: {}".format(tv_name))
                continue

            url = tv_list.pop(tv_name)
            dest.write(m3u_item_format.format(other, tv_name, cate_name, tv_name, url))

    for tv_name in tv_list.keys():
        print(tv_name)
        url = tv_list.get(tv_name)
        dest.write(m3u_item_format.format(other, tv_name, "其他", tv_name, url))

    dest.close()
    print("已生成 {}".format(dest_name))


generate_m3u(
    "山西移动单播原版.txt",
    "山西移动单播.m3u",
    'catchup="append" catchup-source="starttime=${(b)timestamp}&endtime=${(e)timestamp}"'
)

generate_m3u(
    "山西移动组播原版.txt",
    "山西移动组播.m3u"
)
