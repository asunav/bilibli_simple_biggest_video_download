import requests
import json
from tqdm import tqdm
import os
import traceback

SESSDATA = ''
video_save_path = ''

# 写json
# a={'SESSDATA':'1234',
#    'video_save_path': 'C:\\2333'
# }
# fp = open('bilibili_video_download_config.txt', 'w')
# json.dump(a, fp, indent=4)
# fp.close()
# exit()

# 读json
fp = open('bilibili_video_download_config.txt', 'r', encoding="utf-8")
try:
    config = json.load(fp)
    SESSDATA = config['SESSDATA']
    video_save_path = config['video_save_path']
except:
    traceback.print_exc()
    print('配置文件出错，请检查配置文件')
    exit()
print('配置文件加载成功')
    

mycookie = 'SESSDATA=' + SESSDATA

userAgentList = {'Windows':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36 Edg/99.0.1150.46',
                 'Android':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Mobile Safari/537.36 Edg/99.0.1150.46',
                 'Apple':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1'}

video_id2quality = {127:'8K 超高清', 126:'杜比视界', 125:'HDR 真彩色', 120:'4K 超清', 116:'1080P60 高帧率', 112:'1080P+ 高码率', 80:'1080P 高清', 74:'720P60 高帧率', 64:'720P 高清', 32:'480P 清晰', 16:'360P 流畅', 6:'240P 极速'}

def download_file(url, fname):
    resp = requests.get(url, headers={'User-Agent': userAgentList['Windows'], 'referer': 'https://www.bilibili.com/'}, stream=True)
    total = int(resp.headers.get('content-length', 0))

    filename_postfix = url.split('.')[-1]
    with open(fname, 'wb') as file, tqdm(
            desc=fname,
            total=total,
            unit='iB',
            unit_scale=True,
            unit_divisor=1024,
    ) as bar:
        for data in resp.iter_content(chunk_size=1024):
            size = file.write(data)
            bar.update(size)

    print('Download Complete')
    return

def vid2info(ab_vid:str):
    url = 'https://api.bilibili.com/x/web-interface/view?'
    if ab_vid.startswith('av'):
        url += 'aid=' + ab_vid.replace('av', '')
    elif ab_vid.startswith('BV'):
        url += 'bvid=' + ab_vid
    else:
        print('视频链接异常')
        exit()
    # print(url)
    response = requests.get(url, headers={'User-Agent': userAgentList['Windows'], 'referer': 'https://www.bilibili.com/'})
    r_json = json.loads(response.text)
    avid = str(r_json["data"]["aid"])
    BVid = r_json["data"]["bvid"]
    title = r_json["data"]["title"]
    cid = str(r_json["data"]["cid"])
    print('视频信息： ', title, ' avid: ', avid, ' BVid: ', BVid, ' cid: ', cid)
    return avid, BVid, title, cid


print("请输入视频av或BV号（分别以av或BV开头）：")
vid = input()
avid, BVid, title, cid = vid2info(vid)
# 请求高画质必须要https，用http只能得480P
# queryURL = 'https://api.bilibili.com/x/player/playurl?avid=' + avid + '&cid=' + cid + '&qn=0&fnval=80&fnver=0&fourk=1'
queryURL = 'https://api.bilibili.com/x/player/playurl?avid=' + avid + '&cid=' + cid + '&qn=126&fnval=' + str(16|2048|512|256) + '&fnver=0&fourk=1'   # 256会获取杜比音频, id 为 30250,与音频不在一个json数组里
response = requests.get(queryURL, headers={'User-Agent': userAgentList['Windows'], 'referer': 'https://www.bilibili.com/', 'cookie': mycookie})
data = json.loads(response.text)
print("所有画质及链接：", data)

video_url_list = data['data']['dash']['video']

biggest_video_id = ''
biggest_video_url = ''
for i, video_url in enumerate(video_url_list):
    biggest_video_id = video_url['id']
    biggest_video_url = video_url['baseUrl']
    break

print('最佳画质：' + video_id2quality[biggest_video_id])
print('链接：' + biggest_video_url)


# ***************************下载
if video_save_path[-1] != os.sep:
    video_save_path += os.sep
download_file(biggest_video_url, video_save_path + title + '_av' + avid + '.mp4')
