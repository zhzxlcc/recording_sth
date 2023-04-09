rs_txt = defaultdict(list) 
rs_list = []
with open(text_frames_scoring_file) as f:
    for line in f:
        j = json.loads(line.strip())
        video_name = download_object(url=j['video_url'])  # 返回包括路径的video name
        # print(video_name)
        img_names = capture_pic(video_name=video_name)
        if os.path.exists(video_name):
            os.remove(video_path)  # 删除视频
        else:
            print('no such file: %s' % video_name)
        rs_txt['score'] = j['score']
        # rs_txt["frames"] = img_names
        rs_txt["frames"] = [x.replace("a", "b") for x in img_names]
        rs_list.append(copy.deepcopy(rs_txt))
    # print(len(rs_list),rs_list)

with open(f'./frames_scoring_own.txt', 'w+') as f:
    for i in range(len(rs_list)):
       f.write(f'{json.dumps(rs_list[i], ensure_ascii=False)}\n') #按行写入，json写入单个字典

    
    
  
# 读取视频
def get_frame(video_path: pathlib or str, save_path: pathlib or str, target_time: float):
    # cover_path = "./target_frame.jpg"
    try:
        vc = cv2.VideoCapture(video_path)  # 读取
        video_width = int(vc.get(cv2.CAP_PROP_FRAME_WIDTH))  # 视频宽度
        video_height = int(vc.get(cv2.CAP_PROP_FRAME_HEIGHT))  # 视频高度
        vc.set(cv2.CAP_PROP_POS_MSEC, target_time)  # 设置读取位置，1000毫秒, cv2.CAP_PROP_POS_MSEC 表示视频捕获器对象的位置，单位为毫秒。
        # vc.set(cv2.CAP_PROP_POS_FRAMES, frame_index) 是 OpenCV 中的一个函数，用于设置视频读取的起始帧索引,frame_index参数指定了希望读取的视频帧的索引。


        rval, frame = vc.read()  # 读取当前帧，rval用于判断读取是否成功
        if rval:
            cv2.imwrite(save_path, frame)  # 保存
        else:
            print("读取失败")
    except Exception as e:
        print(f"获取视频帧失败: {e}")
